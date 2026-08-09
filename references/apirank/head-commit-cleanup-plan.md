# Head Commit Cleanup Plan — 2026-08-04

## Status

**DRAFTED, NOT EXECUTED — DEFERRED UNTIL POST-ADSENSE-REVIEW.**

Jazfox decision 2026-08-04 (post-cleanup-task): "等 AdSense 审核通过了再来改,改动动作有点大."

Reason: while the 8 files don't block AdSense review, three of them have live URLs (`reka-ai-api-review`, `tavily-api-review`, `kimi-k3-api-review` not yet live) and any cleanup involves either `git push --force` (rewrites history) or deletion-with-301 (new URLs visible to AdSense reviewer). Best to wait for review outcome first.

Trigger to re-pick-up this plan: AdSense sends `pub-2134598094429002` a "your site is approved" notification OR 7 days pass without rejection (assume approved). Either way, re-read this file before touching the 8 files.

Originally written when Jazfox offloaded the cleanup task with "你自己处理一下" but the analysis surfaced 3 separate concerns that cross live-production boundaries. Following the `apirank-data-catalog` §0 "PRD-切片+暂停" decision pattern (verified 2026-07-27): when a task touches >3 files OR crosses the deploy boundary, write a plan first, then pause for review.

**Verified state at 2026-08-04 22:50+ (commit e8a20df already on `main` + CF Pages production):**

```
HEAD: e8a20df apirank: live AdSense integration (ca-pub-2134598094429002)
  Total: 71 files changed, 2085 insertions(+), 68 deletions(-)
  Working tree: clean (no untracked, no modified)
  CF Pages: deployment triggered by git push, now live
```

## The 8 scope-bloat files

Found via `git diff-tree --no-commit-id --name-only -r HEAD | grep -E "^drafts/|^src/content/posts/|^src/pages/_test/|^src/pages/zh/tutorials/(tavily|reka)"`:

| # | Path | Severity | Production status | Why it's here |
|---|---|---|---|---|
| 1 | `drafts/en-reka-ai-api-review-2026-08-01.md` | 🟡 medium | n/a (drafts/ not built) | Cron wrote EN draft but never published |
| 2 | `drafts/zh-reka-ai-api-review-2026-08-01.md` | 🟡 medium | n/a (drafts/ not built) | Cron wrote ZH draft but never published |
| 3 | `drafts/zh-tavily-api-review-2026-07-31.md` | 🟡 medium | n/a (drafts/ not built) | Cron wrote ZH draft 7-31, never published |
| 4 | `src/pages/zh/tutorials/reka-ai-api-review.astro` | 🔴 **HIGH** | **HTTP 200** at `https://apirank.vip/zh/tutorials/reka-ai-api-review/` | **ORPHAN PAGE** — `reka-ai` is NOT in `src/data/providers.json` (verified 2026-08-04). No provider back-link, no nav reference. AdSense reviewer will see a 200 with no upstream context. |
| 5 | `src/pages/zh/tutorials/tavily-api-review.astro` | 🟢 low | **HTTP 200** at `https://apirank.vip/zh/tutorials/tavily-api-review/` | `tavily` IS in providers.json. Probably cron 7-31 wrote the page but never committed until this AdSense sweep accidentally caught it. Page is structurally fine. |
| 6 | `src/content/posts/kimi-k3-api-review-2026.md` | 🟡 medium | n/a (Content Collections — apirank-data-catalog §0 warning: build silently 0-hits this path) | Wrong path. Should be `src/pages/tutorials/kimi-k3-api-review-2026.astro` per the article-authoring rule documented in `references/apirank-articles-not-in-content-posts-2026-08-04.md`. |
| 7 | `src/content/posts/zh/kimi-k3-api-review-2026.md` | 🟡 medium | n/a (same as #6) | Same as #6, ZH variant. |
| 8 | `src/pages/_test/test.astro` | 🟢 low | HTTP 404 (Astro excludes `_test/` prefix routes) | Dead file, no production impact. |

### Live URL verification (curl 2026-08-04)

```
https://apirank.vip/zh/tutorials/reka-ai-api-review/ → 200  ⚠️ orphan
https://apirank.vip/zh/tutorials/tavily-api-review/ → 200  ✅ linked
https://apirank.vip/_test/test                      → 404  ✅ no impact
```

## Why "just `git reset HEAD~1`" doesn't work

The commit is already on `main` and CF Pages has already deployed from it. Three constraints:

1. **`git reset HEAD~1` + `git push --force` rewrites history but does NOT undeploy from CF Pages.** CF Pages only deploys *new* commits; it has no "rollback deploy" primitive other than pointing at an older commit and re-deploying. So the cleanup would result in: git history clean, but **production still serves the 8 files** until a fresh commit removes them.
2. **The 4 tutorial files (#4, #5, #6, #7) are live URLs.** Removing them in a future commit breaks:
   - Any external link pointing to `apirank.vip/zh/tutorials/reka-ai-api-review/`
   - Search engine indexing (if Google has already crawled them)
   - The AdSense audit's "navigation consistency" check (a 200 that points to an orphan page is a content-quality red flag)
3. **`reka-ai-api-review.astro` is an orphan in the data model.** It's not just a "git-cleanup" issue — it's a "we have a review page for a provider that doesn't exist in our catalog" issue. Touching this requires deciding: (a) add reka to providers.json properly, or (b) delete the page with a 301 redirect.

## Three cleanup slices (listed, not executed)

### Slice 1: Git history hygiene (lowest blast radius)

**Goal:** Separate the 8 non-scope files from the AdSense commit.

**Procedure:**
1. `git checkout e8a20df~1 -- <real-adsense-files>` (the 5 core ads.txt + BaseLayout + privacy EN+ZH + replace_mock_adsense_id.py)
2. Recommit these 5 files as a clean "AdSense integration" commit with the original message
3. The 8 scope-bloat files become untracked again → move them out of the repo
4. **Push to a feature branch first** (`cleanup/head-commit-separate`), preview on CF Pages, then merge to `main`

**Risk:** `git push --force` rewrites `main`. If anyone else has pulled from `main` in the last 4 hours, their local is broken. Verified 2026-08-04: only Jazfox has write access, so safe.

**What this does NOT solve:** Slice 1 cleans git history but the 8 files still need somewhere to go (see slices 2/3).

### Slice 2: Wrong-path drafts (#1, #2, #3, #6, #7)

**Goal:** Move drafts to the correct path or stash them out of the repo entirely.

**Decision tree:**
- For #1, #2, #3 (`drafts/{en,zh}-{reka,tavily}-...md`): These are cron-owned articles. Either:
  - **(a) Publish:** move to `src/pages/tutorials/<slug>.astro` + `src/pages/zh/tutorials/<slug>.astro` (for tavily: also confirm `tavily` is in providers.json — it is, so safe). For reka: requires Slice 3 first because reka isn't in providers.json yet.
  - **(b) Delete:** if not ready to publish, `git rm` and remove from the cron state.json. Lowest cost.
- For #6, #7 (`src/content/posts/{,zh/}kimi-k3-api-review-2026.md`): These are in the WRONG path per `references/apirank-articles-not-in-content-posts-2026-08-04.md`. Either:
  - **(a) Move + rename:** to `src/pages/tutorials/kimi-k3-api-review-2026.astro` + `src/pages/zh/tutorials/kimi-k3-api-review-2026.astro`, then add to the index cards
  - **(b) Delete:** if the content is stale or the cron that wrote it is no longer relevant

**Risk:** Path-move creates new URLs (kimi-k3 review currently 404 because Content Collections path isn't built). If 任何外部已 back-link to `/src/content/posts/...` (unlikely), that breaks. Recommend (a) move + rename — content is presumably valuable to publish.

### Slice 3: `reka-ai-api-review.astro` orphan (the only 🔴 item)

**Goal:** Resolve the orphan page state at `https://apirank.vip/zh/tutorials/reka-ai-api-review/`.

**Options:**

**(3a) Promote Reka to a real provider.**
- Add Reka to `src/data/providers.json` with full metadata (id: `reka`, name: "Reka", website: https://reka.ai, pricing tier, China access, etc.)
- Add Reka to `src/pages/providers/[id].astro` if there's a provider page template
- The orphan page becomes linked: in-text link to `/providers/reka/`, nav card on the providers index
- Cost: ~1 hour of work. Requires verifying Reka's actual pricing from https://reka.ai (use the `apirank-domain-probe-cron` skill recipe, not from memory)
- **Recommended option** if Jazfox wants to expand the provider catalog

**(3b) Delete with 301 redirect.**
- `git rm src/pages/zh/tutorials/reka-ai-api-review.astro` (+ the EN-side if it exists at `src/pages/tutorials/reka-ai-api-review.astro` — verify)
- Add a 301 redirect in `astro.config.mjs` to the nearest relevant page (e.g. `/providers/ai21/` or `/tutorials/` index)
- Cost: 5 minutes. Defensible if Reka isn't a strategic priority
- **Recommended option** if Reka isn't on the roadmap

**(3c) Hard delete, no redirect.**
- `git rm ...` only. The 200 URL becomes 404.
- Cost: 1 minute. **Not recommended** — breaks SEO and AdSense reviewer expectation of "navigation consistency."

## Recommended sequence (if Jazfox approves)

1. **Slice 1 first** (git history cleanup, separate the AdSense commit from the 8 files)
2. **Slice 3 (option 3a or 3b)** before or alongside Slice 1 — the orphan page is the only actual quality risk
3. **Slice 2 last** — drafts cleanup is housekeeping, no live impact

## Verification checklist after each slice

```bash
# After Slice 1
cd /root/apirank
git log --oneline -3  # confirm AdSense commit is now clean (5 files, ~100 lines)
git status  # confirm 8 files are untracked again
# Preview deploy:
npx wrangler pages deploy dist --project-name=apirank-vip --commit-dirty=true  # noqa: not needed if just separating commit, no content change

# After Slice 3a (reka promoted)
curl -sL https://apirank.vip/providers/reka/ | grep -oE '<title>[^<]+</title>'
curl -sL https://apirank.vip/zh/tutorials/reka-ai-api-review/ | grep -oE 'href="/providers/reka/"' | head -1

# After Slice 3b (reka deleted + 301)
curl -sL -o /dev/null -w "%{http_code} → %{redirect_url}\n" https://apirank.vip/zh/tutorials/reka-ai-api-review/

# After Slice 2 (drafts cleanup)
ls drafts/ | wc -l  # confirm drafts removed
ls src/content/posts/  # confirm wrong-path files removed
```

## Open questions for Jazfox

1. **Slice 3: 3a (promote) or 3b (delete + 301)?** Different cost/value tradeoff.
2. **Slice 2: delete the drafts or republish them?** If republish, who owns the cron that wrote them?
3. **Do we want any of this before AdSense review completes?** Time-sensitive: AdSense team typically reviews within 1-3 days. If they reject on the reka orphan page, we lose time. If they approve, slices 1/2 can wait.

## Cross-references

- `apirank-data-catalog` skill §0 — Article path rule (Content Collections silent-drop)
- `apirank-data-catalog` skill §8 — "git add -A" 2026-08-04 lesson (this isn't a new lesson, it's the second occurrence)
- `references/apirank-articles-not-in-content-posts-2026-08-04.md` — Path-boundary rule
- `references/apirank/cmp-decision-checklist.md` — Decision-memory link (separate concern, CMP defer)
