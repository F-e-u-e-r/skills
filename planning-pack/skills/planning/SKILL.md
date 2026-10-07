---
name: planning
description: "Produce an executable plan BEFORE building or changing a software/project system — when the user asks for a plan, a spec, a requirements breakdown, a work decomposition, or a design decision; or when operational-rigor classified an ask as plan-first (ambiguous scope, an irreversible or outward action, or a plan was requested). Turns a goal plus the system's real state into a verifiable work contract: testable requirements with acceptance criteria, a dependency-ordered task breakdown with per-item verification, and a hand-off to execution. Do NOT use for a small, clear, low-risk task (operational-rigor's inline task contract covers it — depth D0, below); for personal / career / study / life planning (personal-goal-planning); for picking product direction or priorities when no build contract is being written (product-roadmap); or once execution has started and the plan no longer matches reality, or the work is finished (plan-reconciliation). A planning request authorizes planning only — never execution."
---

# Planning — the executable work contract

You turn *what should we do* into a plan execution can follow: **frame → specify → decide → decompose → validate
→ hand off**. operational-rigor (OR) governs how the work is then *executed*; you stop at the approved plan.

Ops siblings are cited by name + section (resolving against the co-shipped Ops skills): OR = operational-rigor, D&R = delegation-and-review,
GTG = ground-truth-gates, DED = domain-evidence-discipline. References load on demand: `references/plan-artifact.md`
(the artifact model + hand-off contract — the canonical home; it wins on any disagreement), `decision-record.md`,
`policy-parameters.md`.

## Pack invariants — these bind every tier and every artifact (never discounted)

- **INV-1 — a Planning artifact is NOT execution authorization.** A planning request authorizes planning only.
  Carrying out the plan needs its own grant; answering a design question is never consent to act. Every hand-off
  says so, verbatim. (Authorization is Ops-canonical; you stop at the plan and carry no consent forward.)
- **INV-2 — plan state is durable and resumable.** The plan and its progress live in a written artifact a fresh
  session can resume with no conversation memory. Files are state; context is not.
- **INV-3 — depth is proportional; Ops rigor is NOT discounted by depth.** Depth (below) controls *Planning
  artifact* depth only. It never lowers authorization, reviewer independence, the evidence bar, gate truth, stop
  rules, or security rules — those are Ops's at every tier. You may say "this plan is D1"; you may never say
  "therefore self-review is enough."
- **INV-4 — one canonical owner per rule.** Planning *defines* the contract; Ops *enforces* execution of it. You
  reference Ops enforcement compactly; you do not restate Ops doctrine as if you owned it.

## Step 0 — ELIGIBILITY GATE (run before producing anything)

