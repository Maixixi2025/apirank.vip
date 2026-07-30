---
title: "OpenRouter 数据驻留 2026：欧盟区域路由 + ZDR 完全指南"
description: "OpenRouter Sovereign AI 全栈解读：per-request provider 对象、ZDR 开关、企业版 eu.openrouter.ai 端点。GDPR vs PIPL 真实覆盖范围。"
slug: "openrouter-data-residency-2026"
provider: "openrouter"
published: false
date: "2026-06-24"
type: "analysis"
---

# OpenRouter 数据驻留 2026：欧盟区域路由 + ZDR 完全指南

2026 年 6 月 22 日，OpenRouter 发布了博客《*How to Enforce AI Data Residency Without Building Local Infrastructure*》。这篇博客把已有工具包打包成新品牌"**Sovereign AI**"，并新增一个运营原语：企业版专属 `eu.openrouter.ai` 基础 URL，把解密和处理硬锁定在欧盟境内。

本文拆解整个堆栈——从任何账户都能用的 per-request `provider` 对象，到企业版 EU 端点目前承载的 26 个模型。你会看到真实代码、6 月 24 日实测的模型清单，以及与 Cloudflare AI Gateway、LiteLLM、Portkey 的对比。

简短结论：四款方案里，**OpenRouter 是唯一提供单一托管区域 URL 的**。其他三家都需要你自己在 provider 层做区域钉选。

## "Sovereign AI" 的真实含义

OpenRouter 并没有发布单一命名的功能。2026 年 6 月这套组合拳把三个已有原语挂在新品牌名下：

1. **Per-request `provider` 对象**——在请求体里过滤并钉选上游 provider
2. **Zero Data Retention（ZDR）开关**——账户级、按模型组、按 API key 三层 guardrail
3. **`eu.openrouter.ai` 基础 URL**——企业版专属，欧盟境内硬管辖（解密 + 处理）

前两层任何账户都能用。第三层需要企业合同（销售联系，无 SKU）。三者组合可以覆盖 GDPR、欧盟 AI Act 执法、Deloitte 调查中的"country of origin"采购偏好——但**不覆盖中国 PIPL/DSL 数据本地化**。没有中国区，EU 端点没有中国 provider，也没有公开的 CN 端点。

运行机制：OpenRouter 的驻留控制在**路由层**执行。它决定调哪个上游 provider，然后调用该 provider 的现有端点。所以这些控制对任何有区域端点的 provider 都生效——Anthropic、OpenAI、Google、Amazon Bedrock 以及 20+ 其他。

## `provider` 对象：per-request 路由 DSL

最实用的控制也是最简单的。任何 OpenRouter 账户都能在 chat completions 请求体里加 `provider` 对象来过滤和钉选上游路由。

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENR...EY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4.6",
    "messages": [{"role": "user", "content": "总结这份合规报告。"}],
    "provider": {
      "order": ["anthropic", "amazon-bedrock"],
      "allow_fallbacks": false,
      "data_collection": "deny",
      "zdr": true
    }
  }'
```

对驻留场景最重要的四个字段：

| 字段 | 类型 | 默认值 | 驻留效果 |
|---|---|---|---|
| `order` | string[] | – | 按这个优先级顺序尝试 provider |
| `only` | string[] | – | 只允许这些 provider slug（硬限制） |
| `data_collection` | `"allow"` / `"deny"` | `"allow"` | `"deny"` 排除存储或训练输入的 provider |
| `zdr` | boolean | – | 仅使用 Zero-Data-Retention 端点 |

另外两个字段对合规审计有用：`allow_fallbacks: false` 在指定 provider 不可用时直接报错，而不是悄悄 fallback 到非 EU 端点；响应头里的 **Router Metadata** 记录了实际处理请求的 provider，这是 SOC 2 / ISO 27001 控制评审里的关键证据。

常见模式：钉到法兰克福 Bedrock 托管的模型，满足 EU 合规：

```python
import os
import requests

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "anthropic/claude-sonnet-4.6",
        "messages": [{"role": "user", "content": "从这个合同里提取供应商名称。"}],
        "provider": {
            "order": ["amazon-bedrock"],
            "only": ["amazon-bedrock"],
            "data_collection": "deny",
            "zdr": True,
            "allow_fallbacks": False,
        },
    },
    timeout=30,
)
data = response.json()
# 审计追踪：这个请求实际由哪个 provider 处理？
provider_used = response.headers.get("x-openrouter-provider")
print(f"Provider: {provider_used}")
```

`only` + `allow_fallbacks: false` 组合最安全。没有它，Bedrock 一次短暂的故障会悄悄 fallback 到非 EU provider。

## ZDR：按模型组和按 key

ZDR 是第二层。它是 `/settings/privacy` 里的**按模型组**开关：

- **Anthropic**——直连端点被移除；Amazon Bedrock 和 Google Vertex 保留
- **OpenAI**——直连端点被移除；Azure 保留
- **Google**——AI Studio 被移除；Vertex 保留
- **Non-frontier**——不归入以上桶的 provider

行为一致：当某组开启 ZDR，OpenRouter 会过滤掉该组中所有保留数据的 provider。对合规采购方来说很直接——为你可能用的每个模型组都开 ZDR，就把最严重的备选 pool 全部剔除了。

团队级强制靠 OpenRouter 的 **guardrails**——按 API key 的对象，可以按组强制 ZDR：

```typescript
const openRouter = new OpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY!,
});

