---
title: "Arize Phoenix 2026 评测：开源 LLM 可观测性平台"
slug: arize-phoenix-api-review
date: 2026-07-21
lang: zh
locale: zh
provider: arize-phoenix
providerFeatured:
  - arize-phoenix
  - helicone
  - openai
  - anthropic
  - freemodel
primaryAffiliate: freemodel
affiliateUrl: https://freemodel.dev/invite/FRE-7a3b6220
type: review
category: aggregator
---

# Arize Phoenix 2026：开源 LLM 可观测性的参考实现

Arize Phoenix 是 Arize AI 推出的开源 LLM 可观测性与评测平台。截至 2026-07-21 核验,Phoenix 是 **唯一一个** 采用 Elastic-2.0（商业友好）许可、原生支持 OpenTelemetry 协议（业界开源 trace 协议）的顶级 LLM 可观测性平台。它在 GitHub 上积累 **10,600+ 颗星**，以约每周一个版本的节奏发布 19.x 系列，并被 LangChain、LlamaIndex、OpenAI Agents SDK 设为默认的可观测后端。Phoenix 与 Helicone（Apache-2.0、控制面托管的同侪）、Portkey（闭源 SaaS）、Langfuse（LGPL）、LangSmith（LangChain 出品的闭源 SaaS），以及 Arize 自家的企业级产品 Arize AX 形成完整的竞争图谱。

本文将系统比较 Phoenix 与闭源竞品的差异、2026 年的实际定价（免费 Cloud 套餐含 10 GiB、付费档、自托管档），并提供在 OpenAI / Anthropic / vLLM / Ollama 工程中接入 Phoenix tracing 的实战代码。本文与 Helicone、Portkey、Langfuse、LangSmith、OpenLLMetry 的差异对比表，数据来自 v19.3.0（2026-07-20）发布说明、官方 `arize-phoenix` PyPI 包、GitHub README 以及 phoenix-cloud.mdx 文档。

如果你在 2026 年评估 LLM 可观测性、又特别在意厂商锁定（vendor lock-in），本文就是你需要的参考指南。

## Arize Phoenix 是什么（以及不是什么）

Phoenix 是 **AI 可观测性 + 评测平台**，不是 LLM 路由或网关。它位于你的应用与 LLM 提供方之间，捕获每一次请求、每一次工具调用、每一次检索、每一次 trace span，并通过 Web UI、SDK 查询接口与评测框架把它们暴露出来。

Phoenix 的核心能力（截至 2026-07-21，来自 v19.3.0 文档与 GitHub README 核验）：

- **Elastic-2.0 开源。** 源码完整公开在 github.com/Arize-ai/phoenix（10,643 颗星、998 个 fork，自 2022-11-09 持续维护）。你可以自托管、fork、修改并发布衍生版本，无需向任何人付费。这是 Top-3 LLM 可观测性工具里唯一同时满足「许可宽松 + 完全自托管」两个条件的项目。
- **OpenTelemetry 原生。** Phoenix 直接接入标准 OTLP trace，任何 OTel 接入的应用都能上报。它与 Honeycomb、Tempo、Jaeger、Datadog 等其他 OTel 后端可互换。
- **17+ LLM 框架集成。** 开箱即用地自动检测 OpenAI SDK、Anthropic SDK、Google Vertex、AWS Bedrock、Cohere、Mistral、Groq、Together AI、Fireworks、Hugging Face、vLLM、Ollama、LangChain、LlamaIndex、Haystack、OpenAI Agents SDK、smolagents。
- **Tracing + Spans + 评测 + 数据集 + 实验 + 提示词 playground + PXI 代理。** Helicone 主要是个 logging 代理；Phoenix 则是一整套 AI 工程工作台：trace、评测、数据集、实验对比、提示词版本管理、检索检视，外加 2026-Q3 新引入的 "PXI" AI 工程代理（公测中）。
- **可自托管在任意平台。** 文档中可核验的部署方式：CLI（`px setup`）、Docker、Compose、Kubernetes、Helm、AWS CloudFormation、Railway 一键、Render 蓝图、Google Cloud Run、Azure ARM 模板。当然也提供托管版 Phoenix Cloud，避免自建基础设施。
- **Cloud 免费层。** Phoenix Cloud 提供每个工作空间 10 GiB 内置存储的免费版本，注册 `app.arize.com` 账号即可使用，没有时间限制，只受存储上限约束。
- **单命令启动（`px setup`）。** 2026-Q3 的新 CLI 引导式完成五步：Git 安全检查、连接建立、agent 接入、验证、配置回写。新项目五分钟内即可接入 tracing。

