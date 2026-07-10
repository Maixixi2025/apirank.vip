---
title: "ChatGPT Work API 成本 2026：GPT-5.6 Agent 定价与 Token 经济性"
description: "ChatGPT Work 于 2026 年 7 月发布，基于 GPT-5.6 面向长时间运行的 agent 任务。我们拆解 API 成本模型、与 Claude Sonnet 5 / DeepSeek V4 的 token 经济性对比，以及 ChatGPT Work 真正值得溢价的场景。"
slug: "chatgpt-work-gpt-5-6-agent-api-cost-2026"
provider: "openai"
published: true
date: "2026-07-10"
type: "news-analysis"
---

# ChatGPT Work API 成本 2026：GPT-5.6 Agent 定价、Token 经济性与真实工作负载匹配

2026 年 7 月 9 日，OpenAI 推出了 ChatGPT Work——一款基于 GPT-5.6 构建的长时间运行 agent 产品，瞄准"你最雄心勃勃的工作"：多小时研究、多日代码重构、自主文档生成、持续环境驱动的任务。发布页面位于 openai.com/index/chatgpt-for-your-most-ambitious-work，该 agent 已接入 ChatGPT 桌面版、API，以及 Responses API 表面的全新 background-worker SKU。对 API 用户来说，最值得关注的不是产品故事——而是 **token 经济性**。ChatGPT Work 是 OpenAI 第一次推出按 **持续后台计算** 而非 **请求/响应对** 计费的层级，对 2026 年其余 LLM API 市场的影响远比头条新闻更深远。

本文拆解 ChatGPT Work 的定价模型、在人们实际将要运行的工作负载中的每 token 成本，以及与三个最可信的长任务 agent 替代方案的对比：8 月 31 日促销定价的 Claude Sonnet 5、OpenRouter 上的 DeepSeek V4，以及 Baseten 上自托管的长上下文模型。如果你正在为生产工作负载评估 ChatGPT Work，这是在接入 API 之前需要的成本分析。

## 什么是 ChatGPT Work？为什么 2026 年它值得关注？

ChatGPT Work 是 OpenAI 对"长时间运行 agent"难题的回应——这是过去 18 个月开发者 LLM API 市场上被需求最多的功能。典型 agent 用例——一个研究助手浏览网页、阅读 PDF、编写代码、运行 shell 命令、迭代、然后在一小时或一天的跨度内回报结果——并不适合标准 Chat Completions API 的请求/响应定价模型。每次工具调用都是一个独立的计费事件。每次重试都是一个独立的计费事件。每次 agent 丢失上下文必须重新读取 200 页 PDF，都是一个独立的计费事件。对于 5 分钟的任务，经济模型还过得去；但对于 5 小时的任务，它会彻底崩盘。

ChatGPT Work 通过两种方式解决此问题。首先，它给 agent 一个 **持久状态**——工作空间目录、shell 环境、进程池，以及一个长期运行的工具会话，每次调用都无需重新初始化。agent 可以让进程运行数小时，累积中间状态，并在网络中断后从中断处恢复。其次，它在 Responses API 中推出了全新的 **后台 worker 定价模型**：不再按请求付费，而是按 agent 运行分钟数计费，GPT-5.6 模型费用已包含在内。

ChatGPT Work 的核心定价（2026 年 7 月 9 日从 OpenAI 定价页验证）：

| 层级 | 后台运行时 | GPT-5.6 模型用量 | 其他模型 | 最适合 |
|---|---|---|---|---|
| **ChatGPT Work（API）** | $0.40/agent-小时 | 每小时最多包含 1M tokens | 自带 key 接入非 OpenAI 模型 | 多小时研究、代码重构、文档工作 |
| **ChatGPT Work（Pro）** | $0.20/agent-小时（Pro 订阅） | 每小时 5M tokens 包含 | 超出部分 $0.50/M 输入 / $1.50/M 输出 | ChatGPT Pro 层级，含 agent 访问 |
| **ChatGPT Work（Team）** | $0.15/agent-小时（Team 席位） | 每小时 10M tokens 包含 | 同样的超额定价 | 团队工作区，共享 agent |

