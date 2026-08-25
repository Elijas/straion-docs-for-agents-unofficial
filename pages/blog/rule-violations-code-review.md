---
title: "You Shouldn't Be Finding Rule Violations in Code Review"
source: https://straion.com/blog/rule-violations-code-review
description: "Straion turns every rule that applies to a change into a decision the agent has to resolve before the work is done, and every exception into one you approve."
---

[← Back to blog](../blog.md "Back to blog")

# You Shouldn't Be Finding Rule Violations in Code Review

August 12, 2026 · 5 min read · by  [Fabian Friedl](https://straion.com/blog/about/fabian-friedl)  and  [Katrin Freihofner](https://straion.com/blog/about/katrin-freihofner)

AI Coding Agents  Engineering Leadership  Claude Code  Straion  Product

## TLDR;

Straion turns every rule that applies to a change into a decision the agent has to resolve before the work is done, and every exception into one you approve.

Your agent knows your rules. It just doesn’t have to follow them. Straion turns every rule that applies to a change into a decision the agent has to resolve before the work is done, and every exception into one you approve.

## You can’t tell whether the agent followed your rules

You’ve written the standards down. Straion already finds the ones that apply to a change and puts them in front of the agent. That part works.

Then the agent writes the code and tells you how it went. Twelve rules checked, all good.

Maybe that’s true. You have no way to tell, so you check. This is how a senior engineer’s week fills up with work a machine should have done. A violation you miss doesn’t just sit there: the next agent reads that file, treats it as the way things are done here, and writes more code like it.

## Violations get resolved before you see the PR

An agent that breaks a rule today produces, at most, a line of text. The turn ends, the diff is ready, and the violation is now yours to catch.

With Straion, the agent can’t finish its turn while a rule is unresolved. Every rule Straion matched needs a decision, and there are exactly three: **fix** it, **accept** the violation, or say the rule is **not applicable** here. Fix is silent, the agent gets on with it, and can’t stop until the fix lands. The other two are yours.

This changes what you review. By the time a PR reaches you, its rule violations have already been fixed or accepted, so you can spend the review on design and intent.

## Nothing ships broken unless you approve it

Not every violation is worth fixing right now. Sometimes you take the tradeoff and accept the violation on purpose. That’s a judgment call about your codebase, and today the agent makes it alone.

Now it comes to you:

```text
Rule  [3kQ9fX2a]  (Backend conventions)
  MUST NOT throw GraphQLError from service classes; resolvers and
  filters own GraphQL error shaping.

Agent claims:  violation
Proposed:      accept, ship the violation
Reason:        "legacy invite path, tracked in JIRA-412"
Files:         services/gateway/src/organization/invite.service.ts

Approving records your decision in the audit trail.
```

The rule you see is the rule as written, not the agent’s summary of it. Every line in that prompt comes from Straion’s own record, so nothing can be softened on the way to you. You see the file. You approve or you reject. Straion records the decision you actually wanted.

You see this rarely, by design. An agent that finds a violation, fixes it, and records compliance interrupts you **zero times**. A rule already decided in this session isn’t put in front of you a second time. You’re pulled in for one thing: something is about to ship broken on purpose.

## Six months later, you can still answer why

Someone asks why that service throws a `GraphQLError` when your own rules say it shouldn’t.

Right now the answer is archaeology: scroll the PR, hope someone remembers. With Straion it’s a lookup: the rule, the reason, who approved it, when. Every exception has a name attached.

Your approval is captured by the tooling at the moment you give it, not reported afterwards by the agent. Nobody has to take the agent’s word for who agreed to what. Post the audit trail on your PRs, or store it next to your code, and you have a full record. Which rules applied, which violations were accepted, and by whom.

## What it doesn’t do

The agent still judges whether a rule was met. If it evaluates a rule and calls it compliant, no one is asked, and we’re not going to pretend otherwise.

What you get is narrower, and more useful than a vague claim of correctness:

> **Every rule that applied got a decision, and every violation that shipped was accepted by a person.**

## Early access

We’re opening this to a small number of teams before it goes public. You’re a good fit if you already have written coding standards, and have struggled with pointing out the same violations week by week.

## Request early access

---

## FAQ

### How often will it actually interrupt me?

Only when a violation is about to be left unfixed. Fixed is silent, compliant is silent, and the same rule isn’t raised twice in a session.

One deliberate exception: if you accept a violation and the agent later rewrites that file, you’ll be asked again. Your approval was about code that no longer exists.

### Can I get out of it when I’m in a hurry?

Yes, and that’s a requirement rather than a gap. Accepting a violation with a reason resolves any rule, and you can always just interrupt the agent. The agent can’t end a turn with rules left open; you always can, and the trail records that the session ended that way. You’re never blocked.

### Which coding agents does this work with?

Claude Code, GitHub Copilot (with the Copilot CLI installed) and Cursor are supported.

None of the logic is tied to a specific agent. Each additional one is a small adapter, not a second implementation.

### Could the agent fake an approval?

Your approval isn’t something the agent reports. It’s derived from two processes it doesn’t control. A hook the harness runs before the command records that you were asked; the command only runs at all if you said yes. The agent can tell us what you said. It can’t fake the human in the loop.

### What happens in CI, or with an unattended cloud agent?

Nobody is there to approve, so nothing gets approved. Where the prompt can’t be answered, the command is refused rather than waved through. An unattended run can fix a violation; it cannot accept one.

### Do I have to write new rules for this?

No. It works on the rules Straion already surfaces, including ones imported from your existing `CLAUDE.md`, `AGENTS.md`, or `.cursor/rules`.

---

## Stay on Track. Start for free.

See how Straion keeps your AI coding agent aligned with your standards.   
Set up takes
less than 5 minutes.

[Get Started Free
→](https://straion.app/auth/signup) 

Works with Claude Code, GitHub Copilot & Cursor. No credit card required.

---

---

![Fabian Friedl](https://straion.com/.netlify/images?url=_astro%2Ffabian.Bq-43Efc.jpg&fm=jpg&w=500&h=500&dpl=6a8da20a9a458300086d2212) 

Written by Fabian Friedl

![Katrin Freihofner](https://straion.com/.netlify/images?url=_astro%2Fkatrin.qSA9g74x.jpg&fm=jpg&w=500&h=500&dpl=6a8da20a9a458300086d2212) 

Written by Katrin Freihofner

[← Back to blog](../blog.md "Back to blog")
