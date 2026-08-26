# MetaMask Recipe Run

Status: pass
Duration: 52s
Nodes: 21/21 passed

## Side findings
- REVIEW 13 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-status (app.status, 36ms): platform=mobile
- PASS setup-unlock (metamask.wallet.ensure_unlocked, 5.7s): platform=ios, proof=agentic-wallet-unlock
- PASS setup-open-market (ui.navigate, 7.0s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-wait-long (ui.wait_for, 2.7s): matched=true, testId=perps-market-details-long-button, expected=present, present=true, visible=true
- PASS setup-press-long (ui.press, 2.1s): ok=true, testId=perps-market-details-long-button, deviceName=mm-2
- PASS setup-wait-order-screen (ui.wait_for, 1.3s): matched=true, testId=perps-order-view-place-order-button, expected=present, present=true, visible=true
- PASS setup-open-pay-sheet (ui.press, 1.5s): ok=true, testId=pay-with, deviceName=mm-2
- PASS setup-wait-pay-sheet (ui.wait_for, 700ms): matched=true, testId=pay-with-crypto-section-preferred-token-row, expected=present, present=true, visible=true
- PASS setup-reset-to-perps-balance (ui.press, 710ms): ok=true, testId=pay-with-perps-section-balance-row, deviceName=mm-2
- PASS setup-reopen-pay-sheet (ui.press, 524ms): ok=true, testId=pay-with, deviceName=mm-2
- PASS setup-wait-pay-sheet-again (ui.wait_for, 567ms): matched=true, testId=pay-with-crypto-section-preferred-token-row, expected=present, present=true, visible=true
- PASS setup-select-token (ui.press, 1.3s): ok=true, testId=pay-with-crypto-section-preferred-token-row, deviceName=mm-2
- PASS ac1-assert-no-perps-balance-warning (ui.wait_for, 789ms): matched=true, text=Not enough funds available. Deposit funds or select a different payment method, textMatch=contains, expected=absent, present=false
- PASS ac1-assert-no-zero-available-row (ui.wait_for, 576ms): matched=true, text=Available: $0, textMatch=contains, expected=absent, present=false
- PASS ac2-assert-action-button-visible (ui.wait_for, 782ms): matched=true, testId=perps-order-view-place-order-button, expected=present, present=true, visible=true
- PASS ac1-screenshot-single-message (ui.screenshot, 527ms): path=screenshots/evidence-ac1-after-payment-switch.png
- PASS ac2-assert-button-still-visible (ui.wait_for, 573ms): matched=true, testId=perps-order-view-place-order-button, expected=present, present=true, visible=true
- PASS ac3-ac4-run-funding-state-tests (command, 21s): exitCode=0, stdout=  console.error
    An update to PerpsOrderViewContentBase inside a test was not wrapped in act(...).
    
    When testing, code that causes React state updates should be wrapped into act(...):
    
    act(() => {
      /* fire events that update state */
    });
    /* assert on the output */
    
    This ensures that you're testing the behavior the user would see in the browser. Learn more at https://react.dev/link/wrap-tests-with-act

      291 |     // Defer data loading to next frame for faster initial render
      292 |     requestAnimationFrame(() => {
    > 293 |       setIsDataReady(true);
          |       ^
      294 |     });
      295 |   }, []);
      296 |

      at node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14402:19
      at runWithFiberInDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:2315:13)
      at warnIfUpdatesNotWrappedWithActDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14401:9)
      at scheduleUpdateOnFiber (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:12086:9)
      at dispatchSetStateInternal (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6208:13)
      at dispatchSetState (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6165:7)
      at Timeout.setIsDataReady [as _onTimeout] (app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:293:7)

  console.error
    An update to PerpsOrderViewContentBase inside a test was not wrapped in act(...).
    
    When testing, code that causes React state updates should be wrapped into act(...):
    
    act(() => {
      /* fire events that update state */
    });
    /* assert on the output */
    
    This ensures that you're testing the behavior the user would see in the browser. Learn more at https://react.dev/link/wrap-tests-with-act

      291 |     // Defer data loading to next frame for faster initial render
      292 |     requestAnimationFrame(() => {
    > 293 |       setIsDataReady(true);
          |       ^
      294 |     });
      295 |   }, []);
      296 |

      at node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14402:19
      at runWithFiberInDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:2315:13)
      at warnIfUpdatesNotWrappedWithActDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14401:9)
      at scheduleUpdateOnFiber (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:12086:9)
      at dispatchSetStateInternal (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6208:13)
      at dispatchSetState (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6165:7)
      at Timeout.setIsDataReady [as _onTimeout] (app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:293:7)

  console.error
    An update to PerpsOrderViewContentBase inside a test was not wrapped in act(...).
    
    When testing, code that causes React state updates should be wrapped into act(...):
    
    act(() => {
      /* fire events that update state */
    });
    /* assert on the output */
    
    This ensures that you're testing the behavior the user would see in the browser. Learn more at https://react.dev/link/wrap-tests-with-act

      291 |     // Defer data loading to next frame for faster initial render
      292 |     requestAnimationFrame(() => {
    > 293 |       setIsDataReady(true);
          |       ^
      294 |     });
      295 |   }, []);
      296 |

      at node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14402:19
      at runWithFiberInDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:2315:13)
      at warnIfUpdatesNotWrappedWithActDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14401:9)
      at scheduleUpdateOnFiber (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:12086:9)
      at dispatchSetStateInternal (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6208:13)
      at dispatchSetState (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6165:7)
      at Timeout.setIsDataReady [as _onTimeout] (app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:293:7)

  console.error
    An update to PerpsOrderViewContentBase inside a test was not wrapped in act(...).
    
    When testing, code that causes React state updates should be wrapped into act(...):
    
    act(() => {
      /* fire events that update state */
    });
    /* assert on the output */
    
    This ensures that you're testing the behavior the user would see in the browser. Learn more at https://react.dev/link/wrap-tests-with-act

      291 |     // Defer data loading to next frame for faster initial render
      292 |     requestAnimationFrame(() => {
    > 293 |       setIsDataReady(true);
          |       ^
      294 |     });
      295 |   }, []);
      296 |

      at node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14402:19
      at runWithFiberInDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:2315:13)
      at warnIfUpdatesNotWrappedWithActDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14401:9)
      at scheduleUpdateOnFiber (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:12086:9)
      at dispatchSetStateInternal (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6208:13)
      at dispatchSetState (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6165:7)
      at Timeout.setIsDataReady [as _onTimeout] (app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:293:7)

