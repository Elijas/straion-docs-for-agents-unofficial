# Design notes

Why this mirror is built the way it is, and what was measured to justify it.

## Reading order

The sitemap is a flat alphabetical list. The docs sidebar is the *authored* information
architecture — five sections in a deliberate teaching sequence. Discarding it turns a
curriculum into an undifferentiated pile of pages, so the sidebar is parsed separately
from `nav[aria-label="Docs navigation"]` and used to order both emitted artifacts:

```
Start here              Getting started → Prerequisites → Core concepts
Rules                   Import rules → Connect a repository → Rule file format → Best practices
Using Straion           Developing with rules → Validate specs → Validate implementation plans → Validate code
Organization & Account  Invite users → SAML SSO → SCIM provisioning
References              CLI reference → Troubleshooting
```

Every docs page carries its own position in frontmatter, so a single file handed to a
model without an index still knows where it sits:

```yaml
section: "Start here"
order: 1
next: prerequisites.md
```

`prev`/`next` cross section boundaries, matching the site's own pager, giving one
continuous 16-page chain. Verified by walking it end to end.

**The sidebar orders; it never discovers.** `/docs/example-prompts` is in the sitemap and
linked inline from Getting started, but absent from the sidebar — sidebar-driven discovery
would silently lose it. It is mirrored, marked `unlisted: true`, and listed under "Not in
the sidebar" rather than being quietly dropped or silently interleaved.

The sidebar is embedded in every docs page, so any change to it changes every docs page's
ETag. Whenever the structure moves we necessarily have fresh HTML to re-read it from; when
every docs page 304s, the copy in `manifest.json` is still accurate. If the selector ever
matches nothing while docs HTML *is* in hand, the run fails loudly rather than silently
falling back to a stale map.

## Design notes

**Content-address the output, not the input.** The per-page hash is `sha256` of the
*extracted Markdown*, not of the fetched HTML. Astro embeds per-deploy noise in its
markup (island ids, asset fingerprints), so hashing HTML would report every page as
changed on every publish. Hashing the extracted prose means a redeploy with no editorial
change produces zero log lines.

**No timestamps inside generated files.** A `fetched_at` in the frontmatter would make
every file differ from itself on every run and defeat the mechanism entirely. Timestamps
live in `manifest.json` and `sync-log.jsonl`.

**Two-layer incrementality.** HTTP conditional GET (`If-None-Match`) avoids transferring
unchanged pages; the sha256 comparison is the authority on whether anything changed.

**The conditional header is only offered for verified-clean files.** Disk state is checked
against the manifest *before* the request. That inversion is what makes the mirror
self-healing: a locally edited or deleted page simply gets refetched, rather than the
server's 304 being trusted over a file that no longer matches. Verified — corrupting one
page and deleting another repairs exactly those two and leaves the other 43 on their 304
path.

**A changed URL set forces full re-extraction.** Because internal links are rewritten to
local paths, a page's Markdown depends on the whole URL set, so 304s stop being safe the
moment a page is added or removed.

**No bare `<article>` fallback.** Docs pages use `article.docs-article`; marketing pages
fall back to `<main>`, and a few (e.g. `/career`) to `<body>`. An `<article>` fallback
looks reasonable and is a trap — marketing pages use `<article>` for cards, so it matched
a single team-member tile instead of the page body. `<header>`/`<footer>` are stripped
only on the `<body>` path, where site chrome is in scope.

## Determinism and robustness

**Rebuilds are deterministic, and incremental state is provably equivalent to a cold
build.** Measured: two independent cold builds are byte-identical to each other, and both
are byte-identical to the incrementally-maintained mirror across all 43 pages, `llms.txt`
and `llms-full.txt`. There is no path dependence — no sequence of partial, filtered, or
interrupted runs leaves output that differs from `rm -rf out && sync`. Only `manifest.json`
timestamps and the append-only log carry history.

Dependencies are locked in `sync.py.lock` (`uv lock --script`). Use `uv run --locked` in CI
to make a drifted dependency a hard failure — verified enforced: hand-editing a version in
the lock causes `--locked` to reject the run.

### What happens when Straion changes their site

