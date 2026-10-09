# MetaMask Recipe Run

Status: pass
Duration: 153s
Nodes: 45/45 passed

## Side findings
- REVIEW 8 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-flag (metamask.feature_flags.set, 458ms): proof=mobile-remote-feature-flags
- PASS setup-pro (metamask.perps.start_state, 24s): proof=metamask-perps-start-state
- PASS setup-no-btc-position (metamask.perps.ensure_positions, 1.6s): matching=0
- PASS setup-no-btc-orders (metamask.perps.ensure_orders, 1.2s): matching=0
- PASS setup-show-margin-control (ui.scroll, 1.9s): ok=true, testId=perps-pro-order-form-margin-mode, intoView=true, alreadyVisible=true
- PASS setup-open-order-type (ui.press, 1.3s): ok=true, testId=perps-pro-order-form-order-type, deviceName=mm-2
- PASS setup-basic-tab (ui.press, 1.3s): ok=true, testId=perps-order-type-tab-basic, deviceName=mm-2
- PASS setup-wait-market-type (ui.wait_for, 1.3s): matched=true, testId=perps-order-type-market, expected=visible, present=true, visible=true
- PASS setup-pick-market-type (ui.press, 1.6s): ok=true, testId=perps-order-type-market, deviceName=mm-2
- PASS gate-margin-button (ui.wait_for, 1.5s): matched=true, testId=perps-pro-order-form-margin-mode, expected=visible, present=true, visible=true
- PASS ac1-open-sheet (ui.press, 1.3s): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-2
- PASS ac1-wait-cross-option (ui.wait_for, 1.3s): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-press-cross (ui.press, 1.8s): ok=true, testId=perps-margin-mode-cross, deviceName=mm-2
- PASS ac1-wait-sheet-closed (ui.wait_for, 1.5s): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac1-show-margin-control (ui.swipe, 22s): action=ui.swipe, backend=idb-ui, segments=1, settlementWarning=ui.swipe did not reach a settled native UI state: wait timed out waiting for a stable UI
- PASS ac1-wait-cross-label (ui.wait_for, 2.2s): matched=true, testId=perps-pro-order-form-margin-mode, text=Cross, textMatch=exact, expected=visible
- PASS ac1-screenshot-cross-label (ui.screenshot, 3.6s): path=screenshots/evidence-ac1-cross-label.png
- PASS ac1-reopen-sheet (ui.press, 1.5s): ok=true, testId=perps-pro-order-form-margin-mode, deviceName=mm-2
- PASS ac1-wait-cross-selected (ui.wait_for, 931ms): matched=true, testId=perps-margin-mode-cross, expected=visible, present=true, visible=true
- PASS ac1-screenshot-cross-sheet (ui.screenshot, 775ms): path=screenshots/evidence-ac1-cross-sheet.png
- PASS ac2-keep-cross (ui.press, 574ms): ok=true, testId=perps-margin-mode-cross, deviceName=mm-2
- PASS ac2-wait-sheet-closed (ui.wait_for, 750ms): matched=true, testId=perps-margin-mode-bottom-sheet, expected=absent, present=false, visible=false
- PASS ac2-scroll-size (ui.scroll, 776ms): ok=true, testId=perps-pro-order-form-size-card, intoView=true, alreadyVisible=true
- PASS ac2-wait-size (ui.wait_for, 757ms): matched=true, testId=perps-pro-order-form-size-card, expected=visible, present=true, visible=true
- PASS ac2-set-size (ui.set_input, 739ms): ok=true, testId=perps-pro-order-form-size-input, value=15, deviceName=mm-2
- PASS ac2-scroll-submit (ui.scroll, 1.3s): animated=false, offset=600, ok=true, testId=perps-pro-order-form-summary-fees, deviceName=mm-2
- PASS ac2-wait-submit (ui.wait_for, 842ms): matched=true, testId=perps-pro-order-form-place-order, expected=visible, present=true, visible=true
- PASS ac2-press-submit (ui.press, 1.1s): ok=true, testId=perps-pro-order-form-place-order, deviceName=mm-2
- PASS ac2-assert-position-open (metamask.perps.assert_positions, 7.5s): matching=1
- PASS ac2-filter-btc (ui.press, 784ms): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-2
- PASS ac2-swipe-to-positions (ui.swipe, 2.7s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-swipe-to-card (ui.swipe, 2.7s): action=ui.swipe, backend=idb-ui, segments=1
- PASS ac2-wait-cross-tag (ui.wait_for, 804ms): matched=true, testId=cross-margin-tag-pro-BTC, expected=visible, present=true, visible=true
- PASS ac2-screenshot-cross-position (ui.screenshot, 932ms): path=screenshots/evidence-ac2-cross-position.png
- PASS teardown-close-btc (metamask.perps.close_positions, 4.2s): matching=0
- PASS teardown-assert-flat (metamask.perps.assert_positions, 460ms): matching=0
- PASS teardown-unfilter-btc (ui.press, 784ms): ok=true, testId=perps-pro-market-positions-ticker-only, deviceName=mm-2
- PASS teardown-clear-flag (metamask.feature_flags.clear, 342ms): proof=mobile-remote-feature-flags
- PASS ac2-run-order-params-tests (command, 18s): exitCode=0, stderr=PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts (11.477 s)
PASS app/components/UI/Perps/utils/orderParams.test.ts

Test Suites: 2 passed, 2 total
Tests:       329 skipped, 40 passed, 369 total
Snapshots:   0 total
Time:        13.721 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts|app\/components\/UI\/Perps\/utils\/orderParams.test.ts/i with tests matching "margin mode".

- PASS ac2-assert-tests-pass (assert_exit_code, 54ms): source=ac2-run-order-params-tests, expected=0, actual=0
- PASS ac3-run-gating-tests (command, 27s): exitCode=0, stderr=PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.view.test.tsx (14.031 s)
  PerpsProOrderFormPanel Cross orders [ios]
    ✓ selects Cross, updates the form and submits the chosen mode (819 ms)
    ✓ switches back to Isolated without an open position (170 ms)
    ✓ keeps Cross unavailable for rollout flag off (184 ms)
    ✓ keeps Cross unavailable for Pro inactive (213 ms)
    ✓ keeps Cross unavailable for Terminal backend (223 ms)
    ✓ keeps Cross unavailable for HIP-3 market (176 ms)
    ✓ keeps Cross unavailable for Lighter market (198 ms)
    ✓ keeps Cross unavailable for isolated-only asset (167 ms)
    ✓ keeps Cross unavailable for noCross asset (210 ms)
    ✓ keeps Cross unavailable for strictIsolated asset (148 ms)
    ✓ holds Cross selection and submission until the venue lock resolves (476 ms)
    ✓ keeps Cross unavailable until market restrictions arrive (162 ms)
  PerpsProOrderFormPanel Cross orders [android]
    ✓ selects Cross, updates the form and submits the chosen mode (601 ms)
    ✓ switches back to Isolated without an open position (93 ms)
    ✓ keeps Cross unavailable for rollout flag off (101 ms)
    ✓ keeps Cross unavailable for Pro inactive (73 ms)
    ✓ keeps Cross unavailable for Terminal backend (105 ms)
    ✓ keeps Cross unavailable for HIP-3 market (175 ms)
    ✓ keeps Cross unavailable for Lighter market (104 ms)
    ✓ keeps Cross unavailable for isolated-only asset (109 ms)
    ✓ keeps Cross unavailable for noCross asset (72 ms)
    ✓ keeps Cross unavailable for strictIsolated asset (87 ms)
    ✓ holds Cross selection and submission until the venue lock resolves (429 ms)
    ✓ keeps Cross unavailable until market restrictions arrive (155 ms)

Test Suites: 1 passed, 1 total
Tests:       24 passed, 24 total
Snapshots:   0 total
Time:        14.165 s
Force exiting Jest: Have you considered using `--detectOpenHandles` to detect async operations that kept running after all tests finished?

- PASS ac3-assert-tests-pass (assert_exit_code, 36ms): source=ac3-run-gating-tests, expected=0, actual=0
- PASS ac4-run-cross-position-tests (command, 4.2s): exitCode=0, stderr=PASS app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.test.ts
  usePerpsProOrderForm
    availableBalance
      ○ skipped formats spendable balance as "$amount available" when connected
      ○ skipped shows the unavailable placeholder before Perps is initialized
    summary
      ○ skipped builds display-ready margin, liquidation, slippage and numeric fees
      ○ skipped shows the fallback liquidation display when amount is empty
      ○ skipped shows margin and liquidation before-and-after values from the controller preview
      ○ skipped keeps single-value summary when the position-modify preview flag is off
      ○ skipped keeps single-value summary when the controller returns no preview
      ○ skipped keeps single-value summary for unsupported cross-margin previews
      ○ skipped uses the controller fee result unchanged for a TWAP order
      ○ skipped routes Scale fees and validation through the concrete provider
      ○ skipped lets a Scale order switch its size denomination without changing notional
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
      ○ skipped formats the chase reference price with market entry-price decimals
      ○ skipped keeps sub-cent chase prices instead of collapsing them to a 2-decimal floor
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
      ○ skipped shows the size precision bound when a TWAP suborder rounds below it
      ○ skipped shows the TWAP size per suborder at the asset size precision
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
      ○ skipped routes a displayed provider through market fees, validation, preview, and placement
      ○ skipped routes a displayed provider through limit fees, validation, preview, and placement
      ○ skipped routes a displayed provider through stop_market fees, validation, preview, and placement
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
      ○ skipped places a trigger-limit order whose trigger is on the wrong side of mid
      ○ skipped still refuses a trigger-limit order that has no limit price
      ○ skipped keeps the CTA enabled without loading while validation is pending
      ○ skipped runs current validation before executing a pending order
      ○ skipped places a pending trigger order even when the live mid crosses the trigger
      ○ skipped navigates to the cross-margin warning and aborts
      ○ skipped aborts and tracks when the estimated slippage exceeds the max
      ○ skipped aborts submit when the stop loss risks liquidation (doesStopLossRiskLiquidation guard)
      ○ skipped skips updatePositionTPSL and clearPendingConfig when the order fails (shouldHandleTPSLSeparately path)
      ○ skipped skips clearPendingConfig when the order fails (plain else path)
    margin mode
      ○ skipped sends cross margin mode after the trader selects Cross
      ○ skipped sends isolated margin mode by default when Cross is available
      ○ skipped omits margin mode when Cross is unavailable
      ○ skipped shows no liquidation estimate for a Cross order
      ○ skipped keeps the liquidation estimate for an isolated order when Cross is available
      ○ skipped does not flag the stop loss against the isolated liquidation estimate for a Cross order
      ○ skipped keeps Cross unavailable on an asset with onlyIsolated
      ○ skipped keeps Cross unavailable on an asset with a strictIsolated margin mode
      ○ skipped keeps Cross unavailable on an asset with a noCross margin mode
      ○ skipped offers Cross when only another provider restricts the same symbol to isolated
      ○ skipped keeps Cross unavailable when only the selected provider restricts the same symbol to isolated
      ○ skipped keeps Cross unavailable while market data has not loaded
      ○ skipped keeps Cross unavailable while market data is refetching
      ○ skipped still shows the unsupported warning for a cross position on an isolated-only asset
      ○ skipped drops a Cross pick after an account switch
      ○ skipped drops a Cross pick after a network switch
      ○ skipped keeps a Cross pick dropped after switching back to the original account
      ○ skipped drops a Cross pick after a Perps account group switch
      ○ skipped drops a Cross pick once Cross becomes unavailable
      ○ skipped drops a Cross pick after a market switch
      ○ skipped re-reads the venue margin mode lock after an order is placed
      ○ skipped locks the picker on the current mode while the venue lock is unknown
      ○ skipped locks the picker but still places the order when the venue reports the lock as unavailable
      ○ skipped disables Place Order and places nothing while the venue lock is unknown
      ○ skipped holds Place Order after an account switch until the new venue lock resolves
      ○ skipped holds Place Order after a network switch until the new venue lock resolves
      ○ skipped keeps Place Order enabled without a lock answer when Cross is unavailable
      ○ skipped re-reads the venue lock when the screen regains focus
      ○ skipped keeps the picker free without an open position
      ○ skipped looks up the position on the selected market provider
      resting order or TWAP on the market
        ○ skipped follows the venue margin mode and locks the picker
        ○ skipped sends the venue margin mode with the order
        ○ skipped keeps showing the venue margin mode while the lock is re-read
        ○ skipped ignores the venue lock when Cross is unavailable
      existing cross position
        ✓ follows the position margin mode and locks the picker (17 ms)
        ✓ places the order in cross margin instead of showing the unsupported warning (2 ms)
        ✓ still shows the unsupported warning when Cross is unavailable (2 ms)
    execution toasts
      ○ skipped shows the accepted size when the provider rounds the requested size
      ○ skipped returns to the presenting screen after a stay-on-screen order is confirmed
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
      ○ skipped keeps Scale placement disabled for a Lighter route
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
      ○ skipped sends the selected margin mode with a Scale order
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
      ○ skipped reports the whole ladder margin as a single target value
      ○ skipped reports the ladder liquidation price as a single target value
      ○ skipped keeps Scale liquidation unavailable for an existing position
      ○ skipped keeps Scale liquidation unavailable while position state loads
      ○ skipped keeps Scale liquidation unavailable when calculation returns zero
      ○ skipped falls back on both Scale summary rows when the ladder is invalid
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
        ○ skipped pushes the far-from-market notice for a long ladder resting below the bid
        ○ skipped stays quiet for a ladder resting inside the threshold
        ○ skipped stays quiet before any scale price blur
        ○ skipped stays quiet while a scale start price is still being typed
        ○ skipped hides the warning when a finished scale price is edited again
        ○ skipped stays quiet while the ladder itself is invalid
        ○ skipped never disables Place for a far-from-market ladder
        ○ skipped emits the warning-shown event once per distinct message
        ○ skipped labels a limit-order warning as limit and omits scale properties
        ○ skipped emits no telemetry while a limit price is still being typed
        ○ skipped falls back to the far-from-market message on the limit price card
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
      ○ skipped stays quiet for long stop_market before blur and warns after blur
      ○ skipped stays quiet for short stop_market before blur and warns after blur
      ○ skipped stays quiet for long stop_limit before blur and warns after blur
      ○ skipped stays quiet for short stop_limit before blur and warns after blur
      ○ skipped stays quiet for long take_profit_market before blur and warns after blur
      ○ skipped stays quiet for short take_profit_market before blur and warns after blur
      ○ skipped stays quiet for long take_profit_limit before blur and warns after blur
      ○ skipped stays quiet for short take_profit_limit before blur and warns after blur
      ○ skipped clears the helper once a valid trigger price is entered
      ○ skipped shows a new wrong-side warning when live mid crosses a blurred trigger
      ○ skipped warns about a stop limit buy resting below its trigger without blocking it
      ○ skipped warns about a take profit limit sell resting above its trigger without blocking it
      ○ skipped stays quiet about a trigger price the user is still typing
      ○ skipped warns once the half-typed trigger price is committed
      ○ skipped stays quiet when a stop limit buy rests at or above its trigger
      ○ skipped shows the blocking limit error rather than advice about a placeable trigger
      ○ skipped defers a required limit error for stop_limit until the limit price blurs
      ○ skipped defers a required limit error for take_profit_limit until the limit price blurs
      ○ skipped shows a 95% band error before the limit price blurs
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
      ○ skipped opens TP/SL as a bottom sheet when assigned the bottom-sheet arm
      ○ skipped omits useBottomSheet from the TP/SL route on the screen arm
      ○ skipped shows the limit-price-required toast and does not navigate for a limit order without a price
      ○ skipped confirms leverage, clamps an over-max amount, and tracks the change
      ○ skipped tracks leverage change with previous_leverage and not previousLeverage
      ○ skipped saves slippage and opens the slippage sheet
      ○ skipped selects an order type
      ○ skipped forgets committed prices when twap discards them
      ○ skipped forgets committed prices when scale discards them
      ○ skipped forgets committed prices when chase discards them
      ○ skipped clears incompatible prices when TWAP is selected
      ○ skipped ignores TWAP selection while the feature gate is disabled
      ○ skipped preserves typed digits while blocking an out-of-range duration part
      ○ skipped normalizes leading zeros in TWAP duration parts
      ○ skipped blocks a TWAP duration whose individually valid parts exceed the total maximum
      ○ skipped keeps showing the trigger warning when the carried-over price moves to a new order type
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
Tests:       344 skipped, 3 passed, 347 total
Snapshots:   0 total
Time:        1.895 s, estimated 12 s
Ran all test suites matching /app\/components\/UI\/Perps\/Views\/PerpsProMarketView\/components\/PerpsProOrderForm\/usePerpsProOrderForm.test.ts/i with tests matching "existing cross position".

- PASS ac4-assert-tests-pass (assert_exit_code, 37ms): source=ac4-run-cross-position-tests, expected=0, actual=0
- PASS done (end, 0ms)
