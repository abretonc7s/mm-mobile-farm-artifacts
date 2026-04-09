# PR Review: #27898 — feat(perps): disk-backed cold-start cache for instant data display

**Tier:** standard

## Summary

This PR implements MMKV-backed disk persistence for Perps market and user data to eliminate the 1-4s loading skeleton on cold start. The implementation is well-structured: `PerpsController` hydrates caches synchronously from MMKV at construction time, hooks seed initial state from in-memory stream snapshots before falling back to controller cache, and both the controller and `PerpsStreamManager` persist fresh data to disk on a throttled cadence. The PR achieves its stated goal of instant data display on cold start with `$---` placeholder prices until WebSocket delivers fresh values.

The code is clean, well-tested (577 tests pass), and follows domain conventions. The `perpsDiskPersistence.ts` extraction keeps the controller portable. The DI-based `diskCache` interface is testable and platform-agnostic.

## Prior Reviews

| Reviewer | State | Date | Addressed? | Notes |
|----------|-------|------|------------|-------|
| geositta | APPROVED | 2026-04-09 | N/A | Final approval after iterative review |
| geositta | DISMISSED | 2026-04-02, 2026-04-09 | addressed | Earlier reviews superseded by approval |
| michalconsensys | DISMISSED | 2026-04-02 | addressed | Earlier review superseded |
| abretonc7s | COMMENTED | multiple | addressed | Extensive review comments, all addressed in subsequent commits (refactors, extractions, fixes) |
| cursor | COMMENTED | multiple | N/A | Automated review bot |

No `CHANGES_REQUESTED` reviews. All feedback addressed through 44 commits of iterative refinement.

## Acceptance Criteria Validation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Cold start displays market data immediately without loading skeletons | PASS | CDP eval confirms 290 markets cached in `cachedMarketDataByProvider['hyperliquid:mainnet']`; `skipTTL` getter works; `#hydrateCacheFromDiskSync()` runs at construction time |
| 2 | JS reload hydrates cached market data instantly from disk | PASS | Metro logs show `rest_preload_end {duration_ms: 331, markets: 290}`; controller hydration tested in 8 unit tests covering single/multi-provider, corrupt JSON, stale data |
| 3 | Account switch preserves global market cache, refreshes user data only | PASS | `MarketDataChannel.clearCache(preserveCache=true)` keeps market data on account-only switches; `PerpsConnectionManager` only removes `PERPS_DISK_CACHE_USER_DATA` on account switch |

## Code Quality

- **Pattern adherence:** Follows codebase conventions — DI via `PerpsPlatformDependencies`, constants in `perpsConfig.ts`, utility extraction to `utils/`, fire-and-forget disk writes
- **Complexity:** Appropriate for the feature scope. Two-source hydration (snapshot → cache → default) is the minimal complexity needed
- **Type safety:** Clean — TSC passes with 0 errors. New types (`DiskCacheMarketEntry`, `DiskCacheUserEntry`, `HydrateFromDiskResult`) are well-defined
- **Error handling:** Adequate — corrupt JSON caught silently, missing `getItemSync` handled gracefully, all disk writes are fire-and-forget with `.catch(() => {})`
- **Anti-pattern findings:** None. No magic strings (all cache keys are constants), no platform-specific imports in controller, no new MetaMetrics events needed (infrastructure-only change)

## Fix Quality

- **Best approach:** Yes — this is the right fix. DI-based disk cache keeps controller portable. Sync MMKV read at construction time is the optimal hydration point. Price stripping prevents misleading stale prices.
- **Would not ship:** No blocking items.
- **Test quality:** Strong — 577 tests covering disk hydration (single + multi-provider), corrupt JSON, missing API, stale data with `skipTTL`, address mismatch filtering, fresher in-memory state protection, channel snapshot priority, and reconnection behavior.
- **Brittleness:** Minor — `staleHydratedTimestamp = Date.now() - staleGuardMs * 10 - 1` couples timestamp manipulation to TTL constants. If `#preloadGuardMs` changes, the `* 10` factor may need adjustment. Low risk given the constant is stable and well-documented.

## Live Validation

- Recipe: skipped (tier: standard)
- Result: PASS — CDP eval confirmed 290 markets cached, `skipTTL` works for both market and user data, cache keys correct
- Video: review.mp4
- Native changes: none
- Metro errors: none related to PR (pre-existing keychain warnings only)
- Log monitoring: 30s monitored, no errors. Observed `rest_preload_start/end` and `Disk cache hydrated` logs confirming new code paths are active.

## Correctness

- **Diff vs stated goal:** Aligned — PR delivers exactly what it claims
- **Edge cases covered:**
  - Corrupt disk JSON → silently ignored, falls back to empty cache
  - Missing `getItemSync` (E2E) → no-op, graceful fallback
  - Address mismatch on user data → filtered at read time by `getCachedUserDataForActiveProvider`
  - Fresher in-memory data → not overwritten by older disk data (timestamp comparison)
  - Account-only switch → market cache preserved, user cache cleared + disk key deleted
  - Provider/network switch → both disk keys deleted
- **Race conditions:** None introduced. Disk writes are fire-and-forget. Hydration is synchronous at construction (before any async operations). Stream data always overwrites disk data due to stale timestamps.
- **Backward compatibility:** Preserved — `getItemSync` is optional, `skipTTL` defaults to false, `clearCache` default behavior unchanged

## Static Analysis

- lint:tsc: PASS — 0 errors
- Tests: 577/577 pass across 10 test suites (all changed test files)

## Architecture & Domain

- **Scaling:** MMKV reads are ~1ms synchronous, writes are fire-and-forget. 290 markets serialized/deserialized efficiently. Throttle prevents write storms.
- **Multi-provider:** Aggregated mode correctly groups by `providerNetworkKey`, both for persistence and hydration. `#getAggregatedCacheProviderIds` discovers providers from both registered providers AND cache keys (handles pre-init hydration).
- **Preload ownership:** Moving `startMarketDataPreload` from `Wallet/index.tsx` to `PerpsAlwaysOnProvider` is correct — ensures preload runs in both wallet tab and homepage-sections layouts.
- **File size concern:** `PerpsController.ts` is 5,014 lines (exceeds 2,500 guideline). Pre-existing issue — PR adds ~80 lines but extracts 351 to `perpsDiskPersistence.ts`, which is a net improvement. Recommend continued extraction in future PRs.

## Risk Assessment

**MEDIUM** — The core changes (disk hydration, cache persistence, `skipTTL` getters) are well-tested and follow established patterns. The behavioral change to `MarketDataChannel.clearCache()` (preserving cache on account switches) is correct but changes existing semantics. The `PerpsAlwaysOnProvider` preload ownership change is low-risk but affects app lifecycle. No new user-facing UI, no new navigation routes, no new external API calls.

## Recommended Action

**APPROVE** — The PR is well-implemented, thoroughly tested, and achieves its stated goal. The iterative review process with `abretonc7s` and `geositta` has refined the implementation through 44 commits. Already approved by `geositta`. One suggestion below for future consideration (not blocking).
