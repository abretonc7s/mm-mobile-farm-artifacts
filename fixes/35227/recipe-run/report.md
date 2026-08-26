# MetaMask Recipe Run

Status: fail
Duration: 41s
Nodes: 1/4 passed

## Side findings
- REVIEW 3 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS ensure-session/probe-runtime (cdp.target, 49ms): platform=mobile
- FAIL ensure-session/ensure-wallet (metamask.wallet.ensure_unlocked, 30s)
- FAIL ensure-session (call, 31s)
- FAIL cleanup-orders (metamask.perps.ensure_orders, 10s)
