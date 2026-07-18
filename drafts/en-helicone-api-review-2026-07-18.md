# Helicone 2026: Open-Source LLM Observability

_Date: 2026-07-18 | Slug: helicone-api-review | Locale: en_

# Helicone 2026: The Open-Source LLM Observability Platform That Adds One Line to Your Stack

Helicone is the open-source standard for LLM observability in 2026. Founded in 2023 by a Y Combinator W23 team, the project is now a 5,961-star Apache-2.0 codebase on GitHub (verified July 18, 2026) that wraps 100+ LLM providers behind a single AI Gateway with full request logging, cost attribution, prompt versioning, and a SQL-like query language for call analytics. Helicone is the missing layer between your application and OpenAI/Anthropic/Google — drop in one base URL and every prompt, completion, latency, token count, and cost is captured automatically.
This review walks through what Helicone does, how the AI Gateway integrates with the major providers, the verified 2026 pricing (Hobby free, Pro $79/mo, Team $799/mo, Enterprise custom), and how it compares to Portkey, LiteLLM, and Cloudflare AI Gateway. The numbers come from the official Helicone pricing page (helicone.ai/pricing, captured July 18, 2026) and the GitHub repo's public API. If you are evaluating LLM observability vendors in 2026, this is the reference guide.
## What Helicone does (and what it does not)

Helicone is an LLM observability layer, not a model provider. You keep using your existing OpenAI / Anthropic / Google accounts; Helicone sits between your application and the provider as a transparent proxy that logs every call. The core capabilities are:
- AI Gateway — a single base URL that routes to 100+ providers, with provider failover and per-key rate limits.
- Request logging — every prompt, completion, latency, token count, cost, and user metadata is captured and indexed.
- HQL (Helicone Query Language) — SQL-like syntax to query billions of LLM call rows in sub-second time. Available from Pro tier.
- Prompt versioning and experiments — run A/B tests on prompt variants, see cost / latency / quality deltas side by side.
- Cost attribution — tag calls by user, team, or feature and produce per-customer billing breakdowns.
- Self-hosting — Apache-2.0 means you can run the entire platform on your own infrastructure.
Helicone does not train or fine-tune models, does not provide guardrails or content moderation (unlike Portkey), and does not have a no-code app builder. The product is tightly focused on the observability niche, and that focus is what makes the open-source version production-grade.
## Helicone pricing in 2026: Hobby, Pro, Team, Enterprise

Helicone's verified July 2026 pricing (source: helicone.ai/pricing, captured 2026-07-18):TierPriceRequests/moKey featuresHobbyFree10,0001 GB storage, 1 seat, 1 organizationPro$79/moUsage-basedUnlimited seats, alerts, reports, HQL query languageTeam$799/moUsage-based5 organizations, SOC-2 + HIPAA, dedicated Slack channelEnterpriseCustomVolumeSAML SSO, on-prem deployment, custom MSA, bulk discounts
Usage-based pricing applies on top of the seat fee for customers who exceed the included request volume. Public usage rates are not disclosed on the pricing page; enterprise contracts handle high-volume customers. The Apache-2.0 self-hosted deployment has no seat fee — you only pay for the infrastructure you run it on (typically a small Postgres + Redis + the proxy container, all of which fit on a $20/mo VPS).
Helicone is the rare AI infrastructure vendor where the open-source version is feature-equivalent to the SaaS version. Most observability vendors (Portkey, Cloudflare AI Gateway) only offer closed-source SaaS. If you need SOC-2 or HIPAA compliance but want to avoid SaaS vendor lock-in, the Team tier ($799/mo) is the cheapest path that includes both compliance attestations and unlimited seats.
## Helicone vs Portkey vs LiteLLM vs Cloudflare AI Gateway

