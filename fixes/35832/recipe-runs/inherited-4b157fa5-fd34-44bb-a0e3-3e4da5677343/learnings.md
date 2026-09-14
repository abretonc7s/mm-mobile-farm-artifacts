# Learnings — TAT-3786

- **Investigation dominated the time; the fix was two lines.** Finding the root cause meant proving
  that `navigation.canGoBack()` is parent-aware rather than stack-local. The DevLogger marker settled
  it in one press by printing `canGoBack` next to the actual Perps route array — inference from
  reading the navigator code alone would have been a guess. Logging the decision inputs side by side
  is what made the contradiction (`canGoBack: true` with a one-route stack) visible.

- **`mm-harness validate` in TASK.md does not exist in the installed CLI.** The structural validator
  is `mm-harness run <recipe> --plan` (exit 5 on invalid). Steps 12 and 14.2a should be updated. The
  `--plan` output also names the offending field, which caught an `intent` that restated the action.

- **Repeated probe runs mutate the navigation stack and produce false failures.** A verify run failed
  with `perpsRoutes: ["PerpsMarketDetails","PerpsMarketDetails"]` — two stacked market pages left over
  from earlier probes, not a fix defect. Restarting the app before each authoritative recipe run made
  results reproducible. Worth adding to the recipe guidance: treat live stack state as dirty between
  runs.

- **`expected: absent` is the wrong operator for anything behind a tab navigator.** Asserting
  `wallet-send-button` absent failed with `visibility: "tree"` because the wallet tab stays mounted
  behind Perps home. A positive assertion on a screen-unique element (`perps-market-add-funds-button`)
  is the correct proof, matching the TASK.md rule about not equating tree presence with visibility.

- **Editing source invalidates the harness's loaded-source fingerprint.** Any action then fails with
  `MOBILE_SOURCE_NOT_LOADED` until `app.lifecycle --arg command=restart`. Knowing this up front would
  have saved several confusing `fail` results that looked like action-argument problems.

- **The marker and fix landed in the same file, so `git stash pop` conflicted.** Resetting the file to
  the committed state and re-applying the fix was faster and more auditable than hand-merging conflict
  markers, and let me verify the cleanup commit was a byte-exact revert of the marker commit.

## Self-review pass (rev-claude)

- **A mutation test is the cheapest way to answer "could the tests pass if the fix were reverted?"**
  Reverting `if (canGoBack && hasPerpsStackHistory)` to `if (canGoBack)` and re-running jest took one
  command and turned a claim in `recipe-quality.json` into an independently reproduced fact (2 failed,
  13 passed — the exact 2 new tests). Backing up the file first made the restore trivially safe.

- **The load-bearing assumption of a navigation fix is "which navigator does `useNavigation()` return
  here?"** Rather than trusting the code comment, the answer was corroborated from a sibling in the same
  component context: `useDropPerpsHomeFromStackHistory` reads `state.routes` and filters by
  `Routes.PERPS.PERPS_HOME`, which only makes sense on the Perps stack. Same hook, same navigator.

- **Screenshots must actually be opened.** The checklist is explicit that recipe pass status and filenames
  prove nothing, and reading all four PNGs was what turned "evidence exists" into "the before shows the
  wallet token list and the after shows Perps home". A fiber-tree assertion could not have shown that.

- **Checking scope means looking at the call sites that were *not* changed.** Grepping every `canGoBack`
  in Perps surfaced three other consumers; confirming they are dismiss-after-action flows with no
  `backFallback` contract is what made "the fix is correctly narrow" a finding rather than an assumption.

- **`.cursor/rules/unit-testing-guidelines.mdc` referenced by the checklist does not exist in this repo.**
  The canonical guide is `docs/testing/unit-testing.md` (per AGENTS.md); the hard rules were read from
  there instead. Worth updating the checklist path so the step does not silently no-op.

- **The checklist file was swapped underneath the run.** Mid-review, `SELF-REVIEW.rev-claude.md` was
  replaced with a shorter `static-code` variant (15 steps -> 11, renumbered) and
  `review-feedback.rev-claude.md` was moved into `independent-review-2/`, so earlier `mark N` calls
  pointed at the old numbering and the written verdict vanished. Re-reading the checklist from disk
  rather than trusting the copy in context is what caught it; the marks were then remapped and the
  report rewritten in the new template's shape. Worth treating "re-read the checklist before
  finalizing" as routine in this harness.
