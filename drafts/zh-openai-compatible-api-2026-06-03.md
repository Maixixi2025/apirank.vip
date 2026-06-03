---
title: "OpenAI 兼容 API 2026：10 个可直接替换的接口对比"
description: "对比 10 个 OpenAI 兼容 API 提供商：Groq、OpenRouter、Together AI、FreeModel、DeepSeek。迁移代码、价格、国内访问、最佳选择。"
slug: "openai-compatible-api-2026"
provider: "cross-provider"
published: false
date: "2026-06-03"
type: "comparison"
---

# OpenAI 兼容 API 2026：10 个可直接替换的接口对比

如果你正在用 OpenAI 的 Python 或 Node SDK，2026 年你可以通过改一个 `base_url` 参数切换到 30+ 个其他 LLM 提供商。这些提供商都暴露了 OpenAI 兼容的 REST 端点，所以现有的客户端库、重试逻辑和流式处理代码完全不变。这是过去几年 LLM API 设计中最重要的演进——它把 OpenAI SDK 变成了事实上的行业标准。

这篇文章对比 **2026 年真正值得关注的 10 个 OpenAI 兼容提供商**，包含真实价格、速度数据、国内访问情况，以及一段你可以直接复制到自己代码库的迁移示例。

## 什么是 OpenAI 兼容 API？

OpenAI 兼容 API 是一个 REST 端点，模仿 OpenAI 的 Chat Completions 接口——相同的 `POST /v1/chat/completions` 路径、相同的 JSON 请求体、相同的 `stream: true` Server-Sent Events 响应、相同的 `tools`/`function_call` 工具调用负载。实现这个接口契约的提供商，可以与以下工具无缝替换：

- 官方 `openai` Python 和 Node SDK（设置 `base_url` 即可）
- `langchain`、`llama-index`、`autogen` 和大部分 agent 框架
- 本地编码工具：Cursor、Continue.dev、Aider、Cline、OpenHands
- 任何已经在和 `api.openai.com` 对话的 HTTP 客户端

最常见的差异在于：模型名称（每个提供商有自己的命名）、认证头（大部分用 `Authorization: Bearer`，少数用 `x-api-key`）、流式格式（大部分用 SSE，少数用 JSON lines 包装）。

## 为什么开发者从 OpenAI 切换出去

2026 年的切换原因，按频次排序：

1. **成本。** Groq 上的 Llama 3.3 70B 是 **每 1M 输入 token $0.59**，而 **GPT-4o-mini 是 $2.50**。一个每月 1 亿 token 的工作负载，便宜模型上的差异大约是 $190/月 vs $250/月，旗舰模型上的差异更大。
2. **延迟。** Groq 的 LPU 在 Llama 3.1 8B 上达到 ~1,250 tokens/sec，首 token 延迟低于 100ms。OpenAI 的 GPT-4o-mini 首 token 平均 300-500ms。对语音 agent 来说，这个差异决定了可用与不可用。
3. **国内访问。** `api.openai.com` 在中国大陆被屏蔽。FreeModel、DeepSeek 和 apikey.fun 都提供国内直连端点，无需代理。
4. **模型选择。** OpenAI 有 8 个主模型。OpenRouter 有 200+。Together AI 和 Fireworks 在开源模型发布几天内就上线。
5. **微调。** OpenAI 微调是闭源的且昂贵。Together AI、Fireworks、Anyscale 暴露完整的 LoRA/QLoRA 微调能力，支持任何开源模型。
6. **数据隐私。** 闭源 OpenAI 模型把你的 prompt 发到 OpenAI 的基础设施。Self-hosted vLLM 或 Together 的专用端点把数据留在你控制的基础设施上。

## 2026 年值得知道的 10 个 OpenAI 兼容提供商

### 1. OpenRouter — 聚合器

- **端点：** `https://openrouter.ai/api/v1`
- **模型：** 200+（GPT-4o、Claude 3.5、Gemini、Llama、Mistral、DeepSeek、Qwen，以及社区微调）
- **价格：** 透传（提供商价格 + 部分路由 ~5% OpenRouter 费用）
- **免费额度：** 部分模型免费，大部分付费
- **国内访问：** ❌ 需要代理
- **最适合：** 多模型对比、fallback 路由、无需多账号访问闭源模型

