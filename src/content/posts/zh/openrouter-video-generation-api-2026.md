---
title: "OpenRouter 视频生成 API 2026 完整指南：一个端点调用 26 个视频模型"
description: "OpenRouter 新推出的 /api/v1/videos 异步端点统一接入了 Seedance、Veo、Wan、Sora 2、Kling、Runway 等 26 个视频模型。价格区间 $0.03/秒 到 $0.60/秒，一行代码切换模型。"
pubDate: "2026-08-26"
provider: openrouter
category: integration-guide
featured: true
---

# OpenRouter 视频生成 API 2026 完整指南

2026 年 8 月 25 日，OpenRouter 上线了一个统一的异步端点 `POST /api/v1/videos`，将 **26 个视频生成模型**集中托管——覆盖字节跳动的 Seedance、谷歌的 Veo、OpenAI 的 Sora 2、阿里云的 Wan、Runway、Kling、HeyGen、Black Forest Labs 的 FLUX 以及 MiniMax 的 Hailuo。在此之前，要给应用添加视频生成能力意味着每个供应商都要接一套独立的 SDK，每套都有自己的认证、请求格式、任务状态、轮询节奏和下载 URL。OpenRouter 的做法把这一切压缩成了一个工作流：提交任务 → 轮询 `polling_url` → 拉取完成的 MP4。

本文基于 OpenRouter 官方 2026 年 8 月 25 日发布的指南、当日抓取的 `/api/v1/videos/models` 在线目录（26 个模型）以及各模型返回的 `pricing_skus` 价格表。相关事实——端点路径、模型标识符、每秒价格、轮询逻辑、Webhook 负载——都可以从这两个来源复现。

## 为什么是异步 API，而不是普通的阻塞调用

典型的文本补全 API 在 200-800 毫秒内返回。典型的图像生成 API 在 1-4 秒内返回。**视频生成是第一个生成时间经常超过单次 HTTP 请求超时容忍度的 API 类别**。OpenRouter 的指南将 30 秒到几分钟的生成时长列为常见情况。在这种时长下保持 TCP 连接是脆弱的：Serverless 平台（Cloudflare Workers、AWS Lambda）的执行时长上限是 30 秒到 15 分钟；企业代理和负载均衡器在 60-300 秒后闲置超时；移动网络在 30-60 秒无响应后断开。

异步模式是教科书级别的修复方案：把提交和完成分开。你提交一个任务，拿到一个 ID，然后轮询任务直到状态变成 `completed`，最后下载资源。如果你的进程在轮询中途崩溃，任务 ID 在服务端持久存在，你可以从任何设备恢复跟踪。

同步替代方案——打开流式 WebSocket 接收模型逐帧产生的数据——在某些模型上存在，但每个供应商都需要定制传输层，并且无法跨进程重启存活。OpenRouter 选择的是**持久化优于流式**的权衡，这对 Serverless 和批量场景是正确的选择。

## 价格：$0.03/秒 到 $0.60/秒，分辨率和音频是两大成本轴

`/api/v1/videos/models` 的完整价格目录返回每个模型的 `pricing_skus`。大多数模型按**时长-秒数**在特定分辨率档位计费；部分按**视频 token** 计费（Seedance 2.0 系列）或**兆像素-秒**计费（FLUX Video Upscale）。下面是一张可比较的价格表，覆盖主流模型，按 720p/1080p 档位归一化为每秒输出美元成本：

