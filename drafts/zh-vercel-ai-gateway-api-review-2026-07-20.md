# Vercel AI Gateway 2026：零加价的 AI 路由层（Vercel 原生应用首选）

_Date: 2026-07-20 | Slug: vercel-ai-gateway-api-review | Locale: zh_

# Vercel AI Gateway 2026：内嵌在 Vercel 平台的零加价 AI 路由器

Vercel AI Gateway 是 Vercel 在 2026 年推出的 AI 路由层，对标 OpenRouter、Cloudflare AI Gateway、Portkey、LiteLLM 和 Helicone。2026-07-20 核验后的定价对开发者非常友好：**每团队每月 $5 免费 AI Gateway Credits**、**Token 零加价**（包括 BYOK 客户）、以及无论你使用自带密钥还是 Vercel 发放的凭证都按同价 pay-as-you-go 计费。该 Gateway 在所有 Vercel 套餐上可用，原生集成 AI SDK v5/v6，并开箱即支持 OpenAI Chat Completions、OpenAI Responses、Anthropic Messages 和 OpenResponses 多种 API 协议。
本文将介绍 Vercel AI Gateway 的能力、2026 年核验后的定价（免费层、付费层、附加费），并与 OpenRouter、Cloudflare AI Gateway、Portkey、LiteLLM、Helicone 进行对比。所有数据来自 vercel.com/docs/ai-gateway/pricing（页面最后更新于 2026-06-20，2026-07-20 核验）。如果你的技术栈跑在 Vercel 上，正在评估 2026 年的 AI Gateway 厂商，这篇就是参考指南。
## Vercel AI Gateway 的能力（与边界）

Vercel AI Gateway 是 AI 路由层，不是模型供应商。你继续使用现有的 OpenAI / Anthropic / Google / xAI / Mistral / Cohere / Groq 账户；Vercel 充当你的应用与上游 Provider 之间的透明代理，负责鉴权、计费、故障转移和可观测性。核心能力：
- 一个 API Key，访问数百个模型。一个 Vercel 发放的 API Key 即可路由到所有主要 Provider 的数百个模型。
- 统一 API。修改请求中的一个字符串即可在不同 Provider 和模型之间切换 — GPT-4o、Claude Opus 4.8、Gemini 2.5 Pro、Llama 3.5 405B 之间只需几行代码变更。
- 高可靠性。当一个 Provider 请求失败时，自动重试到其他 Provider（模型 Fallback），支持可配置的 Provider 超时。
- Embeddings 支持。一等公民支持 Embeddings、Rerank（Cohere Rerank）、语音转文字、文字转语音、图片生成、视频生成（Beta）。
- 花费监控。按请求的可观测性，支持成本归因、延迟追踪、跨 Provider 用量指标。
- Token 零加价。Token 价格与直接从 Provider 购买一致 — 包括 BYOK 客户，Gateway 不会抬高账单。
- AI SDK v5/v6 原生集成。在任何 Next.js / Vercel 部署的应用中实现一行代码替换；AI SDK 已经是大部分 Vercel 客户正在使用的框架。
Vercel AI Gateway 不训练或微调模型，不托管自有基础模型（与 Cloudflare Workers AI 不同），也不捆绑无代码 Prompt 调试台（与 Portkey 的 App Portal 不同）。该产品紧密聚焦在「Vercel 生态系统的路由 + 可观测性」，而这种聚焦正是「零加价」模型得以持续的根本原因。
## Vercel AI Gateway 2026 定价：每月 $5 免费，然后按量付费

