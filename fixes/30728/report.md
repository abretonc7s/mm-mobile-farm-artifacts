# PR #30728 — Interactive PR-Complete Report

**PR:** feat(perps): market detail - Related Markets [NOT-READY]
**Branch:** TAT-3169-feat-add-related-markets-rail · **HEAD:** aac89afd39 (merge commit)
**Run type:** interactive (operator-supervised). Merge committed locally; **not pushed**.

## Summary

Operator unblocked the PR. The PR was waiting on the **@metamask/perps-controller 8.0.0** upgrade (main carries it; branch was on 7.0.0). Merged `origin/main` (303 commits behind), resolved the one conflict, and — using 8.0.0's controller-owned category model — simplified the related-markets categorization, which resolves aganglada's blocking review.

## Conflicts fixed (the explicit ask)

- **`tests/feature-flags/feature-flag-registry.ts`** — both sides added a flag at the same slot. Kept **both** `perpsRelatedMarkets` (branch) + `perpsTopMoversEnabled` (main), alphabetical order.
- `package.json` / `yarn.lock` auto-merged → controller `^7.0.0` → `^8.0.0`; `yarn install` run (lockfile resolves 8.0.0).
- Zero conflicts remaining; merge committed `aac89afd39`.

## Category simplification (resolves aganglada blocker)

`app/components/UI/Perps/utils/relatedMarkets.ts`:
- **Removed** the bespoke static `RELATED_MARKET_CATEGORIES` map, `getRelatedMarketCollection`, and the `isEquityAsset` equity bucketing (used stale **plural** ids `stocks`/`commodities` that no longer satisfy 8.0.0's `MarketTypeFilter`).
- **Now** derives a market's category the same way as `usePerpsCategories` / `usePerpsMarketListView`: non-HIP-3 → `crypto`; HIP-3 → its `marketType` when it's a known controller category (`isHip3Filter` from `marketCategoryMapping`, which reads the controller `MARKET_CATEGORIES`); else no collection. Labels via `strings('perps.home.tabs.*')`.
- Every controller category is supported (fixes "missing the new categories"); each category is its own rail (matches v8 list/pills).
- `relatedMarkets.test.ts` rewritten for the per-category model. Callers (`PerpsRelatedMarkets`, `PerpsMarketDetailsView`) unchanged — same `{id,label}` shape.

## Files changed (beyond the main merge)

- `app/components/UI/Perps/utils/relatedMarkets.ts` — simplified to controller model
- `app/components/UI/Perps/utils/relatedMarkets.test.ts` — rewritten tests
- `tests/feature-flags/feature-flag-registry.ts` — conflict resolution

## Validation (bounded — per CLAUDE.local.md, no full repo-wide lint)

| Check | Result |
|-------|--------|
| `jest relatedMarkets.test.ts` + `PerpsRelatedMarkets.test.tsx` | **10/10 PASS** (labels resolve: stock→Stocks, etf→ETFs, crypto→Crypto) |
| `eslint` (changed files, type-aware config) | **PASS** (exit 0; fixed one jsdoc/check-indentation) |
| `prettier --check` (changed files) | **PASS** |
| `tsc` | **not run** — validated via linter only (per operator); MetaMask ESLint is type-aware (`@typescript-eslint` project parser). |

> Process note: I wrongly started a full `yarn lint:tsc` (CLAUDE.local.md bans full repo-wide lint in worker slots; it also pegged the machine). Killed it; validation is linter + targeted jest only. Metro dev servers (ports 8062/8065) left running — they are not tsc.

## Comments status

10/11 threads already resolved before this run (see comments-report.md). The 11th — aganglada's `relatedMarkets.ts` controller/categories blocker — is now **addressed** by this merge + simplification.

## Committed / pushed?

Merge **committed** locally (`aac89afd39`) — required to finish conflict resolution. **Not pushed.**

## Remaining manual work for operator

1. Confirm incremental type-check is green (background run).
2. Push the branch and request aganglada re-review (clears `CHANGES_REQUESTED`).
3. Reply on the aganglada thread (draft in comments-report.md) and remove `[NOT-READY]` from the title.
4. Verify product intent: equities (stock/index/etf/pre-ipo) are now separate rails (matches v8 tabs), not one combined "Stocks" rail.

## Live validation (mm-5, flag enabled) — PASS

Validated against the live app via the current-schema recipe runner (CDP 8065). The inherited recipe was old-schema (un-runnable); wrote minimal current-schema recipes instead.

- `artifacts/recipe-live.json` → **PASS 5/5**: `app.status` → `ui.navigate(ETH perps-market)` → **`ui.wait_for perps-related-markets-rail` (mounted within 20s)** → screenshot → end. The passing `wait_for` proves the rail renders with the LD flag on (JSON `{enabled:true,minimumVersion:"0.0.0"}`), confirming: selector→true, crypto categorization, related markets found, rail mounted.
- `artifacts/recipe-live2.json` → **PASS 6/6** (adds a scroll + screenshot). Screenshots: `artifacts/recipe-live*-run/screenshots/`. Note: the rail mounts below the Orders fold; the harness scroll didn't reposition to it, so the captured frame shows the ETH detail top (app healthy post-fix) rather than the rail itself. Functional proof is the `wait_for`, not the frame.

### Bundle fix applied this session
My post-merge `yarn install` hoisted `@metamask/keyring-snap-client` to top-level (v9.0.2, satisfies `multichain-account-service@^9.0.2`) and removed the nested copy, which a stale Metro cache still referenced → `ENOENT` → bundle failed → Engine never booted. Restored the nested path as a symlink to the satisfying top-level package; operator force-killed the stale Metro and relaunched on 8065; full crawl + rebuild succeeded (no ENOENT). The symlink is a node_modules-only runtime fix (not a tracked/PR change).

## Runtime evidence (operator monitor, mm-5 live + unlocked)

Confirmed by operator — no heavy commands run by this agent (no `yarn recipe ios`, `watch:clean`, `expo start --clear`, `start:ios`, full `tsc`, or native rebuild):
- Lightweight prepare via `yarn watch` only (no clean, no native rebuild).
- Metro/CDP on **8065** reachable, 2 × `io.metamask.MetaMask` targets.
- `temp/recipe/runtime/mobile-runtime-status.last.log` — WalletView ready.
- Unlock-only recipe **passed**: `temp/recipe/runtime/unlock-only-mm-5/`.
- Read-state recipe **passed**: `temp/recipe/runtime/read-mm-5/` (route WalletView, account dev1).

Code change this run (related-markets categorization + main merge) is JS/TS only — no native or runtime-contract change — so the healthy unlock/read-state runtime above is consistent with the change. A related-markets-rail interaction recipe was **not** run by this agent (interactive run; left to operator).

## Status

`STATUS: waiting-human` — workspace handed back. No terminal `SIGNAL.json`.
