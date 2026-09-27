# Recipe coverage — PR A (Cross selectable in Pro)

| AC | Proof mode | Primary evidence | Recipe nodes | Verdict | Rationale |
|---|---|---|---|---|---|
| ac1 — flag on: Cross selectable, form reads Cross | visual | `evidence-ac1-cross-sheet.png`, `evidence-ac1-cross-label.png` (before: `before-ac1-cross-sheet.png`) | `ac1-open-sheet` → `ac1-press-cross` → `ac1-wait-sheet-closed` → `ac1-wait-cross-label` → screenshots | PROVEN | Pressing a disabled Cross leaves the sheet open, so `ac1-wait-sheet-closed` and the Cross label wait fail without the change |
| ac2 — Cross pick places a Cross position; `marginMode` reaches order params | mixed | `assert_positions` state, `evidence-ac2-cross-position.png`, `test-logs/ac2-jest.log` | `ac2-press-submit` → `ac2-assert-position-open` → `ac2-wait-cross-tag` → `ac2-run-order-params-tests` | PROVEN | Venue defaults to isolated; the Cross tag only appears when `marginMode: 'cross'` is sent |
| ac3 — Cross unavailable: flag off, HIP-3, non-HyperLiquid, non-Pro, isolated-only | state | `test-logs/ac3-jest.log` | `ac3-run-gating-tests` → `ac3-assert-tests-pass` | PROVEN | Hidden gating; unit tests over sheet and panel |
| ac4 — existing cross position no longer blocks trading when Cross is available | state | `test-logs/ac4-jest.log` | `ac4-run-cross-position-tests` → `ac4-assert-tests-pass` | PROVEN | Needs a pre-existing cross position; covered by form hook tests |

Overall recipe coverage: 4/4 ACs PROVEN (untestable: none, weak: 0, missing: 0)
