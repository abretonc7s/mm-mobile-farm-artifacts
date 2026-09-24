# MetaMask Recipe Run

Status: fail
Duration: 180s
Nodes: 30/31 passed

## Side findings
- REVIEW 8 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 16s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 191ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 824ms): source=start, stream=stdout
- PASS setup-session/account (switch, 317ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 317ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 19s): ref=perps.venue-start-state, status=pass
- PASS setup-assert-position (metamask.perps.ensure_positions, 1.8s): matching=1
- PASS setup-add-home (ui.navigate, 37s): route=WalletView, page=home, proof=agentic-navigation
- PASS setup-add-nav (ui.navigate, 6.3s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-lite-mode (metamask.perps.ensure_mode, 1.3s): proof=visible-market-detail-root-and-active-mode-control
- PASS setup-add-wait-margin-card (ui.wait_for, 3.5s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS setup-add-press-margin-card (ui.press, 3.8s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS setup-press-add (ui.press, 2.5s): ok=true, testId=perps-adjust-margin-add-btn, deviceName=mm-6
- PASS setup-open-keypad (ui.press, 2.9s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS setup-key-2 (ui.press, 3.1s): ok=true, testId=keypad-key-2, deviceName=mm-6
- PASS setup-key-0 (ui.press, 3.6s): ok=true, testId=keypad-key-0, deviceName=mm-6
- PASS setup-close-keypad (ui.press, 4.5s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS setup-confirm-add (ui.press, 3.3s): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mm-6
- PASS setup-assert-added (ui.wait_for, 3.2s): matched=true, text=Added $20 margin, textMatch=contains, expected=visible, present=true
- PASS ac1-home (ui.navigate, 6.3s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac1-nav (ui.navigate, 32s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac1-wait-margin-card (ui.wait_for, 3.2s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac1-press-margin-card (ui.press, 2.8s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS ac1-press-remove (ui.press, 2.9s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mm-6
- PASS ac1-open-keypad (ui.press, 2.5s): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS ac1-press-max (ui.press, 2.8s): ok=true, text=Max, deviceName=mm-6
- PASS ac1-close-keypad (ui.press, 2.0s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS ac1-wait-available (ui.wait_for, 2.1s): matched=true, testId=perps-adjust-margin-available-value, expected=visible, present=true, visible=true
- PASS ac1-screenshot-max-form (ui.screenshot, 4.0s): path=screenshots/evidence-ac1-max-form.png
- FAIL ac1-press-confirm (ui.press, 10s)