Vercel AI Gateway 2026-07-20 核验后的定价（数据源：vercel.com/docs/ai-gateway/pricing，页面最后更新 2026-06-20）：套餐每月额度Token 价格速率限制BYOK 支持免费层每团队每月 $5Provider 官价，零加价每模型更低限制❌ 不支持付费层按购买 Credits 用量付费Provider 官价，零加价可定制限制✅ 支持（零加价）
免费层每个 Vercel 团队账户每月附带 $5 的 AI Gateway Credits。团队发出第一个 AI Gateway 请求后，Credits 即激活。免费额度先用先扣，不滚存。免费层限制在标记为「Free Tier eligible」的子集模型；完整模型目录可在 Vercel 控制台浏览。
一旦任何团队成员购买了 AI Gateway Credits，团队即升级到付费层：每月 $5 免费额度失效，但付费层解锁完整模型目录、更高速率限制、BYOK 支持和附加功能（如 Custom Reporting）。无承诺消费 — Credits 按用量付费，可在控制台配置自动充值。
### 附加费（付费层）
Vercel AI Gateway 招牌的「零加价」承诺适用于 Token。附加功能有从 AI Gateway Credits 余额中扣除的小额按请求附加费：能力费用可用套餐Custom Reporting 写入每 1,000 次 tag / 用户 ID / quota entity 写入 $0.075所有付费层Custom Reporting 查询每 1,000 次 reporting endpoint 查询 $5所有付费层团队级 Provider 白名单每 1,000 次成功请求 $0.10Pro 和 Enterprise团队级 Zero Data Retention（ZDR）每 1,000 次请求 $0.10Pro 和 Enterprise按请求 Provider 过滤无附加费所有套餐按请求 Zero Data Retention无附加费所有套餐
「按请求」版的 Provider 过滤和 ZDR 是免费的；「团队级」版本收费 $0.10 / 1,000 请求。大部分团队不需要团队级强制 — 按请求 providerOptions 已足够且免费。Custom Reporting 是可选启用，对多租户应用的成本归因很有用。
### BYOK：自带密钥，零加价
BYOK 是与 Cloudflare AI Gateway 对比时的重大差异点：Cloudflare 收取 Workers Paid 套餐费 + 每百万请求 $0.20 Gateway 加价；OpenRouter 要求你即使使用自有密钥也要充值 OpenRouter Credits。Vercel AI Gateway 让你将 OpenAI / Anthropic / Google 的密钥粘贴到控制台，通过你的凭证路由请求，并支付零加价。如果 BYOK 请求失败，Vercel 用自己的系统凭证重试并将回退用量计入你的 Credits 余额 — 相比 Cloudflare 的按请求加价，这是一个微小但仍更便宜的可靠性税。
## Vercel AI Gateway vs OpenRouter vs Cloudflare AI Gateway vs Portkey vs LiteLLM vs Helicone

六个产品都解决「我需要在多个 Provider 之间路由 LLM 调用并观测发生了什么」的问题，但优化方向各异。下表针对 50 人工程团队 + 已经部署在 Vercel 上的应用做了校准：特性Vercel AI GatewayOpenRouterCloudflare AI GatewayPortkeyLiteLLMHelicone开源❌ 闭源❌ 闭源❌ 闭源❌ 闭源✅ MIT✅ Apache-2.0自托管❌❌❌❌✅✅Provider 数量数百数百500+200+100+100+免费层每月 $5 Credits部分模型免费每月 100 万次请求1 万次/月无限（OSS）1 万次/月团队层价格按量付费按量付费$5/月 + 用量$49/月（Hobby）免费（OSS）$79/月（Pro）Token 加价零加价大部分零加价Provider 费上加价差异较大免费BYOK 免费零加价BYOK❌ 不支持❌ 不支持❌ 收费✅ 应用配置✅ YAML 配置✅ 环境变量可观测性✅ 内置✅ 内置✅ 内置✅ 全栈⚠️ 仅日志✅ 全栈 HQL模型 Fallback✅ 内置✅ 内置⚠️ 手动配置✅ 内置✅ 可配置✅ 内置图像/视频/语音✅ 支持（Beta）✅ 支持⚠️ 有限⚠️ 有限❌ 不支持❌ 不支持原生框架绑定AI SDK v5/v6OpenAI / Anthropic SDKOpenAI / Anthropic SDKOpenAI / Anthropic SDKPython SDKOpenAI / Anthropic SDK
定价 2026-07-20 核验自各厂商公开定价页。Vercel AI Gateway $5/月免费 + 零加价；OpenRouter 免费 + 大部分模型零加价；Cloudflare AI Gateway 免费 100 万次/月 + $0.20/百万超出；Portkey Hobby $49/月 + 用量；LiteLLM 免费自托管；Helicone Pro $79/月。
如果你的技术栈已经在 Vercel 上，想要零加价 + 最低设置成本，Vercel AI Gateway 是最强选择。如果你不依赖 Vercel，需要最广的 Provider 覆盖，OpenRouter 是默认选项。如果你想要带 App Portal 和 Guardrails 的精致 SaaS 体验，Portkey 更合适。如果你想完全自托管 + 带查询语言的调用分析，Helicone 或 LiteLLM 胜出。Cloudflare AI Gateway 是最便宜的纯代理选项，但每请求加价在大规模时会累加。
## Vercel AI Gateway 工作原理（附代码示例）

