# Archived draft: Tavily API review (ZH mirror)

This is the archived source for `src/pages/zh/tutorials/tavily-api-review.astro`.
Published: 2026-07-31 (ZH mirror added alongside providers.json entry; EN review was already published 2026-06-28).

Title: Tavily 2026 评测：AI Agent 专用搜索 API
Description (112 chars): Tavily 2026 评测：LangChain 默认搜索 API。1,000 calls/月免费、$0.008/credit 起、/research 多步代理、MCP server。vs Jina/Exa/SerpAPI。

Key sections (10 H2 + FAQ with 10 questions):
- TL;DR
- 为什么 Tavily 在 2026 年重要
- Tavily 端点目录（2026 年 6 月）
- Tavily 价格：credits 在实践中如何工作
- Search 端点实际返回什么
- Tavily 与 Jina AI、Exa、SerpAPI 对比
- 生产环境 Tavily：必须知道的运维坑
- Research 端点：何时用它、何时自建
- Tavily MCP server 怎么样？
- 该用 Tavily 还是别的 Provider？
- Tavily 的数据保留策略是什么？
- 能自托管 Tavily 吗？
- Tavily 怎么处理速率限制和配额超额？
- Tavily 与带浏览能力的 LLM 有什么区别？
- FAQ
- 最终结论

Sources verified 2026-07-31:
- https://tavily.com/pricing (Free 1000 credits/Pay-as-you-go $0.008/credit)
- https://tavily.com/ (Series A $25M, Trusted by 2M+ developers, MCP Databricks/IBM WatsonX/JetBrains)
- https://docs.tavily.com/ (6 endpoints, Research $0.04/call)

Companion providers.json change:
- Tavily entry added as 73rd provider (id=tavily, category=aggregator)
- 30 fields: id/name/nameCn/category/website/apiDocs/affiliateUrl/affiliateAvailable/models/modelCount/pricing+pricingEN/freeTier+EN/paidModel+EN/availabilityCN+EN/speedRank/priceRank/overallRank/highlights+EN/cons+EN/bestFor+EN/status/addedDate/source
- Verified against live pricing page (curl 2026-07-31, Free 1000 credits + Pay-as-you-go $0.008/credit confirmed)