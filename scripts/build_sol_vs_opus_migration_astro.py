#!/usr/bin/env python3
"""Build .astro files for the GPT-5.6 Sol vs Claude Opus 4.8 production migration article.
Generates:
  /root/apirank/src/pages/tutorials/gpt-5-6-sol-vs-claude-opus-4-8-production-migration.astro (EN)
  /root/apirank/src/pages/zh/tutorials/gpt-5-6-sol-vs-claude-opus-4-8-production-migration.astro (ZH)
"""
import re
import json
import sys
import os

sys.path.insert(0, '/root/apirank/scripts')
from md_to_astro_body import md_to_astro_body

# --- CONFIG ---
SLUG = "gpt-5-6-sol-vs-claude-opus-4-8-production-migration"
DATE = "2026-07-13"

# --- EN title + description ---
# Title target: 30-60 chars (BaseLayout appends " | APIRank" = +10)
# 50 chars + 10 suffix = 60 chars exactly
EN_TITLE = "GPT-5.6 Sol vs Opus 4.8: Production Migration"
# Decoded 49 chars; +10 suffix = 59
EN_TITLE = "GPT-5.6 Sol vs Claude Opus 4.8: Migration"
# 46 chars + 10 = 56 - good
EN_DESCRIPTION = "Ploy cut agent cost 27% and wall-clock 2.2x switching from Claude Opus 4.8 to GPT-5.6 Sol. 4 engineering fixes + CLIProxyAPI."

# --- ZH title + description ---
# 50 chars + 10 suffix = 60 chars exactly
ZH_TITLE = "GPT-5.6 Sol 对比 Opus 4.8：生产迁移实操"
# 28 ZH chars - need to check
ZH_DESCRIPTION = "Ploy 把默认 agent 从 Opus 4.8 切到 GPT-5.6 Sol 后成本降 27%、构建时间快 2.2 倍。拆解 4 个工程修复 + CLIProxyAPI。"

