# PR Review: #28318 — fix(perps): block Place Order when relay quote reveals insufficient pay token balance

**Tier:** light

## Summary
The PR correctly bridges the perps custom "pay with any token" flow with the standard confirmation alert system by importing `useInsufficientPayTokenBalanceAlert` and `useNoPayTokenQuotesAlert` directly into `PerpsOrderViewContentBase`. When either hook returns a blocking alert, the Place Order button is disabled and the first alert message is shown in red above the button. This addresses frequent on-chain failures (~50% "insufficient funds" errors per Mixpanel) caused by the margin-only validation missing relay quote fee totals.

## Prior Reviews
No prior reviews (only Cursor bot automated comments).

## Acceptance Criteria Validation
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Place Order disabled when relay quote exceeds token balance | PASS | Code review: `hasBlockingPayAlerts` added to both button `isDisabled` conditions; `useInsufficientPayTokenBalanceAlert` returns blocking alert when total > balance |
| 2 | Place Order enabled when balance is sufficient | PASS | Code review: hooks return `[]` when conditions pass, `hasBlockingPayAlerts` is false |
| 3 | Place Order disabled when no relay quotes available | PASS | Code review: `useNoPayTokenQuotesAlert` returns blocking alert when quotes empty |
| 4 | Red error message displayed above button | PASS | Code review: `blockingPayAlertMessage` rendered in `TextColor.Error` inside `validationContainer` |

## Code Quality
- **Pattern adherence:** Follows existing validation pattern — uses same `styles.validationContainer` and `TextVariant.BodySM`/`TextColor.Error` as other validation messages in the component.
- **Complexity:** Appropriate — minimal code to achieve the goal.
- **Type safety:** Clean. `useInsufficientPayTokenBalanceAlert` accepts optional `{ pendingAmountUsd?: string }` defaulting to `{}`; calling with no args is correct for this use case.
- **Error handling:** Adequate — hooks gracefully return `[]` when conditions aren't met.
- **Anti-pattern findings:** None. No magic strings, no controller portability issues, no missing event tracking needed.

## Context Provider Safety
Verified that both hooks work safely outside `AlertsContextProvider`:
- `useNoPayTokenQuotesAlert` — purely Redux-based, no context dependencies.
- `useInsufficientPayTokenBalanceAlert` — uses `useTransactionMetadataRequest` which calls `useGasFeeModalTransaction()`. Verified that this context returns safe defaults (`{ transactionId: null }`) when no provider is present (`gas-fee-modal-transaction.tsx:44`). No crash risk.

## Live Validation
- Recipe: skipped (tier: light)
- Result: SKIPPED
- Video: skipped (tier: light)
- Native changes: none
- Metro errors: skipped (tier: light)
- Log monitoring: skipped (tier: light)

## Correctness
- **Diff vs stated goal:** Aligned — precisely addresses the gap between margin-only validation and relay quote total validation.
- **Edge cases:** The `hasBlockingPayAlerts` check runs unconditionally (not gated by `hasCustomTokenSelected`). However, both hooks rely on Redux pay token state which is only populated when a custom token is selected, so they return `[]` for Perps balance flow. This is correct behavior.
- **Race conditions:** None — hooks are reactive to Redux state changes, same pattern as existing validation.
- **Backward compatibility:** Preserved — adds stricter validation without removing existing checks.

## Static Analysis
- lint:tsc: PASS (0 errors)
- Tests: 88/88 pass

## Architecture & Domain
- The approach of calling individual alert hooks rather than the full `useConfirmationAlerts` aggregate is pragmatic — it avoids pulling in 13+ unrelated alert hooks and keeps the dependency surface minimal.
- PerpsOrderView.tsx is at 1,997 lines (approaching 2,000 threshold). Pre-existing concern, not caused by this PR (+37 net lines).
- PerpsOrderView.test.tsx is at 3,848 lines (exceeds 2,500 hard limit). Pre-existing — this PR only adds 14 mock lines. Not blocking this PR but should be tracked.

## Risk Assessment
- **LOW** — Additive validation that disables the button under stricter conditions. Hooks return `[]` by default, so the change is no-op when pay token state is empty (standard Perps balance flow). Both button variants updated consistently.

## Recommended Action
**APPROVE**
Clean, focused fix. Test mocks ensure existing tests aren't broken, though no new tests exercise the blocking alert behavior directly (the mocks return `[]`). This is acceptable for a light review — the hooks themselves are tested in the confirmations domain.
