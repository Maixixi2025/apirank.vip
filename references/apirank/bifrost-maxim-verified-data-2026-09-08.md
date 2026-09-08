# Bifrost Maxim Verified Data — 2026-09-08

**Source:** apirank add-provider #101 (bifrost-maxim)

## Primary sources (verified live 2026-09-08)

| URL | Status | Use |
|---|---|---|
| `https://github.com/maximhq/bifrost` | 200 | GH API data — stars, forks, license, language, topics, last commit |
| `https://raw.githubusercontent.com/maximhq/bifrost/main/LICENSE` | 200 | License confirmation (Apache-2.0, January 2004) |
| `https://www.getmaxim.ai/bifrost` | 200 | Marketing positioning, "50x faster than LiteLLM", "1000+ AI models" |
| `https://www.getmaxim.ai/bifrost/pricing` | 200 | OSS $0 / Enterprise custom / 14-day trial |
| `https://docs.getbifrost.ai` | 200 | Docs overview — 20+ providers, OpenAI-compatible, sub-100µs @ 5k RPS |

## GitHub API (verified 2026-09-08)

```
stars: 7,869
forks: 1,176
language: Go
license: Apache-2.0
created_at: 2025-03-19T07:21:26Z
updated_at: 2026-09-08T02:09:35Z
pushed_at: 2026-09-08T01:09:03Z
size_kb: 937730
topics: ['ai-gateway', 'gateway', 'gateway-services', 'generative-ai', 'guardrails',
         'llm', 'llm-cost', 'llm-gateway', 'llm-observability', 'llmops',
         'load-balancing', 'mcp-client', 'mcp-gateway', 'mcp-server',
         'model-router', 'token-management']
homepage: https://www.getmaxim.ai/bifrost
description: "Fastest enterprise AI gateway (50x faster than LiteLLM) with adaptive
              load balancer, cluster mode, guardrails, 1000+ models support &
              <100 µs overhead at 5k RPS."
```

## Pricing (verified 2026-09-08 from getmaxim.ai/bifrost/pricing)

- **OSS**: $0 (Apache-2.0 self-hosted forever, Docker / K8s / Go binary / npx)
- **Enterprise Free Trial**: $0 for 14 days
- **Enterprise Production**: Custom (VPC / on-prem / air-gapped, book a demo)
- **Upstream model token prices**: 0% markup — pass-through at list price

## Provider list (from docs.getbifrost.ai)

23+ providers verified: OpenAI, Anthropic, AWS Bedrock, Google Vertex, Azure, Cohere,
Mistral, Groq, Cerebras, Ollama, Hugging Face, Replicate + custom self-deployed models
(vLLM / SGLang / Ollama endpoints).

## Key performance numbers (vendor-published, not independently re-benchmarked)

- 50× LiteLLM at 500 RPS sustained
- 68% lower memory footprint vs LiteLLM
- <100 microseconds added latency at 5,000 RPS

## OpenAI compatibility

- Default endpoint: `http://localhost:8080/v1/chat/completions` (self-hosted)
- Compatible with OpenAI SDK, Vercel AI SDK, LangChain, Anthropic SDK
- Drop-in: swap base_url only

## Quick start (curl)

```bash
npx -y @maximhq/bifrost
# opens http://localhost:8080 for web UI

curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello, Bifrost!"}]
  }'
```

## Notes / Unverified

- Star count + benchmarks from vendor's own marketing page; no independent third-party
  benchmark of the "50× LiteLLM" claim was found during this run.
- The exact feature parity between OSS and Enterprise is described qualitatively
  ("everything in OSS, plus: guardrails, cluster mode, adaptive load balancing,
  enterprise SSO via SAML and OIDC, Vault support, MCP with federated auth, log
  exports, audit logs"); specific cluster sizing limits, log retention windows,
  Vault integration patterns are not enumerated on the public pricing page.
- No published SaaS endpoint — every customer runs Bifrost in their own VPC,
  on-prem, or air-gapped. Confirmed via marketing site footer.
- Founded/raised information for Maxim (H3 Labs Inc.) not surfaced during this run;
  not part of the verified claim set in the article.

## Re-use for future articles

If a future cron run needs to refresh Bifrost pricing or provider counts, re-fetch
`https://api.github.com/repos/maximhq/bifrost` (returns the same schema: stars,
forks, license, language, topics, pushed_at) and `https://docs.getbifrost.ai`
(provider list + perf numbers).

If the "50× LiteLLM" or "<100µs @ 5k RPS" numbers change, both are sourced from
the getmaxim.ai/bifrost marketing copy (the page uses the exact phrase "50x faster
than LiteLLM with enterprise-grade reliability." in its H1), so a curl + diff
against the page text catches any vendor-side updates.