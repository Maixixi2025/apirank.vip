---
title: "Novita AI API 2026: 200+ Open-Source Models from $0.06/M"
description: "Novita AI API review: 200+ hosted open-source models (Llama 3.3 70B, Qwen2.5-72B, DeepSeek-R1), OpenAI-compatible API, China-direct cn.novita.ai, pricing from $0.06/1M tokens."
slug: "novita-ai-api-review"
provider: "novita-ai"
published: true
date: "2026-06-10"
type: "review"
---

# Novita AI API 2026: 200+ Open-Source Models on Singapore + China Infrastructure

## Introduction: The GPU Cloud That Pivoted to LLM Inference

In 2023, Novita AI was a small Singapore-based GPU cloud renting out A100 and H100 instances by the hour. By 2025, the company had added 200+ open-source LLMs to a unified inference API, launched a separate China-direct endpoint at `cn.novita.ai`, and started competing directly with Together AI, Fireworks, and SiliconFlow for the open-source-model inference market.

The pitch is simple: every open-source LLM worth calling — Llama 3.3 70B, Qwen2.5-72B, DeepSeek-R1, Mistral-Nemo, Gemma 2 27B — is hosted behind one OpenAI-compatible API, with pricing that undercuts Together AI on most models by 30-50%, and a separate low-latency endpoint for users inside mainland China. The entry price of $0.06 per million tokens (Llama 3.1 8B) is among the cheapest in the market.

This is not a perfect substitute for OpenAI or Anthropic — Novita does not host GPT-5, Claude 4.8, or Gemini 2.5, and the company is still building its brand outside of GPU-cloud and Chinese-developer circles. But for any team that needs to call 200+ open-source models with predictable pricing and a single OpenAI-shaped endpoint, Novita AI is one of the strongest options in 2026. This review walks through the API surface, pricing, speed benchmarks, China access, and how it stacks up against FreeModel, Together AI, Fireworks, and SiliconFlow.

## What Novita AI Actually Hosts

The model catalog covers the full open-source landscape. The categories that dominate the listing page:

- **Meta Llama series**: Llama 3.3 70B Instruct, Llama 3.1 405B Instruct, Llama 3.1 70B, Llama 3.1 8B (in both base and instruct variants).
- **Qwen series**: Qwen2.5-72B-Instruct, Qwen2.5-Coder-32B-Instruct, Qwen2.5-7B-Instruct, plus the larger Qwen2.5-Plus for long-context.
- **DeepSeek series**: DeepSeek-V3, DeepSeek-R1 (full 671B), DeepSeek-Coder-V2, DeepSeek-Chat.
- **Mistral series**: Mistral-Nemo, Mistral-7B-Instruct-v0.3, Mixtral-8x7B-Instruct, Mistral-Large-2.
- **Google Gemma series**: Gemma 2 27B IT, Gemma 2 9B IT, CodeGemma variants.
- **Vision models**: LLaVA, Qwen-VL, CogVLM, InternVL for multimodal use cases.
- **Embedding models**: BGE-M3, BGE-Large, mxbai-embed-large, plus Cohere English/CN variants.

Beyond the standard catalog, Novita also supports custom model deployment — you can upload a private Hugging Face model and serve it through the same API surface, with billed GPU hours. LoRA fine-tuning is available through the dashboard for select base models.

The catalog is broader than Together AI (200+ vs 200+) but with less curation than SiliconFlow. If you want a specific community fine-tune from Hugging Face, Novita is more likely to have it.

## API Surface: OpenAI-Compatible, Plus Custom Endpoints

The main API endpoint follows the OpenAI `/v1/chat/completions` and `/v1/embeddings` shape. A request that works against `api.openai.com` will work against Novita's endpoint after swapping the base URL and key:

```python
import requests
response = requests.post(
    "https://api.novita.ai/v3/openai/chat/completions",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "meta-llama/llama-3.3-70b-instruct",
        "messages": [{"role": "user", "content": "hi"}],
        "stream": False,
    },
    timeout=30,
)
print(response.json()["choices"][0]["message"]["content"])
```

This OpenAI compatibility means existing tools — LlamaIndex, LangChain, OpenAI's official Python SDK, vLLM, even AutoGen — work against Novita with only a base URL change. No SDK swap required.

On top of the OpenAI shape, Novita adds a few platform-specific endpoints:

