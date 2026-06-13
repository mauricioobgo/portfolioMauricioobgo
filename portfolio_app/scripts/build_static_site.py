"""Generate a fast, dependency-free static portfolio site from the curated content.

This produces a self-contained ``site/`` directory (HTML with inline CSS/JS plus
local fonts) that deploys reliably to GitHub Pages and renders instantly on
mobile - unlike the Pyodide/Flet web build, which downloads a Python runtime in
the browser. The content is read from the same ``portfolio_content.json`` source
of truth, so the YAML data files remain the single place to edit content.
"""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CONTENT_PATH = ROOT / "src" / "assets" / "portfolio_content.json"
FONTS_SRC = ROOT / "src" / "assets" / "fonts"
SITE_DIR = ROOT / "site"

PALETTE = {
    "bg": "#04070F",
    "panel": "#0A1322",
    "card": "#0D1830",
    "border": "#1E3A5F",
    "primary": "#22D3EE",
    "secondary": "#34D399",
    "purple": "#A78BFA",
    "warning": "#FBBF24",
    "rose": "#FB7185",
    "text": "#F1F5F9",
    "muted": "#8FA3BF",
}

NAV_ITEMS = [
    ("focus", "Focus"),
    ("projects", "Projects"),
    ("experience", "Experience"),
    ("certifications", "Certifications"),
    ("github", "GitHub"),
    ("stack", "Stack"),
    ("contact", "Contact"),
]


