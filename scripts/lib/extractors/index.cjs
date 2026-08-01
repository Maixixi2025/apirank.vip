// scripts/lib/extractors/index.js
// Registry of provider-specific extractors.
// Each extractor: async (provider, http, html) => { pricing: {...}, pricingEN?: {...}, sourceUrl, confidence }
// Returns null/undefined to fall through to LLM extractor.

const { fetchText } = require('../http.cjs');
const { stripHtml, extractTables, tablesToText } = require('../html.cjs');

// Helper: fetch a URL, return stripped text + tables text.
async function fetchAndParse(http, url) {
  const res = await fetchText(url, { timeoutMs: http.timeoutMs, retries: http.retries });
  const text = stripHtml(res.text);
  const tables = tablesToText(extractTables(res.text));
  return { text, tables, fetchedUrl: res.url, bytes: res.bytes };
}

// ===== openai =====
// openai.com/api/pricing returns 403 to scrapers — fall back to platform.openai.com/docs/pricing.
// platform.openai.com is the canonical docs site; table extraction works there.
const openai = {
  url: 'https://platform.openai.com/docs/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    // Look for known model id patterns + nearby prices. Tables are the primary source.
    // The pricing page uses these exact substrings: 'gpt-5.6-sol', 'gpt-5.6-terra', 'gpt-5.6-luna'.
    const result = {
      sourceUrl: fp.fetchedUrl,
      confidence: 'high',
      _rawExcerpt: (fp.tables || fp.text).slice(0, 4000),
    };
    // Per-model pricing tables: gpt-5.6-sol $5.00 input / $0.50 cached / $30 output (short ctx)
    // gpt-5.6-terra $2 input / $12 output, gpt-5.6-luna $0.20 input / $1.20 output
    // Note: dynamic prices — let LLM extractor handle if confidence drops.
    if (!fp.tables.includes('gpt-5.6-sol') && !fp.tables.includes('gpt-5.6')) {
      // Pricing page may have changed format — return with low confidence + raw excerpt.
      result.confidence = 'low';
      result._note = 'gpt-5.6 family not detected in extracted tables';
    }
    return result;
  },
};

// ===== anthropic =====
// console.anthropic.com renders pricing dynamically; claude.ai/pricing is the canonical page.
const anthropic = {
  url: 'https://claude.com/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    // Look for "$X / MTok" style
    const priceRe = /\$([\d.]+)\s*\/\s*MTok/gi;
    const matches = [];
    let m;
    while ((m = priceRe.exec(fp.text))) matches.push(parseFloat(m[1]));
    if (!matches.length) return null;
    return {
      pricingEN: {
        input: `Extracted ${matches.length} price points from claude.com/pricing (needs review)`,
        output: 'See claude.com/pricing/ for full breakdown',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.text.slice(0, 2000),
    };
  },
};

// ===== deepseek =====
// deepseek platform has a public pricing API-ish endpoint
const deepseek = {
  url: 'https://api-docs.deepseek.com/quick_start/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('DeepSeek')) return null;
    // 1M tokens ¥X cache miss / ¥Y cache hit
    const priceRe = /(?:¥|￥|CNY)\s*([\d.]+)/g;
    const matches = [];
    let m;
    while ((m = priceRe.exec(fp.text))) matches.push(parseFloat(m[1]));
    if (!matches.length) return null;
    return {
      pricing: {
        input: `从 deepseek 官网提取 ${matches.length} 个价格点（待人工核对）`,
        output: '见 api-docs.deepseek.com/quick_start/pricing',
        note: '由 update_pricing 脚本抓取',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000),
    };
  },
};

// ===== google (gemini) =====
// ai.google.dev/pricing is the canonical page
const google = {
  url: 'https://ai.google.dev/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.tables.includes('Gemini')) return null;
    return {
      pricingEN: {
        input: `Extracted Gemini pricing table from ai.google.dev (needs review)`,
        output: 'See ai.google.dev/pricing/ for full breakdown',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000),
    };
  },
};

