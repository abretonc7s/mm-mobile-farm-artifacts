# Recipe coverage — PR #34789 pr-complete (this run)

Re-validation SKIPPED: `mm-harness launch --platform ios --preflight-mode fast` failed because the portable harness wrapper is missing and the runtime capability catalog has no providers. No on-device nodes were re-run.

Inherited family coverage (AC1–AC4 PROVEN on the parent run) lives at `inputs/inherited/recipe-coverage.md`. This run's review fix does not change those ACs: unknown pay-token balances stay unknown (`undefined`) rather than zero, which is the same gate the inherited recipe already exercises.

| # | AC | Proof mode this run | Evidence verdict |
|---|----|---------------------|------------------|
| 1 | At most one funding message; no false $0 available | state | DEFERRED — recipe skipped; unit tests for undefined-balance gating passed |
| 2 | Place-order button stays reachable after payment switch | state | DEFERRED — recipe skipped |
| 3 | Slider stays usable while pay-token balance is unresolved | state | COVERED by PerpsOrderView funding-state unit tests (135/135) |
| 4 | Below-minimum token shows the $10 minimum-order copy | state | COVERED by PerpsOrderView funding-state unit tests (135/135) |
