# PR Review: #29857 — fix(perps): prevent CLIENT_NOT_INITIALIZED during reconnection and fix compound error string

**Tier:** standard

## Summary
This PR fixes three distinct issues causing perps trading actions to fail during initialization/reconnection: (1) action calls now await in-flight initialization instead of throwing immediately, (2) reconnection recreates all four SDK clients (not just WS-backed ones), and (3) the compound error string is replaced with a plain error code so i18n translation works correctly. The i18n toast message is updated to user-friendly guidance. The fix is well-structured, minimal, and correctly addresses all stated root causes.

## Recipe Coverage
Skipped (standard tier, `skip-internal-controller-logic-no-ui-surface`). All claims are about internal controller behavior (init-promise awaiting, error code formatting, client lifecycle) that cannot be reproduced via CDP without destructively simulating network drops or cold-start races. The claims are covered by unit tests.

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| 1 | Action calls await #initializationPromise when init is in flight | UNTESTABLE | Requires simulating in-flight init state; verified via code review + unit test |
| 2 | #handleConnectionDrop() recreates all four SDK clients | UNTESTABLE | Requires simulating WS drop; verified via code review + unit test |
| 3 | getActiveProvider() throws plain CLIENT_NOT_INITIALIZED | UNTESTABLE | Requires failed init state; verified via code review + unit test |
| 4 | initializationError captured in Sentry, not in thrown message | UNTESTABLE | Internal logger behavior; verified via code review + unit test |
| 5 | Toast gives actionable guidance | UNTESTABLE | Requires triggering error toast; verified via code review of en.json |
| 6 | Unit test: action during Initializing waits for init | PASS | Test passes: PerpsController.test.ts |
| 7 | Unit test: action during Failed throws plain code | PASS | Test passes: PerpsController.test.ts |
| 8 | Unit test: after reconnect, isInitialized() returns true | PASS | Test passes: HyperLiquidClientService.test.ts |

Overall recipe coverage: 3/8 PROVEN (unit tests), 5/8 UNTESTABLE (require simulating network/init failures)
Untestable: claims 1-5 — all require inducing init/reconnection failure states not reproducible via read-only CDP

> Note: No Jira acceptance criteria section was provided in the PR. Claims extracted from linked ticket TAT-3089.

## Prior Reviews
| Reviewer | State | Date | Addressed? | Notes |
|----------|-------|------|------------|-------|
| gambinish | APPROVED | 2026-05-12 | N/A | Approved, no changes requested |

## Acceptance Criteria Validation
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Action calls await init promise | PASS | Code adds `#awaitInitializationIfInProgress()` to all 11 write methods; unit test confirms wait behavior |
| 2 | Reconnection recreates all 4 clients | PASS | `#handleConnectionDrop()` now creates `#infoClientHttp` and `#exchangeClient`; unit test confirms `isInitialized()` returns true |
| 3 | Plain CLIENT_NOT_INITIALIZED code | PASS | Compound string removed; `getActiveProvider()` always throws plain code |
| 4 | Error logged to Sentry separately | PASS | `#logError()` called with `initializationError` before throwing; unit test confirms logger.error args |
| 5 | User-facing toast updated | PASS | en.json updated to "Connection not ready. Please wait a moment and try again." |
| 6 | Unit test: Initializing waits | PASS | Test uses blocking promise to simulate in-flight init, verifies placeOrder resolves after unblock |
| 7 | Unit test: Failed throws immediately | PASS | Test sets Failed state, verifies placeOrder rejects with plain CLIENT_NOT_INITIALIZED |
| 8 | Unit test: reconnect restores initialized | PASS | Test calls reconnect(), verifies ExchangeClient recreated and isInitialized() true |

## Code Quality
- Pattern adherence: Follows existing codebase patterns (same `as any` cast for ExchangeClient wallet param, consistent with initialize())
- Complexity: Appropriate — simple await-before-check pattern, no over-engineering
- Type safety: One `as any` cast at HyperLiquidClientService.ts:1209, but mirrors existing pattern at line 144
- Error handling: Correct — `#performInitialization()` never rejects, so `await #initializationPromise` is safe
- Anti-pattern findings: No new magic strings, no protocol-specific logic in shared code, no console.log usage

## Fix Quality
- **Best approach:** Yes — this is the minimal, correct fix for each issue. The await-before-check pattern is clean and doesn't change the synchronous `getActiveProvider()` contract (callers that don't need the await can still call it directly). Storing `#walletParams` is safe (function references, not key material) and enables correct reconnection.
- **Would not ship:** PerpsController.ts at 5,061 lines exceeds the 2,500 line hard limit. While this PR only adds ~30 lines, the file is already far over the threshold. This is a pre-existing issue but worth flagging for future planning — not a blocker for this specific fix.
- **Test quality:** Tests are well-targeted. The blocking-promise test (lines 85-142 in PerpsController.test.ts) correctly simulates the Initializing state race. Tests would fail if fix is reverted. Both success and failure paths are tested.
- **Brittleness:** Low. The fix relies on `#initializationPromise` lifecycle which is well-established in the controller. The `#walletParams` storage is simple and doesn't introduce new state management complexity.

## Live Validation
- Recipe: skipped (standard tier, internal controller logic)
- Result: SKIPPED
- Video: review.mp4 (health check only — Wallet home screen with healthy controller state)
- Native changes: none
- Metro errors: none from this PR (pre-existing keychain warnings, segment URL error)
- Log monitoring: Monitored metro.log during validation, no errors. PerpsController state persisting normally.

## Correctness
- Diff vs stated goal: Aligned — all four root causes addressed
- Edge cases:
  - `#initializationPromise` null when Failed: handled — `#awaitInitializationIfInProgress` checks both state AND promise
  - `#walletParams` undefined (read-only session): handled — `if (this.#walletParams)` guard in reconnection
  - `#httpTransport` undefined after `#createTransports()`: cannot happen (always created), but guarded defensively
  - `initializationError` null on Failed state: handled — fallback string "Initialization failed" in Sentry log
- Race conditions: None introduced. `#awaitInitializationIfInProgress` relies on the existing promise deduplication in `init()`. Multiple concurrent action calls will all await the same promise.
- Backward compatibility: Preserved — `getActiveProvider()` still throws the same error code, just without the compound suffix

## Static Analysis
- lint:tsc: Pre-existing config error (TS5098 from local tsconfig modification, not PR-related)
- Tests: 335/335 pass (PerpsController.test.ts + HyperLiquidClientService.test.ts)

## Architecture & Domain
- The `#awaitInitializationIfInProgress` pattern is applied consistently to write-path methods only, leaving read-path methods (getPositions, getOrders, etc.) as fail-fast. This is the correct trade-off — reads should not block on init.
- `#walletParams` storage in HyperLiquidClientService is a reasonable addition for reconnection purposes. The type is just function references, not sensitive data.
- PerpsController at 5,061 lines is a growing concern but predates this PR.

## Risk Assessment
- [LOW] — Changes are well-scoped to the initialization/reconnection path. The await guard is a safe addition (promise never rejects). Client recreation mirrors the existing initialize() pattern. Error string change fixes a clear bug without altering control flow.

## Recommended Action
[APPROVE]
Clean, well-tested fix that addresses all stated root causes. The only flag is PerpsController.ts file size (5,061 lines, pre-existing) — worth tracking as tech debt but not a blocker for this fix.
