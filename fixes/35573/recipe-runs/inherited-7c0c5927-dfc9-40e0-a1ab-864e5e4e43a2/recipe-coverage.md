# Recipe coverage

Re-validation of family-inherited recipe against `branch + origin/main` plus review-comment race fix. Live run PASS 13/13.

| # | AC (verbatim) | Proof mode | Primary evidence | Recipe nodes (IDs) | Visual file if any | Evidence verdict | Justification |
|---|---------------|------------|------------------|---------------------|--------------------|------------------|---------------|
| 1 | The deposit button should provide immediate feedback or navigate to a skeleton loader to feel responsive. | mixed | ui.screenshot | ac1-press-deposit, ac1-wait-confirmation, ac1-wait-pay-with, ac1-screenshot-confirmation | recipe-run/screenshots/evidence-ac1-deposit-confirmation.png | PROVEN | After tap, `custom-amount-input` and `pay-with` present. Screenshot shows Add funds amount keypad and Pay with ETH ($3.17). simctl, not a fallback. |
| 2 | The token list should load efficiently without several seconds of lag. | mixed | ui.screenshot | ac2-press-pay-with, ac2-wait-token-sheet, ac2-screenshot-token-list | recipe-run/screenshots/evidence-ac2-pay-with-list.png | PROVEN | Screenshot shows Pay with sheet with ETH ($3.17 available) and Other assets. `pay-with-crypto-section-preferred-token-row` present. |

Forbidden patterns: none.

Overall recipe coverage: 2/2 ACs PROVEN (untestable: none, weak: 0, missing: 0)
