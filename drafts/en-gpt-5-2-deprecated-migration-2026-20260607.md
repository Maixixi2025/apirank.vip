---
title: "GPT-5.2 Deprecated 2026: Migration Guide to 5 Alternatives"
description: "GitHub Copilot dropped GPT-5.2 and GPT-5.2-Codex on June 5, 2026. Here is the API migration path: Anthropic Claude 4.6, DeepSeek V4, OpenRouter, FreeModel, and Cerebras compared."
slug: "gpt-5-2-deprecated-migration-2026"
provider: "openai"
published: false
date: "2026-06-07"
type: "comparison"
---

# GPT-5.2 Deprecated 2026: Migration Guide to 5 Alternatives

## Why this matters

On June 5, 2026, GitHub announced that Copilot is dropping GPT-5.2 and GPT-5.2-Codex, retiring the model in stages over an 8-week window. This is not a routine API version bump — it is the first time OpenAI has allowed a major partner to publicly deprecate a flagship model while the API still serves traffic to other customers. The Copilot deprecation is the leading indicator: most OpenAI customers should expect GPT-5.2 to be removed from the general API by Q4 2026.

For developers who shipped GPT-5.2 in production — agent frameworks, code review tools, IDE integrations, CI-side completions — the question is not whether to migrate but to where. The good news: the 2026 market has five viable alternatives that drop in with minimal code change, depending on your use case.

This guide covers what exactly got deprecated, the 8-week Copilot retirement timeline, and a side-by-side comparison of five migration targets: Anthropic Claude Opus 4.6, DeepSeek V4 Chat, OpenRouter (with auto-routing), FreeModel (China-direct OpenAI-compatible aggregator), and Cerebras (speed-priority for batch jobs).

## TL;DR

- **GPT-5.2 and GPT-5.2-Codex are deprecated as of June 5, 2026**, with the Copilot retirement running through August 2026. Direct API access likely ends Q4 2026.
- **For general-purpose code and chat**: switch to **Anthropic Claude Opus 4.6** (similar pricing, longer context) or **DeepSeek V4 Chat** (5x cheaper, comparable quality on most benchmarks).
- **For multi-vendor flexibility**: route through **OpenRouter** (one key, 400+ models) or **FreeModel** (China-direct, OpenAI-compatible, built-in cost controls).
- **For batch / offline / speed-priority**: use **Cerebras** (2,000+ tokens/sec on Llama 3.3 70B).
- **Migration effort**: 1-2 hours per code path if you stay on OpenAI-compatible APIs (Anthropic needs the messages-format conversion, ~50 lines). For FreeModel and OpenRouter, swap the base URL only.

## What got deprecated

Two model IDs are affected:

1. **gpt-5.2** — the general-purpose flagship, released October 2025, with 256K context and the same multimodal support as GPT-4o.
2. **gpt-5.2-codex** — the code-specialized variant, fine-tuned for code generation, completion, and review, used heavily by Copilot and several IDE integrations.

The deprecation applies in three stages:

| Date | Event |
|---|---|
| June 5, 2026 | Deprecation announced. New Copilot signups no longer get GPT-5.2 by default. |
| July 1, 2026 | Existing Copilot users auto-migrate to GPT-5.3 (preview) or Anthropic Claude Opus 4.6. |
| August 1, 2026 | GPT-5.2 removed from Copilot. Direct API access still works but is documented as "legacy". |
| Q4 2026 (expected) | Direct API access removed. gpt-5.2 returns 410 Gone. |

The Copilot deprecation is the visible part. The deeper signal: OpenAI is consolidating around GPT-5.3 (preview as of June 2026) and GPT-5.4 (shipping Q3 2026), and the 5.2 line is being cut to free up capacity for the newer models.

For direct API users — anyone calling `https://api.openai.com/v1/chat/completions` with `model="gpt-5.2"` — the model still works in June 2026, but OpenAI's deprecation policy means you have a 6-month grace window before the endpoint returns errors. Plan the migration now rather than when the API starts failing.

## The 5 Migration Targets

### 1. Anthropic Claude Opus 4.6 (Best for general quality)

The closest replacement in raw quality. Claude Opus 4.6 matches GPT-5.2 on most reasoning benchmarks (within 1-2 points) and exceeds it on long-context tasks. Pricing is similar: $15/$75 per million input/output tokens for Opus 4.6 vs $10/$30 for GPT-5.2, so Opus costs ~2x more on output-heavy workloads.

