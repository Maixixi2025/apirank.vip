---
title: "GPT-5.6 Sol vs Claude Opus 4.8: Production Migration"
description: "Ploy cut agent cost 27% and wall-clock 2.2x by switching from Claude Opus 4.8 to GPT-5.6 Sol. The 4 engineering fixes + CLIProxyAPI + Sonnet 5 angle."
slug: "gpt-5-6-sol-vs-claude-opus-4-8-production-migration"
provider: "openai"
published: true
date: "2026-07-13"
type: "news-analysis"
---

# GPT-5.6 Sol vs Claude Opus 4.8: What Real Production Migration Taught Ploy (and 4 Engineering Lessons)

On **June 26, 2026**, OpenAI launched the **GPT-5.6 family** with three capability tiers — **Sol, Terra, Luna** — at the same per-token price points as GPT-5.5. The first ten days of public availability produced two well-publicized production migrations away from **Claude Opus 4.8**:

- **Ploy.ai** — switched its default agent model from Opus 4.8 to GPT-5.6 Sol on day one, after Opus had held the default slot for four months through both the 4.7 and 4.8 generations.
- **CLIProxyAPI (Tibo Sottiaux)** — pointed Claude Code's backend at GPT-5.6 Sol via a self-hosted proxy, replacing an Anthropic-direct path without rewriting client code.

Both teams published their numbers. Both got it working in production. Both ran into surprises that the on-paper Sol vs Opus comparison can't tell you. This article is the engineering post-mortem of what each team actually had to change, the cost/cache math that flipped their decision, and where Sol still loses to Opus on workloads that don't make the press release.

If you are evaluating GPT-5.6 Sol as a replacement for Claude Opus 4.8 in a production agent today, this is the operational guide to doing it without breaking your eval harness, your prompt cache, or your tool call layer.

## TL;DR

- **Ploy's head-to-head result on their own agent eval suite (n=10 vs n=11):** GPT-5.6 Sol delivered builds **2.2× faster** (3m 42s vs 8m 00s), **27% cheaper** ($2.22 vs $3.06), at **higher visual score** (0.970 vs 0.936). Output token count was cut roughly in half.
- **The decision was not "Sol is better" — it was "Sol wins on this specific job."** Ploy's agent builds, edits, screenshots, and ships real marketing websites. Opus had held the slot because nothing in 4 months beat it on that workload.
- **The migration required 4 engineering fixes** before the cost numbers made sense. Ploy had to rewrite their eval harness, fix tool schemas for Sol's "fill every parameter" habit, rebuild prompt caching around GPT-5.6's key-partitioned cache nodes, and make Responses API reasoning replay self-contained.
- **Tibo / CLIProxyAPI used a different lever**: a 5-minute proxy install that lets existing Claude Code or Codex clients point at Sol without code changes, useful for solo dev workflows that don't have Ploy's SDK-level access.
- **Where Opus 4.8 still wins**: short-form generation where per-call reasoning quality matters more than throughput, design tasks where Opus plays a more conservative type scale, and any workload that depends on Anthropic's org-scoped shared cache (GPT-5.6 cannot share static prefix across workspaces by design).
- **If you only do one thing carefully during your own migration**, rebuild your prompt caching. Ploy's pre-fix Sol looked **50% more expensive than Opus** purely because of cache misconfiguration. After the fix, it landed **below** Opus on the same suite. Every dollar of the gap they had been staring at was cache config, not model pricing.

## Why this is not a normal "Model A vs Model B" comparison

The standard Opus vs Sol writeup is a benchmark shootout: Terminal-Bench scores, GPQA, MMLU, latency on synthetic prompts. That is not what happened here. Ploy did not run a benchmark; they ran their **production eval suite** — hundreds of cases of "build a homepage from scratch" through "is this clone request safe to execute" — and got a clear answer on their specific workload. The same model can win Ploy's suite and lose yours.

Two reasons their numbers are worth reading carefully:

1. **The harness was tuned to the incumbent, and Ploy didn't know it.** Their tool-call budgets were sized for Opus's sequential style; Sol fans out parallel calls and blew through them on cases it was solving correctly. Their eval executor didn't support batched file reads, which Opus rarely used and Sol uses constantly. Roughly a third of the raw failures in the first cross-model run traced back to **harness assumptions, not model behavior**, and they were not evenly distributed between models. Ploy's lesson: triage the traces before you trust the pass rate.
2. **The "winning model" was the cheaper one.** A common pattern in 2026 model launches is that the new flagship is more expensive and slightly better, and you adopt it for premium workloads. Ploy's case is the inverse: Sol is the same price as Opus ($5/$30) and went 27% cheaper because of token efficiency, then went lower still once the cache was configured. That makes the migration a **cost play**, not a capability play — exactly the kind of decision that gets skipped because the press coverage frames it as a quality comparison.

