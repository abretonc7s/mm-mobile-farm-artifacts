# PR Review: #28897 — fix(perps): use live price for reverse position orders

**Tier:** full

## Summary

PR removes stale `currentPrice` (position `entryPrice`) from `flipPosition()` order params so `HyperLiquidProvider.placeOrder` fetches live market price via `#getAssetInfo` instead. Also removes the redundant client-side fee pre-validation and updates analytics to use executed average price. The fix is minimal, targeted, and correct.

## Recipe Coverage

| # | AC (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|---------------|-----------------|---------------------|---------------------|----------------|---------------|
| 1 | "the order is submitted successfully" — reverse position order submits without stale entry pricing as currentPrice | both | ac1-verify-controller-exists, ac1-screenshot-perps-screen | evidence-ac1-perps-screen.png | UNTESTABLE | Internal placeOrder args not observable via CDP. No flip-position flow exists. Proven by unit test `does not pass entry price as currentPrice to the provider` (TradingService.test.ts:2045) + code review of TradingService.ts:1950 showing currentPrice absent from OrderParams. |
| 2 | "the reverse order does not fail because of stale entry pricing" — flipPosition does not pass currentPrice to provider | both | ac2-verify-positions-state, ac2-screenshot-positions | evidence-ac2-positions-state.png | UNTESTABLE | Same as AC1 — the assertion is about internal method parameters passed to provider.placeOrder, not observable UI state. Unit test uses exact match + negative assertion to prove currentPrice is never sent. |
| 3 | Analytics order_value uses executed average price (falling back to entry price if missing) | both | ac3-verify-balances, ac3-screenshot-balances | evidence-ac3-balances.png | UNTESTABLE | Analytics event properties not observable via CDP. Proven by unit test `tracks analytics on success` asserting order_value: 30000 (0.5 * 60000 averagePrice). |
| 4 | "the tests pass" — unit tests pass for flipPosition regression coverage | N/A | N/A (jest, not recipe) | N/A | PROVEN | 73/73 tests pass including all flipPosition tests. Direct jest execution confirms. |

Overall recipe coverage: 1/4 ACs PROVEN
Untestable: AC1, AC2, AC3 — internal method params and analytics event properties not observable via CDP or UI. All three fully proven by unit tests and code review.

> **Coverage escalation note:** AC1-3 are not proven on device because the fix targets internal method parameters (`placeOrder` args) and analytics event properties — neither of which have a UI or CDP-observable surface. Unit tests provide definitive proof: the new test `does not pass entry price as currentPrice to the provider` uses exact match AND negative assertion, and would FAIL if the fix is reverted. Human reviewer should confirm test correctness at TradingService.test.ts:2045-2071.

## Prior Reviews

| Reviewer | State | Date | Addressed? | Notes |
|----------|-------|------|------------|-------|
| cursor | COMMENTED | 2026-04-16 | N/A | Automated Bugbot review — summary only, no actionable requests |

No prior human reviews.

## Acceptance Criteria Validation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Reverse position order submits without stale pricing | PASS | Code review: `currentPrice` removed from OrderParams (TradingService.ts:1950-1956). Unit test: exact match assertion (TradingService.test.ts:2060-2071). |
| 2 | flipPosition does not pass currentPrice to provider | PASS | Unit test: `not.toHaveBeenCalledWith(expect.objectContaining({currentPrice: expect.any(Number)}))` (TradingService.test.ts:2067-2071). |
| 3 | Analytics order_value uses executed average price | PASS | Code: `result.averagePrice ?? position.entryPrice` (TradingService.ts:1963-1965). Unit test: averagePrice=60000, positionSize=0.5, asserts order_value=30000 (TradingService.test.ts:2109). |
| 4 | Unit tests pass for flipPosition | PASS | 73/73 tests pass. All 9 flipPosition tests green. |

## Code Quality

- **Pattern adherence:** Follows codebase conventions. Uses `PERPS_EVENT_PROPERTY`/`PERPS_EVENT_VALUE` constants. Provider-agnostic order placement.
- **Complexity:** Appropriate — removes complexity (fee pre-validation) rather than adding it.
- **Type safety:** `currentPrice` is optional on `OrderParams` (types/index.ts:165), so omitting it is type-safe. No new type issues.
- **Error handling:** Provider-side validation preserved. Removed client-side fee check was redundant.
- **Anti-pattern findings:** None. No magic strings, no controller portability violations, no WS subscription leaks.

## Fix Quality

- **Best approach:** Yes — this is the minimal, most correct fix. The provider already fetches live price via `#getAssetInfo` (HyperLiquidProvider.ts:3399). Passing `currentPrice` was an optimization hint that backfired when `entryPrice` diverged from market. Removing it lets the provider do what it's designed to do.
- **Would not ship:** Nothing. Clean fix.
- **Test quality:** Strong. New test uses exact object match (`toHaveBeenCalledWith({...})`) not partial, AND negative assertion (`not.toHaveBeenCalledWith(expect.objectContaining({currentPrice}))`). Analytics test verifies correct math with concrete values. Removed tests were for deleted fee-validation logic — appropriate.
- **Brittleness:** None. No import-time evaluation, no mock coupling, no frozen constants. The fix is structurally simple — removing a field from an object literal.

## Live Validation

- Recipe: generated (smoke test — system health + controller verification)
- Result: PASS — 10/10 recipe nodes passed. Core ACs untestable via recipe (internal params).
- Video: review.mp4 (6s, perps system health)
- Native changes: none
- Metro errors: none related to PR. Pre-existing: keychain warnings, transient network errors.
- Log monitoring: metro.log scanned, no perps-specific errors.

## Correctness

- **Diff vs stated goal:** Aligned. PR removes stale `currentPrice` from flip order params, exactly as described.
- **Edge cases:**
  - `result.averagePrice` missing → falls back to `position.entryPrice` (TradingService.ts:1963-1965). Reasonable fallback.
  - Provider receives no `currentPrice` → fetches live price via `#getAssetInfo` (HyperLiquidProvider.ts:3399-3408). Correct behavior.
- **Race conditions:** None. The provider's `#getAssetInfo` fetches price synchronously within the `placeOrder` call.
- **Backward compatibility:** Preserved. `currentPrice` is optional on `OrderParams`. No external API changes.

## Static Analysis

- lint:tsc: PASS — 0 errors
- Tests: 73/73 pass (TradingService.test.ts)

## Architecture & Domain

- Removing client-side fee pre-validation is a net positive — it was duplicating provider-side validation with less accurate data.
- File sizes: TradingService.ts (2,042 lines) and TradingService.test.ts (2,184 lines) are both above 2,000-line suggestion threshold, but this PR reduces both files. Existing tech debt, not introduced by this PR.

## Risk Assessment

- **LOW** — Small, targeted removal of a field from an object literal. Provider already handles the missing-`currentPrice` case correctly. Well-tested with revert-proof assertions.

## Recommended Action

**APPROVE** — Clean, minimal fix with strong test coverage. No blockers.
