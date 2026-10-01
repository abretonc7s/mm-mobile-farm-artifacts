# Review learnings

- Buffered Max is a client suggestion. Only the exchange submission limit can establish that nothing is removable. Using buffered zero for the disabled state blocked a valid retained amount on both forms.
- Earlier tests covered a declining positive buffered limit and both limits reaching zero. The reviewer supplied the missing case: buffered Max zero with enough exchange margin for the selected $2. Real stream updates and an assertion on actual updateMargin submission now cover it.
- The inherited live drain left $1 exchange-removable but expected a zero-margin explanation and closed keypad. Recipe expectations can preserve a product bug. Recheck the drain result against the exchange boundary before treating inherited assertions as acceptance criteria.
- Native post-press observations can miss a short success toast. The persistent return to market, reached only after a successful exchange callback, proves acceptance without claiming the toast was captured. Preserve failed runs and document changes to evidence expectations.
- Runtime screenshots prove presentation and state transitions; they cannot establish that an oversized retained amount is valid. Use the component view test for valid retained submission, and keep Extension parity and production Mixpanel outcomes explicit as unverified.
