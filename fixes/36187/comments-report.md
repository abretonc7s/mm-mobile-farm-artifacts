# PR #36187 comment triage

| # | Source | Author | File | Triage | Action |
|---|---|---|---|---|---|
| 1 | `review_comment` | `cursor[bot]` | `app/components/UI/Perps/hooks/usePerpsTPSLForm.ts:615` | REAL | Restrict the stop-loss maximum-loss clamp to negative RoE. The current `Math.abs` check converts a large positive gain-side SL into a loss-side trigger. Add focused utility and hook regressions. |
| 2 | `issue_comment` | `github-actions[bot]` | `app/components/UI/Perps/Views/PerpsTPSLView/PerpsTPSLView.test.tsx:103` | FALSE POSITIVE | No code change. The outer `beforeEach` resets `mockRouteParams` to `defaultRouteParams` at line 189 before every test. |

The REAL finding conflicts directly with TAT-3561: a positive stop-loss RoE must remain positive when converted to a trigger price. The helper currently clamps every stop-loss magnitude at `leverage * 99`, regardless of sign, to a negative value.

Skipped 2 non-actionable comments: one CLA status-only automation comment and one prior author triage/status response that already covers the flaky-test warning and unrelated CI infrastructure failures.

## Inherited recipe coverage

The inherited family run passed 31/31 nodes and covers default TP/SL signs, both toggles, sign-aware placeholders, signed trigger recomputation, preset sign reset, invalid opposite-sign new-order validation, and sign colors. The review fix's accepted `+99%` SL boundary is covered by focused utility and form tests; the inherited recipe exercises the same positive-SL path at `+5%`.

Proof mapping before execution:

| Proof targets | Proof type | Evidence |
|---|---|---|
| `ac-tp1`, `ac-sl1`, `ac-tp2`, `ac-sl2` | mixed | Test-ID waits and presses establish interaction state; screenshots show the rendered signs. |
| `ac-tp3`, `ac-sl3` | mixed | Text waits establish placeholder state; screenshots show the corresponding badge and label. |
| `ac-tp5`, `ac-sl5` | mixed | Preset/sign interactions exercise recomputation; screenshots show magnitude, trigger, and sign together. |
| `ac-tp7`, `ac-sl7` | mixed | Error test-ID waits establish validation state; screenshots show the invalid signed input context. |
| `ac-tp8`, `ac-sl8` | visual | Screenshots show success/error badge colors. |

## Recipe re-validation

SKIPPED — mobile runtime unavailable, skipping recipe re-validation. The React Native target answered without `__AGENTIC__`, so no bridge target matched iOS device `mm-4`; details are in `temp/recipe/runtime/bridge-status.log`. This was not a module-resolution or bundle failure, so no `--clear-metro` retry was permitted. `artifacts/recipe-run` records that environment preflight failure without claiming a recipe execution.

## Responses

- Review comment `4006517083`: replied with fix commit `9d36e251ec` and resolved thread `PRRT_kwDOCG4DHc6iKSOG`.
- Flaky-test issue comment `5666013671`: already replied in top-level comment `5666172060`; no duplicate response posted.

## Final summary

- Total comments: 2 triaged (1 REAL, 1 FALSE POSITIVE, 0 OUT OF SCOPE). Two additional non-actionable comments were skipped.
- Fix commit: `9d36e251ec2502d94ad523a159c3c16884ed6151`
- Files changed:
  - `app/components/UI/Perps/hooks/usePerpsTPSLForm.test.ts`
  - `app/components/UI/Perps/utils/tpslValidation.test.ts`
  - `app/components/UI/Perps/utils/tpslValidation.ts`
- Local validation: changed-file ESLint, `lint:tsc`, and `format:check` passed; 3 focused suites passed with 285 tests.
- Recipe re-validation: SKIPPED (mobile bridge unavailable; `temp/recipe/runtime/bridge-status.log`).
- Integration status: `rebased`.
