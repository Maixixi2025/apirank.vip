---
title: "Kimi K3 API 评测 2026：1M 上下文与官方价格"
description: "Kimi K3 API 评测：官方价格为缓存输入 ¥2/M、未命中输入 ¥20/M、输出 ¥100/M；含 1M 上下文、视觉、工具调用、K2 选型与限制。"
pubDate: "2026-07-31"
provider: kimi
category: review
featured: true
---

# Kimi K3 API 评测 2026：1M 上下文不是免费午餐

Kimi K3 是月之暗面的新旗舰 API，瞄准的是一个非常明确的场景：需要超大上下文、原生视觉、工具调用和中文能力的长程编程 Agent 与知识工作系统。官方模型文档列出 2.8 万亿参数、1,048,576 token（1M）上下文窗口、图片与视频输入、自动上下文缓存、JSON Mode、结构化输出和工具选择控制。

但 1M 上下文并不等于低成本。Kimi K3 对缓存命中输入、缓存未命中输入和输出分别计费；当前官方价格是缓存命中输入 ¥2/M、未命中输入 ¥20/M、输出 ¥100/M。新用户赠送的 ¥15 代金券也不能用于体验 K3，所以从第一次生产测试开始就应当做预算规划。

本文以当前可用的 Kimi API 为准，覆盖官方价格、模型选型、OpenAI 兼容代码、多模态输入、Agent 控制、限制，以及什么时候 Kimi K2.7 Code 或 K2.6 才是更合理的选择。

## Kimi K3 核心信息

| 项目 | 已核实的 Kimi K3 信息 |
|---|---|
| API 模型 ID | `kimi-k3` |
| 上下文窗口 | 1,048,576 tokens（1M） |
| 输入价格 | 缓存命中 ¥2/M；未命中 ¥20/M |
| 输出价格 | ¥100/M tokens |
| 思考模式 | 始终开启；`reasoning_effort` 当前仅支持 `max` |
| 模态 | 文本、图片、视频输入 |
| 结构化输出 | JSON Mode 与 JSON Schema |
| 工具能力 | Tool Calls、`tool_choice`、动态加载工具 |
| API 形式 | OpenAI 兼容 Chat Completions |
| 适用区域 | Kimi API 开放平台；面向中国大陆直连场景 |

模型 ID 很简洁，但不要据此假设所有 OpenAI 参数都能直接搬过来。K3 有自己的参数约束，官方文档明确说明了若干采样参数是固定值。

## Kimi K3 官方价格：缓存命中会改变成本

Kimi 官方价格表把输入拆成缓存命中和缓存未命中两类。对于长系统提示词、代码仓库说明、政策文档和重复的 Agent 轮次，这个差异非常关键。

| 模型 | 缓存命中输入 / 1M | 未命中输入 / 1M | 输出 / 1M | 上下文 |
|---|---:|---:|---:|---:|
| Kimi K3 | ¥2.00 | ¥20.00 | ¥100.00 | 1,048,576 |
| Kimi K2.7 Code | ¥1.30 | ¥6.50 | ¥27.00 | 262,144 |
| Kimi K2.7 Code HighSpeed | ¥2.60 | ¥13.00 | ¥54.00 | 262,144 |
| Kimi K2.6 | ¥1.10 | ¥6.50 | ¥27.00 | 262,144 |

举个 100,000 token 输入、10,000 token 输出的例子：如果输入未命中缓存，K3 的 token 费用约为 ¥2 + ¥1 = ¥3；同一个稳定前缀命中缓存后，输入部分降到约 ¥0.20，总计约 ¥1.20。这里假设展示的 token 数就是计费 token，且不含其他产品费用。

这并不意味着"K3 很便宜"。输出价格是 ¥100/M，缓存未命中输入也比命中贵 10 倍。更准确的结论是：如果保持系统提示词、工具定义和长前缀稳定，K3 的长上下文工作流可以有可预测的成本；每轮都重建 Prompt、缓存失效并产生长推理输出时，账单会迅速上升。

月之暗面还在运行限时充值返券活动：2026 年 7 月 16 日至 8 月 12 日。官方活动说明同一组织在活动期内仅有一笔符合条件的首次充值交易，¥99–¥499 返 10%，¥500–¥1,999 返 20%，¥2,000–¥4,999 返 25%，¥5,000 及以上返 30%。这是平台活动，不是永久 API 降价，预算时应以活动条款和实际到账为准。

## Kimi K3 到底新增了什么

K3 不只是给 K2 换了一个更大的 context 字段。月之暗面称其为 2.8 万亿参数模型，采用 Kimi Delta Attention 和 Attention Residuals，并使用稀疏 Mixture-of-Experts 架构。对 API 开发者而言，真正重要的是这些能力如何影响工程流程：

