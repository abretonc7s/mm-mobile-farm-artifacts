# MetaMask Recipe Run

Status: pass
Duration: 60s
Nodes: 41/41 passed

## Side findings
- REVIEW 3 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS wallet (metamask.wallet.read_state, 308ms): platform=ios, proof=agentic-wallet-status
- PASS account (assert_output, 96ms): source=wallet, stream=stdout
- PASS unlock (metamask.wallet.ensure_unlocked, 1.3s): platform=ios, proof=agentic-wallet-status
- PASS environment (command, 1.0s): exitCode=0, stdout={"identity":{"address":"0x8dc623e964475d4d669da601fd15ea9125469003","provider":"hyperliquid","isTestnet":true},"positions":[{"symbol":"ETH","size":"0.0051","entryPrice":"2394.1","positionValue":"12.22113","unrealizedPnl":"0.01122","marginUsed":"12.22113","leverage":{"type":"cross","value":1},"liquidationPrice":null,"maxLeverage":25,"returnOnEquity":"0.0009189257","cumulativeFunding":{"allTime":"0.948271","sinceOpen":"0.0","sinceChange":"0.0"},"takeProfitCount":0,"stopLossCount":0,"takeProfitOrders":[],"stopLossOrders":[]}],"venuePositions":[{"type":"oneWay","position":{"coin":"ETH","szi":"0.0051","leverage":{"type":"cross","value":1},"entryPx":"2394.1","positionValue":"12.22674","unrealizedPnl":"0.01683","returnOnEquity":"0.0013783885","liquidationPx":null,"marginUsed":"12.22674","maxLeverage":25,"cumFunding":{"allTime":"0.948271","sinceOpen":"0.0","sinceChange":"0.0"}}}],"orders":[],"leverage":{"type":"cross","value":1}}
, stderr=(node:29288) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/deeeed/dev/metamask/metamask-mobile-1/temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-cross-setup.ts is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/deeeed/dev/metamask/metamask-mobile-1/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)

- PASS positions (command, 1.0s): exitCode=0, stdout={"identity":{"address":"0x8dc623e964475d4d669da601fd15ea9125469003","provider":"hyperliquid","isTestnet":true},"positions":[{"symbol":"ETH","size":"0.0051","entryPrice":"2394.1","positionValue":"12.22674","unrealizedPnl":"0.01683","marginUsed":"12.22674","leverage":{"type":"cross","value":1},"liquidationPrice":null,"maxLeverage":25,"returnOnEquity":"0.0013783885","cumulativeFunding":{"allTime":"0.948271","sinceOpen":"0.0","sinceChange":"0.0"},"takeProfitCount":0,"stopLossCount":0,"takeProfitOrders":[],"stopLossOrders":[]}],"venuePositions":[{"type":"oneWay","position":{"coin":"ETH","szi":"0.0051","leverage":{"type":"cross","value":1},"entryPx":"2394.1","positionValue":"12.22674","unrealizedPnl":"0.01683","returnOnEquity":"0.0013783885","liquidationPx":null,"marginUsed":"12.22674","maxLeverage":25,"cumFunding":{"allTime":"0.948271","sinceOpen":"0.0","sinceChange":"0.0"}}}],"orders":[],"leverage":{"type":"cross","value":1}}
, stderr=(node:29487) [MODULE_TYPELESS_PACKAGE_JSON] Warning: Module type of file:///Users/deeeed/dev/metamask/metamask-mobile-1/temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-cross-setup.ts is not specified and it doesn't parse as CommonJS.
Reparsing as ES module because module syntax was detected. This incurs a performance overhead.
To eliminate this warning, add "type": "module" to /Users/deeeed/dev/metamask/metamask-mobile-1/package.json.
(Use `node --trace-warnings ...` to show where the warning was created)