**Migration friction**: medium. The Anthropic API uses a different message format (`/v1/messages` instead of `/v1/chat/completions`, with separate `system` and `messages` arrays). A direct port needs ~50 lines of conversion code. If you are on a framework like LangChain or LlamaIndex, the swap is one line.

**When to pick this**: high-stakes content generation, long-context document analysis, customer-facing chat where quality matters more than price.

### 2. DeepSeek V4 Chat (Best for cost)

DeepSeek V4 Chat is the cost play. At $0.14/$0.28 per million tokens, it is roughly 70x cheaper than GPT-5.2 on input and 100x cheaper on output, with quality within 5-10% on most coding and reasoning benchmarks. For workloads that are price-sensitive (batch jobs, evaluation pipelines, large-context analysis), the savings are dramatic.

**Migration friction**: low. DeepSeek is OpenAI-compatible at `https://api.deepseek.com/v1`. You can swap the base URL and the API key, change `gpt-5.2` to `deepseek-chat`, and the code works.

**When to pick this**: price-sensitive workloads, China-based deployments (DeepSeek is direct-accessible in China, GPT-5.2 is not), batch jobs and evals.

### 3. OpenRouter (Best for multi-vendor flexibility)

OpenRouter is a router, not a model. It exposes 400+ models from 60+ providers under a single OpenAI-compatible API at `https://openrouter.ai/api/v1`. The killer feature: you can A/B test models without changing code, and OpenRouter's auto-routing can pick the cheapest provider that meets a quality bar.

**Migration friction**: trivial. Swap the base URL to `https://openrouter.ai/api/v1`, swap the API key, change the model string to `anthropic/claude-opus-4.6` or `deepseek/deepseek-chat-v4` or any other model OpenRouter routes. Same OpenAI SDK call shape.

**When to pick this**: products that need to switch models based on user input, A/B testing, fallback chains, multi-vendor setups.

### 4. FreeModel (Best for China + OpenAI-compatible drop-in)

FreeModel is an OpenAI-compatible aggregator that bundles DeepSeek, Qwen, GLM, and other major Chinese and international models behind one endpoint. It is designed for two specific scenarios: (a) China-based developers who need direct access without a proxy, and (b) teams who want OpenAI-compatible endpoints but with built-in cost controls (spend caps, per-team budgets) layered on top.

**Migration friction**: trivial. The endpoint is OpenAI-compatible (`https://api.freemodel.dev/v1`), so the migration is a base URL swap and a model string change. For most code, you change one line and the rest works unchanged.

**When to pick this**: China deployment, multi-model with cost controls, teams that want OpenAI compatibility without vendor lock-in.

### 5. Cerebras (Best for speed-priority batch)

Cerebras is the speed play. Their WSE-3 chip delivers 2,000+ tokens/second on Llama 3.3 70B — roughly 10x faster than OpenAI's GPT-5.2 on a typical prompt. The pricing is $0.60/$0.60 per million tokens for combined input+output, with a 24-hour free tier for new users.

**Migration friction**: medium. Cerebras is OpenAI-compatible at `https://api.cerebras.ai/v1`, but the model selection is limited to Llama, Qwen, and a few other open-source families. If your code is fine-tuned for GPT-5.2's specific output style, the model swap will be visible in some edge cases.

**When to pick this**: batch processing, real-time voice agents, code review pipelines where latency matters, anything where 10x speed is worth the model swap.

## Code: Python Migration Example (OpenAI → DeepSeek)

If you are running code that targets `gpt-5.2` via the OpenAI SDK, the migration to DeepSeek V4 is a four-line change:

```python
# Before (OpenAI direct)
from openai import OpenAI
client = OpenAI(api_key="YOUR_OPENAI_KEY")
response = client.chat.completions.create(
    model="gpt-5.2",
    messages=[{"role": "user", "content": "Write a Python function to compute factorial"}],
)
print(response.choices[0].message.content)

# After (DeepSeek via OpenAI-compatible API)
from openai import OpenAI
client = OpenAI(
    api_key="YOUR_DEEPSEEK_KEY",
    base_url="https://api.deepseek.com/v1",
)
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Write a Python function to compute factorial"}],
)
print(response.choices[0].message.content)
```

That is the entire migration. The OpenAI Python SDK is API-shape-compatible with DeepSeek, so the `chat.completions.create` call, the message format, and the response parsing are identical. You change three things: the API key, the `base_url`, and the model string. The rest of your code (streaming, function calling, tool use, response handling) works unchanged.

