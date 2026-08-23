---
title: "CLI reference"
source: https://straion.com/docs/cli-api-reference
description: "Reference for every Straion CLI command: login, logout, setup, and import-rules, with the options and flags each command accepts."
section: "References"
order: 15
prev: scim.md
next: troubleshooting.md
---

# CLI reference

A complete reference for the `straion` CLI. Install it with `npm install -g @straion/cli` — see the [Getting Started](getting-started.md) guide for full setup instructions.

---

## `straion`

Running `straion` with no subcommand opens the interactive dashboard. If you are not logged in, it starts the login flow. If you are already logged in, it shows your current status and next steps.

```plaintext
straion
```

---

## `straion login`

Authenticate with your Personal Access Token. On success, credentials are stored securely on your machine and the selected organization is set as the default.

```plaintext
straion login [options]
```

**Options**

| Option | Description |
| --- | --- |
| `--org <subdomain>` | Organization subdomain to activate after login — skips the org selection prompt |

**Examples**

```bash
# Interactive login
straion login

# Select org in one step
straion login --org acme
```

---

## `straion logout`

Clear stored credentials and reset the active organization.

```plaintext
straion logout
```

---

## `straion setup`

Configure your coding agents (Claude Code, Cursor, GitHub Copilot, etc.) to use Straion. Runs an interactive wizard that installs the required skills and hooks for each agent you select.

```plaintext
straion setup
```

---

## `straion import-rules`

Extract rules from the current repository’s instruction files and upload them as structured collections. This command is normally invoked for you by the `/straion:import-rules` agent skill rather than run by hand. Requires a git repository with an `origin` remote.

```plaintext
straion import-rules [options]
```

**Options**

| Option | Description |
| --- | --- |
| `--force` | Re-run extraction and overwrite the existing collections for the repository |
| `--skip-precheck` | Skip the check for existing rules and go straight to discovering sources |

---

## `straion source repo connect`

One-time setup for storing your rules as code in your own git repository. Creates and pushes a dedicated `straion/rules/v1` branch, moves any previously imported rules from this repo onto it, registers the repository as a synced rule source, and runs the first sync. Run it from inside a checkout of the repository. Requires git 2.42 or newer and a configured git identity.

```plaintext
straion source repo connect [options]
```

**Options**

| Option | Description |
| --- | --- |
| `--sample` | Seed an empty repository with an example collection to show the layout |
| `--remote <name>` | Use a remote other than `origin` |

**Examples**

```bash
# Connect the current repository
straion source repo connect

# Connect and seed an example collection
straion source repo connect --sample
```

---

## `straion source repo sync`

Read the `straion/rules/v1` branch and upload the current rules to Straion. Run it in CI on every change to the rules branch. It reads the access token from the `STRAION_API_KEY` environment variable, so no interactive login is needed.

```plaintext
straion source repo sync [options]
```

**Options**

| Option | Description |
| --- | --- |
| `--dry-run` | Validate every rule and collection and print the results without uploading. Exits non-zero if any file is invalid |
| `--remote <name>` | Use a remote other than `origin` |

**Examples**

```bash
# Upload the current rules
straion source repo sync

# Validate locally without uploading
straion source repo sync --dry-run
```

---

## `straion switch`

Change the active organization. With no flags, an interactive selector is shown.

```plaintext
straion switch [--org <subdomain>]
```

**Options**

| Option | Description |
| --- | --- |
| `--org <subdomain>` | Organization subdomain to switch to directly — skips the interactive selector |

**Examples**

```bash
# Interactive org selector
straion switch

# Non-interactive
straion switch --org acme
```

---

## Global Options

These options are available on every command.

| Option | Description |
| --- | --- |
| `--version` | Print the installed CLI version |
| `--help` | Show help for any command |
| `--token <token>` | Personal Access Token — use this to pass a token directly without logging in |
