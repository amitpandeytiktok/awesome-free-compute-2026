#!/usr/bin/env python3
"""Static-site generator for Awesome Free Compute.

Renders the evergreen markdown guides into a styled, navigable site and folds in
the live "Wire" news feed (data/news.json, refreshed by news.py). Pure-Python,
no JS build step. Output goes to ../dist/.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.toc import TocExtension
from pygments.formatters import HtmlFormatter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DIST = ROOT / "dist"
TPL = HERE / "templates"
STATIC = HERE / "static"
DATA = HERE / "data"

SITE = {
    "name": "Awesome Free Compute",
    "tagline": "The field guide to $0 AI — compute, tokens, media & the stack.",
    "url": "https://amitpandeytiktok.github.io/awesome-free-compute-2026",
    "repo": "https://github.com/amitpandeytiktok/awesome-free-compute-2026",
    "pulse_url": "https://ai.techwaveacademy.com/",
    "year": 2026,
}

# Guide registry — order matters (drives nav + home cards).
GUIDES = [
    {"file": "PRIMER.md", "slug": "primer", "emoji": "🧠", "title": "AI & Tokens 101",
     "tagline": "Start here: what tokens are, why this is free, and how we got to a $0 stack.", "cat": "Start"},
    {"file": "README.md", "slug": "compute", "emoji": "🖥️", "title": "Free Compute",
     "tagline": "Always-free CPUs & VMs, free GPU notebooks, serverless GPU, trial credits, fine-tuning.", "cat": "Compute"},
    {"file": "TOKEN-MAXXING.md", "slug": "tokens", "emoji": "🪙", "title": "Token-Maxxing",
     "tagline": "Max frontier-model usage for $0: free LLM APIs, the BYO-key move, China's cheap tokens.", "cat": "LLMs"},
    {"file": "AUDIO.md", "slug": "audio", "emoji": "🎙️", "title": "Audio Generation",
     "tagline": "Free music, voice cloning & transcription — with the commercial-licensing landmines flagged.", "cat": "Media"},
    {"file": "POST-PRODUCTION.md", "slug": "post-production", "emoji": "🎬", "title": "Media Post-Production",
     "tagline": "Finish for $0: upscale, 60fps, stems, mastering, subtitles, dubbing, 3D & matting.", "cat": "Media"},
    {"file": "STACK.md", "slug": "stack", "emoji": "🚀", "title": "Ship-It Stack",
     "tagline": "The backend to deploy an AI app for $0 — DBs, vector, embeddings, hosting, auth.", "cat": "Build"},
]
LINKMAP = {g["file"]: f"{g['slug']}.html" for g in GUIDES}


def github_slugify(value: str, separator: str = "-") -> str:
    """Replicate GitHub's heading-anchor algorithm so hand-written TOC links resolve."""
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s]+", separator, value)
    return value


CALLOUT_LABELS = {
    "tip": "💡 Tip", "note": "📝 Note", "warning": "⚠️ Heads-up",
    "important": "❗ Important", "caution": "🚧 Caution",
}
# Leading emoji → callout severity (for `> ⚠️ …` style blockquotes the guides use).
EMOJI_KIND = {
    "⚠️": "warning", "⚠": "warning", "🚧": "warning", "🛑": "warning",
    "🚫": "important", "❗": "important", "❌": "important",
    "💡": "tip", "🍰": "tip", "🍎": "tip", "🔑": "tip", "🎯": "tip", "🥇": "tip",
}
_BQ_RE = re.compile(r"<blockquote>(.*?)</blockquote>", re.DOTALL)


def render_callouts(html: str) -> str:
    """Turn GitHub `> [!TIP]` and emoji-led blockquotes into styled callout cards."""
    def repl(m: re.Match) -> str:
        inner = m.group(1).strip()
        am = re.match(r"<p>\[!(TIP|NOTE|WARNING|IMPORTANT|CAUTION)\]\s*(.*)", inner, re.DOTALL)
        if am:
            kind = am.group(1).lower()
            body = "<p>" + am.group(2)
            return (f'<div class="callout callout-{kind}">'
                    f'<div class="callout-title">{CALLOUT_LABELS[kind]}</div>{body}</div>')
        em = re.match(r"<p>\s*(?:<strong>)?\s*([^\w\s<])", inner)
        if em:
            lead = inner[em.start(1):em.start(1) + 2]
            kind = EMOJI_KIND.get(lead) or EMOJI_KIND.get(lead[0])
            if kind:
                return f'<div class="callout callout-{kind}">{inner}</div>'
        return m.group(0)
    return _BQ_RE.sub(repl, html)


