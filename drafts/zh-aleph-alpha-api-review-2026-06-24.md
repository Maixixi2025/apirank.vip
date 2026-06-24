---
title: "Aleph Alpha 2026 测评：欧洲主权 AI API 完全解析"
description: "Aleph Alpha API 完整测评：Pharia-1-LLM-7B-control 多语言模型、PhariaAI 可私有化部署、OpenAI Responses API 兼容、GDPR 与 EU AI Act 合规。深度解析 2026-04 Cohere 合并、定价策略、与 Mistral AI 的定位差异。"
slug: "aleph-alpha-api-review"
provider: "aleph-alpha"
published: true
date: "2026-06-24"
type: "review"
---

# Aleph Alpha 2026 测评：欧洲主权 AI API 完全解析

## 引言：为什么 Aleph Alpha 在 2026 年值得关注

Aleph Alpha 是欧洲对"美国 AI 实验室从不问的问题"的回答：当买家是政府部委、国防机构或受监管银行（法律上不能向美国托管端点发送 prompt）时，AI 提供商应该长什么样？Aleph Alpha 于 2019 年在德国海德堡由 Jonas Andrulis（前苹果工程师）创立，过去六年时间构建了今天的旗舰产品 **PhariaAI** — 一个完整可私有化部署的 LLM 技术栈，把模型权重、推理运行时（PhariaOS）和开发者工具（PhariaStudio）打包在一起。当前生产模型是 **Pharia-1-LLM-7B-control**，一个 70 亿参数的多语言 LLM，原生训练于 DE/EN/FR/ES/IT/PT/NL（德语及其他主要欧盟语言 — 在硅谷关心这些之前）。

然后在 2026 年 4 月 24 日，Cohere 宣布与 Aleph Alpha 合并，合并后公司估值 $200 亿，Schwarz 集团（Lidl/Kaufland 母公司）同期向 Cohere 的 E 轮投资 $6 亿。截至 2026 年 6 月，交易尚未完成；Aleph Alpha 文档站点仍在自有品牌下运营，API 仍指向 Aleph Alpha 的端点，PhariaAI 产品仍由 Aleph Alpha GmbH 销售。但趋势已不可逆：这家想成为"欧洲 Palantir"的公司正在与想成为"企业级 OpenAI"的公司合并。本文把 Aleph Alpha 当作今天仍独立存在的主权 AI 厂商来评估，并把合并视为 2026 年任何采购决策中最大的单一变量。

Aleph Alpha 的诚实定位：**这不是 GPT-4o 的竞争对手**。Pharia-1-LLM-7B-control 是 7B 模型 — 在参数规模、预训练算力和基准测试分数上，比美国前沿模型小几个数量级。Aleph Alpha 的赌注是：对于欧洲企业市场的一个有意义切片，主权、数据驻留、法规合规和源头透明度比 MMLU 上 5 分的提升更重要。对于这个切片 — 德国政府、国防、受欧盟监管的 BFSI、医疗（受 GDPR 约束）— Aleph Alpha 是唯一在每个维度都打勾的供应商。

## 模型矩阵：Pharia-1 系列

Aleph Alpha 2026 年的当前生产线是 **Pharia-1** 系列（2024 年 8 月发布）。老旧的 **Luminous** 系列（Supreme / Extended / Base / Chat）已完全弃用 — PhariaAI 2026-06-09 的 v1.260600.0 发布说明明确写道"已弃用 luminous worker"，Luminous 模型在 Hugging Face 的卡片返回 404，推理栈已迁移到 vLLM 0.21.0。如果你 2026 年评估 Aleph Alpha，你评估的就是 Pharia-1。