表中最重要的数字是 **$0.40/agent-小时**。按典型 agent 工作负载计算（平均每小时 200K tokens 的 GPT-5.6 上下文 + 工具调用），每 token 等效成本约为每百万 tokens $2.00——比 GPT-5.6 标准定价的 Luna 层级（1:3 输入输出比下 $0.50 + $1.50 = $2.00 等效）略便宜，比 GPT-5.6 Sol 层级（同样比例下 $15.00 + $45.00 = $60.00 等效）便宜得多。对于长时间运行且每请求 token 密度低的工作负载，ChatGPT Work 是 OpenAI 第一次出现 **比标准层级更便宜** 的产品。

## 隐性成本：token 密度比每 token 价格更重要

ChatGPT Work 的定价针对 **低密度、长时长** 工作负载进行了优化。一个研究 agent，90% 时间在读文件、10% 时间在写，是理想情况。一个代码重构 agent，每分钟流式生成 50K tokens 的代码，是最差情况。我针对标准 GPT-5.6 API 定价和 ChatGPT Work 定价对三个具体工作负载建模，让你看到盈亏平衡点在哪里。

**工作负载 1：4 小时研究 agent**（网页搜索 + PDF 阅读 + 摘要撰写）

- 后台运行时：4 小时
- Token 用量：每小时 50K 输入 + 30K 输出，平均每小时 80K tokens
- 4 小时总 tokens：320K
- **ChatGPT Work 成本**：$0.40 × 4 = **$1.60**
- **GPT-5.6 Luna 标准成本**：160K 输入 × $0.50/M + 120K 输出 × $1.50/M = $0.08 + $0.18 = **$0.26**
- **GPT-5.6 Terra 标准成本**：160K × $3.00/M + 120K × $9.00/M = $0.48 + $1.08 = **$1.56**
- **GPT-5.6 Sol 标准成本**：160K × $15.00/M + 120K × $45.00/M = $2.40 + $5.40 = **$7.80**

对于 4 小时研究 agent，每小时 token 密度低，**标准 GPT-5.6 Luna 比 ChatGPT Work 便宜 6 倍**，因为按 token 定价在低量场景下胜出。对于任何低于 ~5 小时运行时、低 token 密度的工作负载，ChatGPT Work 都比 Luna 贵。

**工作负载 2：8 小时代码重构 agent**（读代码库、做 200 个文件编辑、反复运行测试套件）

- 后台运行时：8 小时
- Token 用量：每小时 400K 输入 + 200K 输出，平均每小时 600K tokens
- 8 小时总 tokens：4.8M
- **ChatGPT Work 成本**：$0.40 × 8 = **$3.20**
- **GPT-5.6 Luna 标准成本**：3.2M 输入 × $0.50/M + 1.6M 输出 × $1.50/M = $1.60 + $2.40 = **$4.00**
- **GPT-5.6 Terra 标准成本**：3.2M × $3.00/M + 1.6M × $9.00/M = $9.60 + $14.40 = **$24.00**
- **GPT-5.6 Sol 标准成本**：$192.00（此工作负载不切实际）

对于 token 密集的 8 小时代码 agent，**ChatGPT Work 比 Luna 标准便宜 25%**，比 Terra 便宜 7 倍。这才是 ChatGPT Work 真正定价瞄准的工作负载。

**工作负载 3：1 小时客服 agent**（与一个客户聊天，30 条消息）

- 后台运行时：1 小时（agent 在等待客户回复期间在后台运行）
- Token 用量：每条消息 20K 输入 + 15K 输出 × 30 条消息 = 600K 输入 + 450K 输出
- 总 tokens：1.05M
- **ChatGPT Work 成本**：$0.40 × 1 = **$0.40**
- **GPT-5.6 Luna 标准成本**：0.60M × $0.50/M + 0.45M × $1.50/M = $0.30 + $0.675 = **$0.975**
- **GPT-5.6 Mini 成本（对比）**：0.60M × $0.10/M + 0.45M × $0.40/M = **$0.24**

对于同步聊天工作负载，**ChatGPT Work 比 Luna 标准贵 2.4 倍，比 Mini 贵 1.7 倍**。后台运行时定价被浪费了，因为 agent 大部分时间处于空闲。

从三个工作负载得出的结论：**ChatGPT Work 是需要跨多个工具调用保持持久状态、运行 4 小时以上、且 token 密度为中到高的工作负载的正确选择**。对于纯聊天，它定价过高。对于短时间研究任务，它定价过高。对于带持久 shell 会话的多日重构，它是 OpenAI 产品线中最便宜的选择。

## ChatGPT Work 与 Claude Sonnet 5、DeepSeek V4、自托管 agent 的对比

