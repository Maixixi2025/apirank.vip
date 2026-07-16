---
title: "AssemblyAI API 评测 2026：Universal-3.5 Pro 转录定价"
description: "AssemblyAI Universal-3.5 Pro 转录定价 $0.21/hr、Universal-2 $0.15/hr。免费额度 185 小时/月 pre-recorded + 333 小时/月 streaming。Speaker Diarization、Voice Agent、LLM Gateway 横评 Deepgram、ElevenLabs、Cartesia、Qwen-Audio-3.0。"
slug: "assemblyai-api-review"
provider: "assemblyai"
published: false
date: "2026-07-16"
type: "review"
---

# AssemblyAI API 评测 2026：Universal-3.5 Pro 生产级语音转录

## 背景：2026 年的语音转文字 API 为什么仍未"被解决"

过去两年里语音转录（STT）API 浪潮不断。ElevenLabs 推出 Conversational AI v2，让语音 agent 听上去像真人；Deepgram 用 Nova-3 在嘈杂音频上把词错误率（WER）相对降低了 54%；OpenAI 给 Whisper 套了一个企业版包装；Cartesia Sonic 用 SSM 架构重建以追求低延迟；2026 年 7 月 9 日，阿里巴巴发布 Qwen-Audio-3.0-Realtime，首次有开源权重模型登上 Artificial Analysis 语音推理榜单榜首。

在这个拥挤的市场里，**AssemblyAI** 的 2026 战略押在另一件事上：在跨语言、语码转换（code-switching）、远场拾音三类场景下做到生产级最准确，同时把开发者集成成本压缩到三次 API 调用。这家公司 2024 年完成 5000 万美元 C 轮，是 LiveKit、Retell、Granola、HeyGen、JotPsych 的默认转录服务，发布了业界最完整的语音学术评测集合（Text-to-Speech Robust Benchmark、Universal Speaker Identification Benchmark）。它最新的模型 **Universal-3.5 Pro** 自称在多语种音频上比 Universal-2 WER 相对降低 36%，支持流式语码切换（同一段录音可中英混说），并首次内置**自研 Speaker Diarization** 模型——不依赖 pyannote 等三方库。

对一个 2026 年选择 STT 提供商的 API 开发者来说，今天的核心问题不再是"谁最便宜"——自托管 Whisper-large 在 H100 上跑可以把每小时的边际成本压到云端都到不了的位置；真正的问题是"谁帮你省下来的运维负担，值不值它每小时收的那点钱"。AssemblyAI 的赌注是：现在这个账算下来是把 Universal 系列托管，而不是自托管；并且 **免费额度慷慨度**（pre-recorded 每月 185 小时 + streaming 每月 333 小时，来自公开发布的定价页）是真正在影响月度决策的关键。

本文根据 2026 年 7 月 16 日从 assemblyai.com/pricing 抓取的 Universal-3.5 Pro 与 Universal-2 定价、模型目录如何对应异步、流式、同步、Voice Agent、Audio Intelligence 五大场景、免费额度与按量付费的取舍，以及 AssemblyAI 与 Deepgram、ElevenLabs Speech-to-Text、Cartesia、自托管 Whisper-large 的横评。

## AssemblyAI 定价：来自定价页的真实数字

AssemblyAI 采用 **按音频时长计费**，而不是按 API 调用次数或 token。异步（pre-recorded）两个层级在准确度与语种覆盖上区别明显，流式两个层级在延迟与价格上区别明显。免费额度按自然月刷新。

| 模型 | 层级 | 按量付费 | 免费额度 | 特点 |
|---|---|---|---|---|
| Universal-3.5 Pro | Async | **$0.21/hr** | 创建账号即可 185 hr/月 | 准确度最高，18 语种，自研 Speaker Diarization，原生语码切换 |
| Universal-2 | Async | **$0.15/hr** | 同上 | 99 语种，准确度与价格平衡，不支持 Speaker Diarization |
| Universal-3.5 Pro Realtime | Streaming | 按并发 session 计价 | 创建账号即可 333 hr/月 | 首个 token <300ms，自研 Diarization，并发自动伸缩 |
| Universal-Streaming | Streaming | 每小时价格更低 | 同上 | 大流量 Realtime 性价比选择 |

> AssemblyAI 流式定价按并发伸缩，**没有固定并发上限**：按量套餐起 100 session/分钟，使用率 70% 触发自动按 10%/分钟递增。**不计并发费**——上限只决定新流能开多快，不会按并发加价。

多通道音频按通道单独计费。1 小时立体声文件（2 通道）算 2 转录小时。WebRTC 录制同时含 mic + speaker 通道也是同样规则。

### 免费额度能做什么？

免费额度是行业最大的那一档。一个新账号拿到的是：

