---
title: "Qwen3.5 API 2026：阿里云百炼 vs 开源权重"
description: "Qwen3.5 与阿里云百炼 API 完全指南 2026：核验后的定价、三种访问路径（托管 API、开源权重、聚合器），与 Kimi K3、DeepSeek V4 逐项对比。"
pubDate: 2026-07-20
provider: "aliyun"
category: "domestic"
featured: true
---

# Qwen3.5 API 2026：阿里云百炼 vs 开源权重

Qwen3.5 是 Hugging Face 上下载量最高的中文开源 LLM 系列，阿里云百炼平台是跳过自建 GPU 集群直接调用它的最快方式。截至 2026 年 7 月，Qwen3 系列在国内外团队的选型中处于活跃轮转位置——最接近的竞争对手是 Kimi K3 和 DeepSeek V4。

本文是一份实战指南。你将获得 Qwen3.5 模型矩阵的核验清单、阿里云百炼的最新定价、三种可行的访问路径（托管 API、开源权重自托管、聚合器），以及与 Kimi K3、DeepSeek V4 的逐项对比。

## Qwen3.5 家族在售型号（2026 年 7 月）

当前 Qwen3 系列分两条线：

- **Qwen3-2507（Instruct + Thinking 双模式）**——2025 年 7 月发布，三种 MoE 尺寸：235B-A22B、30B-A3B 和 4B 稠密。2507 系列是支持双模式的版本（每个请求可在 Instruct 与 Thinking 之间切换）。
- **Qwen3.5（Plus、Max、Instruct 多版本）**——2026 年初在阿里云百炼正式商用的生产线，覆盖 72B / 32B / 14B / 7B 几个尺寸。这是阿里云控制台默认展示的版本。

两条线不是同一个模型。如果你在阿里云 API 看到「Qwen3-Plus」或「Qwen3.5-Max」，那是 Qwen3.5 托管线。如果你在 Hugging Face 看到「Qwen3-235B-A22B-Instruct-2507」，那是 2507 开源权重版本，支持混合推理。

| 模型 | 类型 | 激活参数量 | 上下文 | 许可证 | 获取渠道 |
|---|---|---|---|---|---|
| Qwen3-235B-A22B-Instruct-2507 | MoE | 22B | 256K | Apache 2.0 | Hugging Face、ModelScope |
| Qwen3-30B-A3B-Instruct-2507 | MoE | 3B | 256K | Apache 2.0 | Hugging Face、ModelScope |
| Qwen3-4B-Instruct-2507 | Dense | 4B | 256K | Apache 2.0 | Hugging Face、ModelScope |
| Qwen3.5-Max | 托管 | 不公开 | 128K | 专有 | 仅阿里云百炼 |
| Qwen3.5-Plus | 托管 | 不公开 | 128K | 专有 | 仅阿里云百炼 |
| Qwen3.5-72B-Instruct | Dense | 72B | 128K | 专有 | 阿里云百炼 |
| Qwen3.5-32B-Instruct | Dense | 32B | 128K | 专有 | 阿里云百炼 |
| Qwen-Omni-Turbo | 多模态 | 不公开 | 32K | 专有 | 阿里云百炼 |
| Qwen-VL-Plus | 视觉 | 不公开 | 32K | 专有 | 阿里云百炼 |

Qwen3-2507 系列在 Hugging Face 上的 235B-A22B 是今天你可以自托管的最大国产开源权重模型。Qwen3.5 家族是阿里云真正卖 API 访问权限的生产线。

## 阿里云百炼定价（核验 2026-07-20）

以下价格来自阿里云百炼平台按量付费模式服务，CNY 每百万 token。海外用户走 bailian-ss.aliyun.com 国际站用 USD 单独计费——跨境部署前请在国际站控制台确认。

| 模型 | 输入 ¥/M | 输出 ¥/M | 备注 |
|---|---|---|---|
| Qwen3.5-Max | 4 | 12 | 旗舰级，混合推理 |
| Qwen3.5-Plus | 2 | 6 | 默认生产模型 |
| Qwen3.5-72B-Instruct | 4 | 12 | 大尺寸稠密，benchmark 与 Max 接近 |
| Qwen3.5-32B-Instruct | 2 | 6 | 中端甜点位 |
| Qwen3.5-14B-Instruct | 1 | 3 | 最便宜的指令微调版本 |
| Qwen3.5-7B-Instruct | 0.6 | 1.8 | 最低档，快速迭代 |
| QwQ-32B | 2 | 8 | 推理模型，数学能力接近 o1-mini |
| Qwen-Omni-Turbo | 4（文本） | 12（文本） | 音频输入单独计费 |
| Qwen-VL-Plus | 2 | 6 | 视觉输入，按图计费 |

