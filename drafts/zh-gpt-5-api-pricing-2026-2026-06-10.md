---
title: "GPT-5 API 定价 2026：5.5/5.4/Mini 怎么选最划算"
description: "GPT-5 API 定价 2026 拆解：GPT-5.5 旗舰 $5/M 输入、GPT-5.4 $2.50/M、GPT-5 Mini $0.15/M，Batch 半价、cached input 缓存档位，配合真实 token 成本对比。"
slug: "gpt-5-api-pricing-2026"
provider: "openai"
published: false
date: "2026-06-10"
type: "comparison"
---

# GPT-5 API 定价 2026：5.5/5.4/Mini 怎么选最划算

## 为什么这件事重要

GPT-5 系列在 2026 年已经稳定成三档定价，档位之间的价差大到选错就是 20 倍的成本浪费。GPT-5.5 是新旗舰 $5/百万输入 token，GPT-5.4 是中端 $2.50/百万，GPT-5 Mini 是预算档 $0.15/百万。输出侧的价差更夸张：分别是 $15/M、$10/M 和 $0.60/M。如果你在高并发工作流上跑错了模型，等于在烧钱。

2026 年定价故事不只看头牌单价，还有两个复合杠杆：Batch API（所有价格 5 折，异步交付）和 cached input 折扣（命中 5 分钟或 1 小时缓存的 prompt token 半价）。对于重复性的工作流——反复读同样 system prompt 的 agent、反复送同样长文档的 RAG 系统、反复解析同样代码仓库的 code review 工具——cached input 杠杆决定了产品是赚钱还是烧钱。

这篇定价手册就是我们当初选模型时希望存在的那页：三个档位的真实 per-token 单价、Batch 和缓存的数学、三档预算（$100 / $1000 / $10000）的具体 token 算账，以及每个工作流对应哪个模型的决策树。文末还覆盖了国内访问角度（GPT-5 国内不直连，OpenAI 兼容聚合 [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) 可以从国内直连的端点路由同样模型），帮你选最便宜的交付路径，而不只是最便宜的模型。

## TL;DR

- **GPT-5.5（旗舰）**：$5/M 输入、$15/M 输出——复杂推理、长上下文综合、硬编码任务首选。
- **GPT-5.4（中端）**：$2.50/M 输入、$10/M 输出——大多数生产工作流的最佳平衡点，5.5 质量的 90%，价格一半。
- **GPT-5 Mini**：$0.15/M 输入、$0.60/M 输出——分类、抽取、简单补全、高并发 agent 首选。
- **Batch API**：所有价格 5 折，24 小时内异步交付。评测、批处理、不需要实时的场景用。
- **Cached input**：5 分钟缓存半价、1 小时缓存 7.5 折（25% off），针对重复 prompt 段落。对于重复 system prompt 或长上下文的工作流，是单一最大的成本杠杆。
- **真实预算**：$100 在 5.5 上买到 2000 万输入 + 667 万输出 token，在 5.4 上是 4000 万输入 + 1000 万输出，在 Mini 上是 6.66 亿输入 + 1.66 亿输出。
- **国内访问**：OpenAI 国内不直连。[FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) 从国内直连的 OpenAI 兼容端点路由 GPT-5 全系，价格一致。

## 2026 年 GPT-5 阵容

### GPT-5.5——旗舰（$5/M 输入、$15/M 输出）

2026 年 3 月发布的新顶级模型，GPT-5.5 是最难推理任务的主力：800K 上下文窗口、原生多模态（文本+图像+音频），截至 2026 年 6 月在编码（SWE-bench）、数学（MATH）、研究生级推理（GPQA）基准上分数最高。价格是 5.4 的两倍，无论输入输出，所以规则很简单：只有当便宜档位可证明在你的评测上失败时才用 5.5。

5.5 真正的甜区是长上下文综合。如果你送 200K+ token 的输入（整个代码库、论文、法律合同）并需要模型在整个上下文上推理，5.5 对 5.4 的优势会拉开。对于短 prompt（4K token 以内），质量基准上差距通常在 5-10% 以内，几乎不值 2 倍价。

定价（截至 2026 年 6 月 10 日）：

