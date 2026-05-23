# Learnings — PR #29420 Review

- **AccountTreeController is the canonical multichain selector source**: `selectSelectedAccountGroupInternalAccounts` and derivatives from `accountTreeController.ts` are the correct way to get accounts for a selected group. The old `selectSelectedInternalAccountFormattedAddress` from `accountsController.ts` returns whatever account type is selected, including non-EVM.

- **`isEvmAccountType` from `@metamask/keyring-api`** is the canonical EVM type check — not string matching against `eip155:`. The keyring-api function handles all EVM account type variants.

- **log_watch timing caveat**: When `log_watch` executes in ~129ms but is configured with `window_seconds: 10`, the actual scan window may be shorter than expected. The `watch_counts: {}` empty result means no matches were found, but the absence proof is limited to the actual execution window. For stronger absence proof, a longer real-time wait before the log_watch scan would be needed.

- **trace.json lives in `.agent/recipe-runs/`**, not in the recipe artifacts directory. Always check `.agent/recipe-runs/<timestamp>/trace.json` and `summary.json` for authoritative recipe evidence.

- **Dead test mocks accumulate during selector migrations**: When production code migrates from one selector to another, test files that mock the old selector at the module level (`jest.mock(...)`) keep working because Jest doesn't care if the mock is unused. These dead mocks should be cleaned up to avoid confusion.

- **Video recording with `xcrun simctl io` requires kill by PID, not job spec**: `kill -INT %1` may not reach the background process correctly. Use `pgrep -f "simctl io"` to find the PID and `kill -INT <PID>` directly.

- **Perps hooks follow a consistent address-derivation pattern**: All hooks that need the user's EVM address use `const evmAccount = useSelector(selectSelectedAccountGroupEvmInternalAccount); const selectedAddress = evmAccount?.address;` with existing `if (!selectedAddress)` guards handling the undefined case.

- **PR already has 2 domain-expert approvals** (ccharly, michalconsensys) — review comments from ccharly were addressed in commit fbd28d57. No CHANGES_REQUESTED reviews exist.
