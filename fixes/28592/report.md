# Fix Report — TAT-2892

**Ticket:** [TAT-2892](https://consensyssoftware.atlassian.net/browse/TAT-2892)
**Branch:** fix/tat-2892-fix-perps-foreground-reconnect
**PR:** #28592

---

## Summary

When the app returns to foreground within the 20 s grace period, `resumeFromForeground()` pings the WebSocket. The JS thread is often sluggish immediately after the AppState transition, causing the ping to throw even though the socket is alive. The existing catch block fell through directly to `ensureConnected()`, which tore down all 9 stream caches and set `isConnecting=true`, driving loading skeletons across all Perps UI.

**Fix:** Add a 500 ms ping retry before falling through; even if both pings fail, thread `preserveCaches: true` through `ensureConnected()` → `performEnsureConnected()` → `performActualDisconnection()` so stream caches survive the soft reconnect and no skeletons appear.

---

## Root Cause

**File:** `app/components/UI/Perps/services/PerpsConnectionManager.ts`

**Flow:**
1. `resumeFromForeground()` (line ~441) calls `provider.ping()`.
2. JS thread suspension during AppState transition causes `ping()` to reject — not because the WebSocket is dead.
3. The `catch` block (pre-fix line ~460) fell through immediately to `ensureConnected()`.
4. `ensureConnected()` → `performEnsureConnected()` → `performActualDisconnection({ force: true })` cleared all 9 stream caches (`positions`, `orders`, `account`, `prices`, `marketData`, `oiCaps`, `fills`, `topOfBook`, `candles`), set `isConnected=false`, `isInitialized=false`, then called `connect()`.
5. `connect()` set `isConnecting=true` → all Perps UI hooks see loading state → skeletons render.

---

## Reproduction Commit

**SHA:** `86f7f3de39` (`debug(pr-28592): add reproduction marker`)

The marker `DevLogger.log('[PR-28592] BUG_MARKER: ping failed in resumeFromForeground')` was added to the catch block in `resumeFromForeground()`. It fired during the foreground-return scenario, confirmed in Metro logs during the reproduction session (session was rotated; marker commit preserves the evidence in git history).

---

## Changes

| File | Description |
|---|---|
| `app/controllers/perps/constants/perpsConfig.ts` | Added `ForegroundPingRetryDelayMs: 500` to `PERPS_CONSTANTS` |
| `app/components/UI/Perps/services/PerpsConnectionManager.ts` | Added `preserveCaches?: boolean` to `ConnectOptions`; added ping retry in `resumeFromForeground()`; threaded `preserveCaches` through `ensureConnected()` → `performEnsureConnected()` → `performActualDisconnection()` |
| `app/components/UI/Perps/services/PerpsConnectionManager.test.ts` | Added 3 new tests: ping retry success skips reconnect, both-ping-fail uses preserveCaches, performActualDisconnection skips clearCache when preserveCaches=true |

---

## Test Plan

### Automated

- **Lint:** `yarn lint` — PASS
- **TypeScript:** `yarn lint:tsc` — PASS
- **Format:** `yarn format:check` — PASS
- **Unit tests:** `yarn jest app/components/UI/Perps/services/PerpsConnectionManager.test.ts --no-coverage` — 66/66 PASS
- **Recipe:** `validate-recipe.sh` — 5/5 nodes PASS

### Manual Gherkin

```
Given the Perps feature is enabled
  And the user has navigated to the Perps tab
  And the WebSocket is connected and initialized
When the user backgrounds the app for less than 20 seconds
  And the user returns the app to the foreground
Then the Perps tab must NOT show loading skeletons
  And the connection state must remain isConnected=true, isInitialized=true
  And stream caches (positions, orders, account) must NOT be cleared
```

---

## Evidence

| Artifact | Description |
|---|---|
| `before.mp4` | Recipe run on pre-fix code (marker commit active) |
| `after.mp4` | Recipe run on final fixed code — 5/5 nodes pass |
| `recipe.json` | Executable validation recipe (log_watch asserts no full-reconnect log lines) |
