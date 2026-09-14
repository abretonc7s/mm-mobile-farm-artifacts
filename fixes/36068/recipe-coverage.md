# Recipe coverage — TAT-3953

Recipe: `artifacts/recipe.json` (37 nodes)
Run: `artifacts/recipe-run/` — pass, 37/37 nodes, 0 application warnings or errors
Video run: `artifacts/recipe-run-video/` — pass, produced `artifacts/after.mp4`

## Proof targets → recipe nodes → evidence

| Proof target | Recipe node(s) | Evidence | Result |
| --- | --- | --- | --- |
| ac1 — TWAP summary lists `Runtime` | `assert-twap-summary-runtime` | state: `perps-pro-order-form-summary-twap-runtime` present | pass |
| ac1 — TWAP summary lists `Size per suborder` | `assert-twap-summary-size-per-suborder` | state: `perps-pro-order-form-summary-twap-size-per-suborder` present | pass |
| ac1 — TWAP summary drops `Est Liquidation` | `assert-twap-summary-hides-liquidation` | state: `perps-pro-order-form-summary-liquidation` `not_present` | pass |
| ac1 — TWAP summary drops `Slippage` | `assert-twap-summary-hides-slippage` | state: `perps-pro-order-form-summary-slippage` `not_present` | pass |
| ac1 — TWAP summary renders populated values | `set-twap-size`, `capture-twap-summary` | `evidence-twap-summary.png` showing `Runtime 30 mins`, `Size per suborder 0.00001 BTC` | pass |
| ac1 — TWAP `Randomize` present | `assert-twap-randomize` | state: `perps-pro-order-form-twap-randomize` visible | pass |
| ac2 — Scale field copy matches Figma | `assert-scale-start`, `assert-scale-end`, `assert-scale-order-count`, `assert-scale-size-skew` | visible text `Start (USD)`, `End (USD)`, `Order count`, `Size skew` | pass |
| ac2 — Scale form renders as designed | `capture-scale` | `evidence-scale-form.png` | pass |
| ac3 — Chase order-type description matches Figma | `assert-chase-option-copy` | visible text `Auto adjust limit order to the best price` | pass |
| ac3 — Chase form fields match Figma | `assert-chase-max-distance`, `capture-chase` | visible text `Max distance (USD)`; `evidence-chase-form.png` | pass |
| ac3 — TWAP and Scale descriptions unchanged | `assert-twap-option-copy`, `assert-scale-option-copy` | visible text for both Figma descriptions | pass |
| ac4 — Runtime ⓘ affordance exists | `assert-twap-runtime-info` | state: `perps-pro-order-form-twap-duration-info` visible | pass |

## Reasoned N/A

- **TWAP runtime range `5m – 24h` vs Figma `5m - 7d`** — not asserted against the Figma value on
  purpose. Hyperliquid caps TWAP duration at 1,440 minutes
  (`HYPERLIQUID_TWAP_LIMITS.MaxDurationMinutes`), so the app value is correct and the design value
  is unreachable. `assert-twap-runtime-label` asserts the row renders without pinning the range.
- **Chase foreground notice** — no assertion. The ticket owner chose to keep the app's existing
  copy over the non-idiomatic Figma string, so there is no behaviour change to prove.
- **Runtime tooltip contents** — no recipe node. Opening the tooltip is covered by the unit test
  `opens the runtime tooltip when the info affordance is pressed`; the recipe proves the affordance
  exists and is reachable, which is the user-visible part of the design.
- **Scale summary preview rows** — no new assertion. Scale was already Figma-conformant and is
  untouched by this change; `capture-scale` is orientation evidence only.

## Would the recipe fail if the change were reverted?

Yes, at four independent nodes: `assert-chase-option-copy` (old copy), `assert-twap-runtime-info`
(test ID absent), `assert-twap-summary-runtime` / `assert-twap-summary-size-per-suborder` (rows
absent). The two `not_present` assertions additionally fail an implementation that merely adds the
new rows without removing `Est Liquidation` and `Slippage`.

## Known limitation

`open-market` navigates without `mode: "pro"`. The harness `ui.navigate` pro-mode probe reports
`did not visibly switch Perps to pro mode. Observed: none` even when the app is demonstrably in Pro
mode (verified by screenshot and by running the action both ways). The recipe instead waits for
`perps-pro-order-form-order-type`, a test ID that exists only in the Pro order form, so a slot in
Lite mode still fails loudly at `await-order-form`.

## pr-complete re-run (2026-09-14)

PASS 37/37 in 67s (`artifacts/recipe-run/`) against the rebase onto `c131648fc6` plus the review fix `da9e1f7df8`, on Runway dev client `34814181606`. Every proof target above passed again. `evidence-chase-form.png`, `evidence-order-type-advanced.png`, `evidence-scale-form.png` and `evidence-twap-summary.png` were refreshed from this run. `before-*.png` and `after.mp4` still come from the parent run. Attempt 1 (`artifacts/recipe-run-attempt1/`) failed on a CDP bridge timeout under machine load, not on an assertion.
