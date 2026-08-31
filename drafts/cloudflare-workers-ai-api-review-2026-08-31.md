---
title: "Cloudflare Workers AI Review 2026: 86-Model Edge GPU Catalog | APIRank"
description: "Cloudflare Workers AI review 2026: 86 models on Cloudflare edge GPUs, 10K Neurons/day free, $0.011/1K Neurons, GLM-5.3 $1.40/$4.40, DeepSeek V4 Pro 1M ctx, OpenAI-compatible API."
slug: "cloudflare-workers-ai-api-review-2026"
provider: "cloudflare-workers-ai"
published: false
date: "2026-08-31"
type: "review"
---

# Cloudflare Workers AI Review 2026: 86-Model Edge GPU Catalog

## What Is Cloudflare Workers AI?

Cloudflare Workers AI is the only major inference platform whose models run on the same edge network that already serves your application code. As of August 2026 the catalog spans **86 models** across text, embedding, image, and audio — including frontier-tier releases like Z.ai GLM-5.3 ($1.40/$4.40 per million tokens, 1M context, released 2026-08-28), DeepSeek V4 Pro ($1.32/$3.96, 1M context, released 2026-08-13), Moonshot Kimi K2.7-code ($0.95/$4.00), and OpenAI GPT-OSS 120B ($0.35/$0.75). Billing is in Cloudflare's own **Neurons** unit at **$0.011 per 1,000 Neurons**, with **10,000 Neurons per day free** on the Workers Free plan and no credit card required.

## 86-Model Catalog (August 2026)

The catalog covers four model families. **Text generation** is the deepest segment, with frontier-tier models (GLM-5.3, DeepSeek V4 Pro, Kimi K2.7-code, GPT-OSS 120B) coexisting with small open-source models (Llama 3.2 1B at $0.027/$0.201 per million tokens, Llama 3.2 3B at $0.051/$0.335) that cost fractions of a cent per call.

| Model | Input ($/M) | Cached ($/M) | Output ($/M) | Tier |
|---|---|---|---|---|
| @cf/zai-org/glm-5.3 | $1.400 | $0.260 | $4.400 | Frontier (paid only) |
| @cf/zai-org/glm-5.3-flash | $0.150 | $0.030 | $0.500 | Frontier (paid only) |
| @cf/deepseek-ai/deepseek-v4-pro-0813 | $1.320 | $0.044 | $3.960 | Frontier (paid only) |
| @cf/deepseek-ai/deepseek-v4-flash-0731 | $0.440 | $0.014 | $1.320 | Frontier (paid only) |
| @cf/moonshotai/kimi-k2.7-code | $0.950 | $0.190 | $4.000 | Frontier (paid only) |
| @cf/openai/gpt-oss-120b | $0.350 | — | $0.750 | Open-weights |
| @cf/meta/llama-3.3-70b-instruct-fp8-fast | $0.293 | — | $2.253 | Open-weights |
| @cf/meta/llama-4-scout-17b-16e-instruct | $0.270 | — | $0.850 | Open-weights |
| @cf/meta/llama-3.2-1b-instruct | $0.027 | — | $0.201 | Free tier OK |

## Pricing in Neurons

Workers AI uses a two-axis pricing model. The base rate is **$0.011 per 1,000 Neurons**, billed after the daily free allowance is exhausted. Each model also publishes a token-equivalent price so you can compare to other inference APIs. The **Free plan** gives you 10,000 Neurons per day, which resets at 00:00 UTC — no credit card required. However, **frontier models are excluded from the Free plan** — to call GLM-5.3, DeepSeek V4 Pro, or Kimi K2.7-code you need Workers Paid ($5/month base subscription) or prepaid AI Gateway credits.

## Calling Workers AI From a Worker

The Workers binding is the recommended path. In your `wrangler.toml` add `[[ai.bindings]] name = "AI"`, then call `env.AI.run("@cf/zai-org/glm-5.3", { messages: [...] })` from inside the Worker. No API key management, no SDK, no separate billing relationship — the binding ties inference to your Cloudflare account's Workers bill.

## Verdict

Cloudflare Workers AI is the rare inference platform whose economics improve as you go more global: edge routing means non-US users get faster responses than US users, the free tier is generous enough to prototype a real product, and frontier-model coverage is competitive with any dedicated provider on price. It is not the right choice for mainland-China-first deployments, and the curated catalog (86 models vs OpenRouter's 400+) means it does not cover every long-tail model. But for the workload shape that matches Cloudflare Workers — short prompts, edge-served, mixed-size models, low operational overhead — Workers AI is the most coherent option on the market in August 2026.

**Best for:** Teams already running on Cloudflare Workers / Pages; global SaaS with non-US-heavy traffic; startups that want frontier models without negotiating multi-region GPU contracts; agent, RAG, and edge inference workloads.
