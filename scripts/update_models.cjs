#!/usr/bin/env node
// scripts/update_models.cjs
//
// Fetch the latest model pricing/specs from official provider sources,
// diff against src/data/models.json, and (by default) write a report.
// With --apply, write the changes back to models.json + pricing-meta.json,
// commit, and push (triggers CF Pages auto-deploy).
//
// Usage:
//   node scripts/update_models.cjs                  # dry-run, writes report to /tmp/apirank-models-report/
//   node scripts/update_models.cjs --apply          # actually overwrite models.json
//   node scripts/update_models.cjs --apply --no-push  # write + commit, but don't push
//   node scripts/update_models.cjs --no-llm         # skip LLM fallback (faster, less smart)
//
// Differences vs update_pricing.cjs:
// - Operates on src/data/models.json (per-model data, not per-provider)
// - Tracks per-field changes (input/output/cache/context/releaseDate/capabilities)
// - Bumps pricing-meta.json lastVerified on apply
// - Updates `note` and `noteZh` only when LLM confidence is high (manual review otherwise)

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const { fetchText } = require('./lib/http.cjs');
const { stripHtml, extractTables, tablesToText } = require('./lib/html.cjs');
const { getExtractor } = require('./lib/extractors/index.cjs');
const { llmExtractPricing } = require('./lib/llm_extract.cjs');

const REPO = '/root/apirank';
const MODELS_FILE = path.join(REPO, 'src/data/models.json');
const META_FILE = path.join(REPO, 'src/data/pricing-meta.json');
const REPORT_DIR = '/tmp/apirank-models-report';

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
  console.log(`Usage: node scripts/update_models.cjs [options]

Options:
  --apply              Overwrite models.json (default: dry-run, write report)
  --no-push            With --apply: commit but don't push to GitHub
  --no-llm             Skip LLM fallback extractor (faster, less smart)
  --json-only          Same as --no-llm

Notes:
- Operates per-model in src/data/models.json, joined to providers via providerId.
- LLM is only used as fallback when structured extractor returns nothing.
- onlyHighConf pricing changes are applied automatically; low/medium go to queue.`);
  process.exit(0);
}

// ----- helpers -----
function log(msg) { console.log(`[${now()}] ${msg}`); }
function now() { return new Date().toISOString().slice(11, 19); }
function ensureDir(d) { if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true }); }

function isPlaceholder(v) {
  if (v == null || v === '') return true;
  if (typeof v === 'string' && (v.includes('unknown') || v.includes('TODO') || v.length < 3)) return true;
  return false;
}

function pricingChanged(a, b) {
  if (!a || !b) return false;
  for (const k of ['input', 'output', 'cache']) {
    const av = Number(a[k]);
    const bv = Number(b[k]);
    if (Number.isFinite(av) && Number.isFinite(bv) && Math.abs(av - bv) > 1e-9) return true;
  }
  return false;
}

function diffModels(oldModel, newModel) {
  // Compare key fields. Returns array of {field, oldValue, newValue} entries.
  const diffs = [];
  const fields = ['name', 'nameZh', 'tier', 'tierZh', 'contextWindow', 'releaseDate'];
  for (const f of fields) {
    if (oldModel[f] !== newModel[f] && !isPlaceholder(newModel[f])) {
      diffs.push({ field: f, oldValue: oldModel[f], newValue: newModel[f] });
    }
  }
  // Pricing subfields
  if (pricingChanged(oldModel.pricing, newModel.pricing)) {
    for (const k of ['input', 'output', 'cache']) {
      if (Math.abs(Number(oldModel.pricing[k]) - Number(newModel.pricing[k])) > 1e-9) {
        diffs.push({
          field: `pricing.${k}`,
          oldValue: oldModel.pricing[k],
          newValue: newModel.pricing[k],
        });
      }
    }
  }
  // Capabilities
  const oldCaps = (oldModel.capabilities || []).slice().sort().join(',');
  const newCaps = (newModel.capabilities || []).slice().sort().join(',');
  if (oldCaps !== newCaps && newModel.capabilities && newModel.capabilities.length > 0) {
    diffs.push({
      field: 'capabilities',
      oldValue: oldModel.capabilities || [],
      newValue: newModel.capabilities,
    });
  }
  // availabilityCN
  if (oldModel.availabilityCN !== newModel.availabilityCN && !isPlaceholder(newModel.availabilityCN)) {
    diffs.push({
      field: 'availabilityCN',
      oldValue: oldModel.availabilityCN,
      newValue: newModel.availabilityCN,
    });
  }
  // Note fields — only update on high confidence (already gated upstream)
  for (const f of ['note', 'noteZh']) {
    if (oldModel[f] !== newModel[f] && newModel[f] && newModel[f].length > 20) {
      diffs.push({ field: f, oldValue: oldModel[f], newValue: newModel[f] });
    }
  }
  return diffs;
}

