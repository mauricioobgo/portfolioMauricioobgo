from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable

from portfolio_app.services.content import GENERATED_DIR, load_portfolio_content
from portfolio_app.services.resume import (
    build_ai_context,
    build_resume_drift_report,
    build_resume_snapshot,
    download_resume_pdf,
    extract_resume_text,
    resolve_resume_pdf_url,
)


def run_sync(
    *,
    out_dir: Path | None = None,
    load_content_fn: Callable[[], dict[str, Any]] = load_portfolio_content,
    download_resume_pdf_fn: Callable[[str], bytes] = download_resume_pdf,
    extract_resume_text_fn: Callable[[bytes], str] = extract_resume_text,
) -> dict[str, Path]:
    out_dir = out_dir or GENERATED_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    content = load_content_fn()
    profile = content["profile"]
    experience = content["experience"]
    certifications = content["certifications"]
    projects = content["featured_projects"]
    generated_profile = content.get("generated_profile", {})
    generated_repos = content.get("generated_repos", [])

    pdf_url = resolve_resume_pdf_url(profile)
    pdf_bytes = download_resume_pdf_fn(pdf_url)
    resume_text = extract_resume_text_fn(pdf_bytes)

    snapshot = build_resume_snapshot(
        profile=profile,
        experience=experience,
        certifications=certifications,
        projects=projects,
        pdf_url=pdf_url,
        resume_text=resume_text,
    )
    drift_report = build_resume_drift_report(
        profile=profile,
        experience=experience,
        certifications=certifications,
        resume_text=resume_text,
    )
    ai_context = build_ai_context(
        profile=profile,
        experience=experience,
        certifications=certifications,
        projects=projects,
        github_profile=generated_profile,
        github_repositories=generated_repos,
        resume_snapshot=snapshot,
    )

    resume_path = out_dir / "resume_snapshot.json"
    drift_path = out_dir / "resume_drift.json"
    ai_context_path = out_dir / "ai_context.json"
    resume_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    drift_path.write_text(json.dumps(drift_report, indent=2), encoding="utf-8")
    ai_context_path.write_text(json.dumps(ai_context, indent=2), encoding="utf-8")

    return {
        "resume_path": resume_path,
        "drift_path": drift_path,
        "ai_context_path": ai_context_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download the public resume PDF, extract text, and write AI context artifacts."
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=GENERATED_DIR,
        help="Directory where generated resume artifacts will be written.",
    )
    args = parser.parse_args()
    result = run_sync(out_dir=args.out_dir)
    for label, path in result.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
