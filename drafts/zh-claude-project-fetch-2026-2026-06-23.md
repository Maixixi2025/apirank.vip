---
title: "Claude Project Fetch 2026：Opus 4.7 自主任务 20 倍提速"
description: "Anthropic Project Fetch Phase Two：Claude Opus 4.7 自主编写代码、连接硬件传感器，完成任务比人类快19-38倍。Claude Code API 实战指南。"
slug: "claude-project-fetch-2026"
provider: "anthropic"
published: false
date: "2026-06-23"
type: "review"
---

# Claude Opus 4.7 Project Fetch：自主 API 任务提速 20 倍

## TL;DR

Anthropic 于 2026 年 6 月 18 日发布 Project Fetch Phase Two 实验结果：Claude Opus 4.7 通过 Claude Code **全自主完成**机器人软件开发任务，速度比最快的人类团队快 19 倍，比无 AI 辅助团队快 38 倍——4 个任务仅用 9 分 35 秒（人类团队 181 分钟）。Claude 自主连接摄像头和激光雷达传感器、编写控制代码、迭代调试。对 API 开发者来说，Claude Code + Opus 4.7 的自主任务执行能力已可投入生产环境。

## Project Fetch Phase Two 是什么

2026 年 6 月 18 日，Anthropic Frontier Red Team 发表 Project Fetch Phase Two——对 2025 年 8 月实验的升级版。原实验中人类团队使用 Claude 辅助操作四足机器人（"机器狗"），而这一次 **Claude Opus 4.7 通过 Claude Code 完全自主运行**。

人类研究员的角色仅限于：插上电源、输入初始提示、批准命令、批准任务之间的切换。代码编写、硬件连接、传感器集成、迭代调试全部由 Claude 完成。

核心结果：**4 个可比较任务，Claude Opus 4.7 用时 9 分 35 秒**，而最快的人类团队（使用 Claude 辅助）用时 181 分钟——提速 **18.9 倍**；较无 AI 辅助的人类团队（361 分钟）提速 **37.7 倍**。

## 基准测试数据

| 指标 | Claude Opus 4.7 | 人类+Claude 团队 | 纯人类团队 |
|------|:---------------:|:----------------:|:---------:|
| 4 个可比任务 | **9 分 35 秒** | 181 分钟 | 361 分钟 |
| 比纯人类团队快 | **37.7x** | — | 1x |
| 比人类+Claude 团队快 | **18.9x** | 1x | — |
| 全部 5 个任务（3次平均） | **12 分 7 秒** | 264 分钟 | — |
| 编写的代码行数 | **1,045 行** | 10,309 行 | 1,136 行 |

Claude "在比人类团队几乎少写 10 倍代码的情况下，成功率与两个人类团队相当或更高"——不仅更快，而且更高效。

### 自主完成的任务

1. **连接摄像头** — 检测并集成 USB 摄像头
2. **连接激光雷达** — 通过 I2C 接口连接 LIDAR-Lite v4
3. **编写手动控制程序** — 键盘控制机器狗运动
4. **开发路径监控** — 通过激光雷达实时跟踪障碍物
5. **编写沙滩球检测程序** — 基于 OpenCV 的红色物体检测（物理上的"捡球"动作仍需人类）

## 对 API 开发者的意义

Claude Code（Anthropic 的终端代理 CLI）是实现自主任务执行的接口：

1. **安装 Claude Code**：`npm install -g @anthropic-ai/claude-code`
2. **启动自主模式**：使用 Claude Opus 4.7 最大努力自适应思考
3. **用自然语言描述任务** — Claude 负责编写、测试、迭代
4. **批准关键切换** — 人在关键决策节点保持参与

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

# Claude 可自主处理多步骤任务
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    messages=[
        {"role": "user", "content": "写一个 Python 程序，连接 USB 摄像头，以 30fps 采集画面，用 OpenCV 检测红色物体，并支持键盘控制。"}
    ]
)

print(response.content[0].text)
```

## 定价参考

Opus 4.7 与 Opus 4.6 和 4.8 定价相同：

| 模型 | 输入（每百万 token） | 输出（每百万 token） | 上下文 |
|------|:-------------------:|:-------------------:|:------:|
| Claude Opus 4.7 | $5.00 | $25.00 | 1M tokens |
| Claude Opus 4.8（最新） | $5.00 | $25.00 | 1M tokens |
| GPT-5.5 | $15.00 | $60.00 | 256K tokens |

**注意：** Opus 4.7 引入了新的 tokenizer，相同文本产生的 token 数量比 4.7 之前的模型多约 30%。即使单价不变，实际任务成本可能增加约 30%。

## 局限

- **物理精度**：精细运动控制仍需人类（如让机器狗实际推动物体）
- **Tokenizer 变化**：30% 的 token 增加需要重新评估成本预算
- **Opus 4.7 现为上一代**：Opus 4.8（5月28日）和 Fable 5（6月9日）已发布
- **出口管制**：Anthropic 模型面临美国出口管制限制，国际团队受影响

## 常见问题

**Q: Project Fetch Phase Two 的能力可以通过常规 API 使用吗？**
A: 可以。自主任务能力通过 Claude Code CLI（终端代理）实现，使用 Claude Opus 4.7 或更新的模型。API 接口不变，自主性来自 Claude Code 的代理架构。

**Q: Opus 4.7、4.8 和 Fable 5 有什么区别？**
A: Opus 4.7（4月16日）引入了新 tokenizer 和自主能力。Opus 4.8（5月28日）是微调更新。Fable 5（6月9日）是当前前沿模型，$10/$50 每百万 token。Project Fetch 使用 Opus 4.7，但能力向前兼容。

**Q: 国内能使用吗？**
A: Anthropic 需美国账户且有出口管制。国内团队可使用 FreeModel 等提供多厂商路由的聚合平台。

**Q: 一次自主任务大概需要多少费用？**
A: 以 $5/$25 每百万 token 计，一次生成约 10K token 的多步骤任务成本约 $0.25-0.50。即使考虑 30% tokenizer 开销，仍比雇 3-6 名工程师便宜几个数量级。

## 总结

Project Fetch Phase Two 是自主 API 代理能力的里程碑。Claude Opus 4.7 以比人类快 20 倍的速度完成含硬件交互的软件工程任务，这项能力已可复现并投入生产环境。

### 选择建议

- **需要包含硬件交互的自主编码？** Claude Opus 4.7+ 通过 Claude Code
- **纯软件且预算敏感？** Opus 4.7 的 $5/$25 定价性价比极高
- **需要多厂商路由？** 考虑 FreeModel 等聚合平台
- **国内直连？** 使用 OpenAI 兼容的聚合服务
- **追求极致编程质量？** Fable 5 前沿最强，但 Opus 4.7 以一半价格提供接近的能力

---

*更新日期：2026-06-23。Anthropic Frontier Red Team 于 2026 年 6 月 18 日发布。*