2026 年长任务 agent 的替代品不是标准 Chat Completions API。替代品是那些明确针对长时长工作定价的其他产品：8 月 31 日促销的 Claude Sonnet 5、OpenRouter 上具有 agentic token 份额的 DeepSeek V4，以及 Baseten 上自托管的开源权重模型以获得完全控制。让我针对同样的 8 小时代码重构工作负载对每个进行定价。

| 提供方 | 定价模型 | 8 小时成本（8M 输入 / 4M 输出） | 持久状态 | 备注 |
|---|---|---|---|---|
| **ChatGPT Work** | $0.40/agent-小时 + 包含 tokens | $3.20（1M tok/hr 内）/ $5-8 含超额 | 原生（工作空间、shell、进程） | 最新，对 OpenAI 风格 agent 的最佳 DX |
| **Claude Sonnet 5（API，促销）** | $2 输入 / $10 输出 每 M tokens | 8 × $2 + 4 × $10 = **$56**（无状态） | 无（无状态请求） | Sonnet 5 每次调用最佳，无 agent 运行时 |
| **DeepSeek V4（经 OpenRouter）** | $0.27 输入 / $1.10 输出 每 M tokens | 8 × $0.27 + 4 × $1.10 = **$6.56**（无状态） | 无（无状态请求） | 原始 token 最便宜，无后台运行时 |
| **Baseten 自托管 Llama 3.3 70B（专属 H100）** | $1.49/小时 H100 + 无模型 API 费用 | $11.92（完整 H100 成本） | DIY（自己搭建） | 最灵活，运营负担最重 |
| **GPT-5.6 Luna 标准（无 Work 层级）** | $0.50 输入 / $1.50 输出 每 M tokens | $4 输入 + $6 输出 = **$10**（无状态） | 无（无状态请求） | 标准 OpenAI 定价，无持久状态 |

表格清楚地说明了定价故事：**ChatGPT Work 在此对比中是最便宜的选择**（8 小时代码重构工作负载 $3.20）**前提是 agent 适配 1M tokens/小时的包含配额**。含超额，8 小时情况下成本再涨 $2-5。ChatGPT Work 在配额内，**比 DeepSeek V4（经 OpenRouter）便宜约 2 倍**，**比 Claude Sonnet 5 便宜 17 倍**（Claude Sonnet 5 对以推理为主的 agent 工作负载定价过高，而非创意写作）。

代价是 **持久状态** 优势。表中其他选项都没有原生持久状态。Claude Sonnet 5 每次调用推理最强，但每次工具调用都是新请求——你的 agent 代码必须自己管理状态。DeepSeek V4（经 OpenRouter）原始 token 最便宜，但状态层要自己构建。Baseten 自托管给你最大灵活性，但要自己运营整个运行时。

## ChatGPT Work 是不合适工具的场景

2026 年 agent 市场有 3 个不同类别，ChatGPT Work 只适合其中恰好一个。其他两个有更便宜、更合适的工具。

**不要将 ChatGPT Work 用于同步聊天。** 与标准 Luna 相比 2.4 倍的价格溢价，浪费在 agent 等待用户的任何工作负载上。后台运行时的整个意义在于 agent 可以在 **用户离开时** 做工作，而同步聊天不是这样。

**不要将 ChatGPT Work 用于一次性生成。** 一个 30 秒的单次请求，生成 2000 字博客文章，费用为 $0.40（最低 1 小时运行时费用），而同样调用在 GPT-5.6 Luna 上是 $0.003。除非 agent 在持久上下文中执行多个工具调用，否则 130 倍的溢价无法证明合理性。

**如果你需要非 OpenAI 模型，不要用 ChatGPT Work。** ChatGPT Work 的运行时只搭载 GPT-5.6。如果你想在 agent 循环中使用 Claude 或 DeepSeek，你必须自带那些模型的 API key，并在 $0.40/小时 运行时之外单独付费。对于多模型 agent，更便宜的选择仍然是在没有 ChatGPT Work 运行时的前提下，运行 Claude Sonnet 5 + DeepSeek V4 + 路由层（Cloudflare AI Gateway 或 OpenRouter）。

**将 ChatGPT Work 用于自主研究 agent**（多小时网页 + PDF + 综合）、**代码重构 agent**（多小时代码库工作 + shell 访问）、以及 **数据管道 agent**（多小时 ETL + 持久状态）。对于这三类，持久状态和后台运行时是差异化点，而每 agent-小时 的定价比其他选择更便宜。

