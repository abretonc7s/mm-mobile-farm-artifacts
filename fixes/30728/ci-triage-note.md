# CI triage — PR #30728 @ 5a095411f8

**Run:** 27283625045 · badCount 3.

## Failures

| Check | Verdict |
|---|---|
| iOS E2E Smoke / `wallet-platform-ios-smoke-2` | **infra/flaky — NOT this PR** |
| `Check all jobs pass` | gate only — fails because the smoke job failed |
| Run Performance Tests / Send Slack Notification | `in_progress` — not a failure, no action |

## Evidence (infra/flaky)

- Failing spec: `tests/smoke/networks/homepage-sections-network-filter.spec.ts` (SmokeWalletPlatform — homepage tokens / network filter). Unrelated feature area.
- Crash: `Signal 11 (SIGSEGV)` in React Native native Fabric renderer — `RCTComponentViewFactory createComponentViewWithComponentHandle` → `RCTComponentViewRegistry` → `RCTMountingManager performTransaction`. Native UI-mounting crash, not JS logic.
- Secondary flake signatures: "login to app after rehydration failed (3 attempts / 50s)", "Assert Login View container should be visible failed (30 attempts)", "Test made 2 unmocked request(s)", `typeText` timeout after 20 attempts.
- This PR only changes a Perps util (`relatedMarkets.ts`) + related perps files, behind `perpsRelatedMarkets` which defaults **off** — not exercised by the wallet-platform smoke suite. `perps`/`relatedMarkets` appears in the log **only** in the CI `CHANGED_FILES` listing, never in a stack trace or test run.

## Rerun

- Attempted `gh run rerun 27283625045 --failed` → blocked: "This workflow is already running" (the Slack-notification job is still `in_progress`; `rerun --failed` requires the run to be completed).
- **Action:** rerun the failed jobs once the run completes (operator or re-attempt), OR push is unnecessary — no code fix required.

## Cursor thread

- 3389061914 (case-sensitive exclusion): **still resolved** (`isResolved: true`), fixed in 5a095411f8.
