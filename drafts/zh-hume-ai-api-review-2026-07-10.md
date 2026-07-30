---
title: "Hume AI 2026 评测：EVI 3 情感语音接口与 OCTAVE TTS"
description: "Hume AI API 全面评测：EVI 3 情感对话、OCTAVE TTS 声音设计、Expression Measurement 情绪量化。定价对比 ElevenLabs / Cartesia / Deepgram / OpenAI Realtime。"
slug: "hume-ai-api-review"
provider: "hume-ai"
published: true
date: "2026-07-10"
type: "review"
---

# Hume AI 2026：情感语音接口与 OCTAVE TTS 生产级语音 agent 评测

## 什么是 Hume AI？2026 年它为何值得关注？

Hume AI 是一家位于纽约的 AI 研究公司，过去四年专注于构建 2026 年除大厂语音实验室外最成熟的情感语音栈。公司由前 Google DeepMind 研究科学家 Alan Cowen 于 2021 年创立，2024 年完成 5000 万美元 B 轮融资（Union Square Ventures、Nat Friedman、Daniel Gross 参投），截至 2026 年 7 月服务的客户包括 CallMiner（呼叫中心分析）、BetterHelp（治疗陪伴应用）以及越来越多在 LangChain、AutoGen、Vercel AI SDK 之上构建的消费者语音 agent 创业公司。核心承诺是：一个 LLM 无关的语音 API，不仅能转写和合成语音，还能实时测量并回应说话者的情感内容。

让 Hume 在 2026 年成为语音 agent 团队首选的三件事：

1. **EVI 3（情感语音接口）**，2026 年 4 月发布的第三代对话语音模型，是首个在 ASR 转写旁路返回"用户当前感受"量化向量的语音 API。模型每轮返回 48 维情绪向量，并支持会话中途切换语言（EVI 3 实时检测 12 种语言，无需重新初始化 WebSocket 会话）。
2. **OCTAVE TTS**（2025 年 10 月发布），业界首个文本提示词驱动的声音设计模型。无需上传 30 秒参考音频做声音克隆，只需写"温暖、中年女性、轻微英音、节奏沉稳"即可生成新声音。模型同时支持 11 种语言和 9 个预置声音。
3. **MCP server**（2026 年 1 月发布）将每个 Hume 端点作为工具调用暴露给 Claude、Cursor 和任何 MCP 兼容的 agent 框架。`hume-mcp` 包一条命令安装，统一路由语音合成、转写、情绪测量到同一个 agent 工具注册表。

权衡在于价格。Hume 的 EVI 3 约 $0.096/分钟双工音频，比纯 TTS 的 Cartesia Sonic-2 贵 3-5 倍；OCTAVE 声音设计 $0.048/1K 字符，比 ElevenLabs TTS-Multilingual v3 贵约 2 倍。溢价是情感层换来的：如果你的应用需要读懂并回应用户情绪，2026 年没有可替代的 API。纯 TTS 场景，Cartesia 或 ElevenLabs 更便宜。

## Hume API 接口：EVI、OCTAVE、Expression Measurement 与 Voice Design

Hume 提供四个不同的端点家族，每个端点 API 都不同。基础 URL 是 `https://api.hume.ai`，认证使用 `HUME_API_KEY` Bearer Token。

### 1. EVI 3（情感语音接口）

EVI 是 Hume 旗舰产品：一个全双工对话语音 agent，运行在 WebSocket 会话中。客户端按 16 kHz PCM 推流音频输入，EVI 推流 24 kHz PCM 音频输出，并返回转写、情绪和工具调用的结构化事件。会话模型：

```python
import asyncio
from hume import AsyncHumeClient

client = AsyncHumeClient(api_key="HUME_API_KEY")

async with client.empathic_voice.connect() as socket:
    await socket.update_config(
        voice_id="ito",            # 预置声音
        language="en",             # 12 种语言自动检测回退
        emotion_model="evi-3",     # 情感层开启
        system_prompt="你是瑜伽工作室的友好、耐心支持顾问。"
    )

    # 推送音频分块（从麦克风）
    # ... (此处省略)

    # 接收事件
    async for event in socket:
        if event.type == "audio_output":
            play(event.audio)  # 24 kHz PCM
        elif event.type == "user_message":
            print(f"用户说: {event.message.text}")
            print(f"情绪: {event.message.emotion}")  # 48 维向量
```

