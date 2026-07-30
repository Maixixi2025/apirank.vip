# LiteLLM API Review 2026

**Slug:** litellm-api-review
**Date:** 2026-07-15
**Category:** Provider Review
**Provider:** LiteLLM (id: `litellm`, aggregator)

## Verified pricing (live 2026-07-15)

- GitHub stars: 53,599
- Forks: 9,770
- License: MIT (open source core) + Enterprise commercial
- Customers: Netflix, Lemonade, Rocket Money
- Docker pulls: 240M+
- Requests served: 1B+
- OSS: free, self-host, unlimited
- Enterprise: on application (estimated $50K-$500K/year per case studies)
- Website: https://litellm.ai
- Docs: https://docs.litellm.ai

## Brief

LiteLLM is the de facto open-source AI gateway for routing requests across 100+ LLM providers using a single OpenAI-compatible interface. With 53,599 GitHub stars, Y Combinator backing, and production usage at Netflix and Lemonade, it has become the standard tool for platform teams that need to give developers multi-model access while maintaining cost attribution, rate limiting, and observability. The open-source MIT-licensed proxy is free to self-host; an Enterprise tier adds SSO, audit logs, custom SLAs, and air-gapped deployment.

## Article structure

- H1: LiteLLM 2026: The Open-Source AI Gateway That Routes 100+ LLMs Through One API
- H2 (8 sections): What is LiteLLM / Pricing / How the Proxy works / Cost tracking / Fallback / Comparison vs Portkey/Cloudflare/OpenRouter / What's new in 2026 / When NOT to use LiteLLM
- FAQ: 10 Q&A covering use cases, pricing, free tier, China access, OpenAI compat, comparison vs Portkey/OpenRouter/Cloudflare, MCP server, affiliate
- JSON-LD: Article + BreadcrumbList + FAQPage (3 blocks parse cleanly)
- H2 count: 9 (TL;DR section + 8 H2 + FAQ section)
- Affiliate: FreeModel (sidebar CTA, apirank-default for OSS providers without affiliate program)

## Key differentiators vs Portkey/OpenRouter/Cloudflare AI Gateway

- **OSS-first**: MIT-licensed proxy, free, no rate limits
- **Cost attribution**: per-key, per-team, per-org virtual keys
- **MCP server**: Q1 2026, exposes any model as MCP tool
- **Rust core**: Q2 2026, 5-10x throughput improvement (in progress)
- **Guardrails**: PII detection, jailbreak protection, content moderation
- **Fallback + load balancing + traffic mirroring**: production-grade routing

## Files written

- `/root/apirank/src/data/providers.json` — added litellm entry (surgical insertion, 84+/1-)
- `/root/apirank/src/pages/tutorials/litellm-api-review.astro` — EN review (27,581 chars)
- `/root/apirank/src/pages/zh/tutorials/litellm-api-review.astro` — ZH review (19,029 chars, 3-layer import path)
- `/root/apirank/src/pages/index.astro` — EN homepage card inserted (before claude-tokenizer)
- `/root/apirank/src/pages/zh/index.astro` — ZH homepage card inserted
- `/root/apirank/src/pages/tutorials/index.astro` — EN tutorials list entry at top
- `/root/apirank/src/pages/zh/tutorials/index.astro` — ZH tutorials list entry at top