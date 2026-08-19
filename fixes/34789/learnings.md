# Review-driven learnings

- A fallback can be numerically harmless but account-incorrect: `payToken.balanceUsd` and `selectedToken.balanceUsd` are snapshots from the original transaction context, so they must not backfill an override-aware live-balance hook.
- Unknown live balances need surface-specific behavior. Display-only rows can render zero, while the Perps trade screen should suppress false insufficiency copy and independently keep its CTA disabled through `isPayBalanceLoading`.
- Reviewer questions should be traced through the consuming CTA before changing shared alert semantics; the existing two-variant Place Order guard and focused unresolved-balance test showed that the alert comment was already covered.
- A strict changed-file lint gate can surface pre-existing warnings in an otherwise minimal fix. Migrating the four local legacy `Box` usages kept the touched file at zero warnings without changing layout behavior.
