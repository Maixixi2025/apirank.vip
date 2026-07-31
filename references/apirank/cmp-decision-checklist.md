# CMP Decision Checklist — apirank.vip

**Decision date:** 2026-07-31
**Decision:** **Defer CMP until AdSense approved + first ad serving live**

---

## Why deferred

| Reason | Evidence |
|---|---|
| Google policy mandates CMP **only when serving personalized ads to EEA/UK/CH users** | https://support.google.com/adsense/answer/13554116 |
| apirank.vip target audience is China (`.vip` TLD) — not EEA | domain TLD, GSC traffic analytics |
| No ads currently served (30 `<ins class="adsbygoogle">` placeholders use mock `ca-pub-xxxxxxxxxxxxxx`) | grep `adsbygoogle.push` → 0 matches |
| Privacy page already says "plans to display ads" (correct tense) | grep "plans to display" in `src/pages/privacy.astro` |
| No GA4 / analytics script loaded globally | grep `gtag` in BaseLayout → 0 |
| Audit skill §7: "No CMP needed when ads aren't live" | ilang/adsense-site-readiness-audit/SKILL.md §7 |

## When to act

Trigger: any 2 of the following become true:

- [ ] AdSense application **approved** and `pub-` ID available
- [ ] First `<ins class="adsbygoogle">` updated from mock to real `ca-pub-<REAL_ID>` + real `data-ad-slot`
- [ ] `<script src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js">` added to BaseLayout head
- [ ] First `adsbygoogle.push({})` call made
- [ ] EEA / UK / CH traffic measurable in GSC (>5% of impressions)

If any 2 trigger, **stop ads first**, install CMP, then resume.

## Implementation plan (1 hour, when triggered)

### 1. Choose CMP — Quantcast Choice (recommended)

- **Cost:** Free for sites under Quantcast's traffic threshold; certified by Google
- **Why:** TCF v2.2 compliant, Consent Mode v2 built-in, lowest setup cost
- **Alternates:**
  - Cookiebot (Usercentrics): ~$12/mo, 100+ pages tier; mature
  - Iubenda: ~$27/mo Pro; bundles privacy policy + cookie solution
  - OneTrust: enterprise pricing, overkill for apirank

### 2. Integration (4 steps)

#### a. Add CMP script to BaseLayout.astro head

```astro
<head>
  ...
  <!-- CMP — Quantcast Choice TCF v2.2 -->
  <script>
    (function() {
      var host = window.location.hostname;
      var s = document.createElement('script');
      s.src = 'https://quantcast.mgr.consensu.org/tcf.js';
      s.async = true;
      s.setAttribute('data-cmp-id', 'YOUR_QUANTCAST_ID');
      document.head.appendChild(s);
    })();
  </script>
  ...
</head>
```

Replace `YOUR_QUANTCAST_ID` with the actual ID from quantcast.choices.com dashboard after signup.

#### b. Update Privacy page

Change from "plans to display ads" → "displays ads served by Google AdSense, and uses a Google-certified Consent Management Platform (Quantcast Choice) to manage user consent for EEA, UK, and Switzerland visitors."

#### c. Gate adsbygoogle.push on consent

```astro
<script is:inline>
  window.addEventListener('tcfapi', function(tcDataEvent) {
    var tcData = tcDataEvent.detail;
    var hasConsent = tcData.vendor.consents[755]; // Google vendor ID
    if (hasConsent) {
      (adsbygoogle = window.adsbygoogle || []).push({});
    }
  });
</script>
```

#### d. Gate GA4 on consent

```astro
<script>
  window.addEventListener('tcfapi', function(tcDataEvent) {
    var tcData = tcDataEvent.detail;
    var hasConsent = tcData.vendor.consents[755];
    gtag('consent', 'update', {
      ad_storage: hasConsent ? 'granted' : 'denied',
      analytics_storage: hasConsent ? 'granted' : 'denied',
      ad_user_data: hasConsent ? 'granted' : 'denied',
      ad_personalization: hasConsent ? 'granted' : 'denied'
    });
  });
</script>
```

### 3. Verification (run after deploy)

```bash
# CMP script loaded
curl -sL https://apirank.vip/ | grep -c "quantcast.mgr.consensu.org"
# Expected: 1 (in BaseLayout head)

# adsbygoogle.push is gated (not just a hardcoded call)
grep -r "adsbygoogle.push" src/ | wc -l
# Expected: 0 (push only inside tcfapi listener)

# Privacy page updated
curl -sL https://apirank.vip/privacy | grep -c "Consent Management Platform"
# Expected: >= 1

# Test from EU IP (use a VPN or EU-based test)
# - Banner should appear on first visit
# - "Accept all" should trigger tcfapi event
# - adsbygoogle.push should fire only after consent
```

### 4. Confirm with browser (manual, on first EEA-IP visit)

- [ ] Banner appears within 1s
- [ ] "Reject all" → adsbygoogle.push does NOT fire
- [ ] "Accept all" → adsbygoogle.push fires, ad loads
- [ ] Revisit after consent → no banner (state stored)
- [ ] Network tab → tcf.js loaded once, cached

---

## Status as of 2026-07-31

- [ ] CMP installed — **deferred**
- [ ] CMP script in BaseLayout — n/a
- [ ] Privacy page CMP disclosure — n/a
- [ ] adsbygoogle.push consent-gated — n/a
- [ ] GA4 consent-gated — n/a

## Related

- adsense-site-readiness-audit §6 (privacy "plans to" wording)
- adsense-site-readiness-audit §7 (CMP/privacy consistency)
- cloudflare-deploy §1-2 (CF Pages no-runtime integration)
