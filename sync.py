#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.27",
#     "beautifulsoup4>=4.12",
#     "lxml>=5.2",
#     "markdownify>=1.0,<2",
# ]
# ///
"""Mirror straion.com docs to offline, LLM-readable Markdown.

Straion publishes /llms.txt, but it covers only the marketing surface
(/product, /blog, /pricing) and contains zero /docs entries. /llms-full.txt
is 404. This script builds both for the whole site, from the sitemap.

Run:
    ./sync.py               # refresh the corpus in place
    ./sync.py --check       # verify the committed corpus matches the live site
    ./sync.py --only-docs   # /docs pages only
    ./sync.py --force       # ignore ETags, re-extract everything

Rebuilds are deterministic: two cold builds are byte-identical to each other and
to any incrementally-maintained corpus, so `./sync.py` always converges on the
same bytes regardless of what ran before it.

Incrementality is two-layered:
  1. HTTP conditional GET (If-None-Match) -- avoids transferring unchanged pages.
  2. sha256 of the *extracted Markdown* -- the authority on whether anything changed.

Layer 2 hashes the output rather than the input on purpose: the raw HTML carries
per-deploy noise (Astro island ids, asset fingerprints) that changes on every
publish even when the prose is identical. Hashing the extracted Markdown means a
redeploy with no content change produces zero log entries.

For the same reason, generated files contain no timestamp -- a `fetched_at` in
the frontmatter would make every file differ from itself on every run and defeat
the whole mechanism. Timestamps live in the manifest and the log instead.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit

import httpx
from bs4 import BeautifulSoup, Tag
from markdownify import MarkdownConverter

SITE = "https://straion.com"
SITEMAP_INDEX = f"{SITE}/sitemap-index.xml"
USER_AGENT = (
    "straion-docs-for-agents-unofficial/1.0 "
    "(+https://github.com/Elijas/straion-docs-for-agents-unofficial)"
)

# Container selectors, most specific first. Straion's docs pages wrap body copy
# in <article class="docs-article">; marketing pages fall back to <main>, and a
# few (e.g. /career) have neither and land on <body>.
#
# Deliberately no bare "article" fallback: marketing pages use <article> for
# cards, so it would match a single team-member tile rather than the page.
CONTENT_SELECTORS = ("article.docs-article", "main", "body")

# Chrome to drop from inside the selected container before conversion.
# "svg" also drops the inline-SVG code illustration on /product/ai-coding-guidance,
# whose text is decorative sample code restated by the bullets beside it. Measured:
# every alternative that preserved it pulled in more noise than signal.
STRIP_SELECTORS = (
    "script", "style", "noscript", "svg", "nav", "aside", "form", "button",
    "[aria-hidden=true]", ".sr-only", "astro-island > script",
)

# Additionally dropped only when we fell back to <body>, where the site header
# and footer are in scope. Verified safe: docs-article contains no <header>.
BODY_FALLBACK_STRIP = ("header", "footer")

# The docs sidebar. It is stripped from page bodies as chrome, but read separately
# for its structure: the sitemap is a flat alphabetical list, whereas this sidebar
# is the authored information architecture -- grouped into sections and ordered
# pedagogically. Without it the corpus reads as an undifferentiated pile of pages.
SIDEBAR_SELECTOR = 'nav[aria-label="Docs navigation"]'

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# Transient-failure budget per URL. 3 attempts with linear backoff covers the
# read timeouts CI runners see without masking a genuinely unreachable site.
FETCH_ATTEMPTS = 3
FETCH_BACKOFF = 2.0


# --------------------------------------------------------------------------- #
# Markdown conversion
# --------------------------------------------------------------------------- #

class StraionConverter(MarkdownConverter):
    """Markdownify subclass that rewrites internal links to local .md paths."""

    def __init__(self, url_to_relpath: dict[str, str], current_relpath: str, **kwargs):
        super().__init__(**kwargs)
        self.url_to_relpath = url_to_relpath
        self.current_dir = Path(current_relpath).parent

    def convert_a(self, el, text, parent_tags=None, **kwargs):
        href = el.get("href")
        if href and href.startswith("#"):
            # urljoin(SITE, "#frag") canonicalizes to the site root, which would
            # rewrite an in-page anchor into a link to the homepage file. Leave
            # same-page anchors exactly as authored.
            return super().convert_a(el, text, parent_tags=parent_tags, **kwargs)
        if href:
            absolute = urljoin(SITE, href)
            split = urlsplit(absolute)
            key = canonical_url(absolute)
            target = self.url_to_relpath.get(key)
            if target:
                # Point at the local mirror so the corpus is navigable offline.
                rel = Path(_relpath(self.current_dir, Path(target))).as_posix()
                el["href"] = rel + (f"#{split.fragment}" if split.fragment else "")
            else:
                el["href"] = absolute
        return super().convert_a(el, text, parent_tags=parent_tags, **kwargs)

    def convert_img(self, el, text, parent_tags=None, **kwargs):
        src = el.get("src")
        if src:
            el["src"] = urljoin(SITE, src)
        return super().convert_img(el, text, parent_tags=parent_tags, **kwargs)

    def convert_pre(self, el, text, parent_tags=None, **kwargs):
        """Widen the fence when a code block's own content contains backtick runs.

        The docs teach rule-file syntax by showing a Markdown file that itself
        contains fenced examples. markdownify always emits three backticks, so
        the outer fence closed at the first inner ``` and the rest of the page
        was swallowed into one unlabelled block. CommonMark allows any longer
        run, and widening is a no-op for blocks without a >=3 backtick run.
        """
        md = super().convert_pre(el, text, parent_tags=parent_tags, **kwargs)
        longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
        if longest < 3:
            return md

        # Widen the OUTER pair only. Substituting the first two ``` lines instead
        # would hit the block's first *inner* fence and leave the real closer at
        # three backticks -- still unclosed, which is the bug being fixed.
        lines = md.split("\n")
        opens = [i for i, ln in enumerate(lines) if ln.startswith("```")]
        closes = [i for i, ln in enumerate(lines) if ln.strip() == "```"]
        if not opens or not closes:
            return md
        first, last = opens[0], closes[-1]
        if first == last:
            return md
        fence = "`" * (longest + 1)
        lines[first] = fence + lines[first][3:]  # keep the info string (e.g. ```md)
        lines[last] = fence
        return "\n".join(lines)


