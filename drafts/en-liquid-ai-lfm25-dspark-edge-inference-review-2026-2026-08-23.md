# Liquid AI LFM2.5 Review 2026: DSpark Edge Inference & Open License Pricing

**Provider:** Liquid AI (liquid.ai) — id: `liquid-ai`
**Date:** 2026-08-23
**Hot-topic source:** 2026-08-23 briefing ⭐#2 (apirank): "Hugging Face LFM2.5 系列 DSpark 草稿模型：推理速度最高提升 3.18 倍" → huggingface.co/blog/LiquidAI/lfm25-dspark
**Archetype:** review + new-provider (open-license edge inference) + news-analysis (LFM2.5-DSpark)

## Decision rationale
- Both earlier apirank ⭐ topics were ALREADY on disk: ⭐#1 (`qwen-3-8-27b-reasoning-effort-overthinking-tokens-2026.astro`, published 08-23 by daily-article cron) and a *different* DSpark story (`dspark-speculative-decoding-2026.astro` = DeepSeek's DSpark, not Liquid's).
- `liquid-ai` was genuinely ABSENT from providers.json (84 entries before this run). The LFM2.5-DSpark release is Liquid AI's story — a fresh, distinct, body-verified news hook (Aug 20-21, 2026 across MarkTechPost / Unite.AI / GIGAZINE / TUN / finance.biggo).

## Verified facts (body-verified, 2026-08-23)
- **LFM2.5-DSpark** (released 2026-08-20): speculative-decoding draft checkpoints for LFM2.5-1.2B-Instruct, LFM2.5-2.6B, LFM2.5-8B-A1B.
  - Up to 3.18× GPU throughput (H100: MATH500 428→1362 tok/s); up to 2.87× on-device (Apple M4 Max).
  - 57% average function-calling latency cut (LFM2.5-2.6B).
  - Lossless exact output (target verifies all proposed tokens; greedy output == target alone).
  - Day-one llama.cpp + SGLang support; open-sourced integration.
- **Business model:** no per-token hosted API. All LFMs free to download/run/fine-tune under royalty-free **LFM Open License** — commercially free until company passes $10M annual revenue. No copyleft (fine-tunes stay private). Research/education/non-profit always free.
- **LEAP Enterprise** tier: commercial license + OEM/on-prem + SLA, priced by deployment scale (contact sales). Adopted by Mercedes-Benz, Shopify.
- **Models:** LFM2.5 text (230M/350M/1.2B-Instruct/Thinking/Base/JP/2.6B/8B-A1B MoE), VL (450M/1.6B/3B), LFM2 (24B-A2B MoE/2.6B/700M). 350M trained 28T tokens, runs under 1GB. 8B-A1B = 8B/1.5B active MoE, 128K context. LEAP SDK cross-platform (iOS/Android/JVM/Linux/Windows).
- **Company:** Boston (est. 2023), ~$2.4B valuation unicorn (GetLatka Nov 2025); NBC Boston + Business Journals coverage Aug 2026.
- **Ecosystem:** 41.3M+ HF downloads.

## External links (all HTTP 200 verified 2026-08-23)
- https://huggingface.co/blog/LiquidAI/lfm25-dspark (200)
- https://www.liquid.ai/pricing (200)
- https://www.liquid.ai/lfm-license (200)
- https://docs.liquid.ai/llms.txt (200)
- https://marktechpost.com (200) — secondary news

## Internal links (all verified on disk / dynamic provider routes)
- /providers/liquid-ai (new provider detail page, auto-rendered)
- /providers/groq, /providers/modal, /providers/deepseek (dynamic)
- /tutorials/qwen-3-8-27b-workers-ai-edge-inference-2026 (edge inference, related)
- /tutorials/dspark-speculative-decoding-2026 (DeepSeek DSpark — differentiation)
- /tutorials/fireworks-ai-serverless-inference-review-2026 (managed open-model serving)
- /tutorials/cheapest-llm-api-pricing-2026 (per-token comparison)

## Files changed
- `src/data/providers.json` — added `liquid-ai` entry (85th provider), 4 reviewSections EN+ZH
- `src/pages/tutorials/liquid-ai-lfm25-dspark-edge-inference-review-2026.astro` (EN)
- `src/pages/zh/tutorials/liquid-ai-lfm25-dspark-edge-inference-review-2026.astro` (ZH)
- `src/pages/tutorials/index.astro` + `src/pages/zh/tutorials/index.astro` — new card (top)
- `drafts/en-liquid-ai-lfm25-dspark-edge-inference-review-2026-2026-08-23.md` + zh twin (this file)

## Metrics (validated)
- EN title 49 chars / EN desc 151 chars / EN ~1450 words
- ZH title 33 chars / ZH desc ~60 chars / ZH ~1500 words
- FAQ: 7 Q&A (EN+ZH json-ld + visible section)
- reviewSections: 4 (table/list/text/text) — sec3/4 EN text 80-130 words (129, 130)
