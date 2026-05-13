# PR Review: #29817 — fix: handle update position tpsl error handling, dedupe flipPosition trace

**Tier:** standard

## Summary

This PR closes three Sentry observability gaps in the Perps TradingService:

1. Adds missing `logger.error` in `updatePositionTPSL`'s catch block — previously set traceData and rethrew but never logged to Sentry.
2. Removes duplicate `Logger.error` from `usePerpsFlipPosition` UI hook — the controller already reports to Sentry on flip failures; the hook was double-reporting.
3. Adds `logger.error` for non-throwing failure paths (`{success: false}` results) in `cancelOrder`, `closePosition`, `cancelOrders`, and `closePositions` — these were silently swallowed.

All three claims are verified by code review and unit tests. The changes achieve their stated goal.

## Recipe Coverage

Skipped (standard-tier, `skip-internal-logging-only`). All claims concern internal Sentry/logger behavior with no UI surface.

| # | Claim (verbatim) | Status | Rationale |
|---|------------------|--------|-----------|
| 1 | updatePositionTPSL missing logger.error | UNTESTABLE | Internal logging — verified via code review + unit test |
| 2 | flipPosition double-reported to Sentry | UNTESTABLE | Internal logging — verified via code review + unit test |
| 3 | closePosition/cancelOrder silently swallowed | UNTESTABLE | Internal logging — verified via code review + unit test |

Overall recipe coverage: 0/3 ACs PROVEN (all verified via code review + tests)
Untestable: 1, 2, 3 — all claims are about internal logger.error behavior with no UI surface; unit tests are the correct proof

## Prior Reviews

| Reviewer | State | Date | Addressed? | Notes |
|----------|-------|------|------------|-------|
| cursor | COMMENTED | 2026-05-06 | N/A | Bugbot automated summary only |

No human reviews yet.

## Acceptance Criteria Validation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | updatePositionTPSL logger.error added | PASS | Code review: TradingService.ts:1793-1800 adds logger.error in catch. Test: "logs error with message and context when provider throws" passes |
| 2 | flipPosition dedup | PASS | Code review: usePerpsFlipPosition.ts catch block no longer calls Logger.error. Test: "surfaces exception via toast and onError without double-reporting to Sentry" asserts `Logger.error` NOT called |
| 3 | Non-throwing failures now logged | PASS | Code review: cancelOrder:1126, closePosition:1454, cancelOrders:1323, closePositions:1659 all add logger.error. Tests assert logger.error called with correct Error + context |

## Code Quality

- Pattern adherence: Follows codebase conventions. Uses `ensureError` for string→Error conversion, `#getErrorContext` for lightweight context.
- Complexity: Appropriate — each change is a single `logger.error` call at the right place.
- Type safety: No type issues introduced. `ensureError` correctly handles `string | undefined` error values.
- Error handling: Adequate — errors are logged with method name, symbol, and provider error details.
- Anti-pattern findings: None. No magic strings, no `as any`, no `eslint-disable`, no `console.log`.

## Fix Quality

- **Best approach:** Yes — this is the minimal, correct fix. Each added `logger.error` call follows the established pattern. The dedup in the UI hook is the right layer boundary: controller owns Sentry, UI owns toasts.
- **Would not ship:** Nothing blocks merge.
- **Test quality:** Strong. Tests assert the exact arguments passed to `logger.error` (Error message + context object). Negative tests verify batch logging does NOT fire on fallback paths. The `usePerpsFlipPosition` test asserts `Logger.error` is NOT called, which would fail if the removal is reverted.
- **Brittleness:** Low. All logging uses stable internal APIs (`#deps.logger.error`, `#getErrorContext`, `ensureError`).

## Live Validation

- Recipe: skipped (standard-tier, internal-logging-only)
- Result: SKIPPED — no UI surface to validate
- Video: review.mp4 (brief app health capture)
- Native changes: none
- Metro errors: none PR-related (pre-existing Sentry type compat, appwright module, SnapUIRenderer resolution)
- Log monitoring: Metro logs checked, no PR-related errors

## Correctness

- Diff vs stated goal: Aligned — all three stated changes are present and correct.
- Edge cases:
  - `ensureError(result.error)` where `result.error` is `undefined`: produces `"Unknown error (no details provided) [TradingService.*]"` — acceptable.
  - Batch failure summary with many failures: string concatenation could produce very long error messages in Sentry. Not a correctness issue but worth monitoring.
- Race conditions: None — all logging is synchronous within the existing try/catch flow.
- Backward compatibility: Preserved. No public API changes. Additional Sentry events are additive.

## Static Analysis

- lint:tsc: PASS — no PR-related type errors (pre-existing errors in tests/appwright and Sentry type compat only)
- Tests: 94/94 pass (2 suites)

## Architecture & Domain

- Error context format inconsistency: The new `#getErrorContext` calls produce `{controller, method, ...}` flat objects, while existing catch blocks use verbose `{tags: {...}, context: {name, data: {...}}}` format. This means the same method may send two different context shapes to Sentry depending on throw vs non-throwing failure. Pre-existing inconsistency, not introduced by this PR — suggestion to align in a follow-up.
- File size: `TradingService.ts` at 2,119 lines (above 2,000 threshold). `TradingService.test.ts` at 2,413 lines. Both pre-existing but trending upward. This PR adds ~70 lines net. Consider splitting TradingService into per-operation modules in a follow-up.
- JSDoc in `usePerpsFlipPosition.ts` line 19 still mentions "Sentry tracking" but the hook no longer does Sentry reporting. Stale comment.

## Risk Assessment

- [LOW] — Additive error logging only. No behavioral changes to success paths. Test coverage is comprehensive. The only risk is increased Sentry event volume from previously-silent failures, which is the intended effect.

## Recommended Action

[APPROVE]

Minor suggestions:
1. `usePerpsFlipPosition.ts:19` — JSDoc still says "Sentry tracking" after removing Sentry reporting from this hook (nitpick)
2. Consider aligning error context format between throw and non-throwing failure paths in a follow-up (suggestion)
3. `TradingService.ts` at 2,119 lines — monitor file size growth (suggestion)
