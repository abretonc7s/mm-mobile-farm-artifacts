## **Description**

Historical candlestick chart data (`candleSnapshot`) was being fetched through the WebSocket-backed `InfoClient`. On extension, rapid market navigation causes an abort race condition — the UI unmount message arrives too late to cancel in-flight WebSocket requests, leading to bursty candleSnapshot traffic and 429 rate limit errors from Hyperliquid.

This PR switches `fetchHistoricalCandles()` to use the HTTP `InfoClient` instead. Live candle streaming remains on WebSocket. This is the source-of-truth fix in the controller/client-service layer, so both mobile and extension benefit.

Transport split after this change:
- Initial chart history load → **HTTP**
- Load-more historical candles → **HTTP**
- Live candle updates → **WebSocket** (unchanged)

## **Changelog**

CHANGELOG entry: Fixed candlestick chart 429 rate limiting during rapid market navigation by routing historical candle fetches over HTTP

## **Related issues**

Fixes: https://consensyssoftware.atlassian.net/browse/TAT-2954

## **Manual testing steps**

```gherkin
Feature: Candlestick chart loads during rapid market switching

  Scenario: User rapidly switches between 5+ market detail pages
    Given the user is on the Perps trending markets list

    When user taps BTC, then back, then ETH, then back, then SOL, then back, then HYPE, then back, then BTC again, then back, then ETH again
    Then each market detail page loads successfully with chart visible
    And no candleSnapshot errors appear in Metro logs
```

## **Screenshots/Recordings**

### **Before**

N/A — existing behavior (no visible UI change, transport-level fix)

### **After**

https://github.com/user-attachments/assets/after.mp4

## **Validation Recipe**

<details><summary>recipe.json (27 nodes — rapid market switching validation)</summary>

```json
{
  "title": "Validate candlestick chart loads correctly during rapid market switching (TAT-2954)",
  "initial_conditions": { "testnet": false },
  "validate": {
    "workflow": {
      "pre_conditions": ["wallet.unlocked", "perps.feature_enabled"],
      "entry": "setup-nav-perps",
      "nodes": {
        "setup-nav-perps": {
          "action": "navigate",
          "target": "PerpsTrendingView",
          "next": "setup-wait-list"
        },
        "setup-wait-list": {
          "action": "wait_for",
          "test_id": "perps-market-row-item-BTC",
          "timeout": 10000,
          "next": "ac1-open-btc"
        },
        "ac1-open-btc": {
          "action": "press",
          "test_id": "perps-market-row-item-BTC",
          "next": "ac1-wait-detail-btc"
        },
        "ac1-wait-detail-btc": {
          "action": "wait_for",
          "test_id": "perps-market-details-view",
          "timeout": 8000,
          "next": "ac1-back-1"
        },
        "ac1-back-1": {
          "action": "press",
          "test_id": "perps-market-header-back-button",
          "next": "ac1-wait-list-1"
        },
        "ac1-wait-list-1": {
          "action": "wait_for",
          "test_id": "perps-market-row-item-ETH",
          "timeout": 5000,
          "next": "ac1-open-eth"
        },
        "ac1-open-eth": {
          "action": "press",
          "test_id": "perps-market-row-item-ETH",
          "next": "ac1-wait-detail-eth"
        },
        "ac1-wait-detail-eth": {
          "action": "wait_for",
          "test_id": "perps-market-details-view",
          "timeout": 8000,
          "next": "ac1-back-2"
        },
        "ac1-back-2": {
          "action": "press",
          "test_id": "perps-market-header-back-button",
          "next": "ac1-wait-list-2"
        },
        "ac1-wait-list-2": {
          "action": "wait_for",
          "test_id": "perps-market-row-item-SOL",
          "timeout": 5000,
          "next": "ac1-open-sol"
        },
        "ac1-open-sol": {
          "action": "press",
          "test_id": "perps-market-row-item-SOL",
          "next": "ac1-wait-detail-sol"
        },
        "ac1-wait-detail-sol": {
          "action": "wait_for",
          "test_id": "perps-market-details-view",
          "timeout": 8000,
          "next": "ac1-back-3"
        },
        "ac1-back-3": {
          "action": "press",
          "test_id": "perps-market-header-back-button",
          "next": "ac1-wait-list-3"
        },
        "ac1-wait-list-3": {
          "action": "wait_for",
          "test_id": "perps-market-row-item-HYPE",
          "timeout": 5000,
          "next": "ac1-open-hype"
        },
        "ac1-open-hype": {
          "action": "press",
          "test_id": "perps-market-row-item-HYPE",
          "next": "ac1-wait-detail-hype"
        },
        "ac1-wait-detail-hype": {
          "action": "wait_for",
          "test_id": "perps-market-details-view",
          "timeout": 8000,
          "next": "ac1-back-4"
        },
        "ac1-back-4": {
          "action": "press",
          "test_id": "perps-market-header-back-button",
          "next": "ac1-wait-list-4"
        },
        "ac1-wait-list-4": {
          "action": "wait_for",
          "test_id": "perps-market-row-item-BTC",
          "timeout": 5000,
          "next": "ac1-open-btc2"
        },
        "ac1-open-btc2": {
          "action": "press",
          "test_id": "perps-market-row-item-BTC",
          "next": "ac1-wait-detail-btc2"
        },
        "ac1-wait-detail-btc2": {
          "action": "wait_for",
          "test_id": "perps-market-details-view",
          "timeout": 8000,
          "next": "ac1-back-5"
        },
        "ac1-back-5": {
          "action": "press",
          "test_id": "perps-market-header-back-button",
          "next": "ac1-wait-list-5"
        },
        "ac1-wait-list-5": {
          "action": "wait_for",
          "test_id": "perps-market-row-item-ETH",
          "timeout": 5000,
          "next": "ac1-open-eth2"
        },
        "ac1-open-eth2": {
          "action": "press",
          "test_id": "perps-market-row-item-ETH",
          "next": "ac1-wait-detail-eth2"
        },
        "ac1-wait-detail-eth2": {
          "action": "wait_for",
          "test_id": "perps-market-details-view",
          "timeout": 8000,
          "next": "ac1-screenshot-final"
        },
        "ac1-screenshot-final": {
          "action": "screenshot",
          "filename": "evidence-rapid-switch-chart-loaded.png",
          "next": "ac1-back-6"
        },
        "ac1-back-6": {
          "action": "press",
          "test_id": "perps-market-header-back-button",
          "next": "ac2-check-no-rate-limit"
        },
        "ac2-check-no-rate-limit": {
          "action": "log_watch",
          "window_seconds": 45,
          "must_not_appear": ["candleSnapshot error", "historical_candles_api", "candle_subscription_async", "initial_candles_fetch"],
          "watch_for": ["candleSnapshot", "fetchHistoricalCandles", "historical_candles"],
          "next": "ac2-done"
        },
        "ac2-done": {
          "action": "end",
          "status": "pass"
        }
      }
    }
  }
}
```

