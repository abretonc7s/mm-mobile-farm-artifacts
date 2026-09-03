# TAT-3897 self-review learnings (loop 6 — re-review of fixes)

- The gate finally cleared, and confirming that took running it rather than trusting the prediction. Loop 5's simulation said rewording one phrase would yield `evidence_count=0`, `visual_claim=0` and no `FAIL_EMPTY`; the live run matched exactly. Predicting a fix and verifying it are different acts, and the second is cheap.
- Widening the scan past the gate's own input found the real remaining issue. Step 12 greps only `report.md`, so `pr-description.md` was invisible to it — yet that file is what human reviewers read, and it still carried the retracted `ui.press` claim plus the superseded screenshot the manifest had formally omitted. A passing gate is not the same as correct artifacts.
- Mtimes were the fastest way to spot a document left behind. `pr-description.md` at 11:04 against `recipe-coverage.md` at 12:45 and `evidence-manifest.json` at 13:03 immediately showed it predated every correction, before reading a line of it.
- The worker avoided a trap I should note: it described its own fix as touching the "prior-state/subsequent-state regex" rather than writing the trigger words, so the changelog entry did not re-trip the gate it had just cleared. Fixing a text-matching gate means watching the text you write about the fix.
- Corrections propagate unevenly across artifacts. Three files were fixed across loops 3-5 while a fourth stating the same retracted claim was never revisited. When a premise is retracted, the retraction needs a sweep of everything asserting it, not just the file the finding named.

# TAT-3897 self-review learnings (rev-claude pass)

- Gate parity is a productive place to look for defects. Three consumers read the same derived value here; two were gated and one was not. Diffing the gates against each other — rather than reading each consumer in isolation — is what surfaced the blocking issue, and it is a cheap check on any change that fans one computed value out to several sinks.
- Writing a throwaway probe test beat reasoning about the bug. I could have argued from `setLimitPrice` firing per keystroke that telemetry would over-emit, but a temporary test typing `90000` one character at a time turned "probably fires repeatedly" into "fires 3 times with 100%/99%/90% percentages." The exact numbers are what make the finding actionable instead of arguable, and the probe cost one edit plus one revert.
- Reverting the implementation is the only real check that tests are load-bearing. The worker claimed the hook tests fail against `origin/main`; swapping the file in and running proved it (5 failures) in under two minutes. Worth doing on any PR whose central claim is "these tests guard the fix."
- Interpolating a value into a string that doubles as a dedupe key silently defeats the dedupe. The ref-based guard here looks identical to its working sibling, but the sibling keys on a stable error code while this one keys on rendered copy containing a varying percentage. Same shape, opposite behavior.
- Verifying a convention beats assuming it. En-only locale additions looked like a coverage gap until I checked a recently merged perps PR and found the same pattern, which turned a would-be finding into a non-finding.

## Loop 6

- A prior pass left issue 2 half-applied: it wrote the justifying comment ("Ceil, not round…") and a
  test asserting `percent: 6`, but never changed `Math.round` to `Math.ceil`. The comment asserted
  behavior the code did not have, and the test was red. Running the suite before editing surfaced
  this immediately — reading the diff alone would have made the fix look done.
- Checking a checklist step off is not evidence the step happened. Steps 1-2 were marked complete
  while step 3's code change was missing, so the trustworthy starting move in a resumed loop is to
  re-run the tests, not to trust the checkboxes.
- Changing a rounding operator has reach beyond its own file: four pre-existing hook assertions
  encoded `round` output as `percent: 11`. I recomputed 80000 vs bid 89999 = 11.11% by hand to
  confirm `ceil` → 12 was genuinely right, rather than pasting the value Jest printed. Grepping for
  other consumers first bounded the blast radius to the files already in the diff.
- `MOBILE_SOURCE_NOT_LOADED` after a source edit is a stale-runtime signal, not a regression. The
  error names its own remedy (`app.lifecycle restart`), which stays within the "do not rebuild the
  slot" rule; the recipe passed on the very next run.

# TAT-3897 self-review learnings (rev-claude pass 2 — verification of fixes)

- Re-running the original probe was the check that mattered. The worker's report said the telemetry gate was already applied, the new test passed, and the suite was green — all true, and none of it proves the user-visible defect is gone. Replaying the exact repro that found it (0 events now, 3 before) is what closed the loop, and it cost one edit and one revert.
- Deleting only the fix is a sharper test of a regression test than reverting the whole file. Removing just the five-line blur gate failed exactly one test and nothing else, which shows the new test guards that specific behavior rather than passing incidentally on unrelated coupling. A whole-file revert would have failed six tests and told me much less.
- Assertion-count changes deserve arithmetic, not trust. Four pre-existing `percent: 11` assertions became `percent: 12`, which is the shape of a test edited to match new output. Recomputing by hand — 80000 against bid 89999 is 11.11%, and ceil is 12 — confirmed it was a correct consequence of `round`→`ceil` rather than fitting the test to observed behavior.
- A well-built regression test asserts the negative and the positive. The keystroke test checks zero events while typing and exactly one after blur; without the second half it would also pass if the fix had over-gated the warning into never firing. Worth checking that any "emits nothing" test cannot be satisfied by breaking the feature.
- A comment, its operator, and its test can drift apart in three directions. A prior loop shipped the "Ceil, not round" comment and a test asserting ceil behavior while the code still called `round`, so the file documented and tested a behavior it did not have. When a change spans prose, code, and assertion, confirm all three moved.
