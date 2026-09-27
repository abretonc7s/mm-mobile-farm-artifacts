# MetaMask Recipe Run

Status: fail
Duration: 32s
Nodes: 12/13 passed

## Side findings
- REVIEW 16 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-flag (metamask.feature_flags.set, 354ms): proof=mobile-remote-feature-flags
- PASS setup-pro (metamask.perps.start_state, 13s): proof=metamask-perps-start-state
- PASS setup-no-btc-position (metamask.perps.ensure_positions, 894ms): matching=0
- PASS setup-no-btc-orders (metamask.perps.ensure_orders, 1.1s): matching=0
- PASS setup-show-margin-control (ui.scroll, 4.4s): ok=true, testId=perps-pro-order-form-margin-mode, intoView=true, alreadyVisible=true
- PASS setup-open-order-type (ui.press, 919ms): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-2
- PASS setup-basic-tab (ui.press, 1.0s): ok=true, testId=perps-order-type-tab-basic, deviceName=mm-2
- PASS setup-wait-market-type (ui.wait_for, 957ms): matched=true, testId=perps-order-type-market, expected=visible, present=true, visible=true
- PASS setup-pick-market-type (ui.press, 1.3s): ok=true, testId=perps-order-type-market, deviceName=mm-2
- PASS gate-margin-button (ui.wait_for, 3.9s): matched=true, testId=perps-pro-order-form-margin-mode, expected=visible, present=true, visible=true
- PASS ac1-open-sheet (ui.press, 1.0s): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-2
- PASS ac1-wait-cross-option (ui.wait_for, 911ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- FAIL ac1-press-cross (ui.press, 1.1s)
