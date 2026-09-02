# Learnings

- A one-at-a-time network mutation can still have multiple accepted outcomes awaiting reconciliation; the in-flight lock and post-success stale-row guards have different cardinality.
- Post-success guards should be keyed by stable provider/order identity and pruned independently when each schedule becomes terminal.
- Regression coverage needs sequential successful cancellations plus a partial terminal update; a single accepted-order component test cannot expose replacement of earlier state.
- Review-thread resolution is not sufficient code evidence. Re-reading the current state model confirmed the reported behavior still existed at HEAD.
- Runtime selector assertions passed, but the inherited screenshot framed the order form instead of the management panel; evidence framing should be checked independently of runner status.
