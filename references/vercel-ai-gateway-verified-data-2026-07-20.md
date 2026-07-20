# Vercel AI Gateway Verified Data — 2026-07-20

## Source URLs (live captured 2026-07-20)
- Main product page: https://vercel.com/docs/ai-gateway
- Pricing page: https://vercel.com/docs/ai-gateway/pricing
- (Models listing returns 404 — `/docs/ai-gateway/supported-models` was moved; models are now browsed via the in-dashboard model picker)
- Last-updated marker on pricing page: "Last updated June 20, 2026"

## Confirmed pricing (2026-07-20)
- **Free tier**: $5/month in AI Gateway Credits per Vercel team account; subset of models eligible; lower rate limits per model
- **Paid tier**: Pay-as-you-go via purchased AI Gateway Credits; ALL available models; custom rate limits; BYOK available
- **Token pricing**: Provider list rates, ZERO markup (both free and paid tiers)
- **Free credit starts** when first AI Gateway request is made
- Once any credit purchase happens, monthly $5 free credit no longer applies
- **BYOK**: Available on paid tier only; if BYOK request fails, gateway retries with system credentials (charged against credits)

### Add-on surcharges (all paid tier)
- **Custom Reporting writes**: $0.075 / 1,000 tag/user ID/quota entity ID writes
- **Custom Reporting queries**: $5 / 1,000 queries to reporting endpoint
- **Team-wide provider allowlist**: $0.10 / 1,000 successful requests (Pro and Enterprise)
- **Team-wide zero data retention (ZDR)**: $0.10 / 1,000 requests (Pro and Enterprise)
- Per-request ZDR / per-request provider filter: NO additional cost

### Auto top-up
- Available in AI Gateway dashboard; auto-purchase when balance drops below threshold

## Capabilities (from main docs page, 2026-07-20)
- **Hundreds of models** accessible via single API key
- Modalities: Text Generation, Image Generation, Video Generation (Beta), Realtime (Beta), Speech-to-Text (Beta), Text-to-Speech (Beta), Embeddings, Reranking
- **Provider support**: OpenAI, Anthropic, Google, Groq, xAI (Grok), Mistral, Cohere, plus image/video/speech providers
- **API compatibility**: AI SDK v5/v6, OpenAI Chat Completions, OpenAI Responses, Anthropic Messages, OpenResponses, Cohere Rerank, Python, REST
- **Reliability**: Automatic retries with other providers on failure (model fallbacks)
- **Budget controls**: API Key Budgets feature
- **Security**: Zero Data Retention (ZDR), Disallow Prompt Training, Provider Allowlist, Model Allowlist
- **Observability**: Spend monitoring, latency, usage metrics, custom reporting with tags/user-IDs

## Editorial angle
Vercel AI Gateway is positioned as a developer-first aggregator competing with **Cloudflare AI Gateway**, **OpenRouter**, **Portkey**, **LiteLLM**, and **Helicone**. Distinct value props:
1. **Zero markup on tokens** (matches OpenRouter's claim; differs from Cloudflare AI Gateway's per-request surcharges)
2. **Free $5/mo tier** for solo devs / hobby projects (matches OpenRouter free model selection; differs from LiteLLM's free self-host and Cloudflare's $5/mo Workers Paid plan)
3. **Native BYOK with zero markup** (rare; Cloudflare charges for BYOK, OpenRouter requires payment)
4. **Vercel-native integration** with AI SDK v5/v6 — single-line swap in any Next.js / Vercel-deployed app
5. **Built-in observability + spend monitoring + API key budgets** — closes gap vs Helicone for teams already on Vercel

## SEO positioning
- Primary keyword: "vercel ai gateway pricing 2026"
- Long-tail: "vercel ai gateway vs openrouter", "vercel ai gateway free tier", "vercel ai gateway byok"
- Affiliate: NONE confirmed for Vercel AI Gateway — Vercel has no public affiliate program. Use **FreeModel** fallback (apirank default).

## Article plan
- Title: "Vercel AI Gateway 2026: Zero-Markup AI Routing for Vercel-Native Apps"
- Category: Provider Review (aggregator)
- Comparison peers: OpenRouter, Cloudflare AI Gateway, Portkey, LiteLLM, Helicone
- Core insight: "$5/mo free + zero markup + BYOK with zero markup" combo is the differentiator
- Sample-code sections: AI SDK v5 with providerOptions, OpenAI Chat Completions compatibility, BYOK setup, fallback routing, custom reporting