| Change | Behaviour | Loud? |
|---|---|---|
| Page added / removed / edited | Picked up from the sitemap; pruned pages logged `DELETED` | yes |
| Sitemap moved or unreachable | `raise_for_status` aborts before any writes | yes |
| Sidebar `aria-label` changes | `extract_nav` returns empty → run raises | yes |
| No content container matches | Raises `no content container found` | yes |
| `docs-article` class renamed | Falls back to `<main>` — measured byte-identical output, no chrome leak | n/a |
| Code-block language attribute renamed | Fences still emitted, silently **untagged** | **no** |
| Docs restructured into new sections | Sections/order follow automatically; every docs page's ETag changes, so nav is re-read | yes |

The one silent degradation is the last-but-one row: if Shiki stops emitting `data-language`,
code blocks stay intact but lose their language tags, and nothing complains. Everything
else either self-corrects or fails loudly before writing.

KNOWN UNKNOWN: the sidebar is read from whichever docs page happens to be fetched first in
a run. If Straion ever ships per-page sidebars, the captured nav becomes whichever page won
the race — currently safe because the sidebar is identical across all docs pages.


## Audit findings, fixed

A parallel audit compared every mirrored page against its live source and reviewed the
incremental logic. Twelve findings survived adversarial verification; two were refuted.
All are fixed:

- **`--only-docs` was destructive.** `entries` held only the URLs fetched that run, so the
  prune deleted the 26 non-docs pages, dropped them from the manifest, and wrote 26 false
  `DELETED` lines into the append-only log. Pages regenerate; the journal does not.
  Filtered runs now carry forward untouched entries, and `relpaths`/`url_set_changed` key
  off the full sitemap so alternating filtered and full runs don't churn.
- **Nested code fences shredded two docs pages.** `rule-file-format.md` teaches rule syntax
  by showing a Markdown file that itself contains ```` ```cpp ```` examples. markdownify
  always emits three backticks, so the outer fence closed at the first inner one and
  swallowed the remaining 19 lines — including the whole "Things to get right" section —
  into a single unlabelled code block, and propagated into `llms-full.txt`. `convert_pre`
  now widens the outer fence to N+1 backticks per CommonMark.
- **FAQ questions were deleted.** The site renders them as `<h3><button>text</button></h3>`,
  so the blanket `button` strip emptied the heading, leaving 9 bare `###` across three
  product pages. Buttons inside headings are now unwrapped before the strip. (Scoped to
  headings deliberately: unwrapping every button with text leaks close controls and
  duplicate CTAs into the body. The *answers* are never in the served HTML — they live in
  an astro-island props blob — so this yields questions only; full Q&A is in `faqs.md`.)
- **Same-page anchors pointed at the homepage.** `urljoin(SITE, "#frag")` canonicalizes to
  the site root, so 6 in-page anchors were rewritten to `index.md#…`. Fragment-only hrefs
  are now left as authored.
- **`manifest.json` is written atomically** via temp file + rename. It is the only output
  with no self-heal path — a truncated one aborts every later run at startup.
- **The log is written before the manifest**, which is the commit point. A crash between
  them can duplicate a line; over-reporting in an append-only journal is recoverable,
  under-reporting is not. Deletions are logged at unlink time.
- **`markdownify>=0.13` was a false floor** — the converter overrides pass `parent_tags=`,
  which did not exist before 1.0. Now `>=1.0,<2`.
- **Redirects warn** rather than refile, since refiling would dangle local links.

Two findings were correctly refuted, and the synthesis flagged one whose citations were
fabricated even though its conclusion held — worth noting that the reported *fix* for the
fence bug was also wrong (`count=2` hits the block's first inner fence, not its closer);
the unclosed-fence scan caught it. Verification: 44 files scanned, none ends inside an
unclosed fence; 0 bare `###`; 0 `index.md#` links; filtered/full runs alternate with zero
churn.

## Why not CocoIndex

Considered and rejected. CocoIndex's incrementality pays off when expensive per-item work
(embeddings, LLM extraction) runs over thousands of documents and you want lineage-tracked
memoization. Here the corpus is 43 pages, the transform is ~5 ms of HTML parsing, and the
output is Markdown files on disk. Its required Postgres state store would be operationally
heavier than the artifact it produces, in exchange for replacing roughly fifteen lines of
`sha256(content) == stored_hash`.

That calculus flips if this corpus ever gets embedded into a vector store, or if per-page
processing becomes an LLM call. Not at this scale.

## Politeness

`straion.com/robots.txt` is `Disallow:` (empty — everything permitted). Requests carry a
descriptive User-Agent, run 8-at-a-time, and conditional GETs mean a steady-state run
