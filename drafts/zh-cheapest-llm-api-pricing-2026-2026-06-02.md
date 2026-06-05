---
title: "2026 最便宜的 LLM API：真实价格对比（GPT-4o、Claude、Gemini、DeepSeek、Doubao）"
description: "2026 年 20+ 个 LLM API 价格横评。我们将每百万 token 价格、缓存价格、免费额度统一标准化，帮编程、写作、长文本、中国访问场景找到最便宜的选择。"
slug: "cheapest-llm-api-pricing-2026"
provider: "cross-provider"
published: false
date: "2026-06-02"
type: "comparison"
---

# 2026 最便宜的 LLM API：真实价格对比

## 为什么 2026 年价格变得越来越重要

2024 年的 LLM API 市场很简单：OpenAI、Anthropic、Google，加上一长串开源模型供应商。到 2026 年，局面已经爆发 —— 20 多个生产级 LLM API 商业化运营，价格区间从 ByteDance Doubao 的 0.02 美元/百万输入 token 到 Claude Opus 4.7 的 75 美元/百万输出 token。对于一个月处理 5 亿 token 的创业公司，能力相当模型中，最便宜和最贵档位的差距可能达到 5 万美元/月。

本文将我们追踪的所有 LLM API 的每百万 token 价格统一标准化，使用实际工作负载中常见的 3:1 输入输出比，并加入隐藏成本（缓存、限速、最低承诺）。结果是单一的排名表，你可以直接用来为具体场景挑选最便宜的 API。

所有价格截至 2026 年 6 月，按各供应商官方定价页面验证。中国供应商的美元等价价格按 $1 = ¥7 计算（APIKEY.FUN 参考汇率，与 2026 年中主要交易所汇率基本持平）。

## 方法论：如何比较价格

我们对所有供应商使用三个标准化指标：

1. **输入价格 / 百万 token** —— 发送给模型的 prompt token 费率
2. **输出价格 / 百万 token** —— 模型生成 token 的费率
3. **缓存读取价格 / 百万 token** —— 重复 prompt 前缀的折扣价（Anthropic prompt caching、OpenAI automatic caching、DeepSeek cache）

以人民币计价的供应商，我们按 $1 = ¥7 换算。按秒计 GPU 费的供应商（Replicate），我们使用 70B 级别模型已发布的每 token 等价。免费额度单独报告，不从每 token 价格中扣除。

我们排除没有公开按 token 定价的供应商（如仅企业闭门合同），以及不再接受新注册的供应商。截至 2026 年 6 月，对比涵盖 20 个活跃供应商。

## 2026 最便宜 LLM API 排名（每百万 token 价格）

下表按每个供应商最便宜且能用的模型排名，对比相同工作负载（1M 输入 + 333K 输出 token = 在中位价上约花费 $100）：

| 排名 | 供应商 | 最便宜的可用模型 | 输入 $/1M | 输出 $/1M | 缓存读 $/1M | $100 约等于 token 数 |
|------|----------|------------------------|-----------|-------------|-----------------|---------------|
| 1 | ByteDance Doubao | Doubao Lite | $0.02 | $0.02 | 不支持 | 5,000M |
| 2 | Google AI | Gemini 2.0 Flash | $0.03 | $0.06 | $0.005 | 3,300M |
| 3 | Mistral AI | Mistral Small 3 | $0.20 | $0.60 | $0.02 | 500M |
| 4 | DeepSeek | DeepSeek V3 Chat | $0.14 | $0.28 | $0.014 | 714M |
| 5 | Cohere | Command R7B | $0.15 | $0.60 | 不支持 | 500M |
| 6 | OpenAI | GPT-4.1 nano | $0.10 | $0.40 | $0.03 | 833M |
| 7 | xAI Grok | Grok-3 mini | $0.30 | $0.50 | 不支持 | 333M |
| 8 | Together AI | Llama 3.3 70B | $0.88 | $0.88 | 不支持 | 170M |
| 9 | Zhipu AI | GLM-4-Flash | $0.71 | $0.71 | 不支持 | 211M |
| 10 | Anthropic | Claude 3.5 Haiku | $0.80 | $4.00 | $0.03 | 125M |
| 11 | Fireworks AI | Llama 3.1 8B | $0.20 | $0.20 | $0.02 | 500M |
| 12 | Anyscale | Llama 3.3 70B | $0.15 | $0.15 | 不支持 | 667M |
| 13 | Moonshot Kimi | moonshot-v1-8k | $2.86 | $2.86 | $0.57 | 35M |
| 14 | APIKEY.FUN | Claude Haiku 4.5 | $1.00 | $5.00 | $0.04 | 100M |
| 15 | Alibaba Bailian | Qwen-Turbo | $0.57 | $0.57 | 不支持 | 263M |
| 16 | Baidu Ernie | ERNIE-Speed | $1.71 | $1.71 | 不支持 | 88M |
| 17 | Tencent Hunyuan | hunyuan-Turbo | $0.86 | $3.43 | 不支持 | 116M |
| 18 | OpenRouter | （按模型，+5.5% 平台费） | $0.05+ | $0.10+ | 视模型 | 2,000M+ |
| 19 | Stability AI | Stable LM 2 12B | $4.00 | $4.00 | 不支持 | 25M |
| 20 | Replicate | Llama 3 70B | $0.16/秒 | $0.49/秒 | 不支持 | ~140M |

