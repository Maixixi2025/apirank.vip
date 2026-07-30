# LiteLLM API 评测 2026

**Slug:** litellm-api-review
**Date:** 2026-07-15
**Category:** Provider Review
**Provider:** LiteLLM (id: `litellm`, aggregator)

## 已核验定价（2026-07-15 实时）

- GitHub stars: 53,599
- Forks: 9,770
- 协议: MIT（开源核心）+ Enterprise 商业版
- 客户: Netflix、Lemonade、Rocket Money
- Docker pulls: 240M+
- 服务请求: 10 亿+
- OSS: 免费、自部署、无限
- Enterprise: 按申请（根据案例研究估算 5 万–50 万美元/年）
- 官网: https://litellm.ai
- 文档: https://docs.litellm.ai

## 简介

LiteLLM 是通过单一 OpenAI 兼容接口路由 100+ LLM Provider 请求的事实开源 AI 网关标准。GitHub 53,599 stars，Y Combinator 投资，在 Netflix 和 Lemonade 生产使用，已成为需要给开发者提供多模型访问同时保持成本归因、速率限制和可观测性的平台团队的标准工具。开源 MIT 协议 Proxy 可免费自部署；Enterprise tier 增加 SSO、审计日志、自定义 SLA 和气隙部署。

## 文章结构

- H1: LiteLLM 2026：开源 AI 网关，一套接口路由 100+ LLM
- H2（8 节）：什么是 LiteLLM / 定价 / Proxy 工作原理 / 成本跟踪 / Fallback / 对比 Portkey/Cloudflare/OpenRouter / 2026 年新特性 / 什么场景不适合
- FAQ: 10 个问答，覆盖用法、定价、免费套餐、国内访问、OpenAI 兼容、对比 Portkey/OpenRouter/Cloudflare、MCP Server、联盟营销
- JSON-LD: Article + BreadcrumbList + FAQPage（3 块解析正常）
- H2 数: 9（TL;DR + 8 H2 + FAQ 节）
- 联盟: FreeModel（侧边栏 CTA，对无联盟计划的 OSS 厂商使用 apirank 默认）

## 与 Portkey/OpenRouter/Cloudflare AI Gateway 的关键差异

- **OSS 优先**: MIT 协议 Proxy，免费，无速率限制
- **成本归因**: 按 key、团队、组织维度的 virtual key
- **MCP Server**: 2026 Q1，将任何模型暴露为 MCP 工具
- **Rust 核心**: 2026 Q2，吞吐量提升 5-10 倍（进行中）
- **Guardrails**: PII 检测、越狱保护、内容审核
- **Fallback + 负载均衡 + 流量镜像**: 生产级路由

## 已写入文件

- `/root/apirank/src/data/providers.json` — 新增 litellm 条目（surgical insertion，84+/1-）
- `/root/apirank/src/pages/tutorials/litellm-api-review.astro` — EN 评测（27,581 字符）
- `/root/apirank/src/pages/zh/tutorials/litellm-api-review.astro` — ZH 评测（19,029 字符，3 层 import 路径）
- `/root/apirank/src/pages/index.astro` — EN 首页卡片插入（claude-tokenizer 之前）
- `/root/apirank/src/pages/zh/index.astro` — ZH 首页卡片插入
- `/root/apirank/src/pages/tutorials/index.astro` — EN 评测列表顶部插入
- `/root/apirank/src/pages/zh/tutorials/index.astro` — ZH 评测列表顶部插入