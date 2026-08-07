# Luma AI API 2026 Review: Ray 3.2 Video, Uni-1 Images & Pricing

**Date:** 2026-08-07
**Slug:** luma-ai-api-review-2026
**Provider:** Luma AI (luma)
**Category:** international

## Description

Luma AI API 2026 review: Ray 3.2 flagship video model with multi-keyframe control, Uni-1 image reasoning model, V2V up to 20s, credit-based pricing from $30/mo, and how it compares to Runway, Veo, Kling and OpenAI GPT Image 2.

---

## Quick take

Luma AI's transition from a consumer creative app into an API-first media generation platform is complete. The Luma Agents API exposes a single asynchronous REST surface — `POST /v1/generations`, poll, download from presigned URLs — that covers image generation (Uni-1), video generation (Ray 3.2), third-party frontier video models (Veo 3.1, Kling 3.0, Seedance 2.0), and even audio. If you want production-grade video generation with frame-level control, or a single API to reach the best video models without separate integrations, Luma is now a serious candidate.

## What is Luma AI, and why does the API matter in 2026?

Luma Labs (San Francisco, founded 2021) is best known for Dream Machine, the video generator that made cinematic AI clips mainstream. Through 2025 and 2026 the company consolidated its models behind an API-first product: the **Luma Agents API**, documented at `docs.agents.lumalabs.ai`. The pitch to an engineer is three-fold:

1. **One async interface, many model families.** Text-to-video, image-to-video, video-to-video, image generation, and audio all flow through the same `POST /v1/generations` endpoint. You do not learn a different SDK for each model.
2. **Multi-keyframe video control.** Ray 3.2 accepts up to 16 keyframes inside a single clip. Instead of prompting once and hoping the model keeps the sequence straight, you direct the cut frame by frame.
3. **Third-party model aggregation.** Beyond Luma's own Ray and Uni models, the API serves Veo 3.1, Kling 3.0 / Kling Omni / Kling 2.6, Seedance 2.0, MiniMax H3, Flux 3, GPT Image 2, and Nano Banana — the same multi-model gateway pattern OpenRouter applies to text.

## The model lineup in 2026

The current production line splits into first-party and third-party:

| Model | Kind | Output | Best for |
|---|---|---|---|
| **Ray 3.2** | Video (first-party flagship) | 1080p, up to 16 keyframes, V2V to 20s | Cinematic clips, frame-controlled production |
| **Ray 3.14** | Video (previous gen) | SDR / HDR | Lower-cost video where 3.2 is overkill |
| **Uni-1 / Uni-1-Max** | Image (first-party) | 1K–4K | Reasoning + generation, brand-consistent images |
| **Veo 3.1** | Video (Google) | 720p / 1080p | High-end cinematic video |
| **Kling 3.0 / Omni / 2.6** | Video (Kuaishou) | 720p–4K | Character + scene consistency |
| **Seedance 2.0** | Video (ByteDance) | 480p–4K | Short-video format, 4K quality |
| **GPT Image 2 / 1.5** | Image (OpenAI) | 1K–4K | Photorealistic image generation |
| **Nano Banana / Pro / 2** | Image (Gemini) | 512–4K | Versatile image creation |

## Pricing: how the credit system works

Luma is credit-based, not token-based. Subscriptions:

| Plan | Monthly | Credits | Notes |
|---|---|---|---|
| Plus | $30 | 10,000 | Hobbyists, evaluation |
| Pro | $90 | 40,000 | 4x usage, freelancers/agencies |
| Ultra | $300 | 150,000 | 15x usage, studios |
| Team / Enterprise | Custom | Shared | SSO, fine-tuning |

Video is metered per second (or per 5-second clip for Ray 3.2). Representative credits:

- **Ray 3.2** text-to-video: Draft 20 credits/5s, 540p 50/5s, 720p 100/5s, 1080p 400/5s.
- **Seedance 2.0**: 1080p 240 credits/sec, 4K 959 credits/sec.
- **Veo 3.1**: 720p/1080p 140 credits/sec (280/sec with audio).
- **Kling 3.0**: 720p 30 credits/sec, 4K 147 credits/sec.

Images are per image: **Uni-1** 30 credits, **Seedream** 1–3 credits, **GPT Image 2** from 3 (Low-1K) to 255 (High-4K) credits.

Audio: **ElevenLabs v3** TTS 21 credits/1,000 chars; SFX v2 25 credits/min.

**The math that matters:** at Pro's 40,000 credits, a 10-second 1080p Ray 3.2 clip (800 credits) yields roughly 50 clips per month. High-resolution long video (Seedance 4K at 959 credits/sec) burns credits fast; budget for 720p unless 4K is a hard requirement.

## How the Luma Agents API actually works

The workflow is three steps, the same shape in Python, TypeScript, or Go:

```python
from luma_agents import Luma
client = Luma()  # reads LUMA_AGENTS_API_KEY

# 1. Submit a generation
g = client.generations.create(
    prompt="A glass of iced coffee on a marble countertop, morning light",
    model="ray-3.2", resolution="1080p",
)

# 2. Poll until completed
result = g.wait()  # or poll GET /v1/generations/{id} yourself

# 3. Download from the presigned URL
open("clip.mp4", "wb").write(requests.get(result.assets.video).content)
```

Three things to know that the docs do not shout about:

1. **Everything is async.** Acknowledge is fast, but a 5-second 1080p Ray 3.2 clip completes in 30–120 seconds depending on plan and queue depth. This is a batch-generation API, not a low-latency chat API.
2. **Multi-Keyframe costs more.** Each keyframe adds control quality but also generation time and credits. Design to the minimum keyframe count your shot actually needs.
3. **HDR and EXR are the professional differentiator.** Native HDR generation and 16-bit EXR export let AI clips composite beside live-action plates in DaVinci Resolve or Nuke without tone-mapping friction — rare among video APIs.

## Luma vs Runway vs Veo vs Kling

| Provider | Flagship | Output | Pricing | China direct | Best for |
|---|---|---|---|---|---|
| **Luma AI** | Ray 3.2 | 1080p, 16 keyframes, V2V 20s | $30/mo Plus, credits | proxy required | Multi-model video gateway, frame control |
| **Runway** | Gen-4 Turbo | 5s clips, ~$0.50/clip | credit packs from $12 | proxy required | Video ad production |
| **Google Veo 3.1** | Veo 3.1 | 720p–1080p | via Luma or Vertex | proxy required | Cinematic quality |
| **Kuaishou Kling** | Kling 3.0 | 720p–4K | via Luma or direct | proxy required | Character consistency |
| **ByteDance Seedance** | Seedance 2.0 | 480p–4K | via Luma or Doubao | direct (CN) | Short-video format |

**Luma wins** on breadth — one API for video, image, audio, and the best third-party models. **Runway** remains the choice for turnkey ad-production recipes. **Seedance / Doubao** wins for China-direct short-video distribution.

## Limitations to know

- **No permanent free API tier.** Entry at Plus $30/mo; small one-time credit grant for new users only.
- **China access requires a proxy.** No mainland edge nodes or official China program.
- **Credit-based billing is complex.** Many model × resolution combinations; track credits, not dollars, when budgeting.
- **High-res long video is expensive.** Seedance 4K approaches 1,000 credits per clip.
- **Async only.** Not suitable for low-latency or interactive use.
- **No function calling / tool use.** Pure generation API; not an agent tool.

## Verdict

Choose **Luma AI** when you need production-grade video generation with frame-level control, or a single API that reaches the best image and video models (Veo, Kling, Seedance, GPT Image 2) without separate integrations. Plus at $30/mo is the right evaluation tier; Pro at $90/mo suits active production; Ultra at $300/mo fits studios and high-volume pipelines.

For China-direct short-video content, prefer ByteDance Doubao or MiniMax. For turnkey ad-production recipes, Runway remains strong. For everything else — cinematic video, image + video + audio in one API — Luma is a top pick in the 2026 API landscape.

## FAQ

**Does Luma AI have a public API?** Yes — the Luma Agents API (docs.agents.lumalabs.ai) is a single async REST surface. Submit via POST /v1/generations, poll GET /v1/generations/{id}, download from presigned URLs.

**Is there a free tier?** No permanent free API tier. New users get a small one-time credit grant, but sustained use requires Plus at $30/mo.

**What is the best Luma video model in 2026?** Ray 3.2 is the flagship: 1080p, up to 16 keyframes per clip, V2V to 20 seconds, with native HDR and EXR export.

**Can Luma generate video from video?** Yes — V2V on Ray 3.2 runs up to 20 seconds, letting you restyle or extend an existing clip.

**How does Luma pricing compare to Runway?** Luma is subscription + credits ($30/mo Plus). Runway is prepaid credit packs from $12. Compare per-clip: a 5s 720p Luma clip ~100 credits (~$0.30 at Pro), a Runway Gen-4 Turbo 5s clip ~$0.50.

**Does Luma work from China?** Only via a stable overseas proxy. No mainland direct endpoints or official China access program.

**Which third-party models does Luma serve?** Veo 3.1, Kling 3.0 / Omni / 2.6, Seedance 2.0, MiniMax H3, Flux 3, GPT Image 2, Nano Banana, and Seedream, plus ElevenLabs audio.

---

*Sources verified 2026-08-07: Luma pricing and plan details from lumalabs.ai/pricing; API workflow and model list from docs.agents.lumalabs.ai (llms.txt index and quickstart); SDKs (luma_agents Python, TypeScript, Go) from the official docs. No affiliate relationship with Luma AI.*
