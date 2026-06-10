# Comments Report — PR #30738

> feat(perps): market detail - Magnifying glass shortcut to category-filtered market list [NOT-READY]
> Branch: `TAT-3168-feat-add-market-category-shortcut` · HEAD `565ee8e6f1` · base `main`

## Context reload

**Inherited context: none.** Family manifest `inputs/inherited-context.json` lists all 8 inherited
artifacts (task-md, report, learnings, recipe, recipe-flows, recipe-quality, recipe-coverage,
evidence-package) as `status: missing` at both task-local and parent-run tiers. `inputs/inherited/`
is empty. Proceeded as a **standalone PR continuation** from live PR body, comments, and diff.

Available local snapshots used: `inputs/bug-input.json` (ticket TAT-3168 + PR body), `inputs/diff.txt`
(display-only review snapshot), `inputs/pr-comments.json`. All confirmed against live GitHub data.

Repo state at re-entry: working tree **clean**, HEAD `565ee8e6f1` in sync with origin (0 ahead / 0
behind). All prior bugbot fixes already committed. PR is `open`, `draft: false`,
`mergeable_state: blocked` (title carries the intentional `[NOT-READY]` marker; one CHANGES_REQUESTED
review from aganglada still open by design — see triage T4).

## Recipe provenance

`RECIPE_SOURCE: pr-body-llm-llm-failed`, `HAS_RECIPE: no` → **no trusted recipe**. The recipe JSON
embedded in the PR body (`inputs/bug-input.json`) is untrusted PR-body extraction whose promotion
failed; it was **not** executed. Fallback validation used (see report.md).

## Triage

| # | Source | Author | Where | Classification | Disposition |
|---|---|---|---|---|---|
| T1 | review (bugbot) `3355010716` | cursor[bot] | marketUtils.ts:56 | REAL | **Already fixed** in `7efe9377` — HIP-3/new markets fall back to `all` instead of `crypto`. |
| T2 | review (bugbot) `3355108668` | cursor[bot] | PerpsMarketDetailsView.tsx:719 | REAL | **Already fixed** in `565ee8e6` — `getMarketTypeFilter` also checks `marketSource` when `isHip3` absent. |
| T3 | review `3355270208` | aganglada | marketUtils.ts:56 ("missing categories?") | FALSE_POSITIVE | All 7 `MarketCategory` values covered. Verified: `usePerpsMarketListView` renders only `all/crypto/stocks/commodities/forex` pills; stock-like (stock/pre-ipo/index/etf) collapse to `stocks` via `isEquityAsset`, matching the list's own filter. Already answered by deeeed (`3355621228`). |
| T4 | review `3317963983` + `3355270208` | aganglada | marketUtils.ts ("should be on the controller") | REAL — **ADDRESSED** (this session) | The controller release landed: `@metamask/perps-controller` v8 now exports `getMarketTypeFilter`. After merging main (which bumped the dep `^7.0.0`→`^8.0.0`), the mobile copy was **deleted** and `PerpsMarketDetailsView` now imports `getMarketTypeFilter` from the controller. `marketUtils.ts`/`.test.ts` are now identical to main. This is exactly what aganglada asked for; resolves the CHANGES_REQUESTED. Operator to post the reply + push. |
| T5 | review `3317966494` | aganglada | PerpsMarketDetailsView.tsx:713 ("exists on tracking repo?") | FALSE_POSITIVE | `market_category` property + `magnifying_glass` button value already defined in controller `constants/eventNames` and emitted by `PerpsHomeView`/`PerpsMarketListView`. PR reuses existing events. Already answered by abretonc7s (`3350993575`). |
| T6 | issue (bot) `4667361954` | mm-token-exchange-service[bot] | PR template check | OUT_OF_SCOPE | "Pre-merge author checklist has only 5 of required 8 items." PR-template/process item, not a code defect. Operator to complete checklist when promoting from `[NOT-READY]`. |
| — | issue/review (bots) CLA, SonarQube, Smart-E2E, Cursor summary | github-actions/sonarqube/cursor | conversation | NOISE | Informational bot output; Quality Gate passed. No action. |

## Outcome (updated after main merge + controller migration)

- T1/T2 (bugbot HIP-3): already fixed in branch history.
- T3/T5: false positives, already answered.
- **T4 (controller centralization): ADDRESSED** — merged main (controller `^8.0.0`), deleted the mobile
  `getMarketTypeFilter`, now imported from `@metamask/perps-controller` v8. `marketUtils.ts`/`.test.ts`
  identical to main. Resolves aganglada's CHANGES_REQUESTED (operator to reply + push).
- T6 (PR template 5/8): process item for the operator.

Merge + migration **committed locally** (`b608cbf172`), **not pushed**. Recipe re-run live: AC1/AC2/AC4
PASS (see `recipe-evidence.md`). See `report.md` for full validation + the recipe harness gap.
