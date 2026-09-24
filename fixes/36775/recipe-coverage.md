# Recipe coverage — TAT-3985 (#36775 after split)

Source: `artifacts/recipe.json`, run `artifacts/recipe-run/` (48/48 PASS, provenance head bb56c3435cf). Cross-margin ACs (5–7) moved with the code to #36782; proven by `artifacts/cross-split/recipe.json`, run `artifacts/cross-split/recipe-run/` (30/30 PASS, head 9d5f5879753).

| # | AC | Proof mode | Recipe nodes | Visual | Verdict | Justification |
|---|----|------------|--------------|--------|---------|---------------|
| 1 | Max removable is derived from live state and always accepted by the exchange | mixed | ac1-press-max, ac1-wait-available, ac1-screenshot-max-form, ac1-press-confirm, ac1-assert-removed, ac1-screenshot-removed, ac1-assert-no-rejection | recipe-run/screenshots/evidence-ac1-max-form.png, evidence-ac1-removed-toast.png | PROVEN | Offered Max submitted; "Removed $" toast visible; "Margin adjustment failed" asserted absent. |
| 2 | Zero removable disables the control with an explanation | visual | setup-sol-open, ac2-press-remove, ac2-assert-explanation, ac2-screenshot-zero-state | recipe-run/screenshots/evidence-ac2-zero-state.png | PROVEN | `perps-adjust-margin-no-removable-margin` visible on a fresh isolated SOL position. |
| 3 | Position change between open and submit is re-validated; user told the amount changed | state | ac3-run-unit-tests, ac3-assert-tests-pass | — | PROVEN (shrink), PARTIAL (closed) | Hook tests: shrunk position stops with amount-changed toast and new safe max; forms cap Max/slider at the fresh limit until the stream pushes a newer position. A position missing from the fresh read is no longer blocked client-side because the provider returns [] on fetch errors too; the exchange's translated error covers a truly closed position. Live partial fill/liquidation cannot be forced on testnet. |
| 4 | remove_margin failure rate ≤14% in Mixpanel post-release | state | — | — | UNTESTABLE | Needs production traffic on a shipped build. |
| 5–7 | Cross margin order placement, Lite Cross trading, Flip hidden for Cross | — | moved to #36782 | cross-split/recipe-run/screenshots | N/A here | Split out for the 1000-line limit; PASS 30/30 on #36782's branch. |

Overall (#36775): 2/4 PROVEN, 1 PROVEN with a documented partial, 1 UNTESTABLE.
