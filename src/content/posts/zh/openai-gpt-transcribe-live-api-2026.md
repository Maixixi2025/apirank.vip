---
title: "OpenAI GPT Transcribe API 2026：实时与文件转录"
description: "OpenAI GPT Transcribe 文件转录 $0.0045/分钟，GPT Live Transcribe 实时转录 $0.017/分钟。对比端点、延迟档位、语言提示、限制与代码。"
pubDate: "2026-07-29"
provider: openai
category: news-analysis
featured: true
---

# OpenAI GPT Transcribe API 2026：GPT Live Transcribe 与 GPT Transcribe 怎么选

OpenAI 在 2026 年 7 月 28 日发布两款语音转文字模型，但它们并不是简单的“快版”和“慢版”。**GPT Transcribe** 面向已经录完的音频、已上传文件的流式处理，以及通过 WebSocket 提交完成的语音回合；**GPT Live Transcribe** 面向仍在持续输入的麦克风、电话或媒体流，用户说话时就返回增量文本。

两者价差明显。GPT Transcribe 是 **$0.0045/音频分钟**（$0.27/小时），GPT Live Transcribe 是 **$0.017/分钟**（$1.02/小时），后者约贵 3.8 倍。这并不等于实时模型定价不合理，而是提醒你：如果上传文件就能解决问题，不要为持续连接和低延迟增量输出多付钱。

本文基于 OpenAI 7 月 28 日 changelog、两张官方模型卡、转录指南、价格页与数据控制文档。OpenAI 称两款模型对口音、多语言、短语、数字、专业术语、强背景噪声等真实音频有更好的理解和准确率，但官方没有给出可独立复现的完整基准，也没有承诺固定毫秒延迟。生产选型仍要用自己的录音测试。

## 定价：文件 $0.0045/分钟，实时 $0.017/分钟

| 模型 | 官方价格 | 每小时成本 | 主要工作流 | 主端点 |
|---|---:|---:|---|---|
| `gpt-transcribe` | $0.0045/分钟 | $0.27/小时 | 已完成文件、已提交语音回合 | `/v1/audio/transcriptions` 或 Realtime 转录会话 |
| `gpt-live-transcribe` | $0.017/分钟 | $1.02/小时 | 麦克风、通话、实时媒体 | `/v1/realtime/transcription_sessions` |
| `gpt-4o-mini-transcribe` | 估算 $0.003/分钟 | $0.18/小时 | 已有的低成本文件集成 | `/v1/audio/transcriptions` |
| `gpt-4o-transcribe` | 估算 $0.006/分钟 | $0.36/小时 | 已有的高准确率文件集成 | `/v1/audio/transcriptions` |
| `whisper-1` | $0.006/分钟 | $0.36/小时 | 时间戳、字幕、翻译成英文 | `/v1/audio/transcriptions` 或 `/v1/audio/translations` |

如果每月处理 10,000 小时音频，按公开标价计算，GPT Transcribe 约 **$2,700**，GPT Live Transcribe 约 **$10,200**。多出的 $7,500 买的是实时增量输出，而不是官方公布的“四倍准确率”。除非用户确实需要在对话进行时看到文字，否则录音文件应默认走 GPT Transcribe。

有个术语陷阱必须讲清楚：OpenAI 的发布帖称 GPT Transcribe 适合异步和 batch workloads，但模型卡明确写着正式的 **Batch API（`/v1/batch`）不支持**。这里的“批量工作负载”是让你在自己的队列里批量调用普通转录端点，不是把 JSONL 交给 OpenAI Batch API。

OpenAI 没有为两款新模型公布独立免费额度。限制随账户和 usage tier 变化，上线前需要查看组织的 limits 页面。也不要把 Whisper 文档里的免费层速率限制误当成 GPT Transcribe 的免费配额。

## 免费额度与账户限制

GPT Transcribe 和 GPT Live Transcribe 的模型卡、定价表都没有写专属免费音频时长。新账户可能拿到促销 credit，但那是账户条件，不是可长期依赖的产品能力。

速率限制可能按请求数、token 或音频分钟计算，而且同时受组织和项目层控制。OpenAI 会在控制台和响应头里展示真实上限。生产服务需要排队、对 `429` 做指数退避，并避免照抄别人的账户限制。

文件端点最大接受 **25 MB**，格式包括 `mp3`、`mp4`、`mpeg`、`mpga`、`m4a`、`wav` 和 `webm`。更大的录音需要压缩或分块，切分时不要把句子从中间截断。实时指南的基础示例使用 **24 kHz PCM** 音频。

## 速度与延迟：有调节档位，没有统一基准

GPT Live Transcribe 在语音到达时发送 transcript delta，应用提交一个回合后再返回完整转录。服务端音频流水线可用 WebSocket，浏览器麦克风可用 WebRTC。

