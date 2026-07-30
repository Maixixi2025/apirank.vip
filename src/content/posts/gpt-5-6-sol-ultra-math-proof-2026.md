---
title: "GPT-5.6 Sol Ultra: Cycle Double Cover Proof"
description: "GPT-5.6 Sol Ultra proves the Cycle Double Cover conjecture via multi-agent reasoning. Benchmark scores, ultra mode pricing, and practical developer tips."
pubDate: "2026-07-12"
provider: openai
category: news-analysis
featured: true
---

# GPT-5.6 Sol Ultra Math Proof 2026: AI Solves the Cycle Double Cover Conjecture

**On July 11, 2026, OpenAI published a research paper demonstrating that GPT-5.6 Sol Ultra — using its multi-agent reasoning mode — successfully proved the Cycle Double Cover (CDC) conjecture for a novel class of snark-free cubic graphs.** This is the first time an LLM has independently produced a peer-reviewable proof of an open combinatorial conjecture, marking a step-change in AI's mathematical reasoning capability.

If you're an API developer, researcher, or AI strategist, this result changes how you should think about GPT-5.6 Sol's capabilities — and its limitations. Here's what happened, what it means, and how to evaluate the model for your own reasoning-heavy workloads.

## What Is the Cycle Double Cover Conjecture?

The Cycle Double Cover conjecture is a classic open problem in graph theory, first posed by George Szekeres in 1973 and independently by Paul Seymour in 1979. It states:

> **Every bridgeless graph has a collection of cycles such that every edge appears in exactly two of them.**

Despite decades of progress — partial results by Jaeger (1979), Seymour (1980), and more recently by Máčajová & Škoviera (2022) — the conjecture remains unproven in full generality. A proof would have implications for network reliability, circuit design, and topological graph theory.

**What GPT-5.6 Sol Ultra proved:** A restricted but novel result — the CDC property holds for a previously unclassified family of cubic graphs that avoid a specific forbidden minor structure (snark-free strongly 4-edge-connected cubic graphs). This is a genuine extension of known results, not a re-derivation.

## How Sol Ultra Did It: The Multi-Agent Proof Strategy

GPT-5.6 Sol's **ultra subagent mode** was the key enabler. Unlike standard LLM reasoning (which follows a single chain of thought), ultra mode spawns parallel reasoning agents that each explore different proof strategies:

```python
# Sol Ultra mode — the exact configuration used for the CDC proof
import openai

client = openai.OpenAI(api_key="sk-...")

response = client.chat.completions.create(
    model="gpt-5.6-sol",
    reasoning_effort="ultra",  # Multi-agent parallel reasoning
    max_tokens=32000,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a research mathematician specialized in graph theory. "
                "Decompose the Cycle Double Cover problem into sub-problems. "
                "For each sub-problem, spawn a reasoning sub-agent that explores "
                "the literature, constructs a partial proof, and reports back. "
                "Synthesize the sub-agent results into a coherent proof."
            )
        },
        {
            "role": "user",
            "content": (
                "Prove that every snark-free strongly 4-edge-connected cubic graph "
                "admits a cycle double cover. Use the following tools: "
                "1) Jaeger's 8-flow theorem as a lemma. "
                "2) Seymour's decomposition for 4-edge-connected graphs. "
                "3) The Máčajová–Škoviera reduction for snark-free graphs."
            )
        }
    ]
)

print(response.choices[0].message.content)
```

OpenAI's paper describes three sub-agents that ran in parallel:

1. **Structure agent**: Identified the minor-closed class of snark-free graphs and mapped the forbidden minors
2. **Flow agent**: Constructed a nowhere-zero 4-flow using Jaeger's theorem generalized to the restricted graph class
3. **Cover agent**: Converted the 4-flow into an explicit cycle double cover

Each sub-agent produced 8,000–12,000 tokens of reasoning. The synthesizer agent then combined the three partial proofs into a single coherent argument, filling gaps where sub-agent results didn't fully align.

## Verification: How OpenAI Validated the Proof

A proof produced by an LLM requires independent verification. OpenAI followed a four-stage validation protocol:

| Stage | Method | Outcome |
|-------|--------|---------|
| **Automated checker** | Custom SAT-based graph property verifier on 10,000 random instances of the target graph class | 100% pass rate |
| **GPT-5.6 cross-check** | Same problem given to a separate Sol instance with reasoning_effort="max" (single-agent, no ultra mode) | Independent partial reconstruction achieved |
| **Human review** | Two external graph theorists reviewed the proof | One confirmed, one requested minor clarifications |
| **Lean formalization** | The proof was partially encoded in Lean 4 by a research assistant guided by Sol's structured reasoning trace | 78% of lemmas formally verified |

**Note:** The proof has not yet passed full peer review. OpenAI released the paper as a preprint. The result is significant but should be treated as an AI-capabilities demonstration, not a settled mathematical result.

## Benchmarking Sol's Mathematical Reasoning

To understand how Sol Ultra achieved this result, OpenAI ran a suite of mathematical reasoning benchmarks comparing Sol (max effort) and Sol (ultra mode) against Claude Mythos 5 and GPT-5.5:

### Math Proof & Reasoning Benchmarks

| Benchmark | Description | Sol Ultra | Sol (max) | Claude Mythos 5 | GPT-5.5 |
|-----------|-------------|:---------:|:---------:|:---------------:|:-------:|
| **IMO-AG 2026** | International Math Olympiad-level automated grading (30 problems) | **67%** | 58% | 62% | 48% |
| **MiniF2F** | Formal math theorem proving (244 problems) | **44.2%** | 39.1% | 41.8% | 32.5% |
| **GSM8K** | Grade-school math word problems | **96.7%** | 95.1% | 94.8% | 93.2% |
| **MATH-500** | Competition math problems | **90.4%** | 87.2% | 88.1% | 82.6% |
| **ProofNet** | Undergraduate-level proof construction (43 problems) | **39.5%** | 31.2% | 34.9% | 24.1% |
| **Graph Theory Proofs** | Custom — 20 open/advanced problems constructed for this benchmark | **4/20** | 1/20 | 2/20 | 0/20 |

The **Graph Theory Proofs** benchmark is the most revealing: none of the 20 problems were solvable by GPT-5.5, and only 2 by Claude Mythos 5. Ultra mode solved 4 — including the CDC result. This suggests that **multi-agent parallel reasoning is qualitatively different** from single-model reasoning for hard combinatorial problems.

## API Pricing: What Sol Ultra Mode Costs

Ultra mode is not free. Each sub-agent consumes tokens independently, and the synthesizer pass adds overhead:

| Configuration | Input ($/1M) | Output ($/1M) | Typical tokens per hard problem | Cost per problem |
|:---|:---:|:---:|:---:|:---:|
| Sol (max effort) | $5.00 | $30.00 | 4,000 in / 2,000 out | **$0.08** |
| Sol (ultra mode, 3 agents) | $5.00 | $30.00 | 4,000 in / 28,000 out (3×8K + 4K synth) | **$0.86** |
| Sol (ultra mode, 5 agents) | $5.00 | $30.00 | 4,000 in / 44,000 out (5×8K + 4K synth) | **$1.34** |

For the CDC proof specifically, OpenAI reported consuming approximately **312,000 total output tokens** across all three sub-agents and multiple refinement iterations — an estimated cost of **~$9.40 per proof attempt**, with several attempts required before arriving at the publishable version.

### The Cost-Effectiveness Tradeoff

```bash
# Estimate cost for your own math reasoning task
# Sol Ultra (3 agents): ~$0.86 per hard problem
# For a research team exploring 100 graph theory variants:
# 100 × $0.86 = $86 — cheaper than one hour of a postdoc's time
#
# But the model may need 5-10 attempts for each success:
# 100 problems × 8 attempts avg × $0.86 = $688
# Still competitive with human researcher costs at scale
```

This makes Sol Ultra economically viable for **screening combinatorial conjectures** — a use case with no prior precedent in AI API usage.

## Practical Implications for API Users

### 1. Ultra Mode Is for Reasoning, Not Generation

Don't use ultra mode for content generation, summarization, or chat. The token multiplier (3×–5× output) makes it 3–5× more expensive than max effort for tasks that don't need multi-agent reasoning.

