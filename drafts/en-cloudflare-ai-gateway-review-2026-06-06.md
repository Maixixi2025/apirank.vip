---
title: "Cloudflare AI Gateway Review 2026: Cost Control | APIRank"
description: "Cloudflare AI Gateway review: 100+ models one endpoint, edge caching, June 5 spend limits, Workers AI free tier. Compared to Portkey, LiteLLM, OpenRouter."
slug: "cloudflare-ai-gateway-review"
provider: "cloudflare-ai-gateway"
published: false
date: "2026-06-06"
type: "review"
---

# Cloudflare AI Gateway Review 2026: One Endpoint, 100+ Models, Real Spend Limits

## Introduction: The Gateway Layer for the Multi-Provider Era

By 2026 most production AI applications no longer use a single provider. A typical agent stack might call OpenAI for general reasoning, Anthropic Claude for long-context analysis, Google Gemini for vision, and a local Llama deployment for routing. The flexibility is great. The bill is not — and getting visibility into what each team, customer, or feature is actually spending is harder than the model choice itself.

Cloudflare AI Gateway launched in 2024 as a unified proxy for the major LLM APIs. As of June 2026 it has matured into a serious cost-control platform: 100+ supported models from OpenAI, Anthropic, Google, Mistral, Groq, Hugging Face, and Cloudflare's own Workers AI, with built-in caching, real-time spend limits (added June 5, 2026), per-key rate limiting, and full request/response logging on Cloudflare's edge network. It is not a model — it sits in front of the models you already use.

The pitch is simple: keep using OpenAI, Anthropic, and Google, but route every call through a single endpoint that gives you caching, observability, spend caps, and a fallback chain when one provider is down. The cost is $0 in gateway markup (you still pay upstream), plus a small Cloudflare Workers bill for the routing layer itself.

## What Cloudflare AI Gateway Actually Does

Cloudflare AI Gateway is a managed proxy — a single OpenAI-compatible and Anthropic-compatible endpoint that forwards requests to your chosen upstream provider. The four core features:

**1. Unified endpoint (no code rewrite).** You get a stable URL like `https://gateway.ai.cloudflare.com/v1/<account_id>/openai/completions`. Swap your existing `base_url` and your `openai-python` calls Just Work. The same applies to Anthropic, Google, and other supported vendors — each gets a vendor-specific path.

**2. Edge caching.** Identical prompts cached at the edge for a configurable TTL (default 5 minutes, max 1 day). A repeated system prompt + identical user question returns the cached response with no upstream token cost. For high-volume workloads with prompt reuse (RAG pipelines, agent tool definitions, customer support templates), the cache hit rate can hit 30-50%.

**3. Real-time spend limits (June 5, 2026).** Set a USD budget per Cloudflare account, per team (via Cloudflare Access groups), or per API key. When the budget is hit, the gateway returns HTTP 429 and stops forwarding requests — no surprise overage, no manual token tracking. The limit is enforced within 60 seconds, so it works for runaway-agent scenarios.

**4. Logs and analytics.** Every request is logged with token counts, latency, model, cache hit/miss, cost (in USD), and error reason. The dashboard breaks down spend by provider, model, and time. You can export to R2 or send to a logging provider.

There is no model on the gateway itself. You still need an OpenAI / Anthropic / Google account and API key. The gateway stores those keys in Cloudflare's secrets manager and uses them to forward requests.

## Pricing: No Markup, Just Workers

Cloudflare does not charge a percentage on tokens. You pay upstream providers their normal rates, plus a tiny Cloudflare Workers bill for the routing logic.

| Cost Component | Pricing | When It Applies |
|----------------|---------|-----------------|
| Gateway markup | **$0** | Always — no percentage added |
| Upstream provider tokens | Vendor list price | Per token, as if you called directly |
| Cloudflare Workers requests | $0.30 / million requests | Per request through the gateway |
| Cloudflare Workers CPU | $0.02 / million CPU-ms | Routing logic is cheap (~1-2 ms) |
| Workers free tier | 100,000 requests / day | Enough for small projects |
| Log retention | Free 7 days, paid longer | Logs in Cloudflare dashboard |
| Cache hits | **Free** (no upstream cost) | Only for identical prompts within TTL |

**Realistic cost example:** 1 million API calls / month, 500 input + 200 output tokens average, 80% on OpenAI GPT-4o-mini and 20% on Anthropic Claude 3.5 Sonnet:

- OpenAI portion (800K calls × ~$0.0001 each): ~$80
- Anthropic portion (200K calls × ~$0.0009 each): ~$180
- Cloudflare Workers: 1M requests × $0.30/M = $0.30 + ~$0.20 CPU
- **Total gateway overhead: $0.50/month on a ~$260/month AI bill**

The gateway pays for itself if the edge cache eliminates even 5% of upstream calls. On a typical RAG workload with 30% cache hit rate, the savings are 30% of upstream cost, minus a few cents in Workers fees.

## Real-Time Spend Limits (June 5 Update)

The June 5, 2026 launch added three flavors of spend limit, all enforced in near-real-time:

| Limit Type | Scope | Use Case | Enforcement Latency |
|------------|-------|----------|----------------------|
| **Account-level** | All gateway traffic under your Cloudflare account | Global cap | <60 seconds |
| **Team-level** | Cloudflare Access group / team | Department budgets | <60 seconds |
| **Per-key** | Individual API key issued through the gateway | Customer / project isolation | <60 seconds |

When a limit is hit, the gateway returns HTTP 429 with a JSON body like `{"error": "spend_limit_exceeded", "limit_usd": 100, "current_usd": 100.01}`. Your application can catch this and gracefully degrade (queue the request, switch to a cheaper model, return a friendly error).

The per-key limit is the most useful for B2B SaaS. Each customer gets their own gateway API key, with their own spend cap, with full usage visibility. This is the pattern that previously required custom middleware + a billing database + usage metering — Cloudflare now does it as infrastructure.

## Cache Hit Rate: How To Get The Most From The Gateway

The default cache is conservative. To get real savings:

1. **Longer TTL for stable prompts.** If your system prompt and user template don't change, set TTL to 24 hours. RAG workflows where the document set is stable for a few hours are perfect for this.
2. **Cache by exact prompt hash.** Cloudflare caches by exact prompt match — even a single extra space is a cache miss. If your application generates prompts with timestamps, random IDs, or non-deterministic tool results, those will miss.
3. **Set `cache_key` explicitly for user-customized templates.** For prompts that vary by user but share 95% of the content, use the `cache_key` parameter to override the default hash and reuse cached responses for similar-but-not-identical prompts (the prompt prefix is cached separately from the user input).
4. **Use cache for non-streaming calls only.** Streaming responses cannot be cached because the partial chunks don't reassemble cleanly. If you have a high-volume non-streaming batch use case (summarization, classification, embedding-style work), the cache hit rate can hit 50%+.

A practical pattern: send all your "intent classification" and "guardrail" calls through the gateway with a 1-hour TTL. These are usually short, frequently repeated, and the answer rarely changes.

## Model Support: 100+ And Growing

Cloudflare AI Gateway is a proxy, not a model. The model list is the union of every provider it can route to. As of June 2026:

| Provider | Notable Models | Best For |
|----------|----------------|----------|
| **OpenAI** | gpt-4o, gpt-4o-mini, o1, o3-mini, gpt-3.5-turbo | General reasoning, tool use |
| **Anthropic** | claude-3-5-sonnet, claude-3-haiku, claude-3-opus | Long context, code, analysis |
| **Google** | gemini-1.5-pro, gemini-1.5-flash, gemini-2.0-flash | Vision, long context (1M-2M tokens) |
| **Mistral** | mistral-large, mistral-small, mixtral-8x7b | European alternative, function calling |
| **Groq** | llama-3.1-70b, llama-3.1-8b, mixtral | Speed via Groq LPU |
| **Hugging Face** | Any inference endpoint | Custom / open-source models |
| **Workers AI** | llama, qwen, deepseek-r1-distill | Free inference on Cloudflare's edge |

The Workers AI models are a special case: when you route to a Workers AI model through the gateway, the inference runs on Cloudflare's network and the model itself is free (you only pay Workers request + CPU fees). This is useful for cost-sensitive batch workloads on smaller models (Llama 3.1 8B, Qwen 1.5B, DeepSeek R1 Distill).

## How It Compares To Portkey, LiteLLM, And OpenRouter

