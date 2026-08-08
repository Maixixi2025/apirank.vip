# Anyscale API 2026 测评：Ray 与 Endpoints 及 Nscale 收购

**日期：** 2026-08-08
**Slug：** anyscale-api-review-2026
**类型：** review + 新增 provider（为已有 anyscale 条目补充 reviewSections）
**状态：** published

## 文章

EN：`src/pages/tutorials/anyscale-api-review-2026.astro`
ZH：`src/pages/zh/tutorials/anyscale-api-review-2026.astro`

标题（ZH）：Anyscale API 2026 测评:Ray 与 Endpoints 及 Nscale 收购（48 字符）
描述（ZH）：105 字符

## 热点 / 为何现在写

- **Nscale 收购 Anyscale**：2026 年 7 月 30 日英伟达支持的英国 neocloud 厂商以约 **16.5 亿美元**收购 Anyscale，将 Ray + Endpoints 并入其全栈 AI 云（挪威、英国、德州、葡萄牙数据中心）。Bloomberg、SiliconANGLE、Reuters、TechCrunch、The New Stack、Latham & Watkins 等多家证实。
- **Anyscale 于微软 Azure 原生集成**（2026 年 6 月 2 日）——面向主权 AI 与可变 API 成本控制（PR Newswire）。
- Anyscale 是**真实覆盖缺口**：已在 providers.json 但**无 reviewSections**、**无测评文章**——本次为其补充 4 段 reviewSections（中英双语）并新增中英测评文章。

## Provider 条目更新

`src/data/providers.json` — `anyscale` 条目（76 家中第 22 位）：
- status → `active`
- freeTier → `$100 一次性额度 + 项目启动额度`
- 补充 freeTierEN / paidModelEN
- **4 段 reviewSections**（中英双语）：
  1. 💰 价格与方案（表格——模型 + 加速器小时定价）
  2. 🔧 API 与开发者体验（列表，7 项——接口、模型、Ray、SDK、部署、认证、SLA）
  3. 🧠 Ray 与 Nscale 收购（文本，2 段）
  4. 🌐 区域可用性与延迟（文本）
