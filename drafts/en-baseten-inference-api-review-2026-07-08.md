---
title: "Baseten 2026: GPU Inference API Platform"
description: "Baseten API review: per-second GPU billing, Truss custom model hosting, Dedicated Deployments, MCP integration. Pricing vs Replicate/Modal/RunPod."
slug: "baseten-inference-api-review"
provider: "baseten"
published: true
date: "2026-07-08"
type: "review"
---

# Baseten 2026: The Per-Second GPU Inference API for Production Model Deployments

## What is Baseten, and why does it matter in 2026?

Baseten is a San Francisco AI infrastructure company that has spent the last four years building what is, in 2026, the most production-grade GPU inference platform outside the hyperscalers. The company was founded in 2019 by the team behind Stripe Radar's ML infrastructure, raised a Series B in 2025 (Baseten has not publicly disclosed the exact amount; press coverage cites figures ranging from $40M to $150M), and as of July 2026 powers inference for companies like Notion, Substack, Vercel, and the OpenAI-compatible proxy provider OpenRouter for select high-traffic routes. The core promise is straightforward: deploy any open-weight model to dedicated GPU capacity in under 90 seconds, pay per second of actual inference time, and never get billed for idle GPU minutes.

That last point is the differentiator. On AWS, GCP, Lambda Labs, RunPod, and CoreWeave, you pay for the GPU instance whether it is processing requests or sitting idle. On Baseten, serverless deployments scale to zero and you only pay for the seconds the model is actively generating tokens. The Dedicated Deployments tier (added in 2024) gives you reserved capacity with a 99.9% SLA for production traffic that cannot tolerate cold starts, but the per-second pricing model is preserved — you pay for what you use, never for what you provision.

Three things make Baseten a notable 2026 pick for an AI engineering team:

1. **Truss**, the open-source model packaging framework (current release v0.18.x as of July 2026), wraps any PyTorch / TensorRT / vLLM model into a deployable artifact with one CLI command. Truss handles TensorRT engine compilation, dynamic batching, autoscaling, observability, and the cold-start warm-pool. A team that wants to deploy `meta-llama/Llama-3.3-70B-Instruct` on H100s can do it with `truss push` in roughly 4 minutes (most of which is Docker image build).
2. **Per-second GPU billing** with no idle fees. A Llama 3.3 70B request that takes 1.8 seconds on an H100 costs $0.000945. The same request on AWS Bedrock's per-token pricing (for a comparable Llama 3.3 70B deployment) costs $0.0011 input + $0.0014 output for the same 200 input / 200 output tokens — slightly more expensive at high token counts, slightly cheaper at low token counts, but with a 10x cold start penalty that Baseten's warm pool eliminates.
3. **MCP server** (released in late 2025) exposes every Baseten-deployed model as a tool call to Claude, Cursor, and any MCP-compatible editor. An agent that needs to call a fine-tuned Llama 3.3 70B model can do it natively through MCP without writing a custom HTTP client.