| Dimension | Cloudflare AI Gateway | Portkey | LiteLLM | OpenRouter |
|-----------|----------------------|---------|---------|------------|
| **Deployment** | Managed (Cloudflare) | Managed / self-host | Self-host (open source) | Managed |
| **Pricing model** | No markup + Workers | Free tier + usage fees | Free (you pay infra) | Markup on tokens |
| **Edge caching** | ✅ Built-in | ✅ Built-in | ❌ No (add Redis) | ❌ No |
| **Real-time spend limits** | ✅ Per key/team (June 5) | ✅ Per key/team | ⚠️ Custom build | ⚠️ Per-account only |
| **Logs retention** | 7 days free | 30 days free | Self-managed | Unlimited |
| **Self-host option** | ❌ | ✅ | ✅ | ❌ |
| **Models** | 100+ (upstream union) | 200+ | 100+ | 60+ |
| **OpenAI compat** | ✅ | ✅ | ✅ | ✅ |
| **Anthropic compat** | ✅ | ✅ | ✅ | ⚠️ Translate layer |
| **Latency overhead** | 5-20 ms (edge) | 30-80 ms | 5-15 ms | 50-200 ms |
| **Pricing per 1M routed calls** | ~$0.30 | Free tier then varies | Infrastructure cost | Varies by markup |

**Choose Cloudflare AI Gateway when:** you want zero gateway markup, you already use Cloudflare for DNS / Workers / R2, you need edge caching for prompt reuse, and you want managed infrastructure with no self-hosting.

**Choose Portkey when:** you need a self-host option, advanced observability features, or a wider model catalog.

**Choose LiteLLM when:** you want full control, you already have Kubernetes / a server to run it on, and you don't want vendor lock-in.

**Choose OpenRouter when:** you want a single bill for many models with no upstream accounts needed, especially for cost-optimized routing across models you don't have direct contracts with.

## Fallback Chains And Multi-Provider Reliability

One feature that gets overlooked: the gateway can be configured with a fallback chain. If your primary provider returns 429 (rate limited) or 5xx (server error), the gateway automatically retries the next model in the chain. A typical setup:

```
Primary:   OpenAI gpt-4o-mini (cheap default)
Fallback 1: Anthropic claude-3-haiku (similar quality, different vendor)
Fallback 2: Workers AI llama-3.1-8b (free, last resort)
```

If OpenAI is rate-limiting you, the gateway transparently routes to Anthropic. If both fail, Workers AI picks up the slack — completely free, slightly lower quality, but the application stays online. This is the same pattern Vercel AI SDK and OpenAI's "reliability layer" tutorials suggest, but built into the proxy.

## China Access: A Real Limitation

Cloudflare's network is generally blocked or heavily restricted in mainland China. The gateway endpoints (`gateway.ai.cloudflare.com`) are not reliably accessible without a proxy. The dashboard (`dash.cloudflare.com`) is also subject to the same access issues.

For China-based developers, the alternative aggregator pattern is to use a domestic-friendly proxy. [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220), for example, is a China-direct OpenAI-compatible aggregator that handles the upstream routing for you, including DeepSeek and Qwen. It's the inverse trade-off — no Cloudflare ecosystem integration, but you don't need a proxy either.

For teams that need both: route production traffic through Cloudflare AI Gateway (managed, cached, observable) and use a domestic aggregator for any China-based users or China-staging environments.

## Use Cases: When To Use Cloudflare AI Gateway

| Use Case | Recommended? | Why |
|----------|--------------|-----|
| Multi-provider production app | ✅ Best | Single endpoint, fallback chains, observability |
| Cost-controlled B2B SaaS | ✅ Best | Per-customer API keys + per-key spend limits |
| RAG pipeline with stable prompts | ✅ Best | Edge cache cuts upstream cost 30-50% |
| High-volume batch processing | ✅ Best | Cache + Workers AI free tier |
| Single-model single-user app | ⚠️ Overkill | Direct upstream call is simpler |
| Real-time streaming agents | ⚠️ Cache misses | Streaming doesn't benefit from edge cache |
| China-direct access | ❌ No | Cloudflare blocked; use a domestic aggregator |
| Self-hosted on-prem requirement | ❌ No | Use Portkey or LiteLLM instead |

## Pros And Cons

**Pros:**

- ✅ Zero gateway markup — pay upstream list price only
- ✅ Edge caching with 30-50% cost reduction on prompt reuse
- ✅ Real-time spend limits per key, team, or account (June 5 launch)
- ✅ 100+ models behind one OpenAI/Anthropic-compatible endpoint
- ✅ Cloudflare reliability + edge network (sub-20 ms routing overhead)
- ✅ Free Workers AI models for cost-sensitive workloads
- ✅ Built-in logging, 7-day free retention, export to R2
- ✅ Fallback chains for multi-provider reliability

**Cons:**

- ⚠️ Not a model — you still need upstream accounts and API keys
- ⚠️ China access requires a stable proxy
- ⚠️ Streaming responses cannot be cached
- ⚠️ Default cache TTL is conservative; needs tuning
- ⚠️ Workers usage billed separately (small but real)
- ⚠️ Logs only free for 7 days; longer retention is paid

