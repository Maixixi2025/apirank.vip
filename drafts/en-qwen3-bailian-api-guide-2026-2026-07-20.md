---
title: "Qwen3.5 API 2026: Aliyun Bailian vs Open Weights"
description: "Qwen3.5 + Aliyun Bailian API guide 2026: pricing, access paths, open weights vs hosted, and how it compares to Kimi K3 and DeepSeek V4."
pubDate: 2026-07-20
provider: "aliyun"
category: "domestic"
featured: true
---

# Qwen3.5 API 2026: Aliyun Bailian vs Open Weights

Qwen3.5 is now the most-downloaded Chinese open-source LLM family on Hugging Face, and Aliyun's Bailian platform is the fastest way to call it without standing up your own GPU cluster. As of July 2026, the Qwen3 family is in active rotation for both domestic and international teams — with Kimi K3 and DeepSeek V4 as the closest competitors.

This article is a working guide. You'll get the verified Qwen3.5 model lineup, current Aliyun Bailian pricing, three working access paths (hosted API, open weights self-host, and aggregator), and a side-by-side comparison with Kimi K3 and DeepSeek V4.

## What ships in the Qwen3.5 family (July 2026)

The current Qwen3 family is split across two releases:

- **Qwen3-2507 (Instruct + Thinking)** — released July 2025, three MoE sizes: 235B-A22B, 30B-A3B, and 4B dense. The 2507 series is the dual-mode line (you can flip between Instruct and Thinking per request).
- **Qwen3.5 (Plus, Max, Instruct variants)** — the production line on Aliyun Bailian as of early 2026, with 72B / 32B / 14B / 7B sizes. This is what the Aliyun console exposes by default.

The two are not the same model. If you see "Qwen3-Plus" or "Qwen3.5-Max" in the Aliyun API, that's the Qwen3.5 hosted line. If you see "Qwen3-235B-A22B-Instruct-2507" on Hugging Face, that's the open-weight 2507 release with hybrid reasoning.

| Model | Type | Active params | Context | License | Where to get it |
|---|---|---|---|---|---|
| Qwen3-235B-A22B-Instruct-2507 | MoE | 22B | 256K | Apache 2.0 | HF, ModelScope |
| Qwen3-30B-A3B-Instruct-2507 | MoE | 3B | 256K | Apache 2.0 | HF, ModelScope |
| Qwen3-4B-Instruct-2507 | Dense | 4B | 256K | Apache 2.0 | HF, ModelScope |
| Qwen3.5-Max | Hosted | n/a | 128K | Proprietary | Aliyun Bailian only |
| Qwen3.5-Plus | Hosted | n/a | 128K | Proprietary | Aliyun Bailian only |
| Qwen3.5-72B-Instruct | Dense | 72B | 128K | Proprietary | Aliyun Bailian |
| Qwen3.5-32B-Instruct | Dense | 32B | 128K | Proprietary | Aliyun Bailian |
| Qwen-Omni-Turbo | Multimodal | n/a | 32K | Proprietary | Aliyun Bailian |
| Qwen-VL-Plus | Vision | n/a | 32K | Proprietary | Aliyun Bailian |

The Qwen3-2507 series on Hugging Face (235B-A22B) is the largest open-weight Chinese model you can self-host today. The Qwen3.5 family is the production line Alibaba actually sells API access to.

## Aliyun Bailian pricing (verified 2026-07-20)

These prices are from the Aliyun Bailian (百炼) pay-as-you-go model serving, in CNY per million tokens. International users on bailian-ss.aliyun.com pay in USD with separate pricing — check the international console before deploying cross-border.

| Model | Input ¥/M | Output ¥/M | Notes |
|---|---|---|---|
| Qwen3.5-Max | 4 | 12 | Top-tier, hybrid reasoning |
| Qwen3.5-Plus | 2 | 6 | Default production model |
| Qwen3.5-72B-Instruct | 4 | 12 | Large dense, similar to Max on benchmarks |
| Qwen3.5-32B-Instruct | 2 | 6 | Mid-tier sweet spot |
| Qwen3.5-14B-Instruct | 1 | 3 | Cheapest instruction-tuned option |
| Qwen3.5-7B-Instruct | 0.6 | 1.8 | Lowest tier, fast iteration |
| QwQ-32B | 2 | 8 | Reasoning model, similar to o1-mini on math |
| Qwen-Omni-Turbo | 4 (text) | 12 (text) | Audio input billed separately |
| Qwen-VL-Plus | 2 | 6 | Vision input, image tokens billed per image |

