# MetaMask Recipe Run

Status: pass
Duration: 63s
Nodes: 37/37 passed

## Side findings
- REVIEW 3 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS status (app.status, 54ms): platform=mobile
- PASS cdp (cdp.target, 107ms): platform=mobile
- PASS ensure-unlocked (metamask.wallet.ensure_unlocked, 1.2s): platform=ios, proof=agentic-wallet-status
- PASS open-market (ui.navigate, 1.6s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS await-order-form (ui.wait_for, 1.4s): matched=true, testId=perps-pro-order-form-order-type, expected=visible, present=true, visible=true
- PASS open-order-type-sheet-twap (ui.press, 943ms): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-2
- PASS advanced-tab-twap (ui.press, 1.0s): ok=true, testId=perps-order-type-tab-advanced, deviceName=mm-2
- PASS assert-twap-option-copy (ui.wait_for, 948ms): matched=true, text=Split orders to execute at regular time interval, textMatch=contains, expected=visible, present=true
- PASS assert-scale-option-copy (ui.wait_for, 986ms): matched=true, text=Multiple limit orders spread across a price range, textMatch=contains, expected=visible, present=true
- PASS assert-chase-option-copy (ui.wait_for, 1.0s): matched=true, text=Auto adjust limit order to the best price, textMatch=contains, expected=visible, present=true
- PASS capture-order-type-sheet (ui.screenshot, 1.3s): path=screenshots/evidence-order-type-advanced.png
- PASS select-twap (ui.press, 2.8s): ok=true, testId=perps-order-type-twap, deviceName=mm-2
- PASS assert-twap-runtime-label (ui.wait_for, 1.9s): matched=true, testId=perps-pro-order-form-twap-duration-label, expected=visible, present=true, visible=true
- PASS assert-twap-runtime-info (ui.wait_for, 2.0s): matched=true, testId=perps-pro-order-form-twap-duration-info, expected=visible, present=true, visible=true
- PASS assert-twap-randomize (ui.wait_for, 1.9s): matched=true, testId=perps-pro-order-form-twap-randomize, expected=visible, present=true, visible=true
- PASS set-twap-size (ui.set_input, 2.2s): ok=true, testId=perps-pro-order-form-size-input, value=50, deviceName=mm-2
- PASS assert-twap-summary-runtime (ui.wait_for, 3.5s): matched=true, testId=perps-pro-order-form-summary-twap-runtime, expected=present, present=true, visible=true
- PASS assert-twap-summary-size-per-suborder (ui.wait_for, 2.4s): matched=true, testId=perps-pro-order-form-summary-twap-size-per-suborder, expected=present, present=true, visible=true
- PASS assert-twap-summary-hides-liquidation (ui.wait_for, 1.8s): matched=true, testId=perps-pro-order-form-summary-liquidation, expected=not_present, present=false, visible=false
- PASS assert-twap-summary-hides-slippage (ui.wait_for, 2.3s): matched=true, testId=perps-pro-order-form-summary-slippage, expected=not_present, present=false, visible=false
- PASS capture-twap (ui.screenshot, 1.8s): path=screenshots/evidence-twap-form.png
- PASS scroll-twap-summary (ui.scroll, 1.9s): ok=true, testId=perps-pro-order-form-summary-twap-runtime, intoView=true, alreadyVisible=true
- PASS capture-twap-summary (ui.screenshot, 1.9s): path=screenshots/evidence-twap-summary.png
- PASS open-order-type-sheet-scale (ui.press, 1.3s): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-2
- PASS advanced-tab-scale (ui.press, 1.1s): ok=true, testId=perps-order-type-tab-advanced, deviceName=mm-2
- PASS select-scale (ui.press, 1.7s): ok=true, testId=perps-order-type-scale, deviceName=mm-2
- PASS assert-scale-start (ui.wait_for, 2.2s): matched=true, text=Start (USD), textMatch=contains, expected=visible, present=true
- PASS assert-scale-end (ui.wait_for, 3.3s): matched=true, text=End (USD), textMatch=contains, expected=visible, present=true
- PASS assert-scale-order-count (ui.wait_for, 1.9s): matched=true, text=Order count, textMatch=contains, expected=visible, present=true
- PASS assert-scale-size-skew (ui.wait_for, 1.5s): matched=true, text=Size skew, textMatch=contains, expected=present, present=true
- PASS capture-scale (ui.screenshot, 1.5s): path=screenshots/evidence-scale-form.png
- PASS open-order-type-sheet-chase (ui.press, 1.2s): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-2
- PASS advanced-tab-chase (ui.press, 1.1s): ok=true, testId=perps-order-type-tab-advanced, deviceName=mm-2
- PASS select-chase (ui.press, 2.0s): ok=true, testId=perps-order-type-chase, deviceName=mm-2
- PASS assert-chase-max-distance (ui.wait_for, 1.7s): matched=true, text=Max distance (USD), textMatch=contains, expected=visible, present=true
- PASS capture-chase (ui.screenshot, 1.7s): path=screenshots/evidence-chase-form.png
- PASS done (end, 0ms)
