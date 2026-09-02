# Learnings — PR #35573 pr-complete

- A fire-and-forget failure path that sets `dismissWhenShown` still owns the navigation listener. Nulling the guard or the session without `dispose()` leaves that listener armed against the next confirmation.
- Pay With is the same deposit flow, not "user left confirmation". Treat those routes as focused confirmation or a later prep failure leaves the empty amount screen up.
- `waitFor` on a `setTimeout(0)` deposit prep is still a flake even when sibling tests use fake timers. Any test that calls `handleAddFunds` and then asserts prep settlement needs `runAllTimersAsync`.
- Flaky-detector J9 can flag a `let` binding that the outer `beforeEach` already resets. Check HEAD before changing test setup.
- Unrelated loader-enum to string swaps and extra hook mocks showed up in the dirty tree from a prior attempt. Revert anything that is not the comment.
