---
title: "Kimi K3 API Review 2026: 1M Context & Pricing"
description: "Kimi K3 API review with official pricing: ¥2 cached input, ¥20 uncached input, ¥100 output per million tokens, 1M context, vision, tools, and K2 alternatives."
pubDate: 2026-07-17
provider: kimi
category: review
featured: true
---

# Kimi K3 API Review 2026: The 1M-Context Chinese Model

Kimi K3 is Moonshot AI's new flagship API model, released into a very specific market gap: long-running coding agents and knowledge-work systems that need a huge context window, native vision, tool calls, and Chinese-language strength in one endpoint. The official model documentation lists 2.8 trillion total parameters, a 1,048,576-token context window, native image and video understanding, automatic context caching, JSON mode, structured output, and tool-choice controls.

That headline context number is real, but it is not a free-tier shortcut. Kimi K3 is billed separately for cache-hit input, cache-miss input, and output. The current official table lists ¥2 per million cached input tokens, ¥20 per million uncached input tokens, and ¥100 per million output tokens. A new-user ¥15 coupon does not apply to K3, so budget planning matters from the first production test.

This review focuses on the API a developer can use today: pricing, model selection, OpenAI-compatible code, multimodal input, agent controls, limitations, and the cases where Kimi K2.7 Code or K2.6 is the more rational choice.

## Kimi K3 at a Glance

| Item | Verified Kimi K3 detail |
|---|---|
| API model ID | `kimi-k3` |
| Context window | 1,048,576 tokens (1M) |
| Input pricing | ¥2/M cached; ¥20/M cache miss |
| Output pricing | ¥100/M tokens |
| Reasoning | Always enabled; `reasoning_effort` currently supports `max` |
| Modalities | Text, image, and video input |
| Structured output | JSON mode and JSON Schema response format |
| Tools | Tool calls, `tool_choice`, dynamic tool loading |
| API style | OpenAI-compatible Chat Completions |
| Availability | Kimi API Open Platform; Mainland China direct access is the intended path |

The model ID is short and practical, but do not assume that every OpenAI parameter is portable. K3 has its own parameter contract, and the official documentation marks several sampling settings as fixed values.

## Official Kimi K3 Pricing: Cache Hits Change the Math

Kimi's pricing page separates input into cache-hit and cache-miss categories. That is important for long prompts, repository instructions, policy documents, and repeated agent turns. The official values are:

| Model | Cached input / 1M | Uncached input / 1M | Output / 1M | Context |
|---|---:|---:|---:|---:|
| Kimi K3 | ¥2.00 | ¥20.00 | ¥100.00 | 1,048,576 |
| Kimi K2.7 Code | ¥1.30 | ¥6.50 | ¥27.00 | 262,144 |
| Kimi K2.7 Code HighSpeed | ¥2.60 | ¥13.00 | ¥54.00 | 262,144 |
| Kimi K2.6 | ¥1.10 | ¥6.50 | ¥27.00 | 262,144 |

A simple 100,000-token request illustrates the difference. If the input is a cache miss and the model returns 10,000 tokens, the K3 token bill is approximately ¥2 + ¥1 = ¥3. If the same 100,000-token prefix is a cache hit, the input portion falls to ¥0.20, for an approximate total of ¥1.20. This excludes any product-specific fees and assumes the displayed token counts are the billable counts.

The lesson is not “K3 is cheap.” Output is expensive at ¥100/M, and cache misses cost ten times more than cache hits. The lesson is that K3 can be predictable for a stable long-context workflow if you keep the prefix stable, reuse the same system and tool definitions, and inspect usage fields in every response.

Moonshot is also running a time-limited recharge coupon campaign from July 16 through August 12, 2026. The official promotion describes one eligible first recharge transaction per organization during the campaign: 10% for ¥99–¥499, 20% for ¥500–¥1,999, 25% for ¥2,000–¥4,999, and 30% at ¥5,000 or more. Treat this as a platform coupon, not a permanent API price cut; confirm the campaign terms before relying on it in a forecast.

## What Kimi K3 Actually Adds

K3 is not just K2 with a larger context field. Moonshot describes a 2.8-trillion-parameter model built with Kimi Delta Attention and Attention Residuals, with a sparse mixture-of-experts design. Its public documentation emphasizes long-horizon programming, end-to-end knowledge work, and agent workflows rather than a single short-answer benchmark.

For API developers, the practical additions are more useful than the parameter headline:

- **1M context and automatic caching.** The platform says ordinary requests can attempt automatic prefix caching without a user-managed cache ID or TTL.
- **Native vision.** K3 accepts text, images, and video. Images should be sent as base64 or a Kimi file reference rather than a public image URL.
- **Always-on reasoning.** K3 always reasons; the current `reasoning_effort` option is `max`. Do not copy the K2.x thinking parameter contract without checking the K3 guide.
- **Tool control.** K3 supports tool calls, `tool_choice`, and dynamic tool loading. The latter is useful when an agent has a large tool catalog but only needs to expose a small subset per turn.
- **Structured output.** JSON mode and JSON Schema support make K3 more appropriate for extraction and workflow state than a plain conversational endpoint.
- **Long-running coding.** Moonshot positions K3 for repository-scale code work, terminal coordination, and visual feedback loops such as front-end or CAD tasks.

These are platform capabilities, not a guarantee that every task will improve when the context window grows. A 1M window can increase latency, prompt complexity, and debugging cost if your application sends the whole workspace on every turn.

## First API Call with curl

Kimi exposes an OpenAI-compatible endpoint. Keep the API key in an environment variable and start with the smallest useful request:

```bash
export KIMI_API_KEY="YOUR_KIMI_API_KEY"
curl https://api.moonshot.cn/v1/chat/completions \
  --header "Authorization: Bearer YOUR_KIMI_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kimi-k3",
    "messages": [{"role": "user", "content": "Summarize the trade-offs of a 1M-token context window."}]
  }'
```

The endpoint is compatible enough for standard Chat Completions tooling, but use the Kimi model guide when adding reasoning, vision, tool, or structured-output fields. Never paste a real key into source control, logs, or a public issue.

## Python with the OpenAI SDK

The official quickstart uses the OpenAI Python SDK with a Kimi base URL. This makes a migration test easy:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"],
    base_url="https://api.moonshot.cn/v1",
)

response = client.chat.completions.create(
    model="kimi-k3",
    messages=[
        {"role": "system", "content": "You are a precise software engineering assistant."},
        {"role": "user", "content": "List three risks of sending an entire repository in every agent turn."},
    ],
)

