---
title: "Enterprise-Ready.Secure by Design."
source: https://straion.com/security
description: "Straion enforces your engineering standards without touching your source code. See the exact data flow, what the CLI sends, EU hosting, and our compliance status."
---

Security & Trust

# Enterprise-Ready. Secure by Design.

Straion enforces your engineering standards without ever touching your source code. Your
rules. Your codebase. Your control.

[Start Free](https://straion.app/auth/signup)

The commitments

## Secure by design

### Your code stays where it is

Straion syncs rules, not code. The CLI runs locally, your repository is never cloned, and your codebase stays on your machine. There is no copy of your files on our side. Nothing to leak.

### Rules stay under your control

You own every org standard: every change is versioned, and you decide who can read or edit each rule. On Enterprise plans the rules live as plain Markdown on a branch in your own Git, so history and approvals run through your normal pull request flow.

### No model training on your data

Your rules, your task context, and your usage data are never used to train models. Not ours, not anyone else’s.

---

How Straion works 

## Where your data goes, and where it does not

Three parts, one round trip. The agent describes the task, Straion sends back the rules that
apply, and your files stay put.

On your machine

### AI agent + local CLI

Claude Code, Cursor, or Copilot runs in your existing environment. The Straion CLI runs
there too and asks for the rules that fit the task at hand.

✓ Your codebase never leaves this box

 

Straion (EU hosted)

### Rule selection

Straion matches the task description against your rule collections and returns only the
rules that apply. TLS in transit, encrypted at rest, EU-based models.

✓ Rule definitions only, no files

 

In your Git

### Your rule hub

Rules live as plain Markdown on a dedicated branch in your own repository. Changes go
through pull requests, so CODEOWNERS and branch protection apply.

✓ Rule definitions only, and they stay yours

A real request, start to finish

what the CLI sends, and what comes back

$ straion find-rules

--title "feat: add configurable alert threshold for over-temperature detection"

--body "The TMP116 alert pin fires when temperature crosses a high or low limit, but the
driver only exposes raw reads. The host MCU needs an over-temperature interrupt
instead of polling I2C. Proposed API: tmp116.setHighLimit(250.0f) and
tmp116.setAlertCallback(...). Acceptance criteria: write the limit registers via the
existing I2C abstraction, distinguish High / Low alerts, add unit tests, keep the
driver platform-agnostic."

--summary "Add setAlertCallback() to TMP116 driver so host MCU can respond to over/under
temperature events via interrupt rather than polling"

--files "TMP116/Inc/TMP116.hpp,TMP116/Src/TMP116.cpp,TMP116/Test/TMP116.test.cpp"

--tags "driver,embedded,cpp,testing,api"

--keywords "alert,callback,I2C,TMP116,temperature,threshold,interrupt,polling"

Found 14 matching rule(s) across 2 collection(s):

## Embedded C++

- - MUST NOT allocate memory dynamically after initialization.
- - MUST NOT use exceptions or RTTI in firmware code.
- - MUST NOT enable compiler-specific language extensions.
- - MUST pass callbacks as a function pointer plus a void* context, never as
  std::function.
- - MUST keep interrupt service routines free of blocking calls.
- - MUST NOT start an I2C transfer from interrupt context; defer it to the main loop.
- - MUST declare every hardware register access volatile.
- - SHOULD use fixed-width integer types from <cstdint> instead of int or long.
- - SHOULD prefer constexpr constants over preprocessor macros.
- - SHOULD pass buffers as a size-carrying type instead of a pointer and a length.

## Driver Design & Tests

- - MUST keep drivers platform-agnostic by depending on the HAL interface, not vendor
  headers.
- - MUST return a status enum from every driver call that can fail.
- - MUST cover each new public driver method with a test against the mock I2C bus.
- - MUST colocate tests with the driver they cover.

That is the whole exchange. A task description goes out, a list of rule statements comes
back. The files are named, never opened.

For your security team 

## The payload, field by field

Every argument the CLI puts on the wire, and everything it leaves behind.

### What is sent

--title
:   One line describing the task the agent is about to start.

--body
:   The task description written by your agent, in plain language.

--summary
:   A short statement of what is being validated.

--files
:   File paths only. Never file contents.

--tags
:   Coarse labels such as driver, embedded, testing.

--keywords
:   Libraries and patterns involved, such as I2C or interrupt.

### What is never sent

- Your repository, cloned or otherwise
- The contents of the files you name in --files
- Commit history, branches, or diffs
- Environment variables, secrets, or credentials from your machine

"Does the CLI send code snippets?"

It can, and we would rather say so plainly. Your agent writes the task description, so
if it quotes a few lines in --body, those lines travel
with the request. Straion never opens a file to add code itself, and full files are
never transmitted. Run the CLI with verbose output to inspect every call before it
leaves the machine.

The short list

## What Straion does not do

Never reads, transmits, or stores your full code files

Never shares your rule definitions with other organizations

Never uses your data to train AI models

Never sells or monetizes usage data

Compliance 

## Where we stand today, and what is next

### Compliance & certifications

- GDPR-compliant data handling
- Encrypted in transit (TLS)
- Encrypted at rest
- SOC 2 Type II: in progress

We are working towards SOC 2 Type II certification. If that matters for your review,
write to [team@straion.com](mailto:team@straion.com) and
we will share our current status and timeline.

[Live service status →](https://straion.instatus.com/)

### Deployment & data residency

Hosted SaaS, EU based

Straion runs on EU infrastructure. No setup on your side beyond the CLI.

EU-based data and models

The models Straion uses to select rules run in the EU, so task context stays in the
same region as your data.

Roadmap: bring your own cloud

Self-hosted deployment options for larger enterprises are on the roadmap. Talk to us
if you need one.

## Security questions, answered

Does Straion read or store our source code?  

No. Straion never reads your repository, never clones it, and never stores your code files. The CLI runs locally on the developer machine and syncs rules, not code. What travels to Straion is the task context your agent describes: a title, a task description, a summary, file paths, tags, and keywords. That context is used to select the matching rules and is then returned to the agent.

  Can the task context sent by the CLI contain code snippets?  

It can. Your AI agent writes the task description, so if it quotes a few lines of code in the description, those lines are part of the request. Straion never opens your files to add code itself, and full files are never transmitted. If you want to see exactly what leaves the machine, run the CLI with verbose output and inspect the arguments of every find-rules call.

  Do you train models on our data?  

No. Your rules, your task context, and your usage data are never used to train models, ours or anyone else's. We also never share your rule definitions with other organizations, and we never sell or monetize usage data.

  Where is our data hosted?  

Straion is a hosted SaaS running in the EU, and the models it uses for rule selection run in the EU as well. Data is encrypted in transit with TLS and encrypted at rest. Bring your own cloud deployment is on the roadmap for larger enterprises.

  Are you SOC 2 or ISO 27001 certified?  

Not yet. Today Straion runs GDPR-compliant data handling with encryption in transit and at rest, and we are working towards SOC 2 Type II certification. If a certification is a requirement for your team, write to team@straion.com and we will share our current status and timeline.

  Where are my rules stored?  

In your own Git. Straion creates a dedicated branch in your repository and stores each rule as a plain Markdown file, grouped into collections. It works with GitHub, GitLab, Bitbucket, and self-hosted providers. Rule changes go through pull requests, so your CODEOWNERS, branch protection, and required approvals apply to rules exactly as they do to code, and your existing CI syncs every merge to Straion automatically. The files are yours: if you ever leave, you keep every rule in plain text, with no export request needed.

  What happens to our rules if we stop using Straion?  

You keep them. Rules are plain Markdown files, and on the Enterprise plan they live on a dedicated branch in your own repository, so you already have every rule in plain text with no export request needed. On request we delete your workspace data.

  Is Straion built for enterprise security requirements?  

Yes. Straion is designed for teams with strict requirements, including SSO/SAML, organization-scoped access, and managing rules, permissions, and versioning in your own Git system such as GitHub, GitLab, or Bitbucket.

 

## Still have questions? Send them over.

We answer security reviews, vendor questionnaires, and DPA requests directly. No sales
gate.

Write to team@straion.com, or start free and see the data flow yourself.

[Get Started Free
→](https://straion.app/auth/signup)  [Contact the team](mailto:team@straion.com)