// Models-by-provider cache, loaded once.
function loadModels() {
  const raw = fs.readFileSync(MODELS_FILE, 'utf8');
  return JSON.parse(raw);
}

function saveModels(data) {
  fs.writeFileSync(MODELS_FILE, JSON.stringify(data, null, 2) + '\n');
}

function bumpMeta(date) {
  if (!fs.existsSync(META_FILE)) return;
  const meta = JSON.parse(fs.readFileSync(META_FILE, 'utf8'));
  meta.lastVerified = date;
  meta.lastVerifiedDisplay = formatDateDisplay(date, 'en');
  meta.lastVerifiedZh = formatDateDisplay(date, 'zh');
  fs.writeFileSync(META_FILE, JSON.stringify(meta, null, 2) + '\n');
}

function formatDateDisplay(iso, lang) {
  // iso = '2026-08-01'
  const [y, m, d] = iso.split('-');
  const monthsEn = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const monthIdx = parseInt(m, 10) - 1;
  if (lang === 'zh') return `${y}年${parseInt(m, 10)}月${parseInt(d, 10)}日`;
  return `${monthsEn[monthIdx]} ${parseInt(d, 10)}, ${y}`;
}

// ----- per-model update -----
async function updateOne(model, provider, http) {
  const extractor = getExtractor(provider.id);
  let newData = null;

  if (extractor) {
    log(`  → extractor for ${provider.id} on ${model.id}`);
    try {
      newData = await extractor.run(provider, http);
    } catch (e) {
      log(`  ⚠ extractor error: ${e.message}`);
    }
  }

  // Fallback: LLM-based extraction on the model-specific URL
  if (!newData && !FLAGS.noLlm) {
    log(`  → LLM fallback for ${model.id} (source: ${model.officialUrl})`);
    try {
      const fp = await fetchAndParse(http, model.officialUrl);
      newData = await llmExtractPricing({
        provider,
        rawText: fp.text,
        rawTables: fp.tables,
        sourceUrl: fp.fetchedUrl,
        log,
      });
    } catch (e) {
      log(`  ⚠ LLM fallback error: ${e.message}`);
    }
  }

  if (!newData) {
    return { model, diffs: [], status: 'no-data', confidence: null };
  }

  // If extractor returned provider-level data only (e.g. {pricingEN: {...}}), merge with model
  const candidate = { ...model };
  if (newData.pricing) candidate.pricing = { ...candidate.pricing, ...newData.pricing };
  if (newData.contextWindow && !isPlaceholder(newData.contextWindow)) candidate.contextWindow = newData.contextWindow;
  if (newData.capabilities && newData.capabilities.length > 0) candidate.capabilities = newData.capabilities;
  if (newData.availabilityCN && !isPlaceholder(newData.availabilityCN)) candidate.availabilityCN = newData.availabilityCN;
  if (newData.releaseDate && newData.releaseDate !== 'unknown') candidate.releaseDate = newData.releaseDate;
  // Only update notes if explicit
  if (newData.note && newData.note.length > 20) candidate.note = newData.note;
  if (newData.noteZh && newData.noteZh.length > 10) candidate.noteZh = newData.noteZh;

  const diffs = diffModels(model, candidate);
  return {
    model,
    candidate,
    diffs,
    status: diffs.length > 0 ? 'changed' : 'unchanged',
    confidence: newData.confidence || 'medium',
    sourceUrl: newData.sourceUrl || model.officialUrl,
  };
}

// Same fetch-and-parse helper as extractors use
async function fetchAndParse(http, url) {
  const res = await fetchText(url, { timeoutMs: http.timeoutMs, retries: http.retries });
  const text = stripHtml(res.text);
  const tables = tablesToText(extractTables(res.text));
  return { text, tables, fetchedUrl: res.url, bytes: res.bytes };
}

