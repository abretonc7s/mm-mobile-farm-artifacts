# MetaMask Recipe Run

Status: pass
Duration: 23s
Nodes: 13/13 passed

## Side findings
- REVIEW 11 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS prepare-perps (metamask.perps.start_state, 16s): proof=metamask-perps-start-state
- PASS wait-panel-tabs (ui.wait_for, 540ms): matched=true, testId=perps-pro-market-positions-panel-tabs, expected=present, present=true, visible=true
- PASS wait-twap-tab (ui.wait_for, 488ms): matched=true, testId=perps-pro-market-positions-panel-tab-twap, expected=present, present=true, visible=true
- PASS open-twap-tab (ui.press, 470ms): ok=true, testId=perps-pro-market-positions-panel-tab-twap, deviceName=mm-3
- PASS wait-view-active (ui.wait_for, 510ms): matched=true, testId=perps-pro-market-twap-view-tab-active, expected=present, present=true, visible=true
- PASS wait-view-history (ui.wait_for, 489ms): matched=true, testId=perps-pro-market-twap-view-tab-history, expected=present, present=true, visible=true
- PASS wait-view-fill-history (ui.wait_for, 479ms): matched=true, testId=perps-pro-market-twap-view-tab-fill-history, expected=present, present=true, visible=true
- PASS wait-side-filter (ui.wait_for, 479ms): matched=true, testId=perps-pro-market-positions-side-filter-button, expected=present, present=true, visible=true
- PASS wait-ticker-only (ui.wait_for, 501ms): matched=true, testId=perps-pro-market-positions-ticker-only, expected=present, present=true, visible=true
- PASS capture-twap-tab (ui.screenshot, 377ms): path=screenshots/evidence-twap-tab.png
- PASS entry-done (end, 0ms)
- PASS restore-perps (metamask.perps.teardown_state, 2.6s): proof=metamask-perps-teardown-state
- PASS teardown-done (end, 0ms)
