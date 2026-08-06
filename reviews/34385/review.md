# PR Review: #34385 — feat(perps): update mobile to latest perps controller version

**Reviewed commit:** `f506550989cedd3a7ec84d4296291a2b77c5998f`

**Tier:** light

## Summary

The PR cleanly adopts `@metamask/perps-controller` 11.0.0: it widens affected signatures, normalizes widened order types before indexing the two-bucket toast map, updates maker/taker classification through the controller's execution-mode helper, and supplies English translations for the expanded error-code union. The diff is aligned with its stated minimal-adoption goal, type-checks cleanly, and its focused tests pass. No blocking correctness issue was found in static review.

## Recipe Coverage

Skipped (tier: light). The operator explicitly limited this independent review to static analysis and prohibited creating or executing a recipe, device validation, browser validation, and evidence collection.

| # | Review claim | Status | Rationale |
|---|---|---|---|
| 1 | Then an "Order submitted" toast appears and the ETH position opens | UNTESTABLE | Requires a funded, unlocked Perps testnet session and live market-order placement; runtime/device validation was prohibited. |
| 2 | Then the order rests and appears in open orders | UNTESTABLE | Requires live limit-order placement and venue state; runtime/device validation was prohibited. |
| 3 | Then the position keeps its take profit and stop loss and remains open | UNTESTABLE | Requires an existing position and a live Auto close update; runtime/device validation was prohibited. |
| 4 | Then the position is closed and no longer listed | UNTESTABLE | Requires an existing position and a live close flow; runtime/device validation was prohibited. |

Overall recipe coverage: 0/4 ACs PROVEN

Untestable: AC1–AC4 — all require live Perps state and device interaction outside the operator-approved light/static tier.

The inherited implementation artifacts report successful live runs, but they are author-supplied context and were not treated as independent proof in this review.

## Prior Reviews

No prior reviews.

## PR Hygiene

No Jira or linked issue is provided. This review evaluates PR-author claims, not ticket-bound acceptance criteria.

The task context does link TAT-3687, but it supplies no numbered acceptance criteria; the four rows above are therefore verbatim PR-body review claims rather than ticket-bound criteria.

## Acceptance Criteria Validation

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Then an "Order submitted" toast appears and the ETH position opens | UNTESTABLE | Code review only — all changed toast sites normalize `OrderType` through `getTriggerExecution`; live placement was prohibited. |
| 2 | Then the order rests and appears in open orders | UNTESTABLE | Code review only — limit execution remains mapped to the limit toast/fee path; live placement was prohibited. |
| 3 | Then the position keeps its take profit and stop loss and remains open | UNTESTABLE | Code review only — the widened TP/SL form path type-checks; live position mutation was prohibited. |
| 4 | Then the position is closed and no longer listed | UNTESTABLE | Code review only — the widened close-position path type-checks; live closing was prohibited. |

## Code Quality

- Pattern adherence: Follows controller-owned helpers and existing Perps conventions; no duplicate local order-type normalization was introduced.
- Complexity: Appropriate and narrowly scoped for a dependency-major compatibility update.
- Type safety: Clean. The affected signatures use the controller's `OrderType`/`FeeCalculationParams`; no new `any` was introduced.
- Error handling: The 14 newly exposed controller codes are mapped, and the coverage test checks every exported code resolves to an English string.
- Accessibility/fallbacks: N/A. The diff adds no pressable UI and no new asynchronously populated displayed value; it changes toast-key selection and translation copy only.
- Anti-pattern findings: None. No controller portability violation, magic timing/precision value, provider-specific branch, telemetry regression, or new scaling-sensitive state path was introduced.
- File size: `PerpsOrderView.tsx` (2,408 lines) and `usePerpsOrderFees.test.ts` (2,149 lines) warrant non-blocking follow-up splits. The large locale registry and generated lockfile are not meaningfully splittable source modules.

## Fix Quality

- **Best approach:** Pragmatic and appropriate. Using `getTriggerExecution` and `isLimitExecutionOrderType` keeps execution semantics owned by the controller instead of reproducing its trigger-order sets in Mobile.
- **Would not ship:** None identified.
- **Test quality:** The focused tests assert concrete trigger-order maker/taker results and exhaustiveness of the installed controller's exported error-code set. The selected three suites pass 161/161. The four end-user flow claims remain independently untested under the light/static constraint.
- **Brittleness:** Low. The mappings derive from exported controller values/helpers rather than import-time snapshots or local duplicated constants. The unchanged binary UI branches are currently fed only by the market/limit selector or close-position toggle; no trigger-order value is reachable through those callers.

## Live Validation

- Recipe: skipped (tier: light)
- Result: SKIPPED — operator prohibited recipe/device/browser evidence work
- Video: skipped (tier: light)
- Native changes: none
- Metro errors: not assessed; runtime work was explicitly stopped
- Log monitoring: skipped (tier: light)

## Correctness

- Diff vs stated goal: Aligned. The package and lockfile resolve controller 11.0.0, all widened types compile, and new error codes have translations.
- Edge cases: Static coverage includes all six `OrderType` variants in execution-mode classification and all exported controller error codes. Live exchange behavior is untested in this review.
- Race conditions: None introduced by the diff; the changes are synchronous type normalization and static mapping updates.
- Backward compatibility: Existing market/limit semantics are preserved: `market` maps to market/taker and `limit` maps to limit/maker eligibility.

## Static Analysis

- lint:tsc: PASS — zero TypeScript errors.
- Tests: 161/161 pass across `usePerpsOrderFees.test.ts`, `orderUtils.test.ts`, and `translatePerpsErrorCoverage.test.ts`.
- Test-run note: Jest initially detected a pre-existing duplicate haste module under `temp/recipe/harness/mobile/backup-stale.20260611T131613Z`; the focused rerun excluded that unrelated backup path and passed.

## Architecture & Domain

The update preserves the controller/mobile boundary: Mobile imports controller types and semantic helpers, while provider-specific trigger-order classification remains outside UI code. Toast selection now deliberately collapses the six placement types into the existing market/limit execution buckets, matching controller 11.0.0. The expanded translations and exhaustive coverage test reduce the chance that a future controller error silently falls back to an unresolved key.

## Risk Assessment

- MEDIUM — the code delta is small, type-safe, and focused-test clean, but it adopts a major version in trading flows and the operator-approved review tier did not independently exercise live order placement, TP/SL updates, or closing.

## Recommended Action

APPROVE

No blocking finding was identified against published HEAD `f506550989cedd3a7ec84d4296291a2b77c5998f`. The two file-size comments are follow-up maintainability suggestions, not regressions caused by this PR.
