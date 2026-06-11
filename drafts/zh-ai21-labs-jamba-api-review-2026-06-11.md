---
title: "AI21 Labs Jamba API 2026: SSM-Transformer 混合架构 + 256K 原生上下文"
description: "AI21 Labs Jamba API 测评：Jamba 1.5 Large（398B）与 Mini（52B）采用 Mamba-Transformer 混合架构，原生 256K 上下文，OpenAI 兼容 API，起价 $0.20/百万 token。"
slug: "ai21-labs-jamba-api-review"
provider: "ai21-labs"
published: false
date: "2026-06-11"
type: "review"
nameCn: "AI21 Labs"
zhTitle: "AI21 Labs Jamba API 2026:SSM-Transformer 混合架构 + 256K 原生上下文"
zhDescription: "AI21 Labs Jamba API 测评:Jamba 1.5 Large(398B)与 Mini(52B)采用 Mamba-Transformer 混合架构,原生 256K 上下文,OpenAI 兼容 API,起价 $0.20/百万 token。"
---

# AI21 Labs Jamba API 2026:把 Mamba-Transformer 混合架构推到生产环境

## 引言:押注非纯 Transformer 路线的特拉维夫团队

2026 年的大多数 LLM API 都建立在纯 Transformer 架构上。AI21 Labs 选了不同方向——Jamba 系列把 Mamba 状态空间模型（SSM）块和 Transformer 自注意力块交错堆叠。结果是一种既保留 SSM 长上下文效率、又具备注意力机制上下文学习能力的模型家族,跑在 OpenAI 兼容 API 后面,定价瞄准生产可用区间。

旗舰 Jamba 1.5 Large 总参 398B（每 token 激活 94B,采用 MoE 式路由）、原生 256K 上下文、输入输出统一定价 $2.00/百万 token。略小的 Jamba 1.5 Mini 总参 52B / 激活 12B,定价 $0.20/百万 token——多数场景下与 GPT-4o-mini 持平,但具备 256K 原生上下文的架构优势。两个模型都跑在 OpenAI 风格的 `/v1/chat/completions` 端点后面,既有工具（LangChain、LlamaIndex、vLLM、OpenAI Python SDK）零代码改造可切。

公司还把 Jamba 分发到三个主流云市场——AWS Bedrock、Azure AI Foundry、NVIDIA NIM——意味着已经在 AWS 或 Azure 花钱的团队,可以在同一张发票上买 Jamba 推理。本文拆解架构、模型矩阵、定价、速度,以及 Jamba 跟 Llama 3.3 70B、GPT-4o-mini、Claude 4.5 的对比。

## Jamba 架构:SSM-Transformer 混合为什么重要

自 GPT-2 以来主流的纯 Transformer 架构在上下文长度上的显存成本是二次的。128K token 时,光 attention 就吃掉 30-50% 的推理预算。256K 时,这个成本复利放大。

Mamba（状态空间模型）块用线性时间序列处理解决这个:显存成本随上下文线性增长,不是二次。代价是纯 SSM 在中段上下文的事实精确检索上偏弱。AI21 的判断（已在 Jamba 论文和实际部署中验证）:把 Mamba 块和较少的 Transformer 注意力块交错堆叠,可以恢复上下文学习能力,同时保留大部分效率收益。

实际效果:Jamba 1.5 Large 处理 256K token 上下文的显存成本,大致等于纯 Transformer 模型处理 128K 时的成本。这对以下场景最有用:

- **长文档摘要**(法律合同、整库代码、科学论文)
- **带代码的多轮对话**(整个文件需要留在上下文)
- **RAG 替代方案**——不用分块+检索,直接把整篇文档喂进去

对目前依赖「分块 → embedding → 检索」流水线以适应 32K 上下文窗口的团队,Jamba 的 256K 窗口是简化这条链路的最直接路径。

## AI21 在售:Jamba 全家桶

AI21 Studio 当前模型目录刻意收窄——5 个模型,全部 Jamba 家族,全部用同一套 SSM-Transformer 架构:

- **Jamba 1.5 Large** — 总参 398B、每 token 激活 94B、256K 上下文。生产长上下文负载的旗舰。
- **Jamba 1.5 Mini** — 总参 52B、每 token 激活 12B、256K 上下文。多数应用的价格性能默认选择。
- **Jamba Large 1.0** — 94B 参数、256K 上下文。1.5 之前的旗舰,仍保留服务以兼容。
- **Jamba Mini 1.0** — 27B 参数、256K 上下文。最初 Mini,仍保留服务。
- **Jamba-Instruct (52B)** — 原始 Mini 的指令微调版,作为 Jamba 1.5 Mini 的基底。

AI21 不像 Together AI、Novita、Fireworks 那样二次托管开源模型。如果你需要特定的 Llama、Qwen、DeepSeek 变体,得找别的厂商。窄也是强——所有工程时间都用于改进 Jamba 家族,而不是维护 200 个社区微调的对接。

## API 形态:OpenAI 兼容 + AI21 特有端点

主 chat API 沿用 OpenAI 形态。能跑在 `api.openai.com` 的请求,换掉 base URL 和 key 就能跑在 AI21 端点上:

```python
import requests
response = requests.post(
    "https://api.ai21.com/studio/v1/chat/completions",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "jamba-1.5-mini",
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 256,
    },
    timeout=30,
)
print(response.json()["choices"][0]["message"]["content"])
```

在 OpenAI 形态之上,AI21 Studio 加了几个平台特有端点:

- **RAG 引擎 (RAG Engine v2)**:托管的文档库,自动分块、embedding、混合搜索。文档通过 AI21 Studio 后台上传,查询走专用 `/v1/rag/query` 端点。适合不想自维护向量库的团队。
- **Tool use API**:结构化函数调用端点,返回针对函数 schema 验证过的 JSON 工具调用结果。
- **JSON mode**:通过 `response_format={"type": "json_object"}` 强制合法 JSON 输出——形态与 OpenAI JSON mode 一致。
- **流式输出**:chat 端点支持 Server-Sent Events,和 OpenAI `stream: true` 一致。

对多数团队来说,chat-completions 端点 + tool use 覆盖 80% 用例。RAG 引擎对需要文档问答又不想自建检索流水线的团队是差异化卖点。

## 定价:Jamba 怎么排位

AI21 定价按 USD/百万 token 计。2026-06-11 价目表:

| 模型 | 输入(每 1M) | 输出(每 1M) | 激活参数 | 上下文 |
|------|------------|------------|---------|-------|
| jamba-1.5-mini | $0.20 | $0.20 | 12B | 256K |
| jamba-1.5-large | $2.00 | $2.00 | 94B | 256K |
| jamba-large-1.0 | $0.50 | $0.50 | 94B | 256K |
| jamba-mini-1.0 | $0.25 | $0.25 | 27B | 256K |

对比参照:Jamba 1.5 Mini 在 $0.20/$0.20 每百万 token,跟 GPT-4o-mini($0.15/$0.60)输入端持平,输出端显著更便宜。对比 Llama 3.3 70B 在 $0.39-$0.88 每百万(看服务商),Jamba 1.5 Mini 在同一负载级别上大约是半价。

Jamba 1.5 Large 在 $2.00/$2.00 比 Llama 3.3 70B 贵,但比 Claude 4.5 Sonnet($3.00/$15.00)便宜,显著低于 GPT-5($5.00/$15.00)。对需要 256K 上下文的团队,Jamba 1.5 Large 是同能力档位里性价比最高的选项。

没有公开的 cache-read 折扣、batch API、或单独的「缓存输入」分级。超高量团队应该走 AI21 sales 通道谈 enterprise 价。

## 速度与延迟

按 AI21 公开 benchmark 和 2026-06-11 截止的独立测速:

- **Jamba 1.5 Mini**:~95 tok/s 输出,TTFT ~140ms(US 端点)
- **Jamba 1.5 Large**:~32 tok/s 输出,TTFT ~340ms
- **Jamba Large 1.0**:~38 tok/s 输出,TTFT ~280ms

Mini 在速度上和 Groq 上的 Llama 3.1 8B(1,250 tok/s)同档——Groq 单模型生产服务更快,但 Groq 不托管带 256K 上下文的模型。Jamba 1.5 Large 在裸 tok/s 上比一线纯 Transformer 模型慢,但 256K 上下文让你在单次请求里发出去的内容,别的厂商要分块或用自家长上下文溢价档。

