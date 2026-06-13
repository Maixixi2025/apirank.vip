---
title: "Claude Fable 5 and Mythos 5: Anthropic 2026 Frontier"
description: "Anthropic Claude Fable 5 and Mythos 5: $10/$50 per MTok, 1M context, #1 Intelligence Index. Full review vs GPT-5.x and Gemini 3."
slug: "claude-fable-5-mythos-5-2026"
provider: "anthropic"
published: false
date: "2026-06-13"
type: "comparison"
---

# Claude Fable 5 and Mythos 5: Anthropic's 2026 Frontier Models — Full Review vs GPT-5.x and Gemini 3

**June 13, 2026 — Updated with US export control suspension**

> **TL;DR:** On June 9, 2026, Anthropic launched Claude Fable 5 ($10/M input, $50/M output) and Claude Mythos 5 (same model without safety classifiers). They lead the Artificial Analysis Intelligence Index at 64.9 — roughly 5 points ahead of GPT-5.5 — with 1M token context, 128K max output, and state-of-the-art coding performance. However, on June 12, the US government issued an export control directive suspending foreign national access to both models, creating the most significant geopolitical complication in the frontier AI API market to date.

## What's New: Fable 5 and Mythos 5

Claude Fable 5 and Mythos 5 represent Anthropic's most capable models to date — and at roughly half the price of their predecessor (Claude Mythos Preview). The pair is identical under the hood, with one key difference: Fable 5 includes additional safety classifiers for cyber, biological/chemical, and distillation risks, while Mythos 5 omits them for maximum unrestricted capability.

**Model IDs:**
- `claude-fable-5` — Full safety classifiers (recommended for most use cases)
- `claude-mythos-5` — No safety classifiers (for research and trust environments)

**Key Specs:**
- Context window: 1M tokens (matching GPT-5.x)
- Max output: 128K tokens
- Input modalities: Text + Image (vision)
- Adaptive thinking: Always on (no toggle for extended thinking)
- US-only inference available at 1.1x pricing

## Pricing: Half the Cost of Previous Gen

The headline number: Fable 5 costs exactly half of Claude Mythos Preview. At $10/M input and $50/M output, it establishes a new price-performance frontier for Anthropic's model line.

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Cache Read | Cache Write (1hr) |
|-------|----------------------|-----------------------|------------|-------------------|
| **Claude Fable 5** | **$10.00** | **$50.00** | $1.00 | $20.00 |
| Claude Mythos Preview | $20.00 | $100.00 | $2.00 | $40.00 |
| Claude Opus 4.8 | $5.00 | $25.00 | $0.50 | $10.00 |
| GPT-5.5 | $15.00 | $60.00 | $7.50 | — |

**Does not include fallback pricing:** When Fable 5 reroutes to Opus 4.8 (which happens during ~9% of HLE queries), fallback requests are not billed at Fable prices — they use the fallback model's pricing.

## Benchmark Performance: #1 Across the Board

Fable 5 claims the top spot on the Artificial Analysis Intelligence Index with a score of 64.9 — roughly 5 points ahead of GPT-5.5 (~59.9) and significantly above Gemini 3.1 Pro Preview.

| Benchmark | Fable 5 | GPT-5.5 | Gemini 3.1 PP | Opus 4.8 |
|-----------|---------|---------|---------------|----------|
| AA Intelligence Index | **64.9** | ~59.9 | ~57 | ~52 |
| Humanity's Last Exam | **53%** | ~45% | ~42% | ~40% |
| FrontierCode (Cognition) | **Highest** | #2 | #3 | #5 |
| AA-Omniscience | **40** | ~35 | 33 | ~28 |
| Hebbia Finance | **Highest** | — | — | — |
| Slay the Spire (Act 3 reach rate) | **3x Opus 4.8** | — | — | Baseline |
| CursorBench | **SOTA** | — | — | — |

**Key insight:** The gap is most pronounced on coding benchmarks. Cursor, Cognition, and Sourcegraph all report that Fable 5 outperforms GPT-5.x on real software engineering tasks. The FrontierCode benchmark — run by Cognition (the Devin team) — places Fable 5 at the top of frontier models at medium reasoning effort.

## The Export Control Twist (June 12, 2026)

On the evening of June 12, the US government issued an export control directive under the Covered Model framework, suspending all access to Claude Fable 5 and Mythos 5 for foreign nationals. Anthropic is actively disputing the basis, which stems from a narrow jailbreak technique that — according to Anthropic — produces results "widely available from other models (including OpenAI's GPT-5.5)."

