---
title: "GPT-5 API Pricing 2026: 5.5 vs 5.4 vs Mini"
description: "GPT-5 API pricing 2026: 5.5 at $5/M, 5.4 at $2.50/M, Mini at $0.15/M. Batch 50% off, cached input tiers, and a real cost comparison."
slug: "gpt-5-api-pricing-2026"
provider: "openai"
published: false
date: "2026-06-10"
type: "comparison"
---

# GPT-5 API Pricing 2026: 5.5 vs 5.4 vs Mini — Real Cost Math

## Why this matters

The GPT-5 family has settled into a three-tier lineup in 2026, and the pricing differences between the tiers are large enough that picking the wrong model for your workload is a 20x cost mistake waiting to happen. GPT-5.5 is the new flagship at $5 per million input tokens, GPT-5.4 sits at the mid-tier at $2.50 per million, and GPT-5 Mini is the budget option at $0.15 per million. On the output side the spread is wider: $15/M, $10/M, and $0.60/M respectively. If you are running the wrong model on a high-volume workload, you are burning cash.

The price story for 2026 is not just the headline rate. There are two compounding levers: the Batch API (50% off everything, async only) and the cached input discount (50% off prompt tokens that hit the 5-minute or 1-hour cache tier). For repetitive workloads — agents that re-read the same system prompt, RAG systems that send the same long document, code review tools that re-parse a repo's source tree — the cached input lever is the difference between a profitable product and a money pit.

This guide is the pricing page we wished we had when picking a model: the real per-token rates for all three tiers, the Batch and cache math, three concrete $100 / $1000 / $10000 budget worked examples, and a decision tree for which model fits which workload. It also covers the China access angle (GPT-5 is not directly accessible, and the OpenAI-compatible aggregator [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) routes the same models from a China-direct endpoint) so you can pick the cheapest delivery path, not just the cheapest model.

## TL;DR

- **GPT-5.5 (flagship)**: $5/M input, $15/M output — best for complex reasoning, long-context synthesis, hardest coding tasks.
- **GPT-5.4 (mid-tier)**: $2.50/M input, $10/M output — best balance for most production workloads, 90% of 5.5 quality at half the price.
- **GPT-5 Mini**: $0.15/M input, $0.60/M output — best for classification, extraction, simple completions, and high-volume agents.
- **Batch API**: 50% off all rates, async delivery within 24 hours. Use for evals, bulk processing, anything that does not need real-time.
- **Cached input**: 50% off (5-min cache) or 25% off (1-hour cache) on prompt tokens that hit cache. For workloads with repeated system prompts or long context, this is the single biggest cost lever.
- **Real budgets**: $100 buys 20M input + 6.67M output tokens on 5.5, 40M input + 10M output on 5.4, 666M input + 166M output on Mini.
- **China access**: OpenAI is proxy-only. [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) routes the GPT-5 lineup from a China-direct OpenAI-compatible endpoint with the same prices.

## The 2026 GPT-5 Lineup

### GPT-5.5 — Flagship ($5/M in, $15/M out)

Released March 2026 as the new top-tier model, GPT-5.5 is the workhorse for the hardest reasoning tasks: 800K context window, native multimodal (text + image + audio), and the strongest scores on coding (SWE-bench), math (MATH), and graduate-level reasoning (GPQA) benchmarks as of June 2026. The price is double the GPT-5.4 rate on both input and output, so the rule is simple: use 5.5 only when the cheaper tiers are measurably failing your eval.

The real sweet spot for 5.5 is long-context synthesis. If you are sending 200K+ tokens of input (entire codebases, research papers, legal contracts) and need the model to reason across the full context, the 5.5 advantage over 5.4 widens. For short prompts (under 4K tokens) the gap is usually within 5-10% on quality benchmarks, which is rarely worth the 2x cost.

Pricing (as of June 10, 2026):

| Component | Rate |
|---|---|
| Input (text) | $5.00 per 1M tokens |
| Input (cached, 5-min) | $2.50 per 1M tokens |
| Input (cached, 1-hour) | $3.75 per 1M tokens |
| Output (text) | $15.00 per 1M tokens |
| Output (cached write) | $3.75 per 1M tokens |
| Audio input | $10.00 per 1M tokens |
| Audio output | $30.00 per 1M tokens |
| Image input | $5.00 per 1M tokens (1024x1024 ≈ 1,000 tokens) |
| Batch API (all rates) | 50% off |