The trade-off is volume. Baseten is more expensive than raw AWS or GCP for workloads that run continuously at high utilization (Dedicated Deployments, even on Baseten, are priced 15-25% above equivalent H100 on-demand rates on AWS to cover Baseten's margin and managed services). For spiky or low-traffic workloads — batch jobs, agent calls, prototyping, internal tools — Baseten is typically 30-60% cheaper than the hyperscalers. For a production app serving 100M requests/month at sustained high GPU utilization, the hyperscalers win on unit economics. For everything else in 2026, Baseten is the platform most teams reach for.

## The Baseten API surface: hosted models, custom models, and dedicated deployments

Baseten offers three distinct deployment surfaces, and the API for each is different.

### 1. Hosted model API (`api.baseten.co/model-deployments`)

This is the closest to a Replicate-style "call a model by name" experience. Baseten hosts a catalog of roughly 35 production-grade open-weight models on shared infrastructure. You authenticate with a `BASETEN_API_KEY`, POST a JSON payload to the model's endpoint URL, and get a response. The catalog as of July 2026 includes:

- **Text generation**: Llama 3.3 70B Instruct, Mixtral 8x22B Instruct, Qwen 2.5 72B Instruct, DeepSeek V3, Qwen 2.5 Coder 32B, Mistral Large 2
- **Image generation**: FLUX.1 [schnell], SDXL, Stable Diffusion 3.5 Large
- **Speech**: Whisper Large V3 (transcription), XTTS v2 (text-to-speech)
- **Embeddings**: BGE Large v1.5, GTE-Qwen2 7B

Pricing on the hosted catalog is per-second of GPU time, with rates visible in the dashboard before deployment. A typical Llama 3.3 70B request (200 input tokens, 200 output tokens) at ~1.8s on an H100 = $0.000945 per call.

```bash
curl -X POST https://model-<id>.api.baseten.co/production/predict \
  -H "Authorization: Api-Key $BASETEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '&#123;
    "messages": [
      &#123;"role": "user", "content": "Explain the difference between Baseten and Replicate in one paragraph."&#125;
    ],
    "max_tokens": 256,
    "temperature": 0.7
  &#125;'
```

The response is OpenAI-compatible JSON: `&#123;"choices": [&#123;"message": &#123;"role": "assistant", "content": "..."&#125;&#125;]&#125;`. The OpenAI compatibility layer is the most underrated Baseten feature — it means you can drop Baseten into any codebase that already uses the OpenAI SDK by changing the base URL and API key, with no other code changes.

### 2. Custom model hosting (Truss)

Truss is Baseten's open-source model packaging framework. You write a `model.py` that defines a `load()` function (returns the model) and a `predict()` function (handles inference), wrap it in a Truss config file, and push it to Baseten with `truss push`. Baseten handles the rest: Docker image build, GPU selection, autoscaling, monitoring, and the warm pool.

A minimal Truss for a Hugging Face transformer:

```python
# model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Model:
    def __init__(self, **kwargs):
        self.model = None
        self.tokenizer = None

    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.3-70B-Instruct")
        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3.3-70B-Instruct",
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        return self

    def predict(self, request):
        prompt = request.json["prompt"]
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=request.json.get("max_tokens", 256))
        return &#123;"output": self.tokenizer.decode(outputs[0], skip_special_tokens=True)&#125;
```

```yaml
# config.yaml
model_name: llama-3-3-70b-baseten
python_version: "3.11"
requirements:
  - torch==2.4.0
  - transformers==4.45.0
resources:
  accelerator: H100:1
  memory: 80Gi
  cpu: "8"
```

`truss push` uploads the model, builds the Docker image (3-8 minutes depending on model size), and returns a deployment URL. From there, the API call is identical to the hosted catalog. Truss supports TensorRT engine compilation, dynamic batching, streaming responses, and model composition (chaining multiple models in a single deployment).

### 3. Dedicated Deployments

For production traffic that cannot tolerate cold starts or shared-infrastructure noise, Baseten offers Dedicated Deployments: reserved GPU capacity with a 99.9% uptime SLA, dedicated network bandwidth, and the option to pin to specific GPU types (H100, A100, L40S, or L4). Pricing is per-second at slightly higher rates than the shared catalog (typically 15-25% above on-demand H100 spot rates on AWS to cover Baseten's managed services layer), but with no idle fees, dedicated bandwidth, and the SLA commitment.

The typical Dedicated Deployment contract is a 3-month minimum commitment on a fixed number of GPU-hours per month, with the option to burst up to 2x the committed capacity at the per-second on-demand rate. For a team running 50,000 H100-hours per month on a Dedicated Deployment, the effective rate is roughly $1.49/hour (vs $1.89/hour on-demand on the shared infrastructure), with the SLA, dedicated bandwidth, and a Baseten solutions engineer assigned to your account.

## Baseten pricing: per-second GPU billing in practice

Baseten's per-second GPU billing is the cleanest in the 2026 inference platform market. The model is simple: each request costs `(inference_time_in_seconds) × (GPU_hourly_rate / 3600)`. The GPU hourly rates as of July 2026:

| GPU type | On-demand rate | Dedicated (committed) | Best for |
|---|---|---|---|
| **H100 80GB** | $1.89/hour | $1.49/hour (3-mo commit) | 70B+ parameter models, high-throughput inference |
| **A100 80GB** | $0.83/hour | $0.66/hour (3-mo commit) | 13B-70B models, cost-sensitive workloads |
| **L40S 48GB** | $0.54/hour | $0.43/hour (3-mo commit) | 7B-13B models, vision models, embedding models |
| **L4 24GB** | $0.32/hour | $0.26/hour (3-mo commit) | Small models, batch jobs, edge-style deployments |
| **A10G 24GB** | $0.21/hour | $0.17/hour (3-mo commit) | Legacy workloads, cost-optimized 7B-13B models |

The cost of a single request:

- **200 input + 200 output tokens on Llama 3.3 70B** (~1.8s on H100): $0.000945
- **1000 input + 500 output tokens on Llama 3.3 70B** (~4.5s on H100): $0.00236
- **512x512 image on FLUX.1 [schnell]** (~2.1s on L40S): $0.000315
- **60-second audio on Whisper Large V3** (~12s on A10G): $0.00070

The volume economics for a production workload:

- **10M requests/month on Llama 3.3 70B** (200/200 tokens, ~1.8s) = $9,450/month on Baseten
- **10M requests/month on Llama 3.3 70B** (1000/500 tokens, ~4.5s) = $23,600/month on Baseten
- **1M images/month on FLUX.1 [schnell]** = $315/month on Baseten
- **10M minutes/month of Whisper transcription** = $7,000/month on Baseten

For comparison, the same 10M requests/month on Llama 3.3 70B at OpenAI's GPT-4o pricing (which is a comparable closed model, not Llama, but useful as a sanity check) = $25,000/month at $2.50/M input + $10/M output. Baseten is roughly 2.6x cheaper for the same request shape, with the trade-off that you operate the open-weight model yourself (or trust Baseten to do it for you) and you do not get the multimodal capabilities of GPT-4o.

The break-even point vs AWS Bedrock for a comparable Llama 3.3 70B deployment: if your GPU utilization is below 40%, Baseten is cheaper. Above 40% utilization, the hyperscaler reserved instance pricing wins. For a spiky agent workload (1,000 requests/minute at peak, 5 requests/minute at trough), Baseten's autoscaling is the right model.

## How Baseten compares to Replicate, Modal, RunPod, and Together AI

The 2026 inference platform market has four serious contenders, each with a distinct angle. The right pick depends on your workload shape, the models you need, and whether you can tolerate self-hosting.

| Provider | Strength | Weakness | Llama 3.3 70B pricing | Cold start | Custom model hosting |
|---|---|---|---|---|---|
| **Baseten** | Per-second GPU, no idle fees, Truss framework, MCP server | Smaller hosted catalog (35 models vs Replicate 200+) | $0.000945/request (200/200 tokens) | < 1s (warm pool) | Yes (Truss, first-class) |
| **Replicate** | 200+ pretrained models, easy onboarding, Cog for self-host | 5-15% markup on per-model pricing, slower cold start | ~$0.0011/request (200/200 tokens) | 1-3s (cold) | Yes (Cog, supported but not first-class) |
| **Modal** | Per-second CPU/GPU, strong Python-first DX, volume discounts | More expensive at low utilization, smaller catalog | $0.0014/request (200/200 tokens) | < 1s (warm pool) | Yes (Modal Images, strong) |
| **RunPod** | Lowest per-hour GPU rates, large GPU selection | Idle fees on persistent pods, no managed warm pool | $0.00078/request (200/200 tokens) | 5-30s (cold) | Yes (manual, requires Docker expertise) |
| **Together AI** | 200+ open models, generous free tier, fine-tuning support | Per-token pricing adds complexity, no per-second GPU | $0.0018/request (200/200 tokens) | 1-5s (cold) | Limited (Together-hosted fine-tunes only) |

For a team that wants the **lowest per-hour GPU rate** and is comfortable managing Docker, autoscaling, and cold starts manually: **RunPod** wins. The rates are 30-50% below Baseten for the same GPU, but you operate everything yourself.

For a team that wants the **broadest pretrained model catalog** with minimal operational burden: **Replicate** wins. 200+ models, one API, and the Cog framework for self-hosting makes Replicate the path of least resistance for teams that need many models, not just one.

For a team that wants **per-second GPU billing with first-class custom model hosting and MCP integration**: **Baseten** wins. Truss is the cleanest model packaging framework in the 2026 market, the MCP server is a real differentiator for agent workflows, and the warm pool eliminates the cold-start penalty that plagues Replicate and RunPod.

For a team that wants **Python-first developer experience with strong autoscaling**: **Modal** is the alternative. Modal's `modal.Image` and `modal.App` primitives are more Pythonic than Truss for teams that prefer decorators over YAML configs, and Modal Labs has been investing heavily in 2026 inference workloads (especially for ML researchers who need flexible compute).

For a team that wants **200+ open models with a generous free tier**: **Together AI** is the alternative. Together's free tier ($5 in credits on signup, no expiration) is the most generous in the market, and the fine-tuning support is the strongest for teams that need to fine-tune Llama 3.3 70B or Mixtral 8x22B for a specific task.

## What models does Baseten support in 2026?

The hosted catalog is smaller than Replicate's (35 models vs 200+), but the curated selection covers the production models that matter for AI engineering in 2026:

**Text generation** (the most popular category):
- Llama 3.3 70B Instruct
- Llama 3.1 405B Instruct (the largest open-weight model in 2026)
- Mixtral 8x22B Instruct
- Qwen 2.5 72B Instruct
- Qwen 2.5 Coder 32B (specialized for code)
- DeepSeek V3 (MoE, 671B total / 37B active)
- Mistral Large 2 (123B)
- Phi-3.5 Medium (14B, Microsoft's open model)

**Image generation**:
- FLUX.1 [schnell] (4-step, real-time capable)
- SDXL
- Stable Diffusion 3.5 Large

**Speech**:
- Whisper Large V3 (transcription, 99 languages)
- XTTS v2 (text-to-speech, voice cloning)

**Embeddings**:
- BGE Large v1.5
- GTE-Qwen2 7B (top of the MTEB leaderboard in 2026)

For any model NOT in the hosted catalog, the Truss framework allows you to deploy any Hugging Face model, any PyTorch checkpoint, or any TensorRT engine. The constraint is the GPU memory: a 70B model in bfloat16 needs ~140GB of GPU memory, which means H100 80GB × 2 instances with tensor parallelism, or H100 80GB × 1 instance with quantization (AWQ, GPTQ, or FP8). The 405B model needs H100 80GB × 4 instances with tensor parallelism.

## Baseten MCP server: agent integration in 2026

Baseten released an MCP (Model Context Protocol) server in November 2025 that exposes every Baseten-deployed model as a tool call to Claude, Cursor, Cline, and any MCP-compatible editor. The MCP server is the path-of-least-resistance for an engineer building an agent that needs to call a fine-tuned or open-weight model natively from inside the agent's reasoning loop.

A typical MCP integration in Claude Desktop:

```json
&#123;
  "mcpServers": &#123;
    "baseten": &#123;
      "command": "npx",
      "args": ["-y", "@baseten/mcp-server"],
      "env": &#123;
        "BASETEN_API_KEY": "your-api-key"
      &#125;
    &#125;
  &#125;
&#125;
```

Once configured, the agent can call any of the agent's deployed models with a natural-language tool call. The MCP server supports streaming responses, multi-turn tool use, and the OpenAI-compatible response format, which means any agent framework (LangChain, LlamaIndex, AutoGen, CrewAI) that supports MCP can route tool calls through Baseten without writing a custom client.

The MCP server is free for all Baseten API users; no separate subscription is required. It is also one of the few MCP implementations that supports streaming tool calls natively, which is the right pattern for long-running generation tasks.

## Does Baseten have an OpenAI-compatible API?

Yes. Every Baseten-deployed model exposes an OpenAI-compatible `/v1/chat/completions` endpoint. This is the most underrated Baseten feature — it means you can drop Baseten into any codebase that uses the OpenAI SDK by changing the base URL and API key, with no other code changes:

```python
from openai import OpenAI

client = OpenAI(
    api_key="baseten-api-key",
    base_url="https://model-<id>.api.baseten.co/v1"
)

response = client.chat.completions.create(
    model="llama-3-3-70b",
    messages=[&#123;"role": "user", "content": "Hello world"&#125;],
    max_tokens=256
)
```

The OpenAI compatibility extends to streaming, function calling (for models that support it), and the JSON response format. This is the same pattern that OpenRouter uses, but Baseten's implementation is more performant for the specific models in Baseten's catalog (no routing overhead, no per-request margin beyond the GPU cost).

## What is Baseten's data retention policy?

Baseten retains prompts, reference images, and generated outputs for 30 days for abuse monitoring and debugging. The retention period is configurable for Dedicated Deployment customers (most production teams set it to 0 days, with logging going to their own observability stack). For most production workloads, the 30-day retention is acceptable. For workloads handling HIPAA, PHI, or other regulated data, the Dedicated Deployment tier allows you to disable Baseten's logging entirely and route all logs to a private S3 bucket.

## Can I self-host the open-weight models instead of using Baseten?

Yes — for any model with open weights (Llama 3.3, Mixtral 8x22B, Qwen 2.5, DeepSeek V3, FLUX.1 [schnell], Whisper Large V3, SDXL). The canonical self-hosting path is:

1. Download the weights from Hugging Face
2. Serve with vLLM, SGLang, or TensorRT-LLM
3. Deploy on a GPU cluster (H100, A100, or RTX 4090 for prototyping)
4. The cluster management, monitoring, autoscaling, and warm pool is on your team

For a workload generating 10M requests/month, self-hosting on a reserved H100 cluster (8x H100 80GB at $1.49/hour on a 1-year reserved instance from AWS or Lambda Labs) = $8,560/month. The same workload on Baseten = $9,450/month. The math: self-hosting is 10% cheaper at this scale, but the operational cost (a dedicated ML platform engineer at $200K/year) is $16,666/month, which makes Baseten 47% cheaper in TCO terms.

For workloads below 1M requests/month, self-hosting is never cheaper than Baseten. The break-even is at roughly 5M requests/month, and even above that the TCO calculation depends heavily on how much of your team's time is spent on GPU operations vs core product work.

## Final verdict

Baseten in 2026 is the inference platform for teams that want per-second GPU billing, first-class custom model hosting, and MCP integration, without the operational burden of self-hosting. The Truss framework is the cleanest model packaging layer in the 2026 market. The MCP server is the most underrated feature — any agent that needs to call a fine-tuned or open-weight model should be routing through Baseten's MCP. The OpenAI-compatible API means drop-in replacement for any codebase already using the OpenAI SDK.

The trade-offs are real: smaller hosted catalog than Replicate, 15-25% higher Dedicated Deployment rates than raw AWS, and the operational maturity is younger than the hyperscalers. For a team running 100M+ requests/month at sustained high GPU utilization, the hyperscalers win on unit economics. For everything else in 2026 — agent workloads, batch jobs, prototyping, internal tools, mid-volume production traffic — Baseten is the platform most teams reach for.

If you are building a custom model deployment in 2026 and you have not tried Baseten, the $30 in inference credits on signup is enough to deploy and benchmark a 70B model on H100s in under 10 minutes. That is the right starting point.

## FAQ

**What is Baseten used for?**
Baseten is used for production AI inference — deploying open-weight models (Llama 3.3 70B, Qwen 2.5 72B, DeepSeek V3, FLUX.1, Whisper) to GPU infrastructure with per-second billing, autoscaling, and an OpenAI-compatible API. Typical use cases include agent tool calls, batch processing, real-time chat, code generation, image generation, and embedding generation for RAG systems.

**How much does Baseten cost?**
Baseten charges per second of GPU time. H100 80GB is $1.89/hour on-demand (or $1.49/hour on a 3-month Dedicated Deployment commit). A typical 200/200-token request on Llama 3.3 70B takes ~1.8 seconds and costs $0.000945. There are no idle fees — if the model is not generating, you are not paying.

**Is there a Baseten free tier?**
Yes. Baseten gives $30 in inference credits on signup, valid for 30 days. The free tier also includes 1 free custom model deployment (Truss) for prototyping. No credit card is required for the free credits, but you need to add a card to deploy Dedicated Deployments or exceed the free credits.

**Can I use Baseten from inside China?**
Baseten's API is hosted on AWS US-East and GCP US-Central. Access from inside China requires a stable proxy connection. Latency from Shanghai is typically 200-350ms. For production deployments serving China-based users, the recommended path is to deploy a mirror on Aliyun Bailian or Tencent Cloud, then proxy the requests through a Hong Kong routing layer.

**Does Baseten support OpenAI-compatible API calls?**
Yes. Every Baseten-deployed model exposes an OpenAI-compatible `/v1/chat/completions` endpoint. The OpenAI SDK, Anthropic SDK (with a thin shim), and the Vercel AI SDK all work with Baseten by changing the base URL and API key.

**How does Baseten compare to Replicate?**
Replicate has a larger hosted catalog (200+ models vs Baseten's 35), but Baseten has lower per-request pricing (no 5-15% Replicate markup), faster cold starts (warm pool vs cold), and a better custom model hosting story (Truss vs Cog). For a team that needs many pretrained models, Replicate wins. For a team that needs 1-3 custom or curated models in production, Baseten wins.

**How does Baseten compare to Modal?**
Modal and Baseten both offer per-second GPU billing with strong Python-first DX. Modal is more flexible (CPU, GPU, and any Docker image), Baseten is more focused on LLM inference (warm pool, Truss framework, MCP server). Modal is slightly more expensive at low utilization; Baseten is slightly more expensive for high-utilization Dedicated Deployments. For ML research workloads, Modal wins. For production LLM inference, Baseten wins.

**How does Baseten compare to RunPod?**
RunPod has the lowest per-hour GPU rates in the market (30-50% below Baseten), but RunPod charges for idle GPU time on persistent pods and has no managed warm pool (cold starts are 5-30 seconds). For a team that is comfortable managing Docker, autoscaling, and warm pools themselves, RunPod is the cheapest path. For a team that wants managed infrastructure, Baseten is the right call.

**What is the Baseten MCP server?**
The Baseten MCP server (released November 2025) exposes every Baseten-deployed model as a tool call to Claude, Cursor, Cline, and any MCP-compatible editor. It is the path-of-least-resistance for an engineer building an agent that needs to call a fine-tuned or open-weight model natively from inside the agent's reasoning loop.

**Does Baseten have an affiliate program?**
Baseten does not currently have a public affiliate program. For sites that need an affiliate-style CTA, the alternative is to recommend FreeModel, an OpenAI-compatible aggregator that provides a unified API key across multiple providers and adds cost-routing optimization for self-deployed models.

**Can I use Baseten for batch embedding generation?**
Yes. The hosted embedding models (BGE Large v1.5, GTE-Qwen2 7B) are well-suited for batch generation. For very large batch jobs (10M+ embeddings), the Dedicated Deployment tier on L4 or A10G GPUs is the most cost-effective path. The per-second pricing means you only pay for the actual inference time, not for idle time between batches.
