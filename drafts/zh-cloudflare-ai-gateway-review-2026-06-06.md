---
title: "Cloudflare AI Gateway 评测 2026：跨厂商成本控制 | APIRank"
description: "Cloudflare AI Gateway 完整评测：一个端点调用 100+ 模型，边缘缓存，6/5 新增实时消费限制，Workers AI 免费层。对比 Portkey、LiteLLM、OpenRouter。"
slug: "cloudflare-ai-gateway-review"
provider: "cloudflare-ai-gateway"
published: false
date: "2026-06-06"
type: "review"
---

# Cloudflare AI Gateway 评测 2026：一个端点 100+ 模型，真实消费上限

## 引言：多厂商时代的网关层

到 2026 年，大多数生产级 AI 应用已经不再使用单一厂商。一个典型的 Agent 技术栈可能会调用 OpenAI 做通用推理、Anthropic Claude 做长上下文分析、Google Gemini 做视觉理解，再加一个本地 Llama 部署做路由。这种灵活性很好，但账单也很吓人 —— 而且看清每个团队、每个客户、每个功能模块到底花了多少钱，比选模型本身还难。

Cloudflare AI Gateway 在 2024 年上线时是各大 LLM API 的统一代理。截至 2026 年 6 月，它已经演化成一套正经的成本控制平台：支持 OpenAI、Anthropic、Google、Mistral、Groq、Hugging Face 以及 Cloudflare 自家 Workers AI 共 100+ 模型，内置缓存、实时消费限制（2026 年 6 月 5 日新增）、按 key 限速，以及 Cloudflare 边缘网络上的完整请求/响应日志。它本身不是模型 —— 它坐落在你已经在用的模型前面。

卖点很简单：继续用 OpenAI、Anthropic、Google，但把所有调用都路由到同一个端点，从而获得缓存、可观测性、消费上限、以及某个厂商宕机时的 fallback 链。网关本身 $0 加价（你仍然按上游价格付费），外加一点点 Cloudflare Workers 路由层的费用。

## Cloudflare AI Gateway 实际在做什么

Cloudflare AI Gateway 是一个托管代理 —— 一个同时兼容 OpenAI 和 Anthropic 协议的单一端点，把请求转发到你选择的上游厂商。四个核心能力：

**1. 统一端点（无需重写代码）。** 你会得到一个稳定的 URL，例如 `https://gateway.ai.cloudflare.com/v1/<account_id>/openai/completions`。把现有的 `base_url` 换掉，`openai-python` 调用就能直接工作。Anthropic、Google 以及其他支持的厂商也是一样的模式 —— 每个厂商有自己的路径。

**2. 边缘缓存。** 相同的 prompt 在边缘按可配置 TTL 缓存（默认 5 分钟，最长 1 天）。重复出现的 system prompt + 完全相同的用户问题会直接返回缓存响应，不消耗上游 token。对于 prompt 复用度高的工作负载（RAG 管道、Agent 工具定义、客服模板），缓存命中率可以达到 30-50%。

**3. 实时消费限制（2026 年 6 月 5 日）。** 按 Cloudflare 账号、团队（通过 Cloudflare Access 组）或 API key 设置 USD 预算。预算触顶时，网关返回 HTTP 429 并停止转发请求 —— 没有意外超支，没有手工 token 统计。限制在 60 秒内生效，所以对 Agent 失控场景也管用。

**4. 日志与分析。** 每个请求都记录了 token 数、延迟、模型、缓存命中/未命中、成本（USD）以及错误原因。仪表盘按厂商、模型、时间维度拆分花费。你可以导出到 R2 或发送到外部日志服务。

网关本身没有模型。你仍然需要一个 OpenAI / Anthropic / Google 账号和 API key。网关把你的 key 存在 Cloudflare secrets manager 里，用来转发请求。

## 定价：零加价，只需 Workers

Cloudflare 不对 token 收百分比。你按上游厂商的正常价格付费，外加一点点 Cloudflare Workers 路由层的费用。

