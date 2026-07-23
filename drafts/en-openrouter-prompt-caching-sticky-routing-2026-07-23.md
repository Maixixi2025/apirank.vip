# OpenRouter Prompt Caching + Sticky Routing: Agent Cost Math for 2026

2026-07-23

Provider: openrouter
Category: news-analysis

<h1 class="text-3xl font-bold text-gray-900 mt-8 mb-4">OpenRouter Prompt Caching + Sticky Routing: Agent Cost Math for 2026</h1>

<p class="text-gray-700 leading-relaxed my-4">On <strong>July 21, 2026</strong>, OpenRouter published a tutorial titled <em>"The Cheapest Token Is a Cached One: Prompt Caching + Sticky Routing."</em> It is the clearest public breakdown of how their aggregation layer handles cache reads, cache writes, and session pinning across 70+ upstream providers. For anyone running multi-turn agents, the cost math in that post is the difference between a $5,000 month and a $500 month on the same workload.</p>

<p class="text-gray-700 leading-relaxed my-4">This article distills the OpenRouter post into the parts that matter for production builders:</p>

<ol class="list-decimal list-inside text-gray-700 my-4 space-y-1">

<li>The provider-by-provider cache pricing matrix (Anthropic, OpenAI pre/post GPT-5.6, Gemini, Grok, Moonshot, Groq, DeepSeek, Alibaba Qwen, Z.AI).</li>

<li>A concrete 6-turn × 10,000-token example showing what sticky routing actually saves.</li>

<li>The four causes of cache misses and how to stop each one.</li>

<li>The <code>session_id</code> parameter and why it changes stickiness from "sometimes warm" to "reliably warm."</li>

<li>The <code>cached_tokens</code>, <code>cache_discount</code>, and <code>cache_write_tokens</code> fields that confirm caching is working.</li>

</ol>

<p class="text-gray-700 leading-relaxed my-4">All pricing facts are verified from the OpenRouter blog post dated 2026-07-21 and OpenRouter's prompt caching docs as of late July 2026.</p>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">What Is Prompt Caching on OpenRouter?</h2>

<p class="text-gray-700 leading-relaxed my-4">OpenRouter is a unified API that fronts 300+ models across 70+ providers. The "prompt caching" feature means OpenRouter (or the upstream provider) reuses part of the prompt instead of re-tokenizing and re-billing the full input on every turn. The reusable part is usually the <strong>expensive</strong> part — system prompts, tool definitions, JSON schemas, guardrails, retrieved documents, examples — that stay the same across turns.</p>

<p class="text-gray-700 leading-relaxed my-4">Two separate cost components matter:</p>

<ul class="list-disc list-inside text-gray-700 my-4 space-y-1">

<li><strong>Cache write</strong> — the first request that stores the reusable prefix. On some providers this costs more than the regular input token price (Anthropic charges 1.25x for 5-min TTL, 2.0x for 1-hour TTL). On other providers it's free (Gemini, Grok, Moonshot, pre-GPT-5.6 OpenAI, Groq).</li>

<li><strong>Cache read</strong> — every later request that reuses the stored prefix. This is the cheap part: anywhere from <strong>0.1x to 0.5x</strong> of the normal input price, depending on the provider.</li>

</ul>

<p class="text-gray-700 leading-relaxed my-4">A cache read of 0.1x means a 10,000-token system prompt that would cost $30 of input on Claude Sonnet 4.6 costs <strong>$3</strong> when read from cache. Multiply that across 6 turns of a long-running agent and the savings stack fast.</p>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Provider-by-Provider Cache Pricing Matrix (verified 2026-07-21)</h2>

<p class="text-gray-700 leading-relaxed my-4">The following table is the OpenRouter-published breakdown, captured directly from the blog post:</p>

