# MetaMask Recipe Run

Status: pass
Duration: 85s
Nodes: 30/30 passed

## Side findings
- REVIEW 14 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-cross-flag (metamask.feature_flags.set, 347ms): proof=mobile-remote-feature-flags
- PASS setup-cross-pro/choose-account (switch, 35ms): matched=false, value=account:Trading, expected=account:
- PASS setup-cross-pro/select-account (metamask.perps.start_state, 6.8s): proof=metamask-perps-start-state
- PASS setup-cross-pro/ensure-state (metamask.perps.start_state, 5.4s): proof=metamask-perps-start-state
- PASS setup-cross-pro/done (end, 0ms)
- PASS setup-cross-pro (call, 12s): ref=perps.pro-order-start-state, status=pass
- PASS setup-cross-sol-flat (metamask.perps.ensure_positions, 2.7s): matching=0
- PASS ac5-scroll-mode (ui.scroll, 868ms): ok=true, testId=perps-pro-order-form-margin-mode, intoView=true, alreadyVisible=true
- PASS ac5-open-mode (ui.press, 549ms): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-6
- PASS ac5-wait-cross-option (ui.wait_for, 804ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac5-screenshot-sheet (ui.screenshot, 703ms): path=screenshots/evidence-ac5-margin-mode-sheet.png
- PASS ac5-pick-cross (ui.press, 734ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-6
- PASS ac5-assert-cross-label (ui.wait_for, 836ms): matched=true, text=Cross, textMatch=contains, expected=visible, present=true
- PASS ac5-scroll-size (ui.scroll, 834ms): ok=true, testId=perps-pro-order-form-size-card, intoView=true, alreadyVisible=true
- PASS ac5-set-size (ui.set_input, 794ms): ok=true, testId=perps-pro-order-form-size-input, value=15, deviceName=mm-6
- PASS ac5-scroll-submit (ui.scroll, 1.3s): animated=false, offset=600, ok=true, testId=perps-pro-order-form-summary-fees, deviceName=mm-6
- PASS ac5-wait-submit (ui.wait_for, 814ms): matched=true, testId=perps-pro-order-form-place-order, expected=visible, present=true, visible=true
- PASS ac5-place-order (ui.press, 930ms): ok=true, testId=perps-pro-order-form-place-order, deviceName=mm-6
- PASS ac5-assert-position-open (metamask.perps.assert_positions, 5.9s): matching=1
- PASS ac5-swipe-to-positions (ui.swipe, 8.2s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac5-swipe-to-sol-card (ui.swipe, 3.6s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac5-assert-cross-tag (ui.wait_for, 806ms): matched=true, testId=cross-margin-tag-pro-SOL, expected=visible, present=true, visible=true
- PASS ac5-screenshot-position (ui.screenshot, 1.1s): path=screenshots/evidence-ac5-cross-position.png
- PASS teardown-cross-sol (metamask.perps.ensure_positions, 3.7s): matching=0
- PASS teardown-cross-flag (metamask.feature_flags.clear, 305ms): proof=mobile-remote-feature-flags
- PASS ac3-run-unit-tests (command, 10s): exitCode=0, stdout=PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.test.tsx (5.883 s)
PASS app/components/UI/Perps/components/PerpsModifyActionSheet/PerpsModifyActionSheet.test.tsx
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts (6.894 s)
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProPositionCard.test.tsx (7.046 s)
PASS app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.test.tsx
PASS app/components/UI/Perps/utils/orderParams.test.ts

Test Suites: 6 passed, 6 total
Tests:       426 passed, 426 total
Snapshots:   0 total
Time:        7.422 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/orderParams.test.ts|app\/components\/UI\/Perps\/components\/PerpsMarginModeBottomSheet\/PerpsMarginModeBottomSheet.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderFormPanel.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts|app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProPositionCard.test.tsx|app\/components\/UI\/Perps\/components\/PerpsModifyActionSheet\/PerpsModifyActionSheet.test.tsx/i.

- PASS ac3-assert-tests-pass (assert_exit_code, 35ms): source=ac3-run-unit-tests, expected=0, actual=0
- PASS ac6-run-view-test (command, 25s): exitCode=0, stdout=PASS app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.view.test.tsx (12.385 s)
  PerpsOrderView
    ✓ routes cross-margin positions to the warning modal instead of placing an order (650 ms)
    ✓ places a Cross order on a Cross position when cross margin is enabled (481 ms)
    ○ skipped submits a market long after the trader reviews the calculated order fees and details
    ○ skipped keeps the minimum-order error visible during protocol validation
    ○ skipped reopens a below-minimum order while market sizing is unavailable
    ○ skipped switches to limit order, accepts the Mid preset, and routes to TP/SL setup
    ○ skipped blocks order submission when the account cannot satisfy the minimum order amount
    ○ skipped shows a single insufficient-funds treatment when the balance cannot cover the margin
    ○ skipped keeps a blocking minimum-amount error visible next to the insufficient-funds banner
    Trade sheet (bottom-sheet treatment)
      ○ skipped leaves the sheet for the market page as soon as the order is submitted
      ○ skipped does not place an order when the sheet is gone while validation is pending

Test Suites: 1 passed, 1 total
Tests:       9 skipped, 2 passed, 11 total
Snapshots:   0 total
Time:        12.505 s, estimated 13 s
Force exiting Jest: Have you considered using `--detectOpenHandles` to detect async operations that kept running after all tests finished?

- PASS ac6-assert-view-test-pass (assert_exit_code, 31ms): source=ac6-run-view-test, expected=0, actual=0
- PASS done (end, 0ms)
