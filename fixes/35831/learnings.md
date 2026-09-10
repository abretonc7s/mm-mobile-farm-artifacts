# Learnings — PR #35831 pr-complete run

No reviewer-driven code fixes were required on this run (0 REAL, 5 FALSE POSITIVE). The learnings
below are about the run itself rather than about defects reviewers caught.

- **A rebase can silently clear a blocker that a prior run recorded as hard-blocking.** The
  inherited report and the author's PR comment both stated Mobile was blocked on Core #10136 for
  four missing `ORDER_MARGIN_MODE_*` constants. Between that run and this one, Core merged, shipped
  in `@metamask/perps-controller@16.2.0`, and `main` picked up the bump — so step 3's rebase plus
  `yarn install --immutable` cleared the typecheck failure with no code change on the branch. Worth
  re-testing an inherited blocker after integration instead of carrying it forward as still-true.

- **Verify static bot findings against source, not against the historical failure rate.** All five
  flaky findings cited a 0/439 failure rate, which proves nothing either way. The dispositions held
  up only because the actual files were read: the two J4 findings cite an `await waitFor(() => {})`
  line that exists in neither file (one file imports no `waitFor` at all), and the three J3 findings
  ask for a `resetAllMocks()` that would wipe `jest.mock` factory implementations the suites depend
  on — the suggested "fix" would break the tests it claims to stabilize.

- **`clearAllMocks()` without `resetAllMocks()` is correct when the `beforeEach` restores what the
  tests mutate.** In all three J3 suites the `beforeEach` explicitly reinstates every mutated return
  value (selectors, markets, theme, PnL, live prices). The generic pattern-matcher cannot see that,
  so this finding class will keep recurring on well-written perps suites and should be dispositioned
  by reading the setup block.

- **Recipes with live-venue preconditions decay between runs.** The inherited recipe gates on
  exactly one real open Cross position, but the original run deliberately closed its positions
  afterward ("Both were closed and ETH was restored to isolated 3x"). The gate now fails at node 4
  before touching any PR code. A recipe whose precondition is destroyed by its own cleanup cannot
  re-validate later without re-establishing a real financial position — a re-runnability gap worth
  designing around (fixture-backed state rather than live venue state).

- **Distinguishing "runtime unavailable" from "precondition unmet" mattered here.** Launch and
  doctor both passed cleanly, so the skip-on-unhealthy-runtime path did not apply; the failure had
  to be triaged on causation instead, and traced to a fixture path no branch commit touches.
