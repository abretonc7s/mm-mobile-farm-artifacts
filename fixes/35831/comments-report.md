# PR #35831 — Comment Triage Report

Branch: `TAT-3519-feat-mobile-pro-cross-margin`
Triaged at HEAD: (see final section)

## Fetch results

- Inline review comments (`pulls/35831/comments`, `in_reply_to_id == null`): **0**
- `CHANGES_REQUESTED` reviews: **0** (no reviews of any state exist on this PR)
- Issue/conversation comments: **7** (5 bot, 2 human — both authored by the PR author in earlier runs)

## Triage table

| # | ID | Author | Source | File | Triage | Action |
|---|----|--------|--------|------|--------|--------|
| 1 | 5578350099 | github-actions[bot] | issue_comment | — | STATUS-ONLY (skipped) | CLA signature status. No reply. |
| 2 | 5581113223 | github-actions[bot] | issue_comment | — | OUT OF SCOPE | Perf test "Perps add funds" quality-gates exceeded on commit `732dc86` (pre-rebase). Explicitly non-blocking; the add-funds flow is untouched by this PR's diff (display-only changes to position cards + a feature-flag selector). |
| 3 | 5581571760 | github-actions[bot] | issue_comment | 5 perps test files | FALSE POSITIVE | Flaky-test detection. The rendered body reports **"All previously detected unit test flakiness issues in this PR have been fixed"** and its metadata block carries `"findings": []` for all five analyzed files. No outstanding finding to fix. |
| 4 | 5581695034 | abretonc7s (PR author) | issue_comment | — | ALREADY HANDLED | Author's own prior triage of #3. Not a reviewer request; no reply (would be self-reply). |
| 5 | 5619337354 | abretonc7s (PR author) | issue_comment | — | ALREADY HANDLED | Author's own prior rebase/blocker-cleared note. Not a reviewer request; no reply. |
| 6 | 5621086006 | github-actions[bot] | issue_comment | — | STATUS-ONLY (skipped) | Smart E2E tag selection summary. No reply. |
| 7 | 5621245345 | sonarqubecloud[bot] | issue_comment | — | STATUS-ONLY (skipped) | **Quality Gate passed** — 0 security hotspots, 98.9% coverage on new code, 0.0% duplication. The 3 "new issues" did not fail the gate and carry no inline comment on this PR. No reply. |

**Skipped without reply (routine status-only automation): 3** (#1 CLA, #6 E2E selection, #7 Sonar gate-passed).

## CI status

Checked via `gh pr checks 35831`. One non-skipped failure:

- **`check-pr-labels` — FAIL:** `PR cannot be merged because it still contains this label: blocked`.
  **Triage: OUT OF SCOPE for a code fix.** The `blocked` label is an intentional author/product hold, consistent with the PR title suffix `[NOT-READY-NEED-DESIGN]`. It is a process gate, not a defect, and removing it is a product decision outside a review-comment worker's remit. No code change can clear it.

All other checks: `Unit tests (0..9)` pass, `Verify feature flags are registered` pass, `Validate E2E Fixtures` pass, Sonar gate pass. `policy-bot` pending; the remaining entries are `skipping`.

## Integration (step 3)

Rebased `TAT-3519-feat-mobile-pro-cross-margin` onto `origin/main` (`91a66f077a`). Six branch commits replayed cleanly, no conflicts, no merge commit. `main` moved `yarn.lock`/`package.json`/`ios/Podfile.lock`, so `yarn install --immutable` was re-run (completed with pre-existing peer warnings only).

Pre-rebase remote SHA: `4d0f2b7f1009ff49d08f0d36759eff01092803bc` (local HEAD matched remote exactly before the rebase).
Integration status: `rebased`.

## Step 6 — fixes applied

**None.** No comment triaged REAL, so no code change was made. Verification that this is not a
premature no-change:

- The flaky-detection metadata block (base64, decoded) reports `findings: []` for **all five**
  analyzed test files, confirming the rendered "all issues fixed" text rather than relying on it.
- Sonar's quality gate **passed** and posted no inline comment.
- The only failing check (`check-pr-labels`) is a label-process gate with no code remedy.

## Step 9 — bounded local CI gate (post-rebase)

Run against the rebased base `91a66f077a`:

| Gate | Result |
|---|---|
| Scoped ESLint `--max-warnings=0` (16 PR files) | **PASS** — no output |
| `yarn lint:tsc` | **PASS** — 0 errors |
| `yarn format:check` | **PASS** — "All matched files use Prettier code style!" |
| Working tree clean (`git status --porcelain`) | **PASS** — empty |
| Affected suites (5 files) | **PASS** — 112/112 tests |

Suites run: `PerpsPositionsView`, `PerpsProPositionCard`, `PerpsCard`,
`PerpsCrossMarginInfoButton`, `PerpsPositionCard`.

## Step 10 — recipe re-validation

Recipe: `artifacts/recipe.json` (present; `RECIPE_SOURCE: family-inherited`, trusted).
Actions used are all standard validation primitives — `metamask.wallet.*`, `ui.navigate|press|scroll|screenshot|wait_for`, `assert_json`, `assert_output`, `command`, `switch`, `end`. No adversarial primitive.

**Inherited AC coverage** (from the recipe description + `inputs/inherited/report.md`): the recipe
proves, on exactly one real Cross position, the Cross badge, the venue liquidation display for both
the null and numeric fixtures, the shared-collateral explanation, and the non-editable "Margin used"
label in both Lite and Pro. Mixed-book grouping, compact rows, and privacy masking are explicitly
delegated to component tests, not to this recipe.

**Runtime health:** UP. `launch ios --verify` passed (13.7s; fixture READY, 4 accounts) and
`doctor --expect-live` reported Metro `up`, device `mm-2` Booted, capture providers available.

**Result: FAIL at the precondition gate — environmental, not a regression.**

| # | Node | Action | Result |
|---|------|--------|--------|
| 1 | `wallet` | `metamask.wallet.read_state` | pass |
| 2 | `account` | `assert_output` | pass |
| 3 | `unlock` | `metamask.wallet.ensure_unlocked` | pass |
| 4 | `environment` | `command` | pass |
| 5 | `positions` | `command` | pass |
| 6 | `require-cross` | `assert_json` | **fail** |

5 passed / 1 failed of 6. The failure is:
`$.positions length_eq 1` against `selected-account-live-positions.json`, which currently holds
`positions: []` (zero open positions on the testnet account).

`require-cross`'s own stated intent is *"Require exactly one live position so shared value selectors
cannot match another market"* — it is a fixture precondition, not an assertion about this PR. Execution
stopped there and **never reached a single node that touches this PR's display code** (`pro-open`,
`pro-scroll`, and every badge/liquidation/margin assertion are downstream of it).