旗舰是 **Pharia-1-LLM-7B-control** — 精确地说 7,041,544,704 参数，8,192-token 上下文窗口，分组查询注意力（grouped-query attention），旋转位置编码 base 1,000,000，128k 词表的 Unigram 分词器，覆盖七种欧洲语言训练。以 **Open Aleph** 许可证发布，用于研究和教育。对于聊天相关用例，Aleph Alpha 推荐 **Pharia-1-LLM-7B-control-aligned** — 同样的 7B 基础，额外的安全对齐训练。两者都以 Hugging Face safetensors 形式提供（`Pharia-1-LLM-7B-control-hf` 截至 2026 年 6 月已有 1.45k likes），可用 vLLM 或 SGLang 部署自托管推理。

对于检索工作负载，**Pharia-1-Embedding-4608-control** 是一个 7B 参数的嵌入模型，输出 4,608 维向量。它支持推理时的指令调优（与 GritLM 同源的表征指令调优技巧），同一个模型可通过修改指令前缀重新用于非对称搜索、分类或聚类。256 维的 `control-256` 变体可用于成本敏感部署。

除核心 Pharia-1 系列外，托管的 PhariaAI 栈现在还通过 vLLM 提供 **第三方模型** — 例如 PhariaAI Responses API 文档引用了 `qwen3-32b-tool`。这是一个有意义的战略转向：Aleph Alpha 从"我们卖自己的 7B 模型"转向"我们卖一个能托管任何开源权重模型的欧洲主权运行时"。出于主权原因选择 Aleph Alpha 的客户现在可以在同一个合规外壳下使用 Qwen、Llama 和其他开源模型。

## Cohere 合并：这对采购意味着什么

2026 年 4 月 24 日，Cohere 宣布与 Aleph Alpha 战略合并。合并后公司估值 $200 亿；Schwarz 集团同期向 Cohere E 轮投资 $6 亿。定位是"跨大西洋 AI 强权" — Cohere 的企业商业规模（多伦多 + 旧金山 + 伦敦）+ Aleph Alpha 的欧盟监管定位和私有化部署栈（海德堡 + 柏林 + 拜罗伊特 + 慕尼黑）。柏林已公开支持该交易。

对于 2026 年中考虑 Aleph Alpha 的潜在客户，三个实际问题：

1. **Aleph Alpha 的数据驻留和私有化故事能否在合并后存活？** Cohere 当前的企业产品都是托管的（north-america、eu 和 asia 区域在 Cohere 托管云上）。如果 PhariaAI 的私有化栈被纳入 Cohere 的仅托管模式，Aleph Alpha 最强的单一差异化点将显著弱化。截至 2026 年 6 月，PhariaAI 产品页仍以私有化部署为重点，所以立场暂时完好。

2. **定价是否会公开？** Aleph Alpha 的仅企业报价定价姿态是开发者采用的最大单一摩擦点（见下一节）。Cohere 已为 Command R+、Aya 和 Embed 发布了按 token 定价。合并后 Aleph Alpha 可能发布分层定价 — 但没有确认。

3. **Pharia-1 模型路线图是否会继续？** Cohere 的研究方向是北美企业 — Command R+、Aya 多语言和企业检索。Aleph Alpha 的研究方向是欧洲主权 AI — Pharia、TFree-HAT 和 Intelligence Layer SDK。合并后公司的模型路线图是最大的开放问题。

务实的建议：如果你 2026 年评估 Aleph Alpha，请把你的代码写在 **OpenAI Responses API** 端点上（见下文 API 节），这样你可以在不重写应用的情况下换成 Cohere Command R+ 托管端点或任何其他 OpenAI 兼容模型。把 Aleph Alpha 当作一个 API 合同，而不是一个供应商关系，直到合并完成。

## 定价：仅企业报价，无公开列表

Aleph Alpha 不在营销站点或 API 文档上发布按 token 定价。没有像 OpenAI、Anthropic、Mistral 或 Cohere 那样把你丢进按量付费控制台的自助注册流程。注册流程创建一个账号，你可以生成一个 API token，但下一步是"联系销售" — Aleph Alpha"仅服务于企业和政府机构"（维基百科引用 Aleph Alpha 自己的定位）。

托管 PhariaAI 端点的定价基于合同。私有化 PhariaAI 部署按部署定制定价 — 通常是许可费加上按客户硬件规模与推理量量身的年度支持合同。公共部门客户（运行"Lumi"公民信息系统的海德堡市、德国联邦机构）似乎在逐案协商。

