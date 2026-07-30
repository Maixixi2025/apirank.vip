---
title: "Mem0 2026 评测：AI Agent 记忆层的事实标准"
slug: mem0-api-review
date: 2026-07-23
lang: zh
locale: zh-CN
provider: mem0
providerFeatured:
  - mem0
  - openai
  - anthropic
  - freemodel
primaryAffiliate: freemodel
affiliateUrl: https://freemodel.dev/invite/FRE-7a3b6220
type: review
category: aggregator
---

# Mem0 2026 评测：生产 AI Agent 的记忆层标准

Mem0 是 2026 年生产环境 AI Agent 首选的记忆层,也是 6 万+ 开发者选择用来给 LLM 应用添加长期、个性化上下文的事实标准方案——无需手写向量库、事实抽取流水线和遗忘过滤。2026-07-23 核验,Mem0 是**唯一**同时具备 Apache-2.0 开源(61,493 stars)和生产级 Cloud SaaS 的记忆层,广泛应用于客服机器人(记住回访用户的上一次工单)、个性化助手(跨会话记住饮食偏好)、多角色聊天应用,以及新一代把记忆当作一等公民的 Agent 框架(LangChain、LlamaIndex、CrewAI、AutoGen、Mastra)。

本评测涵盖:Mem0 比手写 RAG + 向量库多做的工作、2026 年核验后的定价(Hobby 免费层 10,000 memories、Starter $19/月 50,000 memories、Pro $249/月无限 memories 加 Graph Memory、Enterprise 合同制含 SSO/审计/私有部署)、如何用几行 Python 或 TypeScript 把 Mem0 接入 LangChain 或原生 OpenAI/Anthropic Agent,以及 Mem0 与 Zep、Letta、Redis 向量搜索、自建 Pinecone + LLM 事实抽取的对比。数据来自 Mem0 定价页(2026-07-23 实时核验)、mem0ai/mem0 GitHub 仓库(最后提交 2026-07-23)和 Mem0 官方文档。

如果你在 2026 年构建 AI Agent,想跳过「自己写事实抽取流水线」的税负,同时保留对记忆内容的控制权,本文就是参考指南。

## Mem0 做了什么(以及它不做什么)

Mem0 是**面向 AI 应用的记忆层**,不是 LLM 路由器、网关或独立的向量数据库。它位于应用代码和 LLM 之间,从对话中抽取事实、结构化(并可选向量索引化)存储记忆、在查询时检索相关记忆,并作为上下文回传到 LLM prompt。核心抽象是 `memory.add()` 和 `memory.search()`——其余由平台处理。

核心能力(2026-07-23 从 Mem0 文档与定价页核验):

- **自动事实抽取。** 调用 `memory.add(messages=[...])` 时,Mem0 用一个 LLM(可配置,默认是 GPT-4o-mini 之类的快速模型)从对话里抽取原子事实。一句「我对贝类过敏,而且我喜欢深色模式」会被存成两条记忆:`{"role": "user", "content": "用户对贝类过敏"}` 和 `{"role": "user", "content": "用户偏好深色模式"}`。这是杀手特性——没有它,你得自己写抽取 prompt、管理 JSON 解析、决定什么该遗忘。

- **向量 + 结构化混合存储。** Mem0 同时把记忆存成结构化 JSON(供直接查询)和向量嵌入(供语义检索)。默认向量库是 Qdrant(自托管或 Qdrant Cloud),但你可以换成 Pinecone、Weaviate、Chroma、pgvector 或 Redis。Cloud SaaS 自带托管向量库;自托管版则用你配置的任意一个。

- **可配置 LLM 提供商。** Mem0 开箱支持 8+ LLM 提供商:OpenAI(GPT-4o、GPT-4-Turbo、GPT-3.5)、Anthropic(Claude 3.5 Sonnet、Haiku、Opus)、Google(Gemini 1.5 Pro/Flash)、Mistral(Large、Mixtral、Mistral-7B)、Groq(Llama 3.1 70B、Mixtral)、Ollama(任意本地模型)、AWS Bedrock(Claude / Llama / Titan)、Azure OpenAI。同一 SDK 调用对它们通用——只需改 `LLM_PROVIDER` 与 `LLM_API_KEY` 环境变量。

