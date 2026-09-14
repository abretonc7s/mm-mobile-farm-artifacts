# Comments report — PR #36068

Fetched live from GitHub (not the TASK.md snapshot). HEAD after rebase + push: `7f4a9f244f`.

## PR context

Aligns TWAP / Scale / Chase Pro order UI with Figma `12187:36456`. Chase description copy, TWAP summary rows (`Runtime`, `Size per suborder` instead of Est Liquidation / Slippage), and the Runtime info affordance. Scale already matched.

## Triage table

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | cursor[bot] | PerpsProTwapFields.tsx | REAL | Already fixed on HEAD. Info `ButtonIcon` is an absolutely positioned sibling of the duration `ButtonBase` with 12pt `hitSlop`. Thread resolved; already replied. No further code change. |
| 2 | cursor[bot] | usePerpsProOrderForm.ts | REAL | Already fixed on HEAD. Suborder size below `10 ** -szDecimals` renders `<{bound} {symbol}` instead of a rounded zero. Thread resolved; already replied. No further code change. |
| 3 | github-actions[bot] | PerpsProOrderForm.test.tsx J9/J10; PerpsOrderTypeBottomSheet.test.tsx J3/J10 | FALSE POSITIVE | Suggested `beforeEach`/`afterEach` resets already exist. Historical failure rate 0/432 over 30d. Already replied. |

## Skipped (status-only, no reply)

3 comments skipped:

- `github-actions[bot]` CLA Signature Action (`5621519542`)
- `github-actions[bot]` Smart E2E Test Selection (`5665574964`)
- `sonarqubecloud[bot]` Quality Gate passed (`5665781740`) — QG passed; 1 new issue is informational and does not block merge

Own prior replies (`abretonc7s` issue comment `5661172001` and two inline replies) are not new review input.

No `CHANGES_REQUESTED` reviews. Human review: `michalconsensys` APPROVED.

## Evidence for already-fixed REAL comments

- `PerpsProTwapFields.tsx` lines 98–136: duration `ButtonBase` has no nested `ButtonIcon`. Sibling `Box.absolute` wraps `ButtonIcon` with `hitSlop={12}` and `testID={ids.TWAP_DURATION_INFO}`.
- `usePerpsProOrderForm.ts` lines 3190–3199: `if (sizePerSuborder < smallestSize) return \`<\${smallestSize.toFixed(szDecimals)} ${symbol}\``.
- `PerpsProOrderForm.test.tsx`: `beforeEach` sets `mockInputHandlesActive = true`; `afterEach` calls `jest.restoreAllMocks()`.
- `PerpsOrderTypeBottomSheet.test.tsx`: `beforeEach` calls `jest.clearAllMocks()`; no `spyOn`.

## New code this run

None. Both REAL findings were fixed in earlier commits on this branch (`fdec304329`, `7f4a9f244f` after rebase). No review-fix commit this run. Step 11 still force-pushes because step 3 rebased onto `origin/main`.

## CI note (not a review comment)

Remote HEAD `75ee7f2157` has `statusCheckRollup=FAILURE`: Android Appium swap smoke (`appium-swap-android-smoke-1`) plus the aggregator `Check all jobs pass`. This PR does not touch swap. Rebase onto `origin/main` (`f9fff6ad16`) will re-run CI after the step 11 push.

## Inherited AC coverage (step 10b)

Recipe: `temp/tasks/fix/36068-0914-231005/artifacts/recipe.json` (family-inherited, 37 nodes). Parent report: `inputs/inherited/report.md`. Coverage: `inputs/inherited/recipe-coverage.md`.

| AC | Proof | Recipe nodes |
|---|---|---|
| ac1 TWAP summary matches Figma | mixed | `assert-twap-summary-runtime`, `assert-twap-summary-size-per-suborder`, `assert-twap-summary-hides-liquidation`, `assert-twap-summary-hides-slippage`, `capture-twap-summary` |
| ac2 Scale form matches Figma | visual | `assert-scale-start/end/order-count/size-skew`, `capture-scale` |
| ac3 Chase copy and form match Figma | mixed | `assert-chase-option-copy`, `assert-chase-max-distance`, `capture-chase` |
| ac4 Runtime info affordance | state | `assert-twap-runtime-info` |

This run re-validates against `branch + origin/main` after rebase. No new recipe.

## Replies (step 12)

Already replied on a previous run. No second reply:

- review_comment `3987456324` (cursor[bot], nested info button) — replied `4003416588`, thread resolved
- review_comment `4003455849` (cursor[bot], suborder size zero) — replied `4003874493`, thread resolved
- issue_comment `5629090677` (flaky-test detection) — replied `5661172001`

Skipped status-only: CLA, Smart E2E, SonarQube QG (3). No new CHANGES_REQUESTED.

## Recipe re-validation (step 10)

Result: **PASS** — 37/37 nodes, 63s, `artifacts/recipe-run/`.

First attempt failed at `ensure-unlocked` (stability window during account-discovery timeouts). Second attempt failed at `await-order-form` because the slot was in Lite mode (`perps-mode-toggle-lite`). Neither failure is in this PR's files. Switched to Pro with `metamask.perps.ensure_mode mode=pro`, then the same inherited recipe passed.

Side findings on the passing run: 3 non-blocking app events (circuit-breaker / account discovery). Not related to TWAP/Scale/Chase copy.

## Totals (step 13)

- Total comments triaged: 3 (2 REAL, 1 FALSE POSITIVE, 0 OUT OF SCOPE)
- Skipped status-only: 3 (CLA, Smart E2E, SonarQube)
- Commit SHA for fixes: none this run (already on `fdec304329` and `7f4a9f244f`)
- Files changed this run: none
- Recipe re-validation: PASS (37/37)
- Integration status: rebased
- Pushed: `75ee7f2157` → `7f4a9f244f` with `--force-with-lease`
