---
title: "OpenRouter Video Generation API 2026 Guide"
description: "OpenRouter's new /api/v1/videos endpoint unifies Seedance, Veo, Wan, Sora 2, Kling, and 21 more video models behind one async API. Prices $0.03-0.60/sec."
pubDate: "2026-08-26"
provider: openrouter
category: integration-guide
featured: true
---

# OpenRouter Video Generation API 2026: One Async Endpoint for 26 Video Models

On August 25, 2026, OpenRouter shipped a single async endpoint — `POST /api/v1/videos` — that fronts **26 video generation models** from ByteDance, Google, OpenAI, Alibaba, Runway, Kling, HeyGen, Black Forest Labs, and MiniMax. Before this release, adding video to an application meant wiring one SDK per provider, each with its own auth, request shape, job statuses, polling cadence, and download URL. OpenRouter's approach collapses all of that into one workflow: submit a job, poll a `polling_url`, retrieve the finished MP4.

This review walks through the verified endpoint behavior from OpenRouter's published guide dated August 25, 2026, the live `/api/v1/videos/models` catalog (26 models, snapshot captured the same day), and the per-model pricing SKUs returned in that catalog. The relevant fact bundle — endpoint paths, model identifiers, pricing per second, polling logic, webhook payload — is reproducible from those two sources.

## Why an async API, not a normal blocking call

A typical text-completion API responds in 200-800 ms. A typical image generation API responds in 1-4 seconds. Video generation is the first mainstream API category where the **generation time routinely exceeds the timeout tolerance of a single HTTP request**. OpenRouter's guide lists a 30-second-to-several-minutes generation range as the common case. Holding a TCP connection open that long is fragile: serverless platforms (Cloudflare Workers, AWS Lambda) cap execution at 30s-15min; corporate proxies and load balancers idle out at 60-300s; mobile networks drop after 30-60s of silence.

The asynchronous pattern is the textbook fix: separate submission from completion. You submit a job, receive an ID, poll the job until the status reaches `completed`, and then download the asset. If your process crashes mid-poll, the job ID persists on the server and you can resume tracking from any device.

The synchronous alternative — open a streaming WebSocket and receive frame data as the model produces it — exists for some models but requires a custom transport per provider and does not survive process restarts. OpenRouter chose the persistence-over-streaming tradeoff, which is the right one for serverless and batch use cases.

## Pricing: $0.03/sec to $0.60/sec, with audio and resolution as the two cost axes

The full pricing catalog from `/api/v1/videos/models` returns per-model `pricing_skus`. Most models bill by **duration-seconds** at a given resolution tier; some bill by **video tokens** (Seedance 2.0 family) or **megapixel-seconds** (FLUX Video Upscale). Below is a price-comparable table covering the major models, normalized to USD per second of output at the most common 720p/1080p tier:

| Model | Pricing model | Cost at 720p/1080p | 4K tier | Audio support |
|---|---|---:|---|:---:|
| Veo 3.1 | $0.20/sec (no audio) / $0.40/sec (audio) | $0.20-0.40/sec | $0.40-0.60/sec | ✅ |
| Veo 3.1 Fast | $0.10/sec (no audio) / $0.12/sec (audio) | $0.08-0.10/sec | $0.25-0.30/sec | ✅ |
| Veo 3.1 Lite | $0.05/sec (no audio) / $0.08/sec (audio) | $0.03-0.05/sec | — | ✅ |
| Sora 2 Pro | $0.30-0.50/sec | $0.30 (720p) / $0.50 (1080p) | — | ❌ |
| Seedance 2.5 | video_tokens: $0.0000107/token | ~$0.18/sec | — | ✅ |
| Seedance 2.0 | video_tokens: $0.000007/token | ~$0.13/sec | $0.000004/token | ✅ |
| Seedance 2.0 Fast | video_tokens: $0.0000042/token | ~$0.08/sec | — | ✅ |
| Seedance 2.0 Mini | video_tokens: $0.0000035/token | ~$0.07/sec | — | ✅ |
| Seedance 1.5 Pro | video_tokens: $0.0000024/token | ~$0.05/sec | — | ✅ |
| Wan 3.0 | $0.05-0.10/sec | $0.10 (720p) / $0.20 (1080p) | — | ✅ |
| Wan 2.7 | $0.10/sec | $0.10/sec | — | ❌ |
| Wan 2.6 | $0.04-0.08/sec | $0.08 (720p) / $0.12 (1080p) | — | ❌ |
| Kling v3.0 Pro | $0.112/sec (+ $0.056 audio) | $0.112/sec | $0.112 (1080p) | ✅ (+$0.056/sec) |
| Kling v3.0 Standard | $0.084/sec (+ $0.042 audio) | $0.084/sec | $0.084 (1080p) | ✅ |
| Kling Video O1 | $0.112/sec | $0.112/sec | — | ❌ |
| Runway Gen-4.5 | $0.12/sec | $0.12/sec | — | ❌ |
| Runway Aleph 2.0 | $0.28/sec, $0.56 minimum | $0.28/sec | — | ❌ |
| Grok Imagine Video 1.5 | $0.08-0.14/sec | $0.08 (480p) / $0.14 (720p) / $0.25 (1080p) | — | ❌ |
| Grok Imagine Video | $0.05-0.07/sec | $0.05 (480p) / $0.07 (720p) | — | ❌ |
| MiniMax H3 | $0.13/sec + $0.04 per reference image | $0.13/sec | — | ❌ |
| MiniMax Hailuo 2.3 | $0.0817/sec | $0.0817/sec | — | ❌ |
| HeyGen Avatar IV | $0.05/sec | $0.05/sec | — | ❌ |
| HappyHorse 1.1 | $0.10-0.13/sec | $0.0988 (720p) / $0.1278 (1080p) | — | ❌ |
| FLUX Video Upscale | $0.075-0.105/megapixel-second | — (upscale only) | — | ❌ |
| FLUX.3 Video | $0.17-0.53/sec | $0.17 (720p) / $0.29 (1080p) | $0.41-0.53/sec | ❌ |

Source: `https://openrouter.ai/api/v1/videos/models` snapshot taken August 26, 2026. Pricing_skus are returned as strings; for token-based models (Seedance), the value above is an approximation based on a 5-second clip and a single inference of video-token → wall-clock-second conversion. The four-decimal precision numbers should be treated as the unit price, not the per-clip total.

The headline numbers: **Veo 3.1 Lite at $0.03-0.05/sec is the cheapest 720p model with audio**, and **Wan 2.6 at $0.04-0.08/sec is the cheapest 720p model without audio**. At the top end, **Sora 2 Pro at $0.30-0.50/sec and Veo 3.1 at $0.40-0.60/sec are 6-15× more expensive than the budget tier** for comparable resolutions.

A 5-second 1080p clip with audio runs **$0.40 (Wan 2.6)** to **$3.00 (Veo 3.1 4K audio)** to **$2.50 (Sora 2 Pro)**. Budget for $1-2 per clip as the realistic working figure across most providers.

## Endpoint behavior, verified

### Submit a job

The single submission endpoint is `POST https://openrouter.ai/api/v1/videos`. The request body is JSON, with `model` (required) and `prompt` (required for text-to-video). Models that support image-to-video can omit `prompt` when supplying a frame image. Optional fields: `duration` (seconds), `resolution` (`480p` / `720p` / `1080p` / `4k` depending on model), `aspect_ratio` (`16:9` / `9:16` / `1:1` / `4:3` / `3:4` / `21:9` / `9:21` depending on model), `generate_audio` (boolean, where supported), `seed` (integer for reproducibility), `callback_url` (HTTPS webhook target), and a `provider.options` pass-through block for model-specific parameters.

The verified request shape (from the OpenRouter tutorial):

