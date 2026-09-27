# Recipe coverage — PR #36881 pr-complete re-validation (HEAD 4991fa272b)

Run: `artifacts/recipe-run/` (PASS 45/45, iOS sim mm-2, HyperLiquid testnet). Terminal-on run kept at `artifacts/recipe-run-terminal-on/` (FAIL at `ac1-press-cross`, Cross disabled by the TAT-4022 gate).

| AC | Proof mode | Primary evidence | Recipe nodes | Verdict | Rationale |
|---|---|---|---|---|---|
| ac1 — flag on: Cross selectable, form reads Cross | visual | `recipe-run/screenshots/evidence-ac1-cross-sheet.png`, `evidence-ac1-cross-label.png` | `ac1-open-sheet` → `ac1-press-cross` → `ac1-wait-sheet-closed` → `ac1-wait-cross-label` → screenshots | PROVEN | A disabled Cross has no onPress, so `ac1-press-cross` fails (seen in the Terminal-on run) |
| ac2 — Cross pick places a Cross position; `marginMode` reaches order params | mixed | `assert_positions` open (matching=1), `evidence-ac2-cross-position.png` (tag Cross), `ac2-jest.log` | `ac2-press-submit` → `ac2-assert-position-open` → `ac2-wait-cross-tag` → `ac2-run-order-params-tests` | PROVEN | Venue defaults to isolated; the Cross tag only appears when `marginMode: 'cross'` is sent |
| ac3 — Cross unavailable: flag off, HIP-3, non-HyperLiquid, non-Pro, isolated-only, Terminal on | state | `ac3-jest.log`; Terminal-on device run | `ac3-run-gating-tests` → `ac3-assert-tests-pass` | PROVEN | Gating unit tests over sheet and panel; the Terminal gate was also observed on device |
| ac4 — existing cross position no longer blocks trading when Cross is available | state | `ac4-jest.log` | `ac4-run-cross-position-tests` → `ac4-assert-tests-pass` | PROVEN | Covered by form hook tests |

Teardown: BTC position closed and asserted flat; flag overrides cleared.

Overall recipe coverage: 4/4 ACs PROVEN (untestable: none, weak: 0, missing: 0)
