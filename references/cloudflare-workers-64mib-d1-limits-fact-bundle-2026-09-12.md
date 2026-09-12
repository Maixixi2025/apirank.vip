# Cloudflare Workers 64 MiB size limit + D1 free-tier hard limits — verified fact bundle

Captured 2026-09-12 (apirank daily-article run `aa24405635c9`).
Article: `cloudflare-workers-64mib-size-limit-ai-api-2026` (EN+ZH).

All facts verified from primary sources at capture time. Re-verify pricing/limits
quarterly — Cloudflare re-tiers these on a short cadence.

## Sources (primary, fetched successfully)

| Fact | Source URL | Notes |
|---|---|---|
| Worker size limit change | `https://developers.cloudflare.com/changelog/post/2026-09-04-increased-worker-size-limit/` | Page date: September 4, 2026 |
| D1 free-tier enforcement | `https://developers.cloudflare.com/changelog/post/2026-09-01-d1-free-tier-limit-enforcement/` | Page date: September 1, 2026 |
| Worker plan limits table | `https://developers.cloudflare.com/workers/platform/limits/index.md` | `.md` mirror worked |
| D1 billing metrics | `https://developers.cloudflare.com/d1/platform/pricing/index.md` | `.md` mirror worked |
| Workers pricing | `https://developers.cloudflare.com/workers/platform/pricing/index.md` | Workers Paid $5/min per account |

**Extraction trick:** CF docs expose clean `.md` mirrors by appending `index.md` to
any docs/changelog URL (also advertised via `<link rel="alternate" type="text/markdown">`).
Prefer these over HTML scraping — no nav/theme boilerplate.

## Fact table — Worker size

| Plan | Old limit | Old measured value | New limit | New measured value |
|---|---|---|---|---|
| Workers Free | 3 MB | compressed | 64 MiB | uncompressed |
| Workers Paid | 10 MB | compressed | 64 MiB | uncompressed |

- Verbatim: *"The compressed Worker size limits (3 MB free / 10 MB paid) have been removed.
  Cloudflare now only checks the uncompressed bundle size, which is 64 MiB across all plans."*
- Wrangler still prints the gzip figure; it is **informational only**, no longer gates deploys.
- Check command: `wrangler deploy --outdir bundled/ --dry-run`
- Sample output: `Total Upload: 259.61 KiB / gzip: 47.23 KiB` → **Total Upload** is the
  value counted against 64 MiB.
- 64 MiB is binary (2^20 bytes/ MiB). Counts the **entire** bundle incl. inlined deps.

## Fact table — Worker account plan limits (unchanged by the size change)

| Feature | Workers Free | Workers Paid |
|---|---|---|
| Requests | 100,000/day | No limit |
| CPU time | 10 ms | 5 min |
| Memory | 128 MB | 128 MB |
| Subrequests | 50/request | 10,000/request |
| Simultaneous outgoing connections/request | 6 | 6 |
| Environment variables | 64/Worker | 128/Worker |
| Environment variable size | 5 KB | 5 KB |
| **Worker size** | **64 MiB** | **64 MiB** |
| Worker startup time | 1 second | 1 second |
| Number of Workers | 100 | 500 |
| Cron Triggers per account | 5 | 250 |
| Static Asset files per Worker version | 20,000 | 100,000 |
| Individual Static Asset file size | 25 MiB | 25 MiB |

⚠️ **Key editorial point:** memory (128 MB), CPU time (10 ms), subrequests (50), and
startup time (1 s) are all unchanged. Free and Paid are now equal ONLY on size.
Upload capacity ≠ run capacity — a large Free-plan bundle can upload and still fail
on CPU/memory.

## Fact table — D1 free-tier hard limits (effective 2026-09-01)

| Metric | Workers Free | Workers Paid |
|---|---|---|
| Rows read | 5,000,000 / day | First 25 billion / month incl. + $0.001 / million rows |
| Rows written | 100,000 / day | First 50 million / month incl. + $1.00 / million rows |
| Storage | 5 GB total | First 5 GB incl. + $0.75 / GB-month |

- Read:write ratio = **50:1** — write-heavy workloads fail first.
- Row reads counted per row **examined**, not returned → full table scan on a 1M-row
  table = 1M rows of budget ≈ **5 requests** on the free tier.
- Behaviour: queries via Workers Binding API and REST API **fail and return errors**
  until reset at **midnight UTC**. Stored data NOT affected.
- Email alerts sent when daily limit is reached.
- Upgrade path: Workers Paid ($5/min per account).
- Recommended mitigation (CF docs): add indexes to tables, review queries doing
  full table scans, check row metrics via meta object / GraphQL Analytics API /
  dashboard Metrics → Row Metrics.

### Error strings (exact, for routing/monitoring)

```
Your account has exceeded D1's free tier daily row read limit. Upgrade to a paid plan or wait until tomorrow (midnight UTC) to continue.
```
```
Your account has exceeded D1's free tier daily row write limit. Upgrade to a paid plan or wait until tomorrow (midnight UTC) to continue.
```

## Editorial frame used (reusable)

The two changes are a **trade**: Cloudflare relaxed what you can put *into* a Worker
and tightened what you can cheaply do at *runtime*. Article body:
1. What changed (size) + verify recipe
2. AI-specific bundling workarounds now unnecessary (R2-hosted catalogues,
   multi-Worker splits, vendored SDK forks) — with the honest caveat that some
   splits/forks had non-size reasons and should stay
3. What did NOT change (memory/CPU/subrequests/startup)
4. D1 hard limits + the 50:1 asymmetry + the per-scan cost math
5. The audit that replaces the workarounds

## Deepening-family classification

**Family (f) engine/platform-format-change**, applied at the **deployment-platform
layer** rather than the AI-model layer. Discriminator tokens used (all 0 across
199 prior tutorials at capture time): `64 MiB`, `64MiB`, `increased-worker-size-limit`,
`Worker size limit`, `D1 free tier`, `d1-free-tier`, `module registry`, `Python 3.14`,
`Miniflare v5`, `post-quantum DNSSEC`, `1.1.1.1`, `Automatic Key Exchange`,
`wrangler deploy`, `bundle size`.
