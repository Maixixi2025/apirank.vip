---
title: "Tavily 2026: Search API for AI Agents: Full API Review"
description: "Tavily API review: the search layer inside LangChain, LlamaIndex, and AutoGen. 1000 free calls/month, built-in AI summarization, Research mode for multi-step agent workflows. Pricing, pros/cons, and how it compares to Jina AI, Exa, and SerpAPI."
slug: "tavily-api-review"
provider: "tavily"
published: true
date: "2026-06-28"
type: "review"
---

# Tavily 2026: The Search API That Agent Frameworks Actually Pick

## What is Tavily, and why is it the default search API in 2026?

Tavily is a search API purpose-built for AI agents. Where Google Custom Search and SerpAPI return ten blue links and a sitemap, Tavily returns the answer — a structured JSON object with the raw page content, a relevance score, an AI-generated summary, and a citation graph. The first call is the only call. For an agent in the middle of a multi-step research task, that single-call paradigm is the difference between a workflow that finishes in eight seconds and one that finishes in eight minutes.

The platform matters to an AI engineer in 2026 for three reasons that have nothing to do with the usual "search API" comparison table:

1. **It is the default in every major agent framework.** LangChain's `TavilySearchResults` tool, LlamaIndex's `TavilyToolSpec`, AutoGen's `TavilySearchTool`, CrewAI's `TavilySearchTool`, and smolagents' `TavilySearchTool` all call the same API. When a developer writes a RAG agent in 2026 and types "search the web", the first autocomplete suggestion is Tavily. This network effect is more important than any individual pricing tier.

2. **The 1,000-calls-per-month free tier is real production quota, not a watermarked demo.** No credit card, no quota approval, no 7-day trial. The free tier hits the same backend as the paid tier, with the same latency and the same result quality. A solo developer or a small team can run a 24/7 research agent on the free tier and only pay when the workflow actually takes off.

3. **Research mode replaces a hand-rolled multi-step loop.** The Research endpoint (released December 2025, generally available since February 2026) takes a single natural-language query and runs the multi-step planning, search, extraction, and synthesis loop itself, returning a structured research brief. This used to require 50-100 lines of agent code; now it is a single API call.

This review covers the Tavily API from the perspective of an engineer evaluating it in late June 2026: the Search / Extract / Crawl / Research endpoint catalog, the pricing model across each endpoint, the OpenAI-compatible quirks (or lack thereof), the agent-framework integration surface, and how Tavily compares to Jina AI, Exa, and SerpAPI for the same workloads.

## The Tavily endpoint catalog in 2026

Tavily exposes six endpoints, each designed for a specific stage of an agent's information-gathering loop. The endpoint catalog has been stable since the Research GA in February 2026; new endpoints land roughly once per quarter.

| Endpoint | Purpose | Free tier | Paid per call |
|---|---|---|---|
| **Search** | Real-time web search with AI summary | 1,000/month | $0.008 |
| **Extract** | Pull clean markdown from a known URL | 1,000/month | $0.002/page |
| **Crawl** | BFS from a root URL, return all reachable pages | 500 pages/month | $0.001/page |
| **Map** | Sitemap-level discovery of a domain | 500/month | $0.001/page |
| **Research** | Multi-step search + synthesis, returns a brief | 50/month | $0.04 |
| **AI Extraction** | Structured extraction with a JSON schema | 1,000/month | $0.005 |

