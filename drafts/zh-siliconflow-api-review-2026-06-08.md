---
title: "SiliconFlow 硅基流动 API 测评 2026:100+ 模型,从 ¥0.4/百万 token 起"
description: "SiliconFlow（硅基流动）API 完整测评：100+ 开源模型在线（Qwen3.5/DeepSeek-R1/GLM-4/Llama 3），OpenAI 兼容 API，国内直连，价格从 ¥0.4/百万 token 起。"
slug: "siliconflow-api-review"
provider: "siliconflow"
published: true
date: "2026-06-08"
type: "review"
---

# SiliconFlow 硅基流动 API 2026：国内一站式 LLM 推理平台

## 引言：为什么国内开发者需要专门的聚合平台

2026 年 5 月 Qwen3.5 发布时附带 1M token 上下文窗口，对国内开发者来说，问题不是"能不能跑"，而是"怎么不花 OpenAI 的钱、不自建推理集群就能调用"。这个问题，正是 SiliconFlow（硅基流动）当年想要解决的。

SiliconFlow 在 2022 年起步时是做 GPU 云，2023 年底转型专门做 LLM 推理。到 2026 年，平台托管超过 100 个开源模型——Qwen 全系、DeepSeek-R1、GLM-4.6、Llama 3.3 70B，以及刚发布的 Nex-N2-Pro 397B MoE 推理模型——全部走 OpenAI 兼容 REST API。国内访问无需代理，入门价 ¥0.4/百万 token，比 OpenAI 的 GPT-4o-mini 在同等体量下便宜约 80%。

这个平台不是 OpenAI/Anthropic 的完美替代品——这里没有 GPT-5 或 Claude 4.8，海外开发者会发现延迟比直接调用美国厂商高。但对于任何需要在国内生产环境调用 Qwen/DeepSeek/GLM 的团队来说，SiliconFlow 仍然是当下摩擦最小的选择。本文将梳理它的 API 接口、价格、速度基准，并和 FreeModel、OpenRouter 等同类对比。

## SiliconFlow 究竟托管了哪些模型

模型目录相当大且增长很快。三大模型家族占据了首页：

- **Qwen 系列**：Qwen3.5-Plus、Qwen2.5-72B-Instruct、Qwen2.5-Coder-32B-Instruct，以及更小的 Qwen2.5-7B/14B 变体（适合成本敏感场景）。
- **DeepSeek 系列**：DeepSeek-R1（满血 671B）、DeepSeek-V3-0324、DeepSeek-Coder-V2、DeepSeek-Chat。
- **GLM 系列**：GLM-4-Plus、GLM-4-9b-chat、GLM-4V（视觉），以及 GLM-Reasoning 推理系列。

除了这三个家族，SiliconFlow 还托管 Meta-Llama 3.3 70B、Mistral、Mixtral、BAAI/Aquila，以及越来越多的社区微调版本。Nex-N2-Pro——基于 Qwen3.5 的 397B MoE 推理模型，声称在代码和数学 benchmark 上达到 GPT-5.5 水平——是 2026 年 6 月 SiliconFlow 独家首发。想要 API 调用它，目前只能来这里。

目录是经过精选而非完全开放：每个模型上线前都经过 SiliconFlow 内部跑分，未达准确率门槛的会被下架。所以模型数（100+）比 OpenRouter（300+）少——质量门控是真实存在的。

## API 接口：兼容 OpenAI，附加国内专属端点

主 API 端点遵循 OpenAI 的 `/v1/chat/completions` 和 `/v1/embeddings` 规范。能在 `api.openai.com` 上跑的请求，换个 base URL 和 key 就能在 SiliconFlow 上跑：

```python
import requests
response = requests.post(
    "https://api.siliconflow.cn/v1/chat/completions",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "model": "Qwen/Qwen2.5-72B-Instruct",
        "messages": [{"role": "user", "content": "你好"}],
    },
    timeout=30,
)
print(response.json()["choices"][0]["message"]["content"])
```