| 计费项 | 单价 |
|---|---|
| 输入（文本） | $5.00 / 百万 token |
| 输入（缓存，5 分钟） | $2.50 / 百万 token |
| 输入（缓存，1 小时） | $3.75 / 百万 token |
| 输出（文本） | $15.00 / 百万 token |
| 输出（缓存写入） | $3.75 / 百万 token |
| 音频输入 | $10.00 / 百万 token |
| 音频输出 | $30.00 / 百万 token |
| 图像输入 | $5.00 / 百万 token（1024x1024 约 1,000 token） |
| Batch API（所有价格） | 5 折 |

### GPT-5.4——中端（$2.50/M 输入、$10/M 输出）

GPT-5.4 是 2026 年大多数生产部署的主力。模型比旗舰落后一代，但价格-质量权衡是有利的：大多数推理任务上 5.5 的 90% 质量，更简单的分类和抽取工作流上是 100% 质量，输入成本正好一半。对大多数真实产品团队，5.4 是默认选择。

5.4 的上下文窗口是 400K token——是 5.5 的一半，但仍是大多数生产 prompt 需要的 3-4 倍。多模态支持跟 5.5 相同（文本、图像、音频）。主要限制：在最难推理基准（SWE-bench Verified 80% 以上、GPQA Diamond 75% 以上）上 5.4 落后 5.5 约 5-8 分。如果你的产品差异化是绝对最佳质量，你必须用 5.5。如果你用可接受质量换成本，5.4 是正确答案。

定价（截至 2026 年 6 月 10 日）：

| 计费项 | 单价 |
|---|---|
| 输入（文本） | $2.50 / 百万 token |
| 输入（缓存，5 分钟） | $1.25 / 百万 token |
| 输入（缓存，1 小时） | $1.875 / 百万 token |
| 输出（文本） | $10.00 / 百万 token |
| 输出（缓存写入） | $2.50 / 百万 token |
| 音频输入 | $5.00 / 百万 token |
| 音频输出 | $20.00 / 百万 token |
| 图像输入 | $2.50 / 百万 token |
| Batch API（所有价格） | 5 折 |

### GPT-5 Mini——预算档（$0.15/M 输入、$0.60/M 输出）

GPT-5 Mini 是 2025 年底取代 GPT-4o-mini 和 GPT-3.5-turbo 的新预算档。$0.15/$0.60 per 百万 token 是 2026 年 OpenAI 仍然值得用于生产的最便宜模型——再便宜质量就断崖式下跌。上下文窗口 256K，多模态只支持文本+图像（无音频），模型针对高吞吐低延迟场景优化。

Mini 档是 2026 年 agent 经济学的关键。如果你在构建一个任务里 50+ 次 LLM 调用的 agent 框架，编排器用 Mini（$0.60/M 输出）、最后综合用 5.5 是标准模式。同样的 agent 全程用 5.5，编排器调用上贵 25 倍，并且不会更快（Mini 在简单 prompt 上的 TTFT 跟 5.4 一样）。

定价（截至 2026 年 6 月 10 日）：

| 计费项 | 单价 |
|---|---|
| 输入（文本） | $0.15 / 百万 token |
| 输入（缓存，5 分钟） | $0.075 / 百万 token |
| 输入（缓存，1 小时） | $0.1125 / 百万 token |
| 输出（文本） | $0.60 / 百万 token |
| 输出（缓存写入） | $0.15 / 百万 token |
| 音频输入 | 不支持 |
| 音频输出 | 不支持 |
| 图像输入 | $0.15 / 百万 token |
| Batch API（所有价格） | 5 折 |

## Batch API：5 折、异步

Batch API 是 OpenAI 2026 年提供的单一最大折扣：每个模型每个价格 5 折，换取异步交付。你提交一个 JSONL 文件（每批最多 50,000 个请求、200MB），批在 24 小时内完成（实际上 1-6 小时），按半价支付每个 token。

代价是延迟。Batch 不适合交互式用户场景。适用场景：

- **评测流水线**：对一万条模型输出打 ground truth 分。
- **批量内容生成**：批量产出产品描述、翻译、摘要。
- **回填任务**：对历史数据重新分类、对旧文档生成 embedding。
- **离线分析**：模型跑在夜间数据仓库任务上。

对于实时聊天、agent 循环、或用户正在等待的工作流，Batch 不可用。24 小时 SLA 决定了它跟流式 Chat Completions API 根本不是同一类东西。

算账示例：一个团队每月在 GPT-5.5 上跑 1 亿输出 token 的评测工作：

