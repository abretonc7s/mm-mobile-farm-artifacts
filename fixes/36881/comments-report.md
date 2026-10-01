# PR #36881 review completion

Status: authorized review-completion work finished; fresh remote CI pending.

| # | Source | Author | File | Triage | Action |
|---|---|---|---|---|---|
| 4151206075 | review_comment | geositta | usePerpsProOrderForm.ts:1688 | REAL | Pass typed margin mode to leverage and TP/SL editors; hide isolated estimates and allow Cross stops beyond the isolated threshold. |
| 5844369405 | issue_comment | deeeed | usePerpsProOrderForm.ts:885 | REAL, already fixed | Provider-scoped market lookup and conflicting same-symbol tests remain present after rebase. Author already replied in 5844538507. |

The CHANGES_REQUESTED review 5374215622 repeats inline finding 4151206075 and is covered by the same fix. Two other root review threads were already resolved; both inline replies retained in snapshot. Skipped eight status-only bot issue comments, including performance no_performance_metrics with no green main baseline, plus six author commands/progress updates. No metamask-flaky-test-detection comment present. No status replies planned.

Total comments: 20, with 3 REAL, 1 FALSE POSITIVE, 16 OUT OF SCOPE. One REAL finding fixed this run; two historical REAL findings retained. Status-only and author replies are included as OUT_OF_SCOPE bookkeeping, not treated as reviewer defects. Review body 5374215622 duplicates inline 4151206075. All original snapshot bodies retained in comments-triage.json.

Fix commit: `fbcbda2de2d2d87d83a57b11d140728af248e895`. Integration status: `rebased`. Single explicit-lease push succeeded; commit hooks passed and committed diff SHA256 matches validated staged diff. Working tree clean. No PR merge performed. No new comments fetched after push. Reviewer reply https://github.com/MetaMask/metamask-mobile/pull/36881#discussion_r4152133881 posted and thread resolved.

Recipe re-validation: PASS, 45/45, one complete current evidence package from recipe-run. Bounded gate: policy, ESLint, Prettier, 498 unit, 14 integration, 11 component-view tests PASS; 105 editor consumer tests PASS. Two Cross journeys pass and fail without handoffs. Full-project TypeScript is deferred to remote CI. Fresh post-push CI was not monitored in this single-pass workflow; this report does not claim CI green or merge approval.

Files changed in fix commit:

- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderForm/usePerpsProOrderForm.ts
- app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.tsx
- app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.tsx
- app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.view.test.tsx
- app/components/UI/Perps/components/PerpsLeverageBottomSheet/PerpsLeverageBottomSheet.test.tsx
- app/components/UI/Perps/components/PerpsLeverageBottomSheet/PerpsLeverageBottomSheet.tsx
- app/components/UI/Perps/integration/marginModeLock.integration.test.ts
- app/components/UI/Perps/types/navigation.ts
- tests/component-view/mocks.ts
- app/components/UI/Perps/Views/PerpsProMarketView/PerpsProCrossMargin.view.test.tsx

## Integration

Rebased onto origin/main. Preserved screen/bottom-sheet A/B hook alongside venue-lock imports/mocks. Retained main's perps-controller 19.0.0: released getMarginModeLock, account consistency checks, resting-order/TWAP checks and placement validation match the backport, so the obsolete 18.0.1 patch and manifest changes are removed. yarn install --immutable passed. The 14 integration tests passed against the released API.

## Scope

The ticket and PR require Cross selection/order propagation and no isolated-only estimate for Cross. Both editors are executable from the newly enabled Cross workflow, so the reviewer request is in scope. Terminal restrictions and Lite/Reverse reconciliation remain explicitly deferred in the PR.

## Local validation

Final mm-harness check diff PASS across 24 PR files: ESLint, formatting, policy suppressions, 498 unit tests, 14 released-controller integration tests, 11 component-view tests. Separate editor consumer unit suites: 105 passed. New Cross editor journeys: 2 passed, and both fail when the corresponding margin-mode handoffs are removed; source restored and final gate rerun PASS. codex review --uncommitted exited 0 with no actionable findings. Full-project TypeScript is deferred to remote CI as required by the bounded gate.

## Recipe inheritance

Inherited recipe retains four ACs: Cross picker/label visual proof; actual Cross testnet order plus state/tag mixed proof; provider/flag/market gating and existing Cross position unit state proof. Prior evidence is head 40cdf2f5bce on mm-6, 45/45; it does not cover the new risk-editor fix. Current component-view tests cover that fix. Recipe and node IDs are unchanged.

Capability discovery through the current harness returned ACTION_UNKNOWN for runtime.capability.list. No capability lease is acquired: only the existing authorized iOS slot is needed, not configured android-device. See proof-plan.json.

## Runtime setup and attempts

Launch and doctor passed on mm-2, mini-mm-2, iOS, Metro 8062. The app was at onboarding, so the existing canonical wallet fixture was applied with `fixtures set`. The harness accepts inherited `account_name` but skips account selection, so setup explicitly selected `account=Trading` and confirmed 0x316bde155acd07609872a56bc32ccfb0b13201fa on Hyperliquid testnet before execution. Closed a stray ETH position of 0.0594 with ensure_positions state=none mode=all; the controller asserted flat. No mainnet mutation.

First current-head run is retained in `recipe-run-notifications-blocked`: 32/33 nodes passed, actual BTC position opened, but a first-run notification prompt obscured the screenshots and intercepted native scrolling, leaving the Cross tag offscreen. This is fixture/UI-overlay interference, unrelated to the risk-editor changes. Dismissed the prompt using declared ui.press text=Not now, then reran the unchanged inherited recipe. Its setup converges the leftover BTC before another submission. Diagnostics retain Money Account 403/circuit-breaker errors and SubscriptionController:getBenefits delegation warnings; no risk-editor error.

Recipe re-validation PASS, 45/45 at 2026-10-01T05:21:58.642Z, 113 seconds. Promoted complete current screenshot set and trace from recipe-run, inspected all three images, verified byte equality and staged/source/recipe digests. Teardown closed BTC, asserted flat, cleared both flag overrides. Focused recipe tests passed 40 + 15 + 3. Six diagnostic events are retained as unrelated side findings in recipe-run/diagnostics.json. The device recipe does not enter the new editors; their component-view proof remains separate.

Reviewer comment 4151206075 replied inline in 4152133881 and thread PRRT_kwDOCG4DHc6nx80j resolved successfully. Existing provider-scoping issue 5844369405 was already replied in 5844538507; no duplicate posted. No fresh comments fetched after the single push.

## Remaining scope and proof limits

Production Cross flag remains off. Lite/Reverse reconciliation stays deferred to #36919; Terminal market restrictions stay deferred to TAT-4022. Functional Cross selection, venue locking, parameter routing and new-order risk editors are covered. The original family summary includes layout/responsiveness without measurable criteria; this run provides no general responsiveness measurement, Android proof, or completion claim for those deferrals. family-scope.json therefore records partial-symptom-only.
