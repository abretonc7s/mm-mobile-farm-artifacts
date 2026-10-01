# Recipe coverage — PR #36881 (Cross selectable in Pro)

Rebased head `40cdf2f5bce` (onto `origin/main` `3b1fd8f99e8`). iOS sim mm-6, HyperLiquid testnet, run `artifacts/recipe-run/` 45/45 PASS.

One recipe delta against the inherited copy (`recipe.inherited.json`): `setup-flag` also pins `perpsTerminalBackendEnabled` off. Live remote config now serves it on (`minimumVersion 8.3.0`), and the PR keeps Cross off on the Terminal path until TAT-4022. Earlier device evidence already ran with it off (PR body). Teardown clears every override as before.

| AC | Proof mode | Primary evidence | Recipe nodes | Verdict | Rationale |
|---|---|---|---|---|---|
| ac1 — flag on: Cross selectable, form reads Cross | visual | `evidence-ac1-cross-sheet.png`, `evidence-ac1-cross-label.png` | `ac1-open-sheet` → `ac1-press-cross` → `ac1-wait-sheet-closed` → `ac1-wait-cross-label` → screenshots | PROVEN | `ui.wait_for` text `Cross` on `perps-pro-order-form-margin-mode` before capture; both PNGs read and show the claim. |
| ac2 — Cross pick places a Cross position; `marginMode` reaches order params | mixed | `assert_positions` open (matching=1), `evidence-ac2-cross-position.png`, `test-logs/ac2-jest.log` (40 passed) | `ac2-press-submit` → `ac2-assert-position-open` → `ac2-wait-cross-tag` → `ac2-run-order-params-tests` | PROVEN | Venue state asserted after submit; `cross-margin-tag-pro-BTC` visible; teardown closed it and asserted flat. |
| ac3 — Cross unavailable: flag off, HIP-3, non-HyperLiquid, non-Pro, isolated-only | state | `test-logs/ac3-jest.log` (15 passed) | `ac3-run-gating-tests` → `ac3-assert-tests-pass` | PROVEN | Focused Jest inside the recipe with exit-code assertion. Side proof on device: with Terminal backend on (attempt 2), Cross rendered with no `onPress`. |
| ac4 — existing cross position no longer blocks trading when Cross is available | state | `test-logs/ac4-jest.log` (3 passed) | `ac4-run-cross-position-tests` → `ac4-assert-tests-pass` | PROVEN | Focused Jest with exit-code assertion. |

Overall recipe coverage: 4/4 ACs PROVEN (untestable: none, weak: 0, missing: 0).
