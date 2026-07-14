---
title: "Together AI API 评测 2026：200+ 开源模型 $0.03/M"
description: "Together AI 完整评测：200+ 开源模型、FlashAttention-4 推理引擎、OpenAI 兼容 API、$0.03/M 起步价。对比 Fireworks、DeepInfra、Replicate、Baseten、Modal。"
slug: "together-ai-api-review"
provider: "together-ai"
published: true
date: "2026-07-14"
type: "review"
---

# Together AI API 评测 2026：200+ 开源模型 $0.03/M Token 起

Together AI 是 2026 年最大的**独立开源模型 AI 服务平台**。平台托管 **200+ 模型**，覆盖 Llama 4、DeepSeek V4、Qwen 3.5/3.6/3.7、Mistral、Kimi K2.7、NVIDIA Nemotron、GLM-5，以及图像/视频/音频模型，配合完全兼容 OpenAI 的 API，已成为追求前沿 OSS 质量、又不想自建 GPU 集群的团队的默认选择。

2026 年的杀手锏是**开源模型价格领导力**：Together 上的 DeepSeek V4 Pro 仅 $0.30/M 输入 token，Qwen 3.5 9B 低至 $0.03/M，Llama 4 Maverick $0.27/M，Kimi K2.7 Code $0.72/M。对于 token 量大的工作负载（长上下文 RAG、代码分析、批量摘要），Together 比闭源 API 便宜 30-70%，而质量差距仅约 3 个百分点。

如果你正在评估生产环境下的开源模型托管，或想出于成本原因从 OpenAI/Anthropic 迁移、又不想重写 SDK，Together AI 是 2026 年中值得认真考察的平台。

## TL;DR

- **200+ 开源和商业模型**，包括 Llama 4、DeepSeek V4、Qwen 3.5/3.6/3.7、Mistral、Kimi K2.7、GLM-5.2、NVIDIA Nemotron，外加图像（FLUX、Imagen、Seedream）和音频模型。含嵌入模型。
- **开源模型价格领导力。** Qwen 3.5 9B 仅 $0.03/M 输入；DeepSeek V4 Pro $0.30/M 输入；Llama 4 Maverick $0.27/M 输入。Batch API 五折；支持模型缓存输入折扣。
- **完全 OpenAI 兼容 API。** 直接替换：把 `base_url` 改为 `https://api.together.xyz/v1`，保留 OpenAI SDK 即可调用任何开源模型。
- **FlashAttention-4 推理引擎。** Together 研究团队自研 FA4 并在平台全量部署。内部基准显示比 TensorRT-LLM 多 31% tokens/sec。
- **两种部署模式。** Serverless（按 token 计费，零闲置成本）和 Dedicated（H100/B200/B200 预留 GPU 集群，常驻生产）。
- **最佳适用场景：** token 量大的 OSS 工作负载（RAG、批处理、代码分析）、需要按任务混用模型的多模型 Agent 系统、想降本从 OpenAI 迁移的团队。不适合：超低延迟实时场景、严格中国大陆数据驻留要求。
- **交叉链接：** 与 Baseten（2026-07-08 评测）、Modal（2026-07-13）、Fireworks AI、DeepInfra、Replicate 直接对比——Together 胜在模型广度和价格；Baseten 胜在 Dedicated 常驻；Modal 胜在开发者体验。

## 为什么 Together AI 在 2026 年很重要

三个力量汇聚，使 Together AI 成为 2026 年开源模型托管的顶级选择：

1. **开源质量追上闭源 API。** Llama 4 Maverick、DeepSeek V4 Pro、Qwen 3.6-Max、Kimi K2.7 Code 在大多数推理基准上与 GPT-5.6 / Sonnet 5 相差仅 2-5 个百分点，价格却仅为闭源的 30-70%。
2. **GPU 经济松动。** 2024-2025 年的 H100 短缺在 2025 年中结束。Together 与 NVIDIA 的大宗采购协议让他们能比小型转售商传递更低的单秒 GPU 成本。
3. **推理引擎突破持续叠加。** Together 的研究团队联合发表了 FlashAttention（FA1 至 FA4）。在 H100/B200 上跑 FA4 比基于 TensorRT-LLM 的栈有可量化的 TPS/$ 优势。

