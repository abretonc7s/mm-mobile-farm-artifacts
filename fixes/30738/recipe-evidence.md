# Recipe Evidence — PR #30738 (post-main-merge + controller migration)

Branch `TAT-3168-feat-add-market-category-shortcut` · merge commit `b608cbf172` · base `origin/main` `1780bfa843`
Runtime: iOS sim `mm-2`, Metro/CDP on `8062`, dev build, wallet unlocked on WalletView.

## Result: PASS (live, on the merged + migrated app)

All acceptance criteria validated **on the live merged build** via the recipe runner's
manifest-declared `press-test-id` primitive (React DevTools fiber-walk path) plus device screenshots.

| AC | Check | Evidence | Verdict |
|----|-------|----------|---------|
| AC1/AC5 | Magnifying glass icon present on BTC market detail header | `recipe-manual/clean-1-btc-detail.png` (glass left of star + expand) | ✅ PASS |
| AC2 | Tap glass → Markets list opens with **Crypto** category pre-selected (BTC → crypto) | `recipe-manual/clean-2-market-list.png` (Crypto pill active, BTC/ETH/HYPE…) | ✅ PASS |
| AC4 | Back from Markets → returns to originating BTC market detail | `recipe-manual/clean-3-back-to-detail.png` (BTC-USD detail) | ✅ PASS |

Live flow exercised (clean stack: WalletView → perps-home → BTC detail, no prior market-list):
`press homepage-section-title-perps → press perps-market-row-item-BTC → [AC1 icon present] →
press perps-market-header-category-search-button → [AC2 Markets/Crypto] →
press perps-market-list-close-button-back-button → [AC4 BTC detail]`.

The category-resolution correctness (BTC → `crypto`) is what surfaced live (Crypto pill active) and is
also unit-tested: `getMarketTypeFilter` is now imported from `@metamask/perps-controller` v8, and the
v8 market list filters `marketType === filter` (with `crypto`/`new`/`all` specials), so the controller's
returned value always lands on a populated pill.

Note: an earlier ad-hoc run showed back landing on perps-home — that was a **stack confound** (I had
entered the detail *through* a market-list screen, so `navigation.navigate(PERPS.ROOT,{screen:MARKET_LIST})`
popped to that existing instance). With a clean entry (no prior market-list, the real user flow / AC4
precondition) back correctly returns to the detail, as shown in clean-3.

## Harness gap (recorded per operator instruction — not a product defect)

The automated `metamask-recipe run` path could **not** drive this flow end-to-end because the mobile
runner's navigation/route/wait layers hard-depend on the in-app `globalThis.__AGENTIC__` bridge, which
**`main` removed** (it deleted `app/core/AgenticService/`; `__AGENTIC__` has zero references on
`origin/main`). Confirmed in `metamask-recipe-runner/live-adapters/mobile/bridge-runtime/cdp-bridge.cjs`:

- `get-route` / `navigate` → `globalThis.__AGENTIC__?.getRoute()/navigate()` → returns `undefined`
  → `ui.navigate` fails: *"Mobile CDP bridge returned non-JSON output for get-route: … undefined"*.
- `ui.wait_for` present-check → returns `present=false` for clearly-mounted testIDs
  (`wallet-screen`, `perps-home`) → times out. (Same `__AGENTIC__` dependency.)
- `lib/target-discovery.cjs` even selects the CDP target by *"probing for `__AGENTIC__` installed"*.
- Only `press-test-id` / `scroll-view` / `set-input` have a `__REACT_DEVTOOLS_GLOBAL_HOOK__`
  fiber-walk **fallback**, which is why the press-driven validation above works.

Failed automated attempt artifacts: `recipe-run/summary.json` + `recipe-run/trace.json`
(stops at `wait-perps-home`, `present=false`). Recipe authored at `artifacts/recipe.json`.

**Required follow-up (harness, not this PR):** update the mobile recipe runner to use the fiber-walk
fallback for route/wait/target-discovery (as `press` already does), or have `main` re-expose an
equivalent navigation bridge. Until then, mobile recipes that use `ui.navigate`/`ui.wait_for` cannot run
against post-`AgenticService`-removal builds.
