# MetaMask Recipe Run

Status: fail
Duration: 16s
Nodes: 8/9 passed

## Steps
- PASS setup-session/start (metamask.perps.start_state, 3.5s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 106ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 128ms): source=start, stream=stdout
- PASS setup-session/account (switch, 180ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 118ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 4.7s): ref=perps.venue-start-state, status=pass
- PASS setup-pin-screen-variant (metamask.feature_flags.set, 555ms): proof=mobile-remote-feature-flags
- FAIL setup-assert-position (metamask.perps.ensure_positions, 10s)
