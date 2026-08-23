---
title: "Core concepts"
source: https://straion.com/docs/core-concepts
description: "What rules are and how Straion uses them to keep AI coding agents aligned with your standards"
section: "Start here"
order: 3
prev: prerequisites.md
next: import-rules.md
---

# Core concepts

Straion is built on three ideas: rules, collections, and rule sources.

## Rules

Rules are the core input Straion uses to keep your AI coding agents aligned with your engineering standards. They capture requirements from your existing documentation, markdown files, and repositories, and connect them to the agent’s implementation plan.

### What are rules?

A rule is a single, well-formed requirement that expresses how your code should be written in a specific context. With Straion you can import rules from sources like architecture docs, security guidelines, or repo-local .md files.

### How a rule is structured

Every rule begins with a modal keyword that sets how strongly it is enforced, following the [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) convention:

- **Mandatory** rules start with `MUST` or `MUST NOT`. These are enforced: security controls, compliance constraints, org-wide decisions.
- **Recommended** rules start with `SHOULD` or `SHOULD NOT`. These are preferred, and a deviation is allowed with justification.
- **Optional** rules start with `MAY`. These describe a truly optional choice: an item is genuinely allowed, and another team or vendor can leave it out without harming interoperability.

Straion derives whether a rule is mandatory or recommended straight from this keyword, and uses it when reporting how a plan measures up. See [Best practices](best-practices.md) for how to phrase strong rules. Straion’s import functionality produces rules in this format automatically.

### How does Straion use rules?

- It selects the relevant rules based on task context (team, project, tech stack, change type).
- It matches those rules against the AI agent’s task or implementation plan before code is generated. See [Validate specs](validate-specs.md) and [Validate implementation plans](validate-implementation-plan.md).
- It highlights any plan steps that violate or ignore the rules, so developers can fix them early. See [Validate implementation plans](validate-implementation-plan.md).
- It validates generated code against rules. See [Validate code](validate-code.md).

## Collections

Rules are grouped into **collections**, a set of related rules that share a theme, such as “C++ Naming Conventions” or “API Security”. A collection has a name and a description, and it’s the unit you organize and govern rules by. When you store rules as code, a collection is a folder of rule files. See [Rule file format](rule-file-format.md) for the details.

## Rule sources

### Connected git repositories

When you [connect a git repository](connect-repository.md), your rules live as code in that repository and your git history becomes the source of truth. Straion keeps a **read-only copy in sync**: whenever the rules branch changes, a sync step sends the current rules to Straion so your agents always match against what’s in git.

Because git is authoritative, rules and collections from a connected repository can’t be edited or deleted inside the Straion app. You change them through your normal pull-request workflow, governed by your existing branch protection and [CODEOWNERS](https://docs.github.com/articles/about-code-owners). Rules imported from files or pasted text are unaffected and stay editable in the app.

See [Connect a repository](connect-repository.md) to set this up, and [Rule file format](rule-file-format.md) for how rules look on disk.

### Rules from a file or pasted text

When you upload a file or paste text to import rules, those rules live in Straion and stay editable in the app.
