---
title: "Claude Project Fetch 2026: 20x Faster API Tasks"
description: "Claude Opus 4.7 autonomously writes code, tests hardware, and completes tasks 19-38x faster than humans. Full API integration guide with Claude Code."
slug: "claude-project-fetch-2026"
provider: "anthropic"
published: false
date: "2026-06-23"
type: "review"
---

# Claude Opus 4.7 Project Fetch: Autonomous API Tasks 20x Faster

## TL;DR

Anthropic's Project Fetch Phase Two (published June 18, 2026) shows Claude Opus 4.7 autonomously completing hardware software engineering tasks **19-38x faster** than human teams — in 9 minutes 35 seconds vs 181 minutes for a team using Claude, and vs 361 minutes without Claude. The model wrote code, connected to cameras and lidar sensors, and iterated autonomously with only minimal human prompt. For API developers, this means Claude Code + Opus 4.7 now delivers production-ready autonomous task execution. Anthropic has affiliateAvailable=false, so for multi-provider routing or budget-conscious alternatives, an aggregator like FreeModel provides OpenAI-compatible access to multiple models.

## What Is Project Fetch Phase Two?

On June 18, 2026, Anthropic's Frontier Red Team (Michael Ilie, C. Daniel Freeman, Kevin K. Troy) published Project Fetch Phase Two — a repeat of an August 2025 experiment where teams used Claude to control a robotic quadruped ("robodog"). The twist: this time, Claude Opus 4.7 ran **completely autonomously** via Claude Code.

The human researcher's role was minimal: plug in the laptop, enter the initial prompt, approve commands, and approve transitions between tasks. Everything else — code writing, hardware connection, sensor integration, iteration — was handled by Claude.

The headline result: **9 minutes 35 seconds** for 4 tasks that took the fastest human team 181 minutes. That's an 18.9x speedup over humans-with-Claude, and **37.7x faster** than humans without Claude.

## Benchmark Results: The Numbers

| Metric | Claude Opus 4.7 | Team Claude (human+AI) | Team Claude-less (human only) |
|--------|:----------------:|:----------------------:|:----------------------------:|
| 4 comparable tasks | **9 min 35 sec** | 181 min | 361 min |
| vs Team Claude-less | **37.7x faster** | — | 1x |
| vs Team Claude | **18.9x faster** | 1x | — |
| All 5 tasks (avg 3 trials) | **12 min 7 sec** | 264 min | — |
| Code written | **1,045 lines** | 10,309 lines | 1,136 lines |

The model was "as or more successful than both human teams while producing almost ten times less code than Team Claude" — meaning its solutions were both faster AND more efficient.

### Tasks Completed

Claude autonomously completed the full pipeline:
1. **Connect to video camera** — detected and integrated a USB camera
2. **Connect to lidar** — interfaced with LIDAR-Lite v4 LED sensor via I2C
3. **Write manual control program** — keyboard-controlled robodog movement
4. **Develop path monitoring** — real-time obstacle tracking via lidar
5. **Write beach ball detection** — OpenCV-based red detection (ball movement was the one task Claude struggled with physically)

## What This Means for API Developers

