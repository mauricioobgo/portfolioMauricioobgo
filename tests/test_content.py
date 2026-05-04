import json

import yaml

import portfolio_app.services.content as content_service
from portfolio_app.services.content import (
    build_frontend_content,
    load_portfolio_content,
    write_frontend_content,
)


def test_portfolio_content_loads_yaml_baseline() -> None:
    content = load_portfolio_content()

    assert content["profile"]["name"] == "Mauricio Obando"
    assert len(content["experience"]) >= 3
    assert len(content["certifications"]) >= 6
    assert any(
        certification["title"] == "AWS Certified Solutions Architect - Professional"
        for certification in content["certifications"]
    )
    assert any(
        certification["title"] == "AWS Certified Machine Learning - Specialty"
        for certification in content["certifications"]
    )


def test_build_frontend_content_merges_curated_and_generated(tmp_path, monkeypatch) -> None:
    data_dir = tmp_path / "data"
    generated_dir = tmp_path / "generated"
    data_dir.mkdir()
    generated_dir.mkdir()

    (data_dir / "profile.yaml").write_text(
        yaml.safe_dump(
            {
                "name": "Mauricio Obando",
                "title": "Cloud Data Engineer",
                "subtitle": "Building practical AI systems.",
                "about": "A concise about section.",
                "social_links": {
                    "github": "https://github.com/mauricioobgo",
                    "linkedin": "https://www.linkedin.com/in/mauricioobgo/",
                },
                "skills": ["Python", "Flutter"],
            }
        ),
        encoding="utf-8",
    )
    (data_dir / "projects.yaml").write_text(
        yaml.safe_dump(
            [
                {
                    "title": "Portfolio",
                    "summary": "Static portfolio site.",
                    "link": "https://github.com/mauricioobgo/portfolioMauricioobgo",
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
                    "issued": "Listed on LinkedIn",
                    "credential_url": (
                        "https://www.linkedin.com/in/mauricioobgo/details/certifications/"
                    ),
                    "credential_label": "View on LinkedIn",
                }
            ]
        ),
        encoding="utf-8",
    )
    (generated_dir / "profile.json").write_text(
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
    (generated_dir / "repos.json").write_text(
        json.dumps(
            [
                {
                    "name": "portfolioMauricioobgo",
                    "html_url": "https://github.com/mauricioobgo/portfolioMauricioobgo",
                    "description": "Portfolio source",
                    "updated_at": "2026-05-03T00:00:00Z",
                    "stargazers_count": 2,
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

    monkeypatch.setattr(content_service, "DATA_DIR", data_dir)
    monkeypatch.setattr(content_service, "GENERATED_DIR", generated_dir)

    payload = build_frontend_content()

    assert payload["metadata"]["frontend"] == "flutter"
    assert payload["profile"]["github_url"] == "https://github.com/mauricioobgo"
    assert payload["profile"]["avatar_url"] == "https://example.com/avatar.png"
    assert payload["profile"]["github_followers"] == 9
    assert payload["experience"][0]["company"] == "Globant"
    assert (
        payload["certifications"][0]["title"] == "AWS Certified Solutions Architect - Professional"
    )
    assert payload["github"]["repositories"][0]["name"] == "portfolioMauricioobgo"


def test_write_frontend_content_writes_json_asset(tmp_path, monkeypatch) -> None:
    payload = {"metadata": {"frontend": "flutter"}, "profile": {}}
    output_path = tmp_path / "frontend" / "assets" / "data" / "portfolio_content.json"

    monkeypatch.setattr(content_service, "build_frontend_content", lambda: payload)

    written_path = write_frontend_content(output_path=output_path)

    assert written_path == output_path
    assert json.loads(output_path.read_text(encoding="utf-8")) == payload