- PASS require-cross (assert_json, 151ms): path=temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-live-positions.json
- PASS require-cross-mode (assert_json, 105ms): path=temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-live-positions.json
- PASS require-cross-market (assert_json, 45ms): path=temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-live-positions.json
- PASS price-kind (switch, 51ms): matched=true, value=null, expected=null
- PASS require-null-price (assert_json, 65ms): path=temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-live-positions.json
- PASS require-null-falsy (assert_json, 40ms): path=temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-live-positions.json
- PASS require-null-not-string (assert_json, 89ms): path=temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-live-positions.json
- PASS require-null-not-zero (assert_json, 43ms): path=temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-live-positions.json
- PASS require-null-not-false (assert_json, 49ms): path=temp/tasks/feat/tat-3519-0908-104128/artifacts/selected-account-live-positions.json
- PASS pro-open (ui.navigate, 9.3s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation+visible-native-navigation
- PASS pro-scroll (ui.scroll, 2.7s): animated=false, offset=600, ok=true, testId=cross-margin-tag-pro-ETH, deviceName=mmdev-1
- PASS pro-tag (ui.wait_for, 2.1s): matched=true, testId=cross-margin-tag-pro-ETH, expected=visible, present=true, visible=true
- PASS pro-margin (ui.wait_for, 1.4s): matched=true, text=Position margin used, textMatch=contains, expected=visible, present=true
- PASS pro-no-edit (ui.wait_for, 1.2s): matched=true, testId=perps-pro-market-position-edit-margin, expected=absent, present=false, visible=false
- PASS pro-summary-capture (ui.screenshot, 1.9s): path=screenshots/cross-summary-pro.png
- PASS pro-scroll-price (ui.scroll, 1.1s): ok=true, testId=cross-liquidation-info-pro-ETH, intoView=true, alreadyVisible=true
- PASS pro-price (ui.wait_for, 1.3s): matched=true, testId=perps-pro-market-position-liq-price, text=No liquidation price, textMatch=contains, expected=visible
- PASS pro-position-capture (ui.screenshot, 1.8s): path=screenshots/cross-position-pro.png
- PASS pro-info (ui.press, 769ms): ok=true, testId=cross-liquidation-info-pro-ETH, deviceName=mmdev-1
- PASS pro-explanation (ui.wait_for, 2.4s): matched=true, testId=perps-bottom-sheet-tooltip-content, text=At the current account value, this position has no liquidation price. This can change as the value of your other cross positions changes. A liquidation can affect your entire cross balance., textMatch=exact, expected=visible
- PASS pro-capture (ui.screenshot, 907ms): path=screenshots/cross-explanation-pro.png
- PASS pro-dismiss (ui.press, 948ms): ok=true, testId=perps-bottom-sheet-tooltip-got-it-button, deviceName=mmdev-1
- PASS lite-open (ui.navigate, 5.5s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation+visible-native-navigation
- PASS lite-scroll (ui.scroll, 1.3s): ok=true, testId=cross-margin-tag-lite-ETH, intoView=true, alreadyVisible=true
- PASS lite-tag (ui.wait_for, 2.7s): matched=true, testId=cross-margin-tag-lite-ETH, expected=visible, present=true, visible=true
- PASS lite-margin (ui.wait_for, 1.5s): matched=true, text=Position margin used, textMatch=contains, expected=visible, present=true
- PASS lite-no-edit (ui.wait_for, 2.1s): matched=true, testId=position-card-margin-chevron, expected=absent, present=false, visible=false
- PASS lite-summary-capture (ui.screenshot, 1.6s): path=screenshots/cross-summary-lite.png
- PASS lite-scroll-price (ui.scroll, 1.9s): animated=false, measuredOffset=1178, ok=true, testId=cross-liquidation-info-lite-ETH, deviceName=mmdev-1
- PASS lite-price (ui.wait_for, 1.6s): matched=true, testId=position-card-liquidation-price-value, text=No liquidation price, textMatch=exact, expected=visible
- PASS lite-position-capture (ui.screenshot, 1.9s): path=screenshots/cross-position-lite.png
- PASS lite-info (ui.press, 1.0s): ok=true, testId=cross-liquidation-info-lite-ETH, deviceName=mmdev-1
- PASS lite-explanation (ui.wait_for, 1.0s): matched=true, testId=perps-bottom-sheet-tooltip-content, text=At the current account value, this position has no liquidation price. This can change as the value of your other cross positions changes. A liquidation can affect your entire cross balance., textMatch=exact, expected=visible
- PASS lite-capture (ui.screenshot, 1.2s): path=screenshots/cross-explanation-lite.png
- PASS lite-dismiss (ui.press, 1.3s): ok=true, testId=perps-bottom-sheet-tooltip-got-it-button, deviceName=mmdev-1
- PASS done (end, 0ms)
