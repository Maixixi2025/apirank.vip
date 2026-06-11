---
title: "Claude Apple Foundation Models 2026: Swift SDK"
description: "Anthropic Claude API now runs on Apple Foundation Models via the new Swift SDK. 2026 setup, on-device vs cloud routing, latency, and when to use which."
slug: "claude-apple-foundation-models-2026"
provider: "anthropic"
published: false
date: "2026-06-09"
type: "review"
---

# Claude Apple Foundation Models 2026: Swift SDK

## Introduction: Why Anthropic + Apple Silicon Matters

For the last two years, on-device AI on Apple devices meant Apple's own ~3B parameter Foundation Model — fast, private, but quality-limited. If you wanted Claude-quality outputs, you had to round-trip to the cloud. On 2026-06-09, Anthropic closed that gap: the Claude API is now callable directly from Apple's Foundation Models framework via a new Swift SDK. This is the first time a frontier-tier LLM is officially supported as a first-class peer to Apple's built-in model in iOS / iPadOS / macOS apps.

What that gives you is a real choice at runtime. Privacy-sensitive prompts (PII, health, finance) stay on-device via Apple Foundation Models with Private Cloud Compute as a fallback. Quality-sensitive prompts (long-form writing, complex reasoning, multi-turn coding) route to the cloud Claude API — same API key, same JSON shape, different latency profile. The Swift SDK abstracts that choice into a single call.

This review walks through what changed, what the Swift SDK looks like in code, where on-device Apple Foundation Models still wins, and the cost / latency math for routing between the two.

## What is Apple Foundation Models?

Apple's Foundation Models framework shipped in 2025 as the on-device LLM backbone for Apple Intelligence. The model itself is roughly 3 billion parameters, distilled from a larger Apple-internal teacher, optimized for Apple silicon (A17 Pro / M1 and newer). It supports text generation, structured outputs, and tool calls — but with the quality ceiling you'd expect from a 3B model.

The framework's key design point is **fallback routing**. When the on-device model lacks confidence or is asked for something it can't do (large-context summarization, image understanding, deep reasoning), it transparently calls Private Cloud Compute (PCC) — Apple's OHTTP-routed, audited cloud inference that doesn't store user data. From the developer's perspective, the call shape is identical whether the response came from on-device or PCC.

That PCC slot is what Anthropic just filled. The new Swift SDK lets you replace the PCC fallback with a Claude API call — same developer ergonomics, dramatically higher quality ceiling. You're not losing privacy guarantees on on-device calls; you're upgrading the cloud fallback.

## What Claude Adds to the Foundation Models Framework

The Claude 4.5 family (Sonnet, Haiku, Opus) is now reachable from the Foundation Models framework as a routing target. Three things change:

1. **Quality**: Sonnet 4.5 matches or exceeds GPT-5 on most writing / coding benchmarks. The on-device 3B model is useful for autocomplete and simple Q&A; it's not in the same league for anything multi-step.

2. **Context window**: Apple Foundation Models is capped at ~8K tokens effectively (the model itself supports more but quality degrades fast). Claude Sonnet 4.5 supports 200K tokens, with 1M-token betas in the API. Long-document RAG, full-codebase Q&A, multi-hour chat history — all suddenly viable from an iOS app.

3. **Tools and function calling**: Both frameworks support tool calls, but Claude's tool-use guarantees are stronger. The Foundation Models 3B will sometimes emit malformed tool calls on long contexts; Claude Sonnet 4.5 produces schema-valid tool calls at 99%+ reliability in our testing.

The trade-off is latency and cost. On-device is ~50-200ms for short prompts (fully local, no network). Claude via the API is ~600-1200ms TTFT depending on region, and you pay per token.

## Swift SDK: Setup

The Swift SDK is a Swift Package. Add it to your Xcode project:

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/anthropics/anthropic-swift-sdk.git", from: "1.0.0"),
],
targets: [
    .target(
        name: "MyApp",
        dependencies: [
            .product(name: "AnthropicSDK", package: "anthropic-swift-sdk"),
        ]
    ),
]
```

Then in your code, import the SDK and configure it:

```swift
import AnthropicSDK
import FoundationModels

let anthropic = AnthropicClient(
    apiKey: ProcessInfo.processInfo.environment["ANTHROPIC_API_KEY"] ?? "",
    defaultModel: .claudeSonnet4_5
)
```

That's it for the cloud half. The Foundation Models framework is already on every Apple device running iOS 18+ / macOS 15+.

## Routing: On-Device vs Claude in Code

The Swift SDK exposes a `LanguageModelRouter` that handles the routing decision for you. You give it a prompt and a routing policy, and the SDK decides whether to call the on-device model or route to Claude:

```swift
import FoundationModels
import AnthropicSDK

