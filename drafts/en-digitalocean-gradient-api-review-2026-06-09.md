---
title: "DigitalOcean Gradient API 2026: H100 Inference + OpenRouter Hookup"
description: "DigitalOcean Gradient AI review: H100/H200 GPU inference from $2.16/hr, serverless endpoints from $0.0005/1K tokens, 14 hosted models, June 3 OpenRouter integration. Compared to RunPod, CoreWeave, SambaNova."
slug: "digitalocean-gradient-api-review"
provider: "digitalocean-gradient"
published: true
date: "2026-06-09"
type: "review"
---

# DigitalOcean Gradient API 2026: H100 Inference for the Rest of Us

## Introduction: Why the OpenRouter Hookup Matters

On June 3, 2026, DigitalOcean quietly became a model provider on OpenRouter. That sentence does not sound like much. DigitalOcean has been a household name for indie developers since the $5/month droplet era, and "model provider" is a phrase that gets thrown around a lot. But the move is more strategic than it looks, because the team that built Gradient is the same team that has spent three years selling $2.16/hour H100s to people who used to pay AWS four times that. Adding OpenRouter as a distribution channel means every OpenRouter user — and OpenRouter processes north of 4 trillion tokens per month at this point — can now route traffic to Gradient's hosted Llama 3.3 70B, Llama 3.1 405B, and DeepSeek V2.5 endpoints without ever creating a DigitalOcean account.

For teams that already use DigitalOcean for their database, object storage, and app server, the Gradient API is a natural extension: same dashboard, same API token, same billing, but now the inference layer lives next to the rest of the stack. For teams that do not use DigitalOcean today, Gradient is worth a second look for three reasons — H100 and H200 GPU access at indie pricing, a serverless inference mode that bills per token instead of per GPU hour, and a Knowledge Base / Agent platform that handles the boring RAG plumbing (vector store, chunking, embedding) in the same UI.

This review walks through the API surface, the pricing, the model catalog, the speed story, the China access situation, and the comparison with the alternatives — RunPod, CoreWeave, SambaNova, Together AI, and the OpenRouter direct model providers.

## What DigitalOcean Gradient Actually Is

Gradient is two products glued together:

1. **GPU Droplets** — the long-standing DigitalOcean virtual machines with H100, H200, L40S, or A100 GPUs attached. You rent the box by the hour, you install vLLM or TGI, and you run inference. This is the boring part, and it is the part most people already know.
2. **Gradient AI Platform** — a serverless inference and agent layer that was relaunched in late 2025. You point the platform at a Hugging Face model (or pick one of the curated 14), and the platform handles GPU autoscaling, batching, and request routing. You pay per token. There is no GPU to manage.

The Knowledge Base and Agent features sit on top of the serverless layer. Knowledge Base is a managed vector store (you upload PDFs / docs, the platform chunks and embeds them), and Agent is a hosted tool-calling runtime that ties the inference endpoint to the Knowledge Base. If you have ever stitched together LangChain, Pinecone, and OpenAI, you can imagine what Gradient is going for.

The June 3 OpenRouter integration is the missing piece. Until this month, using Gradient's hosted models meant going to the DigitalOcean dashboard, generating an API token, and pointing your code at `https://inference.do-ai.run/v1/`. Now you can route any OpenRouter request through DigitalOcean's inference cluster with a model string like `digitalocean/llama-3.3-70b-instruct`. Same model, same price, but you do not have to know DigitalOcean exists.

## Model Catalog: 14 Curated Open-Source Models

Gradient's model list is short and deliberate. Unlike Together AI (200+ models) or Hugging Face (600+), Gradient ships with 14 hand-picked open-source models, all optimized on H100 or L40S hardware:

| Model | Parameters | Hardware | Best For |
|-------|-----------|----------|----------|
| Llama 3.3 70B Instruct | 70B | H100 | General chat, default for production |
| Llama 3.1 405B Instruct | 405B | H100 x4 | Hardest reasoning tasks |
| Llama 3.1 8B Instruct | 8B | L40S | Bulk classification, routing |
| Mistral 7B Instruct | 7B | L40S | Lowest cost, high throughput |
| Mistral Nemo | 12B | L40S | Multilingual, mid-tier |
| Mixtral 8x7B Instruct | 47B (active) | L40S | Cost-effective MoE |
| Qwen 2.5 72B Instruct | 72B | H100 | Strong Chinese and English |
| Qwen 2.5 Coder 32B | 32B | H100 | Code generation |
| DeepSeek V2.5 Chat | 236B (active) | H100 | Reasoning + code |
| DeepSeek Coder V2 | 236B (active) | H100 | Code completion |
| Nous Hermes 2 Mixtral | 47B (active) | L40S | Fine-tuned chat |
| OpenHermes 2.5 | 7B | L40S | Lightweight chat |
| Phi-3 Medium | 14B | L40S | Reasoning, small footprint |
| Whisper Large V3 | 1.5B | L40S | Speech-to-text |

The list is curated. DigitalOcean benchmarks every model on its own eval suite before shipping it, and models that fall below the accuracy threshold get pulled. The 405B Llama model is the headline — it is the only fully-open 405B-class model you can call via OpenRouter right now at sub-second TTFT.

The trade-off is obvious: if you need Anthropic Claude, OpenAI GPT, or Google Gemini, you have to call those providers directly. Gradient is an open-weights host. For closed models, use OpenRouter's other providers.

## API Surface: OpenAI-Compatible, Plus a Native SDK

The serverless inference endpoint follows the OpenAI `/v1/chat/completions` shape. A request that works against `api.openai.com` works against Gradient after swapping the base URL and key:

```python
import openai

client = openai.OpenAI(
    base_url="https://inference.do-ai.run/v1/",
    api_key="YOUR_GRADIENT_API_TOKEN",
)

response = client.chat.completions.create(
    model="llama-3.3-70b-instruct",
    messages=[{"role": "user", "content": "Summarize the OpenRouter integration."}],
)
```

This OpenAI compatibility means LangChain, LlamaIndex, AutoGen, and the OpenAI Python SDK all work against Gradient with zero code changes beyond the base URL.

On top of the OpenAI shape, Gradient exposes:

- **Agent endpoint** (`/v1/agents/{agent_id}/invoke`) — call a hosted agent that already has a Knowledge Base and tool bindings attached.
- **Knowledge Base endpoint** (`/v1/knowledge_bases/{kb_id}/search`) — direct vector search without the LLM in the loop.
- **Embeddings endpoint** (`/v1/embeddings`) — bge-large-en and bge-m3 are the defaults.
- **Speech-to-text endpoint** (`/v1/audio/transcriptions`) — Whisper Large V3.
- **Reranker endpoint** — bge-reranker-v2-m3 for RAG pipelines.

There is also a first-party CLI (`doctl ai`) and a Terraform provider for IaC teams.

## Pricing: GPU Hour vs Per-Token

Gradient's pricing has two layers, and the choice between them is the most important decision a new user will make.

### GPU Droplets (you manage the box)

| GPU | VRAM | Hourly Rate | Monthly (24/7) |
|-----|------|-------------|----------------|
| H200 | 141 GB | $3.20/hr | ~$2,330 |
| H100 | 80 GB | $2.16/hr | ~$1,575 |
| L40S | 48 GB | $1.12/hr | ~$817 |
| A100 | 40 GB | $0.76/hr | ~$554 |
| A100 | 80 GB | $1.10/hr | ~$802 |
| RTX 4000 Ada | 20 GB | $0.50/hr | ~$365 |

At $2.16/hour for an H100, DigitalOcean is roughly 30-50% cheaper than AWS `p5.48xlarge` ($4.10/hr for an H100) and 20% cheaper than RunPod's on-demand H100. The reservation discounts (1-year and 3-year) go further, but only make sense for steady-state inference.

### Serverless Inference (no GPU to manage)

Per-token pricing on Llama 3.1 8B starts at $0.0005 per 1,000 tokens (input and output combined at the smaller model). For the larger models, the per-token rate scales roughly with parameter count:

| Model | Per 1M tokens (input) | Per 1M tokens (output) |
|-------|------------------------|------------------------|
| Llama 3.1 8B | $0.20 | $0.20 |
| Mistral 7B | $0.20 | $0.20 |
| Qwen 2.5 72B | $0.90 | $0.90 |
| Llama 3.3 70B | $0.90 | $0.90 |
| DeepSeek V2.5 | $1.20 | $1.20 |
| Llama 3.1 405B | $3.20 | $3.20 |