```bash
curl "https://openrouter.ai/api/v1/videos" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
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

Successful submission returns **HTTP 202 Accepted** with a job envelope:

```json
{
  "id": "job-abc123",
  "status": "pending",
  "polling_url": "https://openrouter.ai/api/v1/videos/job-abc123"
}
```

The HTTP 202 (not 200) is the correct signal — the resource has been *accepted* for asynchronous processing, not *completed*. Persist the `id` immediately. If your process restarts, that ID lets you resume tracking without submitting and paying for a second generation.

### Poll the job

`polling_url` is identical to `GET https://openrouter.ai/api/v1/videos/{id}` — the documented guide notes this explicitly so applications can construct the URL from the job ID alone if needed. The job moves through documented statuses:

| Status | Meaning |
|---|---|
| `pending` | Accepted, waiting to run |
| `in_progress` | Provider is generating |
| `completed` | Video ready to download |
| `failed` | Generation failed (error in response body) |
| `cancelled` | Job was cancelled |
| `expired` | Job exceeded its allowed lifetime |

Treat `completed` as the success exit. Treat `failed`, `cancelled`, `expired` as terminal errors. Anything else (or a connection error mid-poll) should trigger a polling retry, not a new job submission — the model may still be generating. The tutorial provides a defensive Python polling loop with a 30-second interval and a 1-hour ceiling that handles every documented terminal state and the difference between a polling failure and a generation failure.

A recommended polling interval is **30 seconds**; faster polling does not make the provider finish sooner. The 1-hour timeout is operational guidance, not a documented contract from the endpoint.

### Download the finished video

When `status: "completed"` arrives, the response includes a populated `unsigned_urls` array. Despite the name, these URLs require the `Authorization: Bearer` header — they are authenticated content endpoints, not presigned URLs:

```bash
curl "https://openrouter.ai/api/v1/videos/job-abc123/content?index=0" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  --output out.mp4
```

The `index` query parameter defaults to `0` and only needs to change when a model returns multiple video outputs from a single generation. Save the file as `mp4` unless the response `Content-Type` header says otherwise.

### Switch models with one line

The core promise of the unified endpoint: changing the model identifier changes the model, nothing else. The submission, polling, and download functions stay identical.

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

What does NOT carry over is every optional setting. The verified shared configuration across Seedance 2.0, Veo 3.1, and Wan 2.7 is `{duration: 4, resolution: "720p", aspect_ratio: "16:9", generate_audio: false}`. Move outside that combination and the models diverge:

- **Veo 3.1** currently supports 4-, 6-, and 8-second durations.
- **Seedance 2.0** currently supports 4- to 15-second durations plus a wider aspect-ratio range.
- **Wan 2.7** currently supports 2- to 10-second durations and 720p or 1080p resolutions.

A 5-second request validates against Seedance and Wan but fails on Veo. The recommended defensive pattern is to query `/api/v1/videos/models` before submission, read the supported `durations`, `resolutions`, and `aspect_ratios` for the chosen model, and validate locally.

## Model-specific pass-through parameters

Each model exposes `allowed_passthrough_parameters` in the `/api/v1/videos/models` response. These are the keys you can send inside the `provider.options` pass-through block, which is keyed by **provider slug**, not model slug. For example:

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

Only the parameters relevant to the selected provider are forwarded; unrecognized keys are dropped. Verified examples from the live catalog:

- **Veo (google-vertex)**: `negativePrompt`, `enhancePrompt`
- **Wan**: `negative_prompt`, `prompt_extend`
- **HeyGen Avatar IV**: `voice_id`, `voice_settings`, `motion_prompt`, `expressiveness`, `fit`, `remove_background`, `background`, `caption`, `title`

These parameters give the model-specific behavior that the unified endpoint deliberately does not hide. Switching from Veo to Wan means rewriting the pass-through block because the parameter names and valid values change.

## Webhook delivery for production scale

Polling works fine for scripts, prototypes, and tens of concurrent jobs. For hundreds, polling saturates the request budget on the polling side without informing the application any faster. OpenRouter supports **per-request webhook delivery** via a `callback_url` field on the submission:

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

The webhook fires when the job reaches any terminal state. Each delivery includes an `X-OpenRouter-Idempotency-Key` header — for example, `job-abc123-completed` — that the receiving handler should store before processing the event. If OpenRouter retries the webhook (which it will on non-2xx responses), the idempotency key lets the handler recognize the duplicate and avoid downloading the video twice.

