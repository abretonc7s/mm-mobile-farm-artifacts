## **Description**

Bumps `@nktkas/hyperliquid` from `0.30.2` to `0.32.2` (latest). No breaking changes were found affecting the codebase — all existing type imports and runtime behavior remain compatible. Sub-dependencies updated: `@nktkas/rews` 1.2.3 → 2.1.0, `valibot` 1.2.0 → 1.3.1. The CLI binary and `micro-eth-signer` dependency were removed from the SDK in this release.

## **Changelog**

CHANGELOG entry: null

## **Related issues**

Fixes: https://consensyssoftware.atlassian.net/browse/TAT-2906

## **Manual testing steps**

```gherkin
Feature: Hyperliquid SDK update

  Scenario: user opens the perps market list
    Given the wallet is unlocked and perps feature is enabled

    When user navigates to the PerpsTrendingView
    Then market data loads successfully (229+ markets including BTC)
    And prices are displayed correctly
```

## **Screenshots/Recordings**

### **Before**

No UI changes — dependency update only.

### **After**

![Markets loaded with SDK 0.32.2](evidence-market-loaded.png)

## **Pre-merge author checklist**

- [x] I've followed [MetaMask Contributor Docs](https://github.com/MetaMask/contributor-docs) and [MetaMask Mobile Coding Standards](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/CODING_GUIDELINES.md).
- [x] I've completed the PR template to the best of my ability
- [x] I've included tests if applicable
- [x] I've documented my code using [JSDoc](https://jsdoc.app/) format if applicable
- [x] I've applied the right labels on the PR (see [labeling guidelines](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/LABELING_GUIDELINES.md)). Not required for external contributors.

## **Pre-merge reviewer checklist**

- [ ] I've manually tested the PR (e.g. pull and build branch, run the app, test code being changed).
- [ ] I confirm that this PR addresses all acceptance criteria described in the ticket it closes and includes the necessary testing evidence such as recordings and or screenshots.

<details>
<summary>## **Validation Recipe**</summary>

```json
{
  "title": "Hyperliquid SDK update — verify market data loads with SDK 0.32.2",
  "description": "Smoke test: validates that the Hyperliquid SDK 0.32.2 integration works correctly by confirming market data is available via the perps controller.",
  "validate": {
    "runtime": {
      "pre_conditions": [
        "wallet.unlocked",
        "perps.feature_enabled"
      ],
      "steps": [
        {
          "id": "nav-market-list",
          "action": "navigate",
          "target": "PerpsTrendingView"
        },
        {
          "id": "wait-route",
          "action": "wait_for",
          "route": "PerpsTrendingView"
        },
        {
          "id": "wait-market-data",
          "action": "wait_for",
          "expression": "Engine.context.PerpsController.getMarketDataWithPrices().then(function(ms){return JSON.stringify({count:ms.length})})",
          "assert": {
            "operator": "gt",
            "field": "count",
            "value": 0
          },
          "timeout_ms": 30000
        },
        {
          "id": "assert-btc-in-markets",
          "action": "eval_async",
          "expression": "Engine.context.PerpsController.getMarketDataWithPrices().then(function(ms){var m=ms.find(function(x){return x.symbol==='BTC'});return JSON.stringify({found:!!m,symbol:m?m.symbol:null})})",
          "assert": {
            "operator": "eq",
            "field": "found",
            "value": true
          }
        },
        {
          "id": "evidence-market-loaded",
          "action": "screenshot",
          "filename": "evidence-market-loaded.png"
        }
      ]
    }
  }
}
```

**Result: 5/5 steps passed ✅**

</details>
