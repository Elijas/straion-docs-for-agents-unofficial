---
title: "See the Straion Audit Trail Live in Claude Code"
source: https://straion.com/blog/audit-trail-in-claude-code
description: "straion-trail is a Claude Code mod that shows what Straion corrected while the agent works, and tells you when it waits for your approval."
---

[← Back to blog](../blog.md "Back to blog")

# See the Straion Audit Trail Live in Claude Code

October 12, 2026 · 4 min read · by  [Fabian Friedl](https://straion.com/blog/about/fabian-friedl)

AI Coding Agents  Claude Code  Audit Trail  Straion  Product

## TLDR;

straion-trail is a Claude Code mod that shows what Straion corrected while the agent works, and tells you when it waits for your approval.

A few weeks ago we shipped the [audit trail](rule-violations-code-review.md). If you missed it, Straion hands the agent the rules that apply to a task, and the agent has to record a decision for each one before it can end its turn. A violation either gets fixed, or the agent proposes to accept it or mark it as not applicable, and for those two it needs your approval.

The trail is stored on your machine, one file per session. You read it with `straion audit view`, but only once the session has ended. While the agent works, Straion’s checks are buried in the agent logs, between tool calls and diffs. To find out whether Straion caught something, or whether the agent is fixing a violation, you have to scroll through the logs. Or you wait for the audit trail at the end of the session.

Anthropic recently released [mods for Claude Code](https://claude.com/blog/claude-code-mods), and we built one that shows the audit trail live.

## What’s a mod?

Mods are plugins that can add your own UI to Claude Code, a side pane for example, or a line in the status bar. You install them like any other plugin, and they work in the CLI and in the Code tab of the desktop app.

Everything Straion knows about a session, the rules it matched, the verdicts, the fixes, is already in the audit trail. The mod builds on top of that. The pane is only the place where it shows up while the agent works.

## straion-trail

`straion-trail` is a live side pane of what Straion corrected the agent on, and the exceptions you approved. Your rules should be as visible as your diff. We focus on what you need to know while the agent works: what it got wrong, and whether it fixed it. It comes with our Claude Code integration. Run setup and pick Claude Code:

```bash
straion setup
```

Make sure your audit.mode is set to trail or gate:

```bash
straion config audit.mode trail
```

Now run `/straion-trail` in Claude Code. A pane titled “Straion” opens. As long as nothing has happened it shows “Straion is watching”.

   ![A Claude Code terminal session. The /straion-trail command prints 'Straion pane opened.' and below it a bordered pane reads 'Straion is watching' and 'Corrections show up here'.](https://straion.com/.netlify/images?url=_astro%2F2026-10-06-trail-terminal-watching.Cjpa9ATD.png&fm=png&w=2938&h=287&dpl=6ace00993fb9a7907df57551)  

The empty pane in the terminal, before Straion has caught anything.

 

One of the sessions we ran it on: Claude Code upgrading cppcheck in opendbc and fixing the MISRA 10.3 findings, which are integers that get assigned to bools. Straion found 4 rules for the task, and the pane shows “Straion kept everything on track” and “4 rules checked”.

   ![The Claude Code desktop app in light mode. The agent summarizes a cppcheck upgrade and MISRA fix in opendbc. On the right, the Straion pane shows the Straion signet, 'Straion kept everything on track' and '4 rules checked', followed by an expanded list of four compliant rules, among them 'MUST NOT use magic values in code'.](https://straion.com/.netlify/images?url=_astro%2F2026-10-06-trail-pane-on-track.tAA5iawO.png&fm=png&w=2000&h=1249&dpl=6ace00993fb9a7907df57551)  

A session in opendbc. We expanded the compliant rules for the screenshot. Normally they are folded away.

 

## When the agent gets something wrong

When Straion corrects the agent, the rule goes to the top of the pane with a red dot and the fix the agent is working on. Once it’s fixed, the dot turns into a green check. The header counts how often Straion corrected the agent and shows, for example “2 fixed · 1 in progress” below. If the agent wants to keep a violation and waits for you, a yellow “Your approval is needed” row shows up.

Approved exceptions and compliant rules are folded away behind a toggle. A long list of compliant rules doesn’t help much while the agent works. What you look for is the one rule that needs attention.

We also added notifications to Claude Code, so you know when Straion needs your approval, even when the pane isn’t in view.

## How it works

The pane reads the same audit trail as the report, so what you see live is what ends up in the report. It doesn’t add any verification on top. The agent still grades its own work, and if it calls a rule compliant, you’ll see it as compliant.

## Try it

Mods are a Claude Code feature, which means the pane is Claude Code only. If your team is on Cursor or GitHub Copilot, the audit trail works as well, and you read it with `straion audit list` and `straion audit view` like before.

If you’re on Claude Code, run:

```bash
straion setup
straion config audit.mode trail
```

Pick Claude Code during setup. Then run `/straion-trail` in Claude Code, give the agent some real work, and keep the pane open next to it. Seeing a correction and the fix in the same minute gives you a lot more trust in what the agent does than a report you open the next day. If you have ideas about what else the pane should show, or you’re building your own mods, let us know.

---

## Stay on Track. Start for free.

See how Straion keeps your AI coding agent aligned with your standards.   
Set up takes
less than 5 minutes.

[Get Started Free
→](https://straion.app/auth/signup) 

Works with Claude Code, GitHub Copilot & Cursor. No credit card required.

---

**Stay on track.**

Fabian

---

![Fabian Friedl](https://straion.com/.netlify/images?url=_astro%2Ffabian.Bq-43Efc.jpg&fm=jpg&w=500&h=500&dpl=6ace00993fb9a7907df57551) 

Written by Fabian Friedl

[← Back to blog](../blog.md "Back to blog")