结果是：单个开发者就能以 $0.30/M 输入 token 调用 DeepSeek V4 Pro，以 $0.27/M 调用 Llama 4 Maverick 处理视觉任务，回退到 $0.03/M 的 Qwen 3.5 9B 做廉价分类——全部走同一个 OpenAI 兼容端点。

## Together AI 定价 — 2026-07-14 已验证

Together 在 Serverless 层按 token 计费，在 Dedicated 层按 GPU 秒计费。Serverless 是大多数工作负载的默认层。

### 精选 Serverless 模型价格

所有价格均为每百万 token。基于 OpenRouter 镜像交叉验证（Together 在 OpenRouter 上以同价托管相同 SKU）。

| 模型 | 输入 $/M | 输出 $/M | 上下文 | 备注 |
|---|---:|---:|---|---|
| **Qwen 3.5 9B** | $0.03 | $0.12 | 32K | Together 上最便宜的 OSS 模型 |
| **Qwen 3.5 70B** | $0.18 | $0.72 | 128K | 中端，Agent 甜点 |
| **Qwen 3.6 27B** | $0.29 | $0.96 | 128K | Qwen 3.6 中端 |
| **Qwen 3.6-Max Preview** | $1.04 | $6.24 | 256K | 前沿 Qwen 质量 |
| **Qwen 3.7-Plus** | $0.32 | $1.28 | 256K | 生产级 Qwen 3.7 |
| **Qwen 3.7-Max** | $1.25 | $3.75 | 256K | 顶级 Qwen |
| **DeepSeek V4 Pro** | $0.30 | $1.20 | 128K | DeepSeek 旗舰 |
| **Llama 4 Maverick** | $0.27 | $0.85 | 1M | Meta 前沿 OSS |
| **Llama 4 Scout** | $0.11 | $0.34 | 10M | 长上下文 OSS 领跑 |
| **Llama 3.3 70B Turbo** | $0.18 | $0.72 | 128K | 久经验证的主力 |
| **Mistral Medium 3.5** | $0.15 | $0.75 | 128K | Mistral 旗舰 |
| **Kimi K2.7 Code** | $0.72 | $3.49 | 256K | 编程专家 |
| **GLM-5.1（智谱）** | $0.30 | $1.50 | 128K | GLM 旗舰 OSS |
| **NVIDIA Nemotron 3 Ultra 550B** | $0.95 | $3.50 | 256K | NVIDIA 前沿 OSS |

对比 2026 年 7 月的闭源 API 等价物：
- **GPT-5.6**：$3.50/M 输入，$14/M 输出
- **Claude Sonnet 5**：$3/M 输入，$15/M 输出
- **Gemini 2.5 Pro**：$1.25/M 输入，$5/M 输出

Together 上的 Llama 4 Maverick $0.27/$0.85 比 GPT-5.6 在输入上便宜约 **13 倍**、输出上便宜约 **16 倍**，而大多数推理基准上仅落后 3-5 个百分点。

### 免费层和额度

- **$1 初始额度**（注册时赠送），需要绑定支付方式（无真正的免费层）。
- **Batch API**：异步工作负载（24h SLA）享五折。
- **缓存输入**：支持模型 $0.06-$0.26/M（Qwen、Llama 4、DeepSeek V4 Pro）。
- **预留容量**：月度承诺合同可享 Serverless 价格的 30-50% 折扣。

### Dedicated 层（GPU 集群）

对于大规模常驻生产，Dedicated 提供预留的 H100/B200/B300 容量：