`event.message.emotion` 字段是关键差异化点。每个用户轮次返回 48 维情绪强度向量（如 `Joy: 0.62, Sadness: 0.04, Anger: 0.02, Confusion: 0.31`）。应用可以基于该向量路由：例如 `if event.message.emotion.Joy > 0.7: trigger_celebration_sound()`。48 维对应 Hume 公开的 `Expression Measurement` 分类法（见第 3 节）。

EVI 3 还新增了**会话中途语言切换**能力，老版 EVI 2 没有。模型实时检测 12 种语言，无需重启 WebSocket 即可切换输出语言。用户可以先用英语，中途切到西班牙语，EVI 3 无需重新初始化即跟随。这是 2026 年唯一具备此能力的语音 API；Cartesia 和 ElevenLabs 语言切换需要新会话。

### 2. OCTAVE TTS

OCTAVE 是 Hume 的 TTS 模型。两种风格：

**声音设计（文本提示词定制声音）：**

```python
from hume import HumeClient

client = HumeClient(api_key="HUME_API_KEY")

response = client.tts.synthesize(
    text="欢迎来到你的冥想课。找一个舒适的座位，让双肩放松。",
    voice_description="温暖、中年女性、轻微英音、节奏沉稳。",
    language="zh",
    output_format="mp3"
)
with open("welcome.mp3", "wb") as f:
    f.write(response.audio)
```

OCTAVE 的声音描述是自由英文文本，不是受约束的 schema。模型解释"温暖、沙哑、兴奋、平淡"等形容词，产出匹配的声音。同一描述运行两次返回相似但不完全相同的声音，因此模型是随机的。如需确定性声音，可保存首次合成的 `voice_id` 后用 `voice_id="abc123"` 复用。

**声音克隆（参考音频上传）：**

```python
response = client.tts.clone_and_synthesize(
    text="This is a cloned voice.",
    reference_audio_path="voice_sample.wav",  # 30+ 秒干净音频
    reference_transcript="This is the transcript of the reference audio.",
    language="en"
)
```

克隆至少需要 30 秒干净参考音频加逐字转写。质量与 ElevenLabs Instant Voice Cloning 相当，但同时返回情绪向量（Hume 的 Expression Measurement 也可对克隆声音启用）。

OCTAVE 定价 **$0.048/1K 输入字符**。1 分钟配音 ~150 词/分钟 = ~750 字符 = $0.036。ElevenLabs TTS-Multilingual v3 是 $0.018/1K 字符（Creator 套餐），纯 TTS（不需声音设计）约便宜 2.6 倍。

### 3. Expression Measurement（批量情绪分析）

Expression Measurement 是独立情绪 API：传入音频、视频或图片文件，按时间戳返回 48 维情绪向量。端点是 REST，不是 WebSocket：

```python
response = client.expression.measure.batch(
    files=["call_recording.wav"],
    models=["face", "prosody", "language"],  # 多模态
    granularity="utterance"  # 或 "word" / "consecutive-5-second"
)
```

48 种情绪定义在 Hume 公开的 `Expression Taxonomy v3`（MIT 协议）。生产中最常用：`Joy、Sadness、Anger、Fear、Surprise、Disgust、Confusion、Concentration、Awkwardness、Boredom、Excitement、Interest`。分类法与 Plutchik 情绪轮类似，但基于数据驱动，源自 Hume 的 1000 万+ 标注人类情绪训练语料。