### 2. Groq — 速度之王

- **端点：** `https://api.groq.com/openai/v1`
- **模型：** Llama 3.3 70B、Llama 3.1 8B、Mixtral、Gemma、Whisper Large V3
- **价格：** $0.05-0.59/M 输入，$0.08-0.79/M 输出（最快的 LPU 引擎）
- **免费额度：** 每天 1,000 请求，每分钟 30 请求——无需信用卡
- **国内访问：** ❌ 需要代理
- **最适合：** 实时聊天、语音 agent、首 token 延迟 < 200ms 的代码补全

### 3. Together AI — 微调 + 推理

- **端点：** `https://api.together.xyz/v1`
- **模型：** 200+ 开源模型，完整 LoRA/QLoRA 微调支持
- **价格：** $0.18-0.90/M 输入，$0.18-0.90/M 输出（按模型）
- **免费额度：** 注册送 $5 信用
- **国内访问：** ❌ 需要代理
- **最适合：** 自定义微调模型、批量处理、专用端点

### 4. Fireworks AI — 生产推理

- **端点：** `https://api.fireworks.ai/inference/v1`
- **模型：** 100+ 开源模型，优化的推理引擎（部分 benchmark 比 Together 更快）
- **价格：** $0.20-0.90/M 输入，$0.20-0.90/M 输出
- **免费额度：** 注册送 $1 信用
- **国内访问：** ❌ 需要代理
- **最适合：** 生产 LLM 部署、大规模批处理

### 5. Anyscale — 企业级 Ray 架构

- **端点：** `https://api.endpoints.anyscale.com/v1`
- **模型：** Llama、Mistral、Ray Serve 基础设施上的自定义模型
- **价格：** 托管模型 $0.50-1.00/M 输入，专用端点单独定价
- **免费额度：** 注册送 $10 信用（比大部分慷慨）
- **国内访问：** ❌ 需要代理
- **最适合：** 需要专用容量的企业、Ray/Anyscale 栈用户

### 6. FreeModel — 国内直连聚合器

