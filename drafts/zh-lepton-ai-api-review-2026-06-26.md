---
title: "Lepton AI 2026 测评：区域钉住的 OpenAI API"
description: "Lepton AI 2026 测评：多区域数据驻留的 OpenAI 兼容推理 API。覆盖 AWS 四区域定价、SOC 2 / GDPR / HIPAA 合规、Serverless 与 Dedicated 端点对比。"
slug: "lepton-ai-api-review"
provider: "lepton-ai"
published: true
date: "2026-06-26"
type: "review"
---

# Lepton AI 2026 测评：多区域数据驻留的 OpenAI 兼容推理云

## 引言：Lepton AI 是什么（2026 年）

Lepton AI 是一家面向开发者的 AI 云，核心卖点是把 **OpenAI 兼容的推理 API** 和 **多区域数据驻留（data residency）控制** 结合起来。截至 2026 年 6 月，Lepton 的默认部署区域是 AWS us-west-2（俄勒冈），但客户在创建 workspace 时可以把推理钉在 us-east-1（弗吉尼亚）、eu-west-1（爱尔兰）或 ap-northeast-1（东京）—— 一旦钉住，提示词、模型权重、中间计算结果就再也不会跨区域流出。2026 年，给欧洲银行、日本医疗机构、美国国防承包商做 AI 功能的开发者，第一个要问的问题就是「数据能不能钉在某个 AWS 区域」，Lepton 是少数几个能给干净「可以，这是步骤」答案的 OpenAI 兼容 provider。

平台托管 50+ 开源/专有模型（2026 年中）：Meta Llama 3.3 70B 和 Llama 3.1 405B、Mistral Mixtral 8x22B、阿里 Qwen 2.5 72B、DeepSeek-R1 / V3、Mistral Large 2、Stability AI 的 Stable Diffusion 3.5 Large、Black Forest Labs 的 FLUX.1（图像生成）、OpenAI 的 Whisper Large V3（音频转录）、BAAI 的 BGE-M3 / BGE-Large（embedding）。API 表面是 OpenAI `/v1/chat/completions` 和 `/v1/images/generations` 端点的严格超集 —— 同样的 JSON schema、同样的流式协议、同样的 `tools` 参数做 function calling。已经在生产用 OpenAI SDK 的团队，只需改 `base_url` 和 API key 就能切到 Lepton，应用层零重构。

Lepton 在 2026 年的市场定位很具体：它 **不是最便宜** 的推理 provider（Together AI、Fireworks AI、Groq 在主流模型上 token 单价都比它低），也 **不是模型最多** 的（OpenRouter 列出 300+，Lepton 列出 50+）。它最准确的标签是「**最懂企业区域合规 + OpenAI 兼容**」的那个。如果你的项目未来要过企业安全评审，从第一天就用 Lepton，可以省掉后面 Together AI / Fireworks AI / OpenRouter 一定会撞上的那类问题（"这个 vendor 在哪个区域部署我们的数据"）。

这篇测评从 2026 年中评估 Lepton 的工程师视角写：数据驻留实际如何落地、Serverless vs Dedicated 端点定价如何权衡、OpenAI 兼容性在生产里的行为、区域目录差异（东京和爱尔兰不全模型）、以及 Lepton 和 Together AI / Fireworks AI / AWS Bedrock / Azure OpenAI 在「区域钉住」需求上的对比。

## 多区域数据驻留：核心差异化

定义 Lepton 2026 年市场位置的那个特性是 **明确的区域钉住 + 数据驻留保证**。具体来说：

**创建时选区域。** 新建 Lepton workspace 时，选主区域：`aws-us-west-2`（俄勒冈）、`aws-us-east-1`（弗吉尼亚）、`aws-eu-west-1`（爱尔兰）、`aws-ap-northeast-1`（东京）。这个选择是粘性的，workspace 生命周期内不变，也不能后期迁移到别的区域。需要同时在两个区域推理，就建两个 workspace。

**数据不出区域。** 所有推理流量 —— 请求 payload、prompt、模型输出、中间 activations、缓存的 KV state —— 全部在你选的 AWS 区域处理。数据不复制到其他区域、不备份到多区域 bucket、不传给 Lepton 总部（总部在加州 Palo Alto，但这跟数据无关，数据就在你选的 AWS 区域里）。

