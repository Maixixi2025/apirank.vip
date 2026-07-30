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

function pricingChanged(a, b) {
  if (!a || !b) return true;
  const aS = JSON.stringify(a, Object.keys(a).sort());
  const bS = JSON.stringify(b, Object.keys(b).sort());
  return aS !== bS;
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
      note: 'These entries have low/medium extractor confidence. Review the raw excerpts in report.json before manually merging into providers.json.',
      entries: results
        .filter(r => r.wouldChange && r.confidence !== 'high')
        .map(r => ({
          id: r.id, name: r.name, confidence: r.confidence,
          sourceUrl: r.sourceUrl,
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
        if (change.after.pricing && Object.keys(change.after.pricing).length) {
          next.pricing = change.after.pricing;
        }
        if (change.after.pricingEN && Object.keys(change.after.pricingEN).length) {
          next.pricingEN = change.after.pricingEN;
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
  console.log(`Skipped: ${report.summary.skipped}`);
  console.log(`Errors: ${report.summary.errors}`);
  console.log('');
  console.log('Per-provider results:');
  for (const r of results) {
    const tag = r.wouldChange ? '✏' : (r.status === 'ok' ? '✓' : (r.status === 'skipped' ? '–' : '✖'));
    console.log(`  ${tag} ${r.id.padEnd(22)} ${r.status.padEnd(8)} ${r.confidence || ''} ${r.notes || ''}`);
  }
}

main().catch(e => {
  console.error('FATAL:', e);
  process.exit(1);
});