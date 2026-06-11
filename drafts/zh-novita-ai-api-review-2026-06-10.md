---
title: "Novita AI API 测评 2026：200+ 开源模型，从 $0.06/百万 token 起"
description: "Novita AI API 完整测评：200+ 托管开源模型（Llama 3.3 70B、Qwen2.5-72B、DeepSeek-R1），OpenAI 兼容 API，国内直连 cn.novita.ai，价格从 $0.06/百万 token 起。"
slug: "novita-ai-api-review"
provider: "novita-ai"
published: true
date: "2026-06-10"
type: "review"
---

# Novita AI API 2026：新加坡+国内双基础设施的 200+ 开源模型平台

## 引言：从 GPU 云到 LLM 推理的转型

2023 年的 Novita AI 还只是新加坡的一家小 GPU 云厂商，按小时出租 A100 和 H100 实例。到 2025 年，公司在统一推理 API 上接入了 200+ 开源 LLM，开通了独立国内直连端点 `cn.novita.ai`，开始和 Together AI、Fireworks、SiliconFlow 正面竞争开源模型推理市场。

卖点很直接：值得调用的所有开源 LLM——Llama 3.3 70B、Qwen2.5-72B、DeepSeek-R1、Mistral-Nemo、Gemma 2 27B——都在同一个 OpenAI 兼容 API 上，价格比 Together AI 在大多数模型上便宜 30-50%，并为国内用户提供独立的低延迟端点。入门价 $0.06/百万 token（Llama 3.1 8B）是市场上最低之一。

这个平台不是 OpenAI/Anthropic 的完美替代品——Novita 没有托管 GPT-5、Claude 4.8 或 Gemini 2.5，公司在 GPU 云和中文开发者圈之外的认知度还在建设。但对于需要调用 200+ 开源模型、定价可预测、用一个 OpenAI 形态端点的团队来说，Novita AI 是 2026 年最有力的选项之一。本文将梳理它的 API 接口、价格、速度基准、国内访问，以及和 FreeModel、Together AI、Fireworks、SiliconFlow 的对比。

## Novita AI 究竟托管了哪些模型

模型目录覆盖了完整的开源版图。占据列表页的主要类别：

- **Meta Llama 系列**：Llama 3.3 70B Instruct、Llama 3.1 405B Instruct、Llama 3.1 70B、Llama 3.1 8B（base 和 instruct 两个变体）。
- **Qwen 系列**：Qwen2.5-72B-Instruct、Qwen2.5-Coder-32B-Instruct、Qwen2.5-7B-Instruct，以及用于长上下文的 Qwen2.5-Plus。
- **DeepSeek 系列**：DeepSeek-V3、DeepSeek-R1（满血 671B）、DeepSeek-Coder-V2、DeepSeek-Chat。
- **Mistral 系列**：Mistral-Nemo、Mistral-7B-Instruct-v0.3、Mixtral-8x7B-Instruct、Mistral-Large-2。
- **Google Gemma 系列**：Gemma 2 27B IT、Gemma 2 9B IT、CodeGemma 变体。
- **视觉模型**：LLaVA、Qwen-VL、CogVLM、InternVL，用于多模态场景。
- **Embedding 模型**：BGE-M3、BGE-Large、mxbai-embed-large，以及 Cohere 的英文/中文变体。

除了标准目录，Novita 还支持自定义模型部署——你可以上传一个私有 Hugging Face 模型，通过同一个 API 接口服务，按 GPU 小时计费。部分基础模型支持 LoRA 微调。

目录比 Together AI 略广（200+ vs 200+），但没有 SiliconFlow 那种精挑细选。如果想要 Hugging Face 上的某个特定社区微调，Novita 命中的概率更高。

## API 接口：兼容 OpenAI，附加自定义端点

主 API 端点遵循 OpenAI 的 `/v1/chat/completions` 和 `/v1/embeddings` 规范。能在 `api.openai.com` 上跑的请求，换个 base URL 和 key 就能在 Novita 上跑：

```python
import requests
response = requests.post(
    "https://api.novita.ai/v3/openai/chat/completions",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "meta-llama/llama-3.3-70b-instruct",
        "messages": [{"role": "user", "content": "你好"}],
        "stream": False,
    },
    timeout=30,
)
print(response.json()["choices"][0]["message"]["content"])
```

这种 OpenAI 兼容性意味着现有工具——LlamaIndex、LangChain、OpenAI 官方 Python SDK、vLLM，甚至 AutoGen——都只需要改 base URL 就能对接 Novita。不用换 SDK。

在 OpenAI 规范之上，Novita 还提供了一些平台专属端点：

