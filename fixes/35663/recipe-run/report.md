# MetaMask Recipe Run

Status: pass
Duration: 93s
Nodes: 26/26 passed

## Side findings
- REVIEW 4 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS ensure-unlocked (metamask.wallet.ensure_unlocked, 7.0s): platform=ios, proof=agentic-wallet-unlock
- PASS open-market (ui.navigate, 7.5s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS wait-scale-fields (ui.wait_for, 2.8s): matched=true, testId=perps-pro-order-form-scale-start-price, expected=present, present=true, visible=true
- PASS go-long (ui.press, 714ms): ok=true, testId=perps-pro-order-form-direction-long, deviceName=mm-4
- PASS set-orders (ui.set_input, 652ms): ok=true, testId=perps-pro-order-form-scale-total-orders, value=2, deviceName=mm-4
- PASS set-size (ui.set_input, 675ms): ok=true, testId=perps-pro-order-form-size-input, value=35, deviceName=mm-4
- PASS safe-start (ui.set_input, 720ms): ok=true, testId=perps-pro-order-form-scale-start-price, value=76000, deviceName=mm-4
- PASS safe-end (ui.set_input, 754ms): ok=true, testId=perps-pro-order-form-scale-end-price, value=76500, deviceName=mm-4
- PASS expect-quiet (ui.wait_for, 758ms): matched=true, testId=perps-pro-order-form-price-card-message, expected=absent, present=false, visible=false
- PASS partial-end (ui.set_input, 722ms): ok=true, testId=perps-pro-order-form-scale-end-price, value=79000, deviceName=mm-4
- PASS expect-partial-above (ui.wait_for, 701ms): matched=true, text=Part of your price range is above current price, textMatch=contains, expected=present, present=true
- PASS evidence-partial-scroll (ui.scroll, 1.2s): animated=false, offset=180, ok=true, testId=perps-pro-order-form-scale-start-price, deviceName=mm-4
- PASS evidence-partial-shot (ui.capture_surface, 25s): path=screenshots/evidence-partial-shot.png
- PASS full-start (ui.set_input, 764ms): ok=true, testId=perps-pro-order-form-scale-start-price, value=78000, deviceName=mm-4
- PASS expect-full-above (ui.wait_for, 896ms): matched=true, text=Your price range is above current price, textMatch=contains, expected=present, present=true
- PASS evidence-full-above-scroll (ui.scroll, 1.3s): animated=false, offset=180, ok=true, testId=perps-pro-order-form-scale-start-price, deviceName=mm-4
- PASS evidence-full-above-shot (ui.capture_surface, 18s): path=screenshots/evidence-full-above-shot.png
- PASS flip-short (ui.press, 709ms): ok=true, testId=perps-pro-order-form-direction-short, deviceName=mm-4
- PASS expect-cleared-on-flip (ui.wait_for, 686ms): matched=true, testId=perps-pro-order-form-price-card-message, expected=absent, present=false, visible=false
- PASS short-start (ui.set_input, 690ms): ok=true, testId=perps-pro-order-form-scale-start-price, value=75000, deviceName=mm-4
- PASS short-end (ui.set_input, 662ms): ok=true, testId=perps-pro-order-form-scale-end-price, value=76000, deviceName=mm-4
- PASS expect-full-below (ui.wait_for, 713ms): matched=true, text=Your price range is below current price, textMatch=contains, expected=present, present=true
- PASS evidence-full-below-scroll (ui.scroll, 723ms): ok=true, testId=perps-pro-order-form-scale-start-price, intoView=true, alreadyVisible=true
- PASS evidence-full-below-shot (ui.capture_surface, 18s): path=screenshots/evidence-full-below-shot.png
- PASS expect-still-placeable (ui.wait_for, 792ms): matched=true, testId=perps-pro-order-form-place-order, expected=present, present=true, visible=true
- PASS done (end, 0ms)
