---
title: "Validate code"
source: https://straion.com/docs/validate-code
description: "Validate a PR, diff, or AI-generated changes against your rules before merge"
section: "Using Straion"
order: 11
prev: validate-implementation-plan.md
next: invite-users.md
---

# Validate code

Check a pull request, diff, or AI-generated change against your rules.

## What code validation checks

Code validation runs your rules against actual implementation: a pull request diff, a set of uncommitted changes, or AI-generated output. Straion checks whether the changed code satisfies the rules matched to those files and surfaces violations before merge.

### Where it fits in the workflow

Code validation is the last checkpoint before a change ships. It runs after implementation (whether by a human or AI) and before the change is merged. When used as part of [Develop with rules](develop-with-rules.md), code is validated automatically as the final step. You can also trigger it manually on any PR or diff.

## How to trigger

Validate a PR by number:

```text
/validating-rules Check the changes in PR #42 against our rules
```

Validate current uncommitted changes:

```text
/validating-rules Validate the code changes using Straion
```

Natural language alternatives:

```text
Validate these changes against matching rules using Straion
```

```text
Check the current diff against our Straion rules
```

## What Straion checks

### How rules are matched to changed files and code

Straion selects rules based on the files touched by the change — their paths, extensions, and content patterns. A change to an authentication module matches auth rules; a change to a data access layer matches data rules. Rules unrelated to the changed files are not included.

## Understanding the output

Code validation produces a Validation Report in the same format used for plan and spec validation. Matched rules list, rule status, and suggested fixes: [Validate implementation plans](validate-implementation-plan.md#understanding-the-validation-report).

## Acting on the report

- **Fix violations before merge** — address each violated rule in the code before requesting review or merging
- **If a rule seems wrong, update it in Straion** — if the violation indicates a rule is outdated or incorrectly specified, update the rule in Straion before re-validating
- **Re-validate after fixes** — run validation again after fixing violations to confirm the changes now comply
