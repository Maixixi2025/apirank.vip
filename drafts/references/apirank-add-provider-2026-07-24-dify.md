# Dify Add-Provider-and-Review — 2026-07-24

Provider #66 Dify (dify.ai) added to apirank.vip. Aggregator category.

## Key learnings
- **No new pitfalls** — all existing patterns (v3 build OOM fix, double-brace cross-check, backtick escaping, 4-file discoverability) held correctly.
- **Pre-existing bug from daily cron:** the 2026-07-24 comparison article (gpt-5-vs-claude-4-vs-gemini) had `{{}}` double-brace syntax in both `set:html={...}` and `BaseLayout` props. Fixed both EN and ZH variants. When the daily article cron (09:15) and add-provider cron overlap, always grep for `set:html=\{\{` and `title=\{\{` across all recently-created files before building.
- **Dify affiliate:** PartnerStack-based at dify.ai/partners — no direct affiliate URL pattern, partner program requires application.
- **Providers count:** 66 providers, still fitting in providers.json without size issues.

## Build
- 454 HTML pages, ~15s build time
- v3 OOM recipe: `NODE_OPTIONS='--max-old-space-size=384 --max-semi-space-size=64'` + `npx astro build --logLevel error`

## Deploy
- wrangler: 444 files, 3.11s upload
- Git: commit `bfc604c`, 12 files, 1338 insertions, 12 deletions
- Both EN and ZH URLs live within seconds
