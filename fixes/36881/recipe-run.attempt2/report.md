# MetaMask Recipe Run

Status: fail
Duration: 70s
Nodes: 12/13 passed

## Side findings
- REVIEW 26 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-flag (metamask.feature_flags.set, 531ms): proof=mobile-remote-feature-flags
- PASS setup-pro (metamask.perps.start_state, 27s): proof=metamask-perps-start-state
- PASS setup-no-btc-position (metamask.perps.ensure_positions, 2.9s): matching=0
- PASS setup-no-btc-orders (metamask.perps.ensure_orders, 2.3s): matching=0
- PASS setup-show-margin-control (ui.scroll, 5.4s): ok=true, testId=perps-pro-order-form-margin-mode, intoView=true, alreadyVisible=true
- PASS setup-open-order-type (ui.press, 8.7s): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-6
- PASS setup-basic-tab (ui.press, 1.6s): ok=true, testId=perps-order-type-tab-basic, deviceName=mm-6
- PASS setup-wait-market-type (ui.wait_for, 2.0s): matched=true, testId=perps-order-type-market, expected=visible, present=true, visible=true
- PASS setup-pick-market-type (ui.press, 6.2s): ok=true, testId=perps-order-type-market, deviceName=mm-6
- PASS gate-margin-button (ui.wait_for, 4.5s): matched=true, testId=perps-pro-order-form-margin-mode, expected=visible, present=true, visible=true
- PASS ac1-open-sheet (ui.press, 1.6s): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-6
- PASS ac1-wait-cross-option (ui.wait_for, 3.3s): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- FAIL ac1-press-cross (ui.press, 2.2s)
