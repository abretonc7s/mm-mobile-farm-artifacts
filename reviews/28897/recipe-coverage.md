# Recipe Coverage Matrix — PR #28897

| # | AC (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|---------------|-----------------|---------------------|---------------------|----------------|---------------|
| 1 | "the order is submitted successfully" — reverse position order submits without stale entry pricing as currentPrice | both | ac1-verify-controller-exists, ac1-screenshot-perps-screen | evidence-ac1-perps-screen.png | UNTESTABLE | Internal placeOrder args not observable via CDP. No flip-position flow exists. Proven by unit test `does not pass entry price as currentPrice to the provider` (TradingService.test.ts:2045) + code review of TradingService.ts:1950 showing currentPrice absent from OrderParams. |
| 2 | "the reverse order does not fail because of stale entry pricing" — flipPosition does not pass currentPrice to provider | both | ac2-verify-positions-state, ac2-screenshot-positions | evidence-ac2-positions-state.png | UNTESTABLE | Same as AC1 — the assertion is about internal method parameters passed to provider.placeOrder, not observable UI state. Unit test uses exact match + negative assertion to prove currentPrice is never sent. |
| 3 | Analytics order_value uses executed average price (falling back to entry price if missing) | both | ac3-verify-balances, ac3-screenshot-balances | evidence-ac3-balances.png | UNTESTABLE | Analytics event properties not observable via CDP. Proven by unit test `tracks analytics on success` asserting order_value: 30000 (0.5 * 60000 averagePrice). |
| 4 | "the tests pass" — unit tests pass for flipPosition regression coverage | N/A | N/A (jest, not recipe) | N/A | PROVEN | 73/73 tests pass including all flipPosition tests. Direct jest execution confirms. |

Overall recipe coverage: 1/4 ACs PROVEN (untestable: AC1, AC2, AC3 — internal method params and analytics not observable via CDP; weak: 0; missing: 0)
