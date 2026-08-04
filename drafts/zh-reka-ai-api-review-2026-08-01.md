---
title: "Reka AI API 2026 测评：多模态与 Research 代理的同接口整合"
description: "Reka AI API 2026 深度评测：Edge、Flash、Core、Spark 模型、多模态输入、Research 代理、OpenAI 兼容端点、国内可用性、定价与最终结论。"
slug: "reka-ai-api-review"
provider: "reka-ai"
published: true
date: "2026-08-01"
type: "review"
---

# Reka AI API 2026 测评：多模态与 Research 代理的同接口整合

## 引言：为什么 Reka AI 在 2026 年值得关注

Reka AI 是一家位于旧金山的 AI 实验室，由 Dani Yogatama、Cyprien Courtot 与一群来自 Google、Meta 与 DeepMind 的研究者在 2022 年共同创立。它没有沿用美国主流的"一个聊天模型 + 一个独立视觉模型 + 一个独立音频模型"路径，而是训练了一个能原生吞噬<strong>文本 / 图像 / 视频 / 音频</strong>的<strong>单一模型族</strong>，并通过一个 OpenAI 兼容端点 <code>https://api.reka.ai/v1/chat/completions</code> 对外发布。在聊天模型之上，Reka 还上线了一个 <strong>Research 代理</strong>（<code>reka-flash-research</code>）——它会执行多步联网检索、阅读返回页、并最终输出带引用的合成答案，按"千次请求"叠加在 token 之上计费。

对 Reka 在 2026 年 8 月的诚实定位：它<strong>不是</strong>GPT-5.6 或 Claude 4.5 在预训练算力或基准跑分上的正面对手。Reka 旗舰 <code>reka-core</code> 在美国基准跑分总榜上的纯文本推理能力大致处于中段。Reka 的赌注是：对于"多模态 AI 市场"的一个有意义切片——需要文本+图像+视频+音频整合在一张发票上的产品团队、需要"内置可引用研究端点"的 Agent 构建者、能把廉价流量路由到 <code>reka-edge</code>（$0.10/百万 tokens）的成本敏感负载——合并带来的便利胜过 MMLU 上 3 分的领先。对这个切片而言，Reka 是最直接的"一家供应商"答案。

Reka 在 2026 年评测里反复出现的另一个原因：<strong>OpenAI 兼容</strong>的接口形态决定了一个已有 OpenAI SDK 的代码栈只需改一个 <code>base_url</code> 就能落到 Reka。对关心 API 可移植性、不愿意重写 Agent 代码的团队，这是结构性的优势。

## 模型矩阵：Reka 家族（Edge / Flash / Core / Spark）

Reka 当前的生产线是从 <strong>Edge → Flash → Core → Spark</strong> 的四级梯子，加上 <code>reka-flash-research</code> 形态的研究代理。所有这五个模型都由同一个 <code>https://api.reka.ai/v1/chat/completions</code> 端点对外提供，仅靠模型名字区分。

### reka-edge —— 仅文本，最低成本

最小号的生产模型。仅支持文本输入/输出——<strong>不支持</strong>图像、视频或音频。输入/输出均为 <strong>$0.10/百万 tokens</strong>，可选叠加 <strong>$0.005/每张图</strong>的图像加价（用于偶尔的多模态复用）。当需要廉价且快速的路由、意图分类、查询改写、或不需要看像素的后台抓取时，<code>reka-edge</code> 是合适的模型。它<strong>不是</strong>任何涉及非文本模态的工作负载的正确选择。

### reka-flash —— 多模态中段

中间档主力。支持文本、图像、视频与音频输入，<strong>同一</strong> <code>/v1/chat/completions</code> 调用即可。输入/输出分别为 <strong>$0.80 / $2.00</strong> 每百万 tokens，叠加 <strong>$0.01/每张图</strong>、<strong>$0.06/每分钟视频</strong>、<strong>$0.015/每分钟音频</strong>。<code>reka-flash</code> 是大部分多模态生产管线的默认模型——质量与价格都处在合理平衡点上，并且非文本模态的按单位计费对标独立视觉/音频 API 具有竞争力，而这些 API 否则就需要拼装在一起。

### reka-core —— 前沿多模态

Reka 旗舰。文本/图像/视频/音频原生多模态，在联合多模态数据上端到端训练。输入/输出分别为 <strong>$2.00 / $6.00</strong> 每百万 tokens，叠加 <strong>$0.02/每张图</strong>、<strong>$0.08/每分钟视频</strong>、<strong>$0.02/每分钟音频</strong>。当多模态理解必须是"同类最佳"时——尤其是重度视频场景——<code>reka-core</code> 是首选模型。Reka 在视频理解上的按帧采样历史上一直是它的强项。

