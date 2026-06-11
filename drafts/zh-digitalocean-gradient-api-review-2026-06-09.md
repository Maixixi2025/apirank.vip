---
title: "DigitalOcean Gradient API 2026: H100 推理 + OpenRouter 接入"
description: "DigitalOcean Gradient AI 测评：H100/H200 GPU 推理 $2.16/小时起，Serverless 端点 $0.0005/1K tokens，14 个托管模型，6/3 接入 OpenRouter 生态。对比 RunPod、CoreWeave、SambaNova。"
slug: "digitalocean-gradient-api-review"
provider: "digitalocean-gradient"
published: true
date: "2026-06-09"
type: "review"
---

# DigitalOcean Gradient API 2026：把 H100 卖给个人开发者的那家公司

## 引子：6/3 接入 OpenRouter 意味着什么

2026 年 6 月 3 日，DigitalOcean 静悄悄地成为 OpenRouter 的模型供应商之一。这句话听起来平平无奇 — OpenRouter 接入新供应商是每周都有的事 — 但如果把这步棋放到 DigitalOcean 过去三年卖给独立开发者 $2.16/小时 H100 的历史里看，就完全不一样了。现在每个 OpenRouter 用户（每月跑 4 万亿 token 级别的那个量级）都可以把请求路由到 DigitalOcean 托管的 Llama 3.3 70B、Llama 3.1 405B、DeepSeek V2.5 端点，**完全不用注册 DigitalOcean 账号**。

对已经在用 DigitalOcean 跑数据库、对象存储、应用服务器的人来说，Gradient 是这套现有账单的自然延伸：同一个 dashboard、同一个 API token、同一个结算账户，推理层直接搭在剩余的栈上。对还没用过 DigitalOcean 的团队，Gradient 值得看一眼有三个理由：H100 / H200 算力是 indie 价位、Serverless 模式按 token 付费不用管 GPU、Knowledge Base + Agent 一体化把 RAG 的脏活（向量库、分块、嵌入）一站包圆。

这篇测评覆盖 API 接口、定价、模型目录、速度、中国访问，以及和 RunPod、CoreWeave、SambaNova、Together AI、OpenRouter 直接供应商的对比。

## DigitalOcean Gradient 到底是什么

Gradient 是两个产品粘起来的：

1. **GPU Droplets** — DigitalOcean 早就在卖的带 H100 / H200 / L40S / A100 的虚拟机。你按小时租盒子，自己装 vLLM 或 TGI，自己跑推理。这部分不新鲜，DO 卖了好几年。
2. **Gradient AI Platform** — 2025 年底重启的 serverless 推理 + Agent 层。你在 Hugging Face 选一个模型（或者从 DO 精选的 14 个里挑一个），平台负责 GPU 自动扩缩、批处理、请求路由，按 token 付费，没有 GPU 要管。

Knowledge Base 和 Agent 功能是搭在 serverless 层之上的。Knowledge Base 是托管的向量库（你上传 PDF / 文档，平台帮你分块 + 嵌入），Agent 是托管的工具调用 runtime，把推理端点接到 Knowledge Base。如果你以前拼过 LangChain + Pinecone + OpenAI 的组合，可以想象 Gradient 在抢谁的饭碗。

6/3 接入 OpenRouter 是补全的拼图。在此之前，要用 Gradient 托管的模型得去 DO dashboard 申请 API token，再把代码指向 `https://inference.do-ai.run/v1/`。现在用 OpenRouter 的 `digitalocean/llama-3.3-70b-instruct` 字符串就能路由过去。同一个模型、同一个价格，但用户根本不用知道 DigitalOcean 存在。

## 模型目录：14 个精选开源模型

Gradient 的模型目录是短而精。和 Together AI（200+）或 Hugging Face（600+）不同，Gradient 上架了 14 个手工挑选的开源模型，全部跑在 H100 或 L40S 上：

