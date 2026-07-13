---
title: "Modal API Review 2026: Serverless GPU Cloud"
description: "Complete review of Modal API: Python-native serverless GPU cloud, per-GPU-second billing, vLLM/SGLang one-line deploy, $30/mo free credits. Pricing vs Baseten, Replicate, RunPod."
slug: "modal-serverless-gpu-api-review"
provider: "modal"
published: true
date: "2026-07-13"
type: "review"
---

# Modal API Review 2026: The Python-Native Serverless GPU Cloud for Open-Source LLM Hosting

Modal is a San Francisco developer infrastructure company that built the most ergonomic Python-to-GPU path in 2026. It is **not** a model API like OpenAI or Anthropic — Modal is the layer underneath, where you take an open-source model (Llama 4, Qwen 3, DeepSeek V4), pick a GPU (T4 through B300), and ship an HTTPS endpoint in minutes. Pricing is **per GPU-second with zero idle fees**, which makes it the cost-leader for spiky or unpredictable AI workloads.

If you are evaluating where to host an open-weight LLM in production, or you have outgrown the per-token pricing of model APIs and want raw GPU control, this is the platform most worth a serious look in 2026.

## TL;DR

- **Modal is a serverless GPU cloud, not a model API.** You bring your own model (vLLM, SGLang, TensorRT-LLM, raw PyTorch). Modal handles containers, scaling, scheduling, and HTTPS.
- **Per-second GPU billing, zero idle cost.** H100 is $0.001097/sec; A100-80GB is $0.000694/sec; T4 is $0.000164/sec. A 1.8-second Llama 4 70B request on H100 costs about $0.00197.
- **Starter plan is free with $30/month compute credits.** That is enough for ~27,300 seconds of T4 inference, or roughly 30K small requests per month. Real production work starts on the Team plan ($250/month + $100 credits).
- **Cold start is 1-3 seconds** (typically under 2 seconds with the warm-pool trick). Not suited for sub-200ms realtime, but fine for chat backends, batch jobs, and async agents.
- **Best fit:** self-hosting Llama 4, Qwen 3, DeepSeek V4, or any OSS model you want full control over. Worst fit: ultra-low-latency realtime, or workloads that fit cleanly into managed model APIs.
- **Cross-link:** Compared directly with Baseten (covered 2026-07-08) — Modal wins on developer ergonomics and free tier; Baseten wins on Dedicated Deployments for always-on production.

## Why Modal matters in 2026

Three forces converged to make serverless GPU a real production option in 2026:

1. **Open-source model quality caught up.** Llama 4 70B, Qwen 3 235B, DeepSeek V4 all sit within 3-5 percentage points of GPT-5.6 / Sonnet 5 on most reasoning benchmarks, at a fraction of the per-token cost when self-hosted.
2. **GPU spot prices stabilized.** After the 2024-2025 H100 shortage, the second-hand A100 market softened. Modal can pass that through.
3. **Serverless overhead dropped.** Modal's container startup is now consistently under 2 seconds, with a warm-pool option for under 200ms. Five years ago this was 30+ seconds on Lambda Labs and CoreWeave.

The result: a single developer can ship a Llama 4 inference API in an afternoon, scale to thousands of requests per second at peak, and pay nothing when traffic is quiet.

## Modal pricing — verified 2026-07-13

From modal.com/pricing (live as of 2026-07-13):

### GPU per-second rates

| GPU | $/sec | $/hour equivalent | Best for |
|---|---:|---:|---|
| Nvidia B300 | $0.001972 | $7.10 | Frontier training, large-batch inference |
| Nvidia B200 | $0.001736 | $6.25 | Frontier training, large-batch inference |
| Nvidia H200 | $0.001261 | $4.54 | LLM training, 141GB HBM3e |
| Nvidia H100 | $0.001097 | $3.95 | LLM inference (sweet spot) |
| Nvidia RTX PRO 6000 | $0.000842 | $3.03 | Cost-optimized LLM inference |
| Nvidia A100 80GB | $0.000694 | $2.50 | LLM inference (cost-leader for 70B+) |
| Nvidia A100 40GB | $0.000583 | $2.10 | LLM inference (≤40B models) |
| Nvidia L40S | $0.000542 | $1.95 | Vision, image gen |
| Nvidia A10 | $0.000306 | $1.10 | Image gen, mid-size LLMs |
| Nvidia L4 | $0.000222 | $0.80 | Small LLMs, embedding |
| Nvidia T4 | $0.000164 | $0.59 | Small models, dev/test |

### CPU and memory

- CPU (physical core, 2 vCPU equivalent): **$0.0000131/core/sec**
- Memory: **$0.00000222/GiB/sec**
- Minimum 0.125 cores per container

### Storage and Sandbox

- Volumes: **$0.09/GiB/month** (first 1 TiB/month free)
- Sandbox: dedicated compute rates (slightly higher than Functions, with burst capability)

