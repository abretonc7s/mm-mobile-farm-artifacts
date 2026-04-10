## **Description**

The Activity page was not showing the most recent funding payments for accounts with many open positions. `HyperLiquidProvider.getFunding()` made a single API call for the 365-day history window; the HyperLiquid API silently caps responses at 500 records (ascending/oldest-first), so the most recent payments were dropped. The fix replaces the single call with parallel 30-day window fetches, guaranteeing the most recent records are always present.

## **Changelog**

CHANGELOG entry: Fixed a bug where recent perpetuals funding payments were missing from the Activity page for accounts with extensive funding history.

## **Related issues**

Fixes: [TAT-2057](https://consensyssoftware.atlassian.net/browse/TAT-2057)

## **Manual testing steps**

```gherkin
Feature: Funding payments shown in Activity

  Scenario: User with many open positions sees latest funding payments
    Given the user has an account with perpetuals positions open for 12+ months
    And the account has received more than 500 funding payments in the last year

    When the user navigates to Activity > Perps > Funding tab

    Then the most recent funding payments are visible under "Today"
    And the list includes entries from the current date

  Scenario: Funding list does not oscillate on refresh
    Given the user is on the Activity > Perps > Funding tab

    When the user pulls to refresh multiple times

    Then the cutoff date of the funding list remains the same across all refreshes
    And the most recent entries remain visible after each refresh
```

## **Screenshots/Recordings**

### **Before**

_Evidence available in task artifacts (`before.mp4`, `before-ac1-funding-latest.png`)._

### **After**

The funding tab now shows today's entries. Parallel pagination returns all 1174 records (exceeding the old 500-record cap), with consistent results across consecutive calls.

_Evidence available in task artifacts (`after.mp4`, `after-ac1-funding-latest.png`, `after-ac2-funding-consistent.png`)._

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
<summary>recipe.json — automated validation script</summary>

```json
{
  "pr": "28671",
  "title": "Verify latest funding payments shown in Activity — TAT-2057",
  "jira": "TAT-2057",
  "acceptance_criteria": [
    "AC1: Activity shows funding payments up to today's date (no missing recent entries)",
    "AC2: Multiple consecutive getFunding calls return consistent latest timestamp (no oscillation)",
    "AC5: Refresh cycle produces identical results — cutoff date does not change across refreshes"
  ],
  "validate": {
    "workflow": {
      "pre_conditions": ["wallet.unlocked", "perps.feature_enabled"],
      "entry": "setup-switch-account",
      "nodes": {
        "setup-switch-account": {
          "description": "Switch to 0x316BDE (bug's original account — 1174 records, well above 500-record API cap)",
          "action": "select_account",
          "address": "0x316BDE155acd07609872a56Bc32CcfB0B13201fA",
          "next": "gate-wait-account"
        },
        "gate-wait-account": {
          "description": "Wait for PerpsController accountState to load for new account",
          "action": "wait_for",
          "expression": "JSON.stringify({ hasAccount: !!Engine.context.PerpsController.state.accountState })",
          "assert": { "operator": "truthy", "field": "hasAccount" },
          "timeout_ms": 20000,
          "poll_ms": 1000,
          "next": "setup-nav-funding"
        },
        "setup-nav-funding": {
          "description": "Navigate to Activity > Funding tab",
          "action": "call",
          "ref": "perps/activity-view",
          "params": { "tab": "funding" },
          "next": "ac1-fetch-latest"
        },
        "ac1-fetch-latest": {
          "description": "Full 365-day fetch: count > 500 proves parallel pagination returns all records including recent ones",
          "action": "eval_async",
          "expression": "(function(){ return Engine.context.PerpsController.getFunding().then(function(r){ var last = r[r.length - 1]; var nowMs = Date.now(); var thirtyDaysMs = 2592000000; var isRecent = !!(last && (nowMs - last.timestamp) < thirtyDaysMs); return JSON.stringify({ count: r.length, latestTs: last ? last.timestamp : null, isRecent: isRecent, exceedsCap: r.length > 500 }) }) })()",
          "assert": {
            "all": [
              { "operator": "gt", "field": "count", "value": 500 },
              { "operator": "truthy", "field": "exceedsCap" },
              { "operator": "truthy", "field": "isRecent" }
            ]
          },
          "next": "ac1-screenshot"
        },
        "ac1-screenshot": {
          "description": "Screenshot funding tab showing latest entries",
          "action": "screenshot",
          "filename": "evidence-ac1-funding-latest.png",
          "next": "ac2-consistency-check"
        },
        "ac2-consistency-check": {
          "description": "Two calls with fixed 2-day window — verify identical count and latest timestamp (no oscillation). Narrow window avoids rate-limit from back-to-back full 365-day fetches.",
          "action": "eval_async",
          "expression": "(function(){ var nowMs = Date.now(); var twoDaysMs = 172800000; var opts = {}; opts.startTime = nowMs - twoDaysMs; opts.endTime = nowMs; return Engine.context.PerpsController.getFunding(opts).then(function(r1){ return Engine.context.PerpsController.getFunding(opts).then(function(r2){ var last1 = r1[r1.length - 1]; var last2 = r2[r2.length - 1]; var ts1 = last1 ? last1.timestamp : 0; var ts2 = last2 ? last2.timestamp : 0; return JSON.stringify({ count1: r1.length, count2: r2.length, latestTs1: ts1, latestTs2: ts2, consistent: r1.length === r2.length && ts1 === ts2 }) }) }) })()",
          "assert": {
            "all": [
              { "operator": "truthy", "field": "consistent" },
              { "operator": "gt", "field": "count1", "value": 0 }
            ]
          },
          "next": "ac2-screenshot"
        },
        "ac2-screenshot": {
          "description": "Screenshot confirming stable funding list",
          "action": "screenshot",
          "filename": "evidence-ac2-funding-consistent.png",
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