典型用例：通话后分析。呼叫中心录制客服通话，对音频跑 Expression Measurement，按 utterance 返回情绪分数。仪表盘标记客户 `Anger` 超过 0.7 持续 30 秒以上的通话（SLA 违规信号），或客服 `Awkwardness` 高的片段（辅导机会）。商业竞品 CallMiner、Gong、Chorus.ai 每个席位 $1,000+/月。Hume API 是 $0.0008/秒音频，约 $0.05/分钟。10 万通通话/月呼叫中心，Hume 约 $5,000/月 vs CallMiner $120,000+/月。

### 4. Voice Design（预置声音）

想要高质量 TTS 又不写声音描述的团队，Hume 提供 9 个预置声音（`ito, kora, ronan, dave, ...`）和 11 种语言预置（英、西、法、德、意、葡、中、日、韩、印地、阿）。预置声音针对生产用例调优（`kora` 是温暖女声，有声书朗读优化；`ronan` 是低沉男声，冥想 App 优化）。预置价格与定制声音设计相同：$0.048/1K 字符。

## Hume 定价实战：按功能拆分

Hume 按功能定价，不按模型，费率不全列在一处。2026 年 7 月完整价格：

| 端点 | 单位 | 价格 | 备注 |
|---|---|---|---|
| EVI 3（全双工语音） | 每分钟音频 | $0.096 | 按秒计费，~$5.76/小时对话 |
| EVI 3（关闭情感层） | 每分钟 | $0.072 | 仅 ASR + TTS 便宜 25% |
| OCTAVE TTS（定制声音） | 每 1K 字符 | $0.048 | 文本提示词设计 + 参考克隆 |
| OCTAVE TTS（预置声音） | 每 1K 字符 | $0.048 | 同价，预置无单独许可 |
| Expression Measurement（音频） | 每秒 | $0.0008 | ~$0.048/分钟 |
| Expression Measurement（视频） | 每秒 | $0.0012 | 视频帧略高 |
| Expression Measurement（图片） | 每张 | $0.0004 | 单帧人脸分析 |
| 声音克隆设置 | 每个声音一次性 | 免费 | 上传 30s+ 参考音频 + 转写 |

免费层：Hume 注册即送免费 credits（数额变化，通常等值 $5-10）。可试用 EVI 3 对话 50-100 分钟，或对 10,000 分钟音频跑 Expression Measurement。免费 credits 不需信用卡，超出免费层后需要添加卡片。

批量折扣：Hume 不公开列出批量阶梯，月花费 >$5K 的账户通常获 15-20% 定制费率。联系 Hume 销售团队（`sales@hume.ai`）获取报价。

## Hume 与 ElevenLabs、Cartesia、Deepgram、OpenAI Realtime 的对比

2026 年语音 API 市场有五家主要玩家，每家角度不同。选择取决于你需要情感层、语言覆盖、价格还是实时开箱即用集成。

| 提供商 | 优势 | 劣势 | TTS 价格（每 1K 字符） | 实时对话 | 情感层 | MCP server |
|---|---|---|---|---|---|---|
| **Hume AI** | 情感语音（48 维情绪）、EVI 3 会话中语言切换、OCTAVE 文本提示词声音设计 | TTS 价格较高（2-3 倍 ElevenLabs）、WebSocket 协议集成成本 | $0.048 | 是（EVI 3，WebSocket） | 是（48 维情绪向量） | 是（2026 年 1 月） |
| **ElevenLabs** | 业界最佳 TTS 质量、70+ 种语言、大型声音库（3,000+ 社区声音） | 无情感层、声音克隆伦理争议、无实时对话 | $0.018（TTS-Multilingual v3） | 是（Conversational AI，2025） | 否 | 有限（无官方 MCP） |
| **Cartesia** | 最快实时 TTS（Sonic-2，90ms TTFB）、Pythonic API、MCP 集成 | 无情感层、声音库较小（~50 声音）、英文优先 | $0.022（Sonic-2） | 是（Sonic-2 + Ink，2025） | 否 | 是（2025 年 8 月） |
| **Deepgram** | STT（转写）性价比最优、Aura TTS 适合纯 TTS 用例 | TTS 质量低于 ElevenLabs/Hume、无情感层、无实时对话 | $0.015（Aura-2） | 否（Aura 仅 HTTP） | 否 | 否 |
| **OpenAI Realtime** | 开箱即用实时对话（gpt-4o-realtime），OpenAI SDK 一部分 | 无情感层、定价较高（~$0.06/分钟输入 + $0.24/分钟输出）、尚无 MCP | $0.060（gpt-4o-realtime，按分钟） | 是（原生，WebRTC） | 否 | 否 |