### reka-spark —— 实验档

一个更新的、低延迟的模型档位，面向快速交互式助手。定价反映实验属性，以 Reka 官方文档为准。<code>reka-spark</code> 是一个"面向未来"的档位——可能稳定为一个新的 Edge 级别，也可能一直停在实验阶段，请始终以文档为准。

### reka-flash-research —— Research 代理

严格意义上不是"聊天模型"。Research 代理端点会规划多步联网检索、并行执行搜索、阅读返回页、并合成带引用的答案。<strong>按千次请求</strong>而非按 token 计费：

| 档位 | 每千次请求 | 适用场景 |
|---|---|---|
| Standard | $25 | 单轨迹规划、开启引用——默认研究模式 |
| Parallel-low | $35 | 多轮并行检索、放宽并发控制，对成本敏感的研究 |
| Parallel-high | $60 | 高并发并行研究，面向低延迟深度检索 |

当买家需要"带引用的可溯源答案"时，这是正确模型——分析师简报、市场扫描、供应商尽调、对一条说法的核查。它<strong>不是</strong>闲聊或按 token 计费的大批量生成的合适工具；务必把它放到一个明确的产品/UX 闸门之后，并对每千次请求成本做好预算。

## 完整定价（2026 年 8 月，源自 docs.reka.ai）

| 模型 | 输入（USD / 百万 tokens） | 输出（USD / 百万 tokens） | 图像（每张） | 视频（每分钟） | 音频（每分钟） |
|---|---|---|---|---|---|
| reka-edge | 0.10 | 0.10 | 0.005 | 0.03 | — |
| reka-flash | 0.80 | 2.00 | 0.01 | 0.06 | 0.015 |
| reka-core | 2.00 | 6.00 | 0.02 | 0.08 | 0.02 |

Research 加价（每千次请求，叠加在 token 之上）：<strong>标准 $25</strong>、<strong>并行-低 $35</strong>、<strong>并行-高 $60</strong>。

几个必须第一时间钉死的定价说明：

- <strong>无永久免费额度。</strong>Reka 从首个请求起按量计费。app.reka.ai 上的账号必须在任何流量产出使用之前充值。模型发布时偶有促销 credits，但都不在公开价目卡上。
- <strong>每张图 / 每分钟计费与 token 消耗独立。</strong>一段 30 秒视频 + 200 tokens 标题描述的调用，会同时按 0.5 分钟视频和 200 文本 token 计费。请把成本计算器按照<em>两条轴</em>建模。
- <strong>Research 端点成本会复合。</strong>一次计入 <code>parallel-high</code> 的研究请求，会同时消耗 $60/千次请求费用，加上 <code>reka-flash</code> 在规划与合成步骤中实际产生的 token 费用。对每天 1000 次深度查询的工作负载，<em>仅 Research 那一项</em>就是 $60/天。

## API 接口：OpenAI Chat Completions 兼容

Reka 在 2026 年面向开发者最大的故事是：<strong>生产端点遵循 OpenAI Chat Completions 协议</strong>。你只需替换 base URL 与 API Key，就可以在 OpenAI Python SDK、OpenAI Node SDK、Vercel AI SDK、LangChain、LlamaIndex、AutoGen 以及任何 OpenAI 兼容客户端中调用 Reka。

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.reka.ai/v1",
    api_key="YOUR_REKA_API_KEY",
)

