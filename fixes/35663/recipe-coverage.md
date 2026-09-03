# Recipe Coverage — PR #35663 (review round)

Recipe: `artifacts/recipe.json` (26 nodes, all pass — inherited from the family root, re-run here).
Run: `artifacts/recipe-run/` — `summary.json` status `pass`, exitCode 0, 92.6s.

Re-validated against **branch + `origin/main`** after the step-3 rebase onto `6766f343c8` and after
the five review fixes in `50753638e5`. Node count matches the inherited baseline exactly, so no
coverage was lost.

Proof is **mixed**: a `ui.wait_for` assertion on the rendered tree for every claim, plus a
screenshot of each warning variant, captured with `--hud hide` and `ui.capture_surface` so the
warning is not clipped by the viewport.

| AC | Claim | Proof mode | Recipe nodes | Screenshot |
|----|-------|-----------|--------------|------------|
| 1 | Long scale order crossing the best ask warns | mixed | `full-start` → `expect-full-above` (asserts "Your price range is above current price") | `evidence-full-above-shot` |
| 2 | Short scale order crossing the best bid warns with mirrored copy | mixed | `short-start`, `short-end` → `expect-full-below` (asserts "Your price range is below current price") | `evidence-full-below-shot` |
| 3 | Partly-crossing ladder gets distinct copy from a fully-crossing one | mixed | `partial-end` → `expect-partial-above` (asserts "Part of your price range is above current price"), contrasted with `expect-full-above` on the same side | `evidence-partial-shot` |
| 4 | Warning re-evaluates on endpoint edit and on side flip | state | `expect-quiet` (absent) → `partial-end`/`expect-partial-above` (present) → `full-start`/`expect-full-above` (escalated); `flip-short` → `expect-cleared-on-flip` (absent without touching either endpoint) | — |
| 5 | Warning is non-blocking; the order can still be placed | mixed | `expect-still-placeable` asserts the place-order control is present while the warning shows | All three frames show Place order enabled beside the warning |

## Change from the inherited coverage

The inherited artifact recorded **AC 4 as PARTIAL**: the submit-time re-check was implemented but
the recipe could not assert it, because it emitted a `DevLogger` line rather than changing visible
state, and observing it live would have meant placing a real order.

Review comment 3921202954 asked for that path to be either connected to a genuinely fresh quote
with a visible result, or removed. It was removed in `50753638e5`. **AC 4 is therefore now fully
covered rather than partial** — what remains is exactly the stream-driven endpoint-edit and
side-flip behaviour the recipe already asserts, with no unproven half.

Three `ui.wait_for` assertion texts were updated to the reviewer-requested copy from comment
3921202951. Text-only: node IDs, ordering, testIDs, intents, and screenshot nodes are untouched.

## Unit coverage backing the boundary behaviour

The at-the-touch equality case (comment 3921202930) is not reachable through the recipe, which types
round prices against a live market. It is covered by unit tests instead:

- `treats a long endpoint resting exactly at the best ask as taker execution`
- `treats a short endpoint resting exactly at the best bid as taker execution`
- `warns for the whole ladder when both long endpoints sit at the best ask`
- `warns for the whole ladder when both short endpoints sit at the best bid`
- `returns undefined when a long ladder rests entirely below the best ask`
- `returns undefined when a short ladder rests entirely above the best bid`
- `returns undefined for an unavailable book quote`
- `returns undefined for a ladder with only a start endpoint entered` / `only an end endpoint entered`

`yarn jest app/components/UI/Perps/utils/triggerOrderValidation.test.ts` → **79 passed** (was 71).
`yarn jest .../usePerpsProOrderForm.test.ts` → **271 passed**.

## Side findings

4 non-blocking application events during the run, none on the perps scale-order path: a reselect
identity-function warning from `AccountGroupBalance`, and a
`MoneyAccountBalanceService:getMoneyAccountBalance` RPC 401. Unrelated to this PR.
