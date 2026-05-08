from portfolio_app.scripts.validate_links import validate_certifications


def test_validate_links_accepts_featured_certifications_with_linkedin_urls() -> None:
    errors = validate_certifications(
        [
            {
                "title": "AWS Certified Solutions Architect - Professional",
                "issuer": "Amazon Web Services",
                "level": "Professional",
                "category": "Cloud Architecture",
                "status": "Active",
                "featured": True,
                "linkedin_url": "https://www.linkedin.com/in/mauricioobgo/details/certifications/",
            }
        ]
    )

    assert errors == []


def test_validate_links_rejects_featured_certifications_without_linkedin_urls() -> None:
    errors = validate_certifications(
        [
            {
                "title": "AWS Certified Machine Learning - Specialty",
                "issuer": "Amazon Web Services",
                "level": "Specialty",
                "category": "Machine Learning",
                "status": "Active",
                "featured": True,
                "linkedin_url": "",
            }
        ]
    )

    assert errors
    assert "missing linkedin_url" in errors[0]
