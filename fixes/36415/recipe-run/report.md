# MetaMask Recipe Run

Status: pass
Duration: 51s
Nodes: 18/18 passed

## Side findings
- REVIEW 109 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-restart (app.lifecycle, 21s): platform=ios-simulator
- PASS setup-status (app.status, 2ms): platform=mobile
- PASS setup-unlock (metamask.wallet.ensure_unlocked, 6.1s): platform=ios, proof=agentic-wallet-unlock
- PASS ac1-run-transform-tests (command, 17s): exitCode=0, stdout=      ○ skipped transforms all provided transactions (filtering is done by the hook)
      ○ skipped returns deposit PerpsTransaction with amount and Completed status
      ○ skipped uses Deposit title when amount is zero or token data missing
      ○ skipped maps failed status to Failed subtitle
      ○ skipped maps pending status to Pending subtitle
      ○ skipped uses tx.time and tx.hash when present
      ○ skipped uses Deposit title and zero amount when getTokenTransferData returns undefined
    walletPerpsWithdrawalsToRequests
      ○ skipped converts wallet TransactionMeta to WithdrawalRequest format
      ○ skipped maps wallet status to withdrawal request status
      ○ skipped maps submitted status to pending
      ○ skipped returns zero amount when getTokenTransferData returns undefined
      ○ skipped uses tx.time and tx.hash
      ○ skipped prefixes id with wallet-

Test Suites: 1 passed, 1 total
Tests:       124 skipped, 9 passed, 133 total
Snapshots:   0 total
Time:        6.541 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/transactionTransforms.test.ts/i with tests matching "aggregation".

- PASS ac1-assert-transform-tests (assert_exit_code, 0ms): source=ac1-run-transform-tests, expected=0, actual=0
- PASS ac1-index-test-log (index_artifacts, 9ms)
- PASS setup-nav-perps-root (ui.navigate, 1.3s): route=PerpsActivity, proof=agentic-navigation
- PASS setup-open-type-filter (ui.press, 858ms): ok=true, testId=activity-screen-type-filter-chip, deviceName=mm-1
- PASS setup-wait-type-sheet (ui.wait_for, 492ms): matched=true, testId=activity-screen-type-filter-option-perps, expected=visible, present=true, visible=true
- PASS setup-choose-perps (ui.press, 596ms): ok=true, testId=activity-screen-type-filter-option-perps, deviceName=mm-1
- PASS gate-perps-trades (ui.wait_for, 926ms): matched=true, testId=activity-screen-perps-filter-chip, expected=visible, present=true, visible=true
- PASS ac1-wait-control (ui.wait_for, 553ms): matched=true, testId=activity-screen-aggregated-checkbox, expected=visible, present=true, visible=true
- PASS ac2-wait-rows (ui.wait_for, 645ms): matched=true, testId=transaction-item-1, expected=visible, present=true, visible=true
- PASS ac2-screenshot-aggregated (ui.screenshot, 603ms): path=screenshots/evidence-ac2-aggregated-on.png
- PASS ac2-press-control (ui.press, 697ms): ok=true, testId=activity-screen-aggregated-checkbox, deviceName=mm-1
- PASS ac2-wait-after-toggle (ui.wait_for, 541ms): matched=true, testId=transaction-item-12, expected=visible, present=true, visible=true
- PASS ac2-screenshot-individual (ui.screenshot, 535ms): path=screenshots/evidence-ac2-aggregated-off.png
- PASS teardown-done (end, 0ms)
