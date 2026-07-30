---
title: "Meta Model API 2026: Muse Spark $1.25/M Token"
description: "Meta Model API review: Muse Spark 1.1 pricing at $1.25/M input, agentic tool calling, 1M context, search grounding. Comparison vs OpenAI/Anthropic."
slug: "meta-model-api-review"
provider: "meta-ai"
published: true
date: "2026-07-12"
type: "review"
---

# Meta Model API 2026: Muse Spark 1.1 Review — $1.25/M Token Agent Platform

## What is Meta Model API, and why does it matter in 2026?

Meta Model API is Meta's official API platform for its in-house frontier models, launched in early 2026. After years of open-sourcing the Llama family through Hugging Face (Llama 2, Llama 3, Llama 4), Meta has finally built a direct, self-serve API at `api.meta.ai` that competes head-to-head with OpenAI, Anthropic, and Google. The flagship model is **Muse Spark 1.1**, a multimodal (text + image + video + PDF) model with a 1M-token context window, priced at $1.25/M input tokens and $4.25/M output tokens — slotting it between GPT-4o and Claude Sonnet 5 on price.

Three things make Meta Model API a notable July 2026 pick for agent-building teams:

1. **Agentic primitives ship as API defaults.** Muse Spark ships with parallel tool calling, streaming tool-call arguments, computer use (the model operates a computer visually, like Claude's computer use), search grounding (live web data with citations), and multi-agent orchestration — all available on day one through the Responses API. Meta explicitly built the API for the agent era, not for chat.

2. **Three API formats, one backend.** Meta Model API exposes the same model through three endpoints — Responses API (the agentic format with built-in tool state management), Chat Completions API (drop-in OpenAI replacement), and Messages API (Anthropic-style). You pick the format your code already speaks, get the same model, same auth, same pricing. Migration from OpenAI is a `base_url` + `api_key` swap.

3. **OpenAI-compatible + Anthropic-compatible.** The Chat Completions endpoint is a literal drop-in for the OpenAI SDK (`openai.base_url = "https://api.meta.ai/v1"`), and the Messages API uses the Anthropic Messages format. Meta is the first major provider to explicitly dual-support both SDK formats, making it the lowest-friction migration target in 2026.

The trade-off: currently only one model (Muse Spark 1.1) is available via the API — no Llama 4 standalone endpoints, no fine-tuning API, no embeddings. The public preview is US-only. And while $1.25/$4.25 is competitive, the output price is above GPT-4o-mini and DeepSeek V3, so it's not a pure budget play. Meta Model API is for teams that want Meta's first-party model quality with zero SDK rewrite and native agent infrastructure.

## Meta Model API surface: Responses, Chat Completions, and Messages

Meta Model API serves a single backbone model through three endpoint families. The base URL is `https://api.meta.ai/v1` and authentication uses a `MODEL_API_KEY` bearer token.

### 1. Responses API (the agentic endpoint)

The Responses API is Meta's flagship format — it is a stateful endpoint designed for multi-turn agent workflows. Unlike the stateless Chat Completions pattern, Responses carries tool call state across turns automatically: when Muse Spark calls a tool, you submit the result back to the same response, and the model continues with the updated context.

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.meta.ai/v1",
    api_key="MODEL_API_KEY"
)

# Create a response with search grounding
response = client.responses.create(
    model="muse-spark-1.1",
    input="What are the latest VPS hosting deals in July 2026?",
    tools=[{"type": "web_search"}]
)
print(response.output_text)
# Response includes inline citations from web search
```

The Responses API also supports **background responses** (`background: true`) — long-running tasks that return immediately and send results to a webhook. This is useful for multi-hour code refactoring, batch document analysis, or scheduled search crawls.

### 2. Chat Completions API (OpenAI drop-in)

For teams already on the OpenAI SDK, Chat Completions is a zero-migration path:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.meta.ai/v1",
    api_key="MODEL_API_KEY"
)

response = client.chat.completions.create(
    model="muse-spark-1.1",
    messages=[
        {"role": "system", "content": "You are a senior software architect."},
        {"role": "user", "content": "Design a microservices architecture for an e-commerce platform."}
    ],
    tools=[{
        "type": "function",
        "function": {
            "name": "design_service",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "responsibilities": {"type": "array", "items": {"type": "string"}},
                    "api_endpoints": {"type": "array", "items": {"type": "string"}}
                }
            }
        }
    }]
)
print(response.choices[0].message.content)
```

Every Chat Completions feature you expect works: streaming, function calling, structured output (JSON mode), logprobs, max_completion_tokens, temperature, and seed. The model ID `muse-spark-1.1` is the same across all three endpoint families.

### 3. Messages API (Anthropic drop-in)

Meta also supports the Anthropic Messages format:

```python
import anthropic

client = anthropic.Anthropic(
    base_url="https://api.meta.ai/v1",
    api_key="MODEL_API_KEY"
)

response = client.messages.create(
    model="muse-spark-1.1",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "Explain the transformer architecture in simple terms."}
    ]
)
print(response.content[0].text)
```

This dual-compatibility is unique in 2026: no other provider natively supports both OpenAI and Anthropic SDK formats without a proxy layer (like LiteLLM or OpenRouter). Meta does it at the API level.

## Pricing deep dive

Meta Model API's pricing is per-token, pay-as-you-go, with no minimums or commitments:

| Usage | Price per 1M tokens |
|---|---|
| Input (standard) | $1.25 |
| Cached input | **$0.15** (88% discount) |
| Output | $4.25 |
| Web search grounding | $2.50 per 1,000 queries |

Pricing observations:

- **No long-context premium.** Whether your prompt is 100 tokens or 800,000 tokens, you pay the same per-token rate. Google Gemini charges a higher rate for requests above 200K tokens; OpenAI's o-series has per-context pricing. Meta flattens it.

- **Cached input at $0.15/M is aggressive.** OpenAI charges $0.075/M (50% discount on $0.15/M for GPT-4o), Anthropic charges $0.30/M for Claude Sonnet 5 cached input. Meta's $0.15/M sits between them. For high-volume, cache-heavy workloads (customer support with fixed system prompts, document analysis with shared context prefixes), this is the key cost lever.

- **Web search grounding at $2.50/1K queries** is moderate. Google's grounding is free within the Gemini free tier; OpenAI's web search tool costs $5/1K queries. Meta is cheaper than OpenAI but not free.

- **Output is the differentiator.** At $4.25/M, Meta's output is cheaper than Claude Sonnet 5 ($15/M) and GPT-4o ($10/M), but more expensive than DeepSeek V3 ($0.28/M) and Gemini 2.5 Flash ($0.30-5/M). For long-form generation workloads (reports, code generation, multi-turn agent responses), Meta presents a meaningful savings vs the tier-1 incumbents without sacrificing first-party model quality.

### Free tier

The free tier offers **60 requests per minute (RPM) and 2M tokens per minute (TPM)** — generous for prototyping. Compare this to OpenAI's free tier (3 RPM for GPT-4o) and Anthropic's (no free API tier for Claude). The paid tier scales to 3,000 RPM and 4M TPM. Limits apply per team, not per API key.

Note: the free tier is currently limited to **US-based developers** (public preview restriction). Meta has not announced international availability.

## Muse Spark 1.1 capabilities

Muse Spark 1.1 is a multimodal model optimized for agentic and coding work. Key specs:

| Capability | Muse Spark 1.1 |
|---|---|
| Context window | 1,048,576 tokens (1M) |
| Input modalities | Text, image, video, PDF |
| Output modality | Text |
| API endpoint families | Responses, Chat Completions, Messages |
| Tool calling | Parallel, streamed arguments |
| Structured output | JSON mode |
| Search grounding | Web search with citations |
| Computer use | Visual agent operation |
| Prompt caching | Automatic, $0.15/1M cached input |
| Background responses | Webhook-delivered async completion |
| Rate limits (free) | 60 RPM, 2M TPM |
| Rate limits (paid) | 3,000 RPM, 4M TPM |

### Strengths

**Agentic tool calling.** Muse Spark is explicitly trained for multi-step tool use. Meta's benchmarks suggest it performs competitively with Claude Sonnet 5 on agentic tasks (code refactoring across multiple files, browser-based web tasks, multi-tool orchestration). The parallel tool-calling support means the model can invoke multiple functions in a single turn and process all results together — essential for production agent loops.

**1M context window with no price premium.** This is Muse Spark's clearest advantage over OpenAI (128K for GPT-4o) and Anthropic (200K for Claude). For workloads that need to ingest entire codebases, long meeting transcripts, or multi-hour video streams, the 1M window removes chunking complexity. And the lack of a long-context premium means you don't pay extra for exercising it.

**Computer use.** Like Claude's computer use capability, Muse Spark can view and interact with a desktop environment through screenshots. The model identifies UI elements, moves the cursor, clicks, types, and navigates across applications. This is exposed as a tool call — the model requests a screenshot, processes the visual state, and outputs the next action. In early 2026, Claude and Meta are the only two providers shipping production-grade computer use via API.

### Weaknesses

**Single model.** The API serves only Muse Spark 1.1. There is no smaller/faster/cheaper model for lightweight tasks, no vision-specific model, no embedding model. Teams on a budget will need to layer a secondary provider (Groq for fast inference, DeepInfra for budget) for their non-agent workloads.

**US-only preview.** The public preview is geo-restricted. International teams, including China-based developers, cannot directly register. This significantly limits the addressable developer audience in mid-2026. Meta has committed to global expansion but has not published a timeline.

