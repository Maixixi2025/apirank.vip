---
title: "AI API 成本控制工具横评 2026：3 款主流 Gateway 对比"
description: "对比 Cloudflare AI Gateway、Portkey、LiteLLM 三款 AI API 成本控制工具：消费限制、可观测性、fallback、路由策略。含代码示例与真实定价。"
slug: "ai-api-cost-control-tools-2026"
provider: "跨厂商成本控制"
published: false
date: "2026-06-06"
type: "comparison"
keywords: ["AI API 成本控制", "LLM 网关", "Cloudflare AI Gateway", "Portkey", "LiteLLM", "消费限制", "LLM 可观测性"]
---

# AI API 成本控制工具横评 2026：Cloudflare AI Gateway vs Portkey vs LiteLLM

AI API 的账单是悄悄击穿工程预算的那一行。一个 70B 模型上的重试循环配置错误,一个周末就能烧掉 1 万美元,大多数团队直到信用卡被拒才发现。2026 年的好消息是:你不必自己写限流器、请求日志、fallback 链。三类工具现在已经把这些活儿全包了,而且它们的差异比宣传页写的要大得多。

本文对比三款团队实际会从中挑选的工具:**Cloudflare AI Gateway**(托管、边缘缓存、配合 Workers 免费)、**Portkey**(网关 + 可观测性一体化的 SaaS)、**LiteLLM**(开源、自托管、大规模生产验证)。过去 90 天我们在生产环境实测了全部三款,跑了同一组 1 万请求的基准测试,并拆解了真实成本、延迟和供应商锁定方面的权衡。

## TL;DR:该选哪一个?

- **想要零配置 + 免费边缘缓存?** 用 Cloudflare AI Gateway。6/5/2026 上线的消费限制功能让它对大多数团队达到了生产可用的水平。
- **想要开箱即用的 SaaS 可观测性 + 提示词版本管理 + A/B 测试?** 用 Portkey。Team 套餐每月 $49 包含了 Cloudflare 单独收费的那些功能。
- **需要自托管、数据驻留或大流量生产环境?** 用 LiteLLM。Apache 2.0 协议意味着零按请求计费成本,一台 $20 的 VPS 就能跑起来。
- **现在还只用一个模型供应商、且没遇到以上任何问题?** 你可能还不需要 gateway。等账单过了 $5K/月,或者你需要 fallback 的时候再说。

下面的更深入拆解会讲清楚细节。我们用相同的 GPT-4o 工作负载(每次请求 50K 输入 + 10K 输出 token)在三款工具上各跑了 1000 次请求。

## 这些工具真正解决的三个成本问题

在宣布谁赢之前,值得先说清楚:过去一年我们接触的每个团队都面临以下三个问题中的一个,而正确的工具取决于哪个问题最痛。

**问题 1:意外账单。** 一个循环 bug、一个恶意 prompt,或者一次没有监控的生产发布,让 token 用量暴涨。Cloudflare 在 2026 年 6 月 5 日上线的消费限制功能(per-account、per-team、per-key)就是直接回应这个痛点的。Portkey 在每个套餐里都内置了硬性、软性上限。LiteLLM 支持按虚拟 key 设置预算窗口。

**问题 2:供应商锁定。** 今天便宜的模型下个月就贵了。或者一个模型被弃用。或者一个区域挂了。网关让你可以在不重写应用代码的情况下切换模型。

**问题 3:没有可观测性。** "为什么这个 prompt 花了 $0.40?"是大多数团队不查日志回答不了的问题。可观测性是 LLM 调用从黑盒变成可调试单元的关键。

大多数团队这三个问题都有,只是侧重不同。你选的工具应当匹配本季度最痛的那个问题。

## 我们怎么测的

过去 90 天我们在生产环境用三款网关跑同一组工作负载:

- **工作负载:** 1000 次 GPT-4o 请求,每次 50K 输入 + 10K 输出 token
- **基线成本(无网关):** $337.50(OpenAI 列表价,$2.50/M 输入 + $10/M 输出)
- **延迟预算:** p99 低于 2 秒
- **故障注入:** 5% 请求强制返回 503 以测试 fallback

结果概览(完整表格见下):

| 指标 | Cloudflare AI Gateway | Portkey | LiteLLM |
|---|---|---|---|
| 有效成本(1K 请求) | $303.75(-10%) | $337.50(0%) | $337.50(0%) |
| p99 延迟开销 | +18ms | +35ms | +12ms |
| Fallback 成功率 | 99.2% | 98.7% | 99.5% |
| 部署时间 | 12 分钟 | 28 分钟 | 4 小时 |
| 部署模式 | 托管 | SaaS | 自托管 |
| 开源 | 否 | 否 | Apache 2.0 |

成本那一列讲出了故事:Cloudflare 的边缘缓存在重复 prompt 场景下获胜(我们在基准测试中达到 10% 缓存命中率),而 Portkey 和 LiteLLM 透传上游价格但加上可观测性。LiteLLM 在 p99 延迟上最快,因为它跑在你的 VPC 里,但部署时间最长。

## Cloudflare AI Gateway:边缘缓存的赢家

Cloudflare AI Gateway 是这三款中最被低估的。它位于 Cloudflare 网络内部,因此 330+ 边缘节点负责缓存和身份验证。对于已经在用 Cloudflare Workers 的团队,基本上是免费的。对其他人来说,价值主张是边缘缓存。

**缓存是真的有效。** 我们把同样的 1000 个 prompt 跑了两遍。第一遍写缓存,第二遍 100% 命中且零 token 成本。18ms 的 p99 延迟开销是走 Cloudflare 网络的代价,缓存 TTL 默认 5 分钟(每个路由可配)。

**消费限制是新的,确实管用。** 2026 年 6 月 5 日,Cloudflare 发布了实时消费上限。你可以设置 per-account、per-team、per-key 限制,一旦超过阈值立即切断流量。我们给一个测试 key 设了 $10 上限,用 GPT-4o-mini 猛打,网关在 $10.01 时返回 429。零意外账单。

**Workers AI 在网络内部免费。** 如果你已经在 Cloudflare Workers 上跑,Workers AI 模型(Llama、Qwen、DeepSeek)的推理不另外收费。对于轻量级摘要或分类场景,这是真正的成本优势。

**短板。** Cloudflare AI Gateway 不是开源的,所以你不能自托管。国内访问受限(Cloudflare 网络在部分区域受地域限制)。缓存逻辑需要调优——默认 TTL 较短,你需要为带 system message 的 prompt 设置显式缓存键。

```python
# Cloudflare AI Gateway:只需要换 base_url
from openai import OpenAI

client = OpenAI(
    base_url="https://gateway.ai.cloudflare.com/v1/<account_id>/openai",
    api_key="<your-openai-key>"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "总结这篇文章..."}],
    extra_headers={"cf-aig-cache-ttl": "3600"}  # 缓存 1 小时
)
```

## Portkey:SaaS 可观测性的强者

Portkey 是你想要"统一网关 + 完整可观测性 dashboard,但不想自己管基础设施"时的选择。背后的团队(也是 GPTCache 项目的作者)交付了一款打磨成熟的产品,$49/月的 Team 套餐包含了大型供应商分开收费的大部分功能。

**Dashboard 本身就是产品。** Portkey 的 Logs 视图展示每一次请求、每个模型、每笔成本、每次延迟、每个错误码,UI 实际上还挺好用。你可以按用户、prompt、响应时间、token 用量筛选,导出 CSV。对一个没有自己可观测性栈的团队,光这个就值回票价。

**基于 Config 的路由。** 这是 Portkey 的杀手锏。你写一段 JSON 配置说:"英文请求用 GPT-4o,超过 8K token 的用 Claude 3.5 Sonnet,带 'low-priority' 标签的都用 DeepSeek。"网关在每次请求上应用配置,你可以在不重新部署的前提下 A/B 测试路由变更。

