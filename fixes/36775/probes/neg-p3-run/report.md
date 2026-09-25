# MetaMask Recipe Run

Status: fail
Duration: 102s
Nodes: 30/31 passed

## Side findings
- REVIEW 24 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 23s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 122ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 177ms): source=start, stream=stdout
- PASS setup-session/account (switch, 75ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 150ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 24s): ref=perps.venue-start-state, status=pass
- PASS setup-pin-screen-variant (metamask.feature_flags.set, 1.3s): proof=mobile-remote-feature-flags
- PASS setup-assert-position (metamask.perps.ensure_positions, 1.7s): matching=1
- PASS ac5-pin-bottom-sheet (metamask.feature_flags.set, 848ms): proof=mobile-remote-feature-flags
- PASS ac5-add-home (ui.navigate, 4.1s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac5-add-nav (ui.navigate, 5.0s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac5-add-wait-margin-card (ui.wait_for, 2.9s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac5-add-press-margin-card (ui.press, 1.7s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS ac5-add-open-keypad (ui.press, 2.6s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS ac5-add-key-2 (ui.press, 2.8s): ok=true, testId=keypad-key-2, deviceName=mm-6
- PASS ac5-add-key-0 (ui.press, 4.0s): ok=true, testId=keypad-key-0, deviceName=mm-6
- PASS ac5-add-close-keypad (ui.press, 1.6s): ok=true, testId=perps-adjust-margin-bottom-sheet-done-button, deviceName=mm-6
- PASS ac5-add-confirm (ui.press, 3.6s): ok=true, testId=perps-adjust-margin-bottom-sheet-confirm-button, deviceName=mm-6
- PASS ac5-add-assert-added (ui.wait_for, 2.6s): matched=true, text=Added $20 margin, textMatch=contains, expected=visible, present=true
- PASS ac5-home (ui.navigate, 2.5s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac5-nav (ui.navigate, 8.4s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac5-wait-margin-card (ui.wait_for, 2.0s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac5-press-margin-card (ui.press, 2.2s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS ac5-press-remove-mode (ui.press, 1.5s): ok=true, testId=perps-adjust-margin-bottom-sheet-remove-mode, deviceName=mm-6
- PASS ac5-open-keypad (ui.press, 1.4s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS ac5-press-max (ui.press, 3.1s): ok=true, text=Max, deviceName=mm-6
- PASS ac5-close-keypad (ui.press, 1.4s): ok=true, testId=perps-adjust-margin-bottom-sheet-done-button, deviceName=mm-6
- PASS ac5-assert-no-explanation (ui.wait_for, 1.2s): matched=true, testId=perps-adjust-margin-bottom-sheet-no-removable-margin, expected=absent, present=false, visible=false
- PASS ac5-drain-live-limit (command, 2.1s): exitCode=0, stdout="DRAINED removed=19.37 exchangeMaxLeft=1.00"

- FAIL ac5-assert-explanation (ui.wait_for, 15s)