对长上下文用例来说,真正该看的指标是「每美元每秒处理的上下文 token 数」,不是裸 tok/s。在这个维度上,Jamba 在长文档负载上比 GPT-5 和 Claude 4.5 强——它能一次请求处理整篇文档,其他厂商得分块或上长上下文溢价。

## 免费额度与速率限制

AI21 Studio 2026 年免费档:

- **$10 一次性注册额度**——Jamba 1.5 Mini 大约 5M tokens,Large 大约 1M tokens
- **速率限制**:免费档 60 RPM、60K TPM
- **Pay-as-you-go($5+ 充值)**:500 RPM、100K TPM
- **Enterprise(sales 通道)**:自定义限制、专属推理、多区域故障切换

$10 免费额度是一线闭源厂商里最大的——GPT-5、Claude 4.5、Gemini 2.5 都只给 $5 或更少。原型或评估阶段,AI21 的免费额度足够一个周末同时测 Mini 和 Large。

2026 年在线率持续保持 99.9%+(公开 status page)。最显著的事件是 2026-04-22 的 3 小时部分中断,原因是 AWS US-East-1 部署上的区域 GPU 配置问题;AI21 在 30 分钟内把流量切到 Azure AI Foundry 部署,问题未再出现。

## 云市场分发:Bedrock、Azure AI、NIM

一个值得单独说的功能:AI21 Jamba 同样通过三大云市场分发,意味着团队可以在已有的 AWS 或 Azure 发票上买推理。

- **AWS Bedrock**:`us-east-1`、`us-west-2`、`eu-west-1` 可用。定价与直接 AI21 Studio 一致,但账单走 AWS。
- **Azure AI Foundry**:East US、West Europe、Southeast Asia 可用。同样定价。
- **NVIDIA NIM**:作为自托管容器提供,适合本地部署,按 GPU-小时计费,不是按 token。适合有严格数据驻留要求的团队。

对企业采购团队来说,云市场分发往往是决定性因素——能在已有 AWS 或 Azure 合同下买 AI21 推理,比新开供应商关系简单得多。

## 优缺点

**优点**

- ✅ Jamba 1.5 Large 在 $2/M 提供 256K 原生上下文,比同窗口的 Claude 4.5 或 GPT-5 便宜
- ✅ Jamba 1.5 Mini 在 $0.20/M 与 GPT-4o-mini 和 Llama 3.1 8B 价格持平
- ✅ OpenAI 兼容 API——零 SDK 改造,LangChain/LlamaIndex/vLLM 直连
- ✅ Mamba-Transformer 混合给长上下文负载带来显存效率
- ✅ 通过 AWS Bedrock、Azure AI Foundry、NVIDIA NIM 分发(多云采购)
- ✅ RAG Engine v2——托管文档检索,适合没向量库的团队
- ✅ $10 免费额度(一线闭源厂商里最大)

**缺点**

- ❌ 模型种类窄(只 5 个 Jamba 变体,无 Llama / Qwen / DeepSeek 二次托管)
- ❌ 无国内直连端点——需代理访问中国大陆
- ❌ 无 batch API,无 cache-read 折扣
- ❌ 工具调用可靠性弱于 OpenAI / Anthropic 一线厂商
- ❌ 第三方 benchmark 覆盖(MMLU-Pro、GPQA、HumanEval+)比头部闭源模型薄
- ❌ Jamba 1.5 Large 在裸 tok/s 上比一线 Transformer 模型慢

## 使用场景推荐