**合规范围。** 推理路径 SOC 2 Type II、GDPR、HIPAA 合规都已经审计并出报告。欧洲客户走 GDPR 时，Lepton 签标准 DPA（数据处理协议），用 `eu-west-1` 推理就把数据留在欧洲经济区（EEA）—— 这是 2025 年之后任何面向欧盟用户的生产 AI 功能的关键合规项。

**哪些 **不** 钉区域。** 计费元数据、Lepton web console、账户级审计日志、技术支持工单 —— 这些都走美国处理，不管你选哪个推理区域。如果你的威胁模型要求连计费数据都不出区域，那就走 Lepton 的 Dedicated Enterprise 私有部署（见下文定价），或者自托管到 AWS 自己账户里。

对 2026 年大多数企业客户来说，「区域钉住的推理」就是核心要求，「美国处理的计费 / console」是可接受的让步。只有一小撮客户（典型是欧盟 PSD3 / DORA 监管下的金融机构、美国国防 ITAR 下的工作负载）必须用 Dedicated Enterprise 单租户部署才能满足完整数据处理模型。

## Serverless GPU vs Dedicated 端点定价

Lepton 推理有 2 种计费模式，选哪个取决于你的流量模式。

**Serverless GPU。** 按 token 计费，从 Lepton 预付余额里扣。2026 年 6 月价格：

| 模型 | Input（$/M tokens） | Output（$/M tokens） |
|---|---|---|
| Llama 3.3 70B | $0.80 | $0.80 |
| Llama 3.1 405B | $3.50 | $3.50 |
| Qwen 2.5 72B | $0.80 | $0.80 |
| DeepSeek-R1 | $2.00 | $2.00 |
| Mixtral 8x22B | $0.90 | $0.90 |
| Mistral Large 2 | $2.00 | $2.00 |

这个价格是「有竞争力但不领先」。Together AI Llama 3.3 70B 收 $0.90/M、Fireworks AI 收 $0.90/M、Groq 收 $0.59/M（同一模型）。Lepton 的 $0.80/M 处于中游。为啥多付这点溢价？答案就是数据驻留保证 —— 如果你不需要这个，选用更便宜的 provider。

**Dedicated 端点。** 预留 GPU 实例（H100、A100、或者 Lepton 自研的 HD 4000 推理优化芯片），月付或小时付承诺，Lepton 在这台实例上给你 host 模型。2026 年 6 月价格：

| 硬件 | 小时 | 月付（24/7） | 典型场景 |
|---|---|---|---|
| 1× A100（80GB） | $1.80 | $1,100 | 7B-13B 模型，50-100 req/s |
| 1× H100（80GB） | $4.50 | $2,800 | 70B 模型，30-60 req/s |
| 1× HD 4000 | $6.20 | $3,800 | 70B 模型，80-120 req/s（比 H100 推理更快） |
| 8× H100（cluster） | $32.00 | $20,000 | 405B 模型，20-40 req/s |

Dedicated 端点定价是 Lepton 真正有意思的地方。稳态超过 ~50 req/s 的 70B 工作负载，Dedicated 比 Serverless 便宜 40-60%。盈亏平衡点大概是 70B 模型每天 116M tokens 以上 —— 低于这个量级 Serverless 更划算（不为闲置付钱）。

Dedicated 端点还给你 **可预测的延迟**（无冷启动、不跟其他客户争抢硬件）和 **托管自定义微调模型**（你上传一个微调过的 Llama / Qwen checkpoint，Lepton 帮你 host 在 dedicated GPU 上）。对 p99 延迟有严格要求的生产工作负载，Dedicated 是唯一正确选择。

**免费层。** 注册送 $5 Lepton 信用额，30 天有效。够跑 6M tokens 的 Llama 3.3 70B（3M input + 3M output）—— 够做 API 评估和小型 benchmark，不够生产。Together AI 给 $1 初始信用额、Groq 给永不过期的免费模型开发 tier、GitHub Models 给每日配额 —— Lepton 的免费层是主流 provider 里最小的，但 30 天有效期对一个评估周期来说够用。

## OpenAI 兼容性：API 表面有多接近