最简单的集成是在 Vercel AI SDK 中修改一行 model 字符串。默认的 OpenAI Python SDK 替换 base URL 后无需修改：
## 使用 AI SDK v5（Vercel 原生路径）
```typescript
// app/api/chat/route.ts
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'anthropic/claude-opus-4.8', // Vercel AI Gateway 格式：provider/model
  prompt: 'What is the capital of France?',
});
// 后台，Vercel AI Gateway 路由到 Anthropic，
// 应用你的 BYOK 密钥（或 Vercel 发放的凭证），
// 记录请求到可观测性控制台，
// 并从你的 Credits 余额中扣除费用。
```
尚未迁移到 AI SDK v5 的团队，OpenAI Chat Completions 和 Anthropic Messages 兼容垫片让你只替换 base URL 和 API Key 即可保留现有 SDK。
## 使用 OpenAI Chat Completions 兼容接口
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ['AI_GATEWAY_API_KEY'],  # Vercel 发放，不是 OpenAI 的
    base_url='https://ai-gateway.vercel.sh/v1',
)

response = client.chat.completions.create(
    model='openai/gpt-4o',  # Vercel AI Gateway 格式：provider/model
    messages=[{'role': 'user', 'content': '你好，GPT-4o via Vercel。'}],
)
print(response.choices[0].message.content)
```
## 使用 Anthropic Messages 兼容接口
```python
from anthropic import Anthropic
import os

client = Anthropic(
    api_key=os.environ['AI_GATEWAY_API_KEY'],
    base_url='https://ai-gateway.vercel.sh',
)

