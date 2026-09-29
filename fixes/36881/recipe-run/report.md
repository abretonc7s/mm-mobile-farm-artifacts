# MetaMask Recipe Run

Status: pass
Duration: 149s
Nodes: 45/45 passed

## Side findings
- REVIEW 7 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-flag (metamask.feature_flags.set, 880ms): proof=mobile-remote-feature-flags
- PASS setup-pro (metamask.perps.start_state, 2.8s): proof=metamask-perps-start-state
- PASS setup-no-btc-position (metamask.perps.ensure_positions, 1.1s): matching=0
- PASS setup-no-btc-orders (metamask.perps.ensure_orders, 998ms): matching=0
- PASS setup-show-margin-control (ui.scroll, 3.2s): ok=true, testId=perps-pro-order-form-margin-mode, intoView=true, alreadyVisible=true
- PASS setup-open-order-type (ui.press, 2.4s): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-6
- PASS setup-basic-tab (ui.press, 2.2s): ok=true, testId=perps-order-type-tab-basic, deviceName=mm-6
- PASS setup-wait-market-type (ui.wait_for, 1.4s): matched=true, testId=perps-order-type-market, expected=visible, present=true, visible=true
- PASS setup-pick-market-type (ui.press, 2.0s): ok=true, testId=perps-order-type-market, deviceName=mm-6
- PASS gate-margin-button (ui.wait_for, 3.4s): matched=true, testId=perps-pro-order-form-margin-mode, expected=visible, present=true, visible=true
- PASS ac1-open-sheet (ui.press, 2.0s): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-6
- PASS ac1-wait-cross-option (ui.wait_for, 1.4s): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-press-cross (ui.press, 4.0s): ok=true, testId=perps-margin-mode-cross, deviceName=mm-6
- PASS ac1-wait-sheet-closed (ui.wait_for, 5.0s): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac1-show-margin-control (ui.swipe, 19s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac1-wait-cross-label (ui.wait_for, 5.0s): matched=true, testId=perps-pro-order-form-margin-mode, text=Cross, textMatch=exact, expected=visible
- PASS ac1-screenshot-cross-label (ui.screenshot, 3.0s): path=screenshots/evidence-ac1-cross-label.png
- PASS ac1-reopen-sheet (ui.press, 1.7s): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-6
- PASS ac1-wait-cross-selected (ui.wait_for, 1.3s): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-screenshot-cross-sheet (ui.screenshot, 1.7s): path=screenshots/evidence-ac1-cross-sheet.png
- PASS ac2-keep-cross (ui.press, 2.3s): ok=true, testId=perps-margin-mode-cross, deviceName=mm-6
- PASS ac2-wait-sheet-closed (ui.wait_for, 2.0s): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac2-scroll-size (ui.scroll, 2.0s): ok=true, testId=perps-pro-order-form-size-card, intoView=true, alreadyVisible=true
- PASS ac2-wait-size (ui.wait_for, 1.7s): matched=true, testId=perps-pro-order-form-size-card, expected=visible, present=true, visible=true
- PASS ac2-set-size (ui.set_input, 1.6s): ok=true, testId=perps-pro-order-form-size-input, value=15, deviceName=mm-6
- PASS ac2-scroll-submit (ui.scroll, 2.4s): animated=false, offset=600, ok=true, testId=perps-pro-order-form-summary-fees, deviceName=mm-6
- PASS ac2-wait-submit (ui.wait_for, 2.2s): matched=true, testId=perps-pro-order-form-place-order, expected=visible, present=true, visible=true
- PASS ac2-press-submit (ui.press, 2.6s): ok=true, testId=perps-pro-order-form-place-order, deviceName=mm-6
- PASS ac2-assert-position-open (metamask.perps.assert_positions, 4.1s): matching=1
- PASS ac2-filter-btc (ui.press, 1.9s): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-6
- PASS ac2-swipe-to-positions (ui.swipe, 7.2s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-swipe-to-card (ui.swipe, 7.3s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-wait-cross-tag (ui.wait_for, 1.6s): matched=true, testId=cross-margin-tag-pro-BTC, expected=visible, present=true, visible=true
- PASS ac2-screenshot-cross-position (ui.screenshot, 2.2s): path=screenshots/evidence-ac2-cross-position.png
- PASS teardown-close-btc (metamask.perps.close_positions, 4.9s): matching=0
- PASS teardown-assert-flat (metamask.perps.assert_positions, 638ms): matching=0
- PASS teardown-unfilter-btc (ui.press, 2.1s): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-6
- PASS teardown-clear-flag (metamask.feature_flags.clear, 432ms): proof=mobile-remote-feature-flags
- PASS ac2-run-order-params-tests (command, 13s): exitCode=0, stdout=PASS app/components/UI/Perps/utils/orderParams.test.ts (6.939 s)
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts (8.302 s)

Test Suites: 2 passed, 2 total
Tests:       325 skipped, 40 passed, 365 total
Snapshots:   0 total
Time:        8.645 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts|app\/components\/UI\/Perps\/utils\/orderParams.test.ts/i with tests matching "margin mode".

- PASS ac2-assert-tests-pass (assert_exit_code, 94ms): source=ac2-run-order-params-tests, expected=0, actual=0
- PASS ac3-run-gating-tests (command, 9.9s): exitCode=0, stdout=PASS app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.test.tsx
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.test.tsx (5.296 s)

Test Suites: 2 passed, 2 total
Tests:       40 skipped, 15 passed, 55 total
Snapshots:   0 total
Time:        5.524 s
Ran all test suites matching /app\/components\/UI\/Perps\/components\/PerpsMarginModeBottomSheet\/PerpsMarginModeBottomSheet.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderFormPanel.test.tsx/i with tests matching "cross margin".

- PASS ac3-assert-tests-pass (assert_exit_code, 86ms): source=ac3-run-gating-tests, expected=0, actual=0
- PASS ac4-run-cross-position-tests (command, 8.0s): exitCode=0, stdout=      ○ skipped restores reduceOnly from the pending trade draft
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
Tests:       340 skipped, 3 passed, 343 total
Snapshots:   0 total
Time:        3.974 s, estimated 9 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts/i with tests matching "existing cross position".

- PASS ac4-assert-tests-pass (assert_exit_code, 84ms): source=ac4-run-cross-position-tests, expected=0, actual=0
- PASS done (end, 0ms)
