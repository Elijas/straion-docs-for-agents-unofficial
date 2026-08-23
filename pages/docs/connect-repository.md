---
title: "Connect a repository"
source: https://straion.com/docs/connect-repository
description: "Store your rules as code in your own git repository and keep them in sync with Straion."
section: "Rules"
order: 5
prev: import-rules.md
next: rule-file-format.md
---

# Connect a repository

Connecting a repository lets you keep your rules **as code, in your own git repository**. You review them through your normal git workflow (pull requests, code review, branch protection) and Straion keeps a read-only copy in sync so your agents always match against the current rules.

This is a good fit when you want your rules to live alongside your code, be versioned in git, and be governed by the same review process as everything else in the repository.

## How it works

- Your rules are plain Markdown files on a dedicated branch in your repository. Your git history is the source of truth.
- You edit them through normal pull requests. Your existing branch protection and [CODEOWNERS](https://docs.github.com/articles/about-code-owners) govern who can change what.
- A sync step, run in your CI/CD pipeline or locally, sends the current rules to Straion, where they become available to your agents for matching and validation.

Straion never needs write access to your repository. The sync runs inside your own environment and only sends your rules.

## Prerequisites

- The Straion CLI installed. See [Getting Started](getting-started.md).
- An access token. We recommend using an *Organization Access Token* to use in CI. Creating an Organization Access Token requires certain permissions. [Organization Token](https://straion.app/organization/tokens).
- git 2.42 or newer, and a configured git identity (`user.name` and `user.email`) on the machine where you run `straion source repo connect`.

## Step 1: Connect the repository

From inside a checkout of the repository you want to connect, run:

```bash
straion source repo connect
```

This creates a dedicated `straion/rules/v1` branch in your repository, writes your rules to it as Markdown files, pushes the branch, registers the repository as a synced rule source, and runs the first sync.

> **Note: Previously imported rules are moved into the branch automatically.**
> If you have already imported rules from this same repository, `connect` **moves those existing rules** onto the new `straion/rules/v1` branch. You don’t re-create them, and no duplicates are created: the same rules simply become code in your repository. From this point on, they are managed through git.

> **Caution: Connected collections become read-only in the Straion app.**
> Once a repository is connected, the rules and collections that come from it can no longer be edited or deleted inside the Straion web app. Git becomes the single source of truth. Rules imported from files or pasted text are unaffected and stay editable in the app. See [Core Concepts](core-concepts.md) for the difference between rule source types.

### Starting from an empty repository

If Straion doesn’t hold any rules for the repository yet, `connect` creates an empty rules branch for you to add rules to. To include a small example collection so you can see the expected layout, pass `--sample`:

```bash
straion source repo connect --sample
```

## Where your rules live

Your rules live on the `straion/rules/v1` branch, under a top-level `rules/` directory. Each collection is a folder containing a `README.md` header and one Markdown file per rule:

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

See [Rule file format](rule-file-format.md) for the full anatomy of a collection frontmatter header and a rule file, and the handful of things to get right when editing them by hand.

## Step 2: Author rules through git

Because your rules are just files on a branch, you change them the same way you change code:

1. Branch off `straion/rules/v1`.
2. Add, edit, or remove rule files.
3. Open a pull request and get it reviewed.
4. Merge.

You can validate your changes locally before opening a PR:

```bash
straion source repo sync --dry-run
```

`--dry-run` checks that every rule and collection is well-formed and prints the results **without uploading anything**. It exits with non-zero exit code if any file is invalid.

## Step 3: Sync on every change

Add a sync step to your CI/CD pipeline so that whenever a change lands on the rules branch, Straion picks it up automatically.

Store your Access Token as a CI secret named `STRAION_API_KEY`. The CLI reads it automatically, so no interactive login is needed.

You can use the CLI and the sync command in any CI/CD pipeline. You can find example setups for different providers in the following section:

### GitHub Actions

Create `.github/workflows/straion-rules-sync.yml` on the `straion/rules/v1` branch:

```yaml
name: Sync rules to Straion

# Run on every push (merge) to the rules branch.
on:
  push:
    branches:
      - straion/rules/v1

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 24
      - run: npm install -g @straion/cli
      - name: Sync rules to Straion
        run: straion source repo sync
        env:
          STRAION_API_KEY: ${{ secrets.STRAION_API_KEY }}
```

### Validate rules on pull requests

Run a dry-run on every PR that targets the rules branch so invalid rules are caught in review, before they merge:

```yaml
name: Validate rules

on:
  pull_request:
    branches:
      - straion/rules/v1

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-node@v5
        with:
          node-version: 24
      - run: npm install -g @straion/cli
      - name: Validate rules
        run: straion source repo sync --dry-run
        env:
          STRAION_API_KEY: ${{ secrets.STRAION_API_KEY }}
```

Mark this check as required in your branch protection settings to block merges when a rule is malformed.

### Other CI providers

The sync is a single CLI command, so it works in any CI system. For example, in GitLab CI:

```yaml
straion-rules-sync:
  image: node:24
  rules:
    - if: $CI_COMMIT_BRANCH == "straion/rules/v1"
  script:
    - npm install -g @straion/cli
    - straion source repo sync
  # Set STRAION_API_KEY as a CI/CD variable in project settings (mark it masked so it stays hidden in logs).
```

## Governance

Because your rules live in your repository, you govern them with the tools you already use:

- **Require review** on the `straion/rules/v1` branch with branch protection.
- **Assign ownership** of rule folders with `CODEOWNERS`, so the right people approve changes to each collection.
- **Audit history** through your normal git log. Every rule change is a reviewed commit.

Straion does not run a separate approval process. Whatever your repository accepts is what gets synced.

## Good to know

- **Re-running a sync is safe.** Syncing the same commit again does nothing. There’s no harm in running the sync again, or on a schedule, as a safety net that keeps the branch and Straion in step.
- **A sync can’t accidentally wipe your rules.** If a sync would empty out or drastically shrink a rule set that wasn’t empty before, it is held back rather than applied, and the sync in your CI still succeeds. This protects you from a misconfigured branch deleting everything.
- **The initial sync is separate from connecting.** If the first sync after `connect` reports an error, your repository is still connected. Fix the reported files and run `straion source repo sync` again.

## Command reference

| Command | What it does |
| --- | --- |
| `straion source repo connect` | One-time setup: create and push the rules branch, move existing rules into it, register the source, run the first sync. |
| `straion source repo connect --sample` | Same, but seed an empty repository with an example collection. |
| `straion source repo sync` | Read the rules branch and upload the current rules to Straion. Run this in CI. |
| `straion source repo sync --dry-run` | Validate the rules locally and print the results without uploading. Use it on pull requests. |

Both commands accept `--remote <name>` if you push to a remote other than `origin`.
