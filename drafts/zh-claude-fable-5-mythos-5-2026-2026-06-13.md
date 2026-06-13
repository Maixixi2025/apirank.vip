---
title: "Claude Fable 5 / Mythos 5 测评：Anthropic 前沿模型"
description: "Anthropic Claude Fable 5 和 Mythos 5 全面测评：$10/$50 每百万 token、1M 上下文、智能指数第一。对比 GPT-5.x 和 Gemini 3，含 API 接入指南。"
slug: "claude-fable-5-mythos-5-2026"
provider: "anthropic"
published: false
date: "2026-06-13"
type: "comparison"
---

# Claude Fable 5 / Mythos 5 深度测评：Anthropic 2026 前沿模型对决 GPT-5.x 和 Gemini 3

**2026 年 6 月 13 日 — 含美国出口管制暂停更新**

> **核心结论：** 2026 年 6 月 9 日，Anthropic 发布了 Claude Fable 5（$10/M 输入、$50/M 输出）和 Claude Mythos 5（去除安全分类器的同款）。它们在 Artificial Analysis 智能指数上以 64.9 分排名第一——领先 GPT-5.5 约 5 分——拥有 100 万 token 上下文和 128K 最大输出。但 6 月 12 日，美国政府发布出口管制指令，暂停外国人访问这两个模型，成为前沿 AI API 市场迄今最重大的地缘政治事件。

## Fable 5 和 Mythos 5 是什么？

Claude Fable 5 和 Mythos 5 是 Anthropic 迄今为止最强大的模型——价格却只有前代（Claude Mythos Preview）的大约一半。两者底层完全相同，关键区别在于：Fable 5 包含针对网络、生物/化学和蒸馏风险的安全分类器，Mythos 5 则去除这些分类器以获得最大无限制能力。

**模型 ID：**
- `claude-fable-5` — 完整安全分类器（推荐大多数场景）
- `claude-mythos-5` — 无安全分类器（适用于受信任的研究环境）

**关键规格：**
- 上下文窗口：100 万 token（与 GPT-5.x 持平）
- 最大输出：128K token
- 输入模态：文本 + 图像（视觉能力）
- 自适应思考：始终开启（无扩展思考开关）
- 美国独有推理：价格 1.1x

## 定价：前代一半价格

核心数字：Fable 5 的价格正好是 Claude Mythos Preview 的一半。$10/M 输入和 $50/M 输出为 Anthropic 的模型线建立了新的性价比前沿。

| 模型 | 输入（每百万 token） | 输出（每百万 token） | 缓存读取 | 缓存写入（1小时） |
|-------|---------------------|---------------------|---------|----------------|
| **Claude Fable 5** | **$10.00** | **$50.00** | $1.00 | $20.00 |
| Claude Mythos Preview | $20.00 | $100.00 | $2.00 | $40.00 |
| Claude Opus 4.8 | $5.00 | $25.00 | $0.50 | $10.00 |
| GPT-5.5 | $15.00 | $60.00 | $7.50 | — |

## 基准测试：多项第一

Fable 5 在 Artificial Analysis 智能指数上以 64.9 分位居第一——领先 GPT-5.5 约 5 分，显著超过 Gemini 3.1 Pro Preview。

| 基准测试 | Fable 5 | GPT-5.5 | Gemini 3.1 PP | Opus 4.8 |
|---------|---------|---------|---------------|----------|
| AA 智能指数 | **64.9** | ~59.9 | ~57 | ~52 |
| 人类最后的考试 | **53%** | ~45% | ~42% | ~40% |
| FrontierCode（编程） | **最高** | #2 | #3 | #5 |
| AA-Omniscience | **40** | ~35 | 33 | ~28 |
| CursorBench | **SOTA** | — | — | — |

## 出口管制事件（2026 年 6 月 12 日）

6 月 12 日晚间，美国政府根据受控模型框架发布出口管制指令，暂停外国人访问 Claude Fable 5 和 Mythos 5。Anthropic 正积极抗辩，其依据是一种狭窄的越狱技术——根据 Anthropic 的说法，该技术产生的结果"广泛可从其他模型（包括 OpenAI 的 GPT-5.5）获得"。

**截至 6 月 13 日的状态：**
- 美国账户 API 访问：正常 ✅
- 外国人 API 访问：暂停 ❌
- AWS Bedrock / Vertex AI 访问：仅限美国
- Anthropic 正为国际客户寻找合规解决方案

**对开发者的影响：**
1. **美国团队**：正常运行，但建议配置 Opus 4.8 作为备用
2. **国际团队**：暂时使用 Opus 4.8，或探索 GPT-5.5 / Gemini 3 等替代方案
3. **多区域部署**：添加按区域检测可用性的模型路由

## 场景对比

| 场景 | 胜者 | 原因 |
|------|------|------|
| 复杂编程/Agent | **Fable 5** | FrontierCode、CursorBench 双料第一 |
| 长文档分析 | **持平** | 均支持 1M 上下文 |
| 写作与内容 | **Fable 5** | 长篇写作最擅长 |
| 实时对话/低延迟 | **Gemini 3** | Fable 5 约 64 tok/s，Gemini 3 更快 |
| 预算敏感 | **Fable 5** | $10/$50 vs GPT-5.5 的 $15/$60 |
| 多模态分析 | **GPT-5.5** | 原生支持图像、音频、视频 |
| 国内直连 | **需代理** | 三者均无法从中国直接访问 |

## 代码示例：调用 Claude Fable 5

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

response = client.messages.create(
    model="claude-fable-5",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "实现一个带 TTL 的 LRU 缓存"}
    ]
)

print(response.content[0].text)
```

## 常见问题

**Q: Fable 5 和 Mythos 5 有什么区别？**
A: 两者是同一底层模型。Fable 5 包含针对网络、生物/化学和蒸馏风险的安全分类器。Mythos 5 去除了这些分类器。

**Q: 从中国能访问 Fable 5 吗？**
A: 不能。Anthropic 要求美国账户，目前还有出口管制暂停令。所有 Anthropic 模型从中国访问都需要代理。需要国内直连方案的团队，可考虑 FreeModel 等提供 OpenAI 兼容路由的聚合平台。

**Q: Fable 5 比 GPT-5.5 便宜吗？**
A: 是的。Fable 5 价格为 $10/$50 每百万 token，GPT-5.5 为 $15/$60——输入便宜 33%，输出便宜 17%。

## 结论

Claude Fable 5 和 Mythos 5 是目前公开可用的最强 AI 模型——在智能指数、编程基准到 CursorBench 等多项评测中领先。$10/$50 的价格对于 Anthropic 的前沿层级来说相当激进，同时低于 GPT-5.5。

**出口管制暂停是最大变数。** 对美国团队来说，Fable 5 是所有非实时、质量敏感型工作的明确推荐。对国际团队来说，取决于 Anthropic 解决合规问题的速度。

**适合用 Fable 5 的场景：**
- 编程：是，特别是复杂 Agent 任务
- 写作：长文和结构化内容的最佳选择
- 研究：深度分析的最强模型
- 企业：咨询法务团队出口合规问题

**建议等待的场景：**
- 没有美国实体的国际团队
- 实时应用（Gemini 3 更快）
- 需要音频/视频的多模态应用（GPT-5.5 模态支持更广）

需要多供应商灵活性（特别是国内直连）的团队，可考虑 FreeModel 等提供 OpenAI 兼容路由的聚合平台，实现跨模型无缝切换。
