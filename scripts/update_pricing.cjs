#!/usr/bin/env node
// scripts/update_pricing.cjs
//
// Fetch the latest pricing for each provider in src/data/providers.json,
// diff against current values, and (by default) write a report.
// With --apply, write the changes back to providers.json, commit, and push.
//
// Usage:
//   node scripts/update_pricing.cjs                  # dry-run, writes report to /tmp/apirank-pricing-report/
//   node scripts/update_pricing.cjs --provider openai   # only one provider
//   node scripts/update_pricing.cjs --apply          # actually overwrite providers.json
//   node scripts/update_pricing.cjs --apply --no-push   # write + commit, but don't push
//   node scripts/update_pricing.cjs --json-only      # skip LLM fallback (faster, less smart)
//   node scripts/update_pricing.cjs --no-llm         # only use structured extractors

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const { fetchText } = require('./lib/http.cjs');
const { stripHtml, extractTables, tablesToText } = require('./lib/html.cjs');
const { getExtractor } = require('./lib/extractors/index.cjs');
const { llmExtractPricing } = require('./lib/llm_extract.cjs');

const REPO = '/root/apirank';
const DATA_FILE = path.join(REPO, 'src/data/providers.json');
const REPORT_DIR = '/tmp/apirank-pricing-report';

// ----- args -----
const args = process.argv.slice(2);
const FLAGS = {
  apply: args.includes('--apply'),
  noPush: args.includes('--no-push'),
  noLlm: args.includes('--no-llm') || args.includes('--json-only'),
  provider: (() => {
    const i = args.indexOf('--provider');
    return i >= 0 ? args[i + 1] : null;
  })(),
  help: args.includes('--help') || args.includes('-h'),
};

if (FLAGS.help) {
  console.log(`Usage: node scripts/update_pricing.cjs [options]

Options:
  --provider <id>      Only update the named provider (e.g. openai)
  --apply              Overwrite providers.json (default: dry-run, write report)
  --no-push            With --apply: commit but don't push to GitHub
  --no-llm             Skip LLM fallback extractor (faster, less smart)
  --json-only          Same as --no-llm
  --help, -h           Show this help

By default the script:
  1. Fetches each provider's pricing page
  2. Runs a structured extractor (or LLM fallback if configured)
  3. Writes /tmp/apirank-pricing-report/report.json + proposed-diff.json
  4. Exits WITHOUT modifying providers.json
`);
  process.exit(0);
}

// ----- helpers -----
function log(...parts) {
  const ts = new Date().toISOString().slice(11, 19);
  console.log(`[${ts}]`, ...parts);
}