The rest of this article is the four-step engineering post-mortem. If you only read one section, read **Step 2 (prompt caching)** — it is the single largest source of cost surprise in any OpenAI-to-Anthropic or Anthropic-to-OpenAI migration.

## The Ploy numbers, before and after the fixes

From the published Ploy migration post (June 26, 2026), comparing Claude Opus 4.8 vs GPT-5.6 Sol on a redesign suite where the agent rebuilds a brand's homepage against a reference design:

| Metric (per completed build) | Claude Opus 4.8 (n=11) | GPT-5.6 (n=10) | Delta |
|---|---:|---:|---:|
| **Cost per build** | $3.06 | $2.22 | **−27%** |
| **Wall-clock time** | 8m 00s | 3m 42s | **−54% (2.2× faster)** |
| **Input tokens** | 2.60M | 1.70M | **−35%** |
| **Output tokens** | 33.0K | 17.1K | **−48%** |
| **Visual score (1.0 = match)** | 0.936 | 0.970 | **+3.4%** |

**Mean of completed builds**, not best case. The Sol run finished a build in under four minutes on average. Opus on the same suite took eight. The visual score is from a binary-check judge running 10 yes/no questions ("hero is a full-bleed photographic scene", "primary CTAs are rounded rectangles, not pills") plus content checks, tool-trajectory checks, and file assertions. The cost is the actual OpenAI bill for the run, not a calculated estimate.

A representative matched pair: Opus produced a 17,957-character `globals.css` with 174 CSS variables (full color ramps, mostly unused). GPT-5.6 wrote 2,508 characters and 45 variables for a comparable (and sometimes better) rendered page. Sol writes lean code, not just faster code.

The catch: **these numbers are post-fix.** Pre-fix, Sol was 50% more expensive on the same workload because of prompt cache misconfiguration. Read Step 2 before you trust any cross-vendor price comparison in a benchmarking post.

## Step 0: Fix your eval harness before you trust a single number

This is the part nobody wants to write a blog post about because it makes the previous weeks of model evaluations look silly. Ploy ran their suite across both models and found that roughly a third of the raw failures in the first cross-model run traced to harness assumptions, not model behavior — and the failures were not evenly distributed between models.

Two concrete examples from the post:

- **Tool-call budgets were sized for Opus's sequential style.** Sol fans out parallel calls. On cases Sol was solving correctly, it was exceeding the budget the harness had inherited from Opus. Ploy's harness was failing valid Sol runs for hitting a limit designed around a different model.
- **The eval executor didn't support batched file reads.** Opus rarely used them. Sol uses them constantly. The harness was treating each file read as a separate tool call and blowing past the per-step budget.

There was also an inherited default that silently changed pass/fail outcomes: a minScore threshold of 1.0 on the visual judge meant a hero Sol scored 0.98 on was marked "failed", and an Opus run that passed every individual check was also "failed" by the same threshold. One invisible threshold, two different model behaviors, neither was the model being wrong.

**The take-away**: before declaring a model "the winner," triage the traces. You are grading the new model on how well it imitates the old one if you don't. The number that matters is not the pass rate on a tuned-to-the-incumbent harness — it is the pass rate after the harness has been audited for assumptions that the incumbent absorbed and the challenger exposes.

## Step 1: Sol sends every tool parameter, every time

This was the one that was silently corrupting results before Ploy caught it. Ploy's agent's code tool has 25 top-level parameters, one required (`action`) and the rest optional. **Opus sends the two or three it is using and omits the rest. Sol sends all 25, every time**, inventing plausible values for the ones it doesn't need: `offset: 0`, `timeout: 120000`, `siteId: "00000000-0000-0000-0000-000000000000"`.

Ploy's measurement of three days of production traces:

| Model | Calls | Calls carrying all 25 properties | % carrying all 25 |
|---|---:|---:|---:|
| gpt-5.6 | 6,635 | 6,635 | **100%** |
| claude-opus-4.8 | 2,898 | 4 | 0.1% |
| claude-sonnet-5 | 1,933 | 0 | 0% |

