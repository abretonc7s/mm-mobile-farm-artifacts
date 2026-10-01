# Review comment resolution

Completed and pushed `8178666ec8b64f9ec090db0e6ced7331d088b105` to PR #36775. Total actionable comments: 3, comprising 2 REAL, 0 FALSE POSITIVE, 1 OUT OF SCOPE. One REAL finding was already fixed and replied to in the inherited branch; one REAL finding was fixed in this run. Three routine status comments and two prior author replies were inspected and excluded from actionable counts. CHANGES_REQUESTED review 5374271235 duplicates the human inline finding.

Integration status: `rebased`. Remote lease check passed and force-with-lease push succeeded. Pre-commit Prettier and ESLint passed after an approximately ten-minute ESLint run. The committed tree exactly matches tested tree `064e9e782a4eeb4f2847f1788629a00bec6dd732`. No leftover lint changes or stash needed. Remote CI and full TypeScript are deferred to CI and are not claimed passed. No new review comments fetched after the push, as required by the single-pass checklist.

Files changed in the review-fix commit:

- `app/components/UI/Perps/Views/PerpsAdjustMarginView/PerpsAdjustMarginView.tsx`
- `app/components/UI/Perps/components/PerpsAdjustMarginBottomSheet/PerpsAdjustMarginBottomSheet.tsx`
- `app/components/UI/Perps/Views/PerpsAdjustMarginView/PerpsAdjustMarginView.view.test.tsx`

Local validation PASS: changed-file ESLint, Prettier and suppression checks; 7 unit suites with 245 tests; 2 component view suites with 7 tests. Live recipe re-validation PASS 104/104 in `recipe-run-2`. Current evidence is retained only from this final proof run and hashed in `evidence-provenance.json`.

Human inline reply: https://github.com/MetaMask/metamask-mobile/pull/36775#discussion_r4152625837. Thread `PRRT_kwDOCG4DHc6nyECx` resolved successfully. Consolidated performance triage reply: https://github.com/MetaMask/metamask-mobile/pull/36775#issuecomment-5926300065. Historical Cursor thread was already replied and resolved; no duplicate sent.

Family scope remains partial for the original Mobile + Extension ticket: all actionable Mobile review findings are handled; Extension parity and post-release Mixpanel <=14% remain unverified. These limits are recorded in `family-scope.json` and `recipe-coverage.md`.

Review snapshot fetched once before fixes. Three status-only conversation comments skipped without reply: CLA, Smart E2E selection, and Sonar quality summary. One resolved Cursor thread already fixed by the inherited branch; no duplicate reply planned. No flaky-test detection comment was present.

| # | Source | Author | File | Triage | Action |
|---|--------|--------|------|--------|--------|
| 1 | review_comment 4151252455 | geositta | PerpsAdjustMarginView.tsx:155 and bottom sheet | REAL | Derive the zero-removable state from submitLimitAmount; cover retained $2 with buffered Max zero and exchange limit $9.30 on both forms. |
| 2 | issue_comment 5830656003 | github-actions[bot] | Performance run 36118599225 | OUT OF SCOPE | Reports non-blocking add-funds and open/close-position timeouts on historical commit 99ea0b2. Those flows do not execute remove-margin preflight or these form guards. No diagnosis or margin regression is established by this timeout summary. |
| 3 | resolved review_comment 4091373443 | cursor[bot] | PerpsAdjustMarginView.tsx | REAL, already fixed | Inherited usePerpsFreshRemovalLimit keys release to size, entry, leverage and collateral, with a 10s hold. PnL re-deliveries are covered by existing hook tests. Thread already resolved and replied. |

The CHANGES_REQUESTED review 5374271235 repeats item 1. It is covered by the same inline reply and fix.

## Context and scope

Read the PR description, full diff, ticket text in TASK.md, and docs/perps/hyperliquid/margining.md. The ticket requires live removable limits, a truthful zero state, and pre-submit revalidation. The review example matches the implementation: $1,000 notional/$112 margin at 10x offers $2; after a $3 loss, $997/$109 offers zero but the exchange still accepts $9.30. The current zero state incorrectly blocks a retained $2. Max/slider remain buffered; submission and the no-removable explanation must use the exchange limit after any fresh cap.

Extension parity and post-release Mixpanel <=14% are original ticket outcomes that this Mobile PR cannot prove. Cross-margin/Lite/Reverse work is deferred to #36881/#36919 by the PR description and is not expanded in this run.

## Local review and validation notes

