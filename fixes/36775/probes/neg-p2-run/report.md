# MetaMask Recipe Run

Status: fail
Duration: 71s
Nodes: 32/33 passed

## Side findings
- REVIEW 5 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 8.1s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 69ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 62ms): source=start, stream=stdout
- PASS setup-session/account (switch, 68ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 64ms): source=start, stream=stdout
- PASS setup-session/done (end, 6ms)
- PASS setup-session (call, 8.8s): ref=perps.venue-start-state, status=pass
- PASS setup-pin-screen-variant (metamask.feature_flags.set, 583ms): proof=mobile-remote-feature-flags
- PASS setup-assert-position (metamask.perps.ensure_positions, 1.1s): matching=1
- PASS setup-add-home (ui.navigate, 3.3s): route=WalletView, page=home, proof=agentic-navigation
- PASS setup-add-nav (ui.navigate, 6.0s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-lite-mode (metamask.perps.ensure_mode, 533ms): proof=visible-market-detail-root-and-active-mode-control
- PASS setup-add-wait-margin-card (ui.wait_for, 2.6s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS setup-add-press-margin-card (ui.press, 2.3s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS setup-press-add (ui.press, 2.9s): ok=true, testId=perps-adjust-margin-add-btn, deviceName=mm-6
- PASS setup-open-keypad (ui.press, 1.5s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS setup-key-2 (ui.press, 2.0s): ok=true, testId=keypad-key-2, deviceName=mm-6
- PASS setup-key-0 (ui.press, 1.6s): ok=true, testId=keypad-key-0, deviceName=mm-6
- PASS setup-close-keypad (ui.press, 1.0s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS setup-confirm-add (ui.press, 2.7s): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mm-6
- PASS setup-assert-added (ui.wait_for, 2.3s): matched=true, text=Added $20 margin, textMatch=contains, expected=visible, present=true
- PASS ac4-home (ui.navigate, 3.2s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac4-nav (ui.navigate, 6.4s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac4-wait-margin-card (ui.wait_for, 2.5s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac4-press-margin-card (ui.press, 2.0s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS ac4-press-remove (ui.press, 2.8s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mm-6
- PASS ac4-open-keypad (ui.press, 1.2s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS ac4-press-max (ui.press, 1.5s): ok=true, text=Max, deviceName=mm-6
- PASS ac4-close-keypad (ui.press, 2.3s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS ac4-assert-no-explanation (ui.wait_for, 1.3s): matched=true, testId=perps-adjust-margin-no-removable-margin, expected=absent, present=false, visible=false
- PASS ac4-drain-live-limit (command, 1.5s): exitCode=0, stdout="DRAINED removed=19.55 exchangeMaxLeft=1.00"

- PASS ac4-assert-explanation (ui.wait_for, 1.8s): matched=true, testId=perps-adjust-margin-no-removable-margin, expected=visible, present=true, visible=true
- FAIL ac4-assert-no-stale-error (ui.wait_for, 3.4s)
