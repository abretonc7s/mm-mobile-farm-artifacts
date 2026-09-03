# MetaMask Recipe Run

Status: pass
Duration: 34s
Nodes: 17/17 passed

## Side findings
- REVIEW 10 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS unlock (metamask.wallet.ensure_unlocked, 9.4s): platform=ios, proof=agentic-wallet-unlock
- PASS run-helper-tests (command, 4.9s): exitCode=0, stderr=PASS app/components/UI/Perps/utils/limitPriceFarFromMarket.test.ts
  getFarthestRestingLimitPrice
    ✓ returns the limit price for a limit order (2 ms)
    ✓ returns the lower endpoint for a long scale (1 ms)
    ✓ returns the higher endpoint for a short scale
    ✓ returns undefined when a scale endpoint is missing (1 ms)
  getLimitPriceFarFromMarketWarning
    ✓ warns when a long limit is more than 5% below the best bid
    ✓ stays quiet at exactly the 5% long threshold (1 ms)
    ✓ warns when a short scale high endpoint is more than 5% above the ask
    ✓ never renders a percentage at or below the 5% threshold
    ✓ skips reduce-only orders
    ✓ skips market orders

Test Suites: 1 passed, 1 total
Tests:       10 passed, 10 total
Snapshots:   0 total
Time:        1.626 s, estimated 2 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/limitPriceFarFromMarket.test.ts/i.

