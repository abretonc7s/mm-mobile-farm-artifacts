# Recipe coverage — TAT-3561

Provenance: inherited family run `bab8b564-684f-4fe9-aa91-77834e8eda33` passed 31/31 nodes. Re-validation on this run was skipped because the prepared iOS app did not expose `__AGENTIC__`.

| ACs | Mode | Evidence | Verdict |
|---|---|---|---|
| TP1–TP3 | mixed | Badge waits/presses, placeholder waits, inherited screenshots | PROVEN |
| TP4, TP6 | state | Focused open-position hook tests | PROVEN |
| TP5, TP7 | mixed | Signed preset/toggle flow, error wait, inherited screenshots | PROVEN |
| TP8 | visual | Inherited default and toggled screenshots | PROVEN |
| SL1–SL3 | mixed | Badge waits/presses, placeholder wait, inherited screenshots | PROVEN |
| SL4 | state | Focused typed-trigger hook test | PROVEN |
| SL5, SL7 | mixed | Signed preset/toggle flow, error wait, inherited screenshots | PROVEN |
| SL6 | state | Focused open-position hook test now covers an accepted `+99%` SL at the maximum 1x boundary | PROVEN |
| SL8 | visual | Inherited default and toggled screenshots | PROVEN |

Overall inherited coverage: 16/16 derived ACs proven. The review fix's exact positive-SL boundary is additionally covered by `tpslValidation.test.ts` for long and short calculations and by `usePerpsTPSLForm.test.ts` for valid form state.
