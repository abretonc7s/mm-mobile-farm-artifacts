# MetaMask Recipe Run

Status: pass
Duration: 31s
Nodes: 18/18 passed

## Side findings
- REVIEW 16 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-status (app.status, 44ms): platform=mobile
- PASS setup-unlock (metamask.wallet.ensure_unlocked, 6.7s): platform=ios, proof=agentic-wallet-unlock
- PASS setup-perps-home (ui.navigate, 2.7s): route=PerpsMarketListView, page=perps, proof=agentic-navigation
- PASS setup-wait-home (ui.wait_for, 1.8s): matched=true, testId=perps-market-row-item-BTC, expected=visible, present=true, visible=true
- PASS setup-open-market (ui.press, 3.7s): ok=true, testId=perps-market-row-item-BTC, deviceName=mm-2
- PASS setup-ensure-lite (metamask.perps.ensure_mode, 368ms): proof=visible-market-detail-root-and-active-mode-control
- PASS ac2-wait-lite-start (ui.wait_for, 843ms): matched=true, testId=perps-mode-toggle-lite, expected=visible, present=true, visible=true
- PASS ac2-switch-to-pro (metamask.perps.ensure_mode, 3.7s): proof=visible-market-detail-root-and-active-mode-control
- PASS ac2-wait-pro (ui.wait_for, 866ms): matched=true, testId=perps-pro-order-form-place-order, expected=visible, present=true, visible=true
- PASS ac2-screenshot-pro (ui.screenshot, 703ms): path=screenshots/evidence-ac2-pro-workstation.png
- PASS ac2-switch-back-lite (metamask.perps.ensure_mode, 2.3s): proof=visible-market-detail-root-and-active-mode-control
- PASS ac2-wait-lite-return (ui.wait_for, 801ms): matched=true, testId=perps-market-details-long-button, expected=visible, present=true, visible=true
- PASS ac2-screenshot-lite-return (ui.screenshot, 716ms): path=screenshots/evidence-ac2-lite-return.png
- PASS ac1-press-back (ui.press, 2.1s): ok=true, testId=perps-market-header-back-button, deviceName=mm-2
- PASS ac1-wait-perps-home (ui.wait_for, 1.1s): matched=true, testId=perps-watchlist-header, expected=visible, present=true, visible=true
- PASS ac1-assert-not-wallet (ui.wait_for, 795ms): matched=true, testId=perps-market-add-funds-button, expected=visible, present=true, visible=true
- PASS ac1-screenshot-landing (ui.screenshot, 611ms): path=screenshots/evidence-ac1-back-lands-on-perps-home.png
- PASS done (end, 0ms)
