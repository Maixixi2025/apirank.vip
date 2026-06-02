---
title: "Groq API Review 2026: LPU Speed, Llama 3.3 70B Pricing & OpenAI Compatibility | APIRank"
description: "Complete review of Groq API: LPU inference engine speed benchmarks, Llama 3.3 70B vs GPT-4o pricing, OpenAI-compatible REST API, free tier limits, China access, and how Groq compares to Together AI and Fireworks."
slug: "groq-api-review"
provider: "groq"
published: false
date: "2026-06-02"
type: "review"
---

# Groq API Review 2026: LPU-Powered Fastest LLM Inference, Llama 3.3 70B at $0.59/M

## Introduction: The Speed-First Inference Provider

When a chatbot response takes 8 seconds, the user has already closed the tab. Latency has quietly become the most important quality metric for any production LLM application — and Groq has bet the entire company on solving it.

Groq is the Mountain View company founded by Jonathan Ross (one of the original Google TPU architects) in 2016. Their product is the **LPU (Language Processing Unit)** inference engine — a custom-built chip plus compiler stack designed from the ground up for sequential text generation. Unlike GPU inference, which is throughput-optimized, LPU delivers **deterministic low-latency** token streaming: Llama 3.1 8B Instant runs at **1,250 tokens/second** on Groq, compared to roughly 100-200 tokens/second on most cloud GPUs.

In 2024, Groq pivoted from selling on-prem hardware to running a public inference API. By 2026 the platform hosts the most popular open-source models — Llama 3.3 70B, Llama 3.1 8B, Mixtral 8x7B, Gemma 2 9B, plus Whisper Large V3 for speech — and exposes them through an **OpenAI-compatible REST endpoint**. Existing OpenAI SDK code usually works with a 2-line change: swap the base URL and the API key.

This review covers the Groq API in 2026: per-model pricing, free tier limits, the reality of LPU speed, the trade-offs of an inference-only product, China access, and how Groq compares to Together AI, Fireworks AI, and direct OpenAI.

## Groq API Pricing Breakdown

Groq uses **per-token pricing** billed by the second. There is no subscription, no commitment, and no minimum spend. The free tier is generous enough for development and small demos; the paid tier is pay-as-you-go.

| Model | Input ($/1M) | Output ($/1M) | Context | LPU Speed (tok/sec) |
|-------|--------------|---------------|---------|---------------------|
| Llama 3.1 8B Instant | $0.05 | $0.08 | 128K | ~1,250 |
| Llama 3.3 70B Versatile | $0.59 | $0.79 | 128K | ~500 |
| Llama 3.1 70B Versatile (legacy) | $0.59 | $0.79 | 128K | ~480 |
| Mixtral 8x7B | $0.24 | $0.24 | 32K | ~700 |
| Gemma 2 9B | $0.20 | $0.20 | 8K | ~900 |
| Llama Guard 3 8B | $0.20 | $0.20 | 8K | ~1,000 |
| Whisper Large V3 (ASR) | — | $0.006/min audio | — | — |

*Prices reflect the public API as of 2026-06-02. Output token cost is where Groq's pricing differs most from GPU-hosted competitors — Llama 3.3 70B output is ~5x cheaper than GPT-4o output.*

### Free Tier: What's Included

- **30 requests/minute** (per project)
- **14,400 tokens/minute** (per project)
- **1,000 requests/day** (per project)
- No credit card required
- Same model quality as paid tier
- Rate limits reset every minute and every day at 00:00 UTC

For a typical 500-token response, 30 requests/min lets you serve ~1 chat user per second — perfect for solo development. For production traffic, upgrade to the paid tier (no rate limit changes from paid→free, only on paid).

### How Much Can You Get for $100?

| Workload | $100 buys (Llama 3.3 70B) | $100 buys (Llama 3.1 8B) |
|----------|---------------------------|--------------------------|
| Input tokens | 169M tokens | 2,000M tokens |
| Output tokens | 126M tokens | 1,250M tokens |
| Average mixed (1:3 in/out) | ~140M total tokens | ~1,500M total tokens |
| Realistic chat sessions (avg 1K total tokens) | ~140,000 chats | ~1,500,000 chats |

For a chatbot serving 10K users × 5 messages/day × 1K tokens, monthly cost on Llama 3.3 70B is roughly **$21.50** — about 1/4 the cost of equivalent GPT-4o usage, and 5-10x faster.

## Key Advantages of Groq

