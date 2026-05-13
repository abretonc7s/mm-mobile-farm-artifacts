# PR Review: #30114 — fix: hw account abstraction migration

**Tier:** standard

## Summary

This PR prevents Perps from triggering signing prompts for hardware wallet users while the screen is idle. Previously, only the `dexAbstraction` mode was deferred; now `default` and `disabled` modes are also deferred during passive initialization. The fix extracts a shared helper (`shouldDeferUnifiedAccountSetup`), expands hardware wallet detection to cover Trezor, OneKey, and Lattice keyrings (in addition to existing Ledger and QR), and updates tests accordingly.

The PR achieves its stated goal cleanly with minimal code changes and good test coverage.

## Recipe Coverage

Recipe skipped — CDP offline, code review only.

| # | AC (verbatim) | Status | Reason |
|---|---------------|--------|--------|
| 1 | "When the user opens the Perps screen And leaves the Perps screen idle...Then the app does not repeatedly show hardware wallet signing prompts" | UNTESTABLE | CDP offline — no live device validation; code review + test verification only |
| 2 | "When the user opens the Perps screen Then Perps can complete the setup flow during initialization And the first trade can use unified collateral without an extra setup step" | UNTESTABLE | CDP offline — no live device validation; code review + test verification only |

Overall recipe coverage: 0/2 ACs PROVEN
Untestable: AC1, AC2 — CDP offline, code review only

> Warning: Coverage escalation: AC1, AC2 not proven on device.
>   Reason: CDP offline in this slot — no live device validation possible.
>   Human reviewer must validate manually before merging.

## Prior Reviews

No prior reviews.

## Acceptance Criteria Validation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | HW wallet idle signing prevention | PASS (code review) | `shouldDeferUnifiedAccountSetup` defers `dexAbstraction`, `default`, `disabled` when `!allowUserSigning`; called from `#ensureReady()` with `allowUserSigning: !isSelectedHardwareWallet()`. Tests verify all 3 modes are deferred. |
| 2 | Software wallet init-time setup | PASS (code review) | `allowUserSigning: true` for software wallets passes through `shouldDeferUnifiedAccountSetup` (returns false), allowing migration to proceed during init. Existing test `calls userSetAbstraction on init for software-wallet dexAbstraction users` validates this path. |

## Code Quality

- Pattern adherence: Follows codebase conventions — Set-based keyring detection, dedicated utility file with tests, `it.each` for parameterized tests
- Complexity: Appropriate — minimal helper function, no over-engineering
- Type safety: Good — uses `HyperLiquidAbstractionMode` type, no `as any` casts added
- Error handling: N/A — the helper is a pure predicate with no error paths
- Anti-pattern findings: No magic strings (keyring types are in a named constant set), no controller portability violations, no missing event tracking

## Fix Quality

- **Best approach:** This is the correct fix. Extracting `shouldDeferUnifiedAccountSetup` to a shared utility is cleaner than inlining the expanded condition. The Set-based approach for `MIGRATABLE_ABSTRACTION_MODES` mirrors the existing `HARDWARE_KEYRING_TYPES` pattern.
- **Would not ship:** Nothing — this is ready to ship.
- **Test quality:** Tests assert the right behavior — all 3 migratable modes are tested for both defer and allow paths, plus 2 non-migratable modes (`unifiedAccount`, `portfolioMargin`) and `undefined`. The `it.each` in `HyperLiquidProvider.test.ts` was correctly expanded from a single `dexAbstraction` case to all 3 modes. Tests would fail if the fix is reverted.
- **Brittleness:** Low risk. `MIGRATABLE_ABSTRACTION_MODES` in the utility and the explicit guard in HyperLiquidProvider.ts (line 747-751) enumerate the same modes — if a new mode is added to one but not the other, behavior would be inconsistent. This is a minor maintenance concern, not a blocker.
- **Core sync divergence:** Mobile's `HARDWARE_KEYRING_TYPES` now has 5 entries (added Trezor, OneKey, Lattice) but `core/packages/perps-controller/src/services/HyperLiquidWalletService.ts` still only lists Ledger + QR. The file comment says it's "inlined to keep this service portable between mobile and the core monorepo" — the two are now out of sync. A matching core PR should follow.

## Live Validation

- Recipe: skipped (CDP offline)
- Result: SKIPPED
- Video: skipped (CDP offline)
- Native changes: none
- Metro errors: Circuit breaker warnings (pre-existing, unrelated to PR)
- Log monitoring: Metro logs checked, no PR-related errors

## Correctness

- Diff vs stated goal: Aligned — defers all signing-backed migrations for hardware wallets, not just `dexAbstraction`
- Edge cases: Covered — `undefined` mode (new account with no abstraction data) correctly returns `false` (no deferral). `portfolioMargin` and `unifiedAccount` are handled upstream before reaching the defer check.
- Race conditions: None introduced — the in-flight lock mechanism is unchanged
- Backward compatibility: Preserved — software wallet behavior unchanged; hardware wallets get stricter deferral (more conservative, not breaking)

## Static Analysis

- lint:tsc: PASS — 0 errors
- Tests: 371/371 pass (3 suites: HyperLiquidProvider, HyperLiquidWalletService, hyperLiquidAbstraction)

## Architecture & Domain

- The new `hyperLiquidAbstraction.ts` utility is well-placed in `controllers/perps/utils/` — portable, testable, no mobile imports.
- Hardware keyring type strings are inlined (mirroring `@metamask/keyring-controller`) to keep the service portable between mobile and core monorepo, which aligns with the existing comment in `HyperLiquidWalletService.ts:17`.
- Note: `HyperLiquidProvider.ts` (8,633 lines) and its test file (10,751 lines) are well above the 2,500-line guardrail. This PR is net-positive (extracts logic out) but the files remain cautionary examples of unchecked growth.

## Risk Assessment

- LOW — Conservative behavioral change that defers more operations for hardware wallets. Software wallet path is unchanged. Comprehensive test coverage. No new UI, no state schema changes.

## Recommended Action

APPROVE

Clean, well-tested fix that achieves its stated goal. No issues found that would block merge. Human reviewer should validate the hardware wallet prompting behavior on a physical device since CDP was offline for this review.
