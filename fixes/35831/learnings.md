# Learnings — PR #35831 pr-complete run

- No reviewer-driven learnings — no actionable comment fixes on this run. Zero comments triaged REAL:
  no inline review comments and no `CHANGES_REQUESTED` reviews exist on this PR, and every conversation
  comment was status-only automation, an already-handled author note, or a bot finding that verified
  clean.

Process notes worth carrying forward:

- **Verify bot "all clear" claims from their machine-readable payload, not their prose.** The
  flaky-detection comment's rendered body says everything is fixed; the authoritative signal is the
  base64 `metamask-flaky-test-detection-metadata` block, which decodes to `findings: []` per file. One
  `base64 -d | jq` confirmed the disposition instead of trusting rendered text — cheap, and it also
  surfaces the `analyzedSha` so you know which commit the claim covers.
- **A red check is not always a code defect.** The only failing check, `check-pr-labels`, fails on the
  `blocked` label, which is an intentional product hold matching the `[NOT-READY-NEED-DESIGN]` title.
  Clearing it would mean removing a deliberate gate, which is a product decision, not a worker fix.
  Worth distinguishing process gates from defects before attempting a "make CI green" action.
- **Attribute recipe failures by node, not by exit code.** The run reported `status: fail`, but the
  per-node trace showed 5/6 passing and the stop at `require-cross`, a fixture precondition requiring
  exactly one open position. Reading the node sequence proved execution never reached any assertion on
  the PR's display code, which is what separates "environmental" from "regression". Confirming the
  branch touches no fixture or runtime data (`git diff origin/main...HEAD --name-only`) closed the
  attribution.
- **Recurring environmental gap in this family:** the inherited recipe depends on a live testnet
  position that the prior validation run closed at its end. Every follow-up run therefore fails the
  same gate. The recipe would be re-runnable if it either seeded its own position or tolerated setup,
  rather than asserting a precondition it does not establish.
- **`yarn jest` with newline-joined paths silently becomes one pattern.** Passing `$tests` from a
  `git diff | grep` capture matched 0 suites and exited 1, which reads like a failure. The suites must
  be passed as separate arguments; worth word-splitting deliberately rather than interpolating a
  multi-line variable.