Attribution per step 10's RUNTIME/ASSERT FAIL rule: `git diff origin/main...HEAD --name-only` shows the
branch touches **no** fixture, runtime, or `temp/` data — only perps components, tests, selectors,
locales, and the flag registry. The failure is therefore caused by neither the review fixes (there were
none) nor the rebase. It is the same environmental condition documented in PR comment 5619337354: the
positions used for the original validation were closed at the end of that run. Logged as
**unrelated/environmental**; continuing per the checklist.

## Step 11 — commit and push

**No fix commit created** — no comment triaged REAL, so an empty commit was deliberately avoided.

The rebase from step 3 still needed publishing, so the integrated history was force-pushed under a
lease. Remote was verified unmoved (`4d0f2b7f100` expected == actual) immediately before the push.

- Before: `4d0f2b7f1009ff49d08f0d36759eff01092803bc`
- After:  `9b0472a4d4ad6e1981d9be1af041e3fa7b01c8b6`

No leftover lint changes; working tree clean after push.

## Step 12 — replies

- **Inline review comments: none exist**, so no inline replies were posted and no review threads were
  resolved. GraphQL `reviewThreads` returns **0** nodes — nothing to pass to `resolveReviewThread`.
- **One consolidated top-level response posted** covering the flaky-detection finding (FALSE POSITIVE,
  verified via decoded metadata), the performance-test failure (OUT OF SCOPE), the Sonar gate, the
  post-rebase gate results, the recipe precondition failure, and the intentional `blocked` label:
  https://github.com/MetaMask/metamask-mobile/pull/35831#issuecomment-5632089383
- **No reply** to comments 5581695034 and 5619337354 — both are the PR author's own earlier triage
  notes, not reviewer requests; replying would be a self-reply.
- **No reply** to the 3 routine status-only automation comments (CLA, Smart E2E selection, Sonar
  gate-passed).

---

## Final summary

- **Total comments triaged: 7** — 0 REAL, 1 FALSE POSITIVE (flaky detection), 1 OUT OF SCOPE
  (performance test), 2 already-handled author notes, 3 status-only automation skipped without reply.
- **Inline review comments: 0. `CHANGES_REQUESTED` reviews: 0.**
- **Commit SHA for fixes: none** — no code change was required, so no empty commit was created.
- **Files changed this run: none.** Branch content is unchanged; only its base moved.
- **Branch tip:** `9b0472a4d4ad6e1981d9be1af041e3fa7b01c8b6` (was `4d0f2b7f1009ff49d08f0d36759eff01092803bc`).
- **Recipe re-validation: FAIL (environmental).** Stops at the `require-cross` fixture precondition —
  zero open positions on the testnet account. 5/6 nodes pass; no assertion on this PR's code was
  reached. Not attributable to the branch or the rebase.
- **Integration status (step 3): `rebased`** onto `origin/main` `91a66f077a`, clean, linear, no merge
  commit; `yarn install --immutable` re-run for the lockfile move.
- **Local CI gate: all green** — ESLint, `lint:tsc`, `format:check`, clean tree, 112/112 tests.
- **Remaining merge blocker:** `check-pr-labels` fails on the intentional `blocked` label, matching
  the `[NOT-READY-NEED-DESIGN]` title. Product hold, deliberately left in place.
