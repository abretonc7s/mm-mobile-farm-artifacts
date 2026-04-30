# PR Review: #29420 — fix(perps): [Perps] ValiError: non-EVM address passed to HyperLiquid validator via usePerpsPositionForAsset

**Tier:** standard

## Summary
This PR fixes a Sentry-tracked crash (METAMASK-MOBILE-5S5C, 91 occurrences, 46 users) where non-EVM addresses (Bitcoin, Solana, Tron) were passed to HyperLiquid's strict EVM address validator, causing a ValiError. The fix introduces a reusable selector `selectSelectedAccountGroupEvmInternalAccount` that derives the EVM account from the selected account group (via `AccountTreeController`), replacing the old `selectSelectedInternalAccountFormattedAddress` pattern across all 4 affected Perps hooks and 1 view. The fix is correct, minimal, and follows the approach recommended by the accounts team (Charly Chevalier).

## Recipe Coverage

| # | AC (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|---------------|-----------------|---------------------|---------------------|----------------|---------------|
| 1 | "usePerpsPositionForAsset derives userAddress from the selected account group's EVM account, not from AccountsController.state.selectedAccount" | both | ac1-assert-selected-group-evm, ac1-screenshot-selected-group-evm | evidence-ac1-selected-group-evm.png | PROVEN | CDP eval confirmed EVM account (0x8dc6...) in selected group while Solana account was selected. Code review + unit tests confirm selector migration. |
| 2 | "Users with Bitcoin, Solana, or Tron accounts selected can open the Perps Trending view without triggering a ValiError" | both | setup-select-non-evm-account, setup-assert-selected-account-non-evm, setup-open-btc-market, ac2-assert-market-visible, ac2-assert-no-valierror, ac2-screenshot-market-visible | evidence-ac2-perps-market-visible.png | PROVEN | Solana account selected, navigated to Perps market details, no ValiError in logs, market view rendered with price data ($76,051). |
| 3 | "Audit other Perps hooks for the same selectSelectedInternalAccountFormattedAddress anti-pattern and fix accordingly" | both | ac3-assert-perps-hooks-audited, ac3-screenshot-audit-surface | evidence-ac3-perps-audit-surface.png | PROVEN | All 4 Perps hooks/views migrated. grep confirms zero remaining production usages. |
| 4 | "Unit test: hook correctly returns no position data (rather than throwing) when the selected account is non-EVM" | both | ac4-assert-no-position-error-state, ac4-screenshot-no-position-error-state | evidence-ac4-no-position-error-state.png | PROVEN | 184/184 tests pass. Two new test cases cover non-EVM and no-EVM-in-group. |

Overall recipe coverage: 4/4 ACs PROVEN
Untestable: none

## Prior Reviews
No prior reviews.

## Acceptance Criteria Validation
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | usePerpsPositionForAsset derives userAddress from EVM account group | PASS | Code review: selector changed at usePerpsPositionForAsset.ts:92-93. CDP eval confirmed EVM address resolution. |
| 2 | Non-EVM accounts can open Perps without ValiError | PASS | Recipe: Solana account selected, Perps market loaded, no ValiError in 8s log window. |
| 3 | Audit other Perps hooks for anti-pattern | PASS | All 4 hooks + 1 view migrated. grep confirms zero remaining production usages in Perps. |
| 4 | Unit test for non-EVM empty state | PASS | Two new test cases added. 184/184 tests pass. |

## Code Quality
- Pattern adherence: Follows codebase conventions. Uses `createSelector` from reselect, `isEvmAccountType` from `@metamask/keyring-api`.
- Complexity: Appropriate — minimal selector, consistent pattern across all consumers.
- Type safety: Clean. Selector returns `InternalAccount | null`, consumers use optional chaining (`evmAccount?.address`).
- Error handling: Adequate — hooks bail out cleanly when `userAddress` is undefined.
- Anti-pattern findings: Dead mock for `selectSelectedInternalAccountFormattedAddress` remains in `usePerpsOrderFees.test.ts:32-35` (harmless but unnecessary).

## Fix Quality
- **Best approach:** Yes. This is Option B from the ticket (Charly's recommendation) — a reusable selector. It's the right level of abstraction: one selector, multiple consumers.
- **Would not ship:** Nothing blocking. Clean fix.
- **Test quality:** Good. Tests assert specific behaviors: (1) non-EVM selected account still calls API with EVM address, (2) no-EVM-in-group returns empty state and skips API calls, (3) test fixtures properly set up `AccountTreeController` state. Reverting the fix would cause test failures.
- **Brittleness:** Low. Depends on stable `AccountTreeController` API and `isEvmAccountType` from keyring-api.

## Live Validation
- Recipe: existed (included in PR body), re-run by reviewer
- Result: PASS — 12/12 nodes passed
- Video: skipped (iOS simulator recording failed — SimRenderServer error, same issue PR author encountered)
- Native changes: none
- Metro errors: none related to PR (pre-existing keychain warnings only)
- Log monitoring: 8s log watch during recipe, no ValiError or related errors

## Correctness
- Diff vs stated goal: Aligned — all 4 hooks and 1 view migrated from old selector to new account-group-based selector.
- Edge cases: Covered — no-EVM-in-group edge case handled (returns empty state). Case-insensitive symbol matching preserved.
- Race conditions: None introduced. Existing request-id and mounted-ref patterns preserved.
- Backward compatibility: Preserved — the new selector returns `InternalAccount | null`, and `?.address` produces the same `string | undefined` type as before.

## Static Analysis
- lint:tsc: PASS — 0 errors
- Tests: 184/184 pass (5 test suites)

## Architecture & Domain
- Follows the multichain account group architecture recommended by the accounts team.
- `selectSelectedAccountGroupEvmInternalAccount` is properly placed in `accountTreeController.ts` alongside related selectors.
- No protocol abstraction violations — the fix is provider-agnostic.
- No new screens, so no MetaMetrics/Sentry tracking needed.

## Risk Assessment
- LOW — Minimal, targeted fix. Changes are mechanical (selector swap) with proper test coverage. The new selector is narrowly scoped and well-typed. Live validation confirms no regressions.

## Recommended Action
APPROVE
- One minor nitpick: dead mock in `usePerpsOrderFees.test.ts` for old selector (lines 32-35) could be removed.
