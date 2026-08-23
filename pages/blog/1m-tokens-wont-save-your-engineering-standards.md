---
title: "1M Tokens Won't Save Your Engineering Standards"
source: https://straion.com/blog/1m-tokens-wont-save-your-engineering-standards
description: "Sourcegraph data from 1,281 agent runs confirms the research: more context degrades AI coding performance. Why less context wins, and what it means for tools."
---

[← Back to blog](../blog.md "Back to blog")

# 1M Tokens Won't Save Your Engineering Standards

March 19, 2026 · 
Updated May 21, 2026  · 17 min read · by  [Lukas Holzer](https://straion.com/blog/about/lukas-holzer)

AI Coding Agents  Context Windows  Research  Straion  Engineering Leadership

## TLDR;

Sourcegraph data from 1,281 agent runs confirms the research: more context degrades AI coding performance. Why less context wins, and what it means for tools.

> **Update, May 2026:** Two months after this post went out, Sourcegraph published [*Why coding agents fail in large codebases*](https://sourcegraph.com/blog/why-coding-agents-fail-large-codebases), 1,281 agent runs across 40+ of the largest open source repositories. Their conclusion: *“The solution is not a bigger context window; it’s a smarter selection of what goes into the window.”* That’s the same prediction I made in March, now backed by production-scale data. I’ve added a new section below ([Update, May 2026: the empirical evidence is in](#update--may-2026-the-empirical-evidence-is-in)) and refreshed the conclusion. The original argument is unchanged.

[Claude Code just got a one million token context window.](https://claude.com/blog/1m-context-ga) Gemini offers two million. The industry is celebrating. LinkedIn is full of posts about holding entire codebases in a single session, eliminating token budgets, running 28 skills and 24 agents simultaneously in one massive context.

I get the excitement. Bigger context windows remove real friction. No more phasing work across sessions, no more compressing instructions to stay under the limit.

But if you’re an engineering leader hoping that a million tokens will **finally make your AI coding agents follow your internal standards**, the research says you’re betting on the wrong thing. And as of May 2026, the empirical field data says the same.

## What actually breaks when rules get ignored

Before we get into the science, let’s look at what this problem looks like in practice.

Your team runs a Go microservice architecture. **You have clear rules:**

- all inter-service communication goes through the internal `serviceclient` package.
- It must handle:
  - circuit breaking
  - distributed tracing via OpenTelemetry
  - retries with exponential backoff
  - standardized error wrapping

It’s documented. It’s in your `AGENTS.md` or `CLAUDE.md` file. Every engineer on the team knows it.

An AI coding agent picks up a task to integrate with the payments service. It writes clean, idiomatic Go. Tests pass. The PR looks fine at first glance.

```go
// ❌ What the agent generated (direct HTTP calls)
func (s *OrderService) ProcessRefund(ctx context.Context, orderID string) error {
    order, err := s.repo.GetOrder(ctx, orderID)
    if err != nil {
        return fmt.Errorf("fetch order: %w", err)
    }

    payload, err := json.Marshal(RefundRequest{
        OrderID: order.ID,
        Amount:  order.Total,
        Reason:  "customer_request",
    })
    if err != nil {
        return fmt.Errorf("marshal refund request: %w", err)
    }

    req, err := http.NewRequestWithContext(ctx, http.MethodPost,
        "http://payments-service:8080/api/v1/refunds", bytes.NewReader(payload))
    if err != nil {
        return fmt.Errorf("create request: %w", err)
    }
    req.Header.Set("Content-Type", "application/json")

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return fmt.Errorf("call payments service: %w", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusCreated {
        body, _ := io.ReadAll(resp.Body)
        return fmt.Errorf("refund failed (status %d): %s", resp.StatusCode, body)
    }

    return s.repo.MarkRefunded(ctx, orderID)
}
```

This compiles. Tests pass with a mock HTTP server. The logic is correct. But it’s a production incident waiting to happen:

- **No circuit breaking.** If the payments service goes down, every refund request will hang for 30 seconds and pile up. No fallback, no fast failure.
- **No tracing.** The OpenTelemetry span is gone. When something breaks at 2 AM, your on-call engineer sees the order service call but no downstream trace. Debugging takes hours instead of minutes.
- **No retries.** Transient network failures (which happen constantly in Kubernetes) cause permanent refund failures. Customers don’t get their money back.
- **No standardized errors.** Your middleware can’t map the error to the right HTTP status code. Your error tracking groups it as “unknown.”

Here’s what it should look like:

```go
// ✅ What it should have generated (using the internal service client)
func (s *OrderService) ProcessRefund(ctx context.Context, orderID string) error {
    order, err := s.repo.GetOrder(ctx, orderID)
    if err != nil {
        return fmt.Errorf("fetch order: %w", err)
    }

    refundReq := RefundRequest{
        OrderID: order.ID,
        Amount:  order.Total,
        Reason:  "customer_request",
    }

    var refundResp RefundResponse
    err = s.paymentsClient.Post(ctx, "/api/v1/refunds", refundReq, &refundResp)
    if err != nil {
        return apperror.Wrap(err, apperror.CodeUpstream,
            "process refund for order %s", orderID)
    }

    return s.repo.MarkRefunded(ctx, orderID)
}
```

Half the lines. But behind `s.paymentsClient.Post()`, you get circuit breaking, OpenTelemetry spans, retries with backoff, and structured error codes. All enforced automatically.

The refactoring cost? This isn’t adding an attribute. You’re rewriting the entire function, introducing a new dependency, updating the constructor, changing the test setup from mock HTTP servers to mock service clients, and verifying that error codes propagate correctly through your middleware. That’s an hour of rework. Per function.

Now multiply this by every service call the agent writes across your codebase. Each missed rule is another hour of rework, another PR review cycle, another “please use the service client” comment. And if it slips through review, it’s a production incident.

That’s the problem. And pouring a million tokens of context into the window doesn’t fix it. Here’s why.

## The assumption everyone is making

The implicit belief behind the one million token context hype is simple: if we can fit more into the context window, the agent will know more and perform better. More rules, more docs, more architecture decisions, more history. All in one session. Problem solved.

It sounds logical. It’s also wrong.

The relationship between context size and rule adherence isn’t linear. It’s closer to an inverted curve: you add more rules, the output quality improves, peaks, then degrades as you keep adding more. This degradation starts much earlier than most people expect.

## What the research actually shows

### Every model degrades as input length increases

In July 2025, researchers at Chroma published [“Context Rot”](https://research.trychroma.com/context-rot), a study testing 18 frontier models including GPT-4.1, Claude 4, Gemini 2.5, and Qwen3. Their finding was unambiguous: **every single model tested gets worse as input length increases.** None are immune.

The critical insight: context rot isn’t about hitting the context window limit. It occurs well before that. Models with 200K token windows showed measurable degradation at 50K tokens. The researchers found that **all models fell far short of their maximum context window by more than 99%** when it came to reliable performance. A one million token window doesn’t mean one million tokens of useful capacity. Not even close.

### Information in the middle gets lost

Stanford researchers Nelson Liu, Kevin Lin, John Hewitt et al. demonstrated this in [“Lost in the Middle: How Language Models Use Long Contexts”](https://arxiv.org/abs/2307.03172), published in the Transactions of the Association for Computational Linguistics. They found an **accuracy drop of 30%+** when relevant information was placed in the middle of the context versus the beginning or end.

Think about what that means for engineering standards. You dump 200 rules into the context. The rules at the top and bottom get attention. The 150 rules in the middle? The model’s attention drifts right past them. Not because the context window is too small, because the attention spreads thinner as you add more context.

This isn’t a bug that will get fixed with the next model release. It’s a fundamental property of how transformers work. More tokens means it’s more likely that some tokens get overlooked. It’s a zero-sum game.

Accuracy by position of relevant information in context

[Liu et al., "Lost in the Middle" (TACL 2024)](https://arxiv.org/abs/2307.03172) · Illustrative data based on reported findings

**The U-shaped curve:** Models focus on the beginning and end of the context. Rules placed in the middle, where most guidelines end up in a large AGENTS.md, get the least attention. In a one million token context, the "middle" is enormous.

### More instructions = worse compliance

Researchers Daniel Jaroslawicz et al. tested this directly in [“How Many Instructions Can LLMs Follow at Once?”](https://arxiv.org/abs/2507.11538) using a benchmark called IFScale with 500 keyword-inclusion instructions. Their finding: **even the best frontier models only achieve 68% accuracy at maximum instruction density.**

68%. That means a third of your rules get ignored. Not because the model can’t see them, but because there are too many competing for attention. The more rules you add, the less likely any individual rule is to be followed.

Instruction compliance drops as rule count increases

[Jaroslawicz et al., IFScale (2025)](https://arxiv.org/abs/2507.11538) · Projected curves anchored to IFEval single-instruction scores

**More rules = lower compliance per rule.** Opus 4.6 scores 94% and Sonnet 4.6 scores 89.5% on IFEval (low-density, 1 to 3 instructions). But as instruction count climbs to 500, even the best models drop significantly. Adding 500 engineering guidelines doesn't mean 500 rules followed. Each rule is *less* likely to be applied.

This is the core problem with the “put everything in context” approach to engineering standards. You’re not helping the agent by giving it all of your guidelines at once. You’re making it less likely to follow any specific one.

## Update, May 2026: the empirical evidence is in

When I published this in March, the case rested on three controlled studies, Chroma’s Context Rot, Stanford’s Lost in the Middle, and the IFScale benchmark. All rigorous, all directionally consistent, but all stopping short of one thing engineers ask for: **what happens when you point real coding agents at real codebases and watch them work?**

On May 8, 2026, Sourcegraph answered that question. They published [*Why coding agents fail in large codebases*](https://sourcegraph.com/blog/why-coding-agents-fail-large-codebases), summarizing results from [CodeScaleBench](https://sourcegraph.com/blog/codescalebench-testing-coding-agents-on-large-codebases-and-multi-repo-software-engineering-tasks): **1,281 scored agent runs across 40+ of the largest open source repositories, spanning 9 programming languages.**

The headline finding lands almost word-for-word on the March thesis:

> *“The solution is not a bigger context window; it’s a smarter selection of what goes into the window.”* Stephanie Jarmak, Sourcegraph

That isn’t a quote from a Straion deck. It’s the conclusion of a different company, looking at a different surface area (retrieving code, not rules), running a large-scale evaluation of coding agents on production-scale repositories.

Let me be upfront about the obvious objection: Sourcegraph is not a neutral party. They sell structured code retrieval, and CodeScaleBench is their own benchmark, its conclusion is also their pitch. So is ours; Straion sells structured rule retrieval. That’s exactly why the methodology is what matters here, not the logo: 1,281 scored runs, 40+ repositories, 9 languages, all public and reproducible. Judge the data, not the brand on it. And the data arrives at exactly the principle the controlled research predicted: **less, better-selected context beats more, undifferentiated context.**

Here’s what the new data adds.

### The five failure modes are all context-management failures

Sourcegraph’s analysis identifies five repeatable ways coding agents fail at scale:

1. **Lost in the codebase**, endless navigation that never converges on output.
2. **Wrong file, wrong symbol**, lexical match without structural ranking.
3. **Partial completion**, finds *some* affected files, misses the rest.
4. **Tool thrashing**, dozens of redundant searches and reversals.
5. **Context overflow**, reads too much irrelevant code and loses focus.

Read that list again. Every single one of them is a context-management problem. Not a model capability problem. Not a reasoning problem. **A problem of getting the right information in front of the model and keeping everything else out.**

Sourcegraph says this explicitly: *“These are context problems, not intelligence problems.”* Which is the same point I tried to make in March from a different direction: you cannot make engineering standards stick by giving the agent more tokens. You can only make them stick by giving the agent the right tokens.

### Context overflow: the cleanest validation of the March thesis

Failure mode #5 deserves its own callout because it is almost a literal restatement of what Chroma’s Context Rot and Stanford’s Lost in the Middle predicted in the lab.

From Sourcegraph:

> *“Providing agents with more tools sometimes made this worse, likely because they weren’t given sufficient strategic information on when and how to use them… More retrieved code doesn’t improve performance if the model can’t effectively access it.”*

And:

> *“Research on long-context language models shows they struggle to use information in the middle of long contexts. When an agent stuffs its context with search results, the most relevant information may end up in the worst position for the model’s attention.”*

To be precise about what’s new here: Sourcegraph isn’t independently re-measuring positional attention decay, the quote above is them reaching for the same long-context research to *explain* what they saw. What they contribute is the observation that “context overflow” is a distinct, repeatable failure mode at scale, against real repositories like Kubernetes (1.4 million lines, 22,000 files). *Lost in the Middle* supplied the mechanism on synthetic tasks; CodeScaleBench shows that mechanism biting production-grade coding agents doing real work.

This is the single most important update to the March piece. The “you can’t beat attention dilution with more tokens” claim is no longer just a lab extrapolation, the failure mode it predicts was observed, named, and counted across 1,281 agent runs.

### Tool thrashing: 96 calls vs. 5 calls

The most visceral data point in the Sourcegraph post is a single refactoring task:

|  | Tool calls | Time | Score |
| --- | --- | --- | --- |
| Baseline agent (local tools only) | 96 | 84 min | 0.32 |
| Agent with structured retrieval | 5 | 4.4 min | 0.68 |

Same model. Same task. Different retrieval infrastructure. **19× more tool calls. 19× more time. Half the score.**

This isn’t just a slower agent, it’s a structurally worse one. Sourcegraph nails the secondary effect:

> *“Each backtrack leaves residue in the conversation history, file contents that are no longer relevant but still consume context. By the time the agent finds the right files, it may have less context to produce output than it would have had if it had found them on the first try.”*

Translate that to rule adherence and the implication is brutal. Every irrelevant rule you pile into AGENTS.md isn’t just attention noise at the start. It crowds out the rules that actually matter for the task at hand. The cost compounds.

### The reward delta tells you when retrieval starts paying off

This is the engineering number, the one that tells you *at what codebase size* structured retrieval stops being overhead and starts being essential:

> *“Agents with only local tools (grep, file read, glob) begin to struggle systematically when codebases exceed roughly 400,000 lines of code. The reward delta when code intelligence tools are added: +0.259 in the 400K–2M LOC range.”*

In smaller codebases (under 400K LOC), structured retrieval added overhead and *hurt* by 0.080. In larger ones, it gave a +0.259 reward improvement. That’s the shape we keep seeing: **right-sized context beats more context, in both directions.** Too much retrieval on a small problem is just noise. Too little retrieval on a large problem is failure.

There is no universal answer to “how much context.” There is only “the right context for this task.”

### MCP-augmented agents: 30% cheaper, 38% faster

And this is the number for the CFO conversation, cost and wall-clock, not abstract reward:

> *“MCP-augmented agents… are 30% cheaper ($0.51 per task vs. $0.73 baseline) and 38% faster on average.”*

The cost gain doesn’t come from a smarter model. It comes from not burning tokens on dead-end exploration. Same model, smaller bill, faster wall-clock, higher score. The economics of “throw more context at it” are getting harder to defend with every new dataset.

## The principle generalizes: code retrieval and rule retrieval are the same problem

Here is the part I want every engineering leader reading this to internalize.

Sourcegraph is solving structured retrieval of **code**. We at Straion are solving structured retrieval of **rules**. These are different surface areas, but they are exactly the same underlying problem:

> *Given a specific task, deliver the smallest possible set of high-signal tokens, and keep everything else out of the window.*

Sourcegraph’s data shows what happens to code generation when you get this right (and wrong). The IFScale and Context Rot results show what happens to instruction compliance when you get this right (and wrong). They are two readouts on the same underlying phenomenon: **transformers do not handle attention as a free resource. Every token you add competes with every other token.**

If you accept the Sourcegraph result that “the solution is smarter selection, not a bigger window” for code, you have already accepted the Straion thesis for rules. There is no consistent position in which structured retrieval is the right answer for finding the relevant payments package, but stuffing 200 conventions into AGENTS.md is the right answer for following them.

The frontier of reliable AI coding is not the next model release. It is **the engineering layer between the model and the codebase**. Code search. Structured indexes. Retrieval pipelines. Rule selection. Whatever sits between an LLM and a real engineering workload has to do the same job: filter aggressively, deliver only what the current task needs, get out of the way.

## What this means for engineering standards

Let’s make this concrete. You’re working on a Go microservice codebase. You have conventions for inter-service communication, error handling, observability, testing patterns, security, API design, database access, logging, and deployment. 150 rules total.

**The one million token approach** means you dump all 150 rules into the context alongside the codebase, the issue description, conversation history, tool schemas, and whatever else fits. The agent now has everything it could possibly need. It also has so much noise that your `serviceclient` convention on line 847 of the context is competing for attention with 999,000 other tokens.

Now overlay Sourcegraph’s data on that picture. The same agent, on the same codebase, will:

- thrash through redundant searches because it can’t tell which rules apply,
- ignore the rules in the middle of AGENTS.md because attention degrades by position,
- produce locally-correct code that violates standards because the rules competed for attention with everything else,
- leave context residue from rules it considered and discarded.

**Straion solves this with the opposite approach.** The agent is integrating with the payments service. With Straion, it receives **8 rules**: the `serviceclient` package requirement, error wrapping with `apperror`, OpenTelemetry tracing conventions, and retry policies. That’s it. Eight rules in a focused, structured format. The signal-to-noise ratio is orders of magnitude higher.

The research predicted which approach wins. Sourcegraph’s 1,281 runs confirmed it on the code side. The math doesn’t change for rules.

## Retrieval ≠ compliance

One argument I hear often: “But needle-in-a-haystack tests show near-perfect retrieval at one million tokens.” That’s true. Google’s tests show Gemini 1.5 Pro achieving 99.7% recall on retrieving a specific fact from one million tokens of context.

Retrieval and compliance are fundamentally different tasks. Finding a needle is a lookup. Can the model locate a specific piece of information? Following engineering standards is behavioral. Can the model consistently apply multiple rules while generating code, holding each rule in working attention alongside the actual coding task?

The [IFScale research](https://arxiv.org/abs/2507.11538) answers that question directly: compliance degrades with instruction density even when the model can clearly “see” the instructions. The rules are in the context, the model can retrieve them if asked, but it doesn’t consistently apply them while coding. That’s the gap we see in code generation day to day.

Sourcegraph’s “context overflow” mode is the same gap, observed from a different angle: the model *can* read all that retrieved code; it just can’t usefully attend to it while generating new code. Retrieval succeeds. Compliance fails.

## What we’re building at Straion

At Straion, our approach is to have a small, sharp context:

**Dynamically match** only the relevant rules to each specific task. The agent fixing a CSS layout gets frontend conventions. The agent patching a security vulnerability gets compliance policies. No overlap. No noise.

**Keep the agent’s context sharp and narrow.** Fewer rules, higher compliance. The research backed this up across every study we looked at in March. Sourcegraph’s CodeScaleBench has now backed it up across 1,281 production-scale agent runs in May.

**Sit alongside, not against, structural code retrieval.** Tools like Sourcegraph’s MCP find the right code. Straion makes sure the agent follows the right rules while writing it. Both are needed for production-grade AI coding, because both attack the same underlying constraint: the LLM has a fixed attention budget, and how you spend it determines whether the output is shippable or not.

The result: your engineering standards actually get followed. Not because the model has a bigger context window, but because every rule it receives is relevant to what it’s doing right now.

---

## Stay on Track. Start for free.

See how Straion keeps your AI coding agent aligned with your standards.   
Set up takes
less than 5 minutes.

[Get Started Free
→](https://straion.app/auth/signup) 

Works with Claude Code, GitHub Copilot & Cursor. No credit card required.

---

## The context window arms race misses the point

Bigger context windows are genuinely useful for many things. Long conversations, large file analysis, complex multi-step reasoning. **I’m not arguing against the progress.**

But for the specific problem of making AI coding agents follow your engineering standards, the solution was never “fit more rules into the window.” It was always “deliver the right rules at the right time.”

In March, the science said this. In May, the field data said the same. The frontier work in reliable AI coding, Sourcegraph’s CodeScaleBench, the Context Rot study, IFScale, Lost in the Middle, and our own work at Straion, is converging on a single principle: **attention dilutes with scale, compliance drops with instruction density, and performance degrades well before you hit the context limit.** More tokens won’t fix that. Better signal will.

**Stay on track.**

Lukas

---

**References:**

Hong, K., Troynikov, A., & Huber, J. (2025). *Context Rot: How Increasing Input Tokens Impacts LLM Performance.* Chroma Research. <https://research.trychroma.com/context-rot>

Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). *Lost in the Middle: How Language Models Use Long Contexts.* Transactions of the Association for Computational Linguistics. <https://arxiv.org/abs/2307.03172>

Jaroslawicz, D. et al. (2025). *How Many Instructions Can LLMs Follow at Once?* arXiv:2507.11538. <https://arxiv.org/abs/2507.11538>

Gloaguen, T., Mündler, N., Müller, M., Raychev, V., & Vechev, M. (2026). *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* arXiv:2602.11988. <https://arxiv.org/abs/2602.11988>

Jarmak, S. (2026). *Why coding agents fail in large codebases (and what to do about it).* Sourcegraph Blog, May 8, 2026. <https://sourcegraph.com/blog/why-coding-agents-fail-large-codebases>

Sourcegraph. (2026). *CodeScaleBench: Testing coding agents on large codebases and multi-repo software engineering tasks.* <https://sourcegraph.com/blog/codescalebench-testing-coding-agents-on-large-codebases-and-multi-repo-software-engineering-tasks>

---

![Lukas Holzer](https://straion.com/.netlify/images?url=_astro%2Flukas.DfqEGcEf.jpg&fm=jpg&w=500&h=500&dpl=6a85597a97a15700076a9c5e) 

Written by Lukas Holzer

[← Back to blog](../blog.md "Back to blog")
