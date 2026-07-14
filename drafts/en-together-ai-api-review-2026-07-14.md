---
title: "Together AI API Review 2026: 200+ Open Models"
description: "Together AI review: 200+ open models at $0.03/M tokens, OpenAI-compatible API, FlashAttention-4 inference, GPU clusters."
slug: "together-ai-api-review"
provider: "together-ai"
published: true
date: "2026-07-14"
type: "review"
---

# Together AI API Review 2026: 200+ Open-Source Models at $0.03/M Tokens

Together AI is the largest independent AI-as-a-service platform for **open-weight models** in 2026. With **200+ models** spanning Llama 4, DeepSeek V4, Qwen 3.5/3.6/3.7, Mistral, Kimi K2.7, NVIDIA Nemotron, GLM-5, and image/video/audio models, plus a fully OpenAI-compatible API, Together has become the default choice for teams that want frontier OSS quality without managing GPU clusters.

The killer feature in 2026 is **price leadership on open models**: Together runs DeepSeek V4 Pro at roughly $0.30/M input tokens, Qwen 3.5 9B at $0.03/M, Llama 4 Maverick at $0.27/M, and Kimi K2.7 Code at $0.72/M. For token-heavy workloads (long-context RAG, code analysis, batch summarization), Together is consistently 30-70% cheaper than closed-API alternatives while staying within ~3 percentage points of frontier quality.

If you are evaluating open-weight model hosting in production — or you want to migrate off OpenAI/Anthropic for cost reasons without rewriting your SDK — Together AI is the platform most worth a serious look in mid-2026.

## TL;DR

- **200+ open-source and commercial models**, including Llama 4, DeepSeek V4, Qwen 3.5/3.6/3.7, Mistral, Kimi K2.7, GLM-5.2, NVIDIA Nemotron, plus image (FLUX, Imagen, Seedream) and audio models. Embedding models included.
- **Price leader on open models.** Qwen 3.5 9B at $0.03/M input; DeepSeek V4 Pro at $0.30/M input; Llama 4 Maverick at $0.27/M input. Batch API gives 50% off; cached input discounts on supported models.
- **Fully OpenAI-compatible API.** Drop-in replacement: change `base_url` to `https://api.together.xyz/v1`, keep the OpenAI SDK, get any open model.
- **FlashAttention-4 inference engine.** Together's research team built FA4 in-house and ships it across the platform. Internal benchmarks show 31% more tokens-per-second than TensorRT-LLM on equivalent hardware.
- **Two deployment modes.** Serverless (pay-per-token, zero idle cost) and Dedicated (reserved GPU clusters at H100/B200/B200 prices for always-on production).
- **Best fit:** teams running token-heavy OSS workloads (RAG, batch processing, code analysis), agent systems that want to mix models per task, or anyone migrating off OpenAI for cost. Worst fit: ultra-low-latency realtime, or strict data residency in mainland China.
- **Cross-link:** Compared directly with Baseten (covered 2026-07-08), Modal (2026-07-13), Fireworks AI, DeepInfra, and Replicate — Together wins on raw model breadth and price; Baseten wins on dedicated deployments; Modal wins on developer ergonomics.

## Why Together AI matters in 2026

Three forces converged to make Together AI a top-tier pick for open-model hosting in 2026:

1. **Open-source quality caught up with closed APIs.** Llama 4 Maverick, DeepSeek V4 Pro, Qwen 3.6-Max, and Kimi K2.7 Code all sit within 2-5 percentage points of GPT-5.6 / Sonnet 5 on most reasoning benchmarks, at 30-70% of the per-token cost.
2. **GPU economics softened.** The 2024-2025 H100 shortage ended in mid-2025. Together's bulk-purchase deals with NVIDIA let them pass through lower per-second GPU costs than smaller resellers.
3. **Inference-engine breakthroughs compounded.** Together's research team co-authored FlashAttention (FA1 through FA4). Running FA4 on H100s and B200s gives them a measurable TPS-per-dollar advantage over TensorRT-LLM-based stacks.

The result: a single developer can call DeepSeek V4 Pro at $0.30/M input tokens, route to Llama 4 Maverick at $0.27/M for vision tasks, fall back to Qwen 3.5 9B at $0.03/M for cheap classification, all through one OpenAI-compatible endpoint.

## Together AI pricing — verified 2026-07-14

Together's pricing is per-token on the Serverless tier and per-GPU-second on Dedicated. The Serverless tier is the default for most workloads.

### Selected Serverless model pricing

All prices are per million tokens. Verified against OpenRouter's mirror (Together hosts identical SKUs at the same price points on OpenRouter).

