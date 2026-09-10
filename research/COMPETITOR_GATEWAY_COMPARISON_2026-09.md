# Competitor AI Gateway Comparison — verified 2026-09-10

All facts from official pages fetched 2026-09-10. "NOT FOUND" = not stated on official sources.

## 1) Portkey (portkey.ai) — now rebranded "PRISMA AIRS AI Gateway" (Palo Alto Networks)
Source: https://portkey.ai/pricing | docs: https://docs.portkey.ai
(1) Tiers:
- Developer Free Forever: $0. 10K recorded logs/mo (logs-only cap; requests uncapped).
- Production: $49/month. 100K logs/mo; +$9 per extra 100K requests (up to 3M requests, then custom).
- Enterprise: Custom pricing (10M+ logs/mo).
(2) Per-request provider cost override / custom cost / negotiated rate: YES.
- Model Overrides: set custom Input Cost / Output Cost per 1M tokens for any base model.
- Pricing Adjustments: discount/markup MULTIPLIER per Integration (0.8 = 20% off, 1.2 = 20% markup); explicitly for "Negotiated Discounts" + internal cost showback. Via UI + Integrations API (pricing_adjustments). Needs gateway v2.7.0+.
(3) Markup model: pass-through default; OPTIONAL user-set multiplier (markup) for showback; platform = subscription.
(4) Free tier: YES (Developer, free forever).
(5) Self-hostable: YES (OSS host-it-yourself; Enterprise VPC/private; air-gapped no longer offered for new deployments).
(6) Models/providers: 2,300+ LLMs across 35+ providers (Model Catalog); "3000+ models one endpoint"; 57 providers in supported table; "200+ LLMs" (Universal API).

## 2) LiteLLM (litellm.ai)
Sources: https://www.litellm.ai/pricing | https://www.litellm.ai/enterprise | docs.litellm.ai
(1) Tiers:
- Open Source: $0, free forever, self-hosted.
- Enterprise: Custom/annual; priced "by annual gateway request capacity, deployment architecture, and support needs - never per token"; volume discount tiers; 30-day free trial key.
(2) Per-request cost override / custom cost / negotiated rate: YES (most complete).
- Custom LLM Pricing: override input_cost_per_token / output_cost_per_token per model or whole cost map; cost-per-second, per-image, per-audio, reasoning, video/sec.
- Provider Discounts: cost_discount_config % per provider - doc says "useful for negotiated enterprise pricing with providers."
- Fee/Price Margin: cost_margin_config (% e.g. 0.10, or fixed $ e.g. $0.001/req), global or per-provider, for internal chargeback.
- Zero-cost models bypass budget checks; base_model mapping for Azure.
(3) Markup model: pass-through default; optional configurable margin/discount for internal billing.
(4) Free tier: YES (OSS $0 forever).
(5) Self-hostable: YES (core; self-hosted + air-gapped).
(6) Models/providers: 100+ providers (pricing page); 126 provider doc pages; cost map 100+ models.

## 3) Helicone (helicone.ai)
Source: https://www.helicone.ai/pricing | docs.helicone.ai (banner: "Helicone Joins Mintlify")
(1) Tiers:
- Hobby: Free - 10,000 requests/mo, 1 GB storage, 1 seat, 1 org.
- Pro: $79/month (usage-based applies; 7-day trial; unlimited seats).
- Team: $799/month (5 orgs; SOC-2 & HIPAA; dedicated Slack; usage-based; 7-day trial).
- Enterprise: Custom (custom MSA, SAML SSO, on-prem, bulk cloud discounts).
- Discounts: startups 50% off 1st year; students free; OSS companies $100 credit.
(2) Per-request cost override / custom cost / negotiated rate: NOT FOUND. Docs only cover auto-calculation from provider pricing tables + open-source 300+ model cost repo; no cost-override header in header directory.
(3) Markup model: pass-through (no token markup stated); priced by subscription + usage.
(4) Free tier: YES (Hobby 10K req/mo).
(5) Self-hostable: YES (open source github.com/Helicone/helicone; Docker/Kubernetes).
(6) Models/providers: 100+ LLM providers; cost repo 300+ models.

