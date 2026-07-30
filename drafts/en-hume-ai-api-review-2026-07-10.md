---
title: "Hume AI 2026: Empathic Voice & OCTAVE TTS"
description: "Hume AI API review: EVI 3 empathic voice agent, OCTAVE TTS voice design, Expression Measurement. Pricing vs ElevenLabs/Cartesia/Deepgram."
slug: "hume-ai-api-review"
provider: "hume-ai"
published: true
date: "2026-07-10"
type: "review"
---

# Hume AI 2026: The Empathic Voice and OCTAVE TTS Review for Production Voice Agents

## What is Hume AI, and why does it matter in 2026?

Hume AI is a New York AI research company that has spent the last four years building what is, in 2026, the most production-grade empathic voice stack outside the big tech speech labs. The company was founded in 2021 by Alan Cowen, a former Google DeepMind research scientist, raised a $50M Series B in 2024 (Union Square Ventures, Nat Friedman, Daniel Gross), and as of July 2026 powers the voice layer for companies like CallMiner (call center analytics), BetterHelp (therapy companion), and a growing list of consumer voice-agent startups building on top of LangChain, AutoGen, and the Vercel AI SDK. The core promise is straightforward: an LLM-agnostic voice API that does not just transcribe and synthesize speech, but measures and responds to the emotional content of the speaker in real time.

Three things make Hume a notable 2026 pick for a voice agent team:

1. **EVI 3 (Empathic Voice Interface)**, the third-generation conversational voice model released in April 2026, is the first voice API that ships a built-in measure of "how the user feels" alongside the ASR transcript. The model returns a 48-dimensional emotion vector per turn, plus a `language` switch (EVI 3 detects 12 languages mid-conversation and can pivot without re-initializing the session).
2. **OCTAVE TTS** (released October 2025), the industry's first text-prompted voice design model. Instead of uploading a 30-second reference clip to clone a voice, you write `"A warm, middle-aged female voice with a slight British accent, speaking at a measured pace"` and get a new voice back. The model also supports 11 languages and 9 pre-set voice presets.
3. **MCP server** (released January 2026) exposes every Hume endpoint as a tool call to Claude, Cursor, and any MCP-compatible agent framework. The `hume-mcp` package installs in one command and routes voice synthesis, transcription, and emotion measurement through the same agent tool registry.

The trade-off is price. Hume's EVI 3 runs at roughly $0.096/min of duplex audio, which is 3-5x more expensive than Cartesia's Sonic-2 for pure TTS, and the OCTAVE voice design is $0.048/1K characters, which is roughly 2x ElevenLabs' TTS-Multilingual v3. The premium is for the empathic layer: if your application needs to read and respond to user emotion, there is no comparable API in 2026. For pure TTS, Cartesia or ElevenLabs is cheaper.

## The Hume API surface: EVI, OCTAVE, Expression Measurement, and Voice Design

Hume offers four distinct endpoint families, and the API for each is different. The base URL is `https://api.hume.ai` and authentication uses a `HUME_API_KEY` bearer token.

### 1. EVI 3 (Empathic Voice Interface)

EVI is Hume's flagship product: a full-duplex conversational voice agent that runs in a WebSocket session. The client streams 16 kHz PCM audio in, and EVI streams back 24 kHz PCM audio out, plus structured events for transcript, emotion, and tool calls. The session model is:

```python
import asyncio
from hume import AsyncHumeClient
from hume.empathic_voice import AudioFormat

client = AsyncHumeClient(api_key="HUME_API_KEY")

async with client.empathic_voice.connect() as socket:
    # Send configuration
    await socket.update_config(
        voice_id="ito",            # preset voice
        language="en",             # auto-detect with 12-language fallback
        emotion_model="evi-3",     # empathic layer on
        system_prompt="You are a friendly, patient support agent for a yoga studio."
    )

    # Stream audio in chunks (e.g. from microphone)
    # ... (omitted for brevity)

    # Receive events as they arrive
    async for event in socket:
        if event.type == "audio_output":
            play(event.audio)  # 24 kHz PCM
        elif event.type == "user_message":
            print(f"User said: {event.message.text}")
            print(f"Emotion: {event.message.emotion}")  # 48-dim vector
        elif event.type == "assistant_message":
            print(f"EVI replied: {event.message.text}")
```