| 模型 | 计费模式 | 720p/1080p 价格 | 4K 档 | 支持音频 |
|---|---|---:|---|:---:|
| Veo 3.1 | $0.20/秒（无音频）/ $0.40/秒（音频） | $0.20-0.40/秒 | $0.40-0.60/秒 | ✅ |
| Veo 3.1 Fast | $0.10/秒（无音频）/ $0.12/秒（音频） | $0.08-0.10/秒 | $0.25-0.30/秒 | ✅ |
| Veo 3.1 Lite | $0.05/秒（无音频）/ $0.08/秒（音频） | $0.03-0.05/秒 | — | ✅ |
| Sora 2 Pro | $0.30-0.50/秒 | $0.30（720p）/ $0.50（1080p） | — | ❌ |
| Seedance 2.5 | video_tokens: $0.0000107/token | ~$0.18/秒 | — | ✅ |
| Seedance 2.0 | video_tokens: $0.000007/token | ~$0.13/秒 | $0.000004/token | ✅ |
| Seedance 2.0 Fast | video_tokens: $0.0000042/token | ~$0.08/秒 | — | ✅ |
| Seedance 2.0 Mini | video_tokens: $0.0000035/token | ~$0.07/秒 | — | ✅ |
| Seedance 1.5 Pro | video_tokens: $0.0000024/token | ~$0.05/秒 | — | ✅ |
| Wan 3.0 | $0.05-0.10/秒 | $0.10（720p）/ $0.20（1080p） | — | ✅ |
| Wan 2.7 | $0.10/秒 | $0.10/秒 | — | ❌ |
| Wan 2.6 | $0.04-0.08/秒 | $0.08（720p）/ $0.12（1080p） | — | ❌ |
| Kling v3.0 Pro | $0.112/秒（+$0.056 音频） | $0.112/秒 | $0.112（1080p） | ✅（额外 $0.056/秒） |
| Kling v3.0 Standard | $0.084/秒（+$0.042 音频） | $0.084/秒 | $0.084（1080p） | ✅ |
| Kling Video O1 | $0.112/秒 | $0.112/秒 | — | ❌ |
| Runway Gen-4.5 | $0.12/秒 | $0.12/秒 | — | ❌ |
| Runway Aleph 2.0 | $0.28/秒，最低 $0.56 | $0.28/秒 | — | ❌ |
| Grok Imagine Video 1.5 | $0.08-0.14/秒 | $0.08（480p）/ $0.14（720p）/ $0.25（1080p） | — | ❌ |
| Grok Imagine Video | $0.05-0.07/秒 | $0.05（480p）/ $0.07（720p） | — | ❌ |
| MiniMax H3 | $0.13/秒 + $0.04/参考图 | $0.13/秒 | — | ❌ |
| MiniMax Hailuo 2.3 | $0.0817/秒 | $0.0817/秒 | — | ❌ |
| HeyGen Avatar IV | $0.05/秒 | $0.05/秒 | — | ❌ |
| HappyHorse 1.1 | $0.10-0.13/秒 | $0.0988（720p）/ $0.1278（1080p） | — | ❌ |
| FLUX Video Upscale | $0.075-0.105/兆像素-秒 | —（仅放大） | — | ❌ |
| FLUX.3 Video | $0.17-0.53/秒 | $0.17（720p）/ $0.29（1080p） | $0.41-0.53/秒 | ❌ |

来源：`https://openrouter.ai/api/v1/videos/models`，抓取时间 2026 年 8 月 26 日。`pricing_skus` 返回为字符串；对于基于 token 的模型（Seedance），上表中的数字是基于 5 秒片段和视频 token → 物理秒换算的近似值。四位小数精度应视为单价，而非每次生成的总额。

头条数字：**Veo 3.1 Lite $0.03-0.05/秒是带音频的最便宜 720p 模型**，**Wan 2.6 $0.04-0.08/秒是不带音频的最便宜 720p 模型**。高端段，**Sora 2 Pro $0.30-0.50/秒 和 Veo 3.1 $0.40-0.60/秒 比预算档贵 6-15 倍**（同等分辨率下）。

一段带音频的 5 秒 1080p 视频片段价格从 **$0.40（Wan 2.6）** 到 **$3.00（Veo 3.1 4K 音频）** 到 **$2.50（Sora 2 Pro）**。在大多数供应商上，按**每段 $1-2** 做预算估算比较现实。

## 已验证的端点行为

### 提交任务

唯一的提交端点是 `POST https://openrouter.ai/api/v1/videos`。请求体是 JSON 格式，包含 `model`（必填）和 `prompt`（文本到视频时必填）。支持图生视频的模型在提供帧图像时可以省略 `prompt`。可选字段：`duration`（秒）、`resolution`（`480p` / `720p` / `1080p` / `4k`，取决于模型）、`aspect_ratio`（`16:9` / `9:16` / `1:1` / `4:3` / `3:4` / `21:9` / `9:21`，取决于模型）、`generate_audio`（布尔值，仅部分模型支持）、`seed`（整数，可复现）、`callback_url`（HTTPS Webhook 目标），以及用于模型特定参数的 `provider.options` 透传块。