**The problem isn't verbosity. It is that an invented value is indistinguishable from an intended one.** `offset: 0` looks like a real argument. Ploy's file-read implementation treated it as one, and **52% to 64% of Sol's file reads were coming back empty** because of it. The tool returned `success: true` both ways, so the model had no way to know it was reading blank files. It just did the work worse, with more calls.

Prompting doesn't fix this. Ploy tried:

- A tool-description directive to "omit unused parameters": still 25/25.
- Per-property "OPTIONAL, omit if unused" hints: still 25/25.
- OpenAI's `strict` mode: identical behavior, and adopting it would have forced them to strip `pattern`, `format`, and array-bound validation from every schema.

This is **baked into how the model emits function calls**. You don't instruct it away; you design around it.

**The fix that worked is a schema transform at the provider boundary.** For OpenAI-family models only, Ploy rewrites every optional property to be **required but nullable**, using `anyOf: [T, null]`, which gives the model an explicit way to say "not using this." Then, at the single seam every tool invocation passes through, they strip the nulls back out before validation, so no tool implementation changes at all.

```javascript
// Before: 25 keys, every one carrying an invented value
{ "action": "read", "file_paths": [...], "offset": 0, "timeout": 120000, ... }

// After: 25 keys, 4 real values, 21 explicit nulls (stripped before the tool runs)
{ "action": "read", "file_paths": [...], "offset": null, "timeout": null, ... }
```

**Results after the fix**: empty file reads went from 52% to 0%, and the agent needed roughly 30% fewer tool calls for the same work, because it was no longer re-reading files that came back blank.

If you maintain a tool layer with optional properties and you are evaluating Sol, this is the **first** thing to fix. It is not optional. The cost of missing it is invisible to the model (it gets `success: true` back) but shows up as worse work, more tool calls, and higher cost.

## Step 2: Rebuild prompt caching — this is where the real cost lives

This is the most instructive engineering difference in the entire migration, because on the surface both providers offer "prompt caching" and the words hide two entirely different designs. **If you migrate one thing carefully, make it this: before Ploy did, GPT-5.6 looked about 50% more expensive than Opus. It wasn't the model's pricing; it was their cache configuration.**

Ploy's agent opens with a static prefix of roughly 29K tokens (tool schemas plus the core system prompt) that is identical for every conversation. On Claude, they mark cache breakpoints with `cache_control` and that prefix **caches across the whole organization**: any conversation, any workspace, one shared entry, no throughput budget to think about. Cache hit rates run 92% to 96% and caching fades into the background.

**GPT-5.6 changed OpenAI's caching model out from under Ploy.** Earlier GPT models cached implicitly on partial prefix matches, which gave decent hit rates for free. **GPT-5.6 dropped partial-prefix matching**: implicit caching now only creates whole-prompt entries keyed on the latest message. A new conversation sharing Ploy's 29K static prefix cached **0%** of it. Every conversation re-billed the full prefix at the uncached rate, and on GPT-5.6 every uncached prompt also pays a **1.25× cache-write surcharge**, whether or not you use caching.

The intended mechanism is explicit: `prompt_cache_breakpoint` markers plus a mandatory `prompt_cache_key`. And the key is where the design really diverges, because **it is part of cache identity.** Identical prompt, different key: zero cache hits. Each key maps to a cache node that sustains roughly **15 requests per minute** before OpenAI fans traffic to other nodes with independent, cold caches.

That turns "enable caching" into an actual design decision: **what entity do you scope the key to?**

