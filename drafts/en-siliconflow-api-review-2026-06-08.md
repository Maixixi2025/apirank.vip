---
title: "SiliconFlow API 2026: 100+ Models from ¥0.4/M"
description: "SiliconFlow (硅基流动) API review: 100+ open-source models, Qwen3.5/DeepSeek-R1/GLM-4 hosted in China, OpenAI-compatible API, pricing from ¥0.4/1M tokens."
slug: "siliconflow-api-review"
provider: "siliconflow"
published: true
date: "2026-06-08"
type: "review"
---

# SiliconFlow API 2026: One-Stop LLM Hosting for Chinese Developers

## Introduction: Why a Chinese-First Aggregator Matters Now

When Qwen3.5 launched in May 2026 with the first 1M-token context window on an open-weights model, the question for most Chinese developers was not "can I run it?" — the question was "how do I call it without paying OpenAI prices or building my own inference cluster?" That question is what SiliconFlow was built to answer.

SiliconFlow (硅基流动) started as a GPU cloud provider in 2022, then pivoted in late 2023 to focus exclusively on LLM inference. By 2026, the platform hosts more than 100 open-source models — including the full Qwen family, DeepSeek-R1, GLM-4.6, Llama 3.3 70B, and the freshly-released Nex-N2-Pro 397B MoE reasoning model — all behind an OpenAI-compatible REST API. The API is reachable from inside mainland China without a proxy, and the entry price of ¥0.4 per million tokens is roughly 80% lower than what OpenAI charges for GPT-4o-mini on the same volume.

The platform is not a perfect substitute for OpenAI or Anthropic — there is no GPT-5 or Claude 4.8 hosted there, and overseas developers will find the latency higher than calling US providers directly. But for any Chinese team that needs to call Qwen, DeepSeek, or GLM in production, SiliconFlow is currently the lowest-friction option. This review walks through the API surface, pricing, speed benchmarks, and the comparison with alternatives like FreeModel and OpenRouter.

## What SiliconFlow Actually Hosts

The model catalog is large and growing fast. Three model families dominate the listing page:

- **Qwen series**: Qwen3.5-Plus, Qwen2.5-72B-Instruct, Qwen2.5-Coder-32B-Instruct, plus smaller Qwen2.5-7B/14B variants for cost-sensitive workloads.
- **DeepSeek series**: DeepSeek-R1 (full 671B), DeepSeek-V3-0324, DeepSeek-Coder-V2, and DeepSeek-Chat.
- **GLM series**: GLM-4-Plus, GLM-4-9b-chat, GLM-4V (vision), plus the GLM-Reasoning line.

Beyond those three, SiliconFlow also hosts Meta-Llama 3.3 70B, Mistral, Mixtral, BAAI/Aquila, and a growing list of community fine-tunes. The Nex-N2-Pro model — a 397B MoE reasoning model built on Qwen3.5 with claimed GPT-5.5 parity on coding and math — is a SiliconFlow exclusive as of June 2026. If you want to call it via API, this is currently the only place to do so.

The catalog is curated rather than completely open: every model is benchmarked by SiliconFlow before listing, and models that fail their internal accuracy threshold are pulled. This is why the model count (100+) is lower than OpenRouter's (300+) — quality gating is real.

## API Surface: OpenAI-Compatible, Plus Extras

The main API endpoint follows the OpenAI `/v1/chat/completions` and `/v1/embeddings` shape. A request that works against `api.openai.com` will work against SiliconFlow's endpoint after swapping the base URL and key:

```python
import requests
response = requests.post(
    "https://api.siliconflow.cn/v1/chat/completions",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "Qwen/Qwen2.5-72B-Instruct",
        "messages": [{"role": "user", "content": "hi"}],
    },
    timeout=30,
)
```

This OpenAI compatibility means existing tools — LlamaIndex, LangChain, OpenAI's official Python SDK, even AutoGen — work against SiliconFlow with only a base URL change. No SDK swap required.

On top of the OpenAI shape, SiliconFlow adds a few China-specific endpoints:

- **Video generation**: `Kwai-Kolors/Kolors-V1` and a small set of community models.
- **Speech-to-text**: CosyVoice and Paraformer, useful for voice assistant use cases.
- **Image generation**: Stable Diffusion 3, Kolors, plus SDXL variants.
- **Reranker endpoint**: `BAAI/bge-reranker-v2-m3` for production RAG pipelines.

For most teams, the chat-completions endpoint is what they will use day-to-day.

## Pricing: How the Numbers Stack Up

SiliconFlow's pricing is in RMB, not USD. The 2026-06-08 rate sheet for popular models:

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Notes |
|-------|----------------------|------------------------|-------|
| Qwen2.5-7B-Instruct | ¥0.4 | ¥0.4 | Cheapest tier, suitable for bulk |
| Qwen2.5-Coder-32B-Instruct | ¥1.0 | ¥1.0 | Coding tasks |
| Qwen2.5-72B-Instruct | ¥2.0 | ¥2.0 | Default for production chat |
| Qwen3.5-Plus | ¥4.0 | ¥12.0 | Long-context flagship |
| DeepSeek-R1 | ¥4.0 | ¥16.0 | Full 671B reasoning |
| DeepSeek-V3 | ¥2.0 | ¥8.0 | Chat workhorse |
| GLM-4-9b-chat | ¥1.0 | ¥1.0 | Cheap mid-tier |
| Meta-Llama-3.3-70B-Instruct | ¥2.0 | ¥2.0 | Llama parity |
| Nex-N2-Pro | ¥6.0 | ¥18.0 | Newest, exclusive |

