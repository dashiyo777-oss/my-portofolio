# PageSpeed Insights — Release Notes (Appendix)

Release history for the PageSpeed Insights (PSI) API and UI. The API is versioned as **v5**; the underlying Lighthouse version is independent and updated regularly.

## Recent updates

### Oct 20, 2025
PSI and the API updated to [Lighthouse 13.0](https://developer.chrome.com/blog/lighthouse-13-0).

### Dec 5, 2024
CPU throttling factor adjusted to account for the low CPU performance benchmarks typical in PSI production environments. Generally increases lab **TBT** scores for mobile sites. Field data and desktop scores are not affected.

### May 10, 2024
Updated to [Lighthouse 12.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v12.0.0). **Breaking changes** in the API response, including removal of the **PWA category**.

### Aug 28, 2023 (Lighthouse 11, deployed Aug 9)
Updated to [Lighthouse 11.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v11.0.0) with [breaking API changes](https://github.com/GoogleChrome/lighthouse/releases/tag/v11.0.0#:~:text=%F0%9F%92%A5-,Breaking%20changes). The [blog post](https://developer.chrome.com/blog/lighthouse-11-0/) covers Accessibility category and audit updates.

### Aug 8, 2023
`EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT` removed from the API response. Use `INTERACTION_TO_NEXT_PAINT` (same data) for the page's field INP.

### May 10, 2023
**INP is no longer experimental** — now a [pending Core Web Vital](https://web.dev/inp-cwv/), reflected in UI and API. The API response gains `INTERACTION_TO_NEXT_PAINT` (same data as the experimental field, which was removed 90 days later on Aug 8, 2023).

### March 16, 2023
New **shareable links** in the UI: analysis moves to an `/analysis` path with a unique ID. The page holds a shareable snapshot with an analysis timestamp; "Copy Link" yields a link shareable for 30 days. The old `/report` path redirects to `/analysis`.

### March 14, 2023
Updated from Lighthouse 9.6.x to [Lighthouse 10.0.x](https://github.com/GoogleChrome/lighthouse/releases/tag/v10.0.0). [Breaking changes](https://github.com/GoogleChrome/lighthouse/releases/tag/v10.0.0#:~:text=%F0%9F%92%A5-,Breaking%20changes) include a new location for `full-page-screenshot` and updated `Url` properties. See the [blog post](https://developer.chrome.com/blog/lighthouse-10-0/) for scoring changes.

### Oct 27, 2022
UI lab data section adds **Accessibility, Best Practices, and SEO** categories alongside Performance.

### May 10, 2022
Two new **experimental field metrics** in API and UI: [INP](https://web.dev/inp/) and [TTFB](https://web.dev/ttfb/) (experimental metrics may change or disappear). New loading experience: field and lab data load in parallel; PSI resolves HTTP 3XX redirects before handing off to Lighthouse (opt-out to "original" URL possible but not advised); CWV metrics (LCP, FID, CLS) shown directly under the CWV assessment; tighter design.

### Feb 17, 2022
[Lighthouse 9.3.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v9.3.0).

### Nov 15, 2021
New UI look and [home](https://pagespeed.web.dev/) ([blog post](https://web.dev/whats-new-pagespeed-insights)). As of Nov 13, 2021, using [Lighthouse 9.0.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v9.0.0).

### Sept 22, 2021
[Lighthouse 8.4.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v8.4.0).

### Aug 31, 2021
[Lighthouse 8.3.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v8.3.0) (also [8.2.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v8.2.0), [8.1.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v8.1.0)).

### June 10, 2021
Field data now provided **per-metric**: any metric meeting the data threshold is surfaced, even if others lack sufficient data. Previously all metrics had to meet the threshold. Reflected in `loadingExperience` / `originLoadingExperience`.

### June 1, 2021
[Lighthouse 8.0.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v8.0.0) (breaking changes for programmatic users). CrUX API (underpins field data) also updated.

### May 24, 2021
Underlying Chrome upgraded from 88 to 90 — mainly notable for [CLS improvements](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/speed/metrics_changelog/cls.md) in Chrome 89/90.

### April 1, 2021
[Lighthouse 7.3.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v7.3.0).

### March 3, 2021
PSI now uses **HTTP/2** for network requests when the server supports it (previously HTTP/1.1). Brings results closer to Lighthouse CLI/DevTools. Performance scores generally **went up by a few points**. Pages without h2 now show an [audit](https://web.dev/uses-http2/) estimating the improvement h2 would bring.

### March 2, 2021
API max timeout raised from **60s to 120s** for complex/heavy pages.

### February 19, 2021
[Lighthouse 7.1.0](https://github.com/GoogleChrome/lighthouse/releases/tag/v7.0.0) (up from 6.3.0; includes v7 major plus 6.4.0/6.5.0/7.1.0). Breaking changes for programmatic users; small metric adjustments from bug fixes.

### December 3, 2020
PSI now uses the [CrUX API](https://web.dev/chrome-ux-report-api/) for field data (affects `loadingExperience` / `originLoadingExperience`).

### Sept 8, 2020
Lighthouse 6.3.0 deployed.

### May 27, 2020
Lighthouse 6.0.0 deployed.

### May 2020
API v1, v2, v3beta1, and v4 removed (deprecated Nov 2018).

### May 7, 2019
Lighthouse 5.0 released ([notes](https://bit.ly/lhpsi5)).

### January 31, 2019
Lighthouse 4.1 released ([notes](https://bit.ly/2MSS55O)).

### November 2018
**API v5 released** — uses Lighthouse as its analysis engine and incorporates CrUX field data. Provides CrUX data and all Lighthouse audits. Earlier versions deprecated six months later.

## Historical API versions

### Version 4 (Jan 2018)
Added a speed score based on CrUX and refined the original PSI score as an optimization score focused on relative headroom to improve.

### Version 2 (Jan 2015)
Added rule groups (e.g. `SPEED`, `USABILITY`). Later updates: result category (May 12, 2017); render engine switched Webkit → Blink (Feb 2, 2017); image optimization switched to mod_pagespeed's library (Dec 12, 2016); app-install interstitial rule removed from scoring (Aug 23, 2016) and removed completely (Nov 1, 2016). *Deprecated; closed Jun 2018.*

### Version 1
Initial release with localization in 40 languages. On Oct 29, 2013, the deprecated `ruleScore` field was removed — use `ruleImpact` instead. *Closed.*