| 模型 | 参数量 | 硬件 | 适用场景 |
|------|--------|------|----------|
| Llama 3.3 70B Instruct | 70B | H100 | 通用聊天，生产默认 |
| Llama 3.1 405B Instruct | 405B | H100 x4 | 最难的推理任务 |
| Llama 3.1 8B Instruct | 8B | L40S | 批量分类、路由 |
| Mistral 7B Instruct | 7B | L40S | 最低成本、高吞吐 |
| Mistral Nemo | 12B | L40S | 多语言、中端 |
| Mixtral 8x7B Instruct | 47B (active) | L40S | 性价比 MoE |
| Qwen 2.5 72B Instruct | 72B | H100 | 中英文俱佳 |
| Qwen 2.5 Coder 32B | 32B | H100 | 代码生成 |
| DeepSeek V2.5 Chat | 236B (active) | H100 | 推理 + 代码 |
| DeepSeek Coder V2 | 236B (active) | H100 | 代码补全 |
| Nous Hermes 2 Mixtral | 47B (active) | L40S | 微调对话 |
| OpenHermes 2.5 | 7B | L40S | 轻量对话 |
| Phi-3 Medium | 14B | L40S | 推理、小 footprint |
| Whisper Large V3 | 1.5B | L40S | 语音转文字 |

这是**精选**目录，不是全量。DigitalOcean 会在内部 eval 套件上跑每个模型再上架，达不到准确率门槛的直接下架。405B Llama 是其中最显眼的 — 这是目前通过 OpenRouter 能调到的唯一一个 405B 级全开源模型，TTFT 还能压在 1 秒以内。

取舍也很明显：如果你要 Claude / GPT / Gemini，那些要走其他供应商。Gradient 只服务开源权重。

## API 接口：OpenAI 兼容 + 原生 SDK

Serverless 推理端点完全跟随 OpenAI `/v1/chat/completions` 的 shape。在 `api.openai.com` 能跑的请求，换个 base URL + key 就能在 Gradient 跑：

```python
import openai

client = openai.OpenAI(
    base_url="https://inference.do-ai.run/v1/",
    api_key="YOUR_GRADIENT_API_TOKEN",
)

response = client.chat.completions.create(
    model="llama-3.3-70b-instruct",
    messages=[{"role": "user", "content": "总结一下 OpenRouter 接入。"}],
)
```

这种 OpenAI 兼容性意味着 LangChain、LlamaIndex、AutoGen、OpenAI 官方 Python SDK 全部零代码改动能用，只换 base URL。

在 OpenAI shape 之上，Gradient 还额外提供了：

- **Agent 端点**（`/v1/agents/{agent_id}/invoke`）— 调用一个已经绑定 Knowledge Base 和工具的托管 agent。
- **Knowledge Base 端点**（`/v1/knowledge_bases/{kb_id}/search`）— 不经过 LLM 的纯向量搜索。
- **Embeddings 端点**（`/v1/embeddings`）— 默认是 bge-large-en 和 bge-m3。
- **语音转文字端点**（`/v1/audio/transcriptions`）— Whisper Large V3。
- **Reranker 端点** — bge-reranker-v2-m3，用于 RAG 流水线。

另外有一级 CLI（`doctl ai`）和 Terraform provider，给做 IaC 的团队用。

## 定价：GPU 小时 vs 按 token

Gradient 的定价分两层，这两层之间的选择是新人最重要的决策。

### GPU Droplets（自己管盒子）

| GPU | 显存 | 小时价 | 月度（24/7） |
|-----|------|--------|---------------|
| H200 | 141 GB | $3.20/小时 | 约 $2,330 |
| H100 | 80 GB | $2.16/小时 | 约 $1,575 |
| L40S | 48 GB | $1.12/小时 | 约 $817 |
| A100 | 40 GB | $0.76/小时 | 约 $554 |
| A100 | 80 GB | $1.10/小时 | 约 $802 |
| RTX 4000 Ada | 20 GB | $0.50/小时 | 约 $365 |

$2.16/小时的 H100，比 AWS `p5.48xlarge`（$4.10/小时 H100）便宜 30-50%，比 RunPod on-demand H100 便宜 20%。1 年 / 3 年预订折扣更便宜，但只对稳态推理有意义。

### Serverless Inference（不用管 GPU）

Llama 3.1 8B 的按 token 定价从 $0.0005/1K tokens 起（小模型入 + 出合并计费）。大模型的按 token 费率大致和参数量线性相关：

| 模型 | 输入（每 1M tokens） | 输出（每 1M tokens） |
|------|----------------------|----------------------|
| Llama 3.1 8B | $0.20 | $0.20 |
| Mistral 7B | $0.20 | $0.20 |
| Qwen 2.5 72B | $0.90 | $0.90 |
| Llama 3.3 70B | $0.90 | $0.90 |
| DeepSeek V2.5 | $1.20 | $1.20 |
| Llama 3.1 405B | $3.20 | $3.20 |

