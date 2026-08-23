---
title: "Your AGENTS.md is costing more than you think"
source: https://straion.com/blog/delete-your-claude-md-science-says-so
description: "ETH Zurich research: LLM-generated AGENTS.md and CLAUDE.md files cut resolve rates and raise cost. The fix is delivering only the rules that matter, per task."
---

[← Back to blog](../blog.md "Back to blog")

# Your AGENTS.md is costing more than you think

March 3, 2026 · 5 min read · by  [Fabian Friedl](https://straion.com/blog/about/fabian-friedl)

AI Coding Agents  AGENTS.md  CLAUDE.md  Research  Straion

## TLDR;

ETH Zurich research: LLM-generated AGENTS.md and CLAUDE.md files cut resolve rates and raise cost. The fix is delivering only the rules that matter, per task.

If you’ve been working with AI coding agents recently, chances are you’ve set up or at least seen some kind of context file. AGENTS.md, CLAUDE.md, .cursorrules, the names change depending on the tool, but the idea is the same: give the agent a set of rules and guidelines so it writes code the way your team expects.

We’ve been thinking about this problem a lot at Straion.

Researchers from ETH Zurich’s SRI Lab published [“Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?”](https://arxiv.org/abs/2602.11988), the first rigorous study testing whether these files actually improve agent performance. They evaluated **four coding agents** (Claude Code with Sonnet 4.5, Codex with GPT-5.2 and GPT-5.1 Mini, Qwen Code with Qwen3-30B) across **two benchmarks**: the established SWE-bench Lite (300 tasks from 11 popular Python repos) and a brand-new benchmark called AGENTbench (138 instances from 5,694 PRs across 12 repositories with developer-committed context files).

The results should make every engineering leader and developer rethink their context file strategy.

## LLM-generated context files actually hurt agent performance

The files you get when you run `/init` or ask an LLM to generate your coding guidelines? Those reduced task success rates by ~3% on average and increased inference cost by over 20%. They didn’t just fail to help, they actively made things worse while costing more.

The researchers also tested whether better models produce better context files. The short answer: not really. GPT-5.2-generated files improved resolve rates by 2% on SWE-bench Lite but degraded performance by 3% on AGENTbench. Swapping generation prompts between agents didn’t produce a consistent winner either. The problem isn’t which model generates the file; it’s the approach itself.

Despite 100% of Sonnet 4.5-generated and 99% of GPT-5.2-generated context files containing codebase overviews, **agents took roughly the same number of steps to reach the files that needed changing**. The overviews didn’t help them navigate faster. They just burned tokens.

## Developer-written files help, but not by much

Developer-written context files performed better than the auto-generated ones, showing a slight improvement over having no context file at all. But that’s the best case scenario, where a skilled engineer carefully writing focused, minimal guidance and even then the ceiling is modest.

The paper’s behavioral analysis offers a good explanation for why. Both LLM-generated and developer-written files encourage agents to explore more broadly; more testing, more file traversal. In theory that sounds useful. In practice, agents end up spending cycles on rules that have nothing to do with the task at hand. One agent (GPT-5.1 Mini) even wasted steps re-reading context files that were already loaded into its context window.

More context doesn’t automatically mean better outcomes. The research is pretty clear on that.

## The underlying issue: static files have no concept of relevance

A static context file, whether it’s AGENTS.md, CLAUDE.md, .cursorrules, or copilot-instructions.md, dumps everything on the agent regardless of the task. Every task gets every rule, every time.

## Delivering context dynamically, per task

The ETH Zurich findings align closely with the approach we’ve been building at Straion. The researchers concluded that context files should be minimal and focused on essential rules. But “minimal” as a static file forces an uncomfortable choice: include everything (and hurt performance), include almost nothing (and lose the value of your standards) or restructure repositories to try to provide targeted context files.

There’s another option: **Deliver only the rules that matter for the specific task, dynamically, at the moment the agent needs them.**

That’s what Straion does. When a coding agent picks up a task, Straion’s pipeline analyzes the full task context, the prompt, the entire plan and the files being touched and selects only the relevant rules from a centralized rule hub. Fixing a React component? The agent gets frontend conventions, component patterns, accessibility standards. Not your backend architecture rules.
Patching a security issue? Your agent gets compliance constraints and security policies. Not your CSS naming conventions.

The agent gets **sharp, narrow context**. No bloat, no noise, no wasted tokens on rules that don’t apply.

## One line instead of two hundred

If the research says static context files should be minimal. What’s the minimum that still works?

We’ve landed on a single instruction:

```markdown
# AGENTS.md

Always validate your plan and tasks with Straion.
```

No 200-line rule dump that degrades performance. No nested markdown files bloating the context window. No duplicated standards across repos that nobody keeps in sync.

Every AI coding tool, Claude Code, Cursor, Copilot, whatever your team uses reads this one line, checks in with Straion, and gets exactly the rules it needs. Nothing more.

---

## Stay on Track. Start for free.

See how Straion keeps your AI coding agent aligned with your standards.   
Set up takes
less than 5 minutes.

[Get Started Free
→](https://straion.app/auth/signup) 

Works with Claude Code, GitHub Copilot & Cursor. No credit card required.

---

## Where we go from here

Reading through the ETH Zurich paper was a bit of a wake-up call for the industry. The convention of AGENTS.md spread everywhere without anyone measuring whether it actually works. Now that we have data, it’s worth taking a step back.

If you’re maintaining context files across your repos, it might be worth auditing them: How many do you have, when were they last updated, and are they even consistent?

Your engineering standards are valuable. The problem isn’t the content; it’s dumping it all into a flat file and hoping the agent sorts it out.

We are building Straion to get the right context to agents without drowning them in noise, and this research confirms that the current approach of static context files has major flaws. If you’re thinking about this or have ideas, we’d love to hear from you.

**Stay on track.**

Fabian

---

**References:**

Gloaguen, T., Mündler, N., Müller, M., Raychev, V., & Vechev, M. (2026). *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* arXiv:2602.11988. <https://arxiv.org/abs/2602.11988>

---

![Fabian Friedl](https://straion.com/.netlify/images?url=_astro%2Ffabian.Bq-43Efc.jpg&fm=jpg&w=500&h=500&dpl=6a85597a97a15700076a9c5e) 

Written by Fabian Friedl

[← Back to blog](../blog.md "Back to blog")
