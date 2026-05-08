# Content Refresh Cadence

Use this cadence for portfolio data freshness:

- **GitHub repositories/projects:** update **weekly** (every week).
- **LinkedIn-derived profile info:** update **monthly**.
- **Certifications:** update **monthly**.
- **Public Drive resume snapshot / AI context:** update **monthly**.

## Operational checklist
1. Run `uv run python -m portfolio_app.scripts.sync_data --scope weekly` weekly to refresh GitHub-derived data.
2. Review `portfolio_app/data/featured_projects.yaml` weekly and adjust showcased projects.
3. Review `portfolio_app/data/profile.yaml` monthly for title, summary, links, and LinkedIn-related details.
4. Run `uv run python -m portfolio_app.scripts.sync_resume` monthly to refresh the public CV snapshot, drift report, and AI context bundle.
5. Review `portfolio_app/data/certifications.yaml` monthly and add/remove certifications.
6. Run `uv run python -m portfolio_app.scripts.build_content` after curated content or generated JSON changes so the Flet app picks up the latest payload.
7. Re-run the GitHub Pages deploy workflow after content changes when you need an immediate publish outside the normal schedule.
8. Check `portfolio_app/generated/refresh_log.json` to verify which cadence scope ran.