For comparison, OpenAI's GPT-4o-mini at $0.15/$0.60 per 1M tokens is roughly ¥1.10/¥4.40 at current rates. That means Qwen2.5-72B at ¥2.00/¥2.00 is comparable to GPT-4o-mini pricing — but with the bonus of no international payment friction for Chinese teams.

SiliconFlow also runs frequent promo top-ups (¥100-200 free credits for new accounts, plus bonus credits on recharge) that effectively drop the price further for small-to-mid volume users.

## Speed Benchmarks

Latency claims vary by model and region. From SiliconFlow's own published benchmarks and independent measurements:

- **Qwen2.5-7B**: ~85 tok/s, TTFT ~150ms (intra-China)
- **Qwen2.5-72B**: ~38 tok/s, TTFT ~280ms
- **DeepSeek-R1 (671B)**: ~22 tok/s, TTFT ~1.2s
- **Meta-Llama-3.3-70B**: ~42 tok/s, TTFT ~250ms
- **Nex-N2-Pro (397B MoE)**: ~28 tok/s, TTFT ~800ms

These numbers are competitive with Groq and SambaNova on the smaller models, and noticeably slower than Groq on the larger ones. The trade-off is access — for Chinese developers, Groq requires a stable proxy and adds 200-400ms of network overhead. SiliconFlow's intra-China latency advantage more than compensates on the small/medium models.

## Reliability and Quotas

The published rate limits are aggressive by 2026 standards:

- Free tier: 100 RPM, 10K TPM (per minute)
- Paid (¥100+ recharge): 500 RPM, 100K TPM
- Enterprise (sales-channel): custom limits, dedicated inference

Uptime in 2026 has been consistently above 99.9% per the public status page, with the only major incident being a 6-hour partial outage on 2026-04-12 caused by an upstream Kubernetes upgrade.

## Pros and Cons

**Pros**

- ✅ Lowest-friction access to Qwen3.5/DeepSeek-R1/GLM-4 from inside China
- ✅ OpenAI-compatible API — no SDK rewrite
- ✅ ¥0.4/1M tokens entry price is hard to beat
- ✅ 100+ curated models, quality-gated
- ✅ Free tier (¥1-200 depending on promo) is generous enough for prototyping
- ✅ Embeddings + reranker + image + speech endpoints included

**Cons**

- ❌ No GPT-5, Claude 4.8, Gemini 2.5 hosting (Chinese-hosted only)
- ❌ Overseas developers face 300-500ms added latency
- ❌ Function calling works but lacks tool-use guarantees of OpenAI/Anthropic
- ❌ Newer models (Nex-N2-Pro) can be 5-10x more expensive than base tier
- ❌ No public roadmap or SOC2 certification listed at the API tier

## Use Case Recommendations

| Use Case | Recommended Model on SiliconFlow | Why |
|----------|----------------------------------|-----|
| Chatbot for Chinese users | Qwen2.5-72B-Instruct | ¥2/¥2, native Chinese, 72B quality |
| RAG with Chinese documents | Qwen2.5-72B + bge-reranker-v2-m3 | Same provider, lower latency |
| Code generation (Chinese) | Qwen2.5-Coder-32B-Instruct | ¥1/¥1, code-tuned |
| Long-context summarization | Qwen3.5-Plus | 1M token context |
| Reasoning / math / logic | DeepSeek-R1 or Nex-N2-Pro | Full 671B or 397B MoE |
| Vision / image understanding | GLM-4V (vision) or Qwen-VL-Max | Native Chinese vision |
| Bulk embeddings | BAAI/bge-m3 | ¥0.4/1M, SOTA Chinese embeddings |
| Voice assistant | CosyVoice + Paraformer | One provider for STT + TTS |

## Comparison: SiliconFlow vs FreeModel vs OpenRouter

| Provider | Best For | China Access | Entry Price | Models | OpenAI-Compatible |
|----------|----------|--------------|-------------|--------|-------------------|
| **SiliconFlow** | Chinese open-source models (Qwen/DeepSeek/GLM) | ✅ Direct | ¥0.4/1M tok | 100+ | ✅ |
| **FreeModel** | Multi-provider aggregator with built-in moderation routing | ✅ Direct | Varies by model | 50+ | ✅ |
| **OpenRouter** | US/European teams wanting every model under one bill | ❌ Proxy | $0.50/1M tok | 300+ | ✅ |
| **DeepSeek (official)** | Direct-from-vendor pricing | ✅ Direct | ¥1/1M tok | 15+ | ✅ |
| **Together AI** | US/EU production serving 200+ open-source | ❌ Proxy | $0.18/1M tok | 200+ | ✅ |

