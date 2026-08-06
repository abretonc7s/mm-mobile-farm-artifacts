# Learnings — TAT-3687

- **The package's own CHANGELOG was the highest-value artifact in the run.** The
  v11 entry named the exact six Mobile signatures that would stop compiling, by
  file and symbol, and named `translatePerpsError.ts` as the consumer whose
  exhaustive `Record<PerpsErrorCode, …>` would break. Reading it before touching
  code turned an open-ended "fix all breaking changes" into a checklist that
  `tsc` then confirmed exactly — 19 errors across 8 files, no surprises. Bumping
  first and letting the compiler enumerate the work was the right order.

- **Two of the 19 errors needed a decision, not a mechanical widening.**
  `determineMakerStatus` is reachable with a trigger type (v11's
  `Order.orderType` now reports a trigger's execution mode, and
  `PerpsOrderDetailsView` feeds it straight in), so its `=== 'market'` guard had
  to become `!isLimitExecutionOrderType(...)` or a stop-market order would be
  priced at the maker rate. The other four widened hooks are fed only from the
  order-type selector, which offers two options, so their branches were left
  alone. Distinguishing "reachable" from "merely wider type" is what kept this
  minimal without leaving a real bug.

- **Three tooling instructions in TASK.md were stale and cost real time.**
  `--project-root` is now `--target` (the first recipe run exited 2 on it);
  `mm-harness launch --platform ios --preflight-mode fast` is now
  `mm-harness launch ios --verify`; and steps 14/15 (`yarn lint:fix`,
  `yarn format`) expand to whole-repo scans that `CLAUDE.local.md` forbids in a
  worker slot, so they had to be scoped to changed files by hand.

- **Video capture is broken on this slot and burned the most time of anything.**
  `--record-video=full-run` hung in `capture-helper resolve` for 3+ minutes and
  blocked the recipe from executing a single node; the standalone
  `record-window.sh` started but its capture-helper ignored SIGINT and never
  produced a container. Two other slots were holding `capture-helper stream`
  processes, which may be the cause. `xcrun simctl io … recordVideo` worked
  first try. Worth checking whether capture-helper is safe to run concurrently
  across slots before the next run depends on it.

- **The perps library flows are flaky against live testnet, and it took four
  runs to characterise it honestly.** Two runs passed 207/207; two failed in
  *different* library assertions — a teardown that asserted "no open orders"
  0.8s after a market order's TP/SL triggers were placed, and a limit order at
  the live Bid preset that filled instead of resting. Neither touches the code
  under test. The temptation was to re-run until green and report only that;
  recording all four runs in `recipe-coverage.md` and grading
  `recipe-quality.json` as `warn` is the more useful output.

## Self-review fix pass

- **I wrote a helper the dependency already exported, in the same PR that
  upgraded that dependency.** `resolveOrderExecution` was byte-identical to
  `getTriggerExecution` — same body, same signature, and a docblock naming this
  exact use case. I had read the v11 changelog entry that lists
  `getTriggerExecution` among the new order-type helpers, and still wrote my
  own. When adopting a release, the new-exports list is a menu to shop from
  before writing anything, not just a list of things that might break.

- **The more valuable finding was a wrong justification behind correct code.**
  I claimed the `determineMakerStatus` change prevented a Stop Market order
  being priced at the maker rate. It doesn't: the HyperLiquid adapter resolves
  `orderType` through `getTriggerExecution` before the app sees it, so the old
  guard already returned taker. The code was right, the reasoning was inverted,
  and a reviewer would have approved on a premise that doesn't hold. Worth
  remembering that a passing test suite validates the change, never the story
  told about it — I should trace the claimed failure mode to a concrete
  reachable input before writing it down.

- **A test that encodes a known gap as its expected value stops being a test
  for that gap.** Asserting `toStrictEqual(['perps.errors.subscriptionClientNotAvailable'])`
  looked like honest disclosure but froze the bug in place. Fixing the missing
  string and asserting `[]` cost one line and made the test do its job.

- **The perps recipe library silently stopped resolving between runs.** The
  first recipe run of this pass failed validation (exit 5,
  `workflow.unresolved_call_ref`) with no library change on my side; the
  directory was intact but no longer auto-registered. `--library
  perps=<path>` restored it. Worth pinning the library explicitly in the
  recipe invocation so a run is reproducible across slot state changes.

## Self-review fix pass 2 (evidence accuracy)

- **Evidence prose that quotes live values expires the moment the proof is
  re-run.** I read four screenshots, described them with exact figures, then
  re-ran the recipe twice more — each run overwrote those same PNG paths at a
  new mark, and my descriptions quietly stopped matching the shipped frames.
  Nothing warned me: the contract gate checks that files exist, not that prose
  matches pixels. The fix was to key the descriptions to recipe-controlled
  inputs ($10 notional, +25%/-10% presets, 100% close, order type) and say which
  fields are *populated* rather than what they read.

- **Order of operations matters more than I treated it.** Describing evidence
  before the final run is writing a caption for a photo not yet taken. Either
  write evidence prose only after the last run that can touch the artifacts, or
  write it so a re-run cannot invalidate it. The second is strictly better,
  because "the last run" is not knowable in advance.

- **A reviewer caught a factual drift that no automated gate could.** Tests,
  ESLint, tsc, the recipe and the artifact contract gate all passed with the
  wrong numbers in place, because none of them compare narrative claims against
  image content. Worth remembering that a green board says nothing about whether
  the story attached to it is true.

- **The branch was rebased between passes** (`49f7c3f54a` → `446cc379b7`,
  `2df1785419` → `f506550989`). Checking the reflog before assuming work was
  lost took one command and turned an alarming "HEAD moved" into a confirmed
  no-op; content and all fixes verified intact afterwards.
