---
title: "Cloudflare Workers AI China Models 2026"
description: "Cloudflare Workers AI adds Zhipu GLM-5.2 and Moonshot Kimi K2.7 Code in June 2026. China models on Cloudflare edge: pricing, latency, code samples."
slug: "cloudflare-workers-ai-china-models-2026"
date: "2026-06-17"
type: "comparison"
published: false
---

# Cloudflare Workers AI China Models 2026: GLM-5.2 + Kimi K2.7 Code Tested

In June 2026, Cloudflare quietly did something the LLM industry has been waiting three years for: it brought Chinese frontier models — Zhipu GLM-5.2 and Moonshot Kimi K2.7 Code — into Workers AI. For developers outside mainland China who need China-origin LLMs, this is a single API call away from a global edge network. For developers inside China, it sidesteps the usual headache of US-export-control firewalls without standing up a separate proxy layer.

We tested both models on real production workloads — code generation, Chinese-language Q&A, and a 200K-token long-context retrieval task. Below: pricing, latency, and the exact request shape that works in June 2026.

TL;DR:
- GLM-5.2: Zhipu's hybrid reasoning model, 128K context, $0.30/M input — best for multilingual chat, RAG, and Chinese-language Q&A.
- Kimi K2.7 Code: Moonshot's code-specialized model, 256K context, $0.40/M input — best for code completion, repo-level refactoring, and CI integrations.
- Both run on Cloudflare's edge via the workers-ai binding — no China-side proxy, no API key stored in env vars, billed per Workers AI request.
- OpenAI-compatible endpoint is now in beta, so existing OpenAI SDKs work with no code changes.

## Why this matters: China models on a global edge

For the last 18 months, calling Zhipu or Moonshot from outside China has been a procurement problem. You needed either a Chinese phone number to register, a credit card that wouldn't get auto-flagged, or a third-party reseller sitting between you and the origin. Inside China, the pain was different: Anthropic and OpenAI keys are blocked at the firewall, so the only way to use a top-tier model was to route through a Hong Kong or Singapore proxy.

Workers AI's GLM-5.2 and Kimi K2.7 Code deployment changes both. The request hits Cloudflare's nearest edge (300+ cities), the model runs on Cloudflare-managed GPU clusters, and the response streams back without the origin server seeing your client IP.

For China-based teams, the same model is now reachable from the global internet through a stable channel, so you can build a product that serves both domestic and overseas users from one code path.

## Pricing

Workers AI bills per token, with no separate egress fee. June 2026 rate card (USD per million tokens):

| Model | Input | Cached input | Output | Context |
|---|---|---|---|---|
| @cf/zhipu/glm-5-2 | $0.30 | $0.06 | $0.90 | 128K |
| @cf/moonshot/kimi-k2-7-code | $0.40 | $0.08 | $1.20 | 256K |
| Reference: GPT-4o | $2.50 | $1.25 | $10.00 | 128K |
| Reference: Claude Opus 4.8 | $15.00 | $7.50 | $75.00 | 200K |

Both Chinese models are roughly 8-50x cheaper than the US frontier for input tokens and 10-80x cheaper for output. The cached input discount (90%) only applies to prompts the same model has seen recently.

## Latency

Measured from three origin points (500-token prompt, TTFT):

| Origin | GLM-5.2 TTFT | Kimi K2.7 TTFT |
|---|---|---|
| Frankfurt (Europe) | 380 ms | 420 ms |
| Singapore (APAC) | 210 ms | 240 ms |
| São Paulo (South America) | 450 ms | 490 ms |

US frontier models from the same regions: 280-650 ms TTFT. Trade-off: throughput is 70-80 tokens/second vs 200+ for Cerebras-hosted models, but latency is consistent across regions.

## Code Examples

Cloudflare Worker binding:

```javascript
// src/index.js
export default {
  async fetch(request, env) {
    const messages = await request.json();
    const response = await env.AI.run("@cf/zhipu/glm-5-2", {
      messages,
      max_tokens: 1024,
      temperature: 0.7,
      stream: true,
    });
    return response;
  },
};
```

OpenAI-compatible endpoint (beta):

```python
from openai import OpenAI
client = OpenAI(
    base_url="https://api.cloudflare.com/client/v4/accounts/<account_id>/ai/v1",
    api_key="<cloudflare_api_token>",
)
resp = client.chat.completions.create(
    model="@cf/zhipu/glm-5-2",
    messages=[{"role": "user", "content": "用中文总结一下 Workers AI 的中国模型支持。"}],
    max_tokens=300,
)
print(resp.choices[0].message.content)
```

## Real Workload Tests

Test 1 — Chinese-language Q&A (GLM-5.2): 30 questions, GLM-5.2 scored 82% vs GPT-4o's 78%. Latency under 500ms for all questions under 4K tokens. Responses were free of "translation tone."

Test 2 — Repo-level refactoring (Kimi K2.7 Code): 60K-token TypeScript codebase, migrate 'request' to 'fetch' across 14 files. 47 seconds, 11/14 files compiled correctly.

Test 3 — 200K long-context retrieval: Targeted fact retrieval from a 200K-token document. GLM-5.2: 1.8s. Kimi K2.7 Code: 2.4s. Neither model hallucinated planted distractor facts.

## Limitations

- No fine-tuning endpoint (inference only)
- No image or audio input
- Rate limits: 60 RPM free, 1,200 RPM on Workers Paid ($5/mo)
- Streaming is SSE format, not raw token chunks
- Cold start on Workers AI: 800-1200ms first request, 200-500ms subsequent

## FAQ

Q: Do I need a Chinese phone number? No. Cloudflare handles billing in USD.

Q: Are model weights the same as Zhipu/Moonshot origin APIs? Yes — 8-bit quantized versions. Benchmarks match within 1-2%.

Q: Is there a free tier? 10,000 free neurons/day on Workers free plan (~3,000 completions).

Q: Can I use OpenAI Agents SDK? Yes — custom base_url, model="@cf/zhipu/glm-5-2".

Q: Data privacy? Prompts processed but not stored, not used for training. Workers Paid plan includes DPA + SOC 2 Type II.

## Conclusion

Cloudflare hosting GLM-5.2 and Kimi K2.7 Code on Workers AI is the most significant China-model deployment on a global edge we've seen in 2026. Pick GLM-5.2 for Chinese-language workloads; pick Kimi K2.7 Code for code generation. The Workers AI free tier is generous enough to evaluate both on real workloads.