| 场景 | 推荐 Jamba 模型 | 理由 |
|------|---------------|------|
| 长文档问答(法律、科学) | jamba-1.5-large | 256K 上下文,$2/M,单次请求可装整篇文档 |
| 长文档摘要 | jamba-1.5-large | 256K 上下文,中段细节高召回 |
| 生产 chatbot(通用) | jamba-1.5-mini | $0.20/M,12B 激活,与 GPT-4o-mini 持平 |
| 代码评审(整个仓库) | jamba-1.5-large | 256K 装下中等代码库,SSM 高效处理长上下文 |
| 带托管文档库的 RAG | jamba-1.5-mini + RAG Engine | AI21 RAG Engine + Mini 是最简配置 |
| 带工具的多轮 Agent | jamba-1.5-mini | OpenAI 兼容,但要验证工具调用输出 |
| 生产函数调用 | gpt-5 或 claude-4.5 | 工具调用可靠性优于 Jamba |
| 成本敏感的批量推理 | jamba-1.5-mini | 一线闭源模型最便宜档 |
| 严格数据驻留 | NVIDIA NIM 自托管 | 在自有数据中心跑 Jamba |

## 横向对比:Jamba vs Llama 3.3 vs GPT-5 vs Claude 4.5

| 厂商 | 最适合 | 上下文 | 起价 | OpenAI 兼容 | 国内访问 |
|------|-------|-------|-----|-----------|---------|
| **AI21 Jamba** | 256K 长上下文,SSM 高效 | 256K | $0.20/M (Mini) | ✅ | ❌ 需代理 |
| **OpenAI GPT-5** | 一线推理,工具调用 | 1M (有限) | $5.00/M (5) | ✅ | ❌ 需代理 |
| **Anthropic Claude 4.5** | 长上下文,谨慎推理 | 1M | $3.00/M (Sonnet) | ✅ | ❌ 需代理 |
| **Meta Llama 3.3 70B**(via Together) | 开源灵活,128K 上下文 | 128K | $0.39-$0.88/M | ✅ | ❌ 需代理 |
| **Google Gemini 2.5 Pro** | 多模态,2M 上下文 | 2M | $1.25/M | ✅ | ❌ 需代理 |
| **FreeModel** | 多厂商聚合,国内直连 | 视模型而定 | 视模型而定 | ✅ | ✅ 直连 |

对需要 256K 上下文 + 最低单 token 价的团队,AI21 Jamba 1.5 Mini 是当前最直接的路径。对同时需要一线推理 + 工具调用可靠性的团队,GPT-5 或 Claude 4.5 胜出不论价格。对国内团队,AI21 没有可用端点——FreeModel 或 SiliconFlow 是答案。

## FAQ

**Q: Jamba 1.5 Mini 和 Jamba 1.5 Large 有什么区别?**

A: 两者都是 SSM-Transformer 混合模型、256K 上下文。Jamba 1.5 Mini 总参 52B / 激活 12B、$0.20/M tokens——价格性能默认选择。Jamba 1.5 Large 总参 398B / 激活 94B、$2.00/M——适合需要更大激活参数量的负载(复杂推理、长上下文召回)。两者架构相同,256K 原生上下文相同。

**Q: Jamba 支持函数调用 / 工具调用吗?**

A: 支持——chat-completions 端点接受 OpenAI 形态的 `tools` 数组,响应里包含结构化 `tool_calls` 字段。输出格式与 OpenAI 兼容,但对带复杂 schema 或多步推理的生产工具调用流水线,Jamba 的工具调用可靠性弱于 OpenAI GPT-5 或 Anthropic Claude 4.5。简单单工具工作流差异可忽略。

**Q: 不通过代理能在中国大陆使用 Jamba 吗?**

A: 不能——AI21 不运营中国直连端点。所有推理都跑在美国或欧盟数据中心,中国流量需要稳定代理或 VPN。对需要国内直连的团队,带大陆端点的 OpenAI 兼容聚合器(如 FreeModel)是可考虑的替代。

**Q: SSM-Transformer 混合架构在 256K 上下文下跟纯 Transformer 模型相比如何?**

A: Mamba 块以线性时间/显存处理大部分上下文,使得 GPU 显存成本大约是同上下文长度纯 Transformer 模型的一半。Transformer 块(在 Jamba 1.5 里约占 1/8 层)恢复纯 SSM 失去的上下文学习能力。在长文档问答和多跳推理 benchmark 上,Jamba 1.5 Large 在长上下文任务上与同激活参数量级纯 Transformer 模型持平或更强。

**Q: AI21 Studio 定价与自购 GPU 跑 Jamba 相比如何?**

