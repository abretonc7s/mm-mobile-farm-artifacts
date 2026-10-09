# Recipe coverage

Proof run: `recipe-run/`, product `62db857c82c6d9ca58bd79ad94ee95ebfe018772` plus staged test/support-only migration. Recipe SHA-256: `0fd6776d698519bbdc0d9490a1e2ddb3215aa69cb036f9fd73cf9665a6ad3ab5`. Every promoted after-image, recipe and trace matches this one run by SHA-256. The inherited before-image retains its original run scope. No video was produced.

| AC | Proof mode | Evidence | Nodes | Verdict |
|---|---|---|---|---|
| ac1: Cross selectable and selected, form reads Cross | visual | evidence-ac1-cross-sheet.png, evidence-ac1-cross-label.png | ac1-press-cross, ac1-wait-sheet-closed, ac1-wait-cross-label and screenshots | PROVEN |
| ac2: submitted order opens a Cross position | mixed | venue position assertion, evidence-ac2-cross-position.png, command output in recipe-run/trace.json | ac2-press-submit through ac2-wait-cross-tag; ac2-run-order-params-tests | PROVEN |
| ac3: unsupported contexts keep Cross disabled | state | PerpsProOrderFormPanel.view.test.tsx, 24/24 across iOS and Android | ac3-run-gating-tests, ac3-assert-tests-pass | PROVEN |
| ac4: existing Cross position follows its mode and can trade | state | usePerpsProOrderForm existing-cross-position cases, 3/3; new sheet view tests | ac4-run-cross-position-tests, ac4-assert-tests-pass | PROVEN |

The three screenshots were read individually: the label reads Cross; the chooser highlights Cross without Coming soon; the BTC card tags Position margin used as Cross. BTC setup found no position/orders, and teardown asserted BTC flat and cleared feature flag overrides. No pre-existing BTC state was closed. New view coverage also checks position lock release and leverage behavior, separately proven by the bounded gate. Total inherited AC coverage: 4/4 PROVEN.