Choose the depth tier from risk, ambiguity, and kind of work, and **record the tier with its reason** in the
plan artifact. Changing the tier later is a recorded change. Also **record the path** — the kind of work selects a
view over the same steps (architecture X-01), not a different skill: **new capability** · **change to existing
behaviour** (specify against what exists) · **defect repair** (verification = reproducing the original symptom;
Ops's gate-reality bar applies) · **direction/roadmap pass** (ends in decisions, A1-06).

| tier | when | you produce |
|---|---|---|
| **D0** | small, clear, low-risk task; no narrower skill dominates | **nothing — STOP and hand back to OR §1's inline task contract.** Do not build a plan artifact; that is the over-engineering INV-3 forbids. |
| **D1** | one unit of work, correctness matters, some unknowns | one compact plan artifact: intent · requirements + acceptance · scope/non-goals · unknowns · work items with verification; validated before hand-off |
| **D2** | several coupled parts, or significant decisions to record | D1 + layered artifacts + decision records for significant choices + validation |
| **D3** | multi-milestone / high-risk / cross-cutting | D2 + milestones with observable ends + full bidirectional trace + named revisit triggers |

If the task is a **red-line** call reserved to a qualified human (medical, legal, financial buy/sell, safety
sign-off), do not dress it as a plan — say so and route to a human. If it is personal/life planning, route to
personal-goal-planning. **These exits precede any plan artifact.**

## Step 1 — Frame (establish the ground, not the solution)

- Establish the **current state from artifacts** (read the code/system), not from assumption.
- A direction/investment pass ends in **decisions**, not a survey.
- Deliberately **surface implicit constraints** — the ones the request leaves unsaid. This is the batch-elicitation
  side of OR §1's grill pass; honor parameter **P1 `elicitation.cadence`** (one-at-a-time vs batch) — do not
  restate OR's grill pass, reference it.

## Step 2 — Specify (the testable contract)

- State the **need, not a pre-chosen solution**; for a change, specify it **against what already exists**.
- Requirements are **testable and binding**, with **stable IDs**; cover **edge and error behaviour**, not just
  the happy path.
- **Acceptance criteria are observable, written before options** (Ops verifies them at execution; no completion
  claim until met).
- **Unknowns register:** every material gap is either an **assumption** (a recorded default, revisited when
  answered) or an **open question** — governed by parameter **P2 `ask_assume.material_with_default`**
  (ask vs assume-and-log). **Floor (never parameterized):** never ask about immaterial gaps; every unasked gap is
  a recorded assumption; a **high-stakes unknown goes to the OR §1 ambiguity gate**, not silently assumed.
- Declare **non-goals**, **owned scope + explicit non-scope + the surfaces you expect to touch**, and
  **precedence** among conflicting requirement sources.

## Step 3 — Decide (record the load-bearing choices)

- Write a **decision record** for each significant choice (significance + template: `references/decision-record.md`):
  what was decided, the rejected alternative, why.
- **Triage what must be decided now** vs deferred; name **interface obligations**; show each design element **traces
  to a requirement** (a trace check, not a ban on design).
- A record that may need revisiting **names its reopen condition** (consumed later by plan-reconciliation).
- **No silent reversal:** the decision lineage is append-only; a superseded decision is marked superseded, never
  erased (Ops enforces non-reversal during execution).
- **Element admission is Ops's, not yours:** whether an executor may invent an abstraction/optimization/flexibility
  is OR §2/§5's call. Plan-level over-building is a known gap — do not add ceremony the request does not need.

## Step 4 — Decompose & sequence

- **Vertical, independently testable increments**; each a **self-contained, startable task** (action · place ·
  constraints · requirement links); **tests land with their work**.
- **Structural-defect model + repair (A4-03):** name the defects that make the decomposition unexecutable — a
  non-independently-testable increment, a circular or unnamed dependency — and the repair. A structural defect
  **stops dispatch until repaired** (you define the model + repair; Ops owns the no-dispatch enforcement).
- **Dependency graph + explicit order**, dependencies first; apply parameter **P3 `ordering.priority_policy`**
  (risk-first vs value-first vs declared-other) *after* hard dependencies, with a stated reason — no universal
  winner.
- **Milestones with an observable end** (D3); **checkpoints between dependent steps**; name the **evidence each
  item must leave**.
- **Per item: the verification method + its success condition, including off-nominal** — this is the *content* of
  the proof gate. The **gate-reality bar** ("would it fail under the broken behaviour?"), gate proportionality,
  and repair reproduction are **GTG's / Ops's**, enforced at execution — you supply what is checked, not whether
  the gate is real.

## Step 5 — Validate (whole-plan, before hand-off)

- Review the whole plan for **constraint consistency and what is missing**: run the structural-defect check and
  the **orphan check** (every requirement traces to a task and back — `references/plan-artifact.md`).
- **Reviewer independence is Ops's, at every tier (INV-3, D&R §3).** A D1 plan does not earn self-review. Quote,
  do not paraphrase, D&R §3's rule verbatim where it fires: *"The author is not the judge."*

## Step 6 — Hand off & STOP

- Emit the **approved baseline vN**, readable without the planning conversation (INV-2). Its header states,
  verbatim: **"Execution authorization: NOT GRANTED by this artifact."** (INV-1) — Ops obtains its own grant.
- **Dispatch-packet mapping** (you supply content; D&R §2 keeps the packet *format*, readiness refusal, dispatch,
  and the self-sufficiency of packets that load no Planning skill):

  | packet field (D&R §2) | filled from your plan |
  |---|---|
  | goal + motivation | requirement + need |
  | owned scope / non-scope | scope |
  | invariant | constraints + acceptance |
  | proof gate | what is checked + success condition |
  | interfaces | interface obligations (Step 3) |
  | edge behaviour | edge/error spec (Step 2) |

- Hand Ops: intent → done criteria; scope → containment baseline + tripwire; unknowns → Ops decides whether to
  proceed under each default and keeps its high-stakes ambiguity gate; decisions → no silent reversal; work →
  packet content; validation → readiness evidence; closure baseline → what plan-reconciliation will reconcile.
- **Then STOP.** Do not execute, gate, authorize, record evidence, or claim completion — those are Ops's. Once
  execution starts and reality diverges, or the work finishes, control passes to **plan-reconciliation**.

## When NOT to use this skill

- Small, clear, low-risk task → **OR §1** inline task contract (D0; building a plan artifact here is the
  over-engineering INV-3 forbids).
- Personal / career / study / life goals → **personal-goal-planning**.
- Product direction / prioritization with no build contract being written → **product-roadmap**.
- Execution has begun and the plan no longer matches reality, or the work is done → **plan-reconciliation**.
- Executing, gating, authorizing, recording evidence, claiming completion → **operational-rigor / delegation-and-review**.

## Doctrine parameters (no hidden defaults — `references/policy-parameters.md`)

P1 `elicitation.cadence` ∈ {one-at-a-time, batch} · P2 `ask_assume.material_with_default` ∈ {ask, assume-and-log}
· P3 `ordering.priority_policy` ∈ {risk-first, value-first, declared-other}. Each plan **sets its parameters with
a reason**; skill text carries no default.

## Provenance

Part of the planning-pack (Planning ↔ Ops). Planning Pack Architecture v1: §3 `planning` (37 doctrines) + §4 depth +
§5 artifact/hand-off + §7 parameters + §2 invariants. Citations to the Ops siblings (operational-rigor §1–§6,
delegation-and-review §2/§3, ground-truth-gates, domain-evidence-discipline) resolve against those skills as
co-shipped in this pack; re-resolve on install (skill-authoring §6). Development history, the fresh-context
review record, and the adoption-evidence summary are in `references/provenance.md`.
Re-verify sibling section anchors: `grep -n '^## ' ops-pack/skills/{operational-rigor,delegation-and-review}/SKILL.md`.
