---
title: "GitHub Models 2026 测评：免费 GPT-4o / Claude / Llama 凭 GitHub 账户即用"
description: "GitHub Models API 完整测评：50+ 模型 (GPT-4o、Claude 3.5 Sonnet、Llama 3.1 405B、o1-preview) 凭现有 GitHub 账户登录、免费日额度、OpenAI 兼容 chat completions 接口、GitHub Actions/Codespaces 原生集成。深度解析定价、限速与 BYOK 升级路径。"
slug: "github-models-api-review"
provider: "github-models"
published: true
date: "2026-06-25"
type: "review"
---

# GitHub Models 2026 测评：免费 GPT-4o / Claude / Llama 凭 GitHub 账户即用

## 引言：2026 年的 GitHub Models 是什么

GitHub Models 是 GitHub 的 AI 推理服务，给每个 GitHub 账户（含免费个人账户）每天若干次对 50+ 生产 LLM 的推理调用额度。截至 2026 年 6 月，目录包括 OpenAI 的 GPT-4o 和 o1-preview / o1-mini 推理模型、Anthropic 的 Claude 3.5 Sonnet 和 Claude 3.7 Sonnet、Meta 的 Llama 3.1 405B Instruct 和 Llama 3.2 90B Vision、Mistral Large 2、Microsoft Phi-3.5 MoE、DeepSeek-V3、Cohere Command R+ 和 AI21 的 Jamba 1.5 Large。API 是 OpenAI chat completions 端点的严格超集 — 同样的 JSON 结构、同样的流式协议、同样的 function calling `tools` 参数。用过 OpenAI Python SDK 的开发者只需改 `base_url` 和 `Authorization` header 就能切到 GitHub Models。无需学习新 SDK、无需内化并行概念。

关于 GitHub Models 最让人意外的不是模型目录 — 而是**接入路径**。无需信用卡、无需申请访问、无需等待配额审批。凭 GitHub 账户登录，在 `github.com/marketplace/models` 打开 Playground 即可发送 prompt。免费层速率限制紧（每天 GPT-4o 50 次、o1-preview 10 次、Claude 3.5 Sonnet 100 次、Llama 3.1 405B 150 次）但这些都是真实生产模型上的真实生产配额 — 不是带水印的 demo、不是 7 天试用、不是"发邮件给我们，我们再联系你"。对工程师快速原型、评估选哪个模型、构建需要 LLM 判断的 GitHub Actions 工作流，GitHub Models 是 2026 年从想法到运行代码最快的路径。

本文从 2026 年中评估 API 的工程师视角深度测评 GitHub Models：免费层实际能交付什么、OpenAI 兼容层在生产中的表现、限速在哪里咬人、GitHub Actions 和 Codespaces 集成与裸 API 调用的差异、BYOK 升级到付费模型的路径，以及与 OpenRouter、Hugging Face Inference、厂商直连 API 的对比。

## 免费层可用模型（2026 年 6 月）

GitHub Models 目录会轮换，但 2026 年 6 月的核心阵容覆盖以下系列：

| 系列 | 免费层模型 | 日配额（每 GitHub 账户） |
|---|---|---|
| OpenAI | GPT-4o, GPT-4o mini, o1-preview, o1-mini | 50 / 200 / 10 / 50 |
| Anthropic | Claude 3.5 Sonnet, Claude 3.7 Sonnet | 100 / 50 |
| Meta | Llama 3.1 405B Instruct, Llama 3.2 90B Vision | 150 / 100 |
| Mistral | Mistral Large 2 | 75 |
| Microsoft | Phi-3.5 MoE instruct | 200 |
| DeepSeek | DeepSeek-V3（托管变体） | 75 |
| Cohere | Command R+ | 75 |
| AI21 | Jamba 1.5 Large | 75 |

配额是按账户计算，不按"每模型每天"计算 — 同一天内不能用 GPT-4o 调用次数换额外的 Claude 调用。如果你中午之前烧完了每天 10 次 o1-preview 调用，要等到 UTC 午夜重置。对评估生产功能该用哪个模型的工程师，免费层足够跑一个有意义的基准（50 次 GPT-4o 调用覆盖 5 个 prompt × 10 次改写，或 50 次单次补全）。对每次构建需要做少量 LLM 判断的 CI 工作流，100 次/天的 Claude 3.5 Sonnet 足够应付大多数合理用例。