| GPU | $/小时（Dedicated） | $/小时等价（Serverless） | 备注 |
|---|---:|---:|---|
| NVIDIA H100 80GB | $1.89 | $2.10（spot） / $6.30（reserved） | 生产主力 |
| NVIDIA H200 141GB | $2.45 | $2.65（spot） / $7.95（reserved） | HBM3e，大批量推理 |
| NVIDIA B200 | $3.49 | $3.85（spot） / $11.55（reserved） | 前沿训练+推理 |
| NVIDIA B300 | $3.95 | $4.30（spot） / $12.90（reserved） | 前沿训练+推理 |
| NVIDIA A100 80GB | $1.29 | $1.40（spot） / $4.20（reserved） | ≤70B 推理成本领跑 |
| NVIDIA L40S | $1.10 | $1.20（spot） / $3.60（reserved） | 视觉、图像生成 |

### 存储和嵌入定价

- **卷存储**：$0.09/GiB/月（每月前 1 TiB 免费）
- **嵌入模型**：根据模型 $0.03-$0.08/M token（BGE、E5、mxbai-rerank）
- **微调**：Llama 70B 起步 $1.50/M 训练 token；支持 LoRA

### 实际成本样例

**样例 1：Llama 4 Maverick 1M token RAG 查询**
- 800K 输入 + 200K 输出
- 输入成本：0.8 × $0.27 = **$0.216**
- 输出成本：0.2 × $0.85 = **$0.17**
- **总计：$0.386/查询**
- 同一查询在 GPT-5.6 上：0.8 × $3.50 + 0.2 × $14 = $2.80 + $2.80 = **$5.60**
- **该工作负载 Together 节省 14.5 倍**

**样例 2：Qwen 3.5 9B 上每天 10M token 分类**
- 7M 输入 + 3M 输出
- 输入：7 × $0.03 = $0.21
- 输出：3 × $0.12 = $0.36
- **每天成本：$0.57，月度约 $17**
- 同一工作负载在 GPT-4o-mini 上：7 × $0.15 + 3 × $0.60 = $1.05 + $1.80 = $2.85/天，**月约 $86**
- **Together 在分类工作负载上节省 5 倍**

**样例 3：Kimi K2.7 Code 代码审查**
- 每次审查 100K 输入 + 50K 输出
- 输入：0.1 × $0.72 = $0.072
- 输出：0.05 × $3.49 = $0.175
- **每次审查成本：$0.247**

## Together AI API 接口

Together 提供三个主要 API 接口，全部 OpenAI 兼容。

### 1. Chat Completions（`/v1/chat/completions`）

默认端点。OpenAI SDK 直接替换：

```python
from openai import OpenAI

client = OpenAI(
    api_key="TOGETHER_API_KEY",
    base_url="https://api.together.xyz/v1"
)

response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
    messages=[
        {"role": "system", "content": "你是一位资深后端工程师。"},
        {"role": "user", "content": "为一个多租户 API 设计速率限制器。"}
    ],
    temperature=0.7,
    max_tokens=2048,
)

print(response.choices[0].message.content)
```

### 2. Completions（`/v1/completions`）

旧式文本补全端点，用于基础模型（无 chat 格式化）。适用于微调模型或补全式工作流。

### 3. Embeddings（`/v1/embeddings`）

标准 OpenAI 兼容嵌入端点。支持模型包括 `togethercomputer/m2-bert-80M`、`BAAI/bge-base-en-v1.5`、`intfloat/e5-large-v2` 和 `mixedbread-ai/mxbai-rerank-large-v2`。

```python
response = client.embeddings.create(
    model="BAAI/bge-base-en-v1.5",
    input=["什么是 Together AI？", "最便宜的开源模型 API？"]
)
print([d.embedding[:5] for d in response.data])
```

### 4. 图像生成（`/v1/images/generations`）

FLUX.1、FLUX.2、Imagen 4.0 和 Seedream 4.0 通过 images 端点暴露。每张图定价 $0.005-$0.05（取决于分辨率）。

### 5. 音频（`/v1/audio/*`）

Whisper 风格转录，外加 Together 自研音频模型（MusicGen、AudioCraft）。同一 base URL 可用。

### 函数调用和 JSON 模式

