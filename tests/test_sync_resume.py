import json

from portfolio_app.scripts.sync_resume import run_sync
from portfolio_app.services.resume import (
    build_ai_context,
    build_resume_snapshot,
    resolve_resume_pdf_url,
)


def _sample_content() -> dict:
    return {
        "profile": {
            "name": "Mauricio Obando",
            "title": "Backend, Data, Cloud, and AI Engineer",
            "subtitle": "Production-grade systems.",
            "about": "Builds platforms.",
            "email": "mauricioobgo@gmail.com",
            "location": "Bogota, Colombia",
            "resume_pdf_url": "https://drive.google.com/uc?export=download&id=demo",
        },
        "experience": [
            {
                "role": "Technical Account Manager",
                "company": "Amazon Web Services",
                "date": "2024 - Present",
                "location": "Colombia",
                "description": "Cloud and Redshift delivery.",
                "highlights": ["AWS architecture", "FinOps"],
            }
        ],
        "certifications": [
            {
                "title": "AWS Certified Solutions Architect - Professional",
                "issuer": "Amazon Web Services",
                "featured": True,
                "skills": ["AWS", "Architecture"],
            }
        ],
        "featured_projects": [
            {
                "name": "AI DataOps Platform",
                "summary": "Platform case study",
                "tech_stack": ["FastAPI", "AWS"],
                "highlights": ["RAG assistant"],
            }
        ],
        "generated_profile": {"login": "mauricioobgo", "followers": 12, "public_repos": 42},
        "generated_repos": [
            {
                "name": "portfolioMauricioobgo",
                "html_url": "https://github.com/mauricioobgo/portfolioMauricioobgo",
            }
        ],
    }


def test_resolve_resume_pdf_url_uses_explicit_machine_readable_url() -> None:
    url = resolve_resume_pdf_url(
        {
            "resume_pdf_url": "https://drive.google.com/uc?export=download&id=demo",
            "resume_link": "https://drive.google.com/file/d/ignored/view",
        }
    )

    assert url == "https://drive.google.com/uc?export=download&id=demo"


def test_sync_resume_writes_resume_and_ai_context_artifacts(tmp_path) -> None:
    result = run_sync(
        out_dir=tmp_path,
        load_content_fn=_sample_content,
        download_resume_pdf_fn=lambda _url: b"%PDF-1.7\n",
        extract_resume_text_fn=(
            lambda _bytes: (
                "Mauricio Obando\nAmazon Web Services\nAWS Certified Solutions Architect - Professional\nFastAPI AWS"
            )
        ),
    )

    snapshot = json.loads(result["resume_path"].read_text(encoding="utf-8"))
    ai_context = json.loads(result["ai_context_path"].read_text(encoding="utf-8"))
    drift = json.loads(result["drift_path"].read_text(encoding="utf-8"))

    assert snapshot["source_url"].startswith("https://drive.google.com/")
    assert "AWS" in snapshot["keywords"]
    assert ai_context["assistant_mode"] == "cli_only"
    assert ai_context["featured_projects"][0]["name"] == "AI DataOps Platform"
    assert drift["status"] in {"aligned", "review"}


def test_build_helpers_keep_required_top_level_keys() -> None:
    content = _sample_content()
    snapshot = build_resume_snapshot(
        profile=content["profile"],
        experience=content["experience"],
        certifications=content["certifications"],
        projects=content["featured_projects"],
        pdf_url=content["profile"]["resume_pdf_url"],
        resume_text="Mauricio Obando\nAWS\nFastAPI",
    )
    context = build_ai_context(
        profile=content["profile"],
        experience=content["experience"],
        certifications=content["certifications"],
        projects=content["featured_projects"],
        github_profile=content["generated_profile"],
        github_repositories=content["generated_repos"],
        resume_snapshot=snapshot,
    )

    assert set(context) >= {
        "generated_at",
        "assistant_mode",
        "profile",
        "experience",
        "featured_certifications",
        "featured_projects",
        "github",
        "resume",
        "system_prompt",
    }