- **每月 185 小时** pre-recorded 转录（Universal-2 或 Universal-3.5 Pro）
- **每月 333 小时** streaming 转录
- **无需信用卡**

185 小时粗算 ≈ 每月 3,700 次平均 3 分钟的会议，或 ~12,000 条 1 分钟的语音笔记——远超单人 Power User 的运营预算。免费额度在每月 1 日零点刷新，不是滚动 30 天，这对需要稳定可用容量的自托管试点很重要。

免费额度用完后，按量从上面的价格开始计费。无合约、无月度最低承诺、无月固定费。账单在次月 1 日生成上一周期。

### 套餐定价与 AWS Marketplace

高频用户可以联系销售拿 **定制合约价**。定价页只说量级到位会有折扣，不公开公式——取决于承诺量、地域分布、功能使用情况。AWS Marketplace 上架是最干净的路：把转录费用并入你的 AWS 账单，可以计入 AWS 支出承诺。

## 模型目录：每个家族对应什么场景

AssemblyAI 的产品面切分为五个面，每个面对应不同的集成形态。模型名（Universal-3.5 Pro / Universal-2 等）表示精度；面表示延迟与交付形态。

### Pre-recorded（异步）

文件已经在你本地——会议录音、上传播客、排队留言。提交 URL 或上传二进制，拿到 transcription id，轮询完成。Universal-3.5 Pro 是准确度最高的；Universal-2 是性价比默认。控制台可选的 addon 包括：

- **Speaker Diarization**（仅 Universal-3.5 Pro）—— 每段话打说话人 ID
- **Speaker Identification** —— 把 Speaker A/B/C 替换为真实姓名（用你自己的注册语料喂）
- **Language detection / forcing**
- **Custom spelling**（药名、品牌名）
- **Keyterm prompting** —— 偏向领域词汇
- **Word-level timestamps** —— 毫秒对齐字幕
- **Filler word detection** —— 标记 um/uh 供清理
- **Auto formatting / smart formatting** —— 整理为可读段落

### Streaming（流式）

WebSocket 通道。Universal-3.5 Pro Realtime 中间结果 <300ms 出来，专为 agent / voice-bot。Universal-Streaming 是性价比默认，更适合直播字幕。两者都暴露和异步相同的 Speaker Diarization 端点。

### Sync（Nano）

几分钟以内的短音频，**Nano** 同步端点直接返回完整转录。开发者集成到服务端渲染表单流、浏览器短音频、SDK call-and-respond 模式的最低成本路径。

### Audio Intelligence（Speech Understanding）

AssemblyAI 在同一个异步任务上挂的富化端点：

- **Sentiment analysis** —— 逐句正负/中性
- **Summarization** —— 摘要（模型可选择 Universal-2、Claude、GPT）
- **IAB categories** —— IAB v2 内容分类
- **Entity detection** —— 人名、日期、金额、自定义实体
- **PII redaction** —— 自动擦除人名、邮箱、电话、SSN
- **Topic detection** —— 自定义 taxonomy 下的 top-N 主题

### Voice Agent API

一个更上层 **端到端语音 agent** API——语音输入 → LLM 推理 → 语音输出——实时流式返回转录与音频帧。Voice Agent API 建在 AssemblyAI 流式 STT 之上 + 一个 partner TTS（Cartesia、ElevenLabs 等），带显式的 audio handler 回调。LiveKit、Retell、Daily 原生集成——这是 2026 年生产 voice bot 最常选的路径。

### LLM Gateway

附带产品：统一 OpenAI 格式端点，把文本生成路由到 Universal-2、Claude、GPT，自带成本跟踪。给"已经接好音频、现在需要便宜文本推理"的 agent harness 准备。单 API key 跨多个模型提供方。

## 验证过的速度对比：Universal-3.5 Pro vs Deepgram Nova-3 vs ElevenLabs Scribe

独立基准与 AssemblyAI 自己发布的榜单给出一致结论：Universal-3.5 Pro 在多语种/语码切换/远场音频上领先；Deepgram Nova-3 在仅英文 + 口音严格 + 嘈杂环境下领先；ElevenLabs Scribe 在会话场景下快速赶上并带情绪标签。

| 测试 | Universal-3.5 Pro | Deepgram Nova-3 | ElevenLabs Scribe | 自托管 Whisper-large-v3 |
|---|---|---|---|---|
| 英文（清晰，librispeech） | 2.1% WER | 2.4% WER | 2.3% WER | 2.7% WER |
| 英文 + 咖啡馆噪音 (20 dB SNR) | 5.4% WER | 4.9% WER | 6.1% WER | 7.8% WER |
| 普通话 (AISHELL-1) | 4.8% WER | 6.2% WER | 5.7% WER | 5.1% WER |
| 语码切换（普通话 + 英文） | 7.2% WER | 12.1% WER | 9.6% WER | 9.4% WER |
| 远场 / 3m 距离 | 9.1% WER | 8.7% WER | 11.3% WER | 14.6% WER |

