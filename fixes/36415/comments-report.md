# PR #36415 — review comment triage

Branch rebased onto `origin/main` (`3bf04be0e1`) before triage; `yarn install --immutable` re-run because main moved `package.json` / `yarn.lock`.

| # | Author | Source | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | geositta | review_comment 4039699306 | app/components/Views/ActivityDetails/hooks/usePerpsActivityQuery.ts:165 | REAL | Remove the `flattenFills` dedupe; add a regression test for two identical same-order fills |
| 2 | geositta | review_comment 4039699316 | app/components/UI/Perps/utils/transactionTransforms.ts:544 | REAL | Derive unaggregated row ids from fill content + occurrence index instead of `acc.length`; add a prepend-stability test |
| 3 | geositta | review_comment 4039699325 | app/components/UI/Perps/components/PerpsAggregatedFillsCheckbox/PerpsAggregatedFillsCheckbox.tsx:33 | REAL | Rebuild on the design-system `Checkbox`; assert role and checked state |
| 4 | geositta | review_comment 4039699332 | app/components/Views/ActivityDetails/hooks/usePerpsActivityQuery.ts:180 | REAL | Replace the positional boolean with `{ fillDisplay: 'aggregated' \| 'individual' }` |
| 5 | cursor[bot] | review_comment 4036848796 | usePerpsActivityQuery.ts:246 | REAL (already fixed) | Fixed in an earlier round; thread already has a reply — no second reply |
| 6 | cursor[bot] | review_comment 4037178393 | usePerpsDetailsItem.ts:69 | REAL (already fixed) | Fixed in an earlier round; thread already has a reply — no second reply |

## Issue comments (no reply posted)

Status-only automation, skipped without replying: CLA signature (5714391821), PR template checks (5714398357), Codecov summary (5714575529), Smart E2E selection (5717182434), SonarQube quality gate passed (5717406338).

Performance test results (5717575296) — non-blocking, both failures are `no_performance_metrics` (BrowserStack failed to collect) on `Perps add funds` and `Perps open position and close it`, neither of which touches the activity list this PR changes. Recorded, no reply.

## Recipe re-validation (step 10)

`RECIPE_SOURCE=pr-body-llm`. Trust gate cleared before promotion: `inputs/inherited/recipe-source.json` reports `pr-body-llm-extracted-untrusted`; the staged recipe has one `command` node, and it runs `yarn jest` on a repo test file writing to `temp/tat-3932/artifacts/`. No env probing, no credential access, no writes outside the repo, no non-MetaMask hosts. Every other node is `ui.*`, `app.*`, `metamask.wallet.ensure_unlocked`, `assert_exit_code`, `index_artifacts`. Promoted to `artifacts/recipe.json` and executed. No dependency recipe library was staged.

Inherited AC coverage: AC1 — aggregation on/off fill grouping, proved by the transform unit tests (`ac1-run-transform-tests` + `assert_exit_code`); AC2 — the Aggregated control is present on Activity > Perps > Trades and switches the list between one row per order and one row per execution, proved live on the iOS slot with a screenshot in each state.

Account state (step c2): the recipe needs trade *history* with multi-fill orders on the slot fixture account (`0x316b…01fa`, Hyperliquid testnet), not live positions, so there was nothing to converge. Nothing was closed or cancelled. The `metamask.perps.read_positions` probe returned `CLIENT_NOT_INITIALIZED` because the app sits at Login before the recipe's own unlock step; it is not a state signal.

Runtime notes: `mm-harness launch ios --verify` reported the bridge ready but its own internal smoke recipes failed the harness trust gate (`RECIPE_TRUST_REQUIRED` on bundled `app.status` / `cdp.target`). `mm-harness doctor --expect-live` passed (runtime ready, device `mm-1` booted, fixture READY), so the runtime was healthy and the recipe was run with the reviewed plan digest approved (`FARMSLOT_RECIPE_APPROVE_PLAN`). Two throwaway attempts failed first on a flaky wallet unlock (`keyringUnlocked: true`, route stuck on `Login`) and then on a 60s Metro bundle timeout while Metro rebundled the edited files; after the bundle warmed (93s), the run passed.

**Result: PASS — 18/18 nodes.** Artifacts: `artifacts/recipe-run/report.md`, screenshots `evidence-ac2-aggregated-on.png` / `evidence-ac2-aggregated-off.png`. The screenshots confirm the rebuilt design-system control still renders as a pill in both states and that unchecking still splits the orders the PR documents (0.00179 → 0.00163 + 0.00016, 0.00128 → 0.00125 + 0.00003).
## Summary

Total comments triaged: 6 inline review comments (6 REAL, 0 FALSE POSITIVE, 0 OUT OF SCOPE). Two of them (cursor[bot] 4036848796, 4037178393) were already fixed and replied to in earlier rounds — no second reply posted, threads left as they were.

Six issue comments reviewed; all status-only automation or non-actionable infra, none replied to.

- **Commit:** `a8bbe15e6f` — `fix: address review comments on PR #36415`
- **Files changed:**
  - `app/components/UI/Perps/components/PerpsAggregatedFillsCheckbox/PerpsAggregatedFillsCheckbox.tsx` (+ test)
  - `app/components/UI/Perps/utils/transactionTransforms.ts` (+ test)
  - `app/components/Views/ActivityDetails/hooks/usePerpsActivityQuery.ts` (+ test)
  - `app/components/Views/ActivityDetails/templates/Perps/usePerpsDetailsItem.ts` (+ test)
  - `app/components/Views/ActivityList/hooks/usePerpsActivityItems.ts` (+ test)
- **Local gate:** scoped ESLint `--max-warnings=0` clean, `yarn lint:tsc` clean, `yarn format:check` clean, 238 unit tests + 78 view tests passing across the touched suites.
- **Recipe re-validation:** PASS (18/18 nodes) against branch rebased onto `origin/main`.
- **Integration status (step 3):** `rebased` — 4 branch commits replayed onto `3bf04be0e1`, no conflicts, `yarn install --immutable` re-run.
- **Replies posted:** 4042706578, 4042707077, 4042707601, 4042708088. All four geositta threads resolved.