目录由 GitHub 策展。新模型通常在上游厂商宣布 1-2 周后才出现 — GitHub 会在模型上线前完成安全审查、SLA 谈判和集成工作。截至 2026 年 6 月，被请求最多但缺失的模型是 Anthropic 的 Claude Opus 4.5（GitHub 列了 Claude 3.7 Sonnet，最新的 Sonnet，但没有 Opus 档位）。被请求最多但缺失的前沿是 OpenAI 的 GPT-5.5 系列（GitHub 有 GPT-4o 和 o1，但没有 GPT-5.5 或 GPT-5.5 Instant 档位）。

## 定价：免费层 vs BYOK vs GitHub 托管付费

GitHub Models 有三种计费模式，差异很重要：

**免费层。** 无需信用卡。日配额如上所列。模型由 GitHub 从 GitHub 管理的推理基础设施提供（实际是 Azure，但路由和配额强制由 GitHub 执行）。免费层是真正的免费 — 没有隐藏计量使用、没有"如果你不小心超出配额就扣费"（你会收到 429 响应然后停）。

**BYOK（Bring Your Own Key）。** 对 GitHub Copilot Business 和 Enterprise 客户开放。你把你自己的 Azure OpenAI 资源或你自己的 OpenAI 组织接到 GitHub Models，推理在你自己现有账单上跑。免费层配额不适用 — 你获得你 Azure/OpenAI 账户的速率限制。优点是统一账单（GitHub 一张发票，而不是分开的 Azure + OpenAI 账单）和统一访问治理（一个地方管理哪些员工能调用哪些模型）。缺点是你在为推理支付零售价，而你可以直接调用。

**GitHub 托管付费。** 2026 年初新增。在 GitHub 账户加支付方式，直接向 GitHub 支付免费配额以上的推理费用。价格大致匹配上游厂商标价（GPT-4o input $2.50/M，output $10/M，与 OpenAI 公布价格一致） — GitHub 似乎没有给推理加价。优点是统一账单无需单独的 Azure 资源。缺点是此模式尚未在所有区域可用，且模型选择比免费层窄。

对 2026 年中的大多数个人开发者和小团队，免费层 + BYOK（如果你已经有 Copilot Business）覆盖一切。纯 GitHub 托管付费模式是一个面向未来的特性，而不是当前的最佳选择 — 如果你为推理支付零售价，那还不如直接调用上游厂商，跳过 GitHub Models 的路由层。

## API 形态：OpenAI Chat Completions + GitHub 认证

GitHub Models API 是 OpenAI 的 `/v1/chat/completions` 端点，只是把 OpenAI API key 换成 GitHub 认证。Chat 端点是 `https://models.github.ai/inference/chat/completions`，embeddings 端点是 `https://models.github.ai/inference/embeddings`（模型选择有限 — 大多数 embedding 工作负载仍然直接走 OpenAI / Voyage / Cohere）。

认证用 GitHub 个人访问令牌（PAT），scope 是 `models:read`。标准 OpenAI Python SDK 通过设置 `base_url` 为 GitHub Models 端点和 `api_key` 为 PAT 即可工作。Streaming、function calling、system messages、JSON mode 全部无需修改即可工作。JavaScript、Go、Java、Rust 的 OpenAI 兼容 SDK 同理。

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key="ghp_你的_GITHUB_PAT_带_MODELS_READ_scope",
)

response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[
        {"role": "system", "content": "你是 Python 项目的 code reviewer。"},
        {"role": "user", "content": "Review 这个 PR diff，列出 top 3 问题。"}
    ],
    temperature=0.2,
)

print(response.choices[0].message.content)
```

模型名使用 `vendor/model` 前缀 — `openai/gpt-4o`、`anthropic/claude-3.5-sonnet`、`meta/llama-3.1-405b-instruct`。这比上游厂商的裸模型名（`gpt-4o`、`claude-3-5-sonnet-latest`）更啰嗦，但当你在同一个应用里混用厂商时，它明确指出了你调用的是哪家厂商的模型。

## GitHub Actions 和 Codespaces 集成

与 GitHub Actions 的原生集成是让 GitHub Models 与 OpenRouter 或任何其他 aggregator 区分开来的单一特性。Workflow YAML 可以直接调用 GitHub Models 而无需存储 secret：

```yaml
name: AI code review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Get LLM review
        uses: actions/ai-inference@v1
        with:
          model: openai/gpt-4o
          system-prompt: "你是资深 code reviewer。"
          prompt-file: ./diff.patch
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

`actions/ai-inference` action 是一个 GitHub 一方 action，包装了 GitHub Models API，自动使用工作流的 `GITHUB_TOKEN` — 无 PAT、无 secret 管理、无需配置 Azure 资源。对于已经在 GitHub Actions 上运行的团队，这把"给工作流加 LLM 判断"的运维开销从一个多日项目（配置 Azure OpenAI、存 secrets、写推理代码）压缩成一个 YAML 块。