- **端点：** `https://api.freemodel.dev/v1`
- **模型：** 50+ 包括 DeepSeek V3/R1、Qwen 2.5、Llama 3.1-3.3、Mistral、Claude 3.5 Sonnet、GPT-4o
- **价格：** 按模型定价，通常低于官方西方价格
- **免费额度：** 注册送信用
- **国内访问：** ✅ 直连（无需代理）——主要卖点
- **最适合：** 需要国际模型（Claude、GPT-4o）但又不想用代理的国内开发者。[通过 FreeModel 注册](https://freemodel.dev/invite/FRE-7a3b6220)

### 7. DeepSeek — 最便宜的顶级模型

- **端点：** `https://api.deepseek.com/v1`
- **模型：** DeepSeek-V3、DeepSeek-R1（推理）、DeepSeek-Coder
- **价格：** $0.14-0.27/M 输入，$0.28-1.10/M 输出——**2026 年最便宜的顶级模型**
- **免费额度：** 注册送 $2 信用
- **国内访问：** ✅ 直连（国内原生公司）
- **最适合：** 推理任务、代码生成、成本敏感的高吞吐量工作负载

### 8. apikey.fun — 国内直连 Claude + GPT

- **端点：** `https://api.apikey.fun/v1`
- **模型：** 40+ 包括 Claude 3.5 Sonnet、GPT-4o、Gemini 2.5 Pro、DeepSeek、Qwen、Kimi
- **价格：** ¥1 = $1（透明公式：官方价格 × 分组倍率 ÷ 7）
- **免费额度：** 新用户注册信用
- **国内访问：** ✅ 直连
- **最适合：** 需要 Claude Code、OpenAI Codex、Gemini 2.5 Pro 的国内开发者

### 9. vLLM — 自托管开源

- **端点：** 自托管，默认 `http://localhost:8000/v1`
- **模型：** 任何能塞进你 GPU 的 HuggingFace 模型
- **价格：** 你的硬件成本（A100 约 $2-4/小时，H100 spot 约 $1-2/小时）
- **免费额度：** 不适用（自托管）
- **国内访问：** ✅ 取决于你的服务器
- **最适合：** 数据隐私、大规模成本（>10M tokens/天）、自定义模型

### 10. LiteLLM — 通用网关

- **端点：** 自托管代理，默认 `http://localhost:4000`
- **模型：** 路由到 100+ 提供商（OpenAI、Anthropic、Bedrock、Vertex、Azure、以上所有提供商）
- **价格：** 免费（开源）+ 路由目标的成本
- **免费额度：** 不适用
- **国内访问：** 取决于上游
- **最适合：** 多提供商路由、fallback 链、预算上限、跨提供商统一日志

## 价格对比（Llama 3.3 70B 级模型）

| 提供商 | 输入 ($/1M) | 输出 ($/1M) | 免费额度 | 缓存折扣 | 最佳卖点 |
|---|---|---|---|---|---|
| DeepSeek V3 | $0.14 | $0.28 | $2 信用 | $0.014 缓存 | ✅ 最便宜 SOTA |
| Groq Llama 70B | $0.59 | $0.79 | 1K 请求/天 | 无 | ✅ 最快 |
| Together AI Llama 70B | $0.90 | $0.90 | $5 信用 | $0.45 缓存 | ✅ 微调 |
| Fireworks AI Llama 70B | $0.90 | $0.90 | $1 信用 | $0.45 缓存 | ✅ 企业级 |
| OpenAI GPT-4o-mini | $0.15 | $0.60 | $5 (3 月) | $0.075 缓存 | — 基准线 |
| OpenAI GPT-4o | $2.50 | $10.00 | $5 (3 月) | $1.25 缓存 | — 高级 |
| Anthropic Claude 3.5 Sonnet | $3.00 | $15.00 | $5 (1 月) | $0.30 缓存 | — 推理 |
| Google Gemini 2.5 Pro | $1.25 | $10.00 | 2 请求/分钟 免费 | $0.31 缓存 | — 长上下文 |

**规律：** DeepSeek V3 在相似推理质量下比 Claude 3.5 Sonnet 便宜 5-10 倍。Groq 因为 LPU 效率是 Llama 70B 等级中最便宜的。GPT-4o-mini 是最便宜的 OpenAI 原生选项，也是最简单的迁移路径。

## 迁移指南：3 行代码切换提供商

下面这段代码对 6 个不同的提供商都有效：

```python
# 之前 — OpenAI
from openai import OpenAI
client = OpenAI(api_key="sk-...")  # 使用默认 base_url
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "你好"}]
)
```

```python
# 之后 — Groq（即插即用）
from openai import OpenAI
client = OpenAI(
    api_key="gsk_...",
    base_url="https://api.groq.com/openai/v1"  # ← 唯一改动
)
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # ← 只改模型名
    messages=[{"role": "user", "content": "你好"}]
)
```

```python
# DeepSeek（最便宜）
client = OpenAI(api_key="sk-...", base_url="https://api.deepseek.com/v1")
response = client.chat.completions.create(model="deepseek-chat", messages=[...])

# Together AI
client = OpenAI(api_key="...", base_url="https://api.together.xyz/v1")
response = client.chat.completions.create(model="meta-llama/Llama-3.3-70B-Instruct-Turbo", messages=[...])

# OpenRouter（200+ 模型）
client = OpenAI(api_key="sk-or-...", base_url="https://openrouter.ai/api/v1")
response = client.chat.completions.create(model="anthropic/claude-3.5-sonnet", messages=[...])

# FreeModel（国内直连，50+ 模型）
client = OpenAI(api_key="fm-...", base_url="https://api.freemodel.dev/v1")
response = client.chat.completions.create(model="deepseek-v3", messages=[...])

# apikey.fun（国内直连，Claude + GPT）
client = OpenAI(api_key="akf-...", base_url="https://api.apikey.fun/v1")
response = client.chat.completions.create(model="claude-3-5-sonnet", messages=[...])
```

**每次迁移改两处：`base_url` 和 `model` 名称。** 流式、function calling、JSON mode 全部工作方式相同。

## 使用场景推荐

| 使用场景 | 推荐提供商 | 原因 |
|---|---|---|
| 实时聊天，首 token < 200ms | Groq（Llama 3.1 8B Instant） | 1,250 tok/sec，$0.05/M 输入 |
| 语音 agent / 电话机器人 | Groq（Llama 3.3 70B Versatile） | 确定性低延迟 |
| 代码补全 IDE | Groq（Llama 3.1 8B Instant） | 亚 100ms 响应，接近免费 |
| 推理任务（数学、规划） | DeepSeek-R1 或 OpenAI o1 | 推理调优模型 |
| 成本敏感的批量（百万级文档） | DeepSeek V3 或 Fireworks | 最便宜的 per-token，高吞吐 |
| 微调领域模型 | Together AI 或 Fireworks | LoRA/QLoRA 支持 |
| 多模型 fallback（聊天 app） | OpenRouter | 单 API，200+ 模型，自动路由 |
| 国内生产 | FreeModel 或 apikey.fun | 无代理，可访问西方模型 |
| 数据敏感（医疗、法律） | 自托管 vLLM | 数据不离开你的基础设施 |
| 多提供商统一日志 | LiteLLM 代理 | 统一账单、统一日志、统一认证 |

## 局限和坑

- **模型命名不统一。** Groq 用 `llama-3.1-8b-instant`，Together 用 `meta-llama/Llama-3.3-70B-Instruct-Turbo`，OpenRouter 用 `meta-llama/llama-3.3-70b-instruct`。同一个底层模型在不同提供商有 3+ 个不同的 ID。
- **Function calling 支持程度不一。** 大部分提供商支持 OpenAI 风格的 `tools` 参数，但一些老的支持 `function_call`。务必用你的具体工具 schema 测试。
- **流式输出大部分是 SSE，但不是全部。** 少数提供商把流包装在 JSON lines 里。OpenAI Python SDK 自动处理两种，但自定义客户端需要识别格式。
- **Token 计数有差异。** 大部分提供商使用接近 GPT-4 的 tokenizer，但 Qwen 和 DeepSeek 用自己的 BPE tokenizer。你代码里的 "1K tokens" 在不同提供商上可能计费 1,200 tokens。
- **速率限制是提供商级别，不是模型级别。** 一个有 100 个模型的提供商可能有一个全局速率限制，所以一个模型的重度使用会饿死其他模型。
- **有些 "OpenAI 兼容" 端点是部分的。** 少数提供商跳过 embeddings 端点、audio 端点或 assistants 端点。迁移前务必检查提供商的 `/v1/models` 列表。

## 常见问题

**Q：从 OpenAI 切换到其他提供商真的能省钱吗？**
A：对大部分工作负载，是的——50-90% 的成本削减是现实的。例外是你需要 GPT-4o 级推理的场景。对 Llama 70B 级工作负载，Groq 和 DeepSeek 比 GPT-4o 便宜 5-10 倍。坑是模型质量不同。迁移前用你自己的 prompt 测试。

**Q：所有 OpenAI 兼容 API 都支持 function calling 吗？**
A：大部分支持，但实现方式不同。Groq、OpenRouter、Together AI、Fireworks AI 都支持 OpenAI 风格的 `tools` 参数。一些较小的提供商只支持旧的 `function_call` 参数，或者完全跳过工具调用。务必用测试调用验证。

**Q：2026 年生产环境用哪个提供商最好？**
A：OpenAI 兼容生产：Groq（如果你能接受开源模型）、Together AI（需要微调时）、OpenRouter（需要模型灵活性时）。国内生产：FreeModel 或 apikey.fun。数据敏感工作负载：自托管 vLLM。

**Q：我能用 OpenAI Python SDK 调用这些提供商吗？**
A：能——这正是重点。把 `base_url` 设为提供商的端点，其余代码不变。大部分提供商的文档都展示了 OpenAI、Anthropic、LlamaIndex SDK 的一行改动方法。

**Q：Anthropic Claude 呢——它是 OpenAI 兼容的吗？**
A：不是。Claude 用不同的 API schema（Messages API，不是 Chat Completions）。要在 OpenAI 兼容接口中使用 Claude，通过 OpenRouter 或 apikey.fun 路由，它们把 Claude 包装成 OpenAI 格式。直接使用 Claude 需要 `anthropic` SDK。

**Q：缓存（caching）在不同提供商上怎么工作？**
A：Anthropic 开创了 prompt caching，OpenAI 加上了，大部分 OpenAI 兼容提供商现在都支持。缓存读取通常比标准输入价格便宜 50-90%。对长系统 prompt（>2K tokens），缓存能省不少钱。实现是提供商特定的——查看每个提供商的文档。

**Q：哪个提供商的免费额度最好？**
A：Groq——每天 1,000 请求，无需信用卡，无过期。大部分其他提供商是 $1-10 信用额度，30-90 天过期。Groq 的免费额度对业余项目和小规模生产工作负载真的有用。

## 对比表（最终）

| 提供商 | 端点类型 | 主要场景 | 最便宜模型 | 速度 | 国内访问 | 最佳选择 |
|---|---|---|---|---|---|---|
| OpenRouter | 聚合器 (200+) | 多模型访问 | 不定 | 不定 | ❌ 代理 | 路由、fallback |
| Groq | 纯推理 | 实时应用 | $0.05/M (Llama 8B) | ⚡ 最快 (LPU) | ❌ 代理 | 语音、聊天 |
| Together AI | 推理 + 微调 | 自定义模型 | $0.18/M (Llama 8B) | 中 | ❌ 代理 | 微调 |
| Fireworks AI | 纯推理 | 生产 | $0.20/M (Llama 8B) | 快 | ❌ 代理 | 批量、企业 |
| Anyscale | 企业级 Ray | 专用容量 | $0.50/M (Llama 70B) | 中 | ❌ 代理 | 企业 |
| FreeModel | 聚合器 (50+, 国内) | 国内直连 | 按模型 | 中 | ✅ 直连 | 国内 + 西方模型 |
| DeepSeek | 国内原生 | 成本敏感 | $0.14/M (V3) | 快 | ✅ 直连 | 最便宜 SOTA |
| apikey.fun | 聚合器 (40+, 国内) | Claude/GPT 国内 | ¥1=$1 公式 | 中 | ✅ 直连 | Claude Code 用户 |
| vLLM | 自托管开源 | 数据隐私 | 硬件成本 | 取决于 GPU | ✅ 自有 | 隐私、规模 |
| LiteLLM | 通用网关 | 多提供商路由 | 免费 (代理) | N/A | N/A | 统一日志 |

## 结论

2026 年的 OpenAI 兼容 API 生态已经足够成熟，**对大部分 LLM 工作负载，你不需要把 OpenAI 作为主提供商。** 现在的决策树是：

- **需要原始 SOTA 推理？** OpenAI o1/o3 或 Claude 3.5 Sonnet（通过 OpenRouter）。
- **需要速度？** Groq，不用犹豫。
- **需要规模化成本？** DeepSeek V3，然后是 Groq（开源模型）。
- **需要微调？** Together AI 或 Fireworks AI。
- **需要国内访问？** FreeModel（50+ 模型）或 apikey.fun（Claude/GPT 国内）。
- **需要数据隐私？** 自托管 vLLM。

迁移成本接近零——改你现有 OpenAI 客户端的 `base_url` 和 `model`，测试，部署。大部分团队发现他们能把 60-80% 的 OpenAI 用量替换为 30-50% 的成本，同时在实时场景上获得延迟改善。

如果你不想注册 10 个服务就能开始探索，可以从 [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) 入手——一个账号给你 DeepSeek、Qwen、Llama、Claude、GPT-4o 走同一个 OpenAI 兼容端点，自带国内直连。配合 Groq 的免费额度处理实时工作负载，第一天你就有了 90% 生产可用的栈。
