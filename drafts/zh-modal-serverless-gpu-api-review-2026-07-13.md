---
title: "Modal API 评测 2026：Python 原生 Serverless GPU 云平台"
description: "Modal API 完整评测：Python 原生 serverless GPU 云、按 GPU 秒计费、vLLM/SGLang 一行部署、$30/月免费额度。对比 Baseten、Replicate、RunPod 定价与适用场景。"
slug: "modal-serverless-gpu-api-review"
provider: "modal"
published: true
date: "2026-07-13"
type: "review"
---

# Modal API 评测 2026：开源 LLM 自托管的 Python 原生 Serverless GPU 云

Modal 是一家位于旧金山的开发者基础设施公司，2026 年做出了 Python 圈最好用的 GPU 上线路径。它**不是** OpenAI / Anthropic 那种模型 API——Modal 是底层平台：你自己选开源模型（Llama 4、Qwen 3、DeepSeek V4）、选 GPU（T4 到 B300），几行代码就能交付一个 HTTPS 接口。定价是**按 GPU 秒计费、零 idle 费用**，对波动型 / 不可预测的 AI 工作负载是当下成本最优解。

如果你正在评估"哪里托管开源 LLM 才划算"，或者你已经受够了按 token 付费的模型 API 想拿回 GPU 级控制权，Modal 是 2026 年最值得认真考虑的平台。

## TL;DR

- **Modal 是 serverless GPU 云，不是模型 API**。模型自备（vLLM / SGLang / TensorRT-LLM / 原生 PyTorch 都可以），Modal 帮你搞定容器、扩缩容、调度、HTTPS。
- **按 GPU 秒计费，零 idle 成本**。H100 $0.001097/秒、A100 80GB $0.000694/秒、T4 $0.000164/秒。一个 Llama 4 70B 推理平均 1.8 秒，H100 上约 $0.00197。
- **Starter 计划免费 + $30/月 计算额度**。约等于 27,300 秒 T4 推理，或每月约 30K 次轻量请求。真正生产从 Team 计划（$250/月 + $100 额度）起步。
- **冷启动 1-3 秒**（用 warm pool 技巧可压到 200ms 内）。不适合 <200ms 的实时低延迟，但聊天后端、批处理、异步 agent 都没问题。
- **最适合：** 自托管 Llama 4 / Qwen 3 / DeepSeek V4 等开源模型。**最不适合：** 极致低延迟实时场景，或能干净塞进托管模型 API 的工作负载。
- **交叉对比：** 与 Baseten（2026-07-08 评测）直接对比——Modal 赢在开发体验和免费额度；Baseten 赢在 Dedicated Deployments 长期常驻生产。

## 为什么 Modal 在 2026 年值得认真看

三股力量在 2026 年汇聚到一起，让 serverless GPU 真正成为生产选项：

1. **开源模型质量追上来了。** Llama 4 70B、Qwen 3 235B、DeepSeek V4 在大多数推理基准上离 GPT-5.6 / Sonnet 5 只差 3-5 个百分点，自托管的每 token 成本却只是头部模型 API 的零头。
2. **GPU 现货价格稳了。** 经过 2024-2025 的 H100 短缺期，二手 A100 市场降温，Modal 可以把这部分让利传导出去。
3. **Serverless 开销降下来。** Modal 的容器启动时间已经稳定在 2 秒内，加 warm-pool 可以压到 200ms 以内。五年前 Lambda Labs、CoreWeave 这块要 30+ 秒。

结果：一个开发者可以在一个下午交付一个 Llama 4 推理 API，峰值扩到每秒数千请求，流量静默时一分钱不花。

## Modal 定价（2026-07-13 实测）

数据来源：modal.com/pricing（2026-07-13 实时抓取）。

### GPU 按秒费率