- **LPU speed leadership**: 1,250 tokens/sec on Llama 3.1 8B and ~500 tok/sec on Llama 3.3 70B. Streaming responses start in **under 100ms** — versus 1-3 seconds on most GPU stacks.
- **OpenAI-compatible API**: Existing OpenAI Python/Node SDKs work with one line change. Migration from OpenAI → Groq is trivial: `client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")`.
- **Generous free tier**: 1,000 requests/day with no credit card means a weekend hackathon project can run at zero cost. Most competitors' free tiers cap at 50-200 requests/day.
- **Open-source model focus**: Groq hosts the leading open models (Llama 3.3 70B, Mixtral, Gemma) without the data privacy concerns of closed models — useful for regulated industries (healthcare, finance, legal).
- **Whisper Large V3 at rock-bottom price**: $0.006/minute audio transcription is roughly 10x cheaper than OpenAI's Whisper API. Great for call-center transcription or podcast summarization.
- **Deterministic latency**: Unlike GPU inference (which can spike 2-5x under load), LPU inference has stable, predictable response times. This matters for voice agents where inconsistent latency breaks the conversation flow.
- **No commitments or seat minimums**: Pure pay-per-token. No enterprise contract negotiation required to start.

## Limitations to Consider

- **China access requires stable proxy**: `console.groq.com` and `api.groq.com` are both blocked in mainland China. You need a reliable Hong Kong, Singapore, or US-based proxy to sign up, manage API keys, and call the API.
- **Smaller model selection than OpenAI/Anthropic**: Groq hosts open-source models only (Llama, Mixtral, Gemma, Whisper). No GPT-4o, no Claude, no Gemini Pro. If you need closed-source SOTA, Groq isn't the right fit.
- **No fine-tuning service**: Groq is inference-only. If you need to fine-tune Llama 3.3 70B on your data, you must use a different provider (Together AI, Fireworks AI, or self-host) and only use Groq for serving the fine-tuned model.
- **Free-tier rate limits strict for production**: 30 req/min and 1K req/day are fine for development but unusable for any live product. Paid tier is needed for production.
- **Max context window 128K**: Groq's Llama models cap at 128K tokens. GPT-4o offers 1M, Claude 200K. If your use case is processing 500-page PDFs, Groq won't fit.
- **Occasional capacity throttling**: During peak hours (US business hours), Groq's free tier occasionally returns 429 errors. The paid tier has reserved capacity, but budget 10-15% headroom.
- **No native vision or audio output (text-only LLMs)**: For multimodal LLM use cases, you need to combine Groq (text) with a separate vision API.

## Groq vs Together AI vs Fireworks AI vs OpenAI

| Factor | Groq | Together AI | Fireworks AI | OpenAI (GPT-4o) |
|--------|------|-------------|--------------|-----------------|
| **Inference speed (Llama 3.1 8B)** | ~1,250 tok/sec | ~150 tok/sec | ~250 tok/sec | N/A (different model) |
| **Llama 3.3 70B input price** | $0.59/M | $0.90/M | $0.90/M | N/A |
| **Llama 3.3 70B output price** | $0.79/M | $0.90/M | $0.90/M | N/A |
| **Free tier** | 1,000 req/day | $5 credit | $1 credit | $5 credit (3 months) |
| **Fine-tuning** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes (GPT only) |
| **Closed-source models** | ❌ No | ❌ No | ❌ No | ✅ GPT-4o, o1 |
| **China access** | ❌ Proxy | ❌ Proxy | ❌ Proxy | ❌ Proxy |
| **OpenAI-compatible API** | ✅ Yes | ✅ Yes | ✅ Yes | — (native) |
| **Best for** | Real-time chat, voice | Fine-tuning, batch | Production inference | Best-in-class reasoning |

The pattern: **Groq wins on speed and price-per-token, Together AI wins on fine-tuning and model variety, Fireworks AI wins on enterprise reliability, OpenAI wins on raw model quality.** For real-time applications where latency is critical, Groq is the default choice in 2026.

## Use Case Recommendations

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Real-time chatbot (sub-200ms first token) | Groq (Llama 3.1 8B Instant) | 1,250 tok/sec, $0.05/M input |
| Voice agent / phone bot | Groq (Llama 3.3 70B Versatile) | Deterministic low latency, good multilingual |
| Code completion IDE | Groq (Llama 3.1 8B Instant) | Sub-100ms response, near-free |
| Audio transcription pipeline | Groq (Whisper Large V3) | $0.006/min — 10x cheaper than OpenAI Whisper |
| Fine-tuned domain model serving | Together AI or Fireworks AI | Only they support fine-tuning |
| Long-context document analysis (500K+ tokens) | OpenAI (GPT-4o 1M context) | Groq caps at 128K |
| Best-in-class reasoning (math, code) | OpenAI (o1, o3) | Groq has no reasoning-tuned models |
| Batch processing (millions of documents) | Fireworks AI | Higher throughput, lower per-token cost at scale |
| China-direct (no proxy) | FreeModel or DeepSeek | Both offer direct CN access |

## How to Get Started

