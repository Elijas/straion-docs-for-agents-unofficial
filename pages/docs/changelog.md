---
title: "CLI changelog"
source: https://straion.com/docs/changelog
description: "Release notes for every version of the Straion CLI (@straion/cli). The latest release is 0.1.25, published November 4, 2026."
section: "References"
order: 21
prev: cli-api-reference.md
next: troubleshooting.md
---

# CLI changelog

Every release of the Straion CLI ([`@straion/cli`](https://www.npmjs.com/package/@straion/cli)), newest
first. Run this to update to the latest version:

```
npm install -g @straion/cli@latest
```

To hear about new releases, subscribe to the [RSS feed](https://straion.com/docs/changelog/rss.xml). The
[CLI reference](cli-api-reference.md) describes every command.

## 0.1.25

November 4, 2026

- **Feature:** Adds `straion audit notes rewrite`, which keeps line attribution when commits are squashed or rebased. Run it in CI on every push. It finds the commits to carry notes from on its own: a merged GitHub pull request or GitLab merge request (from the GitHub Actions event or the commit message), or the branch head before the push (GitHub Actions, GitLab, or `--before <sha>` on other CI). Each rebased commit gets its original’s note with the line numbers re-mapped, and a squash commit gets a note built from all the commits it combined.

## 0.1.24

November 3, 2026

- **Fix:** `straion setup` now finds Codex when only the ChatGPT desktop app for macOS is installed. It uses the Codex CLI the app ships when no working `codex` is on your PATH. Before, Codex showed as unavailable.

## 0.1.23

November 3, 2026

- **Fix:** When your git is too old for authorship notes and the commit check, `straion setup` now tells you how to fix it: upgrade git to 2.54 or newer, then run `straion setup` again. Setup also exits with a non-zero code when these hooks are not installed, so you and your scripts notice right away instead of finding out later that commits were never checked.
- **Fix:** `straion find-rules` now detects C correctly from the files you pass. `.c` files count as C, and a `.h` header counts as C++ only when you also pass C++ sources. Before, C files were not recognised and every header was treated as C++, so C tasks could be matched against C++ rules.

## 0.1.22

November 2, 2026

- **Feature:** `straion setup` supports Codex. It installs the straion plugin and skills, and its hooks gate `apply_patch` edits and shell commands, record verdicts through the MCP server, record edits for line attribution, and hold a turn whose changes no verdict covers. A forked Codex session starts with the verdicts of the session it was forked from.
- **Feature:** Removes the `--force` option from `straion setup`.

## 0.1.21

October 29, 2026

- **Feature:** Rule collections on the rules branch can sit in grouping folders at any depth, such as `rules/security/payments/`. A folder is a collection when its `README.md` declares a straion `$schema`; any other folder is a grouping folder the sync walks through. A collection’s folder path is its identity, so bindings name a nested collection by that path. Every `.md` file under `rules/` is now either synced or reported: a rule file outside a collection and markdown below a collection folder are validation errors. `straion import-rules` counts nested collections when deciding whether `--force` is needed.

## 0.1.20

October 27, 2026

- **Feature:** A recorded rule verdict goes stale only when a file the agent changed while working on that rule changes again, by the agent or by anyone else. Automode now holds a turn only when the agent changed files that no verdict covers and ran no `straion find-rules` call in that turn.

## 0.1.19

October 27, 2026

- **Feature:** Refuses an agent’s commit while a `gate: deny` rule in its session is still open, marked for fixing, or stale, and names each rule with the step that settles it. `straion setup` registers the check as a global git pre-commit hook next to the authorship notes hooks. It runs at audit mode `trail` or `gate`, lets commits outside an agent session through, and turns off with `git config --global hook.straion.enabled false`. The hook needs git 2.54 or newer; on older git, setup skips it and says so.

## 0.1.18

October 27, 2026

- **Feature:** Records which lines of a commit an agent wrote and attaches them to the commit as a git note in `refs/notes/ai`, in the git-ai authorship format. `straion setup` registers two global git hooks for this: one writes the note after each commit, the other pushes the notes with each push. The hooks need git 2.54 or newer; on older git, setup skips them and says so.

## 0.1.17

October 21, 2026

- **Fix:** CLI usage analytics and error reports now go to Straion’s EU PostHog project, so CLI telemetry stays in the EU.

## 0.1.16

October 21, 2026

- **Feature:** Directory settings (`automode`, `audit.mode` and the org from `straion switch --local`) now apply in every git worktree of a repository, also in worktrees outside the repository folder. `straion config` and `straion switch --local` run in a worktree save the setting for the main checkout, so it covers all worktrees and stays after a worktree is deleted.

## 0.1.15

October 20, 2026

- **Feature:** `straion find-rules` matches only the rules that apply to the repositories of the `--files` entries (or the working directory when none are given). Rules from a git source apply in its own repository; a central source’s bindings decide where its collections apply.

## 0.1.14

October 20, 2026

- **Feature:** Adds `straion source repo validate`, which checks the rule collections and `bindings/*.yaml` files of a rules branch. `straion source repo sync` now validates and uploads the binding files of a central source.

## 0.1.13

October 19, 2026

- **Feature:** `straion source repo connect` names the rule folders and files after the names Straion stores for them, so the first sync keeps the existing rules and their shortcodes. `straion import-rules` needs a `path` on each collection (for example `security/auth`) and a `slug` on each rule. A name that isn’t valid, or a rule slug used twice in a collection, skips that line; a collection path used twice stops the import before anything is uploaded.

## 0.1.12

October 19, 2026

- **Feature:** Identifies rule collections in a rules repository by their folder path under `rules/`, and rules by their file name. Folder and file names may use lowercase letters, digits and dashes, up to 80 characters. The frontmatter `id` is no longer needed: `straion source repo sync` prints a notice for files that still have one, and `connect` and `import-rules` no longer write it. Rules synced with an earlier version are created again on the first sync and get new shortcodes.

## 0.1.11

October 15, 2026

- **Chore:** Refine rule gate wording and restructure its content.

## 0.1.10

October 14, 2026

- **Feature:** Adds `--central` and `--no-central` to `straion source repo connect`. An organization admin can mark the connected repository as a central rule source, or clear the mark.

## 0.1.9

October 13, 2026

- **Feature:** The `straion-trail` pane remembers whether you opened or closed it in each session, also after a resume. A new **Pane** setting for `straion-trail` in Claude Code’s `/config` picks whether new sessions start with the pane open or closed.

## 0.1.8

October 5, 2026

- **Feature:** Adds the `straion-trail` Claude Code plugin. It opens a side pane that lists what Straion corrected the agent on and the exceptions you approved. Run `straion setup` to install it.

## 0.1.7

October 5, 2026

- **Feature:** Adds the `/straion-config` command for Claude Code, Cursor, and GitHub Copilot. It shows and changes your Straion settings from inside the agent. Run `straion setup` to install it.

## 0.1.6

October 5, 2026

- **Feature:** With automode on, hold a turn that changed files until the session has run find-rules, in every audit mode. A turn that commits or deletes files now counts as changing them.
- **Feature:** `straion config automode true` now switches automode on. The `STRAION_AUTOMODE_ENABLED` env var still wins when set, and `0` turns it off.

## 0.1.5

October 4, 2026

- **Fix:** Shorten the Stop hook block reason and the SessionStart rules index to save agent context.
- **Feature:** The record_verdict MCP tool now takes a list of verdicts, records them in one call, and asks once for every verdict that needs approval.

## 0.1.4

September 28, 2026

- **Feature:** Surface changed and deleted collections during repo sync.

## 0.1.3

September 27, 2026

- **Feature:** Adds a gate property that takes ´ask`and`deny` as values to control behavior of a of a recorded violation on a checkpoint.

## 0.1.2

September 25, 2026

- **Feature:** Adds the audit trail. Every rule `straion find-rules` returns now needs a verdict before the agent can end its turn. A rule is either met, or the agent picks fix, accept, or not applicable. The agent can fix a violation on its own. To accept one, or to call a rule not applicable, it has to ask you in its own approval prompt, and the trail records whether a person was asked. Changing code after a decision reopens it. Read a session with `straion audit list` and `straion audit view <id>`. The gate runs in Claude Code, Cursor, and GitHub Copilot.

To record decisions without being asked, set `audit.mode` to `trail` in `~/.straion/config.json`. To turn the trail off, set it to `off`.

## 0.1.1

September 23, 2026

- **Feature:** Adds the references array to the rules format to be able to reference external standards and rules.

## 0.1.0

September 21, 2026

- **Fix:** Claude Code skills now install into `~/.claude/skills` instead of the straion plugin directory. Claude Code copies an installed plugin into a version-pinned cache and drops symlinked directories on the way, so the installed plugin carried no skills at all: they loaded only because Claude Code also resolves the marketplace checkout in place. Run `straion setup` once to move them; skills left inside the plugin by an earlier run are removed, so nothing loads twice.
- **Refactor:** Every skill is now prefixed with `straion-` and two got renamed.
- `import-rules` → `straion-import-rules`
- `validating-rules` → `straion-check-compliance`: it checks code against your rules, not the rules themselves
- `developing-with-rules` → `straion-implement`: names the staged implementation workflow it runs

Invoke the import flow as `/straion-import-rules`. `straion setup` removes the old names and updates the skills in your agents.

## 0.0.31

August 27, 2026

- **Feature:** Adds per-directory organization overrides and a git-style `config` command: different repositories can now use different organizations and settings without touching your global setup, which is especially handy when the CLI is invoked by coding agents across multiple projects.

**`switch --local`**: Pin the active organization to the current directory (and its subdirectories) instead of switching globally

- `switch --local`: pick the organization interactively; the choice is stored only for this directory
- `switch --local --org <subdomain>`: same, non-interactive
- `switch --unset-local`: remove the override and use the global organization again

**`config`**: Get and set straion settings, git-config style. Note the scopes mirror the GitHub CLI: `config` is directory-scoped by default and needs `--global` to apply everywhere, while `switch` is global by default and needs `--local` to scope to a directory. The organization itself is managed via `switch`.

- `config <key>`: print the effective value (directory override first, then global)
- `config <key> <true|false>`: set for the current directory
- `config --global <key> <true|false>`: set globally
- `config --unset <key>`: remove the key from the selected scope (add `--global` for the global one)
- `config list`: print all settings, marking unconfigured ones as `(unset)`; `config list --global` shows only the global scope

## 0.0.30

August 26, 2026

- **Fix:** Stored credentials no longer invalidate when the machine’s hostname changes. Credentials now live in a plaintext file with owner-only permissions (`~/.straion/credentials.json`, mode 0600): the same model the AWS CLI uses: instead of an encrypted file whose machine-derived key macOS could silently rotate on every network change. An existing encrypted credentials file is migrated automatically on first read; only files whose key already drifted require one fresh `straion login`.

## 0.0.29

August 23, 2026

- **Fix:** Fixes an issue where the cli bin was not runnable.

## 0.0.28

August 20, 2026

- **Feature:** Adds automode session-start hooks for Claude Code, Cursor, and GitHub Copilot. When enabled, every session starts with a blueprint of the organization’s rule domains and how to fetch the applicable rules: no straion skill needs to be invoked manually (opt-in via `STRAION_AUTOMODE_ENABLED=1`).

## 0.0.27

August 19, 2026

- **Fix:** Ensures debug level logs are written to .straion/logs

## 0.0.26

August 14, 2026

- **Feature:** Adds permission checks & user feedback regarding the subscription while performing operations on the CLI

## 0.0.25

August 11, 2026

- **Refactor:** Bundles the cli into one executable binary. Ships third party licenses inside the package. Significantly reduced time to execute cli commands.

## 0.0.24

July 29, 2026

- **Feature:** Adds `source repo connect` and `source repo sync` commands to enable git synced rules.

**`source repo connect`**: Connect this repository as a rule source

- `--remote <name>`: Git remote to push the rules branch to (default: `origin`)
- `--sample`: Add an example collection to the rules branch
- `--no-sample`: Create an empty rules branch (skips the initial sync)

**`source repo sync`**: Synchronize rules from the connected source to Straion

- `--dry-run`: Validate the rules tree locally and print results; no upload
- `--remote <name>`: Git remote to read the rules branch from (default: `origin`)

## 0.0.23

July 21, 2026

- **Feature:** Adds `--agent <ids...>` flag to the `setup` command to enable setup in non interactive environments.

## 0.0.22

July 17, 2026

- **Fix:** Ensures trusted publishing.

## 0.0.21

July 17, 2026

- **Refactor:** Prep for audit command.
- **Fix:** `straion setup` no longer fails on Windows with `EPERM: operation not permitted, symlink` when installing skills. Windows restricts symlink creation to administrators (or requires Developer Mode), so skills are now linked via directory junctions, which standard users can create. Affected users can simply re-run `straion setup`.

## 0.0.20

June 30, 2026

- **Fix:** Fixes an issue where the organization always used default organization when a STRAION_API_KEY was set. Ingoring the STRAION_ORG_ID or any stored credentials.

## 0.0.19

June 26, 2026

- **Feature:** Adds frameworks as parameter to find-rules call.
- **Feature:** Provides proper feedback when rules are malformed to the agent.

## 0.0.18

June 17, 2026

- **Fix:** `find-rules` now requires non-empty `--title` and `--body` so an empty task description fails fast instead of returning no rules.

## 0.0.17

June 17, 2026

- **Fix:** detect GitHub Copilot CLI shims and preserve user-installed skills

## 0.0.16

June 9, 2026

- **Fix:** CLI setup bug where existing agent-integrations folder caused missing import-rules skill and failed agent spawn

## 0.0.15

June 3, 2026

- **Fix:** Fixes an issue where a request was sent with outdated credentials.
- **Refactor:** Changes handling of skills. Skills are now shipped inside the cli bundle and installed from the bundle instead of downloading the skill from Github.
- **Feature:** Updates the import-rules capability to use additional files to gather rules and add additional metadata for improved matching and importing rules.
- **Feature:** Adds scope metadata to find-rules command.
- **Feature:** Adds CLI rule import workflow with agent selection

## 0.0.14

April 28, 2026

- **Internal:** Allows local version of agent integrations to be used.

## 0.0.13

April 20, 2026

- **Feature:** Adds version check to showcase minimum supported versions.
- **Fix:** Fixes an issue where the setup command exited before the final result was printed to the terminal.
- **Fix:** Removes session options from find-rules since this is not needed and caused some issues in some agents where the session id was not set correctly.

## 0.0.12

April 9, 2026

- **Feature:** Adds trajectory hooks for copilot

## 0.0.11

April 8, 2026

- **Feature:** Adds cursor hook integration

## 0.0.10

April 3, 2026

- **Feature:** Adds experimental opencode support to the CLI.

## 0.0.9

March 24, 2026

- **Feature:** Adds trajectory collection command + Claude SessionEnd hook integration

## 0.0.8

March 9, 2026

- **Feature:** Add PostHog analytics tracking to the CLI with an opt-out via the `STRAION_ANALYTICS_DISABLED=1` environment variable.

## 0.0.7

February 24, 2026

- **Feature:** Adds switch command that allows switching organisations.
- **Feature:** Improves initial setup flow by showing example prompts to have better guidance for first time users.

## 0.0.6

February 21, 2026

- **Refactor:** Rename requirements to rules.

## 0.0.5

February 18, 2026

- **Feature:** Adds token flag to default command `straion` to allow for direct login during onboarding.

## 0.0.4

February 9, 2026

- **Chore:** Updates and cleans up dependencies.
- **Fix:** Switches credentials to use locally encrypted file instead of accessing keychain using sunsetted `keytar` dependency. Keychain access caused exceptions in some cases where some libraries from the operating system where incompatible and caused exceptions.

## 0.0.3

February 4, 2026

- **Feature:** Adds first time setup flow and setup command.
- **Chore:** Uses SPDX identifier for license reference.
- **Chore:** Removes `--output-format` flag since it was not useful and introduced unnecessary complexity.

## 0.0.2

January 30, 2026

- **Fix:** Fixes issues when running in non interactive terminals
- **Feature:** Adds support to login with the STRAION_API_KEY environment variable
- **Feature:** Adds `--output-format` flag to all commands that accepts `json` and `text` values. It uses `text` by default which renders a rich terminal user interface.

## 0.0.1

January 26, 2026

- Initial release with login, logout, and session management
- Added find-requirements command
