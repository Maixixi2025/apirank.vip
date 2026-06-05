---
title: "Cheapest LLM API 2026: Real Pricing Comparison (GPT-4o, Claude, Gemini, DeepSeek, Doubao)"
description: "Side-by-side pricing comparison of 20+ LLM APIs in 2026. We normalize per-1M-token rates, cache pricing, and free tier to find the cheapest API for coding, writing, long-context, and China access."
slug: "cheapest-llm-api-pricing-2026"
provider: "cross-provider"
published: false
date: "2026-06-02"
type: "comparison"
---

# Cheapest LLM API 2026: Real Pricing Comparison

## Why Price Matters More Than Ever in 2026

In 2024 the LLM API market was simple: OpenAI, Anthropic, Google, and a long tail of open-source providers. By 2026 the table has exploded — over 20 production LLM APIs are commercially available, ranging from $0.02 per million input tokens (ByteDance Doubao) to $75 per million output tokens (Claude Opus 4.7). For a startup processing 500 million tokens per month, the difference between the cheapest and most expensive tier of capable models can be $50,000/month.

This article normalizes the per-million-token rates of every major LLM API we track, applies the standard 3:1 input-to-output ratio used in real workloads, and adds the hidden costs (cache pricing, rate limits, minimum commitments). The result is a single ranking you can use to pick the cheapest API for your specific use case.

All prices are current as of June 2026 and verified against each provider's official pricing page. USD-equivalent prices for Chinese providers are calculated at $1 = ¥7 (the APIKEY.FUN reference rate, which roughly matches the mid-2026 rate on major exchanges).

## Methodology: How We Compare Prices

We use three standardized metrics across all providers:

1. **Input price per 1M tokens** — the rate you pay for prompt tokens sent to the model
2. **Output price per 1M tokens** — the rate you pay for tokens the model generates
3. **Cache read price per 1M tokens** — the discounted rate for repeated prompt prefixes (Anthropic prompt caching, OpenAI automatic caching, DeepSeek cache)

For Chinese providers quoted in ¥, we convert at $1 = ¥7. For per-second GPU billing (Replicate), we use the published per-token equivalent for a 70B-class model. Free tier value is reported separately, not netted into the per-token price.

We exclude providers that have no published per-token pricing (e.g., closed enterprise contracts only) and providers that are no longer accepting new signups. As of June 2026, the comparison covers 20 active providers.

## The 2026 Cheapest LLM API Ranking (Per-1M-Token Rates)

The table below ranks the cheapest capable model on each provider, comparing the same workload (1M input + 333K output tokens = ~$100 spent at the median rate):

| Rank | Provider | Cheapest Capable Model | Input $/1M | Output $/1M | Cache Read $/1M | $100 ≈ Tokens |
|------|----------|------------------------|-----------|-------------|-----------------|---------------|
| 1 | ByteDance Doubao | Doubao Lite | $0.02 | $0.02 | N/A | 5,000M |
| 2 | Google AI | Gemini 2.0 Flash | $0.03 | $0.06 | $0.005 | 3,300M |
| 3 | Mistral AI | Mistral Small 3 | $0.20 | $0.60 | $0.02 | 500M |
| 4 | DeepSeek | DeepSeek V3 Chat | $0.14 | $0.28 | $0.014 | 714M |
| 5 | Cohere | Command R7B | $0.15 | $0.60 | N/A | 500M |
| 6 | OpenAI | GPT-4.1 nano | $0.10 | $0.40 | $0.03 | 833M |
| 7 | xAI Grok | Grok-3 mini | $0.30 | $0.50 | N/A | 333M |
| 8 | Together AI | Llama 3.3 70B | $0.88 | $0.88 | N/A | 170M |
| 9 | Zhipu AI | GLM-4-Flash | $0.71 | $0.71 | N/A | 211M |
| 10 | Anthropic | Claude 3.5 Haiku | $0.80 | $4.00 | $0.03 | 125M |
| 11 | Fireworks AI | Llama 3.1 8B | $0.20 | $0.20 | $0.02 | 500M |
| 12 | Anyscale | Llama 3.3 70B | $0.15 | $0.15 | N/A | 667M |
| 13 | Moonshot Kimi | moonshot-v1-8k | $2.86 | $2.86 | $0.57 | 35M |
| 14 | APIKEY.FUN | Claude Haiku 4.5 | $1.00 | $5.00 | $0.04 | 100M |
| 15 | Alibaba Bailian | Qwen-Turbo | $0.57 | $0.57 | N/A | 263M |
| 16 | Baidu Ernie | ERNIE-Speed | $1.71 | $1.71 | N/A | 88M |
| 17 | Tencent Hunyuan | hunyuan-Turbo | $0.86 | $3.43 | N/A | 116M |
| 18 | OpenRouter | (varies, +5.5% fee) | $0.05+ | $0.10+ | Varies | 2,000M+ |
| 19 | Stability AI | Stable LM 2 12B | $4.00 | $4.00 | N/A | 25M |
| 20 | Replicate | Llama 3 70B | $0.16/sec | $0.49/sec | N/A | ~140M |

