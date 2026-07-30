#!/usr/bin/env python3
"""Build .astro files for the ChatGPT Work / GPT-5.6 agent cost news-analysis article.
Generates:
  /root/apirank/src/pages/tutorials/chatgpt-work-gpt-5-6-agent-api-cost-2026.astro (EN)
  /root/apirank/src/pages/zh/tutorials/chatgpt-work-gpt-5-6-agent-api-cost-2026.astro (ZH)
"""
import re
import json
import sys
import os

sys.path.insert(0, '/root/apirank/scripts')
from md_to_astro_body import md_to_astro_body

# --- CONFIG ---
SLUG = "chatgpt-work-gpt-5-6-agent-api-cost-2026"
DATE = "2026-07-10"

# --- EN title + description ---
# Title target: 30-60 chars (BaseLayout appends " | APIRank" = +10)
# 50 chars + 10 suffix = 60 chars exactly
EN_TITLE = "ChatGPT Work 2026: GPT-5.6 Agent API Cost"
EN_DESCRIPTION = "ChatGPT Work API cost 2026: $0.40/agent-hour pricing for GPT-5.6 long-running agents. Token economics vs Claude Sonnet 5, DeepSeek V4."

# --- ZH title + description ---
# 50 chars + 10 suffix = 60 chars exactly
ZH_TITLE = "ChatGPT Work 成本 2026：GPT-5.6 Agent 定价解析"
ZH_DESCRIPTION = "ChatGPT Work 成本 2026：$0.40/agent-小时 GPT-5.6 长运行 agent 定价。与 Claude Sonnet 5、DeepSeek V4 的 token 经济性对比及适用场景。"

# --- FAQ data (EN) ---
EN_FAQ = [
    ("What is ChatGPT Work?",
     "ChatGPT Work is OpenAI's long-running agent product launched July 9, 2026, built on GPT-5.6. It gives agents a persistent state — workspace directory, shell environment, process pool — and charges per agent-hour of background runtime instead of per request. The runtime is exposed through the Responses API with `background: true`."),
    ("How much does ChatGPT Work cost?",
     "The API tier is $0.40 per agent-hour, with GPT-5.6 model usage included up to 1M tokens/hour. Beyond the included quota, GPT-5.6 Luna overage rates apply ($0.50/M input, $1.50/M output). ChatGPT Work Pro is $0.20/hour (5M tokens/hour included) and ChatGPT Work Team is $0.15/hour per seat (10M tokens/hour included)."),
    ("Is ChatGPT Work cheaper than GPT-5.6 standard API?",
     "It depends on the workload. For a low-token-density 4-hour research agent, ChatGPT Work is 6x more expensive than GPT-5.6 Luna standard. For a token-dense 8-hour code-refactor agent, ChatGPT Work is 25% cheaper than Luna standard. The break-even is roughly 4-5 hours of runtime with moderate-to-high token density."),
    ("What is the difference between ChatGPT Work and GPT-5.6 standard?",
     "ChatGPT Work adds persistent state (workspace, shell, processes) and charges per agent-hour. GPT-5.6 standard is a stateless Chat Completions API that charges per million tokens. ChatGPT Work is for autonomous long-running agents; GPT-5.6 standard is for synchronous request/response."),
    ("Can I use Claude or DeepSeek in ChatGPT Work?",
     "Not directly. ChatGPT Work only ships with GPT-5.6 in the runtime. You can bring your own API key for Claude or DeepSeek as separate tool calls, but you pay separately for those models on top of the $0.40/agent-hour ChatGPT Work runtime. For a multi-model agent, a routing layer (OpenRouter or Cloudflare AI Gateway) without the ChatGPT Work runtime is usually cheaper."),
    ("How does ChatGPT Work compare to Claude Sonnet 5 for agents?",
     "For an 8-hour code-refactor workload with 8M input + 4M output tokens, ChatGPT Work costs $3.20 (within the included quota) versus Claude Sonnet 5 at $56 with the August 31 promo pricing ($2 input / $10 output). ChatGPT Work is 17x cheaper for that specific workload, but Sonnet 5 has stronger per-call reasoning quality for non-agent workloads. Use ChatGPT Work for autonomous long-running tasks, Sonnet 5 for short high-quality generation."),
    ("Does ChatGPT Work have an affiliate program?",
     "No. OpenAI does not currently have a public affiliate program for ChatGPT Work or any other API product. For monetization on a ChatGPT Work review, the standard pattern is to recommend a cost-routing aggregator like FreeModel that lets users spread the same workload across GPT-5.6, Claude Sonnet 5, and DeepSeek V4 with a single API key."),
    ("What is the token quota for ChatGPT Work?",
     "1M tokens/hour for the API tier, 5M tokens/hour for Pro, 10M tokens/hour for Team. The quota is per work_id, not per account — running 5 background agents in parallel gives you 5M tokens/hour total, but each individual agent is capped at 1M. Beyond the quota, GPT-5.6 Luna overage rates apply."),
    ("Can I run ChatGPT Work from inside China?",
     "OpenAI's API is hosted on AWS US-East. Access from inside China requires a stable proxy connection. For production workloads serving China-based users, the recommended pattern is to use a Cloudflare Worker as a proxy, which keeps the work_id state on the OpenAI side while bringing the latency down to 50-100ms for the Chinese client. Note that the proxy does not bypass the OpenAI content policy."),
    ("How long does a ChatGPT Work background task persist?",
     "A work_id that you do not explicitly cancel or complete stays in OpenAI's system for 30 days. Storage is free for the first 7 days, then $0.10/GB-day after. The 30-day retention is for debugging and re-running failed tasks; for production workloads, the recommended pattern is to cancel or complete the work_id as soon as the agent finishes its task."),
    ("Is ChatGPT Work available now?",
     "Yes, as of July 9, 2026, ChatGPT Work is generally available through the OpenAI API with the Responses API surface. The ChatGPT desktop and Team integrations are also live. The launch page is at openai.com/index/chatgpt-for-your-most-ambitious-work.")
]