| GPU | $/秒 | 折合 $/小时 | 适用场景 |
|---|---:|---:|---|
| Nvidia B300 | $0.001972 | $7.10 | 前沿训练、大批量推理 |
| Nvidia B200 | $0.001736 | $6.25 | 前沿训练、大批量推理 |
| Nvidia H200 | $0.001261 | $4.54 | LLM 训练，141GB HBM3e |
| Nvidia H100 | $0.001097 | $3.95 | LLM 推理（甜区） |
| Nvidia RTX PRO 6000 | $0.000842 | $3.03 | 成本优化的 LLM 推理 |
| Nvidia A100 80GB | $0.000694 | $2.50 | LLM 推理（70B+ 性价比之王） |
| Nvidia A100 40GB | $0.000583 | $2.10 | LLM 推理（≤40B 模型） |
| Nvidia L40S | $0.000542 | $1.95 | 视觉、图像生成 |
| Nvidia A10 | $0.000306 | $1.10 | 图像生成、中型 LLM |
| Nvidia L4 | $0.000222 | $0.80 | 小型 LLM、embedding |
| Nvidia T4 | $0.000164 | $0.59 | 小模型、开发测试 |

### CPU 与内存

- CPU（物理核，2 vCPU 等效）：**$0.0000131/核/秒**
- 内存：**$0.00000222/GiB/秒**
- 每个容器最低 0.125 核

### 存储与 Sandbox

- 卷存储：**$0.09/GiB/月**（每月前 1 TiB 免费）
- Sandbox：专用计算费率（略高于 Functions，但支持突发）

### 订阅计划

| 计划 | 月费 | 包含额度 | 容器数 | GPU 并发 | 日志保留 |
|---|---:|---:|---:|---:|---|
| **Starter** | $0 | $30/月 | 100 | 10 | 1 天 |
| **Team** | $250 | $100/月 | 1000 | 50 | 30 天 |
| **Enterprise** | 自定义 | 自定义 | 自定义 | 自定义 | 自定义 |

附加费率：
- **区域选择**：基础价 1.5x – 1.75x
- **非抢占执行**：基础价 3x
- **云市场**：可在 AWS / GCP marketplace 上消耗已承诺消费

### 真实成本样例

- **Llama 4 8B on T4**，平均 200ms/请求：约 $0.0000328/请求
- **Llama 4 70B on A100-80GB**，平均 1.8 秒：约 $0.00125/请求
- **Qwen 3 235B on 2x H100**，平均 5 秒：约 $0.011/请求
- **Stable Diffusion XL on L40S**，平均 3 秒：约 $0.00163/张
- **Whisper Large V3 on A10**，30 秒音频、5 秒计算：约 $0.00153/转录

和模型 API 对照，生产规模下：
- Llama 4 70B via Together AI：~ $0.88/M 输入 token → 1K token 请求 ~ $0.00088
- Llama 4 70B via Modal A100-80GB：1K token 生成约 $0.00125（接近，但 Modal 在长上下文场景更透明）

## Modal 的 API 形态

Modal 围绕三个原语展开：

### 1. `@app.function()` — Pythonic serverless 函数

核心抽象。给任何 Python 函数加 `@app.function(gpu="H100")` 就完事：

```python
import modal

app = modal.App("example-llm")

@app.function(gpu="H100", memory=8192)
def generate(prompt: str) -> str:
    from vllm import LLM, SamplingParams
    llm = LLM(model="meta-llama/Llama-4-70B-Instruct")
    output = llm.generate([prompt], SamplingParams(max_tokens=512))
    return output[0].outputs[0].text
```

`modal deploy` 一下，Modal 自动打包代码、构建容器、起 HTTPS 接口。

### 2. `@app.cls()` — 长生命周期有状态容器

适合希望模型一直驻内存（避免冷启动成本）的场景：

```python
@app.cls(gpu="A100-80GB", memory=8192, container_idle_timeout=300)
class Llama4Endpoint:
    @modal.enter()
    def load_model(self):
        from vllm import LLM
        self.llm = LLM(model="meta-llama/Llama-4-70B-Instruct")

    @modal.method()
    def generate(self, prompt: str) -> str:
        return self.llm.generate([prompt])[0].outputs[0].text
```

`container_idle_timeout=300` 让容器在最后一次请求后保持 5 分钟，消除聊天后端波动流量的冷启动惩罚。

### 3. `@app.webhook()` 与 `@app.asgi()` — HTTPS 接口

把任何函数暴露为 HTTP 端点。ASGI 支持意味着 FastAPI、Flask、LitServe 等所有 Python Web 框架都直接可用。

