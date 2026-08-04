# MetaMask Recipe Run

Status: pass
Duration: 35s
Nodes: 22/22 passed

## Side findings
- REVIEW 8 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-unlock (metamask.wallet.ensure_unlocked, 1.2s): proof=agentic-wallet-status
- PASS setup-limit-order (metamask.perps.ensure_orders, 7.9s): matching=1
- PASS setup-navigate-market (ui.navigate, 1.9s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS gate-pro-view (ui.wait_for, 1.0s): matched=true, testId=perps-pro-market-view, expected=present, present=true
- PASS ac1-assert-size-label (ui.wait_for, 1.0s): matched=true, testId=perps-pro-order-form-size-input, expected=present, present=true, text=Size (USD)
- PASS ac1-screenshot-size-label (ui.screenshot, 1.1s): path=screenshots/evidence-ac1-size-usd-label.png
- PASS ac3-scroll-to-positions (ui.scroll, 840ms): animated=false, offset=650, ok=true, testId=perps-pro-market-scroll-view, deviceName=mmdev-1
- PASS ac3-open-positions-tab (ui.press, 996ms): ok=true, testId=perps-pro-market-positions-panel-tab-positions, deviceName=mmdev-1
- PASS ac3-open-side-filter (ui.press, 500ms): ok=true, testId=perps-pro-market-positions-side-filter-button, deviceName=mmdev-1
- PASS ac3-assert-all-sides (ui.wait_for, 540ms): matched=true, testId=perps-pro-market-positions-side-filter-sheet-option-all, expected=present, present=true, text=All sides
- PASS ac3-screenshot-side-filter (ui.screenshot, 615ms): path=screenshots/evidence-ac3-all-sides-filter.png
- PASS ac3-close-side-filter (ui.press, 919ms): ok=true, testId=perps-pro-market-positions-side-filter-sheet-apply, deviceName=mmdev-1
- PASS ac2-open-orders-tab (ui.press, 904ms): ok=true, testId=perps-pro-market-positions-panel-tab-orders, deviceName=mmdev-1
- PASS ac2-assert-orders-list (ui.wait_for, 906ms): matched=true, testId=perps-pro-market-orders-list, expected=present, present=true
- PASS ac2-assert-limit-order-open (metamask.perps.assert_orders, 441ms): matching=1
- PASS ac2-screenshot-limit-pill (ui.screenshot, 1.0s): path=screenshots/evidence-ac2-order-pill-limit.png
- PASS ac2-scroll-to-stop-order (ui.scroll, 1.1s): animated=false, offset=1250, ok=true, testId=perps-pro-market-scroll-view, deviceName=mmdev-1
- PASS ac2-screenshot-stop-market-pill (ui.screenshot, 1.0s): path=screenshots/evidence-ac2-order-pill-stop-market.png
- PASS ac2-run-pill-label-tests (command, 4.2s): exitCode=0, stderr=PASS app/components/UI/Perps/utils/orderUtils.test.ts
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProPositionsSideFilterSheet.test.tsx
PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderCard.test.tsx

Test Suites: 3 passed, 3 total
Tests:       107 passed, 107 total
Snapshots:   0 total
Time:        2.076 s, estimated 3 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/orderUtils.test.ts|app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderCard.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProPositionsSideFilterSheet.test.tsx/i.

- PASS ac2-assert-pill-label-tests-pass (assert_exit_code, 81ms): source=ac2-run-pill-label-tests, expected=0, actual=0
- PASS teardown-close-limit-order (metamask.perps.close_orders, 4.6s): matching=0
- PASS teardown-done (end, 0ms)
