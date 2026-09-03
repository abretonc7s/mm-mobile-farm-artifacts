# PR #35663 — Review comment triage

Branch rebased onto `origin/main` (6766f343c8) before any fix work; integration status: `rebased`.

Reviewer `geositta` left a `CHANGES_REQUESTED` review (id 5097946487) with 5 inline comments.
All 5 are REAL.

| # | ID | Author | File | Triage | Action |
|---|----|--------|------|--------|--------|
| 1 | 3921202930 | geositta | app/components/UI/Perps/utils/triggerOrderValidation.ts:364 | REAL | Use `>=` / `<=` so an endpoint resting exactly at best ask/bid is treated as taker execution; add exact-boundary tests both directions |
| 2 | 3921202942 | geositta | .../usePerpsProOrderForm.ts:1321 | REAL | Drop the mid fallback; reference is `number \| undefined` and the warning is suppressed until the relevant book side arrives |
| 3 | 3921202948 | geositta | app/components/UI/Perps/utils/triggerOrderValidation.ts:369 | REAL | Require both endpoints to parse before computing the crossing count, so a half-entered ladder produces no partial copy |
| 4 | 3921202951 | geositta | locales/languages/en.json:1748 | REAL | Reword the two new scale strings to taker-execution language; scale rungs stay GTC limit orders |
| 5 | 3921202954 | geositta | .../usePerpsProOrderForm.ts:2407 | REAL | Remove the duplicate submit-time snapshot plumbing and rely on the stream-driven price-card warning |

## Issue comments

| ID | Author | Type | Disposition |
|----|--------|------|-------------|
| 5520232054 | github-actions[bot] | CLA status | Status-only automation — skipped, no reply |
| 5520250746 | github-actions[bot] | Smart E2E test selection | Status-only automation — skipped, no reply |
| 5520252716 | github-actions[bot] | Flaky unit test detection | Already triaged by the author in 5520330778 (both findings false positive, evidence posted); no further reply |
| 5520313021 | sonarqubecloud[bot] | Quality gate | Status-only automation — skipped, no reply |
| 5520330778 | abretonc7s | Author's own flaky triage reply | Own comment, no reply |

3 status-only automation comments skipped without replying.

## Recipe re-validation

Inherited recipe (`family-inherited`, trusted) re-run against `branch + origin/main` after the fixes.

**Result: PASS — 26/26 nodes, exitCode 0, 92.6s.** Matches the inherited baseline node count exactly.

Inherited AC coverage (from `inputs/inherited/recipe-coverage.md`), all still covered:

| AC | Claim | Nodes | Status |
|----|-------|-------|--------|
| 1 | Long scale order crossing the best ask warns | `full-start` → `expect-full-above` | PASS |
| 2 | Short scale order crossing the best bid warns with mirrored copy | `short-start`, `short-end` → `expect-full-below` | PASS |
| 3 | Partly-crossing ladder gets distinct copy from a fully-crossing one | `partial-end` → `expect-partial-above` vs `expect-full-above` | PASS |
| 4 | Warning re-evaluates on endpoint edit and on side flip | `expect-quiet` → `expect-partial-above` → `expect-full-above`; `flip-short` → `expect-cleared-on-flip` | PASS |
| 5 | Warning is non-blocking | `expect-still-placeable` + all three screenshots | PASS |

AC 4's submit-time half is no longer a partial caveat — comment 5 removed that path entirely, so
AC 4 is now fully the stream-driven behaviour the recipe asserts.

Three `ui.wait_for` assertion texts were updated to match the reviewer-requested copy from comment 4
(`expect-partial-above`, `expect-full-above`, `expect-full-below`). Text-only change: node IDs, order,
testIDs, intents, and screenshot nodes are untouched.

Side findings (4, non-blocking, unrelated to this PR): a reselect identity-function warning from
`AccountGroupBalance` and a `MoneyAccountBalanceService:getMoneyAccountBalance` RPC 401 —
neither is on the perps scale-order path.

## Summary

- **Total actionable comments: 5** — 5 REAL, 0 FALSE POSITIVE, 0 OUT OF SCOPE.
- 5 issue comments seen: 3 status-only automation skipped without reply (CLA, Smart E2E selection,
  SonarQube quality gate), 1 flaky-test detection already triaged by the author, 1 the author's own reply.
- **Commit SHA: `50753638e5`** — `fix(perps): tighten scale crossing warning per review`.
- Pushed with `--force-with-lease` (branch was rebased in step 3).
- All 5 inline threads replied to and resolved.

### Files changed by the fixes

| File | Change |
|---|---|
| `app/components/UI/Perps/utils/triggerOrderValidation.ts` | Inclusive crossing comparison, `referencePrice: number \| undefined`, both-endpoints-valid gate, scale-specific full-ladder string keys |
| `app/components/UI/Perps/utils/triggerOrderValidation.test.ts` | New exact-boundary tests both directions, half-entered-ladder cases, unavailable-quote case; updated expected keys (71 → 79 tests) |
| `.../PerpsProOrderForm/usePerpsProOrderForm.ts` | Reference memo returns `undefined` instead of mid; submit-time re-check and its three snapshot fields removed |
| `locales/languages/en.json` | Taker-execution wording; two new `scale_price_above/below_warning` keys |
| `temp/tasks/.../artifacts/recipe.json` | Three `ui.wait_for` assertion texts updated to the new copy (task artifact, not shipped) |

### Validation

| Gate | Result |
|---|---|
| Scoped ESLint (`--max-warnings=0`, 3 changed TS files) | PASS |
| `yarn format:check` | PASS |
| TypeScript diagnostics on the 3 changed files (scoped program, project tsconfig) | 0 errors |
| `yarn jest triggerOrderValidation.test.ts` | 79 passed |
| `yarn jest usePerpsProOrderForm.test.ts` | 271 passed |
| Recipe re-validation (`branch + origin/main`) | PASS, 26/26 nodes |
| Working tree after commit | clean |

Full-project `tsc` was not run: worker slots are barred from repo-wide typecheck (CLAUDE.local.md);
the scoped program above type-checked the changed files against the project's own tsconfig, and CI
runs the full matrix.

**Integration status: `rebased`** — branch replayed onto `origin/main` at `6766f343c8`, linear, no merge commit.
