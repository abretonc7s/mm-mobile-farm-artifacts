# Learnings — TAT-3904 self-review

- **Self-review was dispatched against an unfinished worker run.** The worker's
  `SIGNAL.json` was still `status: "running"` at step 8 ("Record approach") when this
  review started. The orchestrator should gate review dispatch on a terminal worker
  signal (`complete` / `blocked`), otherwise reviewers burn a full session confirming
  there is nothing to review.

- **`TASK_ARTIFACT_CONTRACT_PASS` can be a false green.** The step-12 gate passed on a
  task with zero code, zero recipe, and zero evidence: `--require-recipe-*-if-recipe`
  never triggers without a recipe, and the `visual_claim` heuristic reads `0` when both
  `evidence_count` is 0 and `report.md` is absent. The contract script cannot tell "no
  visual claim to prove" apart from "no work done". A cheap fix would be an explicit
  empty-diff precondition (compare `headSha` to `baseSha`) that fails fast before the
  per-artifact checks run.

- **`git diff main...HEAD` was silently empty while local `main` was stale.** Using
  `origin/main` (per the repo's diff-review rule) plus the worker's own
  `review-diff-stat.json` — which records `baseSha`, `headSha`, and a `diffHash` of
  `e3b0c442…`, the SHA-256 of empty input — gave three independent confirmations of an
  empty diff far faster than reading files. Cross-checking the recorded diff hash is a
  good first move before assuming a diff-read failed.

- **The abandoned run still left reusable value.** `artifacts/approach.md` is a complete,
  defensible plan with its three genuine ambiguities (unratified copy, best-ask/bid vs
  mid, strict vs inclusive comparison) already resolved. The re-dispatch should treat it
  as a frozen plan and resume at Phase 3 rather than redoing the analysis — otherwise the
  cost of the failed run is paid twice.

- **`.cursor/rules/unit-testing-guidelines.mdc` is absent from this checkout**, so the
  step-6 `cat` is a no-op here. Checklist steps that `cat` a rules file should tolerate
  its absence explicitly instead of leaving the reviewer to infer intent.

---

# Learnings — TAT-3904 self-review fix pass

- **Seven review findings, one root cause.** The review listed the missing helper, hook
  wiring, copy keys, recipe, and report as separate issues, but all five acceptance
  criteria were unimplemented for the same reason: the prior run stopped after writing
  its approach. Fixing the cause (implement the ticket) closed all seven at once.
  Working the list item-by-item would have produced the same diff more slowly.

- **Authoring a recipe blind cost a full run, exactly as the slot rules warn.** The first
  end-to-end run failed at `expect-quiet` — not a code defect, but leftover form state: an
  earlier standalone probe had left the side toggle on Short, so a ladder that should have
  been quiet for a long correctly warned for a short. The fix was an explicit direction
  node after navigation. **A recipe that does not reset the state it depends on is testing
  the previous run.** Per-node validation caught every other defect cheaply; this one only
  surfaced end-to-end because it was an interaction between nodes.

- **Failing-first is worth the two app restarts.** Stashing the implementation, restarting
  onto that source, and re-running turned "the recipe passes" into "the recipe fails
  without the change and passes with it". It also exposed that `expect-quiet` passes in
  both worlds — the message element is absent whether or not the feature exists — so that
  node guards against over-warning but is not itself feature proof. Without the
  failing-first run I would have counted it as coverage it does not provide.

- **A screenshot can be weaker evidence than an assertion.** The warning renders below the
  fold on the Pro order form and is covered by the runtime HUD overlay, so the captured
  frame shows the correct form state but never the warning text. The review had listed
  missing `evidence-*.png` as an issue; adding one would have looked like proof without
  being any. `ui.wait_for` with `text` + `text_match: contains` asserts the exact copy on
  the rendered tree instead. Deleted the screenshot rather than ship it as evidence.

- **The harness CLI coerces numeric-looking `--arg` values to numbers**, so
  `--arg value=76000` fails `ui.set_input` validation with "must match type string" and
  there is no quoting that escapes it. Recipe JSON carries proper types, so the workaround
  is to probe via a small recipe file rather than `mm-harness call`. Recipe `intent` fields
  are also validated for meaning — they must state the human-visible goal, not restate the
  action, node id, or selector.

---

# Learnings — TAT-3904 self-review (verification pass)

- **Mutation testing settled "would these tests pass if the fix were reverted?" in one
  run.** Rather than reasoning about the assertions, I forced the helper to return
  `undefined` and re-ran: 5 of 9 new tests failed, and the 4 survivors were exactly the
  intentional negative cases. That converts a judgement call into evidence, and it cost
  one command. Worth doing whenever a review must certify revert-sensitivity.

- **The riskiest line in an additive diff was the early return, not the new code.** The
  Scale branch returns before two existing field-issue branches, which would have silently
  suppressed error messages if scale orders could produce them. Confirming it was safe
  meant resolving `isTriggerOrderType` and `isLimitExecutionOrderType` into the controller
  package to read the actual membership arrays — `'scale'` is in neither. A purely
  additive diff can still change existing behavior through control flow.

- **A stated rationale can be wrong while its conclusion is right.** Both the evidence
  manifest and the coverage doc justified omitting screenshots as "renders below the
  fold". Reading `PerpsProOrderForm.tsx:922` shows the warning renders above the Size
  input — visible in the baseline frame. The real cause was scroll position at capture
  time (no `ui.scroll` node, screenshot taken at the place-order button). Omitting the
  screenshot was still correct, so this is a non-blocking note rather than a finding —
  but accepting the reasoning unread would have propagated a false constraint.

- **Locale-coverage rules need the repo's actual convention before they can be applied.**
  Two en-only keys sitting beside siblings translated into 15 locales looks exactly like
  the anti-pattern the domain doc warns about. Checking the history showed non-en files
  are written solely by the Crowdin bot and a recent perps PR added 59 en-only keys the
  same way. The rule was inapplicable, not violated.

- **The artifact contract gate passed in both runs, meaning opposite things.** Last pass
  it passed vacuously on an empty task; this pass it passed on a real recipe with both
  sidecars and a consistent all-`state` coverage table. The script output alone does not
  distinguish these, so the reviewer still has to check what the counts are derived from.

---

# Learnings — visual evidence correction

- **"Below the fold" is not a reason to give up on visual proof.** I concluded a screenshot
  could not show the scale warning because it renders low in the order form under the recipe
  HUD, and shipped state assertions alone. Both obstacles had flags: `mm-harness run --hud hide`
  suppresses the overlay for the whole run (clearing it per-node loses a race with the runner's
  own repaint), and `ui.capture_surface` stitches a scrolling panel into one unclipped image.
  Anchoring the scroll on the element *above* the target matters — scrolling to the message
  itself pushed it off the top, since it renders just under the scale fields.

- **A green `ui.wait_for` proves the element exists, not that the user would see it usefully.**
  Two defects survived a fully passing 19-node run and only surfaced once I looked at the
  frames: the ticket had no order count or size, so a blocking validation error sat in the
  same message slot; and the full-cross endpoints were mis-ordered (start > end), tripping
  "Start price must be lower than end price" and *disabling* Place order — so the frame meant
  to prove non-blocking placement showed a disabled button. State assertions are necessary but
  they do not see context.

- **Inspect every captured frame, don't trust the exit code.** The run was green while
  producing evidence that argued against the feature. Reading the screenshots was the only
  step that caught it.

- **Recipe values must satisfy the form's own invariants.** The scale form requires
  start < end regardless of side, so proving "the whole ladder crosses" means moving the
  well-ordered range across the market, not inverting the endpoints. The fix for the short
  side was start $75,000 / end $76,000 under the market, not start $76,000 / end $75,000.
