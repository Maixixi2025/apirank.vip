---
title: "DeepInfra API 完整测评 2026：50+ 模型行业最低价 | APIRank"
description: "DeepInfra API 测评：50+ 开源模型，Llama 3.3 70B 仅 $0.35/M，DeepSeek V3、Qwen2.5、OpenAI 兼容、批量推理 5 折。对比 Together AI 与 Groq。"
slug: "deepinfra-api-review"
provider: "deepinfra"
published: false
date: "2026-06-05"
type: "review"
nameCn: "DeepInfra"
zhTitle: "DeepInfra API 完整测评 2026：50+ 模型，行业最低价"
zhDescription: "DeepInfra API 测评：50+ 开源模型，Llama 3.3 70B 仅 $0.35/M，DeepSeek V3、Qwen2.5、OpenAI 兼容、批量推理 5 折。对比 Together AI 与 Groq。"
---

# DeepInfra API 完整测评 2026：50+ 模型，价格屠夫

## 引言：开源 LLM 推理的成本之王

DeepInfra 于 2022 年上线，定位极其清晰：把开源 LLM 推理做到业界最便宜。与 Groq 拼速度、Cerebras 自研芯片不同，DeepInfra 选择了一条更接地气的路线——用顶级 NVIDIA GPU（H100、H200、A100），跑自家深度优化的推理引擎，把 token 成本压到极限。

结果是这家 serverless 推理平台托管了 50+ 开源权重模型，价格比同行低 30-60%。Llama 3.3 70B 在 DeepInfra 跑 $0.35/M 输入 + $0.40/M 输出——比 Together AI、Fireworks 便宜 30%，比自建 AWS GPU 集群更省。DeepSeek V3 与 DeepSeek R1 分别定价 $0.45/M 和 $0.55/M，是开发者用上这些前沿推理模型最便宜的入口。

对开发者来说，最大吸引力是迁移成本极低：相同的 OpenAI 客户端代码，只换 `base_url`，应用就立刻享受大幅降本。DeepInfra 原生支持 OpenAI API 规范——流式输出、function calling、JSON mode、视觉（支持模型）一应俱全。代价也有：单请求吞吐不如 Groq/Cerebras，没有 fine-tuning 服务。但对成本敏感的生产工作负载、批量处理、研究项目而言，DeepInfra 几乎无可替代。

## DeepInfra API 定价明细

DeepInfra 采用**按 token 计费**模式，输入与输出分开计价。定价完全透明，每个模型在 dashboard 单独公示。无订阅费、无最低消费、无隐藏基础设施附加费。

| 模型 | 输入 ($/M tok) | 输出 ($/M tok) | 上下文窗口 | 备注 |
|-------|----------------|----------------|------------|------|
| Llama 3.3 70B Instruct | $0.35 | $0.40 | 128K | Meta 旗舰，性价比最高 |
| Meta-Llama-3.1-405B-Instruct | $0.90 | $0.90 | 128K | 前沿级开源大模型 |
| Meta-Llama-3.1-8B-Instruct | $0.04 | $0.05 | 128K | 最便宜的生产级 8B |
| Meta-Llama-3.1-70B-Instruct | $0.35 | $0.40 | 128K | 上一代 70B |
| Mistral Small 24B | $0.07 | $0.07 | 32K | 性价比欧系模型 |
| Qwen2.5-72B-Instruct | $0.35 | $0.40 | 128K | 国内顶级开源 |
| Qwen2.5-Coder-32B | $0.10 | $0.10 | 32K | 代码场景最佳性价比 |
| DeepSeek V3 | $0.45 | $0.55 | 64K | 综合强于 Llama 70B |
| DeepSeek R1 | $0.55 | $2.19 | 64K | 推理模型，输出贵 |
| Phi-4 (14B) | $0.07 | $0.07 | 16K | 微软小模型 |
| Gemma 2 27B | $0.18 | $0.18 | 8K | Google 开源 |

### 免费额度

DeepInfra 注册即送 **$1 免费额度**，无需信用卡。这点钱能跑约 250 万 token 的 Llama 3.3 70B，或 2000 万 token 的 8B 模型——足以做完整评估和小原型。额度用完后，最低 $5 起充值预付。

### 批量推理（5 折优惠）

DeepInfra 的杀手锏是**serverless 批量推理**：单次 API 调用提交最多 1000 个请求，DeepInfra 在 24 小时内处理完毕，按 token 价格 5 折计费。非常适合评估流水线、数据集标注、批量摘要、或者任何不需要实时响应的场景。

### $100 能跑多少 token？

以 Llama 3.3 70B 的 $0.35/M 输入 + $0.40/M 输出计算，$100 大约能跑 **2.7 亿 token**（输入+输出混合）。换算成实际场景：

- **~13,500 轮长对话**（每轮 10K 输入 + 10K 输出）
- **~540,000 次 API 调用**（每次 500 token）
- **~30 小时连续聊天**（按 70B 典型速度）