- **Serverless GPU 端点**：60 秒内创建一个按需 GPU 实例跑自定义模型，只对实例活跃时间付费。
- **独立 GPU 租赁**：预订 A100、H100 或 H200 实例用于持续负载（按小时计费，无推理加价）。
- **LoRA 微调 API**：从 dashboard 训练 base 模型的 LoRA adapter，通过同一个 OpenAI 兼容端点部署。
- **图像生成**：Stable Diffusion XL、SD3、Kolors、Playground v2.5。
- **音频端点**：Whisper large-v3 做 STT，CosyVoice 和 Bark 做 TTS。

对大部分团队来说，chat-completions 端点是日常主力。Serverless GPU 是目录中没有的模型负载场景下的独特卖点。

## 价格：数字对照

Novita 用美元计费，按百万 token 结算。2026-06-10 的热门模型价目表：

| 模型 | 输入（每百万 token） | 输出（每百万 token） | 备注 |
|-------|----------------------|------------------------|-------|
| meta-llama/llama-3.1-8b-instruct | $0.06 | $0.06 | 最便宜一档，批量负载 |
| meta-llama/llama-3.3-70b-instruct | $0.39 | $0.39 | 生产聊天默认选择 |
| meta-llama/llama-3.1-405b-instruct | $1.52 | $1.52 | 前沿开源 |
| qwen/qwen-2.5-72b-instruct | $0.29 | $0.29 | 中文能力很强 |
| qwen/qwen-2.5-coder-32b-instruct | $0.18 | $0.18 | 编程任务 |
| deepseek/deepseek-v3 | $0.18 | $0.18 | 聊天主力 |
| deepseek/deepseek-r1 | $0.30 | $0.30 | 满血 671B 推理 |
| mistralai/mistral-nemo | $0.09 | $0.09 | 多语言 |
| google/gemma-2-27b-it | $0.16 | $0.16 | 轻量生产 |
| meta-llama/llama-3.3-70b-instruct (cn.novita.ai) | ¥2.0 | ¥2.0 | 国内直连，人民币结算 |

对照来看，Together AI 的 Llama 3.3 70B 按 $0.88/$0.88 百万 token 计费，是 Novita 同模型价格的 2 倍多。Fireworks AI 接近持平（$0.45/$0.45），但仍然比 Novita 贵。Llama 3.1 8B 的 $0.06/1M 是头部 OpenAI 兼容厂商里最低的入门价。

对国内团队，`cn.novita.ai` 是相关端点，按人民币结算，价格表和 SiliconFlow 接近。和 SiliconFlow 比，Novita 的目录更广（更多社区微调、更多 embedding 选项），但国内直连端点更新、稳定性还在积累。

## 速度基准

延迟数据因模型、地区、时段而异。根据 Novita 2026-06-10 公开的基准和独立测试：

- **Llama 3.1 8B**：输出约 120 tok/s，TTFT 约 90ms（新加坡端点）
- **Llama 3.3 70B**：输出约 55 tok/s，TTFT 约 210ms
- **Llama 3.1 405B**：输出约 22 tok/s，TTFT 约 480ms
- **Qwen2.5-72B**：输出约 48 tok/s，TTFT 约 230ms
- **DeepSeek-R1 (671B)**：输出约 25 tok/s，TTFT 约 1.1s
- **Mistral-Nemo**：输出约 95 tok/s，TTFT 约 120ms

对照来看，Groq 在 Llama 3.1 8B 上达到 1,250 tok/s，Cerebras 达到 2,000+ tok/s——两者在同模型上明显快过 Novita。代价是广度：Novita 托管 200+ 模型，Groq 和 Cerebras 各只托管 5-10 个。如果只追求原始速度，Groq 或 Cerebras 胜出。如果生产环境要在 20 个不同模型之间切换，Novita 的广度很难被替代。

`cn.novita.ai` 端点对国内用户比任何海外端点快 50-80ms，但比纯国内厂商（如 SiliconFlow）慢一些。

## 可靠性和配额

Novita API 2026 年公开的限速：

- **免费层**：60 RPM，10K TPM（每分钟）
- **按量付费（$10+ 充值）**：500 RPM，100K TPM
- **企业（销售对接）**：自定义限速，独立推理，BYOC 选项

2026 年正常运行时间稳定在 99.9%+（根据公开状态页）。最显著的事故是 2026-03-18 一次 4 小时局部故障，由上游 H100 供应问题导致；无数据丢失，事故后 30 天内公司加上了多区域 failover。

免费层是头部 OpenAI 兼容厂商里最弱的——只有一次性 $0.5 额度。SiliconFlow 给出 ¥1-200 活动额度，Together AI 给出 $5（所有新账号），Groq 给出 14,400 请求/天。Novita 的免费层适合一个周末的原型开发，不适合长期开发工作。实际的付费入门门槛是 $10 充值。

## 国内访问：cn.novita.ai

