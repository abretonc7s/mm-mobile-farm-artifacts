# PR #35831 comments report

Review: geositta `CHANGES_REQUESTED` (5211202973) on `2204c40070`.

| # | Source | Author | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | review_comment 4016591566 | geositta | PerpsPositionCard.test.tsx:361 | REAL | Privacy test now enables both `selectPrivacyMode` and `selectPerpsCrossMarginEnabledFlag`, asserts the Cross badge renders, dots render, and neither "No liquidation price" nor `$1,800` is visible |
| 2 | review_comment 4016591579 | geositta | selectors/featureFlags/index.ts:541 | REAL | Pass raw flag value to `validatedVersionGatedFeatureFlag(remoteFlag: unknown)`; removed `as unknown as VersionGatedFeatureFlag` |
| 3 | review_comment 4016591590 | geositta | locales/languages/en.json:2296 | REAL | Removed the four duplicated `orderValidation.marginMode*` keys; moved the new copy into the existing (later, winning) definitions |
| 4 | review_comment 4016591601 | geositta | PerpsPositionCard.tsx:460 | REAL | `perps.cross_position.margin_used` → "Position margin used", so it no longer collides with the account summary "Margin used". Same key on Pro card stays consistent. PerpsPositionsView test asserts both labels distinctly |

Skipped status-only automation (no reply): 7 issue comments (CLA, Smart E2E selection, PR template check, SonarQube, performance results, and 2 bot entries previously handled). Flaky-test bot comment 5581571760 was already triaged and replied to in 5581695034 — `already replied`.

## Inherited AC coverage

Inherited recipe (42 nodes, family-inherited) covers the existing Cross position display in Pro and Lite for one live Cross ETH position: Cross badge, "Margin used" label, absent margin edit control, liquidation value (null → "No liquidation price", numeric → venue USD), and the shared-collateral tooltip explanation. Not covered: Android, mixed-book grouping, account-wide refresh, Pro margin-mode picker (disabled in this slice). The label change in comment 4 updated the recipe's `pro-margin`/`lite-margin` text to "Position margin used"; the run proves it live.

## Recipe re-validation (step 10): PASS

The account's pre-existing isolated BTC position was closed first with explicit user authorization (order `60226752331`), leaving an empty account. Null fixture opened: Cross ETH 0.0051 @ 2394.1, venue `liquidationPx: null` (order `60226912393`).

Recipe run: **41/41 nodes pass**, 60s, `artifacts/recipe-run/` (trace, six screenshots, diagnostics). `cross-summary-pro.png` shows "Position margin used $12.23" with the `Cross` badge and "No liquidation price", distinct from the account summary's "Margin used" — the exact collision geositta flagged.

Cleanup: fixture closed (order `60227080843`), ETH leverage restored to the isolated 3x baseline, final read 0 positions / 0 orders.

Note: `yarn lint:tsc` was not run locally (slot rules forbid full-project tsc in the worker pane); LSP reports 0 errors on `selectors/featureFlags/index.ts`, the only type-affecting change.

## Summary (step 13)

- Total actionable comments: 4 inline (4 REAL, 0 FALSE POSITIVE, 0 OUT OF SCOPE); flaky-test bot comment already triaged earlier (FALSE POSITIVE, `already replied`); 7 status-only automation comments skipped.
- Fix commit: `b11117780de`, pushed with lease over `2204c40070`.
- Files changed: `locales/languages/en.json`, `app/components/UI/Perps/selectors/featureFlags/index.ts`, `PerpsPositionCard.test.tsx`, `PerpsPositionsView.test.tsx`, `PerpsProPositionCard.test.tsx`. Recipe `artifacts/recipe.json` label nodes updated.
- Gate: scoped ESLint `--max-warnings=0` clean, `format:check` clean, Jest 6 suites / 278 tests pass, LSP 0 errors on the selector file. `lint:tsc` not run locally (slot rule).
- Recipe re-validation: PASS (41/41) on commit `b11117780de`, with cleanup verified.
- Integration status: `rebased` onto `origin/main` `954c6fe85cf` (6 commits, linear; `yarn install --immutable` after lockfile change).
- GitHub: replied inline to all 4 and resolved the 4 threads. PR body label mentions updated to "Position margin used".
