# TAT-3742 recipe coverage

The family-inherited recipe was re-run after the `origin/main` rebase and review fixes. It passed all 21 nodes in 52 seconds. The mixed/visual screenshot was read at original resolution; the state assertions were verified from the focused Jest command and exit-code assertion.

| AC | Proof mode | Evidence | Verdict |
|---|---|---|---|
| Clean up pay-with-token funding errors without reporting an unmeasured zero balance | mixed | `ac1-assert-no-perps-balance-warning`, `ac1-assert-no-zero-available-row`, and `recipe-run/screenshots/evidence-ac1-after-payment-switch.png` | PROVEN |
| Keep the Place Order CTA in the viewport after switching payment methods | visual | `ac2-assert-action-button-visible`, `ac2-assert-button-still-visible`, and the inspected screenshot | PROVEN |
| Keep the slider usable while the selected token balance is unresolved | state | `ac3-ac4-run-funding-state-tests` and `ac3-ac4-assert-funding-state-tests` | PROVEN |
| Show the protocol minimum state once a resolved pay-token balance cannot reach $10 | state | The focused `pay with token funding state` tests executed by the recipe | PROVEN |

Overall coverage: **4/4 ACs proven** (weak: 0, missing: 0).
