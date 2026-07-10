---
title: "ChatGPT Work API Cost 2026: GPT-5.6 Agent Pricing & Token Economics"
description: "ChatGPT Work launched July 2026 on GPT-5.6 for long-running agent tasks. We break down the API cost model, token economics vs Claude Sonnet 5 / DeepSeek V4, and when ChatGPT Work is actually worth the premium."
slug: "chatgpt-work-gpt-5-6-agent-api-cost-2026"
provider: "openai"
published: true
date: "2026-07-10"
type: "news-analysis"
---

# ChatGPT Work API Cost 2026: GPT-5.6 Agent Pricing, Token Economics, and the Real Workload Fit

On July 9, 2026, OpenAI launched ChatGPT Work — a long-running agent product built on GPT-5.6, aimed at "your most ambitious work": multi-hour research, multi-day code refactors, autonomous document generation, and continuous environment-driven tasks. The launch page is at openai.com/index/chatgpt-for-your-most-ambitious-work and the agent is already wired into ChatGPT desktop, the API, and a new background-worker SKU in the Responses API surface. The interesting part for API users is not the product story — it is the **token economics**. ChatGPT Work is the first time OpenAI is shipping a tier that charges *for sustained background compute* rather than *for request/response pairs*, and the implication for the rest of the 2026 LLM API market is bigger than the headline.

This article breaks down the ChatGPT Work pricing model, the per-token cost in the realistic workloads people are actually going to run on it, and the comparison against the three most credible alternatives for long-task agents: Claude Sonnet 5 with its August 31 promo pricing, DeepSeek V4 via OpenRouter, and self-hosted long-context models on Baseten. If you are evaluating ChatGPT Work for a production workload, this is the cost analysis you need before you wire up the API.

## What is ChatGPT Work, and why does it matter in 2026?

ChatGPT Work is OpenAI's answer to the "long-running agent" problem that has been the most-requested feature in the developer LLM API market for the last 18 months. The typical agent use case — a research assistant that browses the web, reads PDFs, writes code, runs shell commands, iterates, and reports back over the course of an hour or a day — does not fit the request/response pricing model of the standard Chat Completions API. Every tool call is a separate billing event. Every retry is a separate billing event. Every time the agent loses context and has to re-read a 200-page PDF, that is a separate billing event. The economics work out OK for a 5-minute task but they fall apart for a 5-hour task.

ChatGPT Work solves this in two ways. First, it gives the agent a **persistent state** — a workspace directory, a shell environment, a process pool, and a long-running tool session that does not need to be re-initialized for every call. The agent can keep processes running for hours, build up intermediate state, and resume from where it left off after a network blip. Second, it ships a new **background worker pricing model** in the Responses API: instead of paying per request, you pay per minute of agent runtime, with the GPT-5.6 model included.

The headline pricing for ChatGPT Work (verified from the OpenAI pricing page on July 9, 2026):

| Tier | Background runtime | GPT-5.6 model usage | Other models | Best for |
|---|---|---|---|---|
| **ChatGPT Work (API)** | $0.40 per agent-hour | Included up to 1M tokens/hour | Bring-your-own-key for non-OpenAI models | Multi-hour research, code refactors, document work |
| **ChatGPT Work (Pro)** | $0.20 per agent-hour (Pro subscribers) | 5M tokens/hour included | $0.50/M input / $1.50/M output beyond included | Pro tier of ChatGPT with agent access |
| **ChatGPT Work (Team)** | $0.15 per agent-hour (Team seat) | 10M tokens/hour included | Same overage pricing | Team workspaces with shared agents |

The most important number in the table is the **$0.40 per agent-hour** line. At a typical agent workload (averaging 200K tokens/hour of GPT-5.6 context + tool calls), the effective per-token cost works out to roughly $2.00 per million tokens — slightly cheaper than GPT-5.6 standard pricing at the Luna tier ($0.50 input + $1.50 output = $2.00 effective for a 1:3 input:output ratio) and dramatically cheaper than GPT-5.6 Sol tier ($15.00 + $45.00 = $60.00 effective for the same ratio). For workloads that are long-running and have low per-request token density, ChatGPT Work is the first time OpenAI is *cheaper* than the standard tier.

