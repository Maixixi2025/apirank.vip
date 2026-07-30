---
title: "OpenRouter Data Residency 2026: EU Routing + ZDR"
description: "OpenRouter's Sovereign AI stack: provider object, ZDR toggle, and the enterprise-only eu.openrouter.ai base URL. GDPR vs PIPL coverage."
slug: "openrouter-data-residency-2026"
provider: "openrouter"
published: false
date: "2026-06-24"
type: "analysis"
---

# OpenRouter Data Residency 2026: EU Routing + ZDR

On June 22, 2026, OpenRouter published a blog post titled *"How to Enforce AI Data Residency Without Building Local Infrastructure"*. The post packaged an existing toolkit under a new brand name — **"Sovereign AI"** — and added one new operational primitive: an enterprise-only `eu.openrouter.ai` base URL that hard-locks decryption and processing to the EU.

This article walks through every layer of the stack, from the per-request `provider` object that any account can use, to the enterprise EU endpoint that 26 models currently serve. You'll see real code, live model counts (verified June 24), and a side-by-side comparison with the alternatives — Cloudflare AI Gateway, LiteLLM, and Portkey — that compliance teams typically evaluate.

The short version: OpenRouter is the only one of the four that exposes a single managed region URL. Everyone else requires you to wire the region pin yourself at the provider layer.

## What "Sovereign AI" actually means

OpenRouter did not ship a single named feature. The June 2026 push bundles three pre-existing primitives under a marketing brand:

1. **Per-request `provider` object** — filter and pin upstream providers in the request body
2. **Zero Data Retention (ZDR) toggle** — account-wide, per-model-group, and per-API-key guardrails
3. **`eu.openrouter.ai` base URL** — enterprise-only, hard EU jurisdiction for decryption and processing

The first two work for any account. The third requires an enterprise contract (sales contact, not a SKU). Together they cover GDPR, EU AI Act enforcement, and country-of-origin procurement — but not Chinese PIPL/DSL data localization. There is no China region, no Chinese providers on the EU list, and no documented CN endpoint.

The operational reality: OpenRouter's residency is enforced at the **router layer**. It decides which upstream provider to call, then calls that provider's existing endpoint. The residency controls therefore work for any provider that OpenRouter routes to and that publishes a regional endpoint — Anthropic, OpenAI, Google, Amazon Bedrock, and 20+ others.

## The `provider` object: per-request routing DSL

The most useful control is also the simplest. Any OpenRouter account can add a `provider` object to a chat completions request to filter and pin upstream routing.

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4.6",
    "messages": [{"role": "user", "content": "Summarize this compliance report."}],
    "provider": {
      "order": ["anthropic", "amazon-bedrock"],
      "allow_fallbacks": false,
      "data_collection": "deny",
      "zdr": true
    }
  }'
```

The four most important fields for residency use cases:

| Field | Type | Default | Residency effect |
|---|---|---|---|
| `order` | string[] | – | Try providers in this priority order |
| `only` | string[] | – | Allow only these provider slugs (hard restriction) |
| `data_collection` | `"allow"` / `"deny"` | `"allow"` | `"deny"` excludes providers that store or train on inputs |
| `zdr` | boolean | – | Restrict to Zero-Data-Retention endpoints only |

Two more fields matter for compliance audit trails: `allow_fallbacks: false` returns an error instead of silently falling through to a non-listed provider (useful when you need a written guarantee that a specific provider served the request), and the response carries a **Router Metadata** header that records which provider actually handled the call. That audit header is the bread-and-butter evidence you cite in a SOC 2 or ISO 27001 control review.

A common pattern: pin to Bedrock-hosted models in Frankfurt for EU compliance:

```python
import os
import requests

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "anthropic/claude-sonnet-4.6",
        "messages": [{"role": "user", "content": "Extract vendor names from this contract."}],
        "provider": {
            "order": ["amazon-bedrock"],
            "only": ["amazon-bedrock"],
            "data_collection": "deny",
            "zdr": True,
            "allow_fallbacks": False,
        },
    },
    timeout=30,
)
data = response.json()
# Audit trail: which provider served this request?
provider_used = response.headers.get("x-openrouter-provider")
print(f"Provider: {provider_used}")
```

The `only` + `allow_fallbacks: false` combination is the safest. Without it, a transient outage on Bedrock would silently fall through to a non-EU provider.

## ZDR: per-model-group and per-key

The Zero Data Retention toggle is the second layer. It's a **per-model-group** setting in `/settings/privacy`:

- **Anthropic** — first-party endpoints removed; Amazon Bedrock and Google Vertex remain
- **OpenAI** — first-party endpoints removed; Azure remains
- **Google** — AI Studio removed; Vertex remains
- **Non-frontier** — applies to providers that don't fit the above buckets

The behavior is consistent: when ZDR is on for a group, OpenRouter filters out any provider in that group that retains data. For a compliance buyer this is straightforward — turn on ZDR for every group that contains a model you might use, and you've removed the worst offenders from the fallback pool.

For team-level enforcement, OpenRouter has **guardrails** — per-API-key objects that can enforce ZDR by group:

```typescript
const openRouter = new OpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY!,
});