- Chat Completions API 按 $15/M 输出 = 每月 $1,500
- Batch API 按 $7.50/M 输出 = 每月 $750
- 节省：每月 $750，整整一半

坑：你得搭批提交流水线。OpenAI Python SDK 直接支持 `batches` 端点，JSONL 格式文档齐全，但它不是流式聊天的直接替代品。大多数团队把 Batch 作为独立代码路径加在能容忍延迟的工作流上。

## Cached input：重复 prompt 半价

Cached input 折扣是第二个杠杆，对许多生产工作流是更大的杠杆。当你重复送同样的长前缀（50K token 的 system prompt、200K token 的 RAG 文档、1MB 的 code review 工具代码文件）时，OpenAI 缓存 prompt token 并对缓存部分打折。

2026 年有两个缓存档：

| 档位 | 折扣 | 缓存寿命 | 适合场景 |
|---|---|---|---|
| **5 分钟缓存** | 5 折 | 5 分钟不活动 | 交互会话、agent 循环、多轮聊天 |
| **1 小时缓存** | 7.5 折（25% off） | 1 小时不活动 | 批处理、定时报告、评测、稳定语料的 RAG |

5 分钟档是自动应用的默认。当 prompt 前缀匹配 5 分钟内用过的缓存条目时，缓存部分按 5 折计费。无需主动开启——OpenAI 透明地应用。坑：缓存至少 1,024 token 才有资格，缓存键是前缀的字节序列，所以一个空白改动就让它失效。

1 小时档需要主动开启。你在 API 调用里设置 `prompt_cache_retention: "1h"`，OpenAI 把缓存寿命延长到 1 小时（仍然 7.5 折而不是 5 折，因为存储成本更高）。这是反复送同样大文档的批处理任务的正确档位——评测套件、稳定语料的 RAG 系统、反复处理同样仓库的 code review 工具。

算账示例：一个 RAG 系统每次查询送 200K token 文档：

- 无缓存：200K 输入 token × $5/M（5.5）= 每次 $1.00
- 5 分钟缓存命中（200K 半价）：200K × $2.50/M = 每次 $0.50
- 1 小时缓存命中（200K 7.5 折）：200K × $3.75/M = 每次 $0.75

5 分钟档每次折扣更大，但只对交互工作流有效。1 小时档是批处理和定时任务的正确选择。

缓存写入费是第三块。当你写新内容到缓存（之前没送过的新长文档），OpenAI 收"cache write"费是输入价的 25%。这分摊到未来所有缓存命中上，但首次请求你付完整输入价 + 缓存写入。对大多数工作流这不是问题（缓存写入费相对总查询量很小），但对一次性批处理工作流（不受益于重复访问），缓存输入档不是成本节省。

## 真实成本算账：三档预算

下面的算账假设 1:3 的输入输出比（聊天和 agent 工作流的典型情况），以及标准价（无 Batch、无缓存）。输出在账单里占大头，所以减少输出 token 是最高杠杆的优化。

### $100/月预算

| 模型 | 输入 token | 输出 token | 适合 |
|---|---|---|---|
| GPT-5.5 | 2000 万 | 667 万 | 硬推理、小文件 code review |
| GPT-5.4 | 4000 万 | 1000 万 | 通用聊天、中等文档分析 |
| GPT-5 Mini | 6.66 亿 | 1.66 亿 | 高并发 agent、分类、超大语料 RAG |

$100 预算下，选择本质是关于并发量。在 Mini 上，$100 覆盖大量流量——1.66 亿输出 token 约 4000 万字，足够一个每天产出 200 篇文章的内容生成流水线。在 5.5 上，$100 覆盖约 667 万输出 token，约 150 万字——够一个专注的日更内容产品或一个小聊天产品。

### $1,000/月预算

| 模型 | 输入 token | 输出 token | 适合 |
|---|---|---|---|
| GPT-5.5 | 2 亿 | 6670 万 | 中型产品，5.5 作为默认 |
| GPT-5.4 | 4 亿 | 1 亿 | 生产部署，5.4 默认 + 5.5 fallback |
| GPT-5 Mini | 66.6 亿 | 16.6 亿 | 大众市场产品、分类为主、大规模 RAG |

