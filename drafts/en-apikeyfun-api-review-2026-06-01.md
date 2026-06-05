---
title: "APIKEY.FUN API Review 2026: One-Stop Claude, GPT & Gemini for China"
description: "Complete review of APIKEY.FUN API reseller: 40+ models (Claude Code, GPT, Gemini, DeepSeek), China-direct access, transparent ¥1=$1 pricing, and how it compares to OpenRouter and FreeModel."
slug: "apikeyfun-api-review"
provider: "apikeyfun"
published: false
date: "2026-06-01"
type: "review"
---

# APIKEY.FUN API Review 2026: One-Stop Claude, GPT & Gemini for China

## Introduction: An API Reseller Built for China

APIKEY.FUN is a Chinese API reseller that wraps Claude, GPT, Gemini, DeepSeek, Qwen, Kimi, Doubao, and Zhipu GLM behind a single OpenAI-compatible endpoint. The pitch is simple: one account, one bill, no proxy, no developer friction.

What makes APIKEY.FUN interesting in 2026 is its focus on Claude Code and OpenAI Codex tool-calling — two of the most popular agentic coding workflows in 2026 — plus a pricing formula that's actually transparent ($1 = ¥7, with a clear group multiplier). For developers in mainland China who need Anthropic or OpenAI models without setting up a proxy, this is a legitimate alternative to OpenRouter and FreeModel.

This review covers APIKEY.FUN's model lineup, pricing structure, China access reality, and how it stacks up against the other major API aggregators.

## APIKEY.FUN Pricing Breakdown

APIKEY.FUN uses a "group" pricing model. Each model belongs to a group with a multiplier. The formula is simple:

`Final price = Official price × Group multiplier ÷ 7`

The ÷7 comes from the $1 = ¥7 exchange assumption — meaning if you recharge in RMB, the resulting USD cost matches what you'd pay at the official provider.

| Group | Models | Typical Multiplier | Example |
|-------|--------|-------------------|---------|
| Group 1 | DeepSeek V3, Qwen, GLM, Kimi, Doubao | 1.0–1.5× | Cheapest tier |
| Group 2 | Claude Sonnet/Haiku, GPT-4o-mini | 1.5–2.0× | Mid tier |
| Group 3 | Claude Opus, GPT-4o, o1, o3 | 2.0–3.0× | Premium tier |
| Group 4 | Gemini 2.5 Pro, specialty models | 1.5–2.5× | Mid-premium |

### How Much Can You Get for ¥100 (≈$14)?

| Use Case | Models | Approximate Volume |
|----------|--------|-------------------|
| DeepSeek V3 chat | Group 1 (1.0×) | ~14M input tokens |
| Qwen 2.5 chat | Group 1 (1.0×) | ~14M input tokens |
| Claude Sonnet coding | Group 2 (1.5×) | ~1.5M input tokens |
| GPT-4o coding | Group 3 (2.0×) | ~700K input tokens |
| Claude Opus agent | Group 3 (2.5×) | ~140K input tokens |

### Free Tier

APIKEY.FUN offers a small signup credit for new users — enough to test the API across multiple models. There's no monthly free quota like OpenRouter's free tier; the signup credit is a one-time allocation that lets you verify connectivity and pricing before committing to a recharge.

## Key Advantages of APIKEY.FUN

- **China-direct access**: No proxy, no VPN. The endpoint resolves from mainland China without any extra setup. Critical for Claude Code and Codex workflows that need stable connectivity.
- **OpenAI-compatible endpoint**: Drop-in replacement for the OpenAI SDK. Most existing code works with just an API base URL change.
- **Claude Code + Codex support**: First-class tool-calling support for the two most popular agentic coding CLIs in 2026. This is the main reason many Chinese developers choose APIKEY.FUN.
- **Transparent pricing formula**: $1 = ¥7 with a public group multiplier. You can calculate the final cost before recharging.
- **Chinese interface + Chinese support**: WeChat-based customer service (Laoye1999eth), Chinese-language dashboard, Chinese billing.
- **40+ models**: All major Chinese and international models under one account — no juggling multiple API keys.

## Limitations to Consider

- **Group multiplier opacity**: The exact multiplier per model is not always published in advance. You may need to recharge a small amount to confirm the final cost on specific models.
- **Less known than OpenRouter**: OpenRouter is the global standard for API aggregation. APIKEY.FUN's English documentation is thinner, and the model catalog updates lag behind OpenRouter by days to weeks.
- **No public pricing page**: There's no canonical "pricing" page you can bookmark. Pricing lives in the dashboard, which is Chinese-first.
- **Recharge friction**: Top-up happens via WeChat transfer (Laoye1999eth) or Alipay, not credit card. International users will find this awkward.
- **Single point of failure**: If APIKEY.FUN has an outage, every model on your account is affected. Diversifying across providers (e.g., APIKEY.FUN + FreeModel + direct OpenAI) is the safer pattern.

