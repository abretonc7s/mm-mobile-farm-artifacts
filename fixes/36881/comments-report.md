# PR #36881 review follow-up

The lead feedback is the main work: migrate Cross UI behavior to component view tests through the Perps preset/renderer, remove the replaced shallow unit cases, and update the PR test section. No production change. The user prohibits GitHub comments, replies and thread mutations; checklist step 12 will be recorded as suppressed.

| Source | Author | Comment | Triage | Action |
|---|---|---|---|---|
| review_comment | cursor[bot] | 4110687938, provider position lock | REAL | Already fixed: useHasExistingPosition matches symbol and provider; retain its unit regression tests. |
| review_comment | cursor[bot] | 4132234559, refresh locks picker | FALSE POSITIVE | Pending refresh intentionally fails closed. A previous unlocked answer does not authorize changing mode after orders changed elsewhere; current-request tests specify this behavior. |
| review_comment | geositta | 4151206075, risk editors | REAL | Already fixed in rebased 62db857c82c: typed marginMode suppresses isolated estimates in both editors; retain and extend view coverage. |
| review_comment | cursor[bot] | 4228372196, metadata reload resets pick | OUT OF SCOPE | Valid UX concern about an availability-keyed reset; defer production behavior changes under the lead's explicit test-only scope. Provider changes require fresh restrictions; existing reset remains fail-closed. |
| issue_comment | deeeed | 5844369405, provider metadata | REAL | Already fixed: selected provider scopes getMarkets lookup; retain unit regressions. |
| review | geositta | 5374215622, risk editors | REAL | Same risk-editor request as 4151206075, already fixed; tests remain. |
| lead-feedback | Arthur + Javier Vera | component view test placement | REAL | Add margin/position lock, leverage and form-panel view tests; delete replaced shallow cases. |

Skipped 9 status-only bot issue comments and 5 author updates/fixture commands. No flaky-test-detection finding in the fetched comments. Earlier replies are retained in live-review-comments.json, not duplicated.

Layer placement: new UI journeys belong in component view tests. Engine methods are the allowed boundary; Redux flags and mutable position streams drive behavior. Keep pure orderParams and hook tests and the real provider integration suite. Existing unrelated panel capability contracts and leverage native picker tests are outside this Cross migration.

Planned journeys: choose Cross and return to Isolated; reject the opposite margin mode for Cross and isolated positions; release the picker after a position closes; refresh the venue lock on opening; fail closed during pending reads; gate Cross by flag, Pro mode, provider, HIP-3, Terminal and asset restrictions; submit a Cross order; hide the isolated leverage estimate and keep a position's margin mode while leverage changes.

## Local validation

Bounded check diff PASS: ESLint, formatting, 475 unit tests, 14 integration tests and 47 component view tests across five suites. The three new view suites separately passed 36 tests across iOS and Android via yarn test:view:one. Perps preset unit suite: 4/4. Full-project TypeScript is deferred to CI per checklist. All intentional files are staged.

Inherited recipe ACs: ac1 selectable Cross and selected form label, ac2 actual Cross position plus order parameters, ac3 eligibility gates, ac4 existing Cross position trading. The inherited report records earlier risk-policy and provider-scoping fixes. The recipe command for ac3 references deleted shallow cases and will be updated to the equivalent new view suite without changing node IDs or the UI flow.

## Recipe result

PASS 45/45, 153 seconds, proof run recipe-run. Initial position probe returned CLIENT_NOT_INITIALIZED after restart; recipe setup initialized Perps and found no BTC positions or resting orders. No pre-existing BTC state needed closing. The recipe submitted its $15 testnet BTC trade, tagged Cross, closed it and asserted BTC flat; flag overrides were cleared. All three promoted screenshots were read and their SHA-256 digests match this run. No video produced. Node IDs/UI flow unchanged; the migrated gating command uses the view runner and stale output paths were removed.

Eight non-blocking warning signatures concern selector memoization, Veda protocol schema, Terminal global snapshot 400 and the SubscriptionController:getBenefits messenger. They are not caused by these test-only edits; no production changes made for these diagnostics. One native swipe did not settle within the heuristic window; subsequent exact-label wait and screenshot proved the target.

## GitHub actions

Pushed once with the original-head force-with-lease after verifying the remote had not moved. Commit 4a5de379517. PR description updated with the new view-test section. Step 12 replies and review-thread resolution are suppressed by the latest explicit user instruction. No comment or thread mutation was performed.

## Final result

Total root comments triaged: 19 (3 REAL, 1 FALSE POSITIVE, 15 OUT OF SCOPE). Five are actionable review/conversation comments; fourteen are skipped status/author updates. The CHANGES_REQUESTED review duplicates the risk-editor inline request and was assessed separately. The local lead feedback is REAL and addressed by this commit. No new production fix was required; existing provider and risk-editor fixes were verified.

Fix commit: `4a5de37951724a4c57822ef76704ba54a57d6b1f`. Integration status: rebased onto origin/main `fc73ef0ef2b681e79e53a9b9ea7bef96738ddd0e`. One force-with-lease push completed. Working tree clean.

Files changed:

- `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.test.tsx`
- `app/components/UI/Perps/Views/PerpsProMarketView/components/PerpsProOrderFormPanel.view.test.tsx`
- `app/components/UI/Perps/components/PerpsLeverageBottomSheet/PerpsLeverageBottomSheet.test.tsx`
- `app/components/UI/Perps/components/PerpsLeverageBottomSheet/PerpsLeverageBottomSheet.view.test.tsx`
- `app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.test.tsx`
- `app/components/UI/Perps/components/PerpsMarginModeBottomSheet/PerpsMarginModeBottomSheet.view.test.tsx`
- `tests/component-view/helpers/perpsMarginModeTestHelpers.ts`
- `tests/component-view/presets/perpsStatePreset.ts`
- `tests/component-view/renderers/perpsViewRenderer.tsx`

Validation: bounded gate PASS; 47 view, 475 unit and 14 integration tests, plus 4 preset tests. New view suites individually passed 36/36 across both platforms. Recipe PASS 45/45. No production changes. Full TypeScript is deferred to CI under the checklist. New remote CI runs after the push; this run does not claim that matrix has completed or that the PR has an approving review.

Deferred: the metadata-reload pick reset is a UX concern outside the explicitly authorized test-only migration. Production flag stays off under the existing Lite/Reverse and Terminal safety follow-ups.