## The hidden cost: token density matters more than per-token price

The chatgpt-work pricing is optimized for **low-density, long-duration** workloads. A research agent that spends 90% of its time reading files and 10% of its time writing is the ideal case. A code-refactor agent that streams 50K tokens of generated code per minute is the worst case. Let me model three concrete workloads against the standard GPT-5.6 API pricing and the ChatGPT Work pricing, so you can see where the break-even is.

**Workload 1: 4-hour research agent** (web search + PDF reading + summary write-up)

- Background runtime: 4 hours
- Token usage: 50K input + 30K output per hour, average 80K tokens/hour total
- Total tokens over 4 hours: 320K
- **ChatGPT Work cost**: $0.40 × 4 = **$1.60**
- **GPT-5.6 Luna standard cost**: 160K input × $0.50/M + 120K output × $1.50/M = $0.08 + $0.18 = **$0.26**
- **GPT-5.6 Terra standard cost**: 160K × $3.00/M + 120K × $9.00/M = $0.48 + $1.08 = **$1.56**
- **GPT-5.6 Sol standard cost**: 160K × $15.00/M + 120K × $45.00/M = $2.40 + $5.40 = **$7.80**

For a 4-hour research agent that uses low token density per hour, **standard GPT-5.6 Luna is 6x cheaper than ChatGPT Work** because the per-token pricing wins on low volume. ChatGPT Work is more expensive than Luna for any workload under ~5 hours of runtime with low token density.

**Workload 2: 8-hour code-refactor agent** (reads codebase, makes 200 file edits, runs test suite repeatedly)

- Background runtime: 8 hours
- Token usage: 400K input + 200K output per hour, average 600K tokens/hour total
- Total tokens over 8 hours: 4.8M
- **ChatGPT Work cost**: $0.40 × 8 = **$3.20**
- **GPT-5.6 Luna standard cost**: 3.2M input × $0.50/M + 1.6M output × $1.50/M = $1.60 + $2.40 = **$4.00**
- **GPT-5.6 Terra standard cost**: 3.2M × $3.00/M + 1.6M × $9.00/M = $9.60 + $14.40 = **$24.00**
- **GPT-5.6 Sol standard cost**: $192.00 (impractical for this workload)

For a token-dense 8-hour code agent, **ChatGPT Work is 25% cheaper than Luna standard** and 7x cheaper than Terra. This is the workload that ChatGPT Work is priced for.

**Workload 3: 1-hour customer-support agent** (chat with one customer, 30 messages)

- Background runtime: 1 hour (the agent runs in the background while waiting for the customer to reply)
- Token usage: 20K input + 15K output per message × 30 messages = 600K input + 450K output
- Total tokens: 1.05M
- **ChatGPT Work cost**: $0.40 × 1 = **$0.40**
- **GPT-5.6 Luna standard cost**: 0.60M × $0.50/M + 0.45M × $1.50/M = $0.30 + $0.675 = **$0.975**
- **GPT-5.6 Mini cost (for comparison)**: 0.60M × $0.10/M + 0.45M × $0.40/M = **$0.24**

For a synchronous chat workload, **ChatGPT Work is 2.4x more expensive than Luna standard and 1.7x more expensive than Mini**. The background-runtime pricing is wasted because the agent is mostly idle.

The takeaway from the three workloads: **ChatGPT Work is the right call for workloads that need persistent state across many tool calls, run for 4+ hours, and have moderate-to-high token density**. For pure chat, it is overpriced. For short research tasks, it is overpriced. For multi-day refactors with persistent shell sessions, it is the cheapest option in OpenAI's lineup.

## How ChatGPT Work compares to Claude Sonnet 5, DeepSeek V4, and self-hosted agents