def _relpath(from_dir: Path, to_file: Path) -> str:
    """Relative path from a directory to a file, both relative to the same root."""
    from_parts = list(from_dir.parts)
    to_parts = list(to_file.parts)
    common = 0
    while common < len(from_parts) and common < len(to_parts) - 1 and from_parts[common] == to_parts[common]:
        common += 1
    up = [".."] * (len(from_parts) - common)
    down = to_parts[common:]
    return str(Path(*(up + down))) if (up or down) else to_file.name


def code_language(el: Tag) -> str:
    """Shiki (Astro's highlighter) records the language on the <pre> element."""
    for attr in ("data-language", "data-lang"):
        if el.get(attr):
            return el[attr]
    node = el.find("code") or el
    for cls in node.get("class", []):
        if cls.startswith("language-"):
            return cls[len("language-"):]
    return ""


def html_to_markdown(html: str, url: str, url_to_relpath: dict[str, str], relpath: str) -> tuple[str, str, str]:
    """Return (title, description, markdown_body) for one page."""
    soup = BeautifulSoup(html, "lxml")

    desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find(
        "meta", attrs={"property": "og:description"}
    )
    description = (desc_tag.get("content") or "").strip() if desc_tag else ""

    container = None
    matched = None
    for selector in CONTENT_SELECTORS:
        container = soup.select_one(selector)
        if container is not None:
            matched = selector
            break
    if container is None:
        raise RuntimeError(f"no content container found for {url}")

    # Radix accordions render each FAQ question as <h3><button>text<svg/></button></h3>,
    # so the blanket button strip below would empty the heading and leave a bare "###".
    # Unwrapping first keeps the question; the svg strip still drops the chevron. Scoped
    # to headings on purpose -- unwrapping every button with text leaks close controls
    # and duplicate CTAs into the body.
    for node in container.select(", ".join(f"h{n} button" for n in range(1, 7))):
        node.unwrap()

    strip = STRIP_SELECTORS + (BODY_FALLBACK_STRIP if matched == "body" else ())
    for selector in strip:
        for node in container.select(selector):
            node.decompose()

    h1 = container.find("h1")
    if h1 and h1.get_text(strip=True):
        title = h1.get_text(strip=True)
    elif soup.title and soup.title.string:
        title = soup.title.string.strip()
    else:
        title = url.rstrip("/").rsplit("/", 1)[-1] or "index"

    converter = StraionConverter(
        url_to_relpath=url_to_relpath,
        current_relpath=relpath,
        heading_style="ATX",
        bullets="-",
        code_language_callback=code_language,
        escape_asterisks=False,
        escape_underscores=False,
    )
    body = converter.convert_soup(container)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return title, description, body