def rewrite_links(html: str) -> str:
    """Repoint ./GUIDE.md links to their .html pages."""
    def repl(m: re.Match) -> str:
        file = m.group("file")
        anchor = m.group("anchor") or ""
        return f'href="{LINKMAP.get(file, file)}{anchor}"'
    return re.sub(r'href="\.?/?(?P<file>[A-Z0-9-]+\.md)(?P<anchor>#[^"]*)?"', repl, html)


def extract_toc(md_text: str) -> list[dict]:
    """Pull h2/h3 headings for the in-page sidebar."""
    toc: list[dict] = []
    in_code = False
    for line in md_text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(##|###)\s+(.*)", line)
        if not m:
            continue
        level = len(m.group(1))
        text = m.group(2).strip()
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # unwrap links
        text = re.sub(r"[`*_]", "", text)                       # strip md emphasis
        toc.append({"level": level, "text": text, "id": github_slugify(text)})
    return toc


def render_markdown(md_text: str) -> str:
    md = markdown.Markdown(extensions=[
        "fenced_code", "tables", "sane_lists", "attr_list",
        CodeHiliteExtension(guess_lang=False, noclasses=False),
        TocExtension(slugify=github_slugify, anchorlink=True),
    ])
    html = md.convert(md_text)
    html = render_callouts(html)
    html = rewrite_links(html)
    return html


def first_h1(md_text: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return re.sub(r"[`*_#]", "", line[2:]).strip()
    return ""


def rel_time(ts: str) -> str:
    try:
        dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except Exception:
        return ""
    delta = datetime.now(timezone.utc) - dt
    s = int(delta.total_seconds())
    if s < 3600:
        return f"{max(1, s // 60)}m ago"
    if s < 86400:
        return f"{s // 3600}h ago"
    if s < 86400 * 30:
        return f"{s // 86400}d ago"
    return dt.strftime("%b %Y")


def load_news() -> dict:
    try:
        data = json.loads((DATA / "news.json").read_text(encoding="utf-8"))
    except Exception:
        return {"updated": "", "items": []}
    for it in data.get("items", []):
        it["rel"] = rel_time(it.get("ts", ""))
        it["date"] = (it.get("ts", "")[:10])
    return data


def load_ticker() -> list:
    """Headlines for the always-on ticker (AI/tech/crypto)."""
    try:
        data = json.loads((DATA / "ticker.json").read_text(encoding="utf-8"))
        return data.get("items", [])[:30]
    except Exception:
        return []


def main() -> int:
    env = Environment(loader=FileSystemLoader(str(TPL)),
                      autoescape=select_autoescape(["html"]))
    env.filters["slug"] = github_slugify

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    # static assets + pygments stylesheet
    shutil.copytree(STATIC, DIST, dirs_exist_ok=True)
    pyg = HtmlFormatter(style="dracula").get_style_defs(".codehilite")
    (DIST / "pygments.css").write_text(pyg, encoding="utf-8")
    # tell GitHub Pages to serve our files verbatim (no Jekyll processing)
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    news = load_news()
    nav = [{"slug": g["slug"], "title": g["title"], "emoji": g["emoji"]} for g in GUIDES]
    ctx_base = {"site": SITE, "nav": nav, "news_updated": rel_time(news.get("updated", "")),
                "ticker": load_ticker(),
                "build_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}

    # guide pages
    guide_tpl = env.get_template("guide.html")
    for g in GUIDES:
        md_text = (ROOT / g["file"]).read_text(encoding="utf-8")
        body = render_markdown(md_text)
        toc = extract_toc(md_text)
        page = guide_tpl.render(**ctx_base, guide=g, body=body, toc=toc,
                                page_title=f"{g['title']} — {SITE['name']}")
        (DIST / f"{g['slug']}.html").write_text(page, encoding="utf-8")

    # home
    items = news.get("items", [])
    wire = items[:14]
    releases = [it for it in items if it.get("kind") == "release"][:8]
    home = env.get_template("home.html").render(
        **ctx_base, guides=GUIDES, wire=wire, releases=releases,
        page_title=f"{SITE['name']} — Free AI, tokens & compute")
    (DIST / "index.html").write_text(home, encoding="utf-8")

    # news archive
    cats = sorted({it.get("cat") for it in items if it.get("cat")})
    newspage = env.get_template("news.html").render(
        **ctx_base, items=items, cats=cats, count=len(items),
        page_title=f"The Wire — {SITE['name']}")
    (DIST / "news.html").write_text(newspage, encoding="utf-8")

    # embed news json for client-side search on the archive page
    (DIST / "news-data.json").write_text(
        json.dumps({"items": items}, ensure_ascii=False), encoding="utf-8")

    print(f"Built {len(GUIDES)} guides + home + news → {DIST} ({len(items)} news items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