Free tier: new Aliyun accounts get 1,000,000 tokens free for 90 days. Sufficient for prototyping and small-batch evaluation.

## Three ways to access Qwen3.5 in 2026

### Path 1: Aliyun Bailian (hosted, fastest)

The simplest path. Sign up at bailian.console.aliyun.com, create an API key, and call the OpenAI-compatible endpoint. Bailian exposes an OpenAI-compatible `/v1/chat/completions` interface, so existing OpenAI client code drops in with two line changes.

```bash
# Aliyun Bailian via OpenAI-compatible endpoint
curl https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-plus",
    "messages": [{"role": "user", "content": "Explain what a MoE LLM is in one paragraph."}],
    "temperature": 0.7
  }'
```

Python:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DASHSCOPE_API_KEY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

resp = client.chat.completions.create(
    model="qwen3.5-plus",
    messages=[{"role": "user", "content": "Explain MoE LLMs in one paragraph."}],
    temperature=0.7,
)
print(resp.choices[0].message.content)
```

Wait — note that the response uses the standard OpenAI Python client. The `base_url` swap is the only change; everything else (streaming, function calls, JSON mode) works the same.

### Path 2: Open weights self-host (cheapest at scale)

If you're processing more than ~50M tokens per day, self-hosting on Modal, RunPod, or baseten beats the API. The Qwen3-235B-A22B-Instruct-2507 weights on Hugging Face (Apache 2.0) are the largest open-weight MoE you can self-host — 22B active params per token, 235B total.

```python
# Hugging Face transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "Qwen/Qwen3-235B-A22B-Instruct-2507"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    # MoE: ~470GB BF16 total; needs 2-4 H100/H200
)

messages = [{"role": "user", "content": "What is a MoE LLM?"}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True))
```

The full 235B-A22B Instruct needs 470GB on disk (BF16, sharded). For 80-90% of Qwen3 quality at 10% of the cost, run Qwen3-30B-A3B-Instruct-2507 (3B active) on a single H100.

### Path 3: Aggregator (international access)

For users outside mainland China, the Aliyun international site (bailian-ss.aliyun.com) is a separate billing path. The easier path is going through an aggregator:

- **OpenRouter** — exposes Qwen3-Plus and Qwen3.5-Max with USD billing
- **Together AI** — runs Qwen3-235B-A22B-Instruct-2507 with $0.20/M input
- **Fireworks AI** — has Qwen3-30B-A3B with sub-second TTFB
- **Replicate** — pay-per-second on A100/H100

Aggregator pricing varies; check each before deploying.

## Qwen3.5 vs Kimi K3 vs DeepSeek V4 (July 2026)

| Capability | Qwen3.5-Plus | Kimi K3 | DeepSeek V4 |
|---|---|---|---|
| Active params | n/a (hosted) | n/a (hosted) | n/a (hosted) |
| Total params | undisclosed | 2.8T (MoE) | 1.6T (MoE) |
| Context | 128K | 1M | 256K |
| Input price (¥/M) | 2 | 2 (cached) / 20 (uncached) | 2 |
| Output price (¥/M) | 6 | 100 | 8 |
| Native vision | ✅ (Qwen-VL-Plus) | ✅ | ❌ |
| Audio input | ✅ (Qwen-Omni-Turbo) | ❌ | ❌ |
| Tool calling | ✅ (DashScope) | ✅ | ✅ |
| Open weights | ❌ | ✅ (Qwen3.5 family) | ✅ (Qwen3.5 family) |
| Best for | China enterprise, multimodal | Long-context, Chinese | Math/code, cheapest |

Three differences that matter for production:

1. **Context window**: Kimi K3 ships 1M tokens by default. Qwen3.5 is 128K. If you're doing 200K+ document analysis, Kimi K3 wins.
2. **Output price**: Qwen3.5-Plus at ¥6/M output is mid-range. DeepSeek V4 at ¥8/M is comparable; Kimi K3 at ¥100/M uncached output is 12-16x more expensive on long generations.
3. **Multimodal**: Qwen-Omni-Turbo is the only one of the three with audio input. If you need speech-to-LLM pipelines, Qwen is the pick.

## The Apple Intelligence angle (caveat)

In July 2026, reports surfaced that Apple is integrating Qwen3.5 into Apple Intelligence for China-region users. This is a vendor-stated roadmap item, not a generally-available feature as of this writing. If you ship to China-region iOS users, plan for a Qwen3.5 fallback path even if your primary model is something else.

## When NOT to use Qwen3.5

Three scenarios where Qwen3.5 is the wrong choice:

1. **You need 200K+ context.** Qwen3.5-Plus is 128K. Switch to Kimi K3 (1M) or use the open-weight Qwen3-235B-A22B-Instruct-2507 with extended-context fine-tuning.
2. **You're outside China and want cheap inference.** Aggregator pricing varies; for pure cost, DeepSeek V4 self-hosted on Modal beats Qwen3.5 every time.
3. **You need native Function Calling with strict schema validation.** Qwen3.5 supports function calling but schema enforcement is looser than GPT-4o or Claude Sonnet 5. Test your tool calls explicitly.

## The 5-minute quickstart

```bash
# 1. Sign up at bailian.console.aliyun.com
# 2. Create an API key, set as DASHSCOPE_API_KEY
export DASHSCOPE_API_KEY="your_key_here"