Phoenix **不**做模型训练或微调，**不**做推理托管（与 Helicone 的缓存层或 Vercel AI Gateway 的路由功能不同），**不**替代 LLM 提供方的计费 token（仅做观测），**不**默认充当认证代理（Helicone 包裹调用；Phoenix 在标准安装下不直接代理，可用轻量桥接实现）。

定位：**Phoenix 就是 "AI 工程领域的 Honeycomb"，而且开源、可自托管、可扩展**。

## Arize Phoenix 2026 定价：免费 Cloud、付费档、自托管

截至 2026-07-21 核验（官方 Phoenix Cloud 注册页 + 自托管文档）。Phoenix 提供三种部署模式，每种独立定价：

| 部署方式 | 费用 | 存储上限 | 数据保留 |
|---|---|---|---|
| **Phoenix Cloud（免费）** | $0 / 月 | 每工作空间 10 GiB | 直到用满上限 |
| **Phoenix Cloud（付费）** | 按量付费、按数据量阶梯 | 自定义 | 自定义 |
| **Phoenix 自托管（Elastic-2）** | $0（仅付基础设施费） | 无上限 | 无上限 |
| **Arize AX（企业版）** | 合同制 | 无上限 | 无上限 + SSO + RBAC + 审计日志 |

免费 Cloud 套餐是最低门槛的入门方式。在 `app.arize.com` 注册、点击 "Create a Space"，Phoenix 就为你开通一个托管工作空间，附带 10 GiB 存储。付费 Cloud 是按量付费（按数据量阶梯、无按席计费）；企业版（Arize AX）补充 SAML SSO、本地部署、自定义 MSA、审计日志与专属 Slack 支持。

对绝大多数团队来说，正确的入门方式是用免费 Cloud 套餐。当存储用到 10 GiB（约 500-1000 万条 trace span，具体视 payload 而定）时，再二选一：升级到付费 Cloud，或者迁移到自托管。自托管不产生授权费，跑的是同一份 Phoenix 镜像。

> ⚠️ **定价陷阱：** Phoenix Cloud 按 **存储** 计费，而非按席计费。一个独立开发者跑 50 RPS 与一个 50 人团队跑同样的流量，消耗的存储是一样的。席位数计费是 Vercel/Portkey 的模式，Phoenix 是按数据量计费。

## Arize Phoenix vs Helicone vs Langfuse vs Portkey vs LangSmith vs OpenLLMetry

2026 年的 LLM 可观测性战场有六个有竞争力的选项。按所有权与许可分三组：

| 工具 | 许可 | 自托管 | 免费层 | 付费层 | Tracing | 评测 | 数据集/实验 | 原生框架自动接入 | OpenTelemetry 原生 |
|---|---|---|---|---|---|---|---|---|---|
| **Arize Phoenix** | Elastic-2.0 | ✅ | 10 GiB Cloud | 按量付费 | ✅ | ✅ | ✅ | 17+ 框架 | ✅ |
| Helicone | Apache-2.0 | ✅ | 10K req/月 | $79/月（Pro） | ✅ | ⚠️ 有限 | ❌ | 100+ 提供方 | ⚠️ 代理模式 |
| Portkey | 闭源 | ❌ | 10K req/月 | $49/月（Hobby） | ✅ | ✅ | ⚠️ 有限 | 200+ 提供方 | ⚠️ 代理模式 |
| Langfuse | LGPL（托管 Cloud） | ✅ | 50K events/月 | 按量付费 | ✅ | ✅ | ✅ | LangChain + 其他 | ✅ |
| LangSmith | 闭源（LangChain 出品） | ⚠️ 仅企业版 | 5K traces/月 | $39/月（Plus） | ✅ | ✅ | ✅ | LangChain 优先 | ⚠️ 代理模式 |
| OpenLLMetry | MIT（OTel contrib） | ✅ | N/A（库，不是服务） | N/A | ✅ | ❌ | ❌ | 17+ 框架 | ✅ |