免费额度：**注册送 $200，60 天有效**。这够在 Llama 3.3 70B 上跑大约 10 亿 token，或者在 Llama 3.1 8B 上跑 100 亿 token。额度过期后没有永久免费层，纯付费。

对比一下，同样的 Llama 3.3 70B 在 SambaNova 是输入 $0.30 / 输出 $0.70（合并 $1.00）每 1M tokens，在 Groq 是 $0.59 / $0.79（合并 $1.38）。Gradient 的 $0.90 合并价有竞争力，但不是最便宜。**最便宜**仍然是 OpenRouter 路由到 DeepSeek V3 的大约 $0.50/1M tokens 合并价。

## 速度基准

从 DigitalOcean 官方数据 + 第三方实测：

- **Llama 3.1 8B**: ~190 tok/s 输出，TTFT ~180ms（美东，H100）
- **Llama 3.3 70B**: ~75 tok/s 输出，TTFT ~320ms
- **Llama 3.1 405B**: ~38 tok/s 输出，TTFT ~480ms
- **Qwen 2.5 72B**: ~70 tok/s 输出，TTFT ~340ms
- **DeepSeek V2.5 (236B MoE)**: ~52 tok/s 输出，TTFT ~420ms
- **Mixtral 8x7B**: ~95 tok/s 输出，TTFT ~260ms

Serverless 端点的冷启动是软肋 — 静默期后第一个请求要 2-3 秒，平台要临时拉起 H100。暖机后的稳定吞吐在 8B / 70B 段和 Groq、SambaNova 同档，405B 段明显落后 Groq（Groq 的 405B 跑 60+ tok/s，LPU 架构红利；H100 不管哪个供应商都顶到 40 tok/s 封顶）。

Agent 类工作负载（混小模型 + 大模型）推荐模式：分类 / 路由 / 解析走 Llama 3.1 8B（便宜快），推理 / 决策走 70B / 405B。Gradient 的 Knowledge Base 和 Agent 功能就是围绕这个切分设计的。

## 中国访问

DigitalOcean 的数据中心在纽约、硅谷、阿姆斯特丹、法兰克福、伦敦、新加坡、班加罗尔。**没有中国大陆区域**，dashboard（`cloud.digitalocean.com`）在国内多个 ISP 是网络层屏蔽的。

对中国开发者：

- **Dashboard** 需要稳定代理，偶尔有 CAPTCHA 摩擦。
- **API 端点**（`inference.do-ai.run`）在中国境内可达，比美东直连多 200-400ms 延迟。
- **OpenRouter 路由是 workaround。** 用 `digitalocean/llama-3.3-70b-instruct` 模型名走 OpenRouter，OpenRouter 现有的中国直连边缘节点处理连通性。这是 2026 年 6 月起对中国团队摩擦最低的路径。
- **支付**：DigitalOcean 接受 Visa / Mastercard / PayPal / 加密货币（BTC、ETH、USDC）。国内银联卡不直接支持，但加密货币（USDC）路径走 Binance 充值可用。

总结：Gradient 是美/欧托管的平台，没有中国区域，但 OpenRouter 集成 + 加密支付让它对中国团队勉强可用 — 只要你不是非要 dashboard 不可。

## Gradient vs 替代品

2026 年 "AI 推理平台" 已经很拥挤。Gradient 不是最便宜的、不是最快的、也不是模型最多的。它赢在 "无聊基础设施" 那个位置：和你数据库同一个 dashboard、和你 Spaces 同一个 API token、和你剩下的栈同一个 Terraform provider。

| 平台 | 模型数 | 最低价 | 中国访问 | OpenRouter 供应商 | 备注 |
|------|--------|--------|----------|---------------------|------|
| **DigitalOcean Gradient** | 14（仅开源） | $0.0005/1K tok | 代理 / OpenRouter | ✅（自 6/3） | H100 indie 价位，DO 全生态 |
| **SambaNova** | 9（仅开源） | $0.10/M tok | 代理 | ❌ | SN40L 芯片，70B 跑 1,000+ tok/s |
| **Together AI** | 200+（开源 + 闭源） | $0.06/M tok | 代理 | ❌ | $1/M 价位模型数最多 |
| **RunPod** | 200+ | $0.40/小时（H100） | 代理 | ❌ | GPU 租賃为主，托管较少 |
| **CoreWeave** | 50+ | $2.15/小时（H100） | 代理 | ❌ | 企业级 / NVIDIA 合作 |
| **Fireworks AI** | 100+ | $0.20/M tok | 代理 | ❌ | Function calling 优化 |
| **Cerebras** | 6 | $0.10/M tok（合并） | 代理 | ❌ | WSE-3 晶圆级，2,000+ tok/s |