def esc(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def load_content() -> dict[str, Any]:
    return json.loads(CONTENT_PATH.read_text(encoding="utf-8"))


def _pill(label: str, accent: str = "primary") -> str:
    return f'<span class="pill pill--{accent}">{esc(label)}</span>'


def _safe_url(url: str | None) -> str | None:
    if not url:
        return None
    url = str(url).strip()
    if url.startswith(("http://", "https://", "mailto:")):
        return url
    return None


def render_nav(profile: dict[str, Any]) -> str:
    links = "".join(
        f'<a href="#{key}" class="nav__link" data-section="{key}">{esc(label)}</a>'
        for key, label in NAV_ITEMS
    )
    return f"""
    <div class="progress" id="progress"></div>
    <header class="nav" id="nav">
      <a href="#top" class="nav__brand">
        <span class="nav__eyebrow">BACKEND · DATA · CLOUD · AI</span>
        <span class="nav__name">{esc(profile.get("name", "Mauricio Obando"))}</span>
      </a>
      <nav class="nav__links">{links}</nav>
      <button class="nav__toggle" id="navToggle" aria-label="Toggle navigation">☰</button>
    </header>
    <nav class="nav__drawer" id="navDrawer">{links}</nav>
    """


def render_hero(content: dict[str, Any]) -> str:
    profile = content["profile"]
    roles = [item.get("name", "") for item in content.get("engineering_focus", [])]
    skills = profile.get("skills", [])[:8]
    commands = content.get("hero_commands", [])

    resume = _safe_url(profile.get("resume_link"))
    linkedin = _safe_url(profile.get("social_links", {}).get("linkedin"))
    github = _safe_url(profile.get("github_url") or profile.get("social_links", {}).get("github"))

    ctas = []
    if resume:
        ctas.append(
            f'<a class="btn btn--primary" href="{esc(resume)}" target="_blank" rel="noopener">'
            f"<span>Download Resume</span></a>"
        )
    if linkedin:
        ctas.append(
            f'<a class="btn btn--ghost" href="{esc(linkedin)}" target="_blank" rel="noopener">'
            f"LinkedIn</a>"
        )
    if github:
        ctas.append(
            f'<a class="btn btn--ghost" href="{esc(github)}" target="_blank" rel="noopener">'
            f"GitHub</a>"
        )
    ctas.append('<a class="btn btn--text" href="#contact">Contact ↓</a>')

    skills_html = "".join(_pill(skill) for skill in skills)
    terminal_lines = "".join(
        f'<div class="term__line">{esc(line)}</div>' if line else '<div class="term__gap"></div>'
        for line in commands
    )

    certifications = content.get("certifications", [])
    metrics = [
        (len(certifications), "credentials", "AWS Pro & Specialty included", "warning"),
        (len(content.get("featured_projects", [])), "case studies", "production-grade", "primary"),
        (
            content.get("github", {}).get("summary", {}).get("repo_count", 0),
            "public repos",
            "open work on GitHub",
            "secondary",
        ),
        (
            len(content.get("engineering_focus", [])),
            "focus areas",
            "backend·data·cloud·AI",
            "purple",
        ),
    ]
    metric_cards = "".join(
        f"""<div class="metric reveal">
          <div class="metric__value" data-count="{value}">{value}</div>
          <div class="metric__label metric__label--{accent}">{esc(label)}</div>
          <div class="metric__caption">{esc(caption)}</div>
        </div>"""
        for value, label, caption, accent in metrics
    )

    role_list = [r for r in roles if r] or ["Software Engineer"]
    role_data = json.dumps(role_list)
    first_role = esc(role_list[0])

    return f"""
    <section class="hero" id="top">
      <div class="hero__grid">
        <div class="hero__left">
          <div class="status">
            <span class="status__dot"></span>
            shipping in production · {esc(profile.get("company", ""))} · {esc(profile.get("location", ""))}
          </div>
          <p class="hero__prompt">$ whoami</p>
          <h1 class="hero__name">Mauricio <span class="grad">Obando</span></h1>
          <div class="hero__role"><span class="hero__chev">&gt;</span>
            <span id="roleText">{first_role}</span><span class="caret"></span>
          </div>
          <p class="hero__subtitle">{esc(profile.get("subtitle", ""))}</p>
          <div class="hero__ctas">{"".join(ctas)}</div>
          <div class="pillrow">{skills_html}</div>
        </div>
        <div class="hero__right">
          <div class="term">
            <div class="term__bar">
              <span class="dot dot--rose"></span><span class="dot dot--amber"></span>
              <span class="dot dot--green"></span>
              <span class="term__title">mauricio@cloud:~</span>
            </div>
            <div class="term__body">{terminal_lines}<span class="caret caret--term"></span></div>
          </div>
          <div class="signal" id="signal" aria-hidden="true"></div>
        </div>
      </div>
      <div class="metrics">{metric_cards}</div>
    </section>
    <script>window.__ROLES__ = {role_data};</script>
    """


def render_section_header(eyebrow: str, title: str, desc: str = "", accent: str = "primary") -> str:
    desc_html = f'<p class="sec__desc">{esc(desc)}</p>' if desc else ""
    return f"""
      <div class="sec__head reveal">
        <span class="sec__eyebrow sec__eyebrow--{accent}">{esc(eyebrow)}</span>
        <h2 class="sec__title">{esc(title)}</h2>
        <span class="rule rule--{accent}"></span>
        {desc_html}
      </div>
    """


def render_focus(content: dict[str, Any]) -> str:
    accents = ["primary", "secondary", "purple", "warning"]
    cards = ""
    for i, item in enumerate(content.get("engineering_focus", [])):
        accent = accents[i % len(accents)]
        skills = "".join(_pill(s, accent) for s in item.get("skills", [])[:7])
        cards += f"""
          <article class="card focus reveal">
            <div class="focus__eyebrow focus__eyebrow--{accent}">
              <span class="sq sq--{accent}"></span>{esc(item.get("eyebrow", "FOCUS"))}
            </div>
            <h3 class="card__title">{esc(item.get("name", ""))}</h3>
            <p class="card__text">{esc(item.get("description", ""))}</p>
            <div class="pillrow">{skills}</div>
          </article>"""
    return f"""
    <section class="sec" id="focus">
      {
        render_section_header(
            "// focus", "What I build", "Four pillars where my delivery work compounds."
        )
    }
      <div class="grid grid--3">{cards}</div>
    </section>"""


def render_projects(content: dict[str, Any]) -> str:
    cards = ""
    for p in content.get("featured_projects", []):
        gh = _safe_url(p.get("github_url"))
        link = (
            f'<a class="card__icon" href="{esc(gh)}" target="_blank" rel="noopener" '
            f'aria-label="Repository">↗</a>'
            if gh
            else ""
        )
        stack = "".join(_pill(s) for s in p.get("tech_stack", [])[:6])
        cards += f"""
          <article class="card project reveal">
            <div class="card__top">
              <div>
                <div class="project__cat">{esc(p.get("category", "Project"))} ·
                  {esc(p.get("status", "Case study"))}</div>
                <h3 class="card__title">{esc(p.get("name", ""))}</h3>
              </div>{link}
            </div>
            <p class="card__text">{esc(p.get("summary", ""))}</p>
            <div class="ps">
              <div><span class="ps__k ps__k--warn">problem</span>
                <p>{esc(p.get("problem", ""))}</p></div>
              <div><span class="ps__k ps__k--ok">solution</span>
                <p>{esc(p.get("solution", ""))}</p></div>
            </div>
            <div class="pillrow">{stack}</div>
          </article>"""
    return f"""
    <section class="sec" id="projects">
      {
        render_section_header(
            "// projects",
            "Selected work",
            "Production patterns from backend, data, cloud, and LLM delivery.",
        )
    }
      <div class="grid grid--2">{cards}</div>
    </section>"""


def render_experience(content: dict[str, Any]) -> str:
    rows = ""
    for item in content.get("experience", [])[:6]:
        company_url = _safe_url(item.get("company_url"))
        company = esc(item.get("company", ""))
        company_html = (
            f'<a href="{esc(company_url)}" target="_blank" rel="noopener" class="exp__co">{company}</a>'
            if company_url
            else f'<span class="exp__co">{company}</span>'
        )
        highlights = "".join(f"<li>{esc(h)}</li>" for h in item.get("highlights", []))
        rows += f"""
          <article class="exp reveal">
            <div class="exp__dot"></div>
            <div class="card exp__card">
              <div class="exp__head">
                <h3 class="exp__role">{esc(item.get("role", ""))} <span class="exp__sep">/</span>
                  {company_html}</h3>
                <span class="exp__meta">{esc(item.get("date", ""))} · {esc(item.get("location", ""))}</span>
              </div>
              <p class="card__text">{esc(item.get("description", ""))}</p>
              <ul class="exp__list">{highlights}</ul>
            </div>
          </article>"""
    return f"""
    <section class="sec" id="experience">
      {render_section_header("// experience", "Where I've shipped")}
      <div class="timeline">{rows}</div>
    </section>"""


def _cert_card(cert: dict[str, Any], featured: bool) -> str:
    issuer = cert.get("issuer", "")
    initials = "".join(w[0] for w in str(issuer).split()[:2]).upper() or "C"
    url = _safe_url(cert.get("credential_url"))
    label = esc(cert.get("credential_label", "View on LinkedIn"))
    btn = (
        f'<a class="btn btn--{"primary" if featured else "ghost"} btn--sm" '
        f'href="{esc(url)}" target="_blank" rel="noopener">✔ {label}</a>'
        if url
        else ""
    )
    accent = "warning" if featured else "primary"
    skills = "".join(_pill(s, "muted") for s in cert.get("skills", [])[:5])
    cls = "cert cert--featured reveal" if featured else "card cert reveal"
    return f"""
      <article class="{cls}">
        <div class="cert__inner">
          <div class="cert__head">
            <span class="mono mono--{accent}">{esc(initials)}</span>
            <div class="pillrow">{_pill(cert.get("level", "Credential"), accent)}
              {_pill(cert.get("status", "Active"), "secondary")}</div>
          </div>
          <h3 class="card__title">{esc(cert.get("title", ""))}</h3>
          <p class="cert__issuer">{esc(issuer)} · {esc(cert.get("category", ""))}</p>
          <div class="pillrow">{skills}</div>
          {btn}
        </div>
      </article>"""


def render_certifications(content: dict[str, Any]) -> str:
    certs = content.get("certifications", [])
    featured = [c for c in certs if c.get("featured")]
    others = sorted((c for c in certs if not c.get("featured")), key=lambda c: c.get("title", ""))
    verify_url = _safe_url(content["profile"].get("linkedin_certifications_url"))
    banner = (
        f"""<div class="banner reveal">
          <span>🛡 {len(certs)} credentials · {len(featured)} featured AWS certifications</span>
          <a href="{esc(verify_url)}" target="_blank" rel="noopener">verify all on LinkedIn ↗</a>
        </div>"""
        if verify_url
        else ""
    )
    featured_html = "".join(_cert_card(c, True) for c in featured)
    others_html = "".join(_cert_card(c, False) for c in others)
    return f"""
    <section class="sec" id="certifications">
      {
        render_section_header(
            "// certifications",
            "Validated credentials",
            "AWS Professional and Specialty certifications, verifiable on LinkedIn.",
            "warning",
        )
    }
      {banner}
      <div class="grid grid--2">{featured_html}</div>
      <div class="grid grid--3" style="margin-top:18px">{others_html}</div>
    </section>"""


def render_github(content: dict[str, Any]) -> str:
    gh = content.get("github", {})
    repos = gh.get("repositories", [])[:6]
    profile_url = _safe_url(gh.get("profile", {}).get("html_url")) or _safe_url(
        content["profile"].get("github_url")
    )
    summary = gh.get("summary", {})
    cards = ""
    for repo in repos:
        url = _safe_url(repo.get("html_url") or repo.get("github_url"))
        if not url:
            continue
        cards += f"""
          <a class="card repo reveal" href="{esc(url)}" target="_blank" rel="noopener">
            <div class="repo__lang">{esc(repo.get("language") or repo.get("category") or "Repo")}</div>
            <h3 class="repo__name">{esc(repo.get("name", ""))} <span class="repo__arrow">↗</span></h3>
            <p class="card__text">{esc((repo.get("description") or "")[:120])}</p>
          </a>"""
    if not cards:
        link = (
            f'<a class="btn btn--ghost" href="{esc(profile_url)}" target="_blank" rel="noopener">'
            f"View GitHub profile ↗</a>"
            if profile_url
            else ""
        )
        cards = f"""<div class="card reveal" style="grid-column:1/-1;text-align:center">
          <p class="card__text">{esc(summary.get("repo_count", 0))} public repositories on GitHub.</p>
          {link}</div>"""
    return f"""
    <section class="sec" id="github">
      {render_section_header("// github", "Open work", "Selected repositories on GitHub.", "secondary")}
      <div class="grid grid--3">{cards}</div>
    </section>"""


def render_stack(content: dict[str, Any]) -> str:
    cards = ""
    for group in content.get("technical_stack", []):
        items = "".join(_pill(i) for i in group.get("items", []))
        cards += f"""
          <article class="card reveal">
            <div class="focus__eyebrow focus__eyebrow--primary">// {esc(group.get("name", "").lower())}</div>
            <h3 class="card__title">{esc(group.get("name", ""))}</h3>
            <div class="pillrow">{items}</div>
          </article>"""
    return f"""
    <section class="sec" id="stack">
      {render_section_header("// stack", "Tooling I reach for")}
      <div class="grid grid--2">{cards}</div>
    </section>"""


def render_contact(content: dict[str, Any]) -> str:
    profile = content["profile"]
    email = profile.get("email", "")
    social = profile.get("social_links", {})
    year = str(content.get("metadata", {}).get("generated_at", ""))[:4] or "2026"
    buttons = []
    if email:
        buttons.append(f'<a class="btn btn--primary" href="mailto:{esc(email)}">✉ {esc(email)}</a>')
    if _safe_url(social.get("linkedin")):
        buttons.append(
            f'<a class="btn btn--ghost" href="{esc(social["linkedin"])}" target="_blank" '
            f'rel="noopener">LinkedIn</a>'
        )
    if _safe_url(profile.get("github_url")):
        buttons.append(
            f'<a class="btn btn--ghost" href="{esc(profile["github_url"])}" target="_blank" '
            f'rel="noopener">GitHub</a>'
        )
    if _safe_url(profile.get("resume_link")):
        buttons.append(
            f'<a class="btn btn--ghost" href="{esc(profile["resume_link"])}" target="_blank" '
            f'rel="noopener">Resume</a>'
        )
    return f"""
    <section class="sec" id="contact">
      {render_section_header("// contact", "Open a connection")}
      <div class="card contact reveal">
        <h3 class="contact__title">Hiring for backend, data, cloud, or AI?</h3>
        <p class="card__text">One email away. I usually reply within a day.</p>
        <div class="hero__ctas">{"".join(buttons)}</div>
        <p class="contact__loc">📍 {esc(profile.get("location", ""))} · remote-friendly</p>
      </div>
      <footer class="footer">© {esc(year)} {esc(profile.get("name", "Mauricio Obando"))} ·
        100% data-driven · deployed on GitHub Pages</footer>
    </section>"""


def render_html(content: dict[str, Any]) -> str:
    profile = content["profile"]
    body = "".join(
        [
            render_nav(profile),
            '<main class="shell">',
            render_hero(content),
            render_focus(content),
            render_projects(content),
            render_experience(content),
            render_certifications(content),
            render_github(content),
            render_stack(content),
            render_contact(content),
            "</main>",
        ]
    )
    desc = esc(profile.get("subtitle", "Backend, Data, Cloud and AI Engineer"))
    title = f"{esc(profile.get('name', 'Mauricio Obando'))} | {esc(profile.get('title', ''))}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<script>{SW_RESET}</script>
<style>{CSS}</style>
</head>
<body>
{body}
<script>{JS}</script>
</body>
</html>"""


# Earlier Flet/Flutter deploys registered a service worker at this path scope
# that aggressively caches and would keep serving the old (broken) bundle. This
# unregisters it, clears its caches, and reloads once so returning visitors get
# the static site without manually clearing site data.
SW_RESET = """
(function(){
  if(!('serviceWorker' in navigator))return;
  navigator.serviceWorker.getRegistrations().then(function(regs){
    var had=regs.length>0;
    regs.forEach(function(r){r.unregister();});
    if(window.caches&&caches.keys){caches.keys().then(function(ks){ks.forEach(function(k){caches.delete(k);});});}
    if(had&&!sessionStorage.getItem('swCleared')){sessionStorage.setItem('swCleared','1');location.reload();}
  }).catch(function(){});
})();
"""

CSS = """
:root{
  --bg:#04070F;--panel:#0A1322;--card:#0D1830;--border:#1E3A5F;
  --primary:#22D3EE;--secondary:#34D399;--purple:#A78BFA;--warning:#FBBF24;
  --rose:#FB7185;--text:#F1F5F9;--muted:#8FA3BF;
}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Regular.ttf') format('truetype');
  font-weight:400;font-display:swap}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-SemiBold.ttf') format('truetype');
  font-weight:600;font-display:swap}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Bold.ttf') format('truetype');
  font-weight:700;font-display:swap}