Together 上所有主要 chat 模型支持：
- **工具/函数调用**（OpenAI 兼容的 `tools` 参数）
- **JSON 模式**（`response_format={"type": "json_object"}`）
- **结构化输出**（Pydantic、Zod、JSON Schema）
- **流式输出**（`stream=True`）
- **视觉**（Llama 4 Maverick、Qwen 3.6 VL、Pixtral）

这就是为什么从 OpenAI 迁移的团队除了 `base_url` 和模型 ID 外几乎不需要改动任何代码。

## 逐步教程：15 分钟上线 Llama 4 RAG 端点

以下是调用 Llama 4 Maverick 做 RAG 工作流的完整流程。

### 1. 注册并获取 API Key

访问 `https://api.together.xyz`，创建账号并添加支付方式。获得 $1 初始额度。在控制台生成 API Key。

### 2. 安装 SDK 或直接使用 HTTP

官方 Python SDK 是 `together`：

```bash
pip install together
```

或直接使用 OpenAI SDK（推荐用于 OpenAI 兼容代码）：

```bash
pip install openai
```

### 3. 首次调用

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["TOGETHER_API_KEY"],
    base_url="https://api.together.xyz/v1"
)

response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
    messages=[
        {"role": "user", "content": "一句话解释什么是 Together AI？"}
    ],
    max_tokens=100
)

print(response.choices[0].message.content)
```

预期输出类似："Together AI 是一个用于运行和微调开源大语言模型的云平台。"

### 4. 添加 RAG 上下文

```python
def rag_query(question: str, context_docs: list[str]) -> str:
    context = "\n\n".join(f"[文档 {i+1}] {doc}" for i, doc in enumerate(context_docs))
    prompt = f"""基于以下上下文回答问题。如果答案不在上下文中，请说明。

上下文：
{context}

问题：{question}
答案："""
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.1
    )
    return response.choices[0].message.content

# 示例
docs = [
    "Together AI 由 Vipul Ved Prakash 和 Ce Zhang 于 2022 年创立。",
    "公司总部位于加利福尼亚州旧金山。",
    "Together AI 在 2024 年完成由 Salesforce Ventures 领投的 1.02 亿美元 A 轮融资。"
]

