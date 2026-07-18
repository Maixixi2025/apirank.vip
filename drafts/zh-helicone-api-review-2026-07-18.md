# Helicone 2026 评测：开源 LLM 可观测性平台

_Date: 2026-07-18 | Slug: helicone-api-review | Locale: zh_

# Helicone 2026：给 LLM 栈加一行的开源可观测性平台

Helicone 是 2026 年 LLM 可观测性的开源标杆。2023 年由 Y Combinator W23 团队创立，目前在 GitHub 上是 5,961 star 的 Apache-2.0 项目（截至 2026-07-18 验证），通过单一 AI Gateway 包装 100+ LLM Provider，提供完整请求日志、成本归因、Prompt 版本管理与类 SQL 的查询语言。Helicone 是你应用与 OpenAI/Anthropic/Google 之间缺失的那一层——换个 base URL，每次 Prompt、输出、延迟、Token 数、成本都自动捕获。
本文带你了解 Helicone 的功能、AI Gateway 与主流 Provider 的集成方式、2026 年已验证的定价（Hobby 免费、Pro $79/月、Team $799/月、Enterprise 定制），以及它与 Portkey、LiteLLM、Cloudflare AI Gateway 的对比。数据来自 Helicone 官方定价页（helicone.ai/pricing，2026-07-18 抓取）以及 GitHub 公开 API。如果你在 2026 年评估 LLM 可观测性厂商，这就是参考指南。
## Helicone 的能力边界

Helicone 是 LLM 可观测性层，不是模型 Provider。你继续用现有的 OpenAI / Anthropic / Google 账户；Helicone 介于应用与 Provider 之间做透明代理，自动记录每次调用。核心能力包括：
- AI Gateway——单一 base URL，路由 100+ Provider，支持 Provider Failover 与按 Key 限流。
- 请求日志——完整 Prompt、输出、延迟、Token 数、成本与用户元数据全部捕获并建索引。
- HQL（Helicone 查询语言）——类 SQL 语法，亚秒级查询十亿行 LLM 调用记录。从 Pro 档起解锁。
- Prompt 版本管理与实验——A/B 测试 Prompt 变体，并排看成本 / 延迟 / 质量差异。
- 成本归因——按用户、团队、特性打标，生成按客户维度的账单。
- 自部署——Apache-2.0 协议意味着整套平台可以跑在你自己的基础设施上。
Helicone 不做模型训练或微调，不提供 Guardrails 与内容审核（不像 Portkey），也没有无代码 App Builder。Helicone 紧密聚焦在可观测性这一利基，这也是它的开源版本能做出生产级的关键。
## Helicone 2026 定价：Hobby / Pro / Team / Enterprise

Helicone 已验证的 2026-07 定价（来源：helicone.ai/pricing，2026-07-18 抓取）：档位价格请求/月核心功能Hobby免费10,0001 GB 存储，1 个座位，1 个组织Pro$79/月按用量无限座位、告警、报表、HQL 查询语言Team$799/月按用量5 个组织、SOC-2 + HIPAA、专属 Slack 频道Enterprise定制高用量SAML SSO、本地部署、定制 MSA、批量折扣
对超出包含请求量的客户，在座位费之上叠加按用量计费。官网未公开具体用量单价，高用量由 Enterprise 合同承接。Apache-2.0 自部署版本没有座位费——你只需付运行它的基础设施（典型配置：Postgres + Redis + Proxy 容器，跑在 $20/月的 VPS 上即可）。
Helicone 是 AI 基础设施厂商中罕见的"开源版与 SaaS 版功能等价"的案例。大部分可观测性厂商（Portkey、Cloudflare AI Gateway）只提供闭源 SaaS。如果你需要 SOC-2 或 HIPAA 合规，又不想被 SaaS 厂商锁定，Team 档（$799/月）是同时包含两项合规认证 + 无限座位的最便宜路径。
## Helicone vs Portkey vs LiteLLM vs Cloudflare AI Gateway