$1,000 下，选择取决于工作流类型。对于 1 万 DAU 的聊天产品，5.4 是正确默认（1 亿输出 token = 每天每用户约 1,000 token，典型聊天负载）。对于每天 1,000 次运行的内容生成产品，5.5 是合理的（6670 万输出 token = 每次 67K token，一篇长文）。对于审核或分类流水线，Mini 的 16.6 亿输出 token 是海量——每月足够处理几亿次审核决策。

### $10,000/月预算

| 模型 | 输入 token | 输出 token | 适合 |
|---|---|---|---|
| GPT-5.5 | 20 亿 | 6.67 亿 | 旗舰产品、agent、大文档分析 |
| GPT-5.4 | 40 亿 | 10 亿 | 多产品套件，5.4 作为主力 |
| GPT-5 Mini | 666 亿 | 166 亿 | 大众市场分类、搜索、推荐 |

$10,000 下，架构比模型选择更重要。烧这个量级的团队通常跑一个路由层来分发请求——最难的查询用 5.5，大头用 5.4，长尾简单补全用 Mini。OpenAI Python SDK 直接支持 `batches` 端点，大多数团队把它跟 [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220)（一个 OpenAI 兼容聚合层，让你不用改代码就能从不同端点路由同一模型）这样的路由层搭配。

## 决策树：哪个模型什么时候用

```
任务是简单分类、抽取或路由吗？
  → 是：GPT-5 Mini
  → 否，继续。

输入在 4K token 以内，任务是通用聊天/补全？
  → 是：GPT-5.4
  → 否，继续。

输入在 100K token 以上（长上下文综合）？
  → 是：GPT-5.5
  → 否，继续。

任务是质量作为差异化的硬编码或数学题？
  → 是：GPT-5.5
  → 否，继续。

默认：GPT-5.4
```

决策树故意保守。默认是 5.4 而不是 5.5，因为 2026 年价格-质量差距对 5.4 有利。只有当你有证据表明 5.4 在你的具体工作流上失败时才伸手够 5.5。Mini 同理：高并发工作流的默认是 Mini 而不是 5.4，因为成本差输入侧 16 倍，简单任务上的质量差距可以忽略。

## 国内访问和 FreeModel

OpenAI 截至 2026 年 6 月国内大陆不直连。上面价格对所有能访问 OpenAI 的地方都一样，但国内开发者通常走三条路之一：

1. **代理/VPN 直连 OpenAI**——延迟高（增加 200-500ms）、可靠性有波动、偶尔限速。能用但交互场景感觉很慢。
2. **国内直连的 OpenAI 兼容聚合**——[FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) 是最成熟的选项。它在国内直连的 OpenAI 兼容端点后面暴露 GPT-5 全系，付费档跟 OpenAI 直连同价（无加价），免费档覆盖 5.4 和 Mini 的开发用量。
3. **Azure OpenAI Service**——通过 21Vianet 合作在国内运行。价格略有不同（Azure 是独立计费关系），新账户 3-7 天开通流程。

FreeModel 是大多数国内团队最便宜的即插即用：同价、同样的 OpenAI SDK、国内直连延迟。迁移就是换 base URL。唯一坑：FreeModel 免费档限速 60 RPM，够开发但不够生产。付费档从 OpenAI 直连同价开始。

## 代码：Python + OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# 默认：GPT-5.4（中端，最佳价格/质量平衡）
response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the last 3 emails in my inbox."},
    ],
)

print(response.choices[0].message.content)
print(f"Tokens: {response.usage.total_tokens}")
```

要用 cached input（自动应用 5 分钟缓存，前缀 1,024 token 以上）：

```python
# 首次请求：完整价格，写入缓存
response1 = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},  # 50K token
        {"role": "user", "content": "Query 1"},
    ],
)

# 5 分钟内后续请求：缓存前缀 5 折
response2 = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "system", "content": LONG_SYSTEM_PROMPT},  # 同样前缀
        {"role": "user", "content": "Query 2"},
    ],
)

# 检查响应里缓存的 token 数
print(f"Cached: {response2.usage.prompt_tokens_details.cached_tokens}")
```

要开启 1 小时缓存：

```python
response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[...],
    extra_body={"prompt_cache_retention": "1h"},  # 7.5 折而不是 5 折
)
```

## 代码：curl + 手动 JSON

```bash
curl -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-5.4",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Write a haiku about programming."}
    ]
  }'
