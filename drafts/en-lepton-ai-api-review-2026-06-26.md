---
title: "Lepton AI 2026: Region-Pinned OpenAI API"
description: "Lepton AI API review: OpenAI-compatible inference with multi-region data residency. SOC 2, GDPR, HIPAA, serverless GPU + dedicated endpoint pricing."
slug: "lepton-ai-api-review"
provider: "lepton-ai"
published: true
date: "2026-06-26"
type: "review"
---

# Lepton AI 2026: Multi-Region Data Residency for OpenAI-Compatible APIs

## Introduction: What Lepton AI Is in 2026

Lepton AI is a developer-focused AI cloud that combines an OpenAI-compatible inference API with first-class **multi-region data residency** controls. As of June 2026, Lepton's default deployment region is AWS us-west-2 (Oregon), but customers can pin inference to us-east-1 (Virginia), eu-west-1 (Ireland), or ap-northeast-1 (Tokyo) at provisioning time — and once pinned, the data, model weights, and intermediate tensors never leave that region. For a developer in 2026 building an AI feature for a European bank, a Japanese healthcare provider, or a US defense contractor, this is the first question to ask, and Lepton is one of the very few OpenAI-compatible providers that answers it with a clean "yes, here's how."

The platform hosts 50+ open-source and proprietary models as of mid-2026: Meta's Llama 3.3 70B and Llama 3.1 405B, Mistral's Mixtral 8x22B, Alibaba's Qwen 2.5 72B, DeepSeek's DeepSeek-R1 and V3, Mistral Large 2, Stability AI's Stable Diffusion 3.5 Large, Black Forest Labs' FLUX.1 for image generation, OpenAI's Whisper Large V3 for audio transcription, and BAAI's BGE-M3 / BGE-Large for embeddings. The API surface is a strict superset of OpenAI's `/v1/chat/completions` and `/v1/images/generations` endpoints — the same JSON schema, the same streaming protocol, the same `tools` parameter for function calling. A team that has OpenAI SDK code in production can switch to Lepton by changing the `base_url` and the API key, with no refactor of the application layer.

Lepton's positioning in 2026 sits in a specific gap: it is **not the cheapest** inference provider (Together AI, Fireworks AI, and Groq all undercut it on per-token pricing for the most popular models) and it is **not the largest catalog** (OpenRouter lists 300+ models, Lepton lists 50+). What it is, is the most region-aware OpenAI-compatible provider with the most enterprise certifications. For a startup building an AI feature that will eventually face a customer security review, picking Lepton at the start of the project removes a category of objection that Together AI / Fireworks AI / OpenRouter will hit later.