If a signing secret is configured, the webhook request also includes an `X-OpenRouter-Signature` header. **Always verify this signature before processing the payload** in production — without it, anyone can POST to your callback URL and trigger a download.

You can also configure a **workspace default** callback URL so every submission inherits it. The request-level `callback_url` overrides the workspace default.

## Verified limitations and known footguns

- **Zero Data Retention (ZDR) is NOT supported** for video generation. OpenRouter confirms this explicitly in the tutorial FAQ: the async retrieval step requires the generated output to be briefly retained for download, so accounts with ZDR enforced are not routed to video generation. If you have an enterprise data-residency contract that requires ZDR, video cannot be your generation channel.
- **Audio capability varies wildly.** Only 9 of the 26 models support `generate_audio: true`; the rest reject the field. The pricing table above flags which models support audio.
- **Resolution support varies wildly.** Some models support only `720p`, some support `480p`/`720p`/`1080p`, and only Veo 3.1 supports `4k`. Query `/api/v1/videos/models` rather than hardcoding resolutions.
- **The 30-second polling interval is operational guidance, not a contract.** Tune to your own workload. Polling faster does not speed generation.
- **A failed polling request ≠ a failed generation.** If you resubmit the prompt after a polling timeout, you may end up with two videos and two charges for one user request. Always persist the job ID and retry status on the existing job, not generation.
- **`unsigned_urls` is a misleading name.** The URLs are not presigned; you must send your `Authorization: Bearer` header to download.
- **Some models support reference images and `first_frame` / last-frame inputs, others don't.** The `supported_frame_images` field on each model entry tells you what's accepted. Veo does not list any frame-image support in the catalog; Seedance 2.0 Mini supports first and last frame control plus multimodal reference input.

## Curl example: end-to-end with Seedance 2.0

```bash
# 1. Submit a job
RESPONSE=$(curl -s -X POST "https://openrouter.ai/api/v1/videos" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
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
echo "Job: $JOB_ID"

# 2. Poll until completed
while true; do
  STATUS=$(curl -s "https://openrouter.ai/api/v1/videos/$JOB_ID" \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" | \
    python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")
  echo "Status: $STATUS"
  case "$STATUS" in
    completed) break ;;
    failed|cancelled|expired) echo "Terminal error: $STATUS"; exit 1 ;;
  esac
  sleep 30
done

# 3. Download
curl -s "https://openrouter.ai/api/v1/videos/$JOB_ID/content?index=0" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  --output "out_${JOB_ID}.mp4"
echo "Saved out_${JOB_ID}.mp4"
```

## Python example: full workflow with webhook fallback

```python
import os, time, requests
from urllib.parse import urljoin

API_KEY = os.environ["OPENROUTER_API_KEY"]
BASE_URL = "https://openrouter.ai/api/v1"
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
        print(f"Status: {status}")
        if status == "completed":
            return current
        if status in TERMINAL_ERROR_STATES:
            raise RuntimeError(f"Job ended with status '{status}': {current.get('error')}")
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Job {job['id']} did not complete within {timeout}s")
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


# End-to-end
job = submit_video(
    model="bytedance/seedance-2.0",
    prompt="A paper boat drifting down a rain-slicked gutter at night",
    duration=4,
    resolution="720p",
    aspect_ratio="16:9",
    generate_audio=False,
)
print(f"Submitted job {job['id']}")
completed = poll_video(job)
print(f"Final cost: ${completed.get('usage', {}).get('cost', 'unknown')}")
download_video(completed, "boat.mp4")
```

The completed-job response can include a `usage` block with the actual cost:

```json
{
  "usage": {
    "cost": 0.5,
    "is_byok": false
  }
}
```

The `is_byok` flag indicates whether the request was billed against your own provider key (bring-your-own-key, where OpenRouter forwards the call without markup) or against your OpenRouter credit balance. Compare the estimate you built from `pricing_skus` against this actual `cost` to spot unexpected changes from a higher resolution, longer duration, audio addition, or model switch.

## Verdict