- **Graph Memory(Pro 档及以上)。** 在向量记忆之外,Mem0 Pro 新增图存储来追踪实体关系——如果用户提到「我老婆 Sarah」,之后又提到「Sarah 的生日」,图谱会把两个节点连起来,在检索时返回这个关系。这正是 Mem0 与普通 RAG 系统的差别:它记住的不仅是事实,还有关系。

- **通过 user_id 实现多用户隔离。** 每次记忆调用都接受 `user_id`(可选 `agent_id`、`run_id`、`app_id`)。存储自动按 user 分区,单一 Mem0 实例可服务数千用户而不串数据。这是任何生产多租户 Agent 的基础。

- **Docker 自托管。** 开源 `mem0ai/mem0` 仓库自带完整 Docker Compose 配置,打包 API 服务、向量库、LLM worker、可选 Neo4j(用于 Graph Memory)。可在任意云(AWS、GCP、Azure、阿里云、腾讯云)运行,无需走 Mem0 Cloud SaaS。

### Mem0 不做的事

- **不做 LLM 推理。** Mem0 不是 LLM 提供商。你仍然需要 OpenAI / Anthropic / Gemini 的 API key 来做事实抽取和 Agent 主循环。Mem0 做编排,不做生成。

- **不做 RAG-as-a-Service。** Mem0 处理**对话记忆**,不处理文档检索。如果你要在 PDF 库里搜并加引用,你要的是 Pinecone 或 Weaviate 这类向量库(而非 Mem0)。两者互补:Mem0 管用户级对话记忆,向量库管文档级检索。

- **不做 Agent 编排。** Mem0 不跑 Agent loop。你仍然用 LangChain / LlamaIndex / CrewAI / AutoGen / Mastra 或你自己的代码来编排工具调用、规划和执行。Mem0 是记忆层,不是大脑。

- **无内置记忆检视 UI。** Mem0 SaaS 自带 dashboard 用于浏览记忆,但自托管版本只有 API。若你需要给非工程师用的精致记忆检视 UI,要么自己写,要么用 Mem0 Cloud。

## 2026 年核验后的定价(来源 mem0.ai/pricing,2026-07-23 核验)

Mem0 提供四档定价。下列数字 2026-07-23 实时从 `mem0.ai/pricing` 抓取——任何采购决策前请再核验一次,因为 Mem0 在 2024-2025 年调整过两次 Hobby/Starter 配额。

### Hobby(免费)

- **$0 / 月**——无需信用卡
- **10,000 条记忆**存储(按记忆条目数计,非字节)
- **1,000 次 retrieval API 调用 / 月**
- 无限 end users
- 1 个项目
- 社区支持(Discord + GitHub issues)
- 适合:原型、side project、个人使用

### Starter($19/月)

- **$19 / 月**
- **50,000 条记忆**
- **5,000 次 retrieval API 调用 / 月**
- 无限 end users
- 1 个项目
- 社区支持
- 适合:独立开发者上线第一个面向付费用户的 AI Agent 或聊天应用

### Pro($249/月)

- **$249 / 月**
- **无限条记忆**
- **50,000 次 retrieval API 调用 / 月**
- 无限 end users
- **多项目支持**
- **Graph Memory**(在向量记忆之上追踪实体关系)
- **高级分析**(记忆增长、检索命中率、延迟面板)
- **专属 Slack 频道**支持
- 适合:有数千活跃用户的成长型 AI 产品,或需要 Graph Memory 做实体感知检索的团队

### Enterprise(合同制)

- **自定义定价**(通常中型客户起价 $1,000-$2,500/月)
- 无限条记忆
- 无限 retrieval API 调用
- **On-prem 部署**(Docker / Kubernetes,数据不出你的 VPC)
- **SSO**(Okta、Azure AD、Google Workspace)
- **审计日志**(SOC 2 Type II ready)
- **自定义 SLA**(通常 99.9% 或 99.95%)
- 适合:受监管行业(金融、医疗、政府),或有严格数据驻留要求的团队

### 你可能漏算的成本

- **LLM 成本另算。** Mem0 用一个 LLM 做事实抽取(可选的检索重排序步骤也用一个 LLM)。Hobby/Starter/Pro 定价**不包含** LLM token。一个高流量应用每月做上百万次 memory add,可能额外花掉 $200-$500/月的 OpenAI 或 Anthropic API 费用,与 Mem0 订阅完全独立。

