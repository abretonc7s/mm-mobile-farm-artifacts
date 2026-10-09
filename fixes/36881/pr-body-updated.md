## **Description**

Single Mobile PR for the existing TAT-3524 Pro Cross-margin work. This consolidates the order-entry UI, controller venue-lock backport and locked picker previously reviewed in #36881, #36897 and #36918. No separate stack needs to merge first.

With `perpsCrossMarginEnabled` on, eligible Pro markets offer Cross, normal and Scale orders carry the chosen margin mode, and an open position or venue lock takes precedence. The picker refreshes the venue lock on opening, focus and after an order. Cross remains unavailable for unsupported markets and while required data is unresolved. Cross uses no isolated-only liquidation estimate.

The controller patch backports `getMarginModeLock` from MetaMask/core#10414 to perps-controller18.0.1. Replace it after adopting a released Core version with equivalent behavior. MetaMask/core#10464 separately persists the preference; that client integration is not included here.

The integrated implementation includes #36897's final changes. This follow-up migrates Cross UI coverage into component view tests and makes no product change. Keep the production flag off until required safety work is validated, including the remaining Lite/Reverse reconciliation in #36919. The Terminal backend restriction remains tracked in TAT-4022.

## **Changelog**

CHANGELOG entry: Added Cross margin selection to the Perps Pro order form when cross margin is enabled

## **Related issues**

