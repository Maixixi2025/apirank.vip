# NVIDIA Acquires Hugging Face — Verified Fact Bundle (2026-09-05)

Source for the `nvidia-hugging-face-acquisition-2026` news-analysis article on apirank.vip.
All facts verified via curl toward primary/outlet pages on/before 2026-09-05. Reusable for any
future "NVIDIA owns HF / open-model inference supply shift" article without re-fetching.

## 1. Deal facts
- **Value (verbatim, NVIDIA blog):** $12,930,300,000 (reported as ~$12.9B / $12.93B).
  https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/
- **Announced:** Thu 2026-09-03 by Jensen Huang (NVIDIA blog byline). CNBC: Ari Levy, "Published Thu, Sep 3 2026 8:04 AM EDT".
  https://www.cnbc.com/2026/09/03/nvidia-agrees-to-buy-hugging-face-for-almost-13-billion-ai-expansion.html
- **Expected close:** first half of 2027, subject to regulatory approval (The Register).
  https://www.theregister.com/ai-and-ml/2026/09/03/nvidia-buys-hugging-face-for-129b-promises-not-to-squeeze-too-hard/5294208
- **No formal FTC/DOJ/EU/UK-CMA public review/filing reported** as of 2026-09-05 (deal announced days prior).
- **HF last valuation:** $4.5B (2023). Series D 2023: $235M led by Salesforce Ventures; Google, Amazon, IBM, Nvidia participated. Cumulative raised ~$395M+ (Crunchbase) / ~$400M (PitchBook via Wired).
  - The Verge: https://www.theverge.com/tech/985474/nvidia-buying-hugging-face-deal
  - TechCrunch: https://techcrunch.com/2026/09/03/nvidia-confirms-it-will-buy-hugging-face-for-12-9-billion/
- **Rejected prior lower NVIDIA offer:** FT reported HF rejected a ~$500M investment offer from Nvidia the prior year that would have valued it at ~$7B (The Verge / TechCrunch / Wired).
- **NVIDIA deal-sized context:** HF = NVIDIA's 2nd-largest deal ever. Largest: ~$20B for Groq assets (end of 2025). Prior record ~$7B Mellanox (2019). (CNBC)
- **Other HF backers (latest round):** AMD, Intel, Qualcomm, Salesforce (reportedly sought to buy HF pre-NVIDIA) per SiliconANGLE. Earlier/other: Betaworks, Lux, Sequoia Ventures, Coatue, Addition, Greg Brockman, Richard Socher, Kevin Durant (Wired/PitchBook).

## 2. Founders
- Clem(ent) Delangue (CEO), Julien Chaumond, Thomas Wolf — founded ~2016 in NYC (French trio). NVIDIA blog: "Clem, Julien, Thomas".

## 3. HF platform scale (NVIDIA blog verbatim)
- 18M+ developers/researchers/creators; 3M+ models; 500K datasets; 1M applications; 200K+ companies.
- NVIDIA is the largest contributor: 500+ models + 250+ open datasets on HF.

## 4. Openness commitments (NVIDIA blog verbatim)
- "Hugging Face will remain an open platform for the entire AI ecosystem. Developers will choose the models they want, the frameworks they want, the clouds and inference service providers they want and the computing platforms they want."
- "NVIDIA compute will not be required to build on or deploy through Hugging Face."
- "continue to support multi-cloud and multi-accelerator development and deployment."
- Huang open-weights rationale: "asymmetric advantage" to defenders (CNBC quote).