四款产品都解决"我需要把 LLM 调用路由到多个 Provider 并且看清发生了什么"的问题，但各自的优化点不同。下面的决策矩阵按 50 人工程师团队的产线 LLM 应用场景校准。能力HeliconePortkeyLiteLLMCF AI Gateway开源✅ Apache-2.0❌ 闭源 SaaS✅ MIT❌ 闭源自部署✅ 支持❌ 不支持✅ 支持❌ 仅 CFProvider 数100+200+100+40+免费档1 万请求/月1 万请求/月无限（OSS）受限团队档价$799/月$199/月免费（OSS）$5/月+用量SOC-2 / HIPAA✅ Team 起步✅ EnterpriseEnterprise 档CF 全平台A/B 测试✅ HQL✅ App Portal⚠️ 手动❌ 无Guardrails⚠️ 基础✅ 内建⚠️ 插件⚠️ 基础成本归因✅ 按用户/团队✅ 按 Key⚠️ 手动✅ 按 Tag自定义 SQL 分析✅ HQL❌ 仅仪表盘❌ 仅日志❌ 无
价格截至 2026-07-18 各自官网定价页验证。Helicone Pro $79/月，Portkey Growth $199/月，LiteLLM 开源自部署免费，Cloudflare AI Gateway Workers Paid 套餐 $5/月 + $0.20/百万 Gateway 请求。
如果你的优先级是自部署 + 完整可观测性 + 真正的查询语言，Helicone 是最强选项。如果你的优先级是规模化下的最低总成本，LiteLLM（开源、自部署免费）胜出。如果你的优先级是精致的 SaaS 体验 + App Portal，Portkey 是最佳。如果你的优先级是零运维 + 已经在 Cloudflare 上，AI Gateway 是最便宜的路径。
## Helicone AI Gateway 怎么用（含代码）

最简集成是改一行 base URL。OpenAI Python SDK 不用改其他代码：
from openai import OpenAI
import os

# 你现有的 OpenAI 客户端——只要换 base_url 并加上 Helicone 授权
client = OpenAI(
    api_key=os.environ['OPENAI_API_KEY'],
    base_url='https://ai-gateway.helicone.ai',
    default_headers={
        'Helicone-Auth': f'Bearer {os.environ['HELICONE_API_KEY']}',
        # 可选：为成本归因打 tag
        'Helicone-Property-User-Id': 'user_123',
        'Helicone-Property-Feature': 'chat-summary',
    }
)

response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': '请总结 Q3 财报。'}],
)
print(response.choices[0].message.content)
# 每次调用都会自动写入 Helicone 仪表盘
对 Anthropic Claude，走 Helicone 的 Anthropic 兼容端点即可：
from anthropic import Anthropic
import os

client = Anthropic(
    api_key=os.environ['ANTHROPIC_API_KEY'],
    base_url='https://anthropic.helicone.ai',
    default_headers={
        'Helicone-Auth': f'Bearer {os.environ['HELICONE_API_KEY']}',
    }
)

message = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=1024,
    messages=[{'role': 'user', 'content': '你好，Claude。'}],
)
自部署时，把 base_url 换成你自己的网关地址（比如 https://gateway.internal.yourcompany.com），Helicone-Auth 头可以省略或换成你自己的代理授权。
## HQL：让 Helicone 脱颖而出的查询语言

Helicone Query Language（HQL）是 Helicone 区别于 Portkey、LiteLLM、Cloudflare AI Gateway 的唯一特性。后三者只提供纯仪表盘分析或 JSON 过滤查询，HQL 给你一个真正的类 SQL 语法来切片和切块你的 LLM 调用日志。
平台工程师常用的 HQL 查询示例：
-- 最近 30 天 GPT-4o 成本最高的 20 个用户
SELECT user_id, sum(cost) AS total_cost
FROM requests
WHERE model = 'gpt-4o'
  AND created_at > now() - interval '30 days'
GROUP BY user_id
ORDER BY total_cost DESC
LIMIT 20;

-- 每个 Provider 的 P95 延迟
SELECT provider, quantile(latency_ms, 0.95) AS p95_latency
FROM requests
WHERE created_at > now() - interval '7 days'
GROUP BY provider
ORDER BY p95_latency DESC;

-- 按 Prompt 版本统计错误率
SELECT prompt_version,
       count(*) AS total_calls,
       sum(if(status_code >= 400, 1, 0)) / count(*) AS error_rate
FROM requests
GROUP BY prompt_version
ORDER BY error_rate DESC;
HQL 在 SaaS 部署中跑在 ClickHouse 上，对十亿行查询响应在 1 秒内。Pro 档（$79/月）解锁 HQL，Hobby 档和开源自部署免费版只提供基础过滤。
## 用 Docker Compose 自部署 Helicone

Apache-2.0 代码库自带 Docker Compose 配置，一条命令起 Proxy、Web 仪表盘、Postgres、Redis 与 ClickHouse：
# 克隆并启动 Helicone 自部署栈
git clone https://github.com/Helicone/helicone.git
cd helicone
docker compose up -d

# Proxy 监听 http://localhost:8585
# Web 仪表盘 http://localhost:3000
# ClickHouse、Postgres、Redis 都在内网
生产环境推荐把同样镜像部署到 Kubernetes。Helicone 仓库里有官方 Helm Chart。最小推荐配置：4 vCPU / 8 GB RAM 跑 Proxy + ClickHouse 节点，外加托管 Postgres 与 Redis。中小流量下，自部署 Helicone 通常在一台 $50–$100/月的 Hetzner 或 DigitalOcean 主机上就能稳定运行。
## 真实场景：Helicone 怎么帮你省钱

三种一个月内就能回本 Helicone 的典型模式：
- 多租户 SaaS 的成本归因。面向 200 家客户的 B2B AI 产品需要知道哪家客户在产生什么成本。Helicone 的 Helicone-Property-User-Id 头让你给每次调用打上租户 ID，跑 HQL 生成按客户的月度账单。Portkey 与 LiteLLM 需要按 Key 配置，超过几十个客户就难扩展。
- Prompt 实验追踪。每周发版的工程团队需要对比 Prompt A 与 B 在成本、延迟、质量上的差异。Helicone 的 Prompt 版本管理与 HQL 实验仪表盘能并排展示 delta，不需要自己写评测基础设施。
- 生产可观测性 + 事故响应。LLM 应用开始返 500 时，你需要知道是 Provider、Prompt 还是某个用户。Helicone 的请求日志带状态码、延迟、完整 Prompt 与输出，让根因分析从 4 小时缩到 10 分钟。
## 坦诚的限制

- Hobby 档上限 1 万请求/月。任何超出玩票规模的项目都需要至少 Pro（$79/月）。
- Team 档（$799/月）对小团队偏贵。如果你是 5 人小团队，Portkey Growth（$199/月）或 LiteLLM 自部署免费更划算。
- Guardrails 能力有限。Portkey 内建了内容审核、PII 脱敏、Prompt 注入防护等 Guardrails。Helicone 的 Guardrails 比较基础——如果安全是主要诉求，建议搭配一层专门的 Guardrails。
- 自部署依赖 ClickHouse。ClickHouse 让自部署栈比 LiteLLM 的纯 Python Proxy 更重。如果你需要真正的单二进制部署，LiteLLM 胜出。
- 按用量定价不公开。超出免费档的客户需要联系销售才能拿到每请求超额单价。
## 给 API 开发者的结论

Helicone 是 2026 年开源 LLM 可观测性的最强选项。Apache-2.0 协议意味着你能自部署整套平台，AI Gateway 通过一行替换接入 OpenAI / Anthropic / Google，HQL 是 AI Gateway 厂商中唯一的真类 SQL 查询语言。如果你需要 SOC-2 与 HIPAA 开箱即用，又不想走到 Enterprise 档，$799/月的 Team 档是市面上最便宜的合规认证 + 无限座位组合。
对于把原始成本放在特性之上的团队，LiteLLM（免费自部署）或 Cloudflare AI Gateway（$5/月）更划算。对于追求精致 SaaS + App Portal 的团队，Portkey 是首选。Helicone 居于中间：特性丰富、开源、Pro 档在价格上有竞争力，Team 档贵但解锁合规 + 无限座位组合。
想深入对比这四款方案在成本、性能、功能契合度的细节，FreeModel 聚合层是个中立的基准入口——它走同一个 OpenAI 兼容接口，并暴露四家供应商的成本 / 延迟数据，不会把你锁到任何一家。
## 常见问题

Helicone 用来做什么？ Helicone 是由 YC W23 团队开发的开源 LLM 可观测性平台。它在你的代码与 100+ LLM Provider（OpenAI、Anthropic、Google Vertex、AWS Bedrock、Azure、Cohere、Groq、Together、Fireworks、Mistral）之间加一层代理，自动记录每次请求、日志归因成本、跑 Prompt 实验、检测回归。是平台团队建设 LLM 调用分析能力时不需要自建日志流水线的标准工具。
Helicone 2026 年的价格是多少？ Helicone 共有四档。Hobby 免费，每月 10,000 次请求 + 1 GB 存储。Pro $79/月，无限座位、告警、报表、HQL 查询语言。Team $799/月，5 个组织、SOC-2 与 HIPAA 合规、专属 Slack 频道。Enterprise 定制价，含 SAML SSO、本地部署、定制 MSA、大客户折扣。高用量客户在座位费之上叠加按用量计费。
Helicone 是开源的吗？ 是的。Helicone 的 Proxy 与 AI Gateway 是 Apache-2.0 协议（GitHub: github.com/Helicone/helicone，截至 2026-07-18 验证为 5,961 stars / 630 forks）。你可以用 Docker 自部署整套平台，包括请求日志、仪表盘与 HQL 引擎。SaaS 版本是同一套代码库的托管实例，因此自部署与云端的功能保持一致。
Helicone 与 Portkey 怎么选？ 如果你的首要需求是深度请求分析、Prompt 版本管理与自部署，选 Helicone。如果你的首要需求是 AI Gateway 路由 + Guardrails + 给非技术成员用的 App Portal，选 Portkey。Helicone 的 Team 档（$799/月）比 Portkey 的 Growth 档（$199/月）贵，但开箱即用 SOC-2 + HIPAA。Helicone 是开源；Portkey 的 Gateway 是闭源 SaaS 独占。
Helicone 支持 OpenAI、Anthropic、Google Vertex 吗？ 支持。Helicone AI Gateway 是 OpenAI base URL 的直接替换——你只改一行（api_base='https://ai-gateway.helicone.ai' 或你的自部署 URL），并通过 Helicone-Auth 头传入 Provider 授权。Anthropic Claude、Google Gemini/Vertex、AWS Bedrock、Azure OpenAI、Mistral、Cohere、Groq、Together AI、Fireworks AI 都用同一行接入。每次请求都会记录完整 Prompt、输出、延迟、Token、成本与用户元数据。
什么是 HQL（Helicone 查询语言）？ HQL 是用于查询 LLM 调用日志的类 SQL 语法。它在 AI Gateway 厂商中是 Helicone 独有的——Portkey 与 Cloudflare AI Gateway 只提供 JSON 过滤或纯仪表盘。示例：\`SELECT user_id, sum(cost) FROM requests WHERE model = 'gpt-4o' AND latency > 2000 GROUP BY user_id ORDER BY cost DESC LIMIT 20\`。HQL 在 SaaS 部署中跑在 ClickHouse 上，对十亿行查询响应亚秒级。HQL 从 Pro 档（$79/月）起解锁。
Helicone 在中国大陆能用吗？ 可以，通过自部署。Helicone 的 Apache-2.0 Proxy 跑在任何 Docker 或 Kubernetes 可运行的环境——包括阿里云 ECS、腾讯云、华为云中国区节点。Proxy 用你自己的 Key 跟上游 Provider（OpenAI、Anthropic 等）通信，所以如果需要从国内访问这些 Provider，你仍需为那部分调用准备上游代理。SaaS 仪表盘 helicone.ai 在中国大陆被地理屏蔽。
## 参考资料

- Helicone，Pricing，2026-07-18：helicone.ai/pricing
- Helicone，AI Gateway 文档，2026：docs.helicone.ai
- GitHub，Helicone/helicone，5,961 stars / 630 forks / Apache-2.0，访问 2026-07-18：github.com/Helicone/helicone
- Portkey，Pricing，2026-07：portkey.ai/pricing
- LiteLLM，Repository，2026-07：github.com/BerriAI/litellm
- Cloudflare，AI Gateway pricing，2026：developers.cloudflare.com/ai-gateway
