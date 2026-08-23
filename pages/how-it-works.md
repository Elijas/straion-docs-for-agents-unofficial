---
title: "Rules defined once.Applied exactlywhere they matter."
source: https://straion.com/how-it-works
description: "Straion selects rules by context, team, project, stack, and change type, then validates every AI task plan and PR against them. See the full mechanics."
---

How It Works

# Rules defined once. Applied exactly where they matter.

Your architecture decisions are invisible to AI agents by default. Straion makes them
enforceable at the plan stage, before a single line is written, and beyond.

[Get Started Free](https://straion.app/auth/signup)   [Explore the product](product.md)

the governance lifecycle

1. Import standards
2. Straion selects the rules needed for the task
3. Validate the plan before any code
4. Re-check the code after it's written

■ The Flow

## Step by step, from standard to shipped

Every task an AI coding agent touches follows the same path: plans are created, the
applicable rules are selected, validated against, and enforced. Built for scale, teams can
customize this workflow or plug it into their existing process.

1. ### Standards are imported and stored as structured rules

   Lead engineers, architects, and compliance teams use Straion's import mechanisms to add their engineering standards into one central rule hub. Rules are stored as structured policies built to be evaluated by agents: version controlled, permission controlled, and ranging from security guidelines to coding best practices. They can stay in your own Git provider, so rule changes are versioned and reviewed like code. This replaces scattered CLAUDE.md files, repo-level prompts, and wiki pages that agents never reliably read.
2. ### When a task starts, Straion retrieves only the relevant rules

   Context signals like team, repository, tech stack, and change type determine which rules are active for this task. A backend engineer adding a new API route gets authentication and rate limiting rules. A frontend engineer updating a component gets accessibility and design-library rules. Neither gets the other's noise.

   Context signals used for rule selection

   Team

   backend, frontend, platform, mobile

   Repository

   api-service, web-app, shared-lib

   Stack

   Go, Node, Python, React

   Task type

   new feature, refactor, bugfix
3. ### Straion validates the plan, surfaces precise fixes, and re-checks the result

   Before any code is written, the agent proposes a plan. Straion checks it against the retrieved rules. If the plan violates a rule (missing an auth check, skipping the repository pattern, bypassing a required abstraction) it's rejected and adjusted before a single line is written. Correcting intent costs one prompt; correcting code costs a review cycle. Every flag includes the rule that triggered it, where the problem is, and what to do: not "this may have a security issue" but "Route /api/users/export is missing auth.Require(), add it before handler registration."
 4. ### Code changes are checked

   After code is written, Straion analyzes the changes again. This catches issues that are
   hard to spot at the plan stage: a missing pagination boundary, a response that leaks
   PII, a query pattern that won't scale.

---

■ In practice

## What this looks like in the terminal

A rule carries the metadata Straion matches on. find-rules takes a proposed change and
returns the rules that apply to it.

rule definition in Straion

{

"statement": "MUST NOT enable compiler-specific language extensions.",

"meta": {

"tags": ["build", "portability"],

"languages": ["cpp"]

}

}

find-rules call

$ straion find-rules

--title "feat: add configurable alert threshold for over-temperature detection"

--body "The TMP116 alert pin fires when temperature crosses a high or low limit, but the
driver only exposes raw reads. The host MCU needs an over-temperature interrupt
instead of polling I2C. Proposed API: tmp116.setHighLimit(250.0f) and
tmp116.setAlertCallback(...). Acceptance criteria: write the limit registers via the
existing I2C abstraction, distinguish High / Low alerts, add unit tests, keep the
driver platform-agnostic."

--summary "Add setAlertCallback() to TMP116 driver so host MCU can respond to over/under
temperature events via interrupt rather than polling"

--files "TMP116/Inc/TMP116.hpp,TMP116/Src/TMP116.cpp,TMP116/Test/TMP116.test.cpp"

--tags "driver,embedded,cpp,testing,api"

--keywords "alert,callback,I2C,TMP116,temperature,threshold,interrupt,polling"

---

■ Getting Started

## How Straion Works

Set up Straion and start enforcing your coding standards in about five minutes.  
Your rules live in your own Git, reviewed like code. Here's the race plan.

1. ### Install the CLI

   Start your free trial, install the Straion CLI, and connect it to your coding agent. Straion works with GitHub CoPilot, Cursor and Claude
2. ### Connect Your Repo

   Straion creates a dedicated branch in your repo and migrates your AGENTS.md and CLAUDE.md files into rules. From then on a rule change is a commit and a pull request, reviewed like code.
3. ### AI Gets Context

   Straion's CLI dynamically fetches the relevant rules. Your AI knows your standards before writing code.
4. ### Validate & Ship

   Straion validates the AI's task plan against your rules. Catch violations before tokens are wasted.

---

## Thinking about building this yourself?

Rule retrieval, plan validation, structured policies, PR enforcement: the pieces look
manageable until you're six weeks deep and maintaining infrastructure instead of shipping
product.

[Read: Build vs. Buy for AI Coding Governance](blog/build-vs-buy-ai-coding-governance.md)

## Get started in under 5 minutes, stay on track as you scale

Your architecture rules, security policies, and coding standards, automatically in
every developer's AI agent from day one.

Works with Claude Code, GitHub Copilot & Cursor. No credit card required.

[Get Started Free
→](https://straion.app/auth/signup)

### Book a demo

We'll show you how Straion works with your AI coding setup and try it
with your team.
