# Vercel AI Gateway 2026: Zero-Markup AI Routing for Vercel-Native Apps

_Date: 2026-07-20 | Slug: vercel-ai-gateway-api-review | Locale: en_

# Vercel AI Gateway 2026: The Zero-Markup AI Router Built Into the Vercel Platform

Vercel AI Gateway is the AI-routing layer Vercel shipped to compete with OpenRouter, Cloudflare AI Gateway, Portkey, LiteLLM, and Helicone. Verified July 20, 2026, the pricing model is unusually developer-friendly: **$5/month in free AI Gateway Credits** per team, **zero markup on tokens** (including for BYOK customers), and the same pay-as-you-go rate whether you bring your own key or use Vercel-issued credentials. The gateway is available on every Vercel plan, integrates natively with AI SDK v5/v6, and exposes OpenAI Chat Completions, OpenAI Responses, Anthropic Messages, and OpenResponses APIs out of the box.
This review walks through what Vercel AI Gateway does, the verified 2026 pricing (free tier, paid tier, add-on surcharges), and how it compares to OpenRouter, Cloudflare AI Gateway, Portkey, LiteLLM, and Helicone. The numbers come from the official pricing page at vercel.com/docs/ai-gateway/pricing (last updated June 20, 2026, verified July 20, 2026). If you are evaluating AI Gateway vendors in 2026 and your stack runs on Vercel, this is the reference guide.
## What Vercel AI Gateway does (and what it does not)