Claude Code (Anthropic's terminal-based agent CLI) is the interface for autonomous task execution. Any developer can:

1. **Install Claude Code** via `npm install -g @anthropic-ai/claude-code`
2. **Launch autonomous mode** with Claude Opus 4.7 using adaptive thinking at max effort
3. **Describe the task** in natural language — Claude handles code writing, testing, and iteration
4. **Approve critical transitions** — human stays in the loop for key decisions

```python
# Claude Code with Opus 4.7 enables this kind of autonomous pipeline
# Import anthropic SDK
import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

# The model can handle multi-step tasks autonomously
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    messages=[
        {"role": "user", "content": "Write a Python program that connects to a USB camera, captures frames at 30fps, and detects red objects using OpenCV. Include a manual control interface using keyboard arrows."}
    ]
)

# Claude writes the full working program in one response
print(response.content[0].text)
```

```bash
# Claude Code CLI (terminal-based) for autonomous tasks
# npx @anthropic-ai/claude-code --model claude-opus-4-7

# In the CLI, just describe the goal:
# "Connect to the USB camera at /dev/video0, capture frames,
#  detect red objects, and show a real-time tracking window."
```

### Pricing Context

Claude Opus 4.7 maintains the same pricing as Opus 4.6 and 4.8:

| Model | Input (/1M tokens) | Output (/1M tokens) | Context |
|-------|:------------------:|:-------------------:|:-------:|
| Claude Opus 4.7 | $5.00 | $25.00 | 1M tokens |
| Claude Opus 4.6 | $5.00 | $25.00 | 1M tokens |
| Claude Opus 4.8 (latest) | $5.00 | $25.00 | 1M tokens |
| GPT-5.5 | $15.00 | $60.00 | 256K tokens |

**Important note:** Opus 4.7 introduced a new tokenizer that produces ~30% more tokens for the same text compared to pre-4.7 models. This means your token cost for a given task may be ~30% higher even at the same per-token price. When migrating from Opus 4.1 ($15/$75), the effective cost is roughly 3x cheaper for the same output after accounting for the tokenizer change.

## Why This Matters: The "Early Era of Physical Agentic AI"

> "We are plausibly entering the early era of physical agentic AI."
> — Anthropic Frontier Red Team

The key insight: this wasn't a software-only benchmark. Claude controlled **real hardware** — a physical robot with cameras, lidar sensors, and motors. Most autonomous coding evaluations (SWE-bench, HumanEval, etc.) test pure software tasks. Project Fetch Phase Two demonstrates that Claude Opus 4.7 can bridge the gap between code generation and physical-world interaction.

For API developers, the implications are significant:

- **Autonomous debugging**: Claude can connect to hardware, read sensor data, identify issues, and fix code autonomously
- **End-to-end build**: From "write this program" to "make it work with this physical device" in one session
- **Reduced human overhead**: What required 3-6 highly skilled engineers working 6 hours can now be done by one developer with Claude Code in 10-30 minutes

## Limitations

- **Physical precision**: Claude struggled with fine motor control (the actual "fetching" — getting the robodog to physically move a beach ball)
- **Tokenizer change**: The 30% token increase vs pre-4.7 models means cost calculations need updating
- **Opus 4.7 is now previous-gen**: As of May 28, Opus 4.8 is the latest, and Fable 5 (June 9) is Anthropic's current frontier model
- **Export control suspension**: Anthropic models face US export control restrictions affecting international access

## Comparison with Autonomous Coding Tools

Project Fetch Phase Two tests a scenario that no other coding tool has benchmarked: **hardware-in-the-loop autonomous development**. While Devin and Codex focus on software repositories and CI/CD pipelines, Claude Opus 4.7 demonstrates end-to-end hardware interaction — writing code that connects to physical sensors, processes real-world data, and controls motors.

| Capability | Claude Opus 4.7 | Devin | OpenAI Codex |
|------------|:---------------:|:-----:|:------------:|
| Software coding | ✅ | ✅ | ✅ |
| Hardware interaction | ✅ | ❌ | ❌ |
| Autonomous iteration | ✅ | ✅ | ✅ |
| Self-testing | ✅ | ✅ | Partial |
| Real-time sensor data | ✅ | ❌ | ❌ |

## FAQ

**Q: Is Project Fetch Phase Two available through the regular Claude API?**
A: Yes. The autonomous capability is available through Claude Code CLI (terminal-based agent) using Claude Opus 4.7 or newer models. The API interface itself is unchanged — the autonomy comes from the agent architecture in Claude Code.

**Q: What's the difference between Opus 4.7, 4.8, and Fable 5?**
A: Opus 4.7 (April 16) introduced the new tokenizer and autonomous capabilities. Opus 4.8 (May 28) is a minor update maintaining the same pricing. Fable 5 (June 9) is Anthropic's current frontier model at $10/$50 per MTok. The Project Fetch benchmark used Opus 4.7, but the capabilities carry forward to newer models.

**Q: Can I use this from China?**
A: Anthropic requires US-based accounts and there are currently export control restrictions. For teams needing direct China access with multi-provider routing, aggregators like FreeModel provide OpenAI-compatible endpoints that bundle multiple model providers.

**Q: How much does a typical autonomous task cost?**
A: At $5/MTok input and $25/MTok output, a complex multi-step task generating ~10K tokens costs roughly $0.25-0.50. The 30% tokenizer overhead adds ~$0.08-0.15. Even with Claude Code's iterative loop, autonomous development is dramatically cheaper than paying for 3-6 human engineers.

**Q: Can I use Claude Code with other models?**
A: Claude Code is designed for Anthropic's Claude models. For multi-provider autonomous workflows, consider using an aggregator like FreeModel that provides a unified API across multiple providers.

## Verdict

Project Fetch Phase Two is a landmark demonstration of what autonomous API agents can achieve. Claude Opus 4.7 completing hardware software engineering tasks 20x faster than humans is not theoretical — it's a replicable result with real code, real sensors, and real robots.

For API developers, the takeaway is clear: **autonomous multi-step task execution via Claude Code + Opus 4.7 is production-ready**. The model writes code that works on first try, tests it against real hardware, and iterates until the task is complete. The human stays in the decision loop but the execution burden is effectively eliminated.

### Decision Tree

- **Need autonomous coding with hardware?** Claude Opus 4.7+ via Claude Code
- **Budget-sensitive, software-only?** Opus 4.7 at $5/$25 per MTok is excellent value
- **Need multi-provider routing?** Consider FreeModel for unified API access
- **China-direct access required?** Use an OpenAI-compatible aggregator
- **Maximum quality for coding?** Fable 5 is currently the frontier, but Opus 4.7 is close behind at half the price

---

*Updated: June 23, 2026. Anthropic Project Fetch Phase Two published June 18, 2026 by Anthropic Frontier Red Team.*
