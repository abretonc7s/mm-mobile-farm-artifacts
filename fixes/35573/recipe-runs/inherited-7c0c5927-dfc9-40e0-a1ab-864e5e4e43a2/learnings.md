# Learnings — PR #35573 follow-up

- Fire-and-forget `setTimeout` + promise settlement must be generation-aware. Cancelling only the navigation guard leaves the first prep running; its `.then`/`.catch` can null the latest cancel ref or dismiss the confirmation the user is on.
- Two call sites (home actions and market details) copied the same race. Own the timeout in one session helper so the second tap replaces the guard and does not start a second `depositWithConfirmation()`.
- `jest.clearAllMocks()` does not drop `mockImplementation`. A hanging deposit mock from a double-tap test leaked into `onAddFundsSuccess` until `mockReset()` in `beforeEach`.
- Fake-timer tests in a nested describe still leak into sibling `waitFor` tests. Keep every deferred-prep assertion inside the fake-timer block and flush with `runAllTimersAsync`.
- `afterEach` `setTimeout(0)` as a drain is a hang waiting to happen next to fake timers. Prefer explicit timer control over a sleep barrier.