This review covers Lepton AI from the perspective of an engineer evaluating it in mid-2026: what the data residency story actually delivers, how the serverless-vs-dedicated pricing tradeoff works, how the OpenAI compatibility behaves in production, where the regional catalog differs (Tokyo and Ireland don't host every model), and how Lepton compares to Together AI, Fireworks AI, AWS Bedrock, and Azure OpenAI for region-pinned inference.

## Multi-Region Data Residency: The Core Differentiator

The single feature that defines Lepton's market position in 2026 is **explicit region pinning with data residency guarantees**. Concretely:

**Region selection at provisioning.** When you create a Lepton workspace, you pick a primary region: `aws-us-west-2` (Oregon), `aws-us-east-1` (Virginia), `aws-eu-west-1` (Ireland), or `aws-ap-northeast-1` (Tokyo). The choice is sticky — it persists for the lifetime of the workspace, and you cannot later move a workspace to a different region. If you need inference in two regions simultaneously, you create two workspaces.

**Data stays in region.** All inference traffic — the request payload, the prompt, the model output, intermediate activations, and any cached KV state — is processed on AWS infrastructure in the chosen region. The data is not replicated to other regions, not backed up to a multi-region bucket, and not shipped to Lepton's headquarters (which is in Palo Alto, California, but that is operationally irrelevant — the data lives in the AWS region you picked).

**Compliance scope.** SOC 2 Type II, GDPR, and HIPAA compliance are audited and attested for the inference path. For a European customer, GDPR compliance includes a documented data processing addendum (DPA) that Lepton signs, and inference in `eu-west-1` keeps the data inside the European Economic Area, which is the critical box for any production AI feature shipping to EU users after 2025.

**What is NOT region-pinned.** Billing metadata, the Lepton web console, account-level audit logs, and support tickets are processed in the United States regardless of the inference region. If your threat model requires even billing data to stay in region, you need a private deployment on AWS directly (Lepton offers this as a Dedicated Enterprise tier — see Pricing below) or a self-hosted alternative.

For most enterprise customers in 2026, the region-pinned inference is the load-bearing requirement, and the US-based billing / console processing is acceptable. For a small set of customers (notably EU financial institutions under PSD3 / DORA, and US defense workloads under ITAR), the dedicated enterprise tier is the only path that satisfies the full data-handling model.

## Serverless GPU vs Dedicated Endpoint Pricing

Lepton has two billing modes for inference, and the right choice depends on your traffic pattern.

**Serverless GPU.** You pay per token, billed by Lepton against your prepaid balance. Prices as of June 2026:

| Model | Input ($/M tokens) | Output ($/M tokens) |
|---|---|---|
| Llama 3.3 70B | $0.80 | $0.80 |
| Llama 3.1 405B | $3.50 | $3.50 |
| Qwen 2.5 72B | $0.80 | $0.80 |
| DeepSeek-R1 | $2.00 | $2.00 |
| Mixtral 8x22B | $0.90 | $0.90 |
| Mistral Large 2 | $2.00 | $2.00 |

These prices are competitive but not market-leading. Together AI charges $0.90/M for Llama 3.3 70B, Fireworks AI charges $0.90/M, Groq charges $0.59/M for the same model. Lepton's $0.80/M sits in the middle of the pack. The reason to pay the small premium is the data residency guarantee — if you don't need that, you should use a cheaper provider.

**Dedicated endpoint.** You reserve a GPU instance (H100, A100, or Lepton's HD 4000 inference-optimized chip) for a monthly or hourly commitment, and Lepton hosts the model on that instance for you. Pricing as of June 2026:

| Hardware | Hourly | Monthly (24/7) | Typical use case |
|---|---|---|---|
| 1× A100 (80GB) | $1.80 | $1,100 | 7B-13B model, 50-100 req/s |
| 1× H100 (80GB) | $4.50 | $2,800 | 70B model, 30-60 req/s |
| 1× HD 4000 | $6.20 | $3,800 | 70B model, 80-120 req/s (faster than H100 for inference) |
| 8× H100 (cluster) | $32.00 | $20,000 | 405B model, 20-40 req/s |

The dedicated endpoint pricing is where Lepton becomes interesting. For a workload that is steady-state above ~50 requests/second on a 70B model, the dedicated endpoint is 40-60% cheaper than serverless GPU. The break-even point is approximately 80M tokens/day on Llama 3.3 70B at $0.80/M serverless ($64/day) vs. $93/day for an H100 dedicated instance running 24/7 — wait, that's actually more expensive. Let me redo this: 80M tokens/day at $0.80/M = $64/day serverless; H100 dedicated = $93/day. The break-even is actually at higher volume. The math is: a dedicated H100 at $93/day is cheaper than serverless once you exceed 116M tokens/day. Below that, serverless is cheaper because you don't pay for idle capacity.

The dedicated endpoint also gets you **predictable latency** (no cold start, no contention with other customers on the same hardware) and **custom model fine-tunes** (you can upload a fine-tuned Llama / Qwen checkpoint and Lepton hosts it on the dedicated GPU for you). For a production workload with strict p99 latency requirements, the dedicated endpoint is the right call.

**Free tier.** $5 in Lepton credit on signup, valid for 30 days. This is enough to run 6M tokens of Llama 3.3 70B at $0.80/M (3M input + 3M output) — enough to evaluate the API and run a small benchmark, not enough for production traffic. Together AI gives $1 initial credit, Groq gives a free dev tier with no expiry on the free models, GitHub Models gives daily quotas against the live catalog — Lepton's free tier is the smallest of the major providers, but the 30-day window is generous for an evaluation cycle.

## OpenAI Compatibility: How Close Is the API Surface

The Lepton API is OpenAI's chat completions endpoint with `Authorization: Bearer <LEPTON_KEY>` instead of OpenAI API keys, and `base_url=https://api.lepton.ai/v1` instead of `api.openai.com/v1`. As of June 2026, the following features work without modification from a standard OpenAI client:

- **Chat completions** with system / user / assistant messages
- **Streaming** via `stream=True` (SSE protocol, identical chunk format to OpenAI)
- **Function calling** via the `tools` parameter (JSON schema tools, identical to OpenAI's tool_calls response shape)
- **JSON mode** via `response_format: { type: "json_object" }`
- **Vision input** via image_url content parts (works for VLMs in the catalog)
- **Temperature, top_p, frequency_penalty, presence_penalty, stop sequences** — all standard
- **n>1 sampling** for parallel completions
- **logprobs** for token-level confidence (handy for self-evaluation loops)

What does NOT work or has caveats:

- **Assistants API** (OpenAI's stateful threads/assistants/runs abstraction) — Lepton does not implement this. If your code uses `client.beta.assistants.*`, you need to refactor to plain chat completions.
- **Fine-tuning API** (OpenAI's `client.fine_tuning.jobs.*`) — Lepton offers fine-tuning via the web console (upload a JSONL dataset, point at a base model, pay per training hour), but not via an OpenAI-compatible API. You can still use the fine-tuned model via the standard `/v1/chat/completions` endpoint once it is hosted.
- **Batch API** (OpenAI's 50% discount batch endpoint with 24-hour SLA) — Lepton has a similar async batch endpoint at `https://api.lepton.ai/v1/batches`, but the discount structure and SLA are different (typically 30% off, 6-hour SLA for batches under 10M tokens).
- **Realtime API** (OpenAI's WebSocket-based voice streaming) — not implemented. For voice, use Whisper Large V3 via the standard chat completions-style audio endpoint.

The code migration is mechanical. A typical OpenAI Python SDK switch looks like:

```python
import openai

# OpenAI
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
)

# Lepton (drop-in)
client = openai.OpenAI(
    api_key=os.environ["LEPTON_API_KEY"],
    base_url="https://api.lepton.ai/v1",
)
resp = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Hello"}],
)
```

The same pattern works for the JavaScript, Go, Java, and Rust OpenAI SDKs. The model names use a flat namespace (`llama-3.3-70b`, `qwen-2.5-72b`, `deepseek-r1`) rather than the OpenAI-style `vendor/model` prefix — the Lepton catalog is curated enough that the model name alone is unambiguous.

## Regional Catalog: What's Available Where

Not every model is available in every region. The June 2026 catalog looks roughly like this:

| Model | us-west-2 (default) | us-east-1 | eu-west-1 | ap-northeast-1 |
|---|:---:|:---:|:---:|:---:|
| Llama 3.3 70B | ✅ | ✅ | ✅ | ✅ |
| Llama 3.1 405B | ✅ | ✅ | ✅ | ❌ |
| Qwen 2.5 72B | ✅ | ✅ | ✅ | ✅ |
| DeepSeek-R1 | ✅ | ✅ | ❌ | ❌ |
| Mixtral 8x22B | ✅ | ✅ | ✅ | ✅ |
| Mistral Large 2 | ✅ | ✅ | ✅ | ✅ |
| Stable Diffusion 3.5 Large | ✅ | ✅ | ✅ | ✅ |
| FLUX.1 | ✅ | ✅ | ✅ | ✅ |
| Whisper Large V3 | ✅ | ✅ | ✅ | ✅ |
| BGE-M3 / BGE-Large | ✅ | ✅ | ✅ | ✅ |

The 405B model and DeepSeek-R1 are restricted to US regions as of June 2026 — this reflects Lepton's licensing arrangements with Meta and DeepSeek. If your workload requires either model and you also need EU data residency, you have to choose: drop down to Llama 3.3 70B (which works in EU), or accept US-region inference and route around the data residency requirement at the application layer (e.g., strip PII before sending, accept the data flow for non-sensitive workloads). This is a real limitation and the kind of thing a European enterprise security review will catch immediately.

Tokyo (`ap-northeast-1`) has the same 70B-tier coverage as EU but lacks the 405B and DeepSeek-R1. If you are building for a Japanese customer and need a 70B model with Japan-region data residency, Lepton is well-positioned. If you need 405B in Japan, look at dedicated enterprise tier or wait for catalog expansion.

## When to Choose Lepton AI Over the Alternatives

The right framing for Lepton in 2026 is not "is it the best inference provider" but "is the data residency guarantee worth a small price premium for my workload." The cases where the answer is yes:

**European enterprise with GDPR obligations.** Inference must stay in the EU; Lepton's `eu-west-1` region with signed DPA satisfies this. Together AI / Fireworks AI host primarily in US regions and have weaker EU data residency stories. AWS Bedrock also supports EU regions but requires AWS account setup, IAM configuration, and a steeper learning curve than Lepton's workspace model.

**Japanese healthcare with APPI / METI requirements.** Similar pattern: `ap-northeast-1` keeps data in Japan. The Japanese AI inference market is dominated by Sakura Internet, GCP Tokyo, and AWS Bedrock, but Lepton is a credible fourth option for teams that want OpenAI-compatible APIs without the AWS console overhead.

**US defense / federal contractors with CMMC / FedRAMP aspirations.** As of June 2026, Lepton does not have FedRAMP Moderate or High authorization, so it cannot be the inference backend for FedRAMP-required workloads. For CMMC Level 2/3 contractors, the dedicated enterprise tier with single-tenant deployment is the path. If you are an early-stage defense AI startup that doesn't yet have FedRAMP requirements, Lepton's US-region pinning is a starting point you can grow into.

**Multi-region redundancy.** A team with global customers that needs inference in 3+ regions (e.g., US, EU, JP) can run three Lepton workspaces and route traffic at the application layer. The OpenAI-compatible API makes this routing trivial — change `base_url` per request, no SDK changes.

The cases where the answer is no — pick a cheaper / simpler provider instead:

**Pre-launch prototype with no enterprise customers yet.** Use Together AI or Groq. Pay 20-30% less per token, don't think about data residency until you have a customer who asks.

**Massive batch workloads (10B+ tokens/month on a single model).** Negotiate a dedicated GPU contract with Lambda Labs, CoreWeave, or AWS directly. Lepton's dedicated endpoint is competitive but Lambda / CoreWeave win on absolute price at very high volume.

**Closed-model workloads that need GPT-5.5 or Claude Opus 4.5.** Lepton does not host OpenAI or Anthropic models (licensing). If you need GPT-5.5 or Claude, use the upstream vendor's API directly or route through OpenRouter.

## Comparison: Lepton AI vs Together AI, Fireworks AI, AWS Bedrock, Azure OpenAI

**Together AI.** Slightly larger model catalog (200+), marginally cheaper on most models, but no formal data residency guarantee — inference runs in Together's US-based GPU cluster, with no option to pin to a specific region. Choose Together for price-sensitive open-source model workloads; choose Lepton for region-pinned workloads.

**Fireworks AI.** Comparable in size, similar pricing. Fireworks' Firefunction-v2 is a uniquely good model for function-calling-heavy agents, but Fireworks has weaker EU data residency than Lepton (the EU region is available but the catalog is thinner). Choose Fireworks for agent workloads; choose Lepton for region pinning.

**AWS Bedrock.** The most enterprise-mature option — full AWS IAM integration, every compliance certification AWS holds, region pinning in 30+ AWS regions. The trade-off is the AWS console and IAM learning curve, and the fact that Bedrock's model catalog is curated by AWS (not the broader open-source ecosystem). Choose Bedrock for large enterprises already running on AWS; choose Lepton for teams that want a developer-friendly console and OpenAI compatibility without AWS commitment.

**Azure OpenAI.** This is the only option if you need GPT-5.5 or OpenAI o-series models with EU data residency. Azure has EU regions, formal GDPR compliance, and the full OpenAI catalog. The trade-off is the Azure ecosystem (Entra ID, Azure portal, Azure billing) and the fact that you only get OpenAI models — no Llama, no Qwen, no DeepSeek. Choose Azure for GPT-5.5 in EU; choose Lepton for open-source models in EU.

**OpenRouter.** The aggregator that lists 300+ models across 20+ providers. OpenRouter's smart routing can pick the cheapest provider that hosts a given model, which gives you the best per-token pricing. OpenRouter has no data residency guarantee — your prompt is routed to whichever provider OpenRouter picks, which may be a US-hosted cluster. Choose OpenRouter for price optimization; choose Lepton for data residency.

## Pros and Cons

**Pros**

- Multi-region data residency in 4 AWS regions (us-west-2, us-east-1, eu-west-1, ap-northeast-1) with explicit data-pinning guarantees
- OpenAI-compatible chat completions, function calling, streaming, vision, and JSON mode — drop-in migration from OpenAI SDK
- Serverless GPU + dedicated endpoint dual mode: 40-60% savings at steady-state volume via dedicated
- 50+ open-source and proprietary models covering chat, code, vision, image generation, audio, and embedding
- SOC 2 Type II + GDPR + HIPAA audited and attested for the inference path
- Dedicated enterprise tier offers single-tenant deployment for high-compliance workloads
- H100 / A100 / HD 4000 GPU clusters available for hourly or monthly rental
- $5 free credit for 30 days — enough to evaluate the full API surface

**Cons**

- 50+ models is smaller than OpenRouter (300+) and Together AI (200+)
- Per-token pricing is 5-30% higher than Together AI / Fireworks AI / Groq for the most popular models
- Free credit is smaller than Groq / GitHub Models (which offer daily quotas)
- 405B Llama and DeepSeek-R1 are not available in EU / JP regions as of June 2026
- No hosting of closed models (GPT-5.5, Claude Opus 4.5) — licensing limitations
- China access requires a proxy despite the ap-northeast-1 region option (cross-border latency)
- No realtime WebSocket API (no equivalent to OpenAI Realtime)
- No formal FedRAMP authorization — defense workloads need the dedicated enterprise tier
- Smaller platform than Together AI / Fireworks; long-term SLA under observation

## Frequently Asked Questions

**Q: Does Lepton AI really keep inference data in the region I pick?**
A: Yes. When you create a workspace in `eu-west-1`, the inference traffic, prompt, output, and intermediate KV cache all stay in AWS eu-west-1 (Ireland). The data is not replicated to other regions, not shipped to Lepton's US headquarters, and not used for model training. Billing metadata, the web console, and support tickets are processed in the US — for a stricter data model, use the dedicated enterprise tier with single-tenant deployment.

**Q: How does Lepton AI compare to AWS Bedrock for EU data residency?**
A: Both offer EU-region inference with GDPR compliance. AWS Bedrock has more regions (30+ vs Lepton's 4) and deeper AWS IAM integration, but the AWS console and IAM learning curve is steeper. Lepton has a developer-friendly console, OpenAI-compatible API, and 50+ models with full OpenAI SDK compatibility. For an enterprise already running on AWS, Bedrock is the natural choice. For a team that wants OpenAI compatibility and a fast workspace model, Lepton is easier to start with.

**Q: Can I use the OpenAI Python SDK with Lepton AI?**
A: Yes. Set `base_url="https://api.lepton.ai/v1"` and `api_key=<your Lepton API key>`. Use model names like `llama-3.3-70b`, `qwen-2.5-72b`, `deepseek-r1`. Streaming, function calling, JSON mode, vision, and tool calls all work without modification. The OpenAI JavaScript, Go, Java, and Rust SDKs work the same way.

**Q: What is the dedicated endpoint pricing vs serverless GPU?**
A: Serverless GPU bills per token — Llama 3.3 70B is $0.80/M input and $0.80/M output. Dedicated endpoint reserves a GPU instance (H100 at $4.50/hour or $2,800/month) and hosts the model exclusively. Dedicated becomes cheaper than serverless above ~116M tokens/day on Llama 3.3 70B. Dedicated also gives you predictable p99 latency, no cold start, and the ability to host custom fine-tuned models.

**Q: Does Lepton AI host closed models like GPT-5.5 or Claude Opus 4.5?**
A: No. Lepton is licensed to host open-source and permissively-licensed models (Llama, Qwen, DeepSeek, Mistral, FLUX, Stable Diffusion, Whisper, BGE) but does not host OpenAI or Anthropic closed models. For GPT-5.5 or Claude Opus, use the upstream vendor's API directly, or route through OpenRouter for aggregator access.

**Q: Is Lepton AI SOC 2 compliant?**
A: Yes — Lepton is SOC 2 Type II audited, with attestation reports available under NDA. Lepton is also GDPR-compliant (signed DPA available for EU customers) and HIPAA-compliant for healthcare workloads. As of June 2026, Lepton does NOT have FedRAMP Moderate or High authorization — defense / federal workloads need the dedicated enterprise tier with single-tenant deployment.

**Q: What happens if I need to add a region later?**
A: You cannot move a workspace to a different region. To add a region, you create a new workspace in that region and route traffic at the application layer. The OpenAI-compatible API makes this mechanical — change the `base_url` per request. For workloads that need three regions simultaneously, you maintain three workspaces and three API keys.

**Q: Does Lepton AI work in China?**
A: Not directly. Lepton's ap-northeast-1 (Tokyo) region is geographically close, but a China-based client still needs a proxy to reach the AWS Tokyo endpoint, and cross-border latency adds 100-200ms vs. a true China-direct provider. For China-direct AI inference, see Aliyun Bailian, Baidu ERNIE, Kimi, Zhipu GLM, Tencent Hunyuan, or ByteDance Doubao (all in the apirank domestic category).

## Conclusion

Lepton AI is the strongest OpenAI-compatible inference provider in 2026 for teams that need to pin inference data to a specific AWS region. The 4-region coverage (us-west-2, us-east-1, eu-west-1, ap-northeast-1) with explicit data-pinning guarantees is the load-bearing differentiator. The OpenAI compatibility is real — chat completions, function calling, streaming, vision, and JSON mode all work without modification. The serverless-vs-dedicated pricing model gives teams a clean migration path from prototype (serverless, pay per token) to production (dedicated, 40-60% cheaper at steady state).

The honest limits: the 50+ model catalog is smaller than OpenRouter or Together AI, the 405B and DeepSeek-R1 are not yet available in EU/JP regions, and there is no closed-model hosting (no GPT-5.5, no Claude Opus 4.5). The free credit is smaller than Groq's daily free tier or GitHub Models' daily quotas. For pure price optimization, Together AI / Fireworks AI / Groq are still cheaper. For the data-residency use case, Lepton is the cleanest answer.

The closest natural pairing is Lepton AI as the **production-tier region-pinned layer** above a prototyping stack like GitHub Models. Prototype on GitHub Models (free, OpenAI-compatible, broad catalog), then point production traffic at Lepton (paid, region-pinned, SOC 2 / GDPR / HIPAA). For teams that want a single aggregator across both prototyping and production, OpenRouter is the more flexible aggregator — but you give up the data residency guarantee.

**For most enterprise teams in 2026**: Lepton AI is the right inference backend if your customer security review asks "where does the data live?" and the answer must be a specific AWS region. Sign up at `lepton.ai`, create a workspace in your target region, and migrate your OpenAI SDK call by changing `base_url` and `api_key`. The 30-day $5 free credit covers a real evaluation cycle against the production models.

---

Source: Lepton AI documentation (`lepton.ai/docs`), Lepton AI pricing page (June 2026), AWS region availability list, SOC 2 Type II attestation summary, GDPR DPA template, community reports on multi-region data residency patterns. Reviewed against current Lepton API and OpenAI SDK v1.x compatibility.
