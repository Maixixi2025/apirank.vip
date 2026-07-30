---
title: "Arize Phoenix 2026: Open-Source LLM Observability Reference"
slug: arize-phoenix-api-review
date: 2026-07-21
lang: en
locale: en
provider: arize-phoenix
providerFeatured:
  - arize-phoenix
  - helicone
  - openai
  - anthropic
  - freemodel
primaryAffiliate: freemodel
affiliateUrl: https://freemodel.dev/invite/FRE-7a3b6220
type: review
category: aggregator
---

# Arize Phoenix 2026: The Open-Source LLM Observability Reference

Arize Phoenix is the open-source standard for AI observability and evaluation that ships from Arize AI. Verified on 2026-07-21, Phoenix is the **only** top-tier LLM observability platform that is open-source under Elastic-2.0 (commercial-friendly) and that natively speaks OpenTelemetry, the open standard for trace export. The project crossed **10,600 GitHub stars**, ships v19.x on a ~weekly cadence, and has been adopted as the default observability backend inside LangChain, LlamaIndex, and the OpenAI Agents SDK. Phoenix is a peer of Helicone (Apache-2.0 closed-control-plane variant), Portkey (closed SaaS), Langfuse (LGPL), LangSmith (closed SaaS from LangChain), and Arize AX (Arize's commercial enterprise counterpart).

This review walks through what Phoenix does that closed SaaS alternatives do not, the verified 2026 pricing (free Cloud tier with 10 GiB included, paid tiers, and self-host), how to add Phoenix tracing to an OpenAI / Anthropic / vLLM / Ollama app in a few lines, and how Phoenix compares to Helicone, Portkey, Langfuse, LangSmith, and OpenLLMetry. The numbers come from the v19.3.0 release (2026-07-20), the official `arize-phoenix` PyPI package, the GitHub README, and the phoenix-cloud.mdx docs page.

If you are evaluating LLM observability in 2026 and you are allergic to vendor lock-in, this is the reference guide.

## What Arize Phoenix does (and what it does not)

Phoenix is an **AI observability + evaluation platform**, not an LLM router or gateway. It sits between your application and your LLM provider, capturing every request, every tool call, every retrieval, and every trace span, then exposing them through a web UI, an SDK query layer, and an evaluation harness.

Core capabilities (verified 2026-07-21 from Phoenix v19.3.0 docs and the GitHub README):

- **Open-source under Elastic-2.0.** Phoenix's source code is fully public at github.com/Arize-ai/phoenix (10,643 stars, 998 forks, active since 2022-11-09). You can self-host, fork, modify, and ship a derivative without paying anyone. This is the only top-3 LLM observability tool with a permissive license and zero required SaaS tier.
- **OpenTelemetry-native.** Phoenix accepts standard OTLP traces from any OTel-instrumented app. It is fully interchangeable with any other OTel backend (Tempo, Jaeger, Honeycomb, Datadog). The protocol is open; the storage engine is pluggable.
- **17+ LLM framework integrations.** Out of the box, Phoenix auto-instruments OpenAI SDK, Anthropic SDK, Google Vertex, AWS Bedrock, Cohere, Mistral, Groq, Together AI, Fireworks, Hugging Face, vLLM, Ollama, LangChain, LlamaIndex, Haystack, OpenAI Agents SDK, and smolagents.
- **Tracing + spans + evaluations + datasets + experiments + prompt playground + PXI agent.** Helicone is primarily a logging proxy. Phoenix is a full AI engineering workspace: traces, evaluations, datasets, experiment comparison, prompt versioning, retrieval inspection, and a new "PXI" AI engineering agent (BETA, 2026-Q3).
- **Self-host on anything.** Verified deployment options from the docs: CLI (`px setup`), Docker, Compose, Kubernetes, Helm, AWS CloudFormation, Railway one-click, Render blueprint, Google Cloud Run, and Azure ARM. There is also a managed Phoenix Cloud option for teams that want zero infra.
- **Cloud free tier.** Phoenix Cloud ships a free tier with **10 GiB of included storage** per workspace, ready to use with a free `app.arize.com` account. There is no time limit on the free tier beyond the storage quota.
- **Single-command setup (`px setup`).** The new 2026-Q3 CLI walks through the five-step onboarding: git safety check, connection, agent handoff for instrumentation, verification, and artifact write-back. For greenfield apps, you can be tracing in under five minutes.

Phoenix does **not** train or fine-tune models, does **not** host inference (unlike Helicone's caching layer or Vercel AI Gateway's routing), does **not** replace your LLM provider's billed tokens (it is observation-only), and does **not** act as an authentication proxy in the standard install (Helicone wraps your call; Phoenix can do that with a small bridge, but its primary mode is OTel collection).

The positioning is: **Phoenix is the "Honeycomb but for LLM apps" that you can self-host, fork, and extend**.

## Arize Phoenix pricing in 2026: free cloud tier, paid tiers, and self-host

Verified 2026-07-21 from the official Phoenix Cloud sign-up page and the self-hosting docs. Phoenix has three deployment models, each with its own pricing:

| Deployment | Cost | Storage limit | Retention |
|---|---|---|---|
| **Phoenix Cloud (Free)** | $0 / month | 10 GiB per workspace | Until you hit the cap |
| **Phoenix Cloud (Paid)** | Pay-as-you-go, varies by data volume | Custom | Custom |
| **Phoenix Self-Host (Apache-2)** | $0 (your infrastructure cost only) | Unlimited | Unlimited |
| **Arize AX (Enterprise)** | Custom contract | Unlimited | Unlimited + SSO + RBAC + audit log |

The free Cloud tier is the lowest-friction path. Sign in at `app.arize.com`, click "Create a Space," and Phoenix provisions a managed workspace with 10 GiB of storage already attached. The paid Cloud tier is pay-as-you-go (volume-discounted, no per-seat pricing); the enterprise tier (Arize AX) adds SAML SSO, on-prem deployment, custom MSA, audit logs, and dedicated Slack support.

For most teams, the right starting move is the free Cloud tier. Once you hit 10 GiB (about 5–10 million traced LLM spans depending on payload size), the upgrade path is either pay-as-you-go or self-host. Self-host has no licensing cost and runs on the same Phoenix image; you pay only your cloud bill.

> ⚠️ **Pricing gotcha:** Phoenix Cloud pricing scales with **storage**, not with seat count. A solo developer running 50 RPS through Phoenix consumes the same storage as a 50-engineer team running the same traffic. Seat-based pricing is the Vercel/Portkey model; Phoenix is volume-based.

## Arize Phoenix vs Helicone vs Langfuse vs Portkey vs LangSmith vs OpenLLMetry

The 2026 LLM observability landscape has six credible options. They cluster into three groups by ownership and license:

| Tool | License | Self-host | Free tier | Paid tier | Tracing | Evaluations | Dataset / experiments | Native framework auto-instr | OpenTelemetry-native |
|---|---|---|---|---|---|---|---|---|---|
| **Arize Phoenix** | Elastic-2.0 | ✅ | 10 GiB Cloud | Pay-as-you-go | ✅ | ✅ | ✅ | 17+ frameworks | ✅ |
| Helicone | Apache-2.0 | ✅ | 10K req/mo | $79/mo (Pro) | ✅ | ⚠️ Limited | ❌ | 100+ providers | ⚠️ Proxy-based |
| Portkey | Closed source | ❌ | 10K req/mo | $49/mo (Hobby) | ✅ | ✅ | ⚠️ Limited | 200+ providers | ⚠️ Proxy-based |
| Langfuse | LGPL (with managed cloud) | ✅ | 50K events/mo | Pay-as-you-go | ✅ | ✅ | ✅ | LangChain + broad | ✅ |
| LangSmith | Closed (LangChain-owned) | ⚠️ Enterprise-only | 5K traces/mo | $39/mo (Plus) | ✅ | ✅ | ✅ | LangChain-first | ⚠️ Proxy-based |
| OpenLLMetry | MIT (the OTel contrib) | ✅ | N/A (library, not service) | N/A | ✅ | ❌ | ❌ | 17+ frameworks | ✅ |

The structural split:

- **Closed-source paid SaaS (Portkey, LangSmith):** easiest onboarding, but you cannot read the source, cannot self-host, and your data lives in their database. Vendor lock-in is the deal-breaker.
- **Open-source self-hostable (Phoenix, Langfuse):** free to deploy anywhere; OpenTelemetry-native so you can swap backends; you are responsible for operating them.
- **OSS-but-proxy-only (Helicone):** the open-source license applies but the production deploys are SaaS-first; you must use their proxy for the full feature set.
- **Pure library, not a service (OpenLLMetry):** this is the OTel contrib project that Phoenix is built on top of. You can use OpenLLMetry without Phoenix and export to any OTel-compatible backend.

In practice:

- If you want **maximum control + minimum lock-in**, Phoenix is the strongest pick. It is the only top-tier option with a permissive license **and** open telemetry **and** a full UI.
- If you want **easiest onboarding for a non-engineer team**, LangSmith or Portkey will feel more polished.
- If you want **Helicone's proxy pattern with an OSS license**, you can use Helicone self-hosted or open source LiteLLM as a proxy in front of Phoenix.
- If you want **Phoenix-class capabilities for free without self-hosting**, the Phoenix Cloud free tier covers most solo-developer and early-stage-team use cases.

## How to add Phoenix tracing to an OpenAI / Anthropic app (with code)

The simplest integration uses Phoenix's OTel auto-instrumentor. **One line** of code wires every OpenAI / Anthropic / vLLM call into Phoenix without changing your existing client:

```python
# pip install arize-phoenix-otel openai
from phoenix.otel import register
from openai import OpenAI

# Point Phoenix at your local or hosted collector
tracer_provider = register(
    project_name="my-llm-app",
    endpoint="http://localhost:6006/v1/traces",  # Phoenix Cloud or self-hosted
)

client = OpenAI()  # uses OPENAI_API_KEY from env
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello, GPT-4o through Phoenix."}],
)
print(response.choices[0].message.content)
# Every API call now shows up in Phoenix with full spans, token counts, latency.
```

That single `register()` call instruments the OpenAI SDK with OTel spans, exports them to Phoenix, and creates a project in the UI under the name `my-llm-app`. No change to your existing client code.

### Using the Anthropic SDK through Phoenix

```python
# pip install arize-phoenix-otel anthropic
from phoenix.otel import register
from anthropic import Anthropic

tracer_provider = register(
    project_name="claude-eval",
    endpoint="http://localhost:6006/v1/traces",
)

client = Anthropic()  # uses ANTHROPIC_API_KEY
msg = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarize Q2 OKRs."}],
)
print(msg.content[0].text)
# Spans appear in Phoenix with the same metadata as OpenAI calls.
```

### Running Phoenix locally for development

The fastest local setup is `phoenix serve`, which starts a Phoenix UI on `localhost:6006` with an in-process OTel collector and an SQLite storage backend. For dev work this is a one-liner:

```bash
pip install arize-phoenix
phoenix serve
# Open http://localhost:6006 — Phoenix is ready, no config needed.
```

For production-grade self-host, swap SQLite for PostgreSQL and Docker for a deployment platform. The full Docker Compose file lives in the `deploy/docker` directory of the GitHub repo. Kubernetes users have an official Helm chart; AWS / GCP / Azure customers have one-click IaC templates in the self-hosting docs.

## OpenTelemetry: why Phoenix's protocol choice matters

The single most important architectural fact about Phoenix is that it speaks OTLP (OpenTelemetry Line Protocol), the open standard for trace export. This means:

1. **Your existing OTel pipelines work.** If your team already runs Honeycomb, Datadog, Tempo, or any other OTel backend, Phoenix can export to it as a peer. You can also import from any OTel-instrumented app and store traces in Phoenix.
2. **No vendor-locked SDK.** The `phoenix-otel` package is built on `opentelemetry-instrumentation-*` — the same instrumentation packages that OTel users run. If you stop using Phoenix, the traces still flow to your OTel collector.
3. **Multi-backend fan-out.** Because the protocol is open, you can run Phoenix as the primary UI backend and fan traces out to Datadog for production alerts without duplicating instrumenting code. This is the canonical pattern for teams adopting Phoenix mid-project.

The strategic insight: **Phoenix is the Grafana of LLM observability**. OpenTelemetry is the protocol, Phoenix is the UI, and you keep the data and the integrations.

## Evaluations, datasets, and the PXI agent

Phoenix is more than a tracer. The other half of the platform is structured evaluation:

- **Spans → Datasets.** One click in the UI converts any span into a dataset row. If you have 200 traced production calls that you want to grade, the UI extracts them and lets you attach expected outputs and grader configurations.
- **Evaluators.** Phoenix ships with code-based evaluators (exact match, JSON schema validation, regex), LLM-as-judge evaluators (you bring the model), and custom Python evaluators. Run them in batch over a dataset, then compare results across prompt versions or model versions.
- **Experiments.** Compare two prompt versions side-by-side on the same dataset. Phoenix ranks them by evaluator scores and surfaces the per-row wins and losses. This is what A/B testing for prompts looks like in 2026.
- **Prompt playground.** Edit a prompt, regenerate, and grade the outputs without leaving Phoenix. Supports multi-turn conversation editing and the same OTel trace path as production.
- **PXI (Phoenix Intelligence).** The 2026-Q3 agent (currently BETA) reads your existing traces, datasets, evaluations, and experiments, then answers natural-language questions about them. It is the same pattern as a coding agent pointed at observability data: ask "what changed in the prompt-engineering prompt last week," and PXI diffs the versions and highlights the regression.

The takeaway: **Phoenix is the only LLM observability tool that bundles tracing + evaluations + experiments + prompt management + agent-assisted debugging under one license** (Elastic-2.0). Helicone covers tracing and has evaluation experiments, but not at the depth Phoenix offers. Portkey covers evaluations well, but traces only through its proxy. LangSmith covers all of it but is closed source.

## Self-hosting Phoenix with Docker Compose

For teams that need on-prem or air-gapped deploys, Phoenix self-hosts in a single Docker Compose file. The minimal Compose is two services: a Phoenix app server (Python, ~2 CPU, 2 GiB RAM for typical dev workloads) and a PostgreSQL database (Postgres 15+). For dev, you can also use the bundled SQLite path:

```yaml
# docker-compose.yml (minimal Phoenix self-host)
services:
  phoenix:
    image: arizephoenix/phoenix:latest
    ports:
      - "6006:6006"
    environment:
      - PHOENIX_SQL_DATABASE_URL=postgresql://phoenix:phoenix@db:5432/phoenix
      - PHOENIX_ENABLE_AUTH=true   # Optional: enforce local accounts
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: phoenix
      POSTGRES_PASSWORD: phoenix
      POSTGRES_DB: phoenix
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

```bash
docker compose up
# Open http://localhost:6006 — full Phoenix stack on Postgres.
```

For Kubernetes, the official Helm chart at `Arize-ai/phoenix-helm` deploys Phoenix to a cluster with a single `helm install` command. AWS users can use the official CloudFormation template; GCP users have a Cloud Run one-click deploy; Azure users have an ARM template; Railway and Render users have one-click Blueprints.

The pattern at most companies in 2026: **Phoenix Cloud free tier for the first six months, then self-host on EKS or GKE when the storage bill scales**. Switching from Phoenix Cloud to Phoenix self-host is a configuration change, not a code rewrite.

## Real-world use cases

**1. LLM evaluation harness for prompt engineering.** A team running GPT-4o, Claude Opus 4.8, and Gemini 2.5 Pro side-by-side wants to know which prompt produces the best outputs. Phoenix lets them trace every call, convert spans to datasets, run LLM-as-judge evaluations across all three models, and compare results in the UI. The PXI agent can answer "show me all prompts where Claude's score fell below 4.5 last week."

**2. RAG debugging.** A RAG app is producing wrong answers. Phoenix traces each pipeline step: query embedding → vector retrieval → chunk scoring → LLM synthesis. The UI shows the exact retrieved chunks for each trace, so engineers can pinpoint whether the retrieval step is the failure or the synthesis step. This is the canonical use case for Phoenix — RAG apps need span-level visibility, not just request-level logs.

**3. Production cost attribution.** A SaaS product wants per-customer LLM cost. Phoenix spans carry arbitrary tags (`customer_id`, `feature_name`, `tenant`). A backend job queries the spans through the Phoenix API, groups by `customer_id`, and produces monthly invoices. The cost is one extra query per call and the engineering time saved is months vs building a custom logging pipeline.

**4. Agent debugging.** An OpenAI Agents SDK or smolagents workflow produces a 14-step tool-call chain. Phoenix traces every tool invocation, every sub-agent decision, and every LLM call. The UI surfaces the full chain as a waterfall, and PXI can narrate what went wrong — "the agent called `search_web` three times for the same query because the deduplication step fired before the cache was warmed."

**5. Compliance-grade audit log.** A regulated industry (healthcare, finance, government) needs every LLM call logged for audit. Phoenix emits a structured span per call with prompt, response, latency, model, and tokens. Export those spans to S3 via OTel collector, retain for 7 years, done. The Elastic-2.0 license covers commercial deployment.

## Honest limitations

Phoenix is the strongest open-source LLM observability tool in 2026, but it is not magic:

- **No request-side caching or fallback routing.** Phoenix is observation-only. If you want LLM caching, fallback chains, or request retries at the proxy layer, layer Phoenix behind Helicone, Vercel AI Gateway, or LiteLLM. The composition works; Phoenix does not try to be all of them.
- **No built-in token-cost optimization.** Phoenix tells you what your traces cost. It does not negotiate rates or route to cheaper models automatically. That's a Portkey or Helicone pattern.
- **Cloud free tier is 10 GiB.** That's enough for solo developers and small teams but will run out for high-volume production usage. Plan the Cloud→self-host migration before you hit the cap (Phoenix emails you when you approach the limit).
- **PXI is in BETA.** The agent is genuinely useful for trace investigation but produces wrong answers on edge cases. Treat its output as a starting point, not a verified fact.
- **Self-host requires Postgres + Python.** Not as heavy as Langfuse, but you are running a database and an app server. Railway / Render one-click deploys handle this for most teams.
- **Closed-source competitors (LangSmith, Portkey) polish the UX.** Phoenix's UI is functional but less polished than LangSmith's. If a non-engineer team member needs to use the tool daily, expect a learning curve.

These are tradeoffs, not deal-breakers. For technical teams that value control and open standards, Phoenix is the right pick.

## Verdict for API developers

Arize Phoenix is the **best open-source LLM observability platform in 2026**. It is the only top-tier option that is permissive-license, self-hostable, OpenTelemetry-native, evaluation-capable, and actively maintained. The Cloud free tier covers most solo developers and small teams; self-host covers everything else. If your team already runs OTel, Phoenix slots in as a peer backend; if your team is new to LLM observability, Phoenix's `px setup` CLI and 17+ framework integrations make the first hour productive.

Pick Phoenix if you want **maximum control + minimum lock-in** for LLM observability. Pick LangSmith if you want the most polished UI and your stack is LangChain-native. Pick Portkey if you want a SaaS control plane with strong evaluation UX. Pick Helicone if you want a proxy layer with strong caching. Pick Langfuse if you want an LGPL-licensed alternative with broader framework support.

For production use, run Phoenix on the **free Cloud tier** to start. Migrate to **self-host on EKS or GKE** once you exceed 10 GiB of storage. Add **PXI** to your debugging rotation once it leaves BETA. And pair Phoenix with **Helicone or Vercel AI Gateway** if you also need request-side caching and fallback routing — Phoenix and the proxies compose cleanly.

The verified 2026-07-21 numbers are all in the GitHub README, the v19.3.0 release notes, and the official docs. The numbers will change; the architectural pattern will not.

## Frequently asked questions

### What is Arize Phoenix used for in 2026?

Arize Phoenix is an open-source LLM observability and evaluation platform. It captures traces from any OpenTelemetry-instrumented app (OpenAI, Anthropic, vLLM, Ollama, LangChain, LlamaIndex, etc.), exposes them through a web UI, and adds evaluation, dataset management, experiment comparison, and prompt-management features on top. Phoenix is to LLM apps what Honeycomb is to microservices — but open-source and self-hostable. In 2026 it is the default observability backend for teams that want minimal vendor lock-in.

### Is Arize Phoenix free?

Yes, in three ways. The Phoenix Cloud free tier ships with 10 GiB of included storage per workspace and is free indefinitely (no time limit beyond the storage cap). Phoenix self-hosted under Elastic-2.0 is free to deploy anywhere with no licensing cost (you pay only your infrastructure bill). The Phoenix source code on GitHub is fully public. The paid Cloud tier is pay-as-you-go for higher storage quotas; the enterprise tier (Arize AX) is a custom contract with SAML, SSO, audit logs, and on-prem deployment.

### How does Phoenix compare to Helicone in 2026?

Both are LLM observability tools, but they optimize for different things. Phoenix is observation-first (you bring your own client; Phoenix collects traces via OTel) and open-source (Elastic-2.0, self-host anywhere). Helicone is a proxy-first wrapper around your LLM calls with caching, fallbacks, and HQL queries — also open-source (Apache-2.0) but typically deployed as a SaaS via proxy. Use Phoenix if you want full control and OpenTelemetry-native architecture. Use Helicone if you want request-side caching and a no-code observability dashboard. They compose well — Phoenix behind a Helicone proxy is a common 2026 pattern.

### Does Phoenix work with OpenAI's Agents SDK?

Yes. Phoenix ships an OpenTelemetry auto-instrumentor for `openai-agents` (and `smolagents`, LangChain, LlamaIndex, Haystack, etc.). The setup is one line of code — `register(project_name="...", endpoint="...")` — and every agent invocation, sub-agent decision, and tool call is traced into Phoenix. The new PXI agent can narrate the trace for debugging. Agents tracing is the fastest-growing Phoenix use case in 2026.

### Can I self-host Phoenix on Kubernetes?

Yes. The official Phoenix Helm chart at `Arize-ai/phoenix-helm` deploys Phoenix with one `helm install` command. AWS users have an official CloudFormation template; GCP users have a one-click Cloud Run deploy; Azure users have an ARM template; Railway and Render users have one-click Blueprints. The minimum resource footprint is roughly 2 CPU + 2 GiB RAM for the app server and a 10 GiB PostgreSQL database for typical workloads.

### Does Arize Phoenix support LLM evaluations?

Yes. Phoenix includes code-based evaluators (exact match, JSON schema validation, regex), LLM-as-judge evaluators (you bring any LLM as the grader), and custom Python evaluators. Run them over a dataset (one-click conversion from any span), then compare evaluator scores across prompt versions in the experiments UI. The evaluation harness is comparable to LangSmith's at the SDK level and slightly less polished in the UI.

### Is Phoenix OpenTelemetry-native?

Yes. Phoenix accepts standard OTLP traces from any OTel-instrumented app. It is fully interchangeable with Tempo, Jaeger, Honeycomb, Datadog, and any other OTel backend. You can also fan traces out to multiple backends via standard OTel collector configuration. OpenTelemetry is the strategic protocol choice that gives Phoenix its long-term flexibility.

### Who built and maintains Phoenix?

Phoenix is built and maintained by Arize AI, the same company behind the Arize AX enterprise observability product. The Phoenix repo on GitHub has 10 contributors with commit activity on a near-daily cadence. Releases ship weekly on a Semantic Versioning cadence; the v19.x line shipped on 2026-07-20. The maintainer team includes engineers from the OpenTelemetry community, and Phoenix is one of the canonical reference implementations for OTel-based LLM instrumentation.

### What's the difference between Phoenix and Arize AX?

Phoenix is the open-source core (Elastic-2.0, fully self-hostable, free Cloud tier). Arize AX is the commercial enterprise product that builds on Phoenix with SAML SSO, on-prem deployment, role-based access control, audit logs, dedicated Slack support, custom MSAs, and bulk cloud discounts. A typical path is: Phoenix Cloud free tier → Phoenix self-hosted on EKS → Arize AX for the regulated-industry tier. The data model and SDKs are identical across both.

## Sources

- Arize Phoenix GitHub repo: github.com/Arize-ai/phoenix — 10,643 stars, 998 forks, Elastic-2.0 licensed
- Phoenix v19.3.0 release (verified 2026-07-20)
- PyPI package arize-phoenix — Python 3.10-3.14 support
- Phoenix Cloud docs: app.arize.com (sign-up), phoenix-cloud.mdx (setup)
- Phoenix self-hosting docs: docker, kubernetes, helm, aws-with-cloudformation, railway, render, google-cloud-run
- Phoenix Cloud free tier: 10 GiB included storage per workspace
- OpenTelemetry OTLP standard: opentelemetry.io/docs/specs/otlp/
- LLM framework integration list: integrations.mdx — 17+ frameworks including OpenAI SDK, Anthropic SDK, LangChain, LlamaIndex, Haystack, smolagents, OpenAI Agents SDK
- PXI (Phoenix Intelligence) BETA announcement: pxi.mdx
- License details: Elastic-2.0, full text at elastic.co/licensing/elastic-license
