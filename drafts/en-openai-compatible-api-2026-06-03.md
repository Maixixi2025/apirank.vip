---
title: "OpenAI-Compatible API 2026: 10 Drop-in Replacement Endpoints"
description: "Compare 10 OpenAI-compatible API providers in 2026 — Groq, OpenRouter, Together AI, FreeModel, DeepSeek. Migration code, pricing, China access, and when to switch."
slug: "openai-compatible-api-2026"
provider: "cross-provider"
published: false
date: "2026-06-03"
type: "comparison"
---

# OpenAI-Compatible API 2026: 10 Drop-in Replacement Endpoints Compared

If you build with the OpenAI Python or Node SDK, you can switch to roughly 30+ other LLM providers by changing a single `base_url` parameter. Most of those providers expose an OpenAI-compatible REST endpoint, so existing client libraries, retry logic, and streaming handlers all keep working unchanged. This is one of the most consequential pieces of API design in the 2020s — it turned the OpenAI SDK into a de-facto industry standard.

In this article we compare the **10 OpenAI-compatible providers that actually matter in 2026**, with real pricing, speed numbers, China access notes, and a working migration recipe you can paste into your own codebase.

## What Is an OpenAI-Compatible API?

An OpenAI-compatible API is a REST endpoint that mirrors the OpenAI Chat Completions schema — same `POST /v1/chat/completions` path, same JSON request body, same `stream: true` Server-Sent Events response, same `tools`/`function_call` payload for tool use. A provider that implements this contract gets drop-in compatibility with:

- The official `openai` Python and Node SDKs (set `base_url`)
- `langchain`, `llama-index`, `autogen`, and most agent frameworks
- Local coding tools: Cursor, Continue.dev, Aider, Cline, OpenHands
- Any HTTP client that already speaks to `api.openai.com`

The most common deviations are: model names (each provider has its own naming), authentication header (most use `Authorization: Bearer`, a few use `x-api-key`), and streaming format (most use SSE, a few wrap responses in JSON lines).

## Why Developers Switch from OpenAI

The reasons in 2026, in order of frequency:

1. **Cost.** Llama 3.3 70B on Groq is **$0.59 per 1M input tokens** versus **$2.50** for GPT-4o-mini. For a 100M-token-per-month workload, the difference is roughly $190/month vs $250/month on the cheap model, and much more on the flagship.
2. **Latency.** Groq's LPU serves Llama 3.1 8B at ~1,250 tokens/sec, with first-token latency under 100ms. OpenAI's GPT-4o-mini averages 300-500ms time-to-first-token. For voice agents, the difference is the difference between usable and unusable.
3. **China access.** `api.openai.com` is blocked in mainland China. FreeModel, DeepSeek, and apikey.fun all offer China-direct endpoints with no proxy.
4. **Model selection.** OpenAI has 8 main models. OpenRouter has 200+. Together AI and Fireworks host every recent open-source release within days of publication.
5. **Fine-tuning.** OpenAI fine-tuning is closed and expensive. Together AI, Fireworks, and Anyscale expose full LoRA/QLoRA fine-tuning on any open model.
6. **Data privacy.** Closed OpenAI models send your prompts to OpenAI's infrastructure. Self-hosted vLLM or Together's dedicated endpoints keep data on infrastructure you control.

## The 10 OpenAI-Compatible Providers Worth Knowing in 2026

### 1. OpenRouter — The Aggregator

- **Endpoint:** `https://openrouter.ai/api/v1`
- **Models:** 200+ (GPT-4o, Claude 3.5, Gemini, Llama, Mistral, DeepSeek, Qwen, plus community fine-tunes)
- **Pricing:** Pass-through (provider price + ~5% OpenRouter fee for some routes)
- **Free tier:** Some models free, most paid
- **China access:** ❌ Proxy required
- **Best for:** Multi-model comparison, fallback routing, accessing closed models without separate accounts

### 2. Groq — Speed Leader

- **Endpoint:** `https://api.groq.com/openai/v1`
- **Models:** Llama 3.3 70B, Llama 3.1 8B, Mixtral, Gemma, Whisper Large V3
- **Pricing:** $0.05-0.59/M input, $0.08-0.79/M output (fastest LPU engine)
- **Free tier:** 1,000 requests/day, 30 req/min — no credit card
- **China access:** ❌ Proxy required
- **Best for:** Real-time chat, voice agents, code completion where sub-200ms latency matters

### 3. Together AI — Fine-tuning + Inference

- **Endpoint:** `https://api.together.xyz/v1`
- **Models:** 200+ open models, full LoRA/QLoRA fine-tuning support
- **Pricing:** $0.18-0.90/M input, $0.18-0.90/M output depending on model
- **Free tier:** $5 credit on signup
- **China access:** ❌ Proxy required
- **Best for:** Custom fine-tuned models, batch processing, dedicated endpoints

