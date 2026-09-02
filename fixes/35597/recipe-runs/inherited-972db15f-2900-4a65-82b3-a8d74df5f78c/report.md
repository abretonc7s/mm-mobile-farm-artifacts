# TAT-3906 / TAT-3838 / TAT-3874 — report

## Self-Review Fixes

- `app/components/UI/Perps/utils/perpsModeSwitch.ts:247` — softened the `pop: true` comment I added
  in the fix. It claimed callers always arrive from a screen stacked above the target, which is not
  true for all six `useNavigateToPerpsHome` callers (`BrowserTab.tsx:177`, `PerpsDetails.tsx:398`
  and `:459` usually run with the Perps stack unmounted). It now states both cases: pop when the
  target is below the caller, push unchanged when it is not present. This was the reviewer's
  non-blocking "worth softening the comment" note under Fix Quality.

## Declined review findings

The reviewer raised five issues, all the same one: the diff removes pre-existing ticket references
from comments in the two touched files —
`PerpsOrderView.tsx:445` (`TAT-1937`), `:547` (`TAT-3334`),
`perpsModeSwitch.ts:16` (`TAT-3551, AC #4`), `:67` (`TAT-3612`), `:166` (`TAT-3612`).

**Not applied — these removals are an explicit operator instruction, not drive-by churn.** During
the implementation run the operator reviewed the diff and asked for them to be removed, in their
words: *"even if pre existing I really dont like leaving TAT references in the comments those should
be cleaned up."* When the reviewer's finding was put back to them in this pass, they chose "keep
them removed, decline the finding".

The reviewer's reasoning is sound on its own terms — 69 `TAT-` references remain across 43 Perps
files, so the convention is real, and comment-only edits do widen a two-line fix. That trade-off was
put to the operator explicitly, with restoring-the-five as the recommended option, and they decided
otherwise. Recording it here rather than silently reverting their instruction.

Note the removals only cover the two files this fix already touches; the remaining references
elsewhere in Perps were left alone, so no extra files enter the diff.

## Verification after the self-review pass

- `yarn jest app/components/UI/Perps/utils/perpsModeSwitch.test.ts --no-coverage` → 22 passed.
- Bounded ESLint on the changed file → **0 errors**, 1 warning
  (`@typescript-eslint/no-deprecated` on `navigate`), pre-existing — the reviewer independently
  confirmed the same warning at `origin/main:238`. `--max-warnings=0` fails on legacy debt only.
- Recipe regression gate → **exit 0**, all 20 nodes `ok: true`.
- `check-task-artifact-contract.mjs --require-recipe-quality-if-recipe
  --require-recipe-coverage-if-recipe` → `TASK_ARTIFACT_CONTRACT_PASS`.

### Flake observed (external, not a regression)

The first regression run failed at `ac1-wait-position-open`. The cause was venue-side, captured in
Metro:

```
TradingService: Provider response received {"error": "order 0: Only post-only orders allowed
immediately after network upgrade", "success": false}
```

Hyperliquid testnet was in a post-upgrade window that rejects market orders, so no position could
open and the position card never rendered. A retry ~60s later passed with all nodes green. This is
the flake risk already recorded as `warn` in `recipe-quality.json` (the recipe places a real testnet
order), not a defect in the change.