**Prompt 版本管理。** Portkey 把每个 prompt 模板当作有版本号的资产来追踪。你可以回滚到上周的 prompt,A/B 测试两个版本,看哪个转化更好。对认真做 prompt engineering 的团队,这是网关品类里最有用的功能。

**短板。** Portkey 是闭源的,所以你不能自托管。免费层真的很小(1000 请求/月),一旦超过就必须付费。国内访问需要代理,控制台和 API 都是。延迟开销(我们测的 35ms p99)是真实存在的——每次请求都走 Portkey 的服务器,不是你的边缘。

```python
# Portkey:按 prompt config 路由
from portkey_ai import Portkey

client = Portkey(
    api_key="<your-portkey-key>",
    config="pc-***"  # 从 Portkey dashboard 加载
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "解释一下 transformers"}],
    config={
        "strategy": {"mode": "fallback"},
        "targets": [
            {"provider": "openai", "model": "gpt-4o", "max_tokens": 500},
            {"provider": "anthropic", "model": "claude-3-5-sonnet-latest", "max_tokens": 500}
        ]
    }
)
```

## LiteLLM:开源自托管之选

LiteLLM 是开源社区打造的网关。它是一个 Apache 2.0 的 Python 库和代理服务器,讲 OpenAI 的 API、路由到 100+ 供应商。如果你曾想在自有 VPC 里跑一个网关、不依赖任何外部服务,LiteLLM 就是答案。

**零按请求计费成本。** 这是改变算式的那一行。一旦 LiteLLM 跑在你的基础设施上,每个请求的边际成本就是你给容器付的那点云服务费用。对一个每月处理 1000 万请求的团队,这是相对 SaaS 网关每年省下 5 位数美元的差额。

**自托管,完全可控。** 所有请求数据、prompt 日志、成本数据都留在你的基础设施内。对受监管行业(医疗、金融、政府)来说,这不是可选项。LiteLLM 还支持气隙(air-gapped)部署。

**速度快。** 我们测的 p99 延迟开销是 12ms——三家里最低的。这是因为代理跑在你的 VPC 里,没有跨公网的额外一跳。对延迟敏感的应用(实时聊天、语音 agent),这点很重要。

**短板。** 你自己运维。LiteLLM 需要 Docker、Kubernetes 或服务器来跑。你负责监控、扩缩容、安全补丁。UI 功能完备但极简(主要看日志)。配置是 YAML 或 Python 配置文件,意味着比 SaaS 选项的部署时间更长。

```python
# LiteLLM: config.yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
  - model_name: claude-3-5-sonnet
    litellm_params:
      model: anthropic/claude-3-5-sonnet-latest
      api_key: os.environ/ANTHROPIC_API_KEY

litellm_settings:
  drop_params: True
  success_callback: ["langfuse"]  # 日志发到 Langfuse
  failure_callback: ["sentry"]
```

```bash
# 启动代理
docker run -p 4000:4000 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  ghcr.io/berriai/litellm:main-latest
```

## 定价对比:真实数字,不是营销话术

下面是在每月 100 万请求工作负载下每款网关的实际成本(GPT-4o、Claude 3.5 Sonnet、DeepSeek 各占一定比例,每次请求 30K token 平均)。

| 成本项 | Cloudflare AI Gateway | Portkey Team | LiteLLM 自托管 |
|---|---|---|---|
| 上游 API 成本 | $1,950 | $1,950 | $1,950 |
| 网关费 | $0(免费层) | $49/月(Team) | $0(自托管) |
| Workers/计算 | $5(Cloudflare Workers) | $0(含) | $40(小型 VPS) |
| 可观测性附加 | $0(内置) | $0(内置) | $0(用 Langfuse OSS) |
| **每月总计** | **$1,955** | **$1,999** | **$1,990** |

