# MetaMask Recipe Run

Status: pass
Duration: 38s
Nodes: 6/6 passed

## Side findings
- REVIEW 8 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS start (metamask.perps.start_state, 31s): proof=metamask-perps-start-state
- PASS provider (assert_output, 533ms): source=start, stream=stdout
- PASS network (assert_output, 610ms): source=start, stream=stdout
- PASS account (switch, 672ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS account-name (assert_output, 986ms): source=start, stream=stdout
- PASS done (end, 0ms)