@font-face{font-family:'IBM Plex Mono';src:url('fonts/IBMPlexMono-Medium.ttf') format('truetype');
  font-weight:500;font-display:swap}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  background:var(--bg);color:var(--text);
  font-family:'Poppins',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  line-height:1.55;overflow-x:hidden;
  background-image:
    radial-gradient(560px circle at 8% -5%, rgba(34,211,238,.10), transparent 60%),
    radial-gradient(640px circle at 100% 18%, rgba(167,139,250,.09), transparent 60%),
    radial-gradient(620px circle at 30% 108%, rgba(52,211,153,.06), transparent 60%),
    linear-gradient(160deg,#04070F,#071226 55%,#070A1C);
  background-attachment:fixed;
}
.mono,.term,.nav__eyebrow,.sec__eyebrow,.pill,.focus__eyebrow,.project__cat,.repo__lang,
.exp__meta,.status,.hero__prompt,.hero__role,.banner,.footer,.metric__label{
  font-family:'IBM Plex Mono',ui-monospace,monospace}
a{color:inherit;text-decoration:none}
.shell{max-width:1180px;margin:0 auto;padding:0 20px 80px}
/* progress + nav */
.progress{position:fixed;top:0;left:0;height:3px;width:0;z-index:60;
  background:linear-gradient(90deg,var(--primary),var(--purple));
  box-shadow:0 0 12px rgba(34,211,238,.5)}