- **1M 上下文与自动缓存：** 普通请求可自动尝试前缀缓存，不需要手动管理 cache ID 或 TTL。
- **原生视觉：** K3 支持文本、图片和视频。图片应使用 base64 或 Kimi 文件引用，而不是公网图片 URL。
- **始终开启思考：** K3 始终进行推理，当前 `reasoning_effort` 仅有 `max` 档位。不要把 K2.x 的 thinking 参数直接套过来。
- **工具控制：** 支持工具调用、`tool_choice` 和动态加载工具。工具很多但每轮只需一小部分时，动态加载能减少 Prompt 膨胀。
- **结构化输出：** JSON Mode 和 JSON Schema 适合抽取任务与工作流状态。
- **长程编程：** 官方定位包括大型代码库、终端协调、视觉反馈、前端和 CAD 等任务。

这些是平台能力，不是"上下文越大所有任务越好"的保证。把整个工作区在每一轮都发送给模型，可能增加延迟、调试复杂度和缓存失效率。

## curl 首次调用

Kimi 提供 OpenAI 兼容接口。把 API Key 放在环境变量中，用最小请求先验证链路：

```bash
export KIMI_API_KEY="YOUR_KIMI_API_KEY"
curl https://api.moonshot.cn/v1/chat/completions \
  --header "Authorization: Bearer ${KIMI_API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "kimi-k3",
    "messages": [{"role": "user", "content": "请用三句话解释 1M token 上下文的成本权衡。"}]
  }'
```

接口与 Chat Completions 足够兼容，但添加思考、视觉、工具或结构化输出字段时，仍应以 Kimi 模型文档为准。不要把真实 Key 写进仓库、日志或公开 Issue。

## Python + OpenAI SDK

官方快速开始使用 OpenAI Python SDK 配合 Kimi 的 base URL，这使迁移测试很直接：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["MOONSHOT_API_KEY"],
    base_url="https://api.moonshot.cn/v1",
)

response = client.chat.completions.create(
    model="kimi-k3",
    messages=[
        {"role": "system", "content": "你是严谨的软件工程助手。"},
        {"role": "user", "content": "列出把整个代码仓库放进每轮 Agent 请求的三个风险。"},
    ],
)

