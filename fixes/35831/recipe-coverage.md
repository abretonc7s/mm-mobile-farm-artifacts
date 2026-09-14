# Recipe coverage

Scope: PR-complete re-validation of the inherited existing-position Cross display recipe (`artifacts/recipe.json`) against rebased HEAD `2204c40070c`. Proof mode planned: mixed state + visual. The recipe ran (`recipe-run/`) and stopped at `require-cross`, so every display criterion below is N/A with a reason. A first attempt (`recipe-run-cdp-timeout/`) hit `CDP_TIMEOUT` in `environment` and was retried once. Earlier passing runs (`recipe-runs/inherited-bed00bf7-…/recipe-run-recorded-2`, `recipe-run-linked-null-3`) are historical and not claimed as current proof.

| Criterion | Recipe nodes | Current evidence | Status |
| --- | --- | --- | --- |
| Precondition: dev1, Hyperliquid testnet, exactly one live Cross ETH position | `wallet`, `account`, `environment`, `positions`, `require-cross`, `require-cross-mode`, `require-cross-market` | `recipe-run/trace.json`: identity dev1/hyperliquid/testnet verified, controller `positions: []`; `venue-precondition.txt`: 0 venue positions, 0 open orders, spot USDC 629.31 | FAIL at `require-cross` |
| AC7 Cross badge, Pro and Lite | `pro-tag`, `lite-tag`, summary captures | none this round | N/A: blocked by precondition |
| AC8/AC8b venue liquidation price or explicit no-price state | `price-kind`, `require-*-price`, `pro-price`, `lite-price` | none this round | N/A: blocked by precondition |
| AC10 shared-collateral explanation sheet | `pro-info`, `pro-explanation`, `lite-info`, `lite-explanation` | none this round | N/A: blocked by precondition |
| AC11 "Margin used" label, edit control absent | `pro-margin`, `pro-no-edit`, `lite-margin`, `lite-no-edit` | none this round | N/A: blocked by precondition |
| Display logic (static) | not a recipe node | Jest 6 suites 278/278 on rebased HEAD; scoped ESLint exit 0; LSP 0 type errors | Static only, not runtime proof |

Why the display nodes did not run: the recipe creates no trades and requires an existing Cross fixture. Opening one means authorized testnet order placement plus cleanup, which is outside a mechanical PR-complete re-run. Runtime health itself was verified (`mm-harness launch ios --verify` pass, fixture READY).

Replay needs: one Cross ETH position on dev1 opened by an authorized fixture step, a slot-portable helper (the staged copy here only swaps simulator/port), and a refreshed liquidation expectation.
