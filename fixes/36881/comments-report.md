# PR #36881 — pr-complete comments report (round 2)

Branch `TAT-3524-feat-cross-margin-mobile-ui`. Pre-rebase remote head `80a72b69883` (pushed by round 1 on 2026-09-28; round 1 ended `blocked` because mm-6's native build could not parse the branch bundle).

## Triage

Live fetch on 2026-09-29: 2 inline review comments (1 root + own reply), 16 issue comments, 3 reviews. No CHANGES_REQUESTED reviews, no `metamask-flaky-test-detection` comments.

| # | Source | Author | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | review_comment 4110687938 | cursor[bot] | usePerpsProOrderForm.ts (outdated) | REAL | Fixed in 15ab6825f3 in an earlier round. Still present on the rebased head: `useHasExistingPosition.ts:72-74` matches symbol plus `providerId`, and `usePerpsProOrderForm.ts:887` passes `market.providerId`. Already replied (4111117778), thread resolved. No new reply. |
| 2 | issue_comment 5844369405 | deeeed | usePerpsProOrderForm.ts:885 | REAL | Fixed in 9398d2f0e53 in an earlier round. Still present: `usePerpsMarketData.ts:47,100-102` filters by `providerId`. Already answered (5844538507). No new reply. |
| 3 | review 5325190767 | abretonc7s (farmslot incremental review) | — | OUT OF SCOPE | Verdict COMMENT, no findings. Cross-client asks (Core tagging, Extension parity) sit outside this Mobile PR. Own account, no reply. |
| 4 | CI check-pr-max-lines (run 36438237639) | github-actions | — | OUT OF SCOPE | 2332 changed lines against a 1000 limit. The PR merges #36881, #36897 and #36918 into one on purpose (see description), and `size-XL` is already applied. Fixing it means splitting the PR, which is an author/reviewer call, not a review fix. |
| 5 | CI Appium Smoke Android accounts 2/2 + `Check all jobs pass` (run 36438168605) | github-actions | — | OUT OF SCOPE | Infra: `Failed to install Android system image: system-images;android-36;default;x86_64` (`Error on ZipFile unknown archive`) before any spec ran. The aggregate job fails only because of that job. The rebase push re-runs CI. |

Skipped without reply (status-only automation or own comments): 15
- Automation (9): CLA 5831441818, Smart E2E 5831485638, Codecov 5844594095, fixture bot 5845165006 / 5845172803 / 5845776518 / 5845837226, SonarCloud 5872570622 (Quality Gate passed, 97.5% new-code coverage).
- Performance results 5873023683: non-blocking. Both scenarios fail with `no_performance_metrics` and the `main` baseline fails the same scenarios. The one metric over threshold (slow frames, "Perps add funds") is on a flow this PR does not touch.
- Own comments (4): 5845162110, 5845774685 (`@metamaskbot` commands), 5846397436, 5852127495. Own review wrapper 5325638987; cursor[bot] review wrapper 5325164888 holds row 1.

## Integration (step 3)

Rebased 16 commits onto `origin/main` `3b1fd8f99e8` (38 new main commits). No conflicts. `git range-diff 9fea4fe3422..80a72b69883 origin/main..HEAD` shows every PR commit unchanged (`=`). New head `40cdf2f5bce`, linear history.
- Main bumped `@metamask/assets-controller` 17.0.0, `design-system-react-native` 0.51.0, `ramps-controller` 26.0.1, `social-controllers` 3.4.0. `yarn install --immutable` passed. Installed `@metamask/perps-controller` 18.0.1 still carries the `getMarginModeLock` patch.
- PR diff stays at the same 20 files (2309+/45-), all covered by the description.

## Local gate (step 9)

No working-tree changes. `mm-harness check diff` pass on the 20 PR files: ESLint, Prettier, policy suppressions, Jest 7 suites / 467 tests, integration 1 suite / 14 tests. Full TypeScript deferred to CI.

## Recipe re-validation (step 10): PASS 45/45 on `40cdf2f5bce`

Inherited recipe coverage: ac1 (device) Cross selectable, form reads Cross; ac2 (device + Jest) Cross order opens a Cross BTC position, `marginMode` reaches order params; ac3 (Jest) Cross gated off for flag off / HIP-3 / non-HyperLiquid / isolated-only; ac4 (Jest) existing cross position no longer blocks trading.

Runtime: mm-6 dev client was reinstalled 2026-09-29 15:57, so round 1's Hermes/native mismatch is gone. `launch ios --verify` and `doctor --expect-live` both passed.

Attempts:
1. `setup-pro` failed: "Perps did not reach pro mode". The slot `.js.env` had `OVERRIDE_REMOTE_FEATURE_FLAGS="true"`, so `validatedVersionGatedFeatureFlag` returns undefined and Pro mode and Cross can't turn on. Following the repo's documented fix, I commented it out and relaunched through the harness with `--clear-metro` (transform cache only, no native rebuild). Metro then logged "Feature flags updated". I restored `.js.env` to the original afterwards.
2. `ac1-press-cross` failed: Cross rendered with no `onPress`. Live remote config serves `perpsTerminalBackendEnabled` on (`minimumVersion 8.3.0`), and the PR keeps Cross off on the Terminal path until TAT-4022. That is intended behavior and probably what the Jira reporter hit ("even after turning ON the FF for cross margin, I still can't choose cross margin").
3. Recipe delta: `setup-flag` now also pins `perpsTerminalBackendEnabled` off, matching the PR body's evidence conditions. Inherited copy kept as `recipe.inherited.json`. Result: PASS 45/45.

Account state: setup nodes converged BTC to no position and no resting order (matching=0 both). The run opened a 15 USD Cross BTC long (0.00018 BTC), and teardown closed it and asserted flat. Overrides cleared at teardown. Testnet fixture account only, no mainnet mutation.

Evidence (all PNGs read): `evidence-ac1-cross-sheet.png` (Cross selected, no "Coming soon"), `evidence-ac1-cross-label.png` (control reads Cross), `evidence-ac2-cross-position.png` ("Position margin used" tagged Cross, no liquidation price). Jest nodes: ac2 40 passed, ac3 15 passed, ac4 3 passed (`test-logs/`). The recipe's command nodes write logs to `temp/tasks/feat/tat-3524-0925-174920/artifacts/test-logs/`, so I created that missing folder and copied the logs here.

## Replies (step 12)

No new replies. Row 1: already replied (4111117778), thread `PRRT_kwDOCG4DHc6mO8hM` resolved. Row 2: already answered (5844538507). Row 3: own-account review with no findings. Rows 4-5 are CI checks, not comment threads. The rebase push re-runs CI. No duplicate replies posted.

## Summary (step 13)

- Total comments triaged: 5 (2 REAL, 0 FALSE POSITIVE, 3 OUT OF SCOPE). 15 status-only or own comments skipped without reply.
- Fix commit: none this round. Both REAL findings were fixed in earlier rounds and are still present on the rebased head. No-change reason: no open finding needs code.
- Pushed: rebased history `80a72b69883` → `40cdf2f5bce` (`--force-with-lease` against the recorded pre-rebase SHA; remote had not moved).
- Files changed by this run: none beyond the rebase. The PR diff is the same 20 files.
- Recipe re-validation: PASS 45/45 on `40cdf2f5bce` (iOS mm-6, HyperLiquid testnet). Recipe delta: `setup-flag` also pins `perpsTerminalBackendEnabled` off.
- Integration status: `rebased` (see `integration-status.txt`).
- Open items for the author:
  - `check-pr-max-lines` fails by design (2332 > 1000 lines). Either accept it for this consolidated PR or split it.
  - With live remote config, `perpsTerminalBackendEnabled` is on for app >= 8.3.0, so Cross stays unavailable in Pro even with `perpsCrossMarginEnabled` on until TAT-4022 lands or the Mobile `!usesTerminal` gate changes. This matches the Jira comment.
  - The slot's `.js.env` sets `OVERRIDE_REMOTE_FEATURE_FLAGS="true"`, which blocks Pro mode for any Perps Pro recipe on mm-6. I restored it after the run; the running Metro bundle still has the override off until the next cache-cleared launch.
  - Needs an approving review (policy-bot).