await openRouter.guardrails.create({
  api_key_id: '<KEY_ID>',
  enforce_zdr_anthropic: true,
  enforce_zdr_openai: true,
  enforce_zdr_google: true,
  enforce_zdr_other: true,
});
```

它们和 per-request 标志是**或**关系——你只能加强，不能削弱。这是正确的语义：如果 key 被锁死，开发者不可能把合规工作负载意外路由到非 ZDR provider。

## `eu.openrouter.ai` 基础 URL：硬欧盟管辖

这是新东西。企业账户可以把基础 URL 从 `https://openrouter.ai/api/v1` 切到 `https://eu.openrouter.ai/api/v1`，请求在 EU 境内解密、处理，再转发到 EU 区域上游 provider。

集成上 SDK 改一行：

```typescript
import { OpenRouter } from '@openrouter/sdk';

const openRouter = new OpenRouter({
  apiKey: '<OPENROUTER_API_KEY>',
  serverURL: 'https://eu.openrouter.ai/api/v1',  // <-- 唯一改动
});

const completion = await openRouter.chat.send({
  model: 'meta-llama/llama-3.3-70b-instruct',
  messages: [{ role: 'user', content: 'Hello' }],
  stream: false,
});
```

或者原生 `fetch`：

```typescript
const res = await fetch('https://eu.openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <OPENROUTER_API_KEY>',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'anthropic/claude-sonnet-4.6',
    messages: [{ role: 'user', content: 'GDPR 审计摘要' }],
  }),
});
```

想看 EU 端点服务哪些模型，直接调它的模型列表：

```bash
curl https://eu.openrouter.ai/api/v1/models | jq '.data | length'
# 26 (截至 2026-06-24)
```

26 个模型大致分布：8 个 Anthropic（Claude Opus 4.5–4.8、Sonnet 4–4.6、Haiku 4.5），11 个 OpenAI（GPT-4o-mini、GPT-4.1 系列、GPT-5 系列、GPT-5.5、GPT-OSS 20B/120B），3 个 Google（Gemini 2.5 Pro/Flash/Flash-Lite），4 个 Amazon（Nova Micro/Lite/Pro 和 Nova 2 Lite）。这 26 个是 OpenRouter 主目录 338 个模型里，能通过 EU 区域上游 provider 路由的子集。

一个值得指出的细节：OpenRouter 博客把 **Mistral** 框定成可以用 `provider.only: ["mistralai"]` 钉选的"EU 管辖锚点"。这在主端点上是真的——Mistral 在主目录里有 20+ 模型。但 Mistral **不在** `eu.openrouter.ai` 端点列表上。如果你要硬 EU 管辖保证，单靠 Mistral 不够——你需要你用的模型走 EU 区域上游（比如通过法兰克福 Bedrock 的 Anthropic，或通过 Azure Sweden 的 OpenAI）。

## 定价：0% 标价加价，5.5% 平台费

公开材料里没有驻留附加费。定价模型和标准 OpenRouter 一样：

- **0% 标价加价**（在 provider 价基础上）
- **5.5% 平台费**（在充值上），**最低 $0.80**
- **5%** 通过 **BYOK（Bring Your Own Key）**
- **每月前 100 万次请求免费**（BYOK）
- **失败请求不计费**
- **20+ 免费模型**用于评估

EU 区域端点本身被企业销售联系门控（`https://openrouter.ai/enterprise/form`），无 SKU。对严肃的合规采购方，准备好谈企业合同，而不是按需充信用。

对比一下：典型 EU 钉选工作负载，BYOK 模式下每月 100 万请求大约是上游 provider 标价之上的 5%。"无加价 + 5% 平台费"框架相比直接对接有竞争力——直接对接 Anthropic、OpenAI、Google 都要按标价付，但你需要接三个独立账户、三套独立 SSO 集成、三套独立供应商风险评审。

## 替代方案横评

合规团队通常评估的四种方案：

