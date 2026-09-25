## **Description**

Removing isolated margin failed ~20–27% of the time with Hyperliquid's "Position does not have sufficient margin for reduction." Max offered the exact transfer boundary from the last position snapshot. Isolated margin moves 1:1 with mark price, so any adverse tick before the exchange processed the request got it rejected. Max now keeps 1% of notional as headroom, and input is validated against the exchange boundary so a tick after choosing Max doesn't block it. The position is re-read right before a removal; if it shrank, the user gets an "amount changed" message instead of a raw rejection, and Max/slider stay within that fresh limit for up to 10s, or until the position's size, entry, leverage or collateral changes (PnL re-deliveries don't release it). If the re-read fails or comes back without the position (the provider returns an empty list on fetch errors too), the removal goes through and the exchange decides. A position with nothing removable shows an explanation with the amount, slider and Confirm disabled.

Cross margin order placement (previously in this PR) moved to #36782 to keep each PR under the 1000-line limit.

## **Changelog**

CHANGELOG entry: Fixed margin removal failing with "Position does not have sufficient margin for reduction" when removing the maximum amount

## **Related issues**

Fixes: [TAT-3985](https://consensyssoftware.atlassian.net/browse/TAT-3985)

## **Manual testing steps**

```gherkin
Feature: Remove isolated margin

  Scenario: user removes the maximum margin
    Given a funded perps account with an isolated position that has margin above its requirement
    When user opens the position, taps Margin > Remove Margin, taps the amount, taps Max, then Done and Remove Margin
    Then the removal succeeds and a "Removed $X margin" toast appears

  Scenario: user opens Remove Margin with nothing removable
    Given a freshly opened isolated position
    When user taps Margin > Remove Margin
    Then the screen explains that no margin can be removed and the amount, slider and button are disabled

```

## **Screenshots/Recordings**

Hyperliquid testnet, Trading account. Remove margin: Max keeps 1% headroom and is accepted; $0 removable is explained and disabled. Cross margin evidence moved to #36782.

<table>
<tr><td colspan="2"><strong>Max removal: exchange rejection before, accepted after the offered max ticked down</strong></td></tr>
<tr>
<td align="center" valign="top" width="50%"><em>Before</em><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36775/before-evidence-ac1-rejected-toast.png?sha=ced3660debfcf98e" alt="before" width="320" /></td>
<td align="center" valign="top" width="50%"><em>After</em><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36775/after-ac1-max-form.png?sha=179b60a1a54e3824" alt="after" width="320" /></td>
</tr>
<tr><td colspan="2"><strong>Nothing removable: no explanation before, disabled with explanation after</strong></td></tr>
<tr>
<td align="center" valign="top" width="50%"><em>Before</em><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36775/before-evidence-ac2-zero-state.png?sha=c84e5ddcdb00e901" alt="before" width="320" /></td>
<td align="center" valign="top" width="50%"><em>After</em><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36775/after-ac2-zero-state.png?sha=8502e26c23c7a2c3" alt="after" width="320" /></td>
</tr>
</table>

<table>
<tr><td align="center" valign="top" width="50%"><strong>Max removal accepted by the exchange</strong><br/><img src="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36775/after-ac1-removed-toast.png?sha=fcd9eb3511e3bacb" alt="Max removal accepted by the exchange" width="320" /></td><td></td></tr>
</table>

**Video**
<table>
<tr><td align="center" width="50%"><em>Before</em><br/><a href="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36775/before.mp4?sha=f826fde0979b4bc8">before.mp4</a></td>
<td align="center" width="50%"><em>After</em><br/><a href="https://raw.githubusercontent.com/abretonc7s/mm-mobile-farm-artifacts/main/fixes/36775/after.mp4?sha=d0f321fa9c263669">after.mp4</a></td></tr>
</table>

## **Validation Recipe**

<details><summary>recipe.json (Remove margin max is accepted and the zero state is explained)</summary>

```json
{
  "$schema": "https://farmslot.io/schemas/recipe-v1.schema.json",
  "title": "Remove margin max is accepted and the zero state is explained",
  "description": "TAT-3985: on an isolated BTC testnet position (Trading account), add $20 margin, remove the offered Max and require exchange acceptance, then require the zero-removable explanation on a fresh SOL position; pre-submit re-validation is proven by focused tests. Cross margin order placement moved to its own PR.",
  "workflow": {
    "entry": "setup-session",
    "nodes": {
      "setup-session": {
        "action": "call",
        "ref": "perps.venue-start-state",
        "params": {
          "account": "Trading",
          "provider": "hyperliquid",
          "network": "testnet",
          "market": "BTC",
          "market_mode": "lite"
        },
        "intent": "Select the funded Trading account on Hyperliquid testnet where the isolated BTC position lives",
        "next": "setup-pin-screen-variant"
      },
      "setup-assert-position": {
        "action": "metamask.perps.ensure_positions",
        "market": "BTC",
        "side": "long",
        "state": "open",
        "notional": "250",
        "intent": "Converge the isolated BTC long the margin flow acts on, opening one if the testnet account has none",
        "next": "setup-add-home"
      },
      "setup-add-home": {
        "action": "ui.navigate",
        "page": "home",
        "intent": "Reset navigation so the market screen is the only margin entry point",
        "next": "setup-add-nav"
      },
      "setup-add-nav": {
        "action": "ui.navigate",
        "page": "perps-market",
        "market": "BTC",
        "intent": "Open the BTC market holding the isolated position",
        "next": "setup-lite-mode"
      },
      "setup-add-wait-margin-card": {
        "action": "ui.wait_for",
        "test_id": "position-card-margin",
        "expected": "present",
        "timeout_ms": 15000,
        "intent": "Make sure the position margin card is mounted before opening margin actions",
        "next": "setup-add-press-margin-card"
      },
      "setup-add-press-margin-card": {
        "action": "ui.press",
        "test_id": "position-card-margin",
        "intent": "Open the margin action choice for the position to add headroom",
        "next": "setup-press-add"
      },
      "setup-press-add": {
        "action": "ui.press",
        "test_id": "perps-adjust-margin-add-btn",
        "intent": "Choose Add Margin so the position has margin that can later be removed",
        "next": "setup-open-keypad"
      },
      "setup-open-keypad": {
        "action": "ui.press",
        "test_id": "perps-amount-display-touchable",
        "intent": "Open the keypad to type the margin to add",
        "next": "setup-key-2"
      },
      "setup-key-2": {
        "action": "ui.press",
        "test_id": "keypad-key-2",
        "intent": "Type the tens digit of the $20 addition",
        "next": "setup-key-0"
      },
      "setup-key-0": {
        "action": "ui.press",
        "test_id": "keypad-key-0",
        "intent": "Type the units digit of the $20 addition",
        "next": "setup-close-keypad"
      },
      "setup-close-keypad": {
        "action": "ui.press",
        "test_id": "perps-adjust-margin-done-button",
        "intent": "Close the keypad to reach the confirm button",
        "next": "setup-confirm-add"
      },
      "setup-confirm-add": {
        "action": "ui.press",
        "test_id": "perps-adjust-margin-confirm-button",
        "intent": "Submit the $20 margin addition",
        "next": "setup-assert-added"
      },
      "setup-assert-added": {
        "action": "ui.wait_for",
        "text": "Added $20 margin",
        "text_match": "contains",
        "expected": "visible",
        "timeout_ms": 20000,
        "intent": "Confirm the exchange accepted the addition so removable headroom exists",
        "next": "ac1-home"
      },
      "ac1-home": {
        "action": "ui.navigate",
        "page": "home",
        "intent": "Reset navigation so the market screen is the only margin entry point",
        "next": "ac1-nav"
      },
      "ac1-nav": {
        "action": "ui.navigate",
        "page": "perps-market",
        "market": "BTC",
        "intent": "Open the BTC market holding the isolated position",
        "next": "ac1-wait-margin-card"
      },
      "ac1-wait-margin-card": {
        "action": "ui.wait_for",
        "test_id": "position-card-margin",
        "expected": "present",
        "timeout_ms": 15000,
        "intent": "Make sure the position margin card is mounted before opening margin actions",
        "next": "ac1-press-margin-card"
      },
      "ac1-press-margin-card": {
        "action": "ui.press",
        "test_id": "position-card-margin",
        "intent": "Open the margin action choice for the position to remove the maximum",
        "next": "ac1-press-remove"
      },
      "ac1-press-remove": {
        "action": "ui.press",
        "test_id": "perps-adjust-margin-reduce-btn",
        "intent": "Choose Remove Margin as the user in the ticket does",
        "next": "ac1-open-keypad"
      },
      "ac1-open-keypad": {
        "action": "ui.press",
        "test_id": "perps-amount-display-touchable",
        "intent": "Reveal the quick-amount buttons including Max",
        "next": "ac1-press-max"
      },
      "ac1-press-max": {
        "action": "ui.press",
        "text": "Max",
        "intent": "Select the maximum removable amount the app offers",
        "next": "ac1-close-keypad"
      },
      "ac1-close-keypad": {
        "action": "ui.press",
        "test_id": "perps-adjust-margin-done-button",
        "intent": "Close the keypad to show the summary and confirm button",
        "next": "ac1-wait-available"
      },
      "ac1-wait-available": {
        "action": "ui.wait_for",
        "test_id": "perps-adjust-margin-available-value",
        "expected": "visible",
        "timeout_ms": 10000,
        "intent": "Show the offered removable amount before submitting it",
        "next": "ac1-screenshot-max-form"
      },
      "ac1-screenshot-max-form": {
        "action": "ui.screenshot",
        "label": "AC1: Max amount offered for removal",
        "intent": "Record the max removable amount the user is about to submit",
        "next": "ac1-press-confirm"
      },
      "ac1-press-confirm": {
        "action": "ui.press",
        "test_id": "perps-adjust-margin-confirm-button",
        "intent": "Submit the max margin removal to the exchange",
        "next": "ac1-assert-removed"
      },
      "ac1-assert-removed": {
        "action": "ui.wait_for",
        "text": "Removed $",
        "text_match": "contains",
        "expected": "visible",
        "timeout_ms": 20000,
        "intent": "Confirm the exchange accepted the max removal the app offered",
        "next": "ac1-screenshot-removed"
      },
      "ac1-screenshot-removed": {
        "action": "ui.screenshot",
        "label": "AC1: max removal accepted",
        "intent": "Show reviewers the exchange accepted the offered max amount",
        "next": "ac1-assert-no-rejection"
      },
      "ac1-assert-no-rejection": {
        "action": "ui.wait_for",
        "text": "Margin adjustment failed",
        "text_match": "contains",
        "expected": "absent",
        "timeout_ms": 3000,
        "intent": "Confirm no exchange rejection toast followed the max removal",
        "next": "setup-sol-flat"
      },
      "ac2-home": {
        "action": "ui.navigate",
        "page": "home",
        "intent": "Reset navigation so the market screen is the only margin entry point",
        "next": "ac2-nav"
      },
      "ac2-nav": {
        "action": "ui.navigate",
        "page": "perps-market",
        "market": "SOL",
        "intent": "Open the SOL market holding the freshly opened isolated position",
        "next": "ac2-wait-margin-card"
      },
      "ac2-wait-margin-card": {
        "action": "ui.wait_for",
        "test_id": "position-card-margin",
        "expected": "present",
        "timeout_ms": 15000,
        "intent": "Make sure the position margin card is mounted before opening margin actions",
        "next": "ac2-press-margin-card"
      },
      "ac2-press-margin-card": {
        "action": "ui.press",
        "test_id": "position-card-margin",
        "intent": "Open the margin action choice for the position to check the zero state",
        "next": "ac2-press-remove"
      },
      "ac2-press-remove": {
        "action": "ui.press",
        "test_id": "perps-adjust-margin-reduce-btn",
        "intent": "Open Remove Margin on a position that has nothing left to remove",
        "next": "ac2-assert-explanation"
      },
      "ac2-assert-explanation": {
        "action": "ui.wait_for",
        "test_id": "perps-adjust-margin-no-removable-margin",
        "expected": "visible",
        "timeout_ms": 10000,
        "intent": "Confirm the user is told why no margin can be removed",
        "next": "ac2-screenshot-zero-state"
      },
      "ac2-screenshot-zero-state": {
        "action": "ui.screenshot",
        "label": "AC2: zero removable explained, control disabled",
        "intent": "Show reviewers the remove control is disabled and explains why nothing can be removed",
        "next": "teardown-sol"
      },
      "ac3-run-unit-tests": {
        "action": "command",
        "cmd": "yarn jest app/components/UI/Perps/utils/marginUtils.test.ts app/components/UI/Perps/hooks/usePerpsMarginAdjustment.test.ts app/components/UI/Perps/hooks/usePerpsAdjustMarginData.test.ts app/components/UI/Perps/hooks/usePerpsToasts.test.tsx app/components/UI/Perps/Views/PerpsAdjustMarginView/PerpsAdjustMarginView.test.tsx app/components/UI/Perps/components/PerpsAdjustMarginBottomSheet/PerpsAdjustMarginBottomSheet.test.tsx --no-coverage > /tmp/tat3985-jest.log 2>&1\nstatus=$?\ntail -40 /tmp/tat3985-jest.log\nexit $status",
        "timeout_ms": 300000,
        "allow_failure": true,
        "intent": "Prove the pre-submit re-validation, headroom and zero-removable state through focused tests",
        "next": "ac3-assert-tests-pass"
      },
      "ac3-assert-tests-pass": {
        "action": "assert_exit_code",
        "source": "ac3-run-unit-tests",
        "expected": 0,
        "intent": "Require the re-validation and headroom tests to pass",
        "next": "done"
      },
      "done": {
        "action": "end",
        "status": "pass"
      },
      "setup-sol-flat": {
        "action": "metamask.perps.ensure_positions",
        "market": "SOL",
        "state": "none",
        "intent": "Start AC2 from no SOL position so the new one is freshly opened",
        "next": "setup-sol-open"
      },
      "setup-sol-open": {
        "action": "metamask.perps.place_order",
        "market": "SOL",
        "side": "long",
        "notional": "15",
        "leverage": 3,
        "intent": "Open a fresh isolated SOL position whose margin sits at the transfer floor, leaving nothing removable",
        "next": "setup-sol-assert"
      },
      "setup-sol-assert": {
        "action": "metamask.perps.assert_positions",
        "market": "SOL",
        "state": "open",
        "intent": "Require the fresh SOL position before opening its remove-margin screen",
        "next": "ac2-home"
      },
      "teardown-sol": {
        "action": "metamask.perps.ensure_positions",
        "market": "SOL",
        "state": "none",
        "intent": "Close the SOL position this run opened so the account returns to its prior state",
        "next": "teardown-clear-flags"
      },
      "setup-lite-mode": {
        "action": "metamask.perps.ensure_mode",
        "mode": "lite",
        "intent": "Return to Lite so the market screen shows the position margin card, even after a previous run ended in Pro",
        "next": "setup-add-wait-margin-card"
      },
      "setup-pin-screen-variant": {
        "action": "metamask.feature_flags.set",
        "flags": {
          "perpsTAT3938AbtestScreenVsBottomSheet": "control"
        },
        "intent": "Pin the full-screen margin flow this recipe drives; the screen-vs-bottom-sheet A/B test otherwise picks per slot",
        "next": "setup-assert-position"
      },
      "teardown-clear-flags": {
        "action": "metamask.feature_flags.clear",
        "intent": "Drop the A/B pin so later runs start from remote flags",
        "next": "ac3-run-unit-tests"
      }
    }
  }
}
```
</details>

## **Validation Logs**

<details><summary>Full output (50/50 passed, pass)</summary>

```
# MetaMask Recipe Run

Status: pass
Duration: 79s
Nodes: 50/50 passed

## Side findings
- REVIEW 18 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-session/start (metamask.perps.start_state, 13s): proof=metamask-perps-start-state
- PASS setup-session/provider (assert_output, 36ms): source=start, stream=stdout
- PASS setup-session/network (assert_output, 34ms): source=start, stream=stdout
- PASS setup-session/account (switch, 34ms): matched=false, value=0x316b...01fa, expected=Trading
- PASS setup-session/account-name (assert_output, 30ms): source=start, stream=stdout
- PASS setup-session/done (end, 0ms)
- PASS setup-session (call, 13s): ref=perps.venue-start-state, status=pass
- PASS setup-pin-screen-variant (metamask.feature_flags.set, 472ms): proof=mobile-remote-feature-flags
- PASS setup-assert-position (metamask.perps.ensure_positions, 1.2s): matching=1
- PASS setup-add-home (ui.navigate, 1.6s): route=WalletView, page=home, proof=agentic-navigation
- PASS setup-add-nav (ui.navigate, 2.0s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-lite-mode (metamask.perps.ensure_mode, 412ms): proof=visible-market-detail-root-and-active-mode-control
- PASS setup-add-wait-margin-card (ui.wait_for, 1.0s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS setup-add-press-margin-card (ui.press, 796ms): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS setup-press-add (ui.press, 935ms): ok=true, testId=perps-adjust-margin-add-btn, deviceName=mm-6
- PASS setup-open-keypad (ui.press, 926ms): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS setup-key-2 (ui.press, 805ms): ok=true, testId=keypad-key-2, deviceName=mm-6
- PASS setup-key-0 (ui.press, 662ms): ok=true, testId=keypad-key-0, deviceName=mm-6
- PASS setup-close-keypad (ui.press, 690ms): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS setup-confirm-add (ui.press, 1.1s): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mm-6
- PASS setup-assert-added (ui.wait_for, 1.9s): matched=true, text=Added $20 margin, textMatch=contains, expected=visible, present=true
- PASS ac1-home (ui.navigate, 1.4s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac1-nav (ui.navigate, 2.3s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac1-wait-margin-card (ui.wait_for, 1.2s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac1-press-margin-card (ui.press, 1.2s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS ac1-press-remove (ui.press, 1.2s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mm-6
- PASS ac1-open-keypad (ui.press, 804ms): ok=true, testId=perps-amount-display-touchable, deviceName=mm-6
- PASS ac1-press-max (ui.press, 612ms): ok=true, text=Max, deviceName=mm-6
- PASS ac1-close-keypad (ui.press, 689ms): ok=true, testId=perps-adjust-margin-done-button, deviceName=mm-6
- PASS ac1-wait-available (ui.wait_for, 794ms): matched=true, testId=perps-adjust-margin-available-value, expected=visible, present=true, visible=true
- PASS ac1-press-confirm (ui.press, 746ms): ok=true, testId=perps-adjust-margin-confirm-button, deviceName=mm-6
- PASS ac1-assert-removed (ui.wait_for, 1.5s): matched=true, text=Removed $, textMatch=contains, expected=visible, present=true
- PASS ac1-assert-no-rejection (ui.wait_for, 723ms): matched=true, text=Margin adjustment failed, textMatch=contains, expected=absent, present=false
- PASS setup-sol-flat (metamask.perps.ensure_positions, 667ms): matching=0
- PASS setup-sol-open (metamask.perps.place_order, 5.9s): matching=1
- PASS setup-sol-assert (metamask.perps.assert_positions, 608ms): matching=1
- PASS ac2-home (ui.navigate, 1.9s): route=WalletView, page=home, proof=agentic-navigation
- PASS ac2-nav (ui.navigate, 3.0s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS ac2-wait-margin-card (ui.wait_for, 1.2s): matched=true, testId=position-card-margin, expected=present, present=true, visible=true
- PASS ac2-press-margin-card (ui.press, 1.1s): ok=true, testId=position-card-margin, deviceName=mm-6
- PASS ac2-press-remove (ui.press, 1.3s): ok=true, testId=perps-adjust-margin-reduce-btn, deviceName=mm-6
- PASS ac2-assert-explanation (ui.wait_for, 875ms): matched=true, testId=perps-adjust-margin-no-removable-margin, expected=visible, present=true, visible=true
- PASS teardown-sol (metamask.perps.ensure_positions, 3.9s): matching=0
- PASS teardown-clear-flags (metamask.feature_flags.clear, 356ms): proof=mobile-remote-feature-flags
- PASS ac3-run-unit-tests (command, 12s): exitCode=0, stdout=PASS app/components/UI/Perps/components/PerpsAdjustMarginBottomSheet/PerpsAdjustMarginBottomSheet.test.tsx (7.547 s)
PASS app/components/UI/Perps/hooks/usePerpsMarginAdjustment.test.ts
PASS app/components/UI/Perps/hooks/usePerpsAdjustMarginData.test.ts
PASS app/components/UI/Perps/utils/marginUtils.test.ts
PASS app/components/UI/Perps/Views/PerpsAdjustMarginView/PerpsAdjustMarginView.test.tsx (8.612 s)
PASS app/components/UI/Perps/hooks/usePerpsToasts.test.tsx (9.017 s)

Test Suites: 6 passed, 6 total
Tests:       240 passed, 240 total
Snapshots:   0 total
Time:        9.183 s, estimated 12 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/marginUtils.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsMarginAdjustment.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsAdjustMarginData.test.ts|app\/components\/UI\/Perps\/hooks\/usePerpsToasts.test.tsx|app\/components\/UI\/Perps\/Views\/PerpsAdjustMarginView\/PerpsAdjustMarginView.test.tsx|app\/components\/UI\/Perps\/components\/PerpsAdjustMarginBottomSheet\/PerpsAdjustMarginBottomSheet.test.tsx/i.

- PASS ac3-assert-tests-pass (assert_exit_code, 37ms): source=ac3-run-unit-tests, expected=0, actual=0
- PASS done (end, 0ms)
```
</details>

## **Pre-merge author checklist**

- [x] I've followed [MetaMask Contributor Docs](https://github.com/MetaMask/contributor-docs) and [MetaMask Mobile Coding Standards](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/CODING_GUIDELINES.md).
- [x] I've completed the PR template to the best of my ability
- [x] I've included tests if applicable
- [x] I've documented my code using [JSDoc](https://jsdoc.app/) format if applicable
- [x] I've applied the right labels on the PR (see [labeling guidelines](https://github.com/MetaMask/metamask-mobile/blob/main/.github/guidelines/LABELING_GUIDELINES.md)). Not required for external contributors.

#### Performance checks (if applicable)

- [x] I've tested on Android
  - Ideally on a mid-range device; emulator is acceptable
- [x] I've tested with a power user scenario
  - Use these [power-user SRPs](https://consensyssoftware.atlassian.net/wiki/spaces/TL1/pages/edit-v2/401401446401?draftShareId=9d77e1e1-4bdc-4be1-9ebb-ccd916988d93) to import wallets with many accounts and tokens
- [x] I've instrumented key operations with Sentry traces for production performance metrics
  - See [`trace()`](/app/util/trace.ts) for usage and [`addToken`](/app/components/Views/AddAsset/components/AddCustomToken/AddCustomToken.tsx#L274) for an example

For performance guidelines and tooling, see the [Performance Guide](https://consensyssoftware.atlassian.net/wiki/spaces/TL1/pages/400085549067/Performance+Guide+for+Engineers).

## **Pre-merge reviewer checklist**

- [ ] I've manually tested the PR (e.g. pull and build branch, run the app, test code being changed).
- [ ] I confirm that this PR addresses all acceptance criteria described in the ticket it closes and includes the necessary testing evidence such as recordings and or screenshots.

[TAT-3985]: https://consensyssoftware.atlassian.net/browse/TAT-3985?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Changes pre-submit validation and max calculations for real margin withdrawals on isolated positions; incorrect limits could block valid removals or still allow bad submits if fresh-read fallback paths misfire.
> 
> **Overview**
> Fixes frequent **remove margin** failures when users picked **Max** or when the position had nothing left to withdraw.
> 
> **Max / slider** now subtracts **1% of notional** from the removable cap so submissions survive mark-price moves at the exchange. Validation still uses a separate **exchange max** so a small live tick after choosing Max does not falsely block confirm.
> 
> **Before submit**, removals trigger a **fresh position read** (`skipCache`). If the amount no longer fits, the app shows a **warning toast**, resets the input to the new safe max via `onAmountChanged`, and **`usePerpsFreshRemovalLimit`** keeps that cap for ~10s (until size/leverage/collateral changes or the hold expires)—PnL-only stream updates do not lift it early.
> 
> When **nothing is removable**, the full-screen and bottom-sheet flows show **`no_removable_margin`**, disable amount entry, slider, and confirm, and add matching test IDs.
> 
> Copy and toasts cover the zero state and **“Removable margin changed”** messaging.
> 
> <sup>Reviewed by [Cursor Bugbot](https://cursor.com/bugbot) for commit 6421cb99d5b88f3a77298703a3a2ac89ff46f93d. Bugbot is set up for automated code reviews on this repo. Configure [here](https://www.cursor.com/dashboard/bugbot).</sup>
<!-- /CURSOR_SUMMARY -->


