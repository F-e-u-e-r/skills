# External harness pilot — record before routing promotion (2026-10-07)

**Class:** human review record + measurement pointer (not pack doctrine).  
**Canonical skills win** on any conflict (`evidence/README.md`).

## Claim this record supports

A **deterministic coding-lane harness** (good/bad fixtures, subprocess child
oracle, multi-lens gates) can ship as **experiment code** without promoting a
new implementation route in a routing map. Pilot scale **N=3/10** tasks is
enough for harness validation, **not** for fleet routing.

## External artifact (not in this repo)

Harness and gates live in
[firaen22/claude-code-technique](https://github.com/firaen22/claude-code-technique)
under `experiments/qwen-splash-local-2026-10-07/` (merged 2026-10-07).

| Item | Outcome |
|------|---------|
| Pilot tasks | c01–c03; Qwen vs codex luna, 6/6 PASS re-grade |
| Build / cross | luna + agy PROCEED; TypeSafe + Qwen review + grok cross PROCEED (cl30) |
| Precommit | gpt-6.1-sol + grok PROCEED (cl24) on grader tree |
| Routing | **Not promoted** — review-only Splash row stays separate; coding row needs N≥10 |

## Pack changes in the companion PR

- `ground-truth-gates`: portable patterns distilled from that grader (marked
  `unprobed` — shape from external harness, not re-benched inside this repo).
- `cross-model-review`: same-model / same-bench confound called explicitly.

## What would change this record

- Held-out N=10 with preregistered null on the same harness.
- A measured implementation win that clears the operator's routing bar.
- Splash or model swap without re-bench.