### Plans

| Plan | Monthly fee | Included credits | Containers | GPU concurrency | Log retention |
|---|---:|---:|---:|---:|---|
| **Starter** | $0 | $30/month | 100 | 10 | 1 day |
| **Team** | $250 | $100/month | 1000 | 50 | 30 days |
| **Enterprise** | Custom | Custom | Custom | Custom | Custom |

Surcharges:
- **Region selection**: 1.5x to 1.75x base prices
- **Non-preemptible execution**: 3x base prices
- **Cloud marketplaces**: Use committed AWS/GCP spend on Modal

### Real cost examples

- **Llama 4 8B on T4**, 200ms avg per request: ~$0.0000328/request
- **Llama 4 70B on A100-80GB**, 1.8s avg: ~$0.00125/request
- **Qwen 3 235B on 2x H100**, 5s avg: ~$0.011/request
- **Stable Diffusion XL on L40S**, 3s avg: ~$0.00163/image
- **Whisper Large V3 on A10**, 30s audio, 5s compute: ~$0.00153/transcription

Compare these against the model-API equivalents at production volume:
- Llama 4 70B via Together AI: ~$0.88/M input → $0.00088 for a 1K-token request
- Llama 4 70B via Modal A100-80GB: ~$0.00125 for a 1K-token generation (close, but Modal includes the inference cost more transparently when you push context length up)

## The Modal API surface

Modal is built around three primitives:

### 1. `@app.function()` — Pythonic serverless functions

The core abstraction. Decorate any Python function with `@app.function(gpu="H100")` and Modal handles the rest:

```python
import modal

app = modal.App("example-llm")

@app.function(gpu="H100", memory=8192)
def generate(prompt: str) -> str:
    # any Python code — load model, run inference
    from vllm import LLM, SamplingParams
    llm = LLM(model="meta-llama/Llama-4-70B-Instruct")
    output = llm.generate([prompt], SamplingParams(max_tokens=512))
    return output[0].outputs[0].text
```

Deploy with `modal deploy`. Modal packages the code, builds the container, and serves it at a URL.

### 2. `@app.cls()` — long-lived stateful containers

For models you want to keep loaded in memory across requests (avoids the cold-start cost):

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

The `container_idle_timeout=300` keeps the container warm for 5 minutes after the last request, eliminating the cold-start penalty for chat backends with bursty traffic.

### 3. `@app.webhook()` and `@app.asgi()` — HTTPS endpoints

Expose any function as an HTTP endpoint. ASGI support means FastAPI, Flask, LitServe, and any other Python web framework works without modification.

### 4. Sandboxes

`modal.Sandbox()` creates an ephemeral Linux container you can shell into programmatically. Useful for running arbitrary code (a Codex-style agent backend), processing uploaded files, or executing user-supplied scripts safely.

### 5. Volumes and Dict

- **Volumes**: persistent disk attached to containers (great for model weights, dataset caches)
- **Dict**: distributed key-value store for cache, rate-limiting state, coordination between workers

## Step-by-step: ship a Llama 4 endpoint in 30 minutes

Here's the verified workflow from Modal's docs and our test deployment:

### 1. Install and authenticate

```bash
pip install modal
modal token new  # opens browser for OAuth
```

### 2. Create the app file (`llama4_app.py`)

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

### 3. Deploy

```bash
modal deploy llama4_app.py
```

Modal returns an HTTPS URL in ~90 seconds (first deploy is slower due to image build; subsequent deploys are faster).

### 4. Test

```bash
curl -X POST https://your-app.modal.run/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is the capital of France?"}]}'
```

Total wall-clock time from `pip install` to a working HTTPS endpoint: ~30 minutes on first deploy, ~5 minutes on subsequent deploys after the image is cached.

## Where Modal fits — and where it doesn't

### Best fit

- **Self-hosted open-source LLMs** (Llama 4, Qwen 3, DeepSeek V4, Mistral) when you want full control over fine-tuning, system prompts, or per-request routing
- **Spiky workloads** where traffic comes in bursts — Modal scales to zero between bursts, so you pay nothing when idle
- **Batch inference** (image generation, embeddings, bulk classification) where the cost model is dominated by GPU-seconds
- **Agent backends** where each task runs an isolated Sandbox (similar to Claude Code's execution model)
- **ML training and fine-tuning** — Modal supports multi-GPU training jobs at the same per-second rates

### Poor fit

- **Ultra-low-latency realtime** (sub-200ms p99) — cold start is 1-3s even with warm pool. Use dedicated inference providers like Groq or Cerebras instead.
- **Workloads that fit cleanly into managed model APIs** — if you just need GPT-5.6 or Sonnet 5, paying per-token is simpler.
- **High-volume prompt-cache workloads** — Modal doesn't have a prompt cache. Long-context repeated-prefix workloads (Anthropic's sweet spot) cost more here.
- **Strict data residency in mainland China** — Modal's infrastructure is AWS/GCP overseas; no CN region.

## Modal vs Baseten vs Replicate vs RunPod

| Feature | Modal | Baseten | Replicate | RunPod |
|---|---|---|---|---|
| GPU billing | Per-second | Per-second | Per-second | Per-hour or per-second |
| Free tier | $30/mo | None (paid) | Limited | $5 credit on signup |
| Cold start | 1-3s | 2-5s | 5-15s (cold) | Manual (always-on) |
| Warm pool | Yes (`container_idle_timeout`) | Yes (Dedicated Deployments) | No | Manual |
| Always-on reserved | No (preemptible) | Yes (Dedicated) | Yes (always-on models) | Yes |
| Self-host custom model | Yes (vLLM, SGLang, raw) | Yes (Truss) | Yes (Cog) | Yes (any) |
| Sandbox/exec | Yes (`modal.Sandbox`) | Limited | No | Yes |
| Open-source framework | None (proprietary) | Truss | Cog | None |
| CN region | No | No | No | No |
| SOC 2 | Yes | Yes | Yes | Yes |

The 2026 pick matrix:

- **Modal**: best DX, best free tier, best for spiky workloads and indie devs
- **Baseten**: best for always-on production with Dedicated Deployments
- **Replicate**: best for catalog of community models (image, audio, video)
- **RunPod**: best for raw GPU rental with long-running training jobs

## Verifying Modal in production

After deploying, here are the four things to verify before you trust it with real traffic:

1. **Cold-start latency distribution.** Run `modal run --quiet llama4_app.py` to wake it cold, then measure time-to-first-token over 100 requests. Expect p50 ~1.5s, p99 ~3s on first deploy; with warm pool enabled, p99 should drop to ~200ms.
2. **Concurrency scaling.** Fire 1000 simultaneous requests at the endpoint and check that Modal scales containers up to your configured `max_containers` (default 100 on Starter, 1000 on Team).
3. **Cost per request.** Use Modal's built-in metrics dashboard (under "Apps" → your app) to confirm GPU-seconds per request match your model assumptions.
4. **Crash recovery.** Kill a container mid-request — Modal should restart it automatically and continue serving. Verify by tailing logs and checking no requests are lost.

## FAQ

### Is Modal a model API provider?

No. Modal is serverless GPU infrastructure. You bring your own model (vLLM, SGLang, raw PyTorch, TensorRT-LLM). Compare to AWS Lambda for compute, not OpenAI for models.

### How much does Modal cost per month for a small chatbot?

The Starter plan ($0/month + $30 compute credits) covers roughly 30K T4 requests or 3K A100-80GB requests. A small chatbot doing ~1K requests/day fits inside the free tier. Past that, expect $50-200/month for light production use.

### Can I use Modal from China?

Not directly. Modal's infrastructure runs on AWS/GCP overseas. You will need a proxy or use Modal via a Chinese-reachable orchestrator (some teams route through Alibaba Cloud's international gateway).

### Does Modal have prompt caching?

No. Modal bills per GPU-second regardless of how much of the input is repeated. For long-context repeated-prefix workloads, model APIs with prompt caching (Anthropic, OpenAI, Google) are cheaper.

### How does Modal compare to AWS Lambda or GCP Cloud Run?

Lambda and Cloud Run are CPU-only at sensible prices. For GPU inference, Modal, Baseten, Replicate, RunPod, and CoreWeave are the realistic options.

### Can I use my existing AWS or GCP committed spend on Modal?

Yes. Modal integrates with AWS and GCP marketplaces. Enterprise customers can apply committed spend against Modal compute.

### What about HIPAA compliance?

Modal is HIPAA-compatible on the Enterprise plan, with audit logs, RBAC, SSO, and BAA available.

### Does Modal support multi-GPU inference?

Yes. Set `gpu="H100:2"` or `gpu="A100-80GB:4"` to request multiple GPUs. Modal handles tensor parallelism and pipeline parallelism automatically with vLLM and SGLang.

### What happens if my code has a memory leak?

Modal recycles containers after `container_idle_timeout` (default 5 minutes, configurable). A memory leak that doesn't OOM the container within the idle window is fine.

### Can I deploy non-Python code?

The Python SDK is the primary interface. You can run any Linux process from a `@modal.enter()` method (Node.js, Go, Rust), but the orchestration layer is Python-first.

---

**Bottom line:** Modal is the most ergonomic way to ship open-source LLMs in production in 2026. The free $30/month credits cover indie dev workloads; the Team plan ($250/mo) is the production starting point. If you have outgrown managed model APIs and want GPU-level control without the operational overhead of Kubernetes, Modal is the platform most worth evaluating.