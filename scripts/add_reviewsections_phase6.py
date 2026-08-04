#!/usr/bin/env python3
"""
Add reviewSections to meta-ai, aliyun, baidu (Phase 6) using string-splice (FM #15).
Avoids json.dump(indent=2) reformatting the whole file.
"""
import json
import sys

PROVIDERS_PATH = '/root/apirank/src/data/providers.json'

# --- reviewSections payloads (4 sections each, EN+ZH) ---

META_AI_SECTIONS = [
    {
        "title": "💰 Pricing & Plans",
        "titleZh": "💰 价格与方案",
        "type": "table",
        "headers": ["Model", "Input ($/M tokens)", "Output ($/M tokens)", "Best For"],
        "headersZh": ["模型", "输入 ($/百万 token)", "输出 ($/百万 token)", "最佳用途"],
        "rows": [
            ["Muse Spark 1.1", "$1.25", "$4.25", "Agentic tool-calling, computer use"],
            ["Cached input", "$0.15", "—", "Repeated system prompts (10× cheaper)"],
            ["Web search", "—", "$2.50/1k queries", "Search-grounded answers (per-query fee)"]
        ],
        "rowsZh": [
            ["Muse Spark 1.1", "$1.25", "$4.25", "智能体工具调用、电脑使用"],
            ["缓存输入", "$0.15", "—", "重复系统提示（10× 优惠）"],
            ["联网搜索", "—", "$2.50/千次", "搜索增强回答（按查询计费）"]
        ]
    },
    {
        "title": "🔧 API & Developer Experience",
        "titleZh": "🔧 API 与开发者体验",
        "type": "list",
        "items": [
            {"label": "API Style", "value": "OpenAI-compatible /v1/chat/completions — drop-in replacement by swapping base_url and api_key. No SDK migration needed for existing OpenAI codebases."},
            {"label": "Base URL", "value": "https://api.meta.ai/v1 (public preview) — Meta's official endpoint for the developer platform."},
            {"label": "Context Window", "value": "1M tokens — among the largest context windows in any frontier-tier API, suitable for full-codebase analysis and long document processing."},
            {"label": "Multimodal Input", "value": "Native support for text, image, video, and PDF inputs in a single request; text output only. Useful for OCR, video understanding, and document analysis."},
            {"label": "Function Calling & Tools", "value": "First-party native tool calling with structured JSON-schema validation. Includes computer use, search grounding, and multi-agent orchestration primitives — among the most capable agentic tool surfaces available."},
            {"label": "Streaming", "value": "SSE token streaming included by default; intermediate reasoning/tool traces are inspectable in stream chunks for agentic debugging."},
            {"label": "Free Tier", "value": "60 RPM and 2M TPM with free credits on signup for US developers — enough to prototype agentic workflows before paid usage."}
        ],
        "itemsZh": [
            {"label": "API 风格", "value": "OpenAI 兼容的 /v1/chat/completions — 替换 base_url 和 api_key 即可即插即用。现有 OpenAI 代码库无需迁移 SDK。"},
            {"label": "Base URL", "value": "https://api.meta.ai/v1（公开预览）— Meta 开发者平台的官方端点。"},
            {"label": "上下文窗口", "value": "1M token — 一线 API 中最大的上下文窗口之一，适合全代码库分析与长文档处理。"},
            {"label": "多模态输入", "value": "单次请求原生支持文本、图像、视频与 PDF 输入；输出仅文本。适用于 OCR、视频理解和文档分析。"},
            {"label": "函数调用与工具", "value": "官方原生工具调用支持结构化 JSON schema 验证。包含电脑使用、搜索增强与多智能体编排原语 — 是目前最具能力的智能体工具界面之一。"},
            {"label": "流式输出", "value": "默认提供 SSE token 流式；中间推理/工具轨迹可在流块中检查，便于智能体调试。"},
            {"label": "免费额度", "value": "60 RPM 与 2M TPM，美国开发者注册即获免费 credits — 足以在付费使用前对智能体工作流进行原型验证。"}
        ]
    },
    {
        "title": "🧠 Native Agentic Tool Surface",
        "titleZh": "🧠 原生智能体工具界面",
        "type": "text",
        "text": "What sets Meta's API apart from other OpenAI-compatible providers is the depth of its first-party agentic tool surface. While most compatible APIs expose Function Calling as a thin schema-validation wrapper, Meta ships computer use (browser/desktop control), search grounding (real-time web search with citations), and multi-agent orchestration primitives as built-in tools — not third-party add-ons.\n\nFor teams building coding agents, research agents, or browser-automation products, this means the agent's tool loop can stay within Meta's API surface rather than stitching together multiple vendors. The 1M token context window combined with computer use and search grounding is a particularly strong combination for long-horizon agent tasks that need to read, search, and act across many web pages or documents in a single session.",
        "textZh": "Meta API 与其他 OpenAI 兼容提供商的区别在于其官方智能体工具界面的深度。大多数兼容 API 仅将函数调用作为一层薄薄的 schema 验证封装，Meta 则将电脑使用（浏览器/桌面控制）、搜索增强（带引用的实时联网搜索）以及多智能体编排原语作为内置工具直接提供 — 而非第三方附加组件。\n\n对于构建编码智能体、研究智能体或浏览器自动化产品的团队，这意味着智能体的工具循环可以保持在 Meta 的 API 界面内，而无需拼接多家厂商。1M token 上下文窗口结合电脑使用与搜索增强，对于需要在单次会话中跨多个网页或文档进行阅读、搜索与行动的长程智能体任务尤其强大。"
    },
    {
        "title": "🌐 Regional Availability & Latency",
        "titleZh": "🌐 中国访问与延迟",
        "type": "text",
        "text": "Meta's API is currently in public preview and is limited to US developers. Access from mainland China requires a stable proxy or overseas server routing. From a US-based client, latency to api.meta.ai is typically 100-200ms for first-token streaming — comparable to OpenAI/Anthropic from the same region.\n\nFor production workloads serving China-based users, an aggregator (such as OpenRouter with Meta routing, or domestic re-sellers) is the standard pattern. Direct connection from Chinese IPs is not currently supported at the network edge. The public preview also means model availability and pricing may shift before general availability — teams building on Meta's API should plan for API surface changes over the next 6-12 months.",
        "textZh": "Meta 的 API 目前处于公开预览阶段，仅面向美国开发者。从中国大陆访问需要稳定的代理或海外服务器中转。从美国客户端访问 api.meta.ai 的延迟通常在 100-200ms 首 token 流式响应 — 与同区域的 OpenAI/Anthropic 相当。\n\n对面向中国用户的服务生产负载，标准方案是使用聚合器（如带 Meta 路由的 OpenRouter，或国内转售商）。中国 IP 在网络边缘目前不支持直接连接。公开预览也意味着模型可用性与定价可能在正式 GA 前发生变化 — 基于 Meta API 构建的团队应规划未来 6-12 个月内 API 界面的变化。"
    }
]

