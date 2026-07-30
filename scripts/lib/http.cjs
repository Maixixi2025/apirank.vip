// scripts/lib/http.js
// Lightweight HTTP fetcher with timeout + retries.
// Native fetch (Node 22) — no extra deps.

const DEFAULT_TIMEOUT_MS = 20000;
const DEFAULT_RETRIES = 1;
const USER_AGENT =
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
  'Chrome/124.0 Safari/537.36 apirank-pricing-bot';

async function fetchText(url, { timeoutMs = DEFAULT_TIMEOUT_MS, retries = DEFAULT_RETRIES } = {}) {
  let lastErr;
  for (let attempt = 0; attempt <= retries; attempt++) {
    const controller = new AbortController();
    const t = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const res = await fetch(url, {
        signal: controller.signal,
        redirect: 'follow',
        headers: {
          'User-Agent': USER_AGENT,
          'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
        },
      });
      clearTimeout(t);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status} ${res.statusText} for ${url}`);
      }
      const text = await res.text();
      return { url: res.url, status: res.status, text, bytes: text.length };
    } catch (e) {
      clearTimeout(t);
      lastErr = e;
      if (attempt < retries) {
        await new Promise(r => setTimeout(r, 800 * (attempt + 1)));
      }
    }
  }
  throw lastErr;
}

module.exports = { fetchText, USER_AGENT };