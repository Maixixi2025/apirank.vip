---
title: "Mem0 2026: The AI Agent Memory Layer Standard"
slug: mem0-api-review
date: 2026-07-23
lang: en
locale: en
provider: mem0
providerFeatured:
  - mem0
  - openai
  - anthropic
  - freemodel
primaryAffiliate: freemodel
affiliateUrl: https://freemodel.dev/invite/FRE-7a3b6220
type: review
category: aggregator
---

# Mem0 2026: The Memory Layer Standard for Production AI Agents

Mem0 is the memory layer that production AI agents reach for in 2026, and the one 60,000+ developers have starred on GitHub for adding long-term, personalized context to LLM applications without hand-rolling a vector store, fact-extraction pipeline, and forgetfulness filter. Verified on 2026-07-23, Mem0 is **the** open-source (Apache-2.0, 61,493 stars) memory layer behind customer-support bots that remember a returning user's last ticket, personal-assistant apps that recall dietary preferences across sessions, multi-character chat applications, and the new generation of agent frameworks (LangChain, LlamaIndex, CrewAI, AutoGen, Mastra) that treat memory as a first-class primitive.

This review walks through what Mem0 does that hand-rolled RAG + vector store does not, the verified 2026 pricing (Hobby free with 10,000 memories, Starter at $19/month with 50,000 memories, Pro at $249/month with unlimited memories and Graph Memory, Enterprise contract for SSO/audit/on-prem), how to wire Mem0 into a LangChain or vanilla OpenAI/Anthropic agent in a few lines of Python or TypeScript, and how Mem0 compares to alternatives (Zep, Letta, Redis vector search, custom Pinecone + LLM fact extraction). The numbers come from the Mem0 pricing page (verified live 2026-07-23), the mem0ai/mem0 GitHub repository (last commit 2026-07-23), and the Mem0 documentation.

If you are building an AI agent in 2026 and you want skip the "build-your-own-fact-extraction-pipeline" tax without giving up control over what gets remembered, this is the reference guide.

## What Mem0 does (and what it does not)

Mem0 is a **memory layer for AI applications**, not an LLM router, gateway, or vector database on its own. It sits between your application code and your LLM, extracting facts from conversations, storing them in a structured (and optionally vector-indexed) memory store, retrieving relevant memories at query time, and feeding them back into the LLM prompt as context. The core abstraction is `memory.add()` and `memory.search()` — the platform handles the rest.

Core capabilities (verified 2026-07-23 from Mem0 docs and pricing page):

- **Automatic fact extraction.** When you call `memory.add(messages=[...])`, Mem0 uses an LLM (configurable; defaults to a fast model like GPT-4o-mini) to extract atomic facts from the conversation. A chat like "I'm allergic to shellfish and I prefer dark mode" becomes two stored memories: `{"role": "user", "content": "User is allergic to shellfish"}` and `{"role": "user", "content": "User prefers dark mode"}`. This is the killer feature — without it, you would write the extraction prompt, manage the JSON parsing, and decide what to forget yourself.

- **Vector + structured hybrid storage.** Mem0 stores memories as both structured JSON (for direct queries) and vector embeddings (for semantic search). The default vector store is Qdrant (self-hosted or Qdrant Cloud), but you can swap in Pinecone, Weaviate, Chroma, pgvector, or Redis. The Cloud SaaS deploys a managed vector store for you; the self-hosted version uses whatever you configure.

- **Configurable LLM provider.** Mem0 supports 8+ LLM providers out of the box: OpenAI (GPT-4o, GPT-4-Turbo, GPT-3.5), Anthropic (Claude 3.5 Sonnet, Haiku, Opus), Google (Gemini 1.5 Pro/Flash), Mistral (Large, Mixtral, Mistral-7B), Groq (Llama 3.1 70B, Mixtral), Ollama (any local model), AWS Bedrock (Claude / Llama / Titan), and Azure OpenAI. The same SDK call works against any of them — you only swap the `LLM_PROVIDER` and `LLM_API_KEY` env vars.