# --- FAQ data (ZH) ---
ZH_FAQ = [
    ("ChatGPT Work 是什么？",
     "ChatGPT Work 是 OpenAI 于 2026 年 7 月 9 日推出的长运行 agent 产品，基于 GPT-5.6 构建。它为 agent 提供持久状态——工作空间目录、shell 环境、进程池——并按 agent-小时 的后台运行时计费，而非按请求。运行时通过带 `background: true` 的 Responses API 暴露。"),
    ("ChatGPT Work 多少钱？",
     "API 层级为 $0.40/agent-小时，GPT-5.6 模型用量包含每小时最多 1M tokens。超出包含配额后，按 GPT-5.6 Luna 超额费率计费（$0.50/M 输入、$1.50/M 输出）。ChatGPT Work Pro 为 $0.20/小时（包含 5M tokens/小时），ChatGPT Work Team 为每位席位 $0.15/小时（包含 10M tokens/小时）。"),
    ("ChatGPT Work 比 GPT-5.6 标准 API 便宜吗？",
     "取决于工作负载。对于低 token 密度的 4 小时研究 agent，ChatGPT Work 比 GPT-5.6 Luna 标准贵 6 倍。对于 token 密集的 8 小时代码重构 agent，ChatGPT Work 比 Luna 标准便宜 25%。盈亏平衡点约为 4-5 小时 运行时，配中到高 token 密度。"),
    ("ChatGPT Work 与 GPT-5.6 标准的区别是什么？",
     "ChatGPT Work 增加持久状态（工作空间、shell、进程）并按 agent-小时 计费。GPT-5.6 标准是无状态的 Chat Completions API，按每百万 tokens 计费。ChatGPT Work 用于自主长运行 agent；GPT-5.6 标准用于同步请求/响应。"),
    ("ChatGPT Work 中可以使用 Claude 或 DeepSeek 吗？",
     "不能直接使用。ChatGPT Work 的运行时只搭载 GPT-5.6。你可以将 Claude 或 DeepSeek 的 API key 作为单独的工具调用引入，但要在 $0.40/agent-小时 ChatGPT Work 运行时之外单独支付这些模型。对于多模型 agent，没有 ChatGPT Work 运行时的路由层（OpenRouter 或 Cloudflare AI Gateway）通常更便宜。"),
    ("ChatGPT Work 与 Claude Sonnet 5 在 agent 方面如何对比？",
     "对于 8 小时代码重构工作负载（8M 输入 + 4M 输出 tokens），ChatGPT Work 成本 $3.20（在包含配额内），而 Claude Sonnet 5 在 8 月 31 日促销定价下为 $56（$2 输入 / $10 输出）。ChatGPT Work 在该特定工作负载上便宜 17 倍，但 Sonnet 5 在非 agent 工作负载上每次调用推理质量更强。将 ChatGPT Work 用于自主长运行任务，Sonnet 5 用于短时高质量生成。"),
    ("ChatGPT Work 有联盟推广计划吗？",
     "没有。OpenAI 目前对 ChatGPT Work 或任何其他 API 产品都没有公开联盟推广计划。在 ChatGPT Work 评测中实现变现的标准模式是推荐成本路由聚合器，如 FreeModel，让用户用单一 API key 将同样的工作负载分配到 GPT-5.6、Claude Sonnet 5 和 DeepSeek V4。"),
    ("ChatGPT Work 的 token 配额是多少？",
     "API 层级为 1M tokens/小时，Pro 为 5M tokens/小时，Team 为 10M tokens/小时。配额按 work_id 计算，不是按账户——并行运行 5 个后台 agent 给你总共 5M tokens/小时，但每个单独的 agent 上限为 1M。超出配额后，按 GPT-5.6 Luna 超额费率计费。"),
    ("我可以在中国境内使用 ChatGPT Work 吗？",
     "OpenAI 的 API 托管在 AWS US-East。从中国境内访问需要稳定的代理连接。对于服务中国用户的生产工作负载，推荐模式是使用 Cloudflare Worker 作为代理，让 work_id 状态保留在 OpenAI 端，同时将中国客户端的延迟降至 50-100ms。请注意，代理不会绕过 OpenAI 内容政策。"),
    ("ChatGPT Work 后台任务持续多久？",
     "没有显式取消或完成的 work_id 会在 OpenAI 系统中保留 30 天。存储前 7 天免费，之后 $0.10/GB-天。30 天保留期用于调试和重运行失败任务；对于生产工作负载，推荐模式是一旦 agent 完成任务，立即取消或完成该 work_id。"),
    ("ChatGPT Work 现在可用吗？",
     "可用，截至 2026 年 7 月 9 日，ChatGPT Work 通过 OpenAI API（Responses API 表面）已正式上线。ChatGPT 桌面版和 Team 集成也已上线。发布页面位于 openai.com/index/chatgpt-for-your-most-ambitious-work。")
]