*Token counts assume a 3:1 input:output ratio (1M input + 333K output). Cache pricing applies only when prompts are repeated.*

## Cheapest by Use Case

### Cheapest for Bulk Text Classification (100M+ tokens/day)

For high-volume classification, extraction, and embedding-style workloads where model intelligence is less important than throughput:

- **ByteDance Doubao Lite** at $0.02/1M input is the absolute cheapest production API. Quality is lower than frontier models but adequate for classification, simple extraction, and Chinese-language tasks.
- **Gemini 2.0 Flash** at $0.03/1M input is the best value for English workloads requiring higher quality. The 1M-token context window is a bonus for long-document processing.
- **GPT-4.1 nano** at $0.10/1M is the cheapest OpenAI model and the best pick if you need OpenAI's tool-calling, JSON mode, and reliability.

### Cheapest for Code Generation (Frontier Quality Required)

Code generation needs frontier reasoning — cheap models produce too many compile errors. The cheapest options that maintain GPT-4-class quality:

- **DeepSeek V3 Chat** at $0.14/1M input is the cheapest frontier-quality model in 2026. Performance on HumanEval, MBPP, and SWE-bench is within 5% of Claude Sonnet 4.5 and GPT-4.1 at one-tenth the price.
- **Mistral Small 3** at $0.20/1M is the cheapest European-hosted frontier-tier model. Strong on code, hosted in EU for GDPR compliance.
- **Qwen-Turbo via Alibaba Bailian** at $0.57/1M is the cheapest Chinese-hosted model with code-generation quality comparable to GPT-4o mini.

### Cheapest for Long Context (100K+ tokens)

Long-context workloads are dominated by input cost. The cheapest providers with 100K+ context windows:

- **Google Gemini 2.0 Flash** — 1M token context, $0.03/1M input. Best price-per-context-token ratio in 2026.
- **Moonshot Kimi** — 128K context, $2.86/1M input via the official API. Higher price but Kimi handles Chinese long-form better than any other model.
- **Anthropic Claude 3.5 Haiku** — 200K context, $0.80/1M input, with prompt caching at $0.03/1M for repeated prefixes.

### Cheapest with China-Direct Access (No VPN Required)

For users in mainland China, the cheapest options without a proxy:

- **ByteDance Doubao** — Chinese-native, no proxy needed. Absolute lowest price ($0.02/1M).
- **Zhipu AI GLM-4-Flash** — Chinese-native, $0.71/1M, 128K context, generous free tier.
- **Alibaba Bailian Qwen-Turbo** — Chinese-native, $0.57/1M, integrates with Alibaba Cloud.
- **APIKEY.FUN** — Multi-model aggregator with China-direct endpoints. ¥1 = $1 transparent pricing; access to Claude, GPT, Gemini, and DeepSeek without VPN.
- **FreeModel** — DeepSeek official partner, China-direct, free signup credits.

## Free Tier Comparison: Who Gives the Most Free Tokens

The 2026 free tier landscape is fragmented. Some providers give meaningful production-grade credits; others give token amounts that disappear in one afternoon:

