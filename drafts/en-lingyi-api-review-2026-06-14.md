# 01.AI Yi API 2026: Yi-Lightning at ¥0.99/1M Tokens — Smart Routing for China's Cost-Conscious AI Workloads

**Date:** June 14, 2026  
**Provider:** 01.AI (零一万物)  
**Category:** Domestic (China)  
**Slug:** lingyi-api-review  

---

## Introduction: 01.AI's Unusual Value Proposition

01.AI, founded by Dr. Kai-Fu Lee (former Google China president and Microsoft Asia Research director), enters the AI API market with a clear thesis: Chinese developers want OpenAI-compatible APIs at Chinese-friendly prices. The result is Yi-Lightning, a single API endpoint priced at ¥0.99 per million total tokens — combining input and output into one unified rate — with a smart routing layer that automatically selects the best model for each request.

Unlike most providers that expose individual model checkpoints, 01.AI's Yi-Lightning endpoint uses an intelligent routing system. Each request is analyzed and dispatched to one of three underlying models: **DeepSeek-V3**, **Qwen3.5-30B-A3B**, or **Yi-Lightning (01.AI's own model)**. The user never sees which model was chosen — they just get back a response at a fixed price of ¥0.99/1M total tokens.

This model-as-a-service abstraction is 01.AI's biggest differentiator and its most controversial design choice. For teams that care about "what model am I actually calling?", the black-box routing is unsettling. For teams that care about "is the response good enough and is the price low enough?", the abstraction is liberating.

---

## What 01.AI Yi API Actually Offers

01.AI's API platform at `platform.lingyiwanwu.com` exposes two models today:

| Model | Best For | Pricing (Total Tokens) |
|-------|----------|----------------------|
| **Yi-Lightning** | General chat, reasoning, coding — smart routing to DeepSeek-V3 / Qwen3.5 / Yi-Lightning | ¥0.99/1M total tokens |
| **Yi-Vision-v2** | Visual understanding — routing to Qwen2.5-VL-72B or Yi-Vision-V2 | ¥6.00/1M total tokens |

Both models use **combined input+output billing** — there is no separate input and output rate. You pay ¥0.99 for every million tokens regardless of whether they went into the prompt or came out of the generation.

The smart routing mechanism is the key innovation. When you send a request to Yi-Lightning, 01.AI's routing layer evaluates the request characteristics (domain, complexity, language, token budget) and selects among:

- **DeepSeek-V3** — best for complex reasoning, math, and code generation
- **Qwen3.5-30B-A3B** — best for Chinese-language tasks and general knowledge
- **Yi-Lightning (01.AI proprietary)** — best for bilingual chat and balanced performance

The routing is non-deterministic — you cannot pin to a specific underlying model. This is listed as both a feature (simplified decision-making) and a limitation (no model control).

---

## API Surface: Standard OpenAI-Compatible Endpoint

The Yi API is 100% OpenAI-compatible. The base URL is `https://api.lingyiwanwu.com/v1`, and the `/v1/chat/completions` endpoint accepts the standard OpenAI request body. Streaming, JSON mode, and function calling are all supported.

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.lingyiwanwu.com/v1",
    api_key="YOUR_YI_API_KEY"
)

completion = client.chat.completions.create(
    model="yi-lightning",  # or "yi-vision-v2" for vision tasks
    messages=[{"role": "user", "content": "Explain the concept of smart routing in 3 sentences."}],
    max_tokens=512
)