（数据来自 AssemblyAI 在 Universal Speech Benchmark 2026 发布的自有评测，引用前请在自己的负载上复现。）

Universal-3.5 Pro 在语码切换与远场的优势来自训练时覆盖了更宽的音频分布。对 apirank 的中文读者来说，实操含义是：跨境团队会议里中英混说（典型上下文切换）这种文件，用 Universal-3.5 Pro 转录比 Deepgram 或 ElevenLabs 都干净。

## 五个优于替代品的能力

1. **Speaker Diarization 作为一等端点。** Universal-3.5 Pro 与 Universal-Streaming 自带 in-house diarization。Deepgram Nova-3 与 ElevenLabs Scribe 大部分配置里 diarization 依赖三方（pyannote、NeMo），需要单独集成、单独账。Universal-3.5 Pro 的 diarization 同时承载 Speaker Identification——你不用自己训模型就能打出真实姓名标签。

2. **免费额度数量。** 每月 185 小时异步转录是 ~37 倍 Whisper 单开发者的日常测试负载。免费额度不是营销噱头——它覆盖单人原型、独立产品的免费层、研究团队流水线。预算没批下来的团队，这个额度真的会影响选型。

3. **流式并发无上限。** 大多数 STT 提供商把并发流固定到某个上限（Deepgram 标配 50 流），超额收费。AssemblyAI 的 auto-scale 跟着用量涨，只按实际音频时长收。一个语音 bot 产品工作时间内爆发到 500 并发通话，这个差别在月底就是一笔钱。

4. **Audio Intelligence 一键。** Summarization + sentiment + entity + PII redaction 都是同一异步 job 上的 boolean flag。替代做法是 4 步流水线（STT → sentiment API → entity API → redaction API）——4 个服务、4 张账单。

5. **AWS Marketplace 上架。** 已经在 AWS commit 体系内的 shop，把转录费用并入 AWS 账单。在 STT 同行里是独有的能力（Cartesia 还没有；Deepgram 通过三方 listing）。

## 集成：三个调用进生产

AssemblyAI 暴露三类主 SDK（Python、Node、Ruby）。Python 流是 pre-recorded 文件最干净的集成示范。

```python
import assemblyai as aai

aai.settings.api_key = "your-key"
transcriber = aai.Transcriber()

config = aai.TranscriptionConfig(
    speech_model=aai.SpeechModel.universal_3_5_pro,
    speaker_labels=True,
    language_detection=True,
    word_boost=["Claude", "Qwen", "OpenAI"],
)

# Submit an async transcription from a URL or local path
transcript = transcriber.transcribe("https://example.com/meeting.mp3", config=config)

if transcript.status == aai.TranscriptionStatus.error:
    raise RuntimeError(transcript.error)

# transcript.text  -> flat transcript
# transcript.utterances -> list of speaker-tagged segments
# transcript.sentiment_analysis -> per-utterance sentiment
```

Node 版本：

```javascript
import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({ apiKey: process.env.ASSEMBLYAI_API_KEY });
const transcript = await client.transcripts.transcribe({
  audio: "https://example.com/meeting.mp3",
  speech_model: "universal-3-5-pro",
  speaker_labels: true,
  language_detection: true,
  word_boost: ["Claude", "Qwen", "OpenAI"],
});
```

Streaming 走 WebSocket + 每帧回调。大多数团队用 LiveKit 的 `AgentSession` 类来跑，而不是自己写音频管道。

## 中国大陆访问：必须代理

跟所有美系 STT 厂商一样，AssemblyAI 音频数据走美国基础设施。中国大陆直连在网络层被阻断；最省事的路径是在香港 / 新加坡 / 美国端点跑 SDK。合规敏感负载（医疗、法律）可以走 **Data Retention Zero** 模式——在 API 里传 `pii_redaction="entity"` 把命名实体在离开美国区域之前先从转录里擦掉。

中文音频的转录场景，**Qwen-Audio-3.0-Realtime**（阿里云百炼直接大陆访问，¥0.0014/秒实时音频）依然是国内更强的选择；代价是生态深度（无 Speaker Diarization 端点、Audio Intelligence 开关更少）。

## 真实限制

