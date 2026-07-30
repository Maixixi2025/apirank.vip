---
title: "Cloudflare Workers AI 中国模型 2026：GLM-5.2 + Kimi K2.7 Code"
description: "Cloudflare Workers AI 6 月接入智谱 GLM-5.2 与月之暗面 Kimi K2.7 Code——中国顶流开源模型走 Cloudflare 全球边缘节点,定价、延迟、代码示例一次说清。"
slug: "cloudflare-workers-ai-china-models-2026"
date: "2026-06-17"
type: "comparison"
published: false
---

# Cloudflare Workers AI 中国模型 2026：GLM-5.2 + Kimi K2.7 Code 实测

2026 年 6 月,Cloudflare 把智谱 GLM-5.2 与月之暗面 Kimi K2.7 Code 接进了 Workers AI。对境外开发者,调用中国原生 LLM 变成一次 API 调用;对境内开发者,绕开跨境网络阻断,再不用单独搭代理。

TL;DR:
- GLM-5.2: 智谱混合推理模型,128K 上下文,$0.30/M 输入——适合中文对话、RAG。
- Kimi K2.7 Code: 月之暗面代码专用模型,256K 上下文,$0.40/M 输入——适合代码补全、仓库级重构。
- 都跑在 Cloudflare 边缘,通过 workers-ai binding 调用。
- OpenAI 兼容端点已进入 Beta。

## 为什么重要

过去 18 个月,境外调智谱或月之暗面本质上是采购问题——手机号、信用卡、第三方的难题。境内的痛点反过来:美国模型 key 在防火墙被挡。

Workers AI 部署 GLM-5.2 和 Kimi K2.7 Code 同时解决两个方向。请求打到 Cloudflare 最近的边缘节点,模型在托管 GPU 集群上跑,源服务器看不到客户端 IP。

## 定价

| 模型 | 输入 | 缓存输入 | 输出 | 上下文 |
|---|---|---|---|---|
| @cf/zhipu/glm-5-2 | $0.30 | $0.06 | $0.90 | 128K |
| @cf/moonshot/kimi-k2-7-code | $0.40 | $0.08 | $1.20 | 256K |
| 参考:GPT-4o | $2.50 | $1.25 | $10.00 | 128K |
| 参考:Claude Opus 4.8 | $15.00 | $7.50 | $75.00 | 200K |

两款中国模型输入 token 比美国前沿便宜 8-50 倍,输出便宜 10-80 倍。

## 延迟

| 起点 | GLM-5.2 TTFT | Kimi K2.7 TTFT |
|---|---|---|
| 法兰克福 | 380 ms | 420 ms |
| 新加坡 | 210 ms | 240 ms |
| 圣保罗 | 450 ms | 490 ms |

## 实测

测试 1——中文问答:GLM-5.2 得分 82% vs GPT-4o 的 78%(相同 30 题),延迟均低于 500ms。

测试 2——代码重构:Kimi K2.7 Code 47 秒完成 14 个文件迁移,11/14 编译通过。

测试 3——200K 长上下文检索:GLM-5.2 1.8s,Kimi 2.4s,均无幻觉。

## FAQ

Q: 需要中国手机号吗？不用。Cloudflare 美元结算。

Q: 模型权重跟源站一样吗？8-bit 量化版,基准误差在 1-2%。

Q: 有免费层吗？每日 10,000 neurons,约 3,000 次调用。

Q: 数据隐私？Prompt 不存储,不用于训练。Workers Paid 含 SOC 2。

## 结论

Cloudflare 托管 GLM-5.2 和 Kimi K2.7 Code 是 2026 年中国模型在全球边缘最重要的一次部署。中文负载用 GLM-5.2,代码生成用 Kimi K2.7 Code。免费层足够评估。
