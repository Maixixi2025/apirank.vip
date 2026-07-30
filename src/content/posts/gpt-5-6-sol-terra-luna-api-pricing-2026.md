---
title: "GPT-5.6 API Pricing 2026: Sol, Terra & Luna Tiers"
description: "GPT-5.6 Sol ($5/$30), Terra ($2.50/$15), Luna ($1/$6) per 1M tokens. Tier comparison, Terminal-Bench benchmarks, max/ultra modes, and caching costs."
pubDate: "2026-07-11"
provider: openai
category: pricing-guide
featured: true
---

# GPT-5.6 API Pricing 2026: Sol, Terra & Luna — Complete Tier Selection Guide

On **June 26, 2026**, OpenAI launched the **GPT-5.6 family** — three capability tiers named **Sol**, **Terra**, and **Luna** — in a limited, government-coordinated preview. This is OpenAI's most significant model release since GPT-5.5, and it introduces a new naming philosophy: the number (5.6) identifies the generation, while Sol/Terra/Luna are **durable capability tiers** that can each improve independently over time.

If you're building on OpenAI's API today, the GPT-5.6 family changes your cost math, your routing logic, and your capability ceiling. This guide breaks down everything you need to know to choose the right tier.

## GPT-5.6 Pricing Overview

OpenAI priced the three GPT-5.6 tiers to map onto the existing GPT-5.x lineup without disrupting existing budgets:

| Tier | Input ($/1M tokens) | Output ($/1M tokens) | Cached Input ($/1M tokens) | Cache Write ($/1M tokens) |
|------|--------------------|---------------------|--------------------------|--------------------------|
| **Sol** | $5.00 | $30.00 | $0.50 | $6.25 |
| **Terra** | $2.50 | $15.00 | $0.25 | $3.13 |
| **Luna** | $1.00 | $6.00 | $0.10 | $1.25 |

**Key pricing observations:**

- **Sol** matches GPT-5.5's price exactly ($5/$30). You get a capability upgrade at zero cost increase — the best kind of upgrade.
- **Terra** lands at the old GPT-5.4 price ($2.50/$15). OpenAI claims it matches GPT-5.5's capability at half the cost — the biggest value story of this launch.
- **Luna** creates a new budget tier at $1/$6, cheaper than GPT-5.4 mini ($0.75/$4.50 on output) but carrying GPT-5.6 generation technology.

**Prompt caching** delivers a 90% discount on cached input reads across all three tiers. For agentic workflows with long, repeated system prompts, this is a critical cost lever. Cache writes are billed at 1.25× the uncached input rate — caching helps most when system prompts change infrequently.

## What Each Tier Is Best For

### Sol: The Frontier Flagship ($5/$30)

Sol is OpenAI's strongest model to date. It sets new state-of-the-art results on **Terminal-Bench 2.1**, OpenAI's agentic command-line coding benchmark, and introduces two new reasoning controls not available on any previous model.

**Best workloads for Sol:**
- Hard reasoning and multi-step agentic tasks
- Complex code generation requiring planning and iteration
- Cybersecurity analysis and threat detection
- Advanced biology and genomics research (Sol beats GPT-5.5 on GeneBench v1)
- Any task where output quality is the priority and cost is secondary

**New features exclusive to Sol:**
- **Max reasoning effort** — a new top rung above previous reasoning-effort levels, giving Sol more time to reason deeply on a single problem
- **Ultra subagent mode** — spawns parallel sub-agents to accelerate complex multi-step work. This is where Sol's headline ~91.9% Terminal-Bench score comes from

### Terra: The Balanced Default ($2.50/$15)

Terra is the sweet spot of the GPT-5.6 family. At half the flagship price, OpenAI reports it matches GPT-5.5's capability on most production workloads.

**Best workloads for Terra:**
- Premium production workloads where Sol would be overkill
- Long-context agents with substantial repeated system prompts (where caching compounds the savings)
- Tasks that currently use GPT-5.5 and don't need absolute peak reasoning
- High-volume coding assistance

### Luna: The Cost-Efficient Workhorse ($1/$6)

Luna brings GPT-5.6 generation capability to the budget tier. At $1 input / $6 output per million tokens, it competes directly with GPT-5.4 mini ($0.75/$4.50) while delivering a more recent generation of model.

**Best workloads for Luna:**
- High-throughput content generation
- Classification, routing, and extraction pipelines
- Everyday chat and summarization
- Multi-turn conversations where cost accumulates quickly
- API cost-sensitive applications

## Benchmarks: Sol vs the Competition

All benchmark figures here are **OpenAI-reported** from the limited preview. They represent a vendor ceiling pending independent testing at general availability.

### Terminal-Bench 2.1 (Agentic Coding)

Terminal-Bench 2.1 tests command-line workflows requiring planning, iteration, and tool coordination. On OpenAI's own Codex CLI harness:

| Model | Score |
|-------|-------|
| **GPT-5.6 Sol (ultra mode)** | **~91.9%** |
| **GPT-5.6 Sol (max effort)** | **~88.8%** |
| Claude Mythos 5 | 88.0% |
| GPT-5.5 | 83.4% |
| GPT-5.6 Terra | Data TBD |

Sol at max effort (~88.8%) edges Claude Mythos 5 (88.0%) and beats GPT-5.5 (83.4%) by about 5 points. Sol in ultra mode (~91.9%) widens the gap further — but ultra mode is a multi-agent result and may consume significantly more tokens per task.

**Important caveat:** OpenAI used its own Codex CLI harness. This is generally considered easier than SWE-bench Verified, where GPT-5.5 scores ~74.6%. Expect lower public-harness scores once independent evaluations appear.

### Biology (GeneBench v1)

On GeneBench v1, which evaluates long-horizon genomics and quantitative-biology analyses, OpenAI reports Sol achieving stronger results than GPT-5.5.

### Cybersecurity

OpenAI says GPT-5.6 Sol is competitive with the restricted o-series models on cybersecurity benchmarks — though Sol does not cross the "Cyber Critical" threshold that would trigger additional safety restrictions.

### How It Stacks Up to the Competition

| Competitor | Comparison |
|------------|-----------|
| **Claude Opus 4.8** (Anthropic) | Opus 4.8 at $5/$25 is OpenAI's closest competitor at the flagship tier. Sol edges Claude Mythos 5 (88.0%) on Terminal-Bench. No independent shared benchmark yet — verdict pending GA. |
| **Claude Sonnet 5** ($2/$10 intro until Aug 31) | Sol costs more ($5/$30) but delivers higher benchmark scores. Terra ($2.50/$15) is closer to Sonnet 5 territory. |
| **DeepSeek V3/R1** (¥0.14/¥0.28 per M) | DeepSeek still undercuts everyone on raw token price but offers a smaller set of reasoning capabilities. |
| **Google Gemini 2.5 Pro** ($1.25/$5) | Gemini 2.5 Pro's 1M+ context window and $1.25/$5 pricing make it a strong value play, but GPT-5.6 Sol leads on agentic coding benchmarks. |

## Caching: The Hidden Cost Lever

Prompt caching works on all three GPT-5.6 tiers and can dramatically reduce effective costs for production workloads:

```python
# Before caching: a 50K-token system prompt with 10 user turns
# Sol at $5/M input = $0.25 per turn × 10 = $2.50

# After caching (90% discount on cached reads):
# First turn: $0.25 (full uncached)
# Turns 2-10: 50K × 90% × $0.50/M cached + 50K × 10% × $5/M uncached
# = $0.0225 + $0.0025 = $0.025 per cached turn
# 10 turns total: $0.25 + 9 × $0.025 = $0.48
# Savings: ~81%
```

For agent loops and long-running conversations, caching is not optional — it's the difference between viable and uneconomical.

## Code Examples: Calling Each Tier

### curl — Testing All Three Tiers

```bash
# GPT-5.6 Sol
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.6-sol",
    "max_tokens": 1024,
    "reasoning_effort": "max",
    "messages": [{"role": "user", "content": "Design a distributed task queue system with fault tolerance"}]
  }'

# GPT-5.6 Terra
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.6-terra",
    "max_tokens": 2048,
    "messages": [{"role": "user", "content": "Write a Python function that merges overlapping intervals"}]
  }'

# GPT-5.6 Luna
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.6-luna",
    "max_tokens": 4096,
    "messages": [{"role": "user", "content": "Summarize this research paper in 3 paragraphs"}]
  }'
```

### Python — Tier Routing with Cost Awareness

```python
import openai

client = openai.OpenAI(api_key="sk-...")

def route_to_tier(prompt: str, complexity: int):
    """
    Complexity 1-3: Luna
    Complexity 4-6: Terra  
    Complexity 7-10: Sol
    """
    if complexity <= 3:
        model = "gpt-5.6-luna"
    elif complexity <= 6:
        model = "gpt-5.6-terra"
    else:
        model = "gpt-5.6-sol"
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096
    )
    
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    
    # Cost estimate (per 1M tokens)
    costs = {
        "gpt-5.6-sol": (5.00, 30.00),
        "gpt-5.6-terra": (2.50, 15.00),
        "gpt-5.6-luna": (1.00, 6.00)
    }
    in_rate, out_rate = costs[model]
    cost = (input_tokens / 1_000_000 * in_rate) + (output_tokens / 1_000_000 * out_rate)
    
    return response.choices[0].message.content, cost
```

## Ultra Mode: The Multi-Agent Differentiator