对国内开发者，`cn.novita.ai` 端点是最重要的功能。这个端点由独立的国内实体运营，持有 ICP 备案的基础设施，按人民币计费，与国内三大运营商（中国电信、中国联通、中国移动）有直连对等。北京或上海服务器到 cn.novita.ai 的延迟通常在 30ms 以内。

`cn.novita.ai` 的目录略小于全球端点（160+ 模型 vs 200+），重点放在 Qwen、DeepSeek、GLM、Yi 等国内开发的模型上，这些在国内最受欢迎。Llama 和 Mistral 可用，但价格和全球端点一致。

主要限制：国内端点和全球端点的 API key、计费、限速是分开的。在国内外都有业务的团队需要管理两个账号。

## 优缺点

**优点**

- ✅ 头部 OpenAI 兼容厂商中最低的入门价（Llama 3.1 8B $0.06/百万 token）
- ✅ 200+ 托管开源模型，目录比 Together/Fireworks 更广
- ✅ OpenAI 兼容 API——无 SDK 改造
- ✅ 国内直连端点（cn.novita.ai），人民币计费，ICP 备案基础设施
- ✅ Serverless GPU + 独立 GPU 租赁支持自定义模型部署
- ✅ 部分基础模型支持 LoRA 微调 API

**缺点**

- ❌ 不托管闭源模型（GPT-5、Claude 4.8、Gemini 2.5）
- ❌ 免费层小（一次性 $0.5 额度）——比 Groq、Together、SiliconFlow 都弱
- ❌ 速度有竞争力但同模型上比 Groq 和 Cerebras 慢
- ❌ Function calling 可用但工具调用保证弱于 OpenAI/Anthropic
- ❌ 国内和全球端点是分开的账号/key/计费
- ❌ API 等级无公开的 SOC2 或 ISO27001 认证

## 使用场景推荐

| 使用场景 | Novita 推荐模型 | 理由 |
|----------|----------------|------|
| 生产聊天机器人（英文） | llama-3.3-70b-instruct | $0.39/1M，通用质量强 |
| 生产聊天机器人（中文） | qwen-2.5-72b-instruct (cn.novita.ai) | ¥2/1M，原生中文，ICP 直连 |
| 代码生成 | qwen-2.5-coder-32b-instruct | $0.18/1M，代码优化 |
| 推理 / 数学 / 逻辑 | deepseek-r1 | $0.30/1M，满血 671B 推理 |
| 长上下文摘要 | llama-3.1-405b-instruct | 128K 上下文，$1.52/1M |
| 批量 embedding | bge-m3 | $0.02/1M token，SOTA |
| 自定义私有模型 | serverless GPU 端点 | 60 秒部署任意 HF 模型 |
| 视觉 / 图像理解 | llava-onevision-qwen2-7b-ov | 原生多模态，$0.18/1M |
| 语音助手（STT+TTS） | whisper-large-v3 + cosyvoice | 一个厂商覆盖 STT + TTS |

## 对比：Novita AI vs FreeModel vs Together AI vs SiliconFlow

| 厂商 | 最适合 | 国内访问 | 入门价 | 模型数 | OpenAI 兼容 |
|----------|----------|--------------|-------------|--------|-------------------|
| **Novita AI** | 200+ 开源模型，最低单价 | ✅ 直连（cn.novita.ai） | $0.06/1M tok | 200+ | ✅ |
| **FreeModel** | 多厂商聚合，内置审核路由 | ✅ 直连 | 因模型而异 | 50+ | ✅ |
| **Together AI** | 美欧生产部署 200+ 开源 | ❌ 需代理 | $0.18/1M tok | 200+ | ✅ |
| **SiliconFlow** | 国内开源模型（Qwen/DeepSeek/GLM） | ✅ 直连 | ¥0.4/1M tok | 100+ | ✅ |
| **Fireworks AI** | 100+ 开源模型快速推理 | ❌ 需代理 | $0.20/1M tok | 100+ | ✅ |
| **DeepSeek（官方）** | DeepSeek 官方直供 | ✅ 直连 | ¥1/1M tok | 15+ | ✅ |

对于需要 200+ 开源模型 + 最低单价 + 国内直连的团队，Novita AI 目前是最直接的路径。同时需要 GPT/Claude 并希望合并账单的团队，OpenRouter 或 FreeModel 的聚合方案更合适。专门跑 Qwen/DeepSeek/GLM 的国内团队，SiliconFlow 在这些特定模型上的价格更低。

## FAQ

**Q: Novita AI 的 API 真的兼容 OpenAI 吗？包括 Function Calling？**

A: chat-completions 端点完全兼容——请求和响应格式与 OpenAI 一致。简单场景下的 Function Calling 可用（单工具、短上下文），但生产环境多工具或长上下文的工具调用 pipeline 中，tool-call 格式偶尔会偏离 OpenAI 规范。如果依赖工具调用的可靠性，建议加 schema parser 校验。