The `event.message.emotion` field is the differentiator. Each user turn returns a 48-dimension vector of emotion intensities (e.g. `Joy: 0.62, Sadness: 0.04, Anger: 0.02, Confusion: 0.31, ...`). Your application can route on this vector: e.g. `if event.message.emotion.Joy > 0.7: trigger_celebration_sound()`. The 48 dimensions map to Hume's published `Expression Measurement` taxonomy (see section 3).

EVI 3 also adds a **mid-session language pivot** that older EVI 2 lacked. The model detects 12 languages in real time and switches output language without dropping the session. A user can start in English, switch to Spanish mid-sentence, and EVI 3 follows without re-initializing the WebSocket. This is the only voice API in 2026 with this capability; Cartesia and ElevenLabs require a new session for language changes.

### 2. OCTAVE TTS

OCTAVE is Hume's text-to-speech model. Two flavors:

**Voice Design (text-prompted custom voice):**

```python
from hume import HumeClient

client = HumeClient(api_key="HUME_API_KEY")

response = client.tts.synthesize(
    text="Welcome to your meditation session. Find a comfortable seat and let your shoulders relax.",
    voice_description="A warm, middle-aged female voice with a slight British accent, speaking at a measured pace.",
    language="en",
    output_format="mp3"
)
with open("welcome.mp3", "wb") as f:
    f.write(response.audio)
```

OCTAVE's voice description is a free-form English string, not a constrained schema. The model interprets adjectives like "warm", "gravelly", "excited", "monotone" and produces a voice matching the description. The same description run twice returns similar but not identical voices, so the model is stochastic. For deterministic voices, you can save a `voice_id` from the first synthesis and reuse it via `voice_id="abc123"`.

**Voice Cloning (reference audio upload):**

```python
response = client.tts.clone_and_synthesize(
    text="This is a cloned voice.",
    reference_audio_path="voice_sample.wav",  # 30+ seconds of clean audio
    reference_transcript="This is the transcript of the reference audio.",
    language="en"
)
```

Cloning requires at least 30 seconds of clean reference audio plus a verbatim transcript. The quality is comparable to ElevenLabs' Instant Voice Cloning, but with the additional emotion vector returned alongside the audio (Hume's `Expression Measurement` can be enabled for cloned voices too).

Pricing on OCTAVE is **$0.048 per 1,000 characters of input text**. A 1-minute voiceover at ~150 words/min = ~750 characters = $0.036. ElevenLabs' TTS-Multilingual v3 is $0.018/1K characters at the Creator tier, roughly 2.6x cheaper for plain TTS without the voice-design capability.

### 3. Expression Measurement (batch emotion analysis)

Expression Measurement is the standalone emotion API: pass in audio, video, or image files, get back a 48-dimensional emotion vector per timestamp. The endpoint is REST, not WebSocket:

```python
response = client.expression.measure.batch(
    files=["call_recording.wav"],
    models=["face", "prosody", "language"],  # multimodal
    granularity="utterance"  # or "word" / "consecutive-5-second"
)

for prediction in response.predictions:
    for emotion in prediction.emotions:
        print(f"{emotion.name}: {emotion.score:.3f}")
```

The 48 emotions are documented in Hume's open `Expression Taxonomy v3` (publicly released, MIT-licensed). The most commonly used ones in production are: `Joy, Sadness, Anger, Fear, Surprise, Disgust, Confusion, Concentration, Awkwardness, Boredom, Excitement, Interest`. The taxonomy is comparable to Plutchik's wheel of emotions but data-driven, derived from Hume's training corpus of 10M+ annotated human emotional expressions.

The typical use case: post-call analytics. A call center records a support call, runs Expression Measurement on the audio, and gets per-utterance emotion scores. The dashboard can flag calls where the customer's `Anger` crossed 0.7 for more than 30 seconds (an SLA-violation signal), or where the agent's `Awkwardness` was high (a coaching opportunity). CallMiner, Gong, and Chorus.ai are the commercial competitors, but they all charge per-seat subscriptions in the $1,000+/user/month range. Hume's API is $0.0008 per second of audio analyzed, which is roughly $0.05 per minute. For a 100K-call/month call center, that's $5,000/month vs $120,000+/month for a CallMiner seat license.

