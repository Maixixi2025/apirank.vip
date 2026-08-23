# Liquid AI LFM2.5 2026 评测：DSpark 端侧推理与开源许可定价

**厂商：** Liquid AI（liquid.ai）— id: `liquid-ai`
**日期：** 2026-08-23
**热点来源：** 2026-08-23 简报 ⭐#2（apirank）：「Hugging Face LFM2.5 系列 DSpark 草稿模型：推理速度最高提升 3.18 倍」→ huggingface.co/blog/LiquidAI/lfm25-dspark
**类型：** review + 新厂商（开源许可边缘推理）+ news-analysis（LFM2.5-DSpark）

## 选题决策
- 此前两个 apirank ⭐ 选题都已在磁盘上：⭐#1（`qwen-3-8-27b-reasoning-effort-overthinking-tokens-2026.astro`，已由 daily-article cron 于 08-23 发布）以及一个*不同的* DSpark 故事（`dspark-speculative-decoding-2026.astro` = DeepSeek 的 DSpark，不是 Liquid 的）。
- `liquid-ai` 确实不在 providers.json（本次前 84 条）。LFM2.5-DSpark 发布正是 Liquid AI 的故事——一个新鲜、独立、body 已验证的新闻钩子（2026-08-20/21，MarkTechPost / Unite.AI / GIGAZINE / TUN / finance.biggo 多源报道）。

## 已验证事实（2026-08-23 body 验证）
- **LFM2.5-DSpark**（2026-08-20 发布）：为 LFM2.5-1.2B-Instruct、LFM2.5-2.6B、LFM2.5-8B-A1B 添加投机解码草稿检查点。
  - GPU 吞吐最高 3.18×（H100：MATH500 428→1362 tok/s）；端侧最高 2.87×（Apple M4 Max）。
  - LFM2.5-2.6B 函数调用延迟平均降低 57%。
  - 输出精确无损（目标模型验证所有候选 token；贪心输出 == 目标模型本身）。
  - llama.cpp + SGLang 首日支持；集成开源。
- **商业模式：** 无托管按 token API。所有 LFM 在免版税 **LFM Open License** 下免费下载/运行/微调——公司年收入超过 1000 万美元前均可免费商用。无 copyleft（微调可私有）。研究/教育/非营利永久免费。
- **LEAP 企业版：** 商用授权 + OEM/on-prem + SLA，按部署规模定价（联系销售）。企业客户 Mercedes-Benz、Shopify。
- **模型：** LFM2.5 文本（230M/350M/1.2B-Instruct/Thinking/Base/JP/2.6B/8B-A1B MoE）、VL（450M/1.6B/3B）、LFM2（24B-A2B MoE/2.6B/700M）。350M 训练 28T tokens、<1GB 可运行。8B-A1B = 8B/1.5B active MoE、128K 上下文。LEAP SDK 跨平台（iOS/Android/JVM/Linux/Windows）。
- **公司：** 波士顿（est. 2023），约 $2.4B 估值独角兽（GetLatka 2025-11）；2026 年 8 月 NBC Boston + Business Journals 报道。
- **生态：** Hugging Face 下载 4130 万+。

## 外链（2026-08-23 全部 HTTP 200 验证）
- https://huggingface.co/blog/LiquidAI/lfm25-dspark（200）
- https://www.liquid.ai/pricing（200）
- https://www.liquid.ai/lfm-license（200）
- https://docs.liquid.ai/llms.txt（200）
- https://marktechpost.com（200）— 二手新闻源

## 内链（全部验证在磁盘 / 动态厂商路由）
- /providers/liquid-ai（新厂商详情页，自动渲染）
- /providers/groq、/providers/modal、/providers/deepseek（动态）
- /tutorials/qwen-3-8-27b-workers-ai-edge-inference-2026（边缘推理，相关）
- /tutorials/dspark-speculative-decoding-2026（DeepSeek DSpark——区分度）
- /tutorials/fireworks-ai-serverless-inference-review-2026（托管开源模型服务）
- /tutorials/cheapest-llm-api-pricing-2026（按 token 对比）

## 变更文件
- `src/data/providers.json` — 添加 `liquid-ai`（第 85 条），4 段 reviewSections EN+ZH
- `src/pages/tutorials/liquid-ai-lfm25-dspark-edge-inference-review-2026.astro`（EN）
- `src/pages/zh/tutorials/liquid-ai-lfm25-dspark-edge-inference-review-2026.astro`（ZH）
- `src/pages/tutorials/index.astro` + `src/pages/zh/tutorials/index.astro` — 新卡片（顶部）
- `drafts/zh-liquid-ai-lfm25-dspark-edge-inference-review-2026-2026-08-23.md` + en 孪生（本文件）

## 指标（已验证）
- EN 标题 51 字符 / EN 描述 148 字符 / EN 主体约 1450 词
- ZH 标题 41 字符 / ZH 描述 ~91 字符 / ZH 主体约 1500 词
- FAQ：7 组 Q&A（EN+ZH json-ld + 可见区）
- reviewSections：4（table/list/text/text）— sec3/4 EN 文本 80-130 词（129、130）
