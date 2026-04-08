# PR Review: #28511 — fix(perps): show standard Order submitted toast for pay-with-any-token flow

**Tier:** standard

## Summary

The PR removes a conditional branch in `PerpsOrderView.handlePlaceOrder` that showed different toasts depending on payment method. Previously, pay-with-any-token orders showed a persistent "Submitting your trade" toast, while perps-balance orders showed a standard "Order submitted" toast. Now both flows show the same standard "Order submitted" toast with direction, size, and asset details.

The change achieves its stated goal. The deposit progress is still tracked separately by `usePerpsDepositStatus` which shows its own `deposit.inProgress` toast, so users still get feedback during the deposit phase.

## Prior Reviews

No prior reviews.

## Acceptance Criteria Validation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Pay-with-any-token flow shows standard "Order submitted" toast | PASS | Code review: conditional removed, `submitted()` called unconditionally (line 1087-1092) |
| 2 | Persistent "Submitting your trade" toast is not shown | PASS | Code review: `shared.submitting()` call removed from `handlePlaceOrder` |
| 3 | Perps balance flow shows standard "Order submitted" toast | PASS | Code review + test: behavior unchanged for perps balance path |

## Code Quality

- Pattern adherence: Follows codebase conventions. Uses existing `PerpsToastOptions` constants.
- Complexity: Reduces complexity — removes a conditional branch.
- Type safety: No type issues. TypeScript compilation passes for these files.
- Error handling: Not affected — error path untouched.
- Anti-pattern findings: None. No magic strings/numbers, no controller portability issues.

## Fix Quality

- **Best approach:** This is the simplest correct fix. The `submitting` toast was redundant because `usePerpsDepositStatus` already handles deposit progress with its own `deposit.inProgress` toast. Removing the duplicate initial toast is cleaner than trying to fix its persistence behavior.
- **Would not ship:** Nothing blocking.
- **Test quality:** Tests are updated correctly. The custom-token test now asserts `mockSubmitted` is called (was `mockSubmitting`). The perps-balance test removes the now-redundant negative assertion (`mockSubmitting` not called). Both tests verify `mockShowToast` was called, then check the correct toast factory was invoked. Tests would fail if the fix were reverted (the `submitted` call wouldn't happen for custom token path).
- **Brittleness:** None. The change removes a conditional, which reduces possible failure modes.

## Live Validation

- Recipe: skipped (tier: standard)
- Result: PASS — app stable on Perps screen, no errors
- Video: review.mp4
- Native changes: none
- Metro errors: none related to PR (pre-existing keychain warnings only)
- Log monitoring: 30s monitored, no errors or warnings related to Perps order flow

## Correctness

- Diff vs stated goal: Aligned — removes conditional toast, uses standard toast for all flows.
- Edge cases: The `submitting()` toast function in `usePerpsToasts.tsx` is now dead code (only its definition and toast-level test remain). Not a correctness issue but could be cleaned up.
- Race conditions: None. Toast is shown synchronously before async order execution.
- Backward compatibility: Preserved. The deposit progress toast (`usePerpsDepositStatus`) is unaffected.

## Static Analysis

- lint:tsc: PASS — no new type errors (all errors are pre-existing in unrelated files)
- Tests: 90/90 pass

## Architecture & Domain

Minimal change. No architectural implications. The `shared.submitting` toast definition becomes dead code — a follow-up cleanup could remove it from `usePerpsToasts.tsx` along with its test, but this is minor.

## Risk Assessment

- LOW — Removes a conditional UI branch in toast display. No impact on order execution, deposits, or funds handling. The deposit progress tracking (`usePerpsDepositStatus`) is completely independent.

## Recommended Action

APPROVE

The fix is clean, minimal, and well-tested. The only minor item is the now-unused `submitting` toast definition in `usePerpsToasts.tsx`, noted as a nitpick.
