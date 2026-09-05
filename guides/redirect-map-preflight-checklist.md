# Redirect-map preflight checklist

A redirect CSV can be internally inconsistent before it reaches a server. Review the map, then verify the deployed behavior separately.

## Work through one concrete example

```csv
source,target,status
/old-about,/about,301
/summer,/sale,301
/sale,/collections/sale,301
/loop-a,/loop-b,301
/loop-b,/loop-a,301
/contact-old,/contact,301
/contact-old,/support,301
/legacy,/current,301
/legacy,/current,301
```

Expected findings:

| Rules | What to resolve |
|---|---|
| `/summer → /sale → /collections/sale` | Two-hop chain. Check whether the last destination is correct before shortening it. |
| `/loop-a ↔ /loop-b` | Loop. Choose an appropriate destination outside the loop. |
| Two `/contact-old` targets | Conflict. Decide which destination is intended; do not silently keep the first. |
| Repeated `/legacy → /current` | Exact duplicate. Keep one copy if the rule is otherwise correct. |
| `/old-about → /about` | No structural issue in this example. The target's existence and relevance remain unverified. |

## Before import

1. Keep one unambiguous source column, target column and optional status column. Two columns called `target` must be resolved before checking the file.
2. Set old and new site origins explicitly when paths are relative. The same path on two different domains is not necessarily a self-redirect.
3. Resolve contradictory destinations and statuses. Fix loops and any rules that feed into them.
4. Review chains, temporary redirects, external destinations and fragments. A chain should not be shortened automatically without deciding what the destination should be.
5. Preserve the source file. Export a row-by-row review and inspect proposed candidates separately.
6. Convert generic CSV columns into your deployment platform's required format. Exact URL comparisons do not emulate every server's query-string, case, trailing-slash or wildcard behavior.
7. After deployment, verify actual status codes, redirect hops, destination availability and destination relevance. CSV checks cannot prove those facts.

## Optional tool

[Redirect Preflight](https://redirect-preflight-ji.silver-pika-6542.chatgpt.site/) provides a free 25-row browser check and a [$29 offline edition](https://redirect-preflight-ji.silver-pika-6542.chatgpt.site/buy) for up to 20,000 rows / 5 MB. It produces review CSVs, deduplicated candidate exports and printable reports. It does not crawl pages or verify live responses.

**Commercial disclosure:** The repository owner, Jon Ireland, sells this product. This is an original worked example and a product listing, not an independent review. No SEO outcome or daily income is guaranteed.