Lepton API 是 OpenAI 的 chat completions 端点，区别只在 `Authorization: Bearer ***（用 Lepton API key 不用 OpenAI key）、`base_url=https://api.lepton.ai/v1` 不用 `api.openai.com/v1`。截至 2026 年 6 月，下面这些特性用标准 OpenAI client 不用改就能跑：

- **Chat completions**，system / user / assistant 消息
- **Streaming** 用 `stream=True`（SSE 协议，chunk 格式跟 OpenAI 一致）
- **Function calling** 用 `tools` 参数（JSON schema tools，`tool_calls` 响应格式跟 OpenAI 一致）
- **JSON mode** 用 `response_format: { type: "json_object" }`
- **Vision input** 用 image_url content part（目录里的 VLM 都支持）
- **temperature / top_p / frequency_penalty / presence_penalty / stop sequences** 全部标准
- **n>1 sampling** 并行 completion
- **logprobs** 拿到 token 级置信度（自评估循环很好用）

哪些 **不** 支持 / 有 caveat：

- **Assistants API**（OpenAI 的有状态 threads/assistants/runs 抽象）—— Lepton 没实现。如果你的代码用 `client.beta.assistants.*`，需要重构成纯 chat completions。
- **Fine-tuning API**（OpenAI 的 `client.fine_tuning.jobs.*`）—— Lepton 通过 web console 提供微调（上传 JSONL 数据集、指向基础模型、按训练时长付费），但没提供 OpenAI 兼容的 API。微调后的模型仍然可以用标准 `/v1/chat/completions` 端点调用。
- **Batch API**（OpenAI 的 50% 折扣、24h SLA 批量端点）—— Lepton 有类似的异步 batch 端点 `https://api.lepton.ai/v1/batches`，但折扣结构和 SLA 不同（典型是 30% 折扣、6h SLA 适用于 10M tokens 以下的批量）。
- **Realtime API**（OpenAI 的 WebSocket 语音流）—— 没实现。语音用 Whisper Large V3，走标准的 chat completions 风格音频端点。

代码迁移是机械的。典型 OpenAI Python SDK 切换长这样：

```python
import openai

# OpenAI
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
resp = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "你好"}],
)

# Lepton（drop-in 替换）
client = openai.OpenAI(
    api_key=os.environ["LEPTON_API_KEY"],
    base_url="https://api.lepton.ai/v1",
)
resp = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "你好"}],
)
```

同样的模式对 OpenAI JavaScript / Go / Java / Rust SDK 都成立。模型名用扁平命名（`llama-3.3-70b`、`qwen-2.5-72b`、`deepseek-r1`），不用 OpenAI 那种 `vendor/model` 前缀 —— Lepton 目录策展度足够高，光模型名就不歧义。

## 区域目录：每个区域有哪些模型

不是每个区域都全模型。2026 年 6 月目录大致这样：

| 模型 | us-west-2（默认） | us-east-1 | eu-west-1 | ap-northeast-1 |
|---|:---:|:---:|:---:|:---:|
| Llama 3.3 70B | ✅ | ✅ | ✅ | ✅ |
| Llama 3.1 405B | ✅ | ✅ | ✅ | ❌ |
| Qwen 2.5 72B | ✅ | ✅ | ✅ | ✅ |
| DeepSeek-R1 | ✅ | ✅ | ❌ | ❌ |
| Mixtral 8x22B | ✅ | ✅ | ✅ | ✅ |
| Mistral Large 2 | ✅ | ✅ | ✅ | ✅ |
| Stable Diffusion 3.5 Large | ✅ | ✅ | ✅ | ✅ |
| FLUX.1 | ✅ | ✅ | ✅ | ✅ |
| Whisper Large V3 | ✅ | ✅ | ✅ | ✅ |
| BGE-M3 / BGE-Large | ✅ | ✅ | ✅ | ✅ |

405B 模型和 DeepSeek-R1 截至 2026 年 6 月只在美国区域 —— 反映了 Lepton 跟 Meta / DeepSeek 的许可安排。如果你的工作负载需要这两个模型之一、又需要 EU 数据驻留，必须二选一：降到 Llama 3.3 70B（在 EU 可用）、或者接受美区推理并在应用层绕开数据驻留要求（比如发请求前剥离 PII、接受非敏感工作负载走这个数据流）。这是真实限制，也是欧洲企业安全评审一眼会盯上的事。

