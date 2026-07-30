// scripts/lib/llm_extract.js
// LLM-based fallback extractor for providers with no structured pricing data.
// Uses MiniMax-M3 via minimax-cn (OpenAI-compatible API).
//
// Reads MINIMAX_CN_API_KEY + MINIMAX_CN_BASE_URL env vars.
// Falls back to OPENAI_API_KEY / OPENAI_BASE_URL for portability.

const DEFAULT_MODEL = 'MiniMax-M3';

async function llmExtractPricing({ provider, rawText, rawTables, sourceUrl, log = () => {} }) {
  const apiKey = process.env.MINIMAX_CN_API_KEY || process.env.OPENAI_API_KEY;
  const baseUrl = process.env.MINIMAX_CN_BASE_URL
    || process.env.OPENAI_BASE_URL
    || 'https://minimaxi.com/anthropic';
  const model = process.env.MINIMAX_CN_MODEL || DEFAULT_MODEL;

  if (!apiKey) {
    log('  ⚠ no LLM API key set — skipping LLM extraction');
    return null;
  }

  // Compose the prompt — keep it small, give the model the relevant slice.
  const textSlice = (rawText || '').slice(0, 6000);
  const tablesSlice = (rawTables || '').slice(0, 4000);
  const userContent = [
    `Provider: ${provider.name} (${provider.id})`,
    `Source URL: ${sourceUrl}`,
    `Existing pricing in apirank:`,
    `  input: ${provider.pricing?.input || '(none)'}`,
    `  output: ${provider.pricing?.output || '(none)'}`,
    '',
    '=== EXTRACTED PAGE TEXT (first 6KB) ===',
    textSlice,
    '',
    '=== EXTRACTED TABLES (first 4KB) ===',
    tablesSlice,
  ].join('\n');

  const systemPrompt = `You are a pricing extractor for apirank.vip, a directory comparing AI API providers.

Given a provider's pricing page text and existing apirank data, output JSON with the LATEST per-million-token rates you can verify from the page.

Output schema (ONLY output JSON, nothing else):
{
  "pricing": { "input": "<Chinese summary of input rates per model>", "output": "<Chinese summary>" },
  "pricingEN": { "input": "<English summary of input rates per model>", "output": "<English summary>" },
  "confidence": "high" | "medium" | "low",
  "notes": "<short string about what changed or why low confidence>"
}

Rules:
- Per-million-token prices only. Convert from $/1K if needed.
- If only ranges are visible (e.g. "$0.10 - $5"), include the range.
- If pricing page requires login or doesn't show numeric rates, set confidence:"low" and notes to explain.
- Do NOT invent numbers. If you can't read it, say so.
- Keep summaries ≤ 200 chars per field.
- Preserve model name ordering from the source (flagship first).
- Return ONLY JSON. No markdown fences. No preamble.`;

  // Use chat/completions endpoint (Anthropic-compatible baseUrl still typically accepts this)
  const endpoint = baseUrl.includes('anthropic')
    ? `${baseUrl.replace(/\/+$/, '')}/v1/messages`
    : `${baseUrl.replace(/\/+$/, '')}/v1/chat/completions`;

  let res;
  try {
    if (endpoint.includes('/messages')) {
      // Anthropic format
      res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model,
          max_tokens: 800,
          system: systemPrompt,
          messages: [{ role: 'user', content: userContent }],
        }),
      });
    } else {
      // OpenAI format
      res = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          model,
          temperature: 0.1,
          max_tokens: 800,
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: userContent },
          ],
        }),
      });
    }
  } catch (e) {
    log(`  ⚠ LLM fetch failed: ${e.message}`);
    return null;
  }

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    log(`  ⚠ LLM HTTP ${res.status}: ${body.slice(0, 200)}`);
    return null;
  }

  const data = await res.json();
  let content;
  if (data?.content?.[0]?.text) {
    content = data.content[0].text;
  } else if (data?.choices?.[0]?.message?.content) {
    content = data.choices[0].message.content;
  } else {
    log('  ⚠ LLM returned unexpected shape');
    return null;
  }

  // Strip markdown fences if present
  content = content.trim().replace(/^```(?:json)?\s*/i, '').replace(/```\s*$/i, '');

  let parsed;
  try {
    parsed = JSON.parse(content);
  } catch (e) {
    log(`  ⚠ LLM output not JSON: ${content.slice(0, 200)}`);
    return null;
  }

  return {
    ...parsed,
    sourceUrl,
    _extractor: 'llm',
  };
}

module.exports = { llmExtractPricing };