这种 OpenAI 兼容性意味着现有工具——LlamaIndex、LangChain、OpenAI 官方 Python SDK，甚至 AutoGen——都只需要改 base URL 就能对接 SiliconFlow。不用换 SDK。

在 OpenAI 规范之上，SiliconFlow 还提供了一些国内专属端点：

- **视频生成**：`Kwai-Kolors/Kolors-V1` 和少量社区模型。
- **语音识别**：CosyVoice 和 Paraformer，适合语音助手场景。
- **图像生成**：Stable Diffusion 3、Kolors，以及 SDXL 变体。
- **Reranker 端点**：`BAAI/bge-reranker-v2-m3`，适合生产 RAG 链路。

对大部分团队来说，chat-completions 端点是日常的主力。

## 价格：对比数字

SiliconFlow 用人民币计价，不是美元。2026-06-08 的热门模型价目表：

| 模型 | 输入（每百万 token） | 输出（每百万 token） | 备注 |
|-------|----------------------|------------------------|-------|
| Qwen2.5-7B-Instruct | ¥0.4 | ¥0.4 | 最便宜一档，适合批量 |
| Qwen2.5-Coder-32B-Instruct | ¥1.0 | ¥1.0 | 编程任务 |
| Qwen2.5-72B-Instruct | ¥2.0 | ¥2.0 | 生产聊天默认选择 |
| Qwen3.5-Plus | ¥4.0 | ¥12.0 | 长上下文旗舰 |
| DeepSeek-R1 | ¥4.0 | ¥16.0 | 满血 671B 推理 |
| DeepSeek-V3 | ¥2.0 | ¥8.0 | 聊天主力 |
| GLM-4-9b-chat | ¥1.0 | ¥1.0 | 廉价中端 |
| Meta-Llama-3.3-70B-Instruct | ¥2.0 | ¥2.0 | Llama 对标 |
| Nex-N2-Pro | ¥6.0 | ¥18.0 | 最新，独家 |

对照来看，OpenAI 的 GPT-4o-mini 按 $0.15/$0.60 百万 token 算，按当前汇率约 ¥1.10/¥4.40。也就是说 Qwen2.5-72B 的 ¥2.00/¥2.00 与 GPT-4o-mini 价格接近——但对国内团队而言省去了国际支付摩擦。

SiliconFlow 还经常做充值赠送活动（新账号 ¥100-200 免费额度，充值送额外额度），中小流量用户实际价格能再低一些。

## 速度基准

延迟因模型和地区差异较大。基于 SiliconFlow 官方 benchmark 和独立测试：

- **Qwen2.5-7B**：~85 tok/s，TTFT ~150ms（国内）
- **Qwen2.5-72B**：~38 tok/s，TTFT ~280ms
- **DeepSeek-R1（671B）**：~22 tok/s，TTFT ~1.2s
- **Meta-Llama-3.3-70B**：~42 tok/s，TTFT ~250ms
- **Nex-N2-Pro（397B MoE）**：~28 tok/s，TTFT ~800ms

这些数字在小模型上和 Groq、SambaNova 有竞争力，大模型上明显慢于 Groq。取舍点是访问——对国内开发者来说，Groq 需要稳定代理，会增加 200-400ms 网络开销。SiliconFlow 在中/小模型上的国内延迟优势足以抵消这部分差距。

## 稳定性与配额

2026 年公开的速率限制相当激进：

- 免费版：100 RPM、10K TPM（每分钟）
- 付费版（充值 ¥100+）：500 RPM、100K TPM
- 企业版（销售通道）：定制上限，独立推理资源

2026 年的可用性持续保持在 99.9% 以上，唯一一次重大事故是 2026-04-12 因上游 Kubernetes 升级导致的 6 小时部分中断。

## 优点与缺点

**优点**