def render_page(title: str, url: str, description: str, body: str, nav: dict | None = None) -> str:
    """Frontmatter + body. Deliberately contains no timestamp -- see module docstring."""
    lines = ["---", f"title: {json.dumps(title)}", f"source: {url}"]
    if description:
        lines.append(f"description: {json.dumps(description)}")
    if nav:
        # Reading-order context, so a page carries its place in the docs even when
        # a model is handed that single file with no index alongside it.
        if nav.get("unlisted"):
            lines.append("unlisted: true  # in sitemap, absent from the docs sidebar")
        else:
            lines.append(f"section: {json.dumps(nav['section'])}")
            lines.append(f"order: {nav['order']}")
            for key in ("prev", "next"):
                if nav.get(key):
                    lines.append(f"{key}: {nav[key]}")
    lines += ["---", "", body, ""]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Docs information architecture
# --------------------------------------------------------------------------- #

def extract_nav(html: str) -> list[dict]:
    """Parse the docs sidebar into ordered sections.

    Returns [{"section": "Start here", "pages": [{"title": ..., "url": ...}, ...]}, ...]
    Each section is a <div> holding a <p> heading and a <ul> of links; the sidebar
    also contains a search button and dialog, which have neither and are skipped.
    """
    nav = BeautifulSoup(html, "lxml").select_one(SIDEBAR_SELECTOR)
    if nav is None:
        return []
    sections = []
    for block in nav.find_all("div", recursive=False):
        heading, links = block.find("p"), block.select("ul a[href]")
        if heading is None or not links:
            continue
        sections.append({
            "section": heading.get_text(strip=True),
            "pages": [
                {"title": a.get_text(strip=True), "url": canonical_url(urljoin(SITE, a["href"]))}
                for a in links
            ],
        })
    return sections


def nav_metadata(sections: list[dict], entries_urls: set[str]) -> dict[str, dict]:
    """Map each docs URL to its section, 1-based reading position, and neighbours.

    prev/next deliberately run across section boundaries, matching the site's own
    "Page navigation" control, so the corpus has one continuous reading sequence.
    """
    ordered = [
        (sec["section"], page["url"])
        for sec in sections
        for page in sec["pages"]
        if page["url"] in entries_urls
    ]
    meta: dict[str, dict] = {}
    for i, (section, url) in enumerate(ordered):
        meta[url] = {
            "section": section,
            "order": i + 1,
            "prev": _neighbour(ordered, i - 1, url),
            "next": _neighbour(ordered, i + 1, url),
        }
    # Pages the sitemap knows about but the sidebar omits. Discovery stays
    # sitemap-driven precisely so these are not lost: /docs/example-prompts is
    # reachable only from an inline link in getting-started.
    for url in sorted(entries_urls):
        if url.startswith(f"{SITE}/docs") and url not in meta:
            meta[url] = {"unlisted": True}
    return meta


def _neighbour(ordered: list[tuple[str, str]], index: int, from_url: str) -> str | None:
    """Relative .md path to the neighbouring page, or None at either end."""
    if index < 0 or index >= len(ordered):
        return None
    target = Path(url_to_relpath(ordered[index][1]))
    return Path(_relpath(Path(url_to_relpath(from_url)).parent, target)).as_posix()


# --------------------------------------------------------------------------- #
# URL / path helpers
# --------------------------------------------------------------------------- #

