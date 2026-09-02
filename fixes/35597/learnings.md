# Learnings — pr-complete pass on #35597

No REAL comment fixes on this run, so there are no reviewer-caught defects to record. What the pass
did surface:

- **A rebase is validation even when it is never published.** Step 3 pulled 155 files of `main`
  under the branch (+16804/-1184). Re-running the recipe and the three suites on that merged tree is
  what proves the fix survives current `main`, and that result stands whether or not the rebase gets
  pushed. Worth keeping the local rebase rather than resetting it away.

- **The checklist and the standing repo rules can disagree, and the operator owns the tiebreak.**
  Step 11 prescribes `--force-with-lease` after a rebase; `CLAUDE.local.md` says never force-push.
  Both are legitimate. Surfacing it cost one question and avoided invalidating green CI plus two
  triage replies that cite the current SHA.

- **Don't re-reply to comments you already answered.** Two of the seven conversation comments were
  my own prior triage responses, and the two actionable bot findings already had consolidated
  replies. Step 12 read literally would have posted duplicates; checking authorship before replying
  kept the thread clean.

- **The same flaky signals keep coming back, so the durable answer is a ticket, not a reply.** The
  J9 flaky-test finding and the `Perps add funds` perf gate have now been triaged across three
  passes. The order-dependence behind J9 is real and pre-existing, which is why it went to TAT-3910
  rather than into this PR's diff.