### 4. Sandboxes（沙箱）

`modal.Sandbox()` 创建一个可编程 shell 进入的临时 Linux 容器。适合运行任意代码（Codex 风格的 agent 后端）、处理上传文件、安全执行用户提交的脚本。

### 5. Volumes 和 Dict

- **Volumes**：挂载到容器的持久磁盘（模型权重、数据集缓存的好选择）
- **Dict**：分布式 KV 存储，用作缓存、限流状态、工作节点间协调

## 30 分钟上线 Llama 4 接口的完整流程

### 1. 安装与认证

```bash
pip install modal
modal token new  # 浏览器 OAuth
```

### 2. 创建 app 文件（`llama4_app.py`）

```python
import modal
from fastapi import FastAPI

app = modal.App("llama4-70b")
web_app = FastAPI()

image = modal.Image.debian_slim().pip_install(
    "vllm==0.7.3", "fastapi", "uvicorn"
)

@app.cls(
    gpu="A100-80GB",
    memory=8192,
    container_idle_timeout=300,
    image=image,
)
class Llama4:
    @modal.enter()
    def load(self):
        from vllm import LLM, SamplingParams
        self.llm = LLM(model="meta-llama/Llama-4-70B-Instruct")
        self.params = SamplingParams(max_tokens=512, temperature=0.7)

    @modal.method()
    def generate(self, prompt: str) -> str:
        out = self.llm.generate([prompt], self.params)
        return out[0].outputs[0].text

@web_app.post("/v1/chat")
async def chat(body: dict):
    prompt = body["messages"][-1]["content"]
    result = Llama4().generate.remote(prompt)
    return {"choices": [{"message": {"role": "assistant", "content": result}}]}
```

### 3. 部署

```bash
modal deploy llama4_app.py
```

Modal 大约 90 秒返回一个 HTTPS URL（首次部署慢因为要构建镜像；后续部署更快）。

### 4. 测试

```bash
curl -X POST https://your-app.modal.run/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "法国首都是什么？"}]}'
```

从 `pip install` 到能用的 HTTPS 接口总耗时：首次部署约 30 分钟，镜像缓存后约 5 分钟。

## Modal 适合与不适合的场景

### 适合

- **自托管开源 LLM**（Llama 4 / Qwen 3 / DeepSeek V4 / Mistral），需要完全掌控微调、system prompt、按请求路由
- **波动型工作负载**：流量一波一波，Modal 在两波之间缩到零、不收一分钱
- **批量推理**（图像生成、embedding、批量分类）—— 成本主要由 GPU 秒数主导
- **Agent 后端**：每个任务一个隔离 Sandbox（类似 Claude Code 的执行模型）
- **ML 训练与微调** —— Modal 支持多 GPU 训练，费率同按秒

### 不适合

- **极致低延迟实时**（p99 < 200ms）—— 冷启动 1-3 秒，即使加 warm pool。用 Groq、Cerebras 这种专用推理服务商替代。
- **能干净塞进托管模型 API 的工作负载** —— 只需要 GPT-5.6 / Sonnet 5，按 token 付费更简单。
- **大量 prompt cache 工作负载** —— Modal 没有 prompt cache 概念。长上下文重复前缀（Anthropic 的甜区）在这里更贵。
- **国内数据驻留合规** —— Modal 基础设施在 AWS / GCP 海外，没有 CN 区域。

## Modal vs Baseten vs Replicate vs RunPod

| 维度 | Modal | Baseten | Replicate | RunPod |
|---|---|---|---|---|
| GPU 计费 | 按秒 | 按秒 | 按秒 | 按小时或按秒 |
| 免费层 | $30/月 | 无（付费） | 有限 | 注册送 $5 |
| 冷启动 | 1-3 秒 | 2-5 秒 | 5-15 秒（冷） | 手动（常驻） |
| 暖池 | 是（`container_idle_timeout`） | 是（Dedicated） | 否 | 手动 |
| 常驻预留 | 否（可抢占） | 是（Dedicated） | 是（常驻模型） | 是 |
| 自托管自定义模型 | 是（vLLM / SGLang / 原生） | 是（Truss） | 是（Cog） | 是（任意） |
| Sandbox/执行 | 是（`modal.Sandbox`） | 有限 | 否 | 是 |
| 开源框架 | 无（私有） | Truss | Cog | 无 |
| CN 区域 | 否 | 否 | 否 | 否 |
| SOC 2 | 是 | 是 | 是 | 是 |

