# PR #34789 — Review comment report

Branch: `TAT-3742-fix-fix-pay-token-lite-mode`
Integration status (step 3): `rebased` onto `origin/main` (12 commits replayed, no conflicts; `yarn install --immutable` re-run because the rebase moved `package.json`/`yarn.lock`).

## Comments fetched

- Inline review comments (unresolved, top-level): **1** — cursor[bot] on `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:2264`
- General PR-conversation comments from humans: **0** (only CI/status bots: CLA, Smart E2E selection, flaky-test detection, SonarQube quality gate, performance results)
- `CHANGES_REQUESTED` reviews: **0**

## Triage

**Total comments triaged: 1 — 1 REAL, 0 FALSE POSITIVE, 0 OUT OF SCOPE.**

| # | Author | File | Triage | Action |
|---|--------|------|--------|--------|
| 1 | cursor[bot] | app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx:2264 | REAL | Add `hasInsufficientPayTokenBalance` to both Place Order `isDisabled` lists so the button cannot enable during the 300 ms validation debounce after the pay-token balance resolves as too small |

### Comment 1 — "Place order ignores live token shortfall" (Medium)

**Claim, part 1** — while the pay-token balance is unresolved, `effectiveAvailableBalance`
falls through to the Perps balance so validation can report `isValid` for the wrong source.
This half is already covered: `isPayBalanceLoading` (PerpsOrderView.tsx:773) is in both
`isDisabled` lists, so the button is held disabled for the whole unresolved window.

**Claim, part 2 — the real defect.** When the balance resolves as too small,
`isPayBalanceLoading` drops in the same render, but `usePerpsOrderValidation` re-runs behind
`PERFORMANCE_CONFIG.ValidationDebounceMs` (300 ms). During that window `orderValidation.isValid`
is still the stale `true` computed against the Perps balance, and the `isDisabled` list did not
consult `hasInsufficientPayTokenBalance` — so the Place Order button was tappable for ~300 ms
for a trade the live token cannot fund.

`hasInsufficientPayTokenBalance` (PerpsOrderView.tsx:776) is a plain `useMemo` over the same
`spendableBalance` the validation hook uses, so it settles in the same render the balance
resolves in. Adding it to the two `isDisabled` lists closes the window with no new state and no
new source of truth — it is already what the on-screen funding message renders from, so the
button and the message can no longer disagree.

## Fix

Commit: **`27e68e176f5`** — "fix: address review comments on PR #34789"

Files changed:

- `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.tsx` — `hasInsufficientPayTokenBalance` added to both Place Order `isDisabled` lists (the `ButtonSemantic` and `DSButton` A/B variants), plus a comment on the memo stating why it exists next to `orderValidation.isValid`.
- `app/components/UI/Perps/Views/PerpsOrderView/PerpsOrderView.test.tsx` — regression test `disables the place order button while validation still reports the pre-resolution verdict`: validation mocked as the stale `isValid: true`, resolved token balance $3.50 against a $3.67 margin, button must be disabled. Verified it **fails** with the two `isDisabled` lines reverted and passes with them.

## Validation

| Gate | Result |
|---|---|
| Scoped ESLint (changed files) | 0 errors. 7 warnings, all pre-existing — identical set reported with the change stashed (`no-shadow`/`no-deprecated`/`react-compiler`), so `--max-warnings=0` is a baseline condition of these files, not a regression from this fix. |
| `yarn format:check` | pass |
| `yarn lint:tsc` | **not run** — full-project TypeScript is forbidden in worker panes by the repo's standing worker rules; CI is the authoritative signal (`gh pr checks 34789 \| grep lint:tsc`). The change adds one existing `boolean` to a JSX boolean expression and one test using an existing mock. |
| `PerpsOrderView.test.tsx` | 135/135 pass |
| `PerpsOrderView.view.test.tsx` | 4/4 pass (`yarn test:view:one`) |
| Working tree | clean after commit |

## Recipe re-validation — PASS

Inherited recipe (`RECIPE_SOURCE: family-inherited`, 21 nodes) re-run against `branch + origin/main`
after the rebase, with the review fix applied:

- Runner: `mm-harness run … --adapter mobile` → `status: pass`, `exitCode: 0`, no schema migration needed.
- Runtime: `mm-harness status` first reported `liveState: no-bridge`; `mm-harness launch ios --device mm-2 --watcher-port 8072 --verify` brought the bridge up (`Mobile harness verify pass`, fixture READY, 4 accounts). One mid-run `mobile.runtime_recovered` (HUD/CDP transient) — the run recovered and completed.
- Inherited AC coverage, all re-asserted green:
  - **AC1** no Perps-balance warning and no `Available: $0` row after switching to a wallet token (`ui.wait_for … expected: absent`), plus the evidence screenshot `recipe-run/screenshots/evidence-ac1-after-payment-switch.png`.
  - **AC2** place-order button present immediately after the switch and still present once it settles.
  - **AC3 + AC4** unresolved-balance and below-minimum funding states via the `pay with token funding state` Jest block — now **17 passed** (16 inherited + the new regression test), exit 0 asserted by `assert_exit_code`.
- The screenshot also shows the fix does not over-block: a $10 order at 2x paid with ETH keeps the `Long ETH` button enabled and in the viewport with margin $5.06 covered.
- `sideFindings`: 15 app warning/error events observed during the run, relation to the task undetermined; unchanged in character from the inherited run and not caused by the two-line change.

## Non-comment CI observations (informational, not acted on)

- `github-actions[bot]` performance results: 1 non-blocking Android failure
  ("Perps open position and close it" — *Test error*, no assertion detail). Non-blocking by
  policy and not reproducible from the changed files; left for the CI owner.