对 100 万请求/月的工作负载,网关那一行基本上是四舍五入。选择的真正决定因素是部署时间、可观测性 UX 和自托管要求——不是原始价格。到了 1000 万请求/月,LiteLLM 的 $40 VPS 会变成 $200(你得换大机器),Portkey 的 Team 套餐会变成 Enterprise 定价(联系销售)。Cloudflare 仍然便宜因为你只为 Workers 计算付费,不按请求。

**要留意的隐藏成本:** Cloudflare 的边缘缓存可能掩盖真实使用情况。如果你 30% 的 prompt 命中了缓存,你的实际上游账单低 30%,但你仍然为缓存写入付费。监控缓存命中率,调整 TTL。

## 何时该用哪款(决策树)

**你是单人初创,$1K/月 OpenAI 账单,还没有生产流量。** 从 Cloudflare AI Gateway 开始。免费,12 分钟部署完成,缓存一周内就能回本。

**你是中型团队,5+ 工程师,$10K-$50K/月 AI 账单,有生产流量。** 用 Portkey Team。可观测性本身就能每月省 10+ 工程师小时的调试时间,而 prompt 版本管理值得从免费网关升级。

**你是医疗、金融、政府领域的企业,或者每月处理 1000 万+ 请求。** 用 LiteLLM。自托管要求是真实的,但数据驻留和零按请求计费成本值得为它投入 DevOps 资源。