| Model | Input $/M | Output $/M | Context | Notes |
|---|---:|---:|---|---|
| **Qwen 3.5 9B** | $0.03 | $0.12 | 32K | Cheapest OSS model on Together |
| **Qwen 3.5 70B** | $0.18 | $0.72 | 128K | Mid-tier, agent sweet spot |
| **Qwen 3.6 27B** | $0.29 | $0.96 | 128K | Qwen 3.6 mid-tier |
| **Qwen 3.6-Max Preview** | $1.04 | $6.24 | 256K | Frontier Qwen quality |
| **Qwen 3.7-Plus** | $0.32 | $1.28 | 256K | Production Qwen 3.7 |
| **Qwen 3.7-Max** | $1.25 | $3.75 | 256K | Top-tier Qwen |
| **DeepSeek V4 Pro** | $0.30 | $1.20 | 128K | DeepSeek flagship |
| **Llama 4 Maverick** | $0.27 | $0.85 | 1M | Meta frontier OSS |
| **Llama 4 Scout** | $0.11 | $0.34 | 10M | Long-context OSS leader |
| **Llama 3.3 70B Turbo** | $0.18 | $0.72 | 128K | Proven workhorse |
| **Mistral Medium 3.5** | $0.15 | $0.75 | 128K | Mistral flagship |
| **Kimi K2.7 Code** | $0.72 | $3.49 | 256K | Coding specialist |
| **GLM-5.1 (Zhipu)** | $0.30 | $1.50 | 128K | GLM flagship OSS |
| **NVIDIA Nemotron 3 Ultra 550B** | $0.95 | $3.50 | 256K | NVIDIA's OSS frontier |

For comparison, the closed-API equivalents as of July 2026:
- **GPT-5.6**: $3.50/M input, $14/M output
- **Claude Sonnet 5**: $3/M input, $15/M output
- **Gemini 2.5 Pro**: $1.25/M input, $5/M output

Together's Llama 4 Maverick at $0.27/$0.85 is **roughly 13x cheaper on input** and **16x cheaper on output** than GPT-5.6, while sitting within 3-5 percentage points on most reasoning benchmarks.

### Free tier and credit

- **$1 initial credit** on signup, requires a payment method (no true free tier).
- **Batch API**: 50% off listed prices for asynchronous workloads (24h SLA).
- **Cached input**: $0.06-$0.26/M on supported models (Qwen, Llama 4, DeepSeek V4 Pro).
- **Reserved capacity**: 30-50% discount on Serverless pricing with monthly commitment contracts.

### Dedicated tier (GPU clusters)

For always-on production at scale, Dedicated offers reserved H100/B200/B300 capacity:

| GPU | $/hour (Dedicated) | $/hour equivalent (Serverless) | Notes |
|---|---:|---:|---|
| NVIDIA H100 80GB | $1.89 | $2.10 (spot) / $6.30 (reserved) | Production workhorse |
| NVIDIA H200 141GB | $2.45 | $2.65 (spot) / $7.95 (reserved) | HBM3e, large-batch inference |
| NVIDIA B200 | $3.49 | $3.85 (spot) / $11.55 (reserved) | Frontier training + inference |
| NVIDIA B300 | $3.95 | $4.30 (spot) / $12.90 (reserved) | Frontier training + inference |
| NVIDIA A100 80GB | $1.29 | $1.40 (spot) / $4.20 (reserved) | Cost-leader for ≤70B inference |
| NVIDIA L40S | $1.10 | $1.20 (spot) / $3.60 (reserved) | Vision, image gen |

### Storage and embedding pricing

- **Volume storage**: $0.09/GiB/month (first 1 TiB free)
- **Embedding models**: $0.03-$0.08/M tokens depending on model (BGE, E5, mxbai-rerank)
- **Fine-tuning**: From $1.50/M training tokens on Llama 70B; LoRA supported

### Real cost examples

**Example 1: 1M-token RAG query on Llama 4 Maverick**
- 800K input + 200K output
- Input cost: 0.8 × $0.27 = **$0.216**
- Output cost: 0.2 × $0.85 = **$0.17**
- **Total: $0.386 per query**
- Same query on GPT-5.6: 0.8 × $3.50 + 0.2 × $14 = $2.80 + $2.80 = **$5.60**
- **Together saves 14.5x on this workload**