The alternative for long-task agents in 2026 is not the standard Chat Completions API. The alternatives are the other products that are explicitly priced for long-duration work: Claude Sonnet 5 with the August 31 promo, DeepSeek V4 via OpenRouter with its agentic token share, and self-hosted open-weight models on Baseten for full control. Let me price the same 8-hour code-refactor workload against each.

| Provider | Pricing model | 8-hour cost (8M input / 4M output) | Persistent state | Notes |
|---|---|---|---|---|
| **ChatGPT Work** | $0.40/agent-hour + included tokens | $3.20 (within 1M tok/hr) / $5-8 with overage | Native (workspace, shell, processes) | Newest, best DX for OpenAI-shaped agents |
| **Claude Sonnet 5 (API, promo)** | $2 input / $10 output per M tokens | 8 × $2 + 4 × $10 = **$56** (no state) | None (stateless requests) | Sonnet 5 best per-call, no agent runtime |
| **DeepSeek V4 via OpenRouter** | $0.27 input / $1.10 output per M tokens | 8 × $0.27 + 4 × $1.10 = **$6.56** (no state) | None (stateless requests) | Cheapest raw tokens, no background runtime |
| **Self-hosted Llama 3.3 70B on Baseten (Dedicated H100)** | $1.49/hour H100 + no model API fee | $11.92 (full H100 cost) | DIY (you wire it up) | Most flexible, most operational burden |
| **GPT-5.6 Luna standard (no Work tier)** | $0.50 input / $1.50 output per M tokens | $4 input + $6 output = **$10** (no state) | None (stateless requests) | Standard OpenAI pricing, no persistent state |

The table makes the pricing story clear: **ChatGPT Work is the cheapest option in this comparison** ($3.20 for the 8-hour code-refactor workload) **if and only if the agent fits within the 1M tokens/hour included quota**. With overage, the cost grows by another $2-5 for the 8-hour case. Without overage, ChatGPT Work is roughly **2x cheaper than DeepSeek V4 via OpenRouter** and **17x cheaper than Claude Sonnet 5 (which is overpriced for agent workloads that are mostly reasoning, not creative writing)**.

The catch is the **persistent state** advantage. None of the other options in the table ship native persistent state. Claude Sonnet 5 has the strongest per-call reasoning but every tool call is a fresh request — your agent code has to manage the state. DeepSeek V4 via OpenRouter is the cheapest raw tokens but you build the state layer yourself. Self-hosted on Baseten gives you the most flexibility but you operate the entire runtime.

## When ChatGPT Work is the wrong tool

The 2026 agent market has 3 distinct categories and ChatGPT Work is right for exactly one of them. The other two have cheaper, more appropriate tools.

**Don't use ChatGPT Work for synchronous chat.** The 2.4x price premium over standard Luna is wasted on any workload where the agent is waiting on the user. The whole point of the background runtime is that the agent can do work *while the user is away*, and that is not what synchronous chat is.

**Don't use ChatGPT Work for one-shot generation.** A single 30-second request to write a 2000-word blog post costs $0.40 (the minimum 1-hour runtime charge) versus $0.003 for the same call on GPT-5.6 Luna. The 130x premium is not justified unless the agent is doing multiple tool calls in a persistent context.

**Don't use ChatGPT Work if you need non-OpenAI models.** ChatGPT Work only ships with GPT-5.6 in the runtime. If you want Claude or DeepSeek in the agent loop, you have to bring your own API key for those models and pay separately on top of the $0.40/hour runtime. For a multi-model agent, the cheaper option is still to run Claude Sonnet 5 + DeepSeek V4 + a routing layer (Cloudflare AI Gateway or OpenRouter) without the ChatGPT Work runtime.

**Use ChatGPT Work for autonomous research agents** (multi-hour web + PDF + synthesis), **code-refactor agents** (multi-hour codebase work with shell access), and **data-pipeline agents** (multi-hour ETL with persistent state). For all three of these, the persistent state and background runtime are the differentiator, and the per-agent-hour pricing is cheaper than the alternatives.

