---
title: "Straion Rules Now Live in Git"
source: https://straion.com/blog/straion-rules-now-live-in-git
description: "Straion rules can now be managed in Git: versioning, pull request reviews, and full history. Available on the enterprise plan and in the free trial."
---

[← Back to blog](../blog.md "Back to blog")

# Straion Rules Now Live in Git

July 30, 2026 · 5 min read · by  [Fabian Friedl](https://straion.com/blog/about/fabian-friedl)

AI Coding Agents  Engineering Leadership  Git  Straion  Product

## TLDR;

Straion rules can now be managed in Git: versioning, pull request reviews, and full history. Available on the enterprise plan and in the free trial.

Your codebase is managed using a version control system like *git*. Every change is a commit. Every commit has an author, a timestamp, a diff, and someone who signed off on it. You can blame a line, revert a release, and reconstruct exactly what shipped 2 months ago. You govern your code with real rigor, because at 100+ engineers, you have to.

Now look at the rules that govern your AI agents. The security policies, architecture standards, and coding conventions that shape what every developer’s agent writes. Where do those live?

For most teams: scattered CLAUDE.md and AGENTS.md files, some of them not even checked in or a Confluence page nobody updated since 2024. That’s fine when you’re getting started. At scale you need real control: who can change a rule, who has to review it, and a full history of every change. Your rules deserve the same scrutiny your code does.

## Rules in Git

Today we’re closing that gap. Straion rules can now be fully managed in Git, in the workflow your team already uses every day.

> Rule storage that’s ready for the enterprise.

You write, review, and ship rules the same way you write, review, and ship code. It meets your engineers where they already are, in the workflow they use every day.

   ![A Git repository browser showing a dedicated straion/rules/v1 branch with a rules folder containing rule collections and a CI config file.](https://straion.com/.netlify/images?url=_astro%2F2026-07-20-rule-repo-overview.q-R5wwF0.png&fm=png&w=3025&h=1659&dpl=6a85597a97a15700076a9c5e)  

Rules live on a dedicated branch as plain files. Each folder is a collection, grouping rules, versioned and reviewed like any other part of your repo.

 

What you get:

- Works with any Git provider: GitHub, GitLab, Bitbucket, self-hosted, whatever you run.
- Available on the enterprise subscription and in the free trial.
- Auto-syncs on every commit via GitHub Actions, GitLab CI, or your existing CI pipeline. Merge a change, and every developer’s agent picks up the new version automatically. Nobody pulls, nobody updates anything.

## ”I already have my CLAUDE.md checked in, isn’t that the same?”

If you’ve followed Straion, we already highlighted some of the issues that those agent context files have in a [recent blog post](delete-your-claude-md-science-says-so.md). Storing the files in a git repository is not one of them.

The problem was never that the files lived in Git. It was that rules got buried and duplicated across dozens of repos, dumped wholesale into every agent session no matter the task, and left to drift out of sync. Static files have no concept of relevance. That’s the whole reason Straion exists.

Centralized rule sources, living in Git as your storage and governance backend, with Straion’s dynamic context selection and task-plan validation sitting on top. Git handles history, review, and ownership. Straion connects to your rules and decides which rules each task actually needs, and validates the agent’s plan before tokens and time are wasted.

You get your git workflows, versioning and permissions without losing the thing that made Straion powerful: Delivering the relevant rules to your agent’s context. Git becomes the source of truth for rules. Straion remains the delivery and enforcement layer.

## How it works

**Auto-sync.** Your latest commit syncs to Straion automatically through GitHub Actions, GitLab CI, or your existing CI pipeline. There’s no manual publish step, no “did someone push the update?”. Merge your rule updates and it’s enforced on every new run.

   ![A CI pipeline run that passed, showing a single straion-rules-sync job triggered by a commit that adds a new rule.](https://straion.com/.netlify/images?url=_astro%2F2026-07-20-ci-sync-pipeline.1FK491qZ.png&fm=png&w=3023&h=1657&dpl=6a85597a97a15700076a9c5e)  

Every commit triggers a straion-rules-sync job in your existing CI. Merge a rule change, and it reaches every developer's agent automatically.

 

**Isolated history.** Rules live on a dedicated branch that doesn’t share history with your application code. Your rule history stays clean and readable.

**Set it up your way.** Keep rules on a dedicated branch, in a separate central repo for org-wide standards, or a mix of both. A branch keeps rules close to the code. A central repo lets a platform or security team set one standard for the whole organization.

**Your normal workflow.** Create, edit, and delete rules exactly as you would code: commits, branches, pull requests.

**Governance, for free.** This is the part that matters. CODEOWNERS, mandatory PR reviews, branch protection, required approvals: every governance control your organization already runs on code can now apply to rules. Want to guarantee that only the security team can change a security rule? You already have the tool for that. You don’t configure a new permission system inside Straion, you reuse the one you already have.

## The rules are yours

They live in your Git infrastructure, under your control. If you ever walk away from Straion, you walk away with every rule, in plain files, in your own repo. No vendor lock-in or export ticket needed.

Because rule changes flow through the exact review workflow your engineers already know, the adoption cost is close to zero. There’s no new approval process to design, nothing to train anyone on. A rule change is a pull request. Your team has reviewed a few thousand of those.

## Getting started

Three steps, and you’re live in about five minutes:

1. Start your free trial and install the [Straion CLI](https://www.npmjs.com/package/@straion/cli).
2. Connect your repository as a source. Run `straion source repo connect`. Straion will create a dedicated branch for your rules and set up the auto-sync pipeline.
3. Migrate your existing AGENTS.md / CLAUDE.md files into rules.

Once your rules are in Straion, everything the platform already does kicks in. Centralized rules as your single source of truth. Dynamic context selection, so each agent gets only the rules relevant to the task in front of it, not your entire ruleset dumped into every session. Task-plan validation that catches violations before tokens are wasted. It works with Claude Code, GitHub Copilot, and Cursor out of the box.

## Why it matters

Your code has always had history, review, and ownership. It’s the foundation that lets large teams move fast without breaking things. Your AI rules now shape as much of what ships as your code does. It’s time they stood on the same foundation.

Now they do. Your rules, your repo, your history.

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

![Fabian Friedl](https://straion.com/.netlify/images?url=_astro%2Ffabian.Bq-43Efc.jpg&fm=jpg&w=500&h=500&dpl=6a85597a97a15700076a9c5e) 

Written by Fabian Friedl

[← Back to blog](../blog.md "Back to blog")