.nav{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;
  justify-content:space-between;gap:16px;padding:12px 22px;
  background:rgba(7,12,24,.72);backdrop-filter:blur(12px);
  border-bottom:1px solid rgba(30,58,95,.5);transition:padding .25s,background .25s}
.nav.scrolled{padding:8px 22px;background:rgba(7,12,24,.9)}
.nav__brand{display:flex;flex-direction:column}
.nav__eyebrow{color:var(--primary);font-size:10px;letter-spacing:.12em;font-weight:700}
.nav__name{font-weight:700;font-size:18px}
.nav__links{display:flex;gap:6px;flex-wrap:wrap}
.nav__link{font-family:'IBM Plex Mono',monospace;font-size:12.5px;color:var(--muted);
  padding:7px 13px;border-radius:999px;border:1px solid transparent;transition:.2s}
.nav__link:hover{color:var(--text)}
.nav__link.active{color:var(--primary);border-color:rgba(34,211,238,.45);
  background:rgba(34,211,238,.10);box-shadow:0 0 16px rgba(34,211,238,.18)}
.nav__toggle{display:none;background:none;border:1px solid var(--border);color:var(--text);
  font-size:18px;border-radius:10px;padding:4px 11px;cursor:pointer}
.nav__drawer{display:none;position:fixed;top:58px;left:0;right:0;z-index:49;
  flex-direction:column;gap:4px;padding:14px 20px;background:rgba(7,12,24,.97);
  border-bottom:1px solid var(--border)}