message = client.messages.create(
    model='anthropic/claude-sonnet-4-20250514',
    max_tokens=1024,
    messages=[{'role': 'user', 'content': '你好，Claude via Vercel。'}],
)
```
两个 SDK 都通过同一个 Vercel AI Gateway 路由，记录到同一个可观测性控制台，应用同样的零加价定价。修改 `model=` 即可在 Provider 之间切换，无需更换 SDK 或 API Key。
## 控制台 BYOK 设置
要自带密钥，进入 Vercel 控制台的 AI Gateway 板块，点击「Provider Keys」，粘贴每个你想使用的 Provider 的 API Key。Vercel 静态加密密钥，使用 BYOK 的任何请求都按零加价计费。如果 BYOK 请求失败（速率限制、网络抖动、密钥过期），Vercel 用系统凭证重试并将回退用量计入你的 Credits 余额。
## 模型 Fallback 实现高可靠性
对于需要在某个 Provider 故障时保持在线的生产系统，Vercel AI Gateway 的 `providerOptions` API 让你在代码中指定 Fallback 链：
```typescript
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'anthropic/claude-opus-4.8',
  prompt: '总结 Q3 财报。',
  providerOptions: {
    // 如果 Anthropic 失败或超时，尝试 OpenAI
    fallback: ['openai/gpt-4o', 'google/gemini-2.5-pro'],
  },
});
```
Vercel AI Gateway 自动重试 Fallback 链，保留同样的 prompt 和可观测性事件。重试记录在控制台中，因此你可以看到每个 Fallback 触发的频率。
## Custom Reporting 实现成本归因
对于需要按客户 LLM 成本归因的多租户 SaaS 应用，Custom Reporting 将 tag / 用户 ID / quota entity ID 添加到请求中，然后可通过 reporting endpoint 查询：
```typescript
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'openai/gpt-4o',
  prompt: '总结这个客户支持工单。',
  providerOptions: {
    gateway: {
      // 每个 tag / 用户 ID 计 $0.075 / 1,000 次写入
      userId: 'customer_123',
      tag: 'support-ticket-summary',
    },
  },
});
```
后端作业每小时运行一次，查询 reporting endpoint（$5 / 1,000 次查询）并生成按客户的月度账单。与构建自有日志管道相比，Custom Reporting 成本可忽略不计，却能节省大量工程时间。
## 真实应用场景

三种 Vercel AI Gateway 一个月内回本的使用模式：
- 一个跑在 Vercel 上的 Next.js 应用做多 Provider 路由。Vercel 默认推荐的技术栈是 AI SDK v5 + AI Gateway。Drop-in 兼容意味着从 OpenAI 切换到 Anthropic 是改一个 model 字符串，不是重构。对于已支付 Vercel Pro（$20/月/座位）的团队，每月 $5 免费 AI Gateway Credit 几乎是白送。
- 需要按客户 LLM 成本归因的多租户 SaaS。Custom Reporting 用租户 ID 标记每个请求，让你每小时跑一次 SQL 查询 reporting endpoint，生成按客户账单。没有 AI Gateway 的话，要么用第三方可观测性供应商（Helicone Pro $79/月 或 Portkey Hobby $49/月），要么构建自定义日志管道。
- 需要自动 Provider Failover 的生产应用。当 OpenAI 区域故障时，Vercel AI Gateway 的模型 Fallback 链用同样的 prompt 重试 Anthropic 或 Google。控制台显示每个 Provider 的 Fallback 触发率，方便调优路由规则。
## 诚实的局限性

- **Hobby / 免费层模型覆盖有限**。免费 $5/月 Credit 只能在标记为「Free Tier eligible」的模型上使用 — 要用完整目录需要购买 Credits。
- **闭源，无法自托管**。与 LiteLLM（MIT）和 Helicone（Apache-2.0）不同，Vercel AI Gateway 仅作为 Vercel 管理的 SaaS 运行。如果你的合规制度要求自托管，这是一个硬性否决。
- **无 Guardrails**。与 Portkey（内置 Guardrails 支持内容审核、PII 脱敏、Prompt 注入防护）不同，Vercel AI Gateway 不提供安全原语。如果安全是首要需求，需要搭配一个专用的 Guardrails 层。
- **无 Prompt 版本管理或实验**。与 Helicone（带 HQL A/B 控制台的 Prompt 实验）不同，Vercel AI Gateway 专注于路由 + 可观测性，不覆盖 Prompt 迭代工作流。
- **附加费在大规模下累加**。Custom Reporting 查询 $5 / 1,000 次，对高基数控制台可能成为显著成本。本地缓存 reporting 查询结果以摊销成本。
- **锁定 Vercel 生态**。定价和免费层机制与 Vercel 平台绑定。如果你的团队不在 Vercel 上，对比会更偏向 OpenRouter 或 Portkey。
## 给 API 开发者的结论

Vercel AI Gateway 是 2026 年 Vercel 原生团队最强的 AI Gateway 选择。每月 $5 免费 Credit、Token 零加价（包括 BYOK）、以及 AI SDK v5/v6 一行代码集成，使其成为 Next.js / Vercel 部署应用最低摩擦的聚合器。如果你的团队不在 Vercel 上，对比就不那么有利 — OpenRouter 的免费模型选择、Cloudflare AI Gateway 的按请求加价、Portkey 精致的 SaaS 体验在不同维度上各有竞争力。
优先考虑「零加价 + 原生框架集成」的团队，Vercel AI Gateway 是首选。优先考虑「自托管 + 极致成本控制」的团队，LiteLLM（免费、MIT、开源）胜出。优先考虑「Guardrails + 非技术 API Key 管理的 App Portal」的团队，Portkey 是正确选择。Vercel AI Gateway 位于中间：零加价、原生 Vercel 适配，附加费结构在大规模下比 Cloudflare AI Gateway 便宜，但对高用量工作负载比 LiteLLM 贵。
若要深入对比六种 AI Gateway 选项在成本、性能、特性契合度上的差异，FreeModel 聚合层是有用的中立基准 — 它通过同一个 OpenAI 兼容接口路由，并暴露跨多家供应商的成本/延迟数据，不锁定你到任何一家。
## 常见问题

Vercel AI Gateway 用来做什么？ Vercel AI Gateway 是 Vercel 平台的一部分，作为 AI 路由层运行。它提供一个 API Key 访问 OpenAI、Anthropic、Google、xAI（Grok）、Mistral、Cohere、Groq 等数百个模型，内置可观测性、成本归因、模型 Fallback 和 BYOK 支持。它是 AI SDK v5/v6 生态的默认 AI 路由层，也是部署在 Vercel 上的 Next.js 应用的首选。

Vercel AI Gateway 2026 年多少钱？ Vercel AI Gateway 有两层。免费层每个 Vercel 团队账户附带每月 $5 的 AI Gateway Credits，限制在标记为「Free Tier eligible」的模型子集上，配较低的速率限制。付费层通过购买的 AI Gateway Credits 按量付费，解锁完整模型目录、支持零加价 BYOK、并提供 Custom Reporting、团队级 Provider 白名单、团队级 Zero Data Retention 的访问。附加费：Custom Reporting 写入 $0.075 / 1,000 次，Custom Reporting 查询 $5 / 1,000 次，团队级 Provider 白名单 $0.10 / 1,000 次成功请求，团队级 ZDR $0.10 / 1,000 次请求。

Vercel AI Gateway 在 Token 上有加价吗？ 没有。招牌定价承诺是「Token 零加价」— 包括自带密钥（BYOK）。Gateway 按 Provider 的官方列表价收取输入和输出 Token 费用，无 Vercel 加价。BYOK 客户也支付零加价。如果 BYOK 请求失败，Vercel 用系统凭证重试，回退用量按同样的零加价从你的 Credits 余额中扣除。

Vercel AI Gateway 与 OpenRouter 相比如何？ Vercel AI Gateway 和 OpenRouter 都提供 Token 零加价。Vercel 差异化在 Vercel 原生 AI SDK v5/v6 集成、BYOK 支持、$5/月免费 Credit（对比 OpenRouter 的免费模型选择）。OpenRouter 差异化在更广的 Provider 覆盖（数百家 Provider，包括长尾微调端点）、无平台锁定（任何框架可用）、更大的预构建集成社区。对于 Vercel 原生团队，Vercel AI Gateway 是低摩擦之选。对于非 Vercel 团队或需要特定长尾 Provider 的团队，OpenRouter 是默认选项。

Vercel AI Gateway 支持 BYOK（自带密钥）吗？ 支持。Vercel AI Gateway 在付费层支持目录中任何 Provider 的 BYOK。将你的 OpenAI / Anthropic / Google / xAI / Mistral / Cohere / Groq 密钥粘贴到 Vercel 控制台的 AI Gateway 板块；Vercel 静态加密它们并按零加价通过你的凭证路由请求。如果 BYOK 请求失败，Vercel 用系统凭证重试，回退用量计入你的 Credits 余额。

我可以从中国境内使用 Vercel AI Gateway 吗？ 可以，但有注意事项。Vercel AI Gateway 是跑在 Vercel 全球边缘网络上的托管 SaaS。从中国大陆境内，请求到达 Gateway 要走你现有的网络路径（通常经企业 VPN 或代理）。Gateway 不在中国境内运行。需要境内 Gateway 的团队，FreeModel 聚合层或自托管 LiteLLM 代理是更合适的选择。

## 参考来源

- Vercel, AI Gateway 定价，最后更新 2026-06-20（2026-07-20 核验）：vercel.com/docs/ai-gateway/pricing
- Vercel, AI Gateway 概览，2026-07-20 核验：vercel.com/docs/ai-gateway
- OpenRouter, 定价, 2026-07：openrouter.ai/models
- Cloudflare, AI Gateway 定价, 2026：developers.cloudflare.com/ai-gateway
- Portkey, 定价, 2026-07：portkey.ai/pricing
- LiteLLM, 仓库, 2026-07：github.com/BerriAI/litellm
- Helicone, 定价, 2026-07-18：helicone.ai/pricing
