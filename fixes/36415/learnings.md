# Learnings — PR #36415 review round

- **A defensive dedupe was added where no key could be safe.** `flattenFills` keyed on `orderId + timestamp + size + price` to mirror the `flattenPages` pattern next to it, but the provider does not guarantee those four values identify an execution, and only page 0 ever carries fills — so the dedupe protected nothing and could silently drop real trades. Copying a neighbouring function's shape is not a reason to add data-loss logic; check first whether duplicates are even reachable.

- **Index-based ids survive review only while the list is append-only.** `${orderId}-${timestamp}-${acc.length}` was inherited from `main` and extended to individual fills without asking what happens when history grows at the front. Any id handed to another screen (Activity Details) or used as a list key has to be derived from the row's own content, not its position.

- **The provider-neutral model was the real constraint, and it should have been stated up front.** `OrderFill` cannot carry HyperLiquid's `tid`, so exposing individual executions was always going to need a derived id. Naming that limitation in the PR description would have framed the id scheme as a known trade-off instead of an oversight the reviewer had to find.

- **Accessibility semantics were traded away for 6px of visual fidelity.** `ButtonBase` was chosen for the pill look, and the code comment acknowledged it could not express `accessibilityRole="checkbox"` — then shipped anyway with `accessibilityState.checked` alone. When a design-system primitive exists for the exact control, start there and style it; take the visual delta to the designer rather than dropping the semantic contract silently.

- **Tests asserted the prop, not the contract.** The original checkbox tests read back `accessibilityState` — the literal value the component had just set — which cannot fail for the reason that mattered. Assertions should name the behaviour a user or screen reader depends on. Every regression test added this round was verified to fail against the pre-fix code before being kept.
