# Recipe Coverage Audit

| # | AC (verbatim) | Proof mode | Primary evidence | Recipe nodes (IDs) | Visual file if any | Evidence verdict | Justification |
|---|---------------|------------|------------------|---------------------|--------------------|------------------|---------------|
| 1 | Open orders (limit, TP, SL) on wallet home, perps home and perp market detail screens display the same number of decimals for trigger/limit price as the displayed market price (examples: 0 for BTC, 2 for CL, 6 for CHIP). | mixed | trace + screenshot | `ac1-open-chip-order-details`, `ac1-wait-order-details`, `ac1-assert-chip-limit-price`, `ac1-screenshot-chip-order-details` | `after-ac1-chip-order-details.png` | PROVEN | `trace.json` shows every AC1 node passed, and `ac1-assert-chip-limit-price` returned `found: true` for `$0.001234`. The screenshot visibly shows the CHIP order details Price row rendering `$0.001234`, matching six-decimal market precision. |

Recipe scope note: the executable recipe proves the low-priced CHIP limit-order details path. It does not directly exercise wallet home, perps home, market detail compact rows, TP, or SL surfaces. Those broader AC surfaces are covered by targeted Jest assertions in `PerpsCompactOrderRow.test.tsx` and `PerpsOrderDetailsView.test.tsx`.

Forbidden pattern scan: no banned `switch/default`, skip-reason value, wait-over-500 substitute, missing AC-prefixed node, missing mixed-mode screenshot, or ES6 eval syntax was found in `recipe.json`.

Overall recipe coverage: 1/1 recipe-scoped executable checks PROVEN (untestable: none, weak: 0, missing: 0). Broader AC surfaces not exercised by the recipe are explicitly listed in `recipe.json` coverage notes and covered by unit tests.