Self-review retained the existing component view scenarios and added a shared scenario for both forms. Real stream updates drive the calculations; the test waits for offered Max to show $0 before checking Confirm and submission of the retained $2. Initial assertion failures expected decimal formatting that the app does not display; changed assertions to match the real $2/$0 copy.

Prettier passed. The best-effort ESLint autofix was stopped to avoid duplicating the required type-aware lint gate; required changed-file ESLint passed. Full-project TypeScript is deferred to remote CI as directed by the bounded gate.

Attempted `yarn skills --include testing/mobile-testing --save`; the catalog skipped mobile-testing because its source skill.md was missing. Used the canonical docs/testing/component-view-tests.md and testing-layers.md from the skills source.

Independent Claude review was attempted with `claude --print --dangerously-skip-permissions` against HEAD 80944eaf25 plus the local diff. It returned no verdict after more than ten minutes and was terminated. No Claude approval is claimed.

## Inherited recipe criteria correction

Read inputs/inherited-context.json, inputs/inherited/report.md and the 98-node inherited recipe. AC1 proves real Max acceptance, AC2 a fresh zero-margin position, AC3 pre-submit tests, AC4/AC5 previously expected a zero explanation after draining to roughly $1 of positive exchange margin. That AC4/AC5 expectation is the regression geositta reported, not a valid zero-exchange test. Updated only their keypad/zero-explanation expectations and evidence captions to the corrected behavior, preserving node IDs, transitions, UI test IDs, setup, screenshots and exchange mutations. The inherited graph is retained, not recreated. Original saved as recipe.inherited.json.

Restored the explicitly referenced drain-btc-margin.sh byte-for-byte from the parent task artifacts at its inherited repository-relative path. It remains a task-owned Hyperliquid testnet operation. No physical capability acquired; runtime-proof-plan.json scopes proof to mmdev-6/8066.

Session setup PASS confirmed the task-owned Trading account on Hyperliquid testnet. Initial read before setup returned CLIENT_NOT_INITIALIZED; after setup read_positions PASS returned zero positions. No stray positions were closed. The inherited setup will establish BTC and SOL prerequisites. An early concurrent setup attempt was refused by SANDBOX_BUSY; subsequent operations are sequential.

First live run: FAIL 20/21 at setup-assert-added, a brief add-margin toast was already absent after native post-press observations. The Confirm trace shows return to PerpsMarketDetails and margin $103 after a ~$83 entry plus the $20 addition. Add-mode behavior is unaffected by this review fix; source calls onSuccess/navigation.goBack only when updateMargin returns success. Five non-blocking diagnostic findings concerned Money Account 403/circuit breakers and Terminal snapshot 400, unrelated to remove margin.

The public run CLI offers no observation-disable flag. Updated the four transient success-toast waits to require the persistent visible market Close button reached after the exchange success callback. Preserved all node IDs, transitions, trades, amounts and exchange acceptance intent. No live toast-visibility claim is made; the focused toast tests still cover its configuration. The first failing run is retained as recipe-run-first-failed; rerun uses recipe-run-2.

## Final runtime proof

Recipe re-validation PASS 104/104 in recipe-run-2, 484343ms, on the rebased staged product tree recorded in tested-tree-sha.txt. Actual Max $37.07 submitted successfully. Fresh SOL zero state explained and disabled. Full-screen and bottom-sheet drains left exactly $1 exchange-removable; keypad stayed visible and no false zero explanation appeared. Retained amounts in those screenshots exceed $1, so actual retained valid $2 submission is proven separately by the new real-stream component view tests. All five final screenshots opened and visually reviewed. No video or earlier media promoted as current proof. Root recipe matches run bytes; evidence-provenance hashes every final-run artifact and resolved dependency. See recipe-coverage.md for provenance and limits.

SOL teardown and flag clear passed. BTC remains as the inherited fixture intended. Five nonblocking Money Account/Terminal diagnostics reviewed as unrelated. Full local gate PASS: 7 unit suites/245 tests and 2 component view suites/7 tests, with lint, format and suppression checks passed. Remote full TypeScript and CI remain pending.

Final contract packaging correction: `recipe-run/` is a byte-identical promoted copy of the identified `recipe-run-2/` passing proof. Every copied file was compared byte for byte. The failed first run is preserved in `recipe-run-first-failed/`. `evidence-manifest.json` contains the required presentation schema; `evidence-provenance.json` holds all run hashes, product/tree revisions, media review notes and proof limits. No product code or proof bytes changed.