def canonical_url(url: str) -> str:
    """Normalize for set membership: drop query/fragment, drop trailing slash."""
    s = urlsplit(url)
    path = s.path.rstrip("/") or "/"
    return urlunsplit((s.scheme, s.netloc, path, "", ""))


def url_to_relpath(url: str) -> str:
    path = urlsplit(canonical_url(url)).path.strip("/")
    return "pages/index.md" if not path else f"pages/{path}.md"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #

@dataclass
class Fetched:
    url: str
    status: int
    html: str | None
    etag: str | None
    last_modified: str | None


@dataclass
class Changes:
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    unchanged: int = 0

    @property
    def total(self) -> int:
        return len(self.created) + len(self.updated) + len(self.deleted)


def discover_urls(client: httpx.Client) -> list[str]:
    index = client.get(SITEMAP_INDEX)
    index.raise_for_status()
    urls: list[str] = []
    for loc in ET.fromstring(index.content).findall(".//sm:sitemap/sm:loc", SITEMAP_NS):
        child = client.get(loc.text)
        child.raise_for_status()
        urls += [u.text for u in ET.fromstring(child.content).findall(".//sm:url/sm:loc", SITEMAP_NS)]
    if not urls:
        raise RuntimeError(f"sitemap at {SITEMAP_INDEX} yielded no URLs")
    return sorted({canonical_url(u) for u in urls})


def fetch(client: httpx.Client, url: str, etag: str | None, force: bool) -> Fetched:
    headers = {} if force or not etag else {"If-None-Match": etag}

    # Transient transport failures (read timeouts especially) are routine from CI
    # runners and would otherwise abort a whole run through pool.map. Retried with
    # linear backoff, then raised -- exhausting the budget is a real failure, not
    # something to swallow and mirror a partial corpus over.
    for attempt in range(1, FETCH_ATTEMPTS + 1):
        try:
            resp = client.get(url, headers=headers)
            break
        except httpx.TransportError as exc:
            if attempt == FETCH_ATTEMPTS:
                raise RuntimeError(
                    f"{url}: {type(exc).__name__} after {FETCH_ATTEMPTS} attempts"
                ) from exc
            print(
                f"warning: {url}: {type(exc).__name__}, retry {attempt}/{FETCH_ATTEMPTS - 1}",
                file=sys.stderr,
            )
            time.sleep(FETCH_BACKOFF * attempt)

    if resp.status_code not in (200, 304):
        raise RuntimeError(f"HTTP {resp.status_code} for {url}")
    final = canonical_url(str(resp.url))
    if final != url:
        # Warn rather than refile: filing under the redirect target would dangle every
        # local link pointing at the sitemap URL and pin force=True forever, and
        # skipping would silently drop pages whose target is not itself in the sitemap.
        print(f"warning: {url} redirected to {final} -- mirrored under the sitemap URL", file=sys.stderr)
    return Fetched(
        url=url,
        status=resp.status_code,
        html=resp.text if resp.status_code == 200 else None,
        etag=resp.headers.get("etag"),
        last_modified=resp.headers.get("last-modified"),
    )


# --------------------------------------------------------------------------- #
# Emitted aggregates
# --------------------------------------------------------------------------- #

SECTION_TITLES = {
    "docs": "Documentation",
    "blog": "Blog",
    "product": "Product",
    "": "Site",
}


def docs_reading_order(sections: list[dict], entries: dict[str, dict]) -> list[tuple[str, list[str]]]:
    """[(section title, [url, ...]), ...] in authored order, unlisted pages last."""
    grouped: list[tuple[str, list[str]]] = []
    placed: set[str] = set()
    for sec in sections:
        urls = [p["url"] for p in sec["pages"] if p["url"] in entries]
        if urls:
            grouped.append((sec["section"], urls))
            placed.update(urls)
    unlisted = [u for u in sorted(entries) if u.startswith(f"{SITE}/docs") and u not in placed]
    if unlisted:
        grouped.append(("Not in the sidebar", unlisted))
    return grouped


