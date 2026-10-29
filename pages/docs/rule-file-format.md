---
title: "Rule file format"
source: https://straion.com/docs/rule-file-format
description: "The on-disk layout and file format for rules stored in a connected git repository."
section: "Rules"
order: 6
prev: connect-repository.md
next: rule-bindings.md
---

# Rule file format

When you [connect a repository](connect-repository.md), your rules live in it as plain Markdown files. This page is the reference for that layout and file format: what a collection looks like, what a rule looks like, and the few things you need to get right when editing them by hand.

You rarely need to write these files from scratch: Straion’s import functionality produces rules in this format automatically. This page helps you read and edit what it generates.

## Layout

Rules live on the `straion/rules/v1` branch, under a top-level `rules/` directory. Each collection is a folder with a `README.md` header and one Markdown file per rule:

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

The `README.md` is what makes a folder a collection: its frontmatter declares the Straion `$schema` shown in the next section.

A central source can also have a `bindings/` folder next to `rules/`. See [Rule bindings](rule-bindings.md) and the [Binding file reference](binding-file-reference.md).

### Group collections in folders

As your rule set grows, a flat list of collections gets hard to navigate. Put collections in plain folders to organize them by team, domain, or product area, as deep as you like:

```plaintext
rules/
  security/
    payments/
      README.md                      ← collection: name + description
      never-log-card-numbers.md
    auth/
      README.md
      require-mfa-for-admins.md
  cpp-naming-conventions/
    README.md
    upper-case-constant-names.md
```

A grouping folder needs nothing special. It has no `README.md`, or a `README.md` without a Straion `$schema`, so you can keep an ordinary README or an owners file in it for your own readers. Straion looks past grouping folders and finds the collections inside them.

Grouping only changes where a collection sits in your repository. In the Straion app, collections still appear as one flat list. Rules created by the import land directly under `rules/`. You can move them into folders, but a move gives the collection a new identity. See [How Straion identifies rules](#how-straion-identifies-rules). A [binding](binding-file-reference.md) refers to a collection by its path, for example `security/payments`.

Two things to keep in mind:

- **A collection holds its rules directly.** Don’t put rule files or other collections in a subfolder of a collection. The sync rejects them.
- **Every rule file needs a collection.** A rule file in a grouping folder is rejected. Add a `README.md` with the `$schema` to turn that folder into a collection.

## Collection header (`README.md`)

Every collection folder has a `README.md` that names and describes the collection. The text below the frontmatter is the collection’s description:

```md
---
$schema: https://straion.com/schemas/rule-collection/v1.json
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

### Gate

The optional `gate` field sets what happens when the agent wants to leave a violation of this rule unfixed:

| Value | Meaning |
| --- | --- |
| `ask` | Default. You approve or reject the violation in your coding agent’s approval prompt. |
| `deny` | Nobody can accept a violation. The agent has to fix the code. |

```md
---
$schema: https://straion.com/schemas/rule/v1.json
gate: deny
meta:
  tags: [security]
---

MUST NOT write access tokens to logs.
```

Leave `gate` out to get `ask`. Other values are errors. `gate` is set per rule: a collection `README.md` with a `gate` is rejected. See [Rules that can’t be accepted](audit-trail.md#rules-that-cant-be-accepted) for how each value works in the audit trail.

## Things to get right

- **The rule statement is the text before the `## Examples` heading.** Start it with `MUST`, `MUST NOT`, or `SHOULD`. See [Best practices](best-practices.md) for how to phrase strong rules.
- **Examples use fenced code blocks** tagged `kind=compliant` or `kind=violating`.
- **Tags and languages** in `meta` help Straion match the rule to the right work. Keep them accurate.

## How Straion identifies rules

A collection is identified by its folder path under `rules/`, for example `security/payments`. A rule is identified by its file name inside its collection, for example `never-log-card-numbers`. The path is the identity, so files don’t need an `id`.

- **Name folders and files with lowercase letters, digits, and `-`.** Start with a letter or a digit. Each name can be up to 80 characters. The sync rejects other names and tells you which path is wrong.
- **Each path is unique.** Two collections can’t have the same path, and two rules in one collection can’t have the same file name.

> **Caution: Renaming or moving creates a new rule.**
> When you rename a rule file or move it to another collection, Straion deletes the old rule and creates a new one with a new shortcode. The same happens to every rule in a collection when you rename or move the collection folder. Update any [binding](binding-file-reference.md) that lists the old collection path.

Older files can still have an `id` in their frontmatter. Straion ignores it, and `straion source repo sync` prints a notice for each of those files. You can delete the line.

## Validate before you commit

To check that your files are well-formed before opening a pull request, run:

```bash
straion source repo sync --dry-run
```

It exits with a non-zero exit code and lists the violating files if anything is invalid, and uploads nothing. See [Connect a repository](connect-repository.md#step-3-sync-on-every-change) for how to run the same check automatically on every pull request.
