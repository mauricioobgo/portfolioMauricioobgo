from __future__ import annotations

import re
from datetime import datetime, timezone
from io import BytesIO
from typing import Any

import httpx
from pypdf import PdfReader


DEFAULT_TIMEOUT = 60
DRIVE_DOWNLOAD_TEMPLATE = "https://drive.google.com/uc?export=download&id={file_id}"
DRIVE_FILE_ID_PATTERN = re.compile(r"/d/([a-zA-Z0-9_-]+)")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def extract_drive_file_id(url: str | None) -> str | None:
    if not url:
        return None

    match = DRIVE_FILE_ID_PATTERN.search(url)
    if match:
        return match.group(1)

    if "id=" in url:
        candidate = url.split("id=", maxsplit=1)[1].split("&", maxsplit=1)[0]
        return candidate or None

    return None


def resolve_resume_pdf_url(profile: dict[str, Any]) -> str:
    explicit_pdf_url = str(profile.get("resume_pdf_url") or "").strip()
    if explicit_pdf_url:
        return explicit_pdf_url

    resume_link = str(profile.get("resume_link") or "").strip()
    file_id = extract_drive_file_id(resume_link)
    if not file_id:
        raise ValueError("profile.yaml is missing a usable resume_pdf_url or Google Drive file id.")
    return DRIVE_DOWNLOAD_TEMPLATE.format(file_id=file_id)


def download_resume_pdf(
    pdf_url: str,
    *,
    request_get: Any = httpx.get,
) -> bytes:
    response = request_get(pdf_url, follow_redirects=True, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    pdf_bytes = response.content
    if not pdf_bytes.startswith(b"%PDF"):
        raise ValueError("Resume download did not return a PDF payload.")
    return pdf_bytes


def extract_resume_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    lines: list[str] = []
    for page in reader.pages:
        page_text = (page.extract_text() or "").replace("\x00", " ")
        for raw_line in page_text.splitlines():
            normalized = " ".join(raw_line.split())
            if normalized:
                lines.append(normalized)
    return "\n".join(lines)


def _candidate_terms(
    profile: dict[str, Any],
    experience: list[dict[str, Any]],
    certifications: list[dict[str, Any]],
    projects: list[dict[str, Any]],
) -> list[str]:
    candidates = [
        *profile.get("skills", []),
        *(item.get("company", "") for item in experience[:3]),
        *(item.get("role", "") for item in experience[:3]),
        *(item.get("title", "") or item.get("name", "") for item in certifications),
        *(skill for item in certifications for skill in item.get("skills", [])),
        *(item.get("name", "") for item in projects),
        *(skill for item in projects for skill in item.get("tech_stack", item.get("tags", []))),
    ]
    return [candidate for candidate in candidates if candidate]


def derive_resume_keywords(
    resume_text: str,
    profile: dict[str, Any],
    experience: list[dict[str, Any]],
    certifications: list[dict[str, Any]],
    projects: list[dict[str, Any]],
) -> list[str]:
    lower_resume = resume_text.lower()
    matches = {
        candidate
        for candidate in _candidate_terms(profile, experience, certifications, projects)
        if candidate.lower() in lower_resume
    }
    return sorted(matches, key=str.lower)


def build_resume_snapshot(
    *,
    profile: dict[str, Any],
    experience: list[dict[str, Any]],
    certifications: list[dict[str, Any]],
    projects: list[dict[str, Any]],
    pdf_url: str,
    resume_text: str,
) -> dict[str, Any]:
    keywords = derive_resume_keywords(
        resume_text,
        profile=profile,
        experience=experience,
        certifications=certifications,
        projects=projects,
    )
    lines = [line for line in resume_text.splitlines() if line]
    return {
        "source_url": pdf_url,
        "fetched_at": utc_now_iso(),
        "line_count": len(lines),
        "character_count": len(resume_text),
        "excerpt": "\n".join(lines[:20]),
        "keywords": keywords[:24],
        "text": resume_text,
    }


def build_resume_drift_report(
    *,
    profile: dict[str, Any],
    experience: list[dict[str, Any]],
    certifications: list[dict[str, Any]],
    resume_text: str,
) -> dict[str, Any]:
    lowered_resume = resume_text.lower()
    checks = [
        ("profile_name", profile.get("name", "")),
        ("headline", profile.get("title", "")),
        ("current_company", experience[0].get("company", "") if experience else ""),
        (
            "featured_certification",
            next(
                (
                    item.get("title") or item.get("name")
                    for item in certifications
                    if item.get("featured")
                ),
                "",
            ),
        ),
    ]

    matches: list[str] = []
    missing: list[str] = []
    for label, value in checks:
        normalized = str(value or "").strip()
        if not normalized:
            continue
        if normalized.lower() in lowered_resume:
            matches.append(label)
        else:
            missing.append(label)

    observations = []
    if missing:
        observations.append(
            "Resume text does not fully match every curated signal; review the profile YAML and source PDF."
        )
    else:
        observations.append(
            "Curated profile headline, current company, and featured certification cues are visible."
        )

    return {
        "generated_at": utc_now_iso(),
        "status": "review" if missing else "aligned",
        "matches": matches,
        "missing_signals": missing,
        "observations": observations,
    }


def build_ai_context(
    *,
    profile: dict[str, Any],
    experience: list[dict[str, Any]],
    certifications: list[dict[str, Any]],
    projects: list[dict[str, Any]],
    github_profile: dict[str, Any],
    github_repositories: list[dict[str, Any]],
    resume_snapshot: dict[str, Any],
) -> dict[str, Any]:
    featured_certifications = [
        {
            "title": item.get("title") or item.get("name"),
            "issuer": item.get("issuer"),
            "skills": item.get("skills", []),
        }
        for item in certifications
        if item.get("featured")
    ]
    featured_projects = [
        {
            "name": item.get("name") or item.get("title"),
            "summary": item.get("summary"),
            "tech_stack": item.get("tech_stack", item.get("tags", [])),
            "highlights": item.get("highlights", []),
        }
        for item in projects[:5]
    ]
    return {
        "generated_at": utc_now_iso(),
        "assistant_mode": "cli_only",
        "profile": {
            "name": profile.get("name"),
            "title": profile.get("title"),
            "subtitle": profile.get("subtitle"),
            "about": profile.get("about"),
            "email": profile.get("email"),
            "location": profile.get("location"),
        },
        "experience": experience[:3],
        "featured_certifications": featured_certifications,
        "featured_projects": featured_projects,
        "github": {
            "profile": {
                "login": github_profile.get("login"),
                "followers": github_profile.get("followers"),
                "public_repos": github_profile.get("public_repos"),
            },
            "repositories": github_repositories[:6],
        },
        "resume": {
            "source_url": resume_snapshot.get("source_url"),
            "fetched_at": resume_snapshot.get("fetched_at"),
            "keywords": resume_snapshot.get("keywords", []),
            "excerpt": resume_snapshot.get("excerpt", ""),
            "text": resume_snapshot.get("text", ""),
        },
        "system_prompt": (
            "You are Mauricio's CV assistant. Answer only from the provided portfolio, resume, "
            "GitHub, and certification context. If a fact is missing or uncertain, say so plainly."
        ),
    }