Refs: [TAT-3524](https://consensyssoftware.atlassian.net/browse/TAT-3524)

## **Manual testing steps**

```gherkin
Feature: Cross margin in Perps Pro

  Scenario: trader picks Cross margin and places an order
    Given the perps cross margin flag is on
    And the trader is on the BTC market in Pro mode on HyperLiquid with no BTC position
    When the trader taps the Isolated margin button
    And picks Cross in "Choose margin mode"
    Then the margin button reads "Cross"
    When the trader enters a 15 USD size and places the order
    Then the new BTC position card shows "Position margin used" tagged Cross

  Scenario: flag off keeps Cross unavailable
    Given the perps cross margin flag is off
    When the trader opens "Choose margin mode"
    Then Cross is greyed out with "Coming soon"
```

## Tests

Cross UI behavior runs through real Redux and Perps streams in component view tests, with Engine as the mocked boundary:

- `PerpsMarginModeBottomSheet.view.test.tsx`: Cross and isolated position locks, unlocking after a position closes, and a fresh venue lock on picker opening. 8 tests across iOS and Android.
- `PerpsLeverageBottomSheet.view.test.tsx`: selecting Cross suppresses the isolated estimate and distance; changing leverage preserves an open Cross position's margin lock. 4 tests across iOS and Android.
- `PerpsProOrderFormPanel.view.test.tsx`: choose and submit Cross, return to Isolated, eligibility gates, and pending market/venue data. 24 tests across iOS and Android.
- Retained `PerpsProCrossMargin.view.test.tsx` and `PerpsTPSLView.view.test.tsx` cover the Cross risk editors and isolated stop validation.

Removed the replaced shallow margin-sheet suite and Cross UI cases from the panel and leverage unit suites. Pure order-parameter and hook unit tests and the real provider integration suite remain.

Bounded local gate passed: 47 component view tests, 475 unit tests and 14 integration tests. The Perps preset suite also passed 4 tests. ESLint and formatting passed; full-project TypeScript remains with CI. This follow-up changes tests and test support only.

## **Screenshots/Recordings**

Rebased onto current main. The inherited iOS Hyperliquid testnet recipe passed 45/45 against the rebased product plus this test-only migration; all three new local screenshots were inspected. The published images below retain their earlier scope. New component view coverage is listed in Tests.

<table>
<tr><td align="center" valign="top" width="50%"><strong>Cross selectable and selected in margin chooser</strong><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36881/evidence-ac1-cross-sheet.png?sha=8dac766498530b4f" alt="Cross selectable and selected in margin chooser" width="320" /></td><td align="center" valign="top" width="50%"><strong>Order form margin control reads Cross</strong><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36881/evidence-ac1-cross-label.png?sha=e18939ee1d686b67" alt="Order form margin control reads Cross" width="320" /></td></tr>
<tr><td align="center" valign="top" width="50%"><strong>Placed BTC position is tagged Cross</strong><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36881/evidence-ac2-cross-position.png?sha=8b9a74ba53f0163c" alt="Placed BTC position is tagged Cross" width="320" /></td><td></td></tr>
</table>

## **Validation Recipe**

<details><summary>recipe.json (45 nodes — Cross margin selectable in Pro margin mode chooser when flag is on)</summary>

```json
{
  "$schema": "https://farmslot.io/schemas/recipe-v1.schema.json",
  "title": "Cross margin selectable in Pro margin mode chooser when flag is on",
  "description": "TAT-3524. Data prerequisites: fixture Trading account (currently selected), HyperLiquid testnet, BTC market in Pro with no BTC position or resting order (converged by setup nodes, since an open position locks the margin mode); perpsCrossMarginEnabled pinned on via metamask.feature_flags.set and cleared at teardown.",
  "workflow": {
    "entry": "setup-flag",
    "nodes": {
      "setup-flag": {
        "action": "metamask.feature_flags.set",
        "intent": "Turn the cross margin rollout flag on like the reporter did",
        "flags": {
          "perpsCrossMarginEnabled": {
            "enabled": true,
            "minimumVersion": "0.0.0"
          }
        },
        "next": "setup-pro"
      },
      "setup-pro": {
        "action": "metamask.perps.start_state",
        "intent": "Open the BTC market in Pro mode on HyperLiquid testnet with the fixture trading account",
        "account_name": "Trading",
        "provider": "hyperliquid",
        "network": "testnet",
        "market": "BTC",
        "market_mode": "pro",
        "page": "market_details",
        "next": "setup-no-btc-position"
      },
      "setup-no-btc-position": {
        "action": "metamask.perps.ensure_positions",
        "intent": "Start from no BTC position so the margin mode is free to change",
        "market": "BTC",
        "state": "none",
        "next": "setup-no-btc-orders"
      },
      "setup-no-btc-orders": {
        "action": "metamask.perps.ensure_orders",
        "intent": "Start from no resting BTC orders so the margin mode is free to change",
        "market": "BTC",
        "state": "none",
        "next": "setup-show-margin-control"
      },
      "setup-show-margin-control": {
        "action": "ui.scroll",
        "intent": "Let the trader see the margin and leverage controls of the order form",
        "test_id": "perps-pro-order-form-margin-mode",
        "scroll_into_view": true,
        "next": "setup-open-order-type"
      },
      "setup-open-order-type": {
        "action": "ui.press",
        "intent": "Open the order type chooser so the trade starts as a market order",
        "test_id": "perps-pro-order-form-order-type",
        "next": "setup-basic-tab"
      },
      "setup-basic-tab": {
        "action": "ui.press",
        "intent": "Show the basic order types, since a saved advanced order type opens the chooser on another tab",
        "test_id": "perps-order-type-tab-basic",
        "next": "setup-wait-market-type"
      },
      "setup-wait-market-type": {
        "action": "ui.wait_for",
        "intent": "Confirm the Market order type is offered",
        "test_id": "perps-order-type-market",
        "expected": "visible",
        "timeout_ms": 10000,
        "next": "setup-pick-market-type"
      },
      "setup-pick-market-type": {
        "action": "ui.press",
        "intent": "Start from a market order regardless of the saved order type",
        "test_id": "perps-order-type-market",
        "next": "gate-margin-button"
      },
      "gate-margin-button": {
        "action": "ui.wait_for",
        "intent": "Confirm the Pro order form margin mode control is on screen",
        "test_id": "perps-pro-order-form-margin-mode",
        "expected": "visible",
        "timeout_ms": 15000,
        "next": "ac1-open-sheet"
      },
      "ac1-open-sheet": {
        "action": "ui.press",
        "intent": "Open the margin mode chooser the way a trader would",
        "test_id": "perps-pro-order-form-margin-mode",
        "next": "ac1-wait-cross-option"
      },
      "ac1-wait-cross-option": {
        "action": "ui.wait_for",
        "intent": "Confirm the Cross choice is shown in the margin mode chooser",
        "test_id": "perps-margin-mode-cross",
        "expected": "visible",
        "timeout_ms": 10000,
        "next": "ac1-press-cross"
      },
      "ac1-press-cross": {
        "action": "ui.press",
        "intent": "Pick Cross margin for the next trade",
        "test_id": "perps-margin-mode-cross",
        "next": "ac1-wait-sheet-closed"
      },
      "ac1-wait-sheet-closed": {
        "action": "ui.wait_for",
        "intent": "Confirm picking Cross closes the chooser and returns to the order form",
        "test_id": "perps-margin-mode-bottom-sheet",
        "expected": "absent",
        "timeout_ms": 10000,
        "next": "ac1-show-margin-control"
      },
      "ac1-show-margin-control": {
        "action": "ui.swipe",
        "intent": "Let reviewers see the margin control right after Cross was picked, clear of the sticky header",
        "target": {
          "x": 150,
          "y": 500
        },
        "direction": "down",
        "distance": 1200,
        "duration_ms": 400,
        "next": "ac1-wait-cross-label"
      },
      "ac1-wait-cross-label": {
        "action": "ui.wait_for",
        "intent": "Confirm the order form margin control now reads Cross",
        "text": "Cross",
        "text_match": "exact",
        "expected": "visible",
        "timeout_ms": 10000,
        "next": "ac1-screenshot-cross-label",
        "test_id": "perps-pro-order-form-margin-mode"
      },
      "ac1-screenshot-cross-label": {
        "action": "ui.screenshot",
        "intent": "Show the order form margin control reading Cross after the trader picked it",
        "label": "AC1: order form shows Cross margin",
        "next": "ac1-reopen-sheet"
      },
      "ac1-reopen-sheet": {
        "action": "ui.press",
        "intent": "Reopen the chooser to show Cross is the active choice",
        "test_id": "perps-pro-order-form-margin-mode",
        "next": "ac1-wait-cross-selected"
      },
      "ac1-wait-cross-selected": {
        "action": "ui.wait_for",
        "intent": "Confirm the chooser reopens with the Cross choice on screen",
        "test_id": "perps-margin-mode-cross",
        "expected": "visible",
        "timeout_ms": 10000,
        "next": "ac1-screenshot-cross-sheet"
      },
      "ac1-screenshot-cross-sheet": {
        "action": "ui.screenshot",
        "intent": "Show Cross is selectable and selected, without the coming soon note",
        "label": "AC1: Cross selectable in margin mode chooser",
        "next": "ac2-keep-cross"
      },
      "ac2-keep-cross": {
        "action": "ui.press",
        "intent": "Confirm Cross as the margin mode for the trade",
        "test_id": "perps-margin-mode-cross",
        "next": "ac2-wait-sheet-closed"
      },
      "ac2-wait-sheet-closed": {
        "action": "ui.wait_for",
        "intent": "Confirm the trader is back on the order form with Cross kept",
        "test_id": "perps-margin-mode-bottom-sheet",
        "expected": "absent",
        "timeout_ms": 10000,
        "next": "ac2-scroll-size"
      },
      "ac2-scroll-size": {
        "action": "ui.scroll",
        "intent": "Let the trader see where the trade size is entered",
        "test_id": "perps-pro-order-form-size-card",
        "scroll_into_view": true,
        "next": "ac2-wait-size"
      },
      "ac2-wait-size": {
        "action": "ui.wait_for",
        "intent": "Confirm the order size field is ready for input",
        "test_id": "perps-pro-order-form-size-card",
        "expected": "visible",
        "timeout_ms": 10000,
        "next": "ac2-set-size"
      },
      "ac2-set-size": {
        "action": "ui.set_input",
        "intent": "Enter a small 15 USD trade size like a trader would",
        "test_id": "perps-pro-order-form-size-input",
        "value": "15",
        "next": "ac2-scroll-submit"
      },
      "ac2-scroll-submit": {
        "action": "ui.scroll",
        "intent": "Let the trader reach the button that sends the Cross trade",
        "test_id": "perps-pro-order-form-summary-fees",
        "scroll_into_view": true,
        "next": "ac2-wait-submit"
      },
      "ac2-wait-submit": {
        "action": "ui.wait_for",
        "intent": "Confirm the place order button is reachable",
        "test_id": "perps-pro-order-form-place-order",
        "expected": "visible",
        "timeout_ms": 10000,
        "next": "ac2-press-submit"
      },
      "ac2-press-submit": {
        "action": "ui.press",
        "intent": "Place the Cross margin long on BTC testnet",
        "test_id": "perps-pro-order-form-place-order",
        "next": "ac2-assert-position-open"
      },
      "ac2-assert-position-open": {
        "action": "metamask.perps.assert_positions",
        "intent": "Confirm the Cross order actually opened a BTC position",
        "market": "BTC",
        "state": "open",
        "timeout_ms": 30000,
        "next": "ac2-filter-btc"
      },
      "ac2-filter-btc": {
        "action": "ui.press",
        "intent": "Narrow the positions list to BTC so the new position card is shown on its own",
        "test_id": "perps-pro-market-positions-ticker-only",
        "next": "ac2-swipe-to-positions"
      },
      "ac2-swipe-to-positions": {
        "action": "ui.swipe",
        "intent": "Let reviewers see the positions panel below the order form",
        "target": {
          "x": 150,
          "y": 700
        },
        "direction": "up",
        "distance": 600,
        "duration_ms": 400,
        "next": "ac2-swipe-to-card"
      },
      "ac2-swipe-to-card": {
        "action": "ui.swipe",
        "intent": "Let reviewers see the margin details of the new BTC position card",
        "target": {
          "x": 150,
          "y": 700
        },
        "direction": "up",
        "distance": 600,
        "duration_ms": 400,
        "next": "ac2-wait-cross-tag"
      },
      "ac2-wait-cross-tag": {
        "action": "ui.wait_for",
        "intent": "Confirm the venue reports the new BTC position as Cross margin",
        "test_id": "cross-margin-tag-pro-BTC",
        "expected": "visible",
        "timeout_ms": 20000,
        "next": "ac2-screenshot-cross-position"
      },
      "ac2-screenshot-cross-position": {
        "action": "ui.screenshot",
        "intent": "Show reviewers the placed BTC position is tagged Cross",
        "label": "AC2: placed BTC position is Cross margin",
        "next": "teardown-close-btc"
      },
      "teardown-close-btc": {
        "action": "metamask.perps.close_positions",
        "intent": "Close the test BTC position so the testnet account returns to flat",
        "market": "BTC",
        "next": "teardown-assert-flat"
      },
      "teardown-assert-flat": {
        "action": "metamask.perps.assert_positions",
        "intent": "Confirm the testnet account holds no BTC position after cleanup",
        "market": "BTC",
        "state": "none",
        "timeout_ms": 30000,
        "next": "teardown-unfilter-btc"
      },
      "teardown-unfilter-btc": {
        "action": "ui.press",
        "intent": "Restore the positions list to all markets for later runs",
        "test_id": "perps-pro-market-positions-ticker-only",
        "next": "teardown-clear-flag"
      },
      "teardown-clear-flag": {
        "action": "metamask.feature_flags.clear",
        "intent": "Drop the flag override so the slot does not leak the variant",
        "next": "ac2-run-order-params-tests"
      },
      "ac2-run-order-params-tests": {
        "action": "command",
        "intent": "Prove the picked margin mode reaches the placed order parameters",
        "timeout_ms": 900000,
        "next": "ac2-assert-tests-pass"
      },
      "ac2-assert-tests-pass": {
        "action": "assert_exit_code",
        "source": "ac2-run-order-params-tests",
        "expected": 0,
        "intent": "Confirm the order parameter margin mode tests passed",
        "next": "ac3-run-gating-tests"
      },
      "ac3-run-gating-tests": {
        "action": "command",
        "intent": "Prove Cross stays unavailable when the flag is off or the market cannot trade cross",
        "timeout_ms": 900000,
        "next": "ac3-assert-tests-pass"
      },
      "ac3-assert-tests-pass": {
        "action": "assert_exit_code",
        "source": "ac3-run-gating-tests",
        "expected": 0,
        "intent": "Confirm the cross margin gating tests passed",
        "next": "ac4-run-cross-position-tests"
      },
      "ac4-run-cross-position-tests": {
        "action": "command",
        "intent": "Prove an existing cross position no longer blocks trading when Cross is available",
        "timeout_ms": 900000,
        "next": "ac4-assert-tests-pass"
      },
      "ac4-assert-tests-pass": {
        "action": "assert_exit_code",
        "source": "ac4-run-cross-position-tests",
        "expected": 0,
        "intent": "Confirm the existing cross position tests passed",
        "next": "done"
      },
      "done": {
        "action": "end",
        "status": "pass"
      }
    }
  }
}
```
</details>

## **Validation Logs**

<details><summary>Full output (45/45 passed, pass)</summary>

```
# MetaMask Recipe Run

Status: pass
Duration: 93s
Nodes: 45/45 passed

## Side findings
- REVIEW 7 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-flag (metamask.feature_flags.set, 1.0s): proof=mobile-remote-feature-flags
- PASS setup-pro (metamask.perps.start_state, 3.4s): proof=metamask-perps-start-state
- PASS setup-no-btc-position (metamask.perps.ensure_positions, 660ms): matching=0
- PASS setup-no-btc-orders (metamask.perps.ensure_orders, 750ms): matching=0
- PASS setup-show-margin-control (ui.scroll, 1.0s): ok=true, testId=perps-pro-order-form-margin-mode, intoView=true, alreadyVisible=true
- PASS setup-open-order-type (ui.press, 611ms): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-1
- PASS setup-basic-tab (ui.press, 553ms): ok=true, testId=perps-order-type-tab-basic, deviceName=mm-1
- PASS setup-wait-market-type (ui.wait_for, 699ms): matched=true, testId=perps-order-type-market, expected=visible, present=true, visible=true
- PASS setup-pick-market-type (ui.press, 601ms): ok=true, testId=perps-order-type-market, deviceName=mm-1
- PASS gate-margin-button (ui.wait_for, 758ms): matched=true, testId=perps-pro-order-form-margin-mode, expected=visible, present=true, visible=true
- PASS ac1-open-sheet (ui.press, 658ms): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-1
- PASS ac1-wait-cross-option (ui.wait_for, 526ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-press-cross (ui.press, 536ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-1
- PASS ac1-wait-sheet-closed (ui.wait_for, 738ms): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac1-show-margin-control (ui.swipe, 12s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac1-wait-cross-label (ui.wait_for, 809ms): matched=true, testId=perps-pro-order-form-margin-mode, text=Cross, textMatch=exact, expected=visible
- PASS ac1-reopen-sheet (ui.press, 531ms): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-1
- PASS ac1-wait-cross-selected (ui.wait_for, 513ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac2-keep-cross (ui.press, 551ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-1
- PASS ac2-wait-sheet-closed (ui.wait_for, 776ms): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac2-scroll-size (ui.scroll, 730ms): ok=true, testId=perps-pro-order-form-size-card, intoView=true, alreadyVisible=true
- PASS ac2-wait-size (ui.wait_for, 850ms): matched=true, testId=perps-pro-order-form-size-card, expected=visible, present=true, visible=true
- PASS ac2-set-size (ui.set_input, 754ms): ok=true, testId=perps-pro-order-form-size-input, value=15, deviceName=mm-1
- PASS ac2-scroll-submit (ui.scroll, 712ms): ok=true, testId=perps-pro-order-form-summary-fees, intoView=true, alreadyVisible=true
- PASS ac2-wait-submit (ui.wait_for, 758ms): matched=true, testId=perps-pro-order-form-place-order, expected=visible, present=true, visible=true
- PASS ac2-press-submit (ui.press, 810ms): ok=true, testId=perps-pro-order-form-place-order, deviceName=mm-1
- PASS ac2-assert-position-open (metamask.perps.assert_positions, 4.4s): matching=1
- PASS ac2-filter-btc (ui.press, 794ms): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-1
- PASS ac2-swipe-to-positions (ui.swipe, 4.6s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-swipe-to-card (ui.swipe, 4.5s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-wait-cross-tag (ui.wait_for, 743ms): matched=true, testId=cross-margin-tag-pro-BTC, expected=visible, present=true, visible=true
- PASS teardown-close-btc (metamask.perps.close_positions, 4.0s): matching=0
- PASS teardown-assert-flat (metamask.perps.assert_positions, 347ms): matching=0
- PASS teardown-unfilter-btc (ui.press, 804ms): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-1
- PASS teardown-clear-flag (metamask.feature_flags.clear, 323ms): proof=mobile-remote-feature-flags
- PASS ac2-run-order-params-tests (command, 13s): exitCode=0, stdout=PASS app/components/UI/Perps/utils/orderParams.test.ts
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts

Test Suites: 2 passed, 2 total
Tests:       325 skipped, 23 passed, 348 total
Snapshots:   0 total
Time:        2.855 s, estimated 4 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts|app\/components\/UI\/Perps\/utils\/orderParams.test.ts/i with tests matching "margin mode".

- PASS ac2-assert-tests-pass (assert_exit_code, 30ms): source=ac2-run-order-params-tests, expected=0, actual=0
- PASS ac3-run-gating-tests (command, 12s): exitCode=0, stdout=PASS app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.test.tsx
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.test.tsx

Test Suites: 2 passed, 2 total
Tests:       40 skipped, 13 passed, 53 total
Snapshots:   0 total
Time:        1.978 s, estimated 2 s
Ran all test suites matching /app\/components\/UI\/Perps\/components\/PerpsMarginModeBottomSheet\/PerpsMarginModeBottomSheet.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderFormPanel.test.tsx/i with tests matching "cross margin".

- PASS ac3-assert-tests-pass (assert_exit_code, 29ms): source=ac3-run-gating-tests, expected=0, actual=0
- PASS ac4-run-cross-position-tests (command, 11s): exitCode=0, stdout=      ○ skipped restores reduceOnly from the pending trade draft
      ○ skipped clears TP/SL state when Reduce Only turns on
      ○ skipped sets the size slider max to the open position notional when Reduce Only is on
      ○ skipped keeps the margin-based slider max and empty size when Reduce Only is on with no position
      ○ skipped keeps the margin-based slider max and empty size when Reduce Only is on with the wrong direction
      ○ skipped does not commit slider amount when Reduce Only has a position error
      ○ skipped does not restore a focused size after Reduce Only enables with no position
      ○ skipped does not clear typed size while the reduce-only position is loading
      ○ skipped keeps typed size when a valid closing position arrives after Reduce Only load
      ○ skipped uses the limit price for the Reduce Only slider max
      ○ skipped restores the margin-based amount cap when Reduce Only turns off
      ○ skipped does not clamp size to available margin when confirming leverage with Reduce Only on
    handlers
      ○ skipped navigates to the TP/SL screen and its onConfirm sets TP/SL
      ○ skipped shows the limit-price-required toast and does not navigate for a limit order without a price
      ○ skipped confirms leverage, clamps an over-max amount, and tracks the change
      ○ skipped tracks leverage change with previous_leverage and not previousLeverage
      ○ skipped saves slippage and opens the slippage sheet
      ○ skipped selects an order type
      ○ skipped forgets committed prices when twap discards them
      ○ skipped forgets committed prices when scale discards them
      ○ skipped forgets committed prices when chase discards them
      ○ skipped clears incompatible prices when TWAP is selected
      ○ skipped ignores TWAP selection while the feature gate is disabled
      ○ skipped preserves typed digits while blocking an out-of-range duration part
      ○ skipped normalizes leading zeros in TWAP duration parts
      ○ skipped blocks a TWAP duration whose individually valid parts exceed the total maximum
      ○ skipped keeps showing the trigger warning when the carried-over price moves to a new order type
      ○ skipped ignores size input over nine digits and forwards valid input
      ○ skipped ignores limit price input over nine digits and forwards valid input
      ○ skipped normalizes leading zeroes in limit price input
      ○ skipped normalizes comma decimal input in the limit price
      ○ skipped rejects repeated decimal separators in limit price input
      ○ skipped rejects malformed Chase max distance input 1abc
      ○ skipped rejects malformed Chase max distance input 1.2.3
      ○ skipped normalizes Chase max distance and enforces the shared digit cap
      ○ skipped clears Chase max distance only when its unit changes
      ○ skipped accepts a Chase percentage below the basis-point divisor
      ○ skipped rejects a Chase percentage at the basis-point divisor
      ○ skipped finalizes a trailing decimal separator from the limit price on blur
      ○ skipped does not update the limit price on blur when already finalized
      ○ skipped sets the limit price from the live mid
      ○ skipped previews a slider USD amount before committing on drag end
      ○ skipped forwards the direction and add-funds handlers

Test Suites: 1 passed, 1 total
Tests:       323 skipped, 3 passed, 326 total
Snapshots:   0 total
Time:        1.603 s, estimated 3 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts/i with tests matching "existing cross position".

- PASS ac4-assert-tests-pass (assert_exit_code, 29ms): source=ac4-run-cross-position-tests, expected=0, actual=0
- PASS done (end, 0ms)
```
</details>

### Consolidated validation

The retained final-head evidence from #36918 covers this same `4ece3436c4` implementation: venue-lock recipe15/15 and full Cross flow45/45 on iOS, Runway36144509032. Controller-only evidence and review history remain in #36897. Existing evidence below is retained with its original scope. CI must run against this canonical PR before merge.

Venue-lock before:

<img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36918/before-ac1-venue-lock-sheet.png" alt="Cross offered despite a resting isolated order before the fix" width="320" />

Venue-lock after:

<img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36918/after-ac1-venue-lock-sheet.png" alt="Cross disabled while the venue is locked to Isolated" width="320" />

## **Pre-merge author checklist**

- [x] I've followed [MetaMask Contributor Docs](https://github.com/MetaMask/contributor-docs) and [MetaMask Mobile Coding Standards](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/CODING_GUIDELINES.md).
- [x] I've completed the PR template to the best of my ability
- [x] I've included tests if applicable
- [x] I've documented my code using [JSDoc](https://jsdoc.app/) format if applicable
- [x] I've applied the right labels on the PR (see [labeling guidelines](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/LABELING_GUIDELINES.md)). Not required for external contributors.

#### Performance checks (if applicable)

- [x] I've tested on Android
  - N/A: shared RN code with no platform branches; validated on iOS
- [x] I've tested with a power user scenario
  - N/A: no list or account-scale change
- [x] I've instrumented key operations with Sentry traces for production performance metrics
  - N/A: no new async operation

## **Pre-merge reviewer checklist**

<!--
Reviewer checklist items follow the same semantics as the author checklist: an
unchecked box is ambiguous, a checked box means the reviewer consciously
assessed that responsibility. See `docs/readme/ready-for-review.md`.
-->

- [ ] I've manually tested the PR (e.g. pull and build branch, run the app, test code being changed).
- [ ] I confirm that this PR addresses all acceptance criteria described in the ticket it closes and includes the necessary testing evidence such as recordings and or screenshots.

[TAT-3524]: https://consensyssoftware.atlassian.net/browse/TAT-3524?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Changes perps order placement and margin-mode resolution against venue locks; mistakes could submit the wrong collateral mode, though feature flags, market gating, and fail-closed lock pending states mitigate exposure.
> 
> **Overview**
> **Enables Cross margin in Perps Pro** when `perpsCrossMarginEnabled` and market/provider gates pass (Hyperliquid main DEX, Pro mode, no isolated-only restrictions). Traders pick Isolated vs Cross in the margin sheet; the form label, order payload (`marginMode`), and Scale orders follow that choice, with context resets on account/network/market switches.
> 
> **Venue margin-mode locking** is wired through a new `usePerpsMarginModeLock` hook: open positions, resting orders, or TWAPs force the bound mode, lock the picker, refresh on sheet open/focus/post-order, and can block Place Order until the lock resolves. Position and market lookups are scoped by `providerId` so aggregated multi-provider symbols do not cross-contaminate.
> 
> **Cross-specific risk UX**: isolated liquidation estimates and stop-vs-liquidation warnings are suppressed for Cross in the order summary, leverage sheet, and TP/SL flow (including passing `marginMode` into navigation). Existing cross positions can trade when Cross is available instead of only showing the unsupported modal.
> 
> Copy adds `cross_description_available`; coverage spans hook/unit, component-view, and margin-lock integration tests.
> 
> <sup>Reviewed by [Cursor Bugbot](https://cursor.com/bugbot) for commit 51a0dc4075eeef587cb0454ce1b2d6ff0bf4cf88. Bugbot is set up for automated code reviews on this repo. Configure [here](https://www.cursor.com/dashboard/bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

[TAT-4022]: https://consensyssoftware.atlassian.net/browse/TAT-4022?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ

