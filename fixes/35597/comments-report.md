# PR #35597 — comment triage (pr-complete pass)

Fetched live at pr-complete time: **0 inline review comments**, **0 CHANGES_REQUESTED reviews**,
7 conversation comments (5 bot, 2 authored by me in earlier CI-fix passes).

## Triage

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | github-actions[bot] `5508248020` | — | status-only | CLA signature status. Skipped, no reply. |
| 2 | github-actions[bot] `5508283360` | — | status-only | Smart E2E Test Selection output. No suggestion to act on. Skipped, no reply. |
| 3 | github-actions[bot] `5508297311` | `PerpsOrderView.test.tsx` | FALSE POSITIVE | Flaky-test J9. Already triaged and answered in `5508433699`. Bindings it names are reset in the global `beforeEach` at `:1047`/`:1049` and a describe-scoped `beforeEach` at `:2311-2312`. Underlying order-dependence is pre-existing on `main` and filed as TAT-3910. |
| 4 | sonarqubecloud[bot] `5508399788` | — | status-only | Quality Gate **passed**, 0 new issues, 100% coverage on new code. Skipped, no reply. |
| 5 | abretonc7s `5508433699` | — | own reply | My J9 triage from an earlier CI-fix pass. Not an incoming review comment. |
| 6 | github-actions[bot] `5508492087` | `tests/performance/login/perps-add-funds.spec.ts` | FALSE POSITIVE | Perf quality gate on `Perps add funds`. Failing step is `Get Quote` (8301ms vs 7700ms). The spec ends at the quote and never confirms the deposit, so neither changed line executes. Already answered in `5508703825`. |
| 7 | abretonc7s `5508703825` | — | own reply | My performance triage from an earlier CI-fix pass. Not an incoming review comment. |

**Counts:** 0 REAL, 2 FALSE POSITIVE, 0 OUT OF SCOPE, 3 status-only skipped without reply,
2 entries are my own prior replies.

No new reviewer feedback has arrived since those replies were posted, so there is no code change to
make in this pass. The only work is the step-3 integration.

## Integration

`origin/main` moved from `3725c08f67f` to `9128899f301`. The branch was **rebased** (5 commits
replayed, no conflicts, linear history preserved). No `yarn.lock`, `package.json`, `Podfile.lock` or
`build.gradle` changes came in with the merge, so no reinstall was needed.

New SHAs after rebase:

```
8837af43894 fix: address self-review feedback (TAT-3906)
357ff44aa91 fix(perps): pop back to the caller screen after placing an order or adding funds
2f78da71cbe cleanup(tat-3906): remove reproduction marker
380acdffd40 debug(tat-3906): add reproduction marker
f285a3e0807 fix(perps): Navigation bug: back button in BTC lite screen ...
```

## PR state at fetch time

Open, `MERGEABLE`, `reviewDecision: REVIEW_REQUIRED`, no failing checks.

## Step 10 — recipe re-validation (post-rebase)

Recipe source is `family-inherited`, so it was executed as-is; `artifacts/recipe.json` is
byte-identical to the family recipe (`diff -q` clean, 20 nodes). No migration was needed.

Inherited AC coverage (`inputs/inherited/recipe-coverage.md`): **2/2 ACs PROVEN**.
- AC1 (TAT-3906 / TAT-3838): Lite BTC order placed through visible controls, then Back must reach
  Perps home and the order form must be absent. Proof mode mixed, with before/after screenshots.
- AC2 (TAT-3874): Pro add-funds return path, proven by unit tests run inside the recipe with an
  asserted exit code. Live device proof recorded UNTESTABLE (needs a funded Arbitrum Sepolia
  deposit, an external mutation with no funding consent in this slot).

Runtime health: `launch ios --verify` passed (98.0s), `doctor --expect-live` returned
`status: pass`, `devServer: up`.

**Result: PASS** — `mm-harness run` exit 0, all 20 nodes `ok: true`, against the branch rebased onto
`origin/main@9128899f301`. That covers the merge from step 3 as well as the branch's own changes.

## Step 11 — no commit, no push (deliberate)

**No commit:** 0 REAL comments, so there is nothing to fix. No empty commit was created.

**No push, by operator decision.** Step 11 prescribes `git push --force-with-lease` whenever step 3
rebased, but `CLAUDE.local.md` carries a standing "Never force-push" rule. Publishing the rebase
requires a force push, because the branch's 5 commits were rewritten
(`132af96bbac` → `8837af4389`). I put the conflict to the operator and they chose to keep the
remote at `132af96bbac`.

Reasons that supported it:
- The PR is already `MERGEABLE` against `origin/main`; the rebase is not required to merge.
- The remote SHA has green CI and fully triaged bot comments. Force-pushing invalidates that CI and
  re-triggers every check, including the flaky `Perps add funds` perf gate and the flaky-test
  detector, both of which were already triaged as not caused by this PR.
- My two triage replies cite `132af96` as the analyzed SHA. Rewriting it would make them stale.

**The rebase still produced real information, and it is good news.** The branch was rebased locally
onto `origin/main@9128899f301` (155 files of main moved underneath it, +16804/-1184) and everything
was re-validated on that merged tree:

- Scoped ESLint on the 5 changed files: 0 errors (7 pre-existing warnings, unchanged).
- Prettier: clean.
- Language-server diagnostics on both changed source files: no errors.
- `PerpsOrderView.test.tsx` + `perpsModeSwitch.test.ts` + `useTransactionConfirm.test.ts`:
  **200 passed**.
- Inherited recipe: **exit 0, 20/20 nodes green** on the rebased tree.

So the branch is verified compatible with current `main` even though that state is not published.

**Local vs remote divergence:** local `HEAD` is `8837af4389` (rebased); remote is `132af96bbac`.
Whoever merges can either let GitHub rebase/squash at merge time or re-run this step with an
explicit force-push approval.

`yarn lint:tsc` was not run: `CLAUDE.local.base.md` forbids full-project TypeScript from a worker
pane. Language-server diagnostics covered the changed files; the authoritative signal is the PR's
own `lint:tsc` check, which is currently green on `132af96bbac`.

## Step 12 — replies

No new replies posted. Both actionable bot findings already have consolidated responses from
earlier CI-fix passes:
- Flaky-test J9 → https://github.com/MetaMask/metamask-mobile/pull/35597#issuecomment-5508433699
- Performance quality gate → https://github.com/MetaMask/metamask-mobile/pull/35597#issuecomment-5508703825

There are no inline review threads on this PR, so nothing to resolve via GraphQL. Re-posting the
same triage would be noise.

## Step 13 — totals

- Total comments fetched: 7 conversation, 0 inline, 0 CHANGES_REQUESTED reviews.
- Triaged: 5 bot comments — **0 REAL, 2 FALSE POSITIVE, 3 status-only skipped**.
- Excluded from `comments-triage.json`: comments `5508433699` and `5508703825`, which are my own
  triage replies from earlier CI-fix passes, not incoming reviewer feedback.
- Commit SHA for fixes: none (no REAL comments).
- Files changed this pass: none.
- Recipe re-validation: **PASS** (20/20 nodes, exit 0, on the rebased tree).
- Integration status (`artifacts/integration-status.txt`): `rebased` locally onto
  `origin/main@9128899f301`, **not published** — see step 11.
