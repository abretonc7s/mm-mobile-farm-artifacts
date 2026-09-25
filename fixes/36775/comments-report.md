# Comments report — PR #36775 (round 2, 2026-09-25)

## Summary
- Total comments: 2 (2 REAL, 0 FALSE POSITIVE, 0 OUT OF SCOPE)
  - #1 GitHub bugbot thread: already fixed, replied and resolved in round 1.
  - #2 private Codex gpt-6-sol review of b146b0351f5 (P2, operator-relayed, not posted): fixed this round.
- Fix commit: b729f32d3c3 (pushed with lease over 62485907023)
- Files changed by the fix: PerpsAdjustMarginView.tsx (+test), PerpsAdjustMarginBottomSheet.tsx (+test), usePerpsAdjustMarginData.ts
- Recipe re-validation: PASS 104/104 (`artifacts/recipe-run/report.md`)
- Integration status: rebased (`artifacts/integration-status.txt`)
- Independent review on final HEAD b729f32d3c3: Codex gpt-6-sol, VERDICT: APPROVE, no findings (`artifacts/codex-review-b729f32d3c3.md`)

## Triage

| # | Source | Author | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | review_comment 4091373443 | cursor[bot] | PerpsAdjustMarginView.tsx (fresh cap resets on PnL ticks) | REAL (already fixed) | Fixed in c556868d643 / 6421cb99d5b, two replies, thread resolved. Already replied; no new reply. |
| 2 | private review, Codex gpt-6-sol at b146b0351f5 (operator handoff, stash 2a70d5029a4) | operator-relayed | PerpsAdjustMarginView.tsx, PerpsAdjustMarginBottomSheet.tsx | REAL | An already-open keypad (and % buttons) stayed active when the live limit fell to zero. Both screens now clear input focus on that transition. Fixed in b729f32d3c3. Not a GitHub comment, so no reply. |

No new GitHub review comments or reviews since round 1. Skipped 4 status-only automation comments without reply (CLA, smart-e2e selection, SonarCloud passed, non-blocking perf results: 2 × `no_performance_metrics` on Android, no flaky-test marker).

## Integration (step 3)
- Remote head was a merge of main into the branch (62485907023, saved locally at refs/farmslot/recovery/tat3985-local-merge-20260925). Rebased linearly onto origin/main 7fcc3ab7b6a: 14 commits replayed, merge commit dropped.
- One stop at 8585cae (`Perps.testIds.ts`, `PerpsAdjustMarginBottomSheet.tsx` vs main's `PerpsInlineInfoScreen`); rerere reapplied the merge's resolution.
- Rebased tree identical to `git merge-tree 62485907023 origin/main` (empty diff). `yarn install --immutable` after the lockfile change on main.

## Keypad fix (operator handoff)
- Applied stash@{0} (2a70d5029a4) with `git stash apply` on the rebased branch; clean, stash kept.
- Change: `useEffect` closing the keypad when `hasNoRemovableMargin` in both screens; one transition test per screen; the two max-amount memos in `usePerpsAdjustMarginData` folded into one (no behavior change).
- Unit negative control: with the effect removed, both new tests fail (2 failed); with it, 245/245 across the 7 focused suites.
- PR size: +934/−64 = 998 counted lines (CI limit 1000; nothing in the diff matches the ignore patterns). Leaves 2 lines of headroom.

## Local gate (step 9)
- ESLint (PR files + fix files): pass. Prettier / `yarn format:check`: pass. Focused Jest: 245/245.
- Full `yarn lint:tsc` not run: slot rules forbid full-project TypeScript from the worker pane; left to CI (it passed on the equivalent merge tree 62485907023).

## Recipe re-validation (step 10)
- `artifacts/recipe.json` had reverted to the stale inherited copy (cross-margin nodes from #36782); kept as `recipe.stale-inherited.json`. Promoted round 1's passing recipe (AC1–AC5, 92 nodes) and extended AC4/AC5 in place: after Max is retained and validated, reopen the keypad (`*-reopen-keypad`, `*-wait-keypad-open`), drain, then `*-assert-keypad-closed` before the existing explanation/no-stale-error asserts. 98 nodes.
- Result: PASS 104/104 in 280s. AC4 and AC5: keypad visible before drain, absent after, explanation visible, no stale error. Screenshots: `recipe-run/screenshots/ac4-screenshot.png`, `ac5-screenshot.png`.
- Live negative control: full-screen effect removed, app restarted, single-leg probe `probes/p4-keypad.json` → FAIL at `ac4-assert-keypad-closed` (keypad still open 15s after drain), 33/34 (`probes/neg-p4-keypad-run`). Source restored, app restarted, doctor pass, tree clean.
- Failed attempts kept for the record (all environmental, none reached a proof node):
  - attempt 1: invalidated because the local commit was made mid-run (product.status changed).
  - attempt 2 (`recipe-run.attempt2-source-not-loaded.log`): MOBILE_SOURCE_NOT_LOADED. `launch --verify` then showed a bundle failure: Metro's file map missed `@metamask/subscription-controller/dist/index.js` (on disk) after `yarn install`. Recovered with the checklist's single `--clear-metro` launch retry, then `app.lifecycle restart` and doctor pass, as the operator asked.
  - attempts 3–4 (`recipe-run.attempt3-bridge-timeout*`, `recipe-run.attempt4-cdp-timeout*`): CDP timeouts during setup with machine load ~17 (other slots). The bridge answered in <1s afterwards.
- Account state (Trading, testnet): BTC isolated long opened by `setup-assert-position` (the round-1 fixture position was gone); margin added then drained by AC1/AC4/AC5 and the negative probe; SOL opened and closed by the recipe. A pre-existing ETH position was left untouched (possibly another slot's).