东京（`ap-northeast-1`）跟 EU 一样有 70B 档位，但缺 405B 和 DeepSeek-R1。如果你在为日本客户做 70B 模型的日本区数据驻留项目，Lepton 站位很稳。如果要 405B 在日本，请看 Dedicated Enterprise 档位或等目录扩展。

## 什么时候该选 Lepton AI 而不是其他 provider

2026 年 Lepton 的正确框架不是「它是不是最好的推理 provider」而是「数据驻留保证值不值得为我的工作负载多付一点溢价」。值得的场景：

**有 GDPR 义务的欧洲企业。** 推理必须留在 EU，Lepton 的 `eu-west-1` 区域加签名 DPA 就满足。Together AI / Fireworks AI 主力都在美区、EU 数据驻留故事弱。AWS Bedrock 也支持 EU 区域，但需要 AWS 账户、IAM 配置、学习曲线比 Lepton 的 workspace 模型陡。

**有 APPI / METI 要求的日本医疗。** 同理，`ap-northeast-1` 把数据留在日本。日本 AI 推理市场被 Sakura Internet、GCP Tokyo、AWS Bedrock 主导，Lepton 是想要 OpenAI 兼容 API 又不想啃 AWS console 的团队的第四个可信选项。

**有 CMMC / FedRAMP 目标的美国国防 / 联邦承包商。** 截至 2026 年 6 月，Lepton 还没拿到 FedRAMP Moderate 或 High 授权，所以不能作为 FedRAMP 必需工作负载的推理后端。对 CMMC Level 2/3 承包商，Dedicated Enterprise 单租户部署是路径。如果你是早期国防 AI 创业公司还没 FedRAMP 要求，Lepton 的美区钉住是起步，未来可以扩。

**多区域冗余。** 服务全球客户、需要在 3+ 区域推理的团队（比如美、欧、日），可以跑 3 个 Lepton workspace、应用层路由流量。OpenAI 兼容 API 让这个路由变 trivial —— 每个请求改 `base_url` 就行，不用改 SDK。

**不**值得、应该用更便宜 / 更简单 provider 的场景：

**还没客户的前期原型。** 用 Together AI 或 Groq。每 token 便宜 20-30%，数据驻留的事等真有客户问再说。

**超大批量工作负载（单模型每月 10B+ tokens）。** 直接跟 Lambda Labs / CoreWeave / AWS 谈 dedicated GPU 合约。Lepton dedicated 端点有竞争力，但 Lambda / CoreWeave 在超大量级绝对价格更优。

**需要 GPT-5.5 或 Claude Opus 4.5 的闭源模型工作负载。** Lepton 不 host OpenAI 或 Anthropic 模型（许可问题）。需要 GPT-5.5 或 Claude 就直接调上游 vendor API、或者走 OpenRouter 路由。

## 对比：Lepton AI vs Together AI / Fireworks AI / AWS Bedrock / Azure OpenAI

**Together AI。** 模型目录略大（200+），主流模型价格略低，但没有正式数据驻留保证 —— 推理跑在 Together 美区 GPU 集群，没法钉到特定区域。价格敏感的开源模型工作负载选 Together，要区域钉住选 Lepton。

**Fireworks AI。** 规模相当、价格相近。Fireworks 的 Firefunction-v2 是 function-calling 密集 agent 的独特强项，但 Fireworks 的 EU 数据驻留比 Lepton 弱（EU 区域可用但目录薄）。Agent 工作负载选 Fireworks，区域钉住选 Lepton。

**AWS Bedrock。** 最企业成熟的选项 —— 完整 AWS IAM 集成、AWS 持有的所有合规认证、30+ AWS 区域钉住。代价是 AWS console 和 IAM 学习曲线，以及 Bedrock 的模型目录由 AWS 策展（不是更广义的开源生态）。已经在 AWS 上跑的大企业选 Bedrock；想要开发者友好 console 和 OpenAI 兼容、不想被 AWS 绑定的团队选 Lepton。