The split between Search and Extract is deliberate. Search is for discovery (you don't know which URL has the answer); Extract is for ingestion (you have a URL and you need the content). Most agent workflows call Search to find candidate URLs, then Extract to ingest the top three, then loop.

Crawl is the cheaper alternative when you need to ingest an entire domain — useful for building a knowledge base from a documentation site. Map sits between Search and Crawl: it gives you the URL topology of a domain without fetching the content, which is what you want when you are building a planning agent that needs to decide which sub-pages to read.

Research is the most expensive endpoint, but the per-call price is misleading: a single Research call replaces what would otherwise be 5-10 Search calls plus 2-3 Extract calls plus a synthesis LLM call. For multi-step research workflows, Research is the cheapest path to a structured answer.

## Tavily pricing: how the credits work in practice

Tavily uses a credit system where each endpoint consumes a different number of credits per call. The free tier is 1,000 credits per month, which sounds small until you realize that Search costs 1 credit per call, Extract costs 1 credit per page, Crawl costs 1 credit per page, and Research costs 5 credits per call.

For a solo developer running a daily research agent that does 20 Search calls and 3 Extract calls per day, monthly credit consumption is roughly 690 — well within the free tier. A small team with three production agents each doing 200 Search calls per day plus weekly Crawl runs of ~5,000 pages per agent consumes about 50,000 credits per month, which on the paid tier is approximately $80.

The paid tiers (as of June 2026) are:

| Plan | Monthly price | Credits included | Overage |
|---|---|---|---|
| Free | $0 | 1,000 | None — over-quota returns 429 |
| Developer | $30 | 4,000 | $0.008/credit |
| Growth | $200 | 40,000 | $0.006/credit |
| Pro | $1,000 | 250,000 | $0.005/credit |
| Enterprise | Custom | Custom | Custom |

The Developer tier is where most production agents land. The Growth tier is the inflection point where the volume discount starts to matter; above 40,000 credits per month, the marginal rate drops to $0.006, which is 25% cheaper than the Developer overage. Above 250,000 credits per month, the Pro tier's $0.005 marginal rate is meaningful for workloads that ingest large documentation sites.

For workloads that exceed 1 million credits per month, the Enterprise tier includes a dedicated search index, a custom rate-limit ceiling, and a service-level agreement on latency. None of the public-case-study customers have published their actual rate, but the Enterprise tier is roughly $5,000-15,000 per month depending on the SLA and the geographic search coverage required.

## What the Search endpoint actually returns

The Search endpoint is the one most developers start with, and the response shape is the one most people copy into their agent code without reading. A typical Search response for the query "OpenAI moderation API pricing 2026" looks like:

```json
{
  "query": "OpenAI moderation API pricing 2026",
  "follow_up_questions": null,
  "answer": "OpenAI's moderation API is free for all accounts as of June 2026. The endpoint om-preview costs $0 when called against any tier model. Rate limits depend on the account type, not the model tier.",
  "images": [],
  "results": [
    {
      "url": "https://platform.openai.com/docs/guides/moderation",
      "title": "Moderation - OpenAI API",
      "content": "The moderation endpoint is free to use for all OpenAI API accounts...",
      "raw_content": "<full extracted markdown of the page>",
      "score": 0.92
    },
    {
      "url": "https://openai.com/index/previewing-gpt-5-6-sol",
      "title": "Previewing GPT-5.6 Sol",
      "content": "OpenAI's safety team announced on June 25, 2026...",
      "raw_content": "...",
      "score": 0.78
    }
  ],
  "response_time": 1.42
}
```

The interesting fields are `answer` (a Tavily-generated summary grounded on the search results), `results[].raw_content` (the full extracted markdown of the source page, ready to feed to a downstream LLM), and `results[].score` (a 0-1 relevance score that an agent can use to decide whether to extract the page or move on).

For a RAG agent, this response shape is exactly what you want: the answer for direct answering, the raw content for grounded synthesis, and the score for filtering. Most alternatives (SerpAPI, Google Custom Search, Bing Search API) return only the titles and snippets; the agent then has to make a second API call to Extract the actual content. Tavily's single-call design saves 2-5 seconds per research step.

## How Tavily compares to Jina AI, Exa, and SerpAPI

The "search API for AI" space is crowded in 2026. Here is how Tavily stacks up against the three alternatives an engineer is most likely to compare it to:

| Dimension | Tavily | Jina AI | Exa | SerpAPI |
|---|---|---|---|---|
| Default in LangChain | ✅ | ✅ | ✅ | ❌ |
| Built-in AI summary | ✅ | ❌ | ✅ | ❌ |
| Free tier | 1,000/month | 1M tokens (read) | 1,000/month | 100/month |
| Search cost | $0.008 | $0.00006/token | $0.005/result | $0.01 |
| Extract cost | $0.002/page | $0.00006/token | $0.025/page | ❌ |
| Crawl cost | $0.001/page | ❌ | $0.025/page | ❌ |
| Research endpoint | ✅ | ❌ | ✅ | ❌ |
| Latency (P50) | 1.4s | 0.6s | 1.1s | 1.8s |
| Self-hosted | ❌ | ❌ | ❌ | ❌ |

**vs. Jina AI**: Jina's Reader API is cheaper (token-based pricing, ~$0.06 per 1M tokens) and faster (0.6s vs 1.4s P50), but Jina is fundamentally a content-extraction API, not a search API. To use Jina for search, you pair it with a separate search backend (often SerpAPI or Bing). For a workload that already has a search engine and just needs clean extracted content, Jina is the right call. For a workload that wants search + extract in one call, Tavily wins.

**vs. Exa**: Exa's neural search is more semantically accurate for ambiguous queries (it understands "papers on RLHF" not just keyword match), but it costs roughly 2x Tavily for the same call volume, and the free tier is the same. Exa is the right pick for research workflows where query semantics matter more than call cost.

**vs. SerpAPI**: SerpAPI is a Google-results scraper, not an AI search API. It returns ten blue links and a snippet, just like Google. For an agent that needs to do its own extraction and synthesis, SerpAPI plus Jina plus an LLM is a three-API workflow that costs more and runs slower than a single Tavily call. SerpAPI is the right pick only when you specifically need Google ranking data (for SEO tooling) or when you need a search API that bypasses AI summarization entirely.

## Tavily in production: the operational quirks that matter

The marketing page says "1.4 second P50 latency". The actual operational experience in mid-2026 has three quirks worth knowing about before you ship a production agent on Tavily.

**1. Free tier rate limits reset on a rolling 30-day window, not a calendar month.** If you sign up on June 15, your free tier resets on July 15, not August 1. For a team that started the month on the 25th, the first 10 days of the next month are still on the old quota. This is more user-friendly than a calendar reset (you do not lose credits by signing up late in the month) but it means budget forecasting needs to track the rolling window, not the calendar.

**2. Crawl and Search have separate quotas on the free tier.** The free tier gives you 1,000 Search credits AND 500 Crawl pages per month. If you run a single big Crawl that exhausts the Crawl quota on day 3, you still have your Search quota intact but you cannot crawl any more pages until the window resets. The paid tiers consolidate these into a single credit pool.

**3. The AI-generated `answer` field can hallucinate on multi-hop queries.** When the user query requires reasoning across multiple search results (e.g. "Which country has the most regulations on LLM fine-tuning?"), the `answer` field can produce a confident-sounding but incorrect synthesis. The safer pattern is to ignore `answer` for multi-hop queries and feed the raw `results[].raw_content` into your own LLM for synthesis. Tavily's documentation warns about this, but the warning is buried in the API reference, not the quickstart.

## The Research endpoint: when to use it and when to roll your own

The Research endpoint is Tavily's most ambitious product and the one most likely to be misjudged. The marketing pitch — "describe a research question, get a structured brief" — is accurate, but the failure modes are subtle.

A Research call returns:

```json
{
  "query": "Compare the pricing models of the top 5 LLM API providers in 2026",
  "answer": "...",
  "sources": [...],
  "research_steps": [
    {"step": 1, "query": "top LLM API providers 2026", "results": 5},
    {"step": 2, "query": "OpenAI GPT-5.5 pricing 2026", "results": 3},
    ...
  ],
  "citations": [...],
  "response_time": 18.3
}
```

The `research_steps` array is the most useful field for an agent. It shows the multi-step plan that the Research endpoint actually executed, which means you can log it, audit it, and even replay it manually if the result is wrong. This is significantly better than the black-box "I researched this for you" output that most AI research tools return.

The cost is $0.04 per Research call, which is 5x a Search call. But the alternative — your agent making 10 Search calls plus 5 Extract calls plus a synthesis LLM call plus the loop orchestration — costs roughly $0.15 and takes 25-35 seconds. Research is cheaper, faster, and gives you a better-structured result. For any research workflow that needs 5+ search steps, use Research.

The one place where Research is the wrong choice is when you need fine-grained control over the search strategy. If you want to filter sources by domain, weight by recency, or skip certain content types, Research is too opaque — you will end up needing to call Search and Extract yourself with custom logic.

## What about the Tavily MCP server?

Tavily launched a Model Context Protocol (MCP) server in March 2026, and as of June 2026 it is the most-installed MCP server in the Claude Desktop and Cursor ecosystems. The MCP server exposes the Search and Extract endpoints as standard MCP tools, which means any MCP-compatible agent (Claude Code, Codex, Cursor, Cline) can call Tavily without writing a line of integration code.

For a developer evaluating agent stacks, this is the path of least resistance: install the Tavily MCP server, restart your editor, and you have search and extraction as native agent actions. The MCP server costs the same as calling the API directly — no MCP markup, no MCP-only pricing tier.

The MCP server does have one limitation: it does not expose the Research endpoint, only Search and Extract. For multi-step research workflows, you still need to call the Research endpoint from your agent code, not from the MCP server.

## Should you use Tavily or another provider for your agent?

The decision matrix for 2026 is straightforward:

- **You are building a RAG agent in 2026 and you want the path of least resistance.** Use Tavily. It is the default in every major framework, the free tier is enough for prototyping, and the single-call Search+Extract paradigm eliminates the need to glue three APIs together.
- **You are running an existing search pipeline and just need clean content extraction.** Use Jina AI. It is cheaper, faster, and the token-based pricing scales with the size of what you extract, not the number of pages.
- **You are building a research agent that needs semantic search over academic papers or niche domains.** Use Exa. Its neural search understands query semantics in a way that keyword search cannot.
- **You are building an SEO tool that needs Google ranking data.** Use SerpAPI. It is the only one of the four that returns real Google SERPs.
- **You are running a workload above 1 million API calls per month and need custom rate limits.** Use Tavily Enterprise. The dedicated search index and custom rate limits are worth the price for that scale.

For most AI engineers building agents in 2026, the answer is Tavily. The integration is the cheapest, the free tier is the most generous, and the Research endpoint is the only one of the four that actually does multi-step research as a single call. The operational quirks are real but manageable, and the MCP server eliminates the integration tax entirely.

## What is Tavily's data retention policy?

Tavily does not retain search queries or results beyond what is needed to operate the service. The `query` and `results` payloads are processed in memory, scored, and returned; they are not logged to a persistent store. The only persistent logs are aggregate rate-limit counters and billing records, which contain metadata (timestamp, endpoint, credit cost) but not the query or result content.

For enterprise customers, Tavily offers a "no logs" contract addendum that further restricts even the aggregate metadata. This is the right tier for workloads in healthcare, finance, or government where query content itself is regulated.

## Can I self-host Tavily?

No. Tavily is a hosted-only service. The search index, the extraction pipeline, and the Research endpoint's multi-step planning all run on Tavily's infrastructure, and the company has not published a self-hosting option. For workloads that require self-hosting, the closest alternatives are:

- **SearXNG** (free, open-source meta-search, but no AI summary or Research endpoint)
- **Meilisearch** (free, open-source full-text search, but you need to bring your own content)
- **Exa's on-prem enterprise tier** (custom contract, requires Exa sales engagement)

For most production agents in 2026, hosted-only is fine — the alternative is a self-hosted search stack that costs more in engineering time than the API bill would have been.

## How does Tavily handle rate limits and quota overage?

The free tier returns HTTP 429 when you exceed the 1,000-credit monthly quota. There is no overage billing on the free tier — your agent stops working until the window resets. This is a strict but predictable behavior; the worst case is that your agent returns "I am unable to search right now" instead of a surprise bill.

The paid tiers have overage billing, with the marginal rate depending on the plan ($0.008/credit on Developer, $0.005/credit on Pro). You can set a hard spend cap in the dashboard, which will turn back into the 429 behavior once you hit the cap. This is the right default for production agents — runaway agent loops have generated some of the more spectacular API bills in 2026, and a hard cap is the cheapest insurance.

## What is the difference between Tavily and an LLM with browsing?

OpenAI's browsing-enabled GPT models, Anthropic's web search tool, and Google's Gemini with Search Grounding all return answers grounded on real-time web data. The difference is in the output shape and the integration model.

An LLM with browsing returns a synthesized natural-language answer. It does not give you the raw search results, the page contents, or the citation graph. For a chatbot, this is the right shape. For an agent that needs to do further work on the search results — extract structured data, store them in a vector database, chain them with other tool calls — Tavily is the right shape.

The other difference is reliability. Browsing-enabled LLMs occasionally fail to follow redirects, get stuck on JavaScript-heavy pages, or return hallucinated citations. Tavily's pipeline is purpose-built for the agent use case, so the failure modes are different and more predictable. For a production agent that needs to handle a wide range of web content reliably, Tavily is the more dependable backend.

## Final verdict

Tavily in 2026 is the search API for AI agents in the same way that Stripe is the payment API for SaaS: not the only option, but the one that every framework defaults to, the one with the most generous free tier, and the one with the lowest integration cost. The Research endpoint is a genuine differentiator — no other hosted search API does multi-step research as a single call — and the MCP server is the path of least resistance for the Claude Code / Cursor / Codex crowd.

The operational quirks (rolling quota windows, separate Crawl quota, `answer` field hallucinations on multi-hop queries) are real but manageable. The hosted-only constraint is a real limitation for some enterprise workloads, but for the long tail of AI engineers building agents, hosted-only is the right trade.

For a solo developer prototyping an agent, the free tier is enough to ship a production-quality demo. For a team running a production agent at scale, the Developer or Growth tier is the right starting point, with the Pro tier as the inflection point for high-volume workloads. The Enterprise tier is for the small number of workloads that need custom rate limits and a no-logs contract.

If you are building an agent in 2026 and you have not yet picked a search API, the answer is Tavily. The cost is competitive, the integration is free, and the framework default means you will spend your engineering time on the agent logic instead of the search backend.

## FAQ

**Does Tavily work with OpenAI's function calling?**
Yes. The Search, Extract, Crawl, Map, and Research endpoints are all OpenAI-compatible tool definitions. You can pass them as tools in any OpenAI / Anthropic / Google function-calling call, and the LLM will return a structured tool call that you forward to the Tavily API. The response shape is JSON, not OpenAI-specific, so it works equally well with Anthropic's tool use, Google's function calling, and any other tool-calling standard.

**Is there a Tavily free tier for production workloads?**
The free tier is 1,000 credits per month on a rolling 30-day window. For most prototyping and personal-project workloads, this is enough. For production workloads that exceed 1,000 credits per month, the Developer tier at $30/month (4,000 credits, $0.008 overage) is the right starting point.

**Can I use Tavily from inside China?**
Tavily's API is hosted on AWS US-East and EU-West. Access from inside China requires a proxy, and the latency from a CN-based client is typically 200-400ms. For China-based production workloads, the recommended pattern is to use a Cloudflare Worker or a Tencent Cloud edge function as a proxy, which brings the latency down to 50-100ms and avoids the need for client-side proxy configuration.

**How does Tavily handle the same query from multiple users?**
Tavily does not deduplicate or cache results across users. Each Search call is independent, and the same query from two different users returns the same results but counts as two credits. For workloads with repeated queries, the recommended pattern is to add a small Redis cache in front of the Tavily call — for a customer support agent, the same top 20 questions get asked 80% of the time, and a 30-second TTL cache can cut credit consumption by 60-80%.

**What models does Tavily's Research endpoint use?**
Tavily does not publish the model stack behind the Research endpoint. The endpoint is a managed multi-step agent, not a single LLM call, and the company treats the underlying model selection as proprietary. The output quality is consistent with a frontier model (GPT-5.5 / Claude Opus 4.5 / Gemini 3.5 class), but the exact model and the synthesis prompt are not disclosed.

**Does Tavily support streaming?**
The Search, Extract, and Crawl endpoints return complete JSON responses and do not support streaming. The Research endpoint added streaming output in April 2026, returning the research steps as they complete. For an agent that needs to show progress to the user, the Research streaming output is the right pattern; for a backend agent that does not need to show progress, the non-streaming endpoints are simpler to integrate.

**Is Tavily OpenAI-compatible?**
No. Tavily uses its own API surface, not OpenAI's chat completions format. The endpoints are REST POST calls returning JSON, not OpenAI-style chat completions. However, the JSON response shape is designed to be agent-friendly — you can drop the `results[].raw_content` directly into a downstream LLM call as a context block.

**How does Tavily compare to Perplexity's API?**
Perplexity's API is a different product — it returns synthesized natural-language answers, not structured search results. For a chatbot that needs a single answer to a question, Perplexity is the right call. For an agent that needs to do further work on the search results, Tavily is the right call. The two APIs serve different use cases and are not direct competitors.

**Can I use Tavily for SEO keyword research?**
Not directly. Tavily does not return SERP rankings, keyword volumes, or any SEO-specific data. For SEO tooling, use SerpAPI (which returns real Google SERPs) or a dedicated SEO tool like Ahrefs / Semrush / DataForSEO. Tavily is for content discovery, not ranking analysis.

**What is the Tavily affiliate program?**
Tavily does not currently have a public affiliate program. The website does not list one, and the dashboard does not have an "affiliate" or "referral" section. For a content site that wants to monetize Tavily coverage, the right pattern is to use Tavily's API for the content creation workflow (research, fact-checking) and link to the platform as a tool recommendation, not as an affiliate partner.

---

**Reviewed against**: Tavily API documentation (docs.tavily.com), LangChain TavilySearchResults tool reference, LlamaIndex TavilyToolSpec reference, MCP server release notes (March 2026), Research endpoint GA announcement (February 2026), community reports on free-tier rate limits (June 2026).

**Disclosure**: This article contains affiliate links. If you sign up through these links, we may earn a commission at no extra cost to you. Our reviews remain independent.
