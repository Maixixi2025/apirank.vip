---
title: "OpenRouter MCP Server 2026: 400+ Models in 5 Min"
description: "OpenRouter MCP server: connect Claude Code, Codex, Cursor to 400+ LLMs with one URL. Setup guide, code examples, comparison to manual routing."
pubDate: 2026-06-28
provider: openrouter
category: tutorial
featured: true
---

# OpenRouter MCP Server 2026: 400+ Models in 5 Minutes From Claude Code, Codex, or Cursor

**Article path:** `src/pages/tutorials/openrouter-mcp-server-2026.astro`
**Publish date:** 2026-06-28
**Status:** draft (awaiting user publish confirmation)

## Article summary

On June 27, 2026, OpenRouter shipped a first-party MCP (Model Context Protocol) server that exposes its entire 400+ model catalog as native tools inside Claude Code, Codex, Cursor, Cline, and any MCP-compatible client. The pitch is simple but powerful: instead of hand-editing model slugs and re-pasting curl snippets every time you want to compare GPT-5.5 against Claude Fable 5 against Gemini 3.1 Pro, your IDE now does it for you.

## TL;DR

OpenRouter's MCP server is a remote endpoint at `https://mcp.openrouter.ai/mcp` that exposes five tools — `model_search`, `model_info`, `pricing_compare`, `provider_routing`, and `chat_completion` — over Streamable HTTP transport. Setup is a 5-line JSON config in `~/.claude/mcp_servers.json`. Works with Claude Code, Codex CLI, Cursor, Cline, Continue.dev, Zed. Pricing is live. OAuth 2.1 + PKCE auth. Free for read tools; standard 5.5% fee on chat.

## Outline

1. **What the MCP Server Actually Exposes** — five tools explained (4 read-only + 1 chat)
2. **Setup: Claude Code** — 5-line JSON config + first tool call
3. **Setup: OpenAI Codex CLI** — same pattern, different config path
4. **Setup: Cursor** — Settings UI walkthrough
5. **Setup: Cline / Continue.dev / Zed** — VS Code, Continue, Zed patterns
6. **What It Looks Like in Practice** — workflow comparison: with vs without MCP
7. **Architecture: How It Stays Fast and Fresh** — Streamable HTTP, live pricing, OAuth 2.1
8. **Comparison Table: MCP vs Manual vs Custom Proxy** — 4-row matrix
9. **Limitations and Gotchas** — no streaming, fee display quirks, tool count per client
10. **FAQ** — 6 questions (free, Claude Desktop, free account, REST vs MCP, provider-direct, ZDR)
11. **Conclusion** — affiliate CTA

## Affiliate link suggestions

- **Primary: OpenRouter** — `https://openrouter.ai/affiliates` (theme = MCP server for IDE coding agents, OpenRouter affiliateAvailable: true)
- **Secondary: FreeModel** — `https://freemodel.dev/invite/FRE-7a3b6220` (China-direct access fallback for when OpenRouter routing doesn't reach needed regions)

## Internal links in article

- OpenRouter API Review (openrouter-review)
- OpenRouter Fusion API (openrouter-fusion-api-2026)
- OpenRouter Data Residency (openrouter-data-residency-2026)
- OpenRouter Q2 Token Share (openrouter-q2-2026-token-share-leaderboard)

## Build status

- ✅ Build OK (335 pages)
- ✅ Title 58 chars (limit 60)
- ✅ Description 142 chars (limit 70-155)
- ✅ JSON-LD: WebSite + Organization + Article + BreadcrumbList + FAQPage (5 blocks)
- ✅ FAQ: 6 questions, parseable
- ✅ H2: 11 sections
- ✅ Word count: 1995 (target 1500-2500)
- ✅ Affiliate links: 3 (1 OpenRouter + 1 FreeModel + 1 sidebar OpenRouter)

## Verification steps for publish

1. `git add -A && git commit -m "Add OpenRouter MCP server guide"`
2. `cd /root/apirank && npm run build`
3. `npx wrangler pages deploy dist --project-name=apirank-vip --commit-dirty=true`
4. `curl -sIL --max-time 15 -A "Mozilla/5.0" https://apirank.vip/tutorials/openrouter-mcp-server-2026/` must return HTTP 200
5. `curl -sIL --max-time 15 -A "Mozilla/5.0" https://apirank.vip/zh/tutorials/openrouter-mcp-server-2026/` must return HTTP 200

DO NOT push to GitHub — CF Pages Git auto-deploy will OOM fail. Use wrangler only.