- **Graph Memory (Pro tier and up).** Beyond vector-based memory, Mem0 Pro adds a graph store that tracks entity relationships — if a user mentions "my wife Sarah" and later "Sarah's birthday", the graph links the two and surfaces the relationship at retrieval time. This is what differentiates Mem0 from a vanilla RAG system: it remembers not just facts but relationships.

- **Multi-user isolation via user_id.** Every memory call takes a `user_id` (and optionally `agent_id`, `run_id`, `app_id`). The store partitions memories by user automatically, so a single Mem0 instance can serve thousands of users without cross-contamination. This is the foundation of any production multi-tenant agent.

- **Self-hostable with Docker.** The open-source `mem0ai/mem0` repo ships a complete Docker Compose setup that bundles the API server, a vector store, an LLM worker, and an optional Neo4j instance for graph memory. You can run it on any cloud (AWS, GCP, Azure, Aliyun, Tencent Cloud) without proxying through Mem0's Cloud SaaS.

### What Mem0 does NOT do

- **No LLM inference itself.** Mem0 is not an LLM provider. You still need an OpenAI / Anthropic / Gemini API key for fact extraction and for your main agent loop. Mem0 orchestrates; it does not generate.

- **No RAG-as-a-service.** Mem0 handles *conversation memory*, not document retrieval. If you want to search across a corpus of PDFs and cite them, you want a vector database like Pinecone or Weaviate (not Mem0). The two are complementary: use Mem0 for user-specific conversational memory, use a vector DB for document-level retrieval.

- **No agent orchestration.** Mem0 does not run the agent loop. You still use LangChain / LlamaIndex / CrewAI / AutoGen / Mastra / your own code to orchestrate tool calls, planning, and execution. Mem0 is the memory layer, not the brain.

- **No built-in UI for memory inspection.** Mem0 ships a Cloud dashboard for browsing memories in the SaaS version, but the self-hosted version is API-only. If you want a polished memory-explorer UI for non-engineers, you will need to build one or use Mem0 Cloud.

## Verified 2026 pricing (from mem0.ai/pricing, checked 2026-07-23)

Mem0 ships four tiers. The numbers below were captured live from `mem0.ai/pricing` on 2026-07-23 — re-verify before any procurement decision since Mem0 has adjusted its Hobby/Starter quotas twice in 2024-2025.

### Hobby (free)

- **$0 / month** — no credit card required
- **10,000 memories** stored (memory entries, not bytes)
- **1,000 retrieval API calls / month**
- Unlimited end users
- 1 project
- Community support (Discord + GitHub issues)
- Best for prototyping, side projects, and personal use

### Starter ($19/month)

- **$19 / month**
- **50,000 memories** stored
- **5,000 retrieval API calls / month**
- Unlimited end users
- 1 project
- Community support
- Best for solo builders shipping their first AI agent or chat application with paying users

### Pro ($249/month)

- **$249 / month**
- **Unlimited memories** stored
- **50,000 retrieval API calls / month**
- Unlimited end users
- **Multiple projects support**
- **Graph Memory** (entity-relationship tracking on top of vector memory)
- **Advanced Analytics** (memory growth, retrieval hit rates, latency dashboards)
- **Private Slack channel** for support
- Best for growing AI products with thousands of active users, or teams that need Graph Memory for entity-aware retrieval

### Enterprise (custom contract)

- **Custom pricing** (typically starts at $1,000-$2,500/month for mid-market)
- Unlimited memories
- Unlimited retrieval API calls
- **On-prem deployment** (Docker / Kubernetes, no data leaves your VPC)
- **SSO** (Okta, Azure AD, Google Workspace)
- **Audit logs** (SOC 2 Type II readiness)
- **Custom SLAs** (typically 99.9% or 99.95%)
- Best for regulated industries (finance, healthcare, government), or any team with a strict data-residency requirement

### Hidden costs to know about