# --- FAQ data (EN) ---
EN_FAQ = [
    ("What is the cost difference between GPT-5.6 Sol and Claude Opus 4.8 in production?",
     "On Ploy's redesign agent (n=10 vs n=11), GPT-5.6 Sol was 27% cheaper per completed build ($2.22 vs $3.06) and 2.2x faster in wall-clock time (3m 42s vs 8m 00s), with higher visual score. The cost advantage is post-cache-fix; pre-fix, Sol was 50% more expensive. Output token count was cut roughly in half — Sol writes lean code, not just faster code."),
    ("Why did Ploy switch from Claude Opus 4.8 to GPT-5.6 Sol?",
     "Opus 4.8 had held Ploy's default model slot for four months. Nothing in that window beat it. GPT-5.6 Sol was the first model that did, on the specific Ploy workload of building, editing, and screenshotting real marketing websites. The 27% cost reduction + 2.2x speedup + higher visual score was a large enough delta to justify a migration effort. The decision was a cost play, not a capability play — same $5/$30 per-token price, but Sol's token efficiency flipped the per-task total."),
    ("Did the migration require code changes?",
     "Yes. Four engineering fixes: (1) audit the eval harness for incumbent-model assumptions, (2) transform tool schemas at the provider boundary so Sol's 'fill every parameter' habit doesn't get interpreted as real arguments, (3) rebuild prompt caching around GPT-5.6's key-partitioned cache nodes with per-workspace keys, and (4) set `store: false` on Responses API calls to make reasoning replay self-contained. The 4th is the smallest code change. The 3rd is the largest cost lever."),
    ("Can I use GPT-5.6 Sol without rewriting my client code?",
     "Yes, via CLIProxyAPI (github.com/router-for-me/CLIProxyAPI), an open-source proxy that provides OpenAI / Gemini / Claude / Codex / Grok compatible API interfaces. Tibo Sottiaux's X thread walks through a 5-minute setup: install the proxy, connect with your existing OAuth credentials, point your client at the OpenAI-compatible endpoint. Useful for solo dev or small team evaluations; less suitable for Ploy-scale production traffic."),
    ("Where does Claude Opus 4.8 still beat GPT-5.6 Sol?",
     "Three workloads: (1) short-form generation where per-call reasoning quality matters more than throughput, (2) design tasks with strong existing brand systems (Sol 'reaches for very big text' by default per Ploy's design lead), and (3) any multi-tenant architecture that depends on Anthropic's org-scoped shared cache — GPT-5.6 cannot share a static prefix across workspaces by design, so each tenant pays a ~$0.18 cold-write cost on idle."),
    ("How does Claude Sonnet 5 (re-deployed June 30) fit into the comparison?",
     "Sonnet 5 launched with a promo price of $2/$10 through August 31, 2026 — a 33% discount on Sonnet 4.5. For mid-weight agent loops and short high-quality generation, Sonnet 5 at $2/$10 is often the better default than Sol at $5/$30, especially if your workload doesn't need Sol's reasoning depth. The full competitive set today is Sonnet 5 ($2/$10) + Opus 4.8 ($15/$75) + Sol ($5/$30) + Terra ($2.50/$15) + Luna ($1/$6). The right default depends on the workload."),
    ("What is the catch with GPT-5.6's prompt caching?",
     "Two. First, GPT-5.6 dropped partial-prefix matching, so the old 'implicit cache on common prefix' trick no longer works — you need explicit `prompt_cache_breakpoint` markers and a `prompt_cache_key`. Second, the key is part of cache identity, and each key maps to a node that handles ~15 rpm before traffic fans to cold nodes. A wrong key strategy (per-conversation, one global) gives you near-zero first-call hit rates. Per-workspace keys are the sweet spot for multi-tenant apps."),
    ("Is GPT-5.6 Sol available now?",
     "Yes, as of June 26, 2026, all three tiers (Sol, Terra, Luna) are generally available through the OpenAI API. The launch page is at openai.com/index/gpt-5-6. Sonnet 5 (the comparable Anthropic tier) is also live again as of June 30, 2026, after the US export-control directive was lifted."),
    ("How do I get an API key for GPT-5.6 Sol?",
     "Existing OpenAI API keys work — Sol is on the same api.openai.com endpoint, you just specify model: 'gpt-5.6-sol' in the request. The Responses API (/v1/responses) is the recommended surface for agent workloads, and it is where the cache key + breakpoint design applies. Chat Completions (/v1/chat/completions) also works for simpler use cases."),
    ("Should I migrate from Opus 4.8 to GPT-5.6 Sol today?",
     "Only if your workload matches Ploy's: long-running, tool-heavy, output-token-dominated, design or generation. Run the 6-step evaluation before committing. The cost lever (cache strategy) is the largest source of pre-fix waste — if you migrate without rebuilding your cache config, you will conclude Sol is 50% more expensive than Opus and the migration is a mistake. With the cache rebuilt, the conclusion is usually the opposite. The lesson: never trust a cross-vendor cost comparison that was measured on a cold cache."),
]