*Token 数基于 3:1 输入输出比（1M 输入 + 333K 输出）。缓存价格仅在 prompt 重复时适用。*

## 按场景划分的最便宜选择

### 海量文本分类（每天 100M+ token）

高吞吐量的分类、抽取、嵌入类工作负载，模型智能要求不高，更看重吞吐量：

- **ByteDance Doubao Lite**，$0.02/百万输入 token，是绝对最便宜的生产级 API。质量低于前沿模型，但足以应对分类、简单抽取、中文任务。
- **Gemini 2.0 Flash**，$0.03/百万输入 token，是英文工作负载中性价比最高的选择。100 万 token 上下文窗口对长文档处理是加分项。
- **GPT-4.1 nano**，$0.10/百万，是 OpenAI 最便宜模型，如果需要 OpenAI 的工具调用、JSON 模式、稳定性，它是首选。

### 代码生成（需要前沿质量）

代码生成需要前沿推理 —— 便宜模型会产出过多编译错误。能保持 GPT-4 级别质量的最便宜选项：

- **DeepSeek V3 Chat**，$0.14/百万输入 token，是 2026 年最便宜的前沿质量模型。在 HumanEval、MBPP、SWE-bench 上表现与 Claude Sonnet 4.5、GPT-4.1 相差不超过 5%，但价格只有十分之一。
- **Mistral Small 3**，$0.20/百万，是最便宜的欧洲托管前沿级别模型。代码能力强，欧盟托管满足 GDPR 合规。
- **Alibaba Bailian 上的 Qwen-Turbo**，$0.57/百万，是最便宜的中文托管模型，代码生成质量与 GPT-4o mini 相当。

### 长上下文（100K+ token）

长上下文工作负载由输入成本主导。具有 100K+ 上下文窗口的最便宜供应商：

- **Google Gemini 2.0 Flash** —— 1M token 上下文，$0.03/百万输入。2026 年最佳 price-per-context-token 比率。
- **Moonshot Kimi** —— 128K 上下文，官方 API $2.86/百万输入。价格更高，但 Kimi 处理中文长文本能力超过任何其他模型。
- **Anthropic Claude 3.5 Haiku** —— 200K 上下文，$0.80/百万输入，prompt caching 重复前缀仅 $0.03/百万。

### 国内直连（无需 VPN）

对于中国大陆用户，无需代理的最便宜选择：

- **ByteDance Doubao** —— 国内原生，无需代理。绝对最低价格（$0.02/百万）。
- **Zhipu AI GLM-4-Flash** —— 国内原生，$0.71/百万，128K 上下文，慷慨的免费额度。
- **Alibaba Bailian Qwen-Turbo** —— 国内原生，$0.57/百万，与阿里云服务深度集成。
- **APIKEY.FUN** —— 多模型聚合，国内直连节点。¥1 = $1 透明定价；无需 VPN 即可访问 Claude、GPT、Gemini、DeepSeek。
- **FreeModel** —— DeepSeek 官方合作伙伴，国内直连，注册即送免费额度。

## 免费额度对比：谁给的免费 token 最多

2026 年的免费额度市场很分散。有些供应商给的可用于生产，有些给的额度一个下午就用完：