ALIYUN_SECTIONS = [
    {
        "title": "💰 Pricing & Plans",
        "titleZh": "💰 价格与方案",
        "type": "table",
        "headers": ["Model", "Input (¥/M tokens)", "Output (¥/M tokens)", "Best For"],
        "headersZh": ["模型", "输入 (¥/百万 token)", "输出 (¥/百万 token)", "最佳用途"],
        "rows": [
            ["Qwen3.5-Max", "¥4.00", "¥12.00", "Top-tier reasoning, complex tasks"],
            ["Qwen3.5-Plus", "¥2.00", "¥6.00", "General chat, balanced price/quality"],
            ["Qwen3.5-72B", "¥4.00", "¥12.00", "Open-weights equivalent, self-host option"],
            ["QwQ-32B", "¥2.00", "¥8.00", "Chain-of-thought reasoning (o1-like)"],
            ["Qwen-Omni-Turbo", "¥1.60", "¥4.80", "Multimodal (text+image+audio)"]
        ],
        "rowsZh": [
            ["Qwen3.5-Max", "¥4.00", "¥12.00", "顶级推理、复杂任务"],
            ["Qwen3.5-Plus", "¥2.00", "¥6.00", "通用对话、性价比平衡"],
            ["Qwen3.5-72B", "¥4.00", "¥12.00", "开源权重等价、可自托管"],
            ["QwQ-32B", "¥2.00", "¥8.00", "链式推理（o1 同类）"],
            ["Qwen-Omni-Turbo", "¥1.60", "¥4.80", "多模态（文本+图像+音频）"]
        ]
    },
    {
        "title": "🔧 API & Developer Experience",
        "titleZh": "🔧 API 与开发者体验",
        "type": "list",
        "items": [
            {"label": "API Style", "value": "OpenAI-compatible /v1/chat/completions endpoint via Bailian (DashScope) platform — drop-in replacement by changing base_url and api_key."},
            {"label": "Base URL", "value": "https://dashscope.aliyuncs.com/compatible-mode/v1 — direct from China, no proxy required. International users use the same endpoint or aliyun.com overseas variant."},
            {"label": "SDK Compatibility", "value": "Works with OpenAI Python/Node SDKs after base_url swap. Alibaba also provides a native DashScope SDK with extended features (RAG, Agent orchestration)."},
            {"label": "Function Calling", "value": "Supported on Qwen3.5 series; JSON-schema validated tool calls. Some Qwen models ship without native tool calling — verify model card before integration."},
            {"label": "Streaming", "value": "SSE token streaming by default; QwQ reasoning model streams the chain-of-thought before the final answer (similar to DeepSeek-R1)."},
            {"label": "Context Window", "value": "Up to 128K tokens on Qwen3.5-Max/Plus — sufficient for long documents and extended multi-turn dialog. Qwen-Omni-Turbo supports 1M-token context for multimodal long-context workloads."},
            {"label": "Free Tier", "value": "1M tokens free quota for new users, valid for 90 days — enough to evaluate all Qwen3.5 models before paid commitment."}
        ],
        "itemsZh": [
            {"label": "API 风格", "value": "通过 Bailian（DashScope）平台提供 OpenAI 兼容的 /v1/chat/completions 端点 — 替换 base_url 和 api_key 即可即插即用。"},
            {"label": "Base URL", "value": "https://dashscope.aliyuncs.com/compatible-mode/v1 — 中国大陆直连，无需代理。海外用户使用同一端点或 aliyun.com 海外版。"},
            {"label": "SDK 兼容性", "value": "替换 base_url 后可与 OpenAI 官方 Python/Node SDK 配合使用。阿里同时提供原生 DashScope SDK，支持 RAG、Agent 编排等扩展功能。"},
            {"label": "函数调用", "value": "Qwen3.5 系列支持；JSON schema 验证的工具调用。部分 Qwen 模型无原生工具调用 — 集成前请核验模型说明。"},
            {"label": "流式输出", "value": "默认提供 SSE token 流式；QwQ 推理模型在最终答案前流式输出链式推理过程（与 DeepSeek-R1 类似）。"},
            {"label": "上下文窗口", "value": "Qwen3.5-Max/Plus 支持 128K token — 足以处理长文档与多轮对话。Qwen-Omni-Turbo 支持 1M token 上下文，适用于多模态长上下文负载。"},
            {"label": "免费额度", "value": "新用户 100 万 token 免费额度，90 天有效 — 足以在付费前对所有 Qwen3.5 模型进行评估。"}
        ]
    },
    {
        "title": "🏢 Bailian Platform — Beyond the API",
        "titleZh": "🏢 百炼平台 — 超越 API",
        "type": "text",
        "text": "Alibaba's Bailian (百炼) platform is more than a model API — it is a full-stack enterprise AI development environment. Beyond the OpenAI-compatible /v1/chat/completions endpoint, Bailian offers first-party RAG (document upload → vector store → retrieval-augmented generation), Agent orchestration (visual workflow builder, multi-step pipelines), and an app builder (low-code deployment of AI apps to web/mobile endpoints). All Qwen models are accessible through the same dashboard, with usage analytics, per-app quotas, and team collaboration features.\n\nFor China-based teams, the integration with Alibaba Cloud (ECS, OSS, MaxCompute) is a significant operational advantage — same account, same billing, same VPC, same access control. International users get a similar experience through aliyun.com but with separate pricing and quotas. The platform complexity is the main trade-off: Bailian is heavier than a pure API, and teams that only need model inference may find the platform surface larger than necessary.\n\nFor enterprises already on Alibaba Cloud or building China-market AI products, Bailian is the natural default — the model quality is top-tier, the ecosystem is mature, and the operational integration is unmatched by international providers.",
        "textZh": "阿里百炼（Bailian）平台不仅仅是一个模型 API — 它是一个完整的企业级 AI 开发环境。除 OpenAI 兼容的 /v1/chat/completions 端点外，百炼还提供官方 RAG（文档上传 → 向量库 → 检索增强生成）、Agent 编排（可视化工作流构建、多步骤流水线）以及应用构建器（低代码部署 AI 应用到 Web/移动端点）。所有 Qwen 模型可通过同一控制台访问，配有用量分析、每个应用的配额以及团队协作功能。\n\n对中国团队而言，与阿里云（ECS、OSS、MaxCompute）的集成是显著的运营优势 — 同一账户、同一计费、同一 VPC、同一访问控制。海外用户通过 aliyun.com 获得类似体验，但定价与配额独立。平台复杂度是主要权衡点：百炼比纯 API 更重，仅需模型推理的团队可能觉得平台界面超出实际需要。\n\n对于已在阿里云上或构建中国市场 AI 产品的企业，百炼是天然默认 — 模型质量顶级、生态成熟、运营集成是国际提供商无法匹敌的。"
    },
    {
        "title": "🌐 Regional Availability & Latency",
        "titleZh": "🌐 中国访问与延迟",
        "type": "text",
        "text": "Alibaba Cloud Bailian offers first-party direct access from mainland China, with typical latency from Beijing/Shanghai of 50-150ms for first-token streaming — among the lowest in any provider serving the China market. International access is available through the same endpoint (dashscope.aliyuncs.com) from outside China with slightly higher latency (200-400ms to North America/EU).\n\nThe platform is ICP-licensed and SOC 2 / ISO 27001 certified, with data residency options (China-only, no cross-border transfer). For production workloads serving Chinese users, Bailian is operationally equivalent to a domestic cloud service — no proxy, no aggregator, no cross-border routing required. International teams that need to serve both China and global markets typically use Bailian for China traffic and OpenAI/Anthropic for non-China traffic, routing at the application layer.",
        "textZh": "阿里云百炼提供中国大陆官方直连，北京/上海典型延迟在 50-150ms 首 token 流式响应 — 是中国市场所有提供商中最低之一。海外通过同一端点（dashscope.aliyuncs.com）可访问，延迟略高（北美/欧洲 200-400ms）。\n\n该平台具备 ICP 许可证和 SOC 2 / ISO 27001 认证，提供数据驻留选项（仅中国、无跨境传输）。对面向中国用户的服务生产负载，百炼在运营上等同于国内云服务 — 无需代理、聚合器或跨境路由。需要同时服务中国与全球市场的国际团队，通常在应用层做路由：中国流量用百炼、非中国流量用 OpenAI/Anthropic。"
    }
]