- PASS assert-helper-tests (assert_exit_code, 71ms): source=run-helper-tests, expected=0, actual=0
- PASS run-hook-tests (command, 5.0s): exitCode=0, stderr=PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts
  usePerpsProOrderForm
    availableBalance
      ○ skipped formats spendable balance as "$amount available" when connected
      ○ skipped shows the unavailable placeholder before Perps is initialized
    summary
      ○ skipped builds display-ready margin, liquidation, slippage and numeric fees
      ○ skipped shows the fallback liquidation display when amount is empty
      ○ skipped shows margin and liquidation before-and-after values from the controller preview
      ○ skipped keeps single-value summary when the controller returns no preview
      ○ skipped keeps single-value summary for unsupported cross-margin previews
      ○ skipped uses the controller fee result unchanged for a TWAP order
      ○ skipped routes Scale fees and validation through the concrete provider
      ○ skipped routes Chase fees through its placement provider
    notices
      ○ skipped blocks a 0-minute TWAP duration below the controller minimum
      ○ skipped blocks a 1-minute TWAP duration below the controller minimum
      ○ skipped blocks TWAP totals below the controller-supported minimum
      ○ skipped shows a required notice when the TWAP duration is empty
      ○ skipped keeps an empty TWAP size silent while disabling placement
      ○ skipped maps a margin validation error to a priority banner
      ○ skipped keeps an empty amount blocked without an inline message
      ○ skipped blocks after submit without an inline amount message
      ○ skipped blocks silently while market data is loading
      ○ skipped explains why the order is blocked when the live price is unavailable
      ○ skipped shows a failure message when market data loading fails
      ○ skipped maps an OI cap to a banner notice
      ○ skipped shows the sl-liq-risk notice when the stop loss risks liquidation
      ○ skipped shows the tp-invalid notice when the take profit is on the wrong side
      ○ skipped shows the sl-invalid notice when the stop loss is on the wrong side
      ○ skipped shows the reduce-only no-position banner and suppresses TP/SL notices
      ○ skipped shows the reduce-only wrong-side banner for same-direction orders
      ○ skipped shows the reduce-only too-large banner and disables submit when size exceeds position
      ○ skipped shows a position-loading notice while suppressing stale validation errors
      ○ skipped validates the stop loss side against the remaining position direction on a partial decrease
      ○ skipped phrases the stop loss wrong-side warning for the remaining position, not the order
      ○ skipped warns when the stop loss sits past the projected liquidation price
    handlePlaceOrder
      ○ skipped starts a new TWAP draft at the Figma default of 30 minutes
      ○ skipped submits valid TWAP params with live mid price and Randomize
      ○ skipped resets the TWAP draft after accepted placement
      ○ skipped shows TWAP-specific confirmation for accepted placement
      ○ skipped shows TWAP-specific failure copy for rejected placement
      ○ skipped blocks TWAP placement after the feature gate is disabled
      ○ skipped re-checks selected-route TWAP support immediately before placement
      ○ skipped re-checks TWAP rollout after an asynchronous compliance gate
      ○ skipped blocks TWAP placement when its resolved route changes during validation
      ○ skipped resets a selected TWAP after rollout availability disappears
      ○ skipped clears the TWAP draft after rollout availability disappears
      ○ skipped preserves a selected TWAP draft through capability reinitialization
      ○ skipped keeps ordinary placement on controller default routing
      ○ skipped keeps a non-Chase fingerprint out of Chase analytics
      ○ skipped does not show Chase feedback for a stale non-Chase fingerprint
      ○ skipped executes order for an eligible compliant user
      ○ skipped keeps a pending termination in the visible Chase placement limit
      ○ skipped tracks each Chase limit banner episode once
      ○ skipped blocks a Chase submit when refreshed active and pending sessions reach the venue limit
      ○ skipped tracks a controller Chase limit rejection during execution
      ○ skipped blocks Chase placement until session context reconnects
      ○ skipped abandons Chase when compliance resolves after fallback
      ○ skipped locks Chase preflight against repeated taps and draft edits
      ○ skipped releases Chase preflight lock after compliance failure
      ○ skipped abandons deferred Chase compliance after the symbol-keyed form unmounts
      ○ skipped keeps the Chase form active while disabling its blurred polling consumer
      ○ skipped aborts Chase when the provider changes during compliance
      ○ skipped aborts Chase when the Perps network changes during compliance
      ○ skipped aborts Chase when a price tick changes reviewed exposure during compliance
      ○ skipped aborts Chase when effective token precision changes during compliance
      ○ skipped accepts formatting-equivalent prices during compliance
      ○ skipped uses committed Chase refs during a render-phase compliance callback
      ○ skipped places Chase without an optional max distance
      ○ skipped refreshes Chase history after a successful terminal placement
      ○ skipped fails closed before controller placement when Chase is disabled
      ○ skipped re-checks capability and fails closed before controller placement
      ○ skipped fails closed with feedback when the Chase session refresh fails
      ○ skipped asks for route review when the Chase session refresh becomes stale
      ○ skipped blocks a Chase distance-unit edit during capability refresh
      ○ skipped abandons Chase submit when the capability route disappears
      ○ skipped abandons Chase submit when the visible draft changes during validation
      ○ skipped abandons Chase submit when the selected account changes
      ○ skipped revalidates Chase when spendable balance drops during validation
      ○ skipped revalidates Chase when an existing position becomes cross margin
      ○ skipped revalidates Chase when reduce-only position loading starts
      ○ skipped aborts when validation changes the reviewed Chase size
      ○ skipped aborts when MAX-derived size changes during session refresh
      ○ skipped blocks an explicit Chase size edit during session refresh
      ○ skipped blocks a Chase leverage edit during session refresh
      ○ skipped aborts when effective price changes during session refresh
      ○ skipped clears the Chase draft after capability resolves unsupported
      ○ skipped keeps a selected Chase draft while capability discovery is pending
      ○ skipped keeps haptics silent for a duplicate submit
      ○ skipped opens geo-block modal and skips execution for an ineligible user
      ○ skipped skips geo handling and execution when compliance gate blocks
      ○ skipped commits pending slider preview without invoking compliance or submitting
      ○ skipped builds OrderParams including reduceOnly and calls executeOrder
      ○ skipped submits the exact live size and omits USD for a max-slider full close
      ○ skipped keeps a focused max preview from becoming a full close
      ○ skipped submits a smaller interrupted reduce-only preview instead of a full close
      ○ skipped clears the size max override after a successful Reduce Only order
      ○ skipped flushes a pending slider preview before allowing submission
      ○ skipped submits on the first tap when a pending slider preview is unchanged
      ○ skipped blocks reduce-only submit when there is no open position
      ○ skipped blocks reduce-only submit when size exceeds the open position
      ○ skipped blocks submit and shows a toast when validation is invalid
      ○ skipped shows a final trigger-limit field error without executing the order
      ○ skipped keeps the CTA enabled without loading while validation is pending
      ○ skipped runs current validation before executing a pending order
      ○ skipped blocks a pending trigger order when the live mid crosses the trigger
      ○ skipped navigates to the cross-margin warning and aborts
      ○ skipped aborts and tracks when the estimated slippage exceeds the max
      ○ skipped aborts submit when the stop loss risks liquidation (doesStopLossRiskLiquidation guard)
      ○ skipped skips updatePositionTPSL and clearPendingConfig when the order fails (shouldHandleTPSLSeparately path)
      ○ skipped skips clearPendingConfig when the order fails (plain else path)
    execution toasts
      ○ skipped shows the confirmed toast on success
      ○ skipped shows Chase confirmation when Chase starts
      ○ skipped shows the creation-failed toast on error
    TP/SL handling
      ○ skipped places the order without TP/SL then updates position TP/SL when flagged
      ○ skipped shows an error toast when the separate TP/SL update fails
    limit orders
      ○ skipped sets the limit price and the fixed limit slippage on OrderParams
      ○ skipped finalizes a trailing decimal separator from the limit price before submit
    scale orders
      ○ skipped normalizes Scale rungs through the controller precision contract
      ○ skipped applies HyperLiquid precision for each asset size grid
      ○ skipped keeps Scale placement disabled for a MYX route
      ○ skipped starts with a blank Order count to match the default Scale form
      ○ skipped keeps the blank Scale default free of validation banners
      ○ skipped restores Scale validation after switching order types
      ○ skipped bounds ladder sizing work for an extreme accepted skew
      ○ skipped reports unexpected controller ladder failures
      ○ skipped normalizes controller ladder failure ORDER_SCALE_RANGE_INVALID into Scale validation
      ○ skipped normalizes controller ladder failure ORDER_SCALE_COUNT_INVALID into Scale validation
      ○ skipped uses controller-owned price formatting for Scale preview
      ○ skipped clears limit and trigger drafts when Scale is selected
      ○ skipped clears hidden price and TP/SL drafts when Chase is selected
      ○ skipped submits one controller Scale request with canonical strategy parameters
      ○ skipped rejects an unsupported Scale provider before placement
      ○ skipped keeps Scale USD sizing consistent when market and ladder prices differ
      ○ skipped resets Scale configuration after controller placement succeeds
      ○ skipped clears limit and trigger drafts after full Scale placement
      ○ skipped clears limit and trigger drafts after partial Scale placement
      ○ skipped shows localized Scale-specific copy while the ladder is submitted
      ○ skipped shows localized Scale-specific copy when the full ladder is placed
      ○ skipped shows localized Scale-specific copy for a partial controller result
      ○ skipped uses requested ladder for empty child arrays in the confirmation copy
      ○ skipped uses legacy submitted size when accepted size is absent in the confirmation copy
      ○ skipped uses resting-order failure copy when Scale placement fails
      ○ skipped uses Scale failure copy after a Chase placement
      ○ skipped does not submit a duplicate Scale request while placement is pending
      ○ skipped resets Scale configuration after a partial controller result
      ○ skipped does not retry placed children after a partial Scale success
      ○ skipped retains Scale configuration when the controller rejects the placement
      ○ skipped keeps the previous Scale order count when a fractional edit arrives
      ○ skipped blocks and tracks an out-of-range Scale order count
      ○ skipped rejects a ladder when a rung is below the controller minimum
      ○ skipped asks for a Scale size before applying minimum-lot validation
      ○ skipped validates margin from the whole rounded Scale ladder notional
      ○ skipped blocks a Reduce Only Scale order when no position can be reduced
      ○ skipped renders the controller-formatted Scale price ladder
      ○ skipped weights an above-one Scale skew toward the end of the range
      ○ skipped builds the per-rung Scale margin range
      ○ skipped weights a below-one Scale skew toward the start of the range
      ○ skipped keeps an exactly-one Scale skew evenly sized
      ○ skipped rejects a third Scale skew decimal while typing
      ○ skipped restores the default Scale skew when an empty draft blurs
      ○ skipped preserves an invalid Scale skew on blur for validation
      ○ skipped tracks a Scale configuration interaction
      ○ skipped opens the Size skew tooltip
      ○ skipped preserves a supported Scale draft while capability refresh is pending
      ○ skipped preserves an initial persisted Scale draft while capability support is pending
      ○ skipped resets a selected Scale draft after capability resolves unsupported
      ○ skipped blocks Scale selection when the remote flag is disabled
      ○ skipped blocks Scale placement when the remote flag is disabled
      ○ skipped re-checks selected-route Scale support immediately before placement
      ○ skipped restarts Scale validation when the live position changes during validation
      ○ skipped ignores live mid-price ticks during Scale validation
      ○ skipped uses fresh reduce-only position state after the Scale capability gap
      ○ skipped uses fresh sizing and fee inputs after the Scale capability gap
      ○ skipped uses a fresh Scale ladder after the capability gap
      ○ skipped locks retained Scale callbacks before deferred compliance completes
      ○ skipped blocks Scale placement when its flag turns off during validation
      ○ skipped blocks Scale placement when its provider changes during validation
      ○ skipped keeps Scale locked when capability support is lost during placement
      ○ skipped rejects stale Scale mutations during the capability recheck and submits the original snapshot
      far-from-market warning
        ✓ pushes the far-from-market notice for a long ladder resting below the bid (30 ms)
        ✓ stays quiet for a ladder resting inside the threshold (3 ms)
        ✓ stays quiet before any scale price blur (2 ms)
        ✓ stays quiet while a scale start price is still being typed (4 ms)
        ✓ hides the warning when a finished scale price is edited again (2 ms)
        ✓ stays quiet while the ladder itself is invalid (1 ms)
        ✓ never disables Place for a far-from-market ladder (2 ms)
        ✓ emits the warning-shown event once per distinct message (10 ms)
        ✓ labels a limit-order warning as limit and omits scale properties (1 ms)
        ✓ emits no telemetry while a limit price is still being typed (3 ms)
        ✓ falls back to the far-from-market message on the limit price card (1 ms)
    trigger orders
      ○ skipped explains and blocks a preserved trigger order when the feature is disabled
      ○ skipped submits triggerPrice and omits TP/SL for a stop-market order
      ○ skipped validates trigger placement against mid when mark differs
      ○ skipped uses the 10% default slippage for trigger-market sizing and submission
      ○ skipped exposes persisted slippage for trigger-market settings
      ○ skipped tracks persisted slippage when trigger-market settings open
      ○ skipped preserves an explicit trigger-market slippage setting
      ○ skipped submits triggerPrice and limit price for a take-limit order
      ○ skipped submits canonical venue prices after non-canonical trigger input
      ○ skipped blocks long stop_market before blur and shows guidance after blur
      ○ skipped blocks short stop_market before blur and shows guidance after blur
      ○ skipped blocks long stop_limit before blur and shows guidance after blur
      ○ skipped blocks short stop_limit before blur and shows guidance after blur
      ○ skipped blocks long take_profit_market before blur and shows guidance after blur
      ○ skipped blocks short take_profit_market before blur and shows guidance after blur
      ○ skipped blocks long take_profit_limit before blur and shows guidance after blur
      ○ skipped blocks short take_profit_limit before blur and shows guidance after blur
      ○ skipped clears the helper once a valid trigger price is entered
      ○ skipped shows a new wrong-side error when live mid crosses a blurred trigger
      ○ skipped shows the trigger error before the required limit error
      ○ skipped defers a required limit error for stop_limit until the limit price blurs
      ○ skipped defers a required limit error for take_profit_limit until the limit price blurs
      ○ skipped defers a required trigger error until the trigger price blurs
      ○ skipped keeps field copy blur-gated after a blocked submit attempt
      ○ skipped handles marketability warnings for limit orders
      ○ skipped handles marketability warnings for stop_limit orders
      ○ skipped handles marketability warnings for take_profit_limit orders
      ○ skipped handles marketability warnings for take_profit_limit orders
    additional notices
      ○ skipped flags TP invalid, SL invalid and SL-liquidation-risk as inline notices
    summary slippage
      ○ skipped hides the slippage row for Chase orders
      ○ skipped hides the slippage row for limit orders
      ○ skipped hides the slippage row for trigger-limit orders
      ○ skipped shows maximum slippage only for trigger-market orders
      ○ skipped shows a pending slippage row for market orders when no estimate is available
    isPlaceOrderDisabled
      ○ skipped is disabled on mount for amount ""
      ○ skipped is disabled on mount for amount "0"
      ○ skipped is disabled on mount for amount "not-a-number"
      ○ skipped is disabled when protocol validation is not ready for a positive amount
      ○ skipped is disabled without a notice for a filtered size-positive error
      ○ skipped is disabled for limit when limitPrice is missing
      ○ skipped is disabled for stop_market when triggerPrice is missing
      ○ skipped is disabled for take_profit_market when triggerPrice is missing
      ○ skipped is disabled for stop_limit when triggerPrice is missing
      ○ skipped is disabled for stop_limit when limitPrice is missing
      ○ skipped is disabled for take_profit_limit when triggerPrice is missing
      ○ skipped is disabled for take_profit_limit when limitPrice is missing
      ○ skipped shows loading only while order placement is in progress
      ○ skipped is disabled at the OI cap
      ○ skipped is enabled for a valid, uncapped order
      ○ skipped is disabled while awaiting the first position-modify preview
      ○ skipped is disabled when the stop loss risks liquidation
      ○ skipped is disabled when the take profit is on the wrong side
      ○ skipped is disabled when the stop loss is on the wrong side
      ○ skipped ignores TP/SL blockers while Reduce Only is on with a valid closing side
      ○ skipped disables Place Order while the reduce-only position is loading
    reduceOnly toggle
      ○ skipped restores reduceOnly from the pending trade draft
      ○ skipped clears TP/SL state when Reduce Only turns on
      ○ skipped sets the size slider max to the open position notional when Reduce Only is on
      ○ skipped keeps the margin-based slider max and empty size when Reduce Only is on with no position
      ○ skipped keeps the margin-based slider max and empty size when Reduce Only is on with the wrong direction
      ○ skipped does not commit slider amount when Reduce Only has a position error
      ○ skipped does not restore a focused size after Reduce Only enables with no position
      ○ skipped does not clear typed size while the reduce-only position is loading
      ○ skipped keeps typed size when a valid closing position arrives after Reduce Only load
      ○ skipped uses the limit price for the Reduce Only slider max
      ○ skipped restores the margin-based amount cap when Reduce Only turns off
      ○ skipped does not clamp size to available margin when confirming leverage with Reduce Only on
    handlers
      ○ skipped navigates to the TP/SL screen and its onConfirm sets TP/SL
      ○ skipped shows the limit-price-required toast and does not navigate for a limit order without a price
      ○ skipped confirms leverage, clamps an over-max amount, and tracks the change
      ○ skipped tracks leverage change with previous_leverage and not previousLeverage
      ○ skipped saves slippage and opens the slippage sheet
      ○ skipped selects an order type
      ○ skipped clears incompatible prices when TWAP is selected
      ○ skipped ignores TWAP selection while the feature gate is disabled
      ○ skipped preserves typed digits while blocking an out-of-range duration part
      ○ skipped normalizes leading zeros in TWAP duration parts
      ○ skipped blocks a TWAP duration whose individually valid parts exceed the total maximum
      ○ skipped preserves price values while resetting presentation for a new order type
      ○ skipped ignores size input over nine digits and forwards valid input
      ○ skipped ignores limit price input over nine digits and forwards valid input
      ○ skipped normalizes leading zeroes in limit price input
      ○ skipped normalizes comma decimal input in the limit price
      ○ skipped rejects repeated decimal separators in limit price input
      ○ skipped rejects malformed Chase max distance input 1abc
      ○ skipped rejects malformed Chase max distance input 1.2.3
      ○ skipped normalizes Chase max distance and enforces the shared digit cap
      ○ skipped clears Chase max distance only when its unit changes
      ○ skipped accepts a Chase percentage below the basis-point divisor
      ○ skipped rejects a Chase percentage at the basis-point divisor
      ○ skipped finalizes a trailing decimal separator from the limit price on blur
      ○ skipped does not update the limit price on blur when already finalized
      ○ skipped sets the limit price from the live mid
      ○ skipped previews a slider USD amount before committing on drag end
      ○ skipped forwards the direction and add-funds handlers