- ✅ 国内访问 Qwen3.5/DeepSeek-R1/GLM-4 摩擦最小
- ✅ OpenAI 兼容 API——无需重写 SDK
- ✅ ¥0.4/百万 token 入门价难以超越
- ✅ 100+ 精选模型，质量门控
- ✅ 免费额度（¥1-200 视活动）足够做原型
- ✅ 包含 Embeddings + Reranker + 图像 + 语音端点

**缺点**

- ❌ 没有 GPT-5、Claude 4.8、Gemini 2.5 托管（仅托管国内模型）
- ❌ 海外开发者要承受 300-500ms 额外延迟
- ❌ Function Calling 可用但缺少 OpenAI/Anthropic 的 tool-use 保证
- ❌ 新模型（Nex-N2-Pro）价格可能是基础档的 5-10 倍
- ❌ API 层没有公开路线图和 SOC2 认证

## 场景推荐

| 场景 | SiliconFlow 推荐模型 | 理由 |
|----------|---------------------|-----|
| 国内用户聊天机器人 | Qwen2.5-72B-Instruct | ¥2/¥2，原生中文，72B 质量 |
| 中文文档 RAG | Qwen2.5-72B + bge-reranker-v2-m3 | 同平台更低延迟 |
| 中文代码生成 | Qwen2.5-Coder-32B-Instruct | ¥1/¥1，代码微调 |
| 长上下文摘要 | Qwen3.5-Plus | 1M token 上下文 |
| 推理 / 数学 / 逻辑 | DeepSeek-R1 或 Nex-N2-Pro | 满血 671B 或 397B MoE |
| 视觉 / 图像理解 | GLM-4V 或 Qwen-VL-Max | 原生中文视觉 |
| 批量 Embeddings | BAAI/bge-m3 | ¥0.4/百万，SOTA 中文 embeddings |
| 语音助手 | CosyVoice + Paraformer | STT + TTS 一站式 |

## SiliconFlow vs FreeModel vs OpenRouter 对比

| 厂商 | 最适合 | 国内访问 | 入门价 | 模型数 | OpenAI 兼容 |
|----------|----------|----------|---------|--------|-------------|
| **SiliconFlow** | 国内开源模型（Qwen/DeepSeek/GLM） | ✅ 直连 | ¥0.4/百万 | 100+ | ✅ |
| **FreeModel** | 多厂商聚合，内置内容审核路由 | ✅ 直连 | 视模型而定 | 50+ | ✅ |
| **OpenRouter** | 美欧团队一站式调用所有模型 | ❌ 需代理 | $0.50/百万 | 300+ | ✅ |
| **DeepSeek 官方** | 厂商直签 DeepSeek 价格 | ✅ 直连 | ¥1/百万 | 15+ | ✅ |
| **Together AI** | 美欧生产服务 200+ 开源 | ❌ 需代理 | $0.18/百万 | 200+ | ✅ |

对于需要 Qwen/DeepSeek/GLM 低延迟的国内团队，SiliconFlow 是默认选择。对于同时需要 GPT/Claude 并希望合并计费的团队，OpenRouter 是答案（需承受代理开销）。FreeModel 介于两者之间——同样是国内直连聚合，和 SiliconFlow 互补，适合作为 SiliconFlow 还没上线新模型时的内容审核和多模型聚合备用。

## FAQ

**Q：SiliconFlow 的 API 真的兼容 OpenAI 吗？包括 Function Calling？**
A：chat-completions 端点完全兼容——请求和响应格式与 OpenAI 一致。Function Calling 可用，但 tool-use 保证弱一些：长上下文场景下模型可能输出格式异常的 tool 调用。高风险工具调用建议加 schema parser 校验。

**Q：SiliconFlow 和自建推理集群比起来价格如何？**
A：日调用量在 5M token 以下时，SiliconFlow 比一台 A100 80GB（国内零售价约 ¥7K/月）便宜。日调用量超过 50M token 时，H800/H100 专用推理才有成本竞争力。