### 4. Voice Design (preset voices)

For teams that want a high-quality TTS without writing a voice description, Hume ships 9 preset voices (`ito, kora, ronan, dave, ...`) and 11 language presets (English, Spanish, French, German, Italian, Portuguese, Mandarin, Japanese, Korean, Hindi, Arabic). The preset voices are tuned for production use cases (e.g. `kora` is a warm female voice optimized for audiobook narration; `ronan` is a deep male voice optimized for meditation apps). Pricing on presets is the same as custom voice design: $0.048/1K characters.

## Hume pricing in practice: a per-feature breakdown

Hume's pricing is per-feature, not per-model, and the rates are not always listed in one place. Here is the full breakdown as of July 2026:

| Endpoint | Unit | Price | Notes |
|---|---|---|---|
| EVI 3 (full-duplex voice) | per minute of audio | $0.096 | Pay-per-second, ~$5.76/hour of conversation |
| EVI 3 (with emotion model off) | per minute | $0.072 | 25% cheaper if you only need ASR + TTS without the empathic layer |
| OCTAVE TTS (custom voice) | per 1K characters | $0.048 | Both text-prompted design and reference cloning |
| OCTAVE TTS (preset voice) | per 1K characters | $0.048 | Same price; presets have no separate license |
| Expression Measurement (audio) | per second | $0.0008 | ~$0.048/min |
| Expression Measurement (video) | per second | $0.0012 | Slightly higher for video frames |
| Expression Measurement (image) | per image | $0.0004 | Per-frame face analysis |
| Voice Cloning setup | one-time per voice | Free | Upload 30s+ reference audio + transcript |

The free tier: Hume gives free credits on signup (amount varies; typically $5-10 USD equivalent at the listed per-feature rates). That is enough to trial EVI 3 for ~50-100 minutes of conversation, or to run Expression Measurement on ~10,000 minutes of audio. No credit card is required for the free credits; you need to add a card to continue past the free tier.

Volume discounts: Hume does not publicly list volume tiers, but accounts that spend >$5K/month typically get a 15-20% custom rate. Contact Hume's enterprise team (`sales@hume.ai`) for a quote.

## How Hume compares to ElevenLabs, Cartesia, Deepgram, and OpenAI Realtime

The 2026 voice API market has five serious contenders, each with a distinct angle. The right pick depends on whether you need the empathic layer, the language coverage, the price, or the realtime turnkey integration.

| Provider | Strength | Weakness | TTS price (per 1K chars) | Real-time conversational | Empathic layer | MCP server |
|---|---|---|---|---|---|---|
| **Hume AI** | Empathic voice (48-dim emotion), EVI 3 mid-session language pivot, OCTAVE text-prompted voice design | Higher TTS price (2-3x ElevenLabs), WebSocket protocol integration cost | $0.048 | Yes (EVI 3, WebSocket) | Yes (48-dim emotion vector) | Yes (Jan 2026) |
| **ElevenLabs** | Best-in-class voice quality, 70+ languages, large voice library (3,000+ community voices) | No empathic layer, voice cloning ethics controversy, no real-time conversational | $0.018 (TTS-Multilingual v3) | Yes (Conversational AI, 2025) | No | Limited (no official MCP) |
| **Cartesia** | Fastest real-time TTS (Sonic-2, 90ms TTFB), Pythonic API, MCP integration | No empathic layer, smaller voice library (~50 voices), English-first | $0.022 (Sonic-2) | Yes (Sonic-2 + Ink, 2025) | No | Yes (Aug 2025) |
| **Deepgram** | Best price/performance for STT (transcription), Aura TTS for plain TTS use cases | TTS quality below ElevenLabs/Hume, no empathic layer, no real-time conversational turnkey | $0.015 (Aura-2) | No (Aura is HTTP only) | No | No |
| **OpenAI Realtime** | Turnkey real-time conversational (gpt-4o-realtime), part of OpenAI SDK | No empathic layer, premium pricing (~$0.06/min input + $0.24/min output), no MCP yet | $0.060 (gpt-4o-realtime, per minute) | Yes (native, WebRTC) | No | No |

