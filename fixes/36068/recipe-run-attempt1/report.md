# MetaMask Recipe Run

Status: fail
Duration: 163s
Nodes: 19/20 passed

## Side findings
- REVIEW 7 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS status (app.status, 103ms): platform=mobile
- PASS cdp (cdp.target, 120ms): platform=mobile
- PASS ensure-unlocked (metamask.wallet.ensure_unlocked, 8.8s): platform=ios, proof=agentic-wallet-unlock
- PASS open-market (ui.navigate, 26s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS await-order-form (ui.wait_for, 9.2s): matched=true, testId=perps-pro-order-form-order-type, expected=visible, present=true, visible=true
- PASS open-order-type-sheet-twap (ui.press, 5.0s): ok=true, testId=perps-pro-order-form-order-type, deviceName=mmdev-3
- PASS advanced-tab-twap (ui.press, 3.9s): ok=true, testId=perps-order-type-tab-advanced, deviceName=mmdev-3
- PASS assert-twap-option-copy (ui.wait_for, 3.8s): matched=true, text=Split orders to execute at regular time interval, textMatch=contains, expected=visible, present=true
- PASS assert-scale-option-copy (ui.wait_for, 3.1s): matched=true, text=Multiple limit orders spread across a price range, textMatch=contains, expected=visible, present=true
- PASS assert-chase-option-copy (ui.wait_for, 3.1s): matched=true, text=Auto adjust limit order to the best price, textMatch=contains, expected=visible, present=true
- PASS capture-order-type-sheet (ui.screenshot, 4.7s): path=screenshots/evidence-order-type-advanced.png
- PASS select-twap (ui.press, 7.4s): ok=true, testId=perps-order-type-twap, deviceName=mmdev-3
- PASS assert-twap-runtime-label (ui.wait_for, 5.7s): matched=true, testId=perps-pro-order-form-twap-duration-label, expected=visible, present=true, visible=true
- PASS assert-twap-runtime-info (ui.wait_for, 6.0s): matched=true, testId=perps-pro-order-form-twap-duration-info, expected=visible, present=true, visible=true
- PASS assert-twap-randomize (ui.wait_for, 6.6s): matched=true, testId=perps-pro-order-form-twap-randomize, expected=visible, present=true, visible=true
- PASS set-twap-size (ui.set_input, 15s): ok=true, testId=perps-pro-order-form-size-input, value=50, deviceName=mmdev-3
- PASS assert-twap-summary-runtime (ui.wait_for, 9.0s): matched=true, testId=perps-pro-order-form-summary-twap-runtime, expected=present, present=true, visible=true
- PASS assert-twap-summary-size-per-suborder (ui.wait_for, 14s): matched=true, testId=perps-pro-order-form-summary-twap-size-per-suborder, expected=present, present=true, visible=true
- PASS assert-twap-summary-hides-liquidation (ui.wait_for, 14s): matched=true, testId=perps-pro-order-form-summary-liquidation, expected=not_present, present=false, visible=false
- FAIL assert-twap-summary-hides-slippage (ui.wait_for, 10s)
