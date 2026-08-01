# MetaMask Recipe Run

Status: pass
Duration: 32s
Nodes: 10/10 passed

## Side findings
- REVIEW 183 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS start-collector (metamask.analytics.start_capture, 167ms): action=metamask.analytics.start_capture, cursor=1785571405772, port=9165, pid=19762, eventsFile=<metamask-mobile>/temp/recipe/runtime/analytics/events.jsonl
- PASS ensure-unlocked-before-consent (metamask.wallet.ensure_unlocked, 1.2s): proof=agentic-wallet-status
- PASS set-consent (metamask.analytics.set_consent, 1.6s): proof=mobile-settings-consent
- PASS home-before-proof (ui.navigate, 1.4s): route=WalletView, page=home, proof=agentic-navigation
- PASS drain-setup-events (wait, 22s): durationMs=22000
- PASS capture (metamask.analytics.start_capture, 167ms): action=metamask.analytics.start_capture, cursor=1785571432616, port=9165, pid=19762, eventsFile=<metamask-mobile>/temp/recipe/runtime/analytics/events.jsonl
- PASS open-perps (ui.navigate, 1.3s): route=PerpsMarketListView, page=perps, proof=agentic-navigation
- PASS wait-for-market-list (ui.wait_for, 540ms): matched=true, testId=perps-market-list, expected=visible, present=true
- PASS assert-events (metamask.analytics.assert_events, 3.1s): action=metamask.analytics.assert_events, since=1785571432616, exact=false, observed=4 items, capturedCount=3
- PASS done (end, 0ms)
