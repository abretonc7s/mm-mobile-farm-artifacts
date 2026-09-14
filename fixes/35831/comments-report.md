# PR #35831 comments report

Live fetch 2026-09-14 against pre-rebase head `9b0472a4d4a`.

- Inline review comments: 0
- CHANGES_REQUESTED reviews: 0 (no reviews at all)
- Conversation comments: 8

| # | Source | Author | Where | Triage | Action |
|---|--------|--------|-------|--------|--------|
| 1 | issue_comment 5632566796 | github-actions[bot] | Performance Test Results | OUT OF SCOPE | "Perps open position and close it" failed with `no_performance_metrics` (no metrics collected), not a regression. Profiling shows no metric over the +10% baseline margin; check is non-blocking. PR diff is display-only and does not touch the open/close order flow. No code change. |
| 2 | issue_comment 5581571760 | github-actions[bot] | Flaky unit test detection | FALSE POSITIVE (no-op) | Body reports all earlier findings fixed; metadata `findings: []` for all 5 files at `9b0472a4`. Already answered in 5581695034 and 5632089383. No reply needed. |

Skipped without reply (status-only automation / own notes): CLA (5578350099), Smart E2E selection (5632142400), SonarQube quality gate passed (5632252432), 3 own earlier triage notes (5581695034, 5619337354, 5632089383).

## PR context

Display-only Cross margin support for existing positions (Lite `PerpsPositionCard`, Pro `PerpsProPositionCard`, `PerpsCard` list badge), shared-collateral info button, non-editable "Margin used", gated behind `perpsCrossMarginEnabled` (default false). 17 files.

Note: `check-pr-labels` fails only because the PR still carries the `blocked` label. The Core dependency blocker was cleared on 2026-09-10; label removal is left to the author.

## Integration

`rebased` onto origin/main `f9fff6ad167`: 6 commits replayed cleanly, linear, no merge commit. Pre-rebase remote `9b0472a4d4a` → local `2204c40070c`. Main changed `yarn.lock`/`package.json`/`ios/Podfile.lock`; `yarn install --immutable` exit 0.

## Local gate (post-rebase)

- Scoped ESLint `--max-warnings=0` on all 16 PR TS/TSX files: exit 0
- `yarn format:check`: clean
- Type check: LSP diagnostics, 0 errors on the 6 changed source files. Full `yarn lint:tsc` not run from the worker pane per slot rules; CI runs it.
- Jest, 6 affected suites: 278/278 pass
- `git status --porcelain`: clean

## Recipe re-validation: FAIL at fixture precondition (environmental)

Inherited AC coverage (`artifacts/recipe.json`): Lite + Pro Cross badge, venue liquidation price or explicit no-price state, shared-collateral explanation sheet, non-editable "Margin used". Requires exactly one live Cross ETH position on dev1 (`0x8dc623e9…9003`), no trades created.

- Runtime healthy: `mm-harness launch ios --verify` passed, doctor live, fixture READY.
- Precondition fails before any PR assertion. Hyperliquid testnet `clearinghouseState` for the account: `assetPositions: []`, `accountValue: "0.0"`; `frontendOpenOrders`: 0; `spotClearinghouseState` USDC 629.306541 (unified collateral, so the account is funded) (`artifacts/venue-precondition.txt`). `require-cross` (`$.positions length_eq 1`) cannot pass. Building a Cross fixture needs authorized testnet trades plus cleanup, which is outside this mechanical re-run; the recipe itself creates no trades.
- Recipe executed (`mm-harness run … --slot macwork-mmdev-1`). The parent helper was missing from this slot and hardcoded `IOS_SIMULATOR: mm-2`, `WATCHER_PORT: 8062`, so a copy was staged at the recipe's path with only those two values changed to `mmdev-1`/`8061`. The recipe calls only its read-only `inspect` operation.
- Attempt 1 (`recipe-run-cdp-timeout/`): `wallet`, `account`, `unlock` pass; `environment` fails with `CDP_TIMEOUT` on `Runtime.evaluate` right after unlock (app busy). Retried once.
- Attempt 2 (`recipe-run/`): identity verified (dev1, hyperliquid, `isTestnet: true`); controller `positions: []`; fails at `require-cross` (`cause_class: subject`) before any display assertion.
- No branch commit touches fixture setup. Unit/view tests above cover the display logic.

## Result

- Total actionable: 2 (0 REAL, 1 FALSE POSITIVE, 1 OUT OF SCOPE)
- Fix commit: none (no code change needed)
- Files changed: none beyond rebase
- Recipe re-validation: FAIL at `require-cross` precondition (no live Cross position on dev1); no PR display assertion reached
- Integration status: `rebased` (see `integration-status.txt`); pushed `2204c40070c` with `--force-with-lease` against `9b0472a4d4a`
- Replies: no inline threads to resolve; one consolidated top-level reply posted: https://github.com/MetaMask/metamask-mobile/pull/35831#issuecomment-5666569084