.nav__drawer.open{display:flex}
/* hero */
.hero{padding:120px 0 30px}
.hero__grid{display:grid;grid-template-columns:1.15fr .85fr;gap:34px;align-items:center}
.status{display:inline-flex;align-items:center;gap:10px;font-size:12px;color:var(--secondary);
  padding:7px 14px;border:1px solid rgba(52,211,153,.3);border-radius:999px;
  background:rgba(52,211,153,.07)}
.status__dot{width:9px;height:9px;border-radius:50%;background:var(--secondary);
  box-shadow:0 0 10px var(--secondary);animation:pulse 1.6s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
.hero__prompt{color:var(--muted);font-size:13px;margin:18px 0 2px}
.hero__name{font-size:clamp(40px,7vw,68px);font-weight:700;line-height:1.02;letter-spacing:-.02em}
.grad{background:linear-gradient(90deg,var(--primary),var(--purple));
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.hero__role{font-size:clamp(16px,2.4vw,22px);color:var(--primary);font-weight:600;
  margin:10px 0;min-height:1.4em;display:flex;align-items:center;gap:9px}
.hero__chev{color:var(--secondary)}
.caret{display:inline-block;width:10px;height:1.05em;background:var(--primary);border-radius:2px;
  animation:blink 1s step-end infinite;vertical-align:middle}
.caret--term{height:14px;width:9px}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
.hero__subtitle{color:var(--muted);font-size:16.5px;max-width:560px;margin:14px 0 22px}
.hero__ctas{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.btn{display:inline-flex;align-items:center;gap:8px;font-family:'IBM Plex Mono',monospace;
  font-size:13px;font-weight:600;padding:13px 19px;border-radius:13px;cursor:pointer;
  transition:transform .15s,box-shadow .15s,background .15s;border:1px solid transparent}
.btn--sm{padding:10px 15px;font-size:12px}
.btn--primary{background:var(--primary);color:#04070F;font-weight:700}
.btn--primary:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(34,211,238,.32)}
.btn--ghost{border-color:rgba(34,211,238,.38);color:var(--text)}
.btn--ghost:hover{transform:translateY(-2px);background:rgba(34,211,238,.08)}
.btn--text{color:var(--muted)}.btn--text:hover{color:var(--text)}
.pillrow{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.pill{font-size:11px;padding:6px 12px;border-radius:999px;border:1px solid;font-weight:600}
.pill--primary{color:var(--primary);border-color:rgba(34,211,238,.26);background:rgba(34,211,238,.10)}
.pill--secondary{color:var(--secondary);border-color:rgba(52,211,153,.26);background:rgba(52,211,153,.10)}
.pill--purple{color:var(--purple);border-color:rgba(167,139,250,.26);background:rgba(167,139,250,.10)}
.pill--warning{color:var(--warning);border-color:rgba(251,191,36,.26);background:rgba(251,191,36,.10)}
.pill--muted{color:var(--muted);border-color:rgba(143,163,191,.22);background:rgba(143,163,191,.07)}
/* terminal */
.term{background:rgba(8,17,30,.92);border:1px solid rgba(34,211,238,.22);border-radius:18px;
  overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.4)}
.term__bar{display:flex;align-items:center;gap:8px;padding:12px 16px;
  border-bottom:1px solid rgba(30,58,95,.5)}
.dot{width:10px;height:10px;border-radius:50%}
.dot--rose{background:var(--rose)}.dot--amber{background:var(--warning)}.dot--green{background:var(--secondary)}
.term__title{margin-left:6px;font-size:12px;color:var(--muted)}
.term__body{padding:18px 18px 20px;font-size:13px;min-height:170px}
.term__line{color:var(--text);white-space:pre-wrap;opacity:0;animation:fadein .4s forwards}
.term__gap{height:10px}
@keyframes fadein{to{opacity:1}}
.signal{display:grid;grid-template-columns:repeat(18,1fr);gap:5px;height:46px;margin-top:14px;
  align-items:end}
.signal span{background:linear-gradient(180deg,var(--primary),var(--purple));border-radius:3px;
  opacity:.8;transition:height .5s ease}
/* metrics */
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:34px}
.metric{background:var(--card);border:1px solid rgba(30,58,95,.55);border-radius:18px;padding:18px}
.metric__value{font-size:34px;font-weight:700;letter-spacing:-.02em}
.metric__label{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-top:2px}
.metric__label--primary{color:var(--primary)}.metric__label--secondary{color:var(--secondary)}
.metric__label--purple{color:var(--purple)}.metric__label--warning{color:var(--warning)}
.metric__caption{color:var(--muted);font-size:12px;margin-top:4px}
/* sections */
.sec{padding:64px 0 0}
.sec__head{margin-bottom:26px}
.sec__eyebrow{font-size:12px;font-weight:700;letter-spacing:.06em}
.sec__eyebrow--primary{color:var(--primary)}.sec__eyebrow--secondary{color:var(--secondary)}
.sec__eyebrow--warning{color:var(--warning)}
.sec__title{font-size:clamp(26px,4vw,36px);font-weight:700;margin:8px 0 10px;letter-spacing:-.01em}
.rule{display:block;width:64px;height:3px;border-radius:999px;
  background:linear-gradient(90deg,var(--primary),transparent)}
.rule--warning{background:linear-gradient(90deg,var(--warning),transparent)}
.rule--secondary{background:linear-gradient(90deg,var(--secondary),transparent)}
.sec__desc{color:var(--muted);font-size:15px;max-width:680px;margin-top:14px}
.grid{display:grid;gap:18px}
.grid--2{grid-template-columns:repeat(2,1fr)}
.grid--3{grid-template-columns:repeat(3,1fr)}
.card{background:var(--card);border:1px solid rgba(30,58,95,.55);border-radius:18px;padding:22px;
  transition:transform .18s,border-color .18s,box-shadow .18s}
.card:hover{transform:translateY(-4px);border-color:rgba(34,211,238,.4);
  box-shadow:0 16px 40px rgba(0,0,0,.35)}
.card__title{font-size:20px;font-weight:700;margin:6px 0}
.card__text{color:var(--muted);font-size:14px}
.card__top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.card__icon{font-size:18px;color:var(--muted);border:1px solid rgba(143,163,191,.22);
  border-radius:10px;padding:2px 9px}.card__icon:hover{color:var(--primary)}
.focus__eyebrow{font-size:12px;display:flex;align-items:center;gap:8px;font-weight:600}
.focus__eyebrow--primary{color:var(--primary)}.focus__eyebrow--secondary{color:var(--secondary)}
.focus__eyebrow--purple{color:var(--purple)}.focus__eyebrow--warning{color:var(--warning)}
.sq{width:11px;height:11px;border-radius:3px;display:inline-block}
.sq--primary{background:var(--primary)}.sq--secondary{background:var(--secondary)}
.sq--purple{background:var(--purple)}.sq--warning{background:var(--warning)}
/* projects */
.project__cat{color:var(--primary);font-size:10.5px;font-weight:700;letter-spacing:.04em}
.ps{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0}
.ps__k{font-size:10px;font-weight:700;text-transform:uppercase}
.ps__k--warn{color:var(--warning)}.ps__k--ok{color:var(--secondary)}
.ps p{color:var(--muted);font-size:12.5px;margin-top:3px}
/* timeline */
.timeline{position:relative;display:flex;flex-direction:column;gap:18px}
.exp{display:grid;grid-template-columns:24px 1fr;gap:16px}
.exp__dot{width:13px;height:13px;border-radius:50%;background:var(--primary);margin-top:24px;
  box-shadow:0 0 14px rgba(34,211,238,.5);position:relative}
.exp__dot::after{content:"";position:absolute;left:6px;top:14px;width:1px;height:120px;
  background:linear-gradient(rgba(241,245,249,.18),transparent)}
.exp__head{display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;align-items:baseline}
.exp__role{font-size:18px;font-weight:700}.exp__sep{color:var(--muted)}
.exp__co{color:var(--primary)}.exp__meta{color:var(--muted);font-size:12px}
.exp__list{list-style:none;margin-top:10px;display:flex;flex-direction:column;gap:7px}
.exp__list li{color:var(--muted);font-size:13.5px;padding-left:16px;position:relative}
.exp__list li::before{content:"";position:absolute;left:0;top:8px;width:5px;height:5px;
  border-radius:50%;background:var(--warning)}
/* certifications */
.banner{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;
  padding:14px 18px;border-radius:16px;background:rgba(251,191,36,.06);
  border:1px solid rgba(251,191,36,.22);font-size:13px;color:var(--muted);margin-bottom:18px}
.banner a{color:var(--warning);font-weight:700}
.cert--featured{border-radius:20px;padding:1.5px;
  background:linear-gradient(135deg,rgba(251,191,36,.65),rgba(34,211,238,.35),rgba(251,191,36,.15));
  transition:transform .18s}.cert--featured:hover{transform:translateY(-4px)}
.cert--featured .cert__inner{background:var(--card);border-radius:19px;padding:24px}
.cert .cert__inner{padding:0}
.cert__head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:8px}
.mono{width:50px;height:50px;border-radius:14px;display:flex;align-items:center;justify-content:center;
  font-weight:700;font-size:18px;border:1px solid}
.mono--warning{color:var(--warning);border-color:rgba(251,191,36,.45);
  background:linear-gradient(135deg,rgba(251,191,36,.28),rgba(251,191,36,.05))}
.mono--primary{color:var(--primary);border-color:rgba(34,211,238,.45);
  background:linear-gradient(135deg,rgba(34,211,238,.28),rgba(34,211,238,.05))}
.cert__issuer{color:var(--primary);font-size:14px;margin:2px 0 8px}
.cert .btn,.cert--featured .btn{margin-top:14px}
/* repos */
.repo{display:block}.repo__lang{color:var(--primary);font-size:12px;font-family:'IBM Plex Mono',monospace}
.repo__name{font-size:16px;font-weight:700;margin:4px 0}.repo__arrow{color:var(--muted)}
/* contact */
.contact{text-align:left;padding:30px}
.contact__title{font-size:clamp(22px,3.4vw,28px);font-weight:700;margin-bottom:8px}
.contact__loc{color:var(--muted);font-size:13px;margin-top:16px}
.footer{text-align:center;color:var(--muted);font-size:12px;margin-top:40px}
/* reveal */
.reveal{opacity:0;transform:translateY(16px);transition:opacity .6s ease,transform .6s ease}
.reveal.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}
  .caret,.status__dot{animation:none}}
