# Policy parameters — the deferred conflicts, declared not defaulted

Loaded on demand by `planning`. The architecture deferred several genuine conflicts rather than pick a winner.
**Rule (architecture §7): each appears either as a declared plan parameter the plan must SET WITH ITS REASON, or
as an owner-set architecture rule labelled as such. Skill text never carries a hidden default.** Every plan
records its P1–P3 values in the plan-identity block (`plan-artifact.md`).

## P1 — `elicitation.cadence` ∈ {one-at-a-time, batch}

How questions are put to the user during framing/specification. Set by the planning mode. Side "batch" **is** the
operational-rigor §1 grill pass (referenced, never restated here). No universal winner.

## P2 — `ask_assume.material_with_default` ∈ {ask, assume-and-log}

For a **material** unknown that has a plausible default: ask the user, or adopt-and-log the default as an
assumption. Applied identically at both the elicitation stage and the open-question stage (one policy, not
resolved twice).

**Floor — doctrine, NOT parameterized (always holds whatever P2 is set to):**
- Never ask about an **immaterial** gap.
- **Every unasked gap becomes a recorded assumption** (never a silent guess).
- A **high-stakes unknown goes to the operational-rigor §1 ambiguity gate** — it is not assumed away by P2.

## P3 — `ordering.priority_policy` ∈ {risk-first, value-first, declared-other}

How independent work is ordered **after** hard dependencies are satisfied (dependencies always come first —
A5-03). State the reason for the chosen policy. No universal winner between risk-first and value-first.

## Owner-set architecture rules (labelled as rules, not parameters, not doctrine)

- **AR-A9-C1** — working plan mutable; change history + decision records append-only; superseded marked, never
  erased. (Canonical in `plan-artifact.md`.)
- **AR-A11-C1** — closure-time plan correction: if shipped reality legitimately supersedes the plan, record an
  explicit approved baseline change **first**, then reconcile against the amended baseline. (Used by
  `plan-reconciliation` §3.)

## Still open (no criterion prescribed)

- **A9-C2** revision-scope criterion: each revision records the scope it chose and why; no criterion is imposed
  (a candidate is deferred to a future evaluation).

Source: architecture §7 + §6. On disagreement about records/baseline semantics, `plan-artifact.md` wins.