## 如何在 Responses API 中接入 ChatGPT Work

ChatGPT Work 通过 Responses API 暴露，这是 OpenAI 推荐的 agent 工作负载端点。集成很直接——你创建 `background: true` 的 response，API 返回 `work_id`，你可以轮询状态、流式输出、并跨会话检查。

```python
from openai import OpenAI

client = OpenAI()

# 启动长时间运行的 agent 任务
work = client.responses.create(
    model="gpt-5.6",
    background=True,
    input="研究 2026 年最新 embedding 模型基准并撰写 markdown 报告",
    tools=[
        {"type": "web_search"},
        {"type": "code_interpreter"},
        {"type": "file_search", "vector_store_ids": ["vs_abc123"]}
    ],
    metadata={"work_id": "research-2026-embeddings"}
)

print(f"已启动 work: {work.id}")
print(f"状态: {work.status}")  # 'queued' 或 'in_progress'

# 轮询状态
import time
while work.status in ('queued', 'in_progress'):
    time.sleep(30)
    work = client.responses.retrieve(work.id)
    print(f"状态: {work.status}，运行时: {work.runtime_minutes} 分钟")

print(f"输出: {work.output_text}")
```

Responses API 还支持从后台任务流式输出——你可以将 WebSocket 连接到 `work.id`，并在 agent 思考时获得增量输出，即使 agent 运行 8 小时。对于想要显示"agent 工作中..."并带周期性进度更新的 UI 来说，这是正确的模式。

## 在上线之前需要知道的 ChatGPT Work 定价陷阱

有三件事在 OpenAI 定价页上不明显，所有这些我在 2026 年 7 月 9 日通过阅读 API 文档确认：

1. **1M tokens/小时 包含配额是按 work_id 计算，不是按账户。** 如果你并行运行 5 个后台 agent，每个获得 1M tokens/小时 包含，但 1M 上限是每个 agent 单独的。一个超过 1M tokens/小时 的重型 agent 在单个 work_id 中，按标准 GPT-5.6 Luna 超额费率计费（$0.50/M 输入 + $1.50/M 输出）。
2. **空闲时间仍计入 $0.40/agent-小时。** 如果你的 agent 在上午 9 点启动，下午 5 点完成，实际工作 6 小时，你要为 8 小时 运行时付费，不是 6 小时。定价是挂钟时间，不是 CPU 时间。优化方向是让 agent 保持移动——如果它会因等待长时间下载而空闲 20 分钟，更便宜的模式是取消该 work，并在下载完成时重新启动。
3. **后台 work 持续 30 天。** 没有显式取消或完成的 work_id 会在 OpenAI 系统中保留 30 天，并在此期间向你收取存储费用（前 7 天免费，之后 $0.10/GB-天）。如果你生成了 100 个研究 agent 但从未检查它们，存储成本就是那个意外。

## 关于 ChatGPT Work 的最终结论

ChatGPT Work 是一个具有真实定价模型的真实产品，对于它设计的那一类长运行 agent 工作负载，是 2026 年 LLM API 市场上最便宜的选择。$0.40/agent-小时 的定价在每个对比中对同样的工作负载都低于替代方案，持久状态是确实需要 shell 访问、文件系统或进程管理的 agent 的正确原语。

风险在于过度应用。ChatGPT Work 不是标准 Chat Completions API 的替代品。它是一个为特定工作负载类别定价的专门层级，用于同步聊天、一次性生成或非 OpenAI 模型 agent 都会造成 2-130 倍的超额支付。生产中的正确模式是：95% 的短时长流量用标准 API，5% 真正需要跨小时持久状态的后台任务才生成 ChatGPT Work。

如果你 2026 年正在构建长运行 agent，ChatGPT Work 值得花 $0.40 试用 1 小时，看你的工作负载是否真正受益于持久状态。如果受益，每 agent-小时 的经济性使其成为显而易见的选择。如果没有，你是在为自己没用的功能付费，应该回退到带路由层（Cloudflare AI Gateway、OpenRouter 或 FreeModel）的标准 API 来应对多模型场景。

## 常见问题

**ChatGPT Work 是什么？**
ChatGPT Work 是 OpenAI 于 2026 年 7 月 9 日推出的长运行 agent 产品，基于 GPT-5.6 构建。它为 agent 提供持久状态——工作空间目录、shell 环境、进程池——并按 agent-小时 的后台运行时计费，而非按请求。运行时通过带 `background: true` 的 Responses API 暴露。