| 费用项 | 定价 | 何时计费 |
|------|------|---------|
| 网关加价 | **$0** | 永远不加价 |
| 上游厂商 token | 厂商列表价 | 按 token，与直连一致 |
| Cloudflare Workers 请求 | $0.30 / 百万请求 | 每次通过网关的请求 |
| Cloudflare Workers CPU | $0.02 / 百万 CPU-ms | 路由逻辑很轻（~1-2 ms） |
| Workers 免费额度 | 100,000 请求 / 天 | 小型项目够用 |
| 日志保留 | 7 天免费，超出付费 | 日志在 Cloudflare 仪表盘里 |
| 缓存命中 | **免费**（不消耗上游） | 仅对 TTL 内完全相同的 prompt |

**实际成本举例：** 每月 100 万次 API 调用，平均 500 输入 + 200 输出 token，80% 调用 OpenAI GPT-4o-mini、20% 调用 Anthropic Claude 3.5 Sonnet：

- OpenAI 部分（80 万次 × ~$0.0001 每次）：~$80
- Anthropic 部分（20 万次 × ~$0.0009 每次）：~$180
- Cloudflare Workers：100 万请求 × $0.30/M = $0.30 + ~$0.20 CPU
- **网关额外开销：$0.50/月，AI 账单约 $260/月**

只要边缘缓存能省下 5% 的上游调用，网关就回本了。在典型的 30% 缓存命中率的 RAG 工作负载上，节省的上游成本达到 30%，减去几美分的 Workers 费用。

## 实时消费限制（6 月 5 日更新）

2026 年 6 月 5 日的发布新增了三种消费限制，都在近乎实时强制执行：

| 限制类型 | 范围 | 适用场景 | 强制延迟 |
|--------|------|---------|---------|
| **账号级** | Cloudflare 账号下所有网关流量 | 全局上限 | <60 秒 |
| **团队级** | Cloudflare Access 组 / 团队 | 部门预算 | <60 秒 |
| **按 key** | 通过网关签发的单个 API key | 客户 / 项目隔离 | <60 秒 |

触顶时网关返回 HTTP 429，JSON body 类似 `{"error": "spend_limit_exceeded", "limit_usd": 100, "current_usd": 100.01}`。你的应用可以捕获这个错误并优雅降级（排队、切到更便宜的模型、返回友好提示）。

按 key 限制对 B2B SaaS 来说最有用。每个客户拿到自己的网关 API key，有自己的消费上限，有完整的使用情况可见性。这套模式以前需要自己写中间件 + 计费数据库 + 用量统计 —— Cloudflare 现在把它做成了基础设施。

## 缓存命中率：怎么榨干网关的缓存

默认缓存策略偏保守。要拿到真正的节省：

1. **稳定 prompt 用更长的 TTL。** 如果 system prompt 和用户模板都不变，把 TTL 拉到 24 小时。文档集稳定几个小时的 RAG 工作流就特别适合。
2. **按精确 prompt 哈希缓存。** Cloudflare 按精确 prompt 匹配缓存 —— 多一个空格就是缓存未命中。如果你的应用生成的 prompt 里有时间戳、随机 ID 或非确定性工具结果，那些都不会命中。
3. **对用户定制模板显式设置 `cache_key`。** 对那些因用户不同而变化、但 95% 内容相同的 prompt，用 `cache_key` 参数覆盖默认哈希，复用相似（但不完全相同）prompt 的缓存响应（prompt 前缀和用户输入分开缓存）。
4. **只对非流式调用用缓存。** 流式响应没法缓存，因为流式 chunk 没法干净地重组。如果有大批量非流式批处理场景（摘要、分类、embedding 风格的工作），缓存命中率能到 50%+。

一个实用模式：把所有"意图分类"和"守门员"调用都走网关，TTL 设 1 小时。这些调用通常都很短、频繁重复、答案基本不变。

## 模型支持：100+ 且在增长