### 4. Fireworks AI — Production Inference

- **Endpoint:** `https://api.fireworks.ai/inference/v1`
- **Models:** 100+ open models, optimized inference engine (faster than Together on some benchmarks)
- **Pricing:** $0.20-0.90/M input, $0.20-0.90/M output
- **Free tier:** $1 credit on signup
- **China access:** ❌ Proxy required
- **Best for:** Production LLM deployments, batch processing at scale

### 5. Anyscale — Enterprise Ray-Based

- **Endpoint:** `https://api.endpoints.anyscale.com/v1`
- **Models:** Llama, Mistral, custom models on Ray Serve infrastructure
- **Pricing:** $0.50-1.00/M input for hosted models, custom pricing for dedicated
- **Free tier:** $10 credit on signup (more generous than most)
- **China access:** ❌ Proxy required
- **Best for:** Enterprises that need dedicated capacity, Ray/Anyscale stack users

### 6. FreeModel — China-Direct Aggregator

- **Endpoint:** `https://api.freemodel.dev/v1`
- **Models:** 50+ including DeepSeek V3/R1, Qwen 2.5, Llama 3.1-3.3, Mistral, Claude 3.5 Sonnet, GPT-4o
- **Pricing:** Model-dependent, generally below official Western pricing
- **Free tier:** Credits on registration
- **China access:** ✅ Direct (no proxy) — main selling point
- **Best for:** China-based developers who need international models (Claude, GPT-4o) without a proxy. [Sign up via FreeModel](https://freemodel.dev/invite/FRE-7a3b6220)

### 7. DeepSeek — Cheapest Top-Tier Model

- **Endpoint:** `https://api.deepseek.com/v1`
- **Models:** DeepSeek-V3, DeepSeek-R1 (reasoning), DeepSeek-Coder
- **Pricing:** $0.14-0.27/M input, $0.28-1.10/M output — **cheapest top-tier model in 2026**
- **Free tier:** $2 credit on signup
- **China access:** ✅ Direct (CN-native company)
- **Best for:** Reasoning tasks, code generation, cost-sensitive high-volume workloads

### 8. apikey.fun — China-Direct Claude + GPT

- **Endpoint:** `https://api.apikey.fun/v1`
- **Models:** 40+ including Claude 3.5 Sonnet, GPT-4o, Gemini 2.5 Pro, DeepSeek, Qwen, Kimi
- **Pricing:** ¥1 = $1 (transparent formula: official price × group multiplier ÷ 7)
- **Free tier:** New user signup credit
- **China access:** ✅ Direct
- **Best for:** China developers who need Claude Code, OpenAI Codex, and Gemini 2.5 Pro without a proxy

### 9. vLLM — Self-Hosted Open Source

- **Endpoint:** Self-hosted, default `http://localhost:8000/v1`
- **Models:** Any HuggingFace model that fits in your GPU
- **Pricing:** Your hardware cost (~$2-4/hour for an A100, $1-2/hour for H100 spot)
- **Free tier:** N/A (self-hosted)
- **China access:** ✅ Whatever your server has
- **Best for:** Data privacy, cost at scale (>10M tokens/day), custom models

### 10. LiteLLM — The Universal Gateway

- **Endpoint:** Self-hosted proxy, default `http://localhost:4000`
- **Models:** Routes to 100+ providers (OpenAI, Anthropic, Bedrock, Vertex, Azure, all the providers above)
- **Pricing:** Free (open source) + the cost of whatever it routes to
- **Free tier:** N/A
- **China access:** Whatever the upstream has
- **Best for:** Multi-provider routing, fallback chains, budget caps, unified logging across providers

## Pricing Comparison (Llama 3.3 70B-class Models)

| Provider | Input ($/1M) | Output ($/1M) | Free Tier | Cache Discount | Best Deal |
|---|---|---|---|---|---|
| DeepSeek V3 | $0.14 | $0.28 | $2 credit | $0.014 cached | ✅ Cheapest SOTA |
| Groq Llama 70B | $0.59 | $0.79 | 1K req/day | No | ✅ Fastest |
| Together AI Llama 70B | $0.90 | $0.90 | $5 credit | $0.45 cached | ✅ Fine-tuning |
| Fireworks AI Llama 70B | $0.90 | $0.90 | $1 credit | $0.45 cached | ✅ Enterprise |
| OpenAI GPT-4o-mini | $0.15 | $0.60 | $5 (3 mo) | $0.075 cached | — Reference |
| OpenAI GPT-4o | $2.50 | $10.00 | $5 (3 mo) | $1.25 cached | — Premium |
| Anthropic Claude 3.5 Sonnet | $3.00 | $15.00 | $5 (1 mo) | $0.30 cached | — Reasoning |
| Google Gemini 2.5 Pro | $1.25 | $10.00 | 2 req/min free | $0.31 cached | — Long context |

**Pattern:** DeepSeek V3 is 5-10x cheaper than Claude 3.5 Sonnet for similar reasoning quality. Groq is the cheapest for the Llama 70B class specifically because of LPU efficiency. GPT-4o-mini is the cheapest OpenAI-native option and the easiest migration path.

## Migration Guide: 3 Lines to Switch Providers

Here's the same client code working against 6 different providers:

```python
# Before — OpenAI
from openai import OpenAI
client = OpenAI(api_key="sk-...")  # uses default base_url
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}]
)
```

```python
# After — Groq (drop-in)
from openai import OpenAI
client = OpenAI(
    api_key="gsk_...",
    base_url="https://api.groq.com/openai/v1"  # ← only change
)
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # ← only model name change
    messages=[{"role": "user", "content": "Hello"}]
)
```

```python
# DeepSeek (cheapest)
client = OpenAI(api_key="sk-...", base_url="https://api.deepseek.com/v1")
response = client.chat.completions.create(model="deepseek-chat", messages=[...])

# Together AI
client = OpenAI(api_key="...", base_url="https://api.together.xyz/v1")
response = client.chat.completions.create(model="meta-llama/Llama-3.3-70B-Instruct-Turbo", messages=[...])

# OpenRouter (200+ models)
client = OpenAI(api_key="sk-or-...", base_url="https://openrouter.ai/api/v1")
response = client.chat.completions.create(model="anthropic/claude-3.5-sonnet", messages=[...])

# FreeModel (China-direct, 50+ models)
client = OpenAI(api_key="fm-...", base_url="https://api.freemodel.dev/v1")
response = client.chat.completions.create(model="deepseek-v3", messages=[...])

# apikey.fun (China-direct, Claude + GPT)
client = OpenAI(api_key="akf-...", base_url="https://api.apikey.fun/v1")
response = client.chat.completions.create(model="claude-3-5-sonnet", messages=[...])
```

**Two changes per migration: `base_url` and `model` name.** Streaming, function calling, and structured outputs (JSON mode) all work identically.

## Use Case Recommendations

| Use Case | Recommended Provider | Why |
|---|---|---|
| Real-time chatbot, sub-200ms first token | Groq (Llama 3.1 8B Instant) | 1,250 tok/sec, $0.05/M input |
| Voice agent / phone bot | Groq (Llama 3.3 70B Versatile) | Deterministic low latency |
| Code completion IDE | Groq (Llama 3.1 8B Instant) | Sub-100ms response, near-free |
| Reasoning tasks (math, planning) | DeepSeek-R1 or OpenAI o1 | Reasoning-tuned models |
| Cost-sensitive batch (millions of docs) | DeepSeek V3 or Fireworks | Cheapest per-token, high throughput |
| Fine-tuned domain model | Together AI or Fireworks | LoRA/QLoRA support |
| Multi-model fallback (chat app) | OpenRouter | Single API, 200+ models, automatic routing |
| China-direct production | FreeModel or apikey.fun | No proxy, Western models accessible |
| Data-sensitive (healthcare, legal) | Self-hosted vLLM | Data never leaves your infra |
| Multi-provider unified logging | LiteLLM proxy | One billing, one log, one auth |

## Limitations and Gotchas

- **Model naming is not standardized.** Groq uses `llama-3.1-8b-instant`, Together uses `meta-llama/Llama-3.3-70B-Instruct-Turbo`, OpenRouter uses `meta-llama/llama-3.3-70b-instruct`. The same underlying model has 3+ different IDs across providers.
- **Function calling support varies.** Most providers support OpenAI-style `tools` parameter, but some legacy ones require `function_call`. Always test your specific tool schema.
- **Streaming is SSE on most, but not all.** A few providers wrap streams in JSON lines. The OpenAI Python SDK handles both transparently, but custom clients need to detect the format.
- **Token counting differs.** Most providers use a tokenizer close to GPT-4's, but Qwen and DeepSeek use their own BPE tokenizers. A "1K tokens" in your code might bill 1,200 tokens on a different provider.
- **Rate limits are per-provider, not per-model.** A provider with 100 models may have one global rate limit, so heavy use of one model can starve the others.
- **Some "OpenAI-compatible" endpoints are partial.** A handful of providers skip the embeddings endpoint, the audio endpoint, or the assistants endpoint. Always check the provider's `/v1/models` listing before migrating.

## FAQ

**Q: Will switching from OpenAI to another provider actually save money?**
A: For most workloads, yes — 50-90% cost reduction is realistic. The exception is if you need GPT-4o-class reasoning specifically. For Llama-70B-class workloads, Groq and DeepSeek are 5-10x cheaper than GPT-4o. The catch: model quality differs. Test with your own prompts before migrating.

**Q: Do all OpenAI-compatible APIs support function calling?**
A: Most do, but the implementation varies. Groq, OpenRouter, Together AI, and Fireworks AI all support OpenAI-style `tools` parameter. Some smaller providers only support the older `function_call` parameter or skip tool use entirely. Always verify with a test call.

**Q: Which provider is best for production in 2026?**
A: For OpenAI-compatible production: Groq (if you can tolerate open models), Together AI (if you need fine-tuning), or OpenRouter (if you need model flexibility). For China production: FreeModel or apikey.fun. For data-sensitive workloads: self-hosted vLLM.

**Q: Can I use the OpenAI Python SDK with these providers?**
A: Yes — that's the whole point. Set `base_url` to the provider's endpoint and the rest of your code works unchanged. Most providers' docs show the exact one-line change for OpenAI, Anthropic, and LlamaIndex SDKs.

**Q: What about Anthropic Claude — is it OpenAI-compatible?**
A: No. Claude uses a different API schema (Messages API, not Chat Completions). To use Claude through an OpenAI-compatible interface, route through OpenRouter or apikey.fun, which wrap Claude in OpenAI format. Direct Claude usage requires the `anthropic` SDK.

**Q: How does caching work across providers?**
A: Anthropic pioneered prompt caching, OpenAI added it, and most OpenAI-compatible providers now support it. Cache reads are typically 50-90% cheaper than the standard input price. For long system prompts (>2K tokens), caching saves significant money. The implementation is provider-specific — check each provider's docs.

**Q: Which provider has the best free tier?**
A: Groq — 1,000 requests/day, no credit card, no expiration. Most others cap at $1-10 in credits that expire in 30-90 days. Groq's free tier is genuinely useful for hobby projects and small production workloads.

## Comparison Table (Final)

| Provider | Endpoint Type | Top Use Case | Cheapest Model | Speed Tier | China Access | Best For |
|---|---|---|---|---|---|---|
| OpenRouter | Aggregator (200+) | Multi-model access | Varies | Varies | ❌ Proxy | Routing, fallback |
| Groq | Inference-only | Real-time apps | $0.05/M (Llama 8B) | ⚡ Fastest (LPU) | ❌ Proxy | Voice, chat |
| Together AI | Inference + fine-tuning | Custom models | $0.18/M (Llama 8B) | Medium | ❌ Proxy | Fine-tuning |
| Fireworks AI | Inference-only | Production | $0.20/M (Llama 8B) | Fast | ❌ Proxy | Batch, enterprise |
| Anyscale | Enterprise Ray-based | Dedicated capacity | $0.50/M (Llama 70B) | Medium | ❌ Proxy | Enterprise |
| FreeModel | Aggregator (50+, CN) | China-direct | Model-dependent | Medium | ✅ Direct | China + Western models |
| DeepSeek | Native Chinese | Cost-sensitive | $0.14/M (V3) | Fast | ✅ Direct | Cheapest SOTA |
| apikey.fun | Aggregator (40+, CN) | Claude/GPT in China | ¥1=$1 formula | Medium | ✅ Direct | Claude Code users |
| vLLM | Self-hosted OSS | Data privacy | Hardware cost | Depends on GPU | ✅ Yours | Privacy, scale |
| LiteLLM | Universal gateway | Multi-provider routing | Free (proxy only) | N/A | N/A | Unified logging |

## Conclusion

The OpenAI-compatible API ecosystem in 2026 is mature enough that **for most LLM workloads, you do not need OpenAI as your primary provider.** The decision tree is now:

- **Need raw SOTA reasoning?** OpenAI o1/o3 or Claude 3.5 Sonnet (via OpenRouter).
- **Need speed?** Groq, full stop.
- **Need cost at scale?** DeepSeek V3, then Groq for open models.
- **Need fine-tuning?** Together AI or Fireworks AI.
- **Need China access?** FreeModel (50+ models) or apikey.fun (Claude/GPT in China).
- **Need data privacy?** Self-hosted vLLM.

The migration cost is near-zero — change `base_url` and `model` in your existing OpenAI client, test, deploy. Most teams find they can replace 60-80% of their OpenAI usage with 30-50% of the cost, with latency improvements on real-time use cases.

If you want to start exploring without signing up for 10 services, begin with [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) — one account gets you DeepSeek, Qwen, Llama, Claude, and GPT-4o through a single OpenAI-compatible endpoint, with China-direct access included. Pair that with Groq's free tier for real-time workloads, and you have a 90% production-ready stack on day one.
