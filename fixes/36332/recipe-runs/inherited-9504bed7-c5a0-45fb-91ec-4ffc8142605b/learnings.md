# Learnings — TAT-3931

- **Creating the repro data beat hunting for it.** The account's only multi-second multi-fill close
  was 13 months old and unreachable in the UI. Placing a $800 SOL long on testnet with
  `metamask.perps.place_order` produced a 4-fill order at the top of every activity list in one
  command, which turned an untestable AC into a clean before/after pair. Worth reaching for early
  when a bug needs a specific data shape.

- **The old test file encoded a prior fix I nearly regressed.** `transactionTransforms.test.ts` had
  "aggregates split stop loss fills" with *different* order ids, from TAT-2196. Grouping purely by
  order id — the obvious fix — would have silently undone it. Reading `git log -S` on the function
  before changing it was what caught this; the union of both rules is the reason the fix is ~40
  lines instead of ~5.

- **`ui.wait_for expected: absent` is unreliable on a live-updating Perps screen.** Every poll hit
  "Mobile CDP bridge command timed out after 157ms" and the action reported a stale positive, even
  though a manual probe on the same screen confirmed absence. Strictly positive assertions on a
  value that can only exist post-fix (here the summed fee `-$1.15`) are both more robust and more
  discriminating. Also: `ui.scroll` treats `delta_y` as an absolute offset, and `scroll_into_view`
  could not reach the Perps home activity section at all.