Cloudflare AI Gateway 是代理，不是模型。模型列表是它能路由到的所有厂商的并集。截至 2026 年 6 月：

| 厂商 | 代表模型 | 适用场景 |
|------|---------|---------|
| **OpenAI** | gpt-4o, gpt-4o-mini, o1, o3-mini, gpt-3.5-turbo | 通用推理、工具调用 |
| **Anthropic** | claude-3-5-sonnet, claude-3-haiku, claude-3-opus | 长上下文、代码、分析 |
| **Google** | gemini-1.5-pro, gemini-1.5-flash, gemini-2.0-flash | 视觉、长上下文（1M-2M token） |
| **Mistral** | mistral-large, mistral-small, mixtral-8x7b | 欧洲备选、函数调用 |
| **Groq** | llama-3.1-70b, llama-3.1-8b, mixtral | Groq LPU 加速 |
| **Hugging Face** | 任何推理端点 | 自定义 / 开源模型 |
| **Workers AI** | llama, qwen, deepseek-r1-distill | Cloudflare 边缘上免费推理 |

Workers AI 模型是特殊情况：当你在网关上路由到 Workers AI 模型时，推理跑在 Cloudflare 自己的网络上，模型本身免费（你只付 Workers 请求 + CPU 费用）。这对于成本敏感的批处理场景、小模型（Llama 3.1 8B、Qwen 1.5B、DeepSeek R1 Distill）很有用。

## 跟 Portkey、LiteLLM、OpenRouter 的对比

| 维度 | Cloudflare AI Gateway | Portkey | LiteLLM | OpenRouter |
|------|----------------------|---------|---------|------------|
| **部署方式** | 托管（Cloudflare） | 托管 / 自托管 | 自托管（开源） | 托管 |
| **定价模式** | 零加价 + Workers | 免费层 + 用量费 | 免费（你付基础设施） | Token 加价 |
| **边缘缓存** | ✅ 内置 | ✅ 内置 | ❌ 没有（自己加 Redis） | ❌ 没有 |
| **实时消费限制** | ✅ 按 key/团队（6/5） | ✅ 按 key/团队 | ⚠️ 自己搭建 | ⚠️ 仅按账号 |
| **日志保留** | 7 天免费 | 30 天免费 | 自己管理 | 不限 |
| **自托管选项** | ❌ | ✅ | ✅ | ❌ |
| **模型数** | 100+（上游并集） | 200+ | 100+ | 60+ |
| **OpenAI 兼容** | ✅ | ✅ | ✅ | ✅ |
| **Anthropic 兼容** | ✅ | ✅ | ✅ | ⚠️ 翻译层 |
| **延迟开销** | 5-20 ms（边缘） | 30-80 ms | 5-15 ms | 50-200 ms |
| **每 1M 路由调用** | ~$0.30 | 免费层之后另算 | 基础设施成本 | 按加价浮动 |

**选 Cloudflare AI Gateway 的场景：** 想要零网关加价、已经在用 Cloudflare 的 DNS / Workers / R2、需要边缘缓存复用 prompt、想要免运维的托管基础设施。

**选 Portkey 的场景：** 需要自托管选项、更高级的可观测性功能、或者更广的模型目录。

**选 LiteLLM 的场景：** 想要完全控制、已经有 K8s 或服务器可以跑、不想被厂商锁定。

**选 OpenRouter 的场景：** 想要一张账单搞定多种模型、不需要单独开上游账号，特别是想做没有直签合同的模型之间的成本优化路由。

## Fallback 链和多厂商可靠性

一个容易被忽略的能力：网关可以配置 fallback 链。如果你的主厂商返回 429（限流）或 5xx（服务器错误），网关会自动重试链上的下一个模型。典型配置：

```
Primary:   OpenAI gpt-4o-mini（便宜的默认）
Fallback 1: Anthropic claude-3-haiku（质量相近，厂商不同）
Fallback 2: Workers AI llama-3.1-8b（免费，最后兜底）
```

