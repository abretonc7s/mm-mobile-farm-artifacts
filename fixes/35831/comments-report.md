# PR #35831 — Comment Triage Report

Branch: `TAT-3519-feat-mobile-pro-cross-margin`
PR: feat(perps): mobile | Pro mode | Cross margin
Verified against post-rebase HEAD (rebased onto `origin/main` @ `9e21342485`).

## Comment inventory

Fetched live from all three endpoints:

- Inline review comments (`/pulls/35831/comments`): **0**
- REQUEST_CHANGES reviews (`/pulls/35831/reviews`): **0**
- Issue/conversation comments (`/issues/35831/comments`): **6**

### Skipped as status-only automation (4, no reply posted)

| id | author | kind |
|---|---|---|
| 5578350099 | github-actions[bot] | CLA signature status |
| 5581113223 | github-actions[bot] | Performance test results (explicitly non-blocking) |
| 5581569439 | github-actions[bot] | Smart E2E test selection |
| 5581664028 | sonarqubecloud[bot] | Sonar Quality Gate — passed |

### Triaged

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | github-actions[bot] (5581571760, J4) | PerpsPositionsView.test.tsx:56 | FALSE POSITIVE | No `waitFor(() => {})` exists; all 16 `waitFor` callbacks carry `expect` assertions |
| 2 | github-actions[bot] (5581571760, J3) | PerpsProPositionCard.test.tsx:12 | FALSE POSITIVE | `beforeEach` (35–38) restores the one mutated mock (`useSelector`); `resetAllMocks()` would strip module-factory implementations |
| 3 | github-actions[bot] (5581571760, J3) | PerpsCard.test.tsx:12 | FALSE POSITIVE | `beforeEach` (69–92) restores `useSelector` and `mockUsePerpsMarkets`; `resetAllMocks()` would erase the markets factory |
| 4 | github-actions[bot] (5581571760, J4) | PerpsCrossMarginInfoButton.test.tsx:12 | FALSE POSITIVE | File imports and calls no `waitFor` at all; there is no empty callback to replace |
| 5 | github-actions[bot] (5581571760, J3) | PerpsPositionCard.test.tsx:12 | FALSE POSITIVE | `beforeEach` (206–259) restores theme, PnL, markets, live prices and selectors; `resetAllMocks()` would erase all of them |
| 6 | abretonc7s (5581695034) | conversation | ALREADY REPLIED | Author's own prior triage of 5581571760, same dispositions. No new reply — see "Reply policy" below |

Totals: **6 triaged — 0 REAL, 5 FALSE POSITIVE, 1 already-replied (own comment)**; 4 status-only automation skipped without reply.

## Independent verification (not taken on trust from the prior triage)

Counted against current HEAD source rather than relying on the historical 0-failure rate:

```
PerpsPositionsView.test.tsx        empty waitFor: 0   waitFor total: 16
PerpsProPositionCard.test.tsx      empty waitFor: 0   clearAllMocks: 1
PerpsCard.test.tsx                 empty waitFor: 0   clearAllMocks: 1
PerpsCrossMarginInfoButton.test.tsx empty waitFor: 0  waitFor total: 0
PerpsPositionCard.test.tsx         empty waitFor: 0   clearAllMocks: 1
```

Each `beforeEach` was read in full. In all three J3 files the mock return values the tests mutate are
explicitly re-established after `clearAllMocks()`. `jest.resetAllMocks()` additionally wipes
implementations installed by `jest.mock` module factories (`mockUsePerpsMarkets`, `mockUseTheme`,
`usePerpsLivePrices`, the event-tracking factory), which the `beforeEach` blocks do not all
reinstall — so the suggested fix would break these suites rather than stabilize them.

## Dependency blocker — now resolved by the step 3 rebase

The prior conversation comment recorded Mobile as blocked on Core #10136 for four missing
`ORDER_MARGIN_MODE_*` constants. That is no longer true:

- `origin/main` bumped `@metamask/perps-controller` `^16.1.0` → `^16.2.0`.
- Installed `@metamask/perps-controller@16.2.0` exports all four constants
  (`perpsErrorCodes.d.cts:44-47`), and its CHANGELOG credits Core #10136.
- The rebase + `yarn install --immutable` brought that release into this checkout, so the
  typecheck failure cited in the earlier comment is cleared. No `package.json`/`yarn.lock`
  change is needed in this PR's own diff — main already carries it.

## Reply policy

Comment 6 is the PR author's own triage covering exactly the same five findings with the same
dispositions, already posted against the pre-rebase SHA. Per the "do not post a second reply for the
same current-HEAD resolution" rule, no duplicate triage is posted. One short top-level follow-up is
posted instead, reporting only what changed since that comment: the rebase and the now-resolved
Core dependency blocker.

## Local CI gate (step 9) — post-rebase

| Check | Result |
|---|---|
| Scoped ESLint (`--max-warnings=0`, 13 changed files) | PASS (exit 0) |
| `yarn lint:tsc` | PASS (exit 0, zero errors) |
| `yarn format:check` | PASS — all matched files use Prettier style |
| Working tree clean (`git status --porcelain`) | PASS — empty |
| Affected unit tests (5 suites) | PASS — 110/110 tests, 5/5 suites |

