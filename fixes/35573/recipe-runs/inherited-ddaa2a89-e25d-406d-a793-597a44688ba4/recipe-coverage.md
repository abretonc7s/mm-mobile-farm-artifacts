# Recipe coverage

| # | AC (verbatim) | Proof mode | Primary evidence | Recipe nodes (IDs) | Visual file if any | Evidence verdict | Justification |
|---|---------------|------------|------------------|---------------------|--------------------|------------------|---------------|
| 1 | The deposit button should provide immediate feedback or navigate to a skeleton loader to feel responsive. | mixed | ui.screenshot | ac1-press-deposit, ac1-wait-confirmation, ac1-wait-pay-with, ac1-screenshot-confirmation | before-evidence-ac1-deposit-confirmation.png, after-ac1-deposit-confirmation.png | PROVEN | After tap, `custom-amount-input` and `pay-with` are present. After screenshot shows the Add funds amount screen with keypad and Pay with ETH. Trace nodes passed. Unit tests prove navigate is not awaited on deposit prep. |
| 2 | The token list should load efficiently without several seconds of lag. | mixed | ui.screenshot | ac2-press-pay-with, ac2-wait-token-sheet, ac2-screenshot-token-list | before-evidence-ac2-pay-with-list.png, after-ac2-pay-with-list.png | PROVEN | After screenshot shows the Pay with sheet with ETH ($3.17) and Other assets. `pay-with-crypto-section-preferred-token-row` was present. Trace nodes passed. |

Forbidden patterns (step 13): none.

Analyzer note: `yarn coverage:analyze` could not see uncommitted files (no PR). Focused Jest coverage on changed lines: usePerpsHomeActions 98.63% lines, depositConfirmationGuard 92.5% lines.

Overall recipe coverage: 2/2 ACs PROVEN (untestable: none, weak: 0, missing: 0)