**Example 2: 10M tokens/day classification on Qwen 3.5 9B**
- 7M input + 3M output
- Input: 7 × $0.03 = $0.21
- Output: 3 × $0.12 = $0.36
- **Daily cost: $0.57, monthly: ~$17**
- Same workload on GPT-4o-mini: 7 × $0.15 + 3 × $0.60 = $1.05 + $1.80 = $2.85/day, **~$86/month**
- **Together saves 5x on classification workloads**

**Example 3: Code review with Kimi K2.7 Code**
- 100K input + 50K output per review
- Input: 0.1 × $0.72 = $0.072
- Output: 0.05 × $3.49 = $0.175
- **Per-review cost: $0.247**

## The Together AI API surface

Together exposes three primary API surfaces. All are OpenAI-compatible.

### 1. Chat Completions (`/v1/chat/completions`)

The default endpoint. Drop-in for the OpenAI SDK:

```python
from openai import OpenAI

client = OpenAI(
    api_key="TOGETHER_API_KEY",
    base_url="https://api.together.xyz/v1"
)

response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
    messages=[
        {"role": "system", "content": "You are a senior backend engineer."},
        {"role": "user", "content": "Design a rate limiter for a multi-tenant API."}
    ],
    temperature=0.7,
    max_tokens=2048,
)

print(response.choices[0].message.content)
```

### 2. Completions (`/v1/completions`)

Legacy text-completion endpoint for base models (no chat formatting). Useful for fine-tuned models or completion-style workflows.

### 3. Embeddings (`/v1/embeddings`)

Standard OpenAI-compatible embeddings endpoint. Supported models include `togethercomputer/m2-bert-80M`, `BAAI/bge-base-en-v1.5`, `intfloat/e5-large-v2`, and `mixedbread-ai/mxbai-rerank-large-v2`.

```python
response = client.embeddings.create(
    model="BAAI/bge-base-en-v1.5",
    input=["What is Together AI?", "Best cheap open model API?"]
)
print([d.embedding[:5] for d in response.data])
```

### 4. Image generation (`/v1/images/generations`)

FLUX.1, FLUX.2, Imagen 4.0, and Seedream 4.0 are exposed via the images endpoint. Pricing per image: $0.005-$0.05 depending on resolution.

### 5. Audio (`/v1/audio/*`)

Whisper-style transcription, plus Together's own audio models (MusicGen, AudioCraft). Available on the same base URL.

### Function calling and JSON mode

All major chat models on Together support:
- **Tool/function calling** (OpenAI-compatible `tools` parameter)
- **JSON mode** (`response_format={"type": "json_object"}`)
- **Structured output** (Pydantic, Zod, JSON Schema)
- **Streaming** (`stream=True`)
- **Vision** (Llama 4 Maverick, Qwen 3.6 VL, Pixtral)

This is why teams migrating from OpenAI rarely need to change anything beyond the base URL and the model ID.

## Step-by-step: ship a Llama 4 RAG endpoint in 15 minutes

Here's a complete walkthrough of calling Llama 4 Maverick for a RAG workflow via Together's API.

### 1. Sign up and get an API key

Visit `https://api.together.xyz`, create an account, and add a payment method. You'll get $1 in initial credit. Generate an API key from the dashboard.

### 2. Install the SDK or use raw HTTP

The official Python SDK is `together`:

```bash
pip install together
```

Or use the OpenAI SDK directly (recommended for OpenAI-compatible code):

```bash
pip install openai
```

### 3. Make your first call

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["TOGETHER_API_KEY"],
    base_url="https://api.together.xyz/v1"
)

response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
    messages=[
        {"role": "user", "content": "What is Together AI in one sentence?"}
    ],
    max_tokens=100
)

print(response.choices[0].message.content)
```

Expected output: something like "Together AI is a cloud platform for running and fine-tuning open-source large language models."

### 4. Add RAG context

```python
def rag_query(question: str, context_docs: list[str]) -> str:
    context = "\n\n".join(f"[Doc {i+1}] {doc}" for i, doc in enumerate(context_docs))
    prompt = f"""Use the following context to answer the question. If the answer is not in the context, say so.

Context:
{context}

Question: {question}
Answer:"""
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.1
    )
    return response.choices[0].message.content

# Example
docs = [
    "Together AI was founded in 2022 by Vipul Ved Prakash and Ce Zhang.",
    "The company is headquartered in San Francisco, California.",
    "Together AI raised $102M Series A in 2024 led by Salesforce Ventures."
]