**OpenRouter's video API is the first single-endpoint abstraction that covers the realistic price/quality spread for production video generation.** 26 models is enough to A/B test budget vs. flagship output, and the unified submit/poll/download loop means the experiment cost is measured in API minutes, not in integration weeks.

**The expensive models are worth the cost only for hero content.** Veo 3.1 at $0.40/sec is the right pick for a product launch trailer; it is the wrong pick for batch UGC rendering where Wan 2.6 at $0.04-0.08/sec produces comparable 720p output at 5-10× the volume for the same budget.

**The model-specific options are the price of unification.** A switch from Veo to Wan means rewriting the `provider.options` block. A switch from Seedance 2.0 to Seedance 2.5 only changes the model identifier. The asymmetry between "swap-friendly" providers (ByteDance Seedance family) and "per-model-API" providers (Google Veo, HeyGen, Kling) is real and worth factoring into your model-selection strategy.

**Zero Data Retention is the showstopper for regulated workloads.** If your compliance posture requires ZDR, video generation through OpenRouter is not an option today.

The endpoint ships with a clean documented contract: submit, poll, download. The catalog query at `/api/v1/videos/models` gives your application the truth about supported settings, so you do not hardcode resolution or duration assumptions that break on the next model. That combination is the right foundation for adding AI video to production applications without locking into one provider.

## Frequently asked questions

### How much does OpenRouter video generation cost?

Per-second prices range from $0.03 (Veo 3.1 Lite, no audio) to $0.60 (Veo 3.1 4K with audio). The budget tier is Wan 2.6 and Veo 3.1 Lite at $0.04-0.08/sec; the flagship tier is Veo 3.1, Sora 2 Pro, and Runway Aleph 2.0 at $0.30-0.60/sec. A 5-second 1080p clip with audio runs $0.40 to $3.00 depending on the model. The completed-job response includes `usage.cost` for the actual amount billed.

### How do I switch video models without rewriting code?

Change the `model` field in the submission body. The endpoint, authentication, response shape, status handling, and download URL are identical across all 26 supported models. Model-specific optional settings (duration, resolution, aspect ratio, audio) are validated per-model, so query `/api/v1/videos/models` first to confirm the combination you want is supported.

### How long does AI video generation take?

Usually 30 seconds to several minutes, depending on the model, resolution, and clip length. This is why the API is asynchronous rather than a blocking request. The recommended polling interval is 30 seconds; polling faster does not make the provider finish sooner.

### Is video generation eligible for Zero Data Retention?

No. The async retrieval step requires the generated output to be briefly retained so it can be downloaded, so accounts with ZDR enforced are not routed to video generation. For ZDR-compliant video, you must integrate with each provider's endpoint directly.

### Can I use webhooks instead of polling?

Yes. Pass a `callback_url` in the submission body, and OpenRouter will POST to that URL when the job reaches a terminal state. Each delivery includes an `X-OpenRouter-Idempotency-Key` header that the receiving handler should store to deduplicate retries. If a signing secret is configured, verify the `X-OpenRouter-Signature` header before processing the payload.

### Which model should I pick for batch UGC?

Wan 2.6 at $0.04-0.08/sec without audio is the cheapest 720p option that supports a reasonable resolution range. Veo 3.1 Lite at $0.05/sec with audio is the cheapest audio-capable 720p option. Seedance 2.0 Mini at video-token pricing is comparable on a 5-second 720p clip but becomes more expensive at higher resolutions because the token count scales with frame count.

## Sources

- [OpenRouter Video Generation API: A Code-First Guide](https://openrouter.ai/blog/tutorials/video-generation-api) (August 25, 2026)
- [OpenRouter video models catalog (`/api/v1/videos/models`)](https://openrouter.ai/api/v1/videos/models) (snapshot August 26, 2026)
- [OpenRouter docs quickstart](https://openrouter.ai/docs/quickstart)
- [OpenRouter pricing page](https://openrouter.ai/pricing)
- [OpenRouter affiliates](https://openrouter.ai/affiliates)
- [OpenRouter homepage](https://openrouter.ai/)
