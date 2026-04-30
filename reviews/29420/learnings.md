# Learnings — PR #29420 Review

- **AccountTreeController is the canonical multichain source**: `AccountsController.state.selectedAccount` can return non-EVM accounts. Always use `AccountTreeController` selectors for account group resolution, filtering by `isEvmAccountType` when EVM-specific behavior is needed.

- **Fixture accounts include non-EVM types**: The test wallet's account group has Solana (`solana:data-account`), Bitcoin (`bip122:p2wpkh`), and Tron (`tron:eoa`) accounts alongside EVM, making it easy to validate non-EVM scenarios via CDP eval.

- **Recipe AC3/AC4 assertions are weak by design**: When ACs are primarily code-review or unit-test concerns (not runtime-testable), the recipe nodes are effectively static assertions. This is acceptable when paired with actual code review and test execution, but should be acknowledged in the coverage matrix.

- **iOS simulator video recording is unreliable**: `xcrun simctl io mm-1 recordVideo` fails with `SimRenderServer.SimulatorError Code=2` in some environments. AC-bound screenshots from the recipe runner are sufficient evidence when video fails.

- **Dead test mocks after selector migration**: When migrating from one selector to another across multiple files, check that test mocks for the old selector are cleaned up. They're harmless but create confusion about which selector is actually being tested.

- **Selector composition pattern**: `selectSelectedAccountGroupEvmInternalAccount` is a good example of composing selectors — it builds on `selectSelectedAccountGroupInternalAccounts` and adds a filter. This is the recommended pattern for derived selector state.

- **The `?.address` pattern is consistent**: All migrated hooks use `evmAccount?.address` which produces `string | undefined` — matching the previous `selectSelectedInternalAccountFormattedAddress` return type semantics. Downstream guards like `if (!userAddress)` work identically.

- **Recipe runner doesn't always produce trace.json**: When reviewing recipe results, rely on stdout pass/fail counts when trace.json is absent.