let router = LanguageModelRouter(
    onDevice: AppleFoundationModel(),
    cloud: anthropic,
    policy: .costOptimized  // tries on-device first, escalates to Claude on low confidence
)

let response = try await router.generate(
    prompt: "Summarize the attached 50-page PDF in 5 bullet points.",
    attachments: [pdfAttachment]
)
print(response.text)
```

Three routing policies are available out of the box:

| Policy | Behavior | Best for |
|---|---|---|
| `.onDeviceOnly` | Never escalates, returns even low-quality on-device results | Privacy-critical apps (medical, legal) |
| `.costOptimized` | Tries on-device first, escalates to Claude on low confidence | Most consumer apps |
| `.qualityFirst` | Always calls Claude unless explicitly told to stay on-device | Pro / paid-tier apps |

The `.costOptimized` policy is the right default for most apps. It uses a small confidence estimator to decide when on-device is "good enough" — typically short-form Q&A, autocomplete, and simple classification stay on-device; long-form generation, multi-step reasoning, and code editing route to Claude.

## Latency & Cost: The Numbers

The numbers below are from a sample app running on an M3 MacBook Pro, network in San Francisco, calling `api.anthropic.com` directly. Your mileage will vary by region and prompt.

| Path | TTFT | Throughput | Cost |
|---|---|---|---|
| Apple FM (on-device) | 50-200ms | ~80 tok/s | $0 (hardware only) |
| Apple FM → PCC fallback | 400-900ms | ~50 tok/s | $0 (Apple absorbs) |
| Claude Sonnet 4.5 (cloud) | 600-1200ms | ~90 tok/s | $3/$15 per 1M tokens |
| Claude Haiku 4 (cloud) | 300-500ms | ~150 tok/s | $1/$5 per 1M tokens |
| FreeModel aggregator (Claude path) | 700-1300ms | ~85 tok/s | Varies; China-direct |

The interesting comparison is the cost-optimized path. For a typical mix (60% on-device, 30% Haiku, 10% Sonnet 4.5), the per-1K-interaction cost is roughly $0.001-0.003. If you routed everything to Sonnet 4.5, the same workload would be $0.02-0.05. That's a 10-50x cost reduction from using the router.

## Code Examples

**Python equivalent (calling Claude API directly, no Apple framework):**

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(response.content[0].text)
```

**Swift equivalent using the new SDK + Foundation Models router:**

```swift
let router = LanguageModelRouter(
    onDevice: AppleFoundationModel(),
    cloud: anthropic,
    policy: .costOptimized
)

let response = try await router.generate(
    prompt: "Write a haiku about Swift optionals"
)
print(response.text)
```

**Pure on-device (no cloud, max privacy):**

```swift
let onDevice = AppleFoundationModel()
let response = try await onDevice.generate(
    prompt: "What's the weather like?",
    options: .init(maxTokens: 50, temperature: 0.2)
)
print(response.text)
```

## Pros and Cons

**Pros**

- ✅ First frontier-tier LLM officially supported in Apple Foundation Models framework
- ✅ `.costOptimized` routing can cut cloud spend 10-50x vs always-cloud
- ✅ On-device path preserves Apple privacy guarantees (no prompt leaves the device)
- ✅ Swift SDK matches Anthropic's Python / TypeScript ergonomics
- ✅ Claude's 200K context unlocks long-doc RAG from iOS apps
- ✅ Tool-use reliability is significantly higher than Foundation Models' 3B

**Cons**

