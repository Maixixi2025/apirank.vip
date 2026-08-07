---
title: "Stepfun Step-2 API 2026 Review: Multimodal LLM, Step-R Reasoning & Pricing"
description: "Stepfun Step-2 API 2026 review: 1.2T multimodal flagship, Step-R reasoning, OpenAI-compatible endpoint, direct China access and token pricing."
slug: "stepfun-api-review"
provider: "stepfun"
published: true
date: "2026-08-05"
type: "review"
---

# Stepfun Step-2 API 2026 Review: Multimodal LLM, Step-R Reasoning & Pricing

## Introduction: Why Stepfun Matters in 2026

Stepfun (阶跃星辰) is a Shanghai AI lab founded in 2023 whose Step-2 model is a 1.2-trillion-parameter multimodal flagship accepting text, image, audio and video on a single OpenAI-compatible endpoint. Unlike most China LLM stacks that ship separate vision APIs and bill per modality, Step-2 treats every input as a content part — a video understanding call is priced the same as a text chat. The lab also ships Step-R, a reasoning model in the OpenAI o1 / DeepSeek R1 class, at roughly 1/5 the price.

The honest frame for Stepfun in August 2026: this is **not** a frontier-pretraining-beat competitor to GPT-5.6 or Claude Opus 5. Step-2 sits in the upper mid-tier of the open-weight China cohort on text benchmarks, and top-3 on multimodal leaderboards (MMMU, MMBench, MathVista). Stepfun's bet is that for the meaningful slice of the China LLM market that needs a single-endpoint multimodal pipeline plus a cheap reasoning alternative to o1, consolidation wins over a 3-point MMLU uplift. For that slice — domestic multimodal production agents, video understanding pipelines, OCR-heavy document reasoning — Step-2 is the most direct first-party answer.

The other reason Stepfun keeps showing up in 2026 evaluations: the **OpenAI-compatible** API surface means an existing OpenAI SDK-based stack drops into Stepfun with one base URL change. For teams that want API portability without rewriting agent code, that's structural.

## Models: The Stepfun Family (Step-2, Step-2-mini, Step-1, Step-1.5V, Step-R, Step-CC)

Stepfun's current production line is the **Step-2 → Step-2-mini → Step-1 → Step-1.5V** multimodal ladder, plus the **Step-R** reasoning track and the **Step-CC** code-completion endpoint. All chat models are served from the same `https://platform.stepfun.com/v1/chat/completions` endpoint with model selection by name.

### Step-2 — 1.2T multimodal flagship

The largest production model. Accepts text, image, audio and video through a single chat-completions surface. 128K context window. Priced at **¥6 input / ¥18 output per million tokens** (≈$0.83 / $2.50). Step-2 is the right model when multimodal understanding has to be top-of-cohort and you want a single API surface for text + pixels + audio + video. On MMMU and MathVista Step-2 lands top-3 among China open-weight models, and on Chinese-language CV-Bench-QA the smaller Step-1.5V ranked first in early 2026.

### Step-2-mini — fast multimodal

A 200B-parameter fast variant of Step-2. Same multimodal surface (text + image + audio + video) but at 32K context and 5–10× higher throughput. Priced at **¥1 input / ¥3 output per million tokens** (≈$0.14 / $0.42). Step-2-mini is the right model for high-volume multimodal agents, image classification at scale, and any workload that needs multimodal grounding but doesn't need the full Step-2 quality uplift.

### Step-1 — prior flagship, 300B multimodal

The previous-generation flagship. Text + image multimodal, 32K context. Priced at **¥4 input / ¥12 output per million tokens** (≈$0.56 / $1.67). Step-1 remains in production for callers that want a stable, well-documented multimodal endpoint — the model has been in GA long enough that edge cases are well understood.

### Step-1.5V — vision-tuned

The dedicated vision model, 200B parameters. Priced at **¥3 input / ¥9 output per million tokens** (≈$0.42 / $1.25). For OCR-heavy document reasoning, dense image understanding, and pure-vision workloads, Step-1.5V is the right pick — it ranked first on Chinese-language CV-Bench-QA in early 2026.