A: Jamba 1.5 Mini 在 ~5M tokens/天 以下,AI21 Studio 比直接租 A100 80GB 实例(~每月 $1,500 零售)便宜。Mini 50M tokens/天 以上、Large 5M tokens/天 以上,自建 H100 或 H200 推理就有竞争力。NVIDIA NIM 容器选项让你在自有数据中心跑 Jamba,每 H100 ~$1.99/小时(如果你已经有硬件)。

**Q: AI21 是否保留 API 请求数据用于训练?**

A: 按公开隐私政策,请求数据保留 30 天用于滥用监控,然后删除。除非明确 opt-in,数据不用于训练新模型。企业客户可以通过 sales 通道谈数据驻留条款(数据留在所选区域),或通过 NVIDIA NIM 自托管 Jamba 获得完整数据主权。

**Q: AWS Bedrock 和 Azure AI Foundry 上的 Jamba API 与直接 AI21 Studio 端点相同吗?**

A: 模型行为完全一致。API 形态都是相同的 OpenAI 兼容 `/v1/chat/completions` 端点。主要区别在于账单(AWS 发票 vs Azure 发票 vs AI21 发票)、区域可用性(Bedrock 有 `us-east-1`/`us-west-2`/`eu-west-1`,Azure 有 East US/West Europe/Southeast Asia)、和速率限制默认值(云市场默认每账号额度通常较低,需要时申请配额提升)。

**Q: AI21 Jamba 在多厂商配置中与 FreeModel 相比如何?**

A: FreeModel 是多厂商聚合器,通过一个 key 暴露 OpenAI/Anthropic/Google,带国内直连。AI21 Jamba 是带 SSM-Transformer 优势的单厂商模型家族。一个常见组合是 AI21 Jamba 跑长上下文负载(256K)+ FreeModel 提供 OpenAI/Anthropic 访问和审核路由——FreeModel 可在 freemodel.dev/invite/FRE-7a3b6220 注册,获得托管多厂商配置。

## 结论

对 2026 年需要长上下文 + 合理价格构建 LLM 生产系统的团队,AI21 Jamba 是值得评估的强选项。256K 原生上下文解决了 32K-128K 模型强加的长文档分块-检索痛苦。$0.20/M 的 Mini 价格与 GPT-4o-mini 持平。OpenAI 兼容 API 消除了集成摩擦。Bedrock / Azure AI / NIM 分发让企业采购团队不需要新开供应商关系。

2026 年选模型的决策树:

- 需要 256K 原生上下文 + 最低价格 → **AI21 Jamba 1.5 Mini**
- 需要 256K 原生上下文 + 一线质量 → **AI21 Jamba 1.5 Large**
- 需要一线推理 + 工具调用可靠性 → **GPT-5 或 Claude 4.5**
- 需要开源灵活性(Llama / Qwen / DeepSeek)→ **Together AI 或 Novita AI**
- 需要国内直连 → **FreeModel 或 SiliconFlow**
- 需要多模态(图像、音频、视频)→ **Gemini 2.5 Pro 或 GPT-5**

如果你的团队已经在用 Jamba,想找 OpenAI/Anthropic 访问或审核路由的备份提供商,FreeModel 是天然补充——它把审核路由、OpenAI 兼容 API、多厂商直连接口打包在一个 key 后面。在 freemodel.dev/invite/FRE-7a3b6220 注册,从免费档起步。

## 横向对比表(总结)

| 厂商 | 定价模式 | 最适合 | 国内访问 |
|------|---------|-------|---------|
| **AI21 Jamba** | 输入 $0.20-$2.00/M,输出一致 | 256K 上下文,SSM 高效 | ❌ 需代理 |
| **OpenAI GPT-5** | $5.00-$15.00/M | 一线推理,工具调用 | ❌ 需代理 |
| **Anthropic Claude 4.5** | $3.00-$15.00/M | 长上下文,谨慎推理 | ❌ 需代理 |
| **Meta Llama 3.3 70B** | $0.39-$0.88/M | 开源,128K 上下文 | ❌ 需代理 |
| **Google Gemini 2.5 Pro** | $1.25-$5.00/M | 多模态,2M 上下文 | ❌ 需代理 |
| **FreeModel** | 视模型而定 | 多厂商聚合 | ✅ 直连 |
