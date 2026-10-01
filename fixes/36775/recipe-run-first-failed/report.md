# MetaMask Recipe Run

Status: fail
Duration: 190s
Nodes: 20/21 passed

## Side findings
- REVIEW 5 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 12s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 1.2s): source=start, stream=stdout
- PASS setup-session/network (assert_output, 709ms): source=start, stream=stdout
- PASS setup-session/account (switch, 1.2s): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 611ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 22s): ref=perps.venue-start-state, status=pass
- PASS setup-pin-screen-variant (metamask.feature_flags.set, 5.4s): proof=mobile-remote-feature-flags
- PASS setup-assert-position (metamask.perps.ensure_positions, 15s): matching=1
- PASS setup-add-home (ui.navigate, 22s): route=WalletView, page=home, proof=agentic-navigation
- PASS setup-add-nav (ui.navigate, 12s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-lite-mode (metamask.perps.ensure_mode, 3.1s): proof=visible-market-detail-root-and-active-mode-control
- PASS setup-add-wait-margin-card (ui.wait_for, 9.3s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS setup-add-press-margin-card (ui.press, 8.6s): ok=true, testId=position-card-margin, deviceName=mmdev-6
- PASS setup-press-add (ui.press, 5.2s): ok=true, testId=perps-adjust-margin-add-btn, deviceName=mmdev-6
- PASS setup-open-keypad (ui.press, 10s): ok=true, testId=perps-amount-display-touchable, deviceName=mmdev-6
- PASS setup-key-2 (ui.press, 14s): ok=true, testId=keypad-key-2, deviceName=mmdev-6
- PASS setup-key-0 (ui.press, 15s): ok=true, testId=keypad-key-0, deviceName=mmdev-6
- PASS setup-close-keypad (ui.press, 10s): ok=true, testId=perps-adjust-margin-done-button, deviceName=mmdev-6
- PASS setup-confirm-add (ui.press, 7.3s): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mmdev-6
- FAIL setup-assert-added (ui.wait_for, 22s)