**Azure OpenAI。** 如果你需要 GPT-5.5 或 OpenAI o 系列模型带 EU 数据驻留，这是唯一选项。Azure 有 EU 区域、正式 GDPR 合规、完整 OpenAI 目录。代价是 Azure 生态（Entra ID、Azure portal、Azure 计费），以及你只能拿到 OpenAI 模型 —— 没有 Llama、Qwen、DeepSeek。EU 区要 GPT-5.5 选 Azure，EU 区要开源模型选 Lepton。

**OpenRouter。** 跨 20+ provider 聚合 300+ 模型的聚合器。OpenRouter 的智能路由会挑最便宜的 provider 来 host 给定模型，per-token 价格最优。OpenRouter 没有数据驻留保证 —— 你的 prompt 被路由到 OpenRouter 挑的任意 provider，可能是个美区集群。价格优化选 OpenRouter，数据驻留选 Lepton。

## 优缺点

**优点**

- 4 个 AWS 区域（us-west-2、us-east-1、eu-west-1、ap-northeast-1）多区域数据驻留，明确数据钉住保证
- OpenAI 兼容的 chat completions、function calling、streaming、vision、JSON mode —— 从 OpenAI SDK drop-in 迁移
- Serverless GPU + Dedicated 端点双模式：稳态量级走 Dedicated 节省 40-60%
- 50+ 开源和专有模型，覆盖 chat、code、vision、image generation、audio、embedding
- 推理路径 SOC 2 Type II + GDPR + HIPAA 审计并出报告
- Dedicated Enterprise 档位为高合规工作负载提供单租户部署
- H100 / A100 / HD 4000 GPU cluster 可按小时或按月租
- 30 天 $5 免费信用额 —— 够评估完整 API 表面

**缺点**

- 50+ 模型比 OpenRouter（300+）和 Together AI（200+）少
- 主流模型 per-token 价格比 Together AI / Fireworks AI / Groq 高 5-30%
- 免费信用额比 Groq / GitHub Models 小（这两个给每日配额）
- 405B Llama 和 DeepSeek-R1 截至 2026 年 6 月在 EU / JP 区域不可用
- 不 host 闭源模型（GPT-5.5、Claude Opus 4.5）—— 许可限制
- 中国访问需要代理（虽然有 ap-northeast-1 区域，跨境延迟高）
- 没有 realtime WebSocket API（没有 OpenAI Realtime 等价物）
- 没有正式 FedRAMP 授权 —— 国防工作负载需要 Dedicated Enterprise 档位
- 平台比 Together AI / Fireworks 小；长期 SLA 待观察

## 常见问题

**Q: Lepton AI 真的把推理数据留在我选的那个区域吗？**
A: 是的。在 `eu-west-1` 创建 workspace 之后，推理流量、prompt、输出、中间 KV cache 全部留在 AWS eu-west-1（爱尔兰）。数据不复制到其他区域、不传到 Lepton 美国总部、不用于模型训练。计费元数据、web console、技术支持工单走美国处理 —— 对更严格的数据模型，用 Dedicated Enterprise 档位的单租户部署。

**Q: Lepton AI 跟 AWS Bedrock 在 EU 数据驻留上怎么比？**
A: 两者都提供 EU 区域推理 + GDPR 合规。AWS Bedrock 区域更多（30+ 对 Lepton 的 4 个）、AWS IAM 集成更深，但 AWS console 和 IAM 学习曲线更陡。Lepton 有开发者友好 console、OpenAI 兼容 API、50+ 模型全部 OpenAI SDK 兼容。已经在 AWS 上跑的企业选 Bedrock 自然；想要 OpenAI 兼容 + 快速 workspace 模型的团队选 Lepton 上手更快。

**Q: 能用 OpenAI Python SDK 调 Lepton AI 吗？**
A: 能。设置 `base_url="https://api.lepton.ai/v1"` 和 `api_key=<你的 Lepton API key>`。模型名用 `llama-3.3-70b`、`qwen-2.5-72b`、`deepseek-r1` 这种。Streaming、function calling、JSON mode、vision、tool calls 全部不用改就能跑。OpenAI JavaScript / Go / Java / Rust SDK 同样能用。

**Q: Dedicated 端点 vs Serverless GPU 定价怎么比？**
A: Serverless GPU 按 token 计费 —— Llama 3.3 70B input $0.80/M、output $0.80/M。Dedicated 端点预留 GPU 实例（H100 $4.50/小时或 $2,800/月）独占 host 模型。Llama 3.3 70B 每天 116M tokens 以上 Dedicated 比 Serverless 划算。Dedicated 还给你可预测的 p99 延迟、无冷启动、能 host 自定义微调模型。

