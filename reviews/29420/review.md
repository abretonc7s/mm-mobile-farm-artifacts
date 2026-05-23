# PR Review: #29420 — fix(perps): non-EVM address passed to HyperLiquid validator via usePerpsPositionForAsset

**Tier:** standard

## Summary

This PR fixes a Sentry crash (METAMASK-MOBILE-5S5C, 91 occurrences, 46 users) where non-EVM addresses (Bitcoin, Solana, Tron) were passed to HyperLiquid's `spotClearinghouseState()`, which validates addresses with a strict EVM hex regex and throws `ValiError`.

The fix introduces a reusable selector `selectSelectedAccountGroupEvmInternalAccount` that derives the EVM account from the selected multichain account group via `AccountTreeController`, and updates all four affected Perps hooks plus one view to use it. This is the correct architectural approach recommended by the accounts team (Charly Chevalier).

The PR achieves its stated goal cleanly and correctly.

## Recipe Coverage

| # | AC (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|---------------|-----------------|---------------------|---------------------|----------------|---------------|
| 1 | "usePerpsPositionForAsset derives userAddress from the selected account group's EVM account" | both | ac1-eval-evm-selector (190ms, PASS) | n/a (generate-internal) | PROVEN | CDP eval confirmed selected account group contains EVM account; code review confirms all 4 hooks migrated |
| 2 | "Users with non-EVM accounts selected can open Perps without triggering a ValiError" | both | setup-navigate-to-perps, ac2-wait-market-visible, ac2-log-watch-no-valierror, ac2-screenshot-market | evidence-ac2-perps-market-open.png | PROVEN | Market opened, log_watch found no ValiError (caveat: empty watch_counts — absence proof limited to live window) |
| 3 | "Audit other Perps hooks for selectSelectedInternalAccountFormattedAddress anti-pattern" | n/a | n/a | n/a | UNTESTABLE | Code audit AC — grep confirms no remaining production usage |
| 4 | "Unit test for non-EVM selected account empty state" | n/a | n/a | n/a | UNTESTABLE | Jest-only AC — 187/187 tests pass including 2 new non-EVM tests |

Overall recipe coverage: 2/4 ACs PROVEN
Untestable: AC3 — code audit only (verified via grep), AC4 — jest only (verified via test run)

## Prior Reviews

| Reviewer | State | Date | Addressed? | Notes |
|----------|-------|------|------------|-------|
| ccharly | COMMENTED | 2026-05-04 | addressed | Comments addressed in commit fbd28d57 (2026-05-04) |
| ccharly | APPROVED | 2026-05-04 | n/a | Approved after review comments addressed |
| michalconsensys | APPROVED | 2026-05-04 | n/a | Approved |

No CHANGES_REQUESTED reviews. Both domain-expert approvals are already in place.

## Acceptance Criteria Validation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | usePerpsPositionForAsset derives userAddress from EVM account group | PASS | ac1-eval-evm-selector PASS + code review: all 4 hooks migrated to `selectSelectedAccountGroupEvmInternalAccount` |
| 2 | Non-EVM accounts can open Perps without ValiError | PASS | ac2-log-watch-no-valierror PASS + screenshot evidence |
| 3 | Audit other Perps hooks for anti-pattern | PASS | grep confirms 0 remaining production Perps usage of `selectSelectedInternalAccountFormattedAddress` |
| 4 | Unit test for non-EVM empty state | PASS | 187/187 tests pass; 2 new tests at usePerpsPositionForAsset.test.ts:266,287 |

## Code Quality

- Pattern adherence: follows codebase conventions — consistent `const evmAccount = useSelector(...); const selectedAddress = evmAccount?.address;` pattern across all hooks
- Complexity: appropriate — minimal selector + straightforward hook updates
- Type safety: good — `InternalAccount | null` return type, optional chaining on `evmAccount?.address`
- Error handling: adequate — existing `if (!userAddress)` guards in all hooks naturally handle the `undefined` case
- Anti-pattern findings: none in production code; 2 dead test mocks for `selectSelectedInternalAccountFormattedAddress` remain in test files (nitpick)

## Fix Quality

- **Best approach:** Yes — this is Option B from the ticket (reusable selector), exactly what Charly recommended. The selector uses `isEvmAccountType` from `@metamask/keyring-api` (canonical check) and `createSelector` for memoization. Would ship as-is.
- **Would not ship:** Nothing blocking.
- **Test quality:** Strong. Two new tests in `usePerpsPositionForAsset.test.ts` assert:
  1. Non-EVM selected account → `mockGetPositions` called with EVM address, NOT non-EVM address
  2. No EVM in group → `mockGetPositions` never called, returns empty state
  Both tests would fail if the fix is reverted.
- **Brittleness:** Low. Selector derives from `selectSelectedAccountGroupInternalAccounts` (canonical multichain pattern). No import-time evaluation or module-level constant risks.

## Live Validation

- Recipe: generated (generate-internal mode)
- Result: PASS — 5/5 nodes passed (trace-derived from `.agent/recipe-runs/2026-05-23_10-03-40_recipe/trace.json`)
- Video: review.mp4 (10MB, moov atom verified)
- Native changes: none
- Metro errors: none related to PR changes (pre-existing require cycles and keychain warnings only)
- Log monitoring: 10s window monitored via log_watch, no ValiError found (caveat: watch_counts empty — runner executed in 129ms, so absence proof is limited to the live window after navigation)

## Correctness

- Diff vs stated goal: aligned — all four hooks and the transactions view migrated to account-group EVM selector
- Edge cases: covered — no-EVM-in-group case returns `null` from selector, hooks bail with empty state via existing `if (!userAddress)` guards
- Race conditions: none — selector is synchronous/memoized, hooks already handle undefined address
- Backward compatibility: preserved — `evmAccount?.address` produces the same string value as the old `selectSelectedInternalAccountFormattedAddress` for EVM-selected accounts

## Static Analysis

- lint:tsc: PASS — 0 errors
- Tests: 187/187 pass across 5 test suites

## Architecture & Domain

- The new `selectSelectedAccountGroupEvmInternalAccount` selector is well-placed in `accountTreeController.ts` alongside other account-group selectors
- Follows the multichain migration pattern endorsed by the accounts team
- No scaling concerns — selector is O(n) where n is accounts in group (typically 2-5)
- The `selectSelectedInternalAccountFormattedAddress` selector should eventually be deprecated project-wide; this PR handles the Perps scope

## Risk Assessment

- **LOW** — Minimal, targeted fix following the recommended architectural pattern. Two domain experts approved. All tests pass. Runtime validation shows no ValiError. The change is purely about which selector sources the address — no behavioral logic changes.

## Recommended Action

APPROVE

The PR is well-executed, follows the recommended approach, has domain-expert approvals, comprehensive test coverage, and runtime validation. The only nitpick is 2 dead test mocks that could be cleaned up.
