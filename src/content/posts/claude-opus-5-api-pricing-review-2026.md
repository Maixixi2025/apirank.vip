---
title: "Claude Opus 5 API: Pricing, Benchmarks & Migration Guide"
description: "Claude Opus 5 ($5/$25 per 1M tokens) matches Opus 4.8 pricing with near-Fable 5 performance. 1M context window, Fast mode 2.5x, Frontier-Bench SOTA. Full review."
pubDate: "2026-07-30"
provider: anthropic
category: news-analysis
featured: true
---

# Claude Opus 5 API: Pricing, Benchmarks & Migration Guide

On **July 24, 2026**, Anthropic released **Claude Opus 5** — a thoughtful, proactive model that comes close to the frontier intelligence of Claude Fable 5 at **half the price**. If you're building on the Anthropic API today, this changes the calculus: you get near-flagship capability at the same cost as Opus 4.8, with a larger context window, higher speed via Fast mode, and significantly better agentic coding performance.

This is a complete guide to the Claude Opus 5 API — pricing, rate limits, context window, benchmarks, code examples, and whether you should migrate from Opus 4.8 or skip straight to Fable 5.

## Claude Opus 5 Pricing

Anthropic priced Opus 5 identically to Opus 4.8 — no price increase for a meaningful capability upgrade:

| Input ($/1M tokens) | Output ($/1M tokens) |
|--------------------|---------------------|
| **$5.00** | **$25.00** |

### Fast Mode Pricing

Opus 5 supports **Fast mode**, running about **2.5× the default speed** at **2× the base price**:

| Mode | Input ($/1M tokens) | Output ($/1M tokens) | Speed |
|------|--------------------|---------------------|-------|
| Standard | $5.00 | $25.00 | 1× baseline |
| Fast | $10.00 | $50.00 | ~2.5× faster |

Fast mode is available through the Claude Platform and via usage credits in Claude Code. Use it when latency is critical — interactive coding, real-time agent loops, or customer-facing chat where every millisecond counts. Standard mode is more than adequate for batch processing, background agents, and scheduled tasks.

### Prompt Caching

Like all recent Claude models, Opus 5 supports prompt caching:

| Cache Write ($/1M tokens) | Cache Read ($/1M tokens) |
|--------------------------|-------------------------|
| $6.25 | $0.50 (90% discount) |

For agentic workflows with long, repeated system prompts (think 10K–50K tokens of instructions shared across turns), caching makes Opus 5 cheaper than Opus 4.8 in practice. The 90% read discount means a 40K-token system prompt repeated across 20 turns costs approximately $0.01 per turn instead of $0.10.

### Batch API Pricing

Anthropic's Message Batches API offers a **50% discount** on Opus 5 for non-urgent workloads:

| Batch Input ($/1M tokens) | Batch Output ($/1M tokens) |
|--------------------------|---------------------------|
| $2.50 | $12.50 |

Batch API supports up to **300K output tokens per request** — useful for long-form content generation or bulk data extraction. Results are typically available within 1–24 hours.

## Context Window & Output Limits

| Feature | Opus 5 | Opus 4.8 |
|---------|--------|----------|
| **Context window** | 1,000,000 tokens (1M) | 200,000 tokens |
| **Max output** | 128,000 tokens | 8,192 tokens |
| **Knowledge cutoff** | May 2026 | Jan 2026 |
| **Training data cutoff** | May 2026 | Jan 2026 |

The **1M token context window** is a 5× increase over Opus 4.8's 200K. This is the game-changer for long-running agents, codebase-wide refactoring, and processing entire documents in a single pass.

The **128K max output** (vs. Opus 4.8's 8K) enables generation of entire codebases, long-form reports, and complete technical documentation without chunking. On the Batch API, output can go up to 300K tokens.

## Model IDs & Effort Levels

Opus 5 supports **four effort levels** that let you trade capability for speed and cost:

| Effort Level | Use Case |
|-------------|----------|
| **low** | Simple tasks, quick lookups, routine classification |
| **medium** (default) | General-purpose balanced workload |
| **high** | Complex reasoning, multi-step coding |
| **xhigh** | Deep reasoning on hard problems |
| **max** | Maximum capability for the hardest tasks |

The model ID for API access is **`claude-opus-5-20260724`** (or simply `claude-opus-5` for the latest pinned snapshot).

```python
import anthropic

client = anthropic.Client(api_key="your-api-key")

response = client.messages.create(
    model="claude-opus-5-20260724",
    max_tokens=4096,
    thinking={"type": "enabled", "budget_tokens": 2048},
    messages=[{"role": "user", "content": "Write a complete Python FastAPI app that implements a vector search endpoint using cosine similarity."}]
)
print(response.content[0].text)
```

## Benchmarks: Opus 5 vs the Field

Anthropic's internal evaluations position Opus 5 as the best cost-adjusted performer across nearly every category.

### Frontier-Bench v0.1 (Coding & Knowledge Work)

| Metric | Opus 5 | Opus 4.8 | Fable 5 |
|--------|--------|----------|---------|
| **Score** | SOTA | — | — |
| **Cost efficiency** | **2× improvement** over Opus 4.8 | Baseline | Reference |
| **Vs Fable 5** | Within 0.5% on CursorBench 3.2 (max effort) | — | Peak |

On **Frontier-Bench v0.1**, Opus 5 surpasses all other models and more than doubles Opus 4.8's performance at a lower cost per task. On **CursorBench 3.2** at max effort, it performs within 0.5% of Fable 5's peak score but at **half the cost per task**.

### Agentic Benchmarks

| Benchmark | Opus 5 Result | Improvement |
|-----------|--------------|-------------|
| **OSWorld 2.0** (Computer Use) | Best cost-adjusted result | Surpasses Fable 5 at ⅓ the cost |
| **ARC-AGI 3** (Novel Problem Solving) | 3× the next-best model | Massive leap in abstract reasoning |
| **Zapier AutomationBench** | ~1.5× pass rate vs next-best | Top of leaderboard |
| **GDPval-AA v2** | SOTA | — |
| **HLE** | SOTA | — |
| **DeepSearchQA** | SOTA | — |
| **AA Coding Agent Index** | Up 22% over Opus 4.7 | Steadier, less variance |

On **OSWorld 2.0** — the computer-use benchmark that tests whether a model can navigate GUIs and complete multi-step tasks — Opus 5 outperforms every other model at any given cost, surpassing Fable 5's best result at just over a third of the cost.

On **ARC-AGI 3**, the evaluation for solving novel abstract problems, Opus 5's score is **three times as high as the next-best model**. This signals genuine capability improvements in reasoning, not just benchmark overfitting.

### Scientific Research

| Domain | Opus 5 vs Opus 4.8 |
|--------|-------------------|
| Organic chemistry (spectroscopy inference) | +10.2 percentage points |
| Protein sequence variant prediction | +7.7 percentage points |
| All life sciences evaluations | Superior across the board |

Opus 5 is Anthropic's strongest model yet for scientific research, covering structural biology, organic chemistry, and bioinformatics.

### Safety & Alignment

Anthropic's automated behavioral audit found Opus 5 to be its **most aligned model** to date:

- **Overall misaligned behavior score**: 2.3 — lowest of any recent Claude model
- **Constitution adherence**: Better than Opus 4.8, Sonnet 5, or Fable 5
- **Deceptive behavior**: Lowest rates of any model
- **Misuse susceptibility**: Least susceptible to being tricked
- **Dual-use risk**: Does not advance the frontier in risky capabilities

On safety, Anthropic reports that rigorous evaluations conducted alongside private-sector and government partners found Opus 5 remains behind Mythos 5 in dual-use capability benchmarks but does not represent a new risk frontier.

## Code Examples

### Curl: Standard Chat Completion

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-5-20260724",
    "max_tokens": 2048,
    "messages": [
      {"role": "user", "content": "Explain the tradeoffs between edge computing and cloud inference for a real-time object detection pipeline deployed across 50 IoT cameras."}
    ]
  }'
```

### Curl: Fast Mode with Extended Thinking

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-5-20260724",
    "max_tokens": 8192,
    "thinking": {"type": "enabled", "budget_tokens": 4096},
    "metadata": {"user_id": "dev-abc123"},
    "messages": [
      {"role": "user", "content": "Design a distributed rate limiter using Redis and gRPC interceptors. Include the architecture diagram in ASCII and full Go implementation."}
    ]
  }'
```

