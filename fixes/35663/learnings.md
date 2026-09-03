# Learnings — PR #35663 review round

Five REAL comments, zero false positives. The reviewer caught real gaps that unit tests, lint,
and a 26/26 recipe pass all missed, because each one is a domain-correctness question that
green checks cannot answer.

- **A passing recipe proves the copy renders, not that the threshold is right.** The original
  strict `>` / `<` comparison warned correctly for every price the recipe typed, so all 26 nodes
  passed while an endpoint resting exactly at best ask — a genuine taker fill on Hyperliquid —
  was silently treated as resting. Boundary values are exactly what a UI recipe never types.
  When a change hinges on an inequality, write the at-the-boundary unit test before trusting
  end-to-end proof.

- **A fallback that keeps a feature alive can make it lie.** Substituting mid when top-of-book
  had not arrived kept the warning always-available, which reads as robustness. It is not: a long
  between mid and best ask rests on the book, so mid produced a confident wrong answer. Suppressing
  the warning behind `number | undefined` is the better failure mode. Reach for "no answer" over
  "approximate answer" whenever the output is a claim about what will happen to the user's money.

- **Intermediate input states are real states.** Counting crossings before both endpoints parsed
  meant one typed endpoint rendered "part of your order…" when no ladder existed yet. Validation
  helpers on live-typing forms need an explicit not-yet-complete branch, not just valid/invalid.

- **Reusing a shipped string couples you to its wording.** The full-ladder case borrowed
  `limit_price_above_warning`, which says "market order" — wrong for GTC limit rungs, and
  unfixable in place because fifteen locales already ship translations of it. Giving scale its own
  keys was cheaper than a fifteen-locale retranslation. Check the locale blast radius before
  reusing an existing string in a new semantic context.

- **Plumbing added for an unobservable check is a net loss.** The submit-time re-check read the
  same committed snapshot that already produced the price-card message and only wrote a DevLogger
  line, yet it cost three extra fields in the placement snapshot and its dependency array. The
  original PR body already flagged this half of AC 4 as unprovable — that admission should have
  been the signal to cut it before review, not after.
