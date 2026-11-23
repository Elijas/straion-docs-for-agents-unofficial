---
title: "Straion Now Supports Codex"
source: https://straion.com/blog/straion-now-supports-codex
description: "Straion now works with Codex. Your rules, Automode, and the audit trail work the same as in Claude Code, Cursor, and GitHub Copilot. Run straion setup and pick Codex."
---

[← Back to blog](../blog.md "Back to blog")

# Straion Now Supports Codex

November 18, 2026 · 3 min read · by  [Fabian Friedl](https://straion.com/blog/about/fabian-friedl)

AI Coding Agents  Codex  Straion  Product

## TLDR;

Straion now works with Codex. Your rules, Automode, and the audit trail work the same as in Claude Code, Cursor, and GitHub Copilot. Run straion setup and pick Codex.

Straion now works with Codex. Run `straion setup`, pick Codex, and your agent gets the same rules as everyone else on your team.

Most teams don’t use one coding agent. One developer likes Claude Code. Another lives in Cursor. A third switched to Codex last month. Your standards shouldn’t depend on that choice. A security rule is a security rule, whatever agent writes the code.

With Codex, Straion now supports Claude Code, Codex, Cursor, and GitHub Copilot. Your rules live in one place, and every agent gets them.

## What you get in Codex

Everything you know from the other agents.

**The rules for each task.** Codex asks Straion for the rules that fit the task. It gets those rules, and only those. The agent checks its plan against them before it writes code.

**The workflow skills.** `straion-implement`, `straion-check-compliance`, and `straion-import-rules` all work. Codex starts skills with `$` instead of `/`, so you type:

```text
$straion-implement add rate limiting to the login endpoint
```

**Automode.** Turn it on, and Codex looks up your rules in every session, without anyone calling a skill. If it changes code without looking, Straion sends it back once. The [Automode docs](../docs/automode.md) cover the details.

**The audit trail.** Codex records a decision for every rule Straion hands it. A violation gets fixed, or the agent asks you before an exception ships. If a turn changed files that no decision covers, Straion holds the turn until the agent records one. You read the trail with `straion audit view`. The [audit trail docs](../docs/audit-trail.md) explain how it works.

**Forks keep their history.** Fork a Codex session, and the new one starts with the decisions of the session it came from. You don’t approve the same exception twice.

## How it works under the hood

Codex supports plugins, hooks, and MCP servers. Straion uses all three.

`straion setup` installs the Straion plugin into Codex and links the Straion skills. The plugin’s hooks watch what the agent does. Before Codex applies a patch or runs a shell command, Straion checks it. If a patch touches several files, Straion checks each one. The agent records its decisions through Straion’s MCP server, so they land in the audit trail.

There is nothing to configure in Codex itself. Setup does it for you.

## Bring your rules over

Already have an `AGENTS.md`? Codex teams often do. Import it once, so nothing is lost:

```bash
straion import-rules
```

Pick Codex, and Straion starts it with the import skill. The agent finds your rule sources, turns them into structured rules, and uploads them. After that, Straion is the single source of truth. You can retire the `AGENTS.md`. The [import docs](../docs/import-rules.md) walk you through it.

## Getting started

1. Install Codex, version 0.162.1 or newer. On a Mac, the ChatGPT desktop app works too. It ships its own Codex, and Straion finds it.
2. Install the Straion CLI and log in. See [Getting Started](../docs/getting-started.md).
3. Run `straion setup` and pick Codex.
4. Start a new Codex session.

Already set up for another agent? Run `straion setup` again and add Codex. Your rules are already there.

---

## Stay on Track. Start for free.

See how Straion keeps your AI coding agent aligned with your standards.   
Set up takes
less than 5 minutes.

[Start free trial
→](https://straion.app/auth/signup) 

Works with Claude Code, Codex, GitHub Copilot & Cursor. No credit card required.

---

---

![Fabian Friedl](https://straion.com/.netlify/images?url=_astro%2Ffabian.Bq-43Efc.jpg&fm=jpg&w=500&h=500&dpl=6b04606167b333c09f6b189a) 

Written by Fabian Friedl

[← Back to blog](../blog.md "Back to blog")