PASS app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.test.tsx
  PerpsOrderView
    ○ skipped renders the order view
    ○ skipped displays the correct asset from route params
    ○ skipped navigates back when header is present
    ○ skipped handles order submission
    ○ skipped displays components when connected
    ○ skipped handles leverage display
    ○ skipped handles amount display
    ○ skipped handles successful order placement
    ○ skipped shows standard submitted toast when custom token is selected (deposit flow)
    ○ skipped includes discovery attribution from route source_section in order trackingData
    ○ skipped shows standard submitted toast when using perps balance
    ○ skipped handles failed order placement
    ○ skipped shows leverage bottom sheet when leverage pressed
    ○ skipped shows order type bottom sheet when order type pressed
    ○ skipped handles keypad input
    ○ skipped handles percentage buttons when balance available
    ○ skipped handles MAX button press
    ○ skipped handles MIN button press
    ○ skipped should track performance metrics on mount
    ○ skipped shows slider when not focused on input
    ○ skipped hides slider when focused on input
    ○ skipped handles testnet defaults
    ○ skipped opens limit price bottom sheet from limit price row
    ○ skipped handles short direction from route params
    ○ skipped handles custom leverage from route params
    ○ skipped calculates liquidation price
    ○ skipped calculates liquidation price using market price for market orders
    ○ skipped calculates liquidation price using limit price for limit orders
    ○ skipped shows margin required
    ○ skipped shows position size
    ○ skipped should show estimated fees
    ○ skipped handles zero balance warning
    ○ skipped validates order before placement
    ○ skipped handles network error during order placement
    ○ skipped shows PerpsBottomSheetTooltip when info icon is clicked
    unresolved pay-token balance
      ✓ fails closed without a spinner or Perps-balance slider capacity (52 ms)
      ✓ caps slider capacity at zero when the custom pay token is missing (13 ms)
      ✓ keeps unrelated validation errors visible (22 ms)
      ✓ retains capacity only for the same account, chain, and token (54 ms)
    Slider drag commit funnel
      ○ skipped shows the live drag value instead of the stale committed amount while dragging
      ○ skipped commits the live value on drag end
      ○ skipped flushes the live drag value forward on cancel instead of discarding it
      ○ skipped does not commit anything on cancel when the slider was never dragged
      ○ skipped flushes a stuck live drag value instead of submitting a stale order
    Leverage confirm resolves against the live drag amount
      ○ skipped flushes the live drag amount forward when no clamping is required
      ○ skipped clamps against the live drag amount, not the stale committed amount
      ○ skipped tracks leverage change with previous_leverage and not previousLeverage
    Place order button disabled state
      ○ skipped disables button when order validation is invalid
      ○ skipped disables button when order is placing
      ○ skipped shows loading state while order validation is pending
      ○ skipped enables button when validation passes and not placing order
    pay amount readiness
      ○ skipped disables place order while the required token amount is still zero
      ○ skipped enables place order once the required token amount arrives
      ○ skipped ignores a zero amount on a token that is skipped when the balance covers it
      ○ skipped leaves place order enabled when paying from the Perps balance
      ○ skipped disables place order while the pay state would fail the publish guard
      ○ skipped leaves place order enabled when paying from the Perps balance while pay state is not submit ready
    Stop loss liquidation warning
      ○ skipped shows liquidation warning for long position with stop loss below liquidation price
      ○ skipped shows liquidation warning for short position with stop loss above liquidation price
      ○ skipped does not show liquidation warning when stop loss is safe for long position
      ○ skipped does not show liquidation warning when stop loss is safe for short position
      ○ skipped does not show liquidation warning when no stop loss is set
      ○ skipped disables place order button when stop loss risks liquidation
    TP/SL wrong-side price validation
      ○ skipped shows warning and disables button for long position with TP below current price
      ○ skipped shows warning and disables button for long position with SL above current price
      ○ skipped shows warning for short position with TP above current price
      ○ skipped shows warning for short position with SL below current price
      ○ skipped does not show wrong-side warnings when TP/SL prices are valid
      ○ skipped disables button when both TP and SL are on wrong side
      ○ skipped disables control (white) button variant when TP/SL is invalid
      limit order TP/SL validates against entry price, not market price
        ○ skipped accepts TP above limit price for long limit order even when TP is below market price
        ○ skipped accepts SL below limit price for long limit order even when SL is below market price
        ○ skipped rejects TP below limit price for long limit order
        ○ skipped accepts TP below limit price for short limit order even when TP is above market price
        ○ skipped accepts SL above limit price for short limit order
    TP/SL limit price validation
      ○ skipped shows toast and prevents TP/SL bottom sheet from opening on limit order without limit price
      ○ skipped navigates to TP/SL screen on limit order with limit price
    Rewards Points Row
      ○ skipped displays points row when rewards should show
      ○ skipped handles points tooltip interaction
      ○ skipped renders RewardsAnimations component with correct props when rewards shown
      ○ skipped renders RewardsAnimations in loading state
      ○ skipped renders RewardsAnimations in error state
      ○ skipped renders RewardsAnimations with bonus bips when provided
      ○ skipped renders AddRewardsAccount when accountOptedIn is false and account is defined
      ○ skipped renders RewardsAnimations when accountOptedIn is true
      ○ skipped does not render rewards row when accountOptedIn is null
    Info icon tooltip interactions
      ○ skipped should show tooltip when margin info icon is pressed
      ○ skipped should show tooltip when liquidation price info icon is pressed
      ○ skipped should show tooltip when fees info icon is pressed
    Amount validation and display
      ○ skipped should display fallback data when amount is invalid
      ○ skipped should format margin and liquidation price correctly for valid amounts
    Fees display with discount
      ○ skipped should display fees with discount percentage when available
      ○ skipped should display fees without discount when not available
    Points section with rewards
      ○ skipped displays points row and handles tooltip when rewards should show
    Conditional Rendering Coverage - Target Lines
      ○ skipped should render margin with formatPrice when marginRequired is truthy
      ○ skipped should render margin fallback when marginRequired is falsy
      ○ skipped should render fees with formatPerpsFiat when hasValidAmount is true
      ○ skipped should render fees fallback when hasValidAmount is false
      ○ skipped shows rewards state integration with fee discount
    Leverage from existing position
      ○ skipped should not sync leverage from position when route param leverage is provided
      ○ skipped should prioritize existing position leverage over saved config (bug fix)
    Tooltip interactions
      ○ skipped should close tooltip when handleTooltipClose is called
      ○ skipped should show points tooltip when points info icon is pressed
    Insufficient funds handling
      ○ skipped should not show balance warning when account is still loading
      ○ skipped should show normal place order button when amount is sufficient
    Order header interactions
      ○ skipped should open order type bottom sheet when order type is pressed in header
      ○ skipped should display correct asset and price in header
    Market data fallback to route defaults
      ○ skipped uses defaultSzDecimals and defaultMaxLeverage when marketData is loading
      ○ skipped treats market data as loading when no fallback defaults and data is unavailable
    Pay-token validation error analytics tracking
      ○ skipped fires validation error event when a blocking insufficient-balance pay-token alert appears
      ○ skipped fires validation error event when a blocking no-quotes pay-token alert appears
      ○ skipped suppresses a blocking insufficient-balance alert while the live balance is unresolved
      ○ skipped does not fire validation error event when no blocking pay-token alerts exist
      ○ skipped does not fire validation error event when Perps balance is selected instead of custom token
      ○ skipped fires warning event when hasInsufficientPayTokenBalance is true
      ○ skipped does not fire warning event when pay-token balance is sufficient
      ○ skipped uses title as alertMessage fallback when message is not a string
      ○ skipped uses key as alertMessage fallback when neither message nor title exist
      ○ skipped uses unknown_blocking_alert as alertMessage fallback when no message, title, or key
    slippage block on submit
      ○ skipped blocks placeOrder when estimated slippage exceeds the configured cap
      ○ skipped submits with the refreshed Lite slippage cap
    transaction considered + trade quote received
      ○ skipped emits PERPS_TRANSACTION_CONSIDERED once the filled order form settles (1s debounce)
      ○ skipped emits PERPS_TRADE_QUOTE_RECEIVED with quote_latency_ms when a pay-token quote completes
      ○ skipped emits a distinct PERPS_TRADE_QUOTE_RECEIVED per failed attempt when the amount changes (same blocking alert)
    abandon order tracking
      ○ skipped emits abandon_order on beforeRemove (back / hardware back)
      ○ skipped emits abandon_order on tab-away (blur with unchanged depth)
      ○ skipped does NOT emit on blur when a child route was pushed (depth increased)

Test Suites: 1 passed, 1 total
Tests:       123 skipped, 4 passed, 127 total
Snapshots:   0 total
Time:        4.635 s, estimated 6 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsOrderView\/PerpsOrderView.test.tsx/i with tests matching "unresolved pay-token balance".
Force exiting Jest: Have you considered using `--detectOpenHandles` to detect async operations that kept running after all tests finished?

- PASS ac3-ac4-assert-funding-state-tests (assert_exit_code, 44ms): source=ac3-ac4-run-funding-state-tests, expected=0, actual=0
- PASS teardown-index-test-log (index_artifacts, 50ms)
- PASS teardown-done (end, 0ms)