// ===== openrouter =====
// has a public /api/v1/models endpoint
const openrouter = {
  url: 'https://openrouter.ai/api/v1/models',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    let json;
    try {
      json = JSON.parse(fp.text);
    } catch {
      return null;
    }
    if (!json?.data) return null;
    // Compute min/median/max for input and output pricing (in $/M tokens)
    // OpenRouter returns $/token. Free models use "0", some entries have negative
    // or non-numeric placeholders — filter to positive finite numbers only.
    const inputs = [];
    const outputs = [];
    for (const m of json.data) {
      const p = parseFloat(m.pricing?.prompt);
      const o = parseFloat(m.pricing?.completion);
      if (Number.isFinite(p) && p > 0) inputs.push(p * 1_000_000);
      if (Number.isFinite(o) && o > 0) outputs.push(o * 1_000_000);
    }
    if (!inputs.length) return null;
    inputs.sort((a, b) => a - b);
    outputs.sort((a, b) => a - b);
    const med = (arr) => arr[Math.floor(arr.length / 2)];
    return {
      pricingEN: {
        input: `$${inputs[0].toFixed(3)} to $${inputs[inputs.length - 1].toFixed(2)} per 1M tokens, median $${med(inputs).toFixed(3)} (across ${inputs.length} models, free models excluded)`,
        output: `$${outputs[0].toFixed(3)} to $${outputs[outputs.length - 1].toFixed(2)} per 1M tokens, median $${med(outputs).toFixed(3)} (across ${outputs.length} models, free models excluded)`,
        note: `Computed from openrouter.ai/api/v1/models live data (${json.data.length} total, ${inputs.length} paid)`,
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'high',
      _stats: {
        inputMin: inputs[0], inputMax: inputs[inputs.length - 1], inputMedian: med(inputs),
        outputMin: outputs[0], outputMax: outputs[outputs.length - 1], outputMedian: med(outputs),
        paidModelCount: inputs.length,
        totalModelCount: json.data.length,
      },
    };
  },
};

