from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


APP_DIR = Path(__file__).resolve().parents[1]
LINKEDIN_CERTIFICATIONS_URL = "https://www.linkedin.com/in/mauricioobgo/details/certifications/"

ENGINEERING_FOCUS = [
    {
        "name": "Backend Engineering",
        "eyebrow": "API / SYSTEMS",
        "description": (
            "Production-minded Python services, FastAPI APIs, async workflows, testing, "
            "and architecture that stays maintainable under delivery pressure."
        ),
        "skills": [
            "Python 3.14",
            "FastAPI",
            "APIs",
            "PostgreSQL",
            "Async systems",
            "Testing",
            "Clean architecture",
        ],
    },
    {
        "name": "Data Engineering",
        "eyebrow": "DATA / ANALYTICS",
        "description": (
            "Cloud-scale ingestion, transformation, warehouse modeling, and delivery "
            "workflows built for analytics reliability and operational clarity."
        ),
        "skills": [
            "Redshift",
            "dbt",
            "Spark",
            "Glue",
            "Athena",
            "Airflow",
            "Data quality",
        ],
    },
    {
        "name": "LLM Engineering",
        "eyebrow": "AI / ORCHESTRATION",
        "description": (
            "Applied LLM systems that combine RAG, evaluation, tool calling, "
            "structured outputs, and production feedback loops."
        ),
        "skills": [
            "RAG",
            "Agents",
            "Vector databases",
            "Evaluation",
            "Prompt pipelines",
            "Tool calling",
            "Structured outputs",
        ],
    },
    {
        "name": "Cloud & DevOps",
        "eyebrow": "OPS / DELIVERY",
        "description": (
            "AWS-focused delivery with CI/CD, observability, container workflows, "
            "cost awareness, and cloud platform execution."
        ),
        "skills": [
            "AWS",
            "Docker",
            "CI/CD",
            "Observability",
            "Infrastructure as Code",
            "FinOps",
            "GitHub Actions",
        ],
    },
]

TECH_STACK = [
    {
        "name": "Application",
        "items": [
            "Python 3.14",
            "FastAPI",
            "SQLAlchemy",
            "Alembic",
            "Pytest",
            "AsyncIO",
        ],
    },
    {
        "name": "Data",
        "items": [
            "Redshift",
            "dbt",
            "Athena",
            "Glue",
            "Spark",
            "PostgreSQL",
        ],
    },
    {
        "name": "AI",
        "items": [
            "LLMs",
            "RAG",
            "Prompt pipelines",
            "Structured outputs",
            "Evaluation",
            "Vector search",
        ],
    },
    {
        "name": "Cloud",
        "items": [
            "AWS",
            "Docker",
            "GitHub Actions",
            "CloudWatch",
            "FinOps",
            "Observability",
        ],
    },
]

DEFAULT_ASSISTANT_PROMPTS = [
    "Summarize Mauricio for a backend platform engineering role.",
    "Which AWS and data engineering strengths stand out the most?",
    "How does Mauricio apply AI and LLM systems in practical delivery work?",
]


def _resolve_app_dir() -> Path:
    if (APP_DIR / "data").exists():
        return APP_DIR

    workspace_app_dir = Path.cwd() / "portfolio_app"
    if (workspace_app_dir / "data").exists():
        return workspace_app_dir

    return APP_DIR


