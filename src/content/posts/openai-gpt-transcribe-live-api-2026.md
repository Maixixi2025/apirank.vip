---
title: "OpenAI GPT Transcribe API 2026: Live vs File"
description: "OpenAI GPT Transcribe costs $0.0045/min for files while GPT Live Transcribe costs $0.017/min. Compare endpoints, latency controls, limits, and code."
pubDate: "2026-07-29"
provider: openai
category: news-analysis
featured: true
---

# OpenAI GPT Transcribe API 2026: GPT Live Transcribe vs GPT Transcribe

OpenAI released two speech-to-text models on July 28, 2026, and the names make the split sound simpler than it is. **GPT Transcribe** handles completed recordings, streamed processing of uploaded files, and committed audio turns over WebSocket. **GPT Live Transcribe** handles microphone, call, or media audio that is still arriving and returns partial text as people speak.

The price gap is substantial. GPT Transcribe costs **$0.0045 per audio minute** ($0.27 per hour). GPT Live Transcribe costs **$0.017 per minute** ($1.02 per hour), about 3.8 times as much. That does not make the live model overpriced. It means you should not pay for a persistent low-latency session when a file upload will do.

This review uses OpenAI's July 28 changelog, model cards, transcription guides, pricing page, and data-control documentation. OpenAI says both models improve real-world transcription across accents, languages, short phrases, numbers, specialist terminology, and loud background noise. OpenAI has not published an independent benchmark set or fixed millisecond latency for these models, so those claims still need testing on your own audio.

## Pricing: $0.0045/min for files, $0.017/min for live audio

| Model | Official price | Cost per hour | Primary workflow | Main endpoint |
|---|---:|---:|---|---|
| `gpt-transcribe` | $0.0045/min | $0.27/hr | Completed files and committed turns | `/v1/audio/transcriptions` or Realtime transcription sessions |
| `gpt-live-transcribe` | $0.017/min | $1.02/hr | Microphones, calls, and live media | `/v1/realtime/transcription_sessions` |
| `gpt-4o-mini-transcribe` | $0.003/min estimated | $0.18/hr | Existing low-cost file integrations | `/v1/audio/transcriptions` |
| `gpt-4o-transcribe` | $0.006/min estimated | $0.36/hr | Existing high-accuracy file integrations | `/v1/audio/transcriptions` |
| `whisper-1` | $0.006/min | $0.36/hr | Timestamps, subtitles, and English translation | `/v1/audio/transcriptions` or `/v1/audio/translations` |

At 10,000 audio hours per month, the list-price bill is roughly **$2,700 for GPT Transcribe** or **$10,200 for GPT Live Transcribe**. The $7,500 difference pays for low-latency streaming rather than a documented fourfold accuracy gain. Route recorded audio to the file model unless users genuinely need words on screen during the conversation.

One terminology correction matters: OpenAI's announcement describes GPT Transcribe as suitable for asynchronous and batch workloads, but the model card marks the formal **Batch API (`/v1/batch`) as unsupported**. In practice, "batch workload" means queuing ordinary transcription uploads in your own worker system. Do not build a JSONL Batch API integration around this model.

OpenAI publishes no dedicated free allowance for the two new models. Limits vary by account and usage tier, so check the organization limits page before planning concurrency. Do not treat Whisper's documented free-tier rate limits as a free quota for GPT Transcribe.

## Free tier and account limits

There is no model-specific free credit or monthly audio allowance in the GPT Transcribe model cards or pricing table. A new account may have promotional credits, but that is an account condition, not a durable API feature.

Rate limits can be based on requests, tokens, or audio minutes and are set at the organization and project level. OpenAI exposes your actual limits in the dashboard and response headers. Production code should queue uploads, retry `429` responses with exponential backoff, and avoid assuming that another account's limits apply to yours.

The file endpoint accepts audio up to **25 MB** in `mp3`, `mp4`, `mpeg`, `mpga`, `m4a`, `wav`, or `webm`. For larger recordings, compress or split the file without cutting sentences in half. The live guide's basic example sends **24 kHz PCM** over a Realtime session.

## Speed and latency: controls, not a universal benchmark

GPT Live Transcribe emits transcript deltas as speech arrives, then a completed transcript when the application commits the turn. You can connect through WebSocket for a server-side audio pipeline or WebRTC for browser audio.

The model supports five delay presets:

| Delay | Use it for |
|---|---|
| `minimal` | The earliest partial text in highly interactive interfaces |
| `low` | Live captions and voice interfaces |
| `medium` | A balanced latency/accuracy starting point |
| `high` | Workflows that can wait for more context |
| `xhigh` | Maximum context when immediate display is not important |

Higher delay can improve word error rate because the model hears more context before emitting text. OpenAI explicitly says the exact milliseconds vary by configuration. Any article claiming a universal sub-300 ms figure for GPT Live Transcribe would be guessing.

GPT Transcribe can also stream partial text while processing a completed file by setting `stream=true`. That is **file streaming**, not live transcription. You upload a bounded recording first, and the server returns progress events while processing it. If the audio is coming from a microphone or phone call, use the live model.

## Capabilities that matter in production

Both models accept three kinds of context:

- `prompt`: free-form context about the recording or setting
- `keywords`: literal product names, medications, acronyms, or account codes that may be spoken
- `languages`: expected input languages, including ISO 639-1 codes, selected ISO 639-3 codes, and regional Chinese codes such as `zh-cn`, `zh-tw`, and `zh-hk`

This is more useful than a vague claim of "better context." A support team can pass the product name, plan names, and ticket format. A medical workflow can pass a constrained list of drugs relevant to the appointment. A bilingual call center can hint English and French, or Mandarin and Cantonese.

Keywords are hints, not commands. If you stuff the request with unrelated terms, you increase the chance of words appearing that nobody said. OpenAI also rejects keywords containing `<`, `>`, carriage returns, or line feeds.

GPT Transcribe returns detected languages when it can identify them reliably. GPT Live Transcribe does not return language predictions. In Realtime sessions, GPT Transcribe can use earlier completed turns as context, but it waits for a committed turn rather than optimizing for the earliest live delta.

## Limitations: keep Whisper and diarization in the toolbox

The new models do not replace every older audio endpoint.

- **No word-level timestamps on GPT Live Transcribe.** Use `whisper-1` when you need word or segment timestamps.
- **No speaker labels on the live model.** For a recorded meeting, use `gpt-4o-transcribe-diarize` with `diarized_json`.
- **No confidence scores on GPT Live Transcribe.** Build an application-level fallback for high-risk fields.
- **No direct English translation endpoint.** OpenAI still directs completed-audio translation to `whisper-1` and `/v1/audio/translations`.
- **No formal Batch API support.** Queue `/v1/audio/transcriptions` calls yourself.
- **25 MB upload ceiling.** Long recordings need compression or careful chunking.
- **No published third-party benchmark yet.** The launch claims come from OpenAI, not an independent multilingual WER evaluation.

For captions and editing, timestamps may matter more than a lower list price. For meetings, diarization may matter more than raw transcript quality. Model selection should start with the output fields your product requires, not the newest model name.

## Curl example: transcribe a recorded file

The simplest GPT Transcribe request uses the existing multipart transcription endpoint:

```bash
curl --request POST \
  --url https://api.openai.com/v1/audio/transcriptions \
  --header "Authorization: Bearer $OPENAI_API_KEY" \
  --header "Content-Type: multipart/form-data" \
  --form file=@meeting.mp3 \
  --form model=gpt-transcribe \
  --form 'prompt=A customer support call about the Acme Pro plan and account AC-42.' \
  --form 'keywords[]=Acme Pro' \
  --form 'keywords[]=AC-42' \
  --form 'languages[]=en' \
  --form 'languages[]=fr'
```

The response contains the transcript and any reliably detected languages:

```json
{
  "text": "Bonjour, pouvez-vous m'entendre?",
  "languages": [{ "code": "fr" }]
}
```

For a completed recording where you want partial results before the full transcript finishes, add `--form stream=true` and consume transcript delta events.

## Python example: context-aware file transcription

```python
from openai import OpenAI

client = OpenAI()

with open("meeting.wav", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="gpt-transcribe",
        file=audio_file,
        prompt="A bilingual support call about the Acme Pro plan.",
        extra_body={
            "keywords": ["Acme Pro", "AC-42", "billing"],
            "languages": ["en", "fr"],
        },
    )

print(transcript.text)
print(transcript.languages)
```

Pin and test your OpenAI SDK version before rollout. The `keywords` and `languages` fields are new enough that the Python example passes them through `extra_body` in OpenAI's current guide.

## Live transcription session outline

The live path uses a Realtime transcription session rather than the file endpoint. A minimal session update looks like this:

```json
{
  "type": "session.update",
  "session": {
    "type": "transcription",
    "audio": {
      "input": {
        "format": { "type": "audio/pcm", "rate": 24000 },
        "transcription": {
          "model": "gpt-live-transcribe",
          "keywords": ["Acme Pro", "AC-42"],
          "languages": ["en", "fr"],
          "delay": "low"
        },
        "turn_detection": null
      }
    }
  }
}
```

Append base64 audio chunks with `input_audio_buffer.append`. Commit manually with `input_audio_buffer.commit`, or configure voice activity detection to let the server find turn boundaries. Listen for `conversation.item.input_audio_transcription.delta` and `conversation.item.input_audio_transcription.completed`. Completion events from separate turns can arrive out of order, so reconcile them by `item_id`.

## Use cases: which model should you choose?

### Recorded meetings, podcasts, and uploaded interviews

Use GPT Transcribe. It is the lowest-cost OpenAI high-accuracy file option at $0.27 per hour, detects languages, accepts multiple language hints, and can stream processing results without a Realtime session.

### Live captions and call-center assist

Use GPT Live Transcribe. The persistent live connection and delay controls are what you are paying for. Keep the original audio or a post-call recording if you later need timestamps, diarization, or a corrected archival transcript.

### Subtitle production and video editing

Keep `whisper-1` in the pipeline when you need SRT, VTT, or word timestamps. A sensible workflow is GPT Transcribe for the readable transcript and Whisper for timestamp alignment, but test whether the added complexity is worth it.

If the transcript becomes a training, onboarding, or product video, **Synthesia** is the closest affiliate match in APIRank's current catalog. It turns a reviewed script into an avatar-led video in 160+ languages. The final publication should use APIRank's approved Synthesia tracking URL; until that URL is confirmed, the preview uses the official pricing page: [Try Synthesia](https://www.synthesia.io/pricing).

### Voice notes, search, and knowledge-base ingestion

Use GPT Transcribe, then index the final text in your search or RAG system. You do not need the live model just because the source recording contains speech.

## Data handling and privacy

OpenAI's data-controls table says `/v1/audio/transcriptions` data is not used for training, has no abuse-monitoring retention, has no application-state retention, and is eligible for Zero Data Retention. OpenAI also lists the audio transcription endpoint in its regional processing options.

That is unusually clear for a managed speech API, but live-session rules and organization-level controls still need a legal review for regulated deployments. Confirm the exact endpoint, region, account approval, and contract terms rather than extending the file-endpoint policy to every voice workflow by assumption.

## Verdict

**GPT Transcribe is the practical default.** At $0.0045 per minute, it undercuts `whisper-1` and `gpt-4o-transcribe`, adds multilingual context and language detection, and handles both ordinary uploads and streamed processing of completed files.

**GPT Live Transcribe is a specialist model.** Its $0.017 per minute price buys live deltas, a persistent Realtime workflow, and explicit latency tuning. That is worth paying for in captions, calls, and voice interfaces. It is wasteful for offline media queues.

The awkward part is feature fragmentation. Timestamps remain on Whisper, recorded speaker labels use a diarization model, English translation remains on Whisper's translation endpoint, and formal Batch API jobs do not support GPT Transcribe. OpenAI now has a strong default for file transcription and a clear default for live transcription, but production systems will still route among several audio models.

## Frequently asked questions

### How much does GPT Transcribe cost?

GPT Transcribe costs $0.0045 per audio minute, or $0.27 per hour at list price. GPT Live Transcribe costs $0.017 per minute, or $1.02 per hour.

### Does GPT Transcribe have a free tier?

OpenAI does not publish a dedicated free audio allowance for GPT Transcribe or GPT Live Transcribe. Promotional account credits may exist, but limits and billing depend on the account and usage tier.

### Can GPT Transcribe use OpenAI's Batch API?

No. The model card marks `/v1/batch` as unsupported. For large offline queues, run ordinary `/v1/audio/transcriptions` requests through your own job queue and respect account rate limits.

### What is the difference between file streaming and live transcription?

File streaming returns partial text while OpenAI processes an already completed upload. Live transcription consumes audio that is still arriving from a microphone, call, or stream through a Realtime session.

### Does GPT Live Transcribe support speaker diarization or word timestamps?

No. OpenAI says it does not return word-level timestamps, speaker labels, or confidence scores. Use `gpt-4o-transcribe-diarize` for recorded speaker labels and `whisper-1` for timestamps.

### Which languages are supported?

OpenAI accepts ISO 639-1 codes, selected ISO 639-3 codes, and regional Chinese codes such as `zh-cn`, `zh-tw`, and `zh-hk`. The documentation does not publish one exhaustive model-specific language count, so test every target language and accent.

## Sources

- [OpenAI API changelog, July 28, 2026](https://developers.openai.com/api/docs/changelog)
- [OpenAI transcription workflow guide](https://developers.openai.com/api/docs/guides/transcription)
- [OpenAI file transcription guide](https://developers.openai.com/api/docs/guides/speech-to-text)
- [OpenAI Realtime transcription guide](https://developers.openai.com/api/docs/guides/realtime-transcription)
- [GPT Transcribe model card](https://developers.openai.com/api/docs/models/gpt-transcribe)
- [GPT Live Transcribe model card](https://developers.openai.com/api/docs/models/gpt-live-transcribe)
- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing#transcription-and-speech)
- [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data)
- [OpenAI Developers launch post](https://x.com/OpenAIDevs/status/2082201169443905798)
