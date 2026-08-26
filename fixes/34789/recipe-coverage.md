# TAT-3742 — recipe coverage self-audit

Promoted from the trusted inherited family evidence package. The current runtime rerun was
blocked by an iOS native-module mismatch, so this remains the latest valid recipe proof.

## Per-AC coverage matrix

| # | Acceptance criterion | Proof mode | Primary evidence | Evidence verdict |
|---|---|---|---|---|
| 1 | At most one non-contradictory funding message after switching to a wallet token | mixed | Before/after screenshots plus focused funding-state tests | PROVEN |
| 2 | The Place Order action remains in the viewport after switching payment methods | visual | Before/after screenshots and presence assertions | PROVEN |
| 3 | An unresolved wallet-token balance never borrows Perps capacity | state | Focused same-source/new-source capacity tests | PROVEN |
| 4 | A resolved below-minimum wallet-token balance states the minimum order size | state | Focused validation test and recipe exit-code assertion | PROVEN |

## Visual delta

The inherited pre-fix capture shows three contradictory funding messages, a disabled slider,
and no Place Order action in the viewport. The inherited post-fix capture shows the
contradictory messages removed, the slider usable, and the Long ETH action present. The
focused state tests cover the timing-dependent unresolved and below-minimum states that are
not deterministic screenshot targets.

## Runner action gap

The inherited audit found that `ui.wait_for expected=visible` cannot measure the relevant
React Native host nodes on this screen. The recipe therefore uses present/absent state
assertions and read screenshots for viewport evidence rather than claiming a false native
visibility measurement.

Overall inherited recipe coverage: 4/4 ACs PROVEN (untestable: 0, weak: 0, missing: 0).
