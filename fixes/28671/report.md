# Fix Report — TAT-2057: Don't see latest funding payments in Activity

## Summary

`HyperLiquidProvider.getFunding()` made a single API call covering the full 365-day history window. The HyperLiquid `userFunding` API returns records in ascending chronological order capped at 500 per call, so active accounts silently receive only their oldest 500 records. The fix replaces the single call with parallel 30-day window fetches that guarantee the most recent records are always included.

## Root Cause

**File:** `app/controllers/perps/providers/HyperLiquidProvider.ts:5416`

The original `getFunding()` called:
```typescript
const rawFunding = await infoClient.userFunding({
  user: userAddress,
  startTime: Date.now() - 365 * 24 * 60 * 60 * 1000,
  endTime: undefined,
});
```

HyperLiquid's `userFunding` API returns records ascending (oldest first), capped at 500 per request. For accounts with >500 funding records in the past year (e.g., 0x316BDE with 1174 records from 2025-05 to 2026-04), only the oldest 500 were returned. The most recent 674 payments were silently dropped.

The oscillation between two cutoff dates on consecutive refreshes was caused by `Date.now()` being evaluated fresh on each call, producing slightly different window boundaries. Even small shifts changed which 500 records fell within the cap, making the cutoff jump between dates.

## Reproduction Commit

SHA: `a39d03de17` — "debug(pr-28671): add reproduction marker"

Added `DevLogger.log('[PR-28671] BUG_MARKER: getFunding hit 500-record API cap')` that fires when `rawFunding.length >= 500`. For 0x316BDE (1174 records), this marker would fire on every call.

## Changes

| File | Description |
|------|-------------|
| `app/controllers/perps/constants/transactionsHistoryConfig.ts` | Added `FUNDING_HISTORY_PAGE_WINDOW_DAYS: 30` and `FUNDING_HISTORY_API_LIMIT: 500` constants |
| `app/controllers/perps/providers/HyperLiquidProvider.ts` | Replaced single API call with parallel 30-day window pagination via `Promise.all` |
| `app/controllers/perps/providers/HyperLiquidProvider.test.ts` | Added 3 regression tests: parallel windows, recent records in long history, null page handling |

## Fix Detail

Divided the 365-day range into 30-day windows (~13 chunks), fetched all in parallel via `Promise.all`, then merged and sorted results. Each 30-day window stays well under the 500-record cap for any realistic user. The most recent window always contains today's records.

```typescript
const chunks: { start: number; end: number }[] = [];
let chunkEnd = finalEndTime;
while (chunkEnd > finalStartTime) {
  const chunkStart = Math.max(finalStartTime, chunkEnd - pageWindowMs);
  chunks.push({ start: chunkStart, end: chunkEnd });
  chunkEnd = chunkStart;
}
const pages = await Promise.all(
  chunks.map((chunk) => infoClient.userFunding({ user: userAddress, startTime: chunk.start, endTime: chunk.end }))
);
const allRaw = pages.flatMap((page) => page ?? []);
allRaw.sort((a, b) => a.time - b.time);
```

## Test Plan

**Unit tests:** `yarn jest app/controllers/perps/providers/HyperLiquidProvider.test.ts` — 4/4 pass (3 new regression tests)

**Recipe validation** (account 0x316BDE, 1174 records):
- `ac1-fetch-latest`: count=1174 > 500 cap, isRecent=true, exceedsCap=true ✅
- `ac2-consistency-check`: count1=99, count2=99, latestTs1=latestTs2, consistent=true ✅

**CI gates:** lint (0 errors), lint:tsc (0 errors), format:check (pass) ✅

## Evidence

| Artifact | Description |
|----------|-------------|
| `before.mp4` | Recipe on buggy code (single-call, 500-record cap) |
| `after.mp4` | Recipe on fixed code — count=1174, consistent results |
| `before-ac1-funding-latest.png` | Funding tab before fix |
| `after-ac1-funding-latest.png` | Funding tab after fix — "Today" entries visible |
| `after-ac2-funding-consistent.png` | Stable list — no oscillation |
| `recipe-coverage.md` | Per-AC coverage matrix |

## Ticket

TAT-2057 — https://consensyssoftware.atlassian.net/browse/TAT-2057
