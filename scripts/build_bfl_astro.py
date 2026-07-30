#!/usr/bin/env python3
"""Build .astro files from the BFL markdown drafts.
Generates:
  /root/apirank/src/pages/tutorials/black-forest-labs-flux-api-review.astro (EN)
  /root/apirank/src/pages/zh/tutorials/black-forest-labs-flux-api-review.astro (ZH)
"""
import re
import json
import sys
import os
import subprocess

sys.path.insert(0, '/root/apirank/scripts')
from md_to_astro_body import md_to_astro_body

# --- CONFIG ---
SLUG = "black-forest-labs-flux-api-review"
DATE = "2026-07-01"

# --- EN title + description ---
EN_TITLE = "BFL 2026: FLUX.2 Pro API for Image Gen"
EN_DESCRIPTION = "Black Forest Labs API review: FLUX.2 Pro + FLUX.1 family. Pricing, endpoints, fill/depth/canny, EU-Frankfurt GDPR hosting vs Replicate, fal.ai, Stability."

# --- ZH title + description ---
ZH_TITLE = "Black Forest Labs 2026：FLUX.2 Pro 图像生成 API 全面评测"
ZH_DESCRIPTION = "Black Forest Labs API 评测：FLUX.2 Pro + FLUX.1 系列。定价、端点、Fill/Depth/Canny、EU-Frankfurt GDPR 托管 vs Replicate、fal.ai、Stability。"