- **检索配额与新增配额不对称。** 典型聊天应用是 1 add(每条用户消息)+ 1 search(每次助手回复前)。Hobby 计划 1,000 次 search/月 ≈ 每天 33 条消息——对真实产品远远不够。Starter 5,000 次 search ≈ 每天 166 条,才是小规模生产应用的现实下限。

- **Cloud 用户另付向量库。** Mem0 Cloud 自带托管 Qdrant,但如果想用 Pinecone / Weaviate / pgvector,你要单独给那些厂商付款。Cloud 订阅只覆盖 Mem0 的 API 与 graph 层,不覆盖底层向量库。

- **Graph Memory 存储成本。** 在 Pro 上启用 Graph Memory 后,Neo4j(或 Mem0 托管的等价方案)就成为部署的一部分。AWS/GCP 托管 Neo4j 集群在典型 Pro 工作负载下预计 +$50-$200/月。

## Mem0 如何接入 AI Agent 流水线

Mem0 位于 Agent 框架与 LLM 之间。最简模式:

```python
from mem0 import Memory
from openai import OpenAI

# 1. 初始化 memory
memory = Memory()

# 2. 把对话加入记忆
messages = [
    {"role": "user", "content": "我对贝类过敏,而且我喜欢深色模式。"},
    {"role": "assistant", "content": "记下了,我会记住这两条。"}
]
memory.add(messages, user_id="user-12345")

# 3. 下一次 LLM 调用前检索相关记忆
relevant = memory.search(
    query="我今晚应该避免什么食物?",
    user_id="user-12345",
    limit=5
)

# 4. 把记忆注入 prompt
context = "\n".join([m["memory"] for m in relevant["results"]])
system_prompt = f"你是一个有用的助手。用户上下文:\n{context}"

# 5. 用增强后的 prompt 调用 LLM
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "今晚推荐什么餐厅?"}
    ]
)
print(response.choices[0].message.content)
```

TypeScript、Java、Go、Ruby 用同一模式。Mem0 SDK 是一等公民(非社区维护),自带 TypeScript 类型。

LangChain 用户可直接用 `Mem0ChatMemory` 类,与 `ConversationChain`、`AgentExecutor`、`RunnableWithMessageHistory` 配合。LlamaIndex 用户有 `Mem0Memory` 类,与 `ChatMemoryBuffer` 与 agent runner 配合。CrewAI / AutoGen / Mastra 通过原生 Mem0 client 集成(暂无专门 wrapper)。

## Mem0 与 2026 年的替代方案对比

| 维度 | Mem0 | Zep | Letta | Pinecone + 自建 | Redis 向量搜索 |
|---|---|---|---|---|---|
| 许可证 | Apache-2.0(核心)+ Cloud SaaS | Apache-2.0 | Apache-2.0 | 专有 SaaS | Redis Source Available(RSALv2/AGPLv3) |
| 自托管 | 可(Docker) | 可 | 可 | 否(只有 Pinecone) | 可 |
| 自动事实抽取 | 是(基于 LLM) | 是(基于 LLM) | 是(嵌入 agent loop) | 否——你写 prompt | 否——你写 prompt |
| Graph Memory | 是(Pro+) | 否 | 是(内置 agent 上下文) | 否 | 否 |
| 多用户隔离 | 是(user_id 分区) | 是(user_id) | 是(user/agent IDs) | 是(namespace) | 是(key 前缀) |
| 含向量库 | 是(默认 Qdrant) | 是(Postgres + pgvector) | 是(Postgres + pgvector) | 是(Pinecone 托管) | 是(Redis 托管) |
| Cloud SaaS | 是 | 是(Zep Cloud) | 否(只自托管) | 是(Pinecone) | 是(Redis Cloud) |
| 最低月费 | $0(Hobby)/ $19(Starter) | $0(OSS)/ $19(Zep Cloud Starter) | $0(OSS) | $50(Pinecone Standard) | $0(OSS)/ $5(Redis Cloud Essentials) |
| LangChain 集成 | 一等公民 | 一等公民 | 一等公民 | DIY | DIY |
| 最佳场景 | 上线快的生产 Agent | 长上下文 + 时间加权记忆 | 有状态 Agent 框架 | DIY 极客 | 已在用 Redis 的团队 |