为对比目的，Aleph Alpha 的实际定价在按 token 基础上几乎肯定高于最便宜的美国托管前沿模型，但这个套件包含合规、私有化部署权以及对 prompt 数据处理的合同承诺 — 这些是你从 OpenAI 或 Anthropic 无法得到的。交换是美元换主权，不是美元换原始能力。

**定价汇总（截至 2026 年 6 月，所有项"联系企业报价"）：**

| 部署方式 | 定价模式 | 公开标价 |
|---|---|---|
| 托管 PhariaAI（管理云，欧盟区） | 企业合同 | 未发布 |
| 私有化 PhariaAI（你的硬件） | 许可 + 年度支持 | 按部署报价 |
| 嵌入 API（Pharia-1-Embedding-4608-control） | 同托管 PhariaAI | 未发布 |
| PhariaAI 上的第三方模型（Qwen 等） | 同托管 PhariaAI | 未发布 |

如果你是评估 Aleph Alpha 的开发者，务实的建议：用自助注册获取一个 token 来跑通 API，但为任何生产部署预算 4-8 周的销售周期时间。这更接近买企业数据库，而不是启动一个 LLM API。

## API 接口：OpenAI Responses 兼容 + 遗留 Aleph Alpha 客户端

Aleph Alpha 2026 年面向开发者最大的故事是 **PhariaAI Responses API** — OpenAI Responses API 规范的完整实现。端点是 PhariaAI 部署 URL 上的 `/v1/responses`（私有化部署由客户控制，或托管部署由 Aleph Alpha 配置）。你可以通过覆盖 `base_url` 把 OpenAI Python SDK 指向 PhariaAI 部署：

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://your-deployment.aleph-alpha.com/v1",  # PhariaAI 私有化
    api_key="YOUR_AA_TOKEN",
)

response = client.responses.create(
    model="pharia-1-llm-7b-control-aligned",
    input="为询问删除数据的客户写一段礼貌的德语拒绝话术。",
    instructions="你是一名德语客服代表。用德语回复。",
)

print(response.output_text)
```

这能工作是因为 PhariaAI 的 Responses API 实现了 OpenAI Responses 规范：SSE 流式、工具调用、异步任务、软/硬删除、LlamaGuard 集成用于守卫。你也可以直接使用 PydanticAI、LangGraph（通过 langchain-openai）或 curl。与遗留的 Aleph Alpha API 相比，这是一个重大的开发者体验胜利。

对于需要更老、更丰富的 Aleph Alpha 功能的客户，**aleph-alpha-client** Python SDK（v11.5.1，MIT 协议，`pip install aleph-alpha-client`）暴露了 `Client(token, host).complete(request, model="pharia-1-llm-7b-control")`、`AsyncClient`，以及一组更丰富的请求类型 — `EmbeddingRequest`、`SemanticEmbeddingRequest`、`RerankRequest`、`ExplanationRequest`、`EvaluationRequest`、`ChatRequest` — 这些超出了 Responses API 所暴露的范围。`ExplanationRequest` API 尤其独特：它要求模型高亮显示哪些输入 token 对每个输出 token 做出了贡献，是面向可解释性应用的源头透明度功能。如果你在受监管行业构建需要向审计师为模型输出辩护的系统，这是任何美国厂商都不提供的差异化点。

**Intelligence Layer SDK** 是 Pharia-1 系列 + 第三方模型 + 评估流水线的统一框架。**Pharia Data SDK** 处理数据平台层。没有官方 Anthropic 兼容的 API 端点。

认证是 `Authorization: Bearer *** 请求头中的 Bearer token，token 在用户资料中创建，存储在 `AA_TOKEN` / `TEST_TOKEN` 环境变量中。速率限制未公开文档化 — 它们似乎是按账号而非按 IP，私有化部署根本没有速率限制（硬件就是极限）。