Vercel AI Gateway is an AI-routing layer, not a model provider. You keep using your existing OpenAI / Anthropic / Google / xAI / Mistral / Cohere / Groq accounts; Vercel sits between your application and the upstream provider as a transparent proxy that handles authentication, billing, fallbacks, and observability. The core capabilities are:
- One API key, hundreds of models. A single Vercel-issued API key routes to hundreds of models across all major providers.
- Unified API. Switch between providers and models by changing one string in your request — minimal code changes between GPT-4o, Claude Opus 4.8, Gemini 2.5 Pro, and Llama 3.5 405B.
- High reliability. Automatic retries to other providers when one fails (model fallbacks), with configurable provider timeouts.
- Embeddings support. First-class embeddings, reranking (Cohere Rerank), speech-to-text, text-to-speech, image generation, and video generation (Beta).
- Spend monitoring. Per-request observability with cost attribution, latency tracking, and usage metrics across providers.
- No markup on tokens. Tokens cost the same as they would from the provider directly — including for BYOK customers — so the gateway never inflates your bill.
- Native AI SDK v5/v6 integration. One-line swap in any Next.js / Vercel-deployed app; the AI SDK is what most Vercel customers already use.
Vercel AI Gateway does not train or fine-tune models, does not host its own base models (unlike Cloudflare Workers AI), and does not bundle a no-code prompt playground (unlike Portkey's App Portal). The product is tightly focused on routing + observability for the Vercel ecosystem, and that focus is what makes the zero-markup model sustainable.
## Vercel AI Gateway pricing in 2026: $5/mo free, then pay-as-you-go

Vercel AI Gateway's verified July 2026 pricing (source: vercel.com/docs/ai-gateway/pricing, last updated June 20, 2026):TierMonthly creditToken pricingRate limitsBYOK availableFree$5/month per teamProvider list rates, zero markupLower limits per model❌ NoPaidPay-as-you-go via purchased creditsProvider list rates, zero markupCustom limits available✅ Yes (zero markup)
The free tier ships with $5/month in AI Gateway Credits per Vercel team account. Once the team makes its first AI Gateway request, the credits are activated. The free credit is consumed before any paid credits — it does not roll over. The free tier is restricted to a subset of models labeled "Free Tier eligible"; the catalog of every model is browsable in the Vercel dashboard.
Once any team member purchases AI Gateway Credits, the team transitions to the paid tier: the monthly $5 free credit no longer applies, but the paid tier unlocks the full model catalog, higher rate limits, BYOK, and add-on features like Custom Reporting. There is no commitment — credits are pay-as-you-go with optional auto top-up configured in the dashboard.
### Add-on surcharges (paid tier)
Vercel AI Gateway's headline "zero markup" promise applies to tokens. Add-on features have small per-request surcharges deducted from the AI Gateway Credits balance:CapabilityCostAvailabilityCustom Reporting writes$0.075 per 1,000 tag / user ID / quota entity ID writesAll paid tiersCustom Reporting queries$5 per 1,000 queries to the reporting endpointAll paid tiersTeam-wide provider allowlist$0.10 per 1,000 successful requestsPro and EnterpriseTeam-wide zero data retention (ZDR)$0.10 per 1,000 requestsPro and EnterprisePer-request provider filterNo additional costAll plansPer-request zero data retentionNo additional costAll plans
The "per-request" variants of provider filter and ZDR are free; the "team-wide" variants cost $0.10 / 1,000 requests. Most teams do not need team-wide enforcement — per-request providerOptions are sufficient and free. Custom Reporting is opt-in and useful for cost attribution in multi-tenant apps.
### BYOK: bring your own key with zero markup
BYOK is a major differentiator vs Cloudflare AI Gateway, which charges a Workers Paid plan + $0.20/M Gateway requests surcharge on top of provider fees, and vs OpenRouter, which requires you to fund an OpenRouter credit balance even when using your own key. Vercel AI Gateway lets you paste your OpenAI / Anthropic / Google keys into the dashboard, route requests through your credentials, and pay zero markup. If a BYOK request fails, Vercel retries with its own system credentials and charges the fallback usage to your credits balance — a small reliability tax that is still cheaper than Cloudflare's per-request surcharge.
## Vercel AI Gateway vs OpenRouter vs Cloudflare AI Gateway vs Portkey vs LiteLLM vs Helicone

All six products solve the "I need to route LLM calls across providers and see what is happening" problem, but they optimize for different things. The decision matrix below is calibrated for a 50-engineer team already shipping on Vercel:FeatureVercel AI GatewayOpenRouterCloudflare AI GatewayPortkeyLiteLLMHeliconeOpen source❌ Closed❌ Closed❌ Closed❌ Closed✅ MIT✅ Apache-2.0Self-host❌ No❌ No❌ No❌ No✅ Yes✅ YesProvider countHundredsHundreds500+200+100+100+Free tier$5/mo creditsYes (some free models)1M req/mo10K req/moUnlimited (OSS)10K req/moTeam tier pricePay-as-you-goPay-as-you-go$5/mo + usage$49/mo (Hobby)Free (OSS)$79/mo (Pro)Token markupZero markupZero markup on mostZero markup on provider feeMarkup variesFreeFree on BYOKZero markup on BYOKBYOKZero markupNo BYOKNo BYOK (charges apply)BYOK via app configBYOK via YAML configBYOK via env varObservability✅ Built-in✅ Built-in✅ Built-in✅ Full-stack⚠️ Logs only✅ Full-stack HQLModel fallbacks✅ Built-in✅ Built-in⚠️ Manual config✅ Built-in✅ Configurable✅ Built-inImage / video / speech✅ Yes (Beta)✅ Yes⚠️ Limited⚠️ Limited❌ No❌ NoNative framework bindingAI SDK v5/v6OpenAI / Anthropic SDKsOpenAI / Anthropic SDKsOpenAI / Anthropic SDKsPython SDKOpenAI / Anthropic SDKs
Pricing verified 2026-07-20 from each vendor's public pricing page. Vercel AI Gateway $5/mo free + zero markup, OpenRouter free + zero markup on most models, Cloudflare AI Gateway free 1M req/mo + $0.20/M overage, Portkey Hobby $49/mo + usage, LiteLLM free self-host, Helicone Pro $79/mo.
If your stack already runs on Vercel and you want zero markup with the lowest possible setup cost, Vercel AI Gateway is the strongest pick. If you are not on Vercel and need the broadest provider coverage, OpenRouter is the canonical default. If you want managed SaaS with a polished App Portal and guardrails, Portkey is the better choice. If you want full self-hosting with a query language for call analytics, Helicone or LiteLLM wins. Cloudflare AI Gateway is the cheapest pure-proxy option but adds a per-request surcharge that adds up at scale.
## How Vercel AI Gateway works (with code)

The simplest integration is a one-line model-string change in the Vercel AI SDK. The default OpenAI Python SDK works without modification once you swap the base URL:
## Using AI SDK v5 (the Vercel-native path)
```typescript
// app/api/chat/route.ts
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'anthropic/claude-opus-4.8', // Vercel AI Gateway format: provider/model
  prompt: 'What is the capital of France?',
});
// Behind the scenes, Vercel AI Gateway routes to Anthropic,
// applies your BYOK key (or Vercel-issued credential),
// logs the request to the observability dashboard,
// and deducts the cost from your credits balance.
```
For teams not yet on AI SDK v5, the OpenAI Chat Completions and Anthropic Messages compatibility shims let you keep your existing SDK with only the base URL and API key swapped.
## Using the OpenAI Chat Completions compatibility
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ['AI_GATEWAY_API_KEY'],  # Vercel-issued, not OpenAI's
    base_url='https://ai-gateway.vercel.sh/v1',
)

response = client.chat.completions.create(
    model='openai/gpt-4o',  # Vercel AI Gateway format: provider/model
    messages=[{'role': 'user', 'content': 'Hello, GPT-4o via Vercel.'}],
)
print(response.choices[0].message.content)
```
## Using the Anthropic Messages compatibility
```python
from anthropic import Anthropic
import os

