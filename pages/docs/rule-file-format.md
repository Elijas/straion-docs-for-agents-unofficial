---
title: "Rule file format"
source: https://straion.com/docs/rule-file-format
description: "The on-disk layout and file format for rules stored in a connected git repository."
section: "Rules"
order: 6
prev: connect-repository.md
next: best-practices.md
---

# Rule file format

When you [connect a repository](connect-repository.md), your rules live in it as plain Markdown files. This page is the reference for that layout and file format: what a collection looks like, what a rule looks like, and the few things you need to get right when editing them by hand.

You rarely need to write these files from scratch: Straion’s import functionality produces rules in this format automatically. This page helps you read and edit what it generates.

## Layout

Rules live on the `straion/rules/v1` branch, under a top-level `rules/` directory. Each collection is a folder containing a `README.md` header and one Markdown file per rule:

```plaintext
rules/
  cpp-naming-conventions/
    README.md                        ← collection: name + description
    upper-case-constant-names.md     ← one rule
    lower-case-function-names.md
  cpp-build-and-tooling/
    README.md
    treat-compiler-warnings-errors.md
```

## Collection header (`README.md`)

Every collection folder has a `README.md` that names and describes the collection. The text below the frontmatter is the collection’s description:

```md
---
$schema: https://straion.com/schemas/rule-collection/v1.json
id: f11076d9-bcfc-4e0c-9b22-d0b628b4a86c
name: C++ Naming Conventions
meta:
  tags: [style, naming]
  languages: [cpp]
---

Identifier naming rules enforced by the project's `.clang-tidy`. Applies to all
C++ source; violations surface as warnings, which the build treats as errors.
```

## Rule file

Each rule is a single Markdown file. The text below the frontmatter is the rule statement, optionally followed by examples:

````md
---
$schema: https://straion.com/schemas/rule/v1.json
id: 61e9a038-948a-431d-b5e9-91d6eec9f82c
meta:
  tags: [naming, style]
  languages: [cpp]
---

MUST use UPPER_CASE for constant names.

## Examples

```cpp kind=compliant
constexpr int MAX_RETRIES = 3;
```

```cpp kind=violating
constexpr int maxRetries = 3;
```
````

## Things to get right

- **The rule statement is the text before the `## Examples` heading.** Start it with `MUST`, `MUST NOT`, or `SHOULD`. See [Best practices](best-practices.md) for how to phrase strong rules.
- **A rule’s identity is the `id` in its frontmatter, not its filename.** Renaming a file, or moving a rule between collections, keeps the same rule as long as the `id` stays the same. Renaming is safe.
- **Examples use fenced code blocks** tagged `kind=compliant` or `kind=violating`.
- **Tags and languages** in `meta` help Straion match the rule to the right work. Keep them accurate.

> **Caution: Don’t reuse an `id`.**
> Each rule and collection `id` must be unique. Copy-pasting a rule file without changing its `id` will cause that rule to be flagged as a conflict rather than synced. When you add a brand-new rule, give it a fresh UUID or let your agent generate one for you.

## Validate before you commit

To check that your files are well-formed before opening a pull request, run:

```bash
straion source repo sync --dry-run
```

It exits with a non-zero exit code and lists the violating files if anything is invalid, and uploads nothing. See [Connect a repository](connect-repository.md#step-3-sync-on-every-change) for how to run the same check automatically on every pull request.