同样的模式适用于 GitHub Codespaces。Codespace 可以无需任何额外设置地调用 GitHub Models — Codespace 内置的 GitHub 认证就够了。这让 Codespaces 成为 AI 辅助开发教程、demo 和 onboarding 流的特别好的环境：用户点击"在 Codespace 中打开"，LLM 功能立即可用。

## 免费层在哪里不够用

免费层慷慨但不是无限的。三种模式会在午前耗尽你的配额：

**基准扫描。** 50 次 GPT-4o 配额听起来很多，直到你在跑 5 个 prompt × 10 次改写 × 5 个 temperature 的评估网格。这是 250 次调用，不是 50 次。把基准工作移到 BYOK 或付费模式；免费层用于单次评估，不是网格扫描。

**多模型共识。** 如果你的应用并行用 3 个模型并取平均（一个常见的 agent 可靠性模式），你的 50 次 GPT-4o 调用变成 16 次有效决策。相应规划，或把重负载走 OpenRouter。

**CI 循环。** 每次 push 都跑、每次跑做 5 次 LLM 调用的工作流会在 20 次 push 内耗尽 100 次/天的配额。要么移到 BYOK，要么把工作流限制为仅在 merge-ready 分支上跑。

超出免费层配额时，GitHub Models 返回 `429 Too Many Requests` 响应，带 `Retry-After` header 表明每日重置时间。没有超额计费 — 你停。这比 OpenAI 的按量付费默认值更干净，那边一个出 bug 的脚本能在你注意前烧掉 $500 信用额度。

## 与 OpenRouter、Hugging Face、厂商直连 API 的对比

aggregator 空间里 GitHub Models 最接近的对应物是 **OpenRouter**（在我们 provider database 中单独介绍）。OpenRouter 有更多模型（300+ 对 GitHub Models 的 50+），更灵活的路由（你可以指定"用支持此模型的最便宜的 provider"），无需 GitHub 账户。代价是 OpenRouter 没有原生 Actions 集成，没有绑定到你开发环境的一方 Playground，没有每日免费配额 — 你按 token 付费或自带 key。

**Hugging Face Inference API** 是另一个直接竞品。Hugging Face 给开源权重模型（Llama、Mistral、DeepSeek）提供免费层，但不能一方访问 GPT-4o、Claude 这类闭源权重模型。对开源权重模型评估，Hugging Face 更灵活（你可以跑 Hugging Face Hub 上的 1M+ 模型中的任意一个，包括社区微调），但免费层推理比 GitHub Models 慢，限速也更激进。

**厂商直连 API**（OpenAI、Anthropic、Cohere、Mistral）在某些情况下有更慷慨的免费层（Mistral 注册送 $5 免费信用，无每日上限），但需要分开的账户、分开的账单、分开的限速谈判、分开的 SDK（或如果你用 OpenAI 兼容接口就需要仔细的 base_url 管理）。对评估某个特定厂商的开发者，直连 API 更简单。对需要并排评估 5+ 模型的开发者，GitHub Models 的统一目录胜出。

## 优缺点

**优点**

- 真正的免费层，无需信用卡 — 任意 GitHub 账户可用
- 50+ 生产模型，包括 GPT-4o、Claude 3.5 Sonnet、Llama 3.1 405B、o1-preview
- 严格的 OpenAI chat completions 兼容 — 从 OpenAI SDK 直接接入
- 一方 GitHub Actions 集成，无需 secret 管理
- 一方 Codespaces 集成 — 云开发环境中 AI 功能开箱即用
- BYOK 模式在现有 Azure / OpenAI 账户上统一账单
- 策展目录 — GitHub 在加入前审查模型

**缺点**

- 每日配额严格 — 重度用户中午前就触发 429
- 模型版本滞后上游厂商发布 1-2 周
- 截至 2026 年 6 月，目录中没有 Claude Opus 4.5、GPT-5.5 系列
- 中国连通性问题 — GitHub 本身从 CN 需要代理
- 无专用 embedding 模型 — 必须单独接 Voyage 或 OpenAI
- 相比 OpenAI 直连 API，function calling 的细粒度控制有限
- BYOK 模式需要 GitHub Copilot Business（$19/用户/月）— 不免费

## 常见问题