- **Serverless GPU endpoints**: Create an on-demand GPU instance with a custom model in under 60 seconds; pay only for the time the instance is active.
- **Dedicated GPU rental**: Reserve an A100, H100, or H200 instance for ongoing workloads (per-hour billing, no inference markup).
- **LoRA fine-tuning API**: Train a LoRA adapter on a base model from the dashboard, deploy it through the same OpenAI-compatible endpoint.
- **Image generation**: Stable Diffusion XL, SD3, Kolors, Playground v2.5.
- **Audio endpoints**: Whisper large-v3 for STT, plus TTS via CosyVoice and Bark.

For most teams, the chat-completions endpoint is what they will use day-to-day. The serverless GPU is the unique selling point for workloads that need a model not in the hosted catalog.

## Pricing: How the Numbers Stack Up

Novita's pricing is in USD, billed per million tokens. The 2026-06-10 rate sheet for popular models:

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Notes |
|-------|----------------------|------------------------|-------|
| meta-llama/llama-3.1-8b-instruct | $0.06 | $0.06 | Cheapest tier, bulk workloads |
| meta-llama/llama-3.3-70b-instruct | $0.39 | $0.39 | Production chat default |
| meta-llama/llama-3.1-405b-instruct | $1.52 | $1.52 | Frontier open-source |
| qwen/qwen-2.5-72b-instruct | $0.29 | $0.29 | Strong Chinese support |
| qwen/qwen-2.5-coder-32b-instruct | $0.18 | $0.18 | Code tasks |
| deepseek/deepseek-v3 | $0.18 | $0.18 | Chat workhorse |
| deepseek/deepseek-r1 | $0.30 | $0.30 | Full 671B reasoning |
| mistralai/mistral-nemo | $0.09 | $0.09 | Multilingual |
| google/gemma-2-27b-it | $0.16 | $0.16 | Lightweight production |
| meta-llama/llama-3.3-70b-instruct (cn.novita.ai) | ¥2.0 | ¥2.0 | China-direct, RMB billing |

For comparison, Together AI's Llama 3.3 70B at $0.88/$0.88 per 1M tokens is more than 2x Novita's price on the same model. Fireworks AI is closer to parity ($0.45/$0.45), but still pricier than Novita. The Llama 3.1 8B at $0.06 is the cheapest entry price among tier-1 OpenAI-compatible providers.

For Chinese teams, `cn.novita.ai` is the relevant endpoint, billed in RMB at near-parity with SiliconFlow's rate sheet. Compared to SiliconFlow, Novita's catalog is broader (more community fine-tunes, more embedding options) but the China-direct endpoint is newer and less battle-tested.

## Speed Benchmarks

Latency claims vary by model, region, and time of day. From Novita's published benchmarks and independent measurements at the 2026-06-10 cut:

- **Llama 3.1 8B**: ~120 tok/s output, TTFT ~90ms (Singapore endpoint)
- **Llama 3.3 70B**: ~55 tok/s output, TTFT ~210ms
- **Llama 3.1 405B**: ~22 tok/s output, TTFT ~480ms
- **Qwen2.5-72B**: ~48 tok/s output, TTFT ~230ms
- **DeepSeek-R1 (671B)**: ~25 tok/s output, TTFT ~1.1s
- **Mistral-Nemo**: ~95 tok/s output, TTFT ~120ms

For comparison, Groq hits 1,250 tok/s on Llama 3.1 8B and Cerebras hits 2,000+ tok/s — both significantly faster than Novita on the same model. The trade-off is breadth: Novita hosts 200+ models, Groq and Cerebras host 5-10 each. If raw speed is the only criterion, Groq or Cerebras wins. If you need to switch between 20 different models in production, Novita's breadth is hard to match.

The cn.novita.ai endpoint adds ~50-80ms of latency for users inside mainland China compared to a fully domestic provider like SiliconFlow, but is still faster than routing through any overseas endpoint.

## Reliability and Quotas

The published rate limits for Novita's API in 2026:

- **Free tier**: 60 RPM, 10K TPM (per minute)
- **Pay-as-you-go ($10+ top-up)**: 500 RPM, 100K TPM
- **Enterprise (sales-channel)**: custom limits, dedicated inference, BYOC options

Uptime in 2026 has been consistent at 99.9%+ per the public status page. The most notable incident was a 4-hour partial outage on 2026-03-18 caused by an upstream H100 supply issue; no data was lost and the company added a multi-region failover within 30 days of the incident.

The free tier is the weakest of any tier-1 OpenAI-compatible provider — just $0.5 of one-time credit. SiliconFlow offers ¥1-200 promo credits, Together AI offers $5 across all new signups, and Groq offers 14,400 requests/day. The Novita free tier is workable for one weekend of prototyping but not for ongoing dev work. Realistic paid entry is at the $10 top-up tier.

## China Access: cn.novita.ai

