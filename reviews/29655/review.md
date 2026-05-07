# PR Review: #29655 — fix(perps): render PerpsConnectionErrorView once across all provider instances

**Tier:** standard

## Summary
The PR implements the right overall shape: a single `PerpsGlobalErrorGate` owns the visible connection error screen, and route-level providers suppress their own error UI. Unit coverage is strong for rendering, retry, cleanup, and analytics behavior. I would request changes because the runtime debounce no longer matches the PR's stated 1-second flap-suppression behavior.

## Recipe Coverage
Recipe decision: skipped (`skip-cdp-offline`). CDP/Metro probing failed at `http://localhost:8061/json/list`, so no recipe was generated.

| # | AC (verbatim) | Target platform | Recipe nodes (IDs) | Screenshot filename | Visual verdict | Justification |
|---|---------------|-----------------|---------------------|---------------------|----------------|---------------|
| 1 | "Only one `PerpsConnectionErrorView` is displayed when multiple Perps provider stacks are mounted and the shared connection manager reports an error." | ios | n/a | n/a | UNTESTABLE | standard-tier skip: CDP offline |
| 2 | "`PERPS_SCREEN_VIEWED` for the connection error screen fires exactly once for an error occurrence instead of once per provider instance." | ios | n/a | n/a | UNTESTABLE | standard-tier skip: CDP offline |
| 3 | "The connection error view disappears and Perps content is restored when the connection error clears." | ios | n/a | n/a | UNTESTABLE | standard-tier skip: CDP offline |
| 4 | "Tapping retry calls `PerpsConnectionManager.reconnectWithNewContext({ force: true })` and preserves a single visible error view." | ios | n/a | n/a | UNTESTABLE | standard-tier skip: CDP offline |
| 5 | "Each retry attempt emits one connection-error screen-view analytics event with the updated retry attempt count." | ios | n/a | n/a | UNTESTABLE | standard-tier skip: CDP offline |
| 6 | "Rapid error -> null -> error flaps within the debounce window do not emit duplicate connection-error screen-view events." | ios | n/a | n/a | UNTESTABLE | standard-tier skip: CDP offline |
| 7 | "All route-level `PerpsConnectionProvider` instances suppress their own error UI so the centralized gate owns error rendering." | ios | n/a | n/a | UNTESTABLE | standard-tier skip: CDP offline |

Overall recipe coverage: 0/7 ACs PROVEN
Untestable: AC1-AC7 — CDP offline on standard-tier slot

## Prior Reviews
No prior `CHANGES_REQUESTED` reviews.

## Acceptance Criteria Validation
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Only one `PerpsConnectionErrorView` is displayed when multiple Perps provider stacks are mounted and the shared connection manager reports an error. | PASS by unit test; UNTESTABLE on device | `only one error view renders even with multiple children providers`; CDP offline |
| 2 | `PERPS_SCREEN_VIEWED` for the connection error screen fires exactly once for an error occurrence instead of once per provider instance. | PASS by unit test; UNTESTABLE on device | `fires PERPS_SCREEN_VIEWED once after debounce when error occurs`; CDP offline |
| 3 | The connection error view disappears and Perps content is restored when the connection error clears. | PASS by unit test; UNTESTABLE on device | `shows children again when error clears`; CDP offline |
| 4 | Tapping retry calls `PerpsConnectionManager.reconnectWithNewContext({ force: true })` and preserves a single visible error view. | PASS by unit test; UNTESTABLE on device | `calls reconnectWithNewContext with force on retry`; CDP offline |
| 5 | Each retry attempt emits one connection-error screen-view analytics event with the updated retry attempt count. | PASS by unit test; UNTESTABLE on device | `fires one event per retry attempt`; CDP offline |
| 6 | Rapid error flaps within the debounce window do not emit duplicate connection-error screen-view events. | FAIL against PR body | Code uses `150` ms while PR body says 1 second |
| 7 | All route-level providers suppress their own error UI so the centralized gate owns error rendering. | PASS by code read; UNTESTABLE on device | `routes/index.tsx` passes `suppressErrorView` to all three providers |

## Code Quality
- Pattern adherence: mostly follows existing Perps UI/provider patterns.
- Complexity: appropriate for a narrow route-level rendering fix, though polling duplicates provider polling.
- Type safety: no new type issue seen in changed files.
- Error handling: retry failure breadcrumb is reasonable.
- Anti-pattern findings: `PerpsGlobalErrorGate.tsx:14` hardcodes a debounce value that conflicts with the PR body; `routes/index.tsx:137` starts suppressing provider error UI while the provider still records the old "PerpsConnectionErrorView shown" breadcrumb.

## Fix Quality
- **Best approach:** centralized gate plus suppressed provider error views is the right pragmatic approach.
- **Would not ship:** `PerpsGlobalErrorGate.tsx:14` at `150` ms while the PR promises 1-second flap suppression.
- **Test quality:** strong coverage overall, but tests now encode the mismatched 150 ms behavior and do not cover the provider breadcrumb duplication path.
- **Brittleness:** the fix relies on polling; acceptable for this PR, but a connection-manager subscription would be cleaner long term.

## Live Validation
- Recipe: skipped (`skip-cdp-offline`)
- Result: SKIPPED for recipe; code/test validation completed
- Video: `review.mp4` exists and has a `moov` atom; simulator-native `recordVideo` failed, host `screencapture` fallback was used
- Native changes: none
- Metro errors: existing/general warnings observed, including keychain warnings, Contentful fallback, and duplicate key warnings in Wallet
- Log monitoring: 30 seconds monitored in `.task/review/29655-0507-172028/artifacts/evidence/metro-monitor-30s.log`; no new lines captured during that window

## Correctness
- Diff vs stated goal: mostly aligned for visible error-screen dedupe, misaligned for the stated 1-second analytics debounce.
- Edge cases: connection clearing, retry failure, retry success, duplicate children, and unmount cleanup are covered by unit tests.
- Race conditions: potential duplicate analytics remains for flaps between 151 ms and 1000 ms.
- Backward compatibility: route-level provider context remains available under normal content rendering.

## Static Analysis
- lint:tsc: FAIL — two existing-looking errors outside the changed files:
  - `app/controllers/perps/PerpsController.ts(1920,11): Unused '@ts-expect-error' directive.`
  - `app/reducers/rewards/index.ts(571,7): Type instantiation is excessively deep and possibly infinite.`
- Tests: PASS — `18/18` in `PerpsGlobalErrorGate.test.tsx`

## Architecture & Domain
The centralized gate is consistent with the singleton connection-manager architecture and avoids adding controller or protocol coupling. The remaining domain concern is that provider-level Sentry breadcrumbs are not suppressed when provider error UI is suppressed, so the Sentry-noise part of the problem is only partially addressed.

## Risk Assessment
- MEDIUM — error rendering and analytics behavior are central to Perps outage handling; unit tests reduce risk, but the debounce mismatch is a correctness issue against the PR's stated behavior.

## Recommended Action
REQUEST_CHANGES

Fix the debounce/spec mismatch before merge. Also consider suppressing or moving the provider breadcrumb so suppressed providers do not continue to report `PerpsConnectionErrorView shown` multiple times.