// ----- main -----
async function main() {
  ensureDir(REPORT_DIR);
  const http = { timeoutMs: 25000, retries: 1 };

  log(`Loading models from ${MODELS_FILE}`);
  const modelsData = loadModels();
  const models = modelsData.models;
  log(`Loaded ${models.length} models`);

  // Load providers for joining
  const providersPath = path.join(REPO, 'src/data/providers.json');
  const providers = JSON.parse(fs.readFileSync(providersPath, 'utf8'));
  const providerMap = {};
  for (const p of providers) providerMap[p.id] = p;

  const results = [];
  for (const m of models) {
    if (FLAGS.provider && m.providerId !== FLAGS.provider) {
      // Skip models outside the requested provider filter
      continue;
    }
    const provider = providerMap[m.providerId];
    if (!provider) {
      log(`  ✗ ${m.id}: providerId='${m.providerId}' not in providers.json — SKIP`);
      results.push({ modelId: m.id, status: 'orphan', diffs: [] });
      continue;
    }
    log(`Checking ${m.id} (${m.provider})...`);
    try {
      const r = await updateOne(m, provider, http);
      results.push({
        modelId: m.id,
        providerId: m.providerId,
        status: r.status,
        confidence: r.confidence,
        diffs: r.diffs,
        sourceUrl: r.sourceUrl,
        candidate: r.candidate,
      });
      if (r.diffs.length > 0) {
        log(`  ✓ ${r.status} (${r.confidence}): ${r.diffs.length} field(s) — ${r.diffs.map(d => d.field).join(', ')}`);
      } else {
        log(`  · ${r.status}`);
      }
    } catch (e) {
      log(`  ✗ error: ${e.message}`);
      results.push({ modelId: m.id, status: 'error', error: e.message, diffs: [] });
    }
  }

  // ----- summarize -----
  const changed = results.filter(r => r.diffs.length > 0);
  const highConf = changed.filter(r => r.confidence === 'high');
  const medLowConf = changed.filter(r => r.confidence !== 'high');

  const summary = {
    timestamp: new Date().toISOString(),
    total: models.length,
    checked: results.filter(r => r.status !== 'orphan').length,
    orphans: results.filter(r => r.status === 'orphan').length,
    unchanged: results.filter(r => r.status === 'unchanged').length,
    noData: results.filter(r => r.status === 'no-data').length,
    changed: changed.length,
    highConfidence: highConf.length,
    mediumLowConfidence: medLowConf.length,
  };

  const report = { summary, results };
  fs.writeFileSync(path.join(REPORT_DIR, 'report.json'), JSON.stringify(report, null, 2));
  log(`Report → ${REPORT_DIR}/report.json`);

  // ----- apply if --apply -----
  if (FLAGS.apply && changed.length > 0) {
    log(`Applying ${highConf.length} high-confidence changes (${medLowConf.length} queued for manual review)`);

    if (highConf.length === 0) {
      log('No high-confidence changes to apply. Skipping write.');
    } else {
      // Backup
      const backup = `${MODELS_FILE}.bak.${Date.now()}`;
      fs.copyFileSync(MODELS_FILE, backup);
      log(`Backup: ${backup}`);

      // Apply each change to the in-memory data
      for (const r of highConf) {
        const idx = modelsData.models.findIndex(m => m.id === r.modelId);
        if (idx >= 0 && r.candidate) {
          modelsData.models[idx] = r.candidate;
        }
      }

      // Update lastVerified
      const today = new Date().toISOString().slice(0, 10);
      modelsData.lastVerified = today;

      saveModels(modelsData);
      bumpMeta(today);
      log(`Wrote ${MODELS_FILE} + ${META_FILE}`);

      // git commit + push
      try {
        execSync(`git add src/data/models.json src/data/pricing-meta.json`, { cwd: REPO });
        execSync(
          `git commit -m "chore(models): update from official sources [skip ci]\\n\\nApplied ${highConf.length} high-confidence changes (${medLowConf.length} queued)\\nReport: ${REPORT_DIR}/report.json"`,
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
  } else if (FLAGS.apply) {
    log('No changes detected; --apply skipped (no write).');
  } else {
    log('Dry-run complete. To apply, re-run with --apply (only high-confidence changes will be applied).');
  }

  // ----- summary table -----
  console.log('\n=== SUMMARY ===');
  console.log(`Total: ${summary.total}`);
  console.log(`Checked: ${summary.checked}`);
  console.log(`Orphans (providerId mismatch): ${summary.orphans}`);
  console.log(`Unchanged: ${summary.unchanged}`);
  console.log(`No data fetched: ${summary.noData}`);
  console.log(`Changed: ${summary.changed}`);
  console.log(`  - high-confidence (auto-apply): ${summary.highConfidence}`);
  console.log(`  - medium/low-confidence (manual review): ${summary.mediumLowConfidence}`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});