结构性归类：

- **闭源 SaaS（Portkey、LangSmith）：** 上手最容易，但你看不了源码、不能自托管、数据存对方库房。厂商锁定是核心痛点。
- **开源可自托管（Phoenix、Langfuse）：** 免费部署任意位置；OpenTelemetry 原生可换后端；你需要负责运维。
- **OSS 但仅代理模式（Helicone）：** 开源许可存在，但生产部署以 SaaS 为主；想用完整功能必须走代理。
- **纯库而非服务（OpenLLMetry）：** 这是 Phoenix 底层所用的 OTel contrib 项目。你可以用 OpenLLMetry 而不接 Phoenix，把 trace 导出到任意 OTel 兼容后端。

实操选择：

- 如果你要 **最大控制 + 最小锁定**，Phoenix 是首选。它是唯一同时具备宽松许可 + OpenTelemetry 原生 + 完整 UI 的顶级选项。
- 如果你要 **非工程师团队最容易上手**，LangSmith 或 Portkey 的 UI 更精致。
- 如果你要 **Helicone 的代理模式 + OSS 许可**，可以用自托管 Helicone 或开源的 LiteLLM 当代理，后端接 Phoenix。
- 如果你要 **免费的 Phoenix 级能力而不自托管**，Phoenix Cloud 免费层覆盖绝大多数独立开发者和早期团队场景。

## 如何给 OpenAI / Anthropic 应用接入 Phoenix tracing（带代码）

最简单的接入方式是 Phoenix 的 OTel 自动检测器。**一行代码**就可以把每一个 OpenAI / Anthropic / vLLM 调用接入 Phoenix，无需改动既有客户端：

```python
# pip install arize-phoenix-otel openai
from phoenix.otel import register
from openai import OpenAI

# 把 Phoenix 指向本地或托管的 collector
tracer_provider = register(
    project_name="my-llm-app",
    endpoint="http://localhost:6006/v1/traces",  # Phoenix Cloud 或自托管
)

client = OpenAI()  # 用环境变量里的 OPENAI_API_KEY
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "通过 Phoenix 调用 GPT-4o。"}],
)
print(response.choices[0].message.content)
# 每次 API 调用现在都带完整 span、token 计数、延迟显示在 Phoenix 中。
```

这一行 `register()` 把 OpenTelemetry span 自动附加到 OpenAI SDK 并导出到 Phoenix，同时在 UI 里建一个名为 `my-llm-app` 的项目。既有客户端代码完全不动。

### 在 Phoenix 中使用 Anthropic SDK

```python
# pip install arize-phoenix-otel anthropic
from phoenix.otel import register
from anthropic import Anthropic

tracer_provider = register(
    project_name="claude-eval",
    endpoint="http://localhost:6006/v1/traces",
)

client = Anthropic()  # 用 ANTHROPIC_API_KEY
msg = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=1024,
    messages=[{"role": "user", "content": "总结 Q2 OKR。"}],
)
print(msg.content[0].text)
# Span 与 OpenAI 调用显示同样的 metadata。
```

### 本地启动 Phoenix 做开发

最快的本地启动方式：`phoenix serve`，会在 `localhost:6006` 上开一个 Phoenix UI，自带进程内 OTel collector 和 SQLite 存储。开发场景一句话搞定：