For Chinese developers, the `cn.novita.ai` endpoint is the most important feature. The endpoint is operated under a separate China entity with ICP-filed infrastructure, RMB billing, and direct peering to the three major Chinese carriers (China Telecom, China Unicom, China Mobile). Latency from a Beijing or Shanghai server to cn.novita.ai is typically under 30ms.

The cn.novita.ai catalog is slightly smaller than the global endpoint (160+ models vs 200+), with a focus on Qwen, DeepSeek, GLM, Yi, and other Chinese-developed models that are popular inside China. Llama and Mistral are available but at the same prices as the global endpoint.

The main limitation: the China endpoint and the global endpoint have separate API keys, separate billing, and separate rate limits. Teams operating in both China and overseas need to manage two accounts.

## Pros and Cons

**Pros**

- ✅ Lowest entry price among tier-1 OpenAI-compatible providers ($0.06/1M for Llama 3.1 8B)
- ✅ 200+ hosted open-source models, broader catalog than Together/Fireworks
- ✅ OpenAI-compatible API — no SDK rewrite
- ✅ China-direct endpoint (cn.novita.ai) with RMB billing and ICP-filed infrastructure
- ✅ Serverless GPU + dedicated GPU rental for custom model deployment
- ✅ LoRA fine-tuning API for select base models

**Cons**

- ❌ No closed-source models (GPT-5, Claude 4.8, Gemini 2.5) hosted
- ❌ Free tier is small ($0.5 one-time credit) — much weaker than Groq, Together, SiliconFlow
- ❌ Speed is competitive but slower than Groq and Cerebras on the same models
- ❌ Function calling works but tool-use guarantees are weaker than OpenAI/Anthropic
- ❌ China and global endpoints have separate accounts/keys/billing
- ❌ No public SOC2 or ISO27001 certification listed at the API tier

## Use Case Recommendations

| Use Case | Recommended Model on Novita | Why |
|----------|----------------------------|-----|
| Production chatbot (English) | llama-3.3-70b-instruct | $0.39/1M, strong general quality |
| Production chatbot (Chinese) | qwen-2.5-72b-instruct (cn.novita.ai) | ¥2/1M, native Chinese, ICP-direct |
| Code generation | qwen-2.5-coder-32b-instruct | $0.18/1M, code-tuned |
| Reasoning / math / logic | deepseek-r1 | $0.30/1M, full 671B reasoning |
| Long-context summarization | llama-3.1-405b-instruct | 128K context, $1.52/1M |
| Bulk embeddings | bge-m3 | $0.02/1M tokens, SOTA |
| Custom private model | serverless GPU endpoint | Deploy any HF model in 60s |
| Vision / image understanding | llava-onevision-qwen2-7b-ov | Native multimodal, $0.18/1M |
| Voice assistant (STT+TTS) | whisper-large-v3 + cosyvoice | One provider for both |

## Comparison: Novita AI vs FreeModel vs Together AI vs SiliconFlow

| Provider | Best For | China Access | Entry Price | Models | OpenAI-Compatible |
|----------|----------|--------------|-------------|--------|-------------------|
| **Novita AI** | 200+ open-source models, low per-token cost | ✅ Direct (cn.novita.ai) | $0.06/1M tok | 200+ | ✅ |
| **FreeModel** | Multi-provider aggregator with built-in moderation routing | ✅ Direct | Varies by model | 50+ | ✅ |
| **Together AI** | US/EU production serving of 200+ open-source | ❌ Proxy | $0.18/1M tok | 200+ | ✅ |
| **SiliconFlow** | Chinese open-source models (Qwen/DeepSeek/GLM) | ✅ Direct | ¥0.4/1M tok | 100+ | ✅ |
| **Fireworks AI** | Fast inference on 100+ open-source | ❌ Proxy | $0.20/1M tok | 100+ | ✅ |
| **DeepSeek (official)** | DeepSeek-only direct from vendor | ✅ Direct | ¥1/1M tok | 15+ | ✅ |

For a team that needs 200+ open-source models at the lowest per-token price with China-direct access, Novita AI is currently the most direct path. For teams that also need GPT/Claude and prefer consolidated billing, OpenRouter or FreeModel's aggregator setup is the right call. For Chinese teams that exclusively need Qwen/DeepSeek/GLM at the absolute lowest cost, SiliconFlow wins on price for those specific models.

## FAQ

**Q: Is Novita AI's API really OpenAI-compatible, including function calling?**

A: The chat-completions endpoint is fully compatible — request and response shapes match OpenAI's. Function calling works for simple cases (single tool, short context), but for production tool-use pipelines with multiple tools or long context, the tool-call format occasionally deviates from OpenAI's spec. Validate outputs with a schema parser if you depend on tool reliability.

