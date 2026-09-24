# MetaMask Recipe Run

Status: fail
Duration: 28s
Nodes: 13/14 passed

## Side findings
- REVIEW 14 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 15s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 31ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 32ms): source=start, stream=stdout
- PASS setup-session/account (switch, 35ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 40ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 15s): ref=perps.venue-start-state, status=pass
- PASS setup-assert-position (metamask.perps.ensure_positions, 6.1s): matching=1
- PASS setup-add-home (ui.navigate, 1.2s): route=WalletView, page=home, proof=agentic-navigation
- PASS setup-add-nav (ui.navigate, 2.0s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-lite-mode (metamask.perps.ensure_mode, 374ms): proof=visible-market-detail-root-and-active-mode-control
- PASS setup-add-wait-margin-card (ui.wait_for, 1.0s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS setup-add-press-margin-card (ui.press, 1.1s): ok=true, testId=position-card-margin, deviceName=mm-6
- FAIL setup-press-add (ui.press, 743ms)