```bash
pip install arize-phoenix
phoenix serve
# 打开 http://localhost:6006 — Phoenix 就绪，无需任何配置。
```

生产级自托管，把 SQLite 换成 PostgreSQL、用 Docker 当部署平台即可。完整 Docker Compose 文件在 GitHub 仓库的 `deploy/docker` 目录里。Kubernetes 用户有官方 Helm chart；AWS / GCP / Azure 客户可用一键 IaC 模板，详见自托管文档。

## OpenTelemetry：为什么 Phoenix 的协议选择重要

Phoenix 架构上最重要的事实是：它说 OTLP（OpenTelemetry Line Protocol，业界开源 trace 协议标准）。这意味着：

1. **既有的 OTel 流水线可以直接接入。** 如果你的团队已经跑 Honeycomb、Datadog、Tempo 或其他 OTel 后端，Phoenix 可以与它们并列对接。你也可以把任何 OTel 接入的应用的 trace 导入 Phoenix 存储。
2. **没有厂商锁定的 SDK。** `phoenix-otel` 包是建立在 `opentelemetry-instrumentation-*` 之上的，正是 OTel 用户所用的同一组检测包。如果你不接 Phoenix 了，trace 仍然会流向你的 OTel collector。
3. **多后端扇出。** 因为协议开放，你可以让 Phoenix 作为主要 UI 后端，同时把 trace 扇出到 Datadog 做生产告警，无需重复埋点。这是 2026 年中途采用 Phoenix 的团队的典型做法。

战略含义：**Phoenix 是 LLM 可观测性领域的 Grafana**。OpenTelemetry 是协议，Phoenix 是 UI，而你保有数据与集成。

## 评测、数据集与 PXI 代理

Phoenix 不只是 tracer，平台的另一半是结构化评测：

- **Spans → 数据集。** 在 UI 里点一下，把任何 span 转成数据集中的一行。如果你有 200 条线上生产 trace 想打分，UI 会自动提取它们，允许你挂上期望输出与评分器配置。
- **评分器。** Phoenix 内置 code-based 评分器（精确匹配、JSON Schema 校验、正则）、LLM-as-judge 评分器（自备模型）、自定义 Python 评分器。在数据集上批量跑，然后横向比较不同提示词版本或模型版本的得分。
- **实验。** 在同一数据集上比较两个提示词版本。Phoenix 按评分器得分排序，逐行展示谁赢谁输。这就是 2026 年提示词 A/B 测试的样子。
- **提示词 Playground。** 编辑提示词、重新生成、在 Phoenix 内打分，无需切换工具。支持多轮对话编辑、与生产同一条 OTel trace 路径。
- **PXI（Phoenix Intelligence）。** 2026-Q3 推出的代理（目前 BETA）读取你既有的 trace、数据集、评测和实验，然后用自然语言回答关于它们的问题。模式与面向可观测数据的编程 agent 同构——问"上周 prompt-engineering 提示词有什么改动"，PXI 自动 diff 版本并定位回归。

要点：**Phoenix 是唯一一个把 tracing + 评测 + 实验 + 提示词管理 + agent 辅助调试都装进同一个许可（Elastic-2.0）的 LLM 可观测性工具**。Helicone 覆盖 tracing + 实验评测，但深度不及 Phoenix。Portkey 评测做得好，但 trace 只走代理。LangSmith 全部覆盖但闭源。

## 用 Docker Compose 自托管 Phoenix

对需要本地部署或气隙环境的团队，Phoenix 用一个 Docker Compose 文件就能自托管。最小 Compose 是两个服务：一个 Phoenix 应用服务器（Python，常规开发工作负载约 2 CPU、2 GiB RAM）和一个 PostgreSQL 数据库（Postgres 15+）。本地开发也能用内置的 SQLite 路径：

