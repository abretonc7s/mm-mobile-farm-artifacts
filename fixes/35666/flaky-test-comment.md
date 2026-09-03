<!-- metamask-flaky-test-detection -->
## 🧪 Flaky unit test detection

### Run history flaky detection

[View recent run history](https://github.com/MetaMask/metamask-mobile/actions/workflows/ci.yml?query=branch%3Amain)

Historical failure rate is a hint, not proof — review each suggestion in context. See the [flaky-test-detection skill](https://github.com/MetaMask/skills/blob/main/domains/coding/skills/flaky-test-detection/skill.md) for the full pattern reference and manual audit workflow.

Failures / runs sampled per window:

| File | 7d | 15d | 30d |
|---|---|---|---|
| `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts` | 0/170 | 0/264 | 0/431 |
| `app/components/UI/Perps/utils/limitPriceFarFromMarket.test.ts` | 0/170 | 0/264 | 0/431 |


### AI-detected flaky patterns

#### `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts`

- **J9 — Module-level mutable let bindings not reset in beforeEach** (high)
  - There are ~25 module-level `let` variables that are mutated inside individual tests (e.g. `mockIsEligible = false`, `mockChaseOrders = [...]`, `mockExistingPosition = {...}`, `mockIsAtCap = true`, `mockEstimatedSlippageBps = 500`, `mockLivePrice = ''`, `mockIsInitialized = false`, `mockMarketData = null`, `mockPositionStreamLoading = true`, `mockMarketDataError = 'Market data request failed'`, `mockSizeDecimals = 2`, `mockTotalFee`, `mockPerpsNetwork`, `mockSelectedAddress`, `mockPositionModifyPreview`, `mockValidateCalculatedMargin`, etc.). The `beforeEach` only resets `mockExecutionOptions`, `mockOrderForm.type`, and `mockOrderForm.direction` (plus calling `jest.clearAllMocks()`). Any test that mutates one of the other `let` variables leaves that mutation in place for all subsequent tests, causing order-dependent failures. Additionally, `mockOrderForm` is a `const` object whose properties (`amount`, `leverage`, `balancePercent`, `limitPrice`, `takeProfitPrice`, `stopLossPrice`) are mutated in tests but not restored in `beforeEach`. The new `far-from-market` describe block added in this PR also relies on these shared mutable variables (e.g. `mockOrderForm.type`, scale order state), so it inherits the same risk.
  - Suggested fix in [`app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts:57`](https://github.com/MetaMask/metamask-mobile/blob/46bd085def048c3dd067606b83eda95f1d02757f/app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts#L57):
    ```diff
    -let mockTotalFee = 5;
    -let mockComplianceActionDuringRender: (() => void) | undefined;
    -let mockIsEligible = true;
    -let mockExecutionOptions: {
    -  onSuccess?: (position?: unknown) => void;
    -  onError?: (error: unknown) => void;
    -} = {};
    -// ...
    -let mockChaseOrders: { status: string }[] = [];
    -// ...
    -let mockPositionStreamLoading = false;
    -let mockMarketDataLoading = false;
    -let mockMarketDataError: string | null = null;
    -let mockMarketData: { szDecimals: number; maxLeverage: number } | null = {
    -  szDecimals: 3,
    -  maxLeverage: 40,
    -};
    -let mockIsPlacing = false;
    -let mockExistingPosition: { ... } | null = null;
    -let mockPositionModifyPreview: PositionModifyPreviewResult = { status: 'none' };
    -let mockIsAwaitingPositionModifyPreview = false;
    -let mockIsAtCap = false;
    -let mockEstimatedSlippageBps: number | null = 50;
    -let mockMaxSlippageBps = 100;
    -let mockMaxSlippageSource = 'default';
    -let mockLivePrice = '90000';
    -let mockLiveMarkPrice = '90000';
    -let mockSizeDecimals = 3;
    -let mockSelectedAddress = '0xaccount-a';
    -let mockPerpsNetwork: 'mainnet' | 'testnet' = 'mainnet';
    -let mockIsInitialized = true;
    -let mockOrderValidationParams: ... | undefined;
    -let mockValidateCalculatedMargin = false;
    +beforeEach(() => {
    +  jest.clearAllMocks();
    +  // Reset all module-level let variables to their initial values
    +  mockTotalFee = 5;
    +  mockComplianceActionDuringRender = undefined;
    +  mockIsEligible = true;
    +  mockExecutionOptions = {};
    +  mockChaseOrders = [];
    +  mockPositionStreamLoading = false;
    +  mockMarketDataLoading = false;
    +  mockMarketDataError = null;
    +  mockMarketData = { szDecimals: 3, maxLeverage: 40 };
    +  mockIsPlacing = false;
    +  mockExistingPosition = null;
    +  mockPositionModifyPreview = { status: 'none' };
    +  mockIsAwaitingPositionModifyPreview = false;
    +  mockIsAtCap = false;
    +  mockEstimatedSlippageBps = 50;
    +  mockMaxSlippageBps = 100;
    +  mockMaxSlippageSource = 'default';
    +  mockLivePrice = '90000';
    +  mockLiveMarkPrice = '90000';
    +  mockSizeDecimals = 3;
    +  mockSelectedAddress = '0xaccount-a';
    +  mockPerpsNetwork = 'mainnet';
    +  mockIsInitialized = true;
    +  mockOrderValidationParams = undefined;
    +  mockValidateCalculatedMargin = false;
    +  // Reset mutable mockOrderForm properties
    +  mockOrderForm.type = 'market';
    +  mockOrderForm.direction = 'long';
    +  mockOrderForm.amount = '100';
    +  mockOrderForm.leverage = 5;
    +  mockOrderForm.balancePercent = 10;
    +  mockOrderForm.limitPrice = undefined;
    +  mockOrderForm.takeProfitPrice = undefined;
    +  mockOrderForm.stopLossPrice = undefined;
    +  // Reset mutable mockValidation properties
    +  mockValidation.isValid = true;
    +  mockValidation.errors = [];
    +  mockValidation.fieldIssues = [];
    +  mockValidation.isValidating = false;
    +});
    ```
- **J10 — jest.spyOn without restoreAllMocks() in afterEach** (medium)
  - The test file uses `jest.spyOn(perpsController, 'splitScaleSizes')` in at least two places within the `scale orders` describe block (once for the 'reports unexpected controller ladder failures' test and once for the parameterized error-code tests). There is no `afterEach(() => jest.restoreAllMocks())` in the file. Although `mockImplementationOnce` limits the override to a single call, the spy itself persists on the module export for the lifetime of the test suite. If Jest runs tests in a different order or if the spy is not consumed (e.g. the test throws before the spy is triggered), the spy leaks into subsequent tests that call `splitScaleSizes`, causing them to receive the mocked (throwing) implementation instead of the real one. Adding `afterEach(() => jest.restoreAllMocks())` eliminates this risk entirely.
  - Suggested fix in [`app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts:5800`](https://github.com/MetaMask/metamask-mobile/blob/46bd085def048c3dd067606b83eda95f1d02757f/app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts#L5800):
    ```diff
    -const splitScaleSizesSpy = jest
    -  .spyOn(perpsController, 'splitScaleSizes')
    -  .mockImplementationOnce(() => {
    -    throw error;
    -  });
    +afterEach(() => {
    +  jest.restoreAllMocks();
    +});
    ```

#### `app/components/UI/Perps/utils/limitPriceFarFromMarket.test.ts`

- **J3 — Missing jest.clearAllMocks() between tests** (high)
  - `mockStrings` is a module-level `jest.fn()` whose call history accumulates across all tests in the file. There is no `beforeEach(() => jest.clearAllMocks())` (or equivalent) to reset it between tests. The test `'never renders a percentage at or below the 5% threshold'` asserts `expect(mockStrings).toHaveBeenLastCalledWith(...)`. While `toHaveBeenLastCalledWith` is resilient to accumulated calls (it only checks the final call), the absence of clearing means: (1) if Jest randomizes test order (`--randomize`), a later test that calls `strings()` multiple times could make the 'last call' assertion in this test refer to a call from a different test; (2) any future test added after this one that asserts `toHaveBeenCalledTimes` on `mockStrings` will see an inflated count. Adding a `beforeEach` with `jest.clearAllMocks()` is the standard guard.
  - Suggested fix in [`app/components/UI/Perps/utils/limitPriceFarFromMarket.test.ts:7`](https://github.com/MetaMask/metamask-mobile/blob/46bd085def048c3dd067606b83eda95f1d02757f/app/components/UI/Perps/utils/limitPriceFarFromMarket.test.ts#L7):
    ```diff
    -const mockStrings = jest.fn((key: string) => key);
    -
    -jest.mock('../../../../../locales/i18n', () => ({
    -  strings: (key: string, params?: Record<string, unknown>) =>
    -    mockStrings(key, params),
    -}));
    +const mockStrings = jest.fn((key: string) => key);
    +
    +jest.mock('../../../../../locales/i18n', () => ({
    +  strings: (key: string, params?: Record<string, unknown>) =>
    +    mockStrings(key, params),
    +}));
    +
    +beforeEach(() => {
    +  jest.clearAllMocks();
    +});
    ```


_This check is informational only and does not block merging._
<!-- metamask-flaky-test-detection-metadata=eyJ2ZXJzaW9uIjoxLCJ3aW5kb3dzIjpbNywxNSwzMF0sImZpbGVzIjp7ImFwcC9jb21wb25lbnRzL1VJL1BlcnBzL1ZpZXdzL1BlcnBzUHJvTWFya2V0Vmlldy9jb21wb25lbnRzL1BlcnBzUHJvT3JkZXJGb3JtL3VzZVBlcnBzUHJvT3JkZXJGb3JtLnRlc3QudHMiOnsiYW5hbHl6ZWRTaGEiOiI0NmJkMDg1ZGVmMDQ4YzNkZDA2NzYwNmI4M2VkYTk1ZjFkMDI3NTdmIiwiZmluZGluZ3MiOlt7ImZpbGUiOiJhcHAvY29tcG9uZW50cy9VSS9QZXJwcy9WaWV3cy9QZXJwc1Byb01hcmtldFZpZXcvY29tcG9uZW50cy9QZXJwc1Byb09yZGVyRm9ybS91c2VQZXJwc1Byb09yZGVyRm9ybS50ZXN0LnRzIiwicGF0dGVybklkIjoiSjkiLCJwYXR0ZXJuTmFtZSI6Ik1vZHVsZS1sZXZlbCBtdXRhYmxlIGxldCBiaW5kaW5ncyBub3QgcmVzZXQgaW4gYmVmb3JlRWFjaCIsInNldmVyaXR5IjoiaGlnaCIsImxpbmUiOjU3LCJzbmlwcGV0IjoibGV0IG1vY2tUb3RhbEZlZSA9IDU7XG5sZXQgbW9ja0NvbXBsaWFuY2VBY3Rpb25EdXJpbmdSZW5kZXI6ICgoKSA9PiB2b2lkKSB8IHVuZGVmaW5lZDtcbmxldCBtb2NrSXNFbGlnaWJsZSA9IHRydWU7XG5sZXQgbW9ja0V4ZWN1dGlvbk9wdGlvbnM6IHtcbiAgb25TdWNjZXNzPzogKHBvc2l0aW9uPzogdW5rbm93bikgPT4gdm9pZDtcbiAgb25FcnJvcj86IChlcnJvcjogdW5rbm93bikgPT4gdm9pZDtcbn0gPSB7fTtcbi8vIC4uLlxubGV0IG1vY2tDaGFzZU9yZGVyczogeyBzdGF0dXM6IHN0cmluZyB9W10gPSBbXTtcbi8vIC4uLlxubGV0IG1vY2tQb3NpdGlvblN0cmVhbUxvYWRpbmcgPSBmYWxzZTtcbmxldCBtb2NrTWFya2V0RGF0YUxvYWRpbmcgPSBmYWxzZTtcbmxldCBtb2NrTWFya2V0RGF0YUVycm9yOiBzdHJpbmcgfCBudWxsID0gbnVsbDtcbmxldCBtb2NrTWFya2V0RGF0YTogeyBzekRlY2ltYWxzOiBudW1iZXI7IG1heExldmVyYWdlOiBudW1iZXIgfSB8IG51bGwgPSB7XG4gIHN6RGVjaW1hbHM6IDMsXG4gIG1heExldmVyYWdlOiA0MCxcbn07XG5sZXQgbW9ja0lzUGxhY2luZyA9IGZhbHNlO1xubGV0IG1vY2tFeGlzdGluZ1Bvc2l0aW9uOiB7IC4uLiB9IHwgbnVsbCA9IG51bGw7XG5sZXQgbW9ja1Bvc2l0aW9uTW9kaWZ5UHJldmlldzogUG9zaXRpb25Nb2RpZnlQcmV2aWV3UmVzdWx0ID0geyBzdGF0dXM6ICdub25lJyB9O1xubGV0IG1vY2tJc0F3YWl0aW5nUG9zaXRpb25Nb2RpZnlQcmV2aWV3ID0gZmFsc2U7XG5sZXQgbW9ja0lzQXRDYXAgPSBmYWxzZTtcbmxldCBtb2NrRXN0aW1hdGVkU2xpcHBhZ2VCcHM6IG51bWJlciB8IG51bGwgPSA1MDtcbmxldCBtb2NrTWF4U2xpcHBhZ2VCcHMgPSAxMDA7XG5sZXQgbW9ja01heFNsaXBwYWdlU291cmNlID0gJ2RlZmF1bHQnO1xubGV0IG1vY2tMaXZlUHJpY2UgPSAnOTAwMDAnO1xubGV0IG1vY2tMaXZlTWFya1ByaWNlID0gJzkwMDAwJztcbmxldCBtb2NrU2l6ZURlY2ltYWxzID0gMztcbmxldCBtb2NrU2VsZWN0ZWRBZGRyZXNzID0gJzB4YWNjb3VudC1hJztcbmxldCBtb2NrUGVycHNOZXR3b3JrOiAnbWFpbm5ldCcgfCAndGVzdG5ldCcgPSAnbWFpbm5ldCc7XG5sZXQgbW9ja0lzSW5pdGlhbGl6ZWQgPSB0cnVlO1xubGV0IG1vY2tPcmRlclZhbGlkYXRpb25QYXJhbXM6IC4uLiB8IHVuZGVmaW5lZDtcbmxldCBtb2NrVmFsaWRhdGVDYWxjdWxhdGVkTWFyZ2luID0gZmFsc2U7IiwiZXhwbGFuYXRpb24iOiJUaGVyZSBhcmUgfjI1IG1vZHVsZS1sZXZlbCBgbGV0YCB2YXJpYWJsZXMgdGhhdCBhcmUgbXV0YXRlZCBpbnNpZGUgaW5kaXZpZHVhbCB0ZXN0cyAoZS5nLiBgbW9ja0lzRWxpZ2libGUgPSBmYWxzZWAsIGBtb2NrQ2hhc2VPcmRlcnMgPSBbLi4uXWAsIGBtb2NrRXhpc3RpbmdQb3NpdGlvbiA9IHsuLi59YCwgYG1vY2tJc0F0Q2FwID0gdHJ1ZWAsIGBtb2NrRXN0aW1hdGVkU2xpcHBhZ2VCcHMgPSA1MDBgLCBgbW9ja0xpdmVQcmljZSA9ICcnYCwgYG1vY2tJc0luaXRpYWxpemVkID0gZmFsc2VgLCBgbW9ja01hcmtldERhdGEgPSBudWxsYCwgYG1vY2tQb3NpdGlvblN0cmVhbUxvYWRpbmcgPSB0cnVlYCwgYG1vY2tNYXJrZXREYXRhRXJyb3IgPSAnTWFya2V0IGRhdGEgcmVxdWVzdCBmYWlsZWQnYCwgYG1vY2tTaXplRGVjaW1hbHMgPSAyYCwgYG1vY2tUb3RhbEZlZWAsIGBtb2NrUGVycHNOZXR3b3JrYCwgYG1vY2tTZWxlY3RlZEFkZHJlc3NgLCBgbW9ja1Bvc2l0aW9uTW9kaWZ5UHJldmlld2AsIGBtb2NrVmFsaWRhdGVDYWxjdWxhdGVkTWFyZ2luYCwgZXRjLikuIFRoZSBgYmVmb3JlRWFjaGAgb25seSByZXNldHMgYG1vY2tFeGVjdXRpb25PcHRpb25zYCwgYG1vY2tPcmRlckZvcm0udHlwZWAsIGFuZCBgbW9ja09yZGVyRm9ybS5kaXJlY3Rpb25gIChwbHVzIGNhbGxpbmcgYGplc3QuY2xlYXJBbGxNb2NrcygpYCkuIEFueSB0ZXN0IHRoYXQgbXV0YXRlcyBvbmUgb2YgdGhlIG90aGVyIGBsZXRgIHZhcmlhYmxlcyBsZWF2ZXMgdGhhdCBtdXRhdGlvbiBpbiBwbGFjZSBmb3IgYWxsIHN1YnNlcXVlbnQgdGVzdHMsIGNhdXNpbmcgb3JkZXItZGVwZW5kZW50IGZhaWx1cmVzLiBBZGRpdGlvbmFsbHksIGBtb2NrT3JkZXJGb3JtYCBpcyBhIGBjb25zdGAgb2JqZWN0IHdob3NlIHByb3BlcnRpZXMgKGBhbW91bnRgLCBgbGV2ZXJhZ2VgLCBgYmFsYW5jZVBlcmNlbnRgLCBgbGltaXRQcmljZWAsIGB0YWtlUHJvZml0UHJpY2VgLCBgc3RvcExvc3NQcmljZWApIGFyZSBtdXRhdGVkIGluIHRlc3RzIGJ1dCBub3QgcmVzdG9yZWQgaW4gYGJlZm9yZUVhY2hgLiBUaGUgbmV3IGBmYXItZnJvbS1tYXJrZXRgIGRlc2NyaWJlIGJsb2NrIGFkZGVkIGluIHRoaXMgUFIgYWxzbyByZWxpZXMgb24gdGhlc2Ugc2hhcmVkIG11dGFibGUgdmFyaWFibGVzIChlLmcuIGBtb2NrT3JkZXJGb3JtLnR5cGVgLCBzY2FsZSBvcmRlciBzdGF0ZSksIHNvIGl0IGluaGVyaXRzIHRoZSBzYW1lIHJpc2suIiwic3VnZ2VzdGVkRml4IjoiYmVmb3JlRWFjaCgoKSA9PiB7XG4gIGplc3QuY2xlYXJBbGxNb2NrcygpO1xuICAvLyBSZXNldCBhbGwgbW9kdWxlLWxldmVsIGxldCB2YXJpYWJsZXMgdG8gdGhlaXIgaW5pdGlhbCB2YWx1ZXNcbiAgbW9ja1RvdGFsRmVlID0gNTtcbiAgbW9ja0NvbXBsaWFuY2VBY3Rpb25EdXJpbmdSZW5kZXIgPSB1bmRlZmluZWQ7XG4gIG1vY2tJc0VsaWdpYmxlID0gdHJ1ZTtcbiAgbW9ja0V4ZWN1dGlvbk9wdGlvbnMgPSB7fTtcbiAgbW9ja0NoYXNlT3JkZXJzID0gW107XG4gIG1vY2tQb3NpdGlvblN0cmVhbUxvYWRpbmcgPSBmYWxzZTtcbiAgbW9ja01hcmtldERhdGFMb2FkaW5nID0gZmFsc2U7XG4gIG1vY2tNYXJrZXREYXRhRXJyb3IgPSBudWxsO1xuICBtb2NrTWFya2V0RGF0YSA9IHsgc3pEZWNpbWFsczogMywgbWF4TGV2ZXJhZ2U6IDQwIH07XG4gIG1vY2tJc1BsYWNpbmcgPSBmYWxzZTtcbiAgbW9ja0V4aXN0aW5nUG9zaXRpb24gPSBudWxsO1xuICBtb2NrUG9zaXRpb25Nb2RpZnlQcmV2aWV3ID0geyBzdGF0dXM6ICdub25lJyB9O1xuICBtb2NrSXNBd2FpdGluZ1Bvc2l0aW9uTW9kaWZ5UHJldmlldyA9IGZhbHNlO1xuICBtb2NrSXNBdENhcCA9IGZhbHNlO1xuICBtb2NrRXN0aW1hdGVkU2xpcHBhZ2VCcHMgPSA1MDtcbiAgbW9ja01heFNsaXBwYWdlQnBzID0gMTAwO1xuICBtb2NrTWF4U2xpcHBhZ2VTb3VyY2UgPSAnZGVmYXVsdCc7XG4gIG1vY2tMaXZlUHJpY2UgPSAnOTAwMDAnO1xuICBtb2NrTGl2ZU1hcmtQcmljZSA9ICc5MDAwMCc7XG4gIG1vY2tTaXplRGVjaW1hbHMgPSAzO1xuICBtb2NrU2VsZWN0ZWRBZGRyZXNzID0gJzB4YWNjb3VudC1hJztcbiAgbW9ja1BlcnBzTmV0d29yayA9ICdtYWlubmV0JztcbiAgbW9ja0lzSW5pdGlhbGl6ZWQgPSB0cnVlO1xuICBtb2NrT3JkZXJWYWxpZGF0aW9uUGFyYW1zID0gdW5kZWZpbmVkO1xuICBtb2NrVmFsaWRhdGVDYWxjdWxhdGVkTWFyZ2luID0gZmFsc2U7XG4gIC8vIFJlc2V0IG11dGFibGUgbW9ja09yZGVyRm9ybSBwcm9wZXJ0aWVzXG4gIG1vY2tPcmRlckZvcm0udHlwZSA9ICdtYXJrZXQnO1xuICBtb2NrT3JkZXJGb3JtLmRpcmVjdGlvbiA9ICdsb25nJztcbiAgbW9ja09yZGVyRm9ybS5hbW91bnQgPSAnMTAwJztcbiAgbW9ja09yZGVyRm9ybS5sZXZlcmFnZSA9IDU7XG4gIG1vY2tPcmRlckZvcm0uYmFsYW5jZVBlcmNlbnQgPSAxMDtcbiAgbW9ja09yZGVyRm9ybS5saW1pdFByaWNlID0gdW5kZWZpbmVkO1xuICBtb2NrT3JkZXJGb3JtLnRha2VQcm9maXRQcmljZSA9IHVuZGVmaW5lZDtcbiAgbW9ja09yZGVyRm9ybS5zdG9wTG9zc1ByaWNlID0gdW5kZWZpbmVkO1xuICAvLyBSZXNldCBtdXRhYmxlIG1vY2tWYWxpZGF0aW9uIHByb3BlcnRpZXNcbiAgbW9ja1ZhbGlkYXRpb24uaXNWYWxpZCA9IHRydWU7XG4gIG1vY2tWYWxpZGF0aW9uLmVycm9ycyA9IFtdO1xuICBtb2NrVmFsaWRhdGlvbi5maWVsZElzc3VlcyA9IFtdO1xuICBtb2NrVmFsaWRhdGlvbi5pc1ZhbGlkYXRpbmcgPSBmYWxzZTtcbn0pOyIsImhpc3RvcmljYWxIaW50VXNlZCI6ZmFsc2V9LHsiZmlsZSI6ImFwcC9jb21wb25lbnRzL1VJL1BlcnBzL1ZpZXdzL1BlcnBzUHJvTWFya2V0Vmlldy9jb21wb25lbnRzL1BlcnBzUHJvT3JkZXJGb3JtL3VzZVBlcnBzUHJvT3JkZXJGb3JtLnRlc3QudHMiLCJwYXR0ZXJuSWQiOiJKMTAiLCJwYXR0ZXJuTmFtZSI6Implc3Quc3B5T24gd2l0aG91dCByZXN0b3JlQWxsTW9ja3MoKSBpbiBhZnRlckVhY2giLCJzZXZlcml0eSI6Im1lZGl1bSIsImxpbmUiOjU4MDAsInNuaXBwZXQiOiJjb25zdCBzcGxpdFNjYWxlU2l6ZXNTcHkgPSBqZXN0XG4gIC5zcHlPbihwZXJwc0NvbnRyb2xsZXIsICdzcGxpdFNjYWxlU2l6ZXMnKVxuICAubW9ja0ltcGxlbWVudGF0aW9uT25jZSgoKSA9PiB7XG4gICAgdGhyb3cgZXJyb3I7XG4gIH0pOyIsImV4cGxhbmF0aW9uIjoiVGhlIHRlc3QgZmlsZSB1c2VzIGBqZXN0LnNweU9uKHBlcnBzQ29udHJvbGxlciwgJ3NwbGl0U2NhbGVTaXplcycpYCBpbiBhdCBsZWFzdCB0d28gcGxhY2VzIHdpdGhpbiB0aGUgYHNjYWxlIG9yZGVyc2AgZGVzY3JpYmUgYmxvY2sgKG9uY2UgZm9yIHRoZSAncmVwb3J0cyB1bmV4cGVjdGVkIGNvbnRyb2xsZXIgbGFkZGVyIGZhaWx1cmVzJyB0ZXN0IGFuZCBvbmNlIGZvciB0aGUgcGFyYW1ldGVyaXplZCBlcnJvci1jb2RlIHRlc3RzKS4gVGhlcmUgaXMgbm8gYGFmdGVyRWFjaCgoKSA9PiBqZXN0LnJlc3RvcmVBbGxNb2NrcygpKWAgaW4gdGhlIGZpbGUuIEFsdGhvdWdoIGBtb2NrSW1wbGVtZW50YXRpb25PbmNlYCBsaW1pdHMgdGhlIG92ZXJyaWRlIHRvIGEgc2luZ2xlIGNhbGwsIHRoZSBzcHkgaXRzZWxmIHBlcnNpc3RzIG9uIHRoZSBtb2R1bGUgZXhwb3J0IGZvciB0aGUgbGlmZXRpbWUgb2YgdGhlIHRlc3Qgc3VpdGUuIElmIEplc3QgcnVucyB0ZXN0cyBpbiBhIGRpZmZlcmVudCBvcmRlciBvciBpZiB0aGUgc3B5IGlzIG5vdCBjb25zdW1lZCAoZS5nLiB0aGUgdGVzdCB0aHJvd3MgYmVmb3JlIHRoZSBzcHkgaXMgdHJpZ2dlcmVkKSwgdGhlIHNweSBsZWFrcyBpbnRvIHN1YnNlcXVlbnQgdGVzdHMgdGhhdCBjYWxsIGBzcGxpdFNjYWxlU2l6ZXNgLCBjYXVzaW5nIHRoZW0gdG8gcmVjZWl2ZSB0aGUgbW9ja2VkICh0aHJvd2luZykgaW1wbGVtZW50YXRpb24gaW5zdGVhZCBvZiB0aGUgcmVhbCBvbmUuIEFkZGluZyBgYWZ0ZXJFYWNoKCgpID0+IGplc3QucmVzdG9yZUFsbE1vY2tzKCkpYCBlbGltaW5hdGVzIHRoaXMgcmlzayBlbnRpcmVseS4iLCJzdWdnZXN0ZWRGaXgiOiJhZnRlckVhY2goKCkgPT4ge1xuICBqZXN0LnJlc3RvcmVBbGxNb2NrcygpO1xufSk7IiwiaGlzdG9yaWNhbEhpbnRVc2VkIjpmYWxzZX1dfSwiYXBwL2NvbXBvbmVudHMvVUkvUGVycHMvdXRpbHMvbGltaXRQcmljZUZhckZyb21NYXJrZXQudGVzdC50cyI6eyJhbmFseXplZFNoYSI6IjQ2YmQwODVkZWYwNDhjM2RkMDY3NjA2YjgzZWRhOTVmMWQwMjc1N2YiLCJmaW5kaW5ncyI6W3siZmlsZSI6ImFwcC9jb21wb25lbnRzL1VJL1BlcnBzL3V0aWxzL2xpbWl0UHJpY2VGYXJGcm9tTWFya2V0LnRlc3QudHMiLCJwYXR0ZXJuSWQiOiJKMyIsInBhdHRlcm5OYW1lIjoiTWlzc2luZyBqZXN0LmNsZWFyQWxsTW9ja3MoKSBiZXR3ZWVuIHRlc3RzIiwic2V2ZXJpdHkiOiJoaWdoIiwibGluZSI6Nywic25pcHBldCI6ImNvbnN0IG1vY2tTdHJpbmdzID0gamVzdC5mbigoa2V5OiBzdHJpbmcpID0+IGtleSk7XG5cbmplc3QubW9jaygnLi4vLi4vLi4vLi4vLi4vbG9jYWxlcy9pMThuJywgKCkgPT4gKHtcbiAgc3RyaW5nczogKGtleTogc3RyaW5nLCBwYXJhbXM/OiBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPikgPT5cbiAgICBtb2NrU3RyaW5ncyhrZXksIHBhcmFtcyksXG59KSk7IiwiZXhwbGFuYXRpb24iOiJgbW9ja1N0cmluZ3NgIGlzIGEgbW9kdWxlLWxldmVsIGBqZXN0LmZuKClgIHdob3NlIGNhbGwgaGlzdG9yeSBhY2N1bXVsYXRlcyBhY3Jvc3MgYWxsIHRlc3RzIGluIHRoZSBmaWxlLiBUaGVyZSBpcyBubyBgYmVmb3JlRWFjaCgoKSA9PiBqZXN0LmNsZWFyQWxsTW9ja3MoKSlgIChvciBlcXVpdmFsZW50KSB0byByZXNldCBpdCBiZXR3ZWVuIHRlc3RzLiBUaGUgdGVzdCBgJ25ldmVyIHJlbmRlcnMgYSBwZXJjZW50YWdlIGF0IG9yIGJlbG93IHRoZSA1JSB0aHJlc2hvbGQnYCBhc3NlcnRzIGBleHBlY3QobW9ja1N0cmluZ3MpLnRvSGF2ZUJlZW5MYXN0Q2FsbGVkV2l0aCguLi4pYC4gV2hpbGUgYHRvSGF2ZUJlZW5MYXN0Q2FsbGVkV2l0aGAgaXMgcmVzaWxpZW50IHRvIGFjY3VtdWxhdGVkIGNhbGxzIChpdCBvbmx5IGNoZWNrcyB0aGUgZmluYWwgY2FsbCksIHRoZSBhYnNlbmNlIG9mIGNsZWFyaW5nIG1lYW5zOiAoMSkgaWYgSmVzdCByYW5kb21pemVzIHRlc3Qgb3JkZXIgKGAtLXJhbmRvbWl6ZWApLCBhIGxhdGVyIHRlc3QgdGhhdCBjYWxscyBgc3RyaW5ncygpYCBtdWx0aXBsZSB0aW1lcyBjb3VsZCBtYWtlIHRoZSAnbGFzdCBjYWxsJyBhc3NlcnRpb24gaW4gdGhpcyB0ZXN0IHJlZmVyIHRvIGEgY2FsbCBmcm9tIGEgZGlmZmVyZW50IHRlc3Q7ICgyKSBhbnkgZnV0dXJlIHRlc3QgYWRkZWQgYWZ0ZXIgdGhpcyBvbmUgdGhhdCBhc3NlcnRzIGB0b0hhdmVCZWVuQ2FsbGVkVGltZXNgIG9uIGBtb2NrU3RyaW5nc2Agd2lsbCBzZWUgYW4gaW5mbGF0ZWQgY291bnQuIEFkZGluZyBhIGBiZWZvcmVFYWNoYCB3aXRoIGBqZXN0LmNsZWFyQWxsTW9ja3MoKWAgaXMgdGhlIHN0YW5kYXJkIGd1YXJkLiIsInN1Z2dlc3RlZEZpeCI6ImNvbnN0IG1vY2tTdHJpbmdzID0gamVzdC5mbigoa2V5OiBzdHJpbmcpID0+IGtleSk7XG5cbmplc3QubW9jaygnLi4vLi4vLi4vLi4vLi4vbG9jYWxlcy9pMThuJywgKCkgPT4gKHtcbiAgc3RyaW5nczogKGtleTogc3RyaW5nLCBwYXJhbXM/OiBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPikgPT5cbiAgICBtb2NrU3RyaW5ncyhrZXksIHBhcmFtcyksXG59KSk7XG5cbmJlZm9yZUVhY2goKCkgPT4ge1xuICBqZXN0LmNsZWFyQWxsTW9ja3MoKTtcbn0pOyIsImhpc3RvcmljYWxIaW50VXNlZCI6ZmFsc2V9XX19fQ== -->