</details>

## **Validation Logs**

Command:
```bash
bash scripts/perps/agentic/validate-recipe.sh .task/feat/tat-2954-0415-2218/artifacts/ --skip-manual
```

<details><summary>Full output (27/27 passed)</summary>

```
Running recipe: Validate candlestick chart loads correctly during rapid market switching (TAT-2954)
Pre-conditions: wallet.unlocked, perps.feature_enabled
Workflow nodes: 28

Pre-conditions: PASS

[setup-nav-perps] navigate to PerpsTrendingView — PASS
[setup-wait-list] wait for perps-market-row-item-BTC — PASS
[ac1-open-btc] press perps-market-row-item-BTC — PASS
[ac1-wait-detail-btc] wait for perps-market-details-view — PASS
[ac1-back-1] press perps-market-header-back-button — PASS
[ac1-wait-list-1] wait for perps-market-row-item-ETH — PASS
[ac1-open-eth] press perps-market-row-item-ETH — PASS
[ac1-wait-detail-eth] wait for perps-market-details-view — PASS
[ac1-back-2] press perps-market-header-back-button — PASS
[ac1-wait-list-2] wait for perps-market-row-item-SOL — PASS
[ac1-open-sol] press perps-market-row-item-SOL — PASS
[ac1-wait-detail-sol] wait for perps-market-details-view — PASS
[ac1-back-3] press perps-market-header-back-button — PASS
[ac1-wait-list-3] wait for perps-market-row-item-HYPE — PASS
[ac1-open-hype] press perps-market-row-item-HYPE — PASS
[ac1-wait-detail-hype] wait for perps-market-details-view — PASS
[ac1-back-4] press perps-market-header-back-button — PASS
[ac1-wait-list-4] wait for perps-market-row-item-BTC — PASS
[ac1-open-btc2] press perps-market-row-item-BTC — PASS
[ac1-wait-detail-btc2] wait for perps-market-details-view — PASS
[ac1-back-5] press perps-market-header-back-button — PASS
[ac1-wait-list-5] wait for perps-market-row-item-ETH — PASS
[ac1-open-eth2] press perps-market-row-item-ETH — PASS
[ac1-wait-detail-eth2] wait for perps-market-details-view — PASS
[ac1-screenshot-final] capture screenshot — PASS
[ac1-back-6] press perps-market-header-back-button — PASS
[ac2-check-no-rate-limit] scan metro log — PASS

Results: 27/27 passed
Recipe: PASS
```

</details>

## **Pre-merge author checklist**

- [x] I've followed [MetaMask Contributor Docs](https://github.com/MetaMask/contributor-docs) and [MetaMask Mobile Coding Standards](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/CODING_GUIDELINES.md).
- [x] I've completed the PR template to the best of my ability
- [x] I've included tests if applicable
- [x] I've documented my code using [JSDoc](https://jsdoc.app/) format if applicable
- [x] I've applied the right labels on the PR (see [labeling guidelines](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/LABELING_GUIDELINES.md)). Not required for external contributors.

## **Pre-merge reviewer checklist**

- [ ] I've manually tested the PR (e.g. pull and build branch, run the app, test code being changed).
- [ ] I confirm that this PR addresses all acceptance criteria described in the ticket it closes and includes the necessary testing evidence such as recordings and or screenshots.
