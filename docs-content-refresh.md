# Content Refresh Cadence

Use this cadence for portfolio data freshness:

- **GitHub repositories/projects:** update **weekly** (every week).
- **LinkedIn-derived profile info:** update **monthly**.
- **Certifications:** update **monthly**.

## Operational checklist
1. Run `uv run python -m portfolio_app.scripts.sync_data --scope weekly` weekly to refresh GitHub-derived data.
2. Review `portfolio_app/data/featured_projects.yaml` weekly and adjust showcased projects.
3. Review `portfolio_app/data/profile.yaml` monthly for title, summary, links, and LinkedIn-related details.
4. Review `portfolio_app/data/certifications.yaml` monthly and add/remove certifications.
5. Run `uv run python -m portfolio_app.scripts.build_content` after curated content or generated JSON changes so the Flet app picks up the latest payload.
6. Re-run the GitHub Pages deploy workflow after content changes when you need an immediate publish outside the normal schedule.
7. Check `portfolio_app/generated/refresh_log.json` to verify which cadence scope ran.