如果决定因素是 **每 token 价格**（最小模型），SambaNova 和 Cerebras 赢。如果决定因素是 **最广的模型目录**，Together AI 赢。如果决定因素是 **"我已经在给 DigitalOcean 付钱"**，Gradient 是显然答案 — 而且 6/3 的 OpenRouter 集成干掉了以前把团队推到别处的 API key 摩擦。

## 谁该用 DigitalOcean Gradient

Gradient 适合这些场景：

- **现成的 DigitalOcean 客户** 想加一层推理，又不想付第二个 vendor。
- **只用开源权重的团队** 需要 70B+ 模型，但不想自己管 GPU 集群。
- **独立开发者** 想要 H100 算力，又不想签 AWS 合同。
- **OpenRouter 用户** 想要一个新的 Llama 3.x / DeepSeek 路由选项。

Gradient 不适合这些场景：

- **闭源模型用户** — 没有 Claude，没有 GPT，没有 Gemini。请用 OpenAI / Anthropic，或者在 OpenRouter 上换一个 provider 字符串。
- **中国大陆开发者** 需要国内端点 — 用 SiliconFlow、DeepSeek 直连、阿里云百炼。
- **亚 100ms 延迟应用** — Gradient 的 TTFT 有竞争力但不是顶级，Groq 和 Cerebras 更快。
- **极小模型（< 4B）** — Gradient 最小是 7B，7B 以下用 GPU Droplet 就不划算了。

## FAQ

**Q: DigitalOcean Gradient 是模型供应商还是 GPU 租赁平台？**
A: 两个都是。GPU Droplets 是租赁侧；Gradient AI Platform 是 serverless 推理和 Agent 层。6/3 的 OpenRouter 集成让两边都能用一个模型名访问。

**Q: 能在 Gradient 上跑闭源模型（GPT-4o、Claude 3.5）吗？**
A: 不能。Gradient 只做开源权重。闭源模型请用 OpenAI / Anthropic，或者在 OpenRouter 上换一个 provider 字符串。

**Q: Llama 3.3 70B 在 Gradient 上多少钱？**
A: 输入 + 输出合并 $0.90/1M tokens。同一模型在 SambaNova 是 $1.00/M，在 Groq 是 $1.38/M。同一模型更便宜的选项是 OpenRouter 上换 DeepSeek 或 Mistral provider。

**Q: 有免费层吗？**
A: 注册送 $200，60 天有效。没有永久免费层。最便宜的付费层是 Llama 3.1 8B 的 $0.20/M tokens。

**Q: 在中国境内能用 Gradient 吗？**
A: Dashboard 被屏蔽，但 API 端点能用，延迟多 200-400ms。要更低延迟，用 OpenRouter 的 `digitalocean/llama-3.3-70b-instruct` 模型名走 OpenRouter 自己的中国直连边缘。

**Q: Gradient 支持 function calling / 工具调用吗？**
A: 支持，chat completions 端点就有。Agent 平台也内置了常用模式（网页搜索、计算器、代码执行）的工具绑定。

**Q: 6/3 接入 OpenRouter 怎么工作？**
A: OpenRouter 在 6/3 加了 `digitalocean/` 前缀。可以路由请求到 `digitalocean/llama-3.3-70b-instruct`、`digitalocean/llama-3.1-405b-instruct` 等几个模型名。计费照旧，OpenRouter 加 5.5% 平台费，但不用单独开 DigitalOcean 账号。

**Q: 能在 Gradient 上部署自己的私有模型吗？**
A: 能，用 GPU Droplets 装 vLLM / TGI / SGLang。Serverless 端点只对精选 14 个模型开放。

## 结语

DigitalOcean Gradient 不是 2026 年最便宜、最快、模型最广的 AI 推理平台。它是那个 dashboard 摩擦最低的（对 DigitalOcean 现有客户），是 6/3 接入 OpenRouter 后对所有 OpenRouter 用户开放的（无需注册）。$200 免费额度够认真评估一轮。如果你是开源权重开发者 + 在给 DigitalOcean 付钱，下次想拉 H100 时大概率应该拉个 Gradient 端点。

闭源模型用户、亚 100ms 延迟应用、中国大陆直连 — 去别处看。开源 + indie 那个甜蜜点上，Gradient 现在是默认选项之一。