print(response.choices[0].message.content)
print(response.usage)
```

记录 `response.usage` 到成本看板。对 K3 来说，使用量可观测不是可选项：缓存命中与未命中的差距非常大，输出 token 的成本又是未命中输入的 5 倍。

## 视觉、JSON 与 Agent 工作流

视觉请求要求 `message.content` 是结构化的 part 数组，不要把它序列化成一个字符串。一个最简的图片请求大致是：

```python
message = {
    "role": "user",
    "content": [
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}},
        {"type": "text", "text": "描述页面布局，并列出可见的 UI 缺陷。"},
    ],
}
```

K3 同时支持 JSON Mode 与 JSON Schema 响应格式。适合结构化抽取，但 schema 应当尽量小，并请在调用方对返回对象做校验。在 Agent 系统中，把结构化输出与 `tool_choice` 一起使用，避免模型在"回答问题"和"改写外部系统"两种意图之间悄悄切换。

动态加载工具对长上下文 Agent 特别有用：每轮只暴露当前阶段真正需要的那几个工具定义，其余工具在后续步骤再加进来。这既能减少 Prompt 体积，也有助于保持缓存前缀稳定。

## Kimi K3 vs K2.7 Code vs K2.6

K3 在上下文规模和多模态长程任务主导时是默认选择；它并不适合所有编码任务。

**选 Kimi K3**：需要仓库级上下文、长文档、视觉反馈、长期工具工作流，或希望一个模型同时处理中英文知识工作。需要为高输出价格做预算，并测试缓存表现。

**选 Kimi K2.7 Code**：主要做软件工程任务，256K 上下文足够。未命中输入 ¥6.50/M、输出 ¥27/M，远低于 K3 的上限。HighSpeed 变体官方记录约 180 tokens/秒，短上下文可达 260 tokens/秒，但价格是普通 K2.7 Code 的两倍。

**选 Kimi K2.6**：通用多模态模型，256K 上下文，思考与非思考模式可选，输出价格与普通 K2.7 Code 相同（¥27/M）。在不需要 1M 上下文的多模态理解、Agent 任务和日常对话场景下，是更经济的选择。

如果是从 OpenAI 迁移过来的应用，建议用同一套评测对三个模型都跑一遍，对比工具调用有效性、JSON 合规率、缓存命中率、首 token 耗时、总输出 token、人工返工次数。"OpenAI 兼容"描述的是协议，而不是行为。

## 限制与生产风险

下面这些约束应该写到你的上线清单里：

1. **¥15 新用户代金券不能用于 K3。** 官方 K3 快速开始明确说明代金券不能用于体验 K3，测试阶段就要做充值。
2. **始终开启思考。** 当前 K3 的 `reasoning_effort` 只支持 `max`，不是完整的强度档位。简单任务上可能拉高输出量与延迟。
3. **公网图片 URL 不是安全路径。** 视觉输入请使用 base64 或 Kimi 文件引用，并把 `content` 保持成数组结构。
4. **联网搜索处于升级中。** 当前的定价/模型文档提示联网搜索正在升级，不建议用于生产流程，等月之暗面更新文档后再用。
5. **权重尚未发布到 API 之外。** 月之暗面表示 K3 全量权重计划 2026 年 7 月 27 日放出。未来可能影响托管经济性，但不会改变今天的管理 API 账单。
6. **区域可达性影响 TCO。** Kimi API 开放平台主要面向中国大陆直连场景。其他地区团队应在采购前验证网络可达性、数据路由与支持范围。

如果你需要一个外部的多供应商控制平面来评估 Kimi 与其他端点，可以参考 FreeModel API 接入——这是用作评测和路由的一种选择，并不意味着可以忽略上游供应商的模型 ID、用量结算或区域条款。

## 最佳使用场景

Kimi K3 在四类具体工作负载上很能打：

- **仓库级编程 Agent：** 把架构笔记、代码、测试、工具结果保留在同一工作上下文中，并分阶段控制工具集合。
- **中文知识工作：** 在不激进切分文档的情况下，分析长篇政策、法律、产品或研究材料。
- **可视化软件工作流：** 在迭代式编码任务中，查看截图、UI 状态、示意图或视频片段。
- **结构化操作：** 用 JSON Schema 做抽取、用 Tool Calls 做受控动作，配合校验与审批闸门处理副作用。

它在短轮单次聊天、很小的 JSON 抽取、输出主导成本的场景里较弱。这些情况下，更小的 K2.6 或者别的低输出价端点会是更合理的工程选择。

## 结论：购买上下文，而不是 hype

Kimi K3 是一次严肃的 API 发布：1M 上下文、视觉、工具、结构化输出、自动缓存、OpenAI 兼容协议。这份官方能力清单让它对编程 Agent 与长文档工作流立刻具备相关性。

价格是真正的约束。¥20/M 未命中输入 + ¥100/M 输出，意味着 K3 不是一个廉价的通用聊天模型。当你能复用稳定前缀、保持输出节制时，它的成本曲线变得可预测；当每一轮都错过缓存并产生长推理输出时，账单会迅速上升。

我们的建议是：用一组贴近生产的评测同时跑 K3、K2.7 Code、K2.6。如果 K3 更长的上下文显著减少了切分 bug、工具重试和人工复核，并能覆盖它高出来的输出成本，那它就是你工作流里最合适的 Kimi 模型。否则 K2 系列在兼容性和多模态覆盖度上已经够用，并且 token 成本低得多。

## 常见问题

**Kimi K3 多少钱？** 按官方价格表，K3 是缓存命中输入 ¥2/M、未命中输入 ¥20/M、输出 ¥100/M。

**Kimi K3 真的支持 1M tokens 吗？** 是。官方模型指南与价格页都列出 1,048,576 token 的上下文窗口。但应用本身仍需要合理的检索与 Prompt 管理——最大窗口大，不代表每次请求都要塞满。

**能用 OpenAI Python SDK 调用 Kimi K3 吗？** 可以。把 `base_url` 设为 `https://api.moonshot.cn/v1`，填入 Kimi 的 API Key，使用 Kimi 官方文档列出的模型 ID。功能专属参数需各自核对。

**Kimi K3 支持图像与视频输入吗？** 支持。当前文档称 K3 支持文本、图片与视频输入；图片请用 base64 或 Kimi 文件引用发送，`content` 保持为 part 数组。

**¥15 新用户代金券能用在 K3 上吗？** 不能。月之暗面 K3 快速开始明确说明新用户代金券不能用于体验 K3，必须先充值。

**什么情况下该选 Kimi K2.7 Code？** 当 256K 上下文已经够用、且主要任务在编码时。官方价格显示未命中输入 ¥6.50/M、输出 ¥27/M，明显低于 K3。

**Kimi K3 的联网搜索能上生产吗？** 当前官方文档提示联网搜索正在升级，不建议用于生产流程。应等待月之暗面更新文档后再作为关键依赖。

## 来源

- 月之暗面，[Kimi K3 模型文档](https://platform.kimi.com/docs/guide/kimi-k3-quickstart)
- 月之暗面，[Kimi K3 价格](https://platform.kimi.com/docs/pricing/chat-k3)
- 月之暗面，[Kimi K2.7 Code 价格](https://platform.kimi.com/docs/pricing/chat-k27-code)
- 月之暗面，[Kimi K2.6 价格](https://platform.kimi.com/docs/pricing/chat-k26)
- 月之暗面，[Kimi K3 充值返券活动](https://platform.kimi.com/docs/pricing/promotion)
- 月之暗面，[Kimi K3 技术博客](https://www.kimi.com/blog/kimi-k3)
