# MetaMask Recipe Run

Status: pass
Duration: 184s
Nodes: 20/20 passed

## Side findings
- REVIEW 12 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-status (app.status, 628ms): platform=mobile
- PASS setup-unlock (metamask.wallet.ensure_unlocked, 8.5s): platform=ios, proof=agentic-wallet-unlock
- PASS setup-open-perps (ui.navigate, 14s): route=PerpsMarketListView, page=perps, proof=agentic-navigation
- PASS gate-perps-home (ui.wait_for, 4.7s): matched=true, testId=perps-home-heading, expected=present, present=true, visible=true
- PASS setup-open-market (ui.navigate, 18s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation+visible-native-navigation
- PASS setup-clean-market (metamask.perps.start_state, 9.1s): proof=metamask-perps-start-state
- PASS gate-market-page (ui.wait_for, 3.4s): matched=true, testId=perps-market-details-long-button, expected=present, present=true, visible=true
- PASS ac1-open-order-form (ui.press, 5.7s): ok=true, testId=perps-market-details-long-button, deviceName=mmdev-1
- PASS ac1-wait-order-form (ui.wait_for, 2.4s): matched=true, testId=perps-order-view-place-order-button, expected=present, present=true, visible=true
- PASS ac1-place-order (ui.press, 9.5s): ok=true, testId=perps-order-view-place-order-button, deviceName=mmdev-1
- PASS ac1-wait-position-open (ui.wait_for, 6.7s): matched=true, testId=perps-market-details-close-button, expected=present, present=true, visible=true
- PASS ac1-press-back (ui.press, 5.9s): ok=true, testId=perps-market-header-back-button, deviceName=mmdev-1
- PASS ac1-assert-order-screen-gone (ui.wait_for, 4.0s): matched=true, testId=perps-order-view-place-order-button, expected=absent, present=false, visible=false
- PASS ac1-assert-back-to-perps-home (ui.wait_for, 6.5s): matched=true, testId=perps-home-heading, expected=present, present=true, visible=true
- PASS ac1-screenshot-perps-home (ui.screenshot, 14s): path=screenshots/evidence-ac1-back-lands-on-perps-home.png
- PASS ac2-run-navigation-unit-tests (command, 56s): exitCode=0, stdout=      at scheduleUpdateOnFiber (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:12086:9)
      at dispatchSetStateInternal (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6208:13)
      at dispatchSetState (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6165:7)
      at Timeout.setIsDataReady [as _onTimeout] (app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:282:7)

    console.error
      An update to PerpsOrderViewContentBase inside a test was not wrapped in act(...).
      
      When testing, code that causes React state updates should be wrapped into act(...):
      
      act(() => {
        /* fire events that update state */
      });
      /* assert on the output */
      
      This ensures that you're testing the behavior the user would see in the browser. Learn more at https://react.dev/link/wrap-tests-with-act

      280 |     // Defer data loading to next frame for faster initial render
      281 |     requestAnimationFrame(() => {
    > 282 |       setIsDataReady(true);
          |       ^
      283 |     });
      284 |   }, []);
      285 |

      at node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14402:19
      at runWithFiberInDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:2315:13)
      at warnIfUpdatesNotWrappedWithActDEV (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:14401:9)
      at scheduleUpdateOnFiber (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:12086:9)
      at dispatchSetStateInternal (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6208:13)
      at dispatchSetState (node_modules/react-test-renderer/cjs/react-test-renderer.development.js:6165:7)
      at Timeout.setIsDataReady [as _onTimeout] (app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:282:7)

A worker process has failed to exit gracefully and has been force exited. This is likely caused by tests leaking due to improper teardown. Try running with --detectOpenHandles to find leaks. Active timers can also cause this, ensure that .unref() was called on them.

Test Suites: 2 passed, 2 total
Tests:       151 passed, 151 total
Snapshots:   0 total
Time:        41.343 s, estimated 54 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/perpsModeSwitch.test.ts|app\/components\/UI\/Perps\/Views\/PerpsOrderView\/PerpsOrderView.test.tsx/i.

- PASS ac2-assert-navigation-unit-tests-pass (assert_exit_code, 144ms): source=ac2-run-navigation-unit-tests, expected=0, actual=0
- PASS ac2-index-test-log (index_artifacts, 208ms)
- PASS teardown-clean-market (metamask.perps.teardown_state, 7.3s): proof=metamask-perps-teardown-state
- PASS teardown-end (end, 0ms)
