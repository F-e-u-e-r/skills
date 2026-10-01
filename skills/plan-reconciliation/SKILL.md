---
name: plan-reconciliation
description: "Reconcile an approved plan with reality once execution has started — fires FROM execution, not before it. Use when operational-rigor halts planned work because the plan no longer matches reality (repeated failure, a falsified precondition, or a requirement that cannot be met) and the approved plan must be REVISED; or when all planned work items are done and the plan must be CLOSED before completion is claimed. Keeps the approved baseline and its change history distinct, routes each revision to the owning layer and propagates it, never silently relaxes a requirement, and at closure reconciles every intended item against the (possibly amended) baseline with evidence — nothing vanishes. Do NOT use to write a plan before execution (planning); to perform the execution-time stop itself or decide authorization/evidence quality (operational-rigor); or for a small task that never had a plan artifact (D0). Reconciling a plan is not authorization to execute the revision."
---

# Plan reconciliation — revise or close an executing plan

Two activation states, both arising *from* execution:
- **Revise (R3):** OR stopped planned work — repeated failure (OR §2 two-failure rule), a falsified precondition,
  or an unmeetable requirement — so the approved plan is wrong and must change.
- **Close (R4):** all planned work items are done; reconcile before the completion claim OR makes.

The **approved baseline + its change history** is one shared model with `planning` (the artifact model is owned by
`planning`: `../planning/references/plan-artifact.md` — it wins on any disagreement). The one rule you cannot miss, quoted
verbatim (sync note: `plan-artifact.md` is canonical):

> **The baseline and the change history are kept distinct: the working plan is mutable; the change history and
> decision records are append-only — a superseded decision is marked superseded, never erased.** (A10-02; owner rule AR-A9-C1)

Invariants from the pack still bind: **INV-1** (reconciling/revising is not authorization to execute — a revised
baseline needs its own grant), **INV-2** (the revised plan and closure record are durable, resumable artifacts),
**INV-3** (reviewer independence, the evidence bar, honest-completion and stop rules stay Ops's at every depth).

## §1 — Baseline & change record

- A change to a baseline is an **explicit, recorded change** (what changed, why, who approved) — never an in-place
  silent rewrite.
- The working plan is mutable; history is append-only (AR-A9-C1, quoted above).

## §2 — Revise (the plan no longer fits reality)

Trigger: OR has stopped (it owns detection and the stop — OR §2; you do not perform the stop). Then:

1. **Classify by layer** — which layer is wrong: a requirement, a decision, the decomposition, or the ordering?
2. **Revise at the owning layer and PROPAGATE** the change through the dependency/trace links (A9-01, A9-04) — a
   fix at one layer updates everything downstream of it.
3. **Never silently relax a requirement** (A9-05). If a requirement genuinely cannot be met, that is a recorded,
   approved change to the requirement — not a quiet lowering of the bar.
4. **Record the revision scope and why** (which parts of the plan this revision touches). No scope criterion is
   prescribed — state the one you chose.
5. **Revalidate the whole plan — PERFORM the checks now; do not merely ask whether they were done** (A9-06). When
   the revised plan artifact is available, run `planning` Step 5's consistency check AND the orphan check *on it
   yourself*, **surface every defect found** (e.g. a work item left orphaned by a superseded decision), and
   **repair/revise as required**; only a plan that passes this revalidation is ready for re-approval. If the
   revised artifact is not available, obtain it first — asking whether revalidation already happened is not
   revalidation. Plan disturbance is itself a planning consideration (A9-03).
6. **Re-approval → baseline vN+1.** INV-1: the new baseline authorizes nothing; execution resumes only under Ops's
   own grant. *(Whether Ops blocks resume until revalidation is an Ops resume-gate enhancement — backlog, not
   assumed to exist.)*

Supporting seam rules (A9-03, A9-06) are supporting, not core — apply them, do not elevate them to gates.

## §3 — Close (all work items done)

Run before OR's completion claim; OR still owns the honesty of that claim (OR §5).

1. **Does shipped reality legitimately supersede the plan?** If yes, record an **explicit, approved baseline
   change FIRST** (AR-A11-C1) — never reconcile against a stale plan by quietly treating drift as intended.
2. **Reconcile every intended item against the (amended) baseline, with evidence** (A11-03, A11-01), classifying
   each into an explicit delivery state (below).
3. **Both directions:** surface **unrequested work** that was done but not planned (A11-06).
4. **Nothing vanishes:** every undelivered item gets a **recorded disposition** (A11-02). Dropping or waiving an
   item is an **authorized, recorded decision** (A11-05), not a silent omission.
5. Emit the **closure record** (`references/closure-record.md`) → CLOSED.

### The three delivery states (A11; the distinction is load-bearing)

- **delivered** — established *with evidence* as delivered.
- **undelivered** — established *with evidence* as not delivered (missing or partial); a recorded disposition is
  **required**. A *contradicting* item is undelivered **unless** shipped reality legitimately supersedes the plan,
  in which case the explicit approved baseline change (AR-A11-C1) is recorded first and the item is reconciled
  against the amended baseline.
- **NOT VERIFIED** — delivery **cannot be established**. This is an **Ops evidence state**: reported, **never
  counted as delivered**, and it needs **no Planning disposition** (A11-04 is deferred).
  - **"Undelivered" is never inferred from "not counted as delivered."** NOT VERIFIED ≠ undelivered.
  - Evidence *quality* is Ops's call (D&R §3 / OR §4–§5): you record the reconciliation; Ops judges whether an
    item's evidence actually establishes delivery.

## When NOT to use this skill

- Writing a plan before execution → **planning**.
- Performing the execution-time stop, judging evidence quality, deciding authorization, or making the completion
  claim → **operational-rigor / delegation-and-review** (you reconcile the plan; Ops owns execution truth).
- A small task that never produced a plan artifact (D0) → **operational-rigor** inline contract.

## Provenance

Part of the opus-pack (Planning ↔ Ops). Planning Pack Architecture v1: §3 `plan-reconciliation` (11 doctrines) +
§6 lifecycle (revise/close, three delivery states) + owner rules AR-A9-C1 / AR-A11-C1. A9-02 (revision-scope
widening) and A11-04 (Planning disposition for unverifiable items) are **not** doctrine (deferred). Citations to
the Ops siblings (operational-rigor §2/§4/§5, delegation-and-review §3) resolve against those skills as
co-shipped in this pack; re-resolve on install (skill-authoring §6). The artifact model is canonical in
`planning`'s `../planning/references/plan-artifact.md`; the A10-02 clause quoted at the trigger above is kept in
sync with it. **Documented weak-tier limitation:** this skill reliably preserves the revalidation /
re-approval / Ops-authorization gate, but on weaker executor tiers it does not reliably perform absence-sensitive
whole-plan orphan detection itself (prose and forced-record enforcement were both evaluated; neither made it
reliable; the failure mode is fail-safe — under-detection defaults to "cannot resume / escalate"). Retained as an
explicit limitation, not clean coverage. Development/review/adoption history: `references/provenance.md`.
Re-verify: `grep -n '^## ' skills/operational-rigor/SKILL.md`.