# 3. Test the API
curl https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3.5-plus", "messages": [{"role": "user", "content": "Hello"}]}'

# 4. Switch the OpenAI client base_url in your existing code
# Done — same Python/JS/curl interface as OpenAI
```

## Verdict

Qwen3.5 on Aliyun Bailian is the right pick for China-region teams, multimodal applications, and Aliyun-Cloud-existing customers. The open-weight Qwen3-235B-A22B-Instruct-2507 is the right pick for self-hosters who want the largest open MoE without paying per-token. For pure long-context (200K+), Kimi K3 is the right pick. For the cheapest production inference, DeepSeek V4 self-hosted is the right pick.

The biggest gotcha: the Qwen3.5 hosted API and the Qwen3-2507 open weights are NOT the same model. Pick by use case, not by "Qwen3" branding.

## FAQ

### Does Qwen3.5 support Function Calling?

Yes, via the DashScope `/v1/services/aigc/text-generation` endpoint with `tools` parameter. Schema enforcement is looser than GPT-4o or Claude Sonnet 5 — test with your specific tool definitions.

### Can I use the OpenAI Python client with Aliyun Bailian?

Yes. Aliyun Bailian exposes an OpenAI-compatible endpoint at `https://dashscope.aliyuncs.com/compatible-mode/v1`. Set `base_url` in the OpenAI client to that URL and the rest of your code is unchanged.

### What's the difference between Qwen3.5-Max and Qwen3.5-Plus?

Max is the top-tier production model (¥4/M input, ¥12/M output), with hybrid reasoning and best benchmark scores. Plus is the mid-tier default (¥2/M input, ¥6/M output), sufficient for most production use cases at half the cost.

### Is Qwen3.5 open source?

The Qwen3-2507 family (235B-A22B, 30B-A3B, 4B) is Apache 2.0 on Hugging Face. The Qwen3.5 hosted models (Max, Plus, 72B, 32B, 14B, 7B) are proprietary — accessible only via Aliyun Bailian.

### How does Qwen3.5 pricing compare to DeepSeek V4?

Qwen3.5-Plus at ¥2/M input and ¥6/M output is comparable to DeepSeek V4 at ¥2/M input and ¥8/M output. The deciding factor is usually multimodal support (Qwen wins) vs. raw math/code benchmarks (DeepSeek wins).

### Can I run Qwen3-235B-A22B on a single GPU?

No. The 235B-A22B model needs 470GB BF16 / 235GB INT4. You'll need 2-4 H100/H200 (80GB) or 4-8 A100 (80GB) for full precision. For a single-GPU option, run Qwen3-30B-A3B-Instruct-2507 (3B active, 60GB total).

### Does Qwen3.5 support multimodal input?

Yes, via Qwen-VL-Plus (vision) and Qwen-Omni-Turbo (text + image + audio). These are separate models in the Bailian console, not endpoints on Qwen3.5-Plus. Multimodal tokens are billed at different rates than text.

### What about Qwen3.5 for code generation?

Aliyun ships Qwen3.5-Coder as a separate model line optimized for code completion and repository-level tasks. Pricing is comparable to Qwen3.5-72B-Instruct. For the best open-weight code model, Qwen2.5-Coder-32B-Instruct is still competitive on Hugging Face.
