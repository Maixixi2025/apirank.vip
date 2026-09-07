# OpenAI × Cursor Termination — Verification Report

**Task:** Verify the announced termination of OpenAI's API contract with Cursor (Anysphere) following SpaceX acquisition, using only primary sources. Do not invent facts.

## Sources fetched and their status

| # | Source URL | Status |
|---|------------|--------|
| 1 | https://openai.com/index/our-decision-on-cursor-following-its-acquisition-by-spacex/ | **Cloudflare-walled** (only SVG + CF challenge script returned). URL exists; body not retrievable from this environment. |
| 2 | https://the-decoder.com/openai-cuts-off-cursor-after-spacex-acquisition-citing-musks-history-of-breaking-contracts/ | **FULL TEXT RETRIEVED** (1374 lines). By Matthias Bastian, dated Aug 29, 2026. |
| 3 | https://www.reuters.com/business/media-telecom/openai-end-partnership-with-spacexs-cursor-2026-08-29/ | **Cloudflare/datadome-walled** (770-byte block page). Reuters attribution appears in CNBC photo credit ("Manuel Orbegozo \| Reuters") and in Bing News aggregator headlines. Body not directly retrievable. |
| 4 | https://www.cnbc.com/2026/08/29/openai-cursor-spacex-model-access.html | **FULL TEXT RETRIEVED**. By Lora Kolodny, dated Sat Aug 29 2026 3:05 PM EDT. |
| 5 | https://www.forbes.com/sites/jonmarkman/2026/08/31/openai-cuts-off-cursor-after-spacexs-60-billion-takeover/ | **Cloudflare-walled** (770-byte block page). $60B figure corroborated independently by CNBC ("SpaceX completed its $60 billion acquisition of Cursor on Aug. 14"). |
| 6 | https://www.techzine.eu/news/devops/143932/openai-withdraws-models-from-cursor-following-acquisition-by-spacex/ | **Cloudflare-walled** ("Just a moment…" challenge page). Headline only appears in Bing News aggregator. |

## Cross-corroboration matrix

Every fact below is sourced from **the-decoder.com (full body)** AND **CNBC (full body)**, which independently reproduce the OpenAI announcement text, the Cursor/Truell reply, the Anthropic/Tom Brown X post, and the historical precedents.

---

