# Recipe Coverage Matrix

| # | AC (verbatim) | Proof mode | Primary evidence | Recipe nodes (IDs) | Visual file if any | Evidence verdict | Justification |
|---|---------------|------------|------------------|---------------------|--------------------|------------------|---------------|
| 1 | Compact order rows display trigger/limit price with market-appropriate decimals instead of fixed 2 decimals | state | state (eval_async + unit test) | ac1-eval-orders-exist, ac1-assert-btc-price-range, ac1-screenshot-market | after-ac1-market-details.png | PROVEN | eval_async confirms BTC orders have triggerPrice > 10000, unit test asserts formatPerpsFiat called with PRICE_RANGES_UNIVERSAL. Code diff shows MINIMAL_VIEW→UNIVERSAL swap. |
| 2 | Expanded order card detail view continues to display trigger/limit price correctly (no regression) | state | state (eval_async + code review) | ac2-eval-expanded-uses-universal | n/a | PROVEN | eval_async confirms order data available with correct prices. PerpsOpenOrderCard.tsx already uses PRICE_RANGES_UNIVERSAL (lines 291-326) — no change needed, no regression possible. |

Overall recipe coverage: 2/2 ACs PROVEN (untestable: none, weak: 0, missing: 0)