Free credits: **$200 valid for 60 days** on signup. That is enough to run roughly 1 billion tokens on Llama 3.3 70B or 10 billion tokens on Llama 3.1 8B. After the credits expire, there is no permanent free tier — the model is paid-only.

For comparison, the same Llama 3.3 70B on SambaNova is $0.30 input / $0.70 output ($1.00 combined) per 1M tokens, and on Groq is $0.59 / $0.79 ($1.38 combined). Gradient at $0.90 combined is competitive but not the cheapest. The cheap-tier crown still goes to OpenRouter's DeepSeek V3 routing at ~$0.50 combined per 1M tokens.

## Speed Benchmarks

From DigitalOcean's published numbers and independent measurements of the serverless endpoints:

- **Llama 3.1 8B**: ~190 tok/s output, TTFT ~180ms (US east, H100)
- **Llama 3.3 70B**: ~75 tok/s output, TTFT ~320ms
- **Llama 3.1 405B**: ~38 tok/s output, TTFT ~480ms
- **Qwen 2.5 72B**: ~70 tok/s output, TTFT ~340ms
- **DeepSeek V2.5 (236B MoE)**: ~52 tok/s output, TTFT ~420ms
- **Mixtral 8x7B**: ~95 tok/s output, TTFT ~260ms

Cold start on the serverless endpoint is the weak point — first request after a quiet period takes 2-3 seconds while the platform provisions an H100. Sustained throughput after warmup is competitive with Groq and SambaNova on the 8B and 70B tiers, and significantly behind Groq on the 405B tier (Groq's 405B hits 60+ tok/s because of the LPU architecture; H100 inference tops out around 40 tok/s regardless of provider).

For agentic workloads that mix small and large models, the recommended pattern is to route classification / routing / parsing calls to Llama 3.1 8B (cheap, fast) and reserve 70B / 405B calls for the actual reasoning step. Gradient's Knowledge Base and Agent features are designed around this split.

## China Access

DigitalOcean's data centers are in New York, San Francisco, Amsterdam, Frankfurt, London, Singapore, and Bangalore. There is no mainland China region, and the dashboard at `cloud.digitalocean.com` is blocked at the network level in many Chinese ISPs.

For Chinese developers:

- **The dashboard** requires a stable proxy. Expect occasional CAPTCHA friction.
- **The API endpoint** (`inference.do-ai.run`) is reachable from inside China at roughly 200-400ms additional latency over the US-direct baseline.
- **OpenRouter routing is the workaround.** Route through OpenRouter's `digitalocean/llama-3.3-70b-instruct` model string, and OpenRouter's existing China-direct edge handles the connectivity. This is the lowest-friction path for Chinese teams as of June 2026.
- **Payment**: DigitalOcean accepts Visa, Mastercard, PayPal, and crypto (BTC, ETH, USDC). Chinese UnionPay cards are not directly supported, but Binance / stablecoin top-up via the crypto path works.

In short: Gradient is a US/EU-hosted platform with no China region, but the OpenRouter integration and crypto payment make it workable for Chinese teams that do not need the dashboard.

## How Gradient Compares to Alternatives

The "AI inference platform" market in 2026 is crowded. Gradient is not the cheapest, the fastest, or the most model-rich. Where it wins is the "boring infrastructure" position: same dashboard as your database, same API token as your Spaces buckets, same Terraform provider as the rest of your stack.

| Provider | Models | Cheapest Tier | China Access | OpenRouter Provider | Notes |
|----------|--------|---------------|--------------|---------------------|-------|
| **DigitalOcean Gradient** | 14 (open only) | $0.0005/1K tok | Proxy / OpenRouter | ✅ (since 6/3) | Indie pricing on H100, full DO ecosystem |
| **SambaNova** | 9 (open only) | $0.10/M tok | Proxy | ❌ | SN40L chip, 1,000+ tok/s on 70B |
| **Together AI** | 200+ (open + closed) | $0.06/M tok | Proxy | ❌ | Highest model count under $1/M |
| **RunPod** | 200+ | $0.40/hr (H100) | Proxy | ❌ | GPU rental focus, less managed |
| **CoreWeave** | 50+ | $2.15/hr (H100) | Proxy | ❌ | Enterprise / NVIDIA partnership |
| **Fireworks AI** | 100+ | $0.20/M tok | Proxy | ❌ | Function calling optimized |
| **Cerebras** | 6 | $0.10/M tok (combo) | Proxy | ❌ | WSE-3 wafer-scale, 2,000+ tok/s |

If the deciding factor is price per token on the smallest model, SambaNova and Cerebras win. If the deciding factor is the broadest model catalog, Together AI wins. If the deciding factor is "I already pay DigitalOcean for the rest of my stack," Gradient is the obvious answer — and the June 3 OpenRouter integration removes the API key friction that used to push teams to elsewhere.

## Who Should Use DigitalOcean Gradient

Gradient is a strong fit for:

- **Existing DigitalOcean customers** who want to add an inference layer without paying a second vendor.
- **Open-source-only teams** that need 70B+ models but do not want to manage their own GPU cluster.
- **Indie developers** who want H100 access without an AWS contract.
- **OpenRouter users** who want a new routing option for Llama 3.x and DeepSeek endpoints.

Gradient is a poor fit for:

- **Closed-model users** — no Claude, no GPT, no Gemini. Use OpenRouter with a closed-model provider.
- **Mainland China developers** who need a domestic endpoint — use SiliconFlow, DeepSeek direct, or Aliyun Bailian.
- **Sub-100ms latency applications** — Gradient's TTFT is competitive but not best-in-class; Groq and Cerebras are faster.
- **Very small models (< 4B)** — Gradient's smallest is 7B, and for sub-7B inference, the GPU Droplet overhead is not worth it.

## FAQ

**Q: Is DigitalOcean Gradient a model provider or just a GPU rental platform?**
A: Both. GPU Droplets are the rental side; the Gradient AI Platform is the serverless inference and agent layer. The June 3 OpenRouter integration makes both accessible through one model name.

**Q: Can I run closed models like GPT-4o or Claude 3.5 on Gradient?**
A: No. Gradient is open-weights only. For closed models, use OpenAI, Anthropic, or route through OpenRouter with a different provider string.

**Q: How much does Llama 3.3 70B cost on Gradient?**
A: $0.90 per 1M tokens combined input + output. For comparison, the same model is $1.00/M on SambaNova and $1.38/M on Groq. Cheaper option for the same model is OpenRouter with a DeepSeek or Mistral provider.

**Q: Is there a free tier?**
A: $200 in credits for 60 days on signup. No permanent free tier. The cheapest paid tier is Llama 3.1 8B at $0.20/M tokens.

**Q: Can I use Gradient from inside China?**
A: The dashboard is blocked, but the API endpoint works at 200-400ms additional latency. For lower latency, route through OpenRouter's `digitalocean/llama-3.3-70b-instruct` model name and use OpenRouter's China-direct edge.

**Q: Does Gradient support function calling / tool use?**
A: Yes, on the chat completions endpoint. The Agent platform also has hosted tool bindings for common patterns (web search, calculator, code execution).

**Q: How does the OpenRouter integration work?**
A: OpenRouter added `digitalocean/` as a model prefix on June 3, 2026. You can route any request to `digitalocean/llama-3.3-70b-instruct`, `digitalocean/llama-3.1-405b-instruct`, and a few other model names. Billing is the same — OpenRouter's 5.5% platform fee applies, but you do not need a separate DigitalOcean account.

**Q: Can I deploy my own private model on Gradient?**
A: Yes, on GPU Droplets with vLLM / TGI / SGLang. The serverless endpoint is restricted to the curated 14-model catalog.

## Conclusion

DigitalOcean Gradient is not the cheapest, the fastest, or the broadest AI inference platform in 2026. But it is the one with the lowest dashboard friction for the existing DigitalOcean customer base, and the June 3 OpenRouter integration opens it up to every OpenRouter user. The $200 free credit covers a serious evaluation. If you are an open-weights developer with a DigitalOcean bill, the next H100 you spin up should probably be a Gradient endpoint.

For closed-model users, sub-100ms latency applications, or mainland China direct access, look elsewhere. For the indie-and-open-source sweet spot, Gradient is now a default option.
