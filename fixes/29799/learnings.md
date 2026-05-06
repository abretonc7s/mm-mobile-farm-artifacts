# Learnings — TAT-3094

1. **`PRICE_RANGES_MINIMAL_VIEW` is for USD amounts, `PRICE_RANGES_UNIVERSAL` is for market prices.** When formatting trigger/limit/TP/SL prices, always use `PRICE_RANGES_UNIVERSAL`. `MINIMAL_VIEW` caps at 2 decimals — appropriate for position value, margin, PnL, but not for prices that need market-appropriate precision.

2. **Jest mock factories execute before `const` declarations.** When using `jest.mock()` with a factory function, any `const` declared outside the mock at module scope is `undefined` inside the factory due to hoisting. Inline values directly in the factory or use `jest.requireMock()` in the test body.

3. **iOS Simulator video recording fails in headless mode.** `xcrun simctl io recordVideo` requires a visible simulator window. On headless CI or remote machines, use screenshot-based evidence or `record-window.sh` fallback.

4. **Position-level TP/SL orders have `isPositionTpsl: true` and are filtered from the Market Details Orders section.** When designing recipes for order display bugs, verify which orders actually appear in compact rows vs. only in expanded cards.

5. **Cross-reference expanded vs. compact components early.** The expanded card (`PerpsOpenOrderCard`) already used the correct range — comparing both components immediately would have confirmed the fix pattern in under a minute.
