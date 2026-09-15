# Recipe coverage — TAT-3561

| AC | Mode | Primary evidence | Recipe nodes | Verdict | Rationale |
| --- | --- | --- | --- | --- | --- |
| AC-TP1 | visual | `after-ac-defaults.png` | wait-tp-badge, capture-defaults | PROVEN | TP badge visible, screenshot shows green `+` |
| AC-TP2 | visual | `after-ac-tp-minus-empty.png` | toggle-tp-minus, toggle-tp-plus | PROVEN | Tap flips `+` to `−` and back |
| AC-TP3 | visual | `after-ac-tp-minus-empty.png` | wait-tp-loss-placeholder, wait-tp-profit-placeholder | PROVEN | Empty TP reads `% Loss` then `% Profit` |
| AC-TP4 | mixed | form unit test `sets the take profit badge from a typed trigger price on an open position` | (price typing covered indirectly via presets) | PROVEN | Live recipe is new-order; opposite-sign from a typed price needs an open position. Hook test covers it. |
| AC-TP5 | mixed | `after-ac-tp-plus-filled.png`, `after-ac-tp-minus-filled.png` | press-tp-preset-25, toggle-tp-minus-filled | PROVEN | `+25%` sets trigger $2723.7 above market; flip to `−` sets $2304.64 |
| AC-TP6 | mixed | form unit test `accepts a take profit at a smaller loss on a long already underwater` | none | PROVEN | Live PnL is not a recipe input. Hook test uses entry 50k / current 40k / −10% TP, no error. |
| AC-TP7 | mixed | `after-ac-tp-minus-filled.png` | wait-tp-error | PROVEN | New long + negative TP shows "Take profit must be above current price" |
| AC-TP8 | visual | `after-ac-defaults.png`, `after-ac-tp-minus-empty.png` | capture-defaults, capture-tp-minus-empty | PROVEN | `+` is success green, `−` is error red |
| AC-SL1 | visual | `after-ac-defaults.png` | wait-sl-badge, capture-defaults | PROVEN | SL badge visible, screenshot shows red `−` |
| AC-SL2 | visual | `after-ac-sl-plus-empty.png` | toggle-sl-plus-empty | PROVEN | Tap flips SL `−` to `+` |
| AC-SL3 | visual | `after-ac-sl-plus-empty.png` | wait-sl-gain-placeholder | PROVEN | Empty SL reads `% Gain` |
| AC-SL4 | mixed | form unit test `sets the stop loss badge from a typed trigger price on an open position` | (presets snap the badge) | PROVEN | Same as TP4: hook test on an open position |
| AC-SL5 | mixed | `after-ac-sl-plus-filled.png` | press-sl-preset-5, toggle-sl-plus-filled | PROVEN | `−5%` fills a below-market trigger; flip to `+` sets $2556.05 |
| AC-SL6 | mixed | form unit test `accepts a stop loss at a smaller gain on a long already in profit` | none | PROVEN | Hook test uses entry 50k / current 60k / +5% SL, no side error |
| AC-SL7 | mixed | `after-ac-sl-plus-filled.png` | wait-sl-error | PROVEN | New long + positive SL shows "Stop loss must be below current price". Liquidation still checked in hook test. |
| AC-SL8 | visual | `after-ac-defaults.png`, `after-ac-sl-plus-empty.png` | capture-defaults, capture-sl-plus-empty | PROVEN | SL `−` error red, SL `+` success green |

Overall recipe coverage: 16/16 ACs PROVEN (untestable: none, weak: 0, missing: 0). TP4/TP6/SL4/SL6 use focused hook tests for the live-PnL-dependent half; the recipe proves the same controls on a new-order Auto Close sheet.
