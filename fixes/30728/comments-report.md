| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | abretonc7s | conversation | OUT_OF_SCOPE | Worker report is informational and requires no code change. |
| 2 | cursor[bot] | app/components/UI/Perps/components/PerpsRelatedMarkets/PerpsRelatedMarkets.tsx:66 | REAL | Reset slide tracking when the current market symbol changes. |
| 3 | aganglada | app/components/UI/Perps/components/PerpsRelatedMarkets/PerpsRelatedMarkets.tsx:75 | OUT_OF_SCOPE | Tracking-repo registration is external to this mobile PR; mobile analytics docs remain in-repo. |
| 4 | aganglada | app/components/UI/Perps/components/PerpsRelatedMarkets/PerpsRelatedMarkets.tsx:101 | OUT_OF_SCOPE | Same tracking-repo question as comment 3; external analytics registry work is outside this PR. |
| 5 | aganglada | app/components/UI/Perps/components/PerpsRelatedMarkets/PerpsRelatedMarkets.tsx:105 | REAL | Removed the unexplained local 20-item cap; the current perps controller package does not expose a `limit` parameter. |
| 6 | aganglada | app/components/UI/Perps/selectors/featureFlags/index.ts:87 | REAL | Renamed the remote feature flag lookup to `perpsRelatedMarkets`. |
| 7 | aganglada | app/components/UI/Perps/utils/relatedMarkets.ts:43 | REAL | Replaced the static symbol collections with category-based related-market selection from market data. |

Recipe re-validation result: SKIPPED - CDP unavailable on `WATCHER_PORT=8065` (`Cannot reach Metro at http://localhost:8065/json/list`).

## Final Summary

- Total comments: 7 (4 REAL, 0 FALSE POSITIVE, 3 OUT OF SCOPE)
- Commit SHA for fixes: `db4a7c83adda270fd8ed19f6b3874ad92337b35c`
- Files changed:
  - `app/components/UI/Perps/Views/PerpsMarketDetailsView/PerpsMarketDetailsView.test.tsx`
  - `app/components/UI/Perps/components/PerpsRelatedMarkets/PerpsRelatedMarkets.test.tsx`
  - `app/components/UI/Perps/components/PerpsRelatedMarkets/PerpsRelatedMarkets.tsx`
  - `app/components/UI/Perps/selectors/featureFlags/index.test.ts`
  - `app/components/UI/Perps/selectors/featureFlags/index.ts`
  - `app/components/UI/Perps/utils/relatedMarkets.test.ts`
  - `app/components/UI/Perps/utils/relatedMarkets.ts`
- Recipe re-validation result: SKIPPED (CDP unavailable on `WATCHER_PORT=8065`)
- Merge-main status from step 3: clean
