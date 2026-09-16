# MetaMask Recipe Run

Status: pass
Duration: 79s
Nodes: 27/27 passed

## Side findings
- REVIEW 109 distinct application warning/error event(s) (non-blocking; expanded below and stored in diagnostics.json)

## Steps
- PASS setup-restart (app.lifecycle, 23s): platform=ios-simulator
- PASS setup-status (app.status, 49ms): platform=mobile
- PASS setup-unlock (metamask.wallet.ensure_unlocked, 7.0s): platform=ios, proof=agentic-wallet-unlock
- PASS ac1-run-transform-tests (command, 16s): exitCode=0, stdout=      ✓ transforms completed deposit correctly
      ✓ transforms completed withdrawal correctly
      ✓ filters out non-completed items
      ✓ handles missing txHash
    transformWithdrawalRequestsToTransactions
      ✓ transforms completed withdrawal request correctly (1 ms)
      ✓ transforms pending withdrawal with Pending subtitle
      ✓ transforms failed withdrawal with Failed subtitle
      ✓ uses Withdrawal title when amount is zero
      ✓ handles missing txHash
    transformDepositRequestsToTransactions
      ✓ transforms completed deposit request correctly
      ✓ handles zero amount deposits
      ✓ handles zero string amount deposits
      ✓ filters out non-completed deposit requests
      ✓ handles missing txHash
    edge cases
      ✓ handles empty arrays
      ✓ handles BigNumber edge cases (1 ms)
    transformWalletPerpsDepositsToTransactions
      ✓ transforms all provided transactions (filtering is done by the hook)
      ✓ returns deposit PerpsTransaction with amount and Completed status
      ✓ uses Deposit title when amount is zero or token data missing
      ✓ maps failed status to Failed subtitle
      ✓ maps pending status to Pending subtitle
      ✓ uses tx.time and tx.hash when present
      ✓ uses Deposit title and zero amount when getTokenTransferData returns undefined
    walletPerpsWithdrawalsToRequests
      ✓ converts wallet TransactionMeta to WithdrawalRequest format (1 ms)
      ✓ maps wallet status to withdrawal request status
      ✓ maps submitted status to pending
      ✓ returns zero amount when getTokenTransferData returns undefined
      ✓ uses tx.time and tx.hash
      ✓ prefixes id with wallet-

Test Suites: 1 passed, 1 total
Tests:       126 passed, 126 total
Snapshots:   0 total
Time:        6.215 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/transactionTransforms.test.ts/i.

- PASS ac1-assert-transform-tests (assert_exit_code, 28ms): source=ac1-run-transform-tests, expected=0, actual=0
- PASS ac1-index-test-log (index_artifacts, 35ms)
- PASS ac3-run-flip-test (command, 14s): exitCode=0, stdout=      ○ skipped transforms all provided transactions (filtering is done by the hook)
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
Tests:       125 skipped, 1 passed, 126 total
Snapshots:   0 total
Time:        5.311 s, estimated 7 s
Ran all test suites matching /app\/components\/UI\/Perps\/utils\/transactionTransforms.test.ts/i with tests matching "aggregates flip fills of one order and keeps the opening position size".

- PASS ac3-assert-flip-test (assert_exit_code, 27ms): source=ac3-run-flip-test, expected=0, actual=0
- PASS ac3-index-flip-log (index_artifacts, 30ms)
- PASS setup-nav-perps-root (ui.navigate, 2.5s): route=PerpsMarketListView, page=perps, proof=agentic-navigation
- PASS ac2-nav-market (ui.navigate, 2.0s): route=PerpsMarketDetails, page=perps-market, proof=agentic-navigation
- PASS setup-ensure-lite (metamask.perps.ensure_mode, 412ms): proof=visible-market-detail-root-and-active-mode-control
- PASS ac2-wait-trade-rows (ui.wait_for, 764ms): matched=true, testId=perps-market-trades-row-1, expected=present, present=true, visible=true
- PASS ac2-assert-full-size (ui.wait_for, 682ms): matched=true, text=8.29 SOL, textMatch=contains, expected=present, present=true
- PASS ac2-assert-open-total (ui.wait_for, 713ms): matched=true, text=-$1.15, textMatch=contains, expected=present, present=true
- PASS ac2-scroll-to-trades (ui.scroll, 1.3s): animated=false, measuredOffset=1203, ok=true, testId=perps-market-trades-list, deviceName=mm-1
- PASS ac2-wait-trades-visible (ui.wait_for, 646ms): matched=true, testId=perps-market-trades-row-1, expected=visible, present=true, visible=true
- PASS ac2-screenshot-market-detail (ui.screenshot, 564ms): path=screenshots/evidence-ac2-market-detail.png
- PASS ac4-nav-home (ui.navigate, 2.3s): route=PerpsMarketListView, page=perps, proof=agentic-navigation
- PASS ac4-wait-home-rows (ui.wait_for, 821ms): matched=true, testId=perps-recent-activity-row-1, expected=present, present=true, visible=true
- PASS ac4-assert-home-full-size (ui.wait_for, 747ms): matched=true, text=8.29 SOL, textMatch=contains, expected=present, present=true
- PASS ac4-assert-home-open-total (ui.wait_for, 797ms): matched=true, text=-$1.15, textMatch=contains, expected=present, present=true
- PASS ac4-open-activity (ui.press, 1.1s): ok=true, text=Recent activity, deviceName=mm-1
- PASS gate-activity-perps-trades (ui.wait_for, 1.2s): matched=true, testId=activity-screen-perps-filter-chip, expected=visible, present=true, visible=true
- PASS ac4-wait-activity-row (ui.wait_for, 673ms): matched=true, testId=transaction-item-2, expected=visible, present=true, visible=true
- PASS ac4-screenshot-activity (ui.screenshot, 509ms): path=screenshots/evidence-ac4-activity-page.png
- PASS teardown-done (end, 0ms)
