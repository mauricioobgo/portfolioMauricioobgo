from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import yaml


CERTIFICATIONS_PATH = Path(__file__).resolve().parents[1] / "data" / "certifications.yaml"


def load_certifications(path: Path = CERTIFICATIONS_PATH) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("certifications.yaml must contain a top-level list.")
    return data


def _is_valid_linkedin_url(url: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme in {"http", "https"}
        and parsed.netloc.endswith("linkedin.com")
        and "/details/certifications/" in parsed.path
    )


def validate_certifications(certifications: list[dict]) -> list[str]:
    errors: list[str] = []

    for index, certification in enumerate(certifications, start=1):
        label = certification.get("title") or certification.get("name") or f"entry #{index}"
        title = certification.get("title") or certification.get("name")
        required = {
            "issuer": certification.get("issuer"),
            "status": certification.get("status"),
        }

        if not title:
            errors.append(f"{label}: missing title/name")

        for field_name, field_value in required.items():
            if not str(field_value or "").strip():
                errors.append(f"{label}: missing {field_name}")

        if certification.get("featured"):
            featured_required = {
                "level": certification.get("level"),
                "category": certification.get("category"),
                "linkedin_url": certification.get("linkedin_url")
                or certification.get("credential_url"),
            }
            for field_name, field_value in featured_required.items():
                if not str(field_value or "").strip():
                    errors.append(f"{label}: featured certification missing {field_name}")

            linkedin_url = featured_required["linkedin_url"]
            if linkedin_url and not _is_valid_linkedin_url(str(linkedin_url)):
                errors.append(
                    f"{label}: featured certification requires a LinkedIn certifications URL"
                )

    return errors


def main() -> None:
    errors = validate_certifications(load_certifications())
    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
