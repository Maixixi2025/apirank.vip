# Claude Tokenizer 2026 — Verified Data (2026-07-15)

## Source
- **Primary methodology**: Playcode — [The Same TypeScript Costs 73% More on Claude Than on GPT](https://playcode.io/blog/real-price-of-frontier-models) (Ruslan Ianberdin, July 13, 2026; updated July 14, 2026). 16 byte-for-byte matched fixtures, cross-verified against Anthropic `count_tokens`, OpenAI `tiktoken` `o200k_base`, and live billed `usage.input_tokens` on GPT-5.1, GPT-5.5, GPT-5.6 Sol. Gemini and Grok via providers' own count endpoints. DeepSeek and GLM excluded (no production tokenizer counts).

## Anthropic Pricing (live, 2026-07-15, anthropic.com/pricing)
| Model | Input | Output | Cache Write | Cache Read |
|---|---|---|---|---|
| Sonnet 4.6 | $3/MTok | $15/MTok | $3.75/MTok | $0.30/MTok |
| Sonnet 5 (intro through Aug 31, 2026) | $2/MTok | $10/MTok | $2.50/MTok | $0.20/MTok |
| Sonnet 5 (standard from Sep 1, 2026) | $3/MTok | $15/MTok | $3.75/MTok | $0.30/MTok |
| Opus 4.6 | $5/MTok | $25/MTok | $6.25/MTok | $0.50/MTok |
| **Opus 4.7** | $5/MTok | $25/MTok | $6.25/MTok | $0.50/MTok | (likely new tokenizer)
| **Opus 4.8** | $5/MTok | $25/MTok | $6.25/MTok | $0.50/MTok | (new tokenizer, 1.50× effective)
| Haiku 4.5 | $1/MTok | $5/MTok | $1.25/MTok | $0.10/MTok |

## OpenAI Pricing (live, 2026-07-15, platform.openai.com/docs/pricing)
| Model | Input | Cached Input | Output |
|---|---|---|---|
| gpt-5.1 | $1.25/MTok | — | $10.00/MTok |
| gpt-5.5 | $5.00/MTok | $0.50/MTok | $30.00/MTok |
| **gpt-5.6-sol** | $5.00/MTok | $0.50/MTok | $30.00/MTok |
| gpt-5.6-terra | $2.50/MTok | $0.25/MTok | $15.00/MTok |
| gpt-5.6-luna | $1.00/MTok | $0.10/MTok | $6.00/MTok |

## Cross-vendor tokenization multipliers (Playcode 2026-07-13)
| Content | GPT o200k (ref) | Claude (new) | Claude (old) | Gemini 3 Flash | Grok 4.5 |
|---|---:|---:|---:|---:|---:|
| TypeScript | 1.00× | **1.73×** | 1.32× | 1.16× | 1.05× |
| Rust | 1.00× | 1.58× | 1.22× | 1.19× | 1.05× |
| JavaScript | 1.00× | 1.52× | 1.26× | 1.23× | 1.11× |
| Python | 1.00× | 1.50× | 1.22× | 1.20× | 1.09× |
| English prose | 1.00× | 1.40× | 1.05× | 1.01× | 1.00× |
| Chinese prose | 1.00× | 1.44× | 1.45× | 0.85× | 0.86× |

## Anthropic old-vs-new tokenizer table (Playcode via count_tokens endpoint)
| Content | Old tokenizer | New tokenizer | Change |
|---|---:|---:|---:|
| English prose (2,115 chars) | 476 | 636 | +34% |
| HTML (3,195 chars) | 1,131 | 1,302 | +15% |
| JavaScript (1,933 chars) | 659 | 794 | +20% |
| Python (2,251 chars) | 831 | 1,022 | +23% |
| TypeScript (2,888 chars) | 898 | 1,178 | +31% |
| Rust (2,924 chars) | 1,019 | 1,312 | +29% |
| JSON tool schema (9,948 chars) | 2,631 | 3,306 | +26% |
| Agent system prompt (42,661 chars) | 10,761 | 14,953 | +39% |
| Chinese prose (379 chars) | 435 | 433 | ~0% |

## Effective price table (Playcode × verified list prices, 2026-07-15)
| Model | List in/out ($/MTok) | Divergence | Effective in/out ($/MTok) |
|---|---|---:|---:|
| GPT-5.6 Sol | $5.00 / $30.00 | 1.00× (verified) | $5.00 / $30.00 |
| GPT-5.5 | $5.00 / $30.00 | 1.00× | $5.00 / $30.00 |
| GPT-5.1 | $1.25 / $10.00 | 1.00× | $1.25 / $10.00 |
| Grok 4.5 | $2.00 / $6.00 | 1.03× | $2.06 / $6.18 |
| Gemini 3 Flash | $0.50 / $3.00 | 1.09× | $0.55 / $3.27 |
| Claude Sonnet 4.6 | $3.00 / $15.00 | 1.14× (old tokenizer) | $3.42 / $17.10 |
| Claude Sonnet 5 (intro) | $2.00 / $10.00 | 1.50× (new tokenizer) | $3.00 / $15.00 |
| Claude Sonnet 5 (from Sep 1) | $3.00 / $15.00 | 1.50× | $4.50 / $22.50 |
| Claude Opus 4.6 | $5.00 / $25.00 | 1.14× (old tokenizer) | $5.70 / $28.50 |
| **Claude Opus 4.8** | $5.00 / $25.00 | 1.50× (new tokenizer) | **$7.50 / $37.50** |
| Claude Opus 4.7 | $5.00 / $25.00 | (likely 1.50×, same tokenizer as 4.8) | ~$7.50 / $37.50 |
| Claude Fable 5 | $10.00 / $50.00 | 1.50× | $15.00 / $75.00 |

## Cross-references
- Ploy.ai production migration: 2.60M (Opus 4.8) vs 1.70M (GPT-5.6 Sol) input tokens per build, ~35% reduction. Published 2026-06-26 in their engineering blog.
- Sonnet 5 intro window: valid through 2026-08-31, then $3/$15 standard rate from 2026-09-01.

## File references
- `src/pages/tutorials/claude-tokenizer-cost-increase-2026.astro` (EN, 40,778 bytes)
- `src/pages/zh/tutorials/claude-tokenizer-cost-increase-2026.astro` (ZH, 37,649 bytes)
- Markdown draft: `drafts/en-claude-tokenizer-cost-increase-2026-2026-07-15.md`
- Git commit: 25bec7a
- Wrangler deployment: be37d4c, preview https://24a0d59d.apirank-vip.pages.dev
- Built size: 47,989 bytes (EN), 44,376 bytes (ZH)
