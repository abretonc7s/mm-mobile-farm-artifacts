# Recipe coverage — TAT-3953 (PR-complete re-validation)

Recipe: `artifacts/recipe.json` (37 nodes, family-inherited)
Run: `artifacts/recipe-run/` — pass, 37/37 nodes, 63s
HEAD: `7f4a9f244f` (rebased onto `origin/main` `f9fff6ad16`)

## Proof targets → recipe nodes → evidence

| Proof target | Recipe node(s) | Evidence | Result |
| --- | --- | --- | --- |
| ac1 — TWAP summary lists `Runtime` | `assert-twap-summary-runtime` | state: `perps-pro-order-form-summary-twap-runtime` present | pass |
| ac1 — TWAP summary lists `Size per suborder` | `assert-twap-summary-size-per-suborder` | state: `perps-pro-order-form-summary-twap-size-per-suborder` present | pass |
| ac1 — TWAP summary drops `Est Liquidation` | `assert-twap-summary-hides-liquidation` | state: `perps-pro-order-form-summary-liquidation` `not_present` | pass |
| ac1 — TWAP summary drops `Slippage` | `assert-twap-summary-hides-slippage` | state: `perps-pro-order-form-summary-slippage` `not_present` | pass |
| ac1 — TWAP summary renders populated values | `set-twap-size`, `capture-twap-summary` | `artifacts/recipe-run/screenshots/evidence-twap-summary.png` | pass |
| ac1 — TWAP `Randomize` present | `assert-twap-randomize` | state: `perps-pro-order-form-twap-randomize` visible | pass |
| ac2 — Scale field copy matches Figma | `assert-scale-start`, `assert-scale-end`, `assert-scale-order-count`, `assert-scale-size-skew` | visible text `Start (USD)`, `End (USD)`, `Order count`, `Size skew` | pass |
| ac2 — Scale form renders as designed | `capture-scale` | `artifacts/recipe-run/screenshots/evidence-scale-form.png` | pass |
| ac3 — Chase order-type description matches Figma | `assert-chase-option-copy` | visible text `Auto adjust limit order to the best price` | pass |
| ac3 — Chase form fields match Figma | `assert-chase-max-distance`, `capture-chase` | visible text `Max distance (USD)`; `artifacts/recipe-run/screenshots/evidence-chase-form.png` | pass |
| ac3 — TWAP and Scale descriptions unchanged | `assert-twap-option-copy`, `assert-scale-option-copy` | visible text for both Figma descriptions | pass |
| ac4 — Runtime info affordance exists | `assert-twap-runtime-info` | state: `perps-pro-order-form-twap-duration-info` visible | pass |

## Re-validation notes

First attempt failed at `ensure-unlocked` (wallet stability window). Second attempt failed at `await-order-form` because the slot was in Lite mode. After `metamask.perps.ensure_mode mode=pro`, the same inherited recipe passed 37/37. Those failures are not in this PR's files.

## Reasoned N/A

Same as the parent run: TWAP runtime range stays `5m – 24h` (Hyperliquid cap), Chase foreground notice keeps the app wording, runtime tooltip copy is covered by a unit test, Scale was already Figma-conformant.

## Would the recipe fail if the change were reverted?

Yes, at `assert-chase-option-copy`, `assert-twap-runtime-info`, `assert-twap-summary-runtime`, and `assert-twap-summary-size-per-suborder`. The two `not_present` assertions also fail an implementation that only adds rows.