已验证的请求格式（来自 OpenRouter 教程）：

```bash
curl "https://openrouter.ai/api/v1/videos" \
  -H "Authorization: Bearer $OPENR...EY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bytedance/seedance-2.0",
    "prompt": "A paper boat drifting down a rain-slicked gutter at night, neon reflections, slow tracking shot, cinematic lighting",
    "duration": 4,
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "generate_audio": false
  }'
```

成功提交返回 **HTTP 202 Accepted** 以及任务封装：

```json
{
  "id": "job-abc123",
  "status": "pending",
  "polling_url": "https://openrouter.ai/api/v1/videos/job-abc123"
}
```

HTTP 202（而非 200）是正确的信号——资源已被**接受**进入异步处理流程，尚未**完成**。立即持久化 `id`。如果你的进程重启，这个 ID 让你可以恢复跟踪，无需重新提交并支付第二次生成费用。

### 轮询任务

`polling_url` 与 `GET https://openrouter.ai/api/v1/videos/{id}` 相同——文档明确指出这一点，让应用可以仅根据任务 ID 构造 URL。任务会经历以下文档化状态：

| 状态 | 含义 |
|---|---|
| `pending` | 已接受，等待运行 |
| `in_progress` | 供应商正在生成 |
| `completed` | 视频可以下载 |
| `failed` | 生成失败（响应体中包含错误） |
| `cancelled` | 任务被取消 |
| `expired` | 任务超过允许生命周期 |

将 `completed` 视为成功出口。将 `failed`、`cancelled`、`expired` 视为终态错误。其他任何状态（或轮询中的连接错误）应触发轮询重试，而非新任务的提交——模型可能仍在生成。教程提供了一个防御性的 Python 轮询循环，间隔 30 秒，上限 1 小时，处理所有文档化的终态，并区分轮询失败和生成失败。

推荐的轮询间隔是 **30 秒**；更快地轮询不会让供应商更快完成。1 小时超时是操作建议，而非端点的文档化合约。

### 下载完成的视频

当 `status: "completed` 到达时，响应包含一个填充好的 `unsigned_urls` 数组。尽管名称如此，这些 URL 需要 `Authorization: Bearer` 请求头——它们是认证的内容端点，不是预签名 URL：

```bash
curl "https://openrouter.ai/api/v1/videos/job-abc123/content?index=0" \
  -H "Authorization: Bearer $OPENR...EY" \
  --output out.mp4
```

`index` 查询参数默认为 `0`，仅在模型从单次生成返回多个视频输出时需要更改。除非响应 `Content-Type` 标头另有说明，否则保存为 `mp4` 文件。

### 一行切换模型

统一端点的核心承诺：修改模型标识符即可改变模型，其他不变。提交、轮询和下载函数保持完全相同。

```python
# Seedance
MODEL = "bytedance/seedance-2.0"
# Veo
# MODEL = "google/veo-3.1"
# Wan
# MODEL = "alibaba/wan-2.7"

job = submit_video(model=MODEL, prompt=PROMPT)
completed_job = poll_video(job)
download_video(completed_job)
```

**不会随之迁移的是每个可选设置**。在 Seedance 2.0、Veo 3.1 和 Wan 2.7 之间验证的共享配置是 `{duration: 4, resolution: "720p", aspect_ratio: "16:9", generate_audio: false}`。超出这个组合，模型就会出现差异：

- **Veo 3.1** 当前支持 4、6、8 秒时长。
- **Seedance 2.0** 当前支持 4-15 秒时长以及更宽的宽高比范围。
- **Wan 2.7** 当前支持 2-10 秒时长以及 720p 或 1080p 分辨率。

5 秒的请求在 Seedance 和 Wan 上通过验证，但在 Veo 上失败。推荐的防御模式是在提交前查询 `/api/v1/videos/models`，读取所选模型支持的 `durations`、`resolutions` 和 `aspect_ratios`，然后在本地验证。