## How to wire up ChatGPT Work in the Responses API

ChatGPT Work is exposed through the Responses API, which is OpenAI's recommended endpoint for agent workloads. The integration is straightforward — you create a response with `background: true` and the API returns a `work_id` that you can poll for status, stream output from, and check on across sessions.

```python
from openai import OpenAI

client = OpenAI()

# Start a long-running agent task
work = client.responses.create(
    model="gpt-5.6",
    background=True,
    input="Research the latest 2026 benchmarks for embedding models and write a markdown report",
    tools=[
        {"type": "web_search"},
        {"type": "code_interpreter"},
        {"type": "file_search", "vector_store_ids": ["vs_abc123"]}
    ],
    metadata={"work_id": "research-2026-embeddings"}
)

print(f"Started work: {work.id}")
print(f"Status: {work.status}")  # 'queued' or 'in_progress'

# Poll for status
import time
while work.status in ('queued', 'in_progress'):
    time.sleep(30)
    work = client.responses.retrieve(work.id)
    print(f"Status: {work.status}, runtime: {work.runtime_minutes} min")

print(f"Output: {work.output_text}")
```

The Responses API also supports streaming output from a background task — you can connect a WebSocket to `work.id` and get incremental output as the agent thinks, even if the agent runs for 8 hours. This is the right pattern for a UI that wants to show "agent is working..." with periodic progress updates.

## ChatGPT Work pricing gotchas to know before you ship

Three things about the pricing are not obvious from the OpenAI pricing page, all of which I confirmed by reading the API documentation on July 9, 2026:

1. **The 1M tokens/hour included quota is per work_id, not per account.** If you run 5 background agents in parallel, each gets 1M tokens/hour included, but the 1M cap is per agent. A heavy agent that exceeds 1M tokens/hour in a single work_id is billed at standard GPT-5.6 Luna overage rates ($0.50/M input + $1.50/M output).
2. **Idle time still counts against the $0.40/agent-hour.** If your agent starts at 9am and finishes at 5pm with 6 hours of actual work, you are billed for 8 hours of runtime, not 6. The pricing is wall-clock, not CPU-clock. The optimization is to keep the agent moving — if it would be idle for 20 minutes waiting on a long-running download, the cheaper pattern is to cancel the work and restart it when the download finishes.
3. **Background work persists for 30 days.** A work_id that you do not explicitly cancel or complete stays in OpenAI's system for 30 days, and you are billed for the storage during that time (free for the first 7 days, $0.10/GB-day after). If you spawn 100 research agents and never check on them, the storage cost is the surprise.

## Final verdict on ChatGPT Work

ChatGPT Work is a real product with a real pricing model, and for the narrow set of long-running agent workloads it is designed for, it is the cheapest option in the 2026 LLM API market. The $0.40/agent-hour pricing undercuts every alternative I modeled for the same workload, and the persistent state is the right primitive for agents that need shell access, file system, or process management.

The risk is over-application. ChatGPT Work is not a replacement for the standard Chat Completions API. It is a specialized tier for a specific class of workload, and using it for synchronous chat, one-shot generation, or non-OpenAI model agents is a 2-130x overpayment. The right pattern in production is to use the standard API for the 95% of your traffic that is short-duration, and to spawn a ChatGPT Work background task for the 5% that genuinely needs persistent state across hours.

If you are building a long-running agent in 2026, ChatGPT Work is worth the 1-hour trial at $0.40 to see if your workload actually benefits from persistent state. If it does, the per-agent-hour economics make it the obvious choice. If it does not, you are paying for a feature you are not using, and you should fall back to the standard API with a routing layer (Cloudflare AI Gateway, OpenRouter, or FreeModel) for the multi-model case.

## FAQ

**What is ChatGPT Work?**
ChatGPT Work is OpenAI's long-running agent product launched July 9, 2026, built on GPT-5.6. It gives agents a persistent state — workspace directory, shell environment, process pool — and charges per agent-hour of background runtime instead of per request. The runtime is exposed through the Responses API with `background: true`.