免费额度：阿里云新用户送 1,000,000 token，90 天有效期。足够原型设计和小批量评测。

## 2026 年访问 Qwen3.5 的三种方式

### 路径一：阿里云百炼（托管，最快）

最简单的路径。在 bailian.console.aliyun.com 注册并创建 API key 后，调用 OpenAI 兼容端点。百炼暴露了 OpenAI 兼容的 `/v1/chat/completions` 接口，所以现有 OpenAI 客户端代码只需要改两行就能跑。

```bash
# 阿里云百炼 OpenAI 兼容端点
curl https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-plus",
    "messages": [{"role": "user", "content": "用一段话解释 MoE LLM 是什么。"}],
    "temperature": 0.7
  }'
```

Python：

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DASHSCOPE_API_KEY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

resp = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[{"role": "user", "content": "用一段话解释 MoE LLM。"}],
    temperature=0.7,
)
print(resp.choices[0].message.content)
```

注意响应使用标准 OpenAI Python 客户端。`base_url` 替换是唯一改动，其他（流式、函数调用、JSON 模式）全部照常工作。

### 路径二：开源权重自托管（规模化时最便宜）

如果日处理量超过 5000 万 token，在 Modal、RunPod 或 baseten 上自托管比 API 便宜。Hugging Face 上的 Qwen3-235B-A22B-Instruct-2507 权重（Apache 2.0）是目前可自托管的最大开源 MoE——每 token 激活 22B 参数，总参数量 235B。

```python
# Hugging Face transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "Qwen/Qwen3-235B-A22B-Instruct-2507"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    # MoE：BF16 总占用约 470GB；需 2-4 张 H100/H200
)

messages = [{"role": "user", "content": "MoE LLM 是什么？"}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True))
```

完整 235B-A22B Instruct 需要 470GB 磁盘（BF16，分片）。要拿 Qwen3 90% 的质量、付 10% 的成本，跑 Qwen3-30B-A3B-Instruct-2507（激活 3B）就行，单卡 H100 即可。

### 路径三：聚合器（海外访问）

中国大陆以外的用户，阿里云国际站（bailian-ss.aliyun.com）是独立计费通道。更省事的路径是走聚合器：

- **OpenRouter**——暴露 Qwen3-Plus 和 Qwen3.5-Max，USD 计费
- **Together AI**——运行 Qwen3-235B-A22B-Instruct-2507，输入 $0.20/M
- **Fireworks AI**——提供 Qwen3-30B-A3B，TTFB 在亚秒级
- **Replicate**——按秒计费，A100/H100 实例

聚合器定价各有差异，部署前请逐家确认。

## Qwen3.5 vs Kimi K3 vs DeepSeek V4（2026 年 7 月）

| 能力 | Qwen3.5-Plus | Kimi K3 | DeepSeek V4 |
|---|---|---|---|
| 激活参数 | 不公开（托管） | 不公开（托管） | 不公开（托管） |
| 总参数 | 未披露 | 2.8T（MoE） | 1.6T（MoE） |
| 上下文 | 128K | 1M | 256K |
| 输入价格（¥/M） | 2 | 2（缓存命中）/ 20（未缓存） | 2 |
| 输出价格（¥/M） | 6 | 100 | 8 |
| 原生视觉 | ✅（Qwen-VL-Plus） | ✅ | ❌ |
| 音频输入 | ✅（Qwen-Omni-Turbo） | ❌ | ❌ |
| 工具调用 | ✅（DashScope） | ✅ | ✅ |
| 开源权重 | ❌ | ✅ | ✅ |
| 最佳场景 | 国内企业级、多模态 | 超长上下文、中文 | 数学/代码、最便宜 |

生产环境要重点看的三个差异：

1. **上下文窗口**：Kimi K3 默认 1M token。Qwen3.5 是 128K。如果你在做 200K 以上文档分析，Kimi K3 胜出。
2. **输出价格**：Qwen3.5-Plus 输出 ¥6/M 属于中段。DeepSeek V4 输出 ¥8/M 相当；Kimi K3 未缓存输出 ¥100/M 在长生成场景贵 12-16 倍。
3. **多模态**：Qwen-Omni-Turbo 是三者中唯一支持音频输入的。如果你要做语音到 LLM 的流水线，选 Qwen。

## Apple Intelligence 维度（说明）

2026 年 7 月有报道称 Apple 正将 Qwen3.5 集成到 Apple Intelligence 的中国大陆版本。这是厂商路线图项，截至本文撰写时还未正式 GA。如果你面向中国大陆 iOS 用户发布产品，即使主模型是别的，也请为 Qwen3.5 准备一条兜底路径。

## 不要用 Qwen3.5 的三种场景

1. **你需要 200K 以上上下文**。Qwen3.5-Plus 是 128K。改用 Kimi K3（1M）或用开源权重 Qwen3-235B-A22B-Instruct-2507 + 长上下文微调。
2. **你在海外、想要最便宜推理**。聚合器定价参差不齐；纯成本角度，DeepSeek V4 在 Modal 自托管永远比 Qwen3.5 便宜。
3. **你需要严格 schema 校验的原生 Function Calling**。Qwen3.5 支持函数调用但 schema 强制比 GPT-4o 或 Claude Sonnet 5 弱。请用你的具体工具定义显式测试。

## 5 分钟快速上手

```bash
# 1. 在 bailian.console.aliyun.com 注册
# 2. 创建 API key，设为环境变量
export DASHSCOPE_API_KEY="YOUR...Key"