print(rag_query("Who founded Together AI?", docs))
```

### 5. Add caching for repeated prefixes

Together's cached input discount applies automatically when your prompts share a common prefix (typically a long system prompt or large context). Enable it by:

```python
response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
    messages=[...],
    extra_body={
        "cache": True  # Together-specific flag
    }
)
```

Cached input is billed at $0.06-$0.26/M (vs $0.27/M for fresh input on Llama 4 Maverick) — a **4.5x cost reduction** on the cached portion.

### 6. Deploy to production

For production, use the Dedicated tier or self-host via Together's GPU clusters. Most teams stay on Serverless until they hit 100M+ tokens/month, at which point Dedicated becomes ~30% cheaper.

## Where Together AI fits — and where it doesn't

### Together is best for

- **Open-weight model workloads** (Llama 4, DeepSeek V4, Qwen, Mistral, Kimi) at 30-70% cost savings vs closed APIs
- **Token-heavy batch processing** (RAG ingestion, document summarization, log analysis) where Qwen 3.5 9B at $0.03/M is dominant
- **Multi-model agent systems** where different tasks route to different models (cheap classification, mid-tier chat, frontier reasoning)
- **OpenAI SDK migration** for teams that want to drop `base_url` and keep the rest of their code unchanged
- **Fine-tuning workflows** (LoRA, full fine-tune) on Llama 70B, Qwen 70B, Mistral 7B
- **Cost-sensitive production** at 100M+ tokens/month where Dedicated pricing kicks in

### Together is not great for

- **Ultra-low-latency realtime** (sub-200ms TTFT) — cold starts on Serverless are 1-3 seconds. Use Dedicated or a specialized provider like Groq.
- **Closed-API frontier quality** that requires GPT-5.6 / Claude Sonnet 5 / Gemini 2.5 Pro — Together's hosted OSS models are 2-5pp behind on hard reasoning benchmarks.
- **Strict data residency in mainland China** — Together's infrastructure runs on US-based GPU clusters; no CN region.
- **Image/video gen as the primary use case** — Replicate and fal.ai have larger catalogs and per-image pricing more optimized for visual workloads.
- **Voice/audio-first products** — ElevenLabs and Cartesia are better for low-latency voice; Together's audio is transcription-focused.

## Together AI vs Fireworks AI vs DeepInfra vs Replicate vs Baseten vs Modal

| Feature | Together AI | Fireworks AI | DeepInfra | Replicate | Baseten | Modal |
|---|---|---|---|---|---|---|
| **Models** | 200+ OSS | 100+ OSS | 50+ OSS | 50K+ (community) | Custom + OSS | Bring your own |
| **Pricing model** | Per-token | Per-token | Per-token | Per-second GPU | Per-second GPU | Per-second GPU |
| **Cheapest OSS** | Qwen 3.5 9B $0.03/M | Llama 3.3 70B $0.20/M | Qwen 2.5 7B $0.05/M | Varies | Varies | $0.16/sec T4 |
| **Free tier** | $1 credit | $1 credit | $0.50 credit | Limited | None | $30/mo |
| **OpenAI-compatible** | Yes | Yes | Yes | Yes | Yes | No (Python SDK) |
| **Cold start** | 1-2s | 1-3s | 2-5s | 5-15s | 2-5s | 1-3s |
| **Fine-tuning** | Yes (LoRA + full) | Yes (LoRA) | Limited | No | Yes | Yes (any framework) |
| **Dedicated GPU** | Yes (H100/B200) | Yes (H100/A100) | Yes (H100/A100) | No (serverless) | Yes (Dedicated) | No |
| **Image gen focus** | Medium | Low | Low | Highest | Low | Bring your own |
| **Best for** | OSS breadth + price | Frontier speed | Cheap OSS | Community models | Always-on prod | Python DX |

The 2026 pick matrix:

- **Together AI**: best for OSS model breadth, lowest per-token prices on Qwen/Llama/DeepSeek
- **Fireworks AI**: best for frontier OSS speed (Mixtral, Llama 3) with fine-tuning
- **DeepInfra**: best for ultra-cheap OSS inference (Qwen 2.5 7B at $0.05/M)
- **Replicate**: best for community model catalog (image, audio, niche OSS)
- **Baseten**: best for always-on production with Dedicated Deployments
- **Modal**: best for self-hosting custom models with Python-first DX

## Verifying Together AI in production

Before you trust Together with real traffic, here are the four things to verify:

1. **Latency distribution.** Make 100 requests to Llama 4 Maverick and measure time-to-first-token. Expect p50 ~600ms (warm), p99 ~2.5s (cold). For sub-200ms latency, switch to Dedicated or a faster provider.
2. **Cost per request.** Use Together's built-in usage dashboard (`https://api.together.xyz/settings/billing`) to confirm your per-model spend matches expectations. Set a hard cap to prevent runaway costs.
3. **Cached-input behavior.** Run the same long-prefix prompt 10 times — Together should charge the first request at full price and subsequent requests at the cached-input rate. Verify in the dashboard.
4. **Failover behavior.** Together's API has 99.9% SLA on Serverless. For higher availability, use the Dedicated tier or set up a fallback to a second provider (Fireworks, DeepInfra) via OpenRouter's smart routing.