- **`ui.capture_surface` fails when the artifacts dir is on `/Volumes`** ("Detected file type from
  extension: PNG"), while plain `ui.screenshot` works fine there. Cost several runs to isolate,
  since the same recipe passed with a `/private/tmp` artifacts dir. Same family as the known
  `simctl recordVideo` restriction in CLAUDE.local.md. Use `mm-harness run --record-video=full-run`
  rather than a parallel `simctl recordVideo` — the two conflict over the display.

- **Text matching does not reach the Activity list rows.** `ui.wait_for text=...` works on the
  market detail and Perps home lists but not on the Activity screen, whose rows expose composed
  accessibility labels (`transaction-item-N` = "Opened long, 2.92 SOL, -$0.40"). `ui.locators` is
  the fastest way to find that out, but it intermittently returns zero items.

## Self-review pass (rev-claude)

- **The cheapest way to test a grouping rule is to tighten it and rerun the suite.** Applying the
  narrower same-second rule to the committed code left all 120 tests green. That single run proved
  both that the suite does not discriminate the over-merge behaviour and that the recommended fix
  is safe — far stronger evidence than arguing about the union-find in prose.

- **Three-line throwaway probes beat reading union-find code.** Two scratch Jest files (distinct
  order ids inside one second; an A/B/C chain across two seconds) turned "this transitive linking
  looks risky" into two reproduced cases with concrete sizes, in under two minutes. Write the probe
  before writing the finding.

- **Check the aggregation layer's output through the display transform, not just the aggregator.**
  AC3's flip test asserts `result[0].size === 43.23`, which passes, but running the same fixture
  through `transformFillsToTransactions` renders `5.57` — the exact number the ticket calls wrong.
  A passing test one layer below the user-visible value can hide an unproven AC.

- **Negative tests drift toward the case that cannot fail.** The "different orders don't merge"
  test separates them by nine seconds, which no rule in the file would ever have merged. When a
  negative test picks parameters far from the boundary, it documents intent without defending it.

## Self-review pass

- **I widened a rule past the bug it was written for.** The pre-fix same-second grouping existed
  only for close-side trigger splits (TAT-2196). Extending grouping to opens and flips, I carried
  the same-second key along with it — so two unrelated opens inside one second merged, and
  union-find chained further. The bug I was fixing was "one order, many rows"; the rule I wrote
  also did "many orders, one row". When widening an existing rule's domain, check each clause
  separately against its original motivation instead of moving the whole key.

- **My negative test was decorative.** "does not aggregate fills of different orders opening the
  same market" separated the orders by nine seconds — a case the rule was never going to merge.
  The whole suite stayed green under the tightened rule, which proved it did not discriminate.
  The check that catches this: revert the fix and confirm the new tests actually fail. Both new
  negative tests now do (2 failed / 120 passed on the old key).

- **A fixture that reproduces the ticket's numbers by coincidence is a trap.** My flip fixture
  rendered `fill.size` 5.57 — the exact figure TAT-3931 calls wrong — for an unrelated reason
  (5.57 is the resulting short position, not a partial fill). It cost a review cycle. Pinning the
  value at the display-transform layer, with a comment saying what each number means, is what
  settles it.

- **Device evidence did not catch either regression.** The recipe passed before and after, because
  the fixture account has no two same-second orders on one market. Runtime proof shows the fix
  works; only a unit-layer negative test shows it does not over-reach.

## Self-review loop 2 (rev-claude)

- **Reverting only the production file is the cheapest proof a new test earns its place.** Checking
  out `transactionTransforms.ts` at the previous HEAD while keeping the new tests turned "the
  worker added negative tests" into "both fail on the old code, so they defend the fix". Two
  `git checkout <sha> -- <file>` runs, no branches, tree restored clean afterwards.

- **Pick the revert baseline per finding.** The two over-merge tests had to be checked against the
  *previous loop's* HEAD; the flip display test only discriminates against `origin/main`, since
  loop-1 code already aggregated flips. Using one baseline for both would have mislabelled the flip
  test as non-discriminating.

- **A narrowed rule leaves a residual where the rule is still needed.** Bounding the same-second
  merge to the close category fixed the open side but left the A-B-C chain intact for closes,
  because that is exactly where the TAT-2196 trigger-split rule lives. Re-probing the *other* side
  of a scoped fix is what turned an assumed-clean delta into a documented, quantified residual.

- **Checksum the published evidence against the recipe run.** `shasum` on
  `after-*.png` vs `recipe-run/screenshots/*` proved the screenshots came from the post-fix run
  rather than being carried over from the previous loop — a stale-evidence check that costs one
  command and does not need the images to be re-read.

## Static self-review pass (rev-claude)

- **Tracing the union-find by hand found what the tests do not pin.** The per-link reasoning in the
  code comment is sound, but walking three seed groups on paper showed the merge is transitive, so
  unrelated close orders can still chain into one row. Reading the invariant beats trusting the
  comment stating it.
- **`mm-harness review checklist` returned no `## Domain patterns` phase** (no domain declared), so
  the fallback in `temp/recipe/runtime/review-patterns.md` was the only domain signal. Worth
  checking for that phase before assuming the domain list was applied.
- **The parity item is the one a mobile-only review almost skips.** The extension copy at
  `ui/components/app/perps/utils/transactionTransforms.ts:42` is byte-identical pre-fix code; this
  PR creates the divergence deliberately, and it is only tracked in prose in the PR body.
- **Evidence existing is not evidence attached.** Six before/after media files sit in `artifacts/`
  and in `evidence-manifest.json` while the PR body still carries the empty placeholder.

## Self-review pass — round 2

- **My comment was more confident than my code.** I wrote that the linking step "can only chain
  groups that genuinely share an order id" — true per link, false across the transitive union. The
  claim was about a property I had not actually traced end to end. A comment asserting a safety
  property is a claim that needs the same evidence as an assertion; if I cannot name the case it
  excludes, I should describe the mechanism instead of promising a bound.

- **Renaming was the cheap part; the stale comments were the real drift.** `aggregateFillsByTimestamp`
  kept its name and its call-site comment through a change that made both wrong, because I updated
  the JSDoc I was editing and never looked one function down. After changing what a function does,
  grep its name and read every comment that mentions the old behaviour, not just the block above it.

- **A reviewer prescription can be worse than the finding it fixes.** Gating the same-second seed on
  a trigger `detailedOrderType` looked tighter, but that field is enriched in only one of the three
  hooks and its provider-side enrichment is deliberately best-effort inside a try/catch — so the
  gate would be off exactly when a TP/SL fires live. Checking where a field is actually populated,
  before adopting a suggestion that keys on it, is what turned this into a documented decline
  rather than a silent regression.

- **Evidence sections have an owner.** The empty Screenshots placeholder read as missing work, but
  the gateway substitutes that section from `evidence-manifest.json` at publish; hand-writing local
  paths would have shipped broken links. Stating the claim in prose satisfies the human reader
  without fighting the pipeline.

## Static self-review pass 2 (rev-claude, incremental)

- **The right outcome of a speculative suggestion was a decline with evidence.** I proposed gating
  the same-second seed on a trigger `detailedOrderType`; the worker traced where that field is
  actually enriched (`usePerpsTransactionHistory.ts:197` only) and showed the gate would kill close
  aggregation on Perps home and on WS fills. Verifying their counter-evidence was faster than
  defending the suggestion.
- **Re-checking a comment means re-tracing the code, not reading the comment.** The corrected
  transitivity comment was only confirmable by walking the seed keys and the union loop again to
  see that order-seeded groups genuinely cannot chain.
- **A rename is only done when the grep is clean.** Repo-wide, the old name survives solely in
  historical `scripts/reports/coverage-lcov-*.info` files from other branches — worth checking for
  barrel re-exports before calling a rename complete.
- **Evidence placeholders are not always a gap.** The `<!-- [screenshots/recordings] -->` markers
  stay on purpose: the gateway substitutes them from `evidence-manifest.json` at publish, and
  literal local paths would render as broken links on GitHub.