```
=== OpenAI Cursor Termination Verified Facts ===

TERMINATION
- effective: 2026-11-12
  (the-decoder.com: "OpenAI announced that it will terminate its contract with
  Cursor effective November 12, 2026";
  CNBC: "Its 'proposed shutoff date' for OpenAI models via Cursor is
  Nov. 12, 2026")
- notice period: "the maximum notice period allowed under the contract, which
  includes a clause giving OpenAI a limited window to end the agreement after a
  change in ownership" — the-decoder.com
  Source URL: https://the-decoder.com/openai-cuts-off-cursor-after-spacex-acquisition-citing-musks-history-of-breaking-contracts/

OPENAI STATEMENT
- spokesperson: Thibault Sottiaux (title not given in either retrieved source;
  named only as "OpenAI's Thibault Sottiaux" — decoder / CNBC)
- verbatim quote: "It boils down to trust." — Sottiaux, per the-decoder.com
  Full OpenAI announcement quote (reproduced by CNBC):
    "We are making this choice because we cannot be confident that SpaceX will
    use our technology within our terms of service, based on our experience with
    Elon Musk's companies violating contracts."
  Source URLs:
    https://www.cnbc.com/2026/08/29/openai-cursor-spacex-model-access.html
    https://the-decoder.com/openai-cuts-off-cursor-after-spacex-acquisition-citing-musks-history-of-breaking-contracts/
- safety framing (re: Astra):
    "With the upcoming Astra model, which reportedly has advanced cyber
    capabilities, there's 'a new level of accountability' to make sure
    partners comply with the terms of service."
  Source: https://the-decoder.com/openai-cuts-off-cursor-after-spacex-acquisition-citing-musks-history-of-breaking-contracts/
  (CNBC does not mention Astra — only the decoder does.)

SPACEX ACQUISITION
- deal value: $60 billion
  CNBC: "SpaceX completed its $60 billion acquisition of Cursor on Aug. 14,
  according to financial filings"
  CNBC video caption: "SpaceX to buy Cursor AI parent company Anysphere in
  $60 billion deal"
  Source: https://www.cnbc.com/2026/08/29/openai-cursor-spacex-model-access.html
  Forbes URL (https://www.forbes.com/sites/jonmarkman/2026/08/31/openai-cuts-off-cursor-after-spacexs-60-billion-takeover/) was CF-walled and could not be loaded directly, but the $60B figure is independently confirmed by CNBC.
- closing date: 2026-08-14 (CNBC)

CURSOR RESPONSE (Michael Truell, posted on X)
- traffic share: "about 5%"
    CNBC: "OpenAI models serve about 5% of Cursor user traffic"
    Decoder: "OpenAI models made up only about five percent of Cursor's AI
    traffic"
- verbatim quote (from CNBC):
    "OpenAI models serve about 5% of Cursor user traffic, and we're speaking
    with the OpenAI team to resolve this. Cursor was one of the very first
    users of OpenAI, we've worked closely with their team for years, and we've
    trusted their platform to be neutral infrastructure for our business."
  (Decoder reproduces this quote in near-identical form.)

ANTHROPIC RESPONSE
- spokesperson: Tom Brown
  CNBC: "Anthropic co-founder and executive Tom Brown"
  Decoder: "Tom Brown, Anthropic's co-founder and Chief Compute Officer"
- verbatim quote (X post, Friday night Aug 28/29 2026):
    "Cursor has been a trusted partner of Anthropic since Sonnet 3.5. We'll
    continue to increase compute to support Claude models in Cursor and are
    excited for what comes next with them at SpaceX."
  Source: https://www.cnbc.com/2026/08/29/openai-cursor-spacex-model-access.html
  (Decoder paraphrases identically.)
- timestamp: "Friday night" (CNBC) / "Update – Aug 29, 2026" (Decoder banner).
  Exact hh:mm timestamp NOT verifiable from retrieved sources.

CONTINUITY FOR EXISTING USERS
- API key BYO model: "Users who access GPT models through Cursor will still be
  able to use their own OpenAI API keys" — the-decoder.com
- IDE extension continuity: "OpenAI will continue to provide access through
  its IDE extensions for Cursor" — the-decoder.com
  CNBC adds: "OpenAI also said it would not provide future models to Cursor
  as it winds down the agreement."
  Source: https://the-decoder.com/openai-cuts-off-cursor-after-spacex-acquisition-citing-musks-history-of-breaking-contracts/

PRECEDENTS
- Windsurf (Anthropic blocked, 2025-06):
    "In June 2025, Anthropic blocked the coding tool Windsurf from accessing
    its Claude models after reports surfaced that OpenAI wanted to acquire
    Windsurf." — the-decoder.com
    CNBC corroborates: "Last June, Anthropic … blocked Windsurf access to
    its Claude AI models."
  Sources: decoder (above) and
  https://www.cnbc.com/2026/08/29/openai-cursor-spacex-model-access.html
- OpenAI benchmarks (Anthropic revoked, 2025-08):
    "In August 2025, the tables turned on OpenAI when Anthropic revoked the
    company's API access because OpenAI teams had apparently used Claude for
    internal benchmarks ahead of the GPT-5 launch." — the-decoder.com
  Source: https://the-decoder.com/openai-cuts-off-cursor-after-spacex-acquisition-citing-musks-history-of-breaking-contracts/

UPCOMING MODEL
- name: Astra
- capability claim: "the upcoming Astra model, which reportedly has advanced
  cyber capabilities" — the-decoder.com. Phrased as "reportedly has"
  (reporting attribution), not as a direct OpenAI statement.

UNVERIFIED / NOT FOUND:
- Reuters article body: URL CF-walled in this environment; existence implied by
  CNBC photo credit "Manuel Orbegozo | Reuters" and Bing News aggregator
  headlines indexing reuters.com stories about OpenAI/Cursor. No Reuters text
  was directly retrieved.
- Forbes article body ($60B framing): Forbes URL CF-walled; however the $60B
  figure itself is independently confirmed by CNBC's article, so the dollar
  amount is verified even though the Forbes URL could not be loaded.
- Techzine article body: CF-walled; only the headline ("Techzine Europe 17h —
  OpenAI withdraws models from Cursor following acquisition by SpaceX") is
  independently visible via Bing News aggregator.
- OpenAI blog body: CF-walled (URL exists, only CF challenge + OpenAI logo SVG
  returned). All OpenAI statements above are quoted second-hand via
  the-decoder.com and CNBC.
- Sottiaux's exact job title: not stated in either retrieved source (named
  only as "OpenAI's Thibault Sottiaux").
- Specific X-post timestamp (hh:mm) of Tom Brown's tweet: not in the retrieved
  sources; only "Friday night" framing is given.
- Whether Reuters independently quotes Sottiaux by name: UNVERIFIED — Reuters
  body not retrievable.