| Provider | Free Tier | Real Value | Card Required? |
|----------|-----------|-----------|----------------|
| Google AI | Generous free tier, Gemini 2.0 Flash unlimited (rate-limited) | Best free tier overall | No |
| OpenAI | $5 credit (expires 3 months) | ~33M GPT-4.1 nano tokens | No |
| DeepSeek | $2 credit (one-time) | ~14M V3 Chat tokens | No |
| Cohere | 1,000 req/month on trial key | Limited by request count | No |
| Mistral | Rate-limited free tier | ~10M Small tokens | No |
| Grok | Free tier, rate-limited | ~5M Grok-3 mini tokens | No |
| xAI | Free credits via X account | Variable | No |
| Zhipu AI | GLM-3-Turbo free, GLM-4-Flash limited | Most generous CN free tier | No |
| Alibaba Bailian | Free Qwen-Turbo quota | Substantial for CN users | Yes (Alibaba) |
| Baidu Ernie | ERNIE-Lite free | Substantial for CN users | Yes (Baidu) |
| Stability AI | 25 credits (≈3 SD 3.5 images) | Token equivalent: small | No |
| Replicate | Free credits on signup | Small, varies | No |
| APIKEY.FUN | Signup bonus (¥10-50) | ~10-50M tokens via group pricing | No |
| FreeModel | Signup bonus (model-specific) | Competitive with APIKEY.FUN | No |

**Best free tier for production use:** Google AI's Gemini 2.0 Flash unlimited tier remains the gold standard. You can build a substantial side project on it before hitting rate limits.

**Best free tier for Chinese users:** Zhipu AI's GLM-3-Turbo (truly free, no quota) and Alibaba Bailian's Qwen-Turbo (free quota for Alibaba Cloud users).

**Best free tier for Claude and GPT access in China:** FreeModel and APIKEY.FUN both offer signup credits and direct access without VPN.

## The $100 Stress Test: What 100 Bucks Buys You

To translate the per-token prices into something tangible, here's what $100 gets you at each provider's cheapest capable model, assuming a 3:1 input:output mix:

- **$100 on Doubao Lite** = ~5 billion tokens (enough to summarize 50,000 books)
- **$100 on Gemini 2.0 Flash** = ~3.3 billion tokens
- **$100 on DeepSeek V3** = ~714 million tokens (frontier quality, plenty for most apps)
- **$100 on GPT-4.1 nano** = ~833 million tokens
- **$100 on Claude 3.5 Haiku** = ~125 million tokens
- **$100 on GPT-4o** (not nano) = ~50 million tokens
- **$100 on Claude Sonnet 4.5** = ~30 million tokens
- **$100 on Claude Opus 4.7** = ~7 million tokens

The cheapest tier gets you 100x more tokens than the most expensive tier for the same dollar.

## Speed Comparison: Throughput at the Cheapest Tier

Price is only half the story. For real-time applications (chatbots, code assistants, voice agents), tokens-per-second matters:

| Provider | Cheapest Model | Median Output Speed |
|----------|----------------|---------------------|
| Grok | Grok-3 mini | 280 tok/sec |
| Google AI | Gemini 2.0 Flash | 250 tok/sec |
| DeepSeek | DeepSeek V3 | 180 tok/sec |
| Fireworks AI | Llama 3.1 8B | 220 tok/sec |
| Mistral | Mistral Small 3 | 150 tok/sec |
| OpenAI | GPT-4.1 nano | 130 tok/sec |
| Together AI | Llama 3.3 70B | 120 tok/sec |
| APIKEY.FUN | (relays) | 100 tok/sec |
| Zhipu AI | GLM-4-Flash | 100 tok/sec |
| Alibaba Bailian | Qwen-Turbo | 90 tok/sec |

For latency-sensitive apps, **Grok-3 mini** and **Gemini 2.0 Flash** are the cheapest fast options.

## Code Examples: Calling the Cheapest APIs

### DeepSeek V3 (Python)

```python
import requests

response = requests.post(
    "https://api.deepseek.com/v1/chat/completions",
    headers={"Authorization": "Bearer YOUR_DEEPSEEK_API_KEY"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Explain quantum entanglement in 100 words"}],
        "max_tokens": 200,
    },
    timeout=30,
)
print(response.json()["choices"][0]["message"]["content"])
```

