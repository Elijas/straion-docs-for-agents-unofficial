---
title: "Validate specs"
source: https://straion.com/docs/validate-specs
description: "Check specs, RFCs, and design docs against your rules before implementation begins"
section: "Using Straion"
order: 9
prev: develop-with-rules.md
next: validate-implementation-plan.md
---

# Validate specs

Check a spec, software design doc or issue against your rules.

## What is a spec?

A spec is any artifact that describes what will be built before implementation begins: a technical specification, a design document, an RFC, a ticket with acceptance criteria, or a product requirements document.

## Why validate before implementation begins

**Catches missing requirements and ambiguities early.** A spec that contradicts your rules or leaves key constraints unspecified will produce non-compliant code regardless of how well the AI is prompted. Fixing a spec is editing text; fixing the resulting code means rework across files.

**Cheaper to fix a spec than refactor code.** Finding a violation at spec stage has essentially zero implementation cost. Finding the same violation during code review means the code must be rewritten.

## How to trigger

Trigger the skill directly:

```text
/validating-rules Does this spec meet our rules? [paste spec]
```

Natural language alternatives:

```text
Validate this specification using Straion: [specification content]
```

```text
Validate this RFC with Straion. RFC: [rfc content]
```

```text
Check this spec against our rules before we share it with the team: [paste spec]
```

## What Straion checks

### Rule matching against spec content

Straion selects rules relevant to the spec based on the technologies, components, and patterns it describes. It then checks whether each matched rule is satisfied, violated, or unaddressed in the spec.

### What it can and can’t catch

Straion checks **rules coverage**: whether the spec addresses the constraints your team has defined. It does not evaluate general design quality, architectural soundness, or product completeness beyond what your rules describe.

## Acting on the report

- **Refine spec language** — update sections that violate rules so the spec explicitly satisfies the constraint
- **Add missing requirements** — if a rule is flagged as “not covered”, add a section or acceptance criterion that addresses it
- **Re-validate after changes** — run validation again after editing the spec to confirm violations are resolved before handing off to implementation