# --- FAQ data (EN) ---
EN_FAQ = [
    ("What is the Black Forest Labs API used for?",
     "The Black Forest Labs API is used for production image generation in advertising, e-commerce, social media, content marketing, and creative tooling. The flagship endpoints are FLUX.2 [pro] (text rendering, photorealistic portraits, hero images), FLUX.1 [schnell] (high-volume batch, real-time preview), and the Fill/Depth/Canny [pro] endpoints (inpainting, structural edit, sketch-to-image). BFL is the original creator of the FLUX model family, and the BFL API is the only first-party commercial path to the FLUX weights."),
    ("How much does the Black Forest Labs API cost?",
     "BFL uses a flat per-megapixel billing model with no credit packs or subscriptions. FLUX.2 [pro] costs $0.05 per megapixel (~$0.05 per 1024x1024 image, ~$0.21 per 2048x2048 image). FLUX.1.1 [pro] and FLUX.1 [pro] cost $0.04 per megapixel. FLUX.1 [schnell] costs $0.003 per megapixel — the cheapest production-quality image generation in the market. The Fill, Depth, and Canny endpoints cost $0.05 per megapixel."),
    ("Is there a Black Forest Labs free tier?",
     "BFL does not offer a persistent free tier, but the FLUX.1 [schnell] endpoint is priced at $0.003 per megapixel, which means $5 of credits covers roughly 1,500 1024x1024 images. The cheapest credit purchase is $5, which is the recommended starting point for prototyping. BFL does not require a credit card for the first credit purchase, and the [schnell] endpoint is suitable for high-volume batch workflows."),
    ("Can I use Black Forest Labs from inside China?",
     "BFL's API is hosted on AWS US-East and EU-Frankfurt. Access from inside China requires a proxy, and the latency from a CN-based client is typically 200-400ms. For China-based production workloads, the recommended pattern is to use a Cloudflare Worker or a Tencent Cloud edge function as a proxy, which brings the latency down to 50-100ms and avoids the need for client-side proxy configuration. Note that the proxy does not bypass the content policy — BFL still blocks prompts that violate the policy, regardless of geographic origin."),
    ("Does Black Forest Labs support OpenAI-compatible API calls?",
     "No. BFL uses its own API surface, not OpenAI's image generation schema. The endpoints are REST POST calls returning JSON, with the image URL in the response body. The BFL SDK (Python and Node.js) wraps the REST calls and handles rate limits, retries, and seed management. For an agent that needs image generation as a native capability, the BFL MCP server (released April 2026) is the path of least resistance — it exposes the FLUX endpoints as native tools inside Claude Code, Cursor, and other MCP-compatible IDEs."),
    ("How does Black Forest Labs compare to Replicate?",
     "Replicate hosts 100+ image generation models including FLUX.1 [pro], FLUX.1 [schnell], Stable Diffusion 3.5, Ideogram V3, and Playground V3. The pricing is roughly 5-15% higher than BFL direct (Replicate adds a middleman margin), and the cold start is slower (5-15 seconds vs 2-3 seconds for BFL direct). For a workflow that uses only FLUX, BFL is the right call. For a workflow that uses FLUX plus other models on the same bill, Replicate is the right call."),
    ("How does Black Forest Labs compare to fal.ai?",
     "fal.ai hosts 200+ image and video models including FLUX.2 [pro], FLUX.1 [schnell], Kling 2.1, MiniMax Video, HunyuanVideo, and Stable Diffusion 3.5. The pricing is roughly 5-15% higher than BFL direct, and the cold start is the fastest in the market (<1 second). For a workflow that needs FLUX plus video generation on the same bill, fal.ai is the right call. For a workflow that uses only FLUX at the lowest cost, BFL is the right call."),
    ("How does Black Forest Labs compare to Midjourney V8?",
     "Midjourney V8 has the strongest aesthetic quality in the market (April 2026 release), and the API is priced at $0.08 per image flat. Compared to BFL FLUX.2 [pro] at $0.05 per megapixel (~$0.05 per 1024x1024 image), Midjourney is 60% more expensive for the same image size. The aesthetic quality of Midjourney V8 is still slightly ahead of FLUX.2 [pro] for fashion and luxury categories, but for e-commerce, advertising, and content marketing, the quality gap is small enough that the cost differential makes BFL the right call."),
    ("What is the BFL MCP server?",
     "The BFL MCP server is a remote endpoint at `https://mcp.bfl.ml/mcp` that exposes the FLUX.2 [pro], FLUX.1.1 [pro], FLUX.1 [schnell], and the Fill/Depth/Canny endpoints as native tools inside Claude Code, Cursor, Cline, and other MCP-compatible IDEs. The MCP server uses the standard Streamable HTTP transport and is free for all BFL API users. For an engineer building an agent that needs image generation as a native capability, the MCP server is the path of least resistance."),
    ("Can I use Black Forest Labs for batch thumbnail generation?",
     "Yes. The FLUX.1 [schnell] endpoint at $0.003 per megapixel is the right call for batch thumbnail generation. For a workload generating 10,000 512x512 thumbnails per day, the cost is roughly $8/day. The schnell endpoint allows 60+ concurrent requests without rate limit issues, which makes it suitable for high-volume batch workflows. The 4-step diffusion produces \"good enough\" quality for thumbnails and preview use cases."),
    ("Does Black Forest Labs have an affiliate program?",
     "BFL does not currently have a public affiliate program. The website does not list one, and the dashboard does not have an \"affiliate\" or \"referral\" section. For content sites that want to monetize BFL coverage, the right pattern is to use BFL's API for content creation and link to the platform as a tool recommendation. The enterprise team is open to custom partnership arrangements for high-volume content sites; contact enterprise@blackforestlabs.ai for details."),
]