The `lint:tsc` pass is the direct evidence that the `ORDER_MARGIN_MODE_*` blocker recorded in
comment 5581695034 is cleared on the rebased branch.

## Recipe re-validation (step 10) — BLOCKED ON FIXTURE, unrelated to this branch

Recipe: `artifacts/recipe.json` — "Existing cross-position display in Lite and Pro"
(family-inherited, `RECIPE_SOURCE: family-inherited`, trusted; 42 nodes; action mix is normal
validation flow — `ui.*`, `assert_json`, `metamask.wallet.*`, plus two `command` nodes that both
invoke the in-repo `selected-account-cross-setup.ts inspect` probe. No arbitrary-code or
exfiltration primitive present.)

### Inherited AC coverage (step 10b)

From `inputs/inherited/report.md` and the recipe description, the inherited recipe covers:
Cross badge in Lite and Pro cards, venue liquidation display for both the null and numeric
branches, the shared-collateral explanation, and non-editable "Margin used". Explicitly **not**
covered by the recipe and deferred to component tests: mixed-book, compact-row and privacy
behavior.

### Runtime health — PASS

- `mm-harness launch ios --verify` — exit 0, bundle rebuilt against the rebased tree,
  `Mobile bridge ready (17.5s)`, `verify mobile passed (20.7s)`, fixture `READY (accounts=4)`.
- `mm-harness doctor --expect-live --json` — exit 0, `status: pass`, 5/5 checks pass.

So the runtime was live and healthy; this is not a "runtime unavailable" skip.

### Result: FAIL at precondition gate — environmental, not a code regression

```
node:    require-cross   (4th node; entry wallet → account → environment → positions → require-cross)
assert:  $.positions length_eq 1
actual:  "positions": []   (fixture recaptured live at 2026-09-10T13:18:00Z)
error:   APP_LOGIC_FAILURE
```

Causation analysis per step 10's RUNTIME/ASSERT FAIL rule:

- The gate fails **before** any node that touches the PR's code — no badge, liquidation,
  explanation or margin-label assertion was ever reached.
- The failing node reads `temp/tasks/feat/.../selected-account-live-positions.json`. **Zero**
  commits on this branch touch that path, and it is not in the PR diff.
- Not caused by the review fixes: there are no review fixes (0 REAL findings, no code change).
- Not caused by the step 3 merge from main: the failing assertion is on live venue account
  state, not on any file main changed.

Root cause: the recipe requires exactly one **real** open Cross position on testnet account
`0x8dc6…9003`, and that account currently holds none. The PR body records that the positions used
for the original validation were deliberately closed after that run ("Both were closed and ETH was
restored to isolated 3x"), so the fixture precondition can no longer be met without re-opening a
real leveraged testnet position.

Disposition: logged as **unrelated/environmental**, continuing per step 10's explicit instruction
for a failing step unrelated to anything in this branch. Re-establishing a live leveraged position
is a financial mutation outside the scope of a comment-triage run and is not requested by any
comment. The PR's display behavior remains covered by the 110 passing component tests in step 9.

Run artifacts: `artifacts/recipe-run/summary.json`, `artifacts/recipe-run/trace.json`.

## Replies posted (step 12)

- Inline `review_comment` replies: **none** — the PR has zero inline review comments and zero
  REQUEST_CHANGES reviews, so no inline reply and no `resolveReviewThread` mutation applies.
  (Issue comments are not review threads and were correctly not passed to that mutation.)
- Consolidated top-level response: https://github.com/MetaMask/metamask-mobile/pull/35831#issuecomment-5619337354
  Reports the rebase, the cleared Core dependency blocker with typecheck evidence, the post-rebase
  gate results, the re-verified five flaky dispositions, and the recipe fixture gap.
- No duplicate of the author's existing five-finding triage (5581695034) was posted; the new comment
  covers only what changed since it.
- Status-only automation (CLA, performance, E2E selection, Sonar): 4 comments, no reply posted.

---

## Final summary (step 13)

- **Total comments: 10** — 6 issue comments (4 status-only automation skipped without reply,
  1 actionable bot finding-set, 1 pre-existing author triage) + 0 inline review comments + 0 reviews.
- **Triaged: 6 → 0 REAL, 5 FALSE POSITIVE, 0 OUT OF SCOPE, 1 already-replied.**
- **Commit SHA for fixes: none** — no REAL findings, so no fix commit was created and no empty
  commit was made.
- **Pushed:** `fc11c3ec0cc` → `9e350ce121d` (force-with-lease, rebased history only).
- **Files changed by this run: none.** The branch diff is unchanged from the pre-rebase content;
  only the base moved.
- **Recipe re-validation: FAIL (unrelated/environmental)** — precondition gate `require-cross`
  (`$.positions length_eq 1`) against a live testnet account holding zero positions. Fails before
  reaching any PR code; no branch commit touches the fixture. Runtime itself was live and healthy.
- **Integration status:** `rebased` (see `artifacts/integration-status.txt`).
- **Dependency blocker cleared:** `@metamask/perps-controller@16.2.0` from main supplies the four
  `ORDER_MARGIN_MODE_*` constants; `lint:tsc` exits 0.