**Q: Novita AI 的价格和自建推理集群比起来如何？**

A: 单模型日调用量在 10M token 以下时，Novita 比直接租一台 A100 80GB 实例（零售价约 $1,500/月）便宜。单模型日调用量超过 100M token 时，H100 或 H200 专用推理就有成本竞争力——尤其是用 Novita 的独立 GPU 租赁（$1.99/小时 H100）。

**Q: 能在国内用 Novita AI 不需要代理吗？**

A: 可以——`cn.novita.ai` 端点就是为这个设计的。它有 ICP 备案基础设施、人民币计费、与三大运营商直连对等。国内典型服务器到 cn.novita.ai 的延迟在 30ms 以内，接近纯国内厂商。

**Q: Novita AI 会用 API 请求数据训练新模型吗？**

A: 根据公开隐私政策，请求数据保留 30 天用于风控后删除。除非用户明确同意，不会被用于训练新模型。企业客户可以在销售对接时谈数据驻留条款（数据留在他们选择的区域）。

**Q: 全球端点和 cn.novita.ai 的区别是什么？**

A: 同一个 Novita AI 品牌下的两个独立 API 产品。全球端点（api.novita.ai）是原始的新加坡产品，美元计费，托管 200+ 模型。cn.novita.ai 是国内专属产品，人民币计费，托管 160+ 模型，重点是国内开发的 LLM。分开的账号、key、限速。

**Q: 国内多厂商场景下，Novita AI 和 FreeModel 怎么选？**

A: 两者都是国内直连 + OpenAI 兼容，但 Novita 是单一厂商托管 200+ 开源模型，FreeModel 是多厂商聚合 + 内置审核路由。常见做法是 Novita 做主跑开源负载，FreeModel 做审核层和 OpenAI/Anthropic fallback——FreeModel 可以在 freemodel.dev/invite/FRE-7a3b6220 注册，一个 key 覆盖多厂商。

**Q: Novita AI 支持 LoRA 微调吗？什么价格？**

A: 支持——LoRA 微调 API 对部分基础模型开放（Qwen2.5-7B/14B/72B、Llama 3.1 8B/70B、Mistral-7B）。训练成本是 A100 80GB 实例 $0.50/小时。一个典型的 10K 样本微调需要 2-4 小时。产出的 adapter 通过同一个 OpenAI 兼容端点服务，按基础模型的 token 单价 + 少量 adapter 附加费计费。

## 结论

对 2026 年在开源 LLM 上构建生产系统的团队，Novita AI 是最直接的路径之一。OpenAI 兼容 API 消除了集成摩擦，$0.06/百万 token 的入门价是头部 OpenAI 兼容厂商里最低的，200+ 模型目录比 Together AI 或 Fireworks 更广，cn.novita.ai 端点解决了国内团队的访问问题。

2026 年选厂商的决策树：

- 需要 200+ 开源模型 + 最低单价 → **Novita AI**
- 需要 200+ 开源模型 + 最广的全球部署 → **Together AI**
- 需要 Qwen3.5/DeepSeek-R1/GLM-4 + 国内低延迟 → **SiliconFlow**
- 需要国内直连聚合 + 内置审核路由 + 多厂商 fallback → **FreeModel**
- 需要 Llama 3.3 70B 2,000+ tok/s，不需要中文 → **Cerebras 或 Groq**

如果你的团队已经在 Novita AI 上部署，想要一个 backup 做审核路由或在国内调用 OpenAI/Anthropic，FreeModel 是天然搭档——它把审核路由、OpenAI 兼容 API 和多厂商直连整合在一个 key 后面。在 freemodel.dev/invite/FRE-7a3b6220 注册可以先用免费层。

## 对比表（最终）

| 厂商 | 价格模式 | 最适合 | 国内访问 |
|----------|---------------|----------|--------------|
| **Novita AI** | 输入 $0.06-$1.52/1M tok，输出同价 | 200+ 开源模型，最低入门价 | ✅ 直连（cn.novita.ai） |
| **FreeModel** | 因模型而异 | 多厂商聚合 + 审核路由 | ✅ 直连 |
| **Together AI** | $0.18-$0.88/1M tok | 美欧部署 200+ 开源 | ❌ 需代理 |
| **SiliconFlow** | 输入 ¥0.4-2/1M tok，输出 ¥0.4-2/1M tok | 国内开源模型（Qwen/DeepSeek/GLM） | ✅ 直连 |
| **Fireworks AI** | $0.20-$3.00/1M tok | 100+ 开源快速推理 | ❌ 需代理 |
| **DeepSeek（官方）** | 输入 ¥1/1M tok，输出 ¥2/1M tok | DeepSeek 官方直供 | ✅ 直连 |
