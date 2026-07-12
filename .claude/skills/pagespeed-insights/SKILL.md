---
name: pagespeed-insights
description: Reference for understanding Google PageSpeed Insights (PSI) reports — lab vs. field data, Core Web Vitals (FCP, LCP, CLS, INP, TTFB) thresholds and buckets, CrUX real-user data, Lighthouse scoring, and common FAQs. Use when interpreting PSI/Lighthouse results, deciding whether a page passes Core Web Vitals, explaining why field and lab data differ, or advising how to improve a page's performance score.
---

# PageSpeed Insights

PageSpeed Insights (PSI) reports on the user experience of a page on both **mobile** and **desktop** devices, and provides suggestions on how that page may be improved.

PSI provides two kinds of data:

- **Lab data** — collected in a controlled, simulated environment (via Lighthouse). Useful for **debugging**, but may not capture real-world bottlenecks.
- **Field data** — real-world user experience captured over time. Useful for capturing **true user experience**, but with a more limited set of metrics.

See [How To Think About Speed Tools](https://developers.google.com/web/fundamentals/performance/speed-tools) for more on the two types.

## Real-user experience data (field / CrUX)

Field data in PSI is powered by the [Chrome User Experience Report](https://developers.google.com/web/tools/chrome-user-experience-report) (CrUX) dataset. Over a **trailing 28-day** collection period, PSI reports real users':

- [First Contentful Paint](https://web.dev/articles/fcp) (FCP)
- [Interaction to Next Paint](https://web.dev/articles/inp) (INP)
- [Largest Contentful Paint](https://web.dev/articles/lcp) (LCP)
- [Cumulative Layout Shift](https://web.dev/articles/cls) (CLS)
- [Time to First Byte](https://web.dev/articles/ttfb) (TTFB) — experimental

**Data availability:** A page needs sufficient CrUX samples to be shown. Recently published pages or pages with too few real-user samples may lack data. When a page has insufficient data, PSI **falls back to origin-level** granularity (all pages of the site). If the origin also lacks data, PSI shows no real-user data.

### Thresholds — Good / Needs Improvement / Poor

PSI classifies experiences into three buckets, aligned with the [Web Vitals](https://web.dev/articles/vitals) initiative:

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| FCP | [0, 1800ms] | (1800ms, 3000ms] | over 3000ms |
| LCP | [0, 2500ms] | (2500ms, 4000ms] | over 4000ms |
| CLS | [0, 0.1] | (0.1, 0.25] | over 0.25 |
| INP | [0, 200ms] | (200ms, 500ms] | over 500ms |
| TTFB (experimental) | [0, 800ms] | (800ms, 1800ms] | over 1800ms |

### Distribution and the 75th percentile

PSI shows a distribution of each metric split into Good (green), Needs Improvement (amber), and Poor (red) bars. E.g. 11% in LCP's amber bar means 11% of observed LCP values fall between 2500ms and 4000ms.

Above the bars, PSI reports the **75th percentile** for each metric, classified as good/needs-improvement/poor using the thresholds above. The 75th percentile is chosen so pages work well for the majority of users, even under the most difficult device/network conditions. See [Defining the Core Web Vitals metrics thresholds](https://web.dev/articles/defining-core-web-vitals-thresholds).

### Core Web Vitals assessment

Core Web Vitals are **INP, LCP, and CLS**, aggregated at the page or origin level. Assessment rules:

- With sufficient data in all three: **passes** if the 75th percentiles of all three are Good.
- If INP has insufficient data: **passes** if the 75th percentiles of LCP and CLS are both Good.
- If either LCP or CLS has insufficient data: the aggregation **cannot be assessed**.

### PSI field data vs. CrUX on BigQuery

- **PSI**: updated **daily**, supports URL- and origin-level data.
- [CrUX on BigQuery](https://developer.chrome.com/docs/crux/guides/bigquery): updated **monthly**, origin-level only.
- Both represent trailing 28-day periods.

## Lab diagnostics (Lighthouse)

PSI uses [Lighthouse](https://developer.chrome.com/docs/lighthouse/) to analyze the URL in a simulated environment across four categories: **Performance, Accessibility, Best Practices, and SEO**.

### Category scores

Each category gets a score:

- **90+** = Good (green)
- **50–89** = Needs Improvement
- **below 50** = Poor

### Performance metrics

The Performance category reports:
[FCP](https://web.dev/articles/fcp),
[LCP](https://web.dev/articles/lcp),
[Speed Index](https://developer.chrome.com/docs/lighthouse/performance/speed-index/),
[CLS](https://web.dev/articles/cls),
[Time to Interactive](https://developer.chrome.com/docs/lighthouse/performance/interactive/),
and [Total Blocking Time](https://web.dev/articles/tbt).

Each metric is [scored](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring/) and labeled:

- Green circle = Good
- Amber square = Needs Improvement
- Red triangle = Poor

### Audits

Each category contains audits with guidance on improving the page. See the [Lighthouse docs](https://developer.chrome.com/docs/lighthouse/) for a per-category breakdown.

## FAQs

**What device/network conditions does Lighthouse simulate?**
Mobile: a mid-tier device (Moto G4) on a [throttled mobile network](https://github.com/GoogleChrome/lighthouse/blob/master/docs/throttling.md). Desktop: an emulated desktop with a wired connection. PSI runs in a Google datacenter (North America, Europe, or Asia); the location is shown in the Lighthouse report's environment block.

**Why do field and lab data sometimes contradict each other?**
Field data is historical, anonymized real-world data across many devices/networks. Lab data is a single simulated load on one device with fixed network conditions — so values can differ. See [Why lab and field data can be different](https://web.dev/articles/lab-and-field-data-differences).

**Why the 75th percentile?**
To ensure pages work well for the majority of users, including those under the most difficult device and network conditions.

**What is a good lab score?**
Any green score (90+). Note: good lab data does **not** guarantee good real-user experiences.

**Why does the performance score change between runs with no changes?**
[Variability](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring/#fluctuations) comes from local network availability, client hardware availability, and client resource contention, among other sources.

**Why is CrUX data unavailable for a URL/origin?**
CrUX aggregates data from [opted-in users](https://developer.chrome.com/docs/crux/methodology) and requires the URL to be public ([crawlable and indexable](https://developer.chrome.com/docs/lighthouse/seo/is-crawlable/)) with enough distinct samples for a representative, anonymized view.

## Version history

The API is versioned as **v5**; the underlying Lighthouse version is independent and updated regularly (most recently Lighthouse 13.0 as of Oct 20, 2025). For the full release history of both the PSI API and UI — Lighthouse version bumps, breaking API changes, metric additions (INP, TTFB), and historical API versions — see [reference/release-notes.md](reference/release-notes.md).

## Further resources

- Specific, answerable questions: [Stack Overflow (pagespeed-insights)](https://stackoverflow.com/questions/tagged/pagespeed-insights)
- General discussion: [PageSpeed Insights mailing list](https://groups.google.com/forum/#!forum/pagespeed-insights-discuss)
- Web Vitals metric questions: [web-vitals-feedback group](https://groups.google.com/g/web-vitals-feedback)