print(rag_query("谁创立了 Together AI？", docs))
```

### 5. 为重复前缀添加缓存

Together 的缓存输入折扣会在你的 prompt 有共同前缀（通常是长 system prompt 或大上下文）时自动应用。启用方式：

```python
response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct",
    messages=[...],
    extra_body={
        "cache": True  # Together 特定标志
    }
)
```

缓存输入按 $0.06-$0.26/M 计费（vs Llama 4 Maverick 新输入 $0.27/M）——**缓存部分成本降低 4.5 倍**。

### 6. 生产部署

对于生产环境，使用 Dedicated 层或通过 Together 的 GPU 集群自托管。大多数团队在 Serverless 上跑到 100M+ token/月后切到 Dedicated，此时 Dedicated 便宜约 30%。

## Together AI 适用场景 — 以及不适用场景

### Together 最佳适用

- **开源模型工作负载**（Llama 4、DeepSeek V4、Qwen、Mistral、Kimi），比闭源 API 节省 30-70% 成本
- **Token 量大的批处理**（RAG 导入、文档摘要、日志分析），Qwen 3.5 9B $0.03/M 占绝对优势
- **多模型 Agent 系统**，不同任务路由到不同模型（廉价分类、中端聊天、前沿推理）
- **OpenAI SDK 迁移**，只需换 `base_url`，其余代码保持不变
- **微调工作流**（LoRA、全量微调）支持 Llama 70B、Qwen 70B、Mistral 7B
- **100M+ token/月成本敏感生产**，此时 Dedicated 定价生效

### Together 不适合

- **超低延迟实时**（200ms 内 TTFT）——Serverless 冷启动 1-3 秒。需要 Dedicated 或 Groq 这样的专业提供商。
- **闭源前沿质量**，必须用 GPT-5.6 / Claude Sonnet 5 / Gemini 2.5 Pro——Together 托管的 OSS 模型在硬推理基准上落后 2-5 个百分点。
- **严格中国大陆数据驻留**——Together 基础设施在美国 GPU 集群上；无 CN 区域。
- **以图像/视频生成为主要用途**——Replicate 和 fal.ai 在视觉工作负载上有更大的目录和更优化的单图定价。
- **语音/音频优先产品**——ElevenLabs 和 Cartesia 更适合低延迟语音；Together 的音频侧重转录。

## Together AI vs Fireworks AI vs DeepInfra vs Replicate vs Baseten vs Modal

| 特性 | Together AI | Fireworks AI | DeepInfra | Replicate | Baseten | Modal |
|---|---|---|---|---|---|---|
| **模型数量** | 200+ OSS | 100+ OSS | 50+ OSS | 50K+（社区） | 自定义 + OSS | 自带模型 |
| **定价模式** | 按 token | 按 token | 按 token | 按 GPU 秒 | 按 GPU 秒 | 按 GPU 秒 |
| **最便宜 OSS** | Qwen 3.5 9B $0.03/M | Llama 3.3 70B $0.20/M | Qwen 2.5 7B $0.05/M | 不定 | 不定 | $0.16/秒 T4 |
| **免费层** | $1 额度 | $1 额度 | $0.50 额度 | 有限 | 无 | $30/月 |
| **OpenAI 兼容** | 是 | 是 | 是 | 是 | 是 | 否（Python SDK） |
| **冷启动** | 1-2 秒 | 1-3 秒 | 2-5 秒 | 5-15 秒 | 2-5 秒 | 1-3 秒 |
| **微调** | 是（LoRA + 全量） | 是（LoRA） | 有限 | 否 | 是 | 是（任何框架） |
| **Dedicated GPU** | 是（H100/B200） | 是（H100/A100） | 是（H100/A100） | 否（serverless） | 是（Dedicated） | 否 |
| **图像生成侧重** | 中 | 低 | 低 | 最高 | 低 | 自带模型 |
| **最佳适用** | OSS 广度 + 价格 | 前沿速度 | 廉价 OSS | 社区模型 | 常驻生产 | Python DX |

2026 年选型矩阵：

- **Together AI**：OSS 模型广度最佳，Qwen/Llama/DeepSeek 每 token 价格最低
- **Fireworks AI**：前沿 OSS 速度最佳（Mixtral、Llama 3），支持微调
- **DeepInfra**：超廉价 OSS 推理最佳（Qwen 2.5 7B $0.05/M）
- **Replicate**：社区模型目录最佳（图像、音频、小众 OSS）
- **Baseten**：常驻生产最佳，配合 Dedicated Deployments
- **Modal**：自定义模型自托管最佳，Python 优先 DX

## 生产环境验证 Together AI

在把 Together 用于真实流量前，验证以下四件事：

1. **延迟分布。** 对 Llama 4 Maverick 发 100 个请求，测量首 token 时间。预期 p50 ~600ms（热），p99 ~2.5 秒（冷）。亚 200ms 延迟需切到 Dedicated 或更快提供商。
2. **每次请求成本。** 使用 Together 内置用量仪表板（`https://api.together.xyz/settings/billing`）确认每个模型的实际开销与预期一致。设置硬上限防止失控成本。
3. **缓存输入行为。** 跑同一个长前缀 prompt 10 次——Together 应对首次请求按全价收费，后续请求按缓存输入价计费。在仪表板中验证。
4. **故障切换行为。** Together API 对 Serverless 提供 99.9% SLA。要更高可用性，使用 Dedicated 层或通过 OpenRouter 智能路由设置到第二家提供商（Fireworks、DeepInfra）的回退。

## FAQ

### Together AI 比 OpenAI 便宜吗？

对于开源模型（Llama 4、DeepSeek V4、Qwen），Together 在等价工作负载上比 GPT-5.6 便宜 5-15 倍。随着上下文长度增加，价格差距扩大（Together 按上下文长度统一收费，部分提供商对长上下文加价）。

### Together AI 价格这么低，怎么赚钱？