## 模型特定透传参数

每个模型在 `/api/v1/videos/models` 响应中暴露 `allowed_passthrough_parameters`。这些是你可以在 `provider.options` 透传块内发送的键，该块按**供应商 slug**（而非模型 slug）索引。例如：

```json
{
  "provider": {
    "options": {
      "google-vertex": {
        "parameters": {
          "negativePrompt": "blurry, low-resolution",
          "enhancePrompt": true
        }
      }
    }
  }
}
```

只有与所选供应商相关的参数会被转发；无法识别的键会被丢弃。从在线目录验证的示例：

- **Veo（google-vertex）**：`negativePrompt`、`enhancePrompt`
- **Wan**：`negative_prompt`、`prompt_extend`
- **HeyGen Avatar IV**：`voice_id`、`voice_settings`、`motion_prompt`、`expressiveness`、`fit`、`remove_background`、`background`、`caption`、`title`

这些参数提供了统一端点刻意不隐藏的模型特定行为。从 Veo 切换到 Wan 意味着重写透传块，因为参数名称和有效值都会改变。

## 生产规模下的 Webhook 投递

对于脚本、原型和数十个并发任务，轮询效果不错。对于数百个任务，轮询在不更快通知应用的情况下会消耗轮询端的请求预算。OpenRouter 通过提交时的 `callback_url` 字段支持**按请求的 Webhook 投递**：

```json
{
  "model": "bytedance/seedance-2.0",
  "prompt": "A paper boat drifting through neon reflections",
  "duration": 4,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "callback_url": "https://example.com/webhooks/openrouter-video"
}
```

Webhook 在任务达到任何终态时触发。每个投递都包含一个 `X-OpenRouter-Idempotency-Key` 头——例如 `job-abc123-completed`——接收处理器在处理事件前应存储该值。如果 OpenRouter 重试 Webhook（对非 2xx 响应会这样做），幂等键让处理器能够识别重复并避免下载两次视频。

如果配置了签名密钥，Webhook 请求还包含 `X-OpenRouter-Signature` 头。**在生产环境中处理负载前始终验证此签名**——没有它，任何人都可以 POST 到你的回调 URL 并触发下载。

你也可以配置**工作区默认**回调 URL，让每次提交都继承它。请求级别的 `callback_url` 覆盖工作区默认。

## 已验证的限制和已知陷阱

- **零数据保留（ZDR）不支持**视频生成。OpenRouter 在教程 FAQ 中明确确认：异步检索步骤要求生成的输出被短暂保留以便下载，因此强制执行 ZDR 的账户不会被路由到视频生成。如果你有企业数据驻留合约要求 ZDR，视频不能作为生成渠道。
- **音频能力差异巨大**。26 个模型中只有 9 个支持 `generate_audio: true`；其余的会拒绝该字段。上面的价格表标注了哪些模型支持音频。
- **分辨率支持差异巨大**。有些模型仅支持 `720p`，有些支持 `480p`/`720p`/`1080p`，只有 Veo 3.1 支持 `4k`。查询 `/api/v1/videos/models` 而不是硬编码分辨率。
- **30 秒轮询间隔是操作建议，不是合约**。根据你自己的工作负载调整。更快地轮询不会加速生成。
- **轮询请求失败 ≠ 生成失败**。如果在轮询超时后重新提交提示，你可能最终会得到两段视频和两次费用，对应一个用户请求。始终持久化任务 ID 并对现有任务重试状态，而不是重新生成。
- **`unsigned_urls` 是误导性名称**。这些 URL 不是预签名的；你必须发送 `Authorization: Bearer` 头才能下载。
- **某些模型支持参考图像和 `first_frame`/最后一帧输入，有些则不支持**。每个模型条目上的 `supported_frame_images` 字段告诉你接受什么。Veo 在目录中未列出任何帧图像支持；Seedance 2.0 Mini 支持首末帧控制以及多模态参考输入。

## Curl 示例：使用 Seedance 2.0 的端到端流程

