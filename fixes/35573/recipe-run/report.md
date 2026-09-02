# MetaMask Recipe Run

Status: pass
Duration: 46s
Nodes: 13/13 passed

## Side findings
- REVIEW 16 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-unlock (metamask.wallet.ensure_unlocked, 7.7s): platform=ios, proof=agentic-wallet-unlock
- PASS setup-account (metamask.wallet.select_account, 3.8s): proof=agentic-account-selection
- PASS setup-open-perps (ui.navigate, 14s): route=PerpsMarketListView, page=perps, proof=agentic-navigation
- PASS gate-wait-heading (ui.wait_for, 1.9s): matched=true, testId=perps-home-heading-provider-badge, expected=present, present=true, visible=true
- PASS gate-wait-deposit (ui.wait_for, 2.1s): matched=true, testId=perps-market-add-funds-button, expected=present, present=true, visible=true
- PASS ac1-press-deposit (ui.press, 5.7s): ok=true, testId=perps-market-add-funds-button, deviceName=mm-2
- PASS ac1-wait-confirmation (ui.wait_for, 1.9s): matched=true, testId=custom-amount-input, expected=present, present=true, visible=true
- PASS ac1-wait-pay-with (ui.wait_for, 1.6s): matched=true, testId=pay-with, expected=present, present=true, visible=true
- PASS ac1-screenshot-confirmation (ui.screenshot, 2.5s): path=screenshots/evidence-ac1-deposit-confirmation.png
- PASS ac2-press-pay-with (ui.press, 1.7s): ok=true, testId=pay-with, deviceName=mm-2
- PASS ac2-wait-token-sheet (ui.wait_for, 970ms): matched=true, testId=pay-with-crypto-section-preferred-token-row, expected=present, present=true, visible=true
- PASS ac2-screenshot-token-list (ui.screenshot, 835ms): path=screenshots/evidence-ac2-pay-with-list.png
- PASS done (end, 0ms)