<div class="overflow-x-auto my-6"><table class="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg"><thead class="bg-gray-50"><tr><th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Provider</th><th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Cache read multiplier</th><th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Cache write multiplier</th><th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">How to enable</th></tr></thead><tbody class="divide-y divide-gray-200 bg-white"><tr><td class="px-4 py-3 text-sm text-gray-700">Anthropic Claude (5-min TTL)</td><td class="px-4 py-3 text-sm text-gray-700">0.1x input</td><td class="px-4 py-3 text-sm text-gray-700">1.25x input</td><td class="px-4 py-3 text-sm text-gray-700">Automatic or explicit</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Anthropic Claude (1-hour TTL)</td><td class="px-4 py-3 text-sm text-gray-700">0.1x input</td><td class="px-4 py-3 text-sm text-gray-700">2.0x input</td><td class="px-4 py-3 text-sm text-gray-700">Explicit (<code>ttl: "1h"</code>)</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">OpenAI (before GPT-5.6)</td><td class="px-4 py-3 text-sm text-gray-700">0.25x–0.50x input</td><td class="px-4 py-3 text-sm text-gray-700">Free</td><td class="px-4 py-3 text-sm text-gray-700">Automatic</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">OpenAI (GPT-5.6 and later)</td><td class="px-4 py-3 text-sm text-gray-700">0.25x–0.50x input</td><td class="px-4 py-3 text-sm text-gray-700">1.25x input</td><td class="px-4 py-3 text-sm text-gray-700">Automatic or explicit</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Google Gemini (implicit)</td><td class="px-4 py-3 text-sm text-gray-700">0.25x input</td><td class="px-4 py-3 text-sm text-gray-700">Free</td><td class="px-4 py-3 text-sm text-gray-700">Automatic</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Grok (xAI)</td><td class="px-4 py-3 text-sm text-gray-700">0.25x input</td><td class="px-4 py-3 text-sm text-gray-700">Free</td><td class="px-4 py-3 text-sm text-gray-700">Automatic</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Moonshot AI</td><td class="px-4 py-3 text-sm text-gray-700">0.25x input</td><td class="px-4 py-3 text-sm text-gray-700">Free</td><td class="px-4 py-3 text-sm text-gray-700">Automatic</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Groq</td><td class="px-4 py-3 text-sm text-gray-700">0.5x input</td><td class="px-4 py-3 text-sm text-gray-700">Free</td><td class="px-4 py-3 text-sm text-gray-700">Automatic (Kimi K2 models)</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">DeepSeek</td><td class="px-4 py-3 text-sm text-gray-700">0.1x input</td><td class="px-4 py-3 text-sm text-gray-700">1.0x input</td><td class="px-4 py-3 text-sm text-gray-700">Automatic</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Alibaba Qwen</td><td class="px-4 py-3 text-sm text-gray-700">0.1x input</td><td class="px-4 py-3 text-sm text-gray-700">1.25x input</td><td class="px-4 py-3 text-sm text-gray-700">Explicit (<code>cache_control</code>)</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Z.AI</td><td class="px-4 py-3 text-sm text-gray-700">~0.2x input</td><td class="px-4 py-3 text-sm text-gray-700">Free</td><td class="px-4 py-3 text-sm text-gray-700">Automatic</td></tr></tbody></table></div>

<p class="text-gray-700 leading-relaxed my-4">Three patterns stand out:</p>

<ul class="list-disc list-inside text-gray-700 my-4 space-y-1">

<li><strong>Anthropic, DeepSeek, and Alibaba Qwen offer the cheapest cache reads (0.1x)</strong>, but their writes cost more than normal input. If your agent doesn't reuse the prefix enough to amortize the write, caching can actually <em>cost</em> you.</li>

<li><strong>Google Gemini, Grok, and Moonshot give free writes with 0.25x reads.</strong> Best of both worlds for one-shot agents that benefit from cache hits but rarely need multi-hour TTL.</li>

<li><strong>OpenAI moved to paid writes on GPT-5.6.</strong> Pre-GPT-5.6 OpenAI had free writes; GPT-5.6+ charges 1.25x for cache writes. If you migrated to GPT-5.6 in June 2026, your cache economics silently shifted.</li>

</ul>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Concrete Savings: 6-Turn Agent × 10K Cached Tokens</h2>

