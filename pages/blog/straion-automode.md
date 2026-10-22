---
title: "Automode: Straion Now Runs in Every Session"
source: https://straion.com/blog/straion-automode
description: "With Automode, your coding agent looks up your Straion rules in every session, without anyone calling a skill. If it skips that step, Straion sends it back."
---

[← Back to blog](../blog.md "Back to blog")

# Automode: Straion Now Runs in Every Session

October 12, 2026 · 5 min read · by  [Lukas Holzer](https://straion.com/blog/about/lukas-holzer)  and  [Fabian Friedl](https://straion.com/blog/about/fabian-friedl)

AI Coding Agents  Engineering Leadership  Straion  Product

## TLDR;

With Automode, your coding agent looks up your Straion rules in every session, without anyone calling a skill. If it skips that step, Straion sends it back.

> **Update, October 12:** You can now watch Straion work live in Claude Code. Our new Claude Code mod, straion-trail, shows what Straion corrected while the agent works. It also tells you when the agent waits for your approval. [Read the announcement](audit-trail-in-claude-code.md).

Until today, Straion helped when you asked it to. The agent pulled your rules when you ran one of Straion’s skills, like `/straion-implement`. Skip the skill, and the agent wrote code from whatever happened to be in its context.

Automode closes that gap. Turn it on, and your agent asks Straion for your rules in every session, before it changes your code. You don’t type anything new. You give the agent a task, and it gets the rules for that task first.

## A quick fix, twice

Say your team writes C++ firmware and follows CWE. One of your rules:

```text
MUST NOT copy into a fixed-size buffer without checking the input's length (CWE-120).
```

A developer asks the agent to add the device name to the status message. It’s a small task, so they don’t call a skill. The agent copies the name into a 32-byte buffer with `strcpy`. It compiles, and it works on the test board. It never checks the length, because the agent never asked for the rule. Two days later, a reviewer catches it. Or a customer gives their device a long name.

You’ve imported your standards, and Straion knows which rules fit which task. But the agent decides when to ask, and agents are optimistic. A quick fix doesn’t feel like it needs the security rules. At 100+ engineers, “remember to call the skill” isn’t working.

Now the same task with Automode. The developer types the same prompt. Before it writes anything, the agent looks up the rules for “device name in status message” and gets the buffer rule. The length check is in the first version of the code. Nobody had to remember anything.

## What you’ll see

Mostly nothing. The agent looks up the rules on its own and gets on with the task.

If the agent changes code without looking anything up, Straion sends it back before the work reaches you. You see one line:

```text
Straion sent the agent back: files changed without a find-rules call.
```

The agent gets a little more:

```text
This turn changed files, but this session made no `straion find-rules` call.
Run it for the task this turn worked on, and check the change against the
rules it returns.
```

So it looks up the rules and checks what it just wrote against them.

Automode ignores sessions that only answer questions, and it never gets your agent stuck. The [Automode docs](../docs/automode.md) cover the details.

## Why we built it this way

A few decisions shape how Automode behaves.

**It starts with a map.** When a session starts, Straion gives the agent a short list of your rule collections and tells it how to ask for the rules. The agent knows what exists before it begins. That’s why the lookup usually happens on its own, and you see nothing.

**It sends the agent back once, then lets go.** A check that traps an agent is a check developers turn off. One nudge gives the agent a chance to fix its own miss. If it stops again, Straion lets it, and tells you the rules were skipped.

**It checks one thing.** Automode asks a single question: did the agent look up your rules before it changed your code? It doesn’t check that the agent searched for the right task, or that the code follows the rules it found. That’s the job of the [audit trail](../docs/audit-trail.md). It records a decision for every rule and asks you before an exception ships. We wrote about that part in [You Shouldn’t Be Finding Rule Violations in Code Review](rule-violations-code-review.md).

**You can check it.** Every rule search lands in the audit trail, in every audit mode, even off. So for any session, you can see whether the agent looked. You never have to take its word for it.

So the promise is narrow, on purpose:

> **Every session that changes your code looks up your rules.**

## Roll it out one repo at a time

**Try it in one repo.** Run this in the repo’s root folder:

```bash
straion config automode true
```

It covers that folder and everything in it. The setting is saved on your machine, not in the repo, so your teammates aren’t affected.

**Turn it on for all your repos:**

```bash
straion config --global automode true
```

When both are set, the repo setting wins. So you can turn Automode on everywhere and off for one side project with `straion config automode false`.

**Turn it on for your organization.** Set the `STRAION_AUTOMODE_ENABLED` environment variable to `1` in your coding agent’s managed settings. Developers can’t edit those, and this setting wins over their own. Every agent on the team looks up your rules, whether its developer remembers Straion exists or not.

The order is simple: organization beats repo, and repo beats global. Automode starts with the next session, so open a new one after you change a setting.

## Getting started

1. Install the Straion CLI and the Straion plugin for Claude Code, GitHub Copilot (with the Copilot CLI installed), or Cursor. See [Getting Started](../docs/getting-started.md).
2. Run `straion config automode true` in a repo.
3. Start a new session.

The full setup is in the [Automode docs](../docs/automode.md).

---

## FAQ

### Do I still need the Straion skills?

Yes, when you want them. Skills like `/straion-implement` still guide you step by step, from spec to plan to code. Automode covers every session where nobody called a skill.

### Which coding agents does Automode work with?

Claude Code, GitHub Copilot (with the Copilot CLI installed), and Cursor.

### Can a developer turn it off?

On their own machine, yes, for every repo or just one. If you turn it on through your coding agent’s managed settings, no. Developers can’t edit those, and the organization setting wins over their own settings.

### Will Automode ever block my agent?

No. Straion sends the agent back once. If it stops again, Straion lets it finish and tells you the rules were skipped. The audit trail records that too.

---

## Stay on Track. Start for free.

See how Straion keeps your AI coding agent aligned with your standards.   
Set up takes
less than 5 minutes.

[Start free trial
→](https://straion.app/auth/signup) 

Works with Claude Code, GitHub Copilot & Cursor. No credit card required.

---

---

![Lukas Holzer](https://straion.com/.netlify/images?url=_astro%2Flukas.DfqEGcEf.jpg&fm=jpg&w=500&h=500&dpl=6ad948053628acb75d455cb3) 

Written by Lukas Holzer

![Fabian Friedl](https://straion.com/.netlify/images?url=_astro%2Ffabian.Bq-43Efc.jpg&fm=jpg&w=500&h=500&dpl=6ad948053628acb75d455cb3) 

Written by Fabian Friedl

[← Back to blog](../blog.md "Back to blog")