## Code: curl Migration Example (OpenAI → OpenRouter)

For HTTP-based clients without the SDK, the OpenAI → OpenRouter migration is a single base URL swap:

```bash
# Before (OpenAI direct)
curl -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_OPENAI_KEY" \
  -d '{"model":"gpt-5.2","messages":[{"role":"user","content":"hi"}]}'

# After (OpenRouter with auto-routing)
curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_OPENROUTER_KEY" \
  -d '{"model":"anthropic/claude-opus-4.6","messages":[{"role":"user","content":"hi"}]}'
```

The model string `anthropic/claude-opus-4.6` is OpenRouter's path-style identifier. The API shape (request body, response body, streaming chunks) is identical to OpenAI's, so the parsing logic in your application code does not need to change. If you want auto-routing, set the model to `openrouter/auto` and OpenRouter picks the cheapest provider that meets your quality threshold per request.

## Comparison Table

| Feature | OpenAI GPT-5.2 (deprecated) | Claude Opus 4.6 | DeepSeek V4 Chat | OpenRouter | FreeModel | Cerebras |
|---|---|---|---|---|---|---|
| **Input $/M tokens** | $10 | $15 | $0.14 | varies | varies | $0.30 |
| **Output $/M tokens** | $30 | $75 | $0.28 | varies | varies | $0.30 |
| **Context window** | 256K | 200K | 128K | model-dependent | model-dependent | 128K |
| **Speed (output tok/s)** | ~80 | ~70 | ~50 | model-dependent | model-dependent | 2,000+ |
| **OpenAI-compatible** | yes (native) | no (different format) | yes | yes | yes | yes |
| **Migration effort** | — | medium (~50 lines) | trivial (4 lines) | trivial (1 line) | trivial (1 line) | trivial (1 line) |
| **China access** | proxy required | proxy required | direct | proxy required | direct | proxy required |
| **Free tier** | $5 new user | $5 new user | $5 new user | $1 new user | yes | 24h free |
| **Best for** | deprecated | quality | cost | flexibility | China + cost control | speed |

## Migration Patterns

### Drop-in (recommended for most teams)

If you are running a single OpenAI integration, the cleanest migration is to pick one of the OpenAI-compatible alternatives and swap the base URL. The four-line change shown above (DeepSeek, FreeModel, Cerebras all use the same pattern) is the minimum-friction path. The downside: you are committing to one provider. If that provider has an outage or price hike, you have to migrate again.

### Route (recommended for production at scale)

For products with 10+ integrations or >$10K/month API spend, the route pattern is worth the extra setup. The idea: build a thin wrapper around the API call that dispatches to the right provider based on the request type. Code review requests go to Claude Opus 4.6 (quality matters), batch evals go to DeepSeek (cost matters), real-time chat goes to Cerebras (latency matters). OpenRouter and FreeModel both expose this routing layer out of the box; roll-your-own is ~100 lines.

### Dual-write (recommended for high-stakes migrations)

If you cannot afford even a single bad response during the cutover, dual-write for 1-2 weeks: send every request to both GPT-5.2 and the new provider, log the outputs, and compare quality on a sample. Once the new provider's outputs match GPT-5.2 on your eval set, switch the production traffic. The cost is 2x during the dual-write window, but the risk of a bad migration is much lower.

## Limitations and Gotchas

**Anthropic format conversion**: the Anthropic API uses a different message format. If you have a complex tool-use setup (especially parallel function calls), expect 1-2 days of porting work. The `messages` array structure is similar, but the `system` prompt handling and the `tools` schema have subtle differences.

**DeepSeek moderation**: DeepSeek V4 Chat does not have the same content moderation as GPT-5.2. If you rely on OpenAI's moderation pipeline (especially for user-generated content), you need to run a separate moderation layer. This is one of the few cases where the OpenAI-specific same-request moderation field actually matters.

**OpenRouter pricing variance**: OpenRouter's per-model pricing tracks the underlying provider but adds a 5% routing fee. For very high-volume workloads, going direct to the provider is cheaper.

**FreeModel model selection**: FreeModel is optimized for DeepSeek and a handful of Chinese open-source models. If you need Claude or GPT specifically, OpenRouter is the better pick. FreeModel's value is in the OpenAI-compatibility + China access + cost controls combination, not in model breadth.

**Cerebras model availability**: Cerebras only hosts a small set of models (Llama 3.3 70B, Qwen 2.5, a few others). If your code is fine-tuned for GPT-5.2's specific output style, the swap will be visible. For batch and latency-critical workloads, the speed wins outweigh the model differences.

