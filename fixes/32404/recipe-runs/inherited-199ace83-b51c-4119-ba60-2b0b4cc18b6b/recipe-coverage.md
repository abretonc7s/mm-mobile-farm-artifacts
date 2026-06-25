# Recipe coverage — TAT-3398

| AC | Proof mode | Primary evidence | Recipe nodes | Verdict | Rationale |
| --- | --- | --- | --- | --- | --- |
| AC1 — defaults: TP `+`, SL `−` | visual + state | `after-ac1-default-signs.png` | `ac1-tp-badge`, `ac1-sl-badge` (wait_for exact text), `ac1-screenshot` | PROVEN | Badge text read via fiber (`getTextByTestId`) asserts exact `+`/`−`; screenshot shows both badges. |
| AC2 — tap TP `+`→`−`, value kept, trigger recomputed below entry | mixed | `after-ac2-tp-filled-plus.png` → `after-ac2-tp-toggled-kept.png` | `ac2-fill-preset`, `ac2-filled-screenshot`, `ac2-toggle`, `ac2-badge-minus`, `ac2-flipped-screenshot` | PROVEN | Badge flip asserted by exact text; before/after pair shows value `25` kept and trigger moving from above entry ($1872) to below entry ($1414, "Expected loss"). Unit test asserts kept magnitude + recomputed price. |
| AC3 — tap TP `−`→`+`, value kept | state | (badge text) | `ac3-toggle-back`, `ac3-badge-plus` | PROVEN | `ac3-badge-plus` wait_for exact `+`. Unit test asserts value `25` kept and trigger back above entry. |
| AC4 — tap SL `−`→`+`, value kept, trigger recomputed above entry | mixed | `after-ac4-sl-toggled.png` | `ac4-fill-preset`, `ac4-toggle`, `ac4-badge-plus`, `ac4-screenshot` | PROVEN | Badge flip asserted by exact text; screenshot shows SL badge `+`, value `5` kept and trigger above entry ($1657, "Expected profit" — a positive stop loss). Unit test asserts kept + recompute. |
| AC5 — preset flips badge to its sign | mixed | `after-ac5-preset-flips-sign.png` | `ac5-toggle-to-minus`, `ac5-confirm-minus`, `ac5-press-positive-preset`, `ac5-badge-flipped`, `ac5-screenshot` | PROVEN | Badge starts `−`, +25% preset tap flips it to `+` (asserted by exact text); screenshot shows `+` with filled value. |
| AC6 — negative TP → negative RoE trigger | mixed | `after-ac6-negative-tp-trigger.png` | `ac6-toggle-to-minus`, `ac6-confirm-minus`, `ac6-enter-roe`, `ac6-settle`, `ac6-screenshot` | PROVEN | Screenshot shows badge `−`, RoE 10%, trigger $1582.65 below current $1,666.3 (Expected loss) with Set enabled. Unit test asserts trigger < entry and validity passes. |
| AC7 — reopen resets to defaults | state + visual | `after-ac7-reset-defaults.png` | `ac7-back`, `ac7-wait-order-view`, `ac7-reopen`, `ac7-wait-sheet`, `ac7-tp-reset`, `ac7-sl-reset`, `ac7-screenshot` | PROVEN | After dismiss + reopen, badges asserted back to `+`/`−` by exact text; screenshot confirms. |

Overall recipe coverage: 7/7 ACs PROVEN (untestable: none, weak: 0, missing: 0)