DATA_DIR = _resolve_app_dir() / "data"
GENERATED_DIR = _resolve_app_dir() / "generated"
FRONTEND_CONTENT_PATH = APP_DIR.parent / "src" / "assets" / "portfolio_content.json"


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _int_value(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _trim_generated_profile(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "login": profile.get("login"),
        "name": profile.get("name"),
        "company": profile.get("company"),
        "location": profile.get("location"),
        "bio": profile.get("bio"),
        "avatar_url": profile.get("avatar_url"),
        "html_url": profile.get("html_url"),
        "followers": _int_value(profile.get("followers")),
        "public_repos": _int_value(profile.get("public_repos")),
        "updated_at": profile.get("updated_at"),
    }


def _trim_generated_repo(repo: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": repo.get("name"),
        "full_name": repo.get("full_name"),
        "html_url": repo.get("html_url"),
        "description": repo.get("description"),
        "homepage": repo.get("homepage"),
        "language": repo.get("language"),
        "topics": repo.get("topics", []),
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "stargazers_count": _int_value(repo.get("stargazers_count")),
        "forks_count": _int_value(repo.get("forks_count")),
        "open_issues_count": _int_value(repo.get("open_issues_count")),
        "archived": repo.get("archived", False),
    }


def _load_generated_profile() -> dict[str, Any]:
    return (
        _load_json(GENERATED_DIR / "github_profile.json")
        or _load_json(GENERATED_DIR / "profile.json")
        or {}
    )


def _load_generated_repositories() -> list[dict[str, Any]]:
    return (
        _load_json(GENERATED_DIR / "github_repos.json")
        or _load_json(GENERATED_DIR / "repos.json")
        or []
    )


def _load_resume_snapshot() -> dict[str, Any]:
    return _load_json(GENERATED_DIR / "resume_snapshot.json") or {}


def _load_ai_context() -> dict[str, Any]:
    return _load_json(GENERATED_DIR / "ai_context.json") or {}


def _load_resume_drift() -> dict[str, Any]:
    return _load_json(GENERATED_DIR / "resume_drift.json") or {}


def _normalize_certification(certification: dict[str, Any]) -> dict[str, Any]:
    title = certification.get("title") or certification.get("name")
    credential_url = certification.get("credential_url") or certification.get("linkedin_url")
    return {
        "title": title,
        "issuer": certification.get("issuer"),
        "level": certification.get("level"),
        "category": certification.get("category"),
        "status": certification.get("status", "Active"),
        "featured": bool(certification.get("featured", False)),
        "issued": certification.get("issued"),
        "credential_id": certification.get("credential_id"),
        "credential_url": credential_url or LINKEDIN_CERTIFICATIONS_URL,
        "credential_label": certification.get("credential_label", "View on LinkedIn"),
        "skills": certification.get("skills", []),
    }


def _normalize_project(project: dict[str, Any]) -> dict[str, Any]:
    tech_stack = project.get("tech_stack") or project.get("tags") or []
    return {
        "name": project.get("name") or project.get("title"),
        "category": project.get("category", "Platform Engineering"),
        "summary": project.get("summary"),
        "problem": project.get("problem"),
        "solution": project.get("solution"),
        "architecture": project.get("architecture") or project.get("impact"),
        "tech_stack": tech_stack,
        "highlights": project.get("highlights", []),
        "github_url": project.get("github_url") or project.get("link"),
        "demo_url": project.get("demo_url"),
        "status": project.get("status", "Case study"),
        "filters": project.get("filters") or [project.get("category", "Platform")],
    }


def _normalize_experience(experience: dict[str, Any]) -> dict[str, Any]:
    return {
        "role": experience.get("role"),
        "company": experience.get("company"),
        "date": experience.get("date"),
        "location": experience.get("location"),
        "description": experience.get("description"),
        "highlights": experience.get("highlights", []),
        "company_url": experience.get("company_url"),
        "reference_url": experience.get("reference_url"),
        "reference_label": experience.get("reference_label", "Source"),
    }


def _normalize_profile(
    profile: dict[str, Any], generated_profile: dict[str, Any]
) -> dict[str, Any]:
    social_links = profile.get("social_links", {})
    return {
        **profile,
        "github_url": generated_profile.get("html_url") or social_links.get("github"),
        "linkedin_certifications_url": LINKEDIN_CERTIFICATIONS_URL,
        "avatar_url": generated_profile.get("avatar_url"),
        "location": generated_profile.get("location") or profile.get("location"),
        "company": generated_profile.get("company") or profile.get("company"),
        "bio": generated_profile.get("bio") or profile.get("bio") or profile.get("about"),
        "github_followers": _int_value(generated_profile.get("followers")),
        "github_public_repos": _int_value(generated_profile.get("public_repos")),
        "github_updated_at": generated_profile.get("updated_at"),
        "assistant_prompts": profile.get("assistant_prompts") or DEFAULT_ASSISTANT_PROMPTS,
    }


def _build_github_summary(repositories: list[dict[str, Any]]) -> dict[str, Any]:
    languages: dict[str, int] = {}
    for repo in repositories:
        language = repo.get("language")
        if language:
            languages[language] = languages.get(language, 0) + 1

    language_breakdown = [
        {"name": name, "count": count}
        for name, count in sorted(languages.items(), key=lambda item: (-item[1], item[0]))
    ]
    return {
        "language_breakdown": language_breakdown,
        "top_starred": max(
            (_int_value(repo.get("stargazers_count")) for repo in repositories), default=0
        ),
        "repo_count": len(repositories),
    }


def load_portfolio_content() -> dict[str, Any]:
    projects_path = DATA_DIR / "featured_projects.yaml"
    if not projects_path.exists():
        projects_path = DATA_DIR / "projects.yaml"

    return {
        "profile": _load_yaml(DATA_DIR / "profile.yaml"),
        "featured_projects": _load_yaml(projects_path),
        "experience": _load_yaml(DATA_DIR / "experience.yaml"),
        "certifications": _load_yaml(DATA_DIR / "certifications.yaml"),
        "generated_profile": _load_generated_profile(),
        "generated_repos": _load_generated_repositories(),
        "resume_snapshot": _load_resume_snapshot(),
        "ai_context": _load_ai_context(),
        "resume_drift": _load_resume_drift(),
        "refresh_log": _load_json(GENERATED_DIR / "refresh_log.json") or {},
    }


def build_portfolio_content() -> dict[str, Any]:
    content = load_portfolio_content()
    generated_profile = content["generated_profile"]
    repositories = [_trim_generated_repo(repo) for repo in content["generated_repos"]]
    profile = _normalize_profile(content["profile"], generated_profile)
    certifications = [_normalize_certification(cert) for cert in content["certifications"]]
    featured_projects = [_normalize_project(project) for project in content["featured_projects"]]
    experience = [_normalize_experience(item) for item in content["experience"]]
    github_summary = _build_github_summary(repositories)
    resume_snapshot = content["resume_snapshot"]
    ai_context = content["ai_context"]
    resume_drift = content["resume_drift"]

    return {
        "metadata": {
            "generated_at": _utc_now_iso(),
            "frontend": "flet",
            "runtime": "static_web",
            "deployment_url": "https://mauricioobgo.github.io/portfolioMauricioobgo/",
            "refresh_log": content["refresh_log"],
            "assistant_mode": "cli",
            "resume_drift": resume_drift,
        },
        "profile": profile,
        "hero_commands": profile.get("hero_commands")
        or [
            "$ whoami",
            "mauricio_obando",
            "",
            "$ current_focus",
            "backend_engineering | data_platforms | cloud_architecture | llm_systems",
            "",
            "$ stack --top",
            "python3.14 fastapi aws redshift dbt llms spark",
        ],
        "engineering_focus": ENGINEERING_FOCUS,
        "technical_stack": TECH_STACK,
        "experience": experience,
        "featured_projects": featured_projects,
        "certifications": certifications,
        "resume": {
            "source_url": profile.get("resume_link"),
            "source_pdf_url": profile.get("resume_pdf_url"),
            "synced_at": resume_snapshot.get("fetched_at"),
            "excerpt": resume_snapshot.get("excerpt", ""),
            "keywords": resume_snapshot.get("keywords", []),
            "line_count": resume_snapshot.get("line_count", 0),
        },
        "assistant": {
            "status": "CLI mode",
            "description": (
                "This GitHub Pages site stays static. The Mauricio AI assistant is prepared as a local/admin CLI "
                "using generated portfolio context plus the public resume snapshot."
            ),
            "prompts": profile.get("assistant_prompts") or DEFAULT_ASSISTANT_PROMPTS,
            "cli_command": (
                "uv run python -m portfolio_app.scripts.chat_cv --question "
                '"What production-grade systems does Mauricio build?"'
            ),
            "context_files": [
                "portfolio_app/generated/ai_context.json",
                "portfolio_app/generated/resume_snapshot.json",
                "src/assets/portfolio_content.json",
            ],
            "resume_synced_at": resume_snapshot.get("fetched_at"),
            "summary": ai_context.get("profile", {}).get("about") or profile.get("about"),
        },
        "github": {
            "profile": _trim_generated_profile(generated_profile),
            "repositories": repositories,
            "summary": github_summary,
        },
    }


def build_frontend_content() -> dict[str, Any]:
    return build_portfolio_content()


def write_frontend_content(output_path: Path = FRONTEND_CONTENT_PATH) -> Path:
    payload = build_portfolio_content()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path
