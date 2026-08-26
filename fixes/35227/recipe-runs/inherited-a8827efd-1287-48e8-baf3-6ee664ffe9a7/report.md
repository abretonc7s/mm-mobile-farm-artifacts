## Self-Review Fixes
- `app/components/UI/Perps/utils/chartOverlayLines.ts` — added unit tests for trigger skip, synthetic skip, non-open skip, detailed-type limits, and limit-only overlays.
- `app/components/UI/Perps/components/PerpsAdvancedChart/PerpsAdvancedChart.tsx:89` — `mapTpslToPositionLines` now covers limit-only overlays, non-finite limit prices, and entry+limit together; color map asserts limitBuy/limitSell.
- `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProChartPanel.tsx` — Limit overlay host is accessible; panel tests fail if the resting-limit filter is reverted.
- `temp/tasks/feat/tat-3530-0825-094017/artifacts/recipe.json` — recipe run 14/14 pass; artifact contract pass with recipe-quality, coverage, and screenshot.

## Self-Review Fixes
- `artifacts/evidence-manifest.json:10` — standalone file path is `after-ac1-limit-line-on-chart.png` so the contract MISSING check resolves.
- `artifacts/recipe.json` + `after-ac1-limit-line-on-chart.png` — expand the Pro chart, scroll the market page, wait for `perps-pro-market-chart-panel`, recapture. Recipe 17/17. Screenshot is the BTC 15m chart, not the order book.
- `PerpsProChartPanel.tsx:334` — overlay host uses `pointerEvents="none"` so Limit lines do not block chart gestures. Panel test asserts the prop.
- `TradingViewChart.tsx:641` — chart accessibility label uses `strings('perps.order.limit')`.

## Self-Review Fixes
- `artifacts/recipe.json` — `ensure-limit-order` uses `start_state` with `offset_pct: -1` so the resting Limit sits in the 15m frame (green `- Limit` at 80,653). Prior `ensure_orders` defaulted to -30% and the still only showed last price.
- `artifacts/recipe.json` — `expand-chart` is `ui.wait_for` on `perps-pro-market-chart-panel`. Nested `mm-harness call` + toggle press hit SANDBOX_BUSY and could collapse persist.
- `artifacts/after-ac1-limit-line-on-chart.png` — recaptured after the on-scale place. Dashed green Limit line at 80,653 is in frame.
- `TradingViewChartTemplate.tsx` — autoscale still includes off-scale Limit prices when the next run uses the default far offset.

## Self-Review Fixes
- `artifacts/recipe.json:69` — no further edit. `expand-chart` is already `ui.wait_for` on `perps-pro-market-chart-panel`; a second run cannot flip `chartExpanded`.
- `artifacts/after-ac1-limit-line-on-chart.png` — reran recipe with `start_state` `offset_pct: -1`. Still shows the dashed green `- Limit` line on the 15m BTC chart (80,577 vs last 81,404). Overlay wait `present` plus the PNG is the visual proof.

## Self-Review Fixes
- `TradingViewChartTemplate.tsx:1130` — removed `syncLimitScaleSeries` / `limitScaleSeries`; autoscale is only `autoscaleInfoProvider`.
- `TradingViewChartTemplate.tsx:686` — `collectLimitOverlayPrices` dedups and ignores hidden `originalPriceLineData`; hide clears `lastLimitOrderPrices`.
- `TradingViewChartTemplate.tsx:743` — padding uses `PERPS_CHART_CONFIG.LIMIT_AUTOSCALE_PADDING_FRACTION`.
- `PerpsProChartPanel.tsx:333` — deleted empty full-bleed Limit overlay Box (a11y + recipe scaffolding).
- `TradingViewChart.tsx:641` — removed chart-container `accessibilityLabel` of "Limit"; WebView key `v26`.
- `chartOverlayLines.ts:33` — filter uses `isLimitExecutionOrderType` / `getTriggerExecution` (covers scale/chase, no `detailedOrderType` substring).
- `PerpsAdvancedChart.tsx:92` — one finite-entry-or-limits guard; TP/SL/liq only attach when entry is finite. Dropped no-op fallback `testID`.
- `PerpsProChartPanel.test.tsx` — asserts `tpslLines.limitOrders` on `mockPerpsAdvancedChart`.
- `artifacts/recipe.json` — overlay wait replaced with `perps-pro-market-chart-content`. Recipe 18/18 after the fix.

## Self-Review Fixes
- No new product diff this pass. Prior commits already removed `limitScaleSeries`, the empty overlay Box, the "Limit" chart a11y label, `detailedOrderType` matching, unreachable `mapTpslToPositionLines` guards, hidden-scale stretch, and the no-op `testID`.
- Re-verified: 76 Jest tests pass; recipe pass with `--library perps=...`; `TASK_ARTIFACT_CONTRACT_PASS`.

## Self-Review Fixes
- `app/components/UI/Perps/Perps.testIds.ts:374` — removed orphaned `LIMIT_OVERLAY` / `perps-chart-limit-overlay` after the overlay Box and recipe node were deleted.
- `artifacts/recipe-quality.json` — regenerated from current 14-node recipe via `mm-harness recipe-quality build`. Verdict is pass; old WARN about `wait-limit-overlay` is gone.

## Self-Review Fixes
- `TradingViewChartTemplate.tsx:1126` — `clearLimitOrderLines` now also clears `lastLimitOrderPrices` on both exit paths. `CLEAR_TPSL_LINES` and hide no longer leave a canceled Limit price in `autoscaleInfoProvider`.
- `TradingViewChartTemplate.tsx:1144` — `updateLimitOrderLines` writes `lastLimitOrderPrices` after the clear so a new overlay still contributes to the Y-axis.
- `TradingViewChartTemplate.tsx:1137` / `1176` / `1182` — Limit remove, create, and autoscale failures use `console.error` like the existing TPSL `CLEAR_TPSL_LINES` handlers. No new test file: the overlay JS lives inside the WebView HTML string and is not executed by the RN wrapper tests. Recipe still passes after the fix.

## Self-Review Fixes
- `TradingViewChart.incremental.test.tsx:381` — add-then-clear template test: `updateLimitOrderLines` writes `lastLimitOrderPrices`, `clearLimitOrderLines` zeros it on both exits, `collectLimitOverlayPrices` reads the cache, `CLEAR_TPSL_LINES` calls the shared clearer.
- `TradingViewChart.incremental.test.tsx:427` — asserts `console.error` on Limit remove, create, and autoscale failure paths.

## Self-Review Fixes
- `TradingViewChart.incremental.test.tsx:414` — `updateLimitOrderLines` now asserts `clearLimitOrderLines()` index is before the `lastLimitOrderPrices` assignment, so restoring assignment-before-clear fails.
