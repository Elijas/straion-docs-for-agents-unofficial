---
title: "Frequently Asked Questions"
source: https://straion.com/faqs
description: "Answers to the most common questions about Straion, setup, security, and AI coding guidance."
---

![A cave with hovering boxes containing a question mark](https://straion.com/.netlify/images?url=_astro%2Fhero-faq.CTu-733B.jpg&fm=jpg&w=1920&h=815&q=50&dpl=6a8da20a9a458300086d2212)

---

 

FAQs

# Frequently Asked Questions

Have questions about Straion? We’ve got you.

What is Straion?  

Straion is the governance layer for AI coding agents like Claude Code, Cursor, and GitHub Copilot. It stores your engineering standards as structured, version-controlled rules, selects only the rules relevant to each task, validates the agent's plan before code is written, and re-checks the resulting changes.

  What is AI coding governance?  

AI coding governance is the practice of making sure code written by AI coding agents follows an organization's architecture, security, and compliance standards. Straion does this by storing standards as structured rules, selecting the rules relevant to each task, and validating the agent's plan before any code is written.

  Does Straion write the code?  

No. Straion governs the agents that write code. It provides the right rules as context, validates the plan before implementation, and re-checks the changes, so the code your agents produce follows your standards from the start.

  Does Straion replace Cursor, Claude Code, or GitHub Copilot?  

No. Straion is not a code generator and does not replace your AI coding tools. It is a governance layer that works alongside them to make their output match your company standards without manual correction after every task.

  Which AI coding tools does Straion work with?  

Straion works with Claude Code, Cursor, and GitHub Copilot, including Copilot in VS Code and the GitHub Copilot CLI. It integrates through the official integration points of each agent, so your team keeps its existing workflow.

  How does Straion keep AI coding agents aligned with our standards?  

Straion selects only the rules relevant to each task based on team, repository, tech stack, and change type, then validates the agent's implementation plan against those rules before code is generated and re-checks the resulting code changes. Violations come back with the exact rule, location, and fix.

  How does Straion decide which rules apply to a task?  

Straion analyzes the task, including its intent, type, repository and file context, language, and framework, and selects the most relevant rules. This keeps the agent focused and avoids loading rules that do not apply.

  What happens when an agent's plan would violate a rule?  

Straion validates the agent's plan against your rules before any code is written and surfaces violations, so you can correct direction early instead of paying for wrong code and rework. It then re-checks the resulting changes.

  Does Straion help reduce token costs?  

Yes. Because rule files load all of your rules into context on every task, token spend climbs as agent usage scales. Straion selects only the rules relevant to each task, so less irrelevant context is loaded and you pay for fewer wasted tokens.

  How long does setup take?  

About five minutes. Install the Straion CLI, connect your repository as a rule source with `straion source repo connect`, and Straion creates the rules branch and the auto-sync pipeline for you. Importing your existing rules is part of that setup.

  Do I have to rewrite my existing rules?  

No. You import your existing CLAUDE.md, AGENTS.md, and rule files into Straion once, so nothing you have built is lost. The imported rules land as plain files on a dedicated branch in your own repository, where you edit them with commits and pull requests. From there onwards Straion is the single source of truth, so you delete the rules from the scattered files.

  How is Straion different from just using .md files in my repos?  

The problem is not that those files sit in Git. It is that the same rules get copied into every repo, drift apart, and load into context whole on every task, so you pay tokens for rules that do not apply. Straion keeps one source of truth, which can live on a dedicated branch in your own Git, and selects only the rules relevant to each task.

  Should Straion replace my CLAUDE.md and AGENTS.md files, or run alongside them?  

Straion replaces the rules in those files. Import the rules as part of setup, then delete them from CLAUDE.md and AGENTS.md. Anything else in those files can stay, like project structure, build commands, or local setup notes. You do not leave Git behind: your rules can still be managed in your own Git provider, centrally instead of copied into every repo. If you leave the rules in the files as well, your agent loads them twice and you pay tokens for the duplicate.

  What is the difference between AGENTS.md and Straion?  

AGENTS.md is a static markdown file that lists instructions for an AI coding agent in a single repository. Straion is a governance layer that stores your standards as structured, version-controlled rules, selects only the rules relevant to each task, and enforces them across every team, repository, and AI tool. AGENTS.md is a file; Straion is a system.

  Can I import my existing AGENTS.md and CLAUDE.md files into Straion?  

Yes. Straion ingests your existing AGENTS.md, CLAUDE.md, and .cursorrules files and turns them into structured, managed rules. You use your markdown as input, not as infrastructure, so there is nothing to rewrite from scratch.

  Why do AGENTS.md and CLAUDE.md files stop working at scale?  

A single markdown file cannot govern dozens of repositories and hundreds of engineers. Rules get duplicated and drift out of sync, you have no visibility into which rules the agent actually used, and every tool needs its own file (CLAUDE.md, .cursorrules, copilot-instructions.md). Research also shows that dumping every rule on the agent regardless of the task reduces resolve rates and inflates cost.

  Does a bigger context window make AGENTS.md files good enough?  

No. More context does not fix relevance. Studies across thousands of agent runs found that stuffing large context windows with static rules degrades performance rather than improving it. Straion selects only the rules that matter for the current task instead of loading everything.

  What is the difference between custom skills and Straion?  

A custom skill is a file that loads a block of instructions into an AI coding agent when its title or description matches the task. Straion is a governance layer that stores your standards as structured, version-controlled rules, selects only the rules relevant to each task, and validates the agent's plan before code is written. A skill is a file; Straion is a system.

  Can I import my existing custom skills into Straion?  

Yes. Straion ingests your existing skill files, along with your CLAUDE.md and AGENTS.md, and turns them into structured, managed rules. The work you have already done becomes the foundation, so there is nothing to rewrite from scratch.

  Why do custom skills stop working at scale?  

Skills are all-or-nothing: when one fires its entire content lands in context, and the trigger is just a title or description match. Across many repos and engineers, skill files get duplicated and drift out of sync, you have no visibility into which rules the agent actually used, and validation only happens later in code review. Research also shows that dumping every rule on the agent regardless of the task reduces resolve rates and inflates cost.

  How are rules structured?  

A rule is an RFC 2119 statement that starts with MUST, MUST NOT, SHOULD, SHOULD NOT, or MAY, plus metadata such as tags, languages, and frameworks, and provenance. Rules live in collections and each has a stable id. You can manage them in your own Git provider, so every change is versioned and reviewed like code.

  Where are my rules stored?  

In your own Git. Straion creates a dedicated branch in your repository and stores each rule as a plain Markdown file, grouped into collections. It works with GitHub, GitLab, Bitbucket, and self-hosted providers. Rule changes go through pull requests, so your CODEOWNERS, branch protection, and required approvals apply to rules exactly as they do to code, and your existing CI syncs every merge to Straion automatically. The files are yours: if you ever leave, you keep every rule in plain text, with no export request needed.

  Can we manage our rules in our own Git?  

Yes. Straion stores your rules as plain files on a dedicated branch in your own repository, and syncs them on every commit through your existing CI. It works with GitHub, GitLab, Bitbucket, and self-hosted providers. This is part of the Enterprise plan, and it is included in the 14-day free trial.

  Is Straion built for enterprise security requirements?  

Yes. Straion is designed for teams with strict requirements, including SSO/SAML, organization-scoped access, and managing rules, permissions, and versioning in your own Git system such as GitHub, GitLab, or Bitbucket.

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

  What happens to our rules if we stop using Straion?  

You keep them. Rules are plain Markdown files, and on the Enterprise plan they live on a dedicated branch in your own repository, so you already have every rule in plain text with no export request needed. On request we delete your workspace data.

  Is there a free trial?  

Yes. Every Team plan starts with a 14-day free trial, full access to all features, no credit card required.

  Can I switch plans anytime?  

Yes. We can move you between plans as your team scales.

  Do you offer discounts for startups?  

Yes, reach out and we can discuss startup-friendly options.

[Still have questions? Contact us](mailto:team@straion.com)
