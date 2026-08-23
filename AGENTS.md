# Instructions for agents

This repository is a machine-readable mirror of straion.com. It exists to be read by you.

## Getting the content

1. **Refresh first if you can run commands.** The cache may be stale.
   ```bash
   ./sync.py
   ```
   Prints `no changes` when already current. Costs 43 conditional GETs; transfers almost
   nothing in the steady state. Requires [uv](https://docs.astral.sh/uv/).

2. **If you cannot run commands, read the committed files.** They are valid, just possibly
   behind. `manifest.json` records `generated_at` so you can judge staleness yourself.

3. **Read `llms-full.txt`** for the whole corpus in one file, or `llms.txt` for an index if
   you want to fetch selectively.

## Reading order

Documentation is ordered as the site's own sidebar orders it, not alphabetically:

```
Start here              Getting started → Prerequisites → Core concepts
Rules                   Import rules → Connect a repository → Rule file format → Best practices
Using Straion           Developing with rules → Validate specs → Validate implementation plans → Validate code
Organization & Account  Invite users → SAML SSO → SCIM provisioning
References              CLI reference → Troubleshooting
```

Each page's frontmatter carries `section`, `order`, `prev` and `next`, so a single file
tells you where it sits without the index. `prev`/`next` cross section boundaries as one
continuous 16-page chain.

`pages/docs/example-prompts.md` is marked `unlisted: true` — it is published but absent
from the sidebar, so it has no position in that chain.

## Do not

- **Do not hand-edit files in `pages/`, `llms.txt`, or `llms-full.txt`.** They are
  generated. `./sync.py --check` fails on any edit, and the next refresh overwrites it.
  Change `sync.py` instead.
- **Do not treat this as authoritative.** Canonical source is straion.com. This mirror can
  lag, and conversion from HTML is lossy at the margins (images are links, not files;
  inline-SVG illustrations are dropped).

## Verifying freshness

```bash
./sync.py --check    # exit 0 = corpus matches the live site; exit 1 = drift, with a file list
```

This builds cold into a scratch directory and diffs; it writes nothing to the repository.