| 方案 | 驻留机制 | 配置方式 | 定价 | 注意事项 |
|---|---|---|---|---|
| **OpenRouter `provider` 对象** | 按数据策略 / ZDR 过滤 provider | 请求体里 `provider.only`、`provider.zdr`、`provider.data_collection` | 包含在 5.5% 平台费里 | "区域"= provider 总部所在国；不是硬管辖 |
| **OpenRouter `eu.openrouter.ai`** | 硬欧盟管辖 | 基础 URL 切到 `https://eu.openrouter.ai/api/v1` | 企业版，联系销售 | 仅 EU；26 个模型；Mistral 不在 EU 列表 |
| **Cloudflare AI Gateway** | 无原生区域路由 | 仅缓存、限速、重试/fallback | 免费层 + Workers 付费套餐 | 网关本身无驻留原语 |
| **LiteLLM（自托管）** | 你的网络、你的管辖 | `model_list` 上游用 `openrouter/...` 或直连 provider key | 免费开源；基础设施 ~$200–$500/月 | OSS 版无 SOC 2 / ISO 27001 / HIPAA 认证 |
| **Portkey** | 在你的 provider key 上做控制平面 | BYOK + guardrails + PII 脱敏 | $49/月 Production；HIPAA 走 Enterprise | 2026 年被 Palo Alto Networks 收购；Enterprise 提供 HIPAA + BAA |
| **Provider 区域钉选端点** | Provider 自有区域端点 | Vertex 的 `region: eu`、Azure EU 区域、AWS Bedrock `eu-central-1` | Provider 标价 | 每个 provider 对"区域"定义不同 |

关键结论：**四款托管方案里 OpenRouter 是唯一暴露单一托管 EU 端点的**。Cloudflare AI Gateway（OpenRouter 底层基础设施）截至 2026-04-20 文档更新，**没有**把驻留作为一级控制——只有缓存、限速、重试/fallback。LiteLLM 因为自托管给你完整主权，但你需要自己拿 SOC 2 / ISO 27001 / HIPAA 认证。Portkey 在 Enterprise 提供 HIPAA + BAA，但没有托管 EU 端点。

需要医疗 BAA，答案是 Portkey Enterprise 加上你自己的 provider BAA（Azure OpenAI、带 BAA 的 AWS Bedrock）。需要托管 EU 端点但不需要 HIPAA，OpenRouter 是最干净的答案。

## 合规场景映射

| 法规 | OpenRouter 能做到的 | 缺失的 |
|---|---|---|
| **GDPR（第 44–50 条跨境传输）** | `data_collection: "deny"` + `zdr: true` 做 Schrems-II 式数据最小化；`eu.openrouter.ai` 满足硬 EU 管辖 | 第 30 条处理记录必须在控制者层级，不在 API 层 |
| **欧盟 AI Act（2026 执法）** | 同样原语；Sovereign AI 文档明文点名 | 风险分级文档是部署者责任（第 17 条） |
| **Deloitte "country of origin" 采购** | 77% 受访领导者（3235 人）把供应商原产国纳入评估 | 供应商风险问卷仍需逐 provider 填写 |
| **金融服务（PCI-DSS、FINRA、OCC）** | 按模型组 ZDR 开关、按 API key guardrail 职责分离、Router Metadata 头做审计追踪 | SOC 2 Type 2 报告在 `https://trust.openrouter.ai` 对多数第三方风险团队够用，但非全部 |
| **医疗（HIPAA——美国侧）** | 部分：ZDR + `data_collection: "deny"` + EU/US 端点 | OpenRouter **没有** HIPAA 认证；BAA 必须在 provider 层（Azure OpenAI、带 BAA 的 AWS Bedrock） |
| **中国数据本地化（PIPL、DSL）** | **无覆盖** | 无中国区、EU 列表无中国 provider、无公开 CN 端点。这是真实的缺口。 |
| **国防 / 气隙环境** | 不是正确答案 | "基础设施框架适合政府、国防承包商和气隙环境"——这种场景下只有自托管 LiteLLM 可选。 |

中国数据本地化缺口要重复一遍。如果你服务中国用户群且需要 PIPL 合规，OpenRouter 不是答案。你需要中国区域上游（阿里通义千问、DeepSeek、智谱 GLM、月之暗面 Kimi 等），加上你自己的数据本地化控制。这是 OpenRouter 现有能力覆盖不到的范围。

## 30 行落地实现

汇总一个典型 EU 合规工作负载的完整实现：

