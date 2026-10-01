# MetaMask Recipe Run

Status: pass
Duration: 113s
Nodes: 45/45 passed

## Side findings
- REVIEW 6 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-flag (metamask.feature_flags.set, 421ms): proof=mobile-remote-feature-flags
- PASS setup-pro (metamask.perps.start_state, 2.1s): proof=metamask-perps-start-state
- PASS setup-no-btc-position (metamask.perps.ensure_positions, 5.4s): matching=0
- PASS setup-no-btc-orders (metamask.perps.ensure_orders, 754ms): matching=0
- PASS setup-show-margin-control (ui.scroll, 990ms): ok=true, testId=perps-pro-order-form-margin-mode, intoView=true, alreadyVisible=true
- PASS setup-open-order-type (ui.press, 757ms): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-2
- PASS setup-basic-tab (ui.press, 599ms): ok=true, testId=perps-order-type-tab-basic, deviceName=mm-2
- PASS setup-wait-market-type (ui.wait_for, 558ms): matched=true, testId=perps-order-type-market, expected=visible, present=true, visible=true
- PASS setup-pick-market-type (ui.press, 631ms): ok=true, testId=perps-order-type-market, deviceName=mm-2
- PASS gate-margin-button (ui.wait_for, 1.1s): matched=true, testId=perps-pro-order-form-margin-mode, expected=visible, present=true, visible=true
- PASS ac1-open-sheet (ui.press, 585ms): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-2
- PASS ac1-wait-cross-option (ui.wait_for, 700ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-press-cross (ui.press, 595ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-2
- PASS ac1-wait-sheet-closed (ui.wait_for, 858ms): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac1-show-margin-control (ui.swipe, 4.7s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac1-wait-cross-label (ui.wait_for, 869ms): matched=true, testId=perps-pro-order-form-margin-mode, text=Cross, textMatch=exact, expected=visible
- PASS ac1-screenshot-cross-label (ui.screenshot, 986ms): path=screenshots/evidence-ac1-cross-label.png
- PASS ac1-reopen-sheet (ui.press, 594ms): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-2
- PASS ac1-wait-cross-selected (ui.wait_for, 687ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-screenshot-cross-sheet (ui.screenshot, 821ms): path=screenshots/evidence-ac1-cross-sheet.png
- PASS ac2-keep-cross (ui.press, 595ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-2
- PASS ac2-wait-sheet-closed (ui.wait_for, 765ms): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac2-scroll-size (ui.scroll, 840ms): ok=true, testId=perps-pro-order-form-size-card, intoView=true, alreadyVisible=true
- PASS ac2-wait-size (ui.wait_for, 826ms): matched=true, testId=perps-pro-order-form-size-card, expected=visible, present=true, visible=true
- PASS ac2-set-size (ui.set_input, 925ms): ok=true, testId=perps-pro-order-form-size-input, value=15, deviceName=mm-2
- PASS ac2-scroll-submit (ui.scroll, 1.3s): animated=false, offset=600, ok=true, testId=perps-pro-order-form-summary-fees, deviceName=mm-2
- PASS ac2-wait-submit (ui.wait_for, 847ms): matched=true, testId=perps-pro-order-form-place-order, expected=visible, present=true, visible=true
- PASS ac2-press-submit (ui.press, 888ms): ok=true, testId=perps-pro-order-form-place-order, deviceName=mm-2
- PASS ac2-assert-position-open (metamask.perps.assert_positions, 8.5s): matching=1
- PASS ac2-filter-btc (ui.press, 895ms): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-2
- PASS ac2-swipe-to-positions (ui.swipe, 4.6s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-swipe-to-card (ui.swipe, 4.2s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-wait-cross-tag (ui.wait_for, 948ms): matched=true, testId=cross-margin-tag-pro-BTC, expected=visible, present=true, visible=true
- PASS ac2-screenshot-cross-position (ui.screenshot, 1.1s): path=screenshots/evidence-ac2-cross-position.png
- PASS teardown-close-btc (metamask.perps.close_positions, 4.0s): matching=0
- PASS teardown-assert-flat (metamask.perps.assert_positions, 401ms): matching=0
- PASS teardown-unfilter-btc (ui.press, 818ms): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-2
- PASS teardown-clear-flag (metamask.feature_flags.clear, 353ms): proof=mobile-remote-feature-flags
- PASS ac2-run-order-params-tests (command, 28s): exitCode=0, stdout=PASS app/components/UI/Perps/utils/orderParams.test.ts (13.313 s)
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts (14.569 s)

Test Suites: 2 passed, 2 total
Tests:       328 skipped, 40 passed, 368 total
Snapshots:   0 total
Time:        14.717 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts|app\/components\/UI\/Perps\/utils\/orderParams.test.ts/i with tests matching "margin mode".

- PASS ac2-assert-tests-pass (assert_exit_code, 39ms): source=ac2-run-order-params-tests, expected=0, actual=0
- PASS ac3-run-gating-tests (command, 13s): exitCode=0, stdout=PASS app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.test.tsx
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.test.tsx

Test Suites: 2 passed, 2 total
Tests:       40 skipped, 15 passed, 55 total
Snapshots:   0 total
Time:        3.126 s, estimated 4 s
Ran all test suites matching /app\/components\/UI\/Perps\/components\/PerpsMarginModeBottomSheet\/PerpsMarginModeBottomSheet.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderFormPanel.test.tsx/i with tests matching "cross margin".

- PASS ac3-assert-tests-pass (assert_exit_code, 56ms): source=ac3-run-gating-tests, expected=0, actual=0
- PASS ac4-run-cross-position-tests (command, 12s): exitCode=0, stdout=      ○ skipped sets the size slider max to the open position notional when Reduce Only is on
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
      ○ skipped opens TP/SL as a bottom sheet when assigned the bottom-sheet arm
      ○ skipped omits useBottomSheet from the TP/SL route on the screen arm
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
Tests:       343 skipped, 3 passed, 346 total
Snapshots:   0 total
Time:        1.678 s, estimated 15 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts/i with tests matching "existing cross position".

- PASS ac4-assert-tests-pass (assert_exit_code, 41ms): source=ac4-run-cross-position-tests, expected=0, actual=0
- PASS done (end, 0ms)