2026 年选型矩阵：

- **Modal**：开发体验最好、免费额度最好、波动负载和独立开发者的首选
- **Baseten**：Dedicated Deployments 常驻生产场景的最佳选择
- **Replicate**：社区模型目录（图像、音频、视频）最丰富
- **RunPod**：裸 GPU 租赁 + 长跑训练任务的最佳选择

## 上 Modal 生产前的 4 项验证

部署完之后，上真实流量前，先把这 4 项过一遍：

1. **冷启动延迟分布。** `modal run --quiet llama4_app.py` 冷唤醒，然后测 100 次首 token 时延。预期 p50 ~1.5 秒、p99 ~3 秒（首次部署）；启用暖池后 p99 应该压到 ~200ms。
2. **并发扩容。** 瞬时打 1000 并发请求，确认 Modal 把容器扩到你配置的 `max_containers`（Starter 默认 100、Team 默认 1000）。
3. **单次请求成本。** 用 Modal 内置的指标面板（"Apps" → 你的 app）确认 GPU 秒/请求与模型假设一致。
4. **崩溃恢复。** 中途杀一个容器——Modal 应该自动重启并继续服务。验证方法是盯日志 + 确认请求没有丢。

## FAQ

### Modal 是模型 API 提供商吗？

不是。Modal 是 serverless GPU 基础设施。你自备模型（vLLM、SGLang、PyTorch、TensorRT-LLM）。类比是 AWS Lambda 而不是 OpenAI。

### 一个小型聊天机器人每月成本多少？

Starter 计划（$0/月 + $30 计算额度）大约能覆盖 30K 次 T4 请求 或 3K 次 A100-80GB 请求。~1K 请求/天的聊天机器人塞在免费层里就够。超出后，轻量生产 $50-200/月。

### 国内能用 Modal 吗？

不能直连。Modal 基础设施在 AWS / GCP 海外。需要代理，或者通过国内可达的编排层路由（有些团队走阿里云国际版网关）。

### Modal 有 prompt caching 吗？

没有。Modal 按 GPU 秒计费，跟输入重复度无关。长上下文重复前缀场景，用模型 API 的 prompt cache（Anthropic、OpenAI、Google）更便宜。

### Modal 对比 AWS Lambda / GCP Cloud Run？

Lambda 和 Cloud Run 在合理价格下只支持 CPU。GPU 推理只有 Modal、Baseten、Replicate、RunPod、CoreWeave 这些是真正可用的选择。

### 能在 Modal 上花 AWS / GCP 已承诺额度吗？

可以。Modal 与 AWS / GCP marketplace 打通，企业客户可以用已承诺消费抵扣 Modal 计算费用。

### HIPAA 合规？

Modal 在 Enterprise 计划上 HIPAA 兼容，提供审计日志、RBAC、SSO、BAA。

### 支持多 GPU 推理吗？

支持。`gpu="H100:2"` 或 `gpu="A100-80GB:4"` 申请多 GPU。Modal 自动处理 vLLM / SGLang 的张量并行和流水线并行。

### 代码有内存泄漏怎么办？

Modal 在 `container_idle_timeout`（默认 5 分钟，可配置）后回收容器。只要内存泄漏没在 idle 窗口内 OOM 整个容器，就没事。

### 能部署非 Python 代码吗？

Python SDK 是主入口。你可以从 `@modal.enter()` 方法里跑任何 Linux 进程（Node.js / Go / Rust），但编排层是 Python-first。

---

**结论：** Modal 是 2026 年开源 LLM 生产化最顺手的工具。免费 $30/月额度覆盖独立开发者工作负载；Team 计划（$250/月）是生产起步线。如果你已经受够托管模型 API 想拿回 GPU 级控制，又不想扛 Kubernetes 的运维负担，Modal 是最值得评估的平台。