**做面向客户的情感语音 agent（治疗、客服、辅导、陪伴）：** Hume 胜。48 维情绪向量是 2026 年唯一实时返回用户情绪量化度量的 API，EVI 3 会话中语言切换对全球呼叫中心独有价值。

**做最佳 TTS 质量 + 最低价格：** ElevenLabs 胜。声音质量业界领先，声音库大，价格比 Hume 便宜 2.6 倍。放弃情感层，但有声书朗读、视频配音、播客制作 ElevenLabs 是首选。

**做最低延迟实时 TTS 语音 agent：** Cartesia Sonic-2 胜。TTFB 90ms，约是 ElevenLabs 典型 300-400ms 的 1/3。权衡是声音库较小、无情感层。每个 100ms 延迟都重要的交互式语音 agent（如 1 秒总预算的实时客服），Cartesia 是首选。

**做最便宜的 STT（转写）大规模生产：** Deepgram 胜。Nova-2 是英、西语 ASR 性价比领先者。Deepgram TTS（Aura-2）合格但不顶尖，所以多数团队用 Deepgram STT 配 ElevenLabs 或 Cartesia TTS 搭生产栈。

**做最开箱即用 OpenAI 集成：** OpenAI Realtime（gpt-4o-realtime）胜。SDK 与 OpenAI 生态一致，模型单次 API 调用，无需管理单独语音提供商。价格最高（~$0.06/分钟输入 + $0.24/分钟输出），无情感层或 MCP server，但全 OpenAI 团队集成成本为零。

## Hume MCP server：2026 年 agent 集成

Hume 在 2026 年 1 月发布官方 MCP server。服务器将每个 Hume 端点作为工具调用暴露给 Claude、Cursor、Cline 和任何 MCP 兼容 agent 框架。安装一条命令：

```bash
npx -y @hume/mcp-server --api-key $HUME_API_KEY
```

`mcp.json` 配置：

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

配置完成后，agent 可以调用：

- `hume_evi_start_session`：用声音 + 系统提示词开全双工 EVI 3 会话
- `hume_evi_end_session`：关闭会话
- `hume_octave_synthesize`：用定制或预置声音把文本转音频
- `hume_octave_describe_voice`：用文本描述生成新声音
- `hume_expression_measure`：对音频/视频/图片文件跑情绪分析

MCP server 是需要说话（合成）、听并回应（EVI）、读用户情绪（Expression Measurement）的 agent 的阻力最小路径。同一 `HUME_API_KEY` 用于所有端点；无需单独订阅。

MCP server 对所有 Hume API 用户免费。它也是少数支持流式工具调用的语音 API MCP 实现之一，是长时语音合成或 EVI 会话的正确模式。

## Hume 有 OpenAI 兼容 API 吗？

没有。Hume API 是 REST + WebSocket，不是 OpenAI 兼容。没有可直接替换 OpenAI `/v1/audio/speech` 或 `/v1/realtime` 端点的接口。如果从 OpenAI Realtime 迁移到 Hume EVI 3，需要重写客户端使用 Hume WebSocket 协议。权衡是情感层：OpenAI Realtime API 不返回 48 维情绪向量，所以如果你构建需要读用户情绪的语音 agent，重写在所难免。

想要 OpenAI 兼容 + Hume 情感层的团队，方案是 Hume 做语音层 + LLM（Claude、GPT-4o）做推理。典型架构：

