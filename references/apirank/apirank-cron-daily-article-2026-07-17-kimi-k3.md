# APIRank daily article run — Kimi K3 (2026-07-17)

## Decision

Selected the first uncovered ⭐ apirank topic in the 2026-07-17 briefing: Kimi K3, Moonshot AI's 2.8T open model with native vision and a 1M-token context. The existing `moonshot-kimi-api-review` is a May general review; this is a distinct current-model/API pricing article.

## Verified sources (same run)

- Kimi K3 model guide: https://platform.kimi.com/docs/guide/kimi-k3-quickstart
  - 2.8T parameters; 1,048,576-token context; native text/image/video; automatic caching; JSON/JSON Schema; tool calls, `tool_choice`, dynamic tool loading; K3 always reasons and currently supports `reasoning_effort=max`; web search warning; ¥15 new-user coupon cannot be used for K3; weights planned by 2026-07-27.
- Kimi K3 pricing: https://platform.kimi.com/docs/pricing/chat-k3
  - ¥2/M cached input; ¥20/M uncached input; ¥100/M output; 1,048,576 context.
- Kimi K2.7 Code pricing: https://platform.kimi.com/docs/pricing/chat-k27-code
  - ¥1.30/M cached input; ¥6.50/M uncached input; ¥27/M output; 262,144 context; HighSpeed ¥2.60/¥13/¥54.
- Kimi K2.6 pricing: https://platform.kimi.com/docs/pricing/chat-k26
  - ¥1.10/M cached input; ¥6.50/M uncached input; ¥27/M output; 262,144 context.
- Kimi K3 recharge promotion: https://platform.kimi.com/docs/pricing/promotion
  - 2026-07-16 to 2026-08-12; one eligible first recharge per organization; 10/20/25/30% tiers from ¥99 to ¥5,000+.
- Kimi K3 technical blog: https://www.kimi.com/blog/kimi-k3
  - launch positioning; 2.8T open model; Kimi Delta Attention and Attention Residuals; full weights planned by July 27.

## Files and checks

- EN draft: `drafts/en-kimi-k3-api-review-2026-2026-07-17.md`
- ZH draft: `drafts/zh-kimi-k3-api-review-2026-2026-07-17.md`
- EN/ZH Astro pages: `src/pages/tutorials/kimi-k3-api-review-2026.astro`, `src/pages/zh/tutorials/kimi-k3-api-review-2026.astro`
- Updated existing `kimi` provider entry in `src/data/providers.json` with current K3/K2 model and pricing fields.
- Updated EN/ZH home Latest Tutorials cards and EN/ZH tutorials arrays.
- Updated `drafts/state.json` with published entry and `covered_ids`.
- Affiliate: FreeModel fallback (`https://freemodel.dev/invite/FRE-7a3b6220`); Moonshot has no public affiliate program. CTA appears in both language articles with `rel="sponsored noopener" target="_blank"`.
- Article body: EN ~2,377 words; ZH ~1,027 whitespace-delimited CJK/Latin tokens; 7 FAQs; 2 comparison tables per language; two code examples (curl + Python) per language.
- Astro frontmatter starts with `---`; JSON-LD is rendered inside `<article>` via three `set:html` script tags; generated body has zero unescaped template-literal backticks.

## Deployment

Build and Cloudflare Pages deploy are the remaining live verification steps. Use the conservative APIRank heap tier selected from `free -m`, then verify both live URLs with Mozilla UA, title, body keyword, and FAQ JSON-LD counts.