| 供应商 | 免费额度 | 实际价值 | 是否需要信用卡 |
|----------|-----------|-----------|----------------|
| Google AI | 慷慨免费额度，Gemini 2.0 Flash 无限（限速） | 综合最佳免费额度 | 不需要 |
| OpenAI | $5 额度（3 个月内有效） | 约 33M GPT-4.1 nano token | 不需要 |
| DeepSeek | $2 额度（一次性） | 约 14M V3 Chat token | 不需要 |
| Cohere | 试用 key 1,000 req/月 | 受请求数限制 | 不需要 |
| Mistral | 限速免费额度 | 约 10M Small token | 不需要 |
| Grok | 免费层，限速 | 约 5M Grok-3 mini token | 不需要 |
| xAI | 通过 X 账号领免费额度 | 浮动 | 不需要 |
| Zhipu AI | GLM-3-Turbo 全免费，GLM-4-Flash 限量 | 国内最慷慨免费额度 | 不需要 |
| Alibaba Bailian | Qwen-Turbo 免费配额 | 对国内用户充足 | 需要（阿里云） |
| Baidu Ernie | ERNIE-Lite 全免费 | 对国内用户充足 | 需要（百度） |
| Stability AI | 25 积分（≈3 张 SD 3.5 图） | token 等价：少 | 不需要 |
| Replicate | 注册免费积分 | 少，浮动 | 不需要 |
| APIKEY.FUN | 注册奖励（¥10-50） | 通过分组定价约 10-50M token | 不需要 |
| FreeModel | 注册奖励（按模型） | 与 APIKEY.FUN 相当 | 不需要 |

**生产用最佳免费额度：** Google AI 的 Gemini 2.0 Flash 无限层仍是黄金标准。撞到限速前，你可以用它搭一个可观的副业项目。

**国内用户最佳免费额度：** Zhipu AI 的 GLM-3-Turbo（真免费，无配额限制）和 Alibaba Bailian 的 Qwen-Turbo（阿里云用户免费配额）。

**国内访问 Claude 和 GPT 的最佳免费额度：** FreeModel 和 APIKEY.FUN 都提供注册额度，国内直连无需 VPN。

## $100 压力测试：100 美元能买什么

把每 token 价格转换为更具体的东西，以下是 $100 在每个供应商最便宜可用模型上能买到的 token 数（假设 3:1 输入输出比）：

- **Doubao Lite 上花 $100** = 约 50 亿 token（足以总结 5 万本书）
- **Gemini 2.0 Flash 上花 $100** = 约 33 亿 token
- **DeepSeek V3 上花 $100** = 约 7.14 亿 token（前沿质量，大多数应用足够）
- **GPT-4.1 nano 上花 $100** = 约 8.33 亿 token
- **Claude 3.5 Haiku 上花 $100** = 约 1.25 亿 token
- **GPT-4o**（非 nano）**上花 $100** = 约 5 千万 token
- **Claude Sonnet 4.5 上花 $100** = 约 3 千万 token
- **Claude Opus 4.7 上花 $100** = 约 7 百万 token

最便宜档位比最贵档位同样一美元能多拿 100 倍的 token。

## 速度对比：最便宜档位的吞吐量

价格只是故事的一半。对于实时应用（聊天机器人、代码助手、语音 agent），token/秒才是关键：

| 供应商 | 最便宜模型 | 中位输出速度 |
|----------|----------------|---------------------|
| Grok | Grok-3 mini | 280 tok/sec |
| Google AI | Gemini 2.0 Flash | 250 tok/sec |
| DeepSeek | DeepSeek V3 | 180 tok/sec |
| Fireworks AI | Llama 3.1 8B | 220 tok/sec |
| Mistral | Mistral Small 3 | 150 tok/sec |
| OpenAI | GPT-4.1 nano | 130 tok/sec |
| Together AI | Llama 3.3 70B | 120 tok/sec |
| APIKEY.FUN | （转发） | 100 tok/sec |
| Zhipu AI | GLM-4-Flash | 100 tok/sec |
| Alibaba Bailian | Qwen-Turbo | 90 tok/sec |

对延迟敏感的应用，**Grok-3 mini** 和 **Gemini 2.0 Flash** 是最便宜且快速的选项。

## 代码示例：调用最便宜的 API

### DeepSeek V3（Python）

```python
import requests

response = requests.post(
    "https://api.deepseek.com/v1/chat/completions",
    headers={"Authorization": "Bearer YOUR_DEEPSEEK_API_KEY"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "用 100 字解释量子纠缠"}],
        "max_tokens": 200,
    },
    timeout=30,
)
print(response.json()["choices"][0]["message"]["content"])
```