```bash
# 1. 提交任务
RESPONSE=$(curl -s -X POST "https://openrouter.ai/api/v1/videos" \
  -H "Authorization: Bearer $OPENR...EY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "bytedance/seedance-2.0",
    "prompt": "A paper boat drifting down a rain-slicked gutter at night, neon reflections, slow tracking shot, cinematic lighting",
    "duration": 4,
    "resolution": "720p",
    "aspect_ratio": "16:9",
    "generate_audio": false
  }')

JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "任务 ID: $JOB_ID"

# 2. 轮询直到完成
while true; do
  STATUS=$(curl -s "https://openrouter.ai/api/v1/videos/$JOB_ID" \
    -H "Authorization: Bearer $OPENR...EY" | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
  echo "状态: $STATUS"
  case "$STATUS" in
    completed) break ;;
    failed|cancelled|expired) echo "终态错误: $STATUS"; exit 1 ;;
  esac
  sleep 30
done

# 3. 下载
curl -s "https://openrouter.ai/api/v1/videos/$JOB_ID/content?index=0" \
  -H "Authorization: Bearer $OPENR...EY" \
  --output "out_${JOB_ID}.mp4"
echo "已保存 out_${JOB_ID}.mp4"
```

## Python 示例：带 Webhook 回退的完整工作流

```python
import os, time, requests
from urllib.parse import urljoin

API_KEY = os....RL = "https://openrouter.ai/api/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

TERMINAL_ERROR_STATES = {"failed", "cancelled", "expired"}


def submit_video(model, prompt, **opts):
    response = requests.post(
        f"{BASE_URL}/videos",
        headers=HEADERS,
        json={"model": model, "prompt": prompt, **opts},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def poll_video(job, interval=30.0, timeout=3600.0):
    polling_url = urljoin("https://openrouter.ai", job["polling_url"])
    deadline = time.monotonic() + timeout
    current = job
    while True:
        status = current["status"]
        print(f"状态: {status}")
        if status == "completed":
            return current
        if status in TERMINAL_ERROR_STATES:
            raise RuntimeError(f"任务以状态 '{status}' 结束: {current.get('error')}")
        if time.monotonic() >= deadline:
            raise TimeoutError(f"任务 {job['id']} 在 {timeout} 秒内未完成")
        time.sleep(interval)
        response = requests.get(
            polling_url,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30,
        )
        response.raise_for_status()
        current = response.json()


def download_video(job, output_path="out.mp4", index=0):
    unsigned_urls = job.get("unsigned_urls") or []
    download_url = (
        unsigned_urls[index]
        if index < len(unsigned_urls)
        else f"{BASE_URL}/videos/{job['id']}/content?index={index}"
    )
    response = requests.get(
        download_url,
        headers={"Authorization": f"Bearer {API_KEY}"},
        stream=True,
        timeout=120,
    )
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return output_path


# 端到端
job = submit_video(
    model="bytedance/seedance-2.0",
    prompt="A paper boat drifting down a rain-slicked gutter at night",
    duration=4,
    resolution="720p",
    aspect_ratio="16:9",
    generate_audio=False,
)
print(f"已提交任务 {job['id']}")
completed = poll_video(job)
print(f"最终费用: ${completed.get('usage', {}).get('cost', 'unknown')}")
download_video(completed, "boat.mp4")
```

完成任务的响应可以包含一个 `usage` 块，显示实际费用：

```json
{
  "usage": {
    "cost": 0.5,
    "is_byok": false
  }
}
```

`is_byok` 标志表示请求是按你自己的供应商密钥计费（自带密钥，OpenRouter 转发调用且不加价），还是按你的 OpenRouter 信用余额计费。将你从 `pricing_skus` 构建的估算与实际 `cost` 进行比较，以发现因更高分辨率、更长时长、添加音频或切换模型导致的意外变化。

## 总结

**OpenRouter 的视频 API 是首个覆盖生产视频生成现实价格/质量跨度的单端点抽象**。26 个模型足以对预算与旗舰输出进行 A/B 测试，而统一的提交/轮询/下载循环意味着实验成本以 API 分钟数计算，而非集成周数。