## FAQ

**Q: Is Cloudflare AI Gateway a model provider, or just a proxy?**

A: It's a proxy. You bring your own OpenAI, Anthropic, Google, and other upstream API keys. The gateway routes requests to those providers and adds caching, observability, and spend limits. The Workers AI models are an exception — those are free on Cloudflare's network — but for the major providers, you still need direct accounts.

**Q: How much does Cloudflare AI Gateway cost compared to calling OpenAI directly?**

A: For the model itself, $0 extra — you pay OpenAI / Anthropic / Google their normal rates. The only added cost is Cloudflare Workers fees: about $0.30 per million routed requests plus a few dollars in CPU time for typical workloads. On a $1,000/month AI bill, the gateway adds roughly $1-3. The savings from edge caching and per-key spend limits almost always exceed that overhead.

**Q: What happens if I hit my spend limit?**

A: The gateway returns HTTP 429 with a JSON body indicating the spend limit was reached. Your application code can catch this and decide what to do — return an error to the user, queue the request, or fall back to a cheaper model. The limit is enforced within 60 seconds of when the spend is actually incurred, so it's near-real-time.

**Q: Can I use this with the OpenAI Python SDK and Anthropic SDK as-is?**

A: Yes. Set `base_url` to the gateway URL and pass your gateway-issued API key instead of the upstream key. The SDK requests work without code changes. The same pattern works for the Anthropic SDK, Google GenAI SDK, and most OpenAI-compatible clients.

**Q: Does the gateway support streaming responses?**

A: Yes, streaming works — the gateway passes through the SSE stream. However, streaming responses cannot be cached (partial chunks don't reassemble cleanly). For high-volume non-streaming batch workloads the cache shines; for real-time chat / agent loops, you get routing and observability but not cache savings.

**Q: Is there a self-hosted version?**

A: No. Cloudflare AI Gateway is a managed Cloudflare product. If you need self-hosted, the alternatives are Portkey (self-host or managed) and LiteLLM (open source, self-host).

**Q: How does it compare to OpenRouter?**

A: OpenRouter is also a managed aggregator, but it bundles upstream markups and resells the tokens with its own pricing. Cloudflare AI Gateway is a true pass-through proxy: no markup, you bring your own upstream accounts, and the gateway just adds caching, limits, and observability. OpenRouter is simpler (one bill, no upstream accounts needed); Cloudflare is cheaper at scale (no markup, more cache savings).

**Q: Is the June 5 spend-limit feature free?**

A: Yes, real-time spend limits are included with the gateway at no additional cost. You set the limits in the Cloudflare dashboard or via the API, and enforcement is automatic.

## Conclusion: The Cost-Control Layer For Multi-Provider AI Apps

Cloudflare AI Gateway is not a model and not a replacement for OpenAI / Anthropic / Google. It's a routing and observability layer that sits in front of those providers, adds caching, spend limits, and logs, and charges near-zero overhead for the privilege. For any team running multi-provider AI applications at scale, the gateway is worth evaluating for the edge cache alone — 30-50% upstream cost reduction is hard to ignore.

The June 5, 2026 launch of real-time spend limits is the missing piece. Before this update, you could log and observe spend, but couldn't cap it without a custom middleware layer. Now, per-key limits give B2B SaaS a turnkey way to charge customers or departments for their AI usage without building metering infrastructure.

If you're running a multi-vendor AI app, start with Cloudflare AI Gateway as a pass-through proxy. You'll save on caching, get observability for free, and gain the option to add per-key spend limits the moment you need them. For single-model or single-vendor use cases, the gateway is overkill — call the provider directly. For China-direct multi-vendor access, the equivalent role is played by domestic aggregators like [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220), which combine the same multi-model routing with China network access.

---

## Further Reading

- [Cloudflare AI Gateway documentation](https://developers.cloudflare.com/ai-gateway/)
- [Cloudflare blog: AI Gateway spend limits (June 5, 2026)](https://blog.cloudflare.com/ai-gateway-spend-limits/)
- [Cloudflare AI Gateway pricing](https://developers.cloudflare.com/ai-gateway/pricing/)
- [Workers AI model catalog](https://developers.cloudflare.com/workers-ai/models/)
- [Portkey gateway (managed self-host alternative)](https://portkey.ai/)
- [LiteLLM (open source self-host alternative)](https://github.com/BerriAI/litellm)
- [FreeModel (China-direct aggregator, for users needing mainland access)](https://freemodel.dev/invite/FRE-7a3b6220)