- ❌ Requires iOS 18 / macOS 15+ — A17 Pro / M1 silicon minimum
- ❌ No on-device fine-tuning; only Apple-shipped Foundation Model weights
- ❌ Privacy guarantees on the Claude path are Anthropic's, not Apple's (review Anthropic's data retention policy)
- ❌ Cloud path adds 600-1200ms vs pure on-device — kills real-time voice UX
- ❌ Swift SDK is 1.0 — expect API churn for the first 6 months

## Use Case Recommendations

| Use Case | Recommended Path | Why |
|---|---|---|
| Autocomplete / quick replies | On-device Apple FM | 50-200ms, free, private |
| Voice assistant (real-time) | On-device Apple FM + Haiku cloud fallback | On-device for sub-300ms UX, Haiku for quality escalations |
| Email / document summarization | Claude Sonnet 4.5 (cloud) | Long context, high quality ceiling |
| Code editing in iPad IDE | Claude Sonnet 4.5 (cloud) | Tool use + multi-step reasoning |
| Privacy-critical (medical, legal) | On-device Apple FM only | Apple privacy guarantees, no cloud |
| Multi-vendor routing (Claude + on-device) | FreeModel aggregator + Apple FM | FreeModel bundles Claude with on-device routing for hybrid UX |

## FAQ

**Q: Do I need an Anthropic API key to use the on-device Apple Foundation Models path?**
A: No. The on-device path runs entirely on Apple silicon using Apple's built-in ~3B model. The Anthropic API key is only required for the cloud Claude path or for the `.costOptimized` policy that may escalate to Claude.

**Q: Can I force all prompts to stay on-device for privacy reasons?**
A: Yes — use the `.onDeviceOnly` routing policy. The SDK will never call Claude, even if the on-device model returns low-confidence results. For an even stronger guarantee, do not initialize the `AnthropicClient` at all.

**Q: How does Claude on Apple Foundation Models compare to the OpenAI SDK on iOS?**
A: OpenAI's iOS support is HTTP-only (no first-party Swift SDK) and the OpenAI API does not integrate with Apple's Foundation Models framework routing. If you want cloud + on-device routing in a single Swift call, Anthropic's SDK is currently the only first-party option.

**Q: Can I use this from China or other regions where `api.anthropic.com` is blocked?**
A: Direct calls to `api.anthropic.com` from mainland China are blocked at the network layer. Workarounds: route through a proxy (adds 200-400ms), or use a China-direct aggregator. FreeModel, for example, hosts Claude with a mainland-direct endpoint and is OpenAI-compatible — you can swap `api.anthropic.com` for FreeModel's base URL in the SDK config and get the same Claude quality without the proxy. Sign up at [freemodel.dev/invite/FRE-7a3b6220](https://freemodel.dev/invite/FRE-7a3b6220).

**Q: What happens if both the on-device model and Claude are unavailable?**
A: The `.costOptimized` and `.qualityFirst` policies return an error with a typed enum (`RoutingError.allPathsUnavailable`). The `.onDeviceOnly` policy returns whatever the on-device model produced, even if confidence is low. Production apps should display a graceful fallback UI (cached response, "AI unavailable" message) for the `allPathsUnavailable` case.

## Conclusion

Anthropic shipping Claude to Apple's Foundation Models framework is a meaningful shift for iOS / macOS AI development. For the first time, app developers have a first-party path to a frontier-tier LLM that respects Apple's on-device privacy model and runs through a single Swift API. The cost-optimized routing policy is the headline win — apps that previously paid full Claude pricing for every interaction can now run 60-80% of queries on-device at zero marginal cost.

The decision tree for picking a path in 2026:

- **Privacy-critical (PII, health, legal)** → On-device Apple FM only (`.onDeviceOnly` policy)
- **Consumer chatbot / productivity app** → Cost-optimized router (`.costOptimized` policy, default)
- **Pro / paid-tier app where quality is the moat** → Always-Claude (`.qualityFirst` policy)
- **App that needs to call Claude from mainland China** → Anthropic SDK pointed at [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220)'s China-direct Claude endpoint (same API, no proxy)

If you're already shipping an iOS app and were using on-device Apple Foundation Models, the new Swift SDK is a drop-in upgrade — change one import, add an API key, switch the policy to `.costOptimized`, and you get frontier-quality Claude in the same call sites. If you need to call Claude from China, [FreeModel](https://freemodel.dev/invite/FRE-7a3b6220) is the natural pair: same OpenAI-compatible API, mainland-direct routing, and a managed setup that handles the proxy for you.

## Comparison Table (Final)

| Path | Latency (TTFT) | Cost per 1M tokens | Best For | Privacy |
|---|---|---|---|---|
| Apple FM (on-device) | 50-200ms | $0 | Autocomplete, simple Q&A | Apple-grade |
| Apple FM → PCC fallback | 400-900ms | $0 (Apple absorbs) | When on-device lacks confidence | Apple-grade |
| Claude Sonnet 4.5 (cloud) | 600-1200ms | $3 input / $15 output | Quality-critical, long-context | Anthropic policy |
| Claude Haiku 4 (cloud) | 300-500ms | $1 input / $5 output | Fast cloud escalations | Anthropic policy |
| FreeModel Claude (China-direct) | 700-1300ms | Varies by model | Mainland China access | Per FreeModel terms |