| Cache key strategy | First-call hit rate | Notes |
|---|---:|---|
| Per-conversation key | 0% | A new conversation never hits the shared prefix. **The mistake Ploy measured — expensive.** |
| One global key | (high when within budget) | Every request hashes to one cache node. Production traffic obliterates the 15 rpm budget; requests spill to cold nodes and you are back to misses. |
| **Per-workspace key** | **83.7% (Ploy's post-fix result)** | All conversations in a customer workspace share entries; per-key traffic stays low. **The sweet spot.** |

Ploy ships the workspace-scoped key and splits the system prompt into breakpointed layers, mirroring the structure they already used for Anthropic:

```
request ──► hash(prompt head + prompt_cache_key) ──► cache node (~15 req/min per key)
│
├── [ tools + static prefix ]······················ A  every session
├── [ tools + static prefix + workspace context ]·· B  same context
└── [ ····················· + turn 1 + … + latest ]  C  this session
```

- **Entry A** is what makes a session's first call cheap.
- **Entry B** self-heals: when workspace memory changes, the request misses B but still hits A, then writes a fresh B. One context-sized write instead of a full 29K re-bill.
- **Entry C** is OpenAI's implicit whole-prompt chain, which works fine within a session because Ploy's prompts are strictly append-only.

**One consequence has no workaround: cross-workspace sharing of the static prefix is structurally impossible on OpenAI.** Anthropic can share it because its cache is org-scoped without key partitioning. On GPT-5.6, every workspace pays one 29K cold write per idle window — about **$0.18**. A real cost, but bounded and predictable.

**Results after the change**: first-call cache hits went from roughly 0% to **83.7%**, total uncached input tokens dropped **28%**, and GPT-5.6's per-suite cost landed **below** Opus's. **Every dollar of the gap Ploy had been staring at was cache misconfiguration, not model pricing.** If you are cost-comparing models and one of them has a cold cache, you are comparing your config, not the models.

## Step 3: Make Responses API reasoning replay self-contained

Shorter, but it broke real conversations. **GPT-5.6's Responses API replays prior-turn reasoning as server-side item references by default**; Ploy's started intermittently failing mid-conversation with `Item 'rs_...' not found`.

The fix is **`store: false`**, which makes the SDK request encrypted reasoning content and replay self-contained blobs instead of pointers to server state.

```python
# Responses API: turn off server-side reasoning state for self-contained replay
response = client.responses.create(
    model="gpt-5.6-sol",
    input=conversation_history,
    reasoning={"effort": "high"},
    store=False,  # key fix: request encrypted reasoning blobs, not server-side pointers
)
```

A corollary that cost Ploy a debugging afternoon: with server-side reasoning state in the loop, **the effective prompt can change upstream of you even when the bytes you send are append-only.** If you need reproducible conversation state across requests — for evals, for tests, for audit — `store: false` is the only path on GPT-5.6.

## Step 4 (optional): CLIProxyAPI for solo dev / small team migrations

Tibo Sottiaux published a different approach for developers who don't have Ploy's SDK-level access. **CLIProxyAPI** is an open-source proxy server ([github.com/router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)) that provides OpenAI / Gemini / Claude / Codex / Grok compatible API interfaces for CLI clients. The Tibo migration use case: point Claude Code or Codex at GPT-5.6 Sol without rewriting client code.

Tibo's X thread (June 26, 2026): *"If you aren't yet bold enough to install the Codex app, you can stay in the presence of your orange crab and point it at GPT 5.6 Sol. Takes 5 minutes. Kudos to Theo for explaining one of the ways to get this done."*

The setup is three steps:

1. **Install CLIProxyAPI** (binary from the GitHub releases page, or `go install`).
2. **Connect** with your existing Claude Code or Codex OAuth credentials — the proxy reuses the auth you already have.
3. **Define** an OpenAI-compatible endpoint that points to GPT-5.6 Sol, then point your client at the proxy.

For a solo dev or a small team that wants to compare Sol against Opus on real workloads without committing to a full SDK rewrite, this is the lowest-friction path. The trade-off: you are running a proxy in the loop, which adds 5-15ms of latency and means you are depending on the CLIProxyAPI maintainers for security and uptime. For Ploy-scale traffic it would be a non-starter; for personal workflows it is the right tool.

The Tibo approach is the **opposite** of Ploy's in one specific way: Ploy treated GPT-5.6 Sol as a replacement for Opus 4.8 on the same agent. Tibo treated it as a drop-in endpoint reachable through existing Claude Code / Codex tooling. Both work, but they imply different bets: Ploy's bet is that Sol will hold the default slot for at least the next 6 months; Tibo's bet is that endpoint-level flexibility matters more than committing to one provider.

## What Opus 4.8 still does better than Sol

Sol is not a strict upgrade over Opus 4.8. Three workloads where Opus holds the line:

- **Short-form generation where per-call reasoning quality matters.** A single high-stakes summary, a legal review, a design critique — the kinds of calls where you'd rather wait 8 seconds for a careful answer than 3 seconds for a fast one. Opus plays this more conservatively. Ploy's own design lead (in the related Ploy post on Opus vs Sol for web design) notes that Opus "tends to hold a balanced type scale, even when the design is a little less standard" — and that instinct is right for some brand systems.
- **Design tasks with strong existing systems.** Sol reaches for very big text, especially on hero headings. Ploy's pre-migration harness made Sol "ignore existing design systems and instead produce sharp, restrained, and visibly generic output." The fix is design-side steering, but for teams without a Ploy-scale design + engineering org, that is a real cost.
- **Any workload that depends on Anthropic's org-scoped shared cache.** GPT-5.6 cannot share a static prefix across workspaces by design. If your multi-tenant architecture is built on top of Anthropic's cache scoping and you have thousands of customers hitting the same tool definitions, the $0.18/workspace cold-write cost adds up. Anthropic's cache is the right primitive for that architecture; OpenAI's is not.

The opposite is also true: if you have a single-tenant or low-workspace-count deployment, Sol's per-workspace cache hits 83.7% and beats Anthropic's 92-96% only on the metric of cost-per-hit (Sol's cached input is $0.50/M vs Claude's ~$0.30/M, but the cold-write surcharge on Sol changes the math). The right answer depends on the workload.

## The Claude Sonnet 5 wildcard (June 30, 2026)

Ploy's migration story ends June 26 with Sol as the new default. Two weeks later, **Anthropic re-deployed Claude Fable 5 and Mythos 5** (June 30, 2026) after a US government export-control directive was lifted, restoring Claude Sonnet 5 globally. Sonnet 5 launched with a **promo price of $2/$10 (input/output per million tokens)** through August 31, 2026 — a 33% discount on Sonnet 4.5's $3/$15.

If you are running the Ploy comparison today, the model set is not just "Opus 4.8 vs Sol." The competitive landscape is:

- **Claude Sonnet 5** at $2/$10 (promo) — best price/quality for the non-flagship tier, 200K context, ideal for code review, short generation, mid-weight agent loops.
- **Claude Opus 4.8** at $15/$75 — premium tier, worth it only for the workloads where Opus's instincts are categorically better.
- **GPT-5.6 Sol** at $5/$30 (and dropping to GPT-5.5-effective prices post-cache-fix) — flagship tier with the strongest cacheability after the rebuild.
- **GPT-5.6 Terra** at $2.50/$15 — the balanced default for production, matches GPT-5.5 capability at half the cost.
- **GPT-5.6 Luna** at $1/$6 — the budget tier for chat, classification, and one-shot generation.

For the specific Ploy workload (long-running, tool-heavy, design-output agent), Sol still wins. For a 1-hour research agent, Sonnet 5 at $2/$10 is probably the right call. **The migration lesson generalizes: do the math on your own eval suite, on your own cache, on your own cost ceiling, before you commit to a default model.** The default model that won a benchmark isn't the default model that wins your production workload.

## How to evaluate Sol vs Opus on your own agent

If you want to reproduce Ploy's result on your own workload, here is the order of operations:

1. **Audit your eval harness for incumbent-model assumptions.** Tool-call budgets, batched-call support, minScore thresholds, default judge weights. Roughly a third of Ploy's "failures" pre-fix were harness artifacts. Don't skip this.
2. **Fix the tool schema boundary** for Sol's "fill every parameter" habit. Required-but-nullable via `anyOf: [T, null]`, with nulls stripped before tool execution. Verify that empty-read rates drop to zero and that the tool-call count per task drops 20-30%.
3. **Design your cache key strategy before the first request.** Per-workspace for multi-tenant, per-tenant for enterprise, per-user for consumer. Each key maps to a ~15 rpm cache node, so high-traffic keys will spill to cold nodes — design for that, don't discover it.
4. **Add `store: false`** to Responses API calls unless you specifically need server-side reasoning state. This is the default that will bite you in production.
5. **Measure cost on a fixed eval suite for 24-48 hours** with the new cache strategy before you commit to a migration. The pre-fix Sol is 50% more expensive than Opus. The post-fix Sol is cheaper. The difference is configuration, not model.
6. **Re-evaluate after every OpenAI or Anthropic pricing update.** The model you migrate to today at $5/$30 may be $3/$18 in three months. Ploy's migration made sense at GPT-5.6 launch pricing; the math shifts every time either provider touches a price card.

Ploy's result is a real, measured, post-fix number on a specific workload. It is not a general "Sol is better than Opus" claim. If your workload matches Ploy's — long-running, tool-heavy, output-token-dominated, design or generation — Sol is likely the right call. If it doesn't, run the eval yourself. The Ploy post-mortem is the playbook for how to do that eval well, not a substitute for doing it.

## FAQ

### What is the cost difference between GPT-5.6 Sol and Claude Opus 4.8 in production?

On Ploy's redesign agent (n=10 vs n=11), GPT-5.6 Sol was 27% cheaper per completed build ($2.22 vs $3.06) and 2.2× faster in wall-clock time (3m 42s vs 8m 00s), with higher visual score. The cost advantage is post-cache-fix; pre-fix, Sol was 50% more expensive. Output token count was cut roughly in half — Sol writes lean code, not just faster code.

### Why did Ploy switch from Claude Opus 4.8 to GPT-5.6 Sol?

Opus 4.8 had held Ploy's default model slot for four months. Nothing in that window beat it. GPT-5.6 Sol was the first model that did, on the specific Ploy workload of building, editing, and screenshotting real marketing websites. The 27% cost reduction + 2.2× speedup + higher visual score was a large enough delta to justify a migration effort. The decision was a cost play, not a capability play — same $5/$30 per-token price, but Sol's token efficiency flipped the per-task total.

### Did the migration require code changes?

Yes. Four engineering fixes: (1) audit the eval harness for incumbent-model assumptions, (2) transform tool schemas at the provider boundary so Sol's "fill every parameter" habit doesn't get interpreted as real arguments, (3) rebuild prompt caching around GPT-5.6's key-partitioned cache nodes with per-workspace keys, and (4) set `store: false` on Responses API calls to make reasoning replay self-contained. The 4th is the smallest code change. The 3rd is the largest cost lever.

### Can I use GPT-5.6 Sol without rewriting my client code?

Yes, via CLIProxyAPI (github.com/router-for-me/CLIProxyAPI), an open-source proxy that provides OpenAI / Gemini / Claude / Codex / Grok compatible API interfaces. Tibo Sottiaux's X thread walks through a 5-minute setup: install the proxy, connect with your existing OAuth credentials, point your client at the OpenAI-compatible endpoint. Useful for solo dev or small team evaluations; less suitable for Ploy-scale production traffic.

### Where does Claude Opus 4.8 still beat GPT-5.6 Sol?

Three workloads: (1) short-form generation where per-call reasoning quality matters more than throughput, (2) design tasks with strong existing brand systems (Sol "reaches for very big text" by default per Ploy's design lead), and (3) any multi-tenant architecture that depends on Anthropic's org-scoped shared cache — GPT-5.6 cannot share a static prefix across workspaces by design, so each tenant pays a ~$0.18 cold-write cost on idle.

### How does Claude Sonnet 5 (re-deployed June 30) fit into the comparison?

Sonnet 5 launched with a promo price of $2/$10 through August 31, 2026 — a 33% discount on Sonnet 4.5. For mid-weight agent loops and short high-quality generation, Sonnet 5 at $2/$10 is often the better default than Sol at $5/$30, especially if your workload doesn't need Sol's reasoning depth. The full competitive set today is Sonnet 5 ($2/$10) + Opus 4.8 ($15/$75) + Sol ($5/$30) + Terra ($2.50/$15) + Luna ($1/$6). The right default depends on the workload.

### What is the catch with GPT-5.6's prompt caching?

Two. First, GPT-5.6 dropped partial-prefix matching, so the old "implicit cache on common prefix" trick no longer works — you need explicit `prompt_cache_breakpoint` markers and a `prompt_cache_key`. Second, the key is part of cache identity, and each key maps to a node that handles ~15 rpm before traffic fans to cold nodes. A wrong key strategy (per-conversation, one global) gives you near-zero first-call hit rates. Per-workspace keys are the sweet spot for multi-tenant apps.

### Is GPT-5.6 Sol available now?

Yes, as of June 26, 2026, all three tiers (Sol, Terra, Luna) are generally available through the OpenAI API. The launch page is at `openai.com/index/gpt-5-6`. Sonnet 5 (the comparable Anthropic tier) is also live again as of June 30, 2026, after the US export-control directive was lifted.

### How do I get an API key for GPT-5.6 Sol?

Existing OpenAI API keys work — Sol is on the same `api.openai.com` endpoint, you just specify `model: "gpt-5.6-sol"` in the request. The Responses API (`/v1/responses`) is the recommended surface for agent workloads, and it is where the cache key + breakpoint design applies. Chat Completions (`/v1/chat/completions`) also works for simpler use cases.

### Should I migrate from Opus 4.8 to GPT-5.6 Sol today?

Only if your workload matches Ploy's: long-running, tool-heavy, output-token-dominated, design or generation. Run the 6-step evaluation above before committing. The cost lever (cache strategy) is the largest source of pre-fix waste — if you migrate without rebuilding your cache config, you will conclude Sol is 50% more expensive than Opus and the migration is a mistake. With the cache rebuilt, the conclusion is usually the opposite. The lesson: never trust a cross-vendor cost comparison that was measured on a cold cache.