如果 OpenAI 在限流你，网关透明地切到 Anthropic。如果两个都挂了，Workers AI 顶上 —— 完全免费，质量略低，但应用保持在线。这跟 Vercel AI SDK 和 OpenAI "reliability layer" 教程里教的模式一样，但做进了代理层。

## 中国访问：一个真实存在的限制

Cloudflare 的网络在中国大陆基本被墙或严格限制。网关端点（`gateway.ai.cloudflare.com`）没有稳定代理就不太能访问。仪表盘（`dash.cloudflare.com`）也一样。

对国内开发者来说，替代的聚合模式是用国内友好的代理。比如 [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) 就是一个中国直连的 OpenAI 兼容聚合器，帮你处理上游路由，包括 DeepSeek 和 Qwen。这是相反的取舍 —— 没有 Cloudflare 生态集成，但不需要代理。

对需要两者兼顾的团队：把生产流量走 Cloudflare AI Gateway（托管、缓存、可观测），用国内聚合器服务中国用户或中国预发环境。

## 适用场景：什么时候该用 Cloudflare AI Gateway

| 场景 | 推荐度 | 原因 |
|------|-------|------|
| 多厂商生产级应用 | ✅ 最佳 | 单一端点、fallback 链、可观测性 |
| 成本受控的 B2B SaaS | ✅ 最佳 | 按客户 API key + 按 key 消费限制 |
| prompt 稳定的 RAG 管道 | ✅ 最佳 | 边缘缓存砍掉 30-50% 上游成本 |
| 大批量批处理 | ✅ 最佳 | 缓存 + Workers AI 免费层 |
| 单模型单用户应用 | ⚠️ 杀鸡用牛刀 | 直接调上游更简单 |
| 实时流式 Agent | ⚠️ 缓存不命中 | 流式没法享受边缘缓存 |
| 中国直连 | ❌ 不行 | Cloudflare 被墙，用国内聚合器 |
| 自托管 / 私有部署要求 | ❌ 不行 | 用 Portkey 或 LiteLLM |

## 优缺点

**优点：**

- ✅ 零网关加价 —— 只付上游列表价
- ✅ 边缘缓存让 prompt 复用成本下降 30-50%
- ✅ 按 key / 团队 / 账号的实时消费限制（6/5 发布）
- ✅ 100+ 模型走同一个 OpenAI/Anthropic 兼容端点
- ✅ Cloudflare 可靠性 + 边缘网络（路由开销 20 ms 以内）
- ✅ Workers AI 模型免费，适合成本敏感的工作负载
- ✅ 内置日志，7 天免费保留，可导出到 R2
- ✅ Fallback 链提升多厂商可靠性

**缺点：**

- ⚠️ 不是模型 —— 你仍然需要上游账号和 API key
- ⚠️ 中国访问需要稳定代理
- ⚠️ 流式响应无法缓存
- ⚠️ 默认缓存 TTL 偏保守，需要自己调优
- ⚠️ Workers 用量单独计费（金额很小但确实存在）
- ⚠️ 日志只免费 7 天，更长保留需要付费

## FAQ

**Q：Cloudflare AI Gateway 是模型厂商，还是只是代理？**

A：是代理。你自己带 OpenAI、Anthropic、Google 等上游 API key。网关把请求路由到这些厂商，并加上缓存、可观测性、消费限制。Workers AI 模型是例外 —— 那些在 Cloudflare 网络上免费 —— 但对主流厂商，你仍然需要自己的账号。

**Q：跟直接调 OpenAI 相比，Cloudflare AI Gateway 贵多少？**

A：模型本身，$0 额外 —— 你按 OpenAI / Anthropic / Google 正常价付钱。唯一增加的是 Cloudflare Workers 费用：每百万路由请求约 $0.30，外加典型工作负载几美元的 CPU 时间。$1,000/月的 AI 账单上，网关加的成本大约 $1-3。边缘缓存和按 key 消费限制带来的节省几乎总是超过这个开销。

