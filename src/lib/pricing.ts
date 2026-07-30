// Pricing data types and helpers — single source of truth for model pricing.
// Source data: src/data/models.json (lastVerified, currency, unit)
// Source data: src/data/pricing-meta.json (sources, fxNote, disclosure)
//
// PRD §11: "所有金额统一为 Decimal 类型，禁止浮点误差；支持美元与人民币换算。"
// Implementation: store as numbers per 1M tokens (USD). For monthly calc we
// convert to integer cents internally to avoid float drift on summation.

export type Tier = 'frontier' | 'mid' | 'budget';

export type AvailabilityCN = 'direct' | 'blocked' | 'proxy_required';

export interface ModelPricing {
  /** USD per 1M input tokens */
  input: number;
  /** USD per 1M output tokens */
  output: number;
  /** USD per 1M cache-read tokens. 0 means cache not supported. */
  cache: number;
}

export interface Model {
  id: string;
  name: string;
  nameZh: string;
  provider: string;
  providerZh: string;
  /** Matches `id` field in src/data/providers.json so we can join later. */
  providerId: string;
  tier: Tier;
  tierZh: string;
  pricing: ModelPricing;
  contextWindow: number;
  capabilities: string[];
  note: string;
  noteZh: string;
  availabilityCN: AvailabilityCN;
  officialUrl: string;
}

export interface ModelsData {
  lastVerified: string;
  currency: 'USD';
  unit: 'per_1M_tokens';
  fxNote: string;
  models: Model[];
}

export interface PricingSource {
  id: string;
  label: string;
  url: string;
  verifiedAt: string;
}

export interface PricingMeta {
  lastVerified: string;
  lastVerifiedDisplay: string;
  lastVerifiedZh: string;
  verificationCycleDays: number;
  coveragePct: number;
  sources: PricingSource[];
  changeLog30d: number;
  disclosure: { en: string; zh: string };
  fxNote: {
    rate: string;
    rateAsOf: string;
    en: string;
    zh: string;
  };
}

import modelsRaw from '../data/models.json';
import pricingMetaRaw from '../data/pricing-meta.json';

export const modelsData = modelsRaw as ModelsData;
export const pricingMeta = pricingMetaRaw as PricingMeta;

/**
 * Round to N decimals using integer math to avoid IEEE-754 drift on summation.
 * Used for any user-visible price output.
 */
export function roundTo(value: number, decimals = 2): number {
  const factor = Math.pow(10, decimals);
  return Math.round(value * factor) / factor;
}

/**
 * Format USD per 1M tokens: "$1.25 / 1M" or "—" for 0.
 */
export function formatPrice(usdPer1M: number, currency: 'USD' | 'CNY' = 'USD'): string {
  if (!usdPer1M && currency === 'USD') return '—';
  const rate = currency === 'CNY' ? 7 : 1;
  const converted = usdPer1M * rate;
  const symbol = currency === 'USD' ? '$' : '¥';
  // CNY gets no decimals for sub-yuan amounts, USD always 2 decimals
  if (currency === 'CNY' && converted < 1) return `${symbol}${(converted).toFixed(2)}`;
  return `${symbol}${roundTo(converted, converted >= 10 ? 2 : 3)}`;
}

/**
 * Compute monthly cost in cents (integer) to avoid float drift when summing
 * across multiple line items. Returns { cents, currency }.
 */
export function monthlyCostCents(
  model: Model,
  usage: {
    dailyCalls: number;
    inputSharePct: number;       // 0-100
    avgTokensPerCall: number;    // prompt + completion combined
    cacheHitRatePct: number;     // 0-90 (PRD allows up to 90% realistic max)
    daysPerMonth?: number;       // default 30
  }
): number {
  const days = usage.daysPerMonth ?? 30;
  const totalCalls = usage.dailyCalls * days;
  const totalTokens = totalCalls * usage.avgTokensPerCall;
  const inputTokens = totalTokens * (usage.inputSharePct / 100);
  const outputTokens = totalTokens * (1 - usage.inputSharePct / 100);
  const cachedTokens = inputTokens * (usage.cacheHitRatePct / 100);
  const freshInputTokens = inputTokens - cachedTokens;

  // Each term is tokens / 1e6 * price_per_1M, summed in dollars then → cents.
  const usd =
    (freshInputTokens / 1e6) * model.pricing.input +
    (cachedTokens / 1e6) * model.pricing.cache +
    (outputTokens / 1e6) * model.pricing.output;

  return Math.round(usd * 100);
}

/** Convert cents → display string. */
export function formatCents(cents: number, currency: 'USD' | 'CNY' = 'USD'): string {
  const rate = currency === 'CNY' ? 7 : 1;
  const units = cents / 100 * rate;
  const symbol = currency === 'USD' ? '$' : '¥';
  if (units < 0.01) return `${symbol}0.00`;
  if (units < 1) return `${symbol}${units.toFixed(2)}`;
  if (units < 100) return `${symbol}${units.toFixed(2)}`;
  return `${symbol}${Math.round(units).toLocaleString()}`;
}

/**
 * Find model by id; returns undefined if not found.
 */
export function findModel(id: string): Model | undefined {
  return modelsData.models.find((m) => m.id === id);
}

/**
 * Group models by tier, in canonical order.
 */
export function groupByTier(models: Model[] = modelsData.models): Record<Tier, Model[]> {
  const groups: Record<Tier, Model[]> = { frontier: [], mid: [], budget: [] };
  for (const m of models) groups[m.tier].push(m);
  return groups;
}

/**
 * Stale check: returns true if lastVerified is older than verificationCycleDays.
 * Use for header warning banners — page is still safe to show.
 */
export function isStale(now: Date = new Date()): boolean {
  const last = new Date(modelsData.lastVerified);
  const ageDays = (now.getTime() - last.getTime()) / (1000 * 60 * 60 * 24);
  return ageDays > pricingMeta.verificationCycleDays;
}

/**
 * Stale age in days, for "X days ago" UI.
 */
export function ageInDays(now: Date = new Date()): number {
  const last = new Date(modelsData.lastVerified);
  return Math.floor((now.getTime() - last.getTime()) / (1000 * 60 * 60 * 24));
}

/**
 * Localized "Last verified" label.
 */
export function lastVerifiedLabel(locale: 'en' | 'zh'): string {
  return locale === 'zh'
    ? `最后核验：${pricingMeta.lastVerifiedZh}`
    : `Last verified: ${pricingMeta.lastVerifiedDisplay}`;
}