### GPT-5.4 — Mid-Tier ($2.50/M in, $10/M out)

GPT-5.4 is the workhorse for most production deployments in 2026. The model is a generation behind the flagship but the price-quality tradeoff is favorable: 90% of 5.5 quality on most reasoning tasks, 100% on simpler classification and extraction workloads, at exactly half the input cost. For most teams shipping a real product, 5.4 is the default choice.

The 5.4 context window is 400K tokens — half of 5.5 but still 3-4x what most production prompts need. Multimodal support is identical to 5.5 (text, image, audio). The main limitation: on the hardest reasoning benchmarks (SWE-bench Verified above 80%, GPQA Diamond above 75%), 5.4 trails 5.5 by 5-8 points. If your product's differentiation is the absolute best quality, you need 5.5. If you are optimizing for cost with acceptable quality, 5.4 is the right answer.

Pricing (as of June 10, 2026):

| Component | Rate |
|---|---|
| Input (text) | $2.50 per 1M tokens |
| Input (cached, 5-min) | $1.25 per 1M tokens |
| Input (cached, 1-hour) | $1.875 per 1M tokens |
| Output (text) | $10.00 per 1M tokens |
| Output (cached write) | $2.50 per 1M tokens |
| Audio input | $5.00 per 1M tokens |
| Audio output | $20.00 per 1M tokens |
| Image input | $2.50 per 1M tokens |
| Batch API (all rates) | 50% off |

### GPT-5 Mini — Budget ($0.15/M in, $0.60/M out)

GPT-5 Mini is the new budget tier that replaced the GPT-4o-mini and GPT-3.5-turbo lines in late 2025. At $0.15/$0.60 per million tokens it is the cheapest OpenAI model in 2026 that is still worth using for production — anything cheaper and the quality drops off the cliff. The context window is 256K, multimodal support is text and image only (no audio), and the model is optimized for high-throughput low-latency workloads.

The Mini tier is what makes the 2026 economics work for agents. If you are building an agent framework that makes 50+ LLM calls per task, running the orchestrator on Mini at $0.60/M output and reserving 5.5 for the final synthesis step is the standard pattern. The same agent at 5.5 across the board would cost 25x more on the orchestrator calls and would not be faster (Mini has the same TTFT as 5.4 on simple prompts).

Pricing (as of June 10, 2026):

| Component | Rate |
|---|---|
| Input (text) | $0.15 per 1M tokens |
| Input (cached, 5-min) | $0.075 per 1M tokens |
| Input (cached, 1-hour) | $0.1125 per 1M tokens |
| Output (text) | $0.60 per 1M tokens |
| Output (cached write) | $0.15 per 1M tokens |
| Audio input | not supported |
| Audio output | not supported |
| Image input | $0.15 per 1M tokens |
| Batch API (all rates) | 50% off |

## Batch API: 50% Off, Async

The Batch API is the single biggest discount OpenAI offers in 2026: 50% off every rate on every model, in exchange for async delivery. You submit a JSONL file (up to 50,000 requests per batch, 200MB per file), the batch completes within 24 hours (usually 1-6 hours in practice), and you pay the half-rate on every token used.

The tradeoff is latency. Batch is not for interactive user-facing workloads. It is for:

- **Evaluation pipelines**: scoring 10,000 model outputs against ground truth.
- **Bulk content generation**: producing product descriptions, translations, summaries in batch.
- **Backfill jobs**: re-classifying historical data, generating embeddings for old documents.
- **Offline analytics**: running the model on a nightly data warehouse job.

For real-time chat, agent loops, or any workload where the user is waiting, Batch is not an option. The 24-hour SLA makes it fundamentally different from the streaming Chat Completions API.

Worked example: a team that runs 100M output tokens of evaluation work per month on GPT-5.5:

- Chat Completions API at $15/M output = $1,500/month
- Batch API at $7.50/M output = $750/month
- Savings: $750/month, 50% off

