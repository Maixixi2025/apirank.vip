---
title: "阶跃星辰 Step-2 API 2026 测评：多模态旗舰、Step-R 推理与价格"
description: "阶跃星辰 Step-2 API 2026 深度测评：1.2T 多模态旗舰、Step-R 推理、OpenAI 兼容端点、国内直连、按量计费价格明细。"
slug: "stepfun-api-review"
provider: "stepfun"
published: true
date: "2026-08-05"
type: "review"
---

# 阶跃星辰 Step-2 API 2026 测评：多模态旗舰、Step-R 推理与价格

## 引言：为什么 2026 年要关注阶跃星辰

阶跃星辰（Stepfun）是 2023 年成立于上海的 AI 实验室，其 **Step-2** 模型是 1.2 万亿参数的多模态旗舰，通过单一 OpenAI 兼容端点接受文本、图像、音频与视频输入。⚠️ 与多数按模态分别计费、需独立视觉 API 的中国 LLM 栈不同，Step-2 把所有输入都视为 content part —— 视频理解调用与文本对话走同一条计费路径。实验室同时提供 **Step-R** 推理模型，对标 OpenAI o1 与 DeepSeek R1，价格约为前者的 1/5。

对 2026 年 8 月的阶跃星辰给一个诚实的定位：它**不**是 GPT-5.6 或 Claude Opus 5 那种"基础预训练刷榜级"对手。Step-2 在文本基准上属于中国开源权重阵营的中上游；在多模态榜单（MMMU、MMBench、MathVista）位列前三。阶跃星辰的判断是：对于中国 LLM 市场中需要"单端点多模态流水线 + 廉价 o1 替代推理"的那一块，多模态合一的便利性胜过 MMLU 上 3 分的提升。对那一块市场 —— 国内多模态生产 Agent、视频理解流水线、OCR 重型文档推理 —— Step-2 是最直接的一线官方答案。

另一个阶跃星辰在 2026 年评测中持续出现的原因：**OpenAI 兼容的 API 表面**意味着基于 OpenAI SDK 的现有栈只需更换 base URL 即可切换到阶跃星辰。对于希望保留 API 可移植性、又不想重写 agent 代码的团队，这种结构性优势是决定性的。

## 模型族：Step-2 / Step-2-mini / Step-1 / Step-1.5V / Step-R / Step-CC

阶跃星辰当前的生产线是 **Step-2 → Step-2-mini → Step-1 → Step-1.5V** 多模态阶梯，加上 **Step-R** 推理线与 **Step-CC** 代码补全端点。所有 chat 模型均通过同一 `https://platform.stepfun.com/v1/chat/completions` 端点按名称选择。

### Step-2 —— 1.2T 多模态旗舰

最大生产模型。通过单一 chat-completions 接口接受文本、图像、音频、视频。128K 上下文。定价 **¥6 输入 / ¥18 输出 每百万 token**（约 $0.83 / $2.50）。Step-2 适用于"多模态理解必须是开源权重阵营顶尖、且希望一个 API 表面统一处理文本 + 像素 + 音频 + 视频"的场景。在 MMMU 与 MathVista 上，Step-2 位列中国开源权重前三；2026 年初中文 CV-Bench-QA 上，体型更小的 Step-1.5V 排名第一。

### Step-2-mini —— 快速多模态

Step-2 的 200B 参数快速版。同一多模态表面（文本 + 图像 + 音频 + 视频），但上下文 32K，吞吐高 5-10 倍。定价 **¥1 输入 / ¥3 输出 每百万 token**（约 $0.14 / $0.42）。Step-2-mini 适用于高量多模态 Agent、批量图像分类，以及任何需要多模态感知但不需要完整 Step-2 质量提升的工作负载。

### Step-1 —— 上代 300B 多模态旗舰

上一代旗舰。文本 + 图像多模态，32K 上下文。定价 **¥4 输入 / ¥12 输出 每百万 token**（约 $0.56 / $1.67）。Step-1 仍在线上运行，服务那些想要稳定、文档完善的多模态端点的调用方 —— 该模型 GA 时间足够长，边界情况已被充分理解。

### Step-1.5V —— 视觉调优

专用视觉模型，200B 参数。定价 **¥3 输入 / ¥9 输出 每百万 token**（约 $0.42 / $1.25）。对于 OCR 重型文档推理、密集图像理解、纯视觉工作负载，Step-1.5V 是首选 —— 2026 年初在中文 CV-Bench-QA 排名第一。