```python
# requirements: requests, python-dotenv
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 1. 如果合同包含 EU 端点，使用 EU 端点
# 2. 钉选单一 EU 区域上游
# 3. 强制 ZDR + data_collection: deny
# 4. 关闭 fallback，这样短暂故障会直接报错
# 5. 抓取 router metadata 进审计日志

def compliance_chat(prompt: str, model: str = "anthropic/claude-sonnet-4.6") -> dict:
    base = os.environ.get("OPENROUTER_BASE", "https://openrouter.ai/api/v1")
    # 切到 EU 端点获得硬管辖（仅企业版）
    if os.environ.get("EU_RESIDENCY") == "true":
        base = "https://eu.openrouter.ai/api/v1"

    response = requests.post(
        f"{base}/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "provider": {
                "order": ["amazon-bedrock"],
                "only": ["amazon-bedrock"],
                "data_collection": "deny",
                "zdr": True,
                "allow_fallbacks": False,
            },
        },
        timeout=30,
    )
    response.raise_for_status()

    # 审计追踪
    return {
        "provider": response.headers.get("x-openrouter-provider"),
        "content": response.json()["choices"][0]["message"]["content"],
    }


if __name__ == "__main__":
    result = compliance_chat("把这份供应商风险报告总结成 3 点。")
    print(f"由以下 provider 处理: {result['provider']}")
    print(result["content"])
```

两个值得记住的模式：`EU_RESIDENCY=true` 环境变量模式让你在主端点和 EU 端点之间切换不动代码；per-request `provider` 对象和账户级 ZDR 设置是或关系——最严格的保证需要两者都开。

## FAQ

**Q：`eu.openrouter.ai` 端点会增加延迟吗？**
A：端点本身不会。你的请求从 EU 基础设施解密并路由，上游 provider 也是区域内调用。端到端延迟和主端点上的同模型相当。

**Q：能针对同一模型钉选特定上游（比如 Azure Sweden vs AWS 法兰克福）吗？**
A：间接可以，通过 `provider.order` 加 `allow_fallbacks: false`。Azure 的 provider slug 通常是 `azure`，AWS Bedrock 是 `amazon-bedrock`；OpenRouter 按 order 指定的顺序路由。Provider 内的直接区域钉选（比如强制 AWS 法兰克福而不是 AWS 都柏林）OpenRouter 没暴露——那必须在 provider 侧配置。

**Q：EU 端点有免费层吗？**
A：EU 端点企业门控。没有公开免费 SKU；你需要联系销售获取访问。

**Q：ZDR 覆盖微调数据吗？**
A：不覆盖。ZDR 只覆盖推理。微调是独立工作流，使用 provider 专用端点，目前不通过 OpenRouter 的驻留控制暴露。

**Q：OpenRouter 怎么处理新的欧盟 AI Act 要求？**
A：Sovereign AI 文档明文点名欧盟 AI Act 合规。`data_collection: "deny"`、ZDR 和 `eu.openrouter.ai` 端点的组合被定位为运营原语。风险分级和合格评定仍是部署者在第 17 条下的责任。

**Q：ZDR 和 `data_collection: "deny"` 有什么区别？**
A：ZDR 指 provider 不在静态存储中保留 prompt 或 response。`data_collection: "deny"` 指 provider 不把数据用于训练未来模型。一个 provider 可以满足一个而不满足另一个——比如一个 provider 可能保留日志 30 天（违反 ZDR）但永远不在输入上训练（满足 `data_collection: "deny"`）。最严格的保证是两个都开。

## 结论

OpenRouter 2026 年 6 月这套组合拳最好这样理解：**一篇博客（数据驻留叙事）+ 一个新的企业版 EU 端点，把已有工具包硬化**。工具包本身是成熟的——`provider` 对象、ZDR 开关、guardrails 几个月前就在那里。变化的是你现在可以指向一个托管 URL，告诉合规团队"所有推理都在 EU 发生"。

如果你做 EU 产品且不需要 BAA，OpenRouter 是今天最干净的托管选项。需要 HIPAA，Portkey Enterprise 加上 provider BAA。需要 PIPL 数据本地化，需要中国区 provider 栈——OpenRouter 覆盖不到。需要完整主权，唯一路径是自托管 LiteLLM。

有一件事不要做：把 OpenRouter 的"Sovereign AI"品牌名当作合规工件。它是营销标签。真正的控制是 `provider` 对象、ZDR 开关和 `eu.openrouter.ai` 端点——你需要把三者都正确配置，才能给你审计师承诺的保证。

---

如果你想把多 provider 流量（OpenAI、Anthropic、Google）通过一个 OpenAI 兼容端点整合，自带 ZDR 和 provider 路由，**FreeModel**（`https://freemodel.dev/invite/FRE-7a3b6220`）是一个中国直连聚合器，复制了 OpenRouter 模式，底层跑 DeepSeek、Qwen、GLM、Kimi。它的企业版用同样的 `provider` 对象形状，是需要同时接入 EU/美/中国路由的团队最接近的国内等价方案。