# --- Affiliate sidebar (ChatGPT Work has no public affiliate; use FreeModel as primary) ---
AFFILIATE = {
    "title": "试用 FreeModel",
    "description": "一个 API key 走多 provider 路由。GPT-5.6 + Claude Sonnet 5 + DeepSeek V4 —— 跟 ChatGPT Work 配合做长运行 agent 的成本优化。",
    "url": "https://freemodel.dev/invite/FRE-7a3b6220",
    "cta": "获取免费额度"
}

# --- Load markdown bodies ---
with open('/root/apirank/drafts/en-chatgpt-work-gpt-5-6-agent-api-cost-2026.md') as f:
    en_md = f.read()
en_md = re.sub(r'^---\s*\n.*?\n---\s*\n', '', en_md, count=1, flags=re.DOTALL)

with open('/root/apirank/drafts/zh-chatgpt-work-gpt-5-6-agent-api-cost-2026.md') as f:
    zh_md = f.read()
zh_md = re.sub(r'^---\s*\n.*?\n---\s*\n', '', zh_md, count=1, flags=re.DOTALL)

# Convert to HTML bodies
en_body = md_to_astro_body(en_md)
zh_body = md_to_astro_body(zh_md)

# Check title/description lengths
en_title_full = EN_TITLE + ' | APIRank'
zh_title_full = ZH_TITLE + ' | APIRank'
print(f"EN title: {len(en_title_full)} chars, desc: {len(EN_DESCRIPTION)} chars")
print(f"ZH title: {len(zh_title_full)} chars, desc: {len(ZH_DESCRIPTION)} chars")

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

# Use JS single-quoted strings to avoid \uXXXX escape trap (per skill warning)
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
            <li><strong>Product:</strong> ChatGPT Work (long-running agent)</li>
            <li><strong>Base model:</strong> GPT-5.6 (Luna/Terra/Sol tiers available)</li>
            <li><strong>Pricing:</strong> $0.40/agent-hour (API), $0.20 (Pro), $0.15 (Team)</li>
            <li><strong>Token quota:</strong> 1M tokens/hour (API), 5M (Pro), 10M (Team)</li>
            <li><strong>Persistent state:</strong> Workspace, shell, process pool, 30-day retention</li>
            <li><strong>Best for:</strong> Multi-hour research, code refactors, data pipelines</li>
            <li><strong>Avoid for:</strong> Synchronous chat, one-shot generation, non-OpenAI model agents</li>
            <li><strong>Affiliate:</strong> Use FreeModel for cost-routing optimization overlay</li>
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
            <li><strong>产品：</strong> ChatGPT Work（长运行 agent）</li>
            <li><strong>基础模型：</strong> GPT-5.6（Luna/Terra/Sol 三档）</li>
            <li><strong>定价：</strong> $0.40/agent-小时（API），$0.20（Pro），$0.15（Team）</li>
            <li><strong>Token 配额：</strong> 1M tokens/小时（API），5M（Pro），10M（Team）</li>
            <li><strong>持久状态：</strong> 工作空间、shell、进程池，30 天保留</li>
            <li><strong>最适合：</strong> 多小时研究、代码重构、数据管道</li>
            <li><strong>避免使用：</strong> 同步聊天、一次性生成、非 OpenAI 模型 agent</li>
            <li><strong>联盟：</strong> FreeModel 多 provider 路由叠加</li>
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

# Check for { } in body (after the frontmatter)
en_body_section = en_astro[en_astro.index('const enBody = `') + len('const enBody = `'):en_astro.rindex('`;')]
zh_body_section = zh_astro[zh_astro.index('const zhBody = `') + len('const zhBody = `'):zh_astro.rindex('`;')]

# We already escaped them in the md_to_astro_body for code blocks; check
en_unencoded_braces = re.findall(r'(?<!&#)\{(?!\d|\w|123|125)', en_body_section)
zh_unencoded_braces = re.findall(r'(?<!&#)\{(?!\d|\w|123|125)', zh_body_section)
print(f"EN body unescaped {{ in body: {len(en_unencoded_braces)}")
print(f"ZH body unescaped {{ in body: {len(zh_unencoded_braces)}")