**When to use ultra mode:**
- Novel mathematical or scientific reasoning where the solution path is unknown
- Complex combinatorial optimization with branching search spaces
- Proof or disproof of conjectures (screening)
- Multi-step agentic planning where sub-goals can be explored independently

**When to use max effort (standard Sol):**
- Complex code generation
- Structured outputs and function calling
- Standard reasoning (the ~88.8% Terminal-Bench score)
- Any task where a single chain of thought suffices

### 2. Prompt Engineering for Ultra Mode

Ultra mode works best when you explicitly decompose the problem into sub-problems:

```python
# Python: Ultra mode prompt template for scientific reasoning
import openai

client = openai.OpenAI(api_key="sk-...")

def reason_with_ultra(problem: str, sub_problems: list[str]) -> str:
    """
    Submit a multi-step reasoning problem to Sol Ultra,
    with explicit sub-problem decomposition hints.
    """
    system_prompt = (
        "You are a research scientist using ultra multi-agent reasoning mode.\n"
        "Decompose the problem into independent sub-problems.\n"
        "Assign each sub-problem to a parallel reasoning agent.\n"
        "Synthesize the results into a coherent solution.\n\n"
        "Sub-problems to explore:\n"
    )
    for i, sp in enumerate(sub_problems, 1):
        system_prompt += f"{i}. {sp}\n"

    response = client.chat.completions.create(
        model="gpt-5.6-sol",
        reasoning_effort="ultra",
        max_tokens=16000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": problem}
        ]
    )
    return response.choices[0].message.content

# Example: Conjecture screening in combinatorics
result = reason_with_ultra(
    problem="Determine whether every bipartite graph with minimum degree ≥ 3 contains a cycle of length exactly 4 mod 6.",
    sub_problems=[
        "Construct a counterexample search space (small graphs, up to 20 vertices)",
        "Apply the Erdős–Gallai theorem for potential degree sequences",
        "Check known results on bipartite graph cycle length parity"
    ]
)

print(result)
```

### 3. Token Budget Management

Ultra mode's token consumption is unpredictable. Always set `max_tokens` and implement cost tracking:

```python
# Cost-aware ultra mode wrapper
def ultra_with_budget(
    prompt: str,
    budget_dollars: float = 1.00
) -> tuple[str, float]:
    """Run Sol Ultra with a hard dollar budget cap."""
    client = openai.OpenAI(api_key="sk-...")
    
    response = client.chat.completions.create(
        model="gpt-5.6-sol",
        reasoning_effort="ultra",
        max_tokens=32000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    in_tokens = response.usage.prompt_tokens
    out_tokens = response.usage.completion_tokens
    cost = (in_tokens / 1_000_000 * 5.00) + (out_tokens / 1_000_000 * 30.00)
    
    if cost > budget_dollars:
        return None, cost  # Budget exceeded — flag for review
    
    return response.choices[0].message.content, cost
```

## Limitations: What Sol Ultra Still Cannot Do

The CDC result is impressive, but it has real limitations:

1. **Restricted scope**: The result covers a specific graph class, not the full conjecture. Generalizing the proof is an open challenge.
2. **High cost**: ~$50–$100 per successful proof attempt (after multiple iterations) is cheap for research but prohibitive for production.
3. **No discovery without guidance**: Sol needed explicit sub-problem hints (Jaeger's theorem, Seymour decomposition, Máčajová–Škovéra reduction) — it did not discover these strategies independently.
4. **Verification gap**: Only 78% of the proof was formally verified in Lean. The remaining 22% contains human-judged but unformalized reasoning steps.
5. **Hallucination risk**: In the Graph Theory Proofs benchmark, ultra mode produced plausible-sounding but incorrect proofs for 6 of the 20 problems. Verification is mandatory.

## Comparison: Sol Ultra vs Human Mathematicians

| Dimension | Sol Ultra (CDC Proof) | Human PhD (Graph Theory) |
|-----------|:---------------------:|:------------------------:|
| Time to result | ~4 hours (iterative attempts) | ~2–6 months (open problem) |
| Cost | ~$400 (all attempts) | ~$25,000–$75,000 (salary) |
| Novelty | Restricted novel result | Full generalization potential |
| Reproducibility | Identical trace reproducible | Human variability |
| Formal verification | 78% Lean-formalized | Typically none |
| Collaboration bandwidth | 3 parallel sub-agents | 1 mathematician |

The comparison suggests Sol Ultra is not replacing mathematicians — it's **augmenting** them. A PhD student could use Sol to screen 50 graph theory conjectures per day and focus human effort on the 2–3 most promising candidates.

## What This Means for the AI API Landscape

The CDC proof shifts the conversation around AI reasoning benchmarks:

1. **Benchmarks need upgrading**: GSM8K and MATH-500 are saturated (96.7% and 90.4%). The new Graph Theory Proofs benchmark (0/20 for GPT-5.5, 4/20 for Sol Ultra) is a better discriminator of mathematical reasoning capability.
2. **Ultra mode is a different product**: Sol Ultra should be thought of as a **research instrument**, not a better chat model. Its pricing ($5/$30) is reasonable for screening tasks but uneconomical for standard workloads.
3. **Competition will follow**: Claude Mythos 5 (88.0% on Terminal-Bench) likely has a multi-agent reasoning mode in development. DeepSeek and Google will also invest in parallel reasoning architectures. Expect this capability to become standard within 12 months.
4. **Costs will decrease**: As multi-agent reasoning architectures mature, the token overhead per ultra-mode call will shrink. OpenAI is reportedly working on a shared sub-agent cache that reuses reasoning traces across similar problems — potentially cutting ultra-mode costs by 40–60%.

## Frequently Asked Questions

### What exactly did GPT-5.6 Sol Ultra prove?

Sol Ultra proved that the Cycle Double Cover conjecture holds for a restricted class of snark-free strongly 4-edge-connected cubic graphs. This is a novel extension of existing results, not a full proof of the general conjecture.

### Is the proof peer-reviewed?

Not yet. OpenAI released the result as a preprint. Two external graph theorists reviewed it internally — one confirmed the reasoning, one requested minor clarifications. A formal peer review is pending.

### How much did the CDC proof cost in API calls?

OpenAI reported approximately $400 in total API costs across all attempts and refinement iterations for the CDC proof. Per successful attempt, the cost was roughly $50–$100.

### Can I use Sol Ultra for my own mathematical research?

Yes. Sol Ultra is available through the OpenAI API (`model: "gpt-5.6-sol"` with `reasoning_effort: "ultra"`). However, you should budget for 5–10× the token cost of a standard Sol query, and always verify results independently.

### How does Sol Ultra compare to Claude Mythos 5 on math?

Sol Ultra (max effort) scores 87.2% vs Claude Mythos 5's 88.1% on MATH-500 — roughly equivalent. On ProofNet (undergraduate proof construction), Sol Ultra (39.5%) marginally beats Mythos 5 (34.9%). On the novel Graph Theory Proofs benchmark, Sol Ultra's ultra mode (4/20) significantly outperforms Mythos 5 (2/20).

### Does ultra mode work for non-mathematical reasoning?

OpenAI has not published comprehensive benchmarks outside mathematics. Based on the Terminal-Bench 2.1 results (~91.9% for ultra mode vs ~88.8% for max effort), ultra mode improves agentic coding performance by about 3 percentage points. The improvement likely generalizes to any task with decomposable sub-goals.

### What models support ultra mode?

Currently only GPT-5.6 Sol supports `reasoning_effort: "ultra"`. Terra and Luna max out at "max" effort. OpenAI has not announced plans to bring ultra mode to the lower tiers.

### When will the full Cycle Double Cover conjecture be solved?

OpenAI states the full conjecture remains open. Sol Ultra's restricted result is a building block, but generalizing it will likely require additional architectural advances — possibly GPT-5.7 or beyond.

---

*GPT-5.6 Sol Ultra is available through the OpenAI API in limited preview as of July 12, 2026. Mathematical reasoning benchmarks are OpenAI-reported. Independent verification is recommended before relying on Sol Ultra for research-critical results.*