### Gemini 2.0 Flash (curl)

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=YOUR_GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "What is the speed of light?"}]}]
  }'
```

### Doubao Lite (OpenAI-compatible endpoint)

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DOUBAO_API_KEY",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

response = client.chat.completions.create(
    model="doubao-lite-32k",
    messages=[{"role": "user", "content": "Translate to French: Hello, world!"}],
    max_tokens=100,
)
print(response.choices[0].message.content)
```

## FAQ

**Q: What is the absolute cheapest LLM API in 2026?**
A: ByteDance Doubao Lite at $0.02 per million input tokens. Quality is lower than frontier models but adequate for classification, simple extraction, and Chinese-language tasks.

**Q: Is the cheapest API also the best API?**
A: No. The cheapest models (Doubao Lite, Gemini Flash) are optimized for cost, not reasoning. For tasks requiring deep reasoning (math, code, multi-step planning), frontier models like Claude Sonnet 4.5 or GPT-4.1 deliver better results at 10-50x the price but lower cost per correct answer.

**Q: Why is DeepSeek so cheap?**
A: DeepSeek runs on custom H800 clusters optimized for inference, and the company operates on a low-margin, high-volume strategy. They also use MoE architecture (V3 is 671B params but only 37B active per token), which dramatically reduces compute cost.

**Q: Can I use ByteDance Doubao from outside China?**
A: Yes — Volcano Engine (the ByteDance cloud platform) offers international access via ark.cn-beijing.volces.com or the global endpoint. Pricing is the same.

**Q: What's the cheapest API for Claude and GPT access?**
A: FreeModel (DeepSeek official partner) and APIKEY.FUN both offer Claude and GPT access at competitive prices, with China-direct endpoints that work without VPN.

**Q: How do cache prices affect total cost?**
A: Cache pricing matters most for workloads with repeated prompt prefixes. Customer service bots with a fixed system prompt, code assistants with a project context, and RAG pipelines with the same document prefix can save 80-90% on input cost by using Anthropic's prompt caching ($0.03/1M vs $0.80/1M) or DeepSeek's cache ($0.014/1M vs $0.14/1M).

**Q: Does the free tier include rate limits?**
A: Yes. Even Google's "unlimited" Gemini 2.0 Flash free tier has rate limits (15 RPM, 1500 RPD on the standard tier). Production workloads should plan for paid tier or hybrid setup.

**Q: Should I use a multi-model aggregator?**
A: Aggregators like OpenRouter, FreeModel, and APIKEY.FUN add a small markup (5.5% on OpenRouter, transparent pricing on the others) but let you switch between Claude, GPT, Gemini, and DeepSeek with one API key. This is the best setup for products that need to fall back to a different model during outages.

## Conclusion: How to Pick the Cheapest LLM API for You

The cheapest LLM API in 2026 depends on four factors: required quality, geography, use case, and volume.

**For US/EU startups processing under 100M tokens/month:** Start with Google AI's Gemini 2.0 Flash free tier, then graduate to paid as you scale. It's the best price-to-quality ratio for English workloads.

**For code-heavy applications:** Use DeepSeek V3 as the default. It's frontier-quality at one-tenth the price of Claude or GPT.

**For China-based teams:** Use ByteDance Doubao (cheapest, Chinese-native), Zhipu GLM-4-Flash (best Chinese-language quality at low price), or FreeModel / APIKEY.FUN (multi-model aggregator with China-direct access to Claude and GPT).

**For long-context workloads (100K+ tokens):** Use Gemini 2.0 Flash (1M context) or DeepSeek V3 (128K context, with aggressive cache pricing).

**For multi-model production systems:** Use an aggregator like OpenRouter, FreeModel, or APIKEY.FUN to swap models without changing integration code. The slight markup pays for itself in resilience.

The single most expensive mistake is using Claude Opus or GPT-4.1 for tasks that don't need it. A simple two-tier routing setup — cheap model for classification/extraction, frontier model for generation — typically cuts LLM cost by 70% with no measurable quality loss.