**Mem0 优势:**零提示工程成本(一个 `memory.add()` 就有可用记忆)、Pro 档提供 Graph Memory 实现实体感知检索、GitHub 社区最大(61,493 stars,Zep 约 3,500、Letta 约 14,000)、LangChain / LlamaIndex 集成最干净。

**Mem0 劣势:**事实抽取异步(LLM 调用加 200-500ms 延迟,比纯向量检索慢)、Pro $249/月对个人偏高、Graph Memory 需引入 Neo4j 增加自托管运维复杂度、Mem0 不能替代向量库(你仍然需要它来做文档检索)。

**Zep 的反方观点:**Zep 专为长上下文窗口 + 时间加权记忆衰减优化——如果你的场景是「记住用户 30 轮前说过的话、按近因性加权」,Zep 的检索模型更精细。Mem0 在 Hobby/Starter 上的纯向量检索相对朴素。

**Letta 的反方观点:**Letta(原 MemGPT)把记忆管理内嵌进 agent loop 本身——LLM 主动决定何时读写记忆。这更强大,但要求跑 Letta 兼容的 agent 框架,不是简单调 Mem0 API。Mem0 是框架无关的。

**Pinecone + 自建的反方观点:**如果你已有向量库和 LLM 运维团队,用 `pinecone.upsert()` + 一条抽取 prompt + 一个遗忘过滤就能搭起自有记忆层,完全可控。Mem0 的价值在你没有那支工程团队时最明显。

**Redis 的反方观点:**如果你的栈已经在跑 Redis(缓存、会话、队列),用 `redis-vector` 管记忆可让一切共用一个引擎。代价是没有事实抽取——你存的是原始消息,不是结构化记忆,检索质量取决于你的 embedding + 分块策略。

## 何时选 Mem0(以及何时不要)

**选 Mem0 当:**

- 你在构建多轮 AI Agent,**不想**自己写事实抽取 prompt
- 你需要跨用户的记忆隔离(多租户 SaaS Agent、客服机器人、个性化助手)
- 你想尽快上线,优先选择托管 SaaS 而不是自托管基础设施
- 你需要 Graph Memory 做实体关系感知(Pro 档及以上)
- 你已经在用 LangChain / LlamaIndex / CrewAI,想直接 drop-in 一个记忆类

**不要选 Mem0 当:**

- 你在原型阶段,向量库是过度设计(直接用 LLM 上下文窗口承载对话历史,上限 ~50K tokens)
- 你有严格数据驻留要求,Mem0 Cloud 被排除(只剩 Enterprise 自托管,需要走合同)
- 你要的是文档搜索 RAG,不是对话记忆(用 Pinecone / Weaviate / Qdrant——Mem0 不是替代)
- 你的工程团队小,Mem0 + Neo4j + Qdrant 自托管栈运维成本过高(改用 Mem0 Cloud,或退回到原始对话历史)
- 你需要 sub-100ms 检索延迟(Mem0 的 LLM 抽取加 200-500ms——延迟关键路径请用预计算向量索引)

## 来源

- Mem0 定价页:mem0.ai/pricing——2026-07-23 核验
- Mem0 文档:docs.mem0.ai
- Mem0 Python SDK:pypi.org/project/mem0ai
- Mem0 TypeScript SDK:npmjs.com/package/mem0ai
- Mem0 GitHub 仓库:github.com/mem0ai/mem0——61,493 stars、Apache-2.0、最后提交 2026-07-23
- Mem0 支持的 LLM:docs.mem0.ai/components/llms/overview——OpenAI、Anthropic、Gemini、Mistral、Groq、Ollama、AWS Bedrock、Azure OpenAI
- LangChain 集成:docs.mem0.ai/integrations/langchain
- LlamaIndex 集成:docs.mem0.ai/integrations/llamaindex
- 自托管 Docker Compose:github.com/mem0ai/mem0/tree/main/server——打包 Qdrant + Neo4j
- 对比替代:Zep(getzep.com)、Letta(letta.com)、Pinecone(pinecone.io)、Redis 向量搜索(redis.io/docs/latest/develop/interact/search-and-query/vectors)