### Step-R — o1 / R1-class reasoning

Stepfun's answer to OpenAI o1 and DeepSeek R1, with chain-of-thought exposed through the standard streaming interface. 64K context. Priced at **¥8 input / ¥24 output per million tokens** (≈$1.11 / $3.33). On MATH-500 and HumanEval Step-R is competitive with DeepSeek R1, at roughly 1/5 the price of OpenAI o1 and 2× the price of R1. The key differentiator: when Step-R is paired with Step-2 in series, multimodal context (image + video) survives the reasoning pass — the planner takes in the multimodal input, the reasoner reasons over the structured representation.

### Step-CC — code completion

A first-party code completion endpoint at **¥1 / ¥2 per million tokens** (≈$0.14 / $0.28). IDE-friendly: low-latency inline suggestions with per-token streaming. Step-CC is the right pick for inline IDE completions where latency dominates over reasoning depth.

### Step-Embed — embedding (1024-d)

A 1024-dim text embedding model at 8K context, used as the retrieval side of multimodal RAG pipelines. Pairs naturally with Step-2 for end-to-end multimodal RAG.

## Pricing (verified 2026-08-05)

Token rates are in CNY per million tokens. Stepfun is pay-as-you-go from the first production request after the 30-day free window expires.

| Model | Input (¥/M) | Output (¥/M) | USD equiv. | Notes |
|---|---|---|---|---|
| Step-2 | ¥6 | ¥18 | $0.83 / $2.50 | Trillion-param multimodal flagship |
| Step-2-mini | ¥1 | ¥3 | $0.14 / $0.42 | Fast Step-2 variant, 200B |
| Step-1 | ¥4 | ¥12 | $0.56 / $1.67 | 300B multimodal, prior gen |
| Step-1.5V | ¥3 | ¥9 | $0.42 / $1.25 | Vision-tuned 200B |
| Step-R | ¥8 | ¥24 | $1.11 / $3.33 | Reasoning, o1 / R1 class |
| Step-CC | ¥1 | ¥2 | $0.14 / $0.28 | Code completion |

Compared to the closest US/China alternatives at the August 2026 price point:

- **Step-2 vs OpenAI GPT-5** ($1.25 / $10): Step-2 is 33% cheaper on input, 75% cheaper on output, and direct from China.
- **Step-2 vs Anthropic Claude Sonnet 5** ($3 / $15): Step-2 is 50% cheaper on input, 83% cheaper on output.
- **Step-2 vs DeepSeek V3.2** (¥0.14 / ¥0.28, text-only): Step-2 is 40× more expensive per input token, but it's the only one of these that ships native multimodal on a single endpoint.
- **Step-R vs OpenAI o1** ($15 / $60): Step-R is roughly 1/5 the price.
- **Step-R vs DeepSeek R1** (¥4 / ¥16): Step-R is 2× the price, but with multimodal context inheritance when paired with Step-2.

## OpenAI Python SDK Integration

```python
from openai import OpenAI
client = OpenAI(
    base_url="https://platform.stepfun.com/v1",
    api_key="YOUR_STEPFUN_API_KEY"
)
response = client.chat.completions.create(
    model="step-2",
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": "Summarize this clip."},
            {"type": "video_url", "video_url": {"url": "https://example.com/clip.mp4"}}
        ]}
    ]
)
print(response.choices[0].message.content)
```

The same `base_url` works with any OpenAI-compatible framework adapter (LangChain, LlamaIndex, Vercel AI SDK, etc.). Stepfun also ships a first-party Python SDK with multimodal helpers at `github.com/stepfun-ai` for callers that need streaming token-usage reports, image-aware caching, or the Step-CC completions endpoint.

## Step-R Reasoning: 1/5-Price o1 Alternative

Step-R is the most underrated entry in Stepfun's model lineup. The key number: **¥8 input / ¥24 output per million tokens**. OpenAI o1 charges $15 / $60 — Step-R is roughly 1/5. DeepSeek R1 sits at ¥4 / ¥16 — Step-R is 2× R1 but with notably stronger multimodal grounding.

