# Comments report — PR 35227

PR draws resting limit orders on Lite/Pro charts. `tpslLines` includes live `currentPrice`, so the chart effect re-sends `ADD_AUXILIARY_LINES` on every tick. Ticket TAT-3530: display limit orders on the chart.

## Actionable comments

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | cursor[bot] | TradingViewChartTemplate.tsx:1185 | REAL | Stop forcing Y-axis autoscale and skip limit-line teardown when the set is unchanged |
| 2 | geositta (reply on #1) | TradingViewChartTemplate.tsx:1185 | REAL | Same as #1 (must-fix) |
| 3 | geositta | TradingViewChart.tsx:27 | OUT OF SCOPE | Nonblocking types move / TPSLLines rename; leave overlay types where they are |
| 4 | geositta | PerpsAdvancedChart.tsx:82 | REAL | Replace `as` with annotated `side` local |
| 5 | geositta | TradingViewChart.incremental.test.tsx:381 | REAL | Extract overlay helpers and add behavioral scale/line tests |

## Skipped (status-only, no reply)

5 issue comments: CLA, PR template warning, Smart E2E selection, Sonar quality gate, non-blocking performance results. No `metamask-flaky-test-detection` comments. No CHANGES_REQUESTED reviews.

## Notes

- Bugbot is correct: `updateLimitOrderLines` always `applyOptions({ autoScale: true })` after a full clear/recreate, and `updatePriceLines` always calls it. That fights the PR’s own `autoscaleInfoProvider` design.
- geositta types comment is an optional maintainability rename, not required for the ticket.

## Inherited recipe AC coverage

- Source: family-inherited TAT-3530 recipe (`artifacts/recipe.json`).
- AC1 mixed: place on-scale BTC Limit, open Pro market, wait for chart panel/content, screenshot Limit line.
- Prior parent run: 18/18 pass.

## Recipe re-validation

Harness launch/verify passed. Recipe failed twice at `ensure-session/ensure-wallet` (Login route, CDP unlock timeout). Unrelated to overlay review fixes or the origin/main rebase. Logged as environment flake.

## Totals

- Total comments triaged: 10 (5 actionable + 5 skipped status-only)
- Actionable: 4 REAL, 0 FALSE POSITIVE, 1 OUT OF SCOPE
- Commit SHA: `2a9d10c14cb2e7b1b5e71003c9d2fde69f5ffee3`
- Files changed: `PerpsAdvancedChart.tsx`, `TradingViewChartTemplate.tsx`, `TradingViewChart.incremental.test.tsx`, `limitOrderOverlay.ts`, `limitOrderOverlay.test.ts`
- Recipe re-validation: SKIPPED (reason: wallet unlock CDP timeout on Login; environment, not this branch)
- Integration status (step 3): `rebased`