### Python: Streaming with Effort Levels

```python
import anthropic

client = anthropic.Client(api_key="your-api-key")

# Using xhigh effort for a complex code generation task
with client.messages.stream(
    model="claude-opus-5-20260724",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 8000},
    messages=[
        {"role": "user", "content": "Write a Python function that takes a directory path, recursively finds all Python files, extracts their function signatures with type annotations, and generates an OpenAPI-compatible spec from FastAPI route handlers."}
    ]
) as stream:
    for chunk in stream:
        if chunk.type == "content_block_delta":
            print(chunk.delta.text, end="", flush=True)
```

### Python: Prompt Caching for Agentic Workflows

```python
import anthropic

client = anthropic.Client(api_key="your-api-key")

system_prompt = """
You are a senior DevOps engineer with expertise in Kubernetes, Terraform, and CI/CD pipelines.
Analyze the user's infrastructure questions and provide production-ready solutions.

**Context rules:**
- Always include specific CLI commands, YAML configs, and Terraform HCL
- Prefer native Kubernetes resources over Helm charts unless Helm is explicitly requested
- Include resource limits, probes, and security contexts in all Pod specs
- Mention cost implications of your recommendations
"""  # ~500 tokens, will be cached

user_question = "Design a zero-downtime deployment strategy for a microservices application running on EKS with 15 services and an API gateway."

response = client.messages.create(
    model="claude-opus-5-20260724",
    max_tokens=4096,
    system=system_prompt,
    messages=[{"role": "user", "content": user_question}]
)
print(response.content[0].text)
# Second call with same system prompt → cache read (90% off)
```

## Key Improvements Over Opus 4.8

| Capability | Opus 5 | Opus 4.8 | Impact |
|-----------|--------|----------|--------|
| Context window | 1M tokens | 200K tokens | 5× larger — entire codebases fit |
| Max output | 128K tokens | 8,192 tokens | 16× longer generations |
| Frontier-Bench | 2× Opus 4.8 performance | Baseline | Massive coding improvement |
| CursorBench | Within 0.5% of Fable 5 | — | Near-flagship in IDE |
| Agentic coding | +22% over Opus 4.7 | Baseline | Steadier, more reliable |
| Scientific research | +10.2pp on spectroscopy | Baseline | Real domain depth |
| Speed | ~2.5× via Fast mode | Fast mode also available | Same Fast mode benefit |
| Misaligned behavior | 2.3 (lowest ever) | Higher | More trustworthy |

## Migration Guide: Opus 4.8 → Opus 5

### If you're using Opus 4.8 today:

**Step 1 — Test in staging.** Change your model ID from `claude-opus-4-8-20260514` to `claude-opus-5-20260724` in a non-production environment. The Messages API is backward-compatible — all existing parameters (`max_tokens`, `system`, `thinking`, `tools`, `metadata`) work identically.

**Step 2 — Adjust max_tokens.** Opus 5 supports up to 128K output tokens vs. Opus 4.8's 8K. If your application previously chunked outputs, you can simplify by requesting the full output in a single call. Set `max_tokens` to the actual amount of text you need.

**Step 3 — Leverage the larger context window.** If your agent maintains a rolling conversation history, consider keeping more turns in context instead of aggressively summarizing. The 1M window makes it practical to include entire codebase content or meeting transcripts without truncation.

**Step 4 — Evaluate effort levels.** Opus 4.8 has a fixed effort profile. Opus 5 lets you dial between `low` and `max`. Start with `medium` (the default), then adjust based on your latency-vs-quality requirements:

- **Simple classification / routing → low** (fastest, cheapest)
- **Content generation / summarization → medium** (balanced)
- **Complex coding / analysis → high or xhigh**
- **Research-grade reasoning → max**

### If you're on Sonnet 5:

Sonnet 5's limited-time pricing ($2/$10 per 1M tokens, expiring August 31, 2026) still makes it the better choice for high-volume production workloads where cost-per-token dominates. Migrate to Opus 5 when:
- Output quality matters more than cost
- You need the 1M context window
- Your agent requires extended reasoning (xhigh/max effort)
- Latency is acceptable at Opus 5's speed profile

### If you're considering Fable 5:

Fable 5 remains Anthropic's frontier model at **$15/$75 per 1M tokens** — 3× the price of Opus 5. Reserve it for the hardest 5% of tasks where Opus 5 at max effort is still insufficient. For 95% of workloads, Opus 5 at xhigh or max effort will match or come close to Fable 5 at half the cost.

## When to Use Opus 5 vs Alternatives

### Best workloads for Claude Opus 5:

- **Complex agentic coding** — multi-step refactoring, codebase-wide changes, test generation
- **Computer use automation** — GUI automation, browser agents, OSWorld-type tasks
- **Long-running agents** — the 1M context window lets agents maintain coherent state across hours of interaction
- **Scientific research** — spectroscopy, protein analysis, organic chemistry
- **Automation workflows** — Zapier-style business process automation (leaderboard-topping)
- **Reasoning-heavy analysis** — financial modeling, legal document review, audit workflows

### When to use other models instead:

| Scenario | Recommended Model | Why |
|----------|------------------|-----|
| High-volume customer chat | Sonnet 5 (limited-time $2/$10) | 5× cheaper than Opus 5 |
| Fast, simple tasks | Haiku 4.5 ($0.80/$4) | 6× cheaper, 200K context |
| Frontier research | Fable 5 ($15/$75) | Max capability when needed |
| Offensive cybersecurity | Mythos 5 | Invitation-only, specialized |
| Batch processing | Opus 5 via Batch API ($2.50/$12.50) | 50% discount for async work |

## Rate Limits

Anthropic applies rate limits at the API key and organization level. While specific per-model limits depend on your usage tier, Opus 5 generally offers:

- **Free tier**: Limited access (Opus models require Tier 2+)
- **Tier 2+ (API)** : Typically thousands of requests per minute for standard usage
- **Fast mode**: Shares the same rate limit pool but uses 2× the token allocation per request
- **Batch API**: Much higher throughput limits, results within 1–24 hours

To check your specific rate limits, use the `/v1/models` endpoint or check the Anthropic Console.

**Need to optimize API costs across multiple providers?** Use a gateway like [Portkey](https://portkey.ai) or \_Cloudflare AI Gateway to route requests between Opus 5, Sonnet 5, and Haiku 4.5 based on latency and cost requirements.

## Verdict

Claude Opus 5 upgrades the "workhorse" tier without raising the price tag. At **$5/$25 per 1M tokens** — identical to Opus 4.8 — you get:

- **1M token context** (5× Opus 4.8) for whole-codebase reasoning
- **128K max output** (16× Opus 4.8) for full-generation tasks
- **Frontier-Bench SOTA** with 2× the cost-adjusted performance of Opus 4.8
- **Near-Fable-5** capability on CursorBench at half the inference cost
- **For agentic and scientific workloads**, it's the best per-dollar model on the market

The only question is whether you need Fable 5's razor-edge capability for a subset of your hardest tasks. For everything else, Opus 5 is the new default.

## FAQ

### Is Claude Opus 5 available through API?

Yes. The model ID is `claude-opus-5-20260724` (or `claude-opus-5` for the pinned snapshot). Available on the Messages API, Batch API, and through Anthropic's client SDKs.

### What is the context window of Claude Opus 5?

1,000,000 tokens (1M) — 5× the 200K context of Opus 4.8 and matching the 1M window of Sonnet 5 and Fable 5.

### Does Claude Opus 5 support extended thinking?

Yes. Extended thinking is available through the `thinking` parameter with a `budget_tokens` field. It works at all effort levels from low to max.

### How does Claude Opus 5 compare to GPT-5.6 Sol?

Opus 5 ($5/$25) vs GPT-5.6 Sol ($5/$30) are similarly priced on input, but Opus 5 is 16% cheaper on output. Opus 5 excels on agentic benchmarks (OSWorld, AutomationBench) and has a 1M context window vs Sol's (approximately) 200K. Sol leads on raw math reasoning and its Terminal-Bench agentic coding score. The choice depends on whether your workload favors Anthropic's agentic strengths or OpenAI's reasoning depth.

### Can I use Fast mode on the API?

Fast mode is available through the Claude Platform (Web/App) and via usage credits in Claude Code. Standard API calls use the default speed. Batch API operates at standard speed with a 50% discount.