The catch: you have to engineer the batch submission pipeline. The OpenAI Python SDK supports the `batches` endpoint directly, and the JSONL format is well-documented, but it is not a drop-in replacement for streaming chat. Most teams add Batch as a separate code path for the workloads that can tolerate the latency.

## Cached Input: 50% Off Repeated Prompts

The cached input discount is the second lever, and for many production workloads it is the bigger lever. When you send the same long prefix repeatedly (a 50K-token system prompt, a 200K-token document for RAG, a 1MB code file in a code review tool), OpenAI caches the prompt tokens and charges a discount on the cached portion.

There are two cache tiers in 2026:

| Tier | Discount | Cache lifetime | Best for |
|---|---|---|---|
| **5-minute cache** | 50% off | 5 minutes of inactivity | Interactive sessions, agent loops, multi-turn chat |
| **1-hour cache** | 25% off | 1 hour of inactivity | Batch jobs, scheduled reports, evals, RAG with stable corpora |

The 5-minute tier is the default that gets applied automatically. When you send a request where the prefix matches a cache entry that was last used within 5 minutes, the cached portion is billed at 50% off. There is no opt-in — OpenAI applies it transparently. The catch: the cache must be at least 1,024 tokens to qualify, and the cache key is the literal byte sequence of the prefix, so even a single whitespace change invalidates it.

The 1-hour tier is opt-in. You set `prompt_cache_retention: "1h"` in the API call, and OpenAI extends the cache lifetime to 1 hour (still 25% off instead of 50%, because the storage cost is higher). This is the right tier for batch jobs that send the same large document repeatedly — evaluation suites, RAG systems with stable corpora, code review tools that re-process the same repo.

Worked example: a RAG system that sends a 200K-token document on every query:

- Without cache: 200K input tokens × $5/M (5.5) = $1.00 per query
- With 5-min cache hit (50% off on the 200K): 200K × $2.50/M = $0.50 per query
- With 1-hour cache hit (25% off on the 200K): 200K × $3.75/M = $0.75 per query

The 5-minute tier is the better discount per query, but only works for interactive workloads. The 1-hour tier is the right choice for batch and scheduled jobs.

The cached write fee is the third piece. When you write new content to the cache (a new long document that has not been sent before), OpenAI charges a "cache write" fee of 25% of the input rate. This is amortized across all the future cache hits, but on the first request you pay the full input rate plus the cache write. For most workloads this is a non-issue (the cache write fee is small relative to the total query volume), but for one-off batch jobs that do not benefit from repeated access, the cached input tier is not a cost saver.

## Real Cost Math: Three Budgets

These worked examples assume a 1:3 input-to-output ratio (typical for chat and agent workloads) and standard rates (no Batch, no cache). The output share dominates the bill, so reducing output tokens is the highest-leverage optimization.

### $100/month budget

| Model | Input tokens | Output tokens | Best for |
|---|---|---|---|
| GPT-5.5 | 20M | 6.67M | Hard reasoning, code review of small files |
| GPT-5.4 | 40M | 10M | General chat, mid-size document analysis |
| GPT-5 Mini | 666M | 166M | High-volume agents, classification, RAG on huge corpora |

At the $100 budget, the choice is really about volume. On Mini, $100 covers a serious amount of traffic — 166M output tokens is roughly 40 million words, which is enough for a content generation pipeline producing 200 articles per day. On 5.5, $100 covers about 6.67M output tokens, which is roughly 1.5 million words — enough for a focused daily content product or a small chat product.

### $1,000/month budget

| Model | Input tokens | Output tokens | Best for |
|---|---|---|---|
| GPT-5.5 | 200M | 66.7M | Mid-size product with 5.5 as default |
| GPT-5.4 | 400M | 100M | Production deployment, default 5.4 with 5.5 fallback |
| GPT-5 Mini | 6.66B | 1.66B | Mass-market product, classification-heavy, RAG at scale |

At $1,000, the choice depends on the workload type. For a chat product with 10K daily active users, 5.4 is the right default (100M output tokens = ~1,000 tokens per user per day, which is a typical chat workload). For a content generation product with 1,000 daily runs, 5.5 is defensible (66.7M output tokens = 67K tokens per run, which is a long-form document). For a moderation or classification pipeline, Mini at 1.66B output tokens is enormous — enough for hundreds of millions of moderation decisions per month.

