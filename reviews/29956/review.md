# PR Review: #29956 — refactor: update section performance tracking logic across multiple components

**Tier:** standard

## Summary
This PR improves homepage section performance tracing so that **Time to Content** (TTC) completes successfully for error and empty terminal states, recording an accurate `content_state` value (`filled`, `empty`, or `error`). It adds `contentStateForTrace` to `useSectionPerformance`, aligns `sectionId` with `analyticsName` for Perps/Tokens/Predict, and adjusts `contentReady`/`isEmpty` logic across 5 section components. The PR achieves its stated goal cleanly with minimal changes and good test coverage.

## Recipe Coverage
Recipe decision: skip-telemetry-only

| # | AC (verbatim) | Target platform | Recipe nodes | Screenshot | Visual verdict | Justification |
|---|---------------|-----------------|--------------|------------|----------------|---------------|
| 1 | "Given the app is on the wallet homepage... Then no regression is observed in section layout or behavior" | both | N/A | homepage-sections.png | UNTESTABLE | standard-tier skip — telemetry-only changes; homepage screenshot confirms no visual regression |
| 2 | "Given Sentry performance data... Then Time to Content completes with expected content_state... And Homepage Section Data Fetch reflects the first load only" | both | N/A | N/A | UNTESTABLE | standard-tier skip — Sentry trace verification requires Sentry dashboard; unit tests cover hook logic |

Overall recipe coverage: 0/2 ACs PROVEN
Untestable: 1 (telemetry-only, no UI surface), 2 (requires Sentry dashboard access)

> Coverage escalation: AC1, AC2 not proven on device.
>   Reason: PR changes are purely telemetry/tracing semantics — Sentry trace content_state values are not observable via CDP. Unit tests (21/21 pass) validate the hook logic. Homepage screenshot confirms no visual regression.
>   Human reviewer must validate Sentry trace output manually on staging before merging.

## Prior Reviews
| Reviewer | State | Date | Addressed? | Notes |
|----------|-------|------|------------|-------|
| Prithpal-Sooriya | APPROVED | 2026-05-13 | N/A | Approved |
| caieu | APPROVED | 2026-05-13 | N/A | Approved |
| geositta | APPROVED | 2026-05-13 | N/A | Approved |
| wachunei | APPROVED | 2026-05-13 | N/A | Approved |

4 prior approvals, no outstanding CHANGES_REQUESTED.

## Acceptance Criteria Validation
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | No regression in section layout or behavior | PASS | Code review + homepage screenshot — no UI changes, only telemetry param adjustments |
| 2 | TTC completes with expected content_state for error/empty outcomes; data fetch first-load only | PASS | Code review + unit tests (21/21 pass) — `contentStateForTrace` correctly overrides isEmpty-derived state; `fetchEnded.current` guards against refresh tracing |

## Code Quality
- **Pattern adherence:** Follows codebase conventions. Uses existing `HomeSectionNames` and `analyticsName` consistently. Clean union type for `contentStateForTrace`.
- **Complexity:** Appropriate. The `predictTimeToContentReady` logic in PredictionsSection is the most complex addition but is well-commented and matches the section's multi-data-source loading pattern.
- **Type safety:** Good. `contentStateForTrace` typed as `'filled' | 'empty' | 'error'` union — no `any` casts.
- **Error handling:** Adequate. Error states properly routed through `contentStateForTrace` override.
- **Anti-pattern findings:** None. No magic strings, no `console.log`, no `eslint-disable`.

## Fix Quality
- **Best approach:** Yes. The `contentStateForTrace` optional override is minimal and elegant — it avoids overloading `isEmpty` semantics while keeping the API backward-compatible. Using `analyticsName` for `sectionId` is the correct alignment.
- **Would not ship:** Nothing blocks merge.
- **Test quality:** Good. New test verifies `contentStateForTrace: 'error'` override. Existing tests cover first-load-only data fetch, unmount cleanup, and enabled flag gating. Tests would fail if the change is reverted (the new test depends on `contentStateForTrace` parameter).
- **Brittleness:** Low. Simple fallback chain (`contentStateForTrace ?? (isEmpty ? 'empty' : 'filled')`). No import-time or mock-coupling concerns.

## Live Validation
- Recipe: skipped (tier: standard, reason: telemetry-only)
- Result: SKIPPED
- Video: review.mp4 (8s health check)
- Native changes: none
- Metro errors: Pre-existing circuit breaker warnings only — no new errors from PR
- Log monitoring: Metro logs monitored, no PR-related errors

## Correctness
- **Diff vs stated goal:** Aligned. PR correctly adds `contentStateForTrace`, aligns `sectionId` with `analyticsName`, and adjusts `contentReady`/`isEmpty` for error/empty terminal states.
- **Edge cases:**
  - TokensSection: `isEmpty: isZeroBalanceAccount || showTokensError` — error treated as "empty" for the `isEmpty` prop, but `contentStateForTrace: 'error'` correctly overrides the derived `content_state`. Functionally correct, semantically loose. Minor nitpick.
  - PredictionsSection: `predictTimeToContentReady` includes `hasError` as a ready-trigger — correct, since error UI is a valid terminal state.
- **Race conditions:** None. Ref-based bookkeeping prevents double-end. `fetchEnded.current` guard prevents refresh tracing.
- **Backward compatibility:** Preserved. `contentStateForTrace` is optional with `undefined` default, maintaining existing behavior for sections that don't provide it.

## Static Analysis
- lint:tsc: PASS — 0 errors
- Tests: 21/21 pass (useSectionPerformance.test.ts)

## Architecture & Domain
No architectural concerns. Changes are scoped to homepage section telemetry. The `contentStateForTrace` extension to `useSectionPerformance` is well-designed — it handles the three-state content reporting (`filled`/`empty`/`error`) without breaking the existing two-state (`filled`/`empty`) derivation. Sentry dashboard consumers should be aware that `section_id` values will change for Perps/Tokens/Predict sections (from `HomeSectionNames` enum to `analyticsName`).

## Risk Assessment
- **LOW** — Changes are purely to Sentry telemetry semantics. No UI behavior changes. No navigation or state management changes. All existing tests pass plus new test coverage. 4 prior approvals from team reviewers. Risk is limited to Sentry dashboard queries that filter by old `section_id` values needing updates.

## Recommended Action
APPROVE
Well-structured refactor with good test coverage. The PR is already approved by 4 reviewers. Only note: Sentry dashboard queries filtering by old `section_id` values (e.g. `HomeSectionNames.PERPS` vs `analyticsName`) should be updated post-merge.
