import json

import yaml

import portfolio_app.services.content as content_service
from portfolio_app.services.content import (
    build_portfolio_content,
    load_portfolio_content,
    write_frontend_content,
)


def test_portfolio_content_loads_yaml_baseline() -> None:
    content = load_portfolio_content()

    assert content["profile"]["name"] == "Mauricio Obando"
    assert len(content["experience"]) >= 3
    assert len(content["certifications"]) >= 6
    assert len(content["featured_projects"]) >= 5


def test_build_content_merges_curated_and_generated(tmp_path, monkeypatch) -> None:
    data_dir = tmp_path / "data"
    generated_dir = tmp_path / "generated"
    data_dir.mkdir()
    generated_dir.mkdir()

    (data_dir / "profile.yaml").write_text(
        yaml.safe_dump(
            {
                "name": "Mauricio Obando",
                "title": "Backend, Data, Cloud, and AI Engineer",
                "subtitle": "Building production-grade platforms.",
                "about": "A concise about section.",
                "social_links": {
                    "github": "https://github.com/mauricioobgo",
                    "linkedin": "https://www.linkedin.com/in/mauricioobgo/",
                },
                "skills": ["Python 3.14", "Flet"],
            }
        ),
        encoding="utf-8",
    )
    (data_dir / "featured_projects.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "name": "AI DataOps Platform",
                    "summary": "Static portfolio site.",
                    "problem": "Data access is fragmented.",
                    "solution": "Unify ingestion and retrieval.",
                    "tech_stack": ["FastAPI", "AWS"],
                    "highlights": ["RAG assistant"],
                }
            ]
        ),
        encoding="utf-8",
    )
    (data_dir / "experience.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "role": "Senior Data Engineer",
                    "company": "Globant",
                    "date": "2025 - Present",
                    "location": "Bogota, Colombia",
                    "description": "Leading AI delivery programs.",
                    "highlights": ["Production AI pilots"],
                }
            ]
        ),
        encoding="utf-8",
    )
    (data_dir / "certifications.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "title": "AWS Certified Solutions Architect - Professional",
                    "issuer": "Amazon Web Services",
                    "level": "Professional",
                    "category": "Cloud Architecture",
                    "status": "Active",
                    "featured": True,
                    "linkedin_url": (
                        "https://www.linkedin.com/in/mauricioobgo/details/certifications/"
                    ),
                    "credential_label": "View on LinkedIn",
                }
            ]
        ),
        encoding="utf-8",
    )
    (generated_dir / "github_profile.json").write_text(
        json.dumps(
            {
                "login": "mauricioobgo",
                "company": "Globant",
                "location": "Bogota, Colombia",
                "bio": "Generated profile bio",
                "avatar_url": "https://example.com/avatar.png",
                "html_url": "https://github.com/mauricioobgo",
                "followers": 9,
                "public_repos": 42,
                "updated_at": "2026-05-03T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    (generated_dir / "github_repos.json").write_text(
        json.dumps(
            [
                {
                    "name": "portfolioMauricioobgo",
                    "html_url": "https://github.com/mauricioobgo/portfolioMauricioobgo",
                    "description": "Portfolio source",
                    "updated_at": "2026-05-03T00:00:00Z",
                    "stargazers_count": 2,
                    "topics": ["portfolio"],
                }
            ]
        ),
        encoding="utf-8",
    )
    (generated_dir / "refresh_log.json").write_text(
        json.dumps(
            {
                "scope": "all",
                "executed_at": "2026-05-03T00:00:00+00:00",
                "updates": ["github_repositories_weekly", "profile_monthly_review"],
            }
        ),
        encoding="utf-8",
    )
    (generated_dir / "resume_snapshot.json").write_text(
        json.dumps(
            {
                "source_url": "https://drive.google.com/uc?export=download&id=demo",
                "fetched_at": "2026-05-08T00:00:00+00:00",
                "excerpt": "Mauricio resume excerpt",
                "keywords": ["Python 3.14", "AWS", "FastAPI"],
                "line_count": 12,
            }
        ),
        encoding="utf-8",
    )
    (generated_dir / "ai_context.json").write_text(
        json.dumps(
            {
                "profile": {"about": "Context summary from resume and portfolio."},
                "system_prompt": "Use generated context.",
            }
        ),
        encoding="utf-8",
    )
    (generated_dir / "resume_drift.json").write_text(
        json.dumps({"status": "aligned", "matches": ["profile_name"], "missing_signals": []}),
        encoding="utf-8",
    )

    monkeypatch.setattr(content_service, "DATA_DIR", data_dir)
    monkeypatch.setattr(content_service, "GENERATED_DIR", generated_dir)

    payload = build_portfolio_content()

    assert set(payload) >= {
        "metadata",
        "profile",
        "hero_commands",
        "engineering_focus",
        "technical_stack",
        "experience",
        "featured_projects",
        "certifications",
        "resume",
        "assistant",
        "github",
    }
    assert payload["metadata"]["frontend"] == "flet"
    assert payload["profile"]["github_url"] == "https://github.com/mauricioobgo"
    assert payload["profile"]["avatar_url"] == "https://example.com/avatar.png"
    assert payload["profile"]["github_followers"] == 9
    assert payload["experience"][0]["company"] == "Globant"
    assert (
        payload["certifications"][0]["title"] == "AWS Certified Solutions Architect - Professional"
    )
    assert payload["resume"]["line_count"] == 12
    assert payload["assistant"]["status"] == "CLI mode"
    assert payload["featured_projects"][0]["name"] == "AI DataOps Platform"
    assert payload["github"]["repositories"][0]["name"] == "portfolioMauricioobgo"


def test_write_frontend_content_writes_json_asset(tmp_path, monkeypatch) -> None:
    payload = {"metadata": {"frontend": "flet"}, "profile": {}}
    output_path = tmp_path / "src" / "assets" / "portfolio_content.json"

    monkeypatch.setattr(content_service, "build_portfolio_content", lambda: payload)

    written_path = write_frontend_content(output_path=output_path)

    assert written_path == output_path
    assert json.loads(output_path.read_text(encoding="utf-8")) == payload
