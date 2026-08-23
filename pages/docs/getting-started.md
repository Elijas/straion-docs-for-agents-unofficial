---
title: "Getting started"
source: https://straion.com/docs/getting-started
description: "A step by step guide to set up Straion: import your rules, install the CLI, and connect your first AI coding agent in under five minutes."
section: "Start here"
order: 1
next: prerequisites.md
---

# Getting started

Straion keeps your coding agents aligned with your engineering standards.
To get set up, follow the steps below to create an account, install the CLI, and import your rules.

Before you begin, make sure you meet the [prerequisites](prerequisites.md): MacOS or Windows, Node.js v22+, and one of the supported coding agents: Claude Code, GitHub Copilot, and Cursor.

## 1. Sign up

Create an account at [straion.app](https://straion.app/auth/signup).

## 2. Install the CLI and log in

Install the Straion CLI with your package manager. You can find more information in the [npm listing](https://www.npmjs.com/package/@straion/cli).

**npm**

```bash
npm install -g @straion/cli
```

**pnpm**

```bash
pnpm add -g @straion/cli
```

Now log in and start the setup:

```bash
straion
```

If you are not logged in yet, this starts the login flow and then walks you through setup.

To log in without prompts, for example on a build machine, pass a Personal Access Token instead:

```bash
straion --token <your-token>
```

Get a token from your [User Settings](https://straion.app/auth/login?redirectUrl=%2Fsettings%2Fuser-tokens) or the [Getting Started](https://straion.app/auth/login?redirectUrl=%2Fgetting-started) page. The token inherits your permissions and can be scoped with an expiration date.

The CLI configures your agent during setup. See the [agent setup guide](troubleshooting.md#check-agent-setup) for how to verify your installation.

## 3. Import rules

Setup offers to import your existing standards: security requirements, architecture patterns or coding guidelines. You choose where those rules live.

**Rules as code in git.** Connect a repository and your rules live on a branch in your own repo, reviewed through pull requests. Connected rules become read-only in the Straion app, because git is the source of truth. See the [Connect a repository](connect-repository.md) guide.

**Rules in the Straion app.** Upload a file or paste text on your Rules page. Rules imported this way stay editable in the app. See the [Import rules](import-rules.md) guide for how the import flow works.

## 4. Start using Straion

Straion extends your coding agent with skills: specialized workflows that validate code against your rules, break down specs into tasks, and check pull requests for compliance. Skills are invoked using slash commands (e.g. `/developing-with-rules`), which guarantees the skill is loaded before your agent starts working. Any text after the slash command provides context for what the skill should do. Your agent may also invoke skills automatically based on your prompt and other skills it has loaded.

Find ready-to-use prompts to get the most out of Straion in the [example prompts](example-prompts.md) guide.

## Troubleshooting

Having issues? Check the [troubleshooting guide](troubleshooting.md) or reach out to support via email at [support@straion.com](mailto:support@straion.com) or on [Discord](https://discord.gg/KjgK5EHP74).
