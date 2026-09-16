# PR #36332 — comment triage

PR: https://github.com/MetaMask/metamask-mobile/pull/36332
Branch: `TAT-3931-fix-fix-perps-activity-multi-fill`
Integration status (step 3): `rebased` — 8 branch commits replayed onto `origin/main` (`f87b2e60f6`), clean, linear. Pre-rebase remote SHA `c767575ba1bcdc166d0670d1fb7dfdbd5078cee2`, new HEAD `1da65345c1`.

## PR context (step 5)

`aggregateFillsByOrder` replaces `aggregateFillsByTimestamp`: fills group by asset + direction
category + order id, with close-category fills additionally seeded by the second they landed in
(HyperLiquid splits a triggered TP/SL into several child orders) and a union step linking
per-second close groups that share an order id. The aggregated row sums size/PnL/fee, takes VWAP
price, the latest fill's timestamp and metadata, and `startPosition` from the largest magnitude
any fill saw. Three surfaces render from this one transform. Also adds testIDs to
`PerpsMarketTradesList` and `PerpsRecentActivityList`.

## Triage

| # | Source | Author | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | review_comment `4024862745` | cursor[bot] | `app/components/UI/Perps/utils/transactionTransforms.ts:200` | REAL | Already fixed in `c767575ba1` (rebased to `1da65345c1`) before this run; author already replied in comment `4024979881` and the thread is resolved. No new code change, no duplicate reply. |
| 2 | issue_comment `5696372918` | github-actions[bot] (perf results) | — | FALSE POSITIVE | Non-blocking perf report. Both failures are `no_performance_metrics` (BrowserStack metric collection, not an app regression); the only flagged profiling metric is Slow frames +43.5% on "Perps open position and close it". This PR changes a pure fill-grouping transform that runs on history data — it adds no work to a render or network path on the open/close flow, and CPU/memory/app-size all moved down or flat. Device-run frame noise, not caused by this diff. |
| 3 | issue_comment `5696168961` | sonarqubecloud[bot] | — | OUT OF SCOPE | Quality Gate **passed** (100% coverage on new code, 0% duplication, 0 security hotspots). The "3 New issues" link is informational and does not gate. |
| 4 | issue_comment `5695737320` | github-actions[bot] (CLA) | — | skipped (status-only automation) | — |
| 5 | issue_comment `5696046958` | github-actions[bot] (Smart E2E selection) | — | skipped (status-only automation) | — |

- Status-only automation comments skipped without reply: **2** (CLA, Smart E2E selection).
- `CHANGES_REQUESTED` reviews: **0**.
- `metamask-flaky-test-detection` comments: **0** (none posted on this PR).
- Human review comments: **0** (the only `abretonc7s` review is the author's own, empty body, carrying the reply to comment 1).

## Verification of comment 1 against current HEAD

`transactionTransforms.ts` picks `aggregatedStartPosition` by largest absolute magnitude across
the group rather than by list position, so tied-millisecond fills from one book sweep no longer
decide it. The remaining `latestFill` selection only supplies fields that are identical across
fills of one order group when timestamps tie (orderId, side, direction, feeToken, orderType,
timestamp). The reported flip-sizing defect is closed.

## CI status

All required checks pass on the pre-rebase tip (unit, integration, component-view, lint, tsc,
format:check, Appium Android smoke incl. SmokePerps, SonarCloud quality gate, Cursor Bugbot).
The only non-green entry is `policy-bot` — pending human review approval, which is what
`mergeStateStatus=BLOCKED` reflects. Not worker-actionable.

## Recipe re-validation (step 10)

`RECIPE_SOURCE=family-inherited` — trusted provenance, recipe already seeded at
`artifacts/recipe.json`. No gating pass required, no migration performed (the recipe's two
`command` nodes write their logs into the parent run's `temp/tasks/fix/tat-3931-0916-154555/artifacts/`,
which is present in this clone, so the inherited paths still resolve).

**Inherited AC coverage** (from `inputs/inherited/recipe-coverage.md`): 4/4 ACs PROVEN.
- AC1 — multi-fill **close** summed into one row: `state` proof via `ac1-*` transform tests.
- AC2 — multi-fill **open** summed into one row: `mixed` proof, asset detail screenshot plus the
  `8.29 SOL` / `-$1.15` assertions.
- AC3 — multi-fill **flip** summed into one row keeping the opening position size: `state` proof
  via the `ac3-*` targeted flip test.
- AC4 — all three surfaces (Activity page Perps > Trades, Perps home, asset detail): `mixed` proof.

**Runtime health**: `launch ios --verify` passed (fixture READY, 4 accounts), `doctor --expect-live`
reported metro up, bridge up, capture available, device `mm-1` booted.

**Account convergence (step 10c2)**: `metamask.perps.read_positions` returned `count: 0` after
unlocking — no stray positions or orders to close, and nothing was mutated. The recipe's data
prerequisite (Hyperliquid testnet order `60252966679`, the 4-fill 8.29 SOL SOL long on
`0x316B…01fa`) is *history*, not live state, and is still inside the fills lookback window, which
the run's `8.29 SOL` / `-$1.15` assertions confirm.

**Result: PASS — 27/27 nodes, 0 failed**, against `branch + origin/main` merged (HEAD `1da65345c1`).
Artifacts: `artifacts/recipe-run/` (report.md, summary.json, trace.json, screenshots).
Side findings: 109 application warning/error events flagged for review, non-blocking and the same
order of magnitude the parent run recorded (109) — unchanged by the rebase.

## Replies posted (step 12)

- review_comment `4024862745` (cursor[bot]) — **already replied**. The author's reply
  `4024979881` already cites the fix commit, and the review thread `PRRT_kwDOCG4DHc6i4X50` is
  already `isResolved: true`. No duplicate reply, no re-resolve.
- issue_comments (perf results + SonarCloud + the Bugbot finding recap) — one consolidated
  top-level triage posted: https://github.com/MetaMask/metamask-mobile/pull/36332#issuecomment-5697742337
- CLA and Smart E2E selection — status-only automation, no reply.

## Summary (step 13)

- **Total comments triaged: 5** — 1 REAL (already fixed before this run), 1 FALSE POSITIVE,
  1 OUT OF SCOPE, 2 status-only automation skipped without reply.
- **Commit SHA for fixes: none.** No review fix was required this run: the only REAL finding was
  already closed at HEAD by `c767575ba1`. No empty commit created.
- **Files changed by this run: none.** The push published the rebase only.
  `c767575ba1` → `1da65345c1` (8 commits replayed onto `origin/main` `f87b2e60f6`), pushed with
  `--force-with-lease` after confirming the remote had not moved.
- **PR diff vs `origin/main`** (unchanged in content by the rebase):
  - `app/components/UI/Perps/utils/transactionTransforms.ts`
  - `app/components/UI/Perps/utils/transactionTransforms.test.ts`
  - `app/components/UI/Perps/Perps.testIds.ts`
  - `app/components/UI/Perps/components/PerpsMarketTradesList/PerpsMarketTradesList.tsx`
  - `app/components/UI/Perps/components/PerpsRecentActivityList/PerpsRecentActivityList.tsx`
- **Recipe re-validation: PASS** (27/27 nodes, 0 failed).
- **Integration status: `rebased`** (`artifacts/integration-status.txt`).
- **Local gate**: scoped ESLint `--max-warnings=0` clean, `lint:tsc` exit 0, `format:check` clean,
  `transactionTransforms.test.ts` 126/126 pass, `PerpsMarketTradesList` + `PerpsRecentActivityList`
  67/67 pass. Working tree clean throughout.

## Evidence package

`artifacts/evidence-manifest.json` keeps the inherited before/after framing (the pairs already in
the PR body). The `after-*.png` files are **this run's fresh captures on the rebased branch**
(`recipe-run/screenshots/`), not the parent run's — the Activity page now reads
`Closed long 8.29 SOL` / `Opened long 8.29 SOL −$1.15` as two rows under Today, with the unrelated
BTC and ETH trades still separate. The `before-*.png` and the two videos are the parent run's
pre-fix captures, since the defect cannot be re-staged without reverting the fix.
`artifacts/recipe-coverage.md` and `artifacts/recipe-quality.json` carry the inherited verdicts
forward (the recipe is byte-identical) with a re-validation section appended to the coverage doc.
