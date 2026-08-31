---
title: "Cloudflare Workers AI 评测 2026：86 模型边缘 GPU 目录 | APIRank"
description: "Cloudflare Workers AI 评测 2026：86 个模型跑在 Cloudflare 边缘 GPU 上，每日 10K Neurons 免费，$0.011/1K Neurons，GLM-5.3 百万 token $1.40/$4.40，DeepSeek V4 Pro 1M 上下文，OpenAI 兼容 API。"
slug: "cloudflare-workers-ai-api-review-2026"
provider: "cloudflare-workers-ai"
published: false
date: "2026-08-31"
type: "review"
---

# Cloudflare Workers AI 评测 2026：86 模型边缘 GPU 目录

## Cloudflare Workers AI 是什么？

Cloudflare Workers AI 是目前唯一在同一边缘网络上同时承载应用代码与模型推理的主流推理平台。截至 2026 年 8 月，目录已覆盖 **86 个模型**，涵盖文本、Embedding、图像与音频——其中包括前沿模型 Z.ai GLM-5.3（百万 token $1.40/$4.40，1M 上下文，2026-08-28 上线）、DeepSeek V4 Pro（$1.32/$3.96，1M 上下文，2026-08-13 上线）、Moonshot Kimi K2.7-code（$0.95/$4.00）与 OpenAI GPT-OSS 120B（$0.35/$0.75）。计费采用 Cloudflare 自有的 **Neurons** 单位，**$0.011/1000 Neurons**，Workers Free 计划下 **每日 10,000 Neurons 免费**，无需信用卡。

## 86 模型目录（2026 年 8 月）

目录覆盖四类模型。**文本生成**是深度最大的部分，前沿模型（GLM-5.3、DeepSeek V4 Pro、Kimi K2.7-code、GPT-OSS 120B）与小型开源模型（Llama 3.2 1B 百万 token $0.027/$0.201、Llama 3.2 3B $0.051/$0.335）共存。

| 模型 | 输入 ($/M) | 缓存 ($/M) | 输出 ($/M) | 层级 |
|---|---|---|---|---|
| @cf/zai-org/glm-5.3 | $1.400 | $0.260 | $4.400 | 前沿（仅付费） |
| @cf/zai-org/glm-5.3-flash | $0.150 | $0.030 | $0.500 | 前沿（仅付费） |
| @cf/deepseek-ai/deepseek-v4-pro-0813 | $1.320 | $0.044 | $3.960 | 前沿（仅付费） |
| @cf/deepseek-ai/deepseek-v4-flash-0731 | $0.440 | $0.014 | $1.320 | 前沿（仅付费） |
| @cf/moonshotai/kimi-k2.7-code | $0.950 | $0.190 | $4.000 | 前沿（仅付费） |
| @cf/openai/gpt-oss-120b | $0.350 | — | $0.750 | 开放权重 |
| @cf/meta/llama-3.3-70b-instruct-fp8-fast | $0.293 | — | $2.253 | 开放权重 |
| @cf/meta/llama-4-scout-17b-16e-instruct | $0.270 | — | $0.850 | 开放权重 |
| @cf/meta/llama-3.2-1b-instruct | $0.027 | — | $0.201 | 免费层可用 |

## Neurons 计费机制

Workers AI 采用双轴定价。基础费率 **$0.011/1000 Neurons**，在每日免费额度耗尽后开始计费。每个模型同时发布 token 等效价格，便于与其他推理 API 比较。**免费计划**每日提供 10,000 Neurons，UTC 00:00 重置，无需信用卡。但**前沿模型不包含在免费计划**——要调用 GLM-5.3、DeepSeek V4 Pro 或 Kimi K2.7-code，需要 Workers Paid（$5/月基础订阅）或预付 AI Gateway 信用。

## 从 Worker 调用 Workers AI

推荐路径是 Workers binding。在 `wrangler.toml` 中添加 `[[ai.bindings]] name = "AI"`，然后在 Worker 中调用 `env.AI.run("@cf/zai-org/glm-5.3", { messages: [...] })`。无需管理 API 密钥，无需安装 SDK，binding 自动将推理调用计入 Cloudflare 账户的 Workers 账单。

## 结论

Cloudflare Workers AI 是少数几个「越全球化越有优势」的推理平台：边缘路由让非美国用户比美国用户响应更快，免费层足够用来搭建真实产品原型，前沿模型覆盖在价格上对任何独立提供商都具备竞争力。它不是大陆优先部署的正确选择，精选目录（86 模型 vs OpenRouter 400+）也意味着不能覆盖每个长尾模型。但对于与 Cloudflare Workers 形态相匹配的工作负载——短 prompt、边缘服务、混合模型规模、低运维成本——Workers AI 是 2026 年 8 月市场上最自洽的选项。

**适合：**已在 Cloudflare Workers / Pages 上运行的团队；面向全球、非美国流量占比高的 SaaS；想要前沿模型但不想谈多区域 GPU 合同的初创公司；Agent、RAG、边缘推理负载。