- **LLM costs are on top.** Mem0 uses an LLM for fact extraction (and one for the optional re-ranking step at retrieval time). The Hobby/Starter/Pro pricing does NOT include LLM tokens. A high-traffic app doing millions of memory adds can rack up $200-$500/month in OpenAI or Anthropic API costs that are completely separate from the Mem0 subscription.
- **Retrieval quota vs. add quota asymmetry.** A typical chat-app pattern is 1 add (on every user message) + 1 search (before every assistant reply). On the Hobby plan, 1,000 searches/month = ~33 messages/day — not enough for a real product. The Starter plan at 5,000 searches = ~166 messages/day is the realistic minimum for a small production app.
- **Vector store add-on for Cloud users.** Mem0 Cloud ships with a managed Qdrant instance, but if you want Pinecone / Weaviate / pgvector, you pay those vendors separately. The Cloud subscription covers Mem0's API and graph layer, not the underlying vector DB.
- **Graph Memory storage cost.** If you turn on Graph Memory on Pro, Neo4j (or Mem0's managed equivalent) becomes part of your deployment. Expect +$50-$200/month for a managed Neo4j cluster on AWS/GCP at typical Pro workloads.

## How Mem0 fits into an AI Agent pipeline

Mem0 sits between your agent framework and your LLM. The minimal pattern is:

```python
from mem0 import Memory
from openai import OpenAI

# 1. Initialize memory
memory = Memory()

# 2. Add memories from a conversation
messages = [
    {"role": "user", "content": "I'm allergic to shellfish and I prefer dark mode."},
    {"role": "assistant", "content": "Got it, I'll remember both."}
]
memory.add(messages, user_id="user-12345")

# 3. Retrieve relevant memories before the next LLM call
relevant = memory.search(
    query="What food should I avoid?",
    user_id="user-12345",
    limit=5
)

# 4. Inject memories into the prompt
context = "\n".join([m["memory"] for m in relevant["results"]])
system_prompt = f"You are a helpful assistant. User context:\n{context}"

# 5. Call the LLM with the augmented prompt
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "What's a good restaurant for tonight?"}
    ]
)
print(response.choices[0].message.content)
```

The same pattern works in TypeScript, Java, Go, and Ruby. Mem0's SDKs are first-class (not community-maintained) and ship with TypeScript types out of the box.

For LangChain users, Mem0 provides a drop-in `Mem0ChatMemory` class that integrates with `ConversationChain`, `AgentExecutor`, and `RunnableWithMessageHistory`. For LlamaIndex users, there is a `Mem0Memory` class that integrates with `ChatMemoryBuffer` and the agent runner. For CrewAI / AutoGen / Mastra, the integration is via the raw Mem0 client (no special wrapper yet).

## How Mem0 compares to alternatives in 2026

| Feature | Mem0 | Zep | Letta | Pinecone + custom | Redis vector search |
|---|---|---|---|---|---|
| License | Apache-2.0 (core) + Cloud SaaS | Apache-2.0 | Apache-2.0 | Proprietary SaaS | Redis Source Available (RSALv2/AGPLv3) |
| Self-hostable | Yes (Docker) | Yes | Yes | No (Pinecone only) | Yes |
| Auto fact extraction | Yes (LLM-based) | Yes (LLM-based) | Yes (built into agent loop) | No — you write the prompt | No — you write the prompt |
| Graph Memory | Yes (Pro+) | No | Yes (built-in agent context) | No | No |
| Multi-user isolation | Yes (user_id partition) | Yes (user_id) | Yes (user/agent IDs) | Yes (namespace) | Yes (key prefix) |
| Vector store included | Yes (Qdrant default) | Yes (Postgres + pgvector) | Yes (Postgres + pgvector) | Yes (Pinecone-managed) | Yes (Redis-managed) |
| Cloud SaaS | Yes | Yes (Zep Cloud) | No (self-host only) | Yes (Pinecone) | Yes (Redis Cloud) |
| Min monthly cost | $0 (Hobby) / $19 (Starter) | $0 (OSS) / $19 (Zep Cloud Starter) | $0 (OSS) | $50 (Pinecone Standard) | $0 (OSS) / $5 (Redis Cloud Essentials) |
| LangChain integration | First-class | First-class | First-class | DIY | DIY |
| Best for | Production agents needing fast setup | Long-context windows, time-weighted memory | Stateful agent frameworks | DIY power users | Existing Redis users |

**Mem0's edge:** zero prompt-engineering to get started (one `memory.add()` call and you have working memory), Graph Memory on Pro for entity-aware retrieval, the largest GitHub community (61,493 stars vs Zep's ~3,500, Letta's ~14,000), and the cleanest LangChain / LlamaIndex integration.

**Mem0's weakness:** fact extraction is async (the LLM call adds 200-500ms latency vs raw vector search), Pro pricing at $249/month is steep for hobbyists, Graph Memory requires a Neo4j dependency that adds ops complexity on self-host, and Mem0 is not a substitute for a vector database (you still need one for document retrieval).

**The Zep counter-argument:** Zep optimizes for long-context windows with time-weighted memory decay — if your use case is "remember what the user said 30 turns ago, weighted by recency", Zep's retrieval model is more sophisticated. Mem0's vector-only retrieval (on Hobby/Starter) is more naive.

**The Letta counter-argument:** Letta (formerly MemGPT) bakes memory management into the agent loop itself — the LLM actively decides when to read/write memory. This is more powerful but requires running a Letta-compatible agent framework, not just calling Mem0's API. Mem0 is framework-agnostic.

**The Pinecone + custom counter-argument:** if you already have a vector DB and an LLM ops team, building your own memory layer with `pinecone.upsert()` + an extraction prompt + a forgetfulness filter is straightforward and gives you full control. Mem0's value proposition collapses when you have the engineering capacity to maintain that pipeline yourself.

**The Redis counter-argument:** if your stack already runs Redis (caching, sessions, queues), using `redis-vector` for memory keeps everything in one engine. The trade-off is no fact extraction — you store raw messages, not structured memories, so retrieval quality depends on your embedding + chunking strategy.

## When to choose Mem0 (and when not to)

**Choose Mem0 if:**

- You are building a multi-turn AI agent and you do NOT want to write the fact-extraction prompt yourself
- You need memory isolation across users (multi-tenant SaaS agent, customer-support bot, personalized assistant)
- You want to ship fast and prefer a managed SaaS over self-hosting infrastructure
- You need Graph Memory for entity-relationship awareness (Pro tier and up)
- You already use LangChain / LlamaIndex / CrewAI and want a drop-in memory class

**Do NOT choose Mem0 if:**

- You are prototyping and a vector database is overkill (use raw conversation history in your LLM context window up to ~50K tokens)
- You have strict data-residency requirements that rule out Mem0 Cloud (Enterprise self-host is the option, but it requires a contract)
- You need document-search RAG, not conversation memory (use Pinecone / Weaviate / Qdrant instead — Mem0 is not a substitute)
- You have a small engineering team and a self-hosted Mem0 + Neo4j + Qdrant stack is too much ops overhead (use Mem0 Cloud, or stick with raw conversation history)
- You need sub-100ms retrieval latency (Mem0's LLM-based extraction adds 200-500ms — for latency-critical paths, use a pre-computed vector index)

## Sources

- Mem0 pricing page: mem0.ai/pricing — verified 2026-07-23
- Mem0 documentation: docs.mem0.ai
- Mem0 Python SDK: pypi.org/project/mem0ai
- Mem0 TypeScript SDK: npmjs.com/package/mem0ai
- Mem0 GitHub repository: github.com/mem0ai/mem0 — 61,493 stars, Apache-2.0, last commit 2026-07-23
- Mem0 supported LLMs: docs.mem0.ai/components/llms/overview — OpenAI, Anthropic, Gemini, Mistral, Groq, Ollama, AWS Bedrock, Azure OpenAI
- LangChain integration: docs.mem0.ai/integrations/langchain
- LlamaIndex integration: docs.mem0.ai/integrations/llamaindex
- Self-host Docker Compose: github.com/mem0ai/mem0/tree/main/server — bundled Qdrant + Neo4j
- Comparison alternatives: Zep (getzep.com), Letta (letta.com), Pinecone (pinecone.io), Redis vector search (redis.io/docs/latest/develop/interact/search-and-query/vectors)