<p class="text-gray-700 leading-relaxed my-4">The OpenRouter post runs the same hypothetical agent: 6 turns, the same 10,000 tokens of repeated content (system prompt + tool definitions + schemas + policy context) on every turn. Output tokens and changing messages are excluded.</p>

<div class="overflow-x-auto my-6"><table class="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg"><thead class="bg-gray-50"><tr><th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Scenario</th><th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Turn 1</th><th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Turns 2–6</th><th class="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Total cost vs. 1 uncached turn</th></tr></thead><tbody class="divide-y divide-gray-200 bg-white"><tr><td class="px-4 py-3 text-sm text-gray-700">No caching</td><td class="px-4 py-3 text-sm text-gray-700">Full input</td><td class="px-4 py-3 text-sm text-gray-700">Full input each turn</td><td class="px-4 py-3 text-sm font-semibold text-gray-900">6.0x</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Anthropic 5-min cache + sticky routing</td><td class="px-4 py-3 text-sm text-gray-700">1.25x write</td><td class="px-4 py-3 text-sm text-gray-700">0.1x reads</td><td class="px-4 py-3 text-sm font-semibold text-gray-900">1.75x</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Free-write provider + 0.25x reads</td><td class="px-4 py-3 text-sm text-gray-700">1.0x input/write</td><td class="px-4 py-3 text-sm text-gray-700">0.25x reads</td><td class="px-4 py-3 text-sm font-semibold text-gray-900">2.25x</td></tr><tr><td class="px-4 py-3 text-sm text-gray-700">Free-write provider + 0.5x reads</td><td class="px-4 py-3 text-sm text-gray-700">1.0x input/write</td><td class="px-4 py-3 text-sm text-gray-700">0.5x reads</td><td class="px-4 py-3 text-sm font-semibold text-gray-900">3.5x</td></tr></tbody></table></div>

<p class="text-gray-700 leading-relaxed my-4">Read the table as: "for the same repeated content, the total token cost across 6 turns is N times what one uncached turn would cost."</p>

<p class="text-gray-700 leading-relaxed my-4">Anthropic with sticky routing is the <strong>3.4x cheaper than uncached</strong> baseline. Free-write providers with 0.5x reads (Groq) are still 1.7x better than uncached, but a long way behind Anthropic's aggressive cache-read pricing.</p>

<p class="text-gray-700 leading-relaxed my-4">The savings grow with the number of turns. A 20-turn deep-research agent with a 30K-token prefix sees the gap widen by another factor.</p>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Why Doesn't a Warm Cache Always Help?</h2>

<p class="text-gray-700 leading-relaxed my-4">This is the gotcha most engineers hit first. A warm cache only helps if the <strong>next request lands on the same provider endpoint</strong> that holds the cached prefix. OpenRouter fronts 70+ providers; on each turn, the router picks one. Turn two can route to a different provider — and you pay full price even though "the cache should have been warm."</p>

<p class="text-gray-700 leading-relaxed my-4">OpenRouter's <strong>sticky routing</strong> is the fix. After a cached request succeeds on a provider, OpenRouter pins follow-up requests for the same model back to that provider endpoint when its cache-read pricing is cheaper than normal input. If the sticky provider becomes unavailable, OpenRouter falls back to the next available provider instead of failing the request.</p>

<p class="text-gray-700 leading-relaxed my-4">The pinning uses a key. By default, OpenRouter hashes the first system or developer message and the first non-system message. That works if those opening messages stay the same. It does not work if the system prompt changes between turns, or if you inject a per-request timestamp into the prefix.</p>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Force a Warm Cache From Turn One With <code>session_id</code></h2>

<p class="text-gray-700 leading-relaxed my-4">For agent loops, the default hashing key is fragile. OpenRouter recommends passing a stable <code>session_id</code> for the conversation, ticket, or workflow run:</p>

<ul class="list-disc list-inside text-gray-700 my-4 space-y-1">

<li><strong>Without <code>session_id</code></strong>, sticky routing only kicks in after a cache hit is observed. On turn one there's no cache yet, so the router has no signal to pin to. Turn two might land on a cold endpoint.</li>

