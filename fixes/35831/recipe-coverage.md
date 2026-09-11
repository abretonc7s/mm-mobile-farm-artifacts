# Recipe coverage — pr-complete re-validation run

Scope: re-validation only. This run authored no recipe and added no acceptance criteria; it re-ran the
inherited recipe against `branch + origin/main` after rebasing onto `91a66f077a`. The inherited
criteria map is unchanged — see `inputs/inherited/recipe-coverage.md` for the authored slice.

Proof mode this run: **state only**. No new visual evidence was produced, because execution stopped
before the first screenshot node.

## What this run actually proved

| Criterion within this slice | Mode | Evidence this run | Status this run |
| --- | --- | --- | --- |
| Runtime reachable on rebased HEAD | State | `launch ios --verify` pass (13.7s, fixture READY, 4 accounts); `doctor --expect-live` Metro up, `mm-2` Booted | Proved |
| Wallet/account/unlock preamble | State | Recipe nodes `wallet`, `account`, `unlock` pass | Proved |
| Environment + live position read | State | Recipe nodes `environment`, `positions` pass | Proved |
| AC7 Cross badge | Mixed | — | **Not reached** |
| AC8 numeric venue liquidation | Mixed | — | **Not reached** |
| AC8b legitimate null liquidation | Mixed | — | **Not reached** |
| AC10 shared liquidation explanation | Mixed | — | **Not reached** |
| AC11 Margin used and edit suppression | Mixed | — | **Not reached** |
| Existing privacy / isolated / compact-card contracts | State | 5 affected suites pass, 112/112 tests on the rebased base | Proved |

Run result: 5 passed / 1 failed of 6 nodes, `status: fail`, cause `subject: 1`.

## Why the display criteria were not reached

The run stops at `require-cross`, whose stated intent is *"Require exactly one live position so shared
value selectors cannot match another market"*. It asserts `$.positions length_eq 1` against
`selected-account-live-positions.json`, which currently holds `positions: []`. Every display assertion
(`pro-open`, `pro-scroll`, and the badge / liquidation / explanation / margin nodes) is downstream of
that gate.

This is a precondition the recipe requires but does not establish. The inherited coverage document
records the cause directly: *"Final fixtures have been closed, ETH restored to isolated 3x"* — the
authored run closed its own positions on completion, so the fixture the recipe depends on no longer
exists. `git diff origin/main...HEAD --name-only` confirms the branch touches no fixture, runtime, or
`temp/` data, so the failure is attributable to neither the rebase nor any change in this PR.

## Limits

No visual proof, no Android execution, and no re-proof of AC7/AC8/AC8b/AC10/AC11 is claimed for this
run. Replay requires re-seeding one authorized testnet Cross position and a refreshed venue
liquidation expectation. Unit-level coverage of the display code stands on the 5 passing suites and
Sonar's 98.9% new-code coverage.