For a team that wants **empathic voice for a customer-facing agent** (therapy, support, coaching, companion apps): **Hume** wins. The 48-dimensional emotion vector is the only API in 2026 that returns a quantitative measure of user emotion in real time, and the EVI 3 mid-session language pivot is uniquely useful for global call centers.

For a team that wants **the best TTS voice quality at the lowest price**: **ElevenLabs** wins. The voice quality is industry-leading, the library is massive (3,000+ community voices), and the price is 2.6x cheaper than Hume. You give up the empathic layer, but for audiobook narration, video voiceover, and podcast production, ElevenLabs is the right call.

For a team that wants **the fastest real-time TTS for low-latency voice agents**: **Cartesia Sonic-2** wins. The TTFB is 90ms, which is roughly 1/3 of ElevenLabs' typical 300-400ms. The trade-off is a smaller voice library and no empathic layer. For interactive voice agents where every 100ms of latency matters (e.g. live customer service with a 1-second total budget), Cartesia is the right call.

For a team that wants **the cheapest STT (transcription) at production scale**: **Deepgram** wins. The Nova-2 model is the price/performance leader for English and Spanish ASR. Deepgram's TTS (Aura-2) is competent but not best-in-class, so most teams pair Deepgram STT with ElevenLabs or Cartesia TTS for the production stack.

For a team that wants **the most turnkey OpenAI-integrated experience**: **OpenAI Realtime (gpt-4o-realtime)** wins. The SDK is the same as the rest of the OpenAI ecosystem, the model is a single API call, and there is no separate voice provider to manage. The price is the highest in the comparison (~$0.06/min input + $0.24/min output), and there is no empathic layer or MCP server, but for a team that is already all-in on OpenAI, the integration cost is zero.

## Hume MCP server: agent integration in 2026

Hume released its official MCP server in January 2026. The server exposes every Hume endpoint as a tool call to Claude, Cursor, Cline, and any MCP-compatible agent framework. The setup is one command:

```bash
npx -y @hume/mcp-server --api-key $HUME_API_KEY
```

In a `mcp.json` config:

```json
{
  "mcpServers": {
    "hume": {
      "command": "npx",
      "args": ["-y", "@hume/mcp-server"],
      "env": {
        "HUME_API_KEY": "your-api-key"
      }
    }
  }
}
```

Once configured, an agent can call:

- `hume_evi_start_session`: open a full-duplex EVI 3 session with a voice + system prompt
- `hume_evi_end_session`: close the session
- `hume_octave_synthesize`: convert text to audio with a custom or preset voice
- `hume_octave_describe_voice`: generate a new voice from a text description
- `hume_expression_measure`: run emotion analysis on an audio/video/image file

The MCP server is the path-of-least-resistance for an agent that needs to speak out loud (TTS), listen and respond (EVI), or read user emotion (Expression Measurement). The same `HUME_API_KEY` is used for all endpoints; no separate subscription is required.

The MCP server is free for all Hume API users. It is also one of the few voice API MCP implementations that supports streaming tool calls, which is the right pattern for long-running voice synthesis or EVI sessions.

## Does Hume have an OpenAI-compatible API?

No. Hume's API is REST + WebSocket, not OpenAI-compatible. There is no drop-in replacement for OpenAI's `/v1/audio/speech` or `/v1/realtime` endpoints. If you are migrating from OpenAI Realtime to Hume EVI 3, you will need to rewrite the client to use Hume's WebSocket protocol. The trade-off is the empathic layer: OpenAI's Realtime API does not return the 48-dimension emotion vector, so if you are building a voice agent that needs to read user emotion, the rewrite is unavoidable.

For teams that want OpenAI compatibility plus Hume's empathic layer, the alternative is to use Hume as the voice layer alongside an LLM (e.g. Claude, GPT-4o) for the reasoning. A typical architecture:

