# Anyscale API 2026 Review: Ray & Endpoints After Nscale

**Date:** 2026-08-08
**Slug:** anyscale-api-review-2026
**Type:** review + new-provider (adds reviewSections to existing anyscale entry)
**Status:** published

## Article

EN: `src/pages/tutorials/anyscale-api-review-2026.astro`
ZH: `src/pages/zh/tutorials/anyscale-api-review-2026.astro`

Title (EN): Anyscale API 2026: Ray & Endpoints After Nscale (47 chars)
Description (EN): Anyscale API 2026 review: Ray distributed compute, OpenAI-compatible Endpoints, $0.39/M Llama 3.3 inference, the Nscale acquisition and regional access. (152 chars)

## Hot topic / why now

- **Nscale acquires Anyscale** for a reported **$1.65 billion** on **July 30, 2026** — NVIDIA-backed UK neocloud folds Ray + Endpoints into its full-stack AI cloud (Norway, UK, Texas, Portugal data centers). Corroborated by Bloomberg, SiliconANGLE, Reuters, TechCrunch, The New Stack, Latham & Watkins.
- **Anyscale native integration on Microsoft Azure** (June 2, 2026) for sovereign AI + variable API cost control (PR Newswire).
- Anyscale was a **genuine coverage gap**: present in providers.json but had **no reviewSections** and **no review tutorial** — this run adds the 4-section reviewSections (EN+ZH) and the EN+ZH review article.

## Provider entry added/updated

`src/data/providers.json` — `anyscale` entry, position 22 of 76:
- status → `active`
- freeTier → `$100 one-time credit + project starter credits`
- freeTierEN / paidModelEN added
- **4 reviewSections** (EN+ZH):
  1. 💰 Pricing & Plans (table — models + accelerator-hour pricing)
  2. 🔧 API & Developer Experience (list, 7 items — surface, models, Ray, SDKs, deployment, auth, SLA)
  3. 🧠 Ray & the Nscale Acquisition (text, 2 paragraphs)
  4. 🌐 Regional Availability & Latency (text)

## Validation

- providers.json JSON syntax: OK
- reviewSections count: 4 (≥4 required)
- EN title 47 chars (+10 = 57 ≤60) ✓
- EN desc 152 chars (≤155) ✓
- ZH title 48 / ZH desc 105 ✓
- Body `.map()`: 0 (set:html pattern, no esbuild pitfall #10)
- Accident `${`: 0 in body (only canonicalUrl template literals)

## Sources

- anyscale.com/pricing (verified 2026-08-08): $100 credit, pay-as-you-go, compute rates (CPU $0.0135/hr, T4 $0.5682/hr, L4 $0.9542/hr, A10G $1.3635/hr, A100 $4.9591/hr), Hosted + BYOC
- Google News RSS (10+ outlets) for the Nscale $1.65B acquisition
- Existing providers.json anyscale pricing (Llama 3.3 70B $0.39/M, DeepSeek-R1 $1/M, Mixtral 8x22B $0.90/M)

## Deploy

Project: apirank-vip (wrangler pages deploy, --commit-dirty=true)