**Q：GitHub Models 真的免费吗？**
A：是的 — 免费层是真正的免费，无需信用卡。每个模型每天有一定配额（GPT-4o 50 次、Claude 3.5 Sonnet 100 次等）。如果超出配额，你会收到 429 — 没有超额计费。免费层面向原型、评估、轻量 CI 使用。对于生产工作负载，移到 BYOK（如果你有 Copilot Business）或厂商直连 API。

**Q：GitHub Models 跟 OpenRouter 怎么比？**
A：两者都在单一 API 后聚合多模型。OpenRouter 模型更多（300+ 对 50+），路由更灵活，无 GitHub 依赖。GitHub Models 与 GitHub Actions / Codespaces 集成更紧密，免注册摩擦的每日免费配额，GitHub 审查安全性的策展目录。对纯模型评估，OpenRouter 更灵活。对 GitHub 原生工作流和零成本原型，GitHub Models 胜出。

**Q：我能用 OpenAI Python SDK 调 GitHub Models 吗？**
A：能。设置 `base_url="https://models.github.ai/inference"` 和 `api_key=<你的 GitHub PAT 带 models:read scope>`。模型名用 `openai/gpt-4o`（vendor/model 前缀）。Streaming、function calling、JSON mode、system messages 全部无需修改即可工作。

**Q：GitHub Models 用我的 prompt 训练模型吗？**
A：根据 GitHub 数据使用政策，GitHub Models 不用你的 prompt 或补全来训练模型。Prompt 被记录用于滥用监控和限速强制，但不会超出此范围与你的 GitHub 账户关联。对有严格数据处理要求的工作负载，BYOK 模式通过你自己的 Azure OpenAI 或 OpenAI 组织路由推理，上游厂商的数据政策适用。

**Q：GitHub Models 缺哪些模型？**
A：截至 2026 年 6 月，最显著的缺席是 Anthropic Claude Opus 4.5（仅列出 Sonnet 变体）、OpenAI GPT-5.5 / GPT-5.5 Instant 档位（仅 GPT-4o 和 o1 系列）、Google Gemini 系列（目录中无 Gemini 模型）。GitHub 未公布添加这些的时间表。

**Q：我能在 GitHub Actions 中不用 secret 调 GitHub Models 吗？**
A：能。`actions/ai-inference` action 自动使用工作流内置的 `GITHUB_TOKEN`。你不需要配置 PAT、Azure 资源、OpenAI API key。免费层配额适用，所以这最适合轻量 CI 决策，而不是高批量处理。

**Q：GitHub Models 在中国能用吗？**
A：不能。GitHub 本身从中国大陆就需要代理，GitHub Models 端点继承这一约束。对中国直连 AI 推理，请看阿里云百炼、百度文心一言、Kimi、智谱 GLM、腾讯混元、字节豆包（都在 apirank 国内分类下）。

## 结论

对已经生活在 GitHub 生态中的开发者，GitHub Models 是 2026 年最有用的免费 AI API。免费层每日配额足够评估目录中任意模型、构建带 LLM 判断的 GitHub Actions 工作流、或在不必承诺厂商关系的情况下原型功能。OpenAI 兼容性是真的，不是部分 shim — function calling、streaming、JSON mode 全部工作。GitHub Actions 集成消除了让 LLM 功能进入 CI 工作流成为多日项目的运维开销。

诚实的边界：每日配额不够生产工作负载，模型目录比上游厂商滞后 1-2 周，缺失的 Claude Opus / GPT-5.5 档位把严肃生产工作推到别处。对于这些，正确的模式是用 GitHub Models 做评估和原型，然后把生产流量指向 OpenAI / Anthropic / Mistral 直连（或 OpenRouter 做 aggregator 路由）。

最近的自然配对是 GitHub Models 作为付费生产栈之上的**免费层评估层**。在 GitHub Models 上原型，然后把生产流量指向 OpenAI / Anthropic / Mistral 直连。对于想要在原型和生产上都用单一 aggregator 的团队，OpenRouter 是更灵活的 aggregator — 但你放弃了 GitHub 原生集成和免费层。

**对大多数开发者**：GitHub Models 是最简单的入口。打开 `github.com/marketplace/models`，选个模型，在 Playground 跑个 prompt，然后把 SDK 代码片段复制到你的项目里。如果模型不适合你的工作负载，就换 — 免费层覆盖 50+ 模型的评估。

---

来源：GitHub Models 文档（`docs.github.com/en/github-models`）、GitHub Marketplace Models 目录、GitHub Changelog（2026-Q2）、关于免费层限速的社区报告。基于当前 GitHub PAT `models:read` scope 和 OpenAI SDK v1.x 兼容性核查。