/* responsive */
@media(max-width:900px){
  .hero__grid{grid-template-columns:1fr;gap:24px}
  .metrics{grid-template-columns:repeat(2,1fr)}
  .grid--2,.grid--3{grid-template-columns:1fr}
  .nav__links{display:none}.nav__toggle{display:block}
  .ps{grid-template-columns:1fr}
}
@media(max-width:520px){.metrics{grid-template-columns:1fr 1fr}.hero{padding:100px 0 20px}}
"""

JS = """
(function(){
  // scroll progress + nav state
  var nav=document.getElementById('nav'),prog=document.getElementById('progress');
  var links=[].slice.call(document.querySelectorAll('.nav__link'));
  function onScroll(){
    var h=document.documentElement,st=h.scrollTop||document.body.scrollTop;
    var max=(h.scrollHeight-h.clientHeight)||1;
    prog.style.width=(st/max*100)+'%';
    nav.classList.toggle('scrolled',st>20);
  }
  document.addEventListener('scroll',onScroll,{passive:true});onScroll();
  // mobile drawer
  var t=document.getElementById('navToggle'),d=document.getElementById('navDrawer');
  if(t)t.addEventListener('click',function(){d.classList.toggle('open')});
  if(d)d.addEventListener('click',function(e){if(e.target.classList.contains('nav__link'))d.classList.remove('open')});
  // active section
  var secs=[].slice.call(document.querySelectorAll('section[id]'));
  var so=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){var id=e.target.id;links.forEach(function(l){
      l.classList.toggle('active',l.getAttribute('data-section')===id)})}})},
    {rootMargin:'-45% 0px -50% 0px'});
  secs.forEach(function(s){so.observe(s)});
  // reveal on scroll
  var ro=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add('in');ro.unobserve(e.target)}})},
    {rootMargin:'0px 0px -8% 0px'});
  [].slice.call(document.querySelectorAll('.reveal')).forEach(function(el,i){
    el.style.transitionDelay=(Math.min(i,6)*0.05)+'s';ro.observe(el)});
  // count-up metrics
  var counted=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return;var el=e.target,tgt=+el.getAttribute('data-count')||0,n=0,steps=26;
    var iv=setInterval(function(){n++;var p=1-Math.pow(1-n/steps,3);
      el.textContent=Math.round(tgt*p);if(n>=steps){el.textContent=tgt;clearInterval(iv)}},28);
    counted.unobserve(el)})},{threshold:.5});
  [].slice.call(document.querySelectorAll('.metric__value')).forEach(function(el){counted.observe(el)});
  // role typer
  var roles=window.__ROLES__||['Software Engineer'],rt=document.getElementById('roleText'),ri=0;
  function type(){var r=roles[ri%roles.length],i=0;(function ti(){
    rt.textContent=r.slice(0,i);if(i++<=r.length){setTimeout(ti,45)}else{setTimeout(del,1600)}})();
    function del(){(function de(){rt.textContent=r.slice(0,i);if(i-->0){setTimeout(de,22)}
      else{ri++;setTimeout(type,180)}})()}}
  if(rt)type();
  // signal bars
  var sig=document.getElementById('signal');
  if(sig){var bars=[];for(var i=0;i<18;i++){var b=document.createElement('span');
    b.style.height='12px';sig.appendChild(b);bars.push(b)}
    setInterval(function(){bars.forEach(function(b){b.style.height=(10+Math.random()*34)+'px'})},620)}
})();
"""


def build_static_site(output_dir: Path = SITE_DIR) -> Path:
    content = load_content()
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(render_html(content), encoding="utf-8")

    # add .nojekyll so GitHub Pages serves files/dirs verbatim
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")

    fonts_dst = output_dir / "fonts"
    fonts_dst.mkdir(parents=True, exist_ok=True)
    if FONTS_SRC.is_dir():
        for font in FONTS_SRC.glob("*.ttf"):
            shutil.copyfile(font, fonts_dst / font.name)

    favicon = ROOT / "build" / "web" / "favicon.png"
    if favicon.exists():
        shutil.copyfile(favicon, output_dir / "favicon.png")
    return output_dir


def main() -> None:
    out = build_static_site()
    print(f"Static site written to {out}")


if __name__ == "__main__":
    main()