BAIDU_SECTIONS = [
    {
        "title": "💰 Pricing & Plans",
        "titleZh": "💰 价格与方案",
        "type": "table",
        "headers": ["Model", "Input ($/M tokens)", "Output ($/M tokens)", "Best For"],
        "headersZh": ["模型", "输入 ($/百万 token)", "输出 ($/百万 token)", "最佳用途"],
        "rows": [
            ["ERNIE 4.5 Turbo", "$0.003", "$0.009", "Newest flagship, cheap general-purpose"],
            ["ERNIE 4.0 Turbo", "$0.012", "$0.012", "Production-grade quality"],
            ["ERNIE Speed", "Free", "Free", "High-volume lightweight tasks"],
            ["ERNIE Lite", "Free", "Free", "Cost-priority simple chat"],
            ["ERNIE Tiny", "Free", "Free", "Edge / on-device, smallest variant"]
        ],
        "rowsZh": [
            ["ERNIE 4.5 Turbo", "$0.003", "$0.009", "最新旗舰、廉价通用"],
            ["ERNIE 4.0 Turbo", "$0.012", "$0.012", "生产级质量"],
            ["ERNIE Speed", "免费", "免费", "高频轻量任务"],
            ["ERNIE Lite", "免费", "免费", "成本优先的简单对话"],
            ["ERNIE Tiny", "免费", "免费", "边缘/端侧、最小变体"]
        ]
    },
    {
        "title": "🔧 API & Developer Experience",
        "titleZh": "🔧 API 与开发者体验",
        "type": "list",
        "items": [
            {"label": "API Style", "value": "Baidu-specific endpoint at /rpc/2.0/ai_custom/v1/wenxinworkshop — not OpenAI-compatible out of the box. OpenAI-compatible adapter is available via a community wrapper, but the official API surface is Baidu's own design."},
            {"label": "Base URL", "value": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model} — direct from China, no proxy required."},
            {"label": "SDK Compatibility", "value": "Official Baidu Qianfan SDK (Python/Node/Java). Community wrappers provide OpenAI-compatible shims. International teams often need a thin adapter layer."},
            {"label": "Function Calling", "value": "Supported via the dedicated ERNIE Functions model (a specialized variant trained for tool use). Standard ERNIE 4.x models do not expose native tool calling — verify model selection for agentic workloads."},
            {"label": "Streaming", "value": "SSE streaming supported; some ERNIE models occasionally drop the stream on long outputs — implement a reconnect fallback for production reliability."},
            {"label": "Context Window", "value": "Up to 128K tokens on ERNIE 4.5 Turbo / 4.0 Turbo — sufficient for most enterprise document and dialog workloads."},
            {"label": "Free Tier", "value": "ERNIE Speed, Lite, and Tiny are free with monthly quotas of 100K tokens per model — generous enough for evaluation, prototyping, and low-volume production."}
        ],
        "itemsZh": [
            {"label": "API 风格", "value": "百度专属端点 /rpc/2.0/ai_custom/v1/wenxinworkshop — 默认可不是 OpenAI 兼容。社区提供 OpenAI 兼容适配器，但官方 API 界面是百度自有设计。"},
            {"label": "Base URL", "value": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{model} — 中国大陆直连，无需代理。"},
            {"label": "SDK 兼容性", "value": "官方百度千帆 SDK（Python/Node/Java）。社区包装器提供 OpenAI 兼容垫片。国际团队通常需要一层薄适配器。"},
            {"label": "函数调用", "value": "通过专用 ERNIE Functions 模型（针对工具使用训练的专门变体）支持。标准 ERNIE 4.x 模型不暴露原生工具调用 — 智能体工作负载请验证模型选择。"},
            {"label": "流式输出", "value": "支持 SSE 流式；部分 ERNIE 模型在长输出时偶尔会断流 — 生产环境请实现重连回退机制。"},
            {"label": "上下文窗口", "value": "ERNIE 4.5 Turbo / 4.0 Turbo 支持 128K token — 足以应对大多数企业文档与对话负载。"},
            {"label": "免费额度", "value": "ERNIE Speed、Lite、Tiny 免费，每个模型每月 10 万 token — 评估、原型设计与低流量生产足够。"}
        ]
    },
    {
        "title": "🏢 Baidu Ecosystem Integration",
        "titleZh": "🏢 百度生态集成",
        "type": "text",
        "text": "ERNIE's value proposition is its tight integration with the broader Baidu ecosystem — Baidu Search, Baidu Maps, Baidu Cloud, and the Qianfan (千帆) MaaS platform. For China-based applications that already touch any of these surfaces, ERNIE is the lowest-friction option: same authentication, same billing, same access control, same support channels.\n\nThe Qianfan MaaS platform also serves as a unified dashboard for fine-tuning, evaluation, deployment, and monitoring of custom ERNIE variants. Teams can fine-tune ERNIE models on proprietary data, deploy to managed endpoints, and track inference cost and latency in the same console. For enterprises in regulated industries (finance, healthcare, government), the ICP compliance and domestic data residency are mandatory, and ERNIE is among the few frontier-tier models that meet these requirements out of the box.\n\nThe trade-off vs OpenAI/Anthropic is English-language capability, ecosystem tooling maturity, and API design. ERNIE models are tuned for Chinese first; English performance is adequate but not class-leading. The API surface is Baidu-Cloud-style (REST, JSON, OAuth) rather than OpenAI-style, requiring more adaptation work for international SDKs and toolchains.",
        "textZh": "ERNIE 的价值主张在于与更广泛的百度生态深度集成 — 百度搜索、百度地图、百度云以及千帆 MaaS 平台。对已经触及这些场景的中国应用而言，ERNIE 是摩擦最低的选择：同一身份认证、同一计费、同一访问控制、同一支持渠道。\n\n千帆 MaaS 平台同时作为统一控制台，用于 ERNIE 自定义变体的微调、评估、部署与监控。团队可以在同一控制台中基于专有数据微调 ERNIE 模型、部署到托管端点、跟踪推理成本与延迟。对受监管行业（金融、医疗、政府）的企业，ICP 合规与国内数据驻留是强制要求，ERNIE 是少数几个开箱即用满足这些要求的一线模型。\n\n相对 OpenAI/Anthropic 的权衡点是英文能力、生态工具成熟度与 API 设计。ERNIE 模型以中文优先调优；英文能力够用但非业内领先。API 界面是百度云风格（REST、JSON、OAuth）而非 OpenAI 风格，国际 SDK 与工具链需要更多适配工作。"
    },
    {
        "title": "🌐 Regional Availability & Latency",
        "titleZh": "🌐 中国访问与延迟",
        "type": "text",
        "text": "Baidu's Qianfan platform is fully accessible from mainland China with typical latency of 30-100ms for first-token streaming — among the lowest in any commercial LLM API. ICP-licensed, SOC 2 and ISO 27001 certified, with domestic-only data residency by default. There is no proxy, aggregator, or cross-border routing in the path — the request is served entirely within China's network backbone.\n\nInternational access is theoretically supported through Baidu Cloud International, but the practical experience is that the international site is a separate product with different pricing, quotas, and feature parity gaps. For teams serving only China-based users, the domestic Qianfan is the natural default. For teams serving both China and global markets, a split-routing approach (Qianfan for China, OpenAI/Anthropic for global) is the standard pattern, with the API translation layer handled in the application.\n\nERNIE's cost-to-quality ratio at the low end (Speed/Lite/Tiny are free) makes it particularly attractive for high-volume, cost-priority workloads serving Chinese users. For top-quality outputs, ERNIE 4.5 Turbo and 4.0 Turbo remain cheap relative to OpenAI/Anthropic, though the per-token list price is offset by ERNIE's higher token consumption on equivalent tasks — actual cost comparison should be made on a per-task basis, not per-token.",
        "textZh": "百度千帆平台从中国大陆完全可访问，首 token 流式响应典型延迟在 30-100ms — 是任何商业 LLM API 中最低之一。具备 ICP 许可证、SOC 2 与 ISO 27001 认证，默认仅国内数据驻留。请求完全在中国网络骨干网内服务，路径中无代理、聚合器或跨境路由。\n\n理论上通过百度云国际版支持海外访问，但实际体验是国际版是独立产品，定价、配额、功能对等性存在差距。仅服务中国用户的团队，国内千帆是天然默认。服务中国与全球市场的团队，标准方案是分路由（中国流量用千帆、全球流量用 OpenAI/Anthropic），API 转换层在应用中处理。\n\nERNIE 在低端（Speed/Lite/Tiny 免费）的性价比对面向中国用户的高频成本优先负载特别有吸引力。顶级质量输出方面，ERNIE 4.5 Turbo 与 4.0 Turbo 相对 OpenAI/Anthropic 仍然便宜，但单 token 标价被 ERNIE 在等效任务上较高的 token 消耗所抵消 — 实际成本对比应按每任务而非每 token 计算。"
    }
]


def find_entry_span(content: str, target_id: str):
    """Find the byte span of the JSON object for provider with id=target_id.
    Returns (entry_start, entry_close_brace_pos) or raises.
    Search backward from '"id": "X"' to find the entry's opening '{'.
    """
    needle = f'"id": "{target_id}"'
    id_pos = content.find(needle)
    if id_pos < 0:
        raise ValueError(f"id '{target_id}' not found")
    # Find entry's opening { by searching BACKWARDS from id_pos
    entry_open = content.rfind('{\n', 0, id_pos)
    if entry_open < 0:
        entry_open = content.rfind('{', 0, id_pos)
    if entry_open < 0:
        raise ValueError(f"opening brace for '{target_id}' not found")
    # Find matching closing brace via depth counter
    depth = 0
    i = entry_open
    in_string = False
    escape_next = False
    while i < len(content):
        c = content[i]
        if escape_next:
            escape_next = False
        elif c == '\\':
            escape_next = True
        elif c == '"':
            in_string = not in_string
        elif not in_string:
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    return entry_open, i
        i += 1
    raise ValueError(f"matching close brace for '{target_id}' not found")


def build_splice_snippet(field_name: str, value_obj, base_indent: int = 4):
    """Build a JSON snippet ',\\n  "field": <value-indented>' suitable for insertion
    before the entry's closing brace. base_indent = 4 for outer field.
    Avoids the 5-space trap (FM #15 pitfall 4): first line treated specially.
    """
    raw = json.dumps(value_obj, ensure_ascii=False, indent=2)
    lines = raw.split('\n')
    # First line is e.g. '[' — prepend '  "field": '
    field_line = ' ' * base_indent + f'"{field_name}": ' + lines[0]
    # Subsequent lines get base_indent spaces of leading whitespace added
    rest = []
    for ln in lines[1:]:
        rest.append(' ' * base_indent + ln)
    body = '\n'.join([field_line] + rest)
    # Wrap with leading ',\n' to separate from previous field
    return ',\n' + body


def insert_review_sections(content: str, target_id: str, sections) -> str:
    entry_open, entry_close = find_entry_span(content, target_id)
    span = entry_close - entry_open
    if span < 500:
        raise ValueError(
            f"span for '{target_id}' is only {span} bytes — likely found nested object, not entry. Aborting."
        )
    # Build snippet
    snippet = build_splice_snippet('reviewSections', sections, base_indent=4)
    # Insert snippet immediately before the entry's closing brace
    new_content = content[:entry_close] + snippet + '\n  ' + content[entry_close:]
    return new_content


def validate_round_trip(orig_path: str, new_content: str):
    """json.loads the new_content; check no field other than reviewSections changed."""
    new_data = json.loads(new_content)
    orig_data = json.load(open(orig_path))
    if isinstance(new_data, list):
        new_by_id = {p['id']: p for p in new_data}
        orig_by_id = {p['id']: p for p in orig_data}
    else:
        new_by_id = {p['id']: p for p in new_data['providers']}
        orig_by_id = {p['id']: p for p in orig_data['providers']}
    for pid in new_by_id:
        np = new_by_id[pid]
        op = orig_by_id[pid]
        for k in np:
            if k == 'reviewSections':
                continue
            if np.get(k) != op.get(k):
                raise ValueError(f"field '{k}' for {pid} changed! scope violation")
    return new_data


def main():
    with open(PROVIDERS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    targets = [
        ('meta-ai', META_AI_SECTIONS),
        ('aliyun', ALIYUN_SECTIONS),
        ('baidu', BAIDU_SECTIONS),
    ]

    new_content = content
    for tid, sections in targets:
        # Verify this target doesn't already have reviewSections
        entry_open, entry_close = find_entry_span(new_content, tid)
        entry_text = new_content[entry_open:entry_close + 1]
        if '"reviewSections"' in entry_text:
            print(f"SKIP {tid}: already has reviewSections")
            continue
        new_content = insert_review_sections(new_content, tid, sections)
        # Validate JSON after each splice
        try:
            json.loads(new_content)
        except json.JSONDecodeError as e:
            print(f"!! JSON INVALID after splicing {tid}: {e}")
            print(f"   around char {e.pos}: ...{new_content[max(0,e.pos-80):e.pos+80]}...")
            sys.exit(1)
        print(f"OK: {tid} reviewSections spliced ({len(sections)} sections)")

    # Final scope validation
    validate_round_trip(PROVIDERS_PATH, new_content)
    print("OK: scope validation — only reviewSections changed across all entries")

    with open(PROVIDERS_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"WROTE: {PROVIDERS_PATH}")


if __name__ == '__main__':
    main()