### $10,000/month budget

| Model | Input tokens | Output tokens | Best for |
|---|---|---|---|
| GPT-5.5 | 2B | 666.7M | Flagship product, agents, large document analysis |
| GPT-5.4 | 4B | 1B | Multi-product suite, 5.4 as the workhorse |
| GPT-5 Mini | 66.6B | 16.6B | Mass-market classification, search, recommendations |

At $10,000, the architecture matters more than the model choice. The teams spending this much are typically running a router that dispatches requests to the right model — 5.5 for the hardest queries, 5.4 for the bulk, Mini for the long tail of simple completions. The OpenAI Python SDK supports the `batches` endpoint directly, and most teams pair it with a routing layer like [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) (an OpenAI-compatible aggregator that lets you route the same model from a different endpoint without changing code).

## Decision Tree: Which Model When

```
Is the task simple classification, extraction, or routing?
  → Yes: GPT-5 Mini
  → No, continue.

Is the input under 4K tokens and the task is general chat/completion?
  → Yes: GPT-5.4
  → No, continue.

Is the input over 100K tokens (long-context synthesis)?
  → Yes: GPT-5.5
  → No, continue.

Is the task a hard coding or math problem where quality is the differentiator?
  → Yes: GPT-5.5
  → No, continue.

Default: GPT-5.4
```

The decision tree is intentionally conservative. The default is 5.4, not 5.5, because the price-quality gap is favorable for 5.4 in 2026. You should only reach for 5.5 when you have evidence that 5.4 is failing on your specific workload. The same is true for Mini: the default for high-volume workloads is Mini, not 5.4, because the cost difference is 16x on input and the quality gap on simple tasks is negligible.

## China Access and FreeModel

OpenAI is not directly accessible from mainland China as of June 2026. The pricing above is the same everywhere OpenAI is accessible, but Chinese developers typically go through one of three paths:

1. **Proxy/VPN access to OpenAI direct** — high latency (200-500ms added), variable reliability, occasional rate limits. Works but feels slow for interactive workloads.
2. **OpenAI-compatible aggregator with China-direct access** — [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) is the most established option. It exposes the GPT-5 family behind a China-direct OpenAI-compatible endpoint, with the same prices as OpenAI direct (no markup) for paid tiers and a free tier that covers 5.4 and Mini for development.
3. **Azure OpenAI Service** — runs in China through 21Vianet partnership. Slightly different pricing (Azure is a separate billing relationship) and a 3-7 day onboarding process for new accounts.

The FreeModel angle is the cheapest drop-in for most Chinese teams: same prices, same OpenAI SDK, China-direct latency. The migration is a base URL swap. The only catch: FreeModel's free tier is rate-limited to 60 RPM, which is enough for development but not for production. Paid tiers start at the same prices as OpenAI direct.

## Code: Python with the OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# Default: GPT-5.4 (mid-tier, best price/quality balance)
response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the last 3 emails in my inbox."},
    ],
)

print(response.choices[0].message.content)
print(f"Tokens: {response.usage.total_tokens}")
```

To use cached input (automatic 5-minute cache on prompts over 1,024 tokens):

```python
# First request: full price, writes to cache
response1 = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},  # 50K tokens
        {"role": "user", "content": "Query 1"},
    ],
)

# Subsequent requests within 5 minutes: 50% off on the cached prefix
response2 = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},  # same prefix
        {"role": "user", "content": "Query 2"},
    ],
)

# Check cached tokens in the response
print(f"Cached: {response2.usage.prompt_tokens_details.cached_tokens}")
```

To opt into 1-hour cache:

```python
response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[...],
    extra_body={"prompt_cache_retention": "1h"},  # 25% off instead of 50%
)
```

## Code: curl with Manual JSON

```bash
curl -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-5.4",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Write a haiku about programming."}
    ]
  }'
```

To use Batch (50% off all rates):

```bash
# 1. Create a JSONL file with one request per line
cat > batch_input.jsonl << 'EOF'
{"custom_id": "req-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-5.4", "messages": [{"role": "user", "content": "Hello"}]}}
{"custom_id": "req-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-5.4", "messages": [{"role": "user", "content": "World"}]}}
EOF

# 2. Upload the batch input file
BATCH_FILE=$(curl -s -X POST "https://api.openai.com/v1/files" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "file=@batch_input.jsonl" \
  -F "purpose=batch" | jq -r .id)

# 3. Create the batch
BATCH_ID=$(curl -s -X POST "https://api.openai.com/v1/batches" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"input_file_id\": \"$BATCH_FILE\", \"endpoint\": \"/v1/chat/completions\", \"completion_window\": \"24h\"}" | jq -r .id)

echo "Batch created: $BATCH_ID"
```

## Limitations

**GPT-5 is not a single model.** The "GPT-5" name covers three tiers (5.5, 5.4, Mini) with three different price points and three different capability profiles. If you see a benchmark quoted for "GPT-5" without specifying the tier, the result is most likely from GPT-5.5 (the flagship) and will not apply to 5.4 or Mini.

**Cache hits are not guaranteed.** The 5-minute cache is best-effort. If OpenAI evicts your cache entry (high load, capacity management), the next request pays full price. Most production workloads see 80-95% cache hit rates on repeated prompts, but the 5-20% miss rate means you should not budget assuming 100% cache hits.

**The cached write fee is real.** On the first request that writes a new long prefix to the cache, you pay the input rate plus a 25% "cache write" surcharge. For one-off workloads that do not benefit from repeated access, the cache is not a cost saver.

**Mini has no audio support.** If your workload includes audio (transcription, voice agents, audio classification), you need 5.4 or 5.5. Mini handles text and image only.

**Batch has a 24-hour SLA.** For real-time workloads, Batch is not an option. The 24-hour completion window is the contract; most batches complete in 1-6 hours but you cannot depend on faster.

**China access requires a workaround.** OpenAI is not directly accessible from mainland China. The three paths are proxy, FreeModel (China-direct OpenAI-compatible aggregator), or Azure OpenAI (separate billing).

## Use Cases

**Building a chat product with 10K DAU.** Default to **GPT-5.4** for the main chat. Use **GPT-5 Mini** for intent classification, routing decisions, and conversation summarization. Reserve **GPT-5.5** for the long-context synthesis requests where users upload 100K+ tokens of document. At a typical chat workload (1,000 input + 500 output tokens per message), 10K DAU at 10 messages per day = 100M output tokens, which fits in the $1,000 budget for 5.4.

**Building a code review tool.** Use **GPT-5.5** for the final review (the differentiator is quality). Use **GPT-5.4** for the pre-filtering step that decides which PRs to surface. Use **GPT-5 Mini** for the "is this PR description clear?" classification. The cached input lever matters here: a 200K-token repo context can be cached for repeated PRs, halving the input cost on the follow-up calls.

**Building a RAG system on a 10M-token corpus.** Use **GPT-5.4** for the answer generation, with the retrieved document prefix cached for the 1-hour tier. Without cache, a 200K-token retrieved document costs $0.50 per query on 5.4 input alone. With 1-hour cache at 25% off, the same query costs $0.375 — and if the same document is queried repeatedly (typical for a "what is the company's vacation policy" question), the 5-minute cache at 50% off drops it to $0.25.

**Building a high-volume moderation or classification pipeline.** Use **GPT-5 Mini** exclusively. At $0.15/$0.60 per million tokens, the cost is negligible for millions of decisions per day. The quality is more than sufficient for binary classification, and the latency is the lowest of the three tiers.

**Migrating from the GPT-5.2 line (deprecated June 2026).** The migration to GPT-5.4 is a one-line model string change. The pricing is lower (5.4 at $2.50/$10 vs 5.2 at $10/$30), so most workloads see a 3-4x cost reduction on the move. For workloads that were on GPT-5.2 for hard reasoning, GPT-5.5 is the upgrade path (and 5.5 is also cheaper than 5.2 on input: $5 vs $10).

## FAQ

**Q: Which GPT-5 model should I use for a chat product?**

A: GPT-5.4 is the right default for most chat products in 2026. The price-quality gap between 5.4 and 5.5 is small (within 5-10% on most chat benchmarks), but the cost difference is 2x. Reserve 5.5 for the long-context requests (over 100K input tokens) where the model has a measurable advantage, and use Mini for the classification and routing calls.

**Q: Is GPT-5 cheaper than GPT-4o?**

A: Yes, on input. GPT-5.4 at $2.50/M is half the GPT-4o rate of $5/M, and Mini at $0.15/M is dramatically cheaper than GPT-4o-mini at $0.15/M (the same). For most workloads, migrating from GPT-4o to GPT-5.4 is a 2x cost reduction with comparable or better quality.

**Q: Can I mix models in the same workflow?**

A: Yes, and you should. The standard pattern is to use Mini for the long tail of simple completions (intent classification, routing, summarization, extraction), 5.4 for the bulk of user-facing completions, and 5.5 for the hardest tasks. The OpenAI Python SDK supports all three models with the same call shape, so the routing logic is in your application code.

**Q: How does the cached input discount work?**

A: When you send a request with a prefix that matches a cache entry (at least 1,024 tokens, last used within 5 minutes for the 5-minute tier or 1 hour for the 1-hour tier), OpenAI charges a discount on the cached portion. The 5-minute tier is automatic and gives 50% off. The 1-hour tier is opt-in (`prompt_cache_retention: "1h"`) and gives 25% off. Both apply transparently — you do not need to manage the cache yourself.

**Q: Is the Batch API worth the 24-hour wait?**

A: For evals, bulk content generation, and backfill jobs, yes — the 50% discount is significant at scale. For interactive workloads, no. The 24-hour SLA is incompatible with any user-facing product. Most teams add Batch as a separate code path for the async workloads and keep the Chat Completions API for the real-time path.

**Q: Can I use GPT-5 from China?**

A: OpenAI is not directly accessible from mainland China. The three paths are proxy/VPN (high latency, unreliable), [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) (China-direct OpenAI-compatible aggregator with the same prices), or Azure OpenAI Service through 21Vianet (separate billing, 3-7 day onboarding). For most Chinese teams, FreeModel is the cheapest drop-in.

**Q: Is there a free tier?**

A: OpenAI gives $5 in free credit to new accounts (valid for 3 months), but there is no permanent free tier for GPT-5. FreeModel has a permanent free tier for development use of GPT-5.4 and Mini (60 RPM, 100K tokens per day). For production, you need a paid account at OpenAI direct, FreeModel, or Azure.

**Q: What happened to GPT-5.2?**

A: Deprecated on June 5, 2026, with the Copilot retirement running through August 2026. Direct API access is expected to end Q4 2026. Most production workloads should migrate to 5.4 (cheaper, similar quality) or 5.5 (flagship, new) by Q3 2026.

## Conclusion

The GPT-5 pricing in 2026 is structured around three tiers, and the right choice depends on the workload type, not the brand name. GPT-5.5 at $5/$15 per million tokens is the flagship for the hardest reasoning tasks. GPT-5.4 at $2.50/$10 is the workhorse for most production deployments — same quality on most tasks, half the cost. GPT-5 Mini at $0.15/$0.60 is the budget tier for high-volume agents and classification, and the right default for the long tail of simple completions.

The two compounding levers are Batch (50% off all rates, async only) and cached input (50% off on repeated prompts via the 5-minute tier, 25% off via the 1-hour tier). For workloads with long system prompts, RAG on stable corpora, or code review on a fixed repository, the cached input lever is the single biggest cost optimization available — and it is automatic, requiring no code change.

For most teams in 2026, the right architecture is a router: Mini for the simple calls, 5.4 for the bulk, 5.5 for the hard ones. [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) is the most pragmatic pick for China-direct OpenAI-compatible access (the same models, same prices, no proxy). OpenRouter is the alternative for multi-vendor flexibility. The Batch API is the optimization for any workload that can tolerate 24 hours of latency. And the cached input discount is the lever to turn on for any workload with a stable long prefix.

The pricing is not the whole story — model quality, latency, and feature support (function calling, vision, audio) all factor in. But for the cost-conscious team picking a model in 2026, the math is: start with 5.4 as the default, reach for 5.5 only when the eval says 5.4 is failing, and use Mini for anything that does not need 5.4's quality. Turn on cached input for any workload with a long prefix. Turn on Batch for any workload that can wait 24 hours. The combination is the cheapest path to production GPT-5 in 2026.