1. 用户说话 → Hume EVI 3 转写并返回情绪向量
2. 应用把转写 + 情绪发给 LLM，带系统提示词 + 工具定义
3. LLM 生成文本回复，可选包含 `humor: "warm, gentle"` 或 `emotion: "apologetic"` 指令
4. 应用把 LLM 回复发给 Hume OCTAVE，按要求声音风格合成
5. Hume 流式推回音频给用户

这是大多数 Hume 生产部署的架构。WebSocket 是语音层的正确协议，LLM 是推理层的正确协议。两者解耦，应用串接。

## Hume 数据保留策略？

Hume 保留 EVI 会话、OCTAVE 音频、Expression Measurement 输入/输出 30 天，用于滥用监控和调试。企业客户可配置保留期（多数生产团队设为 0 天，日志走自己的可观测栈）。多数生产工作负载 30 天保留可接受。处理 HIPAA、PHI 或其他合规数据的工作负载，企业套餐可完全关闭 Hume 日志，所有日志路由到私有 S3 桶。

Hume 通过 SOC 2 Type II 认证（2026 年 3 月验证），GDPR 合规有公开 DPA。默认 MCP server 数据**不**包含音频内容；只为计费和滥用监控记录工具调用元数据。

## 能自托管 Hume 模型吗？

不能。Hume 模型（EVI 3、OCTAVE、Expression Measurement）不开源权重，不提供自托管。API 是唯一访问路径。自托管情感语音最接近的方案是组合：

- **Whisper**（开源 STT）做转写
- **Llama 3.3 70B** 或 **Claude** 做推理
- **CosyVoice** 或 **ChatTTS**（开源 TTS）做合成
- **自训练情绪分类器**，基于 Hume 公开的 Expression Taxonomy v3（分类法是 MIT 协议，但训练权重不是）

结果约为 Hume 80% 质量、成本 40%，但工程开销巨大（团队需集成 4 个模型、管理 WebSocket 协议、维护情绪分类器）。需要情感层但不愿维护多模型栈的团队，Hume API 是首选。

## 最终结论

Hume AI 在 2026 年是**需要情感层的语音 API** —— 实时返回用户情绪的量化度量，伴随转写，可用于驱动 agent 行为、呼叫分析或内容审核。EVI 3 会话中语言切换是 2026 年唯一支持此能力的语音 API；Cartesia 和 ElevenLabs 语言切换需要新会话。OCTAVE 声音设计是 2026 年唯一无需参考音频即可从自然语言描述生成新声音的 TTS 模型。MCP server 是最被低估的功能 —— 需要说话、听或读用户情绪的 agent 都应通过 Hume MCP 路由。

权衡是真实的：TTS 价格较高（2-3 倍 ElevenLabs）、WebSocket 协议集成成本（vs OpenAI Realtime WebRTC 开箱即用）、无自托管选项。**构建不需要情感层的语音 agent**（有声书、播客制作、视频配音），ElevenLabs 首选。**构建需要情感层且愿意付溢价的团队**，Hume 首选。

如果 2026 年你正在构建语音 agent 且未试过 EVI 3，注册免费 credits 足够跑 30 分钟情感对话，对照你的用例基准测试 48 维情绪向量。这就是正确的起点。

## FAQ

**Hume AI 用来做什么？**

Hume 用于情感语音 agent —— 需要实时读懂并回应用户情绪的语音应用。典型用例：检测呼叫者挫败感的客服 agent、适应用户情绪的治疗和辅导 App、标记高愤怒通话的呼叫中心分析、按用户偏好调整 TTS 韵律的无障碍工具、需要比纯 TTS 更自然对话风格的消费者语音 agent（陪伴、语言导师、销售机器人）。

**Hume AI 多少钱？**

Hume 按端点计费，不按模型。EVI 3 全双工语音 $0.096/分钟。OCTAVE TTS $0.048/1K 字符。Expression Measurement 音频 $0.0008/秒。无订阅费、无最低承诺、无每席位许可。注册免费 credits（$5-10 等值）足够试用 EVI 3 对话 50-100 分钟。

**Hume AI 有免费套餐吗？**

