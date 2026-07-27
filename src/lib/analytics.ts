/**
 * Central analytics event bus — A-09.
 *
 * Goals (PRD §6.1, §11):
 *   - Single API for all events: track('calculator_start', { model_id })
 *   - Multiple sinks can be enabled independently:
 *     - console.debug during development
 *     - window.dataLayer.push when GTM is loaded
 *     - gtag('event', ...) when GA4 is loaded
 *   - Adding a real GA4 measurement ID later is a 1-line change in baseLayout.
 *
 * Naming: snake_case, action-first (calculator_start, cta_click, outbound_click).
 *
 * Safe to import from any .astro frontmatter or inline <script>; the runtime
 * API lives on window.__analytics so client code can call track() without
 * importing this module.
 */

export type AnalyticsEvent =
  | 'calculator_start'        // user opens calculator page
  | 'calculator_complete'     // user triggers a recompute (input change debounced)
  | 'calculator_share'        // user copies share URL (PRD A-02)
  | 'compare_view'            // user opens a /compare/ page
  | 'cta_click'               // any CTA button clicked
  | 'outbound_click'          // link to a provider's external site
  | 'model_select'            // user picked a model from the dropdown
  | 'affiliate_disclosure_view'; // user saw the affiliate footer

export interface AnalyticsPayload {
  [key: string]: string | number | boolean | undefined | null;
}

declare global {
  interface Window {
    __analytics?: {
      track: (event: AnalyticsEvent, params?: AnalyticsPayload) => void;
    };
    dataLayer?: Array<unknown>;
    gtag?: (...args: unknown[]) => void;
  }
}

/**
 * Internal sink dispatcher. Idempotent — re-attaching a sink is a no-op.
 * Sinks are tried in order; the first throw is caught and logged.
 */
function dispatch(event: AnalyticsEvent, params?: AnalyticsPayload): void {
  const enriched = {
    event,
    ts: Date.now(),
    path: typeof window !== 'undefined' ? window.location.pathname : '',
    locale: typeof document !== 'undefined'
      ? (document.documentElement.lang === 'zh-CN' ? 'zh' : 'en')
      : 'en',
    ...params,
  };

  // 1. Dev console — always on, easy local debugging
  if (typeof console !== 'undefined') {
    // eslint-disable-next-line no-console
    console.debug('[analytics]', enriched);
  }

  // 2. GTM dataLayer — works automatically when GTM is loaded on the page.
  //    We only push if dataLayer is already initialized by the GTM snippet.
  try {
    if (Array.isArray(window.dataLayer)) {
      window.dataLayer.push(enriched);
    }
  } catch (e) {
    // eslint-disable-next-line no-console
    console.warn('[analytics] dataLayer push failed', e);
  }

  // 3. GA4 gtag — works automatically when GA4 is loaded.
  //    Signature: gtag('event', name, params)
  try {
    if (typeof window.gtag === 'function') {
      window.gtag('event', event, params ?? {});
    }
  } catch (e) {
    // eslint-disable-next-line no-console
    console.warn('[analytics] gtag call failed', e);
  }
}

/**
 * The track() function exposed to client code. Always safe to call —
 * does nothing in SSR (no `window`) and degrades gracefully when no sink
 * is configured.
 */
export function track(event: AnalyticsEvent, params?: AnalyticsPayload): void {
  if (typeof window === 'undefined') return;
  dispatch(event, params);
}

/**
 * Install the public window.__analytics binding. Call once per page,
 * typically from BaseLayout's <script>. Idempotent — second call is a no-op.
 */
export function installAnalytics(): void {
  if (typeof window === 'undefined') return;
  if (window.__analytics) return;
  window.__analytics = { track };
}

/**
 * Auto-install on module load. Page scripts just import this module and
 * start calling window.__analytics.track(...) — no manual init needed.
 */
if (typeof window !== 'undefined') {
  installAnalytics();
}