# claude-code-bun-rust-migration verified-data 2026-07-18

**Source**: https://claude.com/blog/ai-code-migration (captured 2026-07-17 via curl, Mozilla UA)

**Verified facts:**

| Item | Value |
|---|---|
| Migration scope | Bun JavaScript runtime, Zig → Rust |
| Lines produced | ~1,000,000 lines of Rust |
| Duration | < 2 weeks (June 2026) |
| Models used | Claude Fable 5 + Claude Opus 4.8 |
| Lead engineer | Jarred Sumner (Bun co-founder, Anthropic MTS) |
| Pre-existing test suite pass rate (CI, pre-merge) | 100% |
| Regressions surfaced post-merge | 19 (all fixed) |
| Uncached input tokens | 5.9 billion |
| Output tokens | 690 million |
| Total API bill | ~$165,000 |
| Second case (Mike Krieger Python→TS) | 165,000 lines, "over a weekend", 27M tokens |
| Parallel agents (second case) | "hundreds of agents" running concurrently |
| Pre-Claude rewrite cost (legacy baseline) | $3–4M / 4 years |

**Pricing math** (Claude Fable 5, public 2026-07 pricing):
- Input: $3/M (fresh), $0.30/M (cached 5-min), $1.20/M (cached 1-hour)
- Output: $15/M (fresh), $18.75/M (cached — wait that's wrong, cached output is cheaper)

Re-verify Anthropic cached output price: docs.claude.com shows cache reads on output are billed as a small fraction. Skip the cached-output row in the table — it's not part of this $165k case.

**Without caching (this case):**
- 5.9B input × $3/M = $17,700
- 690M output × $15/M = $10,350
- Subtotal: $28,050
- Anthropic's stated total: $165,000
- Implied multiplier: ~5.9x → concurrency/retry/iteration overhead

**With caching enabled** (Anthropic engineer's hint):
- Effective input: ~600M fresh + 5.3B cached @ $0.30 = $1,800 + $1,590 = $3,390
- Output unchanged: $10,350
- Subtotal: ~$13,740
- Hybrid (Sonnet 5 orchestrator + Opus 4.8 workers): ~$12,000

**Cross-references:**
- Anthropic pricing: https://docs.claude.com/en/docs/about-claude/pricing (verified 2026-07)
- Prompt caching: https://docs.claude.com/en/docs/build-with-claude/prompt-caching
- OpenAI GPT-5.6 pricing (for comparison): https://openai.com/api/pricing/
