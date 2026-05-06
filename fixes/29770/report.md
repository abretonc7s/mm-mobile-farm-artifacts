# TAT-3094 Report

## Summary

Open order trigger and limit prices were using compact/default fiat precision, so low-priced markets such as CHIP rounded to two decimals in compact rows and order details. The fix routes open-order price fields through the same universal price ranges used by market prices while leaving notional value and fee formatting unchanged.

## Root Cause

Market prices are transformed with `PRICE_RANGES_UNIVERSAL` in `app/controllers/perps/utils/marketDataTransform.ts`, but open-order UI used different formatting paths:

- `app/components/UI/Perps/components/PerpsCompactOrderRow/PerpsCompactOrderRow.tsx:51` formatted the order price with compact/minimal ranges.
- `app/components/UI/Perps/Views/PerpsOrderDetailsView/PerpsOrderDetailsView.tsx:135`, `:141`, `:183`, and `:188` formatted limit, trigger, take-profit, and stop-loss prices with universal ranges only after this fix.

The broken data flow was: order price string -> numeric parse -> default/minimal fiat formatter -> visible open-order price, which rounded `0.001234` to the wrong display precision. Order value continues to use default fiat formatting because it is a USD notional value, not a market trigger/limit price.

## Reproduction Commit

Reproduction marker commit: `120dffffbe`

Metro log excerpt:

```text
(NOBRIDGE) DEBUG  [PR-29770] BUG_MARKER: compact open order price rendered with default minimal price precision
```

Pre-fix recipe result: the CHIP order details assertion failed because `$0.001234` was absent from the rendered text.

## Changes

- `app/components/UI/Perps/components/PerpsCompactOrderRow/PerpsCompactOrderRow.tsx` - formats compact open-order prices with `PRICE_RANGES_UNIVERSAL`.
- `app/components/UI/Perps/Views/PerpsOrderDetailsView/PerpsOrderDetailsView.tsx` - formats limit, trigger, TP, and SL prices with `PRICE_RANGES_UNIVERSAL`.
- `app/components/UI/Perps/components/PerpsCompactOrderRow/PerpsCompactOrderRow.test.tsx` - asserts compact order rows pass universal ranges to the formatter.
- `app/components/UI/Perps/Views/PerpsOrderDetailsView/PerpsOrderDetailsView.test.tsx` - adds CHIP six-decimal detail-view coverage and updates trigger/TP/SL expectations.
- `app/controllers/perps/PerpsController.ts` - keeps the existing TS2589 workaround localized to the bound update function so typecheck passes.
- `app/reducers/rewards/index.ts` - narrows the Immer draft assignment path to `RewardsState` so typecheck passes.

## Test Plan

Automated:

- `yarn lint && NODE_OPTIONS='--max-old-space-size=8192' yarn lint:tsc && yarn format:check` - passed; lint emitted existing repository warnings.
- `yarn jest app/components/UI/Perps/Views/PerpsOrderDetailsView/PerpsOrderDetailsView.test.tsx app/components/UI/Perps/components/PerpsCompactOrderRow/PerpsCompactOrderRow.test.tsx --no-coverage` - passed, 2 suites / 44 tests.
- `yarn coverage:analyze` - passed; no changed files were reported for coverage analysis in that staged state.
- `bash scripts/perps/agentic/validate-recipe.sh .task/fix/tat-3094-0506-073600/artifacts/ --skip-manual` - passed 4/4 recipe nodes; latest summary reports clean recipe issues.

Manual Gherkin:

```gherkin
Feature: Open order price precision
  Scenario: Low-priced market limit order details use market precision
    Given the wallet is unlocked and Perps are available
    When a CHIP limit order with price "0.001234" is opened in order details
    Then the Price row displays "$0.001234"
    And the Order value row may still display fiat notional precision such as "$0.12"

  Scenario: Compact open order rows use market precision
    Given the wallet has an open limit, take-profit, or stop-loss order
    When the order is shown in a compact order row
    Then the trigger or limit price uses the same decimal precision as the market price
```

## Evidence

- `.task/fix/tat-3094-0506-073600/artifacts/before.mp4`
- `.task/fix/tat-3094-0506-073600/artifacts/after.mp4`
- `.task/fix/tat-3094-0506-073600/artifacts/after-ac1-chip-order-details.png`
- `.task/fix/tat-3094-0506-073600/artifacts/recipe.json`
- `.task/fix/tat-3094-0506-073600/artifacts/summary.json`
- `.task/fix/tat-3094-0506-073600/artifacts/trace.json`
- `.task/fix/tat-3094-0506-073600/artifacts/workflow.mmd`
- `.task/fix/tat-3094-0506-073600/artifacts/recipe-coverage.md`
- `.task/fix/tat-3094-0506-073600/artifacts/recipe-issues-review.md`

## Ticket

TAT-3094: https://consensyssoftware.atlassian.net/browse/TAT-3094

## Self-Review Fixes

- `app/components/UI/Perps/Views/PerpsOrderDetailsView/PerpsOrderDetailsView.test.tsx:338` - added an assertion that the trigger-condition translation receives `price: '$0.001234'`, covering the universal-range formatting path that the string mock previously hid.
- `.task/fix/tat-3094-0506-073600/artifacts/recipe.json:8` - added coverage notes clarifying that the executable recipe proves the CHIP limit-order details path, while compact-row and TP/SL surfaces are covered by Jest rather than the recipe.
- Recipe rerun after the self-review fix passed 4/4 nodes; the latest issue review observed one non-gating warning: `Error: premature close`.
