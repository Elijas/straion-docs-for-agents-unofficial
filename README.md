# straion-docs-for-agents (unofficial)

[![Refresh mirror](https://github.com/Elijas/straion-docs-for-agents-unofficial/actions/workflows/refresh.yml/badge.svg)](https://github.com/Elijas/straion-docs-for-agents-unofficial/actions/workflows/refresh.yml)
[![Verify mirror](https://github.com/Elijas/straion-docs-for-agents-unofficial/actions/workflows/verify.yml/badge.svg)](https://github.com/Elijas/straion-docs-for-agents-unofficial/actions/workflows/verify.yml)

Machine-readable mirror of [straion.com](https://straion.com) — all 43 pages, including
the full `/docs` set — as Markdown, plus a single-file corpus for pasting into a model's
context. **Auto-synced daily via GitHub Actions.**

**Unofficial.** Not affiliated with or endorsed by Straion. Content belongs to Straion;
this repository only reformats what is already published. Canonical source is always
[straion.com](https://straion.com).

## For agents

Read this first:

| File | Use it for |
|---|---|
| [`llms.txt`](llms.txt) | Index of every page, docs in authored reading order |
| [`llms-full.txt`](llms-full.txt) | Whole corpus (~36k words) in one file |
| [`pages/`](pages/) | One Markdown file per URL, offline-navigable |

Raw single-file corpus:

```
https://raw.githubusercontent.com/Elijas/straion-docs-for-agents-unofficial/main/llms-full.txt
```

**Prefer refreshing over trusting the cache.** The committed corpus is a convenience, not
the source of truth. If you can run commands, refresh first — it costs 43 conditional GETs
and usually transfers almost nothing:

```bash
./sync.py           # refresh in place; prints "no changes" when already current
./sync.py --check   # verify against the live site without writing; exit 1 on drift
```

Every page carries its own position in the docs, so a single file is useful without the
index:

```yaml
---
title: "Getting started"
source: https://straion.com/docs/getting-started
section: "Start here"
order: 1
next: prerequisites.md
---
```

## Why this exists

Straion publishes `/llms.txt`, but it indexes only the marketing surface — `/product`,
`/blog`, `/pricing`, `/security`, `/about-us` — with **zero `/docs` entries**.
`/llms-full.txt` is 404. This repository fills that gap and adds the documentation's
reading order, which the flat sitemap does not carry.

## Rebuilding

Requires [uv](https://docs.astral.sh/uv/). No install step — dependencies are declared
inline ([PEP 723](https://peps.python.org/pep-0723/)) and pinned in `sync.py.lock`.

```bash
./sync.py                    # refresh
uv run --locked ./sync.py    # refresh with exact locked dependencies
```

See [DESIGN.md](DESIGN.md) for why the mirror is built this way, what was measured,
and the audit findings behind the current behaviour.

**Rebuilds are deterministic.** Two independent cold builds are byte-identical to each
other and to the incrementally-maintained corpus. There is no path dependence: no sequence
of partial, filtered, or interrupted runs produces output differing from
`rm -rf pages && ./sync.py`. Only `manifest.json` timestamps and `sync-log.jsonl` carry
history.

Incrementality is two-layered — HTTP conditional GET avoids transferring unchanged pages,
and a sha256 of the *extracted Markdown* decides whether anything actually changed. The
hash covers the output rather than the fetched HTML because Astro embeds per-deploy noise
(island ids, asset fingerprints) that changes on every publish. Generated files therefore
contain no timestamps: a `fetched_at` in the frontmatter would make every file differ from
itself on every run.

`sync-log.jsonl` is append-only and records `CREATED` / `UPDATED` / `DELETED` only. A run
that changes nothing appends nothing.

## CI

Two workflows, doing deliberately different jobs:

- **`refresh.yml`** (daily at 06:17 UTC, or manual) rebuilds the corpus. If the live site
  has changed it opens a pull request and merges it, so every update to the cache has a
  reviewable diff and a trail back to the run that produced it. A run that changes nothing
  opens nothing.
- **`verify.yml`** (every push and PR) runs `./sync.py --check`. It fails if the committed
  corpus does not match a fresh build — catching both hand-edited cache files and upstream
  changes that the daily refresh has not yet picked up.

`verify` compares against the live site, so it can go red because Straion published
something, not because anything here is wrong. The daily refresh is what keeps that
window small; re-running it green is a one-command fix.

**The refresh PR is an audit trail, not a gate**, and it is worth knowing why before
trying to make it one. GitHub deliberately does not trigger workflows from events caused
by `GITHUB_TOKEN`, so `verify` never runs on a PR the refresh opens. Adding `verify` as a
required status check on `main` would therefore not gate those PRs — it would strand them,
waiting forever on a check that never starts. Gating them for real needs the refresh to
push under a PAT or a GitHub App, which is a credential this repo deliberately does not
have. What the PR buys today is a reviewable diff and a link back to the run that produced
it, which is what direct commits to `main` were missing.

**A failing refresh is loud.** If the sync breaks — the site restructures, Cloudflare
starts refusing the runner, a dependency stops resolving — the workflow opens an issue
labelled [`sync-failure`](../../issues?q=label%3Async-failure) with the error output, and
comments on that same issue on subsequent failures rather than filing duplicates. The next
successful refresh closes it. The mirror itself is never left half-written: a failed run
commits nothing, so `main` stays readable and merely goes stale.

**Testing the refresh without waiting for Straion.** Running the workflow manually with
`force_change: true` drops one page (`pages/docs/example-prompts.md`) after syncing, purely
so the run has a real change to carry through the PR path. The next refresh notices the
page is missing, re-fetches it, and restores it byte-for-byte — the two PRs net out to
nothing.

## Scope

Mirrors the 43 URLs in Straion's published sitemap. Images are referenced by absolute URL,
not downloaded. `robots.txt` permits all crawling (`Disallow:` empty); requests are made
8-at-a-time with a descriptive User-Agent, and conditional GETs mean a steady-state refresh
transfers almost nothing.

`/docs/example-prompts` is in the sitemap but absent from the site's sidebar, so it is
mirrored and marked `unlisted: true` rather than dropped.

## Licence

`sync.py` is MIT. The mirrored content in `pages/`, `llms.txt` and `llms-full.txt` is
Straion's and is reproduced here unmodified in substance for machine consumption. If
Straion would like this changed or taken down, open an issue.