**Q: Lepton AI host 闭源模型比如 GPT-5.5 或 Claude Opus 4.5 吗？**
A: 不 host。Lepton 被授权 host 开源和宽松许可模型（Llama、Qwen、DeepSeek、Mistral、FLUX、Stable Diffusion、Whisper、BGE），不 host OpenAI 或 Anthropic 闭源模型。需要 GPT-5.5 或 Claude Opus 直接调上游 vendor API，或者走 OpenRouter 聚合。

**Q: Lepton AI 是 SOC 2 合规吗？**
A: 是 —— Lepton SOC 2 Type II 已审计，报告 NDA 下可拿。Lepton 也 GDPR 合规（欧盟客户 DPA 可签）、HIPAA 合规支持医疗工作负载。截至 2026 年 6 月，Lepton 还没拿到 FedRAMP Moderate 或 High 授权 —— 国防 / 联邦工作负载需要 Dedicated Enterprise 档位的单租户部署。

**Q: 后面要加区域怎么办？**
A: workspace 不能从一个区域迁到另一个。要加区域就建新 workspace 然后在应用层路由流量。OpenAI 兼容 API 让这件事很机械 —— 每个请求改 `base_url`。需要 3 个区域同时在线的工作负载，维护 3 个 workspace 和 3 个 API key。

**Q: Lepton AI 在中国能用吗？**
A: 不能直连。Lepton 的 ap-northeast-1（东京）区域地理上近，但中国客户端仍需代理才能到 AWS Tokyo 端点，跨境延迟比真正的中国直连 provider 多 100-200ms。要中国直连 AI 推理请看阿里云百炼、百度文心一言、Kimi、智谱 GLM、腾讯混元、字节豆包（都在 apirank 国内分类下）。

## 结论

Lepton AI 是 2026 年需要把推理数据钉在特定 AWS 区域的团队的最强 OpenAI 兼容推理 provider。4 区域覆盖（us-west-2、us-east-1、eu-west-1、ap-northeast-1）+ 明确的数据钉住保证是核心差异化。OpenAI 兼容性是真的 —— chat completions、function calling、streaming、vision、JSON mode 全部不用改就能跑。Serverless vs Dedicated 定价模型给团队一个从原型（Serverless、按 token 付）到生产（Dedicated、稳态便宜 40-60%）的清晰迁移路径。

诚实地说限制：50+ 模型目录比 OpenRouter 或 Together AI 小，405B 和 DeepSeek-R1 截至现在在 EU/JP 区域还没上线，不 host 闭源模型（无 GPT-5.5、无 Claude Opus 4.5）。免费信用额比 Groq 每日免费 tier 或 GitHub Models 每日配额小。纯价格优化 Together AI / Fireworks AI / Groq 还是更便宜。数据驻留场景下，Lepton 是最干净的答案。

最自然的一对是 Lepton AI 作为「**生产级区域钉住层**」叠在 GitHub Models 这种原型 stack 之上。原型阶段用 GitHub Models（免费、OpenAI 兼容、目录广），生产流量切到 Lepton（付费、区域钉住、SOC 2 / GDPR / HIPAA）。想要一个聚合器同时覆盖原型和生产的团队，OpenRouter 是更灵活的聚合器 —— 但你放弃数据驻留保证。

**2026 年给大多数企业团队的建议**：如果你的客户安全评审会问「数据住哪儿」而且答案必须是具体 AWS 区域，Lepton AI 是正确的推理后端。去 `lepton.ai` 注册，在目标区域建 workspace，把现有 OpenAI SDK 调用通过改 `base_url` 和 `api_key` 迁过来。30 天 $5 免费信用额够对生产模型做一个完整的评估周期。

---

Source: Lepton AI 文档（`lepton.ai/docs`）、Lepton AI 定价页（2026 年 6 月）、AWS 区域可用性列表、SOC 2 Type II 鉴证摘要、GDPR DPA 模板、多区域数据驻留模式社区报告。对照当前 Lepton API 和 OpenAI SDK v1.x 兼容性审核。
