# MetaMask Recipe Run

Status: pass
Duration: 24s
Nodes: 17/17 passed

## Side findings
- REVIEW 6 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 6.9s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 66ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 177ms): source=start, stream=stdout
- PASS setup-session/account (switch, 127ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 66ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 7.8s): ref=perps.venue-start-state, status=pass
- PASS setup-pin-screen-variant (metamask.feature_flags.set, 769ms): proof=mobile-remote-feature-flags
- PASS setup-assert-position (metamask.perps.ensure_positions, 882ms): matching=1
- PASS setup-add-home (ui.navigate, 2.4s): route=WalletView, page=home, proof=agentic-navigation
- PASS setup-add-nav (ui.navigate, 5.8s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-lite-mode (metamask.perps.ensure_mode, 645ms): proof=visible-market-detail-root-and-active-mode-control
- PASS setup-add-wait-margin-card (ui.wait_for, 1.1s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS setup-add-press-margin-card (ui.press, 1.5s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS locators (ui.locators, 734ms): count=12
- PASS shot (ui.screenshot, 1.3s): path=screenshots/shot.png
- PASS done (end, 0ms)