# 3. 测试 API
curl https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3.5-plus", "messages": [{"role": "user", "content": "你好"}]}'

# 4. 把你已有代码里 OpenAI 客户端的 base_url 换掉
# 完成——Python/JS/curl 接口与 OpenAI 完全一致
```

## 结论

Qwen3.5 配合阿里云百炼是国内团队、多模态应用、阿里云既有客户场景下的正确选择。开源权重 Qwen3-235B-A22B-Instruct-2507 是想要最大开源 MoE 又不想按 token 付费的自托管团队的正确选择。纯长上下文（200K+）选 Kimi K3。最便宜生产推理选 DeepSeek V4 自托管。

最大的坑：Qwen3.5 托管 API 和 Qwen3-2507 开源权重不是同一个模型。按场景选，别按「Qwen3」品牌名选。

## 常见问题

### Qwen3.5 支持函数调用吗？

支持，通过 DashScope 的 `/v1/services/aigc/text-generation` 端点的 `tools` 参数。Schema 强制力度比 GPT-4o 或 Claude Sonnet 5 弱——请用你具体的工具定义测试。

### 我能用 OpenAI Python 客户端访问阿里云百炼吗？

能。阿里云百炼在 `https://dashscope.aliyuncs.com/compatible-mode/v1` 暴露 OpenAI 兼容端点。把 OpenAI 客户端的 `base_url` 设为该 URL，其余代码无需改动。

### Qwen3.5-Max 和 Qwen3.5-Plus 的区别是什么？

Max 是旗舰级生产模型（输入 ¥4/M，输出 ¥12/M），支持混合推理，benchmark 表现最好。Plus 是中段默认模型（输入 ¥2/M，输出 ¥6/M），成本仅一半，覆盖大多数生产场景。

### Qwen3.5 是开源的吗？

Qwen3-2507 系列（235B-A22B、30B-A3B、4B）是 Hugging Face 上的 Apache 2.0。Qwen3.5 托管模型（Max、Plus、72B、32B、14B、7B）是专有的——仅通过阿里云百炼访问。

### Qwen3.5 定价和 DeepSeek V4 相比如何？

Qwen3.5-Plus 输入 ¥2/M、输出 ¥6/M 与 DeepSeek V4 输入 ¥2/M、输出 ¥8/M 相当。决定因素通常是多模态支持（Qwen 胜出）与数学/代码基准（DeepSeek 胜出）。

### 我能在单 GPU 上跑 Qwen3-235B-A22B 吗？

不能。235B-A22B 模型需要 470GB BF16 / 235GB INT4。完整精度需要 2-4 张 H100/H200（80GB）或 4-8 张 A100（80GB）。单卡选项是 Qwen3-30B-A3B-Instruct-2507（激活 3B，总 60GB）。

### Qwen3.5 支持多模态输入吗？

支持，通过 Qwen-VL-Plus（视觉）和 Qwen-Omni-Turbo（文本 + 图像 + 音频）。这两个模型在百炼控制台里是独立模型，不是 Qwen3.5-Plus 的端点。多模态 token 的计费单价和文本不同。

### Qwen3.5 在代码生成场景如何？

阿里云有 Qwen3.5-Coder 这条独立模型线，专门针对代码补全和仓库级任务。定价和 Qwen3.5-72B-Instruct 相当。开源最佳代码模型方面，Qwen2.5-Coder-32B-Instruct 在 Hugging Face 上仍具竞争力。
