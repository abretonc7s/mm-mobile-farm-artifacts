# MetaMask Recipe Run

Status: fail
Duration: 76s
Nodes: 32/33 passed

## Side findings
- REVIEW 4 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-flag (metamask.feature_flags.set, 427ms): proof=mobile-remote-feature-flags
- PASS setup-pro (metamask.perps.start_state, 2.1s): proof=metamask-perps-start-state
- PASS setup-no-btc-position (metamask.perps.ensure_positions, 641ms): matching=0
- PASS setup-no-btc-orders (metamask.perps.ensure_orders, 663ms): matching=0
- PASS setup-show-margin-control (ui.scroll, 3.3s): ok=true, testId=perps-pro-order-form-margin-mode, intoView=true, alreadyVisible=true
- PASS setup-open-order-type (ui.press, 828ms): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-2
- PASS setup-basic-tab (ui.press, 632ms): ok=true, testId=perps-order-type-tab-basic, deviceName=mm-2
- PASS setup-wait-market-type (ui.wait_for, 630ms): matched=true, testId=perps-order-type-market, expected=visible, present=true, visible=true
- PASS setup-pick-market-type (ui.press, 782ms): ok=true, testId=perps-order-type-market, deviceName=mm-2
- PASS gate-margin-button (ui.wait_for, 700ms): matched=true, testId=perps-pro-order-form-margin-mode, expected=visible, present=true, visible=true
- PASS ac1-open-sheet (ui.press, 783ms): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-2
- PASS ac1-wait-cross-option (ui.wait_for, 754ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-press-cross (ui.press, 652ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-2
- PASS ac1-wait-sheet-closed (ui.wait_for, 666ms): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac1-show-margin-control (ui.swipe, 15s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac1-wait-cross-label (ui.wait_for, 878ms): matched=true, testId=perps-pro-order-form-margin-mode, text=Cross, textMatch=exact, expected=visible
- PASS ac1-screenshot-cross-label (ui.screenshot, 1.3s): path=screenshots/evidence-ac1-cross-label.png
- PASS ac1-reopen-sheet (ui.press, 676ms): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-2
- PASS ac1-wait-cross-selected (ui.wait_for, 624ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-screenshot-cross-sheet (ui.screenshot, 719ms): path=screenshots/evidence-ac1-cross-sheet.png
- PASS ac2-keep-cross (ui.press, 725ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-2
- PASS ac2-wait-sheet-closed (ui.wait_for, 938ms): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac2-scroll-size (ui.scroll, 865ms): ok=true, testId=perps-pro-order-form-size-card, intoView=true, alreadyVisible=true
- PASS ac2-wait-size (ui.wait_for, 866ms): matched=true, testId=perps-pro-order-form-size-card, expected=visible, present=true, visible=true
- PASS ac2-set-size (ui.set_input, 842ms): ok=true, testId=perps-pro-order-form-size-input, value=15, deviceName=mm-2
- PASS ac2-scroll-submit (ui.scroll, 1.4s): animated=false, offset=600, ok=true, testId=perps-pro-order-form-summary-fees, deviceName=mm-2
- PASS ac2-wait-submit (ui.wait_for, 804ms): matched=true, testId=perps-pro-order-form-place-order, expected=visible, present=true, visible=true
- PASS ac2-press-submit (ui.press, 942ms): ok=true, testId=perps-pro-order-form-place-order, deviceName=mm-2
- PASS ac2-assert-position-open (metamask.perps.assert_positions, 4.3s): matching=1
- PASS ac2-filter-btc (ui.press, 1.0s): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-2
- PASS ac2-swipe-to-positions (ui.swipe, 4.7s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-swipe-to-card (ui.swipe, 4.6s): action=ui.swipe, backend=idb-ui, segments=1
- FAIL ac2-wait-cross-tag (ui.wait_for, 20s)