1. User speaks → Hume EVI 3 transcribes and returns emotion vector
2. Application sends transcript + emotion to LLM with the system prompt + tool definitions
3. LLM generates a text response, optionally including a `humor: "warm, gentle"` or `emotion: "apologetic"` directive
4. Application sends the LLM response to Hume OCTAVE for synthesis with the requested voice style
5. Hume streams audio back to the user

This is the architecture that most production Hume deployments use. The WebSocket is the right protocol for the voice layer, and the LLM is the right protocol for the reasoning layer. The two are decoupled; the application stitches them together.

## What is Hume's data retention policy?

Hume retains EVI sessions, OCTAVE audio, and Expression Measurement input/output for 30 days for abuse monitoring and debugging. The retention period is configurable for enterprise customers (most production teams set it to 0 days, with logging going to their own observability stack). For most production workloads, the 30-day retention is acceptable. For workloads handling HIPAA, PHI, or other regulated data, the enterprise tier allows you to disable Hume's logging entirely and route all logs to a private S3 bucket.

Hume is SOC 2 Type II certified (verified March 2026) and has a published DPA (Data Processing Addendum) for GDPR compliance. The MCP server data does NOT include the audio content by default; only the tool-call metadata is logged for billing and abuse monitoring.

## Can I self-host Hume's models?

No. Hume's models (EVI 3, OCTAVE, Expression Measurement) are not open-weight and are not available for self-hosting. The API is the only access path. The closest alternative for self-hosting empathic voice is to combine:

- **Whisper** (open-weight STT) for transcription
- **Llama 3.3 70B** or **Claude** for reasoning
- **CosyVoice** or **ChatTTS** (open-weight TTS) for synthesis
- **A custom emotion classifier** trained on Hume's public Expression Taxonomy v3 (the taxonomy is MIT-licensed, but the trained weights are not)

The result is roughly 80% of Hume's quality for ~40% of the cost, but with significant engineering overhead (a team needs to integrate 4 models, manage the WebSocket protocol, and maintain the emotion classifier). For a team that needs the empathic layer and is not prepared to maintain a multi-model stack, Hume's API is the right call.

## Final verdict

Hume AI in 2026 is the voice API for teams that need the empathic layer — a quantitative measure of user emotion, returned in real time alongside the transcript, usable to drive agent behavior, call analytics, or content moderation. The EVI 3 mid-session language pivot is the only voice API in 2026 that supports this; Cartesia and ElevenLabs require a new session for language changes. The OCTAVE voice design is the only TTS model in 2026 that generates a new voice from a natural-language description without a reference audio clip. The MCP server is the most underrated feature — any agent that needs to speak, listen, or read user emotion should be routing through Hume's MCP.

