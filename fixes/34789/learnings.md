# Learnings — PR #34789 pr-complete

- Human review caught an API smell the prior pr-complete round introduced: extra `isResolved`/`isRawResolved` booleans on top of values that were still `'0'` or a stale snapshot. The ticket's own rule ("unknown, not zero") is better expressed as `undefined` on the existing properties.
- A measured zero (`'0'`) and an unknown balance must stay distinguishable. Returning the controller snapshot while unresolved forced every caller to consult a second flag; dropping the snapshot from the hook return made the type the gate.
- Raw units still land before the USD rate. After removing the flags, `balanceRaw !== undefined` with `balanceUsd === undefined` is the same split the fee-alert bugbot already required — do not collapse both fields to a single "resolved" check.
- Display callers (`pay-with-row`, `usePayWithPreferredToken`) still need a snapshot fallback for formatting. Keep that fallback at the call site, not inside the reactive hook, so alerts and order funding cannot treat it as known.
- Flaky-test detection on this PR was all 0/360 static pattern hits. The `setTimeout(0)` in `renderWithPayToken` is a documented rAF-mock flush, not a DOM wait — do not "fix" it into `waitFor('perps-order-header')` without checking why the flush exists.