## Use Cases

**Migrating a CI-side code reviewer**: pick **Anthropic Claude Opus 4.6**. Code review quality matters, latency budget is generous (5-10s per review), and the 200K context is useful for repository-scale reviews.

**Migrating an agent framework with 20+ LLM call sites**: pick **OpenRouter** for the router pattern, or **FreeModel** if the team is China-based. The 1-line swap at each call site is the minimum-friction migration, and the auto-routing saves money on the long tail of calls.

**Migrating a real-time voice agent**: pick **Cerebras**. The 10x speed improvement is the difference between a natural-sounding conversation and a stilted one. Model differences are mostly invisible in voice.

**Migrating a large-batch eval pipeline**: pick **DeepSeek V4 Chat**. The 70-100x cost reduction is the headline number, and the quality difference on most benchmarks is small enough to not matter for eval scoring.

**Migrating a China-based product**: pick **FreeModel** (direct access) or **DeepSeek** (direct access). Both are OpenAI-compatible and China-direct, which GPT-5.2 is not.

## FAQ

**Q: When does GPT-5.2 stop working on the OpenAI API?**

A: The deprecation was announced June 5, 2026. OpenAI's standard policy is a 6-month deprecation window, so direct API access is expected to end around Q4 2026. The endpoint will return a 410 Gone error once retired.

**Q: Can I just keep using GPT-5.2 until it breaks?**

A: You can, but the cost of unplanned migration is much higher than planned migration. The 6-month window is enough time to do a careful dual-write, eval, and cutover. If you wait until the endpoint starts returning errors, you are doing the migration under pressure.

**Q: Which alternative is closest to GPT-5.2 in quality?**

A: Anthropic Claude Opus 4.6. It matches GPT-5.2 on most reasoning benchmarks and exceeds it on long-context tasks. The output quality difference is small enough that most users do not notice.

**Q: Which alternative is cheapest?**

A: DeepSeek V4 Chat, at roughly 70x cheaper on input and 100x cheaper on output. For price-sensitive workloads, the savings are dramatic.

**Q: Can I use the OpenAI SDK with these alternatives?**

A: Yes, for DeepSeek, OpenRouter, FreeModel, and Cerebras — all four are OpenAI-compatible. Anthropic needs a different SDK (`anthropic` package) or a wrapper.

**Q: What about GPT-5.3 (preview)? Should I just upgrade to that?**

A: If you want to stay on OpenAI, GPT-5.3 is the path forward. The catch: it is in preview as of June 2026, with rate limits and feature gaps. For production workloads that need stability now, migrating to one of the alternatives is the safer bet.

**Q: Is there a drop-in replacement that requires zero code change?**

A: FreeModel and OpenRouter are the closest. Both expose OpenAI-compatible endpoints, so the code change is a base URL swap. If you have a thin wrapper around the OpenAI SDK, the migration is one line.

**Q: What if I am already using a framework like LangChain or LlamaIndex?**

A: The migration is even easier. LangChain has built-in integrations for Claude, DeepSeek, OpenRouter, and Cerebras. Switching the model is one line in the chain definition. LlamaIndex is similar.

## Conclusion

The GPT-5.2 deprecation is the leading indicator of OpenAI's roadmap. The 5.2 line is being cut to free up capacity for GPT-5.3 and GPT-5.4, and most production workloads will need to migrate in the next 6 months. The good news: the 2026 market has five viable alternatives that cover every use case — quality, cost, flexibility, China access, and speed — and three of them (DeepSeek, OpenRouter, FreeModel) are drop-in compatible with the OpenAI SDK.

For teams that want to preserve the OpenAI developer experience while gaining flexibility, [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) is the most pragmatic pick. It exposes an OpenAI-compatible endpoint with built-in cost controls and direct China access, so the migration is a base URL swap and the operational overhead stays low. The free tier covers the migration testing period, and the paid tier is priced below direct OpenAI for most model families.

For teams that want model breadth, OpenRouter's auto-routing is the right answer — one key, 400+ models, and the flexibility to swap providers without code changes. For cost-sensitive workloads, DeepSeek is the headline number. For latency-critical batch jobs, Cerebras is in a class of its own. The choice depends on which axis matters most for your workload, but the migration path is well-trodden at this point.

Plan the migration now. The 6-month deprecation window is a gift — use it for a careful eval, a dual-write, and a clean cutover, rather than a fire drill when the API starts returning 410 errors in Q4.
