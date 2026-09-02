<!-- metamask-flaky-test-detection -->
## 🧪 Flaky unit test detection

### Run history flaky detection

[View recent run history](https://github.com/MetaMask/metamask-mobile/actions/workflows/ci.yml?query=branch%3Amain)

Historical failure rate is a hint, not proof — review each suggestion in context. See the [flaky-test-detection skill](https://github.com/MetaMask/skills/blob/main/domains/coding/skills/flaky-test-detection/skill.md) for the full pattern reference and manual audit workflow.

Failures / runs sampled per window:

| File | 7d | 15d | 30d |
|---|---|---|---|
| `app/components/UI/Perps/Views/PerpsMarketDetailsView/PerpsMarketDetailsView.test.tsx` | 0/191 | 0/286 | 0/431 |
| `app/components/UI/Perps/hooks/usePerpsHomeActions.test.ts` | 0/191 | 0/286 | 0/431 |


### AI-detected flaky patterns

#### `app/components/UI/Perps/Views/PerpsMarketDetailsView/PerpsMarketDetailsView.test.tsx`

- **J8 — jest.useFakeTimers() combined with waitFor (polling conflict)** (high)
  - This test calls `jest.useFakeTimers()` mid-test (after the component has already been rendered under real timers). Switching timer mode after rendering can leave React's internal scheduler in an inconsistent state. The `finally` block restores real timers, but if an exception is thrown inside `act()` before `finally` executes, the fake-timer mode leaks into subsequent tests. Other tests in the same file use `waitFor()` (which polls via real `setTimeout`); if fake timers are still active when those tests run, `waitFor` will never resolve and the suite will time out. The fix is to call `jest.useFakeTimers()` before rendering (ideally in a `beforeEach` scoped to a nested describe), so the timer mode is consistent throughout the test and is always restored before the next test begins.
  - Suggested fix in [`app/components/UI/Perps/Views/PerpsMarketDetailsView/PerpsMarketDetailsView.test.tsx:1825`](https://github.com/MetaMask/metamask-mobile/blob/f38520bd51bb1edcbcb7078e3cd786143d3eea94/app/components/UI/Perps/Views/PerpsMarketDetailsView/PerpsMarketDetailsView.test.tsx#L1825):
    ```diff
    -      jest.useFakeTimers();
    -      try {
    -        await act(async () => {
    -          fireEvent.press(addFundsButton);
    -        });
    -
    -        expect(mockNavigateToConfirmation).toHaveBeenCalledWith({
    -          loader: 'customAmount',
    -          stack: 'Perps',
    -        });
    -        expect(mockDepositWithConfirmation).not.toHaveBeenCalled();
    -
    -        await act(async () => {
    -          jest.runAllTimers();
    -        });
    -
    -        expect(mockDepositWithConfirmation).toHaveBeenCalled();
    -      } finally {
    -        jest.useRealTimers();
    -      }
    +      // Wrap in a nested describe with beforeEach/afterEach to guarantee
    +      // timer restoration even on failure:
    +      //
    +      // describe('deferred deposit', () => {
    +      //   beforeEach(() => { jest.useFakeTimers(); });
    +      //   afterEach(() => { jest.useRealTimers(); });
    +      //
    +      //   it('calls navigateToConfirmation and depositWithConfirmation when add funds is pressed', async () => {
    +      //     ... render component here, AFTER useFakeTimers() ...
    +      //     await act(async () => { fireEvent.press(addFundsButton); });
    +      //     expect(mockNavigateToConfirmation).toHaveBeenCalledWith({ loader: 'customAmount', stack: 'Perps' });
    +      //     expect(mockDepositWithConfirmation).not.toHaveBeenCalled();
    +      //     await act(async () => { jest.runAllTimers(); });
    +      //     expect(mockDepositWithConfirmation).toHaveBeenCalled();
    +      //   });
    +      // });
    ```

#### `app/components/UI/Perps/hooks/usePerpsHomeActions.test.ts`

- **J6 — Arbitrary setTimeout/sleep used as a synchronization barrier** (high)
  - The `afterEach` in the `handleAddFunds - eligible user` describe block uses `await new Promise((resolve) => setTimeout(resolve, 0))` as a zero-delay flush to drain pending microtasks/promises. Even a zero-delay `setTimeout` is a real timer and is non-deterministic under CI load — it can fire too early or too late relative to the async work it is meant to drain. More critically, the very next test in this describe block (`'navigates to confirmation without waiting for deposit prep'`) calls `jest.useFakeTimers()`. When that test runs, the `afterEach` fires while fake timers are still active (before `jest.useRealTimers()` is called in the test's `finally` block), so the `setTimeout(resolve, 0)` inside `afterEach` is registered as a fake timer and **never fires**, causing the `afterEach` to hang indefinitely and the test suite to time out. The correct fix is to replace the sleep with a `waitFor` assertion on the actual condition that needs to be settled, or simply remove the `afterEach` if no real condition needs draining.
  - Suggested fix in [`app/components/UI/Perps/hooks/usePerpsHomeActions.test.ts:167`](https://github.com/MetaMask/metamask-mobile/blob/f38520bd51bb1edcbcb7078e3cd786143d3eea94/app/components/UI/Perps/hooks/usePerpsHomeActions.test.ts#L167):
    ```diff
    -    afterEach(async () => {
    -      await act(async () => {
    -        await new Promise((resolve) => setTimeout(resolve, 0));
    -      });
    -    });
    +    // Remove the afterEach sleep entirely — each test already uses
    +    // `await act(async () => { ... })` which drains pending state updates.
    +    // If a specific settled condition must be verified, use waitFor with
    +    // a real assertion instead:
    +    //
    +    // afterEach(async () => {
    +    //   await waitFor(() => {
    +    //     expect(result.current.isProcessing).toBe(false);
    +    //   });
    +    // });
    ```
- **J8 — jest.useFakeTimers() combined with waitFor (polling conflict)** (high)
  - This test calls `jest.useFakeTimers()` at the top of the test body and restores real timers in a `finally` block. The problem is that the `afterEach` hook in the same describe block runs **after** the `finally` block, but the `afterEach` contains `await new Promise((resolve) => setTimeout(resolve, 0))`. If `jest.useRealTimers()` in `finally` runs before `afterEach`, the `afterEach` should be fine — but the ordering is not guaranteed when `act()` is involved. Additionally, `waitFor` (used in sibling tests in this describe block) polls via real `setTimeout` internally; if fake timers are still active when `waitFor` is called (e.g., due to test ordering or a thrown exception before `finally`), `waitFor` will never resolve. The safest fix is to move `jest.useFakeTimers()` / `jest.useRealTimers()` into `beforeEach` / `afterEach` hooks so the timer mode is always restored before the shared `afterEach` runs.
  - Suggested fix in [`app/components/UI/Perps/hooks/usePerpsHomeActions.test.ts:196`](https://github.com/MetaMask/metamask-mobile/blob/f38520bd51bb1edcbcb7078e3cd786143d3eea94/app/components/UI/Perps/hooks/usePerpsHomeActions.test.ts#L196):
    ```diff
    -    it('navigates to confirmation without waiting for deposit prep', async () => {
    -      jest.useFakeTimers();
    -      let resolveDeposit: () => void = () => undefined;
    -      mockDepositWithConfirmation.mockReturnValue(
    -        new Promise<void>((resolve) => {
    -          resolveDeposit = resolve;
    -        }),
    -      );
    -
    -      const { result } = renderHook(() => usePerpsHomeActions());
    -
    -      try {
    -        await act(async () => {
    -          await result.current.handleAddFunds();
    -        });
    -
    -        expect(mockNavigateToConfirmation).toHaveBeenCalledTimes(1);
    -        expect(mockDepositWithConfirmation).not.toHaveBeenCalled();
    -
    -        await act(async () => {
    -          jest.runAllTimers();
    -        });
    -
    -        expect(mockDepositWithConfirmation).toHaveBeenCalledTimes(1);
    -
    -        await act(async () => {
    -          resolveDeposit();
    -        });
    -      } finally {
    -        jest.useRealTimers();
    -      }
    -    });
    +    // Move fake-timer setup into beforeEach/afterEach so restoration
    +    // is guaranteed before the shared afterEach runs.
    +    it('navigates to confirmation without waiting for deposit prep', async () => {
    +      // jest.useFakeTimers() is now set up in a beforeEach for this test,
    +      // or use a nested describe with its own beforeEach/afterEach:
    +      let resolveDeposit: () => void = () => undefined;
    +      mockDepositWithConfirmation.mockReturnValue(
    +        new Promise<void>((resolve) => {
    +          resolveDeposit = resolve;
    +        }),
    +      );
    +
    +      const { result } = renderHook(() => usePerpsHomeActions());
    +
    +      await act(async () => {
    +        await result.current.handleAddFunds();
    +      });
    +
    +      expect(mockNavigateToConfirmation).toHaveBeenCalledTimes(1);
    +      expect(mockDepositWithConfirmation).not.toHaveBeenCalled();
    +
    +      await act(async () => {
    +        jest.runAllTimers();
    +      });
    +
    +      expect(mockDepositWithConfirmation).toHaveBeenCalledTimes(1);
    +
    +      await act(async () => {
    +        resolveDeposit();
    +      });
    +    });
    ```


_This check is informational only and does not block merging._
<!-- metamask-flaky-test-detection-metadata=eyJ2ZXJzaW9uIjoxLCJ3aW5kb3dzIjpbNywxNSwzMF0sImZpbGVzIjp7ImFwcC9jb21wb25lbnRzL1VJL1BlcnBzL1ZpZXdzL1BlcnBzTWFya2V0RGV0YWlsc1ZpZXcvUGVycHNNYXJrZXREZXRhaWxzVmlldy50ZXN0LnRzeCI6eyJhbmFseXplZFNoYSI6ImYzODUyMGJkNTFiYjFlZGNiY2I3MDc4ZTNjZDc4NjE0M2QzZWVhOTQiLCJmaW5kaW5ncyI6W3siZmlsZSI6ImFwcC9jb21wb25lbnRzL1VJL1BlcnBzL1ZpZXdzL1BlcnBzTWFya2V0RGV0YWlsc1ZpZXcvUGVycHNNYXJrZXREZXRhaWxzVmlldy50ZXN0LnRzeCIsInBhdHRlcm5JZCI6Iko4IiwicGF0dGVybk5hbWUiOiJqZXN0LnVzZUZha2VUaW1lcnMoKSBjb21iaW5lZCB3aXRoIHdhaXRGb3IgKHBvbGxpbmcgY29uZmxpY3QpIiwic2V2ZXJpdHkiOiJoaWdoIiwibGluZSI6MTgyNSwic25pcHBldCI6IiAgICAgIGplc3QudXNlRmFrZVRpbWVycygpO1xuICAgICAgdHJ5IHtcbiAgICAgICAgYXdhaXQgYWN0KGFzeW5jICgpID0+IHtcbiAgICAgICAgICBmaXJlRXZlbnQucHJlc3MoYWRkRnVuZHNCdXR0b24pO1xuICAgICAgICB9KTtcblxuICAgICAgICBleHBlY3QobW9ja05hdmlnYXRlVG9Db25maXJtYXRpb24pLnRvSGF2ZUJlZW5DYWxsZWRXaXRoKHtcbiAgICAgICAgICBsb2FkZXI6ICdjdXN0b21BbW91bnQnLFxuICAgICAgICAgIHN0YWNrOiAnUGVycHMnLFxuICAgICAgICB9KTtcbiAgICAgICAgZXhwZWN0KG1vY2tEZXBvc2l0V2l0aENvbmZpcm1hdGlvbikubm90LnRvSGF2ZUJlZW5DYWxsZWQoKTtcblxuICAgICAgICBhd2FpdCBhY3QoYXN5bmMgKCkgPT4ge1xuICAgICAgICAgIGplc3QucnVuQWxsVGltZXJzKCk7XG4gICAgICAgIH0pO1xuXG4gICAgICAgIGV4cGVjdChtb2NrRGVwb3NpdFdpdGhDb25maXJtYXRpb24pLnRvSGF2ZUJlZW5DYWxsZWQoKTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGplc3QudXNlUmVhbFRpbWVycygpO1xuICAgICAgfSIsImV4cGxhbmF0aW9uIjoiVGhpcyB0ZXN0IGNhbGxzIGBqZXN0LnVzZUZha2VUaW1lcnMoKWAgbWlkLXRlc3QgKGFmdGVyIHRoZSBjb21wb25lbnQgaGFzIGFscmVhZHkgYmVlbiByZW5kZXJlZCB1bmRlciByZWFsIHRpbWVycykuIFN3aXRjaGluZyB0aW1lciBtb2RlIGFmdGVyIHJlbmRlcmluZyBjYW4gbGVhdmUgUmVhY3QncyBpbnRlcm5hbCBzY2hlZHVsZXIgaW4gYW4gaW5jb25zaXN0ZW50IHN0YXRlLiBUaGUgYGZpbmFsbHlgIGJsb2NrIHJlc3RvcmVzIHJlYWwgdGltZXJzLCBidXQgaWYgYW4gZXhjZXB0aW9uIGlzIHRocm93biBpbnNpZGUgYGFjdCgpYCBiZWZvcmUgYGZpbmFsbHlgIGV4ZWN1dGVzLCB0aGUgZmFrZS10aW1lciBtb2RlIGxlYWtzIGludG8gc3Vic2VxdWVudCB0ZXN0cy4gT3RoZXIgdGVzdHMgaW4gdGhlIHNhbWUgZmlsZSB1c2UgYHdhaXRGb3IoKWAgKHdoaWNoIHBvbGxzIHZpYSByZWFsIGBzZXRUaW1lb3V0YCk7IGlmIGZha2UgdGltZXJzIGFyZSBzdGlsbCBhY3RpdmUgd2hlbiB0aG9zZSB0ZXN0cyBydW4sIGB3YWl0Rm9yYCB3aWxsIG5ldmVyIHJlc29sdmUgYW5kIHRoZSBzdWl0ZSB3aWxsIHRpbWUgb3V0LiBUaGUgZml4IGlzIHRvIGNhbGwgYGplc3QudXNlRmFrZVRpbWVycygpYCBiZWZvcmUgcmVuZGVyaW5nIChpZGVhbGx5IGluIGEgYGJlZm9yZUVhY2hgIHNjb3BlZCB0byBhIG5lc3RlZCBkZXNjcmliZSksIHNvIHRoZSB0aW1lciBtb2RlIGlzIGNvbnNpc3RlbnQgdGhyb3VnaG91dCB0aGUgdGVzdCBhbmQgaXMgYWx3YXlzIHJlc3RvcmVkIGJlZm9yZSB0aGUgbmV4dCB0ZXN0IGJlZ2lucy4iLCJzdWdnZXN0ZWRGaXgiOiIgICAgICAvLyBXcmFwIGluIGEgbmVzdGVkIGRlc2NyaWJlIHdpdGggYmVmb3JlRWFjaC9hZnRlckVhY2ggdG8gZ3VhcmFudGVlXG4gICAgICAvLyB0aW1lciByZXN0b3JhdGlvbiBldmVuIG9uIGZhaWx1cmU6XG4gICAgICAvL1xuICAgICAgLy8gZGVzY3JpYmUoJ2RlZmVycmVkIGRlcG9zaXQnLCAoKSA9PiB7XG4gICAgICAvLyAgIGJlZm9yZUVhY2goKCkgPT4geyBqZXN0LnVzZUZha2VUaW1lcnMoKTsgfSk7XG4gICAgICAvLyAgIGFmdGVyRWFjaCgoKSA9PiB7IGplc3QudXNlUmVhbFRpbWVycygpOyB9KTtcbiAgICAgIC8vXG4gICAgICAvLyAgIGl0KCdjYWxscyBuYXZpZ2F0ZVRvQ29uZmlybWF0aW9uIGFuZCBkZXBvc2l0V2l0aENvbmZpcm1hdGlvbiB3aGVuIGFkZCBmdW5kcyBpcyBwcmVzc2VkJywgYXN5bmMgKCkgPT4ge1xuICAgICAgLy8gICAgIC4uLiByZW5kZXIgY29tcG9uZW50IGhlcmUsIEFGVEVSIHVzZUZha2VUaW1lcnMoKSAuLi5cbiAgICAgIC8vICAgICBhd2FpdCBhY3QoYXN5bmMgKCkgPT4geyBmaXJlRXZlbnQucHJlc3MoYWRkRnVuZHNCdXR0b24pOyB9KTtcbiAgICAgIC8vICAgICBleHBlY3QobW9ja05hdmlnYXRlVG9Db25maXJtYXRpb24pLnRvSGF2ZUJlZW5DYWxsZWRXaXRoKHsgbG9hZGVyOiAnY3VzdG9tQW1vdW50Jywgc3RhY2s6ICdQZXJwcycgfSk7XG4gICAgICAvLyAgICAgZXhwZWN0KG1vY2tEZXBvc2l0V2l0aENvbmZpcm1hdGlvbikubm90LnRvSGF2ZUJlZW5DYWxsZWQoKTtcbiAgICAgIC8vICAgICBhd2FpdCBhY3QoYXN5bmMgKCkgPT4geyBqZXN0LnJ1bkFsbFRpbWVycygpOyB9KTtcbiAgICAgIC8vICAgICBleHBlY3QobW9ja0RlcG9zaXRXaXRoQ29uZmlybWF0aW9uKS50b0hhdmVCZWVuQ2FsbGVkKCk7XG4gICAgICAvLyAgIH0pO1xuICAgICAgLy8gfSk7IiwiaGlzdG9yaWNhbEhpbnRVc2VkIjpmYWxzZX1dfSwiYXBwL2NvbXBvbmVudHMvVUkvUGVycHMvaG9va3MvdXNlUGVycHNIb21lQWN0aW9ucy50ZXN0LnRzIjp7ImFuYWx5emVkU2hhIjoiZjM4NTIwYmQ1MWJiMWVkY2JjYjcwNzhlM2NkNzg2MTQzZDNlZWE5NCIsImZpbmRpbmdzIjpbeyJmaWxlIjoiYXBwL2NvbXBvbmVudHMvVUkvUGVycHMvaG9va3MvdXNlUGVycHNIb21lQWN0aW9ucy50ZXN0LnRzIiwicGF0dGVybklkIjoiSjYiLCJwYXR0ZXJuTmFtZSI6IkFyYml0cmFyeSBzZXRUaW1lb3V0L3NsZWVwIHVzZWQgYXMgYSBzeW5jaHJvbml6YXRpb24gYmFycmllciIsInNldmVyaXR5IjoiaGlnaCIsImxpbmUiOjE2Nywic25pcHBldCI6IiAgICBhZnRlckVhY2goYXN5bmMgKCkgPT4ge1xuICAgICAgYXdhaXQgYWN0KGFzeW5jICgpID0+IHtcbiAgICAgICAgYXdhaXQgbmV3IFByb21pc2UoKHJlc29sdmUpID0+IHNldFRpbWVvdXQocmVzb2x2ZSwgMCkpO1xuICAgICAgfSk7XG4gICAgfSk7IiwiZXhwbGFuYXRpb24iOiJUaGUgYGFmdGVyRWFjaGAgaW4gdGhlIGBoYW5kbGVBZGRGdW5kcyAtIGVsaWdpYmxlIHVzZXJgIGRlc2NyaWJlIGJsb2NrIHVzZXMgYGF3YWl0IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiBzZXRUaW1lb3V0KHJlc29sdmUsIDApKWAgYXMgYSB6ZXJvLWRlbGF5IGZsdXNoIHRvIGRyYWluIHBlbmRpbmcgbWljcm90YXNrcy9wcm9taXNlcy4gRXZlbiBhIHplcm8tZGVsYXkgYHNldFRpbWVvdXRgIGlzIGEgcmVhbCB0aW1lciBhbmQgaXMgbm9uLWRldGVybWluaXN0aWMgdW5kZXIgQ0kgbG9hZCDigJQgaXQgY2FuIGZpcmUgdG9vIGVhcmx5IG9yIHRvbyBsYXRlIHJlbGF0aXZlIHRvIHRoZSBhc3luYyB3b3JrIGl0IGlzIG1lYW50IHRvIGRyYWluLiBNb3JlIGNyaXRpY2FsbHksIHRoZSB2ZXJ5IG5leHQgdGVzdCBpbiB0aGlzIGRlc2NyaWJlIGJsb2NrIChgJ25hdmlnYXRlcyB0byBjb25maXJtYXRpb24gd2l0aG91dCB3YWl0aW5nIGZvciBkZXBvc2l0IHByZXAnYCkgY2FsbHMgYGplc3QudXNlRmFrZVRpbWVycygpYC4gV2hlbiB0aGF0IHRlc3QgcnVucywgdGhlIGBhZnRlckVhY2hgIGZpcmVzIHdoaWxlIGZha2UgdGltZXJzIGFyZSBzdGlsbCBhY3RpdmUgKGJlZm9yZSBgamVzdC51c2VSZWFsVGltZXJzKClgIGlzIGNhbGxlZCBpbiB0aGUgdGVzdCdzIGBmaW5hbGx5YCBibG9jayksIHNvIHRoZSBgc2V0VGltZW91dChyZXNvbHZlLCAwKWAgaW5zaWRlIGBhZnRlckVhY2hgIGlzIHJlZ2lzdGVyZWQgYXMgYSBmYWtlIHRpbWVyIGFuZCAqKm5ldmVyIGZpcmVzKiosIGNhdXNpbmcgdGhlIGBhZnRlckVhY2hgIHRvIGhhbmcgaW5kZWZpbml0ZWx5IGFuZCB0aGUgdGVzdCBzdWl0ZSB0byB0aW1lIG91dC4gVGhlIGNvcnJlY3QgZml4IGlzIHRvIHJlcGxhY2UgdGhlIHNsZWVwIHdpdGggYSBgd2FpdEZvcmAgYXNzZXJ0aW9uIG9uIHRoZSBhY3R1YWwgY29uZGl0aW9uIHRoYXQgbmVlZHMgdG8gYmUgc2V0dGxlZCwgb3Igc2ltcGx5IHJlbW92ZSB0aGUgYGFmdGVyRWFjaGAgaWYgbm8gcmVhbCBjb25kaXRpb24gbmVlZHMgZHJhaW5pbmcuIiwic3VnZ2VzdGVkRml4IjoiICAgIC8vIFJlbW92ZSB0aGUgYWZ0ZXJFYWNoIHNsZWVwIGVudGlyZWx5IOKAlCBlYWNoIHRlc3QgYWxyZWFkeSB1c2VzXG4gICAgLy8gYGF3YWl0IGFjdChhc3luYyAoKSA9PiB7IC4uLiB9KWAgd2hpY2ggZHJhaW5zIHBlbmRpbmcgc3RhdGUgdXBkYXRlcy5cbiAgICAvLyBJZiBhIHNwZWNpZmljIHNldHRsZWQgY29uZGl0aW9uIG11c3QgYmUgdmVyaWZpZWQsIHVzZSB3YWl0Rm9yIHdpdGhcbiAgICAvLyBhIHJlYWwgYXNzZXJ0aW9uIGluc3RlYWQ6XG4gICAgLy9cbiAgICAvLyBhZnRlckVhY2goYXN5bmMgKCkgPT4ge1xuICAgIC8vICAgYXdhaXQgd2FpdEZvcigoKSA9PiB7XG4gICAgLy8gICAgIGV4cGVjdChyZXN1bHQuY3VycmVudC5pc1Byb2Nlc3NpbmcpLnRvQmUoZmFsc2UpO1xuICAgIC8vICAgfSk7XG4gICAgLy8gfSk7IiwiaGlzdG9yaWNhbEhpbnRVc2VkIjpmYWxzZX0seyJmaWxlIjoiYXBwL2NvbXBvbmVudHMvVUkvUGVycHMvaG9va3MvdXNlUGVycHNIb21lQWN0aW9ucy50ZXN0LnRzIiwicGF0dGVybklkIjoiSjgiLCJwYXR0ZXJuTmFtZSI6Implc3QudXNlRmFrZVRpbWVycygpIGNvbWJpbmVkIHdpdGggd2FpdEZvciAocG9sbGluZyBjb25mbGljdCkiLCJzZXZlcml0eSI6ImhpZ2giLCJsaW5lIjoxOTYsInNuaXBwZXQiOiIgICAgaXQoJ25hdmlnYXRlcyB0byBjb25maXJtYXRpb24gd2l0aG91dCB3YWl0aW5nIGZvciBkZXBvc2l0IHByZXAnLCBhc3luYyAoKSA9PiB7XG4gICAgICBqZXN0LnVzZUZha2VUaW1lcnMoKTtcbiAgICAgIGxldCByZXNvbHZlRGVwb3NpdDogKCkgPT4gdm9pZCA9ICgpID0+IHVuZGVmaW5lZDtcbiAgICAgIG1vY2tEZXBvc2l0V2l0aENvbmZpcm1hdGlvbi5tb2NrUmV0dXJuVmFsdWUoXG4gICAgICAgIG5ldyBQcm9taXNlPHZvaWQ+KChyZXNvbHZlKSA9PiB7XG4gICAgICAgICAgcmVzb2x2ZURlcG9zaXQgPSByZXNvbHZlO1xuICAgICAgICB9KSxcbiAgICAgICk7XG5cbiAgICAgIGNvbnN0IHsgcmVzdWx0IH0gPSByZW5kZXJIb29rKCgpID0+IHVzZVBlcnBzSG9tZUFjdGlvbnMoKSk7XG5cbiAgICAgIHRyeSB7XG4gICAgICAgIGF3YWl0IGFjdChhc3luYyAoKSA9PiB7XG4gICAgICAgICAgYXdhaXQgcmVzdWx0LmN1cnJlbnQuaGFuZGxlQWRkRnVuZHMoKTtcbiAgICAgICAgfSk7XG5cbiAgICAgICAgZXhwZWN0KG1vY2tOYXZpZ2F0ZVRvQ29uZmlybWF0aW9uKS50b0hhdmVCZWVuQ2FsbGVkVGltZXMoMSk7XG4gICAgICAgIGV4cGVjdChtb2NrRGVwb3NpdFdpdGhDb25maXJtYXRpb24pLm5vdC50b0hhdmVCZWVuQ2FsbGVkKCk7XG5cbiAgICAgICAgYXdhaXQgYWN0KGFzeW5jICgpID0+IHtcbiAgICAgICAgICBqZXN0LnJ1bkFsbFRpbWVycygpO1xuICAgICAgICB9KTtcblxuICAgICAgICBleHBlY3QobW9ja0RlcG9zaXRXaXRoQ29uZmlybWF0aW9uKS50b0hhdmVCZWVuQ2FsbGVkVGltZXMoMSk7XG5cbiAgICAgICAgYXdhaXQgYWN0KGFzeW5jICgpID0+IHtcbiAgICAgICAgICByZXNvbHZlRGVwb3NpdCgpO1xuICAgICAgICB9KTtcbiAgICAgIH0gZmluYWxseSB7XG4gICAgICAgIGplc3QudXNlUmVhbFRpbWVycygpO1xuICAgICAgfVxuICAgIH0pOyIsImV4cGxhbmF0aW9uIjoiVGhpcyB0ZXN0IGNhbGxzIGBqZXN0LnVzZUZha2VUaW1lcnMoKWAgYXQgdGhlIHRvcCBvZiB0aGUgdGVzdCBib2R5IGFuZCByZXN0b3JlcyByZWFsIHRpbWVycyBpbiBhIGBmaW5hbGx5YCBibG9jay4gVGhlIHByb2JsZW0gaXMgdGhhdCB0aGUgYGFmdGVyRWFjaGAgaG9vayBpbiB0aGUgc2FtZSBkZXNjcmliZSBibG9jayBydW5zICoqYWZ0ZXIqKiB0aGUgYGZpbmFsbHlgIGJsb2NrLCBidXQgdGhlIGBhZnRlckVhY2hgIGNvbnRhaW5zIGBhd2FpdCBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4gc2V0VGltZW91dChyZXNvbHZlLCAwKSlgLiBJZiBgamVzdC51c2VSZWFsVGltZXJzKClgIGluIGBmaW5hbGx5YCBydW5zIGJlZm9yZSBgYWZ0ZXJFYWNoYCwgdGhlIGBhZnRlckVhY2hgIHNob3VsZCBiZSBmaW5lIOKAlCBidXQgdGhlIG9yZGVyaW5nIGlzIG5vdCBndWFyYW50ZWVkIHdoZW4gYGFjdCgpYCBpcyBpbnZvbHZlZC4gQWRkaXRpb25hbGx5LCBgd2FpdEZvcmAgKHVzZWQgaW4gc2libGluZyB0ZXN0cyBpbiB0aGlzIGRlc2NyaWJlIGJsb2NrKSBwb2xscyB2aWEgcmVhbCBgc2V0VGltZW91dGAgaW50ZXJuYWxseTsgaWYgZmFrZSB0aW1lcnMgYXJlIHN0aWxsIGFjdGl2ZSB3aGVuIGB3YWl0Rm9yYCBpcyBjYWxsZWQgKGUuZy4sIGR1ZSB0byB0ZXN0IG9yZGVyaW5nIG9yIGEgdGhyb3duIGV4Y2VwdGlvbiBiZWZvcmUgYGZpbmFsbHlgKSwgYHdhaXRGb3JgIHdpbGwgbmV2ZXIgcmVzb2x2ZS4gVGhlIHNhZmVzdCBmaXggaXMgdG8gbW92ZSBgamVzdC51c2VGYWtlVGltZXJzKClgIC8gYGplc3QudXNlUmVhbFRpbWVycygpYCBpbnRvIGBiZWZvcmVFYWNoYCAvIGBhZnRlckVhY2hgIGhvb2tzIHNvIHRoZSB0aW1lciBtb2RlIGlzIGFsd2F5cyByZXN0b3JlZCBiZWZvcmUgdGhlIHNoYXJlZCBgYWZ0ZXJFYWNoYCBydW5zLiIsInN1Z2dlc3RlZEZpeCI6IiAgICAvLyBNb3ZlIGZha2UtdGltZXIgc2V0dXAgaW50byBiZWZvcmVFYWNoL2FmdGVyRWFjaCBzbyByZXN0b3JhdGlvblxuICAgIC8vIGlzIGd1YXJhbnRlZWQgYmVmb3JlIHRoZSBzaGFyZWQgYWZ0ZXJFYWNoIHJ1bnMuXG4gICAgaXQoJ25hdmlnYXRlcyB0byBjb25maXJtYXRpb24gd2l0aG91dCB3YWl0aW5nIGZvciBkZXBvc2l0IHByZXAnLCBhc3luYyAoKSA9PiB7XG4gICAgICAvLyBqZXN0LnVzZUZha2VUaW1lcnMoKSBpcyBub3cgc2V0IHVwIGluIGEgYmVmb3JlRWFjaCBmb3IgdGhpcyB0ZXN0LFxuICAgICAgLy8gb3IgdXNlIGEgbmVzdGVkIGRlc2NyaWJlIHdpdGggaXRzIG93biBiZWZvcmVFYWNoL2FmdGVyRWFjaDpcbiAgICAgIGxldCByZXNvbHZlRGVwb3NpdDogKCkgPT4gdm9pZCA9ICgpID0+IHVuZGVmaW5lZDtcbiAgICAgIG1vY2tEZXBvc2l0V2l0aENvbmZpcm1hdGlvbi5tb2NrUmV0dXJuVmFsdWUoXG4gICAgICAgIG5ldyBQcm9taXNlPHZvaWQ+KChyZXNvbHZlKSA9PiB7XG4gICAgICAgICAgcmVzb2x2ZURlcG9zaXQgPSByZXNvbHZlO1xuICAgICAgICB9KSxcbiAgICAgICk7XG5cbiAgICAgIGNvbnN0IHsgcmVzdWx0IH0gPSByZW5kZXJIb29rKCgpID0+IHVzZVBlcnBzSG9tZUFjdGlvbnMoKSk7XG5cbiAgICAgIGF3YWl0IGFjdChhc3luYyAoKSA9PiB7XG4gICAgICAgIGF3YWl0IHJlc3VsdC5jdXJyZW50LmhhbmRsZUFkZEZ1bmRzKCk7XG4gICAgICB9KTtcblxuICAgICAgZXhwZWN0KG1vY2tOYXZpZ2F0ZVRvQ29uZmlybWF0aW9uKS50b0hhdmVCZWVuQ2FsbGVkVGltZXMoMSk7XG4gICAgICBleHBlY3QobW9ja0RlcG9zaXRXaXRoQ29uZmlybWF0aW9uKS5ub3QudG9IYXZlQmVlbkNhbGxlZCgpO1xuXG4gICAgICBhd2FpdCBhY3QoYXN5bmMgKCkgPT4ge1xuICAgICAgICBqZXN0LnJ1bkFsbFRpbWVycygpO1xuICAgICAgfSk7XG5cbiAgICAgIGV4cGVjdChtb2NrRGVwb3NpdFdpdGhDb25maXJtYXRpb24pLnRvSGF2ZUJlZW5DYWxsZWRUaW1lcygxKTtcblxuICAgICAgYXdhaXQgYWN0KGFzeW5jICgpID0+IHtcbiAgICAgICAgcmVzb2x2ZURlcG9zaXQoKTtcbiAgICAgIH0pO1xuICAgIH0pOyIsImhpc3RvcmljYWxIaW50VXNlZCI6ZmFsc2V9XX0sImFwcC9jb21wb25lbnRzL1VJL1BlcnBzL3V0aWxzL2RlcG9zaXRDb25maXJtYXRpb25HdWFyZC50ZXN0LnRzIjp7ImFuYWx5emVkU2hhIjoiZjM4NTIwYmQ1MWJiMWVkY2JjYjcwNzhlM2NkNzg2MTQzZDNlZWE5NCIsImZpbmRpbmdzIjpbXX19fQ== -->
