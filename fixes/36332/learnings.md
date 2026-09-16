# Learnings — PR #36332 pr-complete run

No new reviewer-driven code fixes on this run: the one REAL finding was already closed at HEAD
before the run started. The learnings below come from what that finding exposed and from what
this run had to do around it.

- **Sorting by a field the data ties on is not ordering.** Bugbot caught the real defect the
  upstream worker missed: `aggregateFillsByOrder` sorted a group by `timestamp` and then read
  `startPosition` off the first element. A single HyperLiquid book sweep produces fills that
  share a millisecond, so the sort is a no-op and the "earliest" fill was whichever the
  newest-first history happened to put there — silently wrong flip sizing (37.66 reported as
  7.66). The fix is to stop inferring order from position and derive the value from the data
  itself: `startPosition` is the largest magnitude any fill in the group saw, because a close or
  flip only ever walks a position down. Rule of thumb for future aggregators: when picking a
  representative value out of a group, pick it by a property of the value, not by an index into
  a sort that may not discriminate.
- **A resolved thread is not a reason to skip verification, and a verified thread is not a reason
  to reply again.** The thread was already answered and resolved, but the reply cited a
  pre-rebase SHA. Checking the claim against the actual current HEAD before recording
  `already replied` is cheap; posting a second reply saying the same thing is noise. Both halves
  matter.
- **Rebase-only rounds still need the full proof.** Nothing in the branch changed this run — 8
  commits replayed cleanly onto a `main` that had moved. It would have been easy to treat the
  push as trivial, but the recipe exists precisely to prove `branch + origin/main` together;
  re-running it (27/27) is what makes the force-push defensible.
- **Read the inherited recipe's file paths before assuming it is portable.** The two `command`
  nodes redirect their logs into the *parent* run's task directory
  (`temp/tasks/fix/tat-3931-0916-154555/artifacts/`). That happened to still exist in this clone
  so no migration was needed, but on a fresh clone the redirect would fail and surface as a
  `RUNTIME FAIL` on `assert_exit_code` that looks like a code regression rather than a stale
  path. Inherited recipes should write into `$TASK_DIR`, not a hardcoded sibling.
- **`metamask.perps.*` state probes need an unlocked wallet.** `read_positions` failed with an
  opaque `ACTION_EXECUTION_FAILED` / CDP bridge error for 30s before I noticed `doctor` had
  already reported `walletState: locked`. Running `metamask.wallet.ensure_unlocked` first turned
  the same call into an instant `count: 0`. Read the doctor output before probing controller state.
