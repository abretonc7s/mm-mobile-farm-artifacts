# MetaMask Recipe Run

Status: pass
Duration: 106s
Nodes: 45/45 passed

## Side findings
- REVIEW 9 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-flag (metamask.feature_flags.set, 375ms): proof=mobile-remote-feature-flags
- PASS setup-pro (metamask.perps.start_state, 2.1s): proof=metamask-perps-start-state
- PASS setup-no-btc-position (metamask.perps.ensure_positions, 656ms): matching=0
- PASS setup-no-btc-orders (metamask.perps.ensure_orders, 658ms): matching=0
- PASS setup-show-margin-control (ui.scroll, 618ms): ok=true, testId=perps-pro-order-form-margin-mode, intoView=true, alreadyVisible=true
- PASS setup-open-order-type (ui.press, 541ms): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-2
- PASS setup-basic-tab (ui.press, 578ms): ok=true, testId=perps-order-type-tab-basic, deviceName=mm-2
- PASS setup-wait-market-type (ui.wait_for, 606ms): matched=true, testId=perps-order-type-market, expected=visible, present=true, visible=true
- PASS setup-pick-market-type (ui.press, 733ms): ok=true, testId=perps-order-type-market, deviceName=mm-2
- PASS gate-margin-button (ui.wait_for, 549ms): matched=true, testId=perps-pro-order-form-margin-mode, expected=visible, present=true, visible=true
- PASS ac1-open-sheet (ui.press, 583ms): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-2
- PASS ac1-wait-cross-option (ui.wait_for, 557ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-press-cross (ui.press, 555ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-2
- PASS ac1-wait-sheet-closed (ui.wait_for, 777ms): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac1-show-margin-control (ui.swipe, 13s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac1-wait-cross-label (ui.wait_for, 813ms): matched=true, testId=perps-pro-order-form-margin-mode, text=Cross, textMatch=exact, expected=visible
- PASS ac1-screenshot-cross-label (ui.screenshot, 974ms): path=screenshots/evidence-ac1-cross-label.png
- PASS ac1-reopen-sheet (ui.press, 604ms): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-2
- PASS ac1-wait-cross-selected (ui.wait_for, 546ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-screenshot-cross-sheet (ui.screenshot, 763ms): path=screenshots/evidence-ac1-cross-sheet.png
- PASS ac2-keep-cross (ui.press, 612ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-2
- PASS ac2-wait-sheet-closed (ui.wait_for, 790ms): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac2-scroll-size (ui.scroll, 778ms): ok=true, testId=perps-pro-order-form-size-card, intoView=true, alreadyVisible=true
- PASS ac2-wait-size (ui.wait_for, 777ms): matched=true, testId=perps-pro-order-form-size-card, expected=visible, present=true, visible=true
- PASS ac2-set-size (ui.set_input, 784ms): ok=true, testId=perps-pro-order-form-size-input, value=15, deviceName=mm-2
- PASS ac2-scroll-submit (ui.scroll, 1.5s): animated=false, offset=600, ok=true, testId=perps-pro-order-form-summary-fees, deviceName=mm-2
- PASS ac2-wait-submit (ui.wait_for, 760ms): matched=true, testId=perps-pro-order-form-place-order, expected=visible, present=true, visible=true
- PASS ac2-press-submit (ui.press, 1.2s): ok=true, testId=perps-pro-order-form-place-order, deviceName=mm-2
- PASS ac2-assert-position-open (metamask.perps.assert_positions, 6.2s): matching=1
- PASS ac2-filter-btc (ui.press, 898ms): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-2
- PASS ac2-swipe-to-positions (ui.swipe, 3.9s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-swipe-to-card (ui.swipe, 3.9s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-wait-cross-tag (ui.wait_for, 788ms): matched=true, testId=cross-margin-tag-pro-BTC, expected=visible, present=true, visible=true
- PASS ac2-screenshot-cross-position (ui.screenshot, 977ms): path=screenshots/evidence-ac2-cross-position.png
- PASS teardown-close-btc (metamask.perps.close_positions, 3.8s): matching=0
- PASS teardown-assert-flat (metamask.perps.assert_positions, 396ms): matching=0
- PASS teardown-unfilter-btc (ui.press, 765ms): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-2
- PASS teardown-clear-flag (metamask.feature_flags.clear, 331ms): proof=mobile-remote-feature-flags
- PASS ac2-run-order-params-tests (command, 25s): exitCode=0, stdout=PASS app/components/UI/Perps/utils/orderParams.test.ts (12.133 s)
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts (13.129 s)

Test Suites: 2 passed, 2 total
Tests:       325 skipped, 28 passed, 353 total
Snapshots:   0 total
Time:        13.278 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts|app\/components\/UI\/Perps\/utils\/orderParams.test.ts/i with tests matching "margin mode".

- PASS ac2-assert-tests-pass (assert_exit_code, 31ms): source=ac2-run-order-params-tests, expected=0, actual=0
- PASS ac3-run-gating-tests (command, 13s): exitCode=0, stdout=PASS app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.test.tsx
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.test.tsx

Test Suites: 2 passed, 2 total
Tests:       40 skipped, 14 passed, 54 total
Snapshots:   0 total
Time:        2.909 s, estimated 4 s
Ran all test suites matching /app\/components\/UI\/Perps\/components\/PerpsMarginModeBottomSheet\/PerpsMarginModeBottomSheet.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderFormPanel.test.tsx/i with tests matching "cross margin".

- PASS ac3-assert-tests-pass (assert_exit_code, 61ms): source=ac3-run-gating-tests, expected=0, actual=0
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
Tests:       328 skipped, 3 passed, 331 total
Snapshots:   0 total
Time:        1.561 s, estimated 14 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts/i with tests matching "existing cross position".

- PASS ac4-assert-tests-pass (assert_exit_code, 31ms): source=ac4-run-cross-position-tests, expected=0, actual=0
- PASS done (end, 0ms)
