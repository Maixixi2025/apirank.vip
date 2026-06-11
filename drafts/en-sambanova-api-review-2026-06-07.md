---
title: "SambaNova API 2026: SN40L Dataflow + Llama 405B"
description: "SambaNova Cloud API review: SN40L Reconfigurable Dataflow Unit at 1,000+ tok/s, exclusive Llama 3.1 405B hosting, DeepSeek-R1 full, OpenAI API compatible."
slug: "sambanova-api-review"
provider: "sambanova"
published: false
date: "2026-06-07"
type: "review"
---

# SambaNova API 2026: SN40L Dataflow Speed Meets Llama 405B

## Introduction: The Dataflow Alternative to GPUs and LPUs

SambaNova Systems was founded in 2017 by a Stanford professor and two of his former PhD students — Kunle Olukotun, Chris Ré, and Rodrigo Liang. The trio saw a problem coming: as language models grew from billions to hundreds of billions of parameters, the GPU-centric approach to inference would hit a wall. Memory bandwidth, not compute, would become the bottleneck. The fix, they argued, was not to build a better GPU. It was to abandon the von Neumann architecture entirely.

The result is the **Reconfigurable Dataflow Unit (RDU)**, a chip designed from the ground up for the way transformer models actually move data. Unlike GPUs (which fetch weights from HBM every forward pass) or Groq's LPU (which streams weights deterministically from SRAM), the RDU is **reconfigured per model** — the dataflow graph is compiled into the silicon itself, and weights stay in on-chip memory the entire time the model is running. The third-generation chip, the SN40L, sits on a board called the SN40L-8, eight of which are packed into a 19-inch rack unit to form a SambaNode.

The performance numbers from the SN40L are striking. On Llama 3.1 8B, SambaNova publishes benchmarks of over 1,000 tokens per second per user — about 2-3x Groq's LPU and 10x typical GPU deployments. On Llama 3.1 405B, the only cloud provider offering the full 405-billion-parameter model with sub-second time-to-first-token is SambaNova, because the model fits in the memory of a single SambaNode (1.5 TB of on-chip SRAM across the eight RDUs). For DeepSeek-R1 (671B parameters), SambaNova's dataflow approach keeps the model warm on-chip and avoids the swap-to-disk penalties that GPU clusters face.

In 2024, SambaNova opened up this infrastructure as the **SambaNova Cloud** API — an OpenAI-compatible endpoint that lets any developer call Llama 3.1 405B, DeepSeek-R1, and other frontier models at dataflow speed. The pricing is competitive with Groq and Cerebras, the API surface is familiar, and the platform supports streaming, function calling, and JSON mode out of the box. This review covers the SN40L architecture, the SambaNova Cloud pricing, the model catalog (including the exclusive 405B and R1 hosting), and how SambaNova compares to Cerebras, Groq, and Together AI for the workloads where inference speed is the binding constraint.

## SambaNova Cloud Pricing

SambaNova Cloud uses standard per-token input and output pricing, the same model OpenAI and Groq use. Unlike Cerebras (which charges a flat combined rate), SambaNova's pricing reflects the actual cost asymmetry between input (prefill) and output (decode) compute.

| Model | Input ($/M tok) | Output ($/M tok) | Combined ($/M tok) | Speed (tok/s) | Notes |
|-------|-----------------|------------------|--------------------|----------------|-------|
| Meta-Llama-3.1-8B-Instruct | $0.10 | $0.20 | $0.30 (avg) | 1,200+ | Fastest 8B in cloud |
| Meta-Llama-3.3-70B-Instruct | $0.30 | $0.70 | $1.00 (avg) | 600+ | Balanced quality/speed |
| Meta-Llama-3.1-70B-Instruct | $0.30 | $0.60 | $0.90 (avg) | 600+ | Stable 70B option |
| Meta-Llama-3.1-405B-Instruct | $3.00 | $5.00 | $4.00 (avg) | 100+ | Exclusive full 405B host |
| DeepSeek-R1 (671B) | $3.00 | $5.00 | $4.00 (avg) | 80+ | Full 671B reasoning model |
| DeepSeek-V3-0324 | $0.80 | $0.80 | $0.80 | 200+ | Cost-effective MoE |
| Qwen2.5-72B-Instruct | $0.30 | $0.60 | $0.90 (avg) | 550+ | Strong coding/chinese |
| Qwen2.5-Coder-32B-Instruct | $0.15 | $0.30 | $0.45 (avg) | 800+ | Code-specialized |
| sambanova-1 | TBD | TBD | TBD | TBD | Proprietary model in private preview |

*SambaNova publishes no soft rate limits. The $5 free credits work against the entire model catalog without a separate tier.*

### Free Tier

SambaNova Cloud offers **$5 in free credits** on signup, with no credit card required for the initial trial. This is enough to process roughly 10 million tokens on Llama 3.1 8B (at $0.30/M combined) — a meaningful amount for evaluating the platform on real workloads. After the trial, you top up with prepaid credits in $10 increments. There is no monthly subscription or minimum commitment.

### How Much Can You Get for $100?

At $1.00/M tokens combined for Llama 3.3 70B, $100 buys approximately **100 million tokens** of combined input + output. In practical terms:

- **~5,000 long-form conversations** (10K input + 10K output each)
- **~200,000 API calls** with 500 tokens each
- **~33 hours** of continuous streaming at typical assistant response rates

For the larger models, $100 on Llama 3.1 405B ($4.00/M combined) gets you 25 million tokens — enough for ~1,200 long-form conversations or 50,000 mid-sized API calls. This makes SambaNova Cloud one of the most cost-effective ways to run the full 405B model, especially compared to self-hosting (which requires 8x H100 GPUs at minimum, plus hosting and power).

## Speed Benchmark: SambaNova vs. Cerebras, Groq, Together AI

The SN40L's dataflow architecture delivers a different kind of speed than the alternatives. Where Cerebras's WSE-3 wins on raw token throughput (because the entire model is on one wafer), and Groq's LPU wins on low latency for short prompts, SambaNova's RDU wins on **throughput per user** for long-context workloads.

| Provider | Llama 3.3 70B Speed | Llama 3.1 8B Speed | First-Token Latency | Hardware |
|----------|---------------------|---------------------|---------------------|----------|
| **SambaNova (SN40L)** | 600+ tok/s | 1,200+ tok/s | under 150ms | Reconfigurable Dataflow Unit |
| Cerebras (WSE-3) | 2,000+ tok/s | 4,500+ tok/s | under 200ms | Wafer-Scale Engine |
| Groq (LPU) | 450 tok/s | 900 tok/s | under 300ms | Language Processing Unit |
| Together AI (A100) | 120 tok/s | 280 tok/s | under 1s | NVIDIA A100 |
| Replicate (A10G) | 80 tok/s | 200 tok/s | 5-15s cold | NVIDIA A10G |

SambaNova sits in the second tier of speed players, behind Cerebras on raw throughput but ahead of Groq on Llama 3.1 8B and well ahead of any GPU-based provider. The platform's real edge is the 405B hosting — neither Cerebras nor Groq offers the full 405B model with comparable latency. Self-hosting 405B on 8x H100 clusters gets you 30-50 tok/s at best.

### What Does 1,200 tok/s Feel Like?

On Llama 3.1 8B, a 500-token response appears in **under 420 milliseconds** — effectively instant to a human reader. A 4,000-token code review completes in roughly 3.3 seconds. This opens up use cases that are awkward with slower inference: real-time code completion in IDEs, interactive document drafting, and conversational agents that can generate multi-paragraph responses without any typing delay.

## Key Advantages of SambaNova Cloud

- **Exclusive 405B hosting**: SambaNova is the only cloud provider offering Llama 3.1 405B-Instruct at sub-second latency and per-token pricing. The full model fits in 1.5 TB of on-chip SRAM across eight SN40L RDUs in a single SambaNode — no model sharding, no GPU cluster orchestration.
- **DeepSeek-R1 with full 671B parameters**: Most "DeepSeek-R1" cloud offerings route to a distilled version (1.5B to 70B). SambaNova Cloud runs the full 671B model, including the chain-of-thought reasoning, on the SN40L — at 80+ tok/s with sub-second time-to-first-token.
- **Dataflow efficiency**: The RDU's compiled dataflow graph eliminates the weight-fetch bottleneck. For workloads with long context windows (10K-100K input tokens), SambaNova's prefill speed is 5-10x faster than equivalent GPU deployments, because the model weights stay on-chip and don't need to be re-streamed from HBM for every prompt.
- **OpenAI API compatibility**: Drop-in replacement for OpenAI's Chat Completions API. Uses the same request/response format, supports streaming, function calling, JSON mode, and the system/user/assistant message structure. Migration requires changing the base URL and API key.
- **Energy efficiency**: Per published benchmarks, the SN40L delivers 5-10x better tokens-per-joule than equivalent GPU clusters. For enterprises with sustainability targets or high power costs, this is a meaningful differentiator at scale.
- **No rate limit noise**: SambaNova Cloud publishes no soft rate limits. You pay for what you use, throughput scales with your prepaid balance. No 429 errors or quota surprises during traffic spikes.
- **Private deployment option**: Beyond the cloud, SambaNova sells the DataScale system (8-16 SN40L SambaNodes in a rack) for on-premises deployment. This is the option for government, healthcare, and finance customers who cannot send data to public clouds.

## Limitations to Consider

- **China access requires proxy**: SambaNova Cloud is hosted in the US. There's no China-region deployment or CDN edge. Developers in mainland China need a stable overseas proxy or VPN. For China-direct access, DeepSeek or Alibaba Cloud (Bailian) are better options.
- **Limited model selection**: SambaNova Cloud focuses on the most strategic models: Llama family, DeepSeek family, Qwen family, and the upcoming sambanova-1. You won't find Mixtral, Phi-3, Gemma, BGE embeddings, or Stable Diffusion. If your pipeline requires multiple model types, you'll need a secondary provider.
- **No cache-aware pricing**: OpenAI, Anthropic, DeepSeek, and Google offer reduced rates for cached input tokens (50-90% off). SambaNova doesn't have this feature yet, so repeated prompt prefixes are billed at full price.
- **No embeddings or image generation**: SambaNova is a pure text-in/text-out inference engine. It does not support text embeddings, image generation, audio processing, or speech-to-text. You'll need a complementary provider for multimodal pipelines.
- **Enterprise pricing opaque**: Cloud pricing is transparent per token. Enterprise pricing for DataScale on-prem systems and high-volume cloud contracts goes through SambaNova's sales team — no public rate sheet, no self-serve quote.
- **Newer entrant**: SambaNova Cloud launched in 2024. The model catalog, developer tools, and ecosystem integrations are still maturing. Cerebras, Groq, and Together AI have more mature tooling (LangChain, LlamaIndex, vLLM compatibility).

## SambaNova vs. Cerebras vs. Groq vs. Together AI vs. Replicate

| Factor | SambaNova | Cerebras | Groq | Together AI | Replicate |
|--------|-----------|----------|------|-------------|-----------|
| **Hardware** | SN40L RDU | WSE-3 wafer | LPU | A100/H100 | A10G/H100 |
| **Llama 3.3 70B Speed** | 600+ tok/s | 2,000+ tok/s | 450 tok/s | 120 tok/s | 80 tok/s |
| **Llama 3.1 8B Speed** | 1,200+ tok/s | 4,500+ tok/s | 900 tok/s | 280 tok/s | 200 tok/s |
| **405B support** | ✅ Exclusive | ❌ No | ❌ No | ✅ Hosted, slower | ❌ No |
| **DeepSeek-R1 full** | ✅ 671B | ❌ | ❌ | ✅ Hosted | ❌ |
| **Pricing (70B, $/M tok)** | $0.30 in + $0.70 out | $0.60 (combined) | $0.79 in + $0.99 out | $0.59 in + $0.79 out | ~$1.20/M |
| **Combined 70B cost** | ~$1.00 | $0.60 | $1.78 | $1.38 | $1.20 |
| **Model diversity** | ~10 curated | ~6 LLMs | ~20 models | 200+ models | 10K+ models |
| **Function calling** | ✅ Native | ✅ Native | ✅ Native | ✅ Native | ❌ Limited |
| **Embeddings** | ❌ | ❌ | ❌ | ✅ Multiple | ✅ Many |
| **Free tier** | $5 credits | $5 credits | ❌ No | $5 credits | $5 credits |
| **China access** | ❌ Proxy required | ❌ Proxy required | ❌ Proxy required | ❌ Proxy required | ❌ Proxy required |
| **Best for** | 405B / R1 hosting | Ultra-fast text serving | Fast text serving | Production multi-model | Model experimentation |

### When to Choose SambaNova

SambaNova Cloud is the right pick when you need **frontier-size models at speed**:

- **Llama 3.1 405B production serving** — the only cloud provider with sub-second TTFT on the full 405B model
- **DeepSeek-R1 reasoning** — full 671B chain-of-thought, not a distilled smaller model
- **Long-context workloads** — 10K-100K input prompts where GPU prefill becomes a bottleneck
- **Energy-conscious enterprises** — 5-10x better tokens-per-joule than GPU clusters
- **Hybrid cloud + on-prem** — same SN40L hardware runs in SambaNova Cloud or on-premises as DataScale
- **Government / regulated industries** — DataScale on-prem deployment for FedRAMP, IL5, or HIPAA workloads

If you need model diversity (embeddings, image gen, audio), Together AI or Hugging Face offer broader catalogs. If you need raw speed on 8B/70B models, Cerebras is faster. If you need free-tier speed testing without credit card, Groq is no longer free (free tier removed in 2025). For pure text-based LLM serving where frontier model size matters, SambaNova is the only practical option in 2026.

## Use Case Recommendations

| Use Case | Recommended | Why |
|----------|-------------|-----|
| Llama 3.1 405B production serving | **SambaNova (SN40L)** | Only cloud with sub-second 405B TTFT at per-token pricing |
| DeepSeek-R1 with full reasoning | **SambaNova (SN40L)** | Full 671B R1, not distilled; 80+ tok/s with reasoning traces |
| Real-time customer support chatbot | Cerebras (Llama 3.3 70B) | 2,000 tok/s = instant answers, lower per-token cost |
| Code completion in IDE | **SambaNova (Qwen2.5-Coder-32B)** | 800+ tok/s on a code-specialized 32B; better than 8B for completions |
| Long-context document Q&A (50K+ tokens) | **SambaNova (Llama 3.1 70B)** | On-chip weights = no HBM re-fetch penalty for long prefill |
| Production LLM serving at scale | **SambaNova or Cerebras** | SambaNova for 405B, Cerebras for 70B and below |
| Multi-model experimentation | Together AI or Replicate | More models to compare side-by-side |
| Embedding pipeline (RAG) | Hugging Face or OpenAI | SambaNova doesn't support embeddings |
| Image generation | Replicate (FLUX, SDXL) | SambaNova is text-only |
| Energy-constrained on-prem | **SambaNova DataScale** | 5-10x better tokens-per-joule than GPU racks |

## How to Get Started with SambaNova Cloud

1. **Sign up**: Visit [cloud.sambanova.ai](https://cloud.sambanova.ai) and create an account with email or Google OAuth.
2. **Get API key**: Navigate to the API Keys section in your dashboard and generate a new key. You'll receive $5 in free credits.
3. **Install SDK**: SambaNova Cloud is OpenAI-compatible. Use the standard OpenAI Python SDK:
   ```
   from openai import OpenAI
   client = OpenAI(
       api_key="your-sambanova-api-key",
       base_url="https://api.sambanova.ai/v1"
   )
   ```
4. **Pick a model**: Start with `Meta-Llama-3.1-8B-Instruct` for cheap experimentation, then move to `Meta-Llama-3.3-70B-Instruct` for production quality, and `Meta-Llama-3.1-405B-Instruct` when you need frontier capability.
5. **Send your first request**: Use the standard Chat Completions format. All OpenAI features (streaming, function calling, response_format) work out of the box.
6. **Monitor usage**: The SambaNova dashboard shows real-time token usage, latency breakdowns, and spend. Top up credits as needed.

For on-prem DataScale systems (16+ SN40L SambaNodes in a rack), contact SambaNova's enterprise sales team. Lead time is typically 8-12 weeks for hardware delivery plus on-site installation.

## FAQ

**Q: Is SambaNova Cloud actually faster than GPU-based alternatives?**
A: Yes, but not the fastest. On Llama 3.3 70B, SambaNova delivers 600+ tok/s vs. 120 tok/s on Together AI (A100) and 80 tok/s on Replicate (A10G). The SN40L's dataflow architecture keeps model weights on-chip, avoiding the HBM-fetch bottleneck that limits GPU inference. Internal benchmarks show 3-5x speedup over A100 and 5-10x speedup over A10G for typical workloads. Cerebras is faster on raw token throughput (2,000+ tok/s) but SambaNova is the only option for Llama 3.1 405B at sub-second TTFT.

**Q: How does SambaNova pricing compare to GPT-4o?**
A: SambaNova running Llama 3.3 70B costs $0.30/M input + $0.70/M output (combined ~$1.00/M for balanced usage). OpenAI GPT-4o costs $2.50/M input + $10.00/M output (combined ~$12.50/M). For typical workloads with equal input and output, SambaNova is roughly 10-12x cheaper while offering comparable or better quality on coding and reasoning tasks. For Llama 3.1 405B, SambaNova charges $3.00/M in + $5.00/M out — still significantly cheaper than GPT-4o for tasks that need 405B-class capability.

**Q: Can I use SambaNova Cloud from China?**
A: Not directly. SambaNova infrastructure is hosted in the US. Developers in mainland China need a stable overseas proxy or VPN. Some developers access SambaNova through OpenAI-compatible API resellers that aggregate multiple backends, though this adds latency. For China-direct access, consider DeepSeek or Alibaba Cloud (Bailian), both of which operate China-region deployments.

**Q: Does SambaNova Cloud support function calling and tool use?**
A: Yes — native support for OpenAI-style function calling, tool definitions, and structured output (JSON mode). This makes SambaNova a drop-in replacement for agentic workloads originally built for GPT-4o. Llama 3.3 70B and Llama 3.1 405B both have strong tool-calling capabilities, performing comparably to GPT-4o on the Berkeley Function Calling Leaderboard.

**Q: What models are available on SambaNova Cloud?**
A: As of June 2026, SambaNova Cloud hosts Meta-Llama-3.3-70B-Instruct, Meta-Llama-3.1-8B/70B/405B-Instruct, DeepSeek-R1 (full 671B), DeepSeek-V3-0324, Qwen2.5-72B-Instruct, Qwen2.5-Coder-32B-Instruct, and sambanova-1 (proprietary, in private preview). The catalog focuses on frontier-size models where the SN40L's dataflow advantage is largest. For embeddings, image generation, or audio, you'll need a complementary provider.

**Q: Does SambaNova offer dedicated endpoints or SLAs?**
A: SambaNova Cloud currently offers shared inference pools with always-hot instances. Dedicated endpoint support is in development. For production workloads, the shared pool has been reliable with consistent sub-second latency, but there is no formal SLA guarantee yet. Enterprise customers with SLA requirements should contact SambaNova directly for DataScale on-premises deployment, which includes formal uptime guarantees.

**Q: What's the difference between SambaNova Cloud and SambaNova DataScale?**
A: SambaNova Cloud is the public API hosted in SambaNova's data centers — pay per token, scale elastically, no infrastructure management. DataScale is the on-premises hardware system (8-16 SN40L SambaNodes in a rack) sold to enterprises for private deployment. DataScale is required for government, healthcare, and finance customers who cannot send data to public clouds. Pricing for DataScale goes through SambaNova's sales team and is not published.

## Conclusion

SambaNova Cloud represents a different bet on the future of LLM inference. Where Cerebras bets on raw throughput, Groq bets on low latency, and Together AI bets on model diversity, SambaNova bets on **frontier-size models at speed**. The SN40L's dataflow architecture is uniquely capable of running Llama 3.1 405B and DeepSeek-R1 671B at sub-second time-to-first-token — workloads that no GPU cloud can match at per-token pricing.

The trade-offs are real: limited model selection (no embeddings, no image gen), no China-region deployment, no cache-aware pricing, and a newer platform with less mature tooling. For model experimentation or multimodal pipelines, Together AI or Replicate offer broader catalogs. For pure speed on 8B/70B text models, Cerebras is faster and cheaper.

But for the workloads where frontier model size is the binding constraint — production 405B serving, full DeepSeek-R1 reasoning, long-context document Q&A — SambaNova is the only practical cloud option in 2026. The $5 free trial is enough to run 10 million tokens on Llama 3.1 8B and evaluate whether dataflow inference fits your workload. For enterprises with on-prem requirements, DataScale delivers the same SN40L performance in your own data center.

If you're building with Llama 3.1 405B or DeepSeek-R1 and want responses to feel instantaneous, SambaNova is worth serious consideration. The combination of dataflow speed, exclusive frontier model hosting, and OpenAI API compatibility makes it the most differentiated inference platform in 2026.

---

## Comparison Table (Final)

| Provider | Pricing Model | Best For | China Access |
|----------|---------------|----------|--------------|
| **SambaNova (SN40L)** | $0.30 in + $0.70 out (70B), $3.00 in + $5.00 out (405B) | Frontier model hosting (405B / R1) | ❌ Proxy required |
| Cerebras (WSE-3) | Combined $0.60/M tokens | Ultra-fast 8B/70B LLM serving (2,000+ tok/s) | ❌ Proxy required |
| Groq (LPU) | $0.79 in + $0.99 out per M tok | Fast 8B/70B LLM serving (450 tok/s) | ❌ Proxy required |
| Together AI | $0.59 in + $0.79 out per M tok | Production LLM serving, 200+ models | ❌ Proxy required |
| Replicate | Per-second GPU billing | Open-source model experimentation | ❌ Proxy required |
| OpenAI GPT-4o | $2.50 in + $10.00 out per M tok | Top-tier model quality & multimodal | ❌ Proxy required |