// ===== groq =====
// has a public pricing page; clean HTML
const groq = {
  url: 'https://groq.com/pricing/',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    return {
      pricingEN: {
        input: 'See groq.com/pricing/ for current per-model rates',
        output: 'See groq.com/pricing/ for current per-model rates',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== cohere =====
const cohere = {
  url: 'https://cohere.com/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.toLowerCase().includes('pricing')) return null;
    return {
      pricingEN: {
        input: 'See cohere.com/pricing for current per-model rates',
        output: 'See cohere.com/pricing for current per-model rates',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== mistral =====
const mistral = {
  url: 'https://mistral.ai/technology/#pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.toLowerCase().includes('€')) return null;
    return {
      pricingEN: {
        input: 'See mistral.ai pricing for current rates',
        output: 'See mistral.ai pricing for current rates',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== together =====
const together = {
  url: 'https://www.together.ai/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    return {
      pricingEN: {
        input: 'See together.ai/pricing for current per-model rates',
        output: 'See together.ai/pricing for current per-model rates',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== fireworks =====
const fireworks = {
  url: 'https://fireworks.ai/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    return {
      pricingEN: {
        input: 'See fireworks.ai/pricing for current per-model rates',
        output: 'See fireworks.ai/pricing for current per-model rates',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== modelscope (Alibaba, China; ¥ pricing) =====
const modelscope = {
  url: 'https://www.modelscope.cn/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('¥') && !fp.text.includes('￥')) return null;
    return {
      pricing: {
        input: '见 modelscope.cn/pricing 当前价格',
        output: '见 modelscope.cn/pricing 当前价格',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== siliconflow (China) =====
const siliconflow = {
  url: 'https://siliconflow.cn/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('¥') && !fp.text.includes('￥')) return null;
    return {
      pricing: {
        input: '见 siliconflow.cn 当前价格',
        output: '见 siliconflow.cn 当前价格',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== aliyun (bailian) =====
const aliyun = {
  url: 'https://bailian.console.aliyun.com/',
  async run(provider, http) {
    // bailian pricing is gated behind login; skip with low-value result
    return null;
  },
};

// ===== baidu wenxin =====
const baidu = {
  url: 'https://cloud.baidu.com/product/wenxinworkshop',
  async run(provider, http) {
    // also gated; skip
    return null;
  },
};

// ===== volcengine doubao =====
const volcengine = {
  url: 'https://www.volcengine.com/product/doubao',
  async run(provider, http) {
    return null;
  },
};

// ===== zhipu glm =====
const zhipu = {
  url: 'https://open.bigmodel.cn/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('¥') && !fp.text.includes('￥')) return null;
    return {
      pricing: {
        input: '见 bigmodel.cn/pricing 当前价格',
        output: '见 bigmodel.cn/pricing 当前价格',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== kimi moonshot =====
const kimi = {
  url: 'https://platform.moonshot.cn/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('¥') && !fp.text.includes('￥')) return null;
    return {
      pricing: {
        input: '见 platform.moonshot.cn/pricing 当前价格',
        output: '见 platform.moonshot.cn/pricing 当前价格',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== huggingface =====
const huggingface = {
  url: 'https://huggingface.co/docs/api-inference/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('$')) return null;
    return {
      pricingEN: {
        input: 'See huggingface inference pricing docs',
        output: 'See huggingface inference pricing docs',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== stability-ai =====
const stability = {
  url: 'https://platform.stability.ai/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('$')) return null;
    return {
      pricingEN: {
        input: 'See platform.stability.ai/pricing',
        output: 'See platform.stability.ai/pricing',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== elevenlabs =====
const elevenlabs = {
  url: 'https://elevenlabs.io/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('$')) return null;
    return {
      pricingEN: {
        input: 'See elevenlabs.io/pricing',
        output: 'See elevenlabs.io/pricing',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== deepgram =====
const deepgram = {
  url: 'https://deepgram.com/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('$')) return null;
    return {
      pricingEN: {
        input: 'See deepgram.com/pricing',
        output: 'See deepgram.com/pricing',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== tavily =====
const tavily = {
  url: 'https://tavily.com/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('$')) return null;
    return {
      pricingEN: {
        input: 'See tavily.com/pricing',
        output: 'See tavily.com/pricing',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== jina =====
const jina = {
  url: 'https://jina.ai/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('$')) return null;
    return {
      pricingEN: {
        input: 'See jina.ai/pricing',
        output: 'See jina.ai/pricing',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== voyage-ai =====
const voyage = {
  url: 'https://voyageai.com/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('$')) return null;
    return {
      pricingEN: {
        input: 'See voyageai.com/pricing',
        output: 'See voyageai.com/pricing',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== perplexity =====
const perplexity = {
  url: 'https://docs.perplexity.ai/guides/pricing',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('$')) return null;
    return {
      pricingEN: {
        input: 'See docs.perplexity.ai pricing',
        output: 'See docs.perplexity.ai pricing',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== x.ai grok =====
const grok = {
  url: 'https://docs.x.ai/docs/models',
  async run(provider, http) {
    const fp = await fetchAndParse(http, this.url);
    if (!fp.text.includes('$')) return null;
    return {
      pricingEN: {
        input: 'See docs.x.ai/docs/models',
        output: 'See docs.x.ai/docs/models',
      },
      sourceUrl: fp.fetchedUrl,
      confidence: 'low',
      _rawExcerpt: fp.tables.slice(0, 2000) || fp.text.slice(0, 2000),
    };
  },
};

// ===== registry =====
const registry = {
  openai, anthropic, deepseek, google, openrouter,
  groq, cohere, mistral, together: together, 'fireworks-ai': fireworks,
  modelscope, siliconflow, aliyun, baidu, bytedance: volcengine,
  zhipu, kimi, huggingface, stability: stability, 'stability-ai': stability,
  elevenlabs, deepgram, tavily, jina: jina, 'jina-ai': jina,
  voyage: voyage, 'voyage-ai': voyage, perplexity, grok: grok,
};

function getExtractor(providerId) {
  return registry[providerId] || null;
}

module.exports = { getExtractor, registry };