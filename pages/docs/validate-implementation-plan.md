---
title: "Validate implementation plans"
source: https://straion.com/docs/validate-implementation-plan
description: "Catch rule violations in an implementation plan before any code is written"
section: "Using Straion"
order: 10
prev: validate-specs.md
next: validate-code.md
---

# Validate implementation plans

## What an implementation plan is

An implementation plan is the step-by-step breakdown of how a feature or change will be built, which components to touch, what logic to add, what tests to write, and in what order. It lives before any code is written.

## Why validate before coding starts

Catching a rule violation in a plan is far cheaper than catching it in code. When a plan step is non-compliant, you adjust one line of text. When generated code is non-compliant, you may need to refactor across multiple files. Validating the plan gives the AI a corrected set of constraints before it generates anything.

## How to trigger

Trigger the skill directly:

```text
/validating-rules Validate the implementation plan against my rules using Straion
```

Natural language alternatives:

```text
Validate this implementation plan using Straion: [paste plan]
```

```text
Check this plan against our rules before we start coding: [paste plan]
```

## How rules are matched to the plan

Straion selects rules relevant to the plan based on the technologies, components, and patterns mentioned. Rules about authentication apply to steps that touch auth; data-layer rules apply to steps that touch the database. Unrelated rules are not included.

## Understanding the Validation Report

A Validation Report is a structured review of how well a plan, spec, or code change complies with the rules Straion matched to that task. It connects each step or section of work to the rules it affects and shows whether those rules are satisfied, violated, or missing.

Straion lists all rules it matched to the plan, so you can see exactly which constraints are in scope for this task.

Each matched rule gets a status and, where relevant, a short description of the conflict or gap.

## Acting on the report

- **Adjust the plan** — edit the flagged steps using the suggested fixes, then re-run validation to confirm
- **Ask the AI to revise specific steps** — paste the violation description and ask the AI to rewrite just those steps
