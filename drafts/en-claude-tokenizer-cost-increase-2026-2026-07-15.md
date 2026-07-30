---
title: "Claude Tokenizer 2026: Real Bill Math"
description: "Anthropic's new tokenizer makes the same file 1.36–1.73× more tokens. Same $5/$25 list price as Opus 4.6. Effective Opus 4.8 = $7.50/$37.50. Side-by-side with GPT-5.6 Sol."
slug: "claude-tokenizer-cost-increase-2026"
date: "2026-07-15"
provider: "anthropic"
type: "news-analysis"
---

# Claude Tokenizer 2026: Real Bill Math

On July 13, 2026, Playcode published a measurement of all major production LLM tokenizers that quietly reframes how the "$5 per million input tokens" line item on Anthropic's pricing page should be read. **The number is no longer comparable across vendors**, and one Anthropic model change in particular — the new tokenizer shipped with **Sonnet 5, Opus 4.8 (and likely Opus 4.7)**, plus the unreleased **Fable 5** — raises the real input bill by **about 32%** on a typical English coding request while the published list price is identical.

This article walks through the underlying measurements, the cross-vendor table, the multiplier-corrected "effective price" view, and what it changes about migration decisions in the second half of 2026.

## Why "$/Mtok" is no longer a comparable price

The formula behind every LLM invoice is:

**cost = (tokens your content becomes) × (price per token)**

The pricing page shows the second number and treats the first as a constant. It is not. Each vendor's tokenizer cuts the same bytes into a different number of pieces, and you pay per piece. Two models with identical "input $5/MTok" can produce meaningfully different bills for the same paragraph, because one turns that paragraph into more tokens.

Playcode ran **16 real fixtures** (English prose, HTML, JavaScript, Python, TypeScript, Rust, JSON tool schemas and tool results, Chinese chat, Chinese prose, symbol-heavy text, and a 42,661-character agent system prompt) through every frontier tokenizer using each vendor's own counting endpoint, then **double-checked the counts against real paid requests** with `max_tokens: 1`. The OpenAI counts were confirmed against live `usage.input_tokens` for GPT-5.1, GPT-5.5, and GPT-5.6 Sol. Anthropic counts came from the official `count_tokens` endpoint. Gemini and Grok counts came from their providers' own count endpoints.

**DeepSeek and GLM were left out** because no production tokenizer counts are publicly available — only rough characters-divided-by-four estimates. Anyone claiming comparable numbers for those two is working from a different (and weaker) methodology.

## What Anthropic actually changed

Opus 4.6 and Opus 4.8 list the same `$5.00 / $25.00` per million input/output tokens. **The list price is unchanged.** The tokenizer is different. Sonnet 4.6 and Opus 4.6 use the old tokenizer; **Sonnet 5, Opus 4.8, Fable 5**, and almost certainly Opus 4.7 use the new one.

Counting identical bytes through Anthropic's own `count_tokens` endpoint shows the impact:

| Content | Old tokenizer | New tokenizer | Change |
|---|---:|---:|---:|
| English prose (2,115 chars) | 476 | 636 | +34% |
| HTML page (3,195 chars) | 1,131 | 1,302 | +15% |
| JavaScript (1,933 chars) | 659 | 794 | +20% |
| Python (2,251 chars) | 831 | 1,022 | +23% |
| TypeScript (2,888 chars) | 898 | 1,178 | +31% |
| Rust (2,924 chars) | 1,019 | 1,312 | +29% |
| JSON tool schema (9,948 chars) | 2,631 | 3,306 | +26% |
| Our agent system prompt (42,661 chars) | 10,761 | 14,953 | **+39%** |
| Chinese prose (379 chars) | 435 | 433 | ~0% |

Weighted the way a real agent request is composed — mostly English system prompt, tool schemas, code, and JSON — the **new tokenizer comes out around +32% per request**. Chinese barely moved, so the inflation is concentrated on English and code.

The whole verification across both tokenizers cost about $0.08 in real API calls.

## The cross-vendor tokenization gap

The most cited result from the Playcode measurements is the cross-vendor table, with **GPT-5.x's `o200k` as the 1.00x reference** (it has been frozen and publicly documented for over two years, while Claude's tokenizer is the one that changed):

| Content | Claude (new) | Claude (old) | Gemini 3 Flash | Grok 4.5 |
|---|---:|---:|---:|---:|
| TypeScript | **1.73×** | 1.32× | 1.16× | 1.05× |
| Rust | 1.58× | 1.22× | 1.19× | 1.05× |
| JavaScript | 1.52× | 1.26× | 1.23× | 1.11× |
| Python | 1.50× | 1.22× | 1.20× | 1.09× |
| HTML page | 1.36× | 1.18× | 1.08× | 1.04× |
| English prose | 1.40× | 1.05× | 1.01× | 1.00× |
| Chinese prose | 1.44× | 1.45× | 0.85× | 0.86× |
| Chinese chat | 1.53× | 1.55× | 0.91× | 0.92× |