# --- FAQ data (ZH) ---
ZH_FAQ = [
    ("GPT-5.6 Sol 和 Claude Opus 4.8 在生产里的成本差多少？",
     "在 Ploy 的重设计 agent 上（n=10 vs n=11），GPT-5.6 Sol 每次完成构建便宜 27%（$2.22 vs $3.06），墙钟时间快 2.2 倍（3m 42s vs 8m 00s），视觉评分反而更高。成本优势是修复缓存之后的；修复前 Sol 反而贵 50%。输出 token 数砍掉大约一半——Sol 写的是精简代码，不只是更快。"),
    ("为什么 Ploy 从 Claude Opus 4.8 切到 GPT-5.6 Sol？",
     "Opus 4.8 占据 Ploy 默认模型槽位 4 个月。那 4 个月里没有东西打败它。GPT-5.6 Sol 是第一个在 Ploy 那个具体工作负载（构建、编辑、截图真实营销网站）上打败它的。27% 成本下降 + 2.2 倍速度 + 更高视觉评分，足以支撑一次迁移。这次决定是成本博弈，不是能力博弈——同样的 $5/$30 每 token 价格，但 Sol 的 token 效率翻转了单次任务的总额。"),
    ("这次迁移需要改代码吗？",
     "需要。四个工程修复：(1) 审计 eval harness 找出在位模型假设，(2) 在 provider 边界转换工具 schema，让 Sol 的'填满每个参数'习惯不会被当作真实参数，(3) 围绕 GPT-5.6 的 key 分区缓存节点、用每 workspace key 重建 prompt caching，(4) 给 Responses API 调用设 `store: false` 让推理重放自包含。第 4 步代码改动最小。第 3 步是最大的成本杠杆。"),
    ("我能在不重写客户端代码的情况下用 GPT-5.6 Sol 吗？",
     "可以，通过 CLIProxyAPI（github.com/router-for-me/CLIProxyAPI），一个提供 OpenAI / Gemini / Claude / Codex / Grok 兼容 API 接口的开源代理。Tibo Sottiaux 的 X 贴文演示了 5 分钟的设置：装代理，用你已有的 OAuth 凭证连接，把你的客户端指向 OpenAI 兼容端点。适合独立开发者或小团队评估；不适合 Ploy 量级的生产流量。"),
    ("Claude Opus 4.8 仍然在哪些地方比 GPT-5.6 Sol 强？",
     "三类工作负载：(1) 每次调用推理质量比吞吐更重要的短生成，(2) 带有强现有品牌系统的设计任务（按 Ploy 设计负责人的说法，Sol'默认把文字做很大'），(3) 任何依赖 Anthropic 组织级共享缓存的多租户架构——GPT-5.6 按设计就不能跨 workspace 共享静态前缀，所以每个租户在空闲时要付 ~$0.18 冷写入成本。"),
    ("Claude Sonnet 5（6-30 重新部署）在这个对比里怎么定位？",
     "Sonnet 5 以 $2/$10 的促销价上线，截止 2026-08-31——比 Sonnet 4.5 便宜 33%。对中等重量 agent loop 和短时高质量生成，Sonnet 5 $2/$10 经常是比 Sol $5/$30 更好的默认选择，尤其当你的工作负载不需要 Sol 的推理深度时。今天的完整竞争集是 Sonnet 5（$2/$10）+ Opus 4.8（$15/$75）+ Sol（$5/$30）+ Terra（$2.50/$15）+ Luna（$1/$6）。正确的默认取决于工作负载。"),
    ("GPT-5.6 的 prompt caching 有什么坑？",
     "两个。第一，GPT-5.6 砍掉了部分前缀匹配，所以老的'在公共前缀上隐式缓存'那招不再有效——你需要显式的 `prompt_cache_breakpoint` 标记和 `prompt_cache_key`。第二，key 是缓存身份的一部分，每个 key 映射到一个节点，每分钟处理 ~15 个请求之后流量就分到冷节点。错误的 key 策略（每对话、一个全局）让你首次调用命中率接近 0。每 workspace key 是多租户应用的最佳点。"),
    ("GPT-5.6 Sol 现在能用了吗？",
     "可以，2026 年 6 月 26 日起，三个档位（Sol、Terra、Luna）都已通过 OpenAI API 正式上线。发布页面在 openai.com/index/gpt-5-6。Sonnet 5（可比的 Anthropic 档位）2026-06-30 也在美国出口管制指令解除后恢复上线。"),
    ("怎么拿到 GPT-5.6 Sol 的 API key？",
     "现有的 OpenAI API key 就能用——Sol 在同一个 api.openai.com 端点，你在请求里指定 model: 'gpt-5.6-sol' 即可。Responses API（/v1/responses）是 agent 工作负载推荐的接口表面，缓存 key + breakpoint 设计就用在这。Chat Completions（/v1/chat/completions）也能用，适合更简单的场景。"),
    ("我今天应该从 Opus 4.8 迁移到 GPT-5.6 Sol 吗？",
     "只有当你的工作负载匹配 Ploy 的：长运行、工具密集、输出 token 主导、设计或生成。在承诺之前跑上面那 6 步评估。成本杠杆（缓存策略）是修复前最大浪费源——如果你不重配缓存就迁移，你会得出 Sol 比 Opus 贵 50%、迁移是个错误的结论。缓存重配之后，结论通常相反。教训：永远不要信任在冷缓存上测出来的跨厂商成本对比。"),
]

# --- Affiliate sidebar (OpenAI/Anthropic have no public affiliate; use FreeModel as primary) ---
AFFILIATE = {
    "title": "试用 FreeModel",
    "description": "一个 API key 走多 provider 路由。GPT-5.6 Sol + Claude Sonnet 5 + Opus 4.8 + DeepSeek V4 —— 在 Sol vs Opus 切换时做 cost-routing 优化。",
    "url": "https://freemodel.dev/invite/FRE-7a3b6220",
    "cta": "获取免费额度"
}