这相当于同金额在 OpenAI GPT-4o 上能跑 token 量的 3 倍。DeepInfra 是当下最便宜的前沿级开源推理选项。

## 速度基准：DeepInfra 与竞品对比

DeepInfra 不是最快的——Groq 与 Cerebras 才是。但按**单位美元吞吐（tokens per dollar per second）**衡量，DeepInfra 极具竞争力。

| 提供商 | Llama 3.3 70B 速度 | 首 token 延迟 | 综合价 ($/M tok) |
|----------|---------------------|---------------|------------------|
| **DeepInfra** | **~150 tok/s** | **500ms 以内** | **$0.375**（混合） |
| Cerebras | 2,000+ tok/s | 200ms 以内 | $0.60 |
| Groq (LPU) | 450 tok/s | 300ms 以内 | $1.78/M（输入+输出求和） |
| Together AI | 120 tok/s | 1s 以内 | $1.38/M |
| Fireworks AI | 180 tok/s | 600ms 以内 | $1.40/M |
| OpenAI GPT-4o | 80 tok/s | 500ms 以内 | $12.50/M |

DeepInfra 比 Cerebras/Groq 慢 5-10 倍，但**单 token 价格便宜 5-10 倍**。对非实时负载（批量处理、离线文档分析、数据集生成），DeepInfra 的成本优势是决定性的。

## OpenAI 兼容 API：60 秒迁移

DeepInfra 实现完整的 OpenAI Chat Completions 规范：

- 流式输出（`stream: true`）
- Function calling / 工具调用
- JSON mode（`response_format: { type: "json_object" }`）
- System messages
- 多轮对话
- 视觉输入（Llama 3.2 Vision、Qwen-VL 模型）
- Token 用量统计

迁移只需 60 秒：

```python
# 从 OpenAI 切换到 DeepInfra —— 只改 base_url 和 api_key
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DEEPINFRA_TOKEN",
    base_url="https://api.deepinfra.com/v1/openai",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct",
    messages=[{"role": "user", "content": "用两句话解释 token 定价"}],
)
print(response.choices[0].message.content)
```

无 SDK 变更、无新抽象层、无数据迁移。同一份 `openai-python` SDK，同样的请求/响应结构，同样的错误码。

## 模型矩阵：DeepSeek、Qwen、Mistral、Phi、Llama 一网打尽

DeepInfra 的模型目录是开发者的好朋友——每款主流开源模型发布后数周内即可上。截至 2026 年 6 月：

**前沿级（70B+）：**
- Llama 3.3 70B Instruct
- Meta-Llama-3.1-405B-Instruct
- Qwen2.5-72B-Instruct
- DeepSeek V3（671B MoE，激活 37B）
- DeepSeek R1（推理模型）

**中等规模（7B-32B）：**
- Mistral Small 24B、Mistral 7B
- Qwen2.5-Coder-32B-Instruct
- Phi-4（14B）
- Gemma 2 27B

**轻量高效：**
- Llama 3.1 8B
- Mistral 7B
- Phi-3.5 Mini

**专用模型：**
- DeepSeek Coder V2（代码专用）
- CodeLlama 系列
- Whisper（语音转文字）
- Llama 3.2 Vision（多模态）

50+ 模型数量大约是 Groq 或 Cerebras 的 3 倍。DeepInfra 是跨模型家族测试的最全平台。

## 使用场景：什么时候选 DeepInfra

| 使用场景 | 是否推荐 | 原因 |
|----------|----------|------|
| 实时聊天机器人 | ⚠️ 可用 | Cerebras/Groq 更快，但 DeepInfra 成本可控 |
| 代码补全（Copilot 类） | ✅ 推荐 | 500ms 内延迟，单 token 成本低 |
| 批量文档分析 | ✅ 最佳 | 批量 5 折 + 大上下文 |
| 数据集生成 | ✅ 最佳 | 最便宜的前沿级 70B，跑合成数据 |
| 研究实验 | ✅ 最佳 | 便宜，能跑 1000+ 模型对比 |
| 生产环境面向 C 端 LLM | ⚠️ 谨慎 | 无 SLA；需要 SLA 选 Together AI 或 Fireworks |
| 多模态（视觉） | ⚠️ 有限 | 视觉支持有但不如 OpenAI 全面 |
| 国内直连 | ❌ 不行 | 需代理；选 aliyun/zhipu/tencent |

## DeepInfra vs Together AI vs Groq vs Fireworks

| 维度 | DeepInfra | Together AI | Groq | Fireworks AI |
|-----------|-----------|-------------|------|--------------|
| 模型数量 | 50+ | 200+ | 7 | 100+ |
| 70B 最低价 | $0.35/M | $0.59/M | $0.79/M | $0.50/M |
| 速度（70B tok/s） | 150 | 120 | 450 | 180 |
| 免费额度 | $1 | $5 | 限速免费 | $1 |
| Fine-tuning | ❌ | ✅ | ❌ | ✅ |
| 批量折扣 | ✅ 5 折 | ❌ | ❌ | ✅ 7 折 |
| 企业 SLA | ❌ | ✅ | ✅ | ✅ |
| OpenAI 兼容 | ✅ | ✅ | ✅ | ✅ |

**选 DeepInfra 当：** 成本是首要因素、需要 DeepSeek V3/R1、跑批量任务、或者预算紧的研究项目。

**选 Together AI 当：** 需要 fine-tuning、模型目录更广、或者企业级 SLA。

**选 Groq 当：** 极低延迟至关重要（语音 Agent、实时聊天、代码补全）。

**选 Fireworks AI 当：** 需要 fine-tuning + 快速推理 + 良好企业支持。

## 优缺点

**优点：**
- ✅ 多数模型业内最低价
- ✅ 50+ 开源模型，包括 DeepSeek V3/R1、Qwen2.5、Llama 3.3
- ✅ OpenAI 兼容 API，60 秒迁移
- ✅ 405B 模型 $0.90/M 接入（独家价位）
- ✅ Serverless 批量推理 5 折
- ✅ 注册即送 $1 免费额度，无需信用卡

**缺点：**
- ⚠️ 单请求吞吐不如 Groq/Cerebras（150 vs 2,000 tok/s）
- ⚠️ 国内访问需稳定代理
- ⚠️ 不提供 fine-tuning 服务
- ⚠️ 无企业 SLA，只有尽力而为的可用性
- ⚠️ 多模态（视觉、音频）支持不如 OpenAI 全面

## 常见问题

**Q：DeepInfra 真的比 Together AI 便宜吗？**
A：是的，同款模型便宜 30-50%。Llama 3.3 70B 在 DeepInfra 是 $0.35/M 输入，Together AI 是 $0.59/M。DeepSeek V3 在 DeepInfra 是 $0.45/M，Together AI 是 $0.90/M。代价是吞吐速度和企业级功能。

**Q：能从国内访问 DeepInfra 吗？**
A：不能直接访问。api.deepinfra.com 经常被 GFW 屏蔽。国内开发者通常走代理，或者用香港/台湾节点，或者通过 FreeModel 这类 OpenAI 兼容的 API 中转（聚合多个后端）。要完全国内直连，请考虑阿里云百炼、智谱、腾讯混元。

**Q：DeepInfra 支持 fine-tuning 吗？**
A：不支持。DeepInfra 只做推理。fine-tuning 请用 Together AI、Fireworks AI，或自己跑训练（RunPod / Lambda Labs）。

**Q：批量推理 5 折是怎么算的？**
A：单次 API 调用向批量端点提交最多 1000 个请求，DeepInfra 在 24 小时内处理完毕，token 价格 5 折。适合数据集生成、批量分类、任何不需要同步响应的任务。

**Q：DeepInfra 适合生产环境吗？**
A：对大多数初创公司和中规模应用来说是。历史可用性 99.9%+，但没有正式 SLA。对受监管行业（金融、医疗）或关键任务，请考虑 Together AI、Fireworks 或 Azure OpenAI。

**Q：能在 DeepInfra 跑 DeepSeek R1 吗？**
A：可以。DeepInfra 是最早规模化托管 DeepSeek R1 的平台之一。定价 $0.55/M 输入 + $2.19/M 输出（输出贵是因为推理链产生更多 token）。

## 结论：开源 LLM 推理的预算之选

DeepInfra 是为那些更看重单 token 价格、而非峰值吞吐的开发者设计的成本优先 LLM API。50+ 模型覆盖 Llama 3.3 70B 仅 $0.35/M、DeepSeek V3、Qwen2.5 等几乎所有主流开源需求，价格业内最低。

对延迟敏感的实时应用，把 DeepInfra 与 Groq 或 Cerebras 配合使用。对成本敏感的批量处理、数据集生成、研究项目，DeepInfra 是明显赢家。OpenAI 兼容 API 让迁移只需 60 秒，一个下午就能 A/B 测试成本。

如果你在预算紧的情况下需要前沿级开源模型，DeepInfra 是起点。如果需要 fine-tuning、SLA、或者峰值速度，升级到 Together AI、Fireworks 或 Groq。要国内直连，用阿里云百炼、智谱、腾讯混元。

---

## 延伸阅读

- [DeepInfra 官方文档](https://deepinfra.com/docs)
- [DeepInfra 定价页](https://deepinfra.com/pricing)
- [DeepInfra 上的 DeepSeek V3](https://deepinfra.com/deepseek-ai/DeepSeek-V3)
- [Together AI 测评（对比参考）](https://apirank.vip/zh/providers/together-ai/)
- [Groq 测评（对比参考）](https://apirank.vip/zh/providers/groq/)