```

要用 Batch（所有价格 5 折）：

```bash
# 1. 创建 JSONL 文件，每行一个请求
cat > batch_input.jsonl << 'EOF'
{"custom_id": "req-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-5.4", "messages": [{"role": "user", "content": "Hello"}]}}
{"custom_id": "req-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-5.4", "messages": [{"role": "user", "content": "World"}]}}
EOF

# 2. 上传批输入文件
BATCH_FILE=$(curl -s -X POST "https://api.openai.com/v1/files" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "file=@batch_input.jsonl" \
  -F "purpose=batch" | jq -r .id)

# 3. 创建批
BATCH_ID=$(curl -s -X POST "https://api.openai.com/v1/batches" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"input_file_id\": \"$BATCH_FILE\", \"endpoint\": \"/v1/chat/completions\", \"completion_window\": \"24h\"}" | jq -r .id)

echo "Batch created: $BATCH_ID"
```

## 限制

**GPT-5 不是一个模型。**"GPT-5" 这个名字覆盖三档（5.5、5.4、Mini），三个价格点，三种能力档案。如果看到"GPT-5"的基准没标档位，结果大概率是 5.5（旗舰），不适用于 5.4 或 Mini。

**缓存命中不保证。**5 分钟缓存是尽力而为。如果 OpenAI 驱逐你的缓存条目（高负载、容量管理），下一个请求付全价。大多数生产工作流在重复 prompt 上看到 80-95% 缓存命中率，但 5-20% 的失手率意味着你不该按 100% 缓存命中做预算。

**缓存写入费是真的。**首次请求写新长前缀到缓存时，你付输入价 + 25% 的"cache write"附加费。对一次性工作流（不受益于重复访问），缓存不是成本节省。

**Mini 不支持音频。**如果你的工作流含音频（转写、语音 agent、音频分类），需要 5.4 或 5.5。Mini 只处理文本和图像。

**Batch 有 24 小时 SLA。**对实时工作流，Batch 不可用。24 小时完成窗口是合同；大多数批 1-6 小时完成但你不能依赖更快。

**国内访问需要 workaround。**OpenAI 国内大陆不直连。三条路是代理、FreeModel（国内直连 OpenAI 兼容聚合）、或 Azure OpenAI（独立计费）。

## 使用场景

**1 万 DAU 的聊天产品。** 默认用 **GPT-5.4** 做主聊天。用 **GPT-5 Mini** 做意图分类、路由决策、对话摘要。给长上下文综合请求（用户上传 100K+ token 文档）保留 **GPT-5.5**。典型聊天负载（每条消息 1,000 输入 + 500 输出 token），1 万 DAU 每天 10 条消息 = 1 亿输出 token，落在 5.4 的 $1,000 预算里。

**Code review 工具。** 最终 review 用 **GPT-5.5**（差异化是质量）。预筛选步骤（决定哪些 PR 浮上来）用 **GPT-5.4**。"这个 PR 描述清楚吗？"分类用 **GPT-5 Mini**。Cached input 杠杆这里很重要：200K token 的仓库上下文能缓存起来给反复的 PR 用，后续调用的输入成本砍半。

**10M token 语料的 RAG 系统。** 答案生成用 **GPT-5.4**，检索到的文档前缀用 1 小时档缓存。无缓存情况下，200K token 检索文档在 5.4 输入上每次 $0.50。用 1 小时缓存 7.5 折，同查询 $0.375——如果同样文档被反复查（"公司年假政策是什么"这类典型问题），5 分钟缓存 5 折降到 $0.25。

**高并发审核或分类流水线。** 只用 **GPT-5 Mini**。$0.15/$0.60 per 百万 token，每天数百万次决策的成本可以忽略。质量对二分类绰绰有余，延迟是三档里最低的。

**从已废弃的 GPT-5.2 系列迁移过来。**迁移到 GPT-5.4 是一行模型字符串改动。价格更低（5.4 是 $2.50/$10 vs 5.2 是 $10/$30），所以大多数工作流在迁移中省 3-4 倍成本。对硬推理上原本用 GPT-5.2 的工作流，GPT-5.5 是升级路径（5.5 输入也便宜于 5.2：$5 vs $10）。

## FAQ

**Q：聊天产品应该用哪个 GPT-5 模型？**

A：GPT-5.4 是 2026 年大多数聊天产品的正确默认。5.4 和 5.5 之间的价格-质量差距小（大多数聊天基准上 5-10% 以内），但成本差 2 倍。给长上下文请求（100K 以上输入 token）保留 5.5，分类和路由调用用 Mini。

**Q：GPT-5 比 GPT-4o 便宜吗？**

A：输入侧便宜。GPT-5.4 的 $2.50/M 是 GPT-4o $5/M 的一半，Mini 的 $0.15/M 跟 GPT-4o-mini 的 $0.15/M 一样（无变化）。对大多数工作流，从 GPT-4o 迁到 GPT-5.4 是 2 倍成本节省，质量持平或更好。

**Q：能在同一工作流里混用模型吗？**

A：能，而且应该。标准模式是长尾简单补全（意图分类、路由、摘要、抽取）用 Mini，用户面补全的大头用 5.4，最难的任务用 5.5。OpenAI Python SDK 同样调用形态支持三档模型，所以路由逻辑在你的应用代码里。

**Q：Cached input 折扣怎么工作？**

A：当你送一个前缀匹配缓存条目（至少 1,024 token，5 分钟档 5 分钟内用过、1 小时档 1 小时内用过）的请求时，OpenAI 对缓存部分打折。5 分钟档自动，5 折。1 小时档需主动开启（`prompt_cache_retention: "1h"`），7.5 折。两者透明应用——你不需要自己管理缓存。

**Q：Batch API 值得等 24 小时吗？**

A：对评测、批量内容生成、回填任务，值——5 折折扣在规模上很明显。对交互工作流，不值。24 小时 SLA 跟任何用户面产品不兼容。大多数团队把 Batch 作为独立代码路径加在异步工作流上，实时路径继续用 Chat Completions API。

**Q：能从国内用 GPT-5 吗？**

A：OpenAI 国内大陆不直连。三条路是代理/VPN（高延迟、不可靠）、[FreeModel](https://freemodel.dev/invite/FRE-7a3b6220)（国内直连 OpenAI 兼容聚合，同价）、或通过 21Vianet 的 Azure OpenAI Service（独立计费、3-7 天开通）。对大多数国内团队，FreeModel 是最便宜的即插即用。

**Q：有免费档吗？**

A：OpenAI 给新账户 $5 免费额度（3 个月有效），但 GPT-5 没有永久免费档。FreeModel 有永久免费档用于 GPT-5.4 和 Mini 的开发（60 RPM、每天 100K token）。要生产需要在 OpenAI 直连、FreeModel、或 Azure 跑付费账户。

**Q：GPT-5.2 怎么了？**

A：2026 年 6 月 5 日废弃，Copilot 在 8 月内逐步退役。直连 API 预计 2026 Q4 结束。大多数生产工作流应该在 2026 Q3 之前迁到 5.4（更便宜、质量相似）或 5.5（旗舰、新）。

## 结论

2026 年 GPT-5 定价围绕三档构建，正确选择取决于工作流类型而不是品牌名。GPT-5.5 $5/$15 per 百万 token 是最难推理任务的旗舰。GPT-5.4 $2.50/$10 是大多数生产部署的主力——大多数任务同样质量，成本一半。GPT-5 Mini $0.15/$0.60 是高并发 agent 和分类的预算档，是长尾简单补全的正确默认。

两个复合杠杆是 Batch（所有价格 5 折，仅异步）和 cached input（5 分钟档 5 折、1 小时档 7.5 折，针对重复 prompt）。对长 system prompt、稳定语料的 RAG、或固定仓库的 code review 类工作流，cached input 杠杆是单一最大的成本优化——并且是自动的，无需改代码。

对 2026 年大多数团队，正确架构是路由：简单调用用 Mini，大头用 5.4，难的用 5.5。[FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) 是国内直连 OpenAI 兼容访问（同样模型、同价、无代理）最务实之选。OpenRouter 是多厂商灵活性的替代。Batch API 是对任何能等 24 小时工作流的优化。Cached input 折扣是任何有稳定长前缀工作流必开的杠杆。

定价不是全部故事——模型质量、延迟、特性支持（function calling、视觉、音频）都参与。但对 2026 年成本敏感的团队选模型，数学是：5.4 作为默认开始，只有评测说 5.4 失败才伸手够 5.5，不需要 5.4 质量的工作用 Mini。给任何有长前缀的工作流开 cached input。给任何能等 24 小时的工作流开 Batch。这是 2026 年上生产 GPT-5 的最便宜路径。