## 5. Direct quotes (verbatim + who + where)
1. Jensen Huang / NVIDIA blog 09-03: "I'm excited to announce that NVIDIA has agreed to acquire Hugging Face for $12,930,300,000. Together, we will scale Hugging Face's platform..."
2. Clem Delangue / X post 09-03 (quoted by The Register/TechCrunch/Wired): "Thanks to the community, we've shown that it can be a complement, and even an alternative, to closed-source APIs. But for it to happen at larger scale, it needs more compute, more support, more collaboration and more visibility. That's why we went to talk to Jensen, who offered to do exactly that with us."
3. Clem Delangue / CNBC Squawk Box 09-03: "During the summer, I think we realized that Hugging Face and open-source AI in general was at the turning point... needed more resources, more scale, more visibility." Also: he "approached first because Nvidia was 'a perfect home'... discussions went quite fast."
4. Jensen Huang / CNBC 09-03 (asymmetric defense): "When I say asymmetric capability, there are way more people who are protecting than there are people who are attacking... gives the defenders an asymmetric advantage."
5. Forrester Charlie Dai / The Register 09-03: HF gives Nvidia "a stronger position at the developer, model distribution, and community layers... Enterprises should watch for future shifts."
6. Forrester Naveen Chhabra / SiliconANGLE 09-03: "Nvidia gains visibility into customers' preferences and the AI models they use... They are securing the software layer because hardware-only companies get commoditized over time."
7. GoodData.AI CEO Roman Stanek / SiliconANGLE 09-03 (email): "smaller, specialized models... will ultimately power 80% of AI applications."

## 6. HF inference/hosting infrastructure (early Sept 2026, via HF docs + Hub API)
- **Inference Providers roster (18 partners, verified via Hub API allow-list + docs index):**
  Baseten, Cohere, Cerebras, DeepInfra, Fal AI, Featherless AI, Fireworks, Groq, hf-inference (own),
  Novita, Nscale, OVHcloud, PublicAI, Replicate, Scaleway, Together, WaveSpeedAI, Z.ai.
  SambaNova / Hyperbolic / Nebius NOT on HF. NVIDIA NIM / DGX Cloud NOT a verified partner as of 2026-09-05
  (nvidia-nim/nvidia/dgx queries rejected; no doc page).
- **Zero lock-in / routing model:** Inference Providers = "Zero Vendor Lock-in." Default provider `:fastest`
  (highest tokens/sec); suffix `:cheapest` (lowest $ per output token); `:preferred`. Or explicit
  `openai/gpt-oss-120b:groq` per-model-id. Endpoint `https://router.huggingface.co/v1/chat/completions`
  = "drop-in OpenAI replacement"; auto failover when provider="auto".
- **HF takes NO markup:** "Hugging Face charges you the same rates as the provider... pass through the provider costs directly."
- **Monthly compute credits:** Free $0.10 (spend on Inference Providers); PRO $2.00 (all HF compute);
  Team/Enterprise $2.00/seat. Pay-as-you-go beyond credits. Two billing modes: Routed by HF (default; credits)
  vs Custom Provider Key (bring-your-own key; no HF billing).
- **PRO subscription:** $9/month — 20x included inference credits, private repo 10x storage to 1TB, etc.
- **ZeroGPU:** NVIDIA RTX Pro 6000 Blackwell (48GB/96GB). Daily GPU quota: unauth 2min, Free 5min, PRO 40min,
  Team 40min, Enterprise 60min (all Low/Medium/Highest/Highest priority). Beyond: $1 per 10 min from credits.

## 7. Analyst / community theme (for the "necklace" / risk section)
- Dominant theme = concern over neutral-platform consolidation (HF owned by the dominant AI chipmaker) tempered
  by NVIDIA's openness pledge. NO public statements found from Baseten/Together/Replicate/Fireworks as of 09-05.
- apirank angle: apirank's ICP (devs routing via aggregators/proxies) depends on HF as a neutral, no-markup,
  multi-provider marketplace. The deal's real exposure = whether platform-layer neutrality + `:fastest`/`:cheapest`
  auto-routing + zero-markup pass-through survive, and whether NVIDIA NIM eventually joins the provider roster /
  is favored in routing. Close is H1 2027 — 3 quarters of deal-uncertainty runway.

## 8. Honest caveats
- Reuters syndicated piece was bot-walled (MSN JS shell); facts corroborated via CNBC/TechCrunch/Verge/Register/Wired.
- No dedicated huggingface.co/blog acquisition statement found; HF's public statement came via Delangue's X post.
- Microsoft/Facebook-style precision of "HF generates ~$150M annualized revenue" came from Wired/PitchBook context;
  treat as approximate.
- Enterprise seat pricing $ figures not independently verifiable (JS-shell) beyond docs' $2/seat compute credit.
