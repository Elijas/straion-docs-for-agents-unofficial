---
title: "Example prompts"
source: https://straion.com/docs/example-prompts
description: "Copy-paste prompts for common Straion workflows: build a feature end-to-end, plan an implementation, validate a spec, and validate code."
unlisted: true  # in sitemap, absent from the docs sidebar
---

# Example prompts

A quick copy-paste reference for the most common Straion workflows. Adapt them to your own task and development environment. For the full explanation of each workflow, follow the linked guide.

Before you start, make sure you’ve completed the Straion setup — see [Getting Started](getting-started.md).

## Build a feature end-to-end

See [Develop with rules](develop-with-rules.md) for details.

```text
/developing-with-rules I want to add a password reset flow using email verification
```

```text
/developing-with-rules Here's my spec, validate and implement it: [paste spec]
```

```text
Implement and validate the following task using Straion: [task description]
```

## Plan an implementation

See [Develop with rules](develop-with-rules.md) for details.

```text
/developing-with-rules Break down this spec into tasks, don't implement yet: [paste spec]
```

## Validate a spec or implementation plan

See [Validate specs](validate-specs.md) and [Validate implementation plans](validate-implementation-plan.md) for details.

```text
/validating-rules Does this spec meet our rules? [paste spec]
```

```text
Validate this RFC with Straion. RFC: [rfc content]
```

```text
Validate the implementation plan against my rules using Straion
```

## Validate code

See [Validate code](validate-code.md) for details.

```text
/validating-rules Check the changes in PR #42 against our rules
```

```text
Validate these changes against matching rules using Straion
```