**Current status as of June 13:**
- API access for US-based accounts: Active ✅
- API access for foreign nationals: Suspended ❌
- Access via AWS Bedrock / Vertex AI: US-only
- Data retention: 30-day required (Covered Model designation)
- Anthropic is working on a compliance solution for international customers

**What this means for developers:**
1. **US-based teams**: Continue normally, but consider fallback to Opus 4.8 for redundancy
2. **International teams**: Must use Opus 4.8, or explore alternatives like GPT-5.5 or Gemini 3 for now
3. **Multi-region deployments**: Add model routing that detects availability per region

## Claude Fable 5 vs GPT-5.5 vs Gemini 3: Use Case Comparison

| Use Case | Winner | Why |
|----------|--------|-----|
| Complex coding / agents | **Fable 5** | #1 on FrontierCode, CursorBench; GPT-5.5 close 2nd |
| Long-document analysis | **Tie** | Both support 1M context; Fable 5 slightly better at deep retrieval |
| Writing & content | **Fable 5** | Known verbosity is a feature for long-form; Gemini 3 more concise |
| Real-time chat / low latency | **Gemini 3** | Fable 5 outputs ~64 tok/s (rank #63/152); Gemini 3 is faster |
| Budget-sensitive | **Fable 5** | $10/$50 vs GPT-5.5's $15/$60 — 33% cheaper on input, 17% on output |
| Multi-modal analysis | **GPT-5.5** | Native image, audio, video support; Fable 5 is text+vision only |
| Enterprise compliance | **Opus 4.8** | No export control restrictions, proven deployment track record |
| China direct access | **Needs proxy** | None of the three are directly accessible from China |

## Code Example: Calling Claude Fable 5 via API

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

response = client.messages.create(
    model="claude-fable-5",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Write a Python function that implements a LRU cache with TTL support"}
    ]
)

print(response.content[0].text)
```

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-fable-5",
    "max_tokens": 4096,
    "messages": [{"role": "user", "content": "Write a Python LRU cache with TTL"}]
  }'
```

## Availability & Timelines

| Date | Milestone |
|------|-----------|
| June 9 | Launch on Claude API, AWS Bedrock, Vertex AI |
| June 9-22 | Free on Pro/Max/Team plans (consumes 2x Opus usage) |
| June 12 | US export control suspension (foreign nationals) |
| June 23 | Removed from subscription plans; requires usage credits |

## FAQ

**Q: What is the difference between Fable 5 and Mythos 5?**
A: They are the same underlying model. Fable 5 includes additional safety classifiers for cyber, bio/chem, and distillation risks. Mythos 5 has these classifiers removed for maximum capability in trusted environments.

**Q: Can I access Fable 5 from China?**
A: No. Anthropic requires US-based accounts and currently has an export control suspension for foreign nationals. Like all Anthropic models, direct access from China requires a proxy. For China-direct alternatives, consider an aggregator like FreeModel that bundles multiple providers with OpenAI-compatible routing.

**Q: Is Fable 5 cheaper than GPT-5.5?**
A: Yes. Fable 5 costs $10/$50 per MTok (input/output) vs GPT-5.5's $15/$60 — a 33% savings on input and 17% on output tokens.

**Q: How does Fable 5 compare for coding?**
A: Based on Cursor, Cognition, and Sourcegraph feedback, Fable 5 outperforms GPT-5.x on real software engineering tasks. It scores highest on FrontierCode and CursorBench.

**Q: What happens when Fable 5 falls back to Opus 4.8?**
A: For ~9% of complex queries (particularly on HLE), the model autonomously routes to Opus 4.8. These are billed at Opus 4.8 prices, not Fable 5 prices.

## Verdict

Claude Fable 5 and Mythos 5 are currently the most capable publicly available AI models — leading every major benchmark from the Intelligence Index to FrontierCode to CursorBench. The pricing at $10/$50 per MTok is aggressive for Anthropic's frontier tier, undercutting GPT-5.5 on both input and output costs.

**The export control suspension is the wildcard.** For US-based teams, Fable 5 is the clear recommendation for any non-realtime, quality-sensitive workload. For international teams, the path forward depends on how quickly Anthropic resolves the compliance issue.

**Who should use Fable 5:**
- Coding: Yes, especially for complex agentic tasks
- Writing: Best-in-class for long-form and structured content
- Research: The strongest model for deep analysis
- Enterprises: Consult legal team about export compliance

**Who should wait:**
- International teams without US entity presence
- Real-time applications (Gemini 3 is faster)
- Multi-modal applications needing audio/video (GPT-5.5 has broader modality support)

For teams that need multi-provider flexibility (especially China-direct access), an aggregator like FreeModel provides OpenAI-compatible routing across multiple providers, including models that remain directly accessible from China.
