# MetaMask Recipe Run

Status: fail
Duration: 26s
Nodes: 3/4 passed

## Side findings
- REVIEW 6 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS wallet (metamask.wallet.read_state, 292ms): platform=ios, proof=agentic-wallet-status
- PASS account (assert_output, 78ms): source=wallet, stream=stdout
- PASS unlock (metamask.wallet.ensure_unlocked, 14s): platform=ios, proof=agentic-wallet-unlock
- FAIL environment (command, 11s)
