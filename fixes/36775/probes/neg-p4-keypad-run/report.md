# MetaMask Recipe Run

Status: fail
Duration: 102s
Nodes: 33/34 passed

## Side findings
- REVIEW 22 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 22s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 80ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 65ms): source=start, stream=stdout
- PASS setup-session/account (switch, 66ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 73ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 23s): ref=perps.venue-start-state, status=pass
- PASS setup-pin-screen-variant (metamask.feature_flags.set, 1.3s): proof=mobile-remote-feature-flags
- PASS setup-assert-position (metamask.perps.ensure_positions, 2.9s): matching=1
- PASS setup-add-home (ui.navigate, 3.5s): route=WalletView, page=home, proof=agentic-navigation
- PASS setup-add-nav (ui.navigate, 6.7s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-lite-mode (metamask.perps.ensure_mode, 640ms): proof=visible-market-detail-root-and-active-mode-control
- PASS setup-add-wait-margin-card (ui.wait_for, 2.1s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS setup-add-press-margin-card (ui.press, 2.7s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS setup-press-add (ui.press, 2.1s): ok=true, testId=perps-adjust-margin-add-btn, deviceName=mm-6
- PASS setup-open-keypad (ui.press, 1.7s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS setup-key-2 (ui.press, 1.6s): ok=true, testId=keypad-key-2, deviceName=mm-6
- PASS setup-key-0 (ui.press, 1.4s): ok=true, testId=keypad-key-0, deviceName=mm-6
- PASS setup-close-keypad (ui.press, 1.8s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS setup-confirm-add (ui.press, 1.2s): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mm-6
- PASS setup-assert-added (ui.wait_for, 3.9s): matched=true, text=Added $20 margin, textMatch=contains, expected=visible, present=true
- PASS ac4-home (ui.navigate, 3.5s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac4-nav (ui.navigate, 4.1s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac4-wait-margin-card (ui.wait_for, 2.7s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac4-press-margin-card (ui.press, 1.8s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS ac4-press-remove (ui.press, 3.0s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mm-6
- PASS ac4-open-keypad (ui.press, 2.8s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS ac4-press-max (ui.press, 2.8s): ok=true, text=Max, deviceName=mm-6
- PASS ac4-close-keypad (ui.press, 1.1s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS ac4-assert-no-explanation (ui.wait_for, 1.2s): matched=true, testId=perps-adjust-margin-no-removable-margin, expected=absent, present=false, visible=false
- PASS ac4-reopen-keypad (ui.press, 1.6s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS ac4-wait-keypad-open (ui.wait_for, 1.2s): matched=true, testId=perps-adjust-margin-done-button, expected=visible, present=true, visible=true
- PASS ac4-drain-live-limit (command, 1.9s): exitCode=0, stdout="DRAINED removed=20.1 exchangeMaxLeft=1.01"

- FAIL ac4-assert-keypad-closed (ui.wait_for, 15s)