有。Hume 注册即送免费 credits（数额变化，通常 $5-10 等值）。免费 credits 足够试用 EVI 3 对话 50-100 分钟、对 ~10,000 分钟音频跑 Expression Measurement、或生成 ~150,000 字符 OCTAVE TTS。免费 credits 不需信用卡。

**可以从中国使用 Hume AI 吗？**

Hume API 托管在 AWS US-East 和 GCP US-Central。从中国访问需要稳定代理连接。从上海到 WebSocket 端点延迟通常 200-400ms，对 EVI 会话可接受（EVI 客户端本来就缓冲 200-300ms 音频帧）。服务中国用户生产部署推荐路径：在阿里云百炼或腾讯云部署区域代理，转发到 Hume API。

**Hume 支持会话中语言切换吗？**

支持。EVI 3（2026 年 4 月发布）是 2026 年唯一实时检测用户语言切换、无需重新初始化 WebSocket 即可切换输出语言的语音 API。模型支持 12 种语言（英、西、法、德、意、葡、中、日、韩、印地、阿、俄）。Cartesia 和 ElevenLabs 语言切换需要新会话；Hume EVI 3 跟随用户。

**Hume 与 ElevenLabs 相比如何？**

ElevenLabs 拥有 2026 年最佳 TTS 声音质量和 3,000+ 声音库，但无情感层（不返回情绪向量）、无实时对话开箱即用。Hume EVI 3 有情感层、实时对话、较小的声音库（~50 声音含预置和 OCTAVE 设计）。纯 TTS，ElevenLabs 更便宜（$0.018 vs $0.048/1K 字符）且质量更高。情感语音 agent，Hume 是 2026 年唯一选项。

**Hume 与 Cartesia 相比如何？**

Cartesia Sonic-2 拥有最快实时 TTS（90ms TTFB）和实时 TTS API 最低价格，但无情感层。Hume EVI 3 较慢（200-300ms TTFB）且较贵，但增加 48 维情绪向量。无需情感层的低延迟语音 agent，Cartesia 胜。需要情感层的语音 agent，Hume 胜。

**Hume 与 OpenAI Realtime 相比如何？**

OpenAI Realtime（gpt-4o-realtime）是 2026 年最开箱即用的实时对话 API，支持 WebRTC，对已用 OpenAI 的团队零集成成本。价格是对比中最高（$0.06/分钟输入 + $0.24/分钟输出 = 平衡对话约 $0.30/分钟）。无情感层（不返回情绪向量）、无 MCP server。Hume EVI 3 语音层更便宜（$0.096/分钟总）且增加情感层，但集成成本更高（WebSocket vs WebRTC）。无需情感、已全栈 OpenAI 的团队，OpenAI Realtime 胜。需要情感层，Hume 胜。

**Hume MCP server 是什么？**

Hume MCP server（2026 年 1 月发布）将每个 Hume 端点作为工具调用暴露给 Claude、Cursor、Cline 和任何 MCP 兼容 agent 框架。安装一条 `npx` 命令。配置完成后，agent 可通过同一 agent 工具注册表调用 EVI 会话、OCTAVE 合成、声音设计、Expression Measurement。MCP server 对所有 Hume API 用户免费。

**Hume 有联盟营销计划吗？**

Hume 当前没有公开联盟营销计划。需要联盟风格 CTA 的站点，替代方案是推荐 FreeModel —— 一个 OpenAI 兼容聚合器，提供跨多 provider 统一 API key 并为自部署模型增加成本路由优化。

**能用 Hume 对大型音频档案跑批量情绪分析吗？**

可以。Expression Measurement 是 REST 端点，接收音频、视频或图片文件，按时间戳返回 48 维情绪向量。音频定价 $0.0008/秒（~$0.048/分钟）。100 万分钟音频档案成本约 $48K。默认端点限速每账户 100 并发；企业客户可申请更高限额。典型批量工作流：上传音频到 S3，把 S3 keys 发给 Expression Measurement，把按时间戳的情绪向量存到 Postgres JSONB 列，查询 `Anger > 0.7` 片段，在仪表盘里显示这些片段。