**Q：消费限制触顶了会怎样？**

A：网关返回 HTTP 429，JSON body 里说明触发了消费限制。你的应用代码可以捕获这个错误，决定怎么做 —— 给用户返回错误、把请求排队、或者切到更便宜的模型。限制在实际消费发生后的 60 秒内强制执行，所以是近乎实时的。

**Q：能不能直接用 OpenAI Python SDK 和 Anthropic SDK？**

A：可以。把 `base_url` 设成网关 URL，把你从网关拿到的 API key 传进去（而不是上游厂商的 key）。SDK 调用代码不用改。Anthropic SDK、Google GenAI SDK 以及大多数 OpenAI 兼容客户端都是同样套路。

**Q：网关支持流式响应吗？**

A：支持 —— 网关会透传 SSE 流。但流式响应不能缓存（流式 chunk 没法干净重组）。对大批量非流式批处理工作负载，缓存效果很好；对实时聊天 / Agent 循环，能拿到路由和可观测性，但拿不到缓存节省。

**Q：有自托管版本吗？**

A：没有。Cloudflare AI Gateway 是 Cloudflare 的托管产品。需要自托管的话，备选是 Portkey（自托管或托管）和 LiteLLM（开源、自托管）。

**Q：跟 OpenRouter 怎么比？**

A：OpenRouter 也是托管聚合器，但它把上游加价打包进去，用自己的定价转售 token。Cloudflare AI Gateway 是真正的透传代理：零加价，你自带上游账号，网关只加缓存、限制和可观测性。OpenRouter 更简单（一张账单、不用开上游账号）；Cloudflare 规模上去后更便宜（零加价、缓存节省更多）。

**Q：6 月 5 日的消费限制功能免费吗？**

A：免费。实时消费限制包含在网关里，不另收费。在 Cloudflare 仪表盘或通过 API 设限制，自动强制执行。

## 结论：多厂商 AI 应用的成本控制层

Cloudflare AI Gateway 不是模型，也不是 OpenAI / Anthropic / Google 的替代品。它是坐落在这些厂商前面的路由和可观测性层，加上缓存、消费限制和日志，附带近乎零的开销。任何在规模化跑多厂商 AI 应用的团队，光是为了边缘缓存都应该评估一下网关 —— 30-50% 的上游成本减少很难忽略。

2026 年 6 月 5 日发布的实时消费限制补上了缺失的一块。在此之前，你能记录和观察花费，但没法在不自己写中间件的情况下设上限。现在，按 key 限制让 B2B SaaS 拿到一个开箱即用的方式给客户或部门计费 AI 用量，而不需要自己搭计量基础设施。

如果你在跑多厂商 AI 应用，把 Cloudflare AI Gateway 作为透传代理先接上。你会拿到缓存节省、可观测性白嫖、在需要的那一刻加上按 key 消费限制的选项。单模型或单厂商的场景，网关属于杀鸡用牛刀 —— 直接调厂商就好。需要中国直连多厂商访问的话，类似的角色由国内聚合器（比如 [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220)）扮演，它们把同样的多模型路由跟中国网络访问结合起来。

---

## 延伸阅读

- [Cloudflare AI Gateway 官方文档](https://developers.cloudflare.com/ai-gateway/)
- [Cloudflare 博客：AI Gateway 消费限制（2026/6/5）](https://blog.cloudflare.com/ai-gateway-spend-limits/)
- [Cloudflare AI Gateway 定价](https://developers.cloudflare.com/ai-gateway/pricing/)
- [Workers AI 模型目录](https://developers.cloudflare.com/workers-ai/models/)
- [Portkey 网关（可自托管备选）](https://portkey.ai/)
- [LiteLLM（开源自托管备选）](https://github.com/BerriAI/litellm)
- [FreeModel（中国直连聚合器，给需要国内访问的用户）](https://freemodel.dev/invite/FRE-7a3b6220)
