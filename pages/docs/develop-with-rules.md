---
title: "Developing with rules"
source: https://straion.com/docs/develop-with-rules
description: "Use the developing-with-rules workflow to have Straion select relevant rules, validate your plan, generate constrained code, and check the output before you commit."
section: "Using Straion"
order: 8
prev: best-practices.md
next: validate-specs.md
---

# Developing with rules

The `/developing-with-rules` workflow guides AI-assisted development from the start. Straion selects the rules most relevant to your task, validates your existing spec or plan against those rules, builds an implementation plan constrained by those rules, generates code under those constraints, and then validates the output before you commit.

The result: compliant code, without manual cross-referencing of your team’s standards.

## When to use this

- Turning a spec or task into production-ready code
- Avoiding rework caused by non-compliant AI output

## How to trigger

Trigger the skill directly:

```text
/developing-with-rules I want to add a password reset flow using email verification
```

If you prefer not to use the slash command, you can phrase the request naturally and Claude will invoke the Straion skill automatically:

```text
Implement and validate the following task using Straion: [task description]
```

```text
Use Straion to build [feature description]
```

## What happens step by step

### 1. Rule selection

Straion queries your rules and matches rules to the task context, the feature description, the files involved, and any metadata in the task. Only rules relevant to this specific work are included, so the AI is not overloaded with irrelevant constraints.

### 2. Spec or task validation

If you provide a spec or existing task definition, Straion validates it against the matched rules before planning begins. This catches gaps or conflicts at the cheapest possible stage — before any code is written. See [Validate specs](validate-specs.md) for details on how this works.

### 3. Implementation planning

Straion produces an implementation plan and validates it against the matched rules. Each step in the plan is checked for rule compliance before code generation starts. See [Validate implementation plans](validate-implementation-plan.md) for details on the plan validation report.

### 4. Code generation

The AI generates code using the matched rules and any sample code they contain as explicit constraints. This replaces generic AI defaults with your team’s actual patterns.

### 5. Code validation

After code is generated, Straion validates the output against the same matched rules and produces a validation report. Issues are surfaced before you commit, not during code review. See [Validate code](validate-code.md) for details on the code validation report.

## Example prompts

### From a feature description

```text
/developing-with-rules Implement issue #123
```

### From an existing spec

```text
/developing-with-rules Here's my spec, validate and implement it: [paste spec]
```

### Break down into tasks without implementing yet

```text
/developing-with-rules Break down this spec into tasks, don't implement yet: [paste spec]
```
