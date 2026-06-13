#!/usr/bin/env python3
"""Keyless news + release fetcher for The Wire.

Sources (no API keys required):
  - Hacker News via the Algolia search API (stories matching curated queries).
  - GitHub Releases for the curated open-source tools in data/tools.json.

Design goals: never crash the build. Every network call is best-effort with a
short timeout; on failure we keep whatever is already cached so the site always
builds. New items are merged into a growing, de-duplicated archive.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
NEWS_FILE = DATA / "news.json"
TOOLS_FILE = DATA / "tools.json"
TICKER_FILE = DATA / "ticker.json"

UA = "awesome-free-compute-site/1.0 (+https://github.com/amitpandeytiktok/awesome-free-compute-2026)"
TIMEOUT = 12
MAX_ITEMS = 120          # cap the archive so it never balloons
WINDOW_DAYS = 120        # HN: only keep stories from the last N days

# Hacker News search queries — high-signal topics for this site.
HN_QUERIES = [
    "free LLM API", "open source LLM", "open weights model", "local LLM",
    "free GPU", "free tier AI", "prompt caching", "QLoRA fine-tuning",
    "text to speech open source", "open music generation", "image to 3D",
    "Cloudflare free", "DeepSeek", "Qwen", "Mistral open", " comfyui ",
    "AI gateway", "Model Context Protocol", "stem separation", "video upscaling",
]
HN_MIN_POINTS = 25       # ignore low-signal noise


def _get_json(url: str, headers: dict | None = None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def _get_text(url: str, headers: dict | None = None) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def fetch_hn() -> list[dict]:
    """Pull recent, popular HN stories matching our topics."""
    cutoff = int(time.time()) - WINDOW_DAYS * 86400
    out: dict[str, dict] = {}
    for q in HN_QUERIES:
        url = (
            "https://hn.algolia.com/api/v1/search_by_date"
            f"?query={urllib.parse.quote(q)}"
            "&tags=story"
            f"&numericFilters=created_at_i>{cutoff},points>{HN_MIN_POINTS}"
            "&hitsPerPage=15"
        )
        try:
            data = _get_json(url)
        except Exception as e:
            print(f"  [hn] '{q}' failed: {e}", file=sys.stderr)
            continue
        for hit in data.get("hits", []):
            oid = str(hit.get("objectID"))
            title = _clean(hit.get("title"))
            if not oid or not title:
                continue
            link = hit.get("url") or f"https://news.ycombinator.com/item?id={oid}"
            points = int(hit.get("points") or 0)
            existing = out.get(oid)
            if existing and existing.get("points", 0) >= points:
                continue
            out[oid] = {
                "id": f"hn-{oid}",
                "title": title,
                "url": link,
                "source": "Hacker News",
                "points": points,
                "comments_url": f"https://news.ycombinator.com/item?id={oid}",
                "ts": datetime.fromtimestamp(
                    int(hit.get("created_at_i", 0)), tz=timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "kind": "story",
            }
        time.sleep(0.2)  # be polite
    items = sorted(out.values(), key=lambda x: x["ts"], reverse=True)
    print(f"  [hn] {len(items)} stories", file=sys.stderr)
    return items


def fetch_releases() -> list[dict]:
    """Latest release/tag per curated tool (keyless; uses GITHUB_TOKEN if present)."""
    tools = _load(TOOLS_FILE, {}).get("tools", [])
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    out: list[dict] = []
    for t in tools:
        repo = t.get("repo")
        if not repo:
            continue
        rel = None
        try:
            rel = _get_json(f"https://api.github.com/repos/{repo}/releases/latest", headers)
        except urllib.error.HTTPError as e:
            if e.code == 404:  # no formal releases — fall back to tags
                try:
                    tags = _get_json(f"https://api.github.com/repos/{repo}/tags?per_page=1", headers)
                    if tags:
                        rel = {"tag_name": tags[0].get("name"), "html_url": f"https://github.com/{repo}/releases", "published_at": None}
                except Exception as e2:
                    print(f"  [gh] {repo} tags failed: {e2}", file=sys.stderr)
            else:
                print(f"  [gh] {repo} failed: {e}", file=sys.stderr)
        except Exception as e:
            print(f"  [gh] {repo} failed: {e}", file=sys.stderr)
        if not rel or not rel.get("tag_name"):
            continue
        tag = _clean(rel.get("tag_name"))
        out.append({
            "id": f"gh-{repo}-{tag}",
            "title": f"{t['name']} {tag}",
            "url": rel.get("html_url") or f"https://github.com/{repo}/releases",
            "source": "GitHub",
            "repo": repo,
            "cat": t.get("cat", ""),
            "blurb": t.get("blurb", ""),
            "ts": _clean(rel.get("published_at")) or _now_iso(),
            "kind": "release",
        })
        time.sleep(0.1)
    print(f"  [gh] {len(out)} releases", file=sys.stderr)
    return out


def merge(existing: list[dict], fresh: list[dict]) -> list[dict]:
    by_id = {it["id"]: it for it in existing}
    added = 0
    for it in fresh:
        if it["id"] not in by_id:
            it.setdefault("first_seen", _now_iso())
            added += 1
        else:
            it["first_seen"] = by_id[it["id"]].get("first_seen", _now_iso())
        by_id[it["id"]] = it
    merged = sorted(by_id.values(), key=lambda x: x.get("ts", ""), reverse=True)
    print(f"  [merge] +{added} new, {len(merged)} total (capped {MAX_ITEMS})", file=sys.stderr)
    return merged[:MAX_ITEMS]


# ----------------------------------------------------------------------------
# Always-on ticker: a broader AI + tech + crypto headline feed (keyless).
# ----------------------------------------------------------------------------
TICKER_MAX = 40
TICKER_MIN_POINTS = 15
TICKER_WINDOW_DAYS = 21          # ticker stays fresher than the archive
TICKER_HN = {
    "ai": ["large language model", "open source AI", "AI agents", "diffusion model", "AI coding"],
    "crypto": ["bitcoin", "ethereum", "crypto", "stablecoin", "solana"],
}
# Best-effort RSS (no keys). Failures are skipped — HN is the reliable backbone.
TICKER_RSS = [
    ("https://cointelegraph.com/rss", "crypto", "Cointelegraph"),
    ("https://decrypt.co/feed", "crypto", "Decrypt"),
    ("https://feeds.arstechnica.com/arstechnica/index", "tech", "Ars Technica"),
    ("https://www.theverge.com/rss/index.xml", "tech", "The Verge"),
]


def _short(text: str, n: int = 110) -> str:
    t = _clean(text)
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def _hn_ts(hit: dict) -> str:
    return datetime.fromtimestamp(
        int(hit.get("created_at_i", 0)), tz=timezone.utc
    ).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_ticker_hn() -> list[dict]:
    cutoff = int(time.time()) - TICKER_WINDOW_DAYS * 86400
    out: dict[str, dict] = {}
    for cat, queries in TICKER_HN.items():
        for q in queries:
            url = (
                "https://hn.algolia.com/api/v1/search_by_date"
                f"?query={urllib.parse.quote(q)}&tags=story"
                f"&numericFilters=created_at_i>{cutoff},points>{TICKER_MIN_POINTS}"
                "&hitsPerPage=8"
            )
            try:
                hits = _get_json(url).get("hits", [])
            except Exception:
                continue
            for hit in hits:
                oid = str(hit.get("objectID"))
                title = _clean(hit.get("title"))
                if not oid or not title or oid in out:
                    continue
                out[oid] = {
                    "title": _short(title),
                    "url": hit.get("url") or f"https://news.ycombinator.com/item?id={oid}",
                    "source": "Hacker News", "cat": cat, "ts": _hn_ts(hit),
                }
            time.sleep(0.15)
    # HN front page → general tech pulse
    try:
        for hit in _get_json(
            "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=20"
        ).get("hits", []):
            oid = str(hit.get("objectID"))
            title = _clean(hit.get("title"))
            if not oid or not title or oid in out:
                continue
            out[oid] = {
                "title": _short(title),
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={oid}",
                "source": "Hacker News", "cat": "tech", "ts": _hn_ts(hit),
            }
    except Exception:
        pass
    return list(out.values())


def fetch_rss(url: str, cat: str, source: str) -> list[dict]:
    import xml.etree.ElementTree as ET
    from email.utils import parsedate_to_datetime
    try:
        root = ET.fromstring(_get_text(
            url, {"Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8"}))
    except Exception as e:
        print(f"  [rss] {source} failed: {e}", file=sys.stderr)
        return []
    items: list[dict] = []
    for it in root.iter("item"):  # RSS 2.0
        title = _clean(it.findtext("title") or "")
        link = _clean(it.findtext("link") or "")
        if not title or not link:
            continue
        ts = _now_iso()
        if it.findtext("pubDate"):
            try:
                ts = parsedate_to_datetime(it.findtext("pubDate")).astimezone(
                    timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                pass
        items.append({"title": _short(title), "url": link, "source": source, "cat": cat, "ts": ts})
    if not items:  # Atom fallback
        ns = "{http://www.w3.org/2005/Atom}"
        for it in root.iter(f"{ns}entry"):
            title = _clean(it.findtext(f"{ns}title") or "")
            link_el = it.find(f"{ns}link")
            link = link_el.get("href") if link_el is not None else ""
            if not title or not link:
                continue
            ts = _clean(it.findtext(f"{ns}updated") or it.findtext(f"{ns}published") or "") or _now_iso()
            items.append({"title": _short(title), "url": link, "source": source, "cat": cat, "ts": ts})
    print(f"  [rss] {source}: {len(items)}", file=sys.stderr)
    return items[:12]


def _ticker_from_wire(limit: int = 16) -> list[dict]:
    """Reuse the freshest free-AI stories already in The Wire (tagged ai)."""
    prev = _load(NEWS_FILE, {})
    items = prev.get("items", []) if isinstance(prev, dict) else []
    out: list[dict] = []
    for it in items:
        if it.get("kind") == "story" and it.get("url"):
            out.append({"title": _short(it.get("title", "")), "url": it["url"],
                        "source": it.get("source", "Hacker News"), "cat": "ai",
                        "ts": it.get("ts", "")})
            if len(out) >= limit:
                break
    return out


def fetch_ticker() -> list[dict]:
    items = _ticker_from_wire() + fetch_ticker_hn()
    for url, cat, source in TICKER_RSS:
        items += fetch_rss(url, cat, source)
    seen: set[str] = set()
    uniq: list[dict] = []
    for it in items:
        key = it["url"].split("?")[0].rstrip("/")
        if key in seen:
            continue
        seen.add(key)
        uniq.append(it)
    uniq.sort(key=lambda x: x.get("ts", ""), reverse=True)
    # Round-robin by category so the bar alternates ai/crypto/tech instead of
    # clustering, and a healthy slice of AI always survives the cap.
    buckets: dict[str, list[dict]] = {"ai": [], "crypto": [], "tech": []}
    for it in uniq:
        buckets.get(it.get("cat", "tech"), buckets["tech"]).append(it)
    mixed: list[dict] = []
    order = ("ai", "crypto", "tech")
    i = 0
    while len(mixed) < TICKER_MAX and any(buckets.values()):
        b = buckets[order[i % len(order)]]
        if b:
            mixed.append(b.pop(0))
        i += 1
    print(f"  [ticker] {len(uniq)} items", file=sys.stderr)
    return mixed[:TICKER_MAX]


def write_ticker() -> None:
    fresh = fetch_ticker()
    if not fresh:
        prev = _load(TICKER_FILE, {})
        fresh = prev.get("items", []) if isinstance(prev, dict) else []
        print("  [ticker] no fresh items; keeping cache", file=sys.stderr)
    TICKER_FILE.write_text(
        json.dumps({"updated": _now_iso(), "items": fresh}, indent=2, ensure_ascii=False),
        encoding="utf-8")
    print(f"Wrote {TICKER_FILE} ({len(fresh)} items)")


def main() -> int:
    prev = _load(NEWS_FILE, {})
    existing = prev.get("items", []) if isinstance(prev, dict) else []
    fresh: list[dict] = []
    fresh += fetch_hn()
    fresh += fetch_releases()
    if not fresh and existing:
        print("  [warn] no fresh items fetched; keeping cache", file=sys.stderr)
        items = existing
    else:
        items = merge(existing, fresh)
    payload = {"updated": _now_iso(), "count": len(items), "items": items}
    NEWS_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {NEWS_FILE} ({len(items)} items)")
    write_ticker()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