Test Suites: 1 passed, 1 total
Tests:       271 skipped, 11 passed, 282 total
Snapshots:   0 total
Time:        1.462 s, estimated 4 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts/i with tests matching "far-from-market".

- PASS assert-hook-tests (assert_exit_code, 53ms): source=run-hook-tests, expected=0, actual=0
- PASS open-btc-pro (ui.navigate, 5.7s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation+visible-native-navigation
- PASS wait-pro-form (ui.wait_for, 1.1s): matched=true, testId=perps-pro-order-form, expected=present, present=true, visible=true
- PASS open-order-type (ui.press, 670ms): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-1
- PASS wait-sheet (ui.wait_for, 669ms): matched=true, testId=perps-order-type-tab-advanced, expected=present, present=true, visible=true
- PASS open-advanced-tab (ui.press, 739ms): ok=true, testId=perps-order-type-tab-advanced, deviceName=mm-1
- PASS wait-scale-option (ui.wait_for, 637ms): matched=true, testId=perps-order-type-scale, expected=present, present=true, visible=true
- PASS select-scale (ui.press, 1.1s): ok=true, testId=perps-order-type-scale, deviceName=mm-1
- PASS wait-scale-start (ui.wait_for, 903ms): matched=true, testId=perps-pro-order-form-scale-start-price, expected=present, present=true, visible=true
- PASS wait-scale-end (ui.wait_for, 809ms): matched=true, testId=perps-pro-order-form-scale-end-price, expected=present, present=true, visible=true
- PASS wait-place (ui.wait_for, 867ms): matched=true, testId=perps-pro-order-form-place-order, expected=present, present=true, visible=true
- PASS shot-scale-form (ui.screenshot, 806ms): path=screenshots/after-scale-form.png
- PASS done (end, 0ms)