**昂贵的模型只值得用于核心内容**。Veo 3.1 $0.40/秒 是产品发布预告片的正确选择；但对于批量 UGC 渲染，Wan 2.6 $0.04-0.08/秒 在相同预算下可产出 5-10 倍数量的相当 720p 输出，是错误的选择。

**模型特定选项是统一性的代价**。从 Veo 切换到 Wan 意味着重写 `provider.options` 块。从 Seedance 2.0 切换到 Seedance 2.5 只改变模型标识符。"易于切换"的供应商（字节跳动 Seedance 系列）与"每模型 API"的供应商（谷歌 Veo、HeyGen、Kling）之间的不对称是真实的，值得纳入你的模型选择策略。

**零数据保留是合规工作负载的拦路虎**。如果你的合规姿态要求 ZDR，通过 OpenRouter 进行视频生成今天还不是一个选项。

该端点附带清晰的文档化合约：提交、轮询、下载。`/api/v1/videos/models` 的目录查询为你的应用提供了关于支持设置的真相，因此你不会硬编码分辨率或时长假设，这些假设会在下一个模型上崩溃。这种组合是将 AI 视频添加到生产应用而不锁定单一供应商的正确基础。

## 常见问题

### OpenRouter 视频生成的成本是多少？

每秒价格从 $0.03（Veo 3.1 Lite，无音频）到 $0.60（Veo 3.1 4K 带音频）不等。预算档是 Wan 2.6 和 Veo 3.1 Lite 的 $0.04-0.08/秒；旗舰档是 Veo 3.1、Sora 2 Pro 和 Runway Aleph 2.0 的 $0.30-0.60/秒。带音频的 5 秒 1080p 视频片段根据模型价格在 $0.40 到 $3.00 之间。完成的任务响应包含 `usage.cost` 显示实际计费金额。

### 如何在不重写代码的情况下切换视频模型？

修改提交体中的 `model` 字段。端点、认证、响应形状、状态处理和下载 URL 在所有 26 个支持的模型中是相同的。模型特定的可选设置（时长、分辨率、宽高比、音频）按模型验证，因此首先查询 `/api/v1/videos/models` 以确认你想要的组合是否受支持。

### AI 视频生成需要多长时间？

通常 30 秒到几分钟，取决于模型、分辨率和片段长度。这就是为什么 API 是异步的而不是阻塞请求。推荐的轮询间隔是 30 秒；更快地轮询不会让供应商更快完成。

### 视频生成是否符合零数据保留？

不符合。异步检索步骤要求生成的输出被短暂保留以便下载，因此强制执行 ZDR 的账户不会被路由到视频生成。对于符合 ZDR 的视频，你必须直接与每个供应商的端点集成。

### 我可以使用 Webhook 而不是轮询吗？

可以。在提交体中传递 `callback_url`，OpenRouter 将在任务达到终态时 POST 到该 URL。每次投递都包含一个 `X-OpenRouter-Idempotency-Key` 头，接收处理器应存储该值以去重重试。如果配置了签名密钥，请在处理负载前验证 `X-OpenRouter-Signature` 头。

### 我应该为批量 UGC 选择哪个模型？

Wan 2.6 $0.04-0.08/秒（无音频）是最便宜的 720p 选项，支持合理的分辨率范围。Veo 3.1 Lite $0.05/秒（带音频）是最便宜的带音频 720p 选项。Seedance 2.0 Mini 的视频 token 定价在 5 秒 720p 片段上相当，但在更高分辨率下变得更贵，因为 token 数量随帧数缩放。

## 来源

- [OpenRouter 视频生成 API：代码优先指南](https://openrouter.ai/blog/tutorials/video-generation-api)（2026 年 8 月 25 日）
- [OpenRouter 视频模型目录（`/api/v1/videos/models`）](https://openrouter.ai/api/v1/videos/models)（2026 年 8 月 26 日快照）
- [OpenRouter 文档快速入门](https://openrouter.ai/docs/quickstart)
- [OpenRouter 价格页](https://openrouter.ai/pricing)
- [OpenRouter 联盟](https://openrouter.ai/affiliates)
- [OpenRouter 首页](https://openrouter.ai/)