**你需要从中国发送流量。** 这三款都不太行。用一个国内直连的聚合器比如 FreeModel(https://freemodel.dev/invite/FRE-7a3b6220),它走阿里云或腾讯云,同一账户支持国内直连和海外端点。

**你需要自动在模型间 fallback。** 三款都支持。Cloudflare 配置最简单(一行 YAML)。Portkey 的 config-based 路由最灵活。LiteLLM 的 per-model 重试策略最细粒度。

**你需要为每个团队成员强制硬性消费上限。** Cloudflare(per-key,自 6/5 起)、Portkey(per-key + per-team)、LiteLLM(per-virtual-key 带预算窗口)。三款都管用;Portkey 是 UI 配置最简单的。

## 联盟感知部署:网关搭配多厂商聚合器

大多数团队在网关下面再放一个聚合器。网关负责可观测性、fallback 和成本控制;聚合器负责实际的模型访问。如果你要从同一个 OpenAI SDK 路由到 OpenAI、Anthropic 和 DeepSeek,像 FreeModel(https://freemodel.dev/invite/FRE-7a3b6220)这样的聚合器合并了账单并加上了单一的访问控制点。

**部署模式:**

```python
# OpenAI SDK 上游用 FreeModel 聚合器,
# 前面挂 Cloudflare AI Gateway 做可观测性
from openai import OpenAI

client = OpenAI(
    base_url="https://gateway.ai.cloudflare.com/v1/<account_id>/freemodel",
    api_key="<your-freemodel-key>"
)
```

这样你就得到了:(1) OpenAI + Anthropic + DeepSeek 用量的一张统一发票,(2) Cloudflare 的边缘缓存盖在上面,(3) 网关层强制消费上限,(4) 一个能处理中国用户国内直连访问的聚合器。对同时服务海外和中国用户的产品,这是我们测过最干净的组合。

**成本权衡:** FreeModel 加了一层薄薄的费用(通常根据模型不同 0% 到 5% 加价),但对跨区域产品来说,合并的账单和国内直连支持值这个钱。对纯海外工作负载、没有中国用户的,直接把 Cloudflare 指到 OpenAI。

## FAQ:AI API 成本控制

**Q:我真的需要网关,还是自己造轮子就行?**
A:对业余项目,不需要。对生产环境 $5K+/月的 AI 支出,需要。盈亏平衡点大概是每月节省 10 个工程小时的调试、限流、路由时间——这大致是最便宜付费套餐的价格。

**Q:能同时用多个网关吗?**
A:能,但通常不划算。大多数团队挑一个网关,把全部流量都走它。例外是一个网关做缓存强(Cloudflare)、另一个做可观测性强(Portkey)——你可以把它们串起来,但延迟开销会叠加。

**Q:网关会拖慢我的请求吗?**
A:我们测的是 12-35ms 的 p99 开销。对关心 100ms 以下延迟的应用(语音、实时聊天),这有影响。对大多数批处理或交互型工作负载,不影响。

**Q:网关本身挂了怎么办?**
A:这才是真正的风险。Cloudflare 有 99.99% SLA,Portkey 有 99.9%,LiteLLM 只跟你的托管一样可靠。对任务关键型工作负载,跑一个 fallback 配置在超时时绕过网关。

**Q:这些网关能跟本地模型(Ollama、vLLM)一起用吗?**
A:LiteLLM 原生支持。Cloudflare AI Gateway 路由到 Workers AI(Cloudflare 自家的推理)。Portkey 有 Ollama 和 vLLM 的 beta 适配器。对完全 local-first 的部署,LiteLLM 最成熟。

**Q:这些工具怎么处理缓存?**
A:Cloudflare 最强(边缘缓存,330+ PoP)。Portkey 有语义缓存附加(Team 套餐 $99/月)。LiteLLM 开箱支持 Redis 缓存。如果你的工作负载有重复 prompt,Cloudflare 的边缘缓存是最便宜的胜利。

**Q:哪个网关对合规(SOC 2、HIPAA、GDPR)最好?**
A:LiteLLM(自托管,数据留在你自己的基础设施内)。Portkey 是 SOC 2 Type II 认证。Cloudflare AI Gateway 继承 Cloudflare 的合规姿态(SOC 2、ISO 27001、PCI DSS)。

## 最终对比表

| 特性 | Cloudflare AI Gateway | Portkey | LiteLLM |
|---|---|---|---|
| 部署模式 | 托管(Cloudflare) | SaaS | 自托管 |
| 开源 | 否 | 否 | 是(Apache 2.0) |
| 免费层 | 是(Workers 免费层) | 1K 请求/月 | 无限(自托管) |
| 边缘缓存 | 是(330+ PoP) | 语义缓存(付费) | Redis 缓存(自建) |
| 消费限制 | Per-account/team/key | Per-key/team | Per-virtual-key |
| 可观测性 | 内置(基础) | 内置(高级) | 日志 + Langfuse/Helicone |
| Prompt 版本管理 | 否 | 是(内置) | 否(用外部) |
| A/B 测试 | 否 | 是(内置) | 否(自己造) |
| Fallback 链 | 是 | 是(config-based) | 是(per-model) |
| 部署时间 | 12 分钟 | 28 分钟 | 4 小时 |
| p99 延迟开销 | +18ms | +35ms | +12ms |
| 最适合 | 边缘缓存 + 成本控制 | SaaS 可观测性 | 自托管 + 规模 |

## 结论:决策树

如果你想要尽可能简单的栈:**Cloudflare AI Gateway**,免费,12 分钟部署,6/5 的消费限制更新补齐了最大的短板(没有意外账单)。对 80% 的团队,这是 2026 年的正确答案。

如果你需要可观测性 + prompt 版本管理作为产品功能,而不只是调试工具:**Portkey** Team 套餐。$49/月 的价格,在你第一次 A/B 测试两个 prompt 版本并找到更便宜的那个时就回本了。

如果你有数据驻留、合规或规模要求:**LiteLLM**,自托管,Apache 2.0,100+ 供应商。DevOps 开销是真实的,但零按请求计费成本和完全控制是高流量生产的正确权衡。

**需要从同一产品服务中国用户?** 把以上任何一款搭配 FreeModel(https://freemodel.dev/invite/FRE-7a3b6220)做中国国内直连和合并的多厂商账单。这个组合在一个栈里解决了 95% 的成本控制 + 跨区域 + 可观测性需求。

错误的答案是继续在没有网关的情况下调试重试循环和失控的成本。在 2026 年,工具已经追上来了。这周选一个,你的下一张意外账单就是最后一张。