1. **Sign up**: Visit [console.groq.com](https://console.groq.com) and create an account (Google or GitHub OAuth).
2. **Generate API key**: Console → API Keys → Create new key. Store securely — keys can be rotated but not expired.
3. **Install OpenAI SDK** (or use REST): `pip install openai` (Python), `npm install openai` (Node.js), or any HTTP client.
4. **Test call**: Run a 100-token Llama 3.1 8B request. First response should arrive in <500ms.
5. **Migrate from OpenAI**: Change `base_url` to `https://api.groq.com/openai/v1` and use a Groq model name (e.g. `llama-3.1-8b-instant`).
6. **Scale up**: Move from free to paid tier for higher rate limits. No contract needed.

## FAQ

**Q: Is Groq cheaper than OpenAI for the same workload?**
A: Yes, dramatically. For an equivalent Llama 3.3 70B workload, Groq output is ~5x cheaper than GPT-4o output ($0.79 vs $15 per 1M tokens). Even accounting for slightly lower quality, the cost-per-successful-task is usually 60-80% lower.

**Q: Does Groq support streaming?**
A: Yes — Groq's OpenAI-compatible API supports Server-Sent Events (SSE) streaming out of the box. Tokens begin streaming within 50-150ms of the request.

**Q: Can I fine-tune models on Groq?**
A: No. Groq is inference-only. For fine-tuning, use Together AI (full LoRA/QLoRA support) or Fireworks AI (proprietary fine-tuning). You can fine-tune on another provider, export the merged weights, and serve them via GroqCloud's custom model endpoint (Groq Enterprise tier only).

**Q: How does Groq compare to self-hosting Llama 3.3 70B on AWS?**
A: Self-hosting on AWS p5.48xlarge (8x H100) costs ~$98/hour for the instance alone. At full utilization, you can serve ~3,000 tok/sec — comparable to Groq's paid tier, but with 24/7 cost (~$70K/month). For bursty workloads, Groq wins; for 24/7 high-volume, self-hosting on a reserved instance may break even after 6-12 months.

**Q: Does Groq work from China?**
A: Not directly. The `api.groq.com` and `console.groq.com` domains are blocked. You need a stable proxy (Hong Kong, Singapore, or US VPS running as a forward proxy) to call the API from China-based servers. For China-direct access, consider FreeModel (aggregator with Groq models + China access) or DeepSeek (CN-native).

**Q: Is Groq's free tier truly free?**
A: Yes — no credit card, no trial period, no automatic conversion to paid. You get 1,000 requests/day forever. Limits are tight (30 req/min) but real users can build hobby projects on the free tier indefinitely.

**Q: What happens if I exceed the free-tier rate limit?**
A: Groq returns HTTP 429 (Too Many Requests) with a `Retry-After` header. Implement exponential backoff in your client. The free tier resets every minute and every day at 00:00 UTC.

**Q: Can I use Groq for production?**
A: Yes — the paid tier is the same SLA as free tier (no documented SLA change), but rate limits are negotiated based on usage. For mission-critical workloads, request the Groq Enterprise tier which adds dedicated capacity and SOC 2 compliance.

## Conclusion

Groq is the default choice in 2026 for **speed-sensitive LLM applications**: real-time chatbots, voice agents, code completion, and any use case where sub-200ms first-token latency matters. The LPU engine's combination of throughput (1,250 tok/sec on Llama 3.1 8B) and deterministic low latency is unmatched by GPU-based providers.

The trade-off is model selection — Groq hosts open-source models only, so if you need GPT-4o-level reasoning, you still need OpenAI or Anthropic. For the 80% of LLM applications where Llama 3.3 70B or Mixtral is "good enough" (chat, summarization, extraction, classification), Groq delivers **better cost-per-successful-task than any major competitor** while being 5-10x faster.

If you need fine-tuning, use Together AI or Fireworks AI. If you need closed-source SOTA, use OpenAI or Anthropic. If you need China-direct access, use [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) (which aggregates Groq + others with a China-direct gateway) or DeepSeek. For everything else — start with Groq's free tier and migrate your OpenAI client with a 2-line change.

## Comparison Table (Final)

| Provider | Pricing (Llama 70B-class) | Speed | Fine-tuning | China Access | Best For |
|----------|---------------------------|-------|-------------|--------------|----------|
| **Groq** | $0.59 in / $0.79 out per 1M | ~500 tok/sec | ❌ | ❌ Proxy | Real-time chat, voice agents |
| **Together AI** | $0.90 in / $0.90 out per 1M | ~150 tok/sec | ✅ | ❌ Proxy | Fine-tuning, batch processing |
| **Fireworks AI** | $0.90 in / $0.90 out per 1M | ~250 tok/sec | ✅ | ❌ Proxy | Enterprise production inference |
| **OpenAI (GPT-4o)** | $2.50 in / $10 out per 1M | ~100 tok/sec | ✅ | ❌ Proxy | Best-in-class reasoning |
| **Anthropic (Claude 3.5)** | $3 in / $15 out per 1M | ~80 tok/sec | ❌ | ❌ Proxy | Long-context, safe completions |
| **DeepSeek (V3)** | $0.14 in / $0.28 out per 1M | ~60 tok/sec | ❌ | ✅ Direct | China-direct, low cost |
| **FreeModel** | Aggregator pricing | Model-dependent | ❌ | ✅ Direct | China-direct aggregator |
