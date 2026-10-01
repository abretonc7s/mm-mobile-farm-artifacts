# MetaMask Recipe Run

Status: pass
Duration: 484s
Nodes: 104/104 passed

## Side findings
- REVIEW 5 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 4.2s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 500ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 359ms): source=start, stream=stdout
- PASS setup-session/account (switch, 324ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 261ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 8.3s): ref=perps.venue-start-state, status=pass
- PASS setup-pin-screen-variant (metamask.feature_flags.set, 1.1s): proof=mobile-remote-feature-flags
- PASS setup-assert-position (metamask.perps.ensure_positions, 2.8s): matching=1
- PASS setup-add-home (ui.navigate, 5.2s): route=WalletView, page=home, proof=agentic-navigation
- PASS setup-add-nav (ui.navigate, 7.2s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-lite-mode (metamask.perps.ensure_mode, 1.6s): proof=visible-market-detail-root-and-active-mode-control
- PASS setup-add-wait-margin-card (ui.wait_for, 3.9s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS setup-add-press-margin-card (ui.press, 3.8s): ok=true, testId=position-card-margin, deviceName=mmdev-6
- PASS setup-press-add (ui.press, 3.0s): ok=true, testId=perps-adjust-margin-add-btn, deviceName=mmdev-6
- PASS setup-open-keypad (ui.press, 13s): ok=true, testId=perps-amount-display-touchable, deviceName=mmdev-6
- PASS setup-key-2 (ui.press, 15s): ok=true, testId=keypad-key-2, deviceName=mmdev-6
- PASS setup-key-0 (ui.press, 9.3s): ok=true, testId=keypad-key-0, deviceName=mmdev-6
- PASS setup-close-keypad (ui.press, 12s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mmdev-6
- PASS setup-confirm-add (ui.press, 11s): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mmdev-6
- PASS setup-assert-added (ui.wait_for, 8.5s): matched=true, testId=perps-market-details-close-button, expected=visible, present=true, visible=true
- PASS ac1-home (ui.navigate, 7.4s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac1-nav (ui.navigate, 6.8s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac1-wait-margin-card (ui.wait_for, 6.6s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac1-press-margin-card (ui.press, 5.8s): ok=true, testId=position-card-margin, deviceName=mmdev-6
- PASS ac1-press-remove (ui.press, 5.7s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mmdev-6
- PASS ac1-open-keypad (ui.press, 4.1s): ok=true, testId=perps-amount-display-touchable, deviceName=mmdev-6
- PASS ac1-press-max (ui.press, 825ms): ok=true, text=Max, deviceName=mmdev-6
- PASS ac1-close-keypad (ui.press, 1.5s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mmdev-6
- PASS ac1-wait-available (ui.wait_for, 3.7s): matched=true, testId=perps-adjust-margin-available-value, expected=visible, present=true, visible=true
- PASS ac1-screenshot-max-form (ui.screenshot, 6.0s): path=screenshots/ac1-screenshot-max-form.png
- PASS ac1-press-confirm (ui.press, 2.9s): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mmdev-6
- PASS ac1-assert-removed (ui.wait_for, 1.9s): matched=true, testId=perps-market-details-close-button, expected=visible, present=true, visible=true
- PASS ac1-screenshot-removed (ui.screenshot, 2.1s): path=screenshots/ac1-screenshot-removed.png
- PASS ac1-assert-no-rejection (ui.wait_for, 5.2s): matched=true, text=Margin adjustment failed, textMatch=contains, expected=absent, present=false
- PASS setup-sol-flat (metamask.perps.ensure_positions, 1.0s): matching=0
- PASS setup-sol-open (metamask.perps.place_order, 9.8s): matching=1
- PASS setup-sol-assert (metamask.perps.assert_positions, 553ms): matching=1
- PASS ac2-home (ui.navigate, 5.3s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac2-nav (ui.navigate, 5.1s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac2-wait-margin-card (ui.wait_for, 1.6s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac2-press-margin-card (ui.press, 5.0s): ok=true, testId=position-card-margin, deviceName=mmdev-6
- PASS ac2-press-remove (ui.press, 1.3s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mmdev-6
- PASS ac2-assert-explanation (ui.wait_for, 1.4s): matched=true, testId=perps-adjust-margin-no-removable-margin, expected=visible, present=true, visible=true
- PASS ac2-screenshot-zero-state (ui.screenshot, 2.0s): path=screenshots/ac2-screenshot-zero-state.png
- PASS teardown-sol (metamask.perps.ensure_positions, 4.6s): matching=0
- PASS ac4-add-home (ui.navigate, 3.9s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac4-add-nav (ui.navigate, 5.9s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac4-add-wait-margin-card (ui.wait_for, 4.7s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac4-add-press-margin-card (ui.press, 6.7s): ok=true, testId=position-card-margin, deviceName=mmdev-6
- PASS ac4-add-press-add (ui.press, 4.4s): ok=true, testId=perps-adjust-margin-add-btn, deviceName=mmdev-6
- PASS ac4-add-open-keypad (ui.press, 3.3s): ok=true, testId=perps-amount-display-touchable, deviceName=mmdev-6
- PASS ac4-add-key-2 (ui.press, 3.5s): ok=true, testId=keypad-key-2, deviceName=mmdev-6
- PASS ac4-add-key-0 (ui.press, 4.3s): ok=true, testId=keypad-key-0, deviceName=mmdev-6
- PASS ac4-add-close-keypad (ui.press, 4.9s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mmdev-6
- PASS ac4-add-confirm (ui.press, 7.6s): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mmdev-6
- PASS ac4-add-assert-added (ui.wait_for, 4.0s): matched=true, testId=perps-market-details-close-button, expected=visible, present=true, visible=true
- PASS ac4-home (ui.navigate, 5.0s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac4-nav (ui.navigate, 6.4s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac4-wait-margin-card (ui.wait_for, 4.2s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac4-press-margin-card (ui.press, 4.0s): ok=true, testId=position-card-margin, deviceName=mmdev-6
- PASS ac4-press-remove (ui.press, 4.9s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mmdev-6
- PASS ac4-open-keypad (ui.press, 3.0s): ok=true, testId=perps-amount-display-touchable, deviceName=mmdev-6
- PASS ac4-press-max (ui.press, 1.5s): ok=true, text=Max, deviceName=mmdev-6
- PASS ac4-close-keypad (ui.press, 2.3s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mmdev-6
- PASS ac4-assert-no-explanation (ui.wait_for, 1.2s): matched=true, testId=perps-adjust-margin-no-removable-margin, expected=absent, present=false, visible=false
- PASS ac4-reopen-keypad (ui.press, 2.5s): ok=true, testId=perps-amount-display-touchable, deviceName=mmdev-6
- PASS ac4-wait-keypad-open (ui.wait_for, 1.2s): matched=true, testId=perps-adjust-margin-done-button, expected=visible, present=true, visible=true
- PASS ac4-drain-live-limit (command, 1.8s): exitCode=0, stdout="DRAINED removed=21.55 exchangeMaxLeft=1.00"

- PASS ac4-assert-keypad-closed (ui.wait_for, 2.0s): matched=true, testId=perps-adjust-margin-done-button, expected=visible, present=true, visible=true
- PASS ac4-assert-explanation (ui.wait_for, 1.5s): matched=true, testId=perps-adjust-margin-no-removable-margin, expected=absent, present=false, visible=false
- PASS ac4-assert-no-stale-error (ui.wait_for, 1.5s): matched=true, text=Amount exceeds maximum removable margin, textMatch=contains, expected=absent, present=false
- PASS ac4-screenshot (ui.screenshot, 6.5s): path=screenshots/ac4-screenshot.png
- PASS ac5-pin-bottom-sheet (metamask.feature_flags.set, 1.9s): proof=mobile-remote-feature-flags
- PASS ac5-add-home (ui.navigate, 5.1s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac5-add-nav (ui.navigate, 4.1s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac5-add-wait-margin-card (ui.wait_for, 7.5s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac5-add-press-margin-card (ui.press, 3.5s): ok=true, testId=position-card-margin, deviceName=mmdev-6
- PASS ac5-add-open-keypad (ui.press, 9.2s): ok=true, testId=perps-amount-display-touchable, deviceName=mmdev-6
- PASS ac5-add-key-2 (ui.press, 2.5s): ok=true, testId=keypad-key-2, deviceName=mmdev-6
- PASS ac5-add-key-0 (ui.press, 2.5s): ok=true, testId=keypad-key-0, deviceName=mmdev-6
- PASS ac5-add-close-keypad (ui.press, 2.2s): ok=true, testId=perps-adjust-margin-bottom-sheet-done-button, deviceName=mmdev-6
- PASS ac5-add-confirm (ui.press, 1.9s): ok=true, testId=perps-adjust-margin-bottom-sheet-confirm-button, deviceName=mmdev-6
- PASS ac5-add-assert-added (ui.wait_for, 2.6s): matched=true, testId=perps-market-details-close-button, expected=visible, present=true, visible=true
- PASS ac5-home (ui.navigate, 4.5s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac5-nav (ui.navigate, 5.2s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac5-wait-margin-card (ui.wait_for, 1.2s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac5-press-margin-card (ui.press, 1.5s): ok=true, testId=position-card-margin, deviceName=mmdev-6
- PASS ac5-press-remove-mode (ui.press, 1.4s): ok=true, testId=perps-adjust-margin-bottom-sheet-remove-mode, deviceName=mmdev-6
- PASS ac5-open-keypad (ui.press, 1.5s): ok=true, testId=perps-amount-display-touchable, deviceName=mmdev-6
- PASS ac5-press-max (ui.press, 1.7s): ok=true, text=Max, deviceName=mmdev-6
- PASS ac5-close-keypad (ui.press, 1.5s): ok=true, testId=perps-adjust-margin-bottom-sheet-done-button, deviceName=mmdev-6
- PASS ac5-assert-no-explanation (ui.wait_for, 1.4s): matched=true, testId=perps-adjust-margin-bottom-sheet-no-removable-margin, expected=absent, present=false, visible=false
- PASS ac5-reopen-keypad (ui.press, 2.8s): ok=true, testId=perps-amount-display-touchable, deviceName=mmdev-6
- PASS ac5-wait-keypad-open (ui.wait_for, 4.5s): matched=true, testId=perps-adjust-margin-bottom-sheet-done-button, expected=visible, present=true, visible=true
- PASS ac5-drain-live-limit (command, 3.4s): exitCode=0, stdout="DRAINED removed=19.85 exchangeMaxLeft=1.00"

- PASS ac5-assert-keypad-closed (ui.wait_for, 11s): matched=true, testId=perps-adjust-margin-bottom-sheet-done-button, expected=visible, present=true, visible=true
- PASS ac5-assert-explanation (ui.wait_for, 6.5s): matched=true, testId=perps-adjust-margin-bottom-sheet-no-removable-margin, expected=absent, present=false, visible=false
- PASS ac5-assert-no-stale-error (ui.wait_for, 11s): matched=true, testId=perps-adjust-margin-bottom-sheet-error, expected=absent, present=false, visible=false
- PASS ac5-screenshot (ui.screenshot, 7.2s): path=screenshots/ac5-screenshot.png
- PASS teardown-clear-flags (metamask.feature_flags.clear, 2.9s): proof=mobile-remote-feature-flags
- PASS ac3-run-unit-tests (command, 36s): exitCode=0, stdout=PASS app/components/UI/Perps/components/PerpsAdjustMarginBottomSheet/PerpsAdjustMarginBottomSheet.test.tsx (21.872 s)
PASS app/components/UI/Perps/hooks/usePerpsAdjustMarginData.test.ts
PASS app/components/UI/Perps/Views/PerpsAdjustMarginView/PerpsAdjustMarginView.test.tsx (24.333 s)
PASS app/components/UI/Perps/hooks/usePerpsFreshRemovalLimit.test.ts
PASS app/components/UI/Perps/utils/marginUtils.test.ts
PASS app/components/UI/Perps/hooks/usePerpsToasts.test.tsx (26.116 s)
PASS app/components/UI/Perps/hooks/usePerpsMarginAdjustment.test.ts

Test Suites: 7 passed, 7 total
Tests:       245 passed, 245 total
Snapshots:   0 total
Time:        26.688 s, estimated 43 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/marginUtils.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsMarginAdjustment.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsFreshRemovalLimit.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsAdjustMarginData.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsToasts.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsAdjustMarginView\/PerpsAdjustMarginView.test.tsx|app\/components\/UI\/Perps\/components\/PerpsAdjustMarginBottomSheet\/PerpsAdjustMarginBottomSheet.test.tsx/i.

- PASS ac3-assert-tests-pass (assert_exit_code, 80ms): source=ac3-run-unit-tests, expected=0, actual=0
- PASS done (end, 0ms)