**Code sits well above prose.** TypeScript is the worst case at 1.73×, followed by Rust (1.58×), JavaScript (1.52×), Python (1.50×). English prose is "only" 1.40×, but a coding agent processes code more often than prose, so for that workload the 1.50–1.73× band is what matters.

Why is TypeScript the worst case? Because **`o200k` is unusually efficient on it** — about 4.24 characters per token, which looks like the result of training on a lot of web JavaScript and TypeScript where camelCase identifiers and JSX patterns compress into single tokens. On Rust its efficiency drops to about 3.51 characters per token. Claude's tokenizer is roughly equally dense on both languages, so the gap is widest exactly where GPT is strongest.

Chinese behavior is a long-standing property of the Claude family (the old tokenizer already ran 1.45× above GPT on Chinese prose), not something the new tokenizer introduced. Gemini is actually **more efficient than GPT** on Chinese (0.85×), which matters if your workload is CJK-heavy.

## Effective price per million tokens (the real comparison)

Multiplying list price by the measured divergence gives an effective price for the same work. The "divergence" column is the blended multiplier for a typical English coding request, normalized to GPT's `o200k`:

| Model | List in/out ($/MTok) | Divergence | Effective in/out ($/MTok) |
|---|---|---:|---:|
| **GPT-5.6 Sol** | $5.00 / $30.00 | 1.00× (verified) | $5.00 / $30.00 |
| GPT-5.5 | $5.00 / $30.00 | 1.00× | $5.00 / $30.00 |
| GPT-5.1 | $1.25 / $10.00 | 1.00× | $1.25 / $10.00 |
| Grok 4.5 | $2.00 / $6.00 | 1.03× | $2.06 / $6.18 |
| Gemini 3 Flash | $0.50 / $3.00 | 1.09× | $0.55 / $3.27 |
| Claude Sonnet 4.6 | $3.00 / $15.00 | 1.14× (old tokenizer) | $3.42 / $17.10 |
| Claude Sonnet 5 (intro, through Aug 31, 2026) | $2.00 / $10.00 | 1.50× (new tokenizer) | $3.00 / $15.00 |
| Claude Sonnet 5 (standard, from Sep 1, 2026) | $3.00 / $15.00 | 1.50× | $4.50 / $22.50 |
| Claude Opus 4.6 | $5.00 / $25.00 | 1.14× (old tokenizer) | $5.70 / $28.50 |
| **Claude Opus 4.8** | $5.00 / $25.00 | 1.50× (new tokenizer) | **$7.50 / $37.50** |
| Claude Opus 4.7 | $5.00 / $25.00 | (likely 1.50×, same tokenizer as 4.8) | ~$7.50 / $37.50 |
| Claude Fable 5 | $10.00 / $50.00 | 1.50× | $15.00 / $75.00 |

A few rows deserve a second look:

- **Opus 4.6 and Opus 4.8 share a list price** but differ by about **32%** in effective price. Going from 4.6 to 4.8 looks free on a rate card; it is a one-third price hike hidden in the tokenizer.
- **GPT-5.5 and GPT-5.6 Sol share the tokenizer** (verified against live API calls on all three). Their identical list prices really are identical in effect, and either one is a fair swap.
- **Gemini 3 Flash runs a slightly heavier tokenizer than GPT** but still remains the cheapest option by a wide margin — effective $0.55/$3.27 versus Opus 4.8's $7.50/$37.50 on input, a **13.6×** effective gap.
- **Sonnet 5's $2/$10 intro window** (through August 31, 2026) roughly cancels the new tokenizer's overhead, making it actually competitive against Sonnet 4.6 for the same code. From September 1, 2026 the price reverts to $3/$15 with the same extra tokens — the same work will cost **about a third more** than it did on Sonnet 4.6 at the same list price.

## Cache traffic amplifies the gap

Everything above measures one thing: how many input tokens identical bytes become. A full agent task adds more variables on top, and they are big ones.

**Cache traffic is billed per token.** Prompt caching writes at the writer rate and reads at the reader rate, both on a per-token basis. A tokenizer that produces **32% more tokens** makes every cache write and every cache read **about 32% more expensive**, and on long agent sessions cache reads are most of the bill. Anthropic's published caching prices — write $6.25/MTok, read $0.50/MTok for Opus 4.8 — apply before the tokenizer step. The effective cache read price for Opus 4.8 on a typical coding agent is closer to $0.75/MTok, not the headline $0.50.

For reference, here are the live prompt-cache prices on the Anthropic pricing page as of July 15, 2026:

| Model | Cache write | Cache read |
|---|---|---|
| Sonnet 4.6 | $3.75/MTok | $0.30/MTok |
| Sonnet 5 (intro) | $2.50/MTok | $0.20/MTok |
| Sonnet 5 (standard from Sep 1) | $3.75/MTok | $0.30/MTok |
| Opus 4.6 | $6.25/MTok | $0.50/MTok |
| **Opus 4.8** | $6.25/MTok | $0.50/MTok |
| Opus 4.7 | $6.25/MTok | $0.50/MTok |
| Haiku 4.5 | $1.25/MTok | $0.10/MTok |

Same trend: Opus 4.6 and 4.8 share the cache pricing too. The new tokenizer raises the cache line item in proportion to token count.

## Whole-task costs can diverge much further

The Playcode measurements capped at 1.73× because the methodology focused on input tokenization only. Real workloads add three more variables on top:

- **Output verbosity** — how many tokens the model spends to reach the same result.
- **Thinking** — some models now emit visible or invisible thinking tokens that add to the output bill without changing the user's response.
- **Subagent and tool-call depth** — how many round-trips the harness makes, and how much context each brings along.

When people report that one model "uses 2–4× the tokens" of another on agent work, that can be true for their setup even though the pure input tokenization gap never exceeded 1.73×. The two numbers measure different layers.

**Independent data point from Ploy.ai's production migration (published June 26, 2026)**: when Ploy switched from Opus 4.8 to GPT-5.6 Sol as the default agent model, they measured **1.70M input tokens against Claude Opus 4.8's 2.60M** for the same builds — **about 35% fewer** before any other change. That is a whole-task measurement rather than a tokenizer probe, so it folds in verbosity and cache structure, but it points the same direction: GPT-5.6 Sol is meaningfully cheaper per build than Opus 4.8 on the same workload.

## How to compare model prices in practice

Three rules emerged from the measurements:

1. **Compare on your own content.** Your language and file types set the multiplier, so run a representative sample — at least one English prose file, one HTML file, one Python file, one TypeScript file, one JSON tool schema — through each tokenizer before trusting a rate card. Anthropic's `count_tokens` endpoint is free and returns the same number they bill against. OpenAI ships `o200k_base` via the `tiktoken` package, which matched live billed counts exactly on GPT-5.1, 5.5, and 5.6 Sol.
2. **Treat a tokenizer change as a price change.** When a vendor ships a new model at the same list price, check whether the tokenizer moved. **Opus 4.6 → Opus 4.8 is a ~32% increase with no line item on any invoice.** Announcements rarely call this out; the discount works only if you compare at the token level.
3. **Measure dollars per completed task, not dollars per token.** That single number folds in tokenization, verbosity, thinking, and caching at once, and the provider's `usage` field gives you the ground truth to compute it.

A useful heuristic while the vendors continue to use $/MTok: **multiply every Claude list price on Sonnet 5 / Opus 4.8 / Opus 4.7 / Fable 5 by 1.32 to roughly reflect the new tokenizer's overhead** on a typical coding-agent workload. It will not be exact for every fixture, but it is a more honest starting point than the raw list price.

## What this changes about migration decisions

If you are evaluating Opus 4.8 against GPT-5.6 Sol today:

- **Opus 4.8's effective input price is $7.50/MTok, GPT-5.6 Sol's is $5.00/MTok.** The effective spread is 1.5× on input, 1.25× on output. On a mixed input/output coding workload the headline "Opus is the same price as GPT-5.6" stops being true the moment the new tokenizer is factored in.
- **Sonnet 5 stays attractive only inside the intro window.** Through August 31, 2026, $2/$10 effective $3/$15 lands the new tokenizer in line with Sonnet 4.6 for typical code. After that, the same work costs about a third more than Sonnet 4.6 at the same list price — not catastrophic, but worth planning a backfill review for.
- **Gemini 3 Flash keeps its cost crown.** A slightly heavier tokenizer than GPT-5.x still leaves Gemini's effective input at $0.55/MTok, the cheapest available in 2026. For batch pipelines that can accept its quality, it dominates every other option on a per-token basis.
- **Ploy's whole-task cost** (1.70M vs 2.60M input tokens, −35%) is the most practical data point for a coding-agent team deciding between Opus 4.8 and GPT-5.6 Sol today.

None of this makes one model universally right. GPT-5.x is the token-lean choice on English and code; Gemini 3 Flash is remarkably cheap in effect; and Claude models earn their place on quality even when they cost more tokens to run. Just make sure the price you compare is the one you actually pay, after the tokenizer.

