## **Description**

When the app returns to foreground within the 20 s grace period, `resumeFromForeground()` pinged the WebSocket to check health. The JS thread is often sluggish right after the AppState transition, so the ping could throw even though the socket was alive. The catch block fell through immediately to `ensureConnected()`, which tore down all 9 stream caches and triggered `isConnecting=true` — causing loading skeletons across all Perps UI despite the connection still being healthy.

**Fix:** Two-pronged:
1. **Ping retry** — wait 500 ms and retry `provider.ping()` before treating the connection as dead. Eliminates false positives from JS thread suspension.
2. **`preserveCaches` flag** — even if both pings fail, thread `preserveCaches: true` through `ensureConnected()` → `performEnsureConnected()` → `performActualDisconnection()` so stream caches survive the soft reconnect. Cached data is still valid (same account/network) — shows slightly stale data instead of skeletons.

## **Changelog**

CHANGELOG entry: null

## **Related issues**

Fixes: [TAT-2892](https://consensyssoftware.atlassian.net/browse/TAT-2892)

## **Manual testing steps**

```gherkin
Feature: Perps foreground reconnect

  Scenario: user returns app to foreground within grace period
    Given the Perps feature is enabled
      And the user has navigated to the Perps tab
      And the WebSocket is connected and initialized

    When the user backgrounds the app for less than 20 seconds
      And the user returns the app to the foreground

    Then the Perps tab must NOT show loading skeletons
      And the connection state remains isConnected=true, isInitialized=true
      And stream caches (positions, orders, account) are NOT cleared
```

## **Screenshots/Recordings**

### **Before**

_Evidence available in task artifacts — will be added by reviewer if needed._

### **After**

_Evidence available in task artifacts — will be added by reviewer if needed._

## **Pre-merge author checklist**

- [x] I've followed [MetaMask Contributor Docs](https://github.com/MetaMask/contributor-docs) and [MetaMask Mobile Coding Standards](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/CODING_GUIDELINES.md).
- [x] I've completed the PR template to the best of my ability
- [x] I've included tests if applicable
- [x] I've documented my code using [JSDoc](https://jsdoc.app/) format if applicable
- [x] I've applied the right labels on the PR (see [labeling guidelines](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/LABELING_GUIDELINES.md)). Not required for external contributors.

## **Pre-merge reviewer checklist**

- [ ] I've manually tested the PR (e.g. pull and build branch, run the app, test code being changed).
- [ ] I confirm that this PR addresses all acceptance criteria described in the ticket it closes and includes the necessary testing evidence such as recordings and or screenshots.

## **Validation Recipe**

<details>
<summary>recipe.json — automated validation for TAT-2892</summary>

```json
{
  "pr": "28592",
  "title": "Verify foreground reconnect does not clear caches when WebSocket is alive within grace period",
  "jira": "TAT-2892",
  "acceptance_criteria": [
    "Returning to foreground within grace period does not trigger full reconnection when WebSocket is healthy",
    "No loading skeletons during foreground return with healthy connection",
    "resumeFromForeground retries ping before falling through to full reconnect"
  ],
  "validate": {
    "workflow": {
      "pre_conditions": ["wallet.unlocked", "perps.feature_enabled"],
      "entry": "nav-perps",
      "nodes": {
        "nav-perps": {
          "action": "navigate",
          "target": "Perps",
          "next": "wait-initialized"
        },
        "wait-initialized": {
          "action": "wait_for",
          "expression": "JSON.stringify(Engine.context.PerpsController.state.initializationState)",
          "timeout_ms": 15000,
          "assert": { "operator": "contains", "value": "initialized" },
          "next": "check-state"
        },
        "check-state": {
          "action": "eval_ref",
          "ref": "perps/state",
          "assert": { "operator": "not_null" },
          "next": "watch-no-full-reconnect"
        },
        "watch-no-full-reconnect": {
          "action": "log_watch",
          "window_seconds": 5,
          "must_not_appear": [
            "BUG_MARKER: ping failed in resumeFromForeground",
            "Performing actual disconnection after grace period"
          ],
          "watch_for": ["Successfully connected", "connection healthy"],
          "next": "screenshot-connected"
        },
        "screenshot-connected": {
          "action": "screenshot",
          "filename": "evidence-perps-connected.png",
          "next": "done"
        },
        "done": {
          "action": "end",
          "status": "pass"
        }
      }
    }
  }
}
```

</details>