Together 自营 GPU 集群（H100、B200），联合开发 FlashAttention-4 提升推理效率，并向 NVIDIA 大宗采购。这组合让他们在同价位上比小型转售商有 30-50% 利润空间。

### Together AI 的 API 兼容 OpenAI 吗？

完全兼容。你可以使用 OpenAI Python SDK、Node SDK 或任何支持 OpenAI API 接口的框架（LangChain、LlamaIndex、Vercel AI SDK、AutoGen、CrewAI），只需把 `base_url` 改为 `https://api.together.xyz/v1`。所有模型 ID 使用 HuggingFace 格式（如 `meta-llama/Llama-4-Maverick-17B-128E-Instruct`）。

### 可以从中国使用 Together AI 吗？

不能直接使用。Together 的基础设施在美国，没有 CN 区域。中国开发者应通过代理使用 Together，或使用国内替代方案：DeepSeek（官方 API）、阿里云百炼、腾讯混元以获得类似的模型访问。

### Together AI 的速率限制是多少？

Serverless 默认速率限制：新账号每分钟 60 次请求、500K token/分钟。限制随使用历史动态扩展——高用量账号在持续付费使用 30-60 天后获得更高的 RPM/TPM。Dedicated 层用户获得配置的自定义限制。

### Together AI 支持微调吗？

支持。Together 在 Llama 4、Qwen 3.5/3.6、Mistral 等多个 OSS 模型上支持 LoRA 和全量微调。定价起步 $1.50/M 训练 token。微调模型作为私有端点部署在 Together 基础设施上。

### 什么是 FlashAttention-4？

FlashAttention-4 是 FlashAttention 研究团队（包括 Together AI 联合创始人 Ce Zhang）开发的第四代注意力算法。它针对 H100/B200 硬件优化，让 Together 在等价硬件上比基于 TensorRT-LLM 的推理栈有可量化的 tokens/$ 优势。

### Together AI 和 Fireworks AI 怎么比？

Together 模型覆盖更广（200+ vs 100+），Qwen 3.5/3.6 每 token 价格更低。Fireworks 在较小的一组前沿 OSS 模型上（尤其是 Llama 3 和 Mixtral）有更快推理。对于大多数工作负载，Together 胜在价格/覆盖；对特定模型的延迟关键工作负载，Fireworks 可能略胜。

### Together AI 有企业版吗？

有。企业版提供自定义 SLA（99.9%+）、Dedicated GPU 集群、本地部署选项、HIPAA/PCI 合规、SSO、RBAC 和自定义合同。通过 `enterprise@together.ai` 联系销售。

### 我可以在 Together AI 上部署自己的自定义模型吗？

可以。Bring-Your-Own-Model（BYOM）程序支持 HuggingFace 格式模型，最大 700B 参数。定价按 Dedicated 硬件的 GPU 秒计算。自定义模型获得私有 HTTPS 端点和完全的 Together API 兼容性（OpenAI SDK 可用）。

### Together AI 上我的数据会怎样？

Together 的默认策略是**不基于客户数据训练**——你的 prompt 和补全不会用于改进任何模型。数据保留 30 天用于滥用监控，之后删除。企业客户可以申请零保留合同和本地部署。

### Together AI 支持视觉模型吗？

支持。Llama 4 Maverick、Qwen 3.6 VL 和 Pixtral 都带视觉能力托管。在 OpenAI 格式的 messages 数组中传入 base64 或 URL 图片。Together 还通过单独端点托管 FLUX、Imagen 和 Seedream 用于图像生成。

---

**结论：** Together AI 是 2026 年最大且最具成本效益的开源模型 API 平台。200+ 模型、$0.03-$1.25/M 输入 token、OpenAI 兼容 API、FlashAttention-4 推理，加上持续推动领域前进的研究团队，是生产环境运行开源权重模型的默认选择。如果你正在以 GPT-5.6 / Sonnet 5 的价格支付 Llama 4 Maverick 或 DeepSeek V4 Pro 就能处理的工作负载（成本仅 1/10），Together 是首选评估平台。