**Q：能在海外用 SiliconFlow 吗？**
A：能用，但要承受 300-500ms 额外延迟，且可能需要国内代理保持稳定访问。大部分海外团队只在必须调用 Qwen3.5 或 Nex-N2-Pro 时才用。

**Q：SiliconFlow 的免费额度真的能用吗？**
A：当前注册活动给 ¥1-200 额度（视活动而定）。¥100 足够在 Qwen2.5-7B 上跑约 50M token，做原型够用，做生产不够。

**Q：Nex-N2-Pro 是什么？为什么值得关注？**
A：Nex-N2-Pro 是基于 Qwen3.5 的 397B MoE 推理模型，2026-06-08 由 SiliconFlow 首发。目标是在代码和数学 benchmark 上达到 GPT-5.5 级别，但输入 token 价格只有 GPT-5.5 的 1/3。推理密集型负载值得评估。

**Q：国内聚合场景下，SiliconFlow 和 FreeModel 怎么选？**
A：两者都是国内直连且 OpenAI 兼容，但 SiliconFlow 模型覆盖更深（Qwen3.5/DeepSeek/GLM 独家），FreeModel 主打多厂商聚合 + 内置内容审核路由。常见做法是 SiliconFlow 做主、FreeModel 做内容审核和多厂商聚合备份——FreeModel 可以在 [freemodel.dev/invite/FRE-7a3b6220](https://freemodel.dev/invite/FRE-7a3b6220) 注册，一个集成覆盖国内直连 + 海外模型。

**Q：SiliconFlow 会用 API 请求数据训练新模型吗？**
A：根据公开隐私政策，请求数据保留 30 天用于风控后删除。除非用户明确同意，不会被用于训练新模型。

## 结论

对于在国内生产环境部署 Qwen/DeepSeek/GLM 的开发者，SiliconFlow 是最直接的路径。OpenAI 兼容 API 抹平了集成摩擦，¥0.4/百万 token 的入门价难以超越，模型目录足够覆盖大部分场景。缺点——没有 GPT/Claude 托管、tool-use 保证弱、400B+ 模型吞吐较低——是真实的，但对于目标场景（中文聊天机器人、中文文档 RAG、批量 Embeddings）并不是阻塞。

2026 年选择厂商的决策树：

- 需要 Qwen3.5/DeepSeek-R1/GLM-4 国内低延迟 → **SiliconFlow**
- 同时需要 GPT-5/Claude 4.8/Gemini 2.5、合并计费 → **OpenRouter**
- 需要国内直连 + 内置内容审核路由 + 多厂商备份 → [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220)
- 需要 Llama 3.3 70B 跑 2000+ tok/s、不需要中文 → **Cerebras 或 Groq**

如果你的团队已经在用 SiliconFlow，并希望备份一个能提供内容审核路由 + 国内直连 + 多厂商聚合的供应商，[FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) 是天然搭档——同样国内直连、OpenAI 兼容，并且内置多厂商内容审核路由，一个集成同时覆盖国内直连和海外模型访问。

---

## 对比表（结尾）

| 厂商 | 价格模型 | 最适合 | 国内访问 |
|----------|----------|----------|----------|
| **SiliconFlow** | 输入 ¥0.4-2/百万，输出 ¥0.4-2/百万 | 国内开源模型访问（Qwen/DeepSeek/GLM） | ✅ 直连 |
| **FreeModel** | 视模型而定 | 多厂商聚合 + 内置内容审核路由 | ✅ 直连 |
| **OpenRouter** | $0.50/百万（视模型） | 美欧团队一站式调用所有模型 | ❌ 需代理 |
| **DeepSeek 官方** | 输入 ¥1/百万，输出 ¥2/百万 | DeepSeek 官方直签价 | ✅ 直连 |
| **Together AI** | $0.18-0.88/百万 | 200+ 开源模型，美欧生产服务 | ❌ 需代理 |
| **SambaNova** | $0.30-$3.00/百万 | 405B / R1 满血参数，dataflow 速度 | ❌ 需代理 |