实时模型支持五档 delay：

| Delay | 建议场景 |
|---|---|
| `minimal` | 强交互界面里尽早显示 partial text |
| `low` | 实时字幕和语音界面 |
| `medium` | 延迟与准确率的平衡起点 |
| `high` | 可以等更多上下文的任务 |
| `xhigh` | 能接受最大等待、优先上下文完整度的流程 |

更高 delay 会让模型在输出前听到更多上下文，因此可能改善词错误率。OpenAI 明确说具体毫秒数会随模型配置变化，所以给 GPT Live Transcribe 宣称一个“固定低于 300 ms”的数字并不严谨。

GPT Transcribe 也能在处理已完成文件时流式返回部分文本，只需设置 `stream=true`。这叫**文件流式处理**，不是实时转录：完整录音已经上传，服务端边处理边返回事件。若音频来自正在进行的麦克风或电话，才应使用 live 模型。

## 对生产最有用的能力

两款模型都支持三种上下文：

- `prompt`：录音主题、场景等自由文本背景
- `keywords`：可能实际说出的产品名、药名、缩写或账户编码
- `languages`：预期输入语言，可用 ISO 639-1、部分 ISO 639-3，以及 `zh-cn`、`zh-tw`、`zh-hk` 等中文地区代码

这比一句模糊的“理解上下文更好”有用得多。客服系统可以传产品和套餐名、工单编号格式；医疗场景可传本次就诊相关的有限药物清单；双语呼叫中心可提示英语与法语，或普通话与粤语。

Keywords 是提示，不是强制输出。如果塞入大量无关词，会增加模型写出并未说过内容的风险。OpenAI 也会拒绝包含 `<`、`>`、回车或换行的关键词。

GPT Transcribe 能在有把握时返回检测到的语言；GPT Live Transcribe 不返回语言预测。在 Realtime 会话里，GPT Transcribe 可以利用前面已完成回合的上下文，但它要等语音回合被提交，不是为最早 live delta 优化的模型。

## 限制：Whisper 和 Diarization 仍然不能删

新模型没有覆盖所有旧音频端点。

- **GPT Live Transcribe 没有词级时间戳。** 需要 word 或 segment timestamp 时继续用 `whisper-1`。
- **实时模型没有说话人标签。** 已录制会议可用 `gpt-4o-transcribe-diarize` 和 `diarized_json`。
- **GPT Live Transcribe 没有置信度分数。** 高风险字段需要应用层回退。
- **没有直接翻译成英文的端点。** OpenAI 仍建议用 `whisper-1` 和 `/v1/audio/translations`。
- **不支持正式 Batch API。** 大批文件要自己排队调用 `/v1/audio/transcriptions`。
- **文件上限 25 MB。** 长录音需要压缩或谨慎分块。
- **暂无第三方完整基准。** 发布时的质量描述来自 OpenAI，不是独立多语 WER 测试。

做字幕和剪辑时，时间戳可能比低价更重要；做会议纪要时，diarization 可能比原始准确率更重要。先列清楚产品必须返回的字段，再选模型，不要只看谁更新。

## Curl 示例：转录录音文件

最简单的 GPT Transcribe 请求沿用 multipart 转录端点：

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

返回内容包含转录文本和模型有把握识别出的语言：

```json
{
  "text": "Bonjour, pouvez-vous m'entendre?",
  "languages": [{ "code": "fr" }]
}
```

若是已经录完的文件、但希望在完整结果之前收到部分文本，可增加 `--form stream=true` 并消费 transcript delta 事件。

## Python 示例：带上下文的文件转录

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

上线前固定并测试 OpenAI SDK 版本。`keywords` 和 `languages` 仍是较新的字段，OpenAI 当前 Python 指南通过 `extra_body` 传递它们。

## 实时转录会话轮廓

实时路径使用 Realtime transcription session，而不是文件端点。最小 session update 如下：

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

用 `input_audio_buffer.append` 追加 base64 音频块；可用 `input_audio_buffer.commit` 手动结束一回合，也可配置 VAD 让服务端判断边界。监听 `conversation.item.input_audio_transcription.delta` 与 `conversation.item.input_audio_transcription.completed`。不同回合的 completion 事件可能乱序，必须用 `item_id` 对齐。

## 使用场景：应该选哪一个？

### 会议录音、播客和上传访谈

选 GPT Transcribe。它按 $0.27/小时计算，是 OpenAI 当前最便宜的高准确率文件默认项，支持语言检测、多语言提示，也能在不建立 Realtime 会话的情况下流式返回处理进度。

### 实时字幕和呼叫中心辅助

选 GPT Live Transcribe。持续连接和 delay 调节就是你多付钱买到的能力。如果后续还需要时间戳、说话人标注或更正后的归档文本，应保留原音频或通话后录音，再跑一次文件模型。

### 字幕生产和视频剪辑

需要 SRT、VTT 或词级时间戳时继续保留 `whisper-1`。一种可行组合是用 GPT Transcribe 生成可读文本，再用 Whisper 做时间对齐，但要测试这层复杂度是否值得。

如果转录稿最后会被做成培训、入职或产品演示视频，APIRank 当前联盟库里最贴近这个场景的是 **Synthesia**。它可把审核后的脚本转成 160+ 语言的 AI avatar 视频。正式发布时应换成 APIRank 后台批准的 Synthesia tracking URL；在确认 URL 之前，预览稿仅放官方价格页：[试用 Synthesia](https://www.synthesia.io/pricing)。

### 语音笔记、搜索和知识库入库

选 GPT Transcribe，再把最终文本放入搜索或 RAG 系统。源数据是语音，不代表处理链路一定需要 live 模型。

## 数据处理与隐私

OpenAI 的 data controls 表显示，`/v1/audio/transcriptions` 数据不用于训练、无 abuse monitoring retention、无 application-state retention，并且支持 Zero Data Retention。OpenAI 也把音频转录端点列入 regional processing 支持范围。

这对托管语音 API 来说写得很明确，但实时会话和组织级控制仍要在受监管场景中单独做法务审查。应核对准确端点、区域、账户审批与合同条款，不要把文件转录端点政策直接推断到所有 voice workflow。

## 结论

**GPT Transcribe 是大多数项目的默认选择。** $0.0045/分钟低于 `whisper-1` 与 `gpt-4o-transcribe`，新增多语言上下文和语言检测，同时覆盖普通文件上传与已完成文件的流式处理。

**GPT Live Transcribe 是专业实时模型。** $0.017/分钟买到的是 live delta、持续 Realtime 工作流和显式延迟调节。实时字幕、电话与语音界面值得付这笔钱，离线媒体队列则没有必要。

目前的麻烦是功能仍然分散：时间戳留在 Whisper，录音说话人标签要用 diarization 模型，英文翻译仍走 Whisper translation endpoint，GPT Transcribe 也不能提交到正式 Batch API。OpenAI 已经给文件转录与实时转录各自确定了清晰默认项，但生产系统仍需要在多个音频模型之间路由。

## 常见问题

### GPT Transcribe 多少钱？

GPT Transcribe 是 $0.0045/音频分钟，即 $0.27/小时；GPT Live Transcribe 是 $0.017/分钟，即 $1.02/小时。

### GPT Transcribe 有免费额度吗？

OpenAI 没有公布 GPT Transcribe 或 GPT Live Transcribe 的专属免费音频额度。账户可能有促销 credit，但计费和限制取决于账户与 usage tier。

### GPT Transcribe 能用 OpenAI Batch API 吗？

不能。模型卡把 `/v1/batch` 标为 unsupported。大规模离线队列应在自己的任务系统里调用普通 `/v1/audio/transcriptions`，并遵守账户限制。

### 文件流式处理和实时转录有什么区别？

文件流式处理是在完整录音已经上传后，OpenAI 边处理边返回部分文本；实时转录是在麦克风、电话或媒体流仍持续输入时，通过 Realtime 会话消费音频。

### GPT Live Transcribe 支持说话人分离或词级时间戳吗？

不支持。OpenAI 明确写着它不返回词级时间戳、speaker label 或 confidence score。录音说话人标签用 `gpt-4o-transcribe-diarize`，时间戳用 `whisper-1`。

### 支持哪些语言？

OpenAI 接受 ISO 639-1、部分 ISO 639-3，以及 `zh-cn`、`zh-tw`、`zh-hk` 等地区代码。文档没有给一张完整的模型专属语言数量表，因此每个目标语言和口音都应单独测试。

## 来源

- [OpenAI API changelog（2026-07-28）](https://developers.openai.com/api/docs/changelog)
- [OpenAI 转录工作流指南](https://developers.openai.com/api/docs/guides/transcription)
- [OpenAI 文件转录指南](https://developers.openai.com/api/docs/guides/speech-to-text)
- [OpenAI Realtime 转录指南](https://developers.openai.com/api/docs/guides/realtime-transcription)
- [GPT Transcribe 模型卡](https://developers.openai.com/api/docs/models/gpt-transcribe)
- [GPT Live Transcribe 模型卡](https://developers.openai.com/api/docs/models/gpt-live-transcribe)
- [OpenAI API 定价](https://developers.openai.com/api/docs/pricing#transcription-and-speech)
- [OpenAI 数据控制说明](https://developers.openai.com/api/docs/guides/your-data)
- [OpenAI Developers 发布帖](https://x.com/OpenAIDevs/status/2082201169443905798)