resp = client.chat.completions.create(
    model="reka-flash",
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": "这段视频片段里发生了什么？"},
            {"type": "image_url", "image_url": {"url": "https://example.com/frame.jpg"}}
        ]}
    ],
)
print(resp.choices[0].message.content)
```

同样的模式也适用于 Research 代理——只需要把模型名换为 <code>reka-flash-research</code>，调用就会走 Reka 的研究管线：

```python
resp = client.chat.completions.create(
    model="reka-flash-research",
    messages=[{"role": "user", "content": "总结 2026 年 7 月欧盟 AI Act 的执法动态，并附引用。"}]
)
```

工具/函数调用、JSON 模式、SSE 流式响应均沿用 OpenAI 的语法规范。官方文档站点上<strong>没有</strong>独立的 Reka 原生 SDK——Reka 明确推荐使用 OpenAI 一方 SDK 并覆盖 <code>base_url</code>。这一点与同时发布并行原生 SDK 的友商形成了明确区分：Reka 在赌 OpenAI SDK 表面已经在任何你需要的地方都现成可用。

## 单调用多模态：文本 + 图像 + 视频 + 音频

Reka 在 2026 年面向产品的最大故事是<strong>模态整合</strong>。在 <code>reka-core</code> 和 <code>reka-flash</code> 上，你可以把单条消息的 content 数组混排文本、图像、视频与音频片段，模型会返回统一的答案：

```json
{
  "model": "reka-core",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "text", "text": "这段监控视频里发生了什么？"},
      {"type": "image_url", "image_url": {"url": "https://example.com/frame.jpg"}},
      {"type": "video_url", "video_url": {"url": "https://example.com/clip.mp4"}},
      {"type": "audio_url", "audio_url": {"url": "https://example.com/call.mp3"}}
    ]
  }]
}
```

这<strong>不是</strong>"视觉模型 + 音频模型"管线拼装。Reka 在联合多模态数据上端到端训练模型，因此：

- <strong>图像：</strong>JPEG / PNG / WebP，URL 或 base64。按模型的"每张图"价目计费。reka-core 是视觉最强选择；reka-flash 是预算方案。
- <strong>视频：</strong>MP4 或短视频 URL。Reka 在推理时按帧采样。按分钟计费。视频理解是 Reka 最被频繁提到的能力。
- <strong>音频：</strong>MP3 / WAV。按分钟计费。Reka 在同一遍调用里完成转写与语义推理——可用于客服电话、语音便签、会议录音片段。

对于"减少供应商数量"敏感的工作负载（一个 API Key、一张发票、一个限速面），Reka 的多模态整合方式相对 OpenAI 的"GPT-4o-vision + Whisper + GPT-audio 拆分端点"或 Google 的"Gemini 文本 + Gemini 视觉 + Vertex Speech 拆分"具有结构性优势。

## Research 代理：带引用的多步联网检索

<code>reka-flash-research</code> 端点在形态上与"普通聊天补全"本质不同。它<strong>不是</strong>返回一条模型答案，而是：

1. 针对你给出的主题规划子问题。
2. 并行派发联网搜索。
3. 读取每个返回页。
4. 合成最终答案，并把 URL 作为行内引用附上。

当买家是一个人或者一个 Agent、需要"带可溯源来源的可辩护答案"时，这是正确的工具——分析师简报、市场扫描、供应商尽调、对一条说法的核查。它<strong>不是</strong>闲聊、创意写作或按 token 计费的大批量生成的合适工具。请把它放到一个明确的产品/UX 路径之后，并对每千次请求成本做好预算。

Reka 对 Research 代理的定价姿态是市场上最不寻常的。多数美国实验室要么按 token 给研究定价，要么把成本折进模型档位；Reka 给出一张干净的"每千次请求"价目卡（$25 / $35 / $60，分别对应 Standard / Parallel-low / Parallel-high）。对于围绕"调用量"而非"token 量"做优化的产品团队，这种定价比按 token 定价更可预期。

## 中国大陆与亚太可用性

Reka 是美国总部、生产端点 <code>api.reka.ai</code> 托管在美国区域的服务，<strong>无公开的中国大陆端点</strong>。截至 2026 年 8 月：

- 从中国大陆 ISP 直连的稳定性不做保证。
- 我们刻意<strong>不发布</strong>具体延迟数字——跨境路由条件每周都在变，捏数字会误导而非帮助决策。
- 对面向中国大陆的生产工作负载，Reka 通常通过稳定跨境代理、走香港或新加坡前置层、或替换为提供类似 <code>/v1/chat/completions</code> 接口的国内 OpenAI 兼容厂商来落地。

国内团队需要"Reka 级多模态"能力的现实路径：

- <strong>稳定跨境代理</strong>到 <code>api.reka.ai</code>——适用于低流量原型与小规模生产，但路由健康度需要持续监控。
- <strong>香港或新加坡前置</strong>用于正式生产，配合激进 token 流量缓存来约束跨境带宽。
- <strong>国内 OpenAI 兼容替代</strong>——阿里 Bailian / 通义千问、智谱 GLM、DeepSeek、月之暗面 Kimi、百度文心 Ernie 均提供 <code>/v1/chat/completions</code> 接口，并且国内骨干网内的延迟显著更低。
- <strong>通过 FreeModel 做混合路由</strong>——OpenAI 兼容聚合层，可根据用户所在区域动态选路，在多模态质量与延迟之间取得平衡。FreeModel 是希望保留 OpenAI SDK 契约、又不想被 Reka 区域足迹锁定的团队在 apirank 风格侧边栏中的合适替代。

## Reka vs OpenAI / Anthropic / Google / Mistral

| 厂商 | 旗舰模型 | Reka 优势 | Reka 劣势 |
|---|---|---|---|
| OpenAI | GPT-4o / GPT-5.6 | 单端点覆盖文本+图像+视频+音频（无需拼装独立视觉/音视频 API）；在 <code>reka-edge</code> 上激进压低价格。 | 生态规模与第三方工具深度；Agent 集成更深（Assistants API、function calling 历史积累）。 |
| Anthropic | Claude Sonnet / Opus | 多模态整合；<code>reka-edge</code> 更便宜；一等公民的 Research 代理端点。 | 长上下文推理基准；Claude Code / Computer-Use 套件成熟度。 |
| Google | Gemini 1.5 / 2.x | 单端点跨模态；简化的按量付费账单；省去 Google Cloud 认证 overhead。 | 上下文窗口长度（Gemini 1M+）；面向企业的 Vertex AI / Google Cloud 集成。 |
| Mistral | Pixtral Large / Mistral Large | Research 代理端点；按单位整合的多模态定价。 | 开源权重自托管；EU AI Act 合规；按区域部署控制。 |

诚实的产品定位：Reka 是这样一类场景的最佳选择——<strong>模态整合、单张发票、OpenAI 兼容可移植性</strong>比"绝对前沿基准跑分"更重要。如果负载集中在长上下文推理，或者明确需要百万级 token 上下文窗口，Anthropic 与 Google 在各自轴上仍然胜出。

## 局限性（诚实列出）

若干必须真实纳入 2026 年采购评估的摩擦：

1. <strong>无公开永久免费额度。</strong>Reka 从首个请求即按量付费。需要免费 OpenAI 兼容接口的业余项目、开源工具，应该看 FreeModel 而不是尝试在 Reka 上"薅" credits。
2. <strong>仅美国托管，无中国大陆端点。</strong>中国大陆路由必须经过代理。延迟完全取决于你购买的代理档位。
3. <strong>品牌与生态滞后。</strong>Reka 的品牌识别度显著低于 OpenAI、Anthropic 与 Google。社区 SDK 示例、博客文章、框架集成深度与 SO 答案相应地更稀薄。
4. <strong>Research 端点成本控制是刚需。</strong><code>parallel-high</code> 每千次 $60，意味着生产环境下失控的研究循环可以比按 token 计费的端点更快地累计支出。请给端点设闸门、给账号设额度上限、给配额异常设告警。
5. <strong>企业合规公开材料较少。</strong>SOC 2 Type II 与 HIPAA 的认证覆盖在公开渠道不如头部厂商那么显眼。合规门槛严格的采购团队必须按合同一一确认，不能默认假设已覆盖。
6. <strong>基准跑分的"对外声音"较安静。</strong>Reka 没有像某些前沿实验室那样高调宣传"我们在 X 基准上击败 GPT-5.6"。这让首次接触 Reka 的买家做对比时稍微费力。

## 结论：2026 年谁应该引入 Reka AI

<strong>应引入 Reka：</strong>希望一个 OpenAI 兼容端点统一覆盖文本/图像/视频/音频；重视内置 Research 代理带来的"带引用的多步回答"；希望把开票主体收敛到一家；或者有可路由到 <code>reka-edge</code>（$0.10/M tokens）的成本敏感流量。

<strong>应跳过 Reka：</strong>业余项目需要永久免费额度；主体位于中国大陆、且无法接受代理路由；负载集中在前沿长上下文推理（在 Anthropic / Google 跑分仍更强）；合规团队在签合同前就要求 SOC 2 / HIPAA 认证白纸黑字。

务实的推荐是：把代码写在 OpenAI 的 <code>/v1/chat/completions</code> 契约上，并在部署时再选底层供应商——这样未来从 Reka 迁到 OpenAI、Anthropic、Google 或国内厂商，只是配置改动，不是重写。不管底层选 Reka、OpenAI 还是 FreeModel 路由，应用逻辑保持不变。

## 联盟营销披露

APIRank 与 Reka AI 之间<strong>不存在</strong>联盟营销关系。APIRank 风格评测页侧边栏中的 FreeModel 提及，是 OpenAI 兼容免费额度路由的替代推荐，不是 Reka 的联盟推广。"每千次请求"研究端点定价、每张图、每分钟视频与每分钟音频的费用，已于 2026 年 8 月 1 日从 <code>https://docs.reka.ai/</code> 校验。

## 延伸阅读

- OpenAI API 2026 定价：GPT-4o / GPT-5.6 多模态账单对照
- Anthropic Claude API 测评：长上下文推理基准横向对比
- Google Gemini API 测评：百万级 token 上下文窗口定价
- FreeModel 聚合路由：面向业余项目与原型的 OpenAI 兼容免费额度入口
