# Dify Add-Provider-and-Review Run — 2026-07-24

## Provider
- **Name:** Dify (dify.ai)
- **ID:** dify
- **Category:** aggregator
- **Position:** #66 in providers.json
- **GitHub:** langgenius/dify — 150,010 stars, 23,638 forks, Apache-style license
- **Parent company:** LangGenius (China-based)

## Pricing (verified 2026-07-24)
- Sandbox free: 200 GPT-4 calls, 5MB vector, 10 docs, 2 workflows, 5,000 API calls/mo
- Professional $59/workplace/mo: 100MB, 100 docs, 50 workflows, 50K triggers
- Team $159/workplace/mo: 500MB, 500 docs, 200 workflows, 500K triggers
- Enterprise custom: SSO, private deploy, commercial license, SLA

## Key Differentiators
- Largest OSS LLM app platform community (150k stars — 10x Flowise)
- Native Chinese + international LLM support in one platform
- Self-hostable with Docker/K8s — China deployment via Alibaba Cloud Computing Nest
- SOC 2/GDPR/ISO 27001 certified
- PartnerStack-based affiliate program at dify.ai/partners

## Article
- **Slug:** dify-api-review
- **EN title:** "Dify 2026: Open-Source LLM App Builder & Platform" (50 chars)
- **ZH title:** "Dify 2026 评测：开源 LLM 应用构建平台与 API" (31 chars)
- **EN description:** 155 chars (at cap)
- **6 FAQ items**, 3 JSON-LD blocks (Article + BreadcrumbList + FAQPage)

## Pre-existing Bug Fixes (daily cron comparison article)
The 2026-07-24 daily article cron created `gpt-5-vs-claude-4-vs-gemini-2026-pricing.astro` (EN + ZH) with:
- Double-brace syntax errors (`{{JSON.stringify()}}` should be `{JSON.stringify()}`)
- Double-brace BaseLayout props (`{{enTitle}}` should be `{enTitle}`)
Both variants fixed to enable successful build.

## Build
- **Total pages:** 454 HTML files
- **Heap fix:** v3 recipe (`NODE_OPTIONS=--max-old-space-size=384 --max-semi-space-size=64`)
- **Build command:** `npx astro build --logLevel error`
- **Build time:** ~15s

## Deploy
- **Method:** `wrangler pages deploy dist --project-name=apirank-vip`
- **Files uploaded:** 444
- **Deployment ID:** 91ce9279
- **Git commit:** `bfc604c`
- **EN URL:** https://apirank.vip/tutorials/dify-api-review/ ✅ live verified
- **ZH URL:** https://apirank.vip/zh/tutorials/dify-api-review/ ✅ live verified
- **EN homepage card:** ✅ live
- **EN/ZH tutorials index:** ✅ live

## State.json
- published_count: 101 → 102
- covered_ids: 26 → 27 (added "dify")