```yaml
# docker-compose.yml（Phoenix 最小自托管）
services:
  phoenix:
    image: arizephoenix/phoenix:latest
    ports:
      - "6006:6006"
    environment:
      - PHOENIX_SQL_DATABASE_URL=postgresql://phoenix:***@db:5432/phoenix
      - PHOENIX_ENABLE_AUTH=***   # 可选：启用本地账号
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: phoenix
      POSTGRES_PASSWORD: phoenix
      POSTGRES_DB: phoenix
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

```bash
docker compose up
# 打开 http://localhost:6006 — Phoenix 完整栈已运行在 Postgres 之上。
```

Kubernetes 用户用 `Arize-ai/phoenix-helm` 官方 Helm chart 一条 `helm install` 就能部署。AWS 用户可用官方 CloudFormation 模板；GCP 用户一键 Cloud Run 部署；Azure 用户用 ARM 模板；Railway 与 Render 用户一键 Blueprint。

大多数公司 2026 年的典型路径：**先用 Phoenix Cloud 免费层跑六个月，等存储成本起来后再 EKS 或 GKE 自托管**。从 Phoenix Cloud 切换到自托管只是改配置，不必重写代码。

## 真实使用场景

**1. 提示词工程的 LLM 评测平台。** 某团队同时跑 GPT-4o、Claude Opus 4.8、Gemini 2.5 Pro，想知道哪个提示词产出最优。Phoenix 会 trace 所有调用、把 span 转成数据集、用 LLM-as-judge 在三个模型上批量评分，并在 UI 里对比结果。PXI 代理可以回答"列出上周所有 Claude 评分低于 4.5 的提示词"。

**2. RAG 调试。** 某 RAG 应用产出错误答案。Phoenix 对每一步做 trace：query embedding → 向量检索 → chunk 评分 → LLM 合成。UI 里直接展示每次 trace 实际检索到的 chunk，让工程师精准定位失败是检索环节还是合成环节。这是 Phoenix 的典型场景——RAG 应用需要 span 级可见性，远不止请求级日志。

**3. 生产成本归因。** 一家 SaaS 产品需要按客户归因 LLM 成本。Phoenix span 自带任意 tag（`customer_id`、`feature_name`、`tenant`）。后端任务通过 Phoenix API 查 trace、按 `customer_id` 分组、生成月度账单。相比自建 logging 流水线，每调用多一条查询，节省的工程时间以月计。

**4. Agent 调试。** 一个 OpenAI Agents SDK 或 smolagents 工作流产出 14 步工具调用链。Phoenix trace 每一次工具调用、每一个子代理决策、每一次 LLM 调用。UI 以瀑布图形式呈现完整链路，PXI 可以自然语言叙述"为什么出问题"——"代理对同一查询连续调了三次 `search_web`，因为缓存预热前去重步骤就已触发。"

**5. 合规审计日志。** 受监管行业（医疗、金融、政府）需要把每次 LLM 调用都留痕做审计。Phoenix 对每次调用产出一条带 prompt、response、延迟、模型、token 的结构化 span。通过 OTel collector 导出到 S3，保留七年，搞定。Elastic-2.0 许可覆盖商业部署。

## 客观局限

Phoenix 是 2026 年最强的开源 LLM 可观测性工具，但不是万能药：

- **没有请求侧缓存或 fallback 路由。** Phoenix 是只观测的工具。要 LLM 缓存、fallback 链或请求重试的代理层，在 Phoenix 前面套一层 Helicone、Vercel AI Gateway 或 LiteLLM。组合能工作，Phoenix 不会试图做所有事情。
- **没有内建 token 成本优化。** Phoenix 告诉你每条 trace 的成本，不会自动协商费率或路由到更便宜的模型。这是 Portkey 或 Helicone 的能力。
- **Cloud 免费层只有 10 GiB。** 足以覆盖独立开发者和小型团队，扛不住高流量生产环境。在触顶前规划好 Cloud → 自托管的迁移（Phoenix 在接近上限时会邮件提醒）。
- **PXI 还处于 BETA。** 这个代理在 trace 调查上确实有用，但在边角情况下会答错。把它的输出当作起点，别当作定论。
- **自托管需要 Postgres + Python。** 不像 Langfuse 那么重，但你在跑数据库 + 应用服务器。Railway / Render 一键部署对大多数团队都够用。
- **闭源竞品（LangSmith、Portkey）的 UI 抛光更好。** Phoenix 的 UI 功能完备但不如 LangSmith 精致。如果非工程师团队成员每天都要用这个工具，预留学习曲线。

这些都是权衡，不是致命问题。对看重控制力与开放标准的工程团队，Phoenix 是正确的选择。

## 给 API 开发者的结论

Arize Phoenix 是 **2026 年最好的开源 LLM 可观测性平台**。它是唯一一个同时具备宽松许可、可自托管、OpenTelemetry 原生、可评测、活跃维护的顶级选项。Cloud 免费层覆盖绝大多数独立开发者和小型团队；自托管覆盖剩下的全部场景。如果你的团队已经在用 OTel，Phoenix 作为对等后端直接接上；如果你的团队刚开始接触 LLM 可观测性，Phoenix 的 `px setup` CLI 与 17+ 框架集成会让第一个小时就有产出。

要 **最大控制 + 最小锁定**的 LLM 可观测性，选 Phoenix。想要最精致的 UI，且栈是 LangChain 原生，选 LangSmith。想要强评测 UX 的 SaaS 控制面，选 Portkey。想要带缓存的代理层，选 Helicone。想要更广框架覆盖的 LGPL 替代品，选 Langfuse。

生产场景先用 **Phoenix Cloud 免费层**起步。超过 10 GiB 存储后，再迁移到 **EKS 或 GKE 自托管**。PXI 离开 BETA 后把它加入 debug 工具链。同时需要请求侧缓存和 fallback 路由时，把 Phoenix 与 **Helicone 或 Vercel AI Gateway** 组合——Phoenix 和代理能干净地组合。

截至 2026-07-21 的数据都在 GitHub README、v19.3.0 release notes 和官方文档中。数字会变，架构模式不会变。

## 常见问题

### 2026 年 Arize Phoenix 用来做什么？

Arize Phoenix 是一款开源的 LLM 可观测性与评测平台。它捕获任何 OpenTelemetry 接入应用（OpenAI、Anthropic、vLLM、Ollama、LangChain、LlamaIndex 等）的 trace，通过 Web UI 展示，并在此之上叠加评测、数据集管理、实验对比、提示词版本管理能力。Phoenix 对 LLM 应用的意义正如 Honeycomb 对微服务——但开源、可自托管。2026 年它已成为追求最小厂商锁定的团队的默认可观测性后端。

### Arize Phoenix 是免费的吗？

是的，三种方式都免费。Phoenix Cloud 免费层每个工作空间附带 10 GiB 内置存储，长期免费（除了存储上限没有时间限制）。Phoenix 自托管基于 Elastic-2.0，部署任意位置都不产生授权费（你只付基础设施账）。Phoenix 的源码在 GitHub 完整公开。付费 Cloud 按量付费以扩容存储；企业档（Arize AX）走合同制，包含 SAML、SSO、审计日志、本地部署。

### Phoenix 与 Helicone 在 2026 年相比怎么样？

两者都是 LLM 可观测性工具，但优化方向不同。Phoenix 是「观测优先」（自带客户端、Phoenix 通过 OTel 收集 trace）+ 开源（Elastic-2.0、可自托管）。Helicone 是一个代理式的 LLM 调用包装器，带缓存、fallback、HQL 查询——也是开源（Apache-2.0）但生产部署以 SaaS 代理为主。要完整控制力与 OpenTelemetry 原生架构，选 Phoenix。要请求侧缓存与无代码可观测性仪表板，选 Helicone。它们组合性很好——Phoenix 套在 Helicone 代理后面，是 2026 年的常见组合。

### Phoenix 支持 OpenAI 的 Agents SDK 吗？

支持。Phoenix 为 `openai-agents`（以及 `smolagents`、LangChain、LlamaIndex、Haystack 等）提供了 OpenTelemetry 自动检测器。接入只要一行——`register(project_name="...", endpoint="...")`——所有 agent 调用、子代理决策、工具调用都自动 trace 进 Phoenix。新的 PXI 代理可以为 trace 调试提供叙述解释。Agent 调试是 Phoenix 在 2026 年增长最快的用例。

### 我能在 Kubernetes 上自托管 Phoenix 吗？

可以。`Arize-ai/phoenix-helm` 官方 Helm chart 通过一条 `helm install` 命令部署 Phoenix。AWS 用户有官方 CloudFormation 模板；GCP 用户一键 Cloud Run 部署；Azure 用户用 ARM 模板；Railway 与 Render 用户一键 Blueprint。最小资源占用大约 2 CPU + 2 GiB RAM 用于应用服务器，10 GiB PostgreSQL 数据库用于典型工作负载。

### Arize Phoenix 支持 LLM 评测吗？

支持。Phoenix 内置 code-based 评分器（精确匹配、JSON Schema 校验、正则）、LLM-as-judge 评分器（自备任一 LLM 作裁判）、自定义 Python 评分器。在数据集上批量运行（从任何 span 一键转换），然后在实验 UI 跨提示词版本横向比较评分。评测工具链在 SDK 层面与 LangSmith 相当，UI 上略弱。

### Phoenix 是 OpenTelemetry 原生吗？

是的。Phoenix 接受来自任何 OTel 接入应用的标准 OTLP trace。它可与 Tempo、Jaeger、Honeycomb、Datadog 以及任何其他 OTel 后端完全互换。也可以通过标准 OTel collector 配置把 trace 扇出到多个后端。OpenTelemetry 是 Phoenix 长期灵活性的战略性协议选择。

### Phoenix 由谁开发和维护？

Phoenix 由 Arize AI 构建并维护，他们也是 Arize AX 企业版可观测性产品的出品方。GitHub 上 Arize-ai/phoenix 仓库有 10 位以上贡献者，几乎每天都有提交。版本按 Semantic Versioning 节奏周发布；v19.x 系列于 2026-07-20 发布。维护团队中有 OpenTelemetry 社区工程师，Phoenix 是 OTel 风格 LLM 接入的参考实现之一。

### Phoenix 与 Arize AX 的区别是什么？

Phoenix 是开源核心（Elastic-2.0、完全自托管、Cloud 免费层）。Arize AX 是基于 Phoenix 的商业企业产品，补充了 SAML SSO、本地部署、基于角色的访问控制、审计日志、专属 Slack 支持、自定义 MSA、批量云折扣。典型路径是：Phoenix Cloud 免费层 → Phoenix 在 EKS 自托管 → 受监管行业升级到 Arize AX。两者的数据模型与 SDK 完全一致。

## 来源

- Arize Phoenix GitHub 仓库：github.com/Arize-ai/phoenix — 10,643 颗星、998 个 fork、Elastic-2.0 许可
- Phoenix v19.3.0 发布（核验 2026-07-20）
- PyPI 包 arize-phoenix — Python 3.10-3.14 支持
- Phoenix Cloud 文档：app.arize.com（注册）、phoenix-cloud.mdx（接入）
- Phoenix 自托管文档：docker、kubernetes、helm、aws-with-cloudformation、railway、render、google-cloud-run
- Phoenix Cloud 免费层：每工作空间 10 GiB 内置存储
- OpenTelemetry OTLP 标准：opentelemetry.io/docs/specs/otlp/
- LLM 框架集成列表：integrations.mdx — 17+ 框架，包括 OpenAI SDK、Anthropic SDK、LangChain、LlamaIndex、Haystack、smolagents、OpenAI Agents SDK
- PXI（Phoenix Intelligence）BETA 公告：pxi.mdx
- 许可详情：Elastic-2.0，完整文本见 elastic.co/licensing/elastic-license