## 4) Vercel AI Gateway (vercel.com/ai-gateway)
Sources: https://vercel.com/ai-gateway | https://vercel.com/docs/ai-gateway/pricing
(1) Tiers:
- Free: $5/month of AI Gateway credits included; free-tier-eligible models only; lower rate limits; BYOK NOT available.
- Paid: pay-as-you-go purchased credits; all models; BYOK available.
- Token pricing: provider list rates, ZERO markup on both tiers.
- Metered add-ons beyond tokens: Reporting writes $0.075/1,000; Reporting queries $5/1,000; Team-wide provider allowlist $0.10/1,000 successful reqs (Pro/Enterprise); Team-wide ZDR $0.10/1,000 reqs (Pro/Enterprise); Traces $0.05/1,000; Trace egress $0.50/1 GB.
- Enterprise invoiced billing: no payment processing fees.
(2) Per-request cost override / custom cost / negotiated rate: NOT FOUND as a user-set custom-cost input. BYOK routes on your own provider contracts/committed spend ("existing commitments flow through"), but no documented manual/override cost field.
(3) Markup model: 0% markup, no platform fee on tokens; BYOK no markup/fee.
(4) Free tier: YES ($5/mo credits).
(5) Self-hostable: NO (managed platform).
(6) Models/providers: "hundreds of models", 200+ models per docs; OpenAI, Anthropic, Google, xAI/SpaceXAI, Bedrock, OSS, etc.

## 5) Bifrost by Maxim (getbifrost.ai -> getmaxim.ai/bifrost)
Source: https://www.getmaxim.ai/bifrost/pricing (md: .../pricing.md)
(1) Tiers:
- OSS: Free forever (self-hosted), $0.
- Enterprise: Custom pricing (contact sales); 14-day Enterprise trial.
- No published $ for Enterprise.
(2) Per-request cost override / custom cost / negotiated rate: NOT FOUND (page covers budgets, rate limits, virtual keys, cost tracking - no custom-cost/override/markup input documented).
(3) Markup model: pass-through (OSS self-hosted BYO keys; Enterprise = license/support, not per-token).
(4) Free tier: YES (OSS free forever).
(5) Self-hostable: YES (OSS Apache 2.0 Docker/K8s/Go binary; Enterprise VPC/on-prem/air-gapped/multi-cloud).
(6) Models/providers: 8+ providers and 1,000+ AI models (pricing page Model Catalog); compatible with OpenAI, Anthropic, LiteLLM, Google GenAI, LangChain, Vercel AI SDK.

## 6) OpenRouter (openrouter.ai)
Sources: https://openrouter.ai/pricing | https://openrouter.ai/docs/faq | /docs/use-cases/byok
(1) Tiers:
- Free: $0 - 25+ free models, 4 free providers, 50 reqs/day, platform fee N/A, free models only.
- Pay-as-you-go: platform fee 5.5% (fee discounts available); 500+ models, 80+ providers; credit card/crypto; BYOK allowance $25,000 of list-price inference/month with no BYOK fee.
- Enterprise: Custom; 5% fee (BYOK) after $200,000 of list-price inference/month with no fees; SSO/SAML, SLAs, invoicing, dedicated limits.
- Crypto payments charged an additional fee (exact % not rendered = NOT FOUND).
(2) Per-request cost override / custom cost / negotiated rate: PARTIAL / NOT FOUND. BYOK uses your own provider keys/accounts, but OpenRouter charges its own 5% fee above the free allowance; no custom cost input.
(3) Markup model: 0% markup on inference ("we pass through provider pricing; no markup on inference pricing; we charge a fee when purchasing credits"); 5.5% fee on credit purchase; 5% BYOK fee above allowance.
(4) Free tier: YES (free plan + 25+ free models, 50 reqs/day).
(5) Self-hostable: NO (managed service).
(6) Models/providers: 500+ models, 80+ providers.

## Quick matrix
| Gateway | Free tier | Paid entry $ | Markup on tokens | Custom/override cost input | Self-host |
|---|---|---|---|---|---|
| Portkey | Yes (Free Forever) | $49/mo (Production) | Pass-through (optional user multiplier) | YES (model override + pricing adjustment multiplier) | Yes |
| LiteLLM | Yes (OSS $0) | Custom (Enterprise) | Pass-through (+optional margin) | YES (custom pricing, discounts, margins) | Yes |
| Helicone | Yes (10K req/mo) | $79/mo (Pro) | Pass-through | NOT FOUND | Yes |
| Vercel AI Gateway | Yes ($5/mo credits) | Pay-as-you-go credits | 0% (no markup/fee) | NOT FOUND | No |
| Bifrost (Maxim) | Yes (OSS) | Custom (Enterprise) | Pass-through | NOT FOUND | Yes |
| OpenRouter | Yes (free models) | Pay-as-you-go (5.5% credit fee) | 0% inference markup; 5.5% credit fee; 5% BYOK fee | NOT FOUND (BYOK only) | No |