client = Anthropic(
    api_key=os.environ['AI_GATEWAY_API_KEY'],
    base_url='https://ai-gateway.vercel.sh',
)

message = client.messages.create(
    model='anthropic/claude-sonnet-4-20250514',
    max_tokens=1024,
    messages=[{'role': 'user', 'content': 'Hello, Claude via Vercel.'}],
)
```
Both SDKs route through the same Vercel AI Gateway, log to the same observability dashboard, and apply the same zero-markup pricing. You can change `model=` to switch providers without changing the SDK or the API key.
## BYOK setup in the dashboard
To bring your own key, navigate to the AI Gateway section in your Vercel dashboard, click "Provider Keys," and paste the API key for each provider you want to use. Vercel encrypts the keys at rest, and any request that uses BYOK is billed at zero markup. If a BYOK request fails (rate limit, network blip, expired key), Vercel retries with system credentials and charges the fallback against your credits balance.
## Model fallbacks for high reliability
For production systems that need to stay online when one provider has an outage, Vercel AI Gateway's `providerOptions` API lets you specify a fallback chain in code:
```typescript
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'anthropic/claude-opus-4.8',
  prompt: 'Summarize Q3 earnings.',
  providerOptions: {
    // If Anthropic fails or times out, try OpenAI
    fallback: ['openai/gpt-4o', 'google/gemini-2.5-pro'],
  },
});
```
Vercel AI Gateway retries the fallback chain automatically with the same prompt and the same observability event. The retry is logged in the dashboard so you can see how often each fallback fires.
## Custom Reporting for cost attribution
For multi-tenant SaaS apps that need per-customer billing breakdowns, Custom Reporting adds tag / user ID / quota entity IDs to requests, which can then be queried through the reporting endpoint:
```typescript
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'openai/gpt-4o',
  prompt: 'Summarize this customer support ticket.',
  providerOptions: {
    gateway: {
      // Each tag / user ID costs $0.075 per 1,000 writes
      userId: 'customer_123',
      tag: 'support-ticket-summary',
    },
  },
});
```
A backend job runs hourly to query the reporting endpoint ($5 / 1,000 queries) and produce per-customer monthly invoices. The Custom Reporting cost is negligible compared to the engineering time it saves vs building your own logging pipeline.
## Real-world use cases

Three patterns where Vercel AI Gateway pays for itself within a month:
- A Next.js app shipping on Vercel with multi-provider routing. The default Vercel-recommended stack is AI SDK v5 + AI Gateway. Drop-in compatibility means switching from OpenAI to Anthropic is a model-string change, not a refactor. For teams that already pay Vercel Pro ($20/mo per seat), the $5/mo free AI Gateway credit is essentially free money.
- A multi-tenant SaaS that needs per-customer LLM cost attribution. Custom Reporting tags every request with the tenant ID and lets you run an hourly SQL query against the reporting endpoint to produce per-customer invoices. Without AI Gateway, this requires either a third-party observability vendor ($79/mo for Helicone Pro or $49/mo for Portkey Hobby) or a custom logging pipeline.
- A production app that needs automatic provider failover. When OpenAI has a regional outage, Vercel AI Gateway's model-fallback chain retries Anthropic or Google with the same prompt. The dashboard shows the fallback rate per provider so you can tune your routing rules.
## Honest limitations

- **Hobby / free tier model coverage is limited.** The free $5/mo credit works only on "Free Tier eligible" models — for the full catalog you need to purchase credits.
- **Closed source, no self-hosting.** Unlike LiteLLM (MIT) and Helicone (Apache-2.0), Vercel AI Gateway runs only as a Vercel-managed SaaS. If your compliance regime requires self-hosting, this is a hard no.
- **No guardrails.** Unlike Portkey (built-in guardrails for content moderation, PII redaction, prompt injection defense), Vercel AI Gateway does not ship safety primitives. You need to pair it with a dedicated guardrail layer if safety is a primary requirement.
- **No prompt versioning or experiments.** Unlike Helicone (prompt experiments with HQL-based A/B dashboards), Vercel AI Gateway focuses on routing + observability, not prompt iteration workflows.
- **Add-on surcharges add up at scale.** Custom Reporting queries at $5 / 1,000 queries can become significant for high-cardinality dashboards. Cache the reporting query results locally to amortize the cost.
- **Vercel-locked ecosystem.** The pricing and free-tier mechanics are tied to the Vercel platform. If your team is not on Vercel, the comparison favors OpenRouter or Portkey more strongly.
## Verdict for API developers

Vercel AI Gateway is the strongest AI Gateway choice for Vercel-native teams in 2026. The $5/month free credit, zero markup on tokens (including BYOK), and one-line AI SDK v5/v6 integration make it the lowest-friction aggregator to add to a Next.js / Vercel-deployed app. If your team is not on Vercel, the comparison is less favorable — OpenRouter's free model selection, Cloudflare AI Gateway's per-request surcharges, and Portkey's polished SaaS experience are all competitive on different axes.
For teams that prioritize zero markup + native framework integration, Vercel AI Gateway is the right pick. For teams that prioritize raw cost control with self-hosting, LiteLLM (free, MIT, OSS) wins. For teams that prioritize guardrails and an App Portal for non-technical API key management, Portkey is the right call. Vercel AI Gateway sits in the middle: zero markup, native Vercel fit, with an add-on surcharges structure that is cheaper than Cloudflare AI Gateway at scale but more expensive than LiteLLM for high-volume workloads.
For a deep-dive comparison of all six AI Gateway options on cost, performance, and feature fit, the FreeModel aggregation layer is a useful neutral benchmark — it routes through the same OpenAI-compatible interface and exposes cost / latency data across multiple vendors without locking you into any one of them.
## Frequently asked questions

What is Vercel AI Gateway used for? Vercel AI Gateway is an AI-routing layer that ships as part of the Vercel platform. It provides a single API key to access hundreds of models from OpenAI, Anthropic, Google, xAI (Grok), Mistral, Cohere, Groq, and others, with built-in observability, cost attribution, model fallbacks, and BYOK support. It is the default AI-routing layer for the AI SDK v5/v6 ecosystem and the recommended choice for Next.js apps deployed on Vercel.

How much does Vercel AI Gateway cost in 2026? Vercel AI Gateway has two tiers. The free tier ships with $5/month in AI Gateway Credits per Vercel team account, restricted to a subset of "Free Tier eligible" models with lower rate limits. The paid tier is pay-as-you-go via purchased AI Gateway Credits, unlocks the full model catalog, supports BYOK with zero markup, and adds access to Custom Reporting, team-wide provider allowlist, and team-wide zero data retention. Add-on surcharges are $0.075 per 1,000 Custom Reporting writes, $5 per 1,000 Custom Reporting queries, $0.10 per 1,000 team-wide provider allowlist requests, and $0.10 per 1,000 team-wide zero data retention requests.

Does Vercel AI Gateway add a markup on tokens? No. The headline pricing promise is "zero markup on tokens" — including when you bring your own key (BYOK). The gateway charges you the provider's list rate for input and output tokens, with no Vercel surcharge. BYOK customers also pay zero markup. If a BYOK request fails, Vercel retries with system credentials and the fallback usage is charged against your credits balance at the same zero-markup rate.

How does Vercel AI Gateway compare to OpenRouter? Vercel AI Gateway and OpenRouter both offer zero markup on tokens. Vercel differentiates on Vercel-native AI SDK v5/v6 integration, BYOK support, and a $5/month free credit (vs OpenRouter's free model selection). OpenRouter differentiates on broader provider coverage (hundreds of providers, including long-tail fine-tuning endpoints), no platform lock-in (works with any framework), and a larger community of pre-built integrations. For Vercel-native teams, Vercel AI Gateway is the lower-friction pick. For non-Vercel teams or teams that need a specific long-tail provider, OpenRouter is the canonical default.

Does Vercel AI Gateway support BYOK (bring your own key)? Yes. Vercel AI Gateway supports BYOK on the paid tier for any provider in its catalog. You paste your OpenAI / Anthropic / Google / xAI / Mistral / Cohere / Groq keys into the AI Gateway section of your Vercel dashboard; Vercel encrypts them at rest and routes requests through your credentials at zero markup. If a BYOK request fails, Vercel retries with system credentials and the fallback usage is charged to your credits balance.

Can I use Vercel AI Gateway from inside China? Yes, with a caveat. Vercel AI Gateway is a managed SaaS running on Vercel's global edge network. From inside mainland China, requests to the gateway go through your existing network path (often via a corporate VPN or proxy). The gateway does not run inside China. For teams that need a gateway inside China, the FreeModel aggregation layer or a self-hosted LiteLLM proxy is a better fit.

## Sources

- Vercel, AI Gateway pricing, last updated 2026-06-20 (verified 2026-07-20): vercel.com/docs/ai-gateway/pricing
- Vercel, AI Gateway overview, verified 2026-07-20: vercel.com/docs/ai-gateway
- OpenRouter, Pricing, 2026-07: openrouter.ai/models
- Cloudflare, AI Gateway pricing, 2026: developers.cloudflare.com/ai-gateway
- Portkey, Pricing, 2026-07: portkey.ai/pricing
- LiteLLM, Repository, 2026-07: github.com/BerriAI/litellm
- Helicone, Pricing, 2026-07-18: helicone.ai/pricing