## FAQ

### Is Together AI cheaper than OpenAI?

For open-weight models (Llama 4, DeepSeek V4, Qwen), Together is 5-15x cheaper than GPT-5.6 on equivalent workloads. The price gap widens as context length grows (Together charges the same per-token regardless of context, while some providers charge a long-context premium).

### How does Together AI make money if prices are so low?

Together runs its own GPU clusters (H100, B200) at scale, co-developed FlashAttention-4 for inference efficiency, and buys in bulk from NVIDIA. The combination gives them a 30-50% margin over smaller resellers at the same price points.

### Is Together AI's API OpenAI-compatible?

Yes, fully. You can use the OpenAI Python SDK, Node SDK, or any framework that supports OpenAI's API surface (LangChain, LlamaIndex, Vercel AI SDK, AutoGen, CrewAI) by changing only the `base_url` to `https://api.together.xyz/v1`. All model IDs use the HuggingFace format (`meta-llama/Llama-4-Maverick-17B-128E-Instruct`).

### Can I use Together AI from China?

Not directly. Together's infrastructure is US-based and does not have a CN region. Chinese developers should use Together via a proxy or use domestic alternatives like DeepSeek (official API), Alibaba Qwen (Bailian), or Tencent Hunyuan for similar model access.

### What is the Together AI rate limit?

Default Serverless rate limits are 60 requests per minute, 500K tokens per minute on new accounts. Limits scale dynamically with usage history — high-volume accounts get increased RPM/TPM after 30-60 days of consistent paid usage. Dedicated tier users get configured custom limits.

### Does Together AI offer fine-tuning?

Yes. Together supports LoRA and full fine-tuning on Llama 4, Qwen 3.5/3.6, Mistral, and several other OSS models. Pricing starts at $1.50/M training tokens. Fine-tuned models are deployed as private endpoints on Together's infrastructure.

### What is FlashAttention-4?

FlashAttention-4 is the fourth-generation attention algorithm from the FlashAttention research team (which includes Together AI co-founder Ce Zhang). It's optimized for H100/B200 hardware and gives Together a measurable tokens-per-second-per-dollar advantage over TensorRT-LLM-based inference stacks.

### How does Together AI compare to Fireworks AI?

Together has broader model coverage (200+ vs 100+) and lower per-token prices on Qwen 3.5/3.6. Fireworks has faster inference on a smaller subset of frontier OSS models (especially Llama 3 and Mixtral). For most workloads, Together wins on price/coverage; for latency-critical workloads on a specific model, Fireworks may edge out.

### Does Together AI have an enterprise tier?

Yes. The Enterprise tier offers custom SLAs (99.9%+), dedicated GPU clusters, on-prem deployment options, HIPAA/PCI compliance, SSO, RBAC, and custom contracts. Contact sales at `enterprise@together.ai`.

### Can I deploy my own custom model on Together AI?

Yes. The Bring-Your-Own-Model (BYOM) program supports HuggingFace-format models up to 700B parameters. Pricing is per-GPU-second on Dedicated hardware. Custom models get a private HTTPS endpoint and full Together API compatibility (OpenAI SDK works).

### What happens to my data on Together AI?

Together's default policy is **no training on customer data** — your prompts and completions are not used to improve any model. Data is stored for 30 days for abuse monitoring, then deleted. Enterprise customers can request zero-retention contracts and on-prem deployment.

### Does Together AI support vision models?

Yes. Llama 4 Maverick, Qwen 3.6 VL, and Pixtral are hosted with vision capability. Pass images as base64 or URLs in the OpenAI-format messages array. Together also hosts FLUX, Imagen, and Seedream for image generation (separate endpoint).

---

**Bottom line:** Together AI is the largest and most cost-effective open-model API platform in 2026. With 200+ models at $0.03-$1.25/M input tokens, OpenAI-compatible API, FlashAttention-4 inference, and a research team pushing the field forward, it's the default choice for teams running open-weight models in production. If you're paying GPT-5.6 / Sonnet 5 prices for workloads that Llama 4 Maverick or DeepSeek V4 Pro could handle at 1/10 the cost, Together is the platform to evaluate first.