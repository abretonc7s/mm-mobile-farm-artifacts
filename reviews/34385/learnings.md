# Review Learnings

- Perps-controller 11.0.0 expands `OrderType` to six placement types, while `getTriggerExecution` intentionally reduces them to the two execution buckets (`market` and `limit`) understood by existing Mobile toast and fee code.
- `isLimitExecutionOrderType` is the controller-owned source of truth for limit-execution behavior; using it avoids duplicating trigger-type lists in Mobile.
- The remaining direct market/limit branches are currently protected by their callers: the order selector and close-position toggle expose only those two choices, even though shared signatures now accept the wider controller type.
- Error translation coverage is strongest when it enumerates the installed controller's exported `PerpsErrorCode` values and verifies both a mapping and resolved English copy, so future dependency additions fail the test.
- Focused Jest runs can encounter an unrelated haste collision from `temp/recipe/harness/mobile/backup-stale.20260611T131613Z`; excluding that backup path isolates the affected suites without changing application code.
- No CDP, recipe, simulator, browser, or screenshot timing observation was collected because the operator changed the review to light/static and explicitly prohibited those validation surfaces.
- The four end-user Perps claims require funded testnet state and are therefore UNTESTABLE within this review tier, even though type checking and focused unit behavior can still be proven statically.
- `PerpsOrderView.tsx` and `usePerpsOrderFees.test.ts` are already above the 2,000-line advisory threshold; future work should favor extracting focused submission/toast logic and behavior-specific test suites.
- Localization registries and generated lockfiles need explicit interpretation when applying a source-file size guardrail; splitting either would conflict with their repository/tooling role.