<li><strong>With <code>session_id</code></strong>, OpenRouter uses the session ID directly as the sticky routing key. Stickiness activates after the first successful request — <em>before any cache hit has happened</em>. For multi-turn agents, that is the difference between a cache that is reliably warm from turn one and one that is only sometimes warm.</li>

</ul>

<p class="text-gray-700 leading-relaxed my-4">The implementation in your OpenRouter client is one line:</p>

<pre class="bg-gray-900 text-gray-100 p-4 rounded mb-4 overflow-x-auto text-sm"><code>import requests

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
    json={
        "model": "anthropic/claude-sonnet-4.6",
        "messages": [...],   # your agent's full message history
        "session_id": "support-ticket-9821",   # stable per-conversation key
        # Optional: explicitly set cache TTL on Anthropic 1-hour models
        # "provider": {"cache_control": {"ttl": "1h"}}
    }
)</code></pre>

<p class="text-gray-700 leading-relaxed my-4">For ticket-style workflows where the agent runs against a stable identifier (ticket ID, thread ID, user ID, conversation ID), <code>session_id</code> is the cheapest optimization available.</p>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">How Do I Confirm Prompt Caching Is Working?</h2>

<p class="text-gray-700 leading-relaxed my-4">Three fields in the OpenRouter response confirm caching is live:</p>

<ul class="list-disc list-inside text-gray-700 my-4 space-y-1">

<li><code>usage.prompt_tokens_details.cached_tokens</code> — number of input tokens served from cache. Any value above zero confirms a hit.</li>

<li><code>usage.prompt_tokens_details.cache_write_tokens</code> — number of input tokens stored on the write turn.</li>

<li><code>usage.cache_discount</code> — per-generation cost effect (negative on the write turn if writes are paid, positive on later cache-read turns).</li>

</ul>

<p class="text-gray-700 leading-relaxed my-4">You can also inspect the detail view on the <strong>Activity</strong> page in the OpenRouter dashboard, or hit <code>/api/v1/generation</code> for full per-turn telemetry.</p>

<p class="text-gray-700 leading-relaxed my-4">A practical health check in production:</p>

<pre class="bg-gray-900 text-gray-100 p-4 rounded mb-4 overflow-x-auto text-sm"><code>import requests

def cache_health_check(response_json):
    usage = response_json.get("usage", {})
    details = usage.get("prompt_tokens_details", {})
    cached = details.get("cached_tokens", 0)
    discount = usage.get("cache_discount", 0)
    return {
        "cached_tokens": cached,
        "cache_discount": discount,
        "cache_active": cached &gt; 0,
    }</code></pre>

<p class="text-gray-700 leading-relaxed my-4">If <code>cache_active</code> stays <code>False</code> across multiple turns, you have one of the four common cache-miss causes.</p>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Why Does Your Cache Miss (and How to Fix Each Cause)?</h2>

<p class="text-gray-700 leading-relaxed my-4">When caching looks broken, it almost always comes down to one of four things:</p>

<ol class="list-decimal list-inside text-gray-700 my-4 space-y-1">

<li><strong>Prompt is too short.</strong> Each provider has a minimum cacheable token count — Anthropic requires 1,024 tokens, OpenAI requires 1,024, Gemini requires 4,096. Short prompts won't trigger caching regardless of how stable they are.</li>

<li><strong>Cache expired.</strong> Anthropic's default TTL is 5 minutes; the 1-hour TTL requires explicit <code>ttl: "1h"</code>. If a turn is idle longer than the TTL, the prefix is gone.</li>

<li><strong>Opening content changed.</strong> Any change to the system prompt, tool definitions, or the first user message invalidates the cache prefix hash. Even adding a current timestamp into the system message breaks it.</li>

<li><strong>Request moved to a different provider.</strong> Without <code>session_id</code>, the router can hand turn two to a different provider than turn one. The cache is warm on provider A; your request lands on provider B and pays full price.</li>

</ol>