### Gemini 2.0 Flash（curl）

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=YOUR_GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "光速是多少？"}]}]
  }'
```

### Doubao Lite（OpenAI 兼容端点）

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DOUBAO_API_KEY",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
)

response = client.chat.completions.create(
    model="doubao-lite-32k",
    messages=[{"role": "user", "content": "翻译成法语：你好，世界！"}],
    max_tokens=100,
)
print(response.choices[0].message.content)
```

## FAQ

**Q: 2026 年绝对最便宜的 LLM API 是哪个？**
A: ByteDance Doubao Lite，0.02 美元/百万输入 token。质量低于前沿模型，但足以应对分类、简单抽取、中文任务。

**Q: 最便宜的 API 就是最好的 API 吗？**
A: 不是。最便宜模型（Doubao Lite、Gemini Flash）是为成本优化，不是为推理优化。需要深度推理的任务（数学、代码、多步规划），前沿模型如 Claude Sonnet 4.5 或 GPT-4.1 在价格高 10-50 倍的情况下，正确率更高，每个正确答案的成本反而更低。

**Q: 为什么 DeepSeek 这么便宜？**
A: DeepSeek 运行在定制 H800 集群上，为推理优化，公司采用低毛利高量策略。他们还用 MoE 架构（V3 总参 671B 但每 token 仅激活 37B），大幅降低计算成本。

**Q: 中国大陆以外能用 ByteDance Doubao 吗？**
A: 可以 —— 火山引擎（字节跳动云平台）通过 ark.cn-beijing.volces.com 或全球端点提供国际访问。价格相同。

**Q: 访问 Claude 和 GPT 最便宜的 API 是哪个？**
A: FreeModel（DeepSeek 官方合作伙伴）和 APIKEY.FUN 都以有竞争力的价格提供 Claude 和 GPT 访问，国内直连节点无需 VPN。

**Q: 缓存价格如何影响总成本？**
A: 缓存价格对带重复 prompt 前缀的工作负载影响最大。带固定 system prompt 的客服机器人、带有项目上下文的代码助手、带相同文档前缀的 RAG 管道，可以通过使用 Anthropic 的 prompt caching（$0.03/百万 vs $0.80/百万）或 DeepSeek 的 cache（$0.014/百万 vs $0.14/百万），把输入成本降低 80-90%。

**Q: 免费额度是否包含限速？**
A: 是的。即使 Google 的"无限"Gemini 2.0 Flash 免费层也有限速（标准层 15 RPM、1500 RPD）。生产工作负载应规划付费层或混合方案。

**Q: 我应该用多模型聚合器吗？**
A: OpenRouter、FreeModel、APIKEY.FUN 这样的聚合器加一点小费率（OpenRouter 5.5%，其他家透明定价），但允许你用一个 API key 切换 Claude、GPT、Gemini、DeepSeek。这对于需要在故障时回退到不同模型的产品来说，是最佳方案。

## 结论：如何为你挑选最便宜的 LLM API

2026 年最便宜的 LLM API 取决于四个因素：所需质量、地理、场景、量级。

**月处理 token 不超过 100M 的美国/欧洲创业团队：** 从 Google AI 的 Gemini 2.0 Flash 免费层开始，规模增长后转付费。英文工作负载中最佳 price-to-quality 比率。

**代码密集型应用：** 用 DeepSeek V3 作为默认。Claude 或 GPT 十分之一的价格，前沿质量。

**国内团队：** 用 ByteDance Doubao（最便宜，国内原生）、Zhipu GLM-4-Flash（最便宜档位的中文质量最佳）、或 FreeModel / APIKEY.FUN（多模型聚合，国内直连 Claude 和 GPT）。

**长上下文工作负载（100K+ token）：** 用 Gemini 2.0 Flash（1M 上下文）或 DeepSeek V3（128K 上下文，激进的缓存价格）。

**多模型生产系统：** 用 OpenRouter、FreeModel、APIKEY.FUN 这样的聚合器，无需更换集成代码即可切换模型。微小加价在系统韧性面前值得。

最贵的错误是对不需要的任务用 Claude Opus 或 GPT-4.1。简单的双层路由 —— 分类/抽取用便宜模型、生成用前沿模型 —— 通常能砍掉 70% 的 LLM 成本且无明显质量损失。