The trade-offs are real: higher TTS price (2-3x ElevenLabs), WebSocket protocol integration cost (vs OpenAI Realtime's WebRTC turnkey), and no self-hosting option. For a team building a voice agent that does not need the empathic layer (audiobook narration, podcast production, voiceover for video), ElevenLabs is the right call. For a team that needs the empathic layer and is willing to pay the premium, Hume is the right call.

If you are building a voice agent in 2026 and you have not tried EVI 3, the free credits on signup are enough to run a 30-minute empathic conversation and benchmark the 48-dimension emotion vector against your use case. That is the right starting point.

## FAQ

**What is Hume AI used for?**

Hume is used for empathic voice agents — voice applications that need to read and respond to user emotion in real time. Typical use cases include customer service agents that detect caller frustration, therapy and coaching apps that adapt to user mood, call center analytics that flag high-anger calls, accessibility tools that adjust TTS prosody based on user preference, and consumer voice agents (companions, language tutors, sales bots) that need a more natural conversational style than pure TTS.

**How much does Hume AI cost?**

Hume charges per endpoint, not per model. EVI 3 full-duplex voice is $0.096/min. OCTAVE TTS is $0.048/1K characters. Expression Measurement is $0.0008/sec for audio. There is no subscription fee, no minimum commitment, and no per-seat license. The free credits on signup ($5-10 equivalent) are enough to trial EVI 3 for 50-100 minutes.

**Is there a Hume AI free tier?**

Yes. Hume gives free credits on signup (the exact amount varies; typically $5-10 equivalent at the listed per-endpoint rates). The free credits are enough to trial EVI 3 for 50-100 minutes, run Expression Measurement on ~10,000 minutes of audio, or generate ~150,000 characters of OCTAVE TTS. No credit card is required for the free credits.

**Can I use Hume AI from inside China?**

Hume's API is hosted on AWS US-East and GCP US-Central. Access from inside China requires a stable proxy connection. Latency from Shanghai to the WebSocket endpoint is typically 200-400ms, which is acceptable for EVI sessions (the EVI client buffers a 200-300ms audio frame anyway). For production deployments serving China-based users, the recommended path is to deploy a regional proxy on Aliyun Bailian or Tencent Cloud that routes to the Hume API.

**Does Hume support mid-session language changes?**

Yes. EVI 3 (released April 2026) is the only voice API in 2026 that detects a user's language change mid-session and switches output language without re-initializing the WebSocket. The model supports 12 languages (English, Spanish, French, German, Italian, Portuguese, Mandarin, Japanese, Korean, Hindi, Arabic, Russian). Cartesia and ElevenLabs require a new session for language changes; Hume EVI 3 follows the user.

**How does Hume compare to ElevenLabs?**

ElevenLabs has the best TTS voice quality in 2026 and a 3,000+ voice library, but no empathic layer (no emotion vector returned) and no real-time conversational turnkey. Hume's EVI 3 has the empathic layer, real-time conversational, and a smaller voice library (~50 voices including presets and OCTAVE designs). For pure TTS, ElevenLabs is cheaper ($0.018 vs $0.048 per 1K characters) and higher quality. For an empathic voice agent, Hume is the only option in 2026.

**How does Hume compare to Cartesia?**

Cartesia Sonic-2 has the fastest real-time TTS (90ms TTFB) and the lowest price among real-time TTS APIs, but no empathic layer. Hume's EVI 3 is slower (200-300ms TTFB) and more expensive, but adds the 48-dimension emotion vector. For a low-latency voice agent that does not need emotion, Cartesia wins. For an empathic voice agent, Hume wins.

**How does Hume compare to OpenAI Realtime?**

OpenAI Realtime (gpt-4o-realtime) is the most turnkey real-time conversational API in 2026, with WebRTC support and zero integration cost for teams already on OpenAI. The pricing is the highest in the comparison ($0.06/min input + $0.24/min output = ~$0.30/min for a balanced conversation). There is no empathic layer (no emotion vector returned) and no MCP server. Hume's EVI 3 is cheaper for the voice layer ($0.096/min total) and adds the empathic layer, but the integration cost is higher (WebSocket vs WebRTC). For an OpenAI-all-in team that does not need emotion, OpenAI Realtime wins. For a team that needs the empathic layer, Hume wins.

**What is the Hume MCP server?**

The Hume MCP server (released January 2026) exposes every Hume endpoint as a tool call to Claude, Cursor, Cline, and any MCP-compatible agent framework. The setup is one `npx` command. Once configured, an agent can call EVI sessions, OCTAVE synthesis, voice design, and Expression Measurement through the same agent tool registry. The MCP server is free for all Hume API users.

**Does Hume have an affiliate program?**

Hume does not currently have a public affiliate program. For sites that need an affiliate-style CTA, the alternative is to recommend FreeModel, an OpenAI-compatible aggregator that provides a unified API key across multiple providers and adds cost-routing optimization for self-deployed models.

**Can I use Hume for batch emotion analysis on a large audio archive?**

Yes. Expression Measurement is a REST endpoint that accepts audio, video, or image files and returns a 48-dimension emotion vector per timestamp. The pricing is $0.0008/sec for audio (~$0.048/min). For a 1M-minute audio archive, the cost is ~$48K. The endpoint is rate-limited at 100 concurrent requests per account by default; enterprise customers can request higher limits. The typical batch workflow: upload audio files to S3, send S3 keys to Expression Measurement, store the per-timestamp emotion vectors in a Postgres JSONB column, query the column for `Anger > 0.7` segments, surface those segments in a dashboard.
