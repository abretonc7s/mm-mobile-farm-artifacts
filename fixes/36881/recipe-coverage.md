# Recipe coverage for PR #36881

Current proof run `temp/tasks/fix/36881-1001-124447/artifacts/recipe-run` began 2026-10-01T05:21:58.642Z and passed 45/45 nodes. Product HEAD `2bac9222184e31036d85bb2bc32300b289695606` plus staged diff SHA256 `22a29b1cbcd8637dfdcfffb6a73bc10da257aa8cfb0e9f10bf9b719b824cc45b`; recipe SHA256 `93994b6e2fc8e0a380459f0cb66fe271216827d5990c3d4a067274cfdd38ac88`. iOS simulator mm-2, mini-mm-2, Hyperliquid testnet, canonical Trading fixture. No source or dependency changes during execution. The committed tree will contain these exact staged bytes. Recipe is unchanged from inheritance. No video recorded.

Promoted screenshots and proof trace/summary/manifests are byte-identical to this one run. Every promoted image was read. Failed prior attempt is retained separately and contributes no promoted evidence. Historical mm-6/head 40cdf2f5bce evidence is retained only in the inherited package.

| Criterion | Mode | Evidence | Result |
|---|---|---|---|
| ac1: flag-on Cross selection and form label | visual | evidence-ac1-cross-sheet.png, evidence-ac1-cross-label.png; wait_for Cross targets before capture | PROVEN |
| ac2: submit chosen margin mode and open Cross position | mixed | assert_positions open, Cross-tag wait, evidence-ac2-cross-position.png; recipe-test-logs/ac2-jest.log, 40 passed | PROVEN |
| ac3: flag/provider/market restrictions | state | recipe-test-logs/ac3-jest.log, 15 passed, exit-code assertion | PROVEN by unit tests; live negative cases not rerun |
| ac4: existing Cross position permits trading | state | recipe-test-logs/ac4-jest.log, 3 passed, exit-code assertion | PROVEN by unit tests |
| Reviewer 4151206075: no isolated risk estimate or stop threshold in new Cross editors | state | cross-editors-view.log, 2 passed; cross-editors-negative.log, both fail without handoffs; leverage-cache and isolated-stop regressions in full gate | PROVEN by real component-view journeys; inherited device recipe does not enter editors |

Setup explicitly applied fixture and selected Trading with supported account parameter because inherited account_name is ignored by this harness. Closed stray ETH 0.0594 on testnet. First attempt opened BTC but first-run notification prompt obscured visual proof. Dismissed prompt; repeat setup closed that BTC, then placed a fresh one. Successful teardown closed BTC and asserted flat, cleared both remote flag overrides. Position filter is a toggle and its inherited initial state was not reset; this does not affect the single-BTC assertion or images.

Diagnostics recorded six distinct events: Money Account 403/circuit-breaker errors, Terminal snapshot 400, and missing SubscriptionController:getBenefits delegation warnings. They did not fail the flow and are not evidence of the editor change. Full-project TypeScript and fresh remote CI remain unverified locally. No layout-responsiveness or Android proof is claimed.

Committed as `fbcbda2de2d2d87d83a57b11d140728af248e895`. Post-commit diff SHA256 exactly matched the recorded staged diff, so commit hooks did not change the tested product bytes.