## 欧盟主权、GDPR 与数据驻留

这是对采购决策最重要的章节。Aleph Alpha 的姿态：

- **不存储 prompt 数据。** Pharia-1 模型卡片明确声明："使用我们的系统时不存储 prompt 数据…我们不记录用户对模型的输入。我们不基于用户数据训练。"
- **GDPR 合规的训练数据。** 根据 Aleph Alpha 的公开声明，Pharia-1"在符合适用欧盟和国家法规（包括版权和数据隐私法）的精心策划的数据上训练"。
- **EU AI Act 协调。** Aleph Alpha 于 2026 年 2 月签署欧盟通用 AI 行为准则，并将 Pharia-1 系列定位为符合 EU AI Act。
- **私有化部署。** PhariaAI 可以完全在客户硬件上运行 — 模型权重、推理运行时、所有数据保留在客户基础设施内。这是可能的最强数据驻留姿态：永远不会有任何东西离开客户司法管辖区。
- **不基于用户输入训练。** 即使是托管的 PhariaAI 也不使用客户 prompt 或输出进行模型训练。

对于受 GDPR、EU AI Act、特殊行业法规（银行：MaRisk、BaFin；保险：Solvency II；医疗：MDR；国防：北约出口管制）或要求欧盟司法管辖区处理的公共部门采购规则约束的客户，Aleph Alpha 是极少数商业选项之一。另一个是 Mistral AI（在我们的 provider 数据库中独立覆盖），但 Mistral 的部署姿态是混合的 — 可用托管欧盟区，私有化仅通过开源权重自托管路径，没有技术栈的商业支持合同。

## Aleph Alpha vs Mistral AI

欧洲主权 AI 空间最自然的对比对象是 Mistral AI。两者都立足欧盟；都主打数据驻留和 GDPR 合规；都面向企业销售。差异是结构性的：

| 维度 | Aleph Alpha | Mistral AI |
|---|---|---|
| 总部 | 德国海德堡 | 法国巴黎 |
| 成立年份 | 2019 | 2023 |
| 模型规模（旗舰） | 7B（Pharia-1-LLM） | 12B-123B（Mistral Large 2、Mixtral、Codestral） |
| 前沿能力 | 否（仅 7B） | 是（Mistral Large 2 在大多数基准上与 GPT-4o 竞争） |
| 私有化栈 | 是（PhariaAI） | 仅开源权重，无商业栈 |
| 托管云 | 是（欧盟区） | 是（欧盟区，多区） |
| 定价 | 仅企业报价 | 按 token，已发布 |
| 自助注册 | 是（但付费墙） | 是（完全自助） |
| OpenAI 兼容 | 是（Responses API） | 是（chat completions） |
| 主权定位 | Palantir（部署 + 透明度） | OpenAI（前沿模型 + 全球分销） |
| 2026 年走向 | 与 Cohere 合并 | 独立，B+ 轮规模 |

关键问题是你相信哪个故事。如果你相信主权 AI 是一个部署 + 合规故事（且能力是次要的），Aleph Alpha 的姿态更纯粹。如果你相信主权 AI 是一个模型能力故事（且合规是加分项），Mistral 的姿态更强。合并完成后，Aleph Alpha 获得 Mistral 最大弱点（无公开定价）可能解决；Mistral 获得 Aleph Alpha 最大弱点（无私有化商业栈）可能解决，如果合并后的实体在 PhariaAI 私有化上提供 Cohere Command R+。

## 优势与劣势

**优势**

- 真正的欧盟主权 AI 姿态 — 模型训练、托管、部署全部在欧盟司法管辖区内
- PhariaAI 完整可私有化部署栈，模型权重 + 运行时 + OS + Studio 打包
- OpenAI Responses API 兼容 — OpenAI Python SDK 直接替换
- 强欧盟语言多语言覆盖（DE/EN/FR/ES/IT/PT/NL 原生训练）
- ExplanationRequest API 用于源头透明度（Aleph Alpha 独有）
- 无 prompt 存储、无用户数据训练 — 合同背书
- EU AI Act 行为准则签署方（2026-02）
- Cohere 合并带来企业商业规模，并可能带来公开定价