function now() {
  return new Date().toISOString();
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function isPlaceholder(s) {
  if (!s) return false;
  return /待确认|TBD|placeholder|model-dependent|Model-dependent/i.test(String(s));
}

// A "change" that contains no actual price number is not a change — it is the
// extractor telling us the page had no pricing table (or was bot-blocked).
// Such results must be skipped, not diffed, otherwise they pollute the report
// and (if ever promoted to high confidence) overwrite good data with a sentence
// like "页面未显示具体价格数字".
function looksLikePrice(s) {
  if (!s) return false;
  const t = String(s);
  if (/[¥$￥]\s*\d/.test(t)) return true;                                  // ¥0.8/M, $10/M
  if (/\d\s*\/\s*(1\s*[mk]\b|million|百万|千)/i.test(t)) return true;      // 0.88/M
  if (/\d+\s*credits?\b/i.test(t)) return true;                            // 1,000 credits
  return false;
}

function hasNumericPricing(extracted) {
  const p = extracted?.pricing || {};
  const pe = extracted?.pricingEN || {};
  return looksLikePrice(p.input) || looksLikePrice(p.output)
    || looksLikePrice(pe.input) || looksLikePrice(pe.output);
}

function pricingChanged(a, b) {
  if (!a || !b) return true;
  const aS = JSON.stringify(a, Object.keys(a).sort());
  const bS = JSON.stringify(b, Object.keys(b).sort());
  return aS !== bS;
}

// ---------------------------------------------------------------------------
// Coverage-preservation guard.
//
// The extractors (and the LLM fallback) summarise a pricing PAGE, they do not
// re-derive the catalog. The LLM prompt caps every field at 200 chars and the
// page slice is only 6KB of text, so a summary legitimately covers fewer
// models than the curated entry it replaces.
//
// "high confidence" from an extractor means "these NUMBERS are right", not
// "this is the complete picture". Applying it verbatim therefore deletes
// curated coverage (model families, cache rates, free-tier notes, GPU hours)
// that the page slice simply did not mention.
//
// Rule: an extraction that would DROP information relative to the current
// curated entry is not auto-appliable. Demote it to the review queue and let
// a human merge the new numbers into the existing entry.
const COVERAGE_MIN_RATIO = 0.75;

const PRICING_NOISE = new Set(`api apis llm llms ai usd cny eur gbp jpy rmb gpu gpus cpu vram faq cta http https json html xml dom pdf url uri id ids ip os ok yes no na gb mb kb tb ms hr mo yr vs and or the mcp saas tee oss mit agpl bsd cc nc pd py js ts css seo mvp ocr rag rl hf nlp sla eula sdk cli ui ux pr qps rps ttl ot cr dr sr fr it es jp kr us uk eu ag sg hk tw my tokens token input output cache cached per million model models price pricing free paid serverless standard batch flex fast long context note rate rates details page full breakdown see also visit site official intro deduction includes including only from this that with and for not all new old latest current about more less than then some`.split(/\s+/));

function normalizeKey(s) {
  return String(s || '').toLowerCase().replace(/[^a-z0-9.]+/g, ' ').replace(/\s+/g, ' ').trim();
}

// Extract a comparable set of model identifiers from a pricing string.
function modelTokens(text) {
  const out = new Set();
  if (!text) return out;
  const s = String(text);
  for (const m of s.matchAll(/\b([A-Za-z][A-Za-z0-9]{1,14})[\s-]?(\d[\w.]*[A-Za-z][\w.]*|\d[\d.]*)\b/g)) {
    out.add(normalizeKey(`${m[1]} ${m[2]}`));
  }
  for (const m of s.matchAll(/\b([A-Za-z][A-Za-z0-9]*(?:[.\-][A-Za-z0-9]+)+)\b/g)) {
    out.add(normalizeKey(m[1]));
  }
  for (const m of s.matchAll(/\b([A-Z]{2,6}\d{0,3}[A-Z]*|[A-Z]\d[\w.\-]*)\b/g)) {
    if (!PRICING_NOISE.has(m[1].toUpperCase())) out.add(normalizeKey(m[1]));
  }
  for (const m of s.matchAll(/\b([A-Z][a-z]{2,}(?: [A-Z][a-z]{2,}){0,2})\b/g)) {
    out.add(normalizeKey(m[1]));
  }
  return out;
}

// Returns an array of human-readable reasons why `after` would lose coverage
// relative to `before`. Empty array = safe to apply.
function coverageLossReasons(before, after) {
  const reasons = [];
  for (const obj of ['pricing', 'pricingEN']) {
    const b = before?.[obj] || {};
    const a = after?.[obj] || {};
    for (const k of Object.keys(b)) {
      if (!String(b[k] ?? '').trim()) continue;
      if (!(k in a)) reasons.push(`${obj}.${k} dropped`);
    }
    for (const k of ['input', 'output']) {
      const bt = b[k];
      const at = a[k];
      if (!bt || !at) continue;
      const bl = String(bt).length;
      const al = String(at).length;
      if (al < bl * COVERAGE_MIN_RATIO) {
        reasons.push(`${obj}.${k} shrank ${bl}->${al} chars`);
      }
      const bm = modelTokens(bt);
      const am = modelTokens(at);
      if (bm.size && am.size && !([...bm].some(t => am.has(t)))) {
        reasons.push(`${obj}.${k} covers a disjoint model set`);
      }
    }
  }
  return reasons;
}

async function fetchAndParse(url, httpCfg) {
  const res = await fetchText(url, httpCfg);
  const text = stripHtml(res.text);
  const tables = tablesToText(extractTables(res.text));
  return { text, tables, fetchedUrl: res.url, bytes: res.bytes };
}

async function updateOne(provider, opts) {
  const result = {
    id: provider.id,
    name: provider.name,
    website: provider.website,
    startedAt: now(),
    status: 'pending',
  };

  // 1. Try structured extractor
  const extractor = getExtractor(provider.id);
  let extracted = null;
  let fetched = null;
  let fetchError = null;

  if (extractor) {
    try {
      const httpCfg = { timeoutMs: 25000, retries: 1 };
      // inject timeoutMs + retries into the http namespace for extractor to read
      const http = httpCfg;
      fetched = await fetchAndParse(extractor.url, httpCfg);
      extracted = await extractor.run(provider, {
        ...http,
        // helpers for extractors that want them:
        fetchText: (url, cfg) => fetchText(url, cfg || httpCfg),
      });
      if (extracted) {
        // strip internal helpers from result
        delete extracted._rawExcerpt;
        delete extracted._stats;
      }
    } catch (e) {
      fetchError = `structured extractor failed: ${e.message}`;
      log(`  [${provider.id}] ${fetchError}`);
    }
  }

  // 2. LLM fallback (if structured returned nothing OR confidence was low AND not --no-llm)
  const needLlm = !FLAGS.noLlm && (
    !extracted
    || extracted.confidence === 'low'
    || (!extracted.pricing && !extracted.pricingEN)
  );

  // Providers with no registered extractor still need a fetch before the LLM
  // fallback can run — otherwise `fetched` is null and the LLM branch is
  // unreachable (this is why 94/109 providers were skipped every week).
  if (needLlm && !fetched) {
    const url = provider.website;
    if (url) {
      log(`  [${provider.id}] fetching ${url} for LLM fallback`);
      try {
        fetched = await fetchAndParse(url, { timeoutMs: 25000, retries: 1 });
      } catch (e) {
        log(`  [${provider.id}] fetch for LLM failed: ${e.message}`);
        fetchError = `fetch failed: ${e.message}`;
      }
    }
  }

  if (needLlm && fetched) {
    log(`  [${provider.id}] → LLM fallback`);
    try {
      const llmResult = await llmExtractPricing({
        provider,
        rawText: fetched.text,
        rawTables: fetched.tables,
        sourceUrl: fetched.fetchedUrl,
        log: (m) => log(`  [${provider.id}] ${m}`),
      });
      if (llmResult) {
        extracted = llmResult;
      }
    } catch (e) {
      log(`  [${provider.id}] LLM fallback error: ${e.message}`);
    }
  } else if (needLlm && !fetched && extractor) {
    // extractor had a hard error — try once more for LLM
    log(`  [${provider.id}] retrying fetch for LLM`);
    try {
      fetched = await fetchAndParse(extractor.url, { timeoutMs: 25000, retries: 1 });
      const llmResult = await llmExtractPricing({
        provider,
        rawText: fetched.text,
        rawTables: fetched.tables,
        sourceUrl: fetched.fetchedUrl,
        log: (m) => log(`  [${provider.id}] ${m}`),
      });
      if (llmResult) extracted = llmResult;
    } catch (e) {
      log(`  [${provider.id}] LLM retry failed: ${e.message}`);
    }
  }

  if (!extracted) {
    result.status = 'skipped';
    result.reason = fetchError || 'no extractor and no LLM result';
    result.finishedAt = now();
    return result;
  }

  // 2b. Guard: a result with no price number in it means the page had no
  // pricing table (or was bot-blocked). Treat it as "no data" instead of a
  // diff — otherwise the report is polluted and a promotion to high
  // confidence would overwrite good pricing with prose.
  if (!hasNumericPricing(extracted)) {
    result.status = 'skipped';
    result.reason = 'no numeric pricing found on page';
    result.confidence = extracted.confidence || 'low';
    result.sourceUrl = extracted.sourceUrl;
    result.notes = extracted.notes || '';
    result.finishedAt = now();
    log(`  → skipped: no numeric pricing found on page`);
    return result;
  }

  // 3. Diff against current
  const beforePricing = provider.pricing || {};
  const beforePricingEN = provider.pricingEN || {};
  const afterPricing = extracted.pricing || {};
  const afterPricingEN = extracted.pricingEN || {};

  const pricingChangedVal = pricingChanged(beforePricing, afterPricing);
  const pricingENChangedVal = !beforePricingEN && afterPricingEN
    ? !!afterPricingEN.input || !!afterPricingEN.output
    : pricingChanged(beforePricingEN, afterPricingEN);

  result.status = 'ok';
  result.confidence = extracted.confidence || 'low';
  result.sourceUrl = extracted.sourceUrl;
  result.before = { pricing: beforePricing, pricingEN: beforePricingEN };
  result.after = { pricing: afterPricing, pricingEN: afterPricingEN };
  result.diff = {
    pricing: pricingChangedVal,
    pricingEN: pricingENChangedVal,
  };
  result.notes = extracted.notes || '';
  result.finishedAt = now();

  // Mark as "would change"
  if (pricingChangedVal || pricingENChangedVal) {
    result.wouldChange = true;
  }

  // 3b. Coverage guard — an extraction that would drop curated information is
  // not auto-appliable, regardless of what the extractor called its confidence.
  // Demote it to the review queue instead of silently deleting coverage.
  if (result.wouldChange) {
    const losses = coverageLossReasons(result.before, result.after);
    if (losses.length) {
      result.coverageLoss = losses;
      result.demoted = true;
      result.confidence = 'low';
      result.notes = `${result.notes ? result.notes + ' | ' : ''}demoted to review: would lose coverage (${losses.join('; ')})`;
      log(`  → demoted to review (would lose coverage): ${losses.join('; ')}`);
    }
  }

  // Flag placeholders
  if (isPlaceholder(beforePricing.input) || isPlaceholder(beforePricing.output)) {
    result.hadPlaceholder = true;
  }

  return result;
}

async function main() {
  ensureDir(REPORT_DIR);

  const providers = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  const targets = FLAGS.provider
    ? providers.filter(p => p.id === FLAGS.provider)
    : providers;

  if (!targets.length) {
    console.error(`No provider matched: ${FLAGS.provider}`);
    process.exit(2);
  }

  log(`Starting pricing update for ${targets.length} providers`);
  log(`Mode: ${FLAGS.apply ? 'APPLY' : 'dry-run'}${FLAGS.noLlm ? ' (no-LLM)' : ''}`);

  const results = [];
  for (const p of targets) {
    log(`[${p.id}] ${p.name} (${p.website})`);
    try {
      const r = await updateOne(p, {});
      results.push(r);
      if (r.status === 'ok') {
        const flag = r.wouldChange ? '✏ would change' : '✓ no change';
        log(`  → ${flag} (confidence: ${r.confidence})`);
      } else {
        log(`  → ${r.status}: ${r.reason || ''}`);
      }
    } catch (e) {
      log(`  ✖ unexpected error: ${e.message}`);
      results.push({
        id: p.id,
        name: p.name,
        status: 'error',
        error: e.message,
        finishedAt: now(),
      });
    }
  }

  // ----- write report -----
  const report = {
    generatedAt: now(),
    mode: FLAGS.apply ? 'apply' : 'dry-run',
    flags: FLAGS,
    summary: {
      total: results.length,
      ok: results.filter(r => r.status === 'ok').length,
      wouldChange: results.filter(r => r.wouldChange).length,
      skipped: results.filter(r => r.status === 'skipped').length,
      errors: results.filter(r => r.status === 'error').length,
      demoted: results.filter(r => r.demoted).length,
      autoApplicable: results.filter(r => r.wouldChange && r.confidence === 'high').length,
    },
    results,
  };

  fs.writeFileSync(path.join(REPORT_DIR, 'report.json'), JSON.stringify(report, null, 2));
  log(`Report: ${REPORT_DIR}/report.json`);

  // Proposed diff (only entries that would change)
  const proposedDiff = {
    generatedAt: now(),
    entries: results
      .filter(r => r.wouldChange)
      .map(r => ({
        id: r.id,
        name: r.name,
        confidence: r.confidence,
        sourceUrl: r.sourceUrl,
        before: r.before,
        after: r.after,
        notes: r.notes,
        demoted: !!r.demoted,
        coverageLoss: r.coverageLoss || null,
      })),
  };
  fs.writeFileSync(path.join(REPORT_DIR, 'proposed-diff.json'), JSON.stringify(proposedDiff, null, 2));
  log(`Diff: ${REPORT_DIR}/proposed-diff.json (${proposedDiff.entries.length} changes)`);

  // ----- apply? -----
  if (FLAGS.apply) {
    // Only auto-apply entries that the extractor itself marked as high-confidence.
    // Low/medium confidence changes are written to a separate "review queue"
    // so a human can vet them before they go live.
    const highConf = proposedDiff.entries.filter(e => e.confidence === 'high');
    const lowConf = proposedDiff.entries.filter(e => e.confidence !== 'high');

    const reviewQueue = {
      generatedAt: now(),
      note: 'These entries have low/medium extractor confidence, or were demoted because applying them would drop curated coverage. Review the raw excerpts in report.json before manually merging into providers.json.',
      entries: results
        .filter(r => r.wouldChange && r.confidence !== 'high')
        .map(r => ({
          id: r.id, name: r.name, confidence: r.confidence,
          sourceUrl: r.sourceUrl,
          demoted: !!r.demoted,
          coverageLoss: r.coverageLoss || null,
          before: r.before, after: r.after, notes: r.notes,
        })),
    };
    fs.writeFileSync(path.join(REPORT_DIR, 'review-queue.json'), JSON.stringify(reviewQueue, null, 2));

    if (!highConf.length) {
      log('No high-confidence changes to apply.');
      if (lowConf.length) {
        log(`${lowConf.length} low-confidence changes queued for manual review at ${REPORT_DIR}/review-queue.json`);
      }
    } else {
      log(`Applying ${highConf.length} high-confidence changes to ${DATA_FILE}...`);
      const updated = providers.map(p => {
        const change = highConf.find(e => e.id === p.id);
        if (!change) return p;
        const next = { ...p };
        // Merge sub-keys instead of replacing the whole object: an extraction
        // that only produced `input`/`output` must not delete curated
        // `cacheRead` / `freeTier` / `unit` siblings.
        for (const objKey of ['pricing', 'pricingEN']) {
          const after = change.after?.[objKey];
          if (!after || !Object.keys(after).length) continue;
          const before = p[objKey] || {};
          const merged = { ...before, ...after };
          next[objKey] = merged;
        }
        return next;
      });

      // Backup
      const backup = DATA_FILE + '.bak.' + Date.now();
      fs.copyFileSync(DATA_FILE, backup);
      log(`Backup: ${backup}`);

      fs.writeFileSync(DATA_FILE, JSON.stringify(updated, null, 2) + '\n');
      log(`Wrote ${DATA_FILE}`);

      // git commit + push
      try {
        execSync(`git add src/data/providers.json`, { cwd: REPO });
        execSync(
          `git commit -m "chore(pricing): update from official sources [skip ci]\\n\\nApplied ${highConf.length} high-confidence changes (${lowConf.length} queued for manual review)\\nReport: ${REPORT_DIR}/report.json"`,
          { cwd: REPO, stdio: 'inherit' },
        );
        log('Committed.');
        if (!FLAGS.noPush) {
          execSync(`git push origin main`, { cwd: REPO, stdio: 'inherit' });
          log('Pushed.');
        } else {
          log('Skipped push (--no-push).');
        }
      } catch (e) {
        log(`⚠ git operation failed: ${e.message}`);
        log('File is updated on disk. Commit/push manually if needed.');
        process.exit(3);
      }
    }
  } else {
    log('Dry-run complete. To apply, re-run with --apply (only high-confidence changes will be applied).');
  }

  // ----- summary table -----
  console.log('\n=== SUMMARY ===');
  console.log(`Total: ${report.summary.total}`);
  console.log(`OK: ${report.summary.ok}`);
  console.log(`Would change: ${report.summary.wouldChange}`);
  console.log(`  - auto-applicable (high confidence): ${report.summary.autoApplicable}`);
  console.log(`  - demoted to review (coverage loss): ${report.summary.demoted}`);
  console.log(`Skipped: ${report.summary.skipped}`);
  console.log(`Errors: ${report.summary.errors}`);
  console.log('');
  console.log('Per-provider results:');
  for (const r of results) {
    const tag = r.demoted ? '⚠' : (r.wouldChange ? '✏' : (r.status === 'ok' ? '✓' : (r.status === 'skipped' ? '–' : '✖')));
    console.log(`  ${tag} ${r.id.padEnd(22)} ${r.status.padEnd(8)} ${r.confidence || ''} ${r.notes || ''}`);
  }
}

main().catch(e => {
  console.error('FATAL:', e);
  process.exit(1);
});