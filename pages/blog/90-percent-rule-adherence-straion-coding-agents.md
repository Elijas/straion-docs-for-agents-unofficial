---
title: "90% Rule Adherence"
source: https://straion.com/blog/90-percent-rule-adherence-straion-coding-agents
description: "When Claude Code runs with Straion, rule adherence climbs into the 90%+ range. See how the automated context layer keeps AI code on your standards."
---

[← Back to blog](../blog.md "Back to blog")

# 90% Rule Adherence

March 26, 2026 · 5 min read · by  [Katrin Freihofner](https://straion.com/blog/about/katrin-freihofner)

AI Coding Agents  Research  Straion  Engineering Leadership  Benchmarks

## TLDR;

When Claude Code runs with Straion, rule adherence climbs into the 90%+ range. See how the automated context layer keeps AI code on your standards.

## The Problem: AI Ignores How You Work

Most teams already use an AI code assistant. Yet you still see pull requests that:

- Break internal guidelines
- Cross architecture boundaries
- Re‑implement patterns you already solved

That gap isn’t about model quality. It’s about context. Your docs, rules, and conventions rarely make it into the prompt in a structured way. The result is context drift between “how we say we code” and “what the AI actually does.”

Straion’s structured context layer promises **Code accuracy and Rule adherence**.

This benchmark is our way to measure something senior engineers feel every day, not to create another synthetic leaderboard.

## Benchmark: Real Repos, Real Fixes

We used two open‑source repositories:

- [**Argo Workflows**](https://github.com/argoproj/argo-workflows)
- [**Elastic Kibana**](https://github.com/elastic/kibana/)

Kibana is a realistic enterprise codebase: large, TypeScript‑heavy, and full of internal conventions, from Elastic UI (in a separate repo with its own docs) to testing patterns and plugin architecture.

For each repository we:

1. Check out the repository at the commit before the fix
2. Run the [Harbor](https://harborframework.com/) scenario that triggers Claude Code with the selected context wiring
3. Apply the generated patch and run the tests
4. Repeat across multiple trials to see stability and variance

The task stayed constant. Only the way we wired context into Claude changed.

Each run was evaluated on:

- **Code correctness** – tests pass, and instructions are followed
- **Rule adherence** – generated code follows the relevant guidelines
- **Efficiency** – token usage, steps, and duration

To avoid lucky runs, we executed each variant as repeatable jobs in a containerized environment using [Harbor](https://harborframework.com/). All scripts and configs live in the [Straion Benchmark Repository](https://github.com/straion-dev/benchmarks) so you can rerun or extend the benchmark on your own codebase.

## Three Ways to Give Claude Context

At a high level, the variants differ only in how much context Claude receives and how structured that context is.

| Variant | Context | How it’s provided |
| --- | --- | --- |
| No context | Issue description only | Baseline, no explicit rules |
| CLAUDE.md | Human‑compiled rule file | Manually copy‑pasted docs, unstructured |
| With Straion | Same docs as CLAUDE.md | Automatically extracted, filtered, and rule‑matched |

### 1. Baseline: No Context

Here, Claude gets only the issue description. It can infer some conventions from local files and its prior training, but it never sees your explicit rules. This shows how far a strong model can go without project knowledge.

None of the repositories we tested contained a `CLAUDE.md` or `Agent.md` at the target commit.

### 2. CLAUDE.md: Manual Context Injection

This reflects what many teams do today: maintain a `CLAUDE.md` with rules and best practices.

We pulled relevant sections from:

- [Elastic UI](https://github.com/elastic/eui/) developer guidelines (testing, component usage) and [Kibana](https://github.com/elastic/kibana/)
- [Argo repositories](https://github.com/argoproj/) (UI and backend guidelines)

We placed the rules we were testing for near the top or bottom of the file, [ideal conditions](delete-your-claude-md-science-says-so.md) for the model to notice them.

### 3. Claude Code + Straion: Automated Context Layer

In the third variant, Straion acts as a context engine on top of Claude Code.

Straion:

- Ingests docs and dev guidelines
- Automatically extracts rules like:
  - “Prefer EUI components over custom CSS”
  - “Include `data-test-subj` attribute”
  - “Align with WCAG 2.1 accessibility patterns”
- Matches the relevant rules to the current task

Claude receives a smaller, high‑signal context window: specific rules that matter to this change, not a dump of everything you might ever need.

## Results: Near‑Perfect Guideline Adherence

Claude + Straion reaches near‑perfect guideline adherence while maintaining or improving correctness compared to the baselines. Token usage is higher, but teams win that back through less manual correction and shorter review cycles.

| Guideline adherence | No context | CLAUDE.md | With Straion |
| --- | --- | --- | --- |
| Kibana | 0% | 5% | 90% |
| Argo | 10% | 75% | 85% |

The no‑context variant often produced code that compiled and passed tests but ignored organization‑specific rules.

`CLAUDE.md` improved adherence but still missed some cases and showed **high variance** across runs.

With Straion, Claude reliably applied project‑specific rules:

- It chose the right rules for the specific step in the implementation plan
- It followed the rules during the code generation
- It validated that the code adheres to the rules

Across runs, this is reflected in a **90% guideline adherence score**.

We also saw a qualitative shift: with Straion, Claude more often performed extra validation passes before finalizing the patch. That behavior isn’t hand‑prompted, it emerges from Straion’s workflow.

## Why This Changes the Way You Work

The key point isn’t just that Straion improves scores, it changes the workflow of the coding agent.

With structured rules available, Claude:

- Runs its own validation steps before emitting the final implementation
- Keeps changes scoped, instead of leaking new patterns across unrelated files

For transparency, we slightly adapted the instructions in the Straion variant to include “…using Straion,” so runs remain reproducible.

Static `CLAUDE.md` files help a bit but don’t scale. They become another document to maintain, drifting away from reality, over time.

## Why It Matters Once You Have 100+ Engineers

After about 100 engineers, every organization feels context drift:

- Guidelines fall out of date
- Docs become partial and scattered

AI coding agents make that drift more visible, and more expensive.

Straion acts as a context layer for your AI coding agents. Instead of each developer acting as the prompt router and rule enforcer in every session, Straion:

- Matches the right rules to the current task
- Feeds those rules into Claude at the specific step needed

The impact shows up where it matters in practice:

- **Faster reviews:** fewer “please align with our coding guidelines” comments
- **More consistent quality:** AI‑generated code becomes an extension of your standards, not a parallel universe

---

## Stay on Track. Start for free.

See how Straion keeps your AI coding agent aligned with your standards.   
Set up takes
less than 5 minutes.

[Get Started Free
→](https://straion.app/auth/signup) 

Works with Claude Code, GitHub Copilot & Cursor. No credit card required.

---

## Try It on Your Own Codebase

You don’t have to take our word for it. You can run the benchmark yourself.

We’ve open‑sourced our setup. Tasks, configs, and definitions, in the [Straion Benchmark Repository](https://github.com/straion-dev/benchmarks), so you can rerun our scenarios or adapt them to your own repositories.

If you want to explore Straion in your organization, reach out via [Discord](https://discord.gg/jd5btNuC), our [email](mailto:team@straion.com), or [GitHub Discussions](https://github.com/straion-dev/benchmarks/discussions). We’re expanding the benchmark pool beyond the two examples presented to cover more services, tech stacks, and complex multi‑service workflows, [let us know](mailto:katrin@straion.com) if you have an example in mind you’d like to see.

---

![Katrin Freihofner](https://straion.com/.netlify/images?url=_astro%2Fkatrin.qSA9g74x.jpg&fm=jpg&w=500&h=500&dpl=6a85597a97a15700076a9c5e) 

Written by Katrin Freihofner

[← Back to blog](../blog.md "Back to blog")
