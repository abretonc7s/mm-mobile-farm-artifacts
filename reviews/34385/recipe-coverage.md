# Recipe Coverage

Skipped (tier: light). The operator prohibited creating or executing a review recipe and all device/browser evidence work.

| # | Review claim | Target platform | Recipe nodes | Screenshot | Visual verdict | Justification |
|---|---|---|---|---|---|---|
| 1 | Then an "Order submitted" toast appears and the ETH position opens | both | skipped | none | UNTESTABLE | Requires funded live Perps state and device interaction, which were prohibited for this review. |
| 2 | Then the order rests and appears in open orders | both | skipped | none | UNTESTABLE | Requires live limit-order placement and venue state, which were prohibited for this review. |
| 3 | Then the position keeps its take profit and stop loss and remains open | both | skipped | none | UNTESTABLE | Requires a live position and Auto close mutation, which were prohibited for this review. |
| 4 | Then the position is closed and no longer listed | both | skipped | none | UNTESTABLE | Requires a live position close flow, which was prohibited for this review. |

Overall recipe coverage: 0/4 ACs PROVEN (untestable: 1, 2, 3, 4; weak: 0, missing: 0)