**Q: How does Novita AI pricing compare to running my own inference cluster?**

A: At under ~10M tokens/day on a single model, Novita is cheaper than renting even an A100 80GB instance directly (which costs ~$1,500/month retail). Above 100M tokens/day on a single model, dedicated inference on H100 or H200 becomes cost-competitive, especially with Novita's dedicated GPU rental at $1.99/hr for an H100.

**Q: Can I use Novita AI from inside China without a proxy?**

A: Yes — the cn.novita.ai endpoint is designed for this. It has ICP-filed infrastructure, RMB billing, and direct peering to all three Chinese carriers. Latency from a typical China server to cn.novita.ai is under 30ms, comparable to a fully domestic provider.

**Q: Does Novita AI keep training data from API requests?**

A: Per the published privacy policy, request data is stored for 30 days for abuse monitoring and then deleted. The data is not used to train new models unless explicit opt-in is given. Enterprise customers can negotiate a data-residency clause (data stays in their chosen region) at the sales channel.

**Q: What is the difference between the global endpoint and cn.novita.ai?**

A: Two separate API products under the same Novita AI brand. The global endpoint (api.novita.ai) is the original Singapore-based product, billed in USD, hosting 200+ models. The cn.novita.ai endpoint is the China-specific product, billed in RMB, hosting 160+ models with a focus on Chinese-developed LLMs. Separate accounts, separate keys, separate rate limits.

**Q: How does Novita AI compare to FreeModel for a multi-vendor China-direct setup?**

A: Both are China-direct and OpenAI-compatible, but Novita is a single-vendor host of 200+ open-source models while FreeModel is a multi-vendor aggregator with built-in moderation routing. A common pattern is Novita as the primary provider for open-source workloads plus FreeModel as the moderation layer and OpenAI/Anthropic fallback — FreeModel can be signed up at freemodel.dev/invite/FRE-7a3b6220 for a managed multi-vendor setup.

**Q: Does Novita AI support LoRA fine-tuning, and what's it cost?**

A: Yes — the LoRA fine-tuning API is available for select base models (Qwen2.5-7B/14B/72B, Llama 3.1 8B/70B, Mistral-7B). Training cost is $0.50/hour on an A100 80GB instance. A typical 10K-example fine-tune takes 2-4 hours. The resulting adapter is served through the same OpenAI-compatible endpoint, billed at the base model's per-token rate plus a small adapter surcharge.

## Conclusion

For teams building production systems on open-source LLMs in 2026, Novita AI is one of the most direct paths. The OpenAI-compatible API removes integration friction, the $0.06/1M token entry price is the lowest among tier-1 OpenAI-compatible providers, the catalog of 200+ models is broader than Together AI or Fireworks, and the cn.novita.ai endpoint solves the China access problem for Chinese teams.

The decision tree for picking a provider in 2026:

- Need 200+ open-source models at the lowest per-token cost → **Novita AI**
- Need 200+ open-source models with the broadest global serving → **Together AI**
- Need Qwen3.5/DeepSeek-R1/GLM-4 with low latency from inside China → **SiliconFlow**
- Need a China-direct aggregator with built-in moderation routing and multi-vendor fallback → **FreeModel**
- Need Llama 3.3 70B at 2,000+ tok/s and don't need Chinese → **Cerebras or Groq**

If your team is already deploying on Novita AI and wants a backup provider for moderation routing or to call OpenAI/Anthropic from China, FreeModel is a natural complement — it bundles moderation routing, OpenAI-compatible APIs, and direct access to multiple vendors behind one key. Sign up at freemodel.dev/invite/FRE-7a3b6220 to get started with the free tier.

## Comparison Table (Final)

| Provider | Pricing Model | Best For | China Access |
|----------|---------------|----------|--------------|
| **Novita AI** | $0.06-$1.52/1M tok input, same for output | 200+ open-source models, lowest entry price | ✅ Direct (cn.novita.ai) |
| **FreeModel** | Varies by model | Multi-provider aggregation with moderation routing | ✅ Direct |
| **Together AI** | $0.18-$0.88/1M tok | US/EU serving of 200+ open-source | ❌ Proxy |
| **SiliconFlow** | ¥0.4-2/1M tok input, ¥0.4-2/1M tok output | Chinese open-source model access (Qwen/DeepSeek/GLM) | ✅ Direct |
| **Fireworks AI** | $0.20-$3.00/1M tok | Fast inference on 100+ open-source | ❌ Proxy |
| **DeepSeek (official)** | ¥1/1M tok input, ¥2/1M tok output | DeepSeek-only direct from vendor | ✅ Direct |