All four products solve the "I need to route LLM calls across providers and see what is happening" problem, but they optimize for different things. The decision matrix below is calibrated for a 50-engineer team shipping LLM-backed features in production.FeatureHeliconePortkeyLiteLLMCF AI GatewayOpen source✅ Apache-2.0❌ Closed SaaS✅ MIT❌ ClosedSelf-host✅ Yes❌ No✅ Yes❌ No (CF only)Provider count100+200+100+40+Free tier10K req/mo10K req/moUnlimited (OSS)LimitedTeam tier price$799/mo$199/moFree (OSS)$5/mo + usageSOC-2 / HIPAA✅ Team+✅ EnterpriseEnterprise tierCF-wideA/B testing✅ HQL-based✅ App Portal⚠️ Manual❌ NoGuardrails⚠️ Limited✅ Built-in⚠️ Plugin⚠️ LimitedCost attribution✅ Per-user/per-team✅ Per-key⚠️ Manual✅ Per-tagCustom SQL analytics✅ HQL❌ Dashboard only❌ Logs only❌ No
Pricing verified 2026-07-18 from each vendor's public pricing page. Helicone Pro $79/mo, Portkey Growth $199/mo, LiteLLM free self-host, Cloudflare AI Gateway $5/mo Workers Paid plan + $0.20/M Gateway requests.
If your priority is self-hosting with full observability and a real query language, Helicone is the strongest choice. If your priority is lowest total cost at scale, LiteLLM (open-source, free self-host) wins. If your priority is polished managed SaaS with App Portal, Portkey is the best. If your priority is zero ops and you are already on Cloudflare, AI Gateway is the cheapest path.
## How the Helicone AI Gateway works (with code)

The simplest integration is a one-line base URL change. The OpenAI Python SDK works without modification once you swap the base URL:
from openai import OpenAI
import os

# Your existing OpenAI client — just change the base_url and add Helicone auth
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    base_url='https://ai-gateway.helicone.ai',
    default_headers={
        'Helicone-Auth': f'Bearer {os.environ['HELICONE_API_KEY']}',
        # Optional: tag calls for cost attribution
        'Helicone-Property-User-Id': 'user_123',
        'Helicone-Property-Feature': 'chat-summary',
    }
)

response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': 'Summarize Q3 earnings.'}],
)
print(response.choices[0].message.content)
# Every call is automatically logged to the Helicone dashboard
For Anthropic Claude, the same pattern works through Helicone's Anthropic-compatible endpoint:
from anthropic import Anthropic
import os

client = Anthropic(
    api_key=os.environ['ANTHROPIC_API_KEY'],
    base_url='https://anthropic.helicone.ai',
    default_headers={
        'Helicone-Auth': f'Bearer {os.environ['HELICONE_API_KEY']}',
    }
)

message = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=1024,
    messages=[{'role': 'user', 'content': 'Hello, Claude.'}],
)
For self-hosted deployments, replace the base_url with your own gateway URL (e.g. https://gateway.internal.yourcompany.com) and skip the Helicone-Auth header or replace it with your proxy auth.
## HQL: the query language that sets Helicone apart

Helicone Query Language (HQL) is the single feature that distinguishes Helicone from Portkey, LiteLLM, and Cloudflare AI Gateway. Where those vendors ship dashboard-only analytics or JSON-filter queries, HQL gives you a real SQL-like syntax for slicing and dicing your LLM call logs.
Example HQL queries that platform engineers actually run:
-- Top 20 users by GPT-4o cost in the last 30 days
SELECT user_id, sum(cost) AS total_cost
FROM requests
WHERE model = 'gpt-4o'
  AND created_at > now() - interval '30 days'
GROUP BY user_id
ORDER BY total_cost DESC
LIMIT 20;

-- P95 latency per provider
SELECT provider, quantile(latency_ms, 0.95) AS p95_latency
FROM requests
WHERE created_at > now() - interval '7 days'
GROUP BY provider
ORDER BY p95_latency DESC;

-- Error rate by prompt version
SELECT prompt_version,
       count(*) AS total_calls,
       sum(if(status_code >= 400, 1, 0)) / count(*) AS error_rate
FROM requests
GROUP BY prompt_version
ORDER BY error_rate DESC;
HQL runs on ClickHouse in the SaaS deployment, so queries against billions of rows return in under a second. The Pro tier ($79/mo) is where HQL unlocks; Hobby and the open-source self-hosted free build have basic filtering only.
## Self-hosting Helicone with Docker Compose

The Apache-2.0 codebase ships with a Docker Compose setup that brings up the proxy, the web dashboard, Postgres, Redis, and ClickHouse in one command:
# Clone and launch the Helicone self-hosted stack
git clone https://github.com/Helicone/helicone.git
cd helicone
docker compose up -d

# The proxy is now listening on http://localhost:8585
# The web dashboard is on http://localhost:3000
# ClickHouse, Postgres, Redis are all on the internal network
For production, deploy the same Docker images to Kubernetes. Helicone publishes official Helm charts in the repo. The minimum recommended infrastructure is 4 vCPU / 8 GB RAM for the proxy + ClickHouse node, plus a managed Postgres and Redis instance. A self-hosted Helicone deployment typically runs comfortably on a $50–$100/mo Hetzner or DigitalOcean box for low-to-medium traffic.
## Real-world use cases

Three patterns where Helicone pays for itself within a month:
- Cost attribution for a multi-tenant SaaS. A B2B AI product with 200 customers needs to know which customer is generating which cost. Helicone's Helicone-Property-User-Id header lets you tag every call with a tenant ID and run HQL to produce per-customer monthly invoices. Portkey and LiteLLM require a per-key setup that does not scale beyond a few dozen customers.
- Prompt experiment tracking. An engineering team shipping prompt changes weekly needs to compare variant A vs variant B on cost, latency, and quality. Helicone's prompt versioning and HQL-based experiment dashboard show the deltas side by side without writing custom eval infrastructure.
- Production observability + incident response. When an LLM-powered feature starts returning 500s, you need to know whether it is the provider, your prompt, or a specific user. Helicone's request logs with status code, latency, and full prompt/completion make root-causing a 10-minute exercise instead of a 4-hour one.
## Honest limitations

- Hobby tier caps at 10,000 requests/mo. Anything beyond a hobby project will need at least Pro ($79/mo).
- Team tier ($799/mo) is expensive for small teams. If you are a 5-person team, Portkey Growth ($199/mo) or LiteLLM free self-host is more cost-effective.
- Guardrails are limited. Portkey has first-class guardrails for content moderation, PII redaction, and prompt injection defense. Helicone's guardrails are basic — if safety is the primary requirement, pair Helicone with a dedicated guardrail layer.
- Self-hosting requires ClickHouse. The ClickHouse dependency makes the self-hosted stack heavier than LiteLLM's Python-only proxy. For a true single-binary deployment, LiteLLM wins.
- Usage-based pricing is not publicly disclosed. Customers above the free tier need to contact sales for the per-request overage rate.
## Verdict for API developers

Helicone is the strongest open-source choice for LLM observability in 2026. The Apache-2.0 license means you can self-host the full platform, the AI Gateway works as a one-line drop-in for OpenAI / Anthropic / Google, and HQL is the only real SQL-like query language among the AI Gateway vendors. If you need SOC-2 and HIPAA out of the box without going to Enterprise tier, the $799/mo Team tier is the cheapest compliance-attested option on the market.
For teams that prioritize raw cost over feature depth, LiteLLM (free self-host) or Cloudflare AI Gateway ($5/mo) are better value. For teams that prioritize a polished SaaS experience with App Portal, Portkey is the right pick. Helicone sits in the middle: feature-rich, open-source, with a Pro tier that is competitive on price and a Team tier that is expensive but unlocks the compliance and unlimited-seat combination.
For a deep-dive comparison of all four options on cost, performance, and feature fit, the FreeModel aggregation layer is a useful neutral benchmark — it routes through the same OpenAI-compatible interface and exposes cost / latency data across all four vendors without locking you into any one of them.
## Frequently asked questions

What is Helicone used for? Helicone is an open-source LLM observability platform built by a YC W23 team. It adds a one-line proxy layer between your code and 100+ LLM providers (OpenAI, Anthropic, Google Vertex, AWS Bedrock, Azure, Cohere, Groq, Together, Fireworks, Mistral) so you can log every request, attribute cost per user, run prompt experiments, and detect regressions. It is the standard tool for platform teams that need LLM call analytics without building their own logging pipeline.
How much does Helicone cost in 2026? Helicone has four tiers. Hobby is free with 10,000 requests per month and 1 GB of storage. Pro is $79 per month with unlimited seats, alerts, reports, and the HQL query language. Team is $799 per month with 5 organizations, SOC-2 and HIPAA compliance, and a dedicated Slack channel. Enterprise is custom-priced with SAML SSO, on-prem deployment, custom MSA, and bulk cloud discounts. Usage-based pricing applies on top of the seat fee for high-volume customers.
Is Helicone open-source? Yes — the Helicone proxy and AI Gateway are Apache-2.0 licensed on GitHub (github.com/Helicone/helicone, verified 5,961 stars and 630 forks as of July 18, 2026). You can self-host the full platform with Docker, including the request logging, dashboard, and HQL engine. The SaaS version is a managed instance of the same codebase, so feature parity is maintained between self-hosted and cloud deployments.
Helicone vs Portkey — which should I pick? Pick Helicone if your primary need is deep request analytics, prompt versioning, and self-hosting. Pick Portkey if your primary need is AI Gateway routing with guardrails and a polished App Portal for non-technical API key management. Helicone's Team tier ($799/mo) is more expensive than Portkey's Growth tier ($199/mo) but unlocks SOC-2 and HIPAA out of the box. Helicone is open-source; Portkey's Gateway is closed-source SaaS-only.
Does Helicone work with OpenAI, Anthropic, and Google Vertex? Yes. The Helicone AI Gateway is a drop-in replacement for the OpenAI base URL — you change one line (api_base='https://ai-gateway.helicone.ai' or your self-hosted URL) and pass Helicone-Auth headers for provider auth. Anthropic Claude, Google Gemini/Vertex, AWS Bedrock, Azure OpenAI, Mistral, Cohere, Groq, Together AI, and Fireworks AI all work with the same one-line integration. Each request is logged with full prompt, completion, latency, tokens, cost, and user metadata.
What is HQL (Helicone Query Language)? HQL is a SQL-like syntax for querying LLM call logs. It is unique to Helicone among the AI Gateway vendors — Portkey and Cloudflare AI Gateway use JSON filters or dashboards only. Example: \`SELECT user_id, sum(cost) FROM requests WHERE model = 'gpt-4o' AND latency > 2000 GROUP BY user_id ORDER BY cost DESC LIMIT 20\`. HQL runs on top of ClickHouse in the SaaS deployment, giving sub-second response times on billions of rows. HQL is available from the Pro tier ($79/mo) and up.
Can I use Helicone from inside China? Yes, via self-hosting. The Helicone Apache-2.0 proxy runs anywhere Docker or Kubernetes runs — including on Aliyun ECS, Tencent Cloud, or Huawei Cloud inside China. The proxy talks to the upstream providers (OpenAI, Anthropic, etc.) using your own keys, so if you need to access the providers from inside China you still need an upstream proxy for those specific calls. The SaaS dashboard at helicone.ai is geo-blocked in mainland China.
## Sources

- Helicone, Pricing, 2026-07-18: helicone.ai/pricing
- Helicone, AI Gateway documentation, 2026: docs.helicone.ai
- GitHub, Helicone/helicone, 5,961 stars / 630 forks / Apache-2.0, accessed 2026-07-18: github.com/Helicone/helicone
- Portkey, Pricing, 2026-07: portkey.ai/pricing
- LiteLLM, Repository, 2026-07: github.com/BerriAI/litellm
- Cloudflare, AI Gateway pricing, 2026: developers.cloudflare.com/ai-gateway