print(completion.choices[0].message.content)
```

For teams already using the OpenAI Python SDK, migration is a one-line change: swap the `base_url` and `api_key`. No SDK rewrite, no request body restructuring.

The API also supports:
- **Streaming** via `stream=True` for real-time token delivery
- **Function calling** for tool-use workflows
- **JSON mode** via `response_format={"type": "json_object"}`

---

## Pricing: The ¥0.99/1M Story

At ¥0.99 per million total tokens, Yi-Lightning is one of the cheapest API offerings available in China. For comparison, here is how it stacks up against other providers:

| Provider | Equivalent Model | Price per 1M tokens | Billing Model |
|----------|-----------------|-------------------|---------------|
| **01.AI Yi-Lightning** | Smart routing (DeePSeeK-V3 / Qwen3.5 / Yi) | **¥0.99** | Combined input+output |
| **DeepSeek** (official) | DeepSeek-V3 | ~¥1.00-$2.00 | Separate input/output |
| **SiliconFlow** | DeepSeek-V3 hosted | ~¥1.00-$4.00 | Separate input/output |
| **Tencent Hunyuan** | Large model | ~¥0.80-¥3.00 | Separate input/output |
| **OpenAI GPT-4o** | GPT-4o (USD) | ~$2.50/¥18+ | Separate input/output |

The ¥0.99 price point is remarkable for what it bundles. You get access to DeepSeek-V3 — one of the strongest open-weight models for reasoning and coding — at a lower effective rate than calling DeepSeek directly through its official API. The routing to Qwen3.5 for Chinese tasks and Yi's own model for bilingual chat makes the endpoint versatile across use cases.

**Yi-Vision-v2** at ¥6.00/1M total tokens is more expensive but still competitive for vision tasks in China, where alternative vision APIs range from ¥4 to ¥20 per million tokens.

---

## Availability and Getting Started

01.AI is a Chinese company with full domestic compliance:

- ✅ **ICP-filed** — operates legally within China's regulatory framework
- ✅ **Phone number registration** — supports Chinese mainland phone numbers
- ✅ **Alipay / WeChat Pay** — domestic payment methods accepted
- ✅ **Direct connectivity** — no proxy needed within mainland China
- ❌ **No initial free credits** — you must recharge before making API calls
- ✅ **Free rate limit tier** — limited RPM/TPM available without payment

Registration is straightforward: visit `platform.lingyiwanwu.com`, register with your phone number, and top up your account. There is no free initial credit, so the first API call requires a deposit — unlike competitors that offer ¥5-¥20 new-user credits.

---

## Pros and Cons

**Pros**

- ✅ **¥0.99/1M total tokens** — among the cheapest API rates in China for frontier-level responses
- ✅ **Smart routing** — automatically selects DeepSeek-V3, Qwen3.5, or Yi-Lightning per request
- ✅ **100% OpenAI-compatible** — zero SDK migration cost
- ✅ **Combined billing** — no need to track input vs output separately, one flat rate
- ✅ **Domestic availability** — ICP-filed, Alipay/WeChat Pay, mainland direct access
- ✅ **Founded by Dr. Kai-Fu Lee** — strong research pedigree and open-source contributions
- ✅ **Streaming, function calling, JSON mode** — all supported

**Cons**

- ❌ **Only 2 API models** — Yi-Lightning + Yi-Vision-v2, no direct access to Llama, Qwen, or other open models
- ❌ **Smart routing is non-deterministic** — you cannot pin to DeepSeek-V3 or control which model answers
- ❌ **Combined billing is opaque** — you cannot tell if you are paying ¥0.99 for cheap DeepSeek-V3 inference or expensive Yi-Lightning compute
- ❌ **No free initial credits** — must deposit before first API call
- ❌ **English support is weaker** — documentation and community are primarily in Chinese
- ❌ **No model-level SLAs** — routing means individual model latency and quality vary

---

## Use Case Recommendations

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| General bilingual chat | Yi-Lightning | ¥0.99/1M, routing auto-selects best model |
| Chinese-language Q&A | Yi-Lightning | Routes to Qwen3.5-30B-A3B for Chinese tasks |
| Complex reasoning / math | Yi-Lightning | Routes to DeepSeek-V3 for hard problems |
| Image understanding | Yi-Vision-v2 | ¥6.00/1M for vision tasks |
| Cost-sensitive bulk processing | Yi-Lightning | Flat ¥0.99/1M rate, no surprise pricing |
| Production systems needing model control | ❌ Not recommended | Non-deterministic routing is a reliability concern |

---

## Comparison: 01.AI Yi vs Key Competitors

| Provider | Best For | China Access | Billing | Models |
|----------|----------|-------------|---------|--------|
| **01.AI Yi** | Smart routing, ¥0.99 flat rate | ✅ Direct | Combined | 2 (routed) |
| **DeepSeek** | Direct DeepSeek-V3/R1 access | ✅ Direct | Separate | 3 |
| **SiliconFlow** | Open-source model diversity | ✅ Direct | Separate | 100+ |
| **Tencent Hunyuan** | Enterprise Chinese LLM | ✅ Direct | Separate | ~5 |
| **Novita AI** | Open-source + proprietary hybrid | ✅ Direct | Separate | 200+ |
| **FreeModel** | Multi-provider aggregator | ✅ Direct | Varies | 50+ |

---

## FAQ

**Q: Does Yi-Lightning let me choose which underlying model to use?**
A: No. The smart routing system selects one of DeepSeek-V3, Qwen3.5-30B-A3B, or Yi-Lightning automatically per request. There is no parameter to pin to a specific model. If you need deterministic model selection, use DeepSeek directly or an aggregator like FreeModel.

**Q: What does "combined billing" mean in practice?**
A: 01.AI bills on total tokens — input tokens plus output tokens combined. There is no separate rate for prompts vs completions. You pay ¥0.99 for every million tokens in the sum total. This simplifies cost tracking but prevents separate cost optimization of prompt vs generation.

**Q: Can I use 01.AI Yi from outside China?**
A: Yes, the API is accessible globally, but the platform is optimized for Chinese users. English documentation is limited, and customer support response times may be slower for non-Chinese accounts. Payment in CNY via Alipay/WeChat Pay requires a Chinese payment method.

**Q: How fast is Yi-Lightning compared to DeepSeek directly?**
A: 01.AI does not publish per-model latency benchmarks. Since routing adds a decision layer before inference, expect slightly higher time-to-first-token versus calling DeepSeek-V3 directly. In practice, most users report response times under 2 seconds for typical chat queries.

**Q: Is Yi-Lightning suitable for production workloads?**
A: Yes, for workloads where model selection non-determinism is acceptable. For scenarios requiring specific model behavior (e.g., always using DeepSeek-V3 for math), the routing abstraction is a liability. Consider FreeModel as a multi-provider aggregator if you need pinned model access alongside 01.AI's pricing.

---

## Conclusion

01.AI Yi occupies a unique niche in China's AI API landscape. It is not trying to be the broadest catalog (2 models), the fastest (routing adds overhead), or the most transparent (black-box model selection). Instead, it offers a simple proposition: pay ¥0.99 per million total tokens and get competitive responses routed automatically across frontier-level models.

The value is clearest for cost-sensitive teams in China who want OpenAI-compatible API access without managing model selection, without worrying about input vs output pricing splits, and without paying international USD rates. The ¥0.99/1M price point makes Yi-Lightning viable for high-volume chat, customer service, content generation, and bulk classification.

For teams that need more control over model selection, direct DeepSeek access, or multi-provider routing with fixed model pins, FreeModel at [freemodel.dev/invite/FRE-7a3b6220](https://freemodel.dev/invite/FRE-7a3b6220) complements the setup — it bundles 01.AI's pricing alongside OpenAI, Anthropic, and other providers behind one API key with deterministic model selection.

---

## Comparison Table (Final)

| Provider | Pricing Model | Best For | China Access |
|----------|--------------|----------|-------------|
| **01.AI Yi** | ¥0.99/1M combined | Smart routing, budget Chinese chat | ✅ Direct |
| **DeepSeek** | ¥1.00-$2.00/M separate | Direct DeepSeek-V3/R1 | ✅ Direct |
| **SiliconFlow** | ¥0.50-$4.00/M separate | Open-source model diversity | ✅ Direct |
| **Tencent Hunyuan** | ¥0.80-$3.00/M separate | Enterprise Chinese LLM | ✅ Direct |
| **Novita AI** | $0.06-$1.52/M separate | 200+ open-source | ✅ Direct |
| **FreeModel** | Varies by model | Multi-provider aggregator | ✅ Direct |