<p class="text-gray-700 leading-relaxed my-4">The fixes are mechanical:</p>

<ul class="list-disc list-inside text-gray-700 my-4 space-y-1">

<li>For (1): consolidate small prompts or accept that short requests don't benefit from caching.</li>

<li>For (2): pick a TTL that matches your agent's typical turn cadence. For 1-hour Anthropic caching, set <code>provider: { cache_control: { ttl: "1h" } }</code>.</li>

<li>For (3): move any per-request data (timestamps, request IDs, user-specific tokens) to the <strong>end</strong> of the prompt, not the start.</li>

<li>For (4): set <code>session_id</code>. Without it, sticky routing only kicks in after a cache hit, which is too late for turn one.</li>

</ul>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Does Caching Work With the Auto Router?</h2>

<p class="text-gray-700 leading-relaxed my-4">Yes. With <code>session_id</code> set, router models such as <strong>Auto Router</strong> and <strong>Pareto Router</strong> pin both the resolved model and the provider endpoint for the session. Without <code>session_id</code>, Auto Router is allowed to switch models between turns, which is fine for exploration but invalidates any cache the previous model would have held.</p>

<p class="text-gray-700 leading-relaxed my-4">If you are using Auto Router for cost optimization, the value of <code>session_id</code> is even higher. It tells the router "stay on the model you picked for this conversation." Without it, you may pay cache-write costs on every turn because the model flips and the prefix is new each time.</p>

<p class="text-gray-700 leading-relaxed my-4"><strong>One catch:</strong> if you set <code>provider.order</code> yourself, your explicit order wins over sticky routing. To get sticky routing on a multi-provider model, leave <code>provider.order</code> unset and let OpenRouter pick. Use the <code>provider</code> routing controls only when you have a specific provider order requirement that overrides the cache benefits.</p>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Putting It Together: The Agent-Loop Checklist</h2>

<p class="text-gray-700 leading-relaxed my-4">For any agent that sends the same expensive content every turn:</p>

<ol class="list-decimal list-inside text-gray-700 my-4 space-y-1">

<li>Put stable content first — system prompt, tool definitions, JSON schemas, policies, long-lived context.</li>

<li>Put changing content later — user messages, tool results, timestamps, run-specific metadata.</li>

<li>Set a stable <code>session_id</code> for the conversation, ticket, or workflow run.</li>

<li>Inspect <code>cached_tokens</code> and <code>cache_discount</code> in the response to confirm reads are happening.</li>

<li>For 1-hour Anthropic TTLs, set <code>provider: { cache_control: { ttl: "1h" } }</code>.</li>

<li>Don't set <code>provider.order</code> — let sticky routing pick the warm endpoint.</li>

</ol>

<p class="text-gray-700 leading-relaxed my-4">The cheap-token trick is mechanical, but the order matters. If you fix the cache reads but the opening prefix keeps changing, no amount of <code>session_id</code> magic will save you. Stable prefix + stable session ID + provider that offers low cache reads is the combination that turns 6.0x into 1.75x.</p>

<h2 class="text-2xl font-bold text-gray-900 mt-8 mb-4">Affiliate Recommendation: FreeModel for Multi-Provider Agent Routing</h2>

<p class="text-gray-700 leading-relaxed my-4">If you are running multi-turn agents across multiple model providers, <a href="https://freemodel.com/?via=apirank" rel="sponsored noopener" target="_blank" class="text-blue-600 hover:underline font-medium">FreeModel</a> offers a unified API surface that aggregates many of the same providers OpenRouter does, with its own routing and caching layer. For workloads where you don't need every provider OpenRouter supports but want similar cache-routing behavior, FreeModel is a leaner alternative worth benchmarking against your current setup.</p>

<p class="text-gray-700 leading-relaxed my-4">For OpenRouter itself, the public affiliate program is at <a href="https://openrouter.ai/affiliates" rel="sponsored noopener" target="_blank" class="text-blue-600 hover:underline font-medium">openrouter.ai/affiliates</a> — link your readers to that page if you cover OpenRouter in your own product or newsletter.</p>


