# Cloudflare AI Gateway Custom Costs — verified fact bundle (2026-09-10)

Primary source: https://developers.cloudflare.com/ai-gateway/configuration/custom-costs/ (dateModified 2026-09-09)
Changelog entry: https://developers.cloudflare.com/changelog/post/2026-09-09-custom-cache-token-costs/ (datetime 2026-09-09)
Changelog index: https://developers.cloudflare.com/ai-gateway/changelog/

## The feature

`cf-aig-custom-cost` — a request header on AI Gateway calls that overrides the default
or public model cost with negotiated/contracted rates. Applied **per request**, not per
account or per key.

Properties (all costs are **per single token**, arbitrary decimal precision — docs:
"There is no limit to the number of decimal places you can include"):

| Property | Meaning |
|---|---|
| `per_token_in` | Cost per input token |
| `per_token_out` | Cost per output token |
| `per_cache_read_token` | Cost per cache-read token (optional) |
| `per_cache_write_token` | Cost per cache-write token (optional) |

Docs example: `cf-aig-custom-cost: {"per_token_in":0.000001,"per_token_out":0.000002,"per_cache_read_token":0.0000001,"per_cache_write_token":0.0000005}`
= $1 / $2 / $0.10 / $0.50 per **million** input / output / cache-read / cache-write tokens.

## The 2026-09-09 change (what's actually new)

The header and the general override mechanism existed before. **The Sep 9, 2026 changelog
entry is titled "AI Gateway custom costs support cache tokens"** — the new part is
`per_cache_read_token` + `per_cache_write_token`.

Cache-token activation rules (verbatim):
- Cache-token pricing is optional. It turns on if you specify **at least one** cache rate.
- If you specify only one cache rate, **the other defaults to `per_token_in`**.
- If you omit both, AI Gateway **ignores cache-token counts** and uses the existing
  input/output calculation.

Double-counting rule (verbatim): "When cache tokens are included in the input count, AI
Gateway **subtracts them before applying `per_token_in`**. When cache tokens are reported
separately, AI Gateway **applies their costs in addition to the input cost**. This prevents
cache tokens from being double-counted."

Worked example from docs: response reports 1,000 input + 600 cache-read + 200 cache-write
+ 100 output → AI Gateway computes `1,000 - 600 - 200 = 200` fresh input tokens, then
applies each custom rate to its own token count.

Cache-hit rule (verbatim): "If a response is served from cache (cache hit), the cost is
always **0**, even if you specified a custom cost. Custom costs only apply when the request
reaches the model provider."

Token requirement: custom costs only apply to requests that **pass tokens in their
response**. Requests without token information get no cost calculated.

Visibility: "Custom costs will appear in the logs with an **underline**, making it easy to
identify when custom pricing has been applied."

## Plan availability and pricing

- **"AI Gateway is available to use on all plans."** No Enterprise gate on Custom costs.
- Core features (dashboard analytics, caching, rate limiting) are **free**.
- Paid: **10 million requests/month included, then +$0.05 per million requests.**
- Persistent logs: Workers Free = 100,000 logs total across all gateways;
  Workers Paid = 10,000,000 logs per gateway.
- Unified Billing: **5% fee on credits purchased**; provider inference pricing passed
  through with no markup.
- Source: https://developers.cloudflare.com/ai-gateway/reference/pricing/

## Model / provider coverage

- Model catalog: **235 models** (source: https://developers.cloudflare.com/ai-gateway/models/,
  updated 2026-08-12).
- The custom-cost docs example targets a **non-Cloudflare provider** (OpenAI endpoint:
  `.../openai/chat/completions`), so the override works across routed providers, not just
  Workers AI.
- Which vendors report cache tokens inclusively vs separately is **not named by Cloudflare**.
  Independent cross-check of vendor API schemas (not asserted by Cloudflare):
  OpenAI reports inclusively (`cached_tokens` nested in `prompt_tokens_details`);
  Anthropic reports separately (`cache_creation_input_tokens` / `cache_read_input_tokens`);
  Google prices context caching separately.

## Cloudflare Workers paid plan (the underlying platform cost)

Source: https://developers.cloudflare.com/workers/platform/pricing/
- $5 USD/month minimum per account
- 10 million requests included/month, +$0.30 per additional million
- 30 million CPU ms included/month, +$0.02 per additional million CPU ms

## Adjacent AI Gateway features (page dateModified dates, NOT verified launch dates)

- Custom Providers (any HTTPS endpoint as a provider): page updated 2026-06-15
- BYOK / Store Keys (Secrets Store-backed key storage): page updated 2026-07-31
- Costs observability page: updated 2026-04-20

## AI Gateway changelog, Aug–Sep 2026 (dates verified)

| Date | Entry |
|---|---|
| 2026-09-09 | AI Gateway custom costs support cache tokens |
| 2026-09-01 | Consolidates monthly usage invoice line items; standardizes model names to `provider/model` |
| 2026-08-19 | 50% off GPT-5.6 Sol through AI Gateway (Unified Billing only, not BYOK; in $2.50 vs $5, out $15 vs $30, cache read $0.25 vs $0.50 per 1M; through 2026-09-18) |
| 2026-08-07 | Workers AI and AI Gateway unify model access and billing |
| 2026-08-05 | User Insights (AI spend tracking / anomaly detection) |
| 2026-08-05 | Identity-aware controls (Cloudflare Access integration, `cf.user_id`, spend limits by user) |

## NOT FOUND (do not assert these)

- Any Cloudflare **blog post** about Custom costs (blog search returned nothing).
- **Original launch date** of the pre-cache-token Custom costs feature.
- Original launch dates for Custom Providers and BYOK.
- An explicit "BYOK is free" sentence (free only by omission from the paid-features list).
- A Cloudflare-authored list of which providers report cache tokens inclusively vs separately.

## Competitor context — see COMPETITOR_GATEWAY_COMPARISON_2026-09.md

Only two of six compared gateways document a user-set per-request/per-model cost override:
**Portkey** (rebranded "PRISMA AIRS AI Gateway", Palo Alto Networks) via Model Overrides +
Pricing Adjustments multiplier, and **LiteLLM** via custom pricing maps +
`cost_discount_config` + `cost_margin_config`. Helicone, Vercel AI Gateway, Bifrost, and
OpenRouter have no documented per-request custom-cost input. OpenAI / Anthropic / Google
expose no gateway-level negotiated-rate override at all — enterprise rates go through
contracts and invoicing.
