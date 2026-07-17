---
title: "Kimi K3 API 评测 2026：1M 上下文与官方价格"
description: "Kimi K3 API 评测：官方价格为缓存输入 ¥2/M、未命中输入 ¥20/M、输出 ¥100/M；含 1M 上下文、视觉、工具调用、K2 选型与限制。"
pubDate: 2026-07-17
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

这并不意味着“K3 很便宜”。输出价格是 ¥100/M，缓存未命中输入也比命中贵 10 倍。更准确的结论是：如果保持系统提示词、工具定义和长前缀稳定，K3 的长上下文工作流可以有可预测的成本；每轮都重建 Prompt、缓存失效并产生长推理输出时，账单会迅速上升。

月之暗面还在运行限时充值返券活动：2026 年 7 月 16 日至 8 月 12 日。官方活动说明同一组织在活动期内仅有一笔符合条件的首次充值交易，¥99–¥499 返 10%，¥500–¥1,999 返 20%，¥2,000–¥4,999 返 25%，¥5,000 及以上返 30%。这是平台活动，不是永久 API 降价，预算时应以活动条款和实际到账为准。

## Kimi K3 到底新增了什么

K3 不只是给 K2 换了一个更大的 context 字段。月之暗面称其为 2.8 万亿参数模型，采用 Kimi Delta Attention 和 Attention Residuals，并使用稀疏 Mixture-of-Experts 架构。对 API 开发者而言，真正重要的是这些能力如何影响工程流程：

- **1M 上下文与自动缓存：** 普通请求可自动尝试前缀缓存，不需要手动管理 cache ID 或 TTL。
- **原生视觉：** K3 支持文本、图片和视频。图片应使用 base64 或 Kimi 文件引用，而不是公网图片 URL。
- **始终开启思考：** K3 始终进行推理，当前 `reasoning_effort` 仅有 `max` 档位。不要把 K2.x 的 thinking 参数直接套过来。
- **工具控制：** 支持工具调用、`tool_choice` 和动态加载工具。工具很多但每轮只需一小部分时，动态加载能减少 Prompt 膨胀。
- **结构化输出：** JSON Mode 和 JSON Schema 适合抽取任务与工作流状态。
- **长程编程：** 官方定位包括大型代码库、终端协调、视觉反馈、前端和 CAD 等任务。

这些是平台能力，不是“上下文越大所有任务越好”的保证。把整个工作区在每一轮都发送给模型，可能增加延迟、调试复杂度和缓存失效率。

## curl 首次调用

Kimi 提供 OpenAI 兼容接口。把 API Key 放在环境变量中，用最小请求先验证链路：