await openRouter.guardrails.create({
  api_key_id: '<KEY_ID>',
  enforce_zdr_anthropic: true,
  enforce_zdr_openai: true,
  enforce_zdr_google: true,
  enforce_zdr_other: true,
});
```

These OR with the per-request flags — you can only strengthen, not weaken. That's the right semantic: a developer can't accidentally route a compliance workload to a non-ZDR provider if the key is locked.

## The `eu.openrouter.ai` base URL: hard EU jurisdiction

This is the new piece. Enterprise accounts can switch the base URL from `https://openrouter.ai/api/v1` to `https://eu.openrouter.ai/api/v1`, and the request is decrypted and processed entirely within the EU before being forwarded to an EU-region upstream provider.

The integration is a one-line change in the SDK:

```typescript
import { OpenRouter } from '@openrouter/sdk';

const openRouter = new OpenRouter({
  apiKey: '<OPENROUTER_API_KEY>',
  serverURL: 'https://eu.openrouter.ai/api/v1',  // <-- the only change
});

const completion = await openRouter.chat.send({
  model: 'meta-llama/llama-3.3-70b-instruct',
  messages: [{ role: 'user', content: 'Hello' }],
  stream: false,
});
```

Or with raw `fetch`:

```typescript
const res = await fetch('https://eu.openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <OPENROUTER_API_KEY>',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'anthropic/claude-sonnet-4.6',
    messages: [{ role: 'user', content: 'GDPR audit summary' }],
  }),
});
```

To see what models the EU endpoint serves, query its model list directly:

```bash
curl https://eu.openrouter.ai/api/v1/models | jq '.data | length'
# 26 (as of 2026-06-24)
```

The 26 models break down roughly as: 8 Anthropic (Claude Opus 4.5–4.8, Sonnet 4–4.6, Haiku 4.5), 11 OpenAI (GPT-4o-mini, GPT-4.1 family, GPT-5 family, GPT-5.5, GPT-OSS 20B/120B), 3 Google (Gemini 2.5 Pro/Flash/Flash-Lite), and 4 Amazon (Nova Micro/Lite/Pro and Nova 2 Lite). The 26 are the subset of OpenRouter's 338-model main catalog that are routed through EU-region upstream providers.

One nuance worth flagging: the OpenRouter blog frames **Mistral** as an "EU-jurisdiction anchor" you can pin via `provider.only: ["mistralai"]`. That's true for the main endpoint — Mistral is in the main catalog with 20+ models. But Mistral is **not** on the `eu.openrouter.ai` endpoint list. If you need a hard EU-jurisdiction guarantee, Mistral alone is not enough; you need an EU-region upstream for the model you're using (e.g. Anthropic via Bedrock Frankfurt, or OpenAI via Azure Sweden).

## Pricing: 0% markup, 5.5% platform fee

No residency surcharge appears in public materials. The pricing model is the same as standard OpenRouter:

- **0% markup** on underlying provider prices
- **5.5% platform fee** on credit purchases, **$0.80 minimum**
- **5%** with **Bring Your Own Key (BYOK)**
- **First 1M requests/month waived** (on BYOK)
- **Failed requests not billed**
- **20+ free models** for evaluation

The EU in-region endpoint itself is gated behind enterprise sales contact (`https://openrouter.ai/enterprise/form`) rather than a SKU. For a serious compliance buyer, expect an enterprise contract, not pay-as-you-go credits.

For comparison: a typical EU-pinned workload at 1M requests/month on BYOK is roughly 5% on top of upstream provider list price. The "no markup + 5% platform fee" framing is competitive against going direct — direct Anthropic, OpenAI, and Google all charge standard list price, but you'd need to wire three separate accounts, three separate SSO integrations, and three separate vendor-risk reviews.

## How the alternatives stack up

The four approaches compliance teams typically evaluate:

| Approach | Residency mechanism | How it's configured | Pricing | Caveats |
|---|---|---|---|---|
| **OpenRouter `provider` object** | Filter providers by data policy / ZDR | `provider.only`, `provider.zdr`, `provider.data_collection` in body | Included in 5.5% platform fee | "Region" = provider-headquartered; not hard jurisdiction |
| **OpenRouter `eu.openrouter.ai`** | Hard EU jurisdiction | Switch base URL to `https://eu.openrouter.ai/api/v1` | Enterprise, contact sales | EU only; 26 models; Mistral not on the EU list |
| **Cloudflare AI Gateway** | No native region-routing | Caching, rate limits, retry/fallback only | Free tier + Workers paid plan | No residency primitive in the gateway itself |
| **LiteLLM (self-hosted)** | Your network, your jurisdiction | `model_list` with `openrouter/...` upstream | Free OSS; infra ~$200–$500/mo | No SOC 2 / ISO 27001 / HIPAA certs on the OSS build |
| **Portkey** | Control-plane over your provider keys | BYOK + guardrails + PII redaction | $49/mo Production; Enterprise for HIPAA | Acquired by Palo Alto Networks in 2026; HIPAA + BAAs on Enterprise |
| **Direct provider region-pinned endpoints** | Provider's own regional endpoints | `region: eu` on Vertex, Azure EU, AWS Bedrock in `eu-central-1` | Provider list price | Each provider defines "region" differently |

The key takeaway: **OpenRouter is the only one of the four managed options that exposes a single managed EU-only base URL.** Cloudflare AI Gateway (the infrastructure under OpenRouter itself) does not expose residency as a first-class control — caching, rate limiting, retry/fallback only, as of the last doc update on April 20, 2026. LiteLLM gives you full sovereignty because you host it, but you own the SOC 2 / ISO 27001 / HIPAA certification. Portkey adds HIPAA + BAAs on its Enterprise plan but no managed EU base URL.

If you need a BAA for healthcare, the answer is Portkey Enterprise plus your own provider BAAs (Azure OpenAI, AWS Bedrock with a BAA). If you need a managed EU endpoint and don't need HIPAA, OpenRouter is the cleanest answer.

## Compliance use cases, mapped

| Regime | How OpenRouter helps | What's missing |
|---|---|---|
| **GDPR (Articles 44–50)** | `data_collection: "deny"` + `zdr: true` for Schrems-II-style data minimization; `eu.openrouter.ai` for hard EU jurisdiction | Article 30 records of processing — must be at the controller level, not the API |
| **EU AI Act (2026 enforcement)** | Same primitives; Sovereign AI doc calls it out by name | Risk classification documentation must be at the deployer level |
| **Deloitte "country of origin" procurement** | 77% of 3,235 surveyed leaders now factor country of origin into vendor selection | Vendor risk questionnaires still need to be filled out per-provider |
| **Financial services (PCI-DSS, FINRA, OCC)** | ZDR per-model-group toggle, guardrails per API key for segregation of duties, Router Metadata header for audit trail | SOC 2 Type 2 report at `https://trust.openrouter.ai` is sufficient for most, but not all, third-party risk teams |
| **Healthcare (HIPAA — US-side)** | Partial: ZDR + `data_collection: "deny"` + EU/US-only base URL | OpenRouter is **not** HIPAA-certified; a BAA must be at the provider layer (Azure OpenAI, AWS Bedrock with a BAA) |
| **China data localization (PIPL, DSL)** | **No coverage** | No China region, no Chinese providers on the EU list, no documented CN endpoint. This is a real gap. |
| **Defense / air-gapped** | Not the right answer | "The infrastructure framing fits governments, defense contractors, and air-gapped environments" — for those, self-hosted LiteLLM is the only option. |

The China gap is worth repeating. If you're serving a Chinese user base and need PIPL compliance, OpenRouter is not the answer. You'd need a China-region upstream (Alibaba Qwen, DeepSeek, Zhipu GLM, Moonshot Kimi, etc.) configured at the provider layer, plus your own data localization controls. That's outside the scope of what OpenRouter offers today.

## A 30-line implementation recipe

Putting it all together for a typical EU compliance workload:

```python
# requirements: requests, python-dotenv
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 1. Use the EU endpoint if your contract covers it
# 2. Pin to a single EU-region upstream
# 3. Enforce ZDR + data_collection: deny
# 4. Disable fallbacks so a transient outage surfaces as an error
# 5. Capture the router metadata for audit logs

def compliance_chat(prompt: str, model: str = "anthropic/claude-sonnet-4.6") -> dict:
    base = os.environ.get("OPENROUTER_BASE", "https://openrouter.ai/api/v1")
    # Switch to EU endpoint for hard jurisdiction (enterprise only)
    if os.environ.get("EU_RESIDENCY") == "true":
        base = "https://eu.openrouter.ai/api/v1"

    response = requests.post(
        f"{base}/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "provider": {
                "order": ["amazon-bedrock"],
                "only": ["amazon-bedrock"],
                "data_collection": "deny",
                "zdr": True,
                "allow_fallbacks": False,
            },
        },
        timeout=30,
    )
    response.raise_for_status()

    # Audit trail
    return {
        "provider": response.headers.get("x-openrouter-provider"),
        "content": response.json()["choices"][0]["message"]["content"],
    }


if __name__ == "__main__":
    result = compliance_chat("Summarize this vendor risk report in 3 bullets.")
    print(f"Served by: {result['provider']}")
    print(result["content"])
```

Two patterns worth keeping in mind: the `EU_RESIDENCY=true` env-var pattern lets you flip between the main and EU endpoints without code changes, and the per-request `provider` object ORs with the account-wide ZDR setting — both have to be on for the strictest guarantee.

## FAQ

**Q: Does the `eu.openrouter.ai` endpoint add latency?**
A: The endpoint itself does not. Your request is decrypted and routed from EU infrastructure, and the upstream provider is also called in-region. End-to-end latency is comparable to the main endpoint for the same model.

**Q: Can I pin a specific upstream (e.g. Azure Sweden vs AWS Frankfurt) for the same model?**
A: Indirectly, via `provider.order` with `allow_fallbacks: false`. The provider slug for Azure is typically `azure` and for AWS Bedrock is `amazon-bedrock`; OpenRouter routes to whichever the order specifies. Direct region pinning within a provider (e.g. forcing AWS Frankfurt over AWS Ireland) is not exposed — that has to be configured on the provider side.

**Q: Is there a free tier for the EU endpoint?**
A: The EU endpoint is enterprise-gated. There is no public free SKU; you need to contact sales for access.

**Q: Does ZDR cover fine-tuning data?**
A: No. ZDR covers inference only. Fine-tuning is a separate workflow that uses provider-specific endpoints and is not currently exposed through OpenRouter's residency controls.

**Q: How does OpenRouter handle the new EU AI Act requirements?**
A: The Sovereign AI doc explicitly calls out EU AI Act compliance. The combination of `data_collection: "deny"`, ZDR, and the `eu.openrouter.ai` endpoint is positioned as the operational primitive. Risk classification and conformity assessments remain the deployer's responsibility under Article 17.

**Q: What's the difference between ZDR and `data_collection: "deny"`?**
A: ZDR means the provider does not retain the prompt or response at rest. `data_collection: "deny"` means the provider does not use the data to train future models. A provider can have one without the other — for example, a provider might retain logs for 30 days (violating ZDR) but never train on inputs (satisfying `data_collection: "deny"`). For the strictest guarantee, set both.

## Verdict

OpenRouter's June 2026 push is best understood as: **a blog post (data-residency framing) + a new enterprise-only EU endpoint that hardens an existing toolkit.** The toolkit is mature — the `provider` object, ZDR toggles, and guardrails have been there for months. What changed is that you can now point at a single managed URL and tell your compliance team "all inference happens in the EU."

If you're building an EU product and don't need a BAA, OpenRouter is the cleanest managed option today. If you need HIPAA, you need Portkey Enterprise plus provider BAAs. If you need PIPL data localization, you need a China-region provider stack — OpenRouter does not cover it. If you need full sovereignty, self-hosted LiteLLM is the only path.

The one thing not to do: assume that the OpenRouter brand name "Sovereign AI" alone is a compliance artifact. It's a marketing label. The actual controls are the `provider` object, the ZDR toggles, and the `eu.openrouter.ai` endpoint — and you need to wire all three correctly to get the guarantee you're promising your auditor.

---

If you ship to production and want to consolidate multi-provider traffic (OpenAI, Anthropic, Google) through one OpenAI-compatible endpoint with built-in ZDR and provider routing, [**FreeModel**](https://freemodel.dev/invite/FRE-7a3b6220) is a China-direct aggregator that mirrors the OpenRouter pattern with DeepSeek, Qwen, GLM, and Kimi under the hood. It runs a similar `provider` object shape on its enterprise tier and is the closest domestic equivalent for teams that need China access alongside EU/US routing.
