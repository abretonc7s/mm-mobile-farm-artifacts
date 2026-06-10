# PR #30728 — Merge main + controller-aligned category simplification

**Branch:** TAT-3169-feat-add-related-markets-rail
**Merged:** `origin/main` (branch was 303 behind / 14 ahead) — merge commit (not rebase), not yet created/committed pending validation.

## Why this unblocks the PR

The PR was `[NOT-READY]` waiting on the **@metamask/perps-controller 8.0.0** upgrade, which main now carries (branch was on `^7.0.0`). 8.0.0 makes the controller the source of truth for market categories:
- `MarketTypeFilter` now uses **singular** category ids matching `MarketCategory` (`stock`/`index`/`etf`/`commodity`), and exports the `MARKET_CATEGORIES` constant.
- `getMarketDataWithPrices` gains `categories`, `excludeSymbols`, `sortBy`, `limit`.

This is what aganglada's blocking review asked for ("this logic should be on the controller, and it's missing the new categories").

## Conflicts resolved

| File | Side preferred | Why |
|------|----------------|-----|
| `tests/feature-flags/feature-flag-registry.ts` | **both (manual)** | Branch added `perpsRelatedMarkets`; main added `perpsTopMoversEnabled` at the same alphabetical slot. Kept **both** entries, in alphabetical order. No semantic loss. |

`package.json` / `yarn.lock` auto-merged → `@metamask/perps-controller` bumped `^7.0.0` → `^8.0.0`; `yarn install` run, lockfile now resolves `8.0.0`.

## Controller-aligned simplification (resolves aganglada blocker)

`app/components/UI/Perps/utils/relatedMarkets.ts` rewritten to use the controller-backed category model instead of a bespoke static map:

- **Removed**: local `RELATED_MARKET_CATEGORIES` static map, `getRelatedMarketCollection`, and the `isEquityAsset` equity-bucketing (which mashed stock/pre-ipo/index/etf into one "stocks" group and used stale **plural** ids `stocks`/`commodities` that no longer satisfy 8.0.0's `MarketTypeFilter`).
- **Now**: a market's category id derives the same way as `usePerpsCategories` / `usePerpsMarketListView`:
  - non-HIP-3 (main DEX) → `crypto`
  - HIP-3 with a known `marketType` → that category (`stock`, `pre-ipo`, `index`, `etf`, `commodity`, `forex`) via `isHip3Filter` from `marketCategoryMapping` (derived from controller `MARKET_CATEGORIES`)
  - uncategorised HIP-3 → no collection
  - labels via `strings('perps.home.tabs.<key>')`, identical to the category pills.
- **Effect**: every controller category is supported (fixes "missing the new categories"); each HIP-3 category is its own rail group (matches v8 list/pills); no more stale plural ids.

`relatedMarkets.test.ts` rewritten for the per-category model (6 cases incl. "no equity bucketing"). Component (`PerpsRelatedMarkets`) and view (`PerpsMarketDetailsView`) consume `{id,label}` unchanged — no caller signature change.

## Validation

| Check | Result |
|-------|--------|
| `relatedMarkets.test.ts` + `PerpsRelatedMarkets.test.tsx` | 10/10 PASS (labels resolve: stock→Stocks, etf→ETFs, crypto→Crypto) |
| `eslint` (changed files, type-aware) | PASS (exit 0) |
| `prettier --check` (changed files) | PASS |
| `tsc` | not run — linter-only validation per operator |

## Risks / manual verification for operator

- Behaviour change: equities (stock/pre-ipo/index/etf) are no longer one combined "Stocks" rail — each is its own category rail, matching the v8 market list & product pills. Confirm this matches product intent (it aligns with how the Stocks/Indices/ETFs tabs now work in main).
- `'new'` pseudo-category dropped from related-markets grouping (it was never a controller category and isn't a product pill); new markets now group by their underlying category.
- Merge commit + refactor are staged in the working tree but **not committed/pushed** (interactive run) — operator finalizes.