### Step-R —— o1 / R1 同级推理

阶跃星辰对标 OpenAI o1 与 DeepSeek R1 的推理模型，链式思考通过标准流式接口暴露。64K 上下文。定价 **¥8 输入 / ¥24 输出 每百万 token**（约 $1.11 / $3.33）。在 MATH-500 与 HumanEval 上，Step-R 与 DeepSeek R1 持平，价格约为 OpenAI o1 的 1/5、R1 的 2 倍。关键差异点：当 Step-R 与 Step-2 串联使用时，多模态上下文（图像 + 视频）会在推理过程中保留 —— 规划器读入多模态输入，推理器基于结构化表示进行推理。

### Step-CC —— 代码补全

一线代码补全端点，**¥1 / ¥2 每百万 token**（约 $0.14 / $0.28）。IDE 友好：低延迟内联建议，按 token 流式。Step-CC 适用于延迟主导而非推理深度的内联 IDE 补全。

### Step-Embed —— 嵌入（1024 维）

1024 维文本嵌入模型，上下文 8K，用于多模态 RAG 流水线的检索侧。与 Step-2 自然配对，做端到端多模态 RAG。

## 价格（2026-08-05 验证）

词元价格单位为人民币每百万 token。30 天免费窗口结束后，阶跃星辰按预充值按量计费。

| 模型 | 输入 (¥/M) | 输出 (¥/M) | 美元等值 | 备注 |
|---|---|---|---|---|
| Step-2 | ¥6 | ¥18 | $0.83 / $2.50 | 万亿参数多模态旗舰 |
| Step-2-mini | ¥1 | ¥3 | $0.14 / $0.42 | Step-2 快速版，200B |
| Step-1 | ¥4 | ¥12 | $0.56 / $1.67 | 300B 多模态，上代 |
| Step-1.5V | ¥3 | ¥9 | $0.42 / $1.25 | 视觉调优 200B |
| Step-R | ¥8 | ¥24 | $1.11 / $3.33 | 推理，o1 / R1 同级 |
| Step-CC | ¥1 | ¥2 | $0.14 / $0.28 | 代码补全 |

对比 2026 年 8 月时点上最接近的中美替代品：

- **Step-2 vs OpenAI GPT-5**（$1.25 / $10）：Step-2 输入便宜 33%，输出便宜 75%，且国内直连。
- **Step-2 vs Anthropic Claude Sonnet 5**（$3 / $15）：Step-2 输入便宜 50%，输出便宜 83%。
- **Step-2 vs DeepSeek V3.2**（¥0.14 / ¥0.28，纯文本）：Step-2 输入贵 40 倍，但这是这几家里**唯一**在单一端点提供原生多模态的。
- **Step-R vs OpenAI o1**（$15 / $60）：Step-R 约为 o1 价格的 1/5。
- **Step-R vs DeepSeek R1**（¥4 / ¥16）：Step-R 是 R1 价格的 2 倍，但与 Step-2 配对时具备多模态上下文继承。

## OpenAI Python SDK 接入

```python
from openai import OpenAI
client = OpenAI(
    base_url="https://platform.stepfun.com/v1",
    api_key="YOUR_STEPFUN_API_KEY"
)
response = client.chat.completions.create(
    model="step-2",
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": "总结这个视频片段。"},
            {"type": "video_url", "video_url": {"url": "https://example.com/clip.mp4"}}
        ]}
    ]
)
print(response.choices[0].message.content)
```

同一 `base_url` 适用于任何 OpenAI 兼容框架适配器（LangChain、LlamaIndex、Vercel AI SDK 等）。阶跃星辰同时提供官方 Python SDK（含多模态辅助），仓库 `github.com/stepfun-ai` —— 适合需要流式 token 用量统计、图像感知缓存、Step-CC completions 端点的调用方。

## Step-R 推理：1/5 价格的 o1 替代

Step-R 是阶跃星辰模型阵容中最被低估的一项。关键数字：**¥8 输入 / ¥24 输出 每百万 token**。OpenAI o1 定价 $15 / $60 —— Step-R 约为 1/5。DeepSeek R1 定价 ¥4 / ¥16 —— Step-R 是其 2 倍，但多模态上下文继承显著更强。

差异点在推理必须作用于多模态上下文时。标准生产模式是：用 Step-2 作为规划器（它能读图、解析文档、看视频），用 Step-R 作为推理器（它接收结构化计划 + 多模态上下文进行推理）。链式思考通过流式接口暴露，推理过程可在最终答案前被检查。

**代价**。Step-R 是纯文本 —— 推理模型本身不接受图像 / 视频输入。多模态上下文必须来自规划器调用。Step-R 同样没有原生 tool calling，工具型 Agent 需把它包在规划器层中。

## 对比 DeepSeek V3.2 / Qwen3.5-Max / Kimi K3

| 厂商 | 旗舰 | 上下文 | 输入/输出(每 M) | 多模态 | 国内直连 |
|---|---|---|---|---|---|
| 阶跃星辰 | Step-2 | 128K | ¥6 / ¥18 | ✅ 单一端点 | ✅ |
| DeepSeek | V3.2 | 64K | ¥0.14 / ¥0.28 | ❌ 纯文本 | ✅ |
| 阿里 Qwen | Qwen3.5-Max | 1M | ¥4 / ¥12 | ✅ 独立 VL | ✅ |
| 月之暗面 Kimi | K3 | 1M | ¥2 / ¥20 | ✅ 原生 | ✅ |
| OpenAI | GPT-5 | 128K | $1.25 / $10 | ✅ 走 GPT-4o | ❌ 需代理 |

**Step-2 的主要优势**是单端点多模态流水线。单一 chat-completions 调用即可处理任意组合的文本/图像/音频/视频。

**DeepSeek V3.2 胜在**裸价（输入 token 便宜 10 倍），但仅文本且需调用方额外集成视觉 API。

**Qwen3.5-Max 与 Kimi K3 领先**于上下文窗口（1M token），更适合代码仓库或长文档 RAG。

**OpenAI GPT-5 仍主导**生态成熟度与 tool calling，但中国大陆无法直接访问。

国内多模态生产负载，Step-2 是当前开源权重阵营中接口最干净的方案。

## 已知限制

- **128K 上下文**落后于 Kimi K3 与 Qwen3.8-Max（均为 1M）。
- **国际端点仅香港**，美/欧延迟高于国内。
- **Function Calling 处于 Beta**，生产调用方需在 Step-2 外面包一层规划器做工具路由。
- **官网无 SOC 2 / HIPAA 文档**，部署医疗或金融负载前需在合同中确认企业合规条款。
- **模型发布节奏中等**，部分新模型 Beta 周期长于竞品。
- **除标准预充值档位外**，无批量或量级折扣。

## 选型建议

当你需要在中国大陆以单一 OpenAI 兼容端点获得一线多模态 LLM 接入，或以 o1 / R1 1/5 价格获得推理替代（Step-R）时，选阶跃星辰。

**不要选阶跃星辰**如果：你需要 1M token 上下文（Kimi K3、Qwen3.8-Max）；需要最便宜纯文本（DeepSeek V3.2）；需要美国前沿生态 + tool calling（OpenAI GPT-5）；或需要永久免费档位（100 万 token / 30 天 是唯一的免费路径）。

务实的建议是：按 OpenAI `/v1/chat/completions` 契约写代码，部署时再选底层服务商 —— 这样将来迁移到 OpenAI、Anthropic、Google 或其他国产厂商只是配置变更，不是重写。

## 关联披露

APIRank 与阶跃星辰**没有**联盟营销关系。本测评中 FreeModel 侧边栏是 OpenAI 兼容的免费档多厂商路由替代，不是阶跃星辰的联盟营销。Token 价格、模型阵容与免费档细节已在 2026-08-05 从 `https://platform.stepfun.com/` 与 `https://docs.stepfun.com/` 验证。

## 相关阅读

- Qwen3.8-Max API 测评 —— 1M 上下文 + 95B 激活参数开源旗舰
- DeepSeek V3.2 API 测评 —— ¥0.14/M 最便宜国产纯文本
- Kimi K3 API 测评 —— 1M 上下文 + 原生多模态
- OpenAI GPT-5.6 Luna 测评 —— 永久降价 80%，美侧生态
- AI API 成本控制工具 2026 横评 —— Cloudflare AI Gateway、Portkey、LiteLLM 对比
- FreeModel 聚合器 —— OpenAI 兼容的免费档路由，适合原型与个人项目