print(response.choices[0].message.content)
print(response.usage)
```

Log `response.usage` in a cost dashboard. For K3, usage observability is not optional: the difference between a cache hit and a cache miss is large, and output tokens cost five times as much as uncached input tokens.

## Vision, JSON, and Agent Workflows

For vision, Kimi's documentation requires `message.content` to be an array of content parts. Do not serialize that array into a string. A minimal image request looks like this conceptually:

```python
message = {
    "role": "user",
    "content": [
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}},
        {"type": "text", "text": "Describe the layout and list the visible UI defects."},
    ],
}
```

K3 also supports JSON mode and JSON Schema response formats. Use them for extraction, but keep the schema small and validate the returned object on your side. In agent systems, combine structured output with `tool_choice` so the model cannot silently switch between answering and mutating an external system.

Dynamic tool loading is especially interesting for long-context agents. Instead of sending every tool definition in every turn, expose a short tool set for the current phase, then load more definitions when the model reaches a step that needs them. This can reduce prompt bloat and improve the chance of a stable cache prefix.

## Kimi K3 vs K2.7 Code vs K2.6

K3 is the right default when context size and multimodal long-horizon work dominate. It is not the default for every coding task.

Choose **Kimi K3** when you need repository-scale context, long documents, visual feedback, persistent tool workflows, or a single model for Chinese and English knowledge work. Budget for expensive output and test cache behavior.

Choose **Kimi K2.7 Code** when the job is primarily software engineering and 256K is enough. Its uncached input is ¥6.50/M and output is ¥27/M, a much lower ceiling than K3. The HighSpeed variant is documented at about 180 tokens/second, with short-context cases reaching about 260 tokens/second, but it doubles the regular K2.7 Code prices.

Choose **Kimi K2.6** for a general-purpose multimodal model with 256K context, thinking and non-thinking modes, and the same ¥27/M output price as regular K2.7 Code. It is a more economical option for visual understanding, agent tasks, and ordinary conversation when 1M context is unnecessary.

If you are migrating from OpenAI, run the same eval suite against all three. Compare tool-call validity, JSON adherence, cache-hit ratio, time-to-first-token, total output tokens, and human correction time. “OpenAI-compatible” describes the wire format; it does not make behavior identical.

## Limitations and Production Risks

K3 has several constraints that should be in your launch checklist:

1. **The ¥15 new-user coupon does not unlock K3.** The official K3 guide says the coupon cannot be used for K3 after the model launch; plan to recharge for testing.
2. **Reasoning is always on.** The current K3 contract supports `reasoning_effort=max`, not a full range of effort levels. This can increase output and latency on simple tasks.
3. **Public image URLs are not the safe path.** Use base64 or Kimi file references for vision input, and keep the content field as an array.
4. **Web search is under upgrade.** The pricing/model docs currently warn that the web-search feature is being updated and should not be used in production workflows until the documentation catches up.
5. **The weights are not yet the API.** Moonshot says full K3 weights are planned by July 27, 2026. A future open release may change hosting economics, but it does not change today's managed API bill.
6. **Regional access is part of TCO.** The Kimi API Open Platform is designed for direct Mainland China access. Teams elsewhere should verify network reachability, data routing, and support expectations before committing.

For an external multi-provider control plane, you can also test Kimi alongside other endpoints through [FreeModel API access](https://freemodel.dev/invite/FRE-7a3b6220). Use that as an evaluation and routing option, not as a reason to ignore the upstream provider's model IDs, usage accounting, or regional terms.

## Best Use Cases

Kimi K3 is compelling for four concrete workloads:

- **Repository-scale coding agents:** keep architecture notes, code, tests, and tool results in one working context, while controlling tools by phase.
- **Chinese knowledge work:** analyze long policy, legal, product, or research collections without aggressively chunking every document.
- **Visual software workflows:** inspect screenshots, UI states, diagrams, or video snippets as part of an iterative coding task.
- **Structured operations:** use JSON Schema for extraction and tool calls for controlled actions, with validation and approval gates around side effects.

It is a weaker fit for short single-turn chat, tiny JSON extraction, or workloads where output dominates cost. In those cases, a smaller K2.6 or another low-output-price endpoint can be the better engineering decision.

## Verdict: Buy the Context, Not the Hype

Kimi K3 is a serious API release: 1M context, vision, tools, structured output, automatic caching, and an OpenAI-compatible surface. The official feature set makes it relevant to coding agents and long-document workflows immediately.

The pricing is the catch. At ¥20/M uncached input and ¥100/M output, K3 is not a cheap general chatbot. Its economics become more attractive when you reuse a stable prefix and keep outputs disciplined; they become painful when every agent turn misses the cache and produces long reasoning traces.

Our recommendation is to pilot K3 against K2.7 Code and K2.6 with a production-shaped eval set. If K3's longer context reduces chunking bugs, tool retries, and human review enough to offset its output price, it can be the best Kimi model for your workflow. If not, the K2 family gives you most of the compatibility and multimodal surface at a much lower token cost.

## Frequently Asked Questions

**How much does Kimi K3 cost?** K3 costs ¥2 per million cached input tokens, ¥20 per million uncached input tokens, and ¥100 per million output tokens according to the official pricing table.

**Does Kimi K3 really support 1M tokens?** Yes. The official model guide and pricing page list a 1,048,576-token context window. Your application still needs sensible retrieval and prompt management; a large maximum does not mean every request should fill it.

**Can I use Kimi K3 with the OpenAI Python SDK?** Yes. Set the client `base_url` to `https://api.moonshot.cn/v1`, provide a Kimi API key, and use the documented Kimi model ID. Validate feature-specific parameters separately.

**Does Kimi K3 support image and video input?** Yes. The current guide says K3 supports text, image, and video input. For images, use base64 or a Kimi file reference and send `content` as an array of parts.

**Can the ¥15 new-user coupon be used for K3?** No. Moonshot's K3 quickstart explicitly says the new-user coupon cannot be used to experience K3; a recharge is required.

**Should I choose Kimi K2.7 Code instead?** Choose K2.7 Code when 256K context is sufficient and coding cost matters. Its official table lists ¥6.50/M uncached input and ¥27/M output, far below K3's output price.

**Is Kimi K3's web search ready for production?** The current official documentation warns that web search is being upgraded and is not recommended for production workflows. Treat it as a moving feature until Moonshot updates the guidance.

## Sources

- Moonshot AI, [Kimi K3 model guide](https://platform.kimi.com/docs/guide/kimi-k3-quickstart)
- Moonshot AI, [Kimi K3 pricing](https://platform.kimi.com/docs/pricing/chat-k3)
- Moonshot AI, [Kimi K2.7 Code pricing](https://platform.kimi.com/docs/pricing/chat-k27-code)
- Moonshot AI, [Kimi K2.6 pricing](https://platform.kimi.com/docs/pricing/chat-k26)
- Moonshot AI, [Kimi K3 recharge promotion](https://platform.kimi.com/docs/pricing/promotion)
- Moonshot AI, [Kimi K3 technical blog](https://www.kimi.com/blog/kimi-k3)