def build_llms_txt(entries: dict[str, dict], sections: list[dict]) -> str:
    """The index Straion publishes for marketing pages, extended to cover /docs.

    Docs follow the sidebar's authored sequence rather than alphabetical order:
    "Getting Started -> Prerequisites -> Core Concepts" is a curriculum, and
    sorting it destroys the only signal about where to start.
    """
    out = [
        "# Straion",
        "",
        "> Offline mirror of straion.com generated by sync.py from the",
        "> published sitemap. Unlike the upstream /llms.txt, this index covers",
        "> every /docs page and preserves the documentation's authored reading",
        "> order and section grouping. Full text: llms-full.txt",
        "",
    ]

    grouped = docs_reading_order(sections, entries)
    if grouped:
        out += ["## Documentation", "", "Listed in reading order, grouped as on the site.", ""]
        for section, urls in grouped:
            out.append(f"### {section}")
            for url in urls:
                meta = entries[url]
                desc = meta.get("description", "")
                out.append(f"- [{meta['title']}]({url}){f': {desc}' if desc else ''}")
            out.append("")

    rest: dict[str, list[str]] = {}
    for url in sorted(entries):
        if url.startswith(f"{SITE}/docs"):
            continue
        segments = urlsplit(url).path.strip("/").split("/")
        rest.setdefault(segments[0] if segments and segments[0] else "", []).append(url)
    for key in sorted(rest):
        out.append(f"## {SECTION_TITLES.get(key, key.replace('-', ' ').title())}")
        for url in rest[key]:
            meta = entries[url]
            desc = meta.get("description", "")
            out.append(f"- [{meta['title']}]({url}){f': {desc}' if desc else ''}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def build_llms_full(entries: dict[str, dict], out_dir: Path, sections: list[dict]) -> str:
    """Every page concatenated -- one paste-able file for a model's context.

    Docs come first and in reading order, so a model consuming this top-to-bottom
    encounters concepts in the sequence their authors intended.
    """
    grouped = docs_reading_order(sections, entries)
    docs_urls = [u for _, urls in grouped for u in urls]
    rest_urls = [u for u in sorted(entries) if u not in set(docs_urls)]

    parts = [
        "# Straion -- full documentation corpus",
        "",
        "Generated by sync.py from https://straion.com/sitemap-index.xml",
        "Documentation appears first, in the reading order published on the site.",
        "",
        "## Reading order",
        "",
    ]
    for section, urls in grouped:
        parts.append(f"**{section}**")
        parts += [f"{i}. {entries[u]['title']}" for i, u in enumerate(urls, 1)]
        parts.append("")

    for url in docs_urls + rest_urls:
        meta = entries[url]
        page_path = out_dir / meta["path"]
        if not page_path.exists():
            raise RuntimeError(
                f"{meta['path']} is in the manifest but missing from disk; "
                f"rerun without --only-docs to rebuild the full mirror"
            )
        page = page_path.read_text(encoding="utf-8")
        body = page.split("---", 2)[-1].strip()
        parts += [f"\n---\n\n# {meta['title']}", f"\nSource: {url}\n", body, ""]
    return "\n".join(parts).rstrip() + "\n"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def write_if_changed(path: Path, content: str, relpath: str, changes: Changes) -> str:
    """Write only on content change. Returns the sha256 either way."""
    digest = sha256_text(content)
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing is not None and sha256_text(existing) == digest:
        changes.unchanged += 1
        return digest
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    (changes.updated if existing is not None else changes.created).append(relpath)
    return digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent, help="output directory")
    parser.add_argument("--only-docs", action="store_true", help="mirror only /docs pages")
    parser.add_argument("--force", action="store_true", help="ignore ETags and re-extract every page")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed corpus matches a fresh build; writes nothing, exits 1 on drift",
    )
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    # --check builds cold into a scratch directory and diffs. Cold on purpose: it must
    # answer "does the committed corpus equal what the live site produces right now",
    # which a warm build reusing the committed manifest's ETags could not detect.
    committed_dir: Path = args.out
    scratch = Path(tempfile.mkdtemp(prefix="straion-check-")) if args.check else None
    out_dir: Path = scratch if scratch is not None else committed_dir
    manifest_path = out_dir / "manifest.json"
    log_path = out_dir / "sync-log.jsonl"
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    except json.JSONDecodeError as exc:
        # Deliberately not treated as "absent": that would convert visible corruption
        # into a silent full re-extraction. Name the escape hatch instead.
        raise RuntimeError(f"{manifest_path} is not valid JSON ({exc}); delete it to rebuild") from exc
    prev_entries: dict[str, dict] = manifest.get("entries", {})

    with httpx.Client(
        headers={"User-Agent": USER_AGENT},
        timeout=args.timeout,
        follow_redirects=True,
    ) as client:
        all_urls = discover_urls(client)
        urls = [u for u in all_urls if urlsplit(u).path.startswith("/docs")] if args.only_docs else all_urls
        if not urls:
            raise RuntimeError("no URLs selected -- check --only-docs filter")

        # Both of these are keyed on the FULL sitemap, never the filtered subset.
        # relpaths drives link rewriting, so narrowing it would turn cross-scope
        # links absolute on a filtered run and flip them back on the next full one;
        # url_set_changed would see every filtered run as a changed set and force a
        # permanent full re-extraction.
        relpaths = {u: url_to_relpath(u) for u in all_urls}

        # Internal links are rewritten to local paths, so a page's Markdown depends
        # on the whole URL set. If the set moved, 304s are no longer safe to trust.
        url_set_changed = set(all_urls) != set(prev_entries)
        force = args.force or url_set_changed
        if url_set_changed and not args.force:
            print("url set changed since last run -> re-extracting all pages", file=sys.stderr)

        def conditional_etag(url: str) -> str | None:
            """ETag to revalidate against, or None to force a full fetch.

            Only offered when the local file still matches what the manifest
            recorded. Verifying disk *before* the request means a 304 always
            means "trust disk" -- a locally edited or deleted page repairs
            itself instead of erroring out.
            """
            prev = prev_entries.get(url)
            if force or not prev or not prev.get("etag"):
                return None
            page = out_dir / prev["path"]
            if not page.exists() or sha256_text(page.read_text(encoding="utf-8")) != prev.get("sha256"):
                return None
            return prev["etag"]

        print(f"fetching {len(urls)} urls (concurrency={args.concurrency}, force={force})", file=sys.stderr)
        with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
            results = list(pool.map(
                lambda u: fetch(client, u, conditional_etag(u), force=False), urls
            ))

    # Read the sidebar before rendering, since every page's frontmatter carries its
    # place in the reading order. The sidebar is embedded in every docs page, so any
    # change to it changes every docs page's ETag -- whenever the structure moves we
    # necessarily have fresh HTML to re-read it from. If every docs page 304s, the
    # copy stored in the manifest is still accurate.
    docs_html = next(
        (r.html for r in results if r.html and urlsplit(r.url).path.startswith("/docs")), None
    )
    if docs_html is not None:
        nav_sections = extract_nav(docs_html)
        if not nav_sections:
            raise RuntimeError(
                f"docs sidebar {SIDEBAR_SELECTOR!r} matched nothing -- site structure changed"
            )
    else:
        nav_sections = manifest.get("nav", [])
    nav_meta = nav_metadata(nav_sections, set(all_urls))

    changes = Changes()
    entries: dict[str, dict] = {}
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    for res in results:
        relpath = relpaths[res.url]
        page_path = out_dir / relpath
        prev = prev_entries.get(res.url, {})

        if res.status == 304:
            # A conditional request was only sent for pages whose local copy was
            # already verified against the manifest, so 304 means the mirror is
            # authoritative. This is the early-stop: no parse, no convert.
            changes.unchanged += 1
            entries[res.url] = {**prev, "etag": res.etag or prev.get("etag")}
            continue

        if res.html is None:
            raise RuntimeError(f"{res.url}: HTTP 200 with no body")

        title, description, body = html_to_markdown(res.html, res.url, relpaths, relpath)
        content = render_page(title, res.url, description, body, nav_meta.get(res.url))
        digest = write_if_changed(page_path, content, relpath, changes)
        entries[res.url] = {
            "path": relpath,
            "title": title,
            "description": description,
            "sha256": digest,
            "etag": res.etag,
            "last_modified": res.last_modified,
            "fetched_at": now,
        }

    # Carry forward pages this run did not fetch but the sitemap still lists, so a
    # filtered run reports on its own scope without the prune below treating the rest
    # of the mirror as stale. Without this, --only-docs deletes 26 pages, drops them
    # from the manifest, and writes 26 false DELETED lines into the append-only log.
    if args.only_docs:
        in_sitemap = set(all_urls)
        entries = {**{u: e for u, e in prev_entries.items() if u in in_sitemap}, **entries}

    # Prune pages that left the sitemap.
    live = {out_dir / e["path"] for e in entries.values()}
    pages_root = out_dir / "pages"
    if pages_root.exists():
        for stale in sorted(pages_root.rglob("*.md")):
            if stale not in live:
                stale.unlink()
                # Logged at unlink time: once the file is gone the deletion cannot be
                # recovered from state, so it must not wait on a later write succeeding.
                changes.deleted.append(str(stale.relative_to(out_dir)))
        for d in sorted(pages_root.rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()

    write_if_changed(out_dir / "llms.txt", build_llms_txt(entries, nav_sections), "llms.txt", changes)
    write_if_changed(
        out_dir / "llms-full.txt", build_llms_full(entries, out_dir, nav_sections), "llms-full.txt", changes
    )

    # Log records change events only -- an unchanged run appends nothing. Written
    # BEFORE the manifest, which is the commit point: a crash in between can duplicate
    # a line on the next run, and over-reporting in an append-only journal is
    # recoverable where under-reporting is not.
    if changes.total:
        with log_path.open("a", encoding="utf-8") as fh:
            for event, paths in (("CREATED", changes.created), ("UPDATED", changes.updated), ("DELETED", changes.deleted)):
                for p in sorted(paths):
                    fh.write(json.dumps({"ts": now, "event": event, "path": p}) + "\n")
            fh.flush()

    # Written via a temp file and an atomic rename. The manifest is the only output
    # with no self-heal path: a truncated one aborts every later run at startup,
    # before the network is touched, with no CLI escape.
    manifest_tmp = manifest_path.with_name(manifest_path.name + ".tmp")
    manifest_tmp.write_text(
        json.dumps(
            {"version": 2, "site": SITE, "generated_at": now, "nav": nav_sections, "entries": entries},
            indent=2, sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    manifest_tmp.replace(manifest_path)

    print(
        f"{len(entries)} pages | created={len(changes.created)} "
        f"updated={len(changes.updated)} deleted={len(changes.deleted)} unchanged={changes.unchanged}",
        file=sys.stderr,
    )
    if scratch is not None:
        try:
            return report_drift(committed_dir, scratch)
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
    if not changes.total:
        print("no changes", file=sys.stderr)
    return 0


def report_drift(committed: Path, fresh: Path) -> int:
    """Compare a committed corpus against a fresh build. 0 if identical, 1 if not.

    manifest.json and sync-log.jsonl are excluded: both carry timestamps and history
    by design, so they differ on every run without indicating any content drift.
    """
    def corpus(root: Path) -> dict[str, str]:
        files = sorted(root.rglob("pages/**/*.md"))
        files += [root / name for name in ("llms.txt", "llms-full.txt") if (root / name).exists()]
        return {
            str(f.relative_to(root)): sha256_text(f.read_text(encoding="utf-8"))
            for f in files
        }

    have, want = corpus(committed), corpus(fresh)
    added = sorted(want.keys() - have.keys())
    removed = sorted(have.keys() - want.keys())
    changed = sorted(k for k in have.keys() & want.keys() if have[k] != want[k])

    if not (added or removed or changed):
        print(f"up to date: {len(want)} files match a fresh build", file=sys.stderr)
        return 0

    # Labels describe the observed difference, not a guessed cause: a file present in
    # the fresh build but not the corpus means either upstream added it or someone
    # deleted it locally, and the check cannot tell which.
    for label, paths in (
        ("in live site, missing from corpus", added),
        ("in corpus, no longer on live site", removed),
        ("content differs", changed),
    ):
        for p in paths:
            print(f"  {label}: {p}", file=sys.stderr)
    print(
        f"\nDRIFT: {len(added) + len(removed) + len(changed)} file(s) differ from the live site.\n"
        f"Run './sync.py' and commit the result.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
