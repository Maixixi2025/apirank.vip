# Qwen3.8 vs Kimi K3: Open-Source 2T+ Models API Comparison (2026-07-21)

## Verified-data summary

| Field | Qwen3.8-Max-Preview | Kimi K3 |
|---|---|---|
| Vendor | Alibaba Cloud Bailian (Model Studio) | Moonshot AI |
| Released | 2026-07-19 | 2026-07-12 |
| Total params | 2.4T (MoE) | 2.8T |
| Context | 1M class (long) | 1,048,576 tokens (1M) |
| Native vision | Via separate Qwen-VL model id | Yes (image + video on same endpoint) |
| Function calling | Full | Full (tool_choice, dynamic loading, JSON Schema) |
| Structured output | JSON Schema | JSON mode + JSON Schema |
| Auto context caching | Not exposed (manual prompt reuse) | Yes (auto, cache-hit rate) |
| API protocols | OpenAI / Anthropic / DashScope | OpenAI-compatible |
| Regions | 5 (Beijing, Singapore, Tokyo, Frankfurt, Virginia) | China-mainland |
| Access model | Token Plan subscription | Pay-as-you-go (prepaid) |
| Input cache miss | Token Plan quota | ¥20 / M tokens |
| Input cache hit | N/A | ¥2 / M tokens |
| Output | Token Plan quota | ¥100 / M tokens |
| Reasoning control | Default on, no public knob | On, `reasoning_effort=max` only |

## Sources verified

- Aliyun help center text-generation page: https://help.aliyun.com/zh/model-studio/text-generation-model (last-modified 2026-07-19, confirmed Qwen3.8-Max-Preview positioned as GPT-5.5 / Claude Opus 4.7 / Gemini 3.1 Pro competitor)
- Aliyun model list: https://help.aliyun.com/zh/model-studio/models (confirmed `qwen3.8-max-preview` model card "Token Plan only")
- Token Plan overview: https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/overview
- Kimi docs: https://platform.kimi.com/docs (K2.7/K2.6/K3 pricing)
- Kimi platform: https://platform.kimi.com (CNY pricing, K3 coupon exclusion)
- @Alibaba_Qwen launch post: https://x.com/Alibaba_Qwen/status/2078754377473601787 (2.4T params, 2026-07-19)

## Pipeline

1. Briefing read: 2026-07-21 daily-hot-topics cron, ⭐ priority = "Qwen3.8 + Kimi K3 双开源 2T+ 模型横评"
2. State.json check: 96 published articles, no prior Qwen3.8 article, kimi-k3-api-review-2026 covers Kimi K3 in isolation (news angle ≠ existing review)
3. Verified-data probe: urllib.request against aliyun docs (1049KB models page with confirmed Qwen3.8-Max-Preview card)
4. Title/description pre-flight:
   - EN title: 44 chars (BaseLayout +10 → 54 chars, within 60 limit)
   - EN desc: 144 chars (within 70-155 limit)
   - ZH title: 37 chars (BaseLayout +10 → 47 chars, within 60 limit)
   - ZH desc: 93 chars (within 70-155 limit)
5. Article assembly: 1905 EN words / 2479 ZH chars, 11 H2 sections, 8 FAQPage questions
6. JSON-LD as `<script type="application/ld+json">` inside `<article>` body (verified pattern from 2026-07-15 Claude Tokenizer fix)
7. Discoverability: 4 files touched — EN+ZH homepages (before vercel card) + EN+ZH tutorials lists (top of array)
8. Build: `NODE_OPTIONS=--max-old-space-size=300 npx astro build --silent` → 16.0s, exit 0
   - heap=400 was OOM-killed (MemAvailable=1025MB); heap=300 worked
9. Deploy: `wrangler pages deploy dist --project-name=apirank-vip --commit-dirty=true` → 15.3s, deployment ID `61740c59`, 187 new files uploaded
10. Live verify: EN URL 35,656B, ZH URL 25,778B, both with correct titles, 8 FAQ questions, 3 JSON-LD types (Article+BreadcrumbList+FAQPage), all 5 unique content markers (qwen3.8-max-preview, kimi-k3, Token Plan, 1,048,576, moonshot)
11. State.json: published 96→97, covered_ids 22→24 (added qwen3.8 + kimi-k3)
12. Selective git add: 7 files (+181/-3); commit 6dc4ceb; pushed 0aefeed..6dc4ceb

## Key decisions

- **Slug**: `qwen3-8-vs-kimi-k3-open-source-2t-models-api-2026` (single slug covers both models, no need for separate per-model reviews since both shipped within 8 days and share the same news hook)
- **Category**: News Analysis (not Provider Review — Qwen3.8-Max-Preview is a tier inside the existing `aliyun` provider, not a new provider)
- **Title style**: keyword_front (Qwen3.8 vs Kimi K3) + function (2T+ Open Models API 2026) — matches seo-title pattern
- **Affiliate CTA**: none — neither Qwen3.8 nor Kimi K3 has an affiliate program; section-8 disclosure is the only CTA-adjacent text
- **ZH import path**: `../../../layouts/BaseLayout.astro` (3-layer, matches all other ZH tutorials — was a bug in earlier 2026-06-06 crons, now standardized)

## NEW lessons

1. **Qwen3.8-Max-Preview has no public per-token pricing card.** Unlike Kimi K3 (¥2/¥20/¥100), the 3.8-Max-Preview tier is gated behind Token Plan subscription. The article acknowledges this honestly with "cost is plan-dependent" rather than inventing numbers — verified-data protocol from 2026-07-15 Claude Tokenizer run.

2. **Token Plan-only access for top-tier preview models is a recurring 2026 pattern.** When a vendor releases a flagship preview tier (Qwen3.8-Max-Preview here, similar to Claude Opus 4.7 preview / GPT-5.5 preview earlier in the year), they gate it behind a plan subscription rather than a per-token rate. The article calls this out explicitly so buyers don't waste time looking for a rate card.

3. **The 2T+ open-weights inflection is the structural story.** The body frames both models as part of a wider industry shift — open-weights 2T+ models in production APIs within an 8-day window. This is the editorial angle that justifies the comparison article format vs. two separate per-model reviews.

## Verified-data file

This is the run record. The full 13-row spec table from the article body is the canonical verified-data table for both models as of 2026-07-21.
