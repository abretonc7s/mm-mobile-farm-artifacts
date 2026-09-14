# MetaMask Recipe Run

Status: fail
Duration: 36s
Nodes: 4/5 passed

## Side findings
- REVIEW 1 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS status (app.status, 130ms): platform=mobile
- PASS cdp (cdp.target, 191ms): platform=mobile
- PASS ensure-unlocked (metamask.wallet.ensure_unlocked, 1.5s): platform=ios, proof=agentic-wallet-status
- PASS open-market (ui.navigate, 3.7s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- FAIL await-order-form (ui.wait_for, 30s)