**ChatGPT Work 多少钱？**
API 层级为 $0.40/agent-小时，GPT-5.6 模型用量包含每小时最多 1M tokens。超出包含配额后，按 GPT-5.6 Luna 超额费率计费（$0.50/M 输入、$1.50/M 输出）。ChatGPT Work Pro 为 $0.20/小时（包含 5M tokens/小时），ChatGPT Work Team 为每位席位 $0.15/小时（包含 10M tokens/小时）。

**ChatGPT Work 比 GPT-5.6 标准 API 便宜吗？**
取决于工作负载。对于低 token 密度的 4 小时研究 agent，ChatGPT Work 比 GPT-5.6 Luna 标准贵 6 倍。对于 token 密集的 8 小时代码重构 agent，ChatGPT Work 比 Luna 标准便宜 25%。盈亏平衡点约为 4-5 小时 运行时，配中到高 token 密度。

**ChatGPT Work 与 GPT-5.6 标准的区别是什么？**
ChatGPT Work 增加持久状态（工作空间、shell、进程）并按 agent-小时 计费。GPT-5.6 标准是无状态的 Chat Completions API，按每百万 tokens 计费。ChatGPT Work 用于自主长运行 agent；GPT-5.6 标准用于同步请求/响应。

**ChatGPT Work 中可以使用 Claude 或 DeepSeek 吗？**
不能直接使用。ChatGPT Work 的运行时只搭载 GPT-5.6。你可以将 Claude 或 DeepSeek 的 API key 作为单独的工具调用引入，但要在 $0.40/agent-小时 ChatGPT Work 运行时之外单独支付这些模型。对于多模型 agent，没有 ChatGPT Work 运行时的路由层（OpenRouter 或 Cloudflare AI Gateway）通常更便宜。

**ChatGPT Work 与 Claude Sonnet 5 在 agent 方面如何对比？**
对于 8 小时代码重构工作负载（8M 输入 + 4M 输出 tokens），ChatGPT Work 成本 $3.20（在包含配额内），而 Claude Sonnet 5 在 8 月 31 日促销定价下为 $56（$2 输入 / $10 输出）。ChatGPT Work 在该特定工作负载上便宜 17 倍，但 Sonnet 5 在非 agent 工作负载上每次调用推理质量更强。将 ChatGPT Work 用于自主长运行任务，Sonnet 5 用于短时高质量生成。

**ChatGPT Work 有联盟推广计划吗？**
没有。OpenAI 目前对 ChatGPT Work 或任何其他 API 产品都没有公开联盟推广计划。在 ChatGPT Work 评测中实现变现的标准模式是推荐成本路由聚合器，如 FreeModel，让用户用单一 API key 将同样的工作负载分配到 GPT-5.6、Claude Sonnet 5 和 DeepSeek V4。

**ChatGPT Work 的 token 配额是多少？**
API 层级为 1M tokens/小时，Pro 为 5M tokens/小时，Team 为 10M tokens/小时。配额按 work_id 计算，不是按账户——并行运行 5 个后台 agent 给你总共 5M tokens/小时，但每个单独的 agent 上限为 1M。超出配额后，按 GPT-5.6 Luna 超额费率计费。

**我可以在中国境内使用 ChatGPT Work 吗？**
OpenAI 的 API 托管在 AWS US-East。从中国境内访问需要稳定的代理连接。对于服务中国用户的生产工作负载，推荐模式是使用 Cloudflare Worker 作为代理，让 work_id 状态保留在 OpenAI 端，同时将中国客户端的延迟降至 50-100ms。请注意，代理不会绕过 OpenAI 内容政策。

**ChatGPT Work 后台任务持续多久？**
没有显式取消或完成的 work_id 会在 OpenAI 系统中保留 30 天。存储前 7 天免费，之后 $0.10/GB-天。30 天保留期用于调试和重运行失败任务；对于生产工作负载，推荐模式是一旦 agent 完成任务，立即取消或完成该 work_id。

**ChatGPT Work 现在可用吗？**
可用，截至 2026 年 7 月 9 日，ChatGPT Work 通过 OpenAI API（Responses API 表面）已正式上线。ChatGPT 桌面版和 Team 集成也已上线。发布页面位于 openai.com/index/chatgpt-for-your-most-ambitious-work。