**劣势**

- 7B 模型 — 与 GPT-4o、Claude 3.5 Sonnet、Mistral Large 2 相比能力差距明显
- 无公开定价 — 仅企业报价
- Cohere 合并尚未完成 — 产品路线图不确定
- 无中国大陆服务（受欧盟出口管制约束）
- 开发者文档面向企业买家，自助开发者文档相对简略
- 社区和生态较 OpenAI/Anthropic/Mistral 小
- 无 Chat Completions 端点 — 仅 Responses API（迁移需适配）

## 使用场景推荐

| 使用场景 | 适配度 | 原因 |
|---|---|---|
| 德国政府/公共部门 | **优秀** | 海德堡总部，PhariaAI 私有化，GDPR + EU AI Act 合规 |
| 欧盟国防/北约承包商 | **优秀** | 欧盟出口管制姿态，私有化，无美国 CLOUD Act 暴露 |
| 欧盟 BFSI（银行、保险）受 BaFin/MaRisk 约束 | **优秀** | 源头透明度，合同背书无训练，私有化 |
| 多语言欧盟客服（DE/FR/ES/IT） | **良好** | 所有主要欧盟语言原生训练 |
| 通用聊天机器人/RAG | **差** | 7B 模型相比 GPT-4o/Mistral Large 能力受限 |
| 代码生成 | **差** | 非代码专用模型，无 Codestral 等价物 |
| 图像/多模态 | **差** | Pharia-1 仅文本，当前系列无原生视觉模型 |
| 中国市场消费应用 | **不适用** | 欧盟出口管制，无 CN 服务 |

## Aleph Alpha 与 apirank 其他厂商的对比

apirank provider 数据库中最接近的同类是：

- **Mistral AI** — 法国，前沿能力，开源权重，按 token 定价。姿态不同但同样的欧盟主权叙事。
- **OpenAI / Anthropic / Google** — 美国托管，前沿能力，但适用美国 CLOUD Act。当美国司法管辖区是阻碍因素时，Aleph Alpha 是替代品。
- **OpenRouter** — 路由层，可以为欧盟司法管辖区请求路由到 Aleph Alpha，为其他所有请求路由到 OpenAI/Anthropic。天然的多供应商架构。
- **Cohere**（合并后目标） — 北美企业，仅托管云，按 token 定价。合并后 Aleph Alpha 更接近 Cohere。

推荐矩阵：

- **当**主权、私有化或欧盟司法管辖区是硬性要求时，选择 Aleph Alpha。
- **当**你想要具有公开定价的前沿能力欧洲模型时，选择 Mistral。
- **当**原始能力是优先且欧盟数据驻留不是约束条件时，选择 OpenAI/Anthropic/Google。
- **当**不同 prompt 分类需要不同司法管辖区时，使用 OpenRouter 在它们之间路由。

## 常见问题

**Q: Aleph Alpha 的 API 兼容 OpenAI 吗？**
A: 部分兼容。PhariaAI Responses API 是 OpenAI Responses API 规范在 `/v1/responses` 端点的完整实现 — 你可以通过覆盖 `base_url` 把 OpenAI Python SDK 指向 PhariaAI 部署。遗留的 aleph-alpha-client SDK 暴露了额外的 Aleph Alpha 特有请求类型（`EmbeddingRequest`、`SemanticEmbeddingRequest`、`RerankRequest`、`ExplanationRequest`、`EvaluationRequest`、`ChatRequest`），这些超出了 Responses API 覆盖范围。没有 Anthropic 兼容的端点。

**Q: Aleph Alpha 2026 年的价格是多少？**
A: 没有公开的按 token 价格。Aleph Alpha 仅销售企业合同 — 托管 PhariaAI 端点和私有化 PhariaAI 部署都按客户定价。自助注册给你一个 API token 来跑通 API，但生产部署需要 4-8 周的销售周期。这更接近企业数据库采购，而不是启动一个 LLM API。