```bash
export KIMI_API_KEY="YOUR_KIMI_API_KEY"
curl https://api.moonshot.cn/v1/chat/completions \
  --header "Authorization: Bearer YOUR_KIMI_API_KEY" \
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

把 `response.usage` 写进成本面板。对 K3 来说，用量观测不是可选项：缓存命中与未命中的差距很大，输出 token 的单价也远高于输入。

## 视觉、JSON 与 Agent 工作流

Kimi 文档要求视觉请求中的 `message.content` 是内容部件数组，不要把数组序列化成字符串：

```python
message = {
    "role": "user",
    "content": [
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}},
        {"type": "text", "text": "描述界面布局，并列出可见的 UI 缺陷。"},
    ],
}
```

K3 同时支持 JSON Mode 和 JSON Schema。用于抽取时，Schema 应保持小而明确，并在客户端验证返回对象。在 Agent 系统里，可以把结构化输出和 `tool_choice` 组合起来，避免模型在回答与修改外部系统之间静默切换。

动态加载工具对长上下文 Agent 尤其有意义：不要每轮发送完整工具目录，而是在 Agent 进入对应阶段时再加载所需定义。这既能减少 Prompt 体积，也有助于保持缓存前缀稳定。

## Kimi K3、K2.7 Code、K2.6 怎么选

当上下文规模和多模态长程工作是核心诉求时，选 **Kimi K3**。它适合大型代码库、长文档、视觉反馈、持续工具调用和中英文知识工作，但需要为输出价格和缓存行为做预算。

当任务主要是编程、256K 已够用时，选 **Kimi K2.7 Code**。它的未命中输入是 ¥6.50/M、输出 ¥27/M，成本上限明显低于 K3。HighSpeed 版本官方说明输出速度约 180 tokens/s，短上下文可达约 260 tokens/s，但价格也翻倍到 ¥13/M 未命中输入、¥54/M 输出。

当你要的是更便宜的通用多模态模型，选 **Kimi K2.6**。它支持 256K 上下文、思考与非思考模式、文本图片视频输入，适合普通对话、视觉理解和 Agent 任务，输出价格同样是 ¥27/M。

从 OpenAI 迁移时，建议用生产形态的评测集同时测试三个模型：工具调用有效率、JSON 遵循率、缓存命中率、首 token 延迟、总输出 token 和人工修正时间。“OpenAI 兼容”描述的是线路格式，并不意味着行为完全相同。

## 限制与生产风险

1. **¥15 新用户代金券不能解锁 K3。** 官方 K3 指南明确说明，模型发布后该券不能用于体验 K3，需要充值。
2. **推理始终开启。** 当前 K3 仅支持 `reasoning_effort=max`，简单任务也可能付出更高输出与延迟。
3. **公网图片 URL 不是稳妥路径。** 视觉输入使用 base64 或 Kimi 文件引用，且 content 必须是数组。
4. **联网搜索正在升级。** 当前官方文档提示 web search 仍在更新，暂不建议用于生产流程。
5. **权重发布不等于 API 变价。** 月之暗面称完整 K3 权重计划在 2026 年 7 月 27 日前发布；未来开源可能改变托管经济，但不会改变今天的 API 账单。
6. **区域访问属于 TCO。** Kimi API 开放平台面向中国大陆直连设计；其他地区团队应先验证网络、数据流向和服务支持。

如果需要跨 provider 的控制面板，也可以通过 [FreeModel API 接入](https://freemodel.dev/invite/FRE-7a3b6220)把 Kimi 和其他端点放进同一套评测与路由流程。它是路由选择，不应替代对上游模型 ID、用量口径和区域条款的核对。

## 最适合的使用场景

- **仓库级 Coding Agent：** 把架构说明、代码、测试和工具结果放在同一工作上下文，并按阶段控制工具。
- **中文长文档知识工作：** 分析政策、法律、产品或研究资料，减少过度切块。
- **视觉软件流程：** 在前端、游戏、CAD 或 UI 迭代中读取截图、界面状态和短视频。
- **结构化运营：** 用 JSON Schema 做抽取，用工具调用执行受控动作，并为副作用加审批门。

如果只是短问答、小型 JSON 抽取，或者输出 token 占据主要成本，K3 可能并不划算；这时 K2.6 或其他低输出价格的端点更合理。

## 结论：买上下文，不要买参数幻觉

Kimi K3 是一次有实际工程价值的 API 发布：1M 上下文、视觉、工具、结构化输出、自动缓存和 OpenAI 兼容接口，足以让它进入 Coding Agent 与长文档工作流的候选名单。

代价同样清楚：未命中输入 ¥20/M、输出 ¥100/M，K3 不是便宜的通用聊天 API。稳定复用前缀、控制输出长度时，它的长上下文优势可能抵消成本；每轮缓存失效并产生长推理时，账单会迅速失控。

我们的建议是用生产形态评测集同时跑 K3、K2.7 Code 和 K2.6。如果 K3 能减少切块错误、工具重试和人工审核，并超过高输出单价带来的成本差，它就是最值得买的 Kimi 模型；否则 K2 系列以更低价格提供了大部分兼容和多模态能力。

## 常见问题

**Kimi K3 的价格是多少？** 根据官方价格表，缓存命中输入 ¥2/M，缓存未命中输入 ¥20/M，输出 ¥100/M。

**Kimi K3 真有 1M token 上下文吗？** 有。官方模型文档和价格页都列出 1,048,576 token 上下文窗口。但上限很大不代表每次请求都应塞满，仍需要合理的检索和 Prompt 管理。

**Kimi K3 能用 OpenAI Python SDK 吗？** 可以。把 `base_url` 设置为 `https://api.moonshot.cn/v1`，使用 Kimi API Key 和官方模型 ID；视觉、思考、工具等扩展字段要单独按 Kimi 文档验证。

**Kimi K3 支持图片和视频吗？** 支持。当前指南说明 K3 支持文本、图片和视频输入；图片建议使用 base64 或 Kimi 文件引用，`content` 使用部件数组。

**¥15 新用户代金券能用于 K3 吗？** 不能。月之暗面的 K3 快速开始文档明确说新用户代金券不能体验 K3，需要充值。

**应该改用 Kimi K2.7 Code 吗？** 如果 256K 已够用、且你主要做代码任务，应该认真比较 K2.7 Code。官方价格为未命中输入 ¥6.50/M、输出 ¥27/M，明显低于 K3。

**Kimi K3 的联网搜索能上生产吗？** 当前官方文档提示联网搜索正在升级，不建议用于生产流程。应等待月之暗面更新文档后再作为关键依赖。

## 来源

- 月之暗面，[Kimi K3 模型文档](https://platform.kimi.com/docs/guide/kimi-k3-quickstart)
- 月之暗面，[Kimi K3 价格](https://platform.kimi.com/docs/pricing/chat-k3)
- 月之暗面，[Kimi K2.7 Code 价格](https://platform.kimi.com/docs/pricing/chat-k27-code)
- 月之暗面，[Kimi K2.6 价格](https://platform.kimi.com/docs/pricing/chat-k26)
- 月之暗面，[Kimi K3 充值返券活动](https://platform.kimi.com/docs/pricing/promotion)
- 月之暗面，[Kimi K3 技术博客](https://www.kimi.com/blog/kimi-k3)