# --- FAQ data (ZH) ---
ZH_FAQ = [
    ("Black Forest Labs API 用于什么？",
     "Black Forest Labs API 用于广告、电商、社交媒体、内容营销和创意工具中的生产图像生成。旗舰端点是 FLUX.2 [pro]（文字渲染、写实人像、hero 图）、FLUX.1 [schnell]（大批量、实时预览）以及 Fill/Depth/Canny [pro] 端点（修复、结构编辑、草图转图像）。BFL 是 FLUX 模型家族的原始创建者，BFL API 是访问 FLUX 权重的唯一原厂商业路径。"),
    ("Black Forest Labs API 多少钱？",
     "BFL 使用平价每兆像素计费模型，没有积分包或订阅。FLUX.2 [pro] 成本为每兆像素 $0.05（每张 1024x1024 约 $0.05，每张 2048x2048 约 $0.21）。FLUX.1.1 [pro] 和 FLUX.1 [pro] 成本为每兆像素 $0.04。FLUX.1 [schnell] 成本为每兆像素 $0.003——市场上最便宜的生产质量图像生成。Fill、Depth 和 Canny 端点成本为每兆像素 $0.05。"),
    ("Black Forest Labs 有免费层吗？",
     "BFL 不提供持久的免费层，但 FLUX.1 [schnell] 端点定价为每兆像素 $0.003，这意味着 $5 的信用额度覆盖大约 1,500 张 1024x1024 图像。最便宜的信用购买是 $5，这是原型设计的推荐起点。BFL 第一次信用购买不需要信用卡，schnell 端点适合大批量工作流。"),
    ("我可以在中国使用 Black Forest Labs 吗？",
     "BFL 的 API 托管在 AWS US-East 和 EU-Frankfurt。从中国境内访问需要代理，从中国客户端的延迟通常为 200-400ms。对于中国生产工作负载，推荐模式是使用 Cloudflare Worker 或腾讯云边缘函数作为代理，将延迟降低到 50-100ms，并避免客户端代理配置的需要。请注意，代理不会绕过内容政策——BFL 仍然阻止违反政策的 prompt，无论地理来源如何。"),
    ("Black Forest Labs 支持 OpenAI 兼容的 API 调用吗？",
     "不支持。BFL 使用自己的 API 表面，而不是 OpenAI 的图像生成模式。端点是返回 JSON 的 REST POST 调用，响应体中包含图像 URL。BFL SDK（Python 和 Node.js）包装了 REST 调用并处理速率限制、重试和种子管理。对于需要将图像生成本地化为原生能力的代理，BFL MCP 服务器（2026 年 4 月发布）是阻力最小的路径——它将 FLUX 端点作为本地工具暴露在 Claude Code、Cursor 和其他兼容 MCP 的 IDE 中。"),
    ("Black Forest Labs 与 Replicate 相比如何？",
     "Replicate 托管 100+ 图像生成模型，包括 FLUX.1 [pro]、FLUX.1 [schnell]、Stable Diffusion 3.5、Ideogram V3 和 Playground V3。定价比 BFL 直接贵约 5-15%（Replicate 添加中间商利润），冷启动较慢（5-15 秒 vs BFL 直接的 2-3 秒）。对于仅使用 FLUX 的工作流，BFL 是正确选择。对于在同一个账单上使用 FLUX 和其他模型的工作流，Replicate 是正确选择。"),
    ("Black Forest Labs 与 fal.ai 相比如何？",
     "fal.ai 托管 200+ 图像和视频模型，包括 FLUX.2 [pro]、FLUX.1 [schnell]、Kling 2.1、MiniMax Video、HunyuanVideo 和 Stable Diffusion 3.5。定价比 BFL 直接贵约 5-15%，冷启动是市场上最快的（<1 秒）。对于需要在同一账单上使用 FLUX 和视频生成的工作流，fal.ai 是正确选择。对于以最低成本仅使用 FLUX 的工作流，BFL 是正确选择。"),
    ("Black Forest Labs 与 Midjourney V8 相比如何？",
     "Midjourney V8 在市场上具有最强的美学质量（2026 年 4 月发布），API 定价为每张 $0.08 的统一价格。与 BFL FLUX.2 [pro] 每兆像素 $0.05（每张 1024x1024 约 $0.05）相比，Midjourney 对于相同图像尺寸贵 60%。Midjourney V8 的美学质量在时尚和奢侈品类目上仍略领先于 FLUX.2 [pro]，但对于电商、广告和内容营销，质量差距足够小，成本差异使 BFL 成为正确选择。"),
    ("什么是 BFL MCP 服务器？",
     "BFL MCP 服务器是位于 `https://mcp.bfl.ml/mcp` 的远程端点，将 FLUX.2 [pro]、FLUX.1.1 [pro]、FLUX.1 [schnell] 和 Fill/Depth/Canny 端点作为本地工具暴露在 Claude Code、Cursor、Cline 和其他兼容 MCP 的 IDE 中。MCP 服务器使用标准的 Streamable HTTP 传输，对所有 BFL API 用户免费。对于构建需要将图像生成本地化为原生能力的代理的工程师，MCP 服务器是阻力最小的路径。"),
    ("我可以将 Black Forest Labs 用于批量缩略图生成吗？",
     "可以。$0.003/MP 的 FLUX.1 [schnell] 端点是批量缩略图生成的正确选择。对于每天生成 10,000 张 512x512 缩略图的工作负载，成本约为 $8/天。schnell 端点允许 60+ 并发请求而没有速率限制问题，这使其适合大批量工作流。4 步扩散为缩略图和预览用例产生\"足够好\"的质量。"),
    ("Black Forest Labs 有联盟推广计划吗？",
     "BFL 目前没有公共联盟推广计划。网站未列出，仪表板也没有\"联盟\"或\"推荐\"部分。对于希望通过 BFL 内容获利的网站，正确模式是使用 BFL 的 API 进行内容创建并将平台链接为工具推荐。企业团队对大批量内容网站的定制合作伙伴关系持开放态度；详情请联系 enterprise@blackforestlabs.ai。"),
]

