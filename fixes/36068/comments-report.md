# PR #36068 — comments report

## Triage

| # | Source | Author | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | review_comment 3987456324 | cursor[bot] | PerpsProTwapFields.tsx:124 | REAL | Move runtime info `ButtonIcon` out of the duration `ButtonBase` (absolute sibling in a relative container) and add `hitSlop`. In RN the innermost touchable wins the responder, so a double-fire is unlikely, but the nested button collapses into the parent's accessibility node (unreachable for screen readers) and has a tiny tap target. |
| 2 | issue_comment 5629090677 | github-actions[bot] (flaky-test-detection) | PerpsProOrderForm.test.tsx, PerpsOrderTypeBottomSheet.test.tsx | FALSE POSITIVE | Every suggested safeguard already exists at HEAD: `mockInputHandlesActive = true` in `beforeEach` (line 194), `jest.restoreAllMocks()` in `afterEach` (line 200), `jest.clearAllMocks()` in `beforeEach` of the bottom-sheet test (line 155). 0 failures across 489 runs / 30d. |

Skipped status-only automation (no reply): 2 (CLA signature, SonarCloud quality gate). Review body 5176678532 (cursor[bot] summary) covered by #1.
No CHANGES_REQUESTED reviews.

## Inherited AC coverage (parent run f3085f27)

Recipe `artifacts/recipe.json` (37 nodes, identical to inherited) passed 37/37 in the parent run: ac1 TWAP summary Runtime / Size per suborder with Est Liquidation and Slippage absent (state + screenshot), ac2 Scale field copy (visible text + screenshot), ac3 Chase description and Max distance (visible text + screenshot), ac4 Runtime ⓘ affordance (`perps-pro-order-form-twap-duration-info` visible). Deliberate deviations: runtime range `5m – 24h` (Hyperliquid 1,440-minute cap) and the existing Chase foreground-notice copy.

## Recipe re-validation — PASS (37/37)

- The first launch after the rebase failed. The mmdev-3 iOS dev client (Runway run `34547211786`, Sep 11 00:36) predates main's native dependency bump in #35615 (`react-native-reanimated` 4.5.3, `react-native-worklets` 0.10.4, gesture-handler 2.32), so the app threw `Exception in HostFunction` / `"MetaMask" has not been registered`. `--clear-metro` did not help.
- Fix: refreshed only `macwork-mmdev-3` with `runway-update --slots macwork-mmdev-3 --run 34814181606`. That Expo Dev Build ran on main `c131648fc6`, the exact rebase base. The skill's own "latest" resolved a stale Sep 4 run (`33931142729`), so the run id was pinned.
- Attempt 1 (`artifacts/recipe-run-attempt1/`): 19/20. `assert-twap-summary-hides-slippage` failed with `Mobile CDP bridge command timed out ... last result=null` at load average ~60–112, which is a bridge timeout, not a rendered Slippage row. A follow-up probe could not even find the Runtime row, and harness status reported `no-bridge`.
- After `mm-harness launch ios --verify` (no rebuild), attempt 2 (`artifacts/recipe-run/`) passed 37/37 in 67s: Chase copy, TWAP Runtime ⓘ (`perps-pro-order-form-twap-duration-info` visible after the fix), Runtime and Size per suborder present, Est Liquidation and Slippage `not_present`, Scale copy, Chase Max distance.
- Screenshots `evidence-twap-form.png` / `evidence-twap-summary.png` show the ⓘ icon still aligned on the Runtime label row after moving it out of the button.

## Summary

- Total comments: 2 actionable (1 REAL, 1 FALSE POSITIVE, 0 OUT OF SCOPE). Skipped 2 status-only bot comments (CLA, SonarCloud).
- Fix commit: `da9e1f7df8ba59b27e00628937256bc55dd25a70`, pushed with `--force-with-lease` against the pre-rebase remote SHA `a193f031bd`.
- Files changed:
  - `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/PerpsProTwapFields.tsx`
  - `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/PerpsProTwapFields.test.tsx`
- Local gate: changed-file ESLint pass, Prettier check pass, LSP diagnostics clean on both files; Jest `PerpsProTwapFields`, `PerpsProOrderForm` and `PerpsOrderTypeBottomSheet` 190/190 pass. Full `lint:tsc` not run (forbidden in worker slots); CI covers it.
- Replies: inline reply on 3987456324 (thread resolved); consolidated issue comment 5661172001 for the flaky-test detection triage.
- Recipe re-validation: PASS 37/37 (`artifacts/recipe-run/`) after the Runway refresh.
- Integration status: `rebased` (`artifacts/integration-status.txt`). Clean rebase onto `origin/main` c131648fc6, no conflicts, `yarn install --immutable` re-run.