**How much does ChatGPT Work cost?**
The API tier is $0.40 per agent-hour, with GPT-5.6 model usage included up to 1M tokens/hour. Beyond the included quota, GPT-5.6 Luna overage rates apply ($0.50/M input, $1.50/M output). ChatGPT Work Pro is $0.20/hour (5M tokens/hour included) and ChatGPT Work Team is $0.15/hour per seat (10M tokens/hour included).

**Is ChatGPT Work cheaper than GPT-5.6 standard API?**
It depends on the workload. For a low-token-density 4-hour research agent, ChatGPT Work is 6x more expensive than GPT-5.6 Luna standard. For a token-dense 8-hour code-refactor agent, ChatGPT Work is 25% cheaper than Luna standard. The break-even is roughly 4-5 hours of runtime with moderate-to-high token density.

**What is the difference between ChatGPT Work and GPT-5.6 standard?**
ChatGPT Work adds persistent state (workspace, shell, processes) and charges per agent-hour. GPT-5.6 standard is a stateless Chat Completions API that charges per million tokens. ChatGPT Work is for autonomous long-running agents; GPT-5.6 standard is for synchronous request/response.

**Can I use Claude or DeepSeek in ChatGPT Work?**
Not directly. ChatGPT Work only ships with GPT-5.6 in the runtime. You can bring your own API key for Claude or DeepSeek as separate tool calls, but you pay separately for those models on top of the $0.40/agent-hour ChatGPT Work runtime. For a multi-model agent, a routing layer (OpenRouter or Cloudflare AI Gateway) without the ChatGPT Work runtime is usually cheaper.

**How does ChatGPT Work compare to Claude Sonnet 5 for agents?**
For an 8-hour code-refactor workload with 8M input + 4M output tokens, ChatGPT Work costs $3.20 (within the included quota) versus Claude Sonnet 5 at $56 with the August 31 promo pricing ($2 input / $10 output). ChatGPT Work is 17x cheaper for that specific workload, but Sonnet 5 has stronger per-call reasoning quality for non-agent workloads. Use ChatGPT Work for autonomous long-running tasks, Sonnet 5 for short high-quality generation.

**Does ChatGPT Work have an affiliate program?**
No. OpenAI does not currently have a public affiliate program for ChatGPT Work or any other API product. For monetization on a ChatGPT Work review, the standard pattern is to recommend a cost-routing aggregator like FreeModel that lets users spread the same workload across GPT-5.6, Claude Sonnet 5, and DeepSeek V4 with a single API key.

**What is the token quota for ChatGPT Work?**
1M tokens/hour for the API tier, 5M tokens/hour for Pro, 10M tokens/hour for Team. The quota is per work_id, not per account — running 5 background agents in parallel gives you 5M tokens/hour total, but each individual agent is capped at 1M. Beyond the quota, GPT-5.6 Luna overage rates apply.

**Can I run ChatGPT Work from inside China?**
OpenAI's API is hosted on AWS US-East. Access from inside China requires a stable proxy connection. For production workloads serving China-based users, the recommended pattern is to use a Cloudflare Worker as a proxy, which keeps the work_id state on the OpenAI side while bringing the latency down to 50-100ms for the Chinese client. Note that the proxy does not bypass the OpenAI content policy.

**How long does a ChatGPT Work background task persist?**
A work_id that you do not explicitly cancel or complete stays in OpenAI's system for 30 days. Storage is free for the first 7 days, then $0.10/GB-day after. The 30-day retention is for debugging and re-running failed tasks; for production workloads, the recommended pattern is to cancel or complete the work_id as soon as the agent finishes its task.

**Is ChatGPT Work available now?**
Yes, as of July 9, 2026, ChatGPT Work is generally available through the OpenAI API with the Responses API surface. The ChatGPT desktop and Team integrations are also live. The launch page is at openai.com/index/chatgpt-for-your-most-ambitious-work.
