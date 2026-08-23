---
title: "Developers Asked Anthropic to Build This. We Did."
source: https://straion.com/blog/developers-asked-anthropic-to-build-this
description: "A developer filed GitHub issue #14467 on claude-code describing exactly the problem Straion solves. We built it. Here is the full story."
---

[← Back to blog](../blog.md "Back to blog")

# Developers Asked Anthropic to Build This. We Did.

June 2, 2026 · 6 min read · by  [Katrin Freihofner](https://straion.com/blog/about/katrin-freihofner)

AI Coding Agents  Engineering Leadership  Straion  Claude Code  Product

## TLDR;

A developer filed GitHub issue #14467 on claude-code describing exactly the problem Straion solves. We built it. Here is the full story.

In December 2025, someone opened a GitHub issue on the `anthropics/claude-code` repo with a precise, frustrated description of a structural problem with AI coding at the team level.

Here it is:

> *“Our team has multiple repos under the same GitHub organization. We want to share company-level context, conventions, and coding standards with Claude Code across all repos. Currently our options are: duplicate `CLAUDE.md` in every repo (gets out of sync), each developer manually symlinks to a shared repo (manual setup, easy to forget), or enterprise deployment…”*
>
> GitHub [#14467](https://github.com/anthropics/claude-code/issues/14467), anthropics/claude-code, Dec 2025

If you were one of folks who upvoted the issue, this post is for you.

What you are asking for is a layer that makes an AI coding assistant usable inside a real engineering organisation. That’s Straion.

## The problem is not speed

Teams that have rolled out Cursor, Claude Code, or GitHub Copilot are not struggling with output volume. They’re struggling with what happens when agents move fast in the wrong direction.

When an agent skips a mandatory workflow step, violates your naming conventions, or ignores a compliance rule, the cost is on your team, in the form of review cycles, rework, and the growing suspicion that you can’t actually trust the tool for anything that matters.

For lead engineers, that trust gap is the real problem. And because of the way these coding agents are set up, the problem increases as your team grows.

## A file isn’t a policy

The standard advice is to put your rules in `CLAUDE.md`, or `AGENTS.md`, or `.cursor/rules.md`, and call it done. This works fine for a single developer working alone. It breaks down the moment you have a second repo.

By the time you have eight repos, you don’t have rules. You have suggestions. Some repos have updated files, some have stale ones, some have none. New joiners miss the file entirely. The agent reads whatever is nearest. Nobody knows which rules are actually being applied.

GitHub [#14467](https://github.com/anthropics/claude-code/issues/14467) laid out the three workarounds teams reach for and why none of them work:

- **Duplicate `CLAUDE.md` in every repo**, drifts immediately, maintained by whoever remembers to update it
- **Manual symlinks to a shared repo**, works until a developer forgets, which happens constantly
- **Enterprise deployment**, requires IT infrastructure and an enterprise contract teams might not have

The gap between “we have a `CLAUDE.md`” and “our standards are reliably applied” is the gap Straion fills.

## It gets worse: even when the file exists, the rules get ignored

Six months before [#14467](https://github.com/anthropics/claude-code/issues/14467), a separate issue was opened: [#2544](https://github.com/anthropics/claude-code/issues/2544), titled *“[BUG] CLAUDE.md Mandatory Rules Consistently Ignored Across Multiple Repositories.”*

The examples in that thread weren’t cosmetic preferences. Teams reported agents skipping issue checkout procedures, ignoring documentation requirements, missing testing steps, breaking commit formats, and bypassing compliance rules, repeatedly, across repos, even when the rules were explicitly marked as mandatory.

One commenter put it plainly:

> *“This is becoming a bit of a deal breaker for me. I only have a handful of rules, some of them critical, that it needs to adhere to. Without guaranteed adherence, I simply can’t allow auto-accept of edits, which reduces the efficacy of this tool.”*
>
> GitHub [#2544](https://github.com/anthropics/claude-code/issues/2544), anthropics/claude-code, 2025

That’s the trust failure in one sentence. The agent is fast. But if you can’t trust it to follow mandatory rules, you can’t let it run unsupervised. And if you can’t let it run unsupervised, you’ve traded one kind of overhead for another.

## Built for how engineering orgs actually work

We didn’t build Straion in response to these GitHub issues. We built it because we’d spent years inside large enterprise software teams and knew what the real environment of these teams looks like.

It’s rarely clean. Teams reorganise. Ownership shifts without the repo structure following. A single codebase gets split across teams with different standards, or one team inherits a dozen repos with no consistency between them. The rules that matter aren’t flat. There are company-wide security policies, domain-specific conventions, team-level standards, and project-specific requirements, and they sit at different levels of authority and specificity.

The tools that came before Straion weren’t designed for this. They assumed a simple, stable mapping: one team, a handful of repos, rules that fit in a single file. That’s a workable assumption for a solo developer or a small startup. **We built the solution for 100, 500, or 1,000 engineers.**

Straion is built to handle that complexity directly: hierarchical rules, flexible scope, and the kind of resilience that survives a reorg.

## What Straion changes

Straion is not another place to store your `CLAUDE.md`. It’s the enforcement layer that makes your rules actually work, across every repo, every developer, every AI coding tool your team uses.

Here’s what that looks like in practice:

**One source of truth, not fifteen files.** You import your engineering standards once into Straion. Every developer on your team, whether they’re using Cursor, Claude Code, or GitHub Copilot, gets the same rules automatically, without touching a file in any repo.

**Context injection that scales.** Dumping every rule into every session hits the context ceiling immediately. Straion selects the rules relevant to the current task, based on implementation step, team, project, domain, and stack, and injects only what’s needed. This is especially important once you have more than a handful of rules.

**Validation before the code is written.** Straion checks the agent’s plan against your standards before a line is generated. Catching a violation at that stage costs almost nothing. Catching it after a PR is open costs significantly more.

**Cross-repo updates without the manual work.** When your security policy changes, you update it once. Every agent connected to Straion picks it up automatically. No pull requests, no symlinks, no hoping someone remembers.

### The honest version of what you’d have to build instead

We’re seeing some teams tackle aspects of this with custom skills, automating specific workflows and encoding team conventions at the task level. That’s a legitimate approach for certain problems, and we’ll get into it in a future post.If you’re looking to build something that scales the way Straion does, the [Build vs. Buy post](build-vs-buy-ai-coding-governance.md) is worth a read first.

## Straion is what these developers were asking for

The person who filed [#14467](https://github.com/anthropics/claude-code/issues/14467) was asking for centralised standards, automatic context injection, and cross-repo consistency. That’s exactly what Straion delivers. We didn’t build it in response to the issue. We built it because every lead engineer managing a team with AI coding tools eventually hits the same wall. The issue just said it clearly.

If your team is serious about AI in production engineering, give me a call.

---

## Stay on Track. Start for free.

See how Straion keeps your AI coding agent aligned with your standards.   
Set up takes
less than 5 minutes.

[Get Started Free
→](https://straion.app/auth/signup) 

Works with Claude Code, GitHub Copilot & Cursor. No credit card required.

---

---

![Katrin Freihofner](https://straion.com/.netlify/images?url=_astro%2Fkatrin.qSA9g74x.jpg&fm=jpg&w=500&h=500&dpl=6a85597a97a15700076a9c5e) 

Written by Katrin Freihofner

[← Back to blog](../blog.md "Back to blog")