## Verification methodology (for the skeptical)

The Playcode measurements are reproducible:

- **Anthropic**: `count_tokens` endpoint on the Messages API is free and returns the same count Anthropic bills against. Verified against real billed `usage.input_tokens` on Opus 4.6 (2,541 input tokens predicted vs billed) and Opus 4.8 (3,191 predicted vs billed; Fable 5 also 3,191 — same tokenizer, no hidden markup).
- **OpenAI**: `o200k_base` via the documented `tiktoken` Python package, double-checked against live `usage.input_tokens` on GPT-5.1, GPT-5.5, and GPT-5.6 Sol. All three matched the local count exactly using a long-minus-short delta that cancels request framing.
- **Gemini and Grok**: providers' own count endpoints.
- **DeepSeek and GLM**: excluded — only rough characters-divided-by-four estimates are available, not real tokenizer counts.
- **Fixtures**: 16 byte-for-byte matched samples (English prose, HTML, JavaScript, Python, TypeScript, Rust, two JSON tool types, Chinese chat, Chinese prose, agent system prompt, etc.).
- **Verification cost**: about $0.08 in real API calls.

Anthropic, OpenAI, Google Gemini, and xAI pricing pages were live-confirmed against the published rate card as of July 15, 2026.

## Frequently asked questions

**Is the Claude tokenizer change a price increase?**
Effectively yes — about 32% on a typical English coding workload. The list price is unchanged, but since you pay per token, the new tokenizer multiplies your input bill by ~1.32× on Sonnet 5 / Opus 4.8 / Fable 5. There is no line item on the invoice that explains this; the discount works only at the token level.

**Which Claude models use the new tokenizer?**
Sonnet 5, Opus 4.8, and Fable 5 are confirmed. Opus 4.7, listed at the same $5/$25 as Opus 4.8, almost certainly uses the same new tokenizer (no separate measurement exists yet, but the identical list price + identical cache pricing makes this the safe assumption).

**Should I switch from Claude Opus 4.8 to GPT-5.6 Sol?**
On a pure cost basis the answer is yes for a typical English coding workload: Opus 4.8's effective input is $7.50/MTok versus GPT-5.6 Sol's $5.00/MTok, and Ploy's production migration published a 35% reduction in real-world token counts. If your workload depends on Claude's specific quality on long-form reasoning or its tool-use conventions, the cost savings may not be worth the switch; if cost is the primary decision driver, the data say GPT-5.6 Sol wins.

**Will Sonnet 5's intro pricing ($2/$10) last?**
No. Anthropic's pricing page states the intro price is valid through August 31, 2026; the standard rate is $3/$15 from September 1, 2026. After the intro ends the same code will cost about a third more than it did on Sonnet 4.6, because the 32% tokenizer overhead remains and the rate-card discount disappears.

**How can I measure my own real cost?**
Two practical recipes. (1) Run a representative mix of your real prompts through `count_tokens` on Anthropic and `tiktoken` on OpenAI to compute your own weighted multiplier. (2) Send a fixed set of representative prompts to each candidate model, read the `usage.input_tokens` field from each response, and divide the actual invoice line by your token count to get an effective $/MTok that already folds in verbosity, thinking, and caching. The latter is the only number that fully reflects what you pay.

**Is Gemini 3 Flash really cheaper than every Claude and GPT option?**
Yes, on the effective price table. Gemini 3 Flash's effective input lands at $0.55/MTok and effective output at $3.27/MTok, making it the cheapest option in 2026 by a wide margin. The catch is output quality: Gemini 3 Flash is optimized for speed and cost over reasoning quality, so use it for high-throughput batch pipelines where model quality is not the bottleneck.

## Sources

- Playcode — *The Same TypeScript Costs 73% More on Claude Than on GPT* (Ruslan Ianberdin, July 13, 2026; updated July 14, 2026). [playcode.io/blog/real-price-of-frontier-models](https://playcode.io/blog/real-price-of-frontier-models)
- Anthropic — *API Pricing* (live rate card, confirmed July 15, 2026). [anthropic.com/pricing](https://www.anthropic.com/pricing)
- OpenAI — *API Pricing* (live rate card, confirmed July 15, 2026). [platform.openai.com/docs/pricing](https://platform.openai.com/docs/pricing)
- Google Gemini — *Gemini API Pricing* (effective prices confirmed against the published rate card, July 15, 2026). [ai.google.dev](https://ai.google.dev)
- xAI — *API Pricing* (effective prices confirmed against the published rate card, July 15, 2026). [docs.x.ai](https://docs.x.ai)
- Ploy.ai — *Migration Notes: Claude Opus 4.8 to GPT-5.6 Sol* (June 26, 2026).
