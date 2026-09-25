# Comments report — PR #36775

## Triage

| # | Source | Author | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | review_comment 4091373443 | cursor[bot] | PerpsAdjustMarginView.tsx (fresh cap resets on PnL ticks) | REAL (already fixed) | Fixed in earlier rounds (c556868d643, 6421cb99d5b); two replies posted, thread resolved. Already replied, no new reply. |
| 2 | operator-relayed private review (gpt-6-sol, HEAD 6421cb99, REQUEST_CHANGES, not posted) | operator | PerpsAdjustMarginBottomSheet.tsx:559 | REAL | Zero-removable explanation now wins over a validation error on a retained amount and over an earlier submission error (bottom sheet); full screen drops the stale "exceeds max" error when nothing is removable. Tests cover retained amount → limit 0 (both screens) and failed submission → limit 0 (bottom sheet). |

Skipped status-only automation without reply: 4 issue comments (CLA, smart-e2e selection, SonarCloud gate passed, non-blocking perf results with `no_performance_metrics` on add-funds / open-close flows that this PR does not touch).
No CHANGES_REQUESTED reviews on GitHub.

## Notes
- Step 3: rebased cleanly onto origin/main (12 commits replayed); package.json/yarn.lock changed on main, ran `yarn install --immutable`.
- New tests fail on the pre-fix source (3 failed) and pass with the fix (78/78).

## Recipe re-validation (step 10)
- Inherited `artifacts/recipe.json` was stale (still carried the cross-margin nodes moved to #36782 and lacked the screen-variant pin); saved as `recipe.stale-inherited.json`. Used the current PR-body recipe as the base, unchanged node IDs/ACs.
- Inherited AC coverage: AC1 Max removal accepted by exchange; AC2 zero-removable explained on a fresh SOL position; AC3 focused unit tests.
- Added AC4 (full screen, control variant) and AC5 (bottom sheet, treatment variant): add $20, keep Max in the form, `ac4/ac5-drain-live-limit` removes all but ~$1 of exchange-removable margin via the controller from outside the form (helper `artifacts/scripts/drain-btc-margin.sh`, uses the harness cdp-bridge; asserts post-drain state), then require the zero explanation visible and no stale error.
- Negative control (source fix stashed, app restarted): `ac5-assert-explanation` FAILED (bottom sheet hid the explanation behind the validation error) and `ac4-assert-no-stale-error` FAILED (full screen showed "Amount exceeds maximum removable margin" beside the explanation). Logs: `artifacts/probes/neg-p3-run`, `artifacts/probes/neg-p2-run`.
- Final run on fixed code: PASS 98/98 in 339s (`artifacts/recipe-run/report.md`).
- Account state: BTC isolated long on Trading (testnet) reused; margin added/removed by the recipe; SOL opened and closed by the recipe. No stray positions left open other than the BTC fixture position.
- Metro stalled ~1 min after `yarn install` (re-crawl); recovered on its own, then `mm-harness launch ios --verify` passed. No rebuild.

## Local gate (step 9)
- Scoped ESLint: pass. `yarn format:check`: pass. Affected tests: 78/78 (3 new tests fail on pre-fix source).
- Full `yarn lint:tsc` not run: slot rules forbid full-project TypeScript from the worker pane, and no language server is installed; left to CI.

## Independent review (gpt-6-sol, fresh read-only Codex session)
- HEAD 650798f5e59: VERDICT: APPROVE, no findings (`artifacts/codex-review-650798f.md`).

## CI check-pr-max-lines (job 107693385985, run 36017410599)
- At 650798f5e59: 1046+53 = 1099 counted lines (> 1000).
- b146b0351f5 (test-only) removes genuine duplication, with no source or recipe evidence removed:
  - The fresh-limit release rules (PnL re-delivery, size/collateral change, hold window) were tested through both screens, but they live in `usePerpsFreshRemovalLimit`. They are now tested once there (`usePerpsFreshRemovalLimit.test.ts`, which adds entry and leverage changes). Each screen keeps one slider wiring test; the bottom sheet keeps its mode-switch test.
  - The older "blocks a retained amount" and "hides the zero-state explanation" tests folded into the zero-limit transition tests. These now assert no explanation before the drop, then explanation, no error, Confirm disabled and not called.
  - The seven submit-through cases of the pre-submit re-read are now one `it.each` table; every row also asserts the `skipCache` read and that `onAmountChanged` is not called.
- Result: 908+53 = 961 counted lines (−138). Focused suites: 102/102. The transition tests still fail on the pre-fix source (3 failed).