**Q: Aleph Alpha 的模型能在我的硬件上运行吗？**
A: 可以。PhariaAI 作为完整的私有化栈销售 — Pharia-1-LLM-7B-control 权重、PhariaOS 推理运行时、PhariaStudio 开发者工具。Hugging Face 模型卡片包含用于自托管推理的 vLLM 和 SGLang 部署片段。私有化部署没有速率限制（硬件就是极限）。

**Q: Aleph Alpha 会基于我的 prompt 进行训练吗？**
A: 不会。根据 Pharia-1 模型卡片："使用我们的系统时不存储 prompt 数据…我们不记录用户对模型的输入。我们不基于用户数据训练。" 这在企业协议中有合同背书。

**Q: 我能从中国使用 Aleph Alpha 吗？**
A: 不能。Aleph Alpha 是受欧盟出口管制约束的德国主权 AI 厂商，不提供中国大陆服务。对于中国可访问的 LLM API，请参阅 apirank 国内类别的阿里云百炼、百度文心一言、Kimi、智谱 GLM、腾讯混元或字节豆包。

**Q: Pharia-1-LLM-7B-control-aligned 是什么？**
A: 与 Pharia-1-LLM-7B-control 相同的 7B 基础模型，但有额外的安全对齐训练。Aleph Alpha 推荐此变体用于聊天相关用例。两者都以 Open Aleph 许可证（用于研究和教育）发布；PhariaAI 托管栈和私有化部署有单独的商业条款。

**Q: Cohere 合并是什么？什么时候完成？**
A: 2026 年 4 月 24 日宣布。Cohere 和 Aleph Alpha 以 $200 亿估值合并；Schwarz 集团向 Cohere E 轮投资 $6 亿。截至 2026 年 6 月交易尚未完成；Aleph Alpha 文档站点和 API 仍在 Aleph Alpha 品牌下运营。合并是 2026 年采购决策中最大的单一变量 — 请把你的代码写在 OpenAI Responses API 合同上，这样如果合并后实体的产品方向发生变化，你可以迁移到 Cohere Command R+ 托管端点。

**Q: Aleph Alpha 支持图像/多模态模型吗？**
A: 当前 Pharia-1 系列不支持。Pharia-1-LLM 仅文本。PhariaAI 通过 vLLM 托管栈提供第三方多模态模型（例如 Qwen-VL），但这些不是 Aleph Alpha 开发的模型。

## 结论

Aleph Alpha 是欧洲企业市场特定但有意义的切片的可靠选择：任何数据分类规则要求欧盟司法管辖区处理、私有化部署或 EU AI Act 合规的组织。7B Pharia-1 模型相比美国前沿模型能力受限，但对于主要约束是主权而非基准分数的买家，Aleph Alpha 是 2026 年欧洲市场上最干净的答案。

Cohere 合并是 2026 年最大的单一变量。在交易完成之前，谨慎的工程选择是把你的应用代码写在 PhariaAI 实现的 **OpenAI Responses API 合同**上 — 这给了你一个干净的迁移路径到 Cohere Command R+ 托管端点，或到任何其他 OpenAI 兼容模型，无需在合并后实体的产品方向发生变化时重写应用。

最自然的搭配是 Aleph Alpha 作为 OpenRouter **欧盟数据驻留路由**背后的**欧盟主权**端点 — 当 prompt 的数据分类要求德国司法管辖区时，路由到 Aleph Alpha 私有化；其他情况路由到 OpenAI/Anthropic/Mistral。这是我们 2026 年中期从欧盟公共部门和 BFSI 客户看到的架构。

**对大多数开发者**：Aleph Alpha 不是正确的起点。从 OpenAI、Anthropic、Mistral 或 DeepSeek 开始 — 它们有前沿能力、公开定价、自助注册和数十万个 Stack Overflow 社区答案。当你遇到这些厂商无法满足的硬性欧盟司法管辖区要求时，再去找 Aleph Alpha。
