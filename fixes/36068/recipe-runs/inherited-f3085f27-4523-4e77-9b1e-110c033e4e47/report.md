# TAT-3953 — Match final Figma design for advanced order types

## Summary

Aligned the TWAP, Scale and Chase order forms with Figma section `12187:36456`: the Chase
order-type description now uses the Figma copy, the TWAP summary lists `Runtime` and
`Size per suborder` in place of `Est Liquidation` and `Slippage`, and the TWAP runtime row gained
the ⓘ affordance from the design. Scale already matched and is unchanged.

## Changes

| File | Change |
| --- | --- |
| `locales/languages/en.json` | Chase description → Figma copy; new TWAP summary/duration strings; new `twap_runtime` tooltip |
| `app/components/UI/Perps/Perps.testIds.ts` | Test IDs for the runtime info button and the two TWAP summary rows |
| `.../PerpsProOrderForm/PerpsProOrderForm.tsx` | `OrderSummary` renders the TWAP-specific rows and drops Est Liquidation / Slippage for TWAP |
| `.../PerpsProOrderForm/PerpsProOrderForm.types.ts` | Optional `twapSummary` on the summary props; `onRuntimeInfoPress` on the TWAP model |
| `.../PerpsProOrderForm/PerpsProTwapFields.tsx` | Runtime ⓘ button; `formatTwapRuntimeSummary` for spelled-out durations |
| `.../PerpsProOrderForm/usePerpsProOrderForm.ts` | Computes runtime summary and size per suborder; opens the runtime tooltip |
| `app/components/UI/Perps/constants/perpsConfig.ts` | `SuborderIntervalSeconds` (Hyperliquid submits one suborder per 30s) and `SecondsPerMinute` |
| `.../PerpsBottomSheetTooltip/PerpsBottomSheetTooltip.types.ts` | `twap_runtime` tooltip key |

Test files updated: `PerpsProTwapFields.test.tsx`, `PerpsProOrderForm.test.tsx`,
`PerpsOrderTypeBottomSheet.test.tsx` (the last pinned the old Chase copy).

## Deliberate deviations from Figma

| Item | Figma | Shipped | Reason |
| --- | --- | --- | --- |
| TWAP runtime range | `5m - 7d` | `5m – 24h` | Hyperliquid caps TWAP duration at 1,440 minutes (`HYPERLIQUID_TWAP_LIMITS.MaxDurationMinutes`) |
| Chase foreground notice | `Keep the app opened to wait for Chase order to fulfil.` | `Keep the app open while the Chase order is running.` | Figma copy is non-idiomatic; ticket owner chose to keep the app wording |

## Test plan

| Check | Result |
| --- | --- |
| `mm-harness run recipe.json` | pass — 37/37 nodes, 0 application warnings or errors |
| `PerpsProTwapFields.test.tsx` | 13 passed |
| `PerpsProOrderForm.test.tsx` | 118 passed |
| `usePerpsProOrderForm.test.ts` | 290 passed |
| `PerpsOrderTypeBottomSheet` | 59 passed |
| `PerpsBottomSheetTooltip` | 50 passed |
| Changed-file ESLint + Prettier | pass (`mm-harness check diff --profile fast`) |
| Scoped coverage (changed components) | 93.5% lines, 90.2% branches |

Full-project TypeScript was left to CI: the worker-slot rules forbid running `lint:tsc` locally.
Editor/language-server diagnostics on the touched files are clean.

## Evidence fit

| AC | Proof mode | Primary evidence | Notes |
| --- | --- | --- | --- |
| ac1 TWAP matches Figma | mixed | `evidence-twap-summary.png` + state assertions | Screenshot shows `Runtime 30 mins`, `Size per suborder 0.00001 BTC`, `Margin`, `Fees ⓘ`; recipe also asserts Est Liquidation and Slippage are absent |
| ac2 Scale matches Figma | visual | `evidence-scale-form.png` | Recipe asserts `Start (USD)`, `End (USD)`, `Order count`, `Size skew` |
| ac3 Chase matches Figma | mixed | `evidence-order-type-advanced.png` + state assertion | The Advanced tab screenshot carries the new Chase copy, so `evidence-chase-form.png` is kept only for the max-distance field |
| ac4 Runtime ⓘ affordance | state | recipe node `assert-twap-runtime-info` | No screenshot — a 20pt icon does not read at screenshot scale; the test ID assertion is the stronger proof |

Screenshots intentionally omitted from the PR body: `evidence-twap-form.png` shows the same
panel state as `evidence-twap-summary.png` before scrolling, so only the summary view is included.

## Recipe notes

`open-market` navigates without `mode: "pro"`. The harness `ui.navigate` pro-mode probe reports
`did not visibly switch Perps to pro mode. Observed: none` even when the app is demonstrably in Pro
mode, so the mode hint is omitted and the following node waits for
`perps-pro-order-form-order-type`, which exists only in the Pro order form. A slot in Lite mode
still fails the recipe loudly at that node.

The recipe lives in `temp/tasks/feat/tat-3953-0910-233844/artifacts/recipe.json`. It is
perps-specific and reusable, so it is a candidate for the perps recipe library
(`experimental-metamask-recipe-perps`); the ticket named no in-repo destination, so nothing was
committed into the product repo.

## Ticket

https://consensyssoftware.atlassian.net/browse/TAT-3953
