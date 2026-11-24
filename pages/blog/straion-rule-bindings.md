---
title: "Control Where Your Rules Land"
source: https://straion.com/blog/straion-rule-bindings
description: "Straion already gets your rules to every agent in your organization. Rule bindings let you decide, as code, which repositories each rule reaches. Every change goes through a pull request."
---

[← Back to blog](../blog.md "Back to blog")

# Control Where Your Rules Land

November 25, 2026 · 4 min read · by  [Fabian Friedl](https://straion.com/blog/about/fabian-friedl)

AI Coding Agents  Engineering Leadership  Git  Straion  Product

## TLDR;

Straion already gets your rules to every agent in your organization. Rule bindings let you decide, as code, which repositories each rule reaches. Every change goes through a pull request.

Straion already gets your rules to every agent in your organization. A developer in any repository, on Claude Code, Codex, Cursor, or GitHub Copilot, gets the rules that fit their task. Nobody copies a CLAUDE.md from repo to repo anymore.

Until now, you had two choices for where a rule applied. Rules you create in the Straion app apply to every repository. Rules in a [connected repository](straion-rules-now-live-in-git.md) apply only to that repository. Most organizations need something in between.

Take a rule that says agents must never log a full card number. It belongs in billing, ledger, and checkout. It doesn’t belong in the marketing site or the internal design system. Your agents there have no reason to see it.

Today we’re shipping rule bindings. You decide, as code, where each rule lands.

## What a binding looks like

A binding is a short YAML file in your rules repository. It lists collections and the repositories they apply to.

```yaml
$schema: https://straion.com/schemas/rule-binding/v1.json
description: Payments safety rules for the services that move money.
collections:
  - payments-safety
repos:
  - github.com/acme/billing
  - github.com/acme/ledger
submodules: exclude
```

In `billing` and `ledger`, your agents now follow `payments-safety`. Everywhere else, they don’t. The marketing site never sees them. When a developer in `billing` asks their agent for a change, the agent gets the payments rules that fit the task.

## What you get

**You decide where rules land.** Bind a collection to every repository, to the repositories of one team, or to a single pilot project. Your agents only see rules that are meant for the code they work on.

**Policy as code, for your agents.** The bindings sit next to your rules, as files. Open the `bindings/` folder and you see which rules reach which repositories. Git history shows who changed it and when.

**Every change is a pull request.** A binding decides which rules your agents follow. So you change it like code. You edit it on a branch, explain why in the description, and a reviewer approves it. CI checks the file before anyone can merge it.

**Clear ownership.** Use `CODEOWNERS` to decide who approves what. The platform team owns the bindings, the payments team owns the payments rules. You already know how this works, because you do it for your code every day.

**Teams keep their own rules.** The platform team sets a baseline for the whole organization. Each team adds its own rules on top, in its own repository, without waiting for anyone.

## Three ways teams use it

**A baseline for everyone.** Set `repos` to `all`, and the collections apply in every repository you have, including the ones you’ll create next month.

```yaml
$schema: https://straion.com/schemas/rule-binding/v1.json
description: Baseline rules that every repository in the organization must obey.
collections:
  - secure-coding
  - logging
repos: all
submodules: exclude
```

**A careful rollout.** You wrote new API design rules and you aren’t sure yet how they’ll land. Bind them to one repository first. If it goes well, add more. When they’re ready, switch to `all`. Each step is one pull request, so the team sees and approves every widening.

**Code with submodules.** Firmware teams often pull in libraries as git submodules. Set `submodules` to `include`, and the rules reach every nested repository too. Your agent follows the embedded C rules in the vendored library, not only in the main project.

## Getting started

Bindings build on [rules in Git](straion-rules-now-live-in-git.md). If your rules already live in a connected repository, you’re most of the way there:

1. Pick the repository that holds your shared rules. Connect it if you haven’t yet.
2. Mark it as central. An organization admin runs `straion source repo connect --central` in a checkout.
3. Protect the rules branch and require a review.
4. Add your first binding as `bindings/<name>.yaml` and open a pull request.

The [rule bindings docs](../docs/rule-bindings.md) walk you through each step and have more examples. The [binding file reference](../docs/binding-file-reference.md) lists every field.

Don’t need any of this? If your rules apply everywhere, or each repository only needs its own, you’re set. Bindings are for everything in between.

---

## Stay on Track. Start for free.

See how Straion keeps your AI coding agent aligned with your standards.   
Set up takes
less than 5 minutes.

[Start free trial
→](https://straion.app/auth/signup) 

Works with Claude Code, Codex, GitHub Copilot & Cursor. No credit card required.

---

Your rules already reach every agent. Now you decide where they land. We’d love to hear how you split your rules between the platform and your teams.

**Stay on track.**

Fabian

---

![Fabian Friedl](https://straion.com/.netlify/images?url=_astro%2Ffabian.Bq-43Efc.jpg&fm=jpg&w=500&h=500&dpl=6b0582111ac3dd9075fbe9d9) 

Written by Fabian Friedl

[← Back to blog](../blog.md "Back to blog")
