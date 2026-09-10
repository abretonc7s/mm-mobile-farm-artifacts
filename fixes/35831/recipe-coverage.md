# Recipe coverage — pr-complete run (PR #35831)

Scope: re-validation only. **Proof mode for this run: state only.** This run made **no code change**
(0 REAL comment findings), so it adds no new criteria to the inherited map and produces no visual
proof of its own. It attempted to replay the inherited recipe against the rebased
tree (`branch + origin/main`) and did not reach the assertion nodes. Nothing below is claimed as a
new passing execution.

## This run's re-validation attempt

| Stage | Result | Evidence |
| --- | --- | --- |
| Runtime launch + verify (`mm-harness launch ios --verify`) | PASS | exit 0; bundle rebuilt on rebased tree; `Mobile bridge ready (17.5s)`; `verify mobile passed (20.7s)`; fixture `READY (accounts=4)` |
| Runtime health (`mm-harness doctor --expect-live --json`) | PASS | exit 0; `status: pass`; 5/5 checks |
| Recipe replay (42-node graph) | FAIL at node 4 — precondition | `recipe-run/summary.json`, `recipe-run/trace.json` |
| Display-assertion nodes (badges, liquidation, explanation, Margin used) | NOT REACHED | run aborted at `require-cross` |

Failing gate: `require-cross`, `$.positions length_eq 1`, actual `"positions": []` (fixture
recaptured live at 2026-09-10T13:18:00Z). The selected testnet account
`0x8dc623e964475d4d669da601fd15ea9125469003` currently holds no open position.

This is the replay limit the inherited coverage doc predicted: *"this requires fresh authorized
testnet fixtures and a refreshed venue liquidation expectation before replay. Final fixtures have
been closed, ETH restored to isolated 3x."* The precondition was destroyed by the original run's own
cleanup, so the recipe is not re-runnable without re-opening a real leveraged testnet position —
a financial mutation outside this comment-triage task's scope and not requested by any comment.

Causation: the failing node reads a fixture path under `temp/tasks/feat/tat-3519-0908-104128/`;
zero commits on this branch touch it, and it is not in the PR diff. Neither the (absent) review
fixes nor the step 3 merge from main can explain it. Logged as unrelated/environmental per step 10.

## Inherited coverage map (historical — NOT re-executed by this run)

The inherited package proved the criteria below in mixed state+visual mode on the pre-rebase tree,
via `recipe-run-recorded-2` (37/37, numeric branch) and `recipe-run-linked-null-3` (39/39, null
branch): AC7 current-position Cross badge, AC8 numeric venue liquidation, AC8b legitimate null
liquidation, AC10 shared liquidation explanation, and AC11 Margin used with edit suppression.

Those runs and their screenshots live in the inherited package. They are historical evidence for the
original run and are **not** re-claimed, re-referenced, or counted as proof for this run. Detail is
preserved verbatim in `inputs/inherited/recipe-coverage.md`.

## State-mode coverage that WAS re-executed on the rebased tree

The display behavior the recipe would have asserted is independently covered by component tests,
which did run and pass post-rebase:

| Suite | Result |
| --- | --- |
| `PerpsPositionsView.test.tsx` | PASS |
| `PerpsProPositionCard.test.tsx` | PASS |
| `PerpsCard.test.tsx` | PASS |
| `PerpsCrossMarginInfoButton.test.tsx` | PASS |
| `PerpsPositionCard.test.tsx` | PASS |

**5/5 suites, 110/110 tests.** Plus `lint:tsc` exit 0 (the first clean typecheck since the Core
dependency landed in `@metamask/perps-controller@16.2.0`), scoped ESLint `--max-warnings=0` clean,
and `format:check` clean.

Limits: no runtime/visual proof was produced by this run. No Android execution, no account-wide
health, no Pro picker enablement, and no full-epic completion is claimed.
