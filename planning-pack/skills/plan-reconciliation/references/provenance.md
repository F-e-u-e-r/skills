# plan-reconciliation · references: provenance

Historical development, review, and adoption-evidence records for the `plan-reconciliation` skill. The canonical
rules live in `SKILL.md`; this file is history and an evidence summary only.

## Origin

Distilled from Planning Pack Architecture v1 (owner-sealed 2026-09-30): §3 `plan-reconciliation` (11 folded
doctrines), §6 lifecycle (revise / close, the three delivery states), owner rules AR-A9-C1 (the baseline is kept
distinct from an append-only change history) and AR-A11-C1 (closure-time plan correction before reconciling). The
closure-record template is in `references/closure-record.md`; the artifact model is canonical in `planning`'s
`../planning/references/plan-artifact.md`.

## Review

Fresh-context review (2026-10-01) → ADOPT-WITH-FIXES; the quote label was unified to "A10-02; owner rule AR-A9-C1"
against the canonical artifact model.

## Documented weak-tier limitation

`plan-reconciliation` reliably preserves the revalidation / re-approval / Ops-authorization gate: on a revised
plan it refuses to recommend resuming execution, requires re-approval of the revised baseline and a **separate**
Ops execution grant, and does not self-approve the baseline or self-authorize execution (INV-1). However, on the
weaker executor tier tested it does **not** reliably PERFORM absence-sensitive whole-plan orphan detection itself —
it tends to describe or request the revalidation rather than carrying it out. Two enforcement forms were evaluated
(an imperative prose repair and a forced structured-record escalation); neither made the behaviour reliable. The
failure mode is **fail-safe**: under-detection defaults to "cannot resume / escalate", never a false "safe to
resume". The system therefore retains this as an explicit v1 limitation rather than claiming clean behavioural
coverage.

Overall adoption: Planning Pack v1 = **QUALIFIED-ADOPTABLE · 13/14 clean behavioural claims · 1 documented
weak-tier limitation · 0 harmful · D0 preserved.**

## Re-verify

Citations resolve against the co-shipped Ops skills; re-check their section anchors with
`grep -n '^## ' ops-pack/skills/operational-rigor/SKILL.md`.
