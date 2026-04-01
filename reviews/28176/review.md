# PR Review: #28176 — fix(perps): prevent rate limit exhaustion during rapid market switching (#28141)

**Tier:** standard

## Summary
This PR addresses HyperLiquid rate limit exhaustion (1200 weight/min) during rapid market switching through four targeted fixes: debounced candle WebSocket connections, lighter initial candle fetches (OneWeek/OneDay vs YearToDate), abortable REST calls via AbortController, and race guards on async subscription promises. The fix is well-structured, addresses the root causes, and achieves its stated goal.

## Prior Reviews
No prior CHANGES_REQUESTED reviews. Only COMMENTED reviews from cursor (bot summary) and abretonc7s.

## Acceptance Criteria Validation
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | No 429 errors after 4+ market switches | PASS | CDP validation: BTC→ETH→SOL→HYPE rapid switching, zero 429 errors in Metro log |
| 2 | Chart data loads for each market visited | PASS | CDP: successfully navigated to HYPE market, candle subscriptions established |
| 3 | Candle subscriptions debounced during rapid switching | PASS | Code review: 500ms debounce via PERFORMANCE_CONFIG.CandleConnectDebounceMs, tests verify |
| 4 | Stale subscriptions cleaned up | PASS | Code review: race guards in .then() handlers, pending promise tracking, abort on cleanup |

## Code Quality
- Pattern adherence: Follows codebase conventions. New constant in PERFORMANCE_CONFIG. Uses existing ensureError pattern.
- Complexity: Appropriate — each fix targets a specific root cause without over-engineering.
- Type safety: Two minor `as Promise<void>` casts in HyperLiquidSubscriptionService.ts:2667,3148 (promise chain returns `void | undefined`). Pragmatic and low-risk.
- Error handling: AbortError suppression is correct — abort is intentional, not an error.
- Anti-pattern findings:
  - Hardcoded `200` at CandleStreamChannel.ts:279 duplicates `PERFORMANCE_CONFIG.NavigationParamsDelayMs`. Minor inconsistency.
  - No magic strings, no console.log, no eslint-disable comments.

## Fix Quality
- **Best approach:** Yes, this is the correct fix. The four-pronged approach (debounce, lighter fetch, abort, race guards) addresses all identified root causes. A single fix (e.g., only debounce) would not fully solve the problem.
- **Would not ship:** Nothing blocking. All changes are shippable.
- **Test quality:** Good. Tests verify debounce timing via `flushConnectDebounce()`, cold/warm cache duration selection, abort error suppression. The abort test specifically verifies that `onError` is NOT called when abort fires — this is the right assertion.
- **Brittleness:** Low. The debounce constant is externalized. The race guard pattern (check subscriber count + existing subscription in .then()) is robust against re-ordering. The `as Promise<void>` casts are cosmetic.

## Live Validation
- Recipe: skipped (tier: standard)
- Result: PASS — CDP validation with 4 rapid market switches, zero errors
- Video: failed (SimulatorError — simulator recording unavailable)
- Native changes: none
- Metro errors: none related to PR changes (only pre-existing keychain warnings)
- Log monitoring: 30s monitored, zero 429/rate-limit errors, clean candle subscription establishment

## Correctness
- Diff vs stated goal: Aligned — all four root causes addressed
- Edge cases:
  - Covered: rapid away-and-back (pending promise replaced), cleanup during pending subscription, abort during in-flight REST
  - Covered: cache hit vs cold cache for duration selection
  - Covered: reconnection path clears pending promise maps
- Race conditions: Addressed — the entire PR is about fixing race conditions in async subscription lifecycle
- Backward compatibility: Preserved — no API changes, internal behavior only

## Static Analysis
- lint:tsc: PASS — 0 errors
- Tests: 115/115 pass (CandleStreamChannel.test.ts + HyperLiquidClientService.test.ts)

## Architecture & Domain
- HyperLiquidSubscriptionService.ts is at 3,731 lines (exceeds 2,500 hard limit). This PR adds ~50 lines but the file was already over-limit. Recommend planning a split in a follow-up.
- The debounce + abort + race guard pattern could serve as a reference for other subscription channels if similar issues arise.
- No controller portability issues — all changes are within the HyperLiquid provider layer.

## Risk Assessment
- [MEDIUM] — Changes core subscription lifecycle logic. However, the race guards are defensive (fail-safe: unsubscribe stale) and the debounce is a well-understood pattern. Tests cover the critical paths.

## Recommended Action
[APPROVE]
- Two minor nitpicks (hardcoded 200, `as Promise<void>` casts) — neither blocks merge.
- File size of HyperLiquidSubscriptionService.ts should be tracked for future split.
