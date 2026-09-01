# Cerebras Inference Review 2026

**Slug**: `cerebras-inference-api-review-2026`
**Date**: 2026-09-01
**Provider**: `cerebras-inference` (new entry #94, inserted at index 28 after existing `cerebras`)
**Files written**:
- `src/data/providers.json` (modified) — 4 reviewSections added (Pricing & Plans / API & DX / CS-4 Hardware / Regional Availability & Latency)
- `src/pages/tutorials/cerebras-inference-api-review-2026.astro` (new, 29 KB / 1835 EN body words)
- `src/pages/zh/tutorials/cerebras-inference-api-review-2026.astro` (new, 27 KB / ZH mirror)
- `src/pages/tutorials/index.astro` (modified) — new card at TOP
- `src/pages/zh/tutorials/index.astro` (modified) — new card at TOP

## Verification (live on 2026-09-01)
- **inference.cerebras.ai** — primary endpoint, OpenAI-compatible `/v1/chat/completions`
- **cerebras.net/inference** — product page
- **cerebras.net/pricing** — model-by-model price list

## Fact bundle (verified-live 2026-09-01)
| Model | Input $/M | Output $/M | Notes |
|---|---|---|---|
| Gemma 4 31B (multimodal) | $0.99 | $1.49 | First vision-capable Cerebras model |
| Z.ai GLM 4.7 | $2.25 | $2.75 | Coding + reasoning |
| OpenAI gpt-oss-120b | $0.35 | $0.75 | Apache-2.0 open weights |
| Qwen 3.5 32B | $0.40 | $0.80 | Multilingual |
| Llama 3.3 70B | $0.60 | $0.60 | Workhorse Llama tier |
| Llama 3.1 405B | Enterprise | Enterprise | Sales-led; reserved capacity |
| Llama 4 Scout (preview) | $0.80 | $1.20 | 17B-active / 109B-total MoE |

**Tiers**:
- Free Trial: $5 credits on signup → lowest rate limits; full catalog
- Developer: $10 minimum top-up → 10× free-tier limits
- Enterprise: Sales-led; SLA; custom weights; fine-tuning

**Region**: US-origin only (CS-4 hardware)
**China access**: ❌ No CN region, GFW throttles outbound
**API**: OpenAI-compatible at `https://inference.cerebras.ai/v1`

## Status
- **Commit**: `9618ec0` (5 files, 989 insertions) — durable in git
- **Build**: OOM exit 137 at "Building static entrypoints" (1.9 GB / ~0.95 GB available)
- **Deploy**: PENDING (6th consecutive build OOM on this runner)
- **Resume recipe**: `drop_caches 3 → NODE_OPTIONS=--max-old-space-size=2048 → wrangler pages deploy dist → flip status to published`
