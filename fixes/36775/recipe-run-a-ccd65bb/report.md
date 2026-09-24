# MetaMask Recipe Run

Status: pass
Duration: 92s
Nodes: 50/50 passed

## Side findings
- REVIEW 15 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 14s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 218ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 431ms): source=start, stream=stdout
- PASS setup-session/account (switch, 99ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 66ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 15s): ref=perps.venue-start-state, status=pass
- PASS setup-pin-screen-variant (metamask.feature_flags.set, 384ms): proof=mobile-remote-feature-flags
- PASS setup-assert-position (metamask.perps.ensure_positions, 970ms): matching=1
- PASS setup-add-home (ui.navigate, 1.6s): route=WalletView, page=home, proof=agentic-navigation
- PASS setup-add-nav (ui.navigate, 2.4s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-lite-mode (metamask.perps.ensure_mode, 556ms): proof=visible-market-detail-root-and-active-mode-control
- PASS setup-add-wait-margin-card (ui.wait_for, 944ms): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS setup-add-press-margin-card (ui.press, 1.1s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS setup-press-add (ui.press, 1.1s): ok=true, testId=perps-adjust-margin-add-btn, deviceName=mm-6
- PASS setup-open-keypad (ui.press, 1.6s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS setup-key-2 (ui.press, 953ms): ok=true, testId=keypad-key-2, deviceName=mm-6
- PASS setup-key-0 (ui.press, 949ms): ok=true, testId=keypad-key-0, deviceName=mm-6
- PASS setup-close-keypad (ui.press, 850ms): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS setup-confirm-add (ui.press, 1.2s): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mm-6
- PASS setup-assert-added (ui.wait_for, 1.6s): matched=true, text=Added $20 margin, textMatch=contains, expected=visible, present=true
- PASS ac1-home (ui.navigate, 1.7s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac1-nav (ui.navigate, 2.4s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac1-wait-margin-card (ui.wait_for, 1.1s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac1-press-margin-card (ui.press, 1.4s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS ac1-press-remove (ui.press, 1.1s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mm-6
- PASS ac1-open-keypad (ui.press, 903ms): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS ac1-press-max (ui.press, 941ms): ok=true, text=Max, deviceName=mm-6
- PASS ac1-close-keypad (ui.press, 848ms): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS ac1-wait-available (ui.wait_for, 843ms): matched=true, testId=perps-adjust-margin-available-value, expected=visible, present=true, visible=true
- PASS ac1-screenshot-max-form (ui.screenshot, 1.2s): path=screenshots/evidence-ac1-max-form.png
- PASS ac1-press-confirm (ui.press, 947ms): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mm-6
- PASS ac1-assert-removed (ui.wait_for, 1.5s): matched=true, text=Removed $, textMatch=contains, expected=visible, present=true
- PASS ac1-screenshot-removed (ui.screenshot, 1.1s): path=screenshots/evidence-ac1-removed-toast.png
- PASS ac1-assert-no-rejection (ui.wait_for, 1.7s): matched=true, text=Margin adjustment failed, textMatch=contains, expected=absent, present=false
- PASS setup-sol-flat (metamask.perps.ensure_positions, 827ms): matching=0
- PASS setup-sol-open (metamask.perps.place_order, 7.3s): matching=1
- PASS setup-sol-assert (metamask.perps.assert_positions, 485ms): matching=1
- PASS ac2-home (ui.navigate, 1.4s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac2-nav (ui.navigate, 2.3s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac2-wait-margin-card (ui.wait_for, 1.2s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac2-press-margin-card (ui.press, 1.1s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS ac2-press-remove (ui.press, 1.2s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mm-6
- PASS ac2-assert-explanation (ui.wait_for, 1.1s): matched=true, testId=perps-adjust-margin-no-removable-margin, expected=visible, present=true, visible=true
- PASS ac2-screenshot-zero-state (ui.screenshot, 1.4s): path=screenshots/evidence-ac2-zero-state.png
- PASS teardown-sol (metamask.perps.ensure_positions, 4.8s): matching=0
- PASS teardown-clear-flags (metamask.feature_flags.clear, 556ms): proof=mobile-remote-feature-flags
- PASS ac3-run-unit-tests (command, 16s): exitCode=0, stdout=PASS app/components/UI/Perps/hooks/usePerpsMarginAdjustment.test.ts
PASS app/components/UI/Perps/components/PerpsAdjustMarginBottomSheet/PerpsAdjustMarginBottomSheet.test.tsx (7.487 s)
PASS app/components/UI/Perps/hooks/usePerpsAdjustMarginData.test.ts
PASS app/components/UI/Perps/Views/PerpsAdjustMarginView/PerpsAdjustMarginView.test.tsx (10.838 s)
PASS app/components/UI/Perps/utils/marginUtils.test.ts
PASS app/components/UI/Perps/hooks/usePerpsToasts.test.tsx (11.975 s)

Test Suites: 6 passed, 6 total
Tests:       238 passed, 238 total
Snapshots:   0 total
Time:        12.361 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/marginUtils.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsMarginAdjustment.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsAdjustMarginData.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsToasts.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsAdjustMarginView\/PerpsAdjustMarginView.test.tsx|app\/components\/UI\/Perps\/components\/PerpsAdjustMarginBottomSheet\/PerpsAdjustMarginBottomSheet.test.tsx/i.

- PASS ac3-assert-tests-pass (assert_exit_code, 61ms): source=ac3-run-unit-tests, expected=0, actual=0
- PASS done (end, 0ms)