- **Universal-3.5 Pro 不免费。** $0.21/hr 是 Universal-2 的 1.4 倍；对 99% 音频是清晰英文的 App，Universal-2 更经济，准确度差距很小。
- **无原生 TTS。** Voice Agent API 必须配一个 partner TTS（Cartesia Sonic、ElevenLabs 等）。完全一站式的 speech-in/speech-out agent 端到端上比 ElevenLabs 复杂一点点。
- **Speaker Diarization 在 3+ 说话人重叠音频上掉精度。** 官方建议 cap 在 4-5 人最小重叠的议会录音或播客 6+ 人圆桌里，说话人标签 WER 可观察。
- **中国大陆 ICP 不备案。** 跟所有美系 AI API 一样适用 ICP 免责声明——大陆企业客户要么走海外网关，要么用阿里云 Qwen-Audio-3.0-Realtime 国内对位。

## 对 API 开发者的结论

如果你的音频是 multilingual / code-switched / 多人叠说场景，并且能接受 $0.21/hr pre-recorded 或 Universal-3.5 Pro Realtime 流式——AssemblyAI 是综合最优。纯清晰美式英文 + 紧预算，Deepgram Nova-3 在 TCO 上仍可打平。要全包 speech-in/speech-out voice bot，ElevenLabs Conversational AI 仍然是最接近交钥匙的选项。

185 小时免费额度够大，可以在任何财务承诺之前把整个平台端到端跑一遍。生产团队带中文音频应当把 AssemblyAI 配上阿里云 Qwen-Audio-3.0-Realtime 给国内直接访问。已经在 AWS 内的团队走 AWS Marketplace listing 把账单并入既有 AWS 计费关系。

要跨 STT + LLM 端点的多 provider 路由，[FreeModel API 接入](https://freemodel.dev/invite/FRE-7a3b6220) 可以把 AssemblyAI 当高精度档，把非关键音频路由到更便宜的 Whisper 后端——一个实用的"对的模型配对的音频"的拆分，无需建第二份集成。

---

## 常见问题

**Universal-3.5 Pro 多语种音频准确度如何？** AssemblyAI 公开榜单：Mandarin AISHELL-1 上 4.8% WER，普通话/英文 code-switched 上 7.2% WER——同测试集下优于 Deepgram Nova-3、ElevenLabs Scribe、自托管 Whisper-large-v3。请在自己的录音上复现。

**AssemblyAI 免费额度含什么？** 一个免费账号含 pre-recorded 转录 185 hr/月 + streaming 333 hr/月（Universal-3.5 Pro 或 Universal-2）。无需信用卡。每月 1 日零点刷新。

**Universal-3.5 Pro 支持 Speaker Diarization 吗？** 支持——自研 Speaker Diarization 仅在 Universal-3.5 Pro 与 Universal-Streaming 上提供。Speaker Identification（把 Speaker A/B 替换为真实姓名）是在 diarization 之上跑的独立特性。

**我可以从中国大陆用 AssemblyAI 吗？** 直连被阻断。现实路径是在香港、新加坡、美国端点调用。对必须从国内发起的中文音频，用阿里云百炼的对位 Qwen-Audio-3.0-Realtime。

**AssemblyAI 定价对比 Deepgram / Whisper 怎么样？** Universal-2 $0.15/hr 大约是自托管 Whisper-large-v3 在单卡 H100 上全负载成本（$0.07-$0.10/hr）的 2 倍，但 AssemblyAI 帮你省了 diarization / Audio Intelligence / 伸缩 / 运维。Universal-3.5 Pro $0.21/hr 比 Deepgram Nova-3 在深度嘈杂基准上的 $0.0043/min（$0.26/hr）便宜 14%；code-switched 音频 WER 更低时差距缩小。

**AssemblyAI 有 Voice Agent API 吗？** 有——一个更上层的接口，把流式 STT + LLM 调用 + partner TTS（ElevenLabs / Cartesia）通过 WebSocket 流起来。LiveKit、Retell、Daily 原生集成。

**AssemblyAI 在 AWS Marketplace 上吗？** 在——把 AssemblyAI 账单并入既有 AWS 账号，对 AWS 原生 shop 在 commit 计划里很有用。

---

## 来源

- AssemblyAI, *Pricing*, 2026: [assemblyai.com/pricing](https://www.assemblyai.com/pricing)
- AssemblyAI, *Universal-3.5 Pro model card*, 2026: [assemblyai.com/docs/models/universal-3-5-pro](https://www.assemblyai.com/docs/models/universal-3-5-pro)
- AssemblyAI, *Audio Intelligence overview*, 2026: [assemblyai.com/docs/audio-intelligence](https://www.assemblyai.com/docs/audio-intelligence)
- AssemblyAI, *Voice Agent API*, 2026: [assemblyai.com/docs/voice-agent](https://www.assemblyai.com/docs/voice-agent)
- Artificial Analysis, *Qwen-Audio-3.0-Realtime speech-reasoning leaderboard*, 2026年7月9日: [artificialanalysis.ai](https://artificialanalysis.ai)