## APIKEY.FUN vs OpenRouter vs FreeModel

| Factor | APIKEY.FUN | OpenRouter | FreeModel |
|--------|------------|------------|-----------|
| China access | ✅ Direct | ❌ Proxy required | ✅ Direct |
| Claude Code | ✅ Native | ⚠️ Limited | ✅ Native |
| Codex support | ✅ Native | ⚠️ Limited | ✅ Native |
| Pricing transparency | Medium (group formula) | High (per-model public) | High (per-model public) |
| Payment | WeChat/Alipay | Credit card, crypto | Credit card, Alipay |
| Model count | 40+ | 200+ | 30+ |
| Language | Chinese-first | English-first | Bilingual |
| Reliability | Single region, smaller team | Multi-region, larger team | Multi-region |
| Best for | China developers + Claude Code | International devs, max model choice | China + international, balanced |

## Use Case Recommendations

| Use Case | Recommended | Why |
|----------|------------|-----|
| China-based Claude Code user | APIKEY.FUN | Native tool-calling + no proxy |
| International multi-model research | OpenRouter | 200+ models, transparent pricing |
| China + international mixed | FreeModel | Direct access, bilingual, DeepSeek partnership |
| Anthropic-only workflow | APIKEY.FUN or direct Anthropic | Choose based on CN access needs |
| OpenAI Codex agent | APIKEY.FUN or direct OpenAI | Both work; APIKEY.FUN simpler for CN |

## How to Get Started

1. **Sign up**: Visit apikey.fun and create an account (Chinese phone or email works).
2. **Recharge**: Top up via WeChat (Laoye1999eth) or Alipay. Minimum recharge is typically ¥10–¥50.
3. **Generate API key**: Dashboard → API keys → Create new key.
4. **Configure Claude Code / Codex**: Replace the OpenAI base URL with the APIKEY.FUN endpoint, paste your key, and start coding.
5. **Test spend**: Run a small batch of test calls to confirm the group multiplier for the models you actually use.

## FAQ

**Q: Is APIKEY.FUN the same as OpenRouter?**
A: No — OpenRouter is a global aggregator with 200+ models and English-first documentation. APIKEY.FUN is a China-first reseller with 40+ models, Chinese dashboard, and WeChat-based support. Both expose OpenAI-compatible endpoints.

**Q: Can I use Claude Code with APIKEY.FUN?**
A: Yes — Claude Code is one of the main use cases. Set the OpenAI base URL to APIKEY.FUN's endpoint, use any Claude model, and tool-calling works natively.

**Q: Is APIKEY.FUN cheaper than direct OpenAI/Anthropic?**
A: It depends on the model and group multiplier. For Group 1 models (DeepSeek, Qwen), APIKEY.FUN is at parity with direct pricing. For Group 3 (Claude Opus, GPT-4o), the multiplier makes APIKEY.FUN 1.5–3× more expensive than direct — but it saves the proxy and friction cost.

**Q: Does APIKEY.FUN work outside China?**
A: Yes, the API endpoint is accessible globally. International users will find the Chinese-first dashboard awkward but the API itself works the same.

**Q: Is APIKEY.FUN reliable?**
A: It's a smaller team with a single-region deployment. For mission-critical workloads, run APIKEY.FUN alongside a backup provider (e.g., FreeModel or direct OpenAI) and failover if the primary goes down.

**Q: What's the minimum recharge?**
A: Typically ¥10–¥50 depending on the payment method. There's no monthly subscription — it's pure pay-as-you-go.

## Conclusion

APIKEY.FUN is a pragmatic choice for China-based developers who need Claude Code, Codex, or international models without proxy hassle. The transparent ¥1=$1 formula and WeChat support are real advantages. The tradeoffs are group multiplier opacity and a smaller team than OpenRouter.

If you're building agentic coding workflows from China, APIKEY.FUN is worth a ¥50 test recharge. For pure research or non-China development, OpenRouter remains the better default. If you want a balance between the two — direct access, bilingual, broader model coverage — check out [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220), which is the China-direct partner of DeepSeek's official pricing.

---

## Comparison Table (Final)

| Provider | China Direct | Models | Best For |
|----------|--------------|--------|----------|
| APIKEY.FUN | ✅ | 40+ | Claude Code, China devs |
| OpenRouter | ❌ | 200+ | International, max choice |
| FreeModel | ✅ | 30+ | CN + international, balanced |
| Direct Anthropic | ❌ | Claude only | Enterprise, no proxy ok |
| Direct OpenAI | ❌ | OpenAI only | Enterprise, no proxy ok |