# --- Load markdown bodies ---
with open('/root/apirank/drafts/en-gpt-5-6-sol-vs-claude-opus-4-8-production-migration-2026-07-13.md') as f:
    en_md = f.read()
en_md = re.sub(r'^---\s*\n.*?\n---\s*\n', '', en_md, count=1, flags=re.DOTALL)

with open('/root/apirank/drafts/zh-gpt-5-6-sol-vs-claude-opus-4-8-production-migration-2026-07-13.md') as f:
    zh_md = f.read()
zh_md = re.sub(r'^---\s*\n.*?\n---\s*\n', '', zh_md, count=1, flags=re.DOTALL)

# Convert to HTML bodies
en_body = md_to_astro_body(en_md)
zh_body = md_to_astro_body(zh_md)

# Check title/description lengths
en_title_full = EN_TITLE + ' | APIRank'
zh_title_full = ZH_TITLE + ' | APIRank'
print(f"EN title: {len(en_title_full)} chars (decoded: {len(EN_TITLE)}), desc: {len(EN_DESCRIPTION)} chars")
print(f"ZH title: {len(zh_title_full)} chars (decoded: {len(ZH_TITLE)}), desc: {len(ZH_DESCRIPTION)} chars")

assert len(en_title_full) <= 60, f"EN title too long: {len(en_title_full)}"
assert len(zh_title_full) <= 60, f"ZH title too long: {len(zh_title_full)}"
assert 70 <= len(EN_DESCRIPTION) <= 155, f"EN desc out of range: {len(EN_DESCRIPTION)}"
assert 70 <= len(ZH_DESCRIPTION) <= 155, f"ZH desc out of range: {len(ZH_DESCRIPTION)}"

# Build FAQ JSON-LD
def build_faq_jsonld(faq_list):
    items = []
    for q, a in faq_list:
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items
    }

en_faq_jsonld = build_faq_jsonld(EN_FAQ)
zh_faq_jsonld = build_faq_jsonld(ZH_FAQ)

# Use JS single-quoted strings to avoid \uXXXX escape trap
def js_str(s: str) -> str:
    """Quote a string for use in a JS .astro const declaration. Use single quotes, escape internal single quotes."""
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"

# --- EN .astro ---
en_astro = f"""---
import BaseLayout from '../../layouts/BaseLayout.astro';

const slug = {js_str(SLUG)};
const date = {js_str(DATE)};
const locale = 'en';

const enTitle = {js_str(EN_TITLE)};
const enDescription = {js_str(EN_DESCRIPTION)};
const canonicalUrl = `https://apirank.vip/tutorials/${{slug}}`;
const zhCanonicalUrl = `https://apirank.vip/zh/tutorials/${{slug}}`;

const articleJsonLd = {{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": enTitle,
  "description": enDescription,
  "datePublished": date,
  "dateModified": date,
  "author": {{ "@type": "Organization", "name": "APIRank", "url": "https://apirank.vip" }},
  "publisher": {{ "@type": "Organization", "name": "APIRank", "logo": {{ "@type": "ImageObject", "url": "https://apirank.vip/favicon.svg" }} }},
  "mainEntityOfPage": {{ "@type": "WebPage", "@id": `https://apirank.vip/tutorials/${{slug}}` }}
}};

const breadcrumbJsonLd = {{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://apirank.vip" }},
    {{ "@type": "ListItem", "position": 2, "name": "Tutorials", "item": "https://apirank.vip/tutorials" }},
    {{ "@type": "ListItem", "position": 3, "name": enTitle, "item": `https://apirank.vip/tutorials/${{slug}}` }}
  ]
}};

const faqJsonLd = {json.dumps(en_faq_jsonld, ensure_ascii=False)};

const enBody = `{en_body}`;

const affiliateSidebar = {{
  title: {js_str(AFFILIATE["title"])},
  description: {js_str(AFFILIATE["description"])},
  url: {js_str(AFFILIATE["url"])},
  cta: {js_str(AFFILIATE["cta"])}
}};
---

<BaseLayout
  title={{enTitle + ' | APIRank'}}
  description={{enDescription}}
  canonicalUrl={{canonicalUrl}}
  zhCanonicalUrl={{zhCanonicalUrl}}
  type="article"
>
  <script type="application/ld+json" set:html={{JSON.stringify(articleJsonLd)}} />
  <script type="application/ld+json" set:html={{JSON.stringify(breadcrumbJsonLd)}} />
  <script type="application/ld+json" set:html={{JSON.stringify(faqJsonLd)}} />
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="lg:grid lg:grid-cols-[1fr_300px] lg:gap-8">
      <div class="lg:col-span-2 space-y-8">
        <nav class="text-sm text-gray-500 mb-2">
          <a href="/" class="hover:underline">Home</a> &rsaquo;
          <a href="/tutorials" class="hover:underline">Tutorials</a> &rsaquo;
          <span class="text-gray-700">{{enTitle}}</span>
        </nav>
        <div set:html={{enBody}} />
      </div>
      <aside class="space-y-6 mt-8 lg:mt-0">
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 class="text-lg font-bold text-blue-900 mb-2">{{affiliateSidebar.title}}</h3>
          <p class="text-sm text-blue-800 mb-4">{{affiliateSidebar.description}}</p>
          <a href={{affiliateSidebar.url}} rel="sponsored noopener" target="_blank"
             class="inline-block bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
            {{affiliateSidebar.cta}}
          </a>
        </div>
        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h3 class="font-semibold text-gray-900 mb-2">Quick Facts</h3>
          <ul class="text-sm text-gray-700 space-y-1">
            <li><strong>Headline:</strong> Ploy cut cost 27% and time 2.2x by switching Opus 4.8 to GPT-5.6 Sol</li>
            <li><strong>Per-build cost:</strong> $2.22 (Sol) vs $3.06 (Opus 4.8)</li>
            <li><strong>Wall-clock:</strong> 3m 42s (Sol) vs 8m 00s (Opus 4.8)</li>
            <li><strong>Visual score:</strong> 0.970 (Sol) vs 0.936 (Opus 4.8)</li>
            <li><strong>Output tokens:</strong> 17.1K (Sol) vs 33.0K (Opus 4.8) — half the tokens</li>
            <li><strong>Cache lever:</strong> Pre-fix Sol was 50% MORE expensive (cold cache); per-workspace key raised first-call hit to 83.7%</li>
            <li><strong>Tool schema fix:</strong> Sol sends all 25 tool params with invented defaults; rewrite as required-but-nullable</li>
            <li><strong>Sonnet 5 angle:</strong> $2/$10 promo through 8/31/2026 is a cheaper default for non-flagship workloads</li>
            <li><strong>Affiliate:</strong> Use FreeModel to multi-route between Sol / Opus / Sonnet 5 with one key</li>
          </ul>
        </div>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-xxxxxxxxxxxxxx"
             data-ad-slot="xxxxxxxxxx"
             data-ad-format="auto"></ins>
      </aside>
    </div>
  </main>
</BaseLayout>
"""

# --- ZH .astro ---
zh_astro = f"""---
import BaseLayout from '../../../layouts/BaseLayout.astro';

const slug = {js_str(SLUG)};
const date = {js_str(DATE)};
const locale = 'zh';

const zhTitle = {js_str(ZH_TITLE)};
const zhDescription = {js_str(ZH_DESCRIPTION)};
const canonicalUrl = `https://apirank.vip/zh/tutorials/${{slug}}`;
const enCanonicalUrl = `https://apirank.vip/tutorials/${{slug}}`;

const articleJsonLd = {{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": zhTitle,
  "description": zhDescription,
  "datePublished": date,
  "dateModified": date,
  "author": {{ "@type": "Organization", "name": "APIRank", "url": "https://apirank.vip" }},
  "publisher": {{ "@type": "Organization", "name": "APIRank", "logo": {{ "@type": "ImageObject", "url": "https://apirank.vip/favicon.svg" }} }},
  "mainEntityOfPage": {{ "@type": "WebPage", "@id": `https://apirank.vip/zh/tutorials/${{slug}}` }}
}};

const breadcrumbJsonLd = {{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "首页", "item": "https://apirank.vip" }},
    {{ "@type": "ListItem", "position": 2, "name": "测评中心", "item": "https://apirank.vip/zh/tutorials" }},
    {{ "@type": "ListItem", "position": 3, "name": zhTitle, "item": `https://apirank.vip/zh/tutorials/${{slug}}` }}
  ]
}};

const faqJsonLd = {json.dumps(zh_faq_jsonld, ensure_ascii=False)};

const zhBody = `{zh_body}`;

const affiliateSidebar = {{
  title: {js_str(AFFILIATE["title"])},
  description: {js_str(AFFILIATE["description"])},
  url: {js_str(AFFILIATE["url"])},
  cta: {js_str(AFFILIATE["cta"])}
}};
---

<BaseLayout
  title={{zhTitle + ' | APIRank'}}
  description={{zhDescription}}
  canonicalUrl={{canonicalUrl}}
  enCanonicalUrl={{enCanonicalUrl}}
  type="article"
>
  <script type="application/ld+json" set:html={{JSON.stringify(articleJsonLd)}} />
  <script type="application/ld+json" set:html={{JSON.stringify(breadcrumbJsonLd)}} />
  <script type="application/ld+json" set:html={{JSON.stringify(faqJsonLd)}} />
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="lg:grid lg:grid-cols-[1fr_300px] lg:gap-8">
      <div class="lg:col-span-2 space-y-8">
        <nav class="text-sm text-gray-500 mb-2">
          <a href="/zh" class="hover:underline">首页</a> &rsaquo;
          <a href="/zh/tutorials" class="hover:underline">测评中心</a> &rsaquo;
          <span class="text-gray-700">{{zhTitle}}</span>
        </nav>
        <div set:html={{zhBody}} />
      </div>
      <aside class="space-y-6 mt-8 lg:mt-0">
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 class="text-lg font-bold text-blue-900 mb-2">{{affiliateSidebar.title}}</h3>
          <p class="text-sm text-blue-800 mb-4">{{affiliateSidebar.description}}</p>
          <a href={{affiliateSidebar.url}} rel="sponsored noopener" target="_blank"
             class="inline-block bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
            {{affiliateSidebar.cta}}
          </a>
        </div>
        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h3 class="font-semibold text-gray-900 mb-2">速查</h3>
          <ul class="text-sm text-gray-700 space-y-1">
            <li><strong>核心数据：</strong> Ploy 切到 Sol 后成本 -27%、墙钟 -54%</li>
            <li><strong>单次构建成本：</strong> $2.22（Sol） vs $3.06（Opus 4.8）</li>
            <li><strong>墙钟时间：</strong> 3m 42s（Sol） vs 8m 00s（Opus 4.8）</li>
            <li><strong>视觉评分：</strong> 0.970（Sol） vs 0.936（Opus 4.8）</li>
            <li><strong>输出 tokens：</strong> 17.1K（Sol） vs 33.0K（Opus 4.8）—— 一半</li>
            <li><strong>缓存杠杆：</strong> 修复前 Sol 反而贵 50%；每 workspace key 把首次命中拉到 83.7%</li>
            <li><strong>Schema 修复：</strong> Sol 会把工具全部 25 个参数都发；用 anyOf[T,null] 重写</li>
            <li><strong>Sonnet 5 角度：</strong> $2/$10 促销到 8/31/2026 是非旗舰档位更便宜的默认</li>
            <li><strong>联盟：</strong> FreeModel 一个 key 多 provider 路由（Sol / Opus / Sonnet 5）</li>
          </ul>
        </div>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-xxxxxxxxxxxxxx"
             data-ad-slot="xxxxxxxxxx"
             data-ad-format="auto"></ins>
      </aside>
    </div>
  </main>
</BaseLayout>
"""

# Write files
en_path = f'/root/apirank/src/pages/tutorials/{SLUG}.astro'
zh_path = f'/root/apirank/src/pages/zh/tutorials/{SLUG}.astro'

with open(en_path, 'w') as f:
    f.write(en_astro)
print(f"\nWrote EN: {en_path} ({len(en_astro)} chars)")

with open(zh_path, 'w') as f:
    f.write(zh_astro)
print(f"Wrote ZH: {zh_path} ({len(zh_astro)} chars)")

# Pre-build checks
print("\n=== Pre-build checks ===")
print(f"EN title len: {len(EN_TITLE + ' | APIRank')}")
print(f"ZH title len: {len(ZH_TITLE + ' | APIRank')}")
print(f"EN desc len: {len(EN_DESCRIPTION)}")
print(f"ZH desc len: {len(ZH_DESCRIPTION)}")