Sol's **ultra subagent mode** is arguably the most interesting new capability. It spawns parallel sub-agents that work on different parts of a complex problem simultaneously, then synthesizes the results.

```bash
# Sol with ultra mode enabled
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.6-sol",
    "reasoning_effort": "ultra",
    "max_tokens": 8192,
    "messages": [
      {"role": "user", "content": "Analyze this codebase architecture, identify bottlenecks, and propose a refactoring plan with benchmarks"}
    ]
  }'
```

**Important limitation:** Ultra mode consumes more tokens per task (each sub-agent's reasoning is billed). The headline ~91.9% Terminal-Bench score is an ultra-mode result. For single-model reasoning, max effort (~88.8%) is the like-for-like comparison.

## Access: Limited Preview with Government Coordination

GPT-5.6 is not a general release. Key access facts:

- **Limited preview** for select partners and organizations via OpenAI's trust-and-safety framework
- **Government coordination**: The US Commerce Department approved large-scale deployment under the new AI export framework
- **M365 Copilot**: Microsoft has selected GPT-5.6 as the preferred model for Microsoft 365 Copilot
- **Cerebras acceleration**: Sol will be available on Cerebras at up to 750 tokens/second in July 2026 for select customers
- **GA timeline**: OpenAI says general availability across ChatGPT, Codex, and the API is planned "in the coming weeks"

**Safeguards built into the preview:**
- Safety-trained model weights
- Real-time cyber and biology misuse classifiers that can pause generation for a larger reasoning model to review
- Account-level review across conversations
- Differentiated access, monitoring, and enforcement

## Which Tier Should You Start With?

### Use GPT-5.6 Sol if:
- Your current workflow uses GPT-5.5 and you want a free capability upgrade at the same price
- You're building complex agent systems where ultra mode's multi-agent parallelism could accelerate development
- You need the absolute highest ceiling in coding, biology, or cybersecurity analysis

### Use GPT-5.6 Terra if:
- Your current workflow uses GPT-5.4 and you want a big capability gain at the same price
- You're happy with GPT-5.5's quality but want to cut costs in half
- You need a balanced model for production where price and quality both matter

### Use GPT-5.6 Luna if:
- You're running high-volume classification, extraction, or generation pipelines
- Your quality needs are met by GPT-5.4 mini or GPT-4.1 mini today
- You want GPT-5.6 generation technology at the lowest possible price point

## Frequently Asked Questions

### What is the context window for GPT-5.6?

OpenAI has not published the context window for the preview. Secondary coverage reports approximately **1.5 million tokens for Sol** — unconfirmed. Terra and Luna likely have smaller context windows, though exact specifications are data not available. We will update this page when OpenAI publishes the full specs at GA.

### Does GPT-5.6 Sol beat GPT-5.5?

On OpenAI's own Terminal-Bench 2.1, yes: Sol at max effort scores ~88.8% versus GPT-5.5's 83.4%. Sol at ultra mode reaches ~91.9%. Sol costs the same as GPT-5.5 ($5/$30), so it's a strict upgrade on capability. The value winner, however, may be **Terra**: OpenAI says it matches GPT-5.5's capability at half the cost.

### How does GPT-5.6 compare to Claude Mythos 5?

On Terminal-Bench 2.1, Sol at max effort (~88.8%) edges Claude Mythos 5 (88.0%). No independent shared-harness benchmarks exist yet. A complete comparison requires GA with independent evaluation.

### When will GPT-5.6 be available on the API generally?

OpenAI says general availability across ChatGPT, Codex, and the API is planned "in the coming weeks" from the June 26, 2026 launch date. No firm GA date has been given. The Cerebras launch for Sol (up to 750 tokens/second) is scheduled for July for select customers.

### Does GPT-5.6 support structured outputs and function calling?

GPT-5.6 inherits OpenAI's Structured Outputs infrastructure from GPT-5.5 and earlier models. All three tiers support function calling, response_format parameters, and the full OpenAI API surface. Ultra mode's interaction with structured outputs is not yet fully documented.

### Can I use GPT-5.6 from China?

OpenAI API remains subject to US export controls. As with GPT-5.5 and earlier flagship models, access from China requires a proxy or VPN. The government-coordinated preview adds an additional layer of access restrictions for the Sol tier specifically.

### Does GPT-5.6 work as a drop-in replacement for GPT-5.5?

Most likely yes for Terra at the same API format, though exact model strings were not published in the preview. Sol includes new parameters (reasoning_effort: "max" or "ultra") that GPT-5.5 does not support — these are additive, not breaking changes. Test your specific workflow before production switchover.

---

*Pricing and benchmarks in this article are based on OpenAI's limited preview as of July 11, 2026. All benchmark figures are OpenAI-reported using their own Codex CLI harness. When GPT-5.6 reaches general availability, we will update with independent benchmarks and confirmed context window specifications.*
