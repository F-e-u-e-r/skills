# Plan artifact model & hand-off contract (CANONICAL)

Loaded on demand by `planning` and read by `plan-reconciliation`. **This file is the canonical home for the
logical artifact model; on any disagreement with a quote elsewhere, this file wins.** The *physical* home (a
pathname/format) is deferred to the implementation prototype — this model is independent of where the artifact
lives (architecture O7).

## What a Planning artifact must carry (logical elements)

| element | carries |
|---|---|
| **plan identity** | id · path (kind of work) · depth tier + reason · declared policy parameters (P1–P3) · **authorization marker** (INV-1) |
| **baseline** | the approved, versioned contract (vN) |
| **change history** | append-only record of revisions, approvals, and superseded decisions |
| **current status** | one of: draft · validated · handed off · approved vN · executing · revising · closing · closed |
| **intent & scope** | need + reason · current-state grounding · requirements (stable IDs) · edge/error behaviour · acceptance criteria + scenarios · owned scope / non-scope / expected surfaces · non-goals · constraints with precedence |
| **unknowns register** | **assumption** entries (default adopted, revisited when answered) and **open-question** entries; a recorded default lives **once**, as an assumption linked to its question; P2 decides which a material unknown becomes |
| **decision links** | decision records with lineage + reopen conditions; interface obligations; derivation links to requirements |
| **task / dependency graph** | work items (stable IDs: action · place · constraints) · requirement links · edges + parallel-safety · ordering rationale (P3) · milestone membership · tests-with-the-work |
| **verification requirements** | per item: method + success condition (incl. off-nominal) · evidence to leave · checkpoints · structural-defect model + repair (A4-03) · the validation record |
| **closure reconciliation** | the intended-item list + trace (the closure baseline) → the closure record with dispositions |

## Two trace/record rules (A10 — owned here)

- **A10-01 — bidirectional trace with stable IDs.** Every requirement traces forward to at least one work item,
  and every work item traces back to a requirement. An untraced item either side is an **orphan** — the orphan
  check in `planning` Step 5 (validate) and in `plan-reconciliation` revision revalidation reads this rule.
- **A10-02 — baseline and change history are kept DISTINCT.** The working plan is mutable; the change history and
  decision records are append-only; a superseded decision is marked superseded, never erased (owner rule
  AR-A9-C1). `plan-reconciliation` quotes this verbatim at its trigger; this file is the source it syncs to.

## Hand-off contract (Planning → Ops)

The hand-off is the **approved baseline vN**, readable without the planning conversation (INV-2). Its header
states, verbatim:

> **Execution authorization: NOT GRANTED by this artifact.** (INV-1)

Ops obtains its own grant and consumes the baseline as: intent → done criteria; scope → containment baseline +
tripwire; unknowns → Ops decides whether to proceed under each recorded default and keeps its high-stakes
ambiguity gate; decisions → no silent reversal; work → dispatch-packet content (format/readiness/dispatch stay
D&R §2, and the D&R §2 packet stays self-sufficient for delegations that load no Planning skill); validation →
readiness evidence; closure baseline → what `plan-reconciliation` reconciles.

**Excluded — these stay Ops's, never in the hand-off as Planning's:** wave limits and dispatch-time sequencing;
execution-time stop conditions; evidence recording; authorization; the gate-reality bar and gate proportionality
(GTG).

## Sync

Canonical for the artifact model (A10) and the hand-off contract. The `planning` and `plan-reconciliation` skills
reference these; where either quotes a clause (e.g. AR-A9-C1), this file wins on disagreement. Source: architecture
§5 + §3 (A10 folding). Re-verify element coverage against architecture §5 when that seal advances.