# --- Affiliate sidebar (BFL has no public affiliate; use FreeModel as primary) ---
AFFILIATE = {
    "title": "试用 FreeModel",
    "description": "一个 API key 走多 provider 路由。DeepSeek + Qwen + Llama + OpenAI 兼容上游 —— 跟 BFL 配合做图像生成的成本优化。",
    "url": "https://freemodel.dev/invite/FRE-7a3b6220",
    "cta": "获取免费额度"
}

# --- Load markdown bodies ---
with open('/root/apirank/drafts/en-black-forest-labs-flux-api-review-2026-07-01.md') as f:
    en_md = f.read()
en_md = re.sub(r'^---\s*\n.*?\n---\s*\n', '', en_md, count=1, flags=re.DOTALL)

with open('/root/apirank/drafts/zh-black-forest-labs-flux-api-review-2026-07-01.md') as f:
    zh_md = f.read()
zh_md = re.sub(r'^---\s*\n.*?\n---\s*\n', '', zh_md, count=1, flags=re.DOTALL)

# Convert to HTML bodies
en_body = md_to_astro_body(en_md)
zh_body = md_to_astro_body(zh_md)

# Check title/description lengths
en_title_full = EN_TITLE + ' | APIRank'  # BaseLayout doesn't auto-append because title already includes APIRank; but title doesn't include APIRank, so BaseLayout will add
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
# But since we're writing the .astro as a file, we need to use proper JSON syntax
# In .astro frontmatter (JavaScript), we use single quotes for const strings
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
            <li><strong>Provider:</strong> Black Forest Labs (FLUX creator)</li>
            <li><strong>Endpoints:</strong> FLUX.2 [pro], FLUX.1.1 [pro], FLUX.1 [schnell], Fill/Depth/Canny [pro]</li>
            <li><strong>Pricing:</strong> $0.003-$0.05 per megapixel (no subscription)</li>
            <li><strong>Hosting:</strong> AWS US-East + EU-Frankfurt (GDPR option)</li>
            <li><strong>API:</strong> <code>https://api.bfl.ml</code> + MCP server at <code>https://mcp.bfl.ml/mcp</code></li>
            <li><strong>Open-source:</strong> FLUX.1 [schnell] is Apache 2.0 (self-host OK)</li>
            <li><strong>Affiliate:</strong> Use FreeModel for cost optimization overlay</li>
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
            <li><strong>Black Forest Labs:</strong> FLUX 模型原厂 + FLUX.2 Pro（2026 年 7 月）</li>
            <li><strong>端点：</strong> FLUX.2 [pro]、FLUX.1.1 [pro]、FLUX.1 [schnell]、Fill/Depth/Canny [pro]</li>
            <li><strong>定价：</strong> 每兆像素 $0.003-$0.05（无订阅）</li>
            <li><strong>托管：</strong> AWS US-East + EU-Frankfurt（GDPR 选项）</li>
            <li><strong>API：</strong> <code>https://api.bfl.ml</code> + MCP <code>https://mcp.bfl.ml/mcp</code></li>
            <li><strong>开源：</strong> FLUX.1 [schnell] 是 Apache 2.0（可自托管）</li>
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
