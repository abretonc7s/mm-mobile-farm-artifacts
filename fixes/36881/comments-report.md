# PR #36881 — comments report (pr-complete round, HEAD 4991fa272b)

| # | Source | Author | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | review_comment 4110687938 | cursor[bot] | usePerpsProOrderForm.ts:936 | REAL (already fixed) | Fixed earlier in 15ab6825f3 (`useHasExistingPosition` provider-scoped, verified at hooks/useHasExistingPosition.ts:72-74); author already replied; thread resolved. No new reply. |
| 2 | issue_comment 5844369405 | deeeed | usePerpsProOrderForm.ts:885 | REAL (already fixed) | Fixed earlier in 9398d2f0e53 (`usePerpsMarketData` takes `providerId`; form passes `market.providerId` at usePerpsProOrderForm.ts:884); author already replied 5844538507. Asked for final-HEAD device re-check → covered by step 10 recipe run. |
| 3 | issue_comment 5845770720 | github-actions[bot] | perf tests | OUT OF SCOPE | Non-blocking perf run, `no_performance_metrics` on both Perps scenarios; baseline on main also failing. No reply (status automation). |
| 4 | issue_comment 5845172803 | github-actions[bot] | fixture update | OUT OF SCOPE (resolved) | Earlier fixture-update failure; later run succeeded ("E2E fixtures updated"). Already covered in author follow-up 5846397436. |

Skipped status-only automation without reply: 6 (CLA, smart-E2E selection, codecov, sonarcloud, fixture-started x2, fixture-updated).
REQUEST_CHANGES reviews: none.
CI on 4991fa272b: all checks green; only `policy-bot` pending (needs reviewer approval).

## Code changes this round
None — every actionable comment was already fixed and replied to on the current HEAD.

## Recipe re-validation (step 10) — PASS 45/45 on 4991fa272b
Inherited coverage: AC1 Cross selectable + form label reads Cross (device), AC2 Cross order places a BTC position tagged Cross (device + state assertion `assert_positions open`, teardown asserts flat), AC2/AC3/AC4 Jest nodes (order params carry marginMode; gating off for flag-off/HIP-3/Lighter/isolated-only; existing cross position).

- Run 1 (`artifacts/recipe-run-terminal-on/`): FAIL at `ac1-press-cross` — "no onPress prop". Live flags: `perpsTerminalBackendEnabled` = `{enabled:true, minimumVersion:8.3.0}` remotely. Cross is disabled by design while Terminal is on (PanelTSX gate `!usesTerminal`, added in this PR for TAT-4022). Not a regression; confirms that gate on device.
- Recipe precondition update: `setup-flag` now also pins `perpsTerminalBackendEnabled` off (original kept as `recipe.pre-terminal-gate.json`). Teardown `metamask.feature_flags.clear` drops both overrides.
- Run 2 (`artifacts/recipe-run/`): PASS 45/45. Screenshots checked: Cross sheet selectable, margin control reads Cross, BTC position "Position margin used · Cross", Est. Liquidation `--`.
- Account state: setup nodes found 0 BTC positions and 0 BTC orders; the test position was closed at teardown (assert flat passed). Nothing else touched.
- Slot prep: created `temp/tasks/feat/tat-3524-0925-174920/artifacts/test-logs/` because the recipe's Jest nodes write logs there.

## Local checks (step 9)
No working-tree changes. The PR's 6 test suites pass (445 tests). `lint:tsc` not run locally (slot rules forbid full-project tsc in the worker pane); CI passed it on this exact SHA.

## Totals
Total actionable comments: 4 (2 REAL, already fixed earlier; 0 FALSE POSITIVE; 2 OUT OF SCOPE). No new commit this round. Files changed: none. Integration: skipped (already on origin/main). Recipe: PASS.

## Replies (step 12)
- 4110687938 (cursor[bot]): already replied (4111117778) and thread resolved; no new reply.
- 5844369405 (deeeed): already replied (5844538507). Posted the device re-check at final HEAD: https://github.com/MetaMask/metamask-mobile/pull/36881#issuecomment-5852127495
- Perf/fixture bot comments: status automation, no reply.