## FAQ

### How much do cached tokens cost on OpenRouter?

Cache reads cost 0.1x to 0.5x of normal input pricing, depending on the provider. Anthropic, DeepSeek, and Alibaba Qwen can read at 0.1x. OpenAI reads at 0.25x-0.50x. Gemini, Grok, and Moonshot read at 0.25x. Groq reads at 0.5x. Cache writes cost between free (Gemini, Grok, Moonshot, pre-GPT-5.6 OpenAI, Groq) and 2.0x input (Anthropic 1-hour TTL). Verified from the OpenRouter blog post dated 2026-07-21.

### Why is prompt caching not working through OpenRouter?

The common causes are a prompt below the provider's token minimum (Anthropic requires 1,024, Gemini requires 4,096), an expired cache (5-min default TTL on Anthropic), an unstable prompt prefix (any change to the first system/developer message breaks the hash), or provider drift between turns. Set a stable session_id, put per-request data at the end of the prompt, and inspect cached_tokens to confirm hits.

### Does OpenRouter support prompt caching across all providers?

OpenRouter supports prompt caching across all providers and models that implement it. Most providers enable it automatically - Anthropic and Alibaba Qwen use cache_control for explicit caching. Check the OpenRouter prompt caching docs for the per-model breakdown; not every model on every provider implements the feature.

### How do I check whether caching saved money?

Inspect usage.prompt_tokens_details.cached_tokens for cache reads and cache_write_tokens for cache writes. A cached_tokens value above zero confirms a hit. You can also read cache_discount in the response to see the per-generation cost effect. On providers with paid writes, you may see a negative discount on the write turn because the cache write costs more than normal input. On later cache-read turns, the discount should turn positive.

### What is sticky routing on OpenRouter?

Sticky routing pins follow-up requests to the provider that holds the warm cache. After a cached request succeeds on a provider, OpenRouter routes later requests for the same model back to that endpoint when its cache-read pricing is cheaper than normal input. If the sticky provider becomes unavailable, OpenRouter falls back to the next available provider instead of failing the request.

### Does caching work with the OpenRouter Auto Router?

Yes. With a session_id set, Auto Router and Pareto Router pin both the resolved model and the provider endpoint for the session. Without session_id, Auto Router may switch models between turns, which invalidates the cache. The combination of session_id + Auto Router gives you cost-optimized model selection with reliable cache reuse.

### Should I use Anthropic or DeepSeek for the cheapest cache reads?

Both Anthropic and DeepSeek offer 0.1x cache reads, the cheapest tier on OpenRouter. Anthropic charges 1.25x for the 5-min TTL write (or 2.0x for 1-hour). DeepSeek charges 1.0x for the write. If your agent loop is dense (turns every few minutes), Anthropic's higher write cost is quickly amortized; for sparser sessions, DeepSeek's lower write cost may net out cheaper.

### What happens if I set provider.order myself?

Your explicit provider order wins over sticky routing. The request will always land on your first available provider, even if a cached prefix is sitting on a different endpoint. Use the provider routing controls only when you have a specific provider preference that overrides the cache benefits. For most agent workloads, leave provider.order unset.

### How long does an OpenRouter cache last?

It depends on the provider and the TTL you set. Anthropic's default is 5 minutes; setting ttl: 1h extends it to one hour. OpenAI pre-GPT-5.6 caches for up to 5-10 minutes. Gemini's implicit cache TTL is around 1 hour. Alibaba Qwen's cache_control TTL is configurable per request. For long-running agents, the 1-hour Anthropic TTL or 1-hour Gemini implicit cache will cover most conversation patterns without per-turn write costs.

### Can I disable prompt caching on OpenRouter?

Yes. Set provider: { cache_control: { ttl: no-cache } } on Anthropic or Alibaba Qwen to opt out. On other providers where caching is implicit and free, there is no per-request opt-out - caching happens automatically but only saves you money when reads occur. If you prefer not to cache at all, route to providers that don't implement it (and pay full input price each turn).