The differentiator matters when reasoning has to act on multimodal context. The standard production pattern is: use Step-2 as the planner (it can read the image, parse the document, watch the video), and use Step-R as the reasoner (it takes the structured plan + multimodal context and reasons). The chain-of-thought is exposed through the streaming interface, so the trace is inspectable before the final answer.

**Trade-offs.** Step-R is text-only — there's no image/video input on the reasoning model itself. The multimodal context has to come from a planner call. Step-R also has no first-class tool calling, so tool-using agents must wrap it in a planner layer.

## vs DeepSeek V3.2 / Qwen3.5-Max / Kimi K3

| Provider | Flagship | Context | In / Out (per M) | Multimodal | Direct CN |
|---|---|---|---|---|---|
| Stepfun | Step-2 | 128K | ¥6 / ¥18 | ✅ single endpoint | ✅ |
| DeepSeek | V3.2 | 64K | ¥0.14 / ¥0.28 | ❌ text only | ✅ |
| Alibaba Qwen | Qwen3.5-Max | 1M | ¥4 / ¥12 | ✅ separate VL | ✅ |
| Moonshot Kimi | K3 | 1M | ¥2 / ¥20 | ✅ native | ✅ |
| OpenAI | GPT-5 | 128K | $1.25 / $10 | ✅ via GPT-4o | ❌ proxy |

**Step-2's main edge** is the single-endpoint multimodal pipeline. A single chat-completions call handles an arbitrary mix of text/image/audio/video.

**DeepSeek V3.2 wins** on raw price (10× cheaper input tokens) but ships text-only and forces callers to integrate a separate VL API.

**Qwen3.5-Max and Kimi K3 lead** on context window (1M tokens) and are better for code-archive or long-doc RAG.

**OpenAI GPT-5 still leads** on ecosystem maturity and tool calling but is unreachable from mainland China without proxying.

For multimodal production in China, Step-2 is currently the cleanest single-endpoint option in the open-weight cohort.

## Limits to Know

- **128K context** trails Kimi K3 and Qwen3.8-Max (both 1M).
- **International endpoint is Hong Kong only**; US/EU latency higher than domestic.
- **Function calling is beta** — production callers wrap Step-2 in a planner layer for tool routing.
- **No SOC 2 or HIPAA documentation** on the public site — confirm enterprise compliance contractually before deploying patient or financial workloads.
- **Model release cadence is moderate**; some new models stay in beta longer than competing labs.
- **No batch or volume discount** beyond the standard prepaid tiers.

## Verdict

Choose Stepfun when you need first-party multimodal LLM access from mainland China on a single OpenAI-compatible endpoint, or when a 1/5-price substitute for OpenAI o1 / DeepSeek R1 reasoning (Step-R) is the deciding factor.

**Skip Stepfun** if you need a 1M-token context window (Kimi K3, Qwen3.8-Max); text-only at the lowest possible cost (DeepSeek V3.2); frontier US ecosystem maturity with tool calling (OpenAI GPT-5); or a permanent free tier for hobby projects (the 1M-token / 30-day window is the only free path).

The pragmatic recommendation is to write your code against the OpenAI `/v1/chat/completions` contract and pick the underlying provider at deploy time — that way a future migration to OpenAI, Anthropic, Google, or another domestic Chinese provider is a configuration change, not a rewrite.

## Affiliate Disclosure

APIRank does **not** have an affiliate relationship with Stepfun. The FreeModel sidebar mention on this review is an OpenAI-compatible free-tier routing alternative for cross-region production, not an affiliate pitch. Token prices, model lineup and free-tier details were verified from `https://platform.stepfun.com/` and `https://docs.stepfun.com/` on 2026-08-05.

## See Also

- Qwen3.8-Max API review — 1M context + 95B active parameters open-weight flagship
- DeepSeek V3.2 API review — cheapest text-only China LLM at ¥0.14/M
- Kimi K3 API review — 1M context + native multimodal
- OpenAI GPT-5.6 Luna review — 80% permanent price cut, US-side ecosystem
- AI API cost control tools 2026 — Cloudflare AI Gateway, Portkey, LiteLLM compared
- FreeModel aggregator — OpenAI-compatible free-tier routing for hobby projects and prototypes
