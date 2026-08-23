---
title: "Best practices"
source: https://straion.com/docs/best-practices
description: "How to write clear, well-formed rules that AI coding agents can interpret correctly"
section: "Rules"
order: 7
prev: rule-file-format.md
next: develop-with-rules.md
---

# Best practices

The following are some best practices for writing great rules. Straion’s import functionality produces rules in this format automatically, so imported rules already follow them. When you edit rules by hand in a [connected repository](connect-repository.md), these are the habits that keep them clear and machine-readable.

## Start with an RFC 2119 keyword

Every rule statement begins with an RFC 2119 keyword, and that keyword is the **first word** of the statement, in uppercase. [Core Concepts](core-concepts.md#how-a-rule-is-structured) explains what each keyword means and how Straion uses it. This page is about phrasing: lead with the keyword so both people and agents read the strength the same way.

- Good: `MUST reject requests without an Authorization header.`
- Good: `SHOULD prefer composition over inheritance for shared behavior.`
- Avoid: “It is important that requests are authenticated.” No keyword, no clear strength.

## Describe exactly one thing (atomicity)

A rule describes one action. If you find yourself writing “and”, it is usually two rules.

- Good: `MUST reject requests without an Authorization header.`
- Bad: `MUST reject unauthenticated requests **and** log all errors to Datadog.`

Splitting them keeps each rule independently matchable and independently fixable.

## Be complete and precise (clarity)

A rule includes a precise verb, the object it acts on, and any important conditions or scope. Use active voice and avoid vague verbs like “support”, “handle”, or “ensure”.

- Good: `MUST retry failed webhook deliveries up to 3 times with exponential backoff.`
- Vague: `MUST handle webhook failures.`
- Good: `MUST accept uploads up to 500 MB and process them within 60 seconds.`
- Vague: `SHOULD support large files.`

The more concrete the statement, the more reliably an agent can match its plan against it.

## Show it with an example

A rule can carry code examples that demonstrate it. Give a compliant example (and, where it helps, a violating one) so the agent has a concrete pattern to follow rather than a generic template.

Choose a snippet that illustrates the rule directly, and keep it short. Each example is a fenced code block that carries a language and a `kind=compliant` or `kind=violating` tag. The language is just for syntax highlighting, it doesn’t have to be one of the rule’s `languages`:

````md
## Examples

```cpp kind=compliant
constexpr int MAX_RETRIES = 3;
```

```cpp kind=violating
int maxRetries = 3;
```
````

See [Rule file format](rule-file-format.md) for the full anatomy of a rule file and how examples are structured.
