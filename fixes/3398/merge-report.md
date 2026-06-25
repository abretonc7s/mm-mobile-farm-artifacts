# Merge Report — main → TAT-3398-feat-add-roe-sign-toggle

**Merge commit:** `cfaa5f4e5a` (Merge remote-tracking branch 'origin/main')
**Main range merged:** `f0b7a32503..d85e43d259`

## Conflicted files

| File | Resolution | Notes |
| --- | --- | --- |
| `app/components/UI/Perps/hooks/usePerpsTPSLForm.test.ts` | **manual** | Both sides added independent test suites; kept both. |

### usePerpsTPSLForm.test.ts (manual)

Both branch and main appended **new, non-overlapping `describe` blocks** at the
same location in the file, so git interleaved them on shared boilerplate
(`renderHook(...)`, `handleTakeProfitPercentageChange('10')`).

- **Branch (HEAD)** added `describe('RoE sign badge', ...)` — 5 tests covering
  the PR feature (default signs, TP/SL sign toggle, preset chip sign flip, AC6
  negative TP trigger). These are the acceptance-criteria tests for TAT-3398.
- **Main** added `describe('bidirectional sync', ...)` — 6 tests covering
  price↔% auto-compute in both directions plus stale-focus regression.

**Resolution:** kept **both** describe blocks in full, reconstructed as two
separate sibling suites. Neither side's intent is lost — the PR's RoE sign-badge
tests and main's bidirectional-sync tests are independent and both valid.

Auto-merged cleanly (no conflict) in the same area:
`PerpsTPSLView.tsx`, `PerpsTPSLView.test.tsx`, `usePerpsTPSLForm.ts`,
`locales/languages/en.json`.

## Local working-tree changes (not part of merge)

Pre-existing uncommitted dev-only instrumentation was stashed before the merge
and restored afterward (NOT committed):
- `app/components/Nav/App/App.tsx` — `AgentStepHud` (`__DEV__` only)
- `app/core/NavigationService/NavigationService.ts` — `AgenticService.install` (`__DEV__` only)

`AGENTS.md` has a stray single-line prettier whitespace change (linter) left
uncommitted; harmless, unrelated to the merge.

## Risks / manual verification

- The only manual resolution is a **test file** — low risk. Run
  `yarn jest usePerpsTPSLForm` to confirm both suites pass.
- Type check (`yarn lint:tsc`) recommended after merge.