**No fine-tuning.** Unlike OpenAI (fine-tuning API for GPT-4o-mini) and Together AI (native fine-tuning for open models), Meta Model API offers zero model customization. For teams that need domain-specific model adaptation, Meta is not yet an option.

## Meta Model API vs competitors

| Factor | Meta Muse Spark 1.1 | OpenAI GPT-4o | Claude Sonnet 5 | Gemini 2.5 Flash |
|---|---|---|---|---|
| Input price | $1.25/M | $2.50/M | $3/M (intro $2) | $0.15-1.25/M |
| Output price | $4.25/M | $10/M | $15/M (intro $10) | $0.30-5/M |
| Cached input | $0.15/M | $0.075/M | $0.30/M | N/A |
| Context window | 1M | 128K | 200K | 1M |
| OpenAI SDK | ✅ Native | ✅ Native | ❌ (proxy needed) | ❌ (different SDK) |
| Anthropic SDK | ✅ Native | ❌ | ✅ Native | ❌ |
| Computer use | ✅ | ❌ | ✅ | ❌ |
| Search grounding | ✅ ($2.50/1K) | ✅ ($5/1K) | ❌ | ✅ (included) |
| Fine-tuning | ❌ | ✅ | ❌ | ❌ |
| Free tier | 60 RPM / 2M TPM | 3 RPM GPT-4o | None | 15 RPM |
| Geo-restriction | US only | Global | Global | Global (CN proxy) |

### When to pick Meta Model API

1. **Agentic code assistants** — Muse Spark 1.1's computer use + parallel tool calling + 1M context makes it ideal for autonomous coding agents that need to navigate an IDE and reference the full codebase.

2. **Multi-format migration** — teams with both OpenAI and Anthropic SDK codebases can consolidate on Meta Model API without rewriting either format.

3. **Long-context document processing** — 1M context at standard rates eliminates chunking for long documents, meeting transcripts, and video content.

4. **Cache-heavy production workloads** — $0.15/M cached input makes high-volume customer support, document Q&A, and code analysis pipelines cost-efficient.

## Frequently asked questions

### How do I get started with Meta Model API?

Visit https://developer.meta.com/ai/, sign up for the public preview, generate an API key, and set your OpenAI SDK base URL to `https://api.meta.ai/v1`. The "Get started" quickstart guide walks through making your first request in under five minutes.

### Is Meta Model API free?

The free tier offers 60 requests per minute and 2 million tokens per minute. There is also free credits on signup for the public preview. No credit card is required for the free tier. For production workloads, the paid tier starts at pay-as-you-go per-token pricing with no minimum commitment.

### Can I use Meta Model API from China?

Currently, Meta Model API is in public preview for US developers only. Access from mainland China requires a stable proxy connection. Meta has committed to international expansion but has not announced a timeline. For China-based developers, alternatives like DeepSeek, Alibaba Qwen (Bailian), and Tencent Hunyuan provide direct-access options.

### How does Meta Model API compare to Llama open-source?

The Llama open-weight models (Llama 2, 3, 4) remain available on Hugging Face and GitHub under the Llama Community License for self-hosted use. Meta Model API is a separate, managed service running Muse Spark 1.1 — a different, more capable model not available for download. Think of it like OpenAI: GPT-4o-mini is not open-source, but you can call it via API. Similarly, Muse Spark is Meta's API-only frontier model.

### Does Meta Model API support image generation?

No. Muse Spark 1.1 can understand images (read text, describe scenes, analyze charts) but cannot generate images. For image generation, Meta provides a separate product (Imagine with Meta) which is not part of the Model API.

### What rate limits apply?

Free tier: 60 RPM, 2M TPM per team. Paid tier: 3,000 RPM, 4M TPM per team. Rate limits apply per team, not per API key. Background responses have a separate submission limit of 600 per minute per team.

### Does Meta Model API offer an SLA?

Meta has not published a public SLA for the Model API. Enterprise customers can negotiate SLAs through Meta's enterprise sales team. The public preview terms do not include uptime guarantees.

### How do I get a Meta Model API key?

Sign up at https://developer.meta.com/ai/ (US-only preview). After approval, generate an API key from the dashboard. The key is a bearer token used as `MODEL_API_KEY` in your environment.

### Can I use Meta Model API with LangChain or LlamaIndex?

Yes. Since the API is OpenAI-compatible, any framework that supports the OpenAI SDK (LangChain, LlamaIndex, AutoGen, CrewAI, Vercel AI SDK) works by changing the `base_url` to `https://api.meta.ai/v1`. The model ID is `muse-spark-1.1`.

### What is the context window for Muse Spark 1.1?

1,048,576 tokens (1M). This matches Google Gemini 2.5 Pro's context window and far exceeds OpenAI (128K) and Anthropic (200K). There is no long-context premium — you pay the same per-token rate regardless of context length.