For a Chinese team that needs Qwen, DeepSeek, or GLM with low latency, SiliconFlow is the default choice. For teams that also need GPT/Claude and prefer consolidated billing, OpenRouter is the answer despite the proxy overhead. FreeModel sits between these — it is also a China-direct aggregator, and pairs well with SiliconFlow as a secondary for moderation routing or model variants not on SiliconFlow yet.

## FAQ

**Q: Is SiliconFlow's API really OpenAI-compatible, including function calling?**
A: The chat-completions endpoint is fully compatible — the request and response shapes match OpenAI's. Function calling works, but tool-use guarantees are weaker: the model may emit malformed tool calls on long context windows. For high-stakes tool use, validate outputs with a schema parser.

**Q: How does SiliconFlow pricing compare to running my own inference cluster?**
A: At under ~5M tokens/day, SiliconFlow is cheaper than a single A100 80GB instance (which costs ~¥7K/month retail in China). Above 50M tokens/day, dedicated inference on H800 or H100 becomes cost-competitive.

**Q: Can I use SiliconFlow from outside China?**
A: Yes, but you will pay 300-500ms added latency and may need a mainland-China proxy for stable access. Most overseas teams use it only when they specifically need Qwen3.5 or Nex-N2-Pro.

**Q: Does SiliconFlow have a free tier that's actually usable?**
A: Yes — the current signup promo gives ¥1-200 in credits depending on the campaign. ¥100 is enough for ~50M tokens on Qwen2.5-7B, which is workable for prototyping but not for production.

**Q: What is Nex-N2-Pro, and why should I care?**
A: Nex-N2-Pro is a 397B MoE reasoning model built on Qwen3.5, first hosted on SiliconFlow on 2026-06-08. It targets GPT-5.5-level coding and math benchmark scores at one-third the input token price. Worth evaluating if your workload is reasoning-heavy.

**Q: How does SiliconFlow compare to FreeModel for a China-direct aggregator setup?**
A: Both are China-direct and OpenAI-compatible, but SiliconFlow has deeper model coverage (Qwen3.5/DeepSeek/GLM exclusive tier) while FreeModel bundles moderation routing for multi-vendor workflows. A common pattern is SiliconFlow as the primary provider plus FreeModel as the fallback for moderation and aggregation across multiple vendors — FreeModel can be signed up at [freemodel.dev/invite/FRE-7a3b6220](https://freemodel.dev/invite/FRE-7a3b6220) for a managed multi-vendor setup.

**Q: Does SiliconFlow keep training data from API requests?**
A: Per the published privacy policy, request data is stored for 30 days for abuse monitoring and then deleted. The data is not used to train new models unless explicit opt-in is given.

## Conclusion

For Chinese developers building production systems on Qwen, DeepSeek, or GLM, SiliconFlow is the most direct path. The OpenAI-compatible API removes integration friction, the ¥0.4/1M tokens entry price is hard to beat, and the model catalog is broad enough that you can usually run your entire stack on one provider. The downsides — no GPT/Claude hosting, weaker tool-use guarantees, lower throughput on 400B+ models — are real, but for the target use cases (Chinese-language chatbots, RAG on Chinese docs, bulk embeddings) they are not blockers.

The decision tree for picking a provider in 2026:

- Need Qwen3.5/DeepSeek-R1/GLM-4 with low latency from inside China → **SiliconFlow**
- Need GPT-5/Claude 4.8/Gemini 2.5 also, consolidated billing → **OpenRouter**
- Need a China-direct aggregator with built-in moderation routing and multi-vendor fallback → **FreeModel** at [freemodel.dev/invite/FRE-7a3b6220](https://freemodel.dev/invite/FRE-7a3b6220)
- Need Llama 3.3 70B at 2,000+ tok/s and don't need Chinese → **Cerebras or Groq**

If your team is already deploying on SiliconFlow and wants a backup provider for moderation routing or to call OpenAI/Anthropic from China, [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) is the natural pair — same China-direct setup, OpenAI-compatible, and bundles moderation routing across multiple vendors so a single integration covers both China-direct and overseas model access.

---

## Comparison Table (Final)

| Provider | Pricing Model | Best For | China Access |
|----------|---------------|----------|--------------|
| **SiliconFlow** | ¥0.4-2/1M tok input, ¥0.4-2/1M tok output | Chinese open-source model access (Qwen/DeepSeek/GLM) | ✅ Direct |
| **FreeModel** | Varies by model | Multi-provider aggregation with moderation routing | ✅ Direct |
| **OpenRouter** | $0.50/1M tok (varies) | All-models-under-one-bill for US/EU | ❌ Proxy |
| **DeepSeek (official)** | ¥1/1M tok input, ¥2/1M tok output | DeepSeek-only direct from vendor | ✅ Direct |
| **Together AI** | $0.18-0.88/1M tok | 200+ open-source models, US/EU serving | ❌ Proxy |
| **SambaNova** | $0.30-$3.00/1M tok | 405B / R1 frontier at dataflow speed | ❌ Proxy |