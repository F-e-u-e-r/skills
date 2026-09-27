# HCSA1-A DESIGN v1.1 Amendment

**Status:** DESIGN ONLY / FREEZE CANDIDATE. This document governs its amended clauses only
once an owner freeze gate records this version; it authorizes no build, packet repair,
labeling, or execution on its own.

## Relationship to v1.0 (immutable)

v1.0 remains immutable and canonical. Do not edit either v1.0 file.

```
v1.0 DESIGN.md        sha256 842e55b0e9ae314717c2ad963396f15ac5ea29277311fe205ebd5f3d54e7492d
v1.0 PHASE0-RECON.md  sha256 6f368f47f1069a168da41458a89d2eb00745cae2593b565fc20817a5d5ca81fa
```

This amendment supersedes v1.0 **only for the specific clauses amended in sections A, B,
and C below**. Every other v1.0 clause remains governing. Until this amendment passes a new
owner freeze gate, **v1.0 remains the current frozen contract** (superseded-in-part pending
v1.1).

## Trigger / provenance

v1.1 exists because the DEVELOPMENT-only Item 4A model-proxy diagnostic and the Item 4A-T
disagreement triage exposed load-bearing target-definition ambiguity **before** any human
ground-truth labeling was spent. This is the intended function of development/calibration.

- Item 4A model-proxy labels are NOT ground truth and are not cited as such here.
- The triage classified 8 cross-family disagreements by root cause **without producing final
  labels**: `repetition_state` boundary ambiguity (L3, load-bearing); `evidence_progress`
  across a COMPACTION boundary undefined (L3, load-bearing); `evidence_progress` on
  repeated/confirmatory negative observation = **L3-or-L2 unresolved under v1.0** (v1.0 never
  operationalized when a repeated observation counts as new decision-relevant evidence, and
  the packet may also lack the discriminating context); two labeler over-readings (L1); two
  legitimately underdetermined sparse-real cases where `uncertain` is appropriate (L5); zero
  sanitization-loss cases (L4 — ruled out by raw check).
- The correction that `evidence_progress` on repeated evidence is NOT purely L2 is recorded:
  the "same-conditions vs changed-conditions" phrasing used during triage was owner
  diagnostic commentary, not v1.0 normative text, and is not treated as v1.0 contract.

## Amendment A — `repetition_state` operational boundary

Supersedes the v1.0 §6 `repetition_state` domain gloss (values unchanged; their operational
meaning is defined here). Repetition is assessed by first identifying a **relevant
recurrence**, then judging progress across it — NOT by requiring an operation and its result
to be jointly equivalent.

**Relevant recurrence** exists when one or more of these recur:

- the same or an equivalent operation on the same or an equivalent task object / goal;
- the same or an equivalent decision-relevant evidence state (this can recur even across
  different operations — e.g. a `grep` then a `Read` that re-fetch the same evidence);
- the same or an equivalent observable task / decision state;
- the same multi-step state pattern.

But **the same tool verb alone is not a recurrence** — `Read A; Read B; Read C` is not a
recurrence merely because all use `Read` (distinct objects, distinct evidence).

Values (relevant recurrence + progress):

- `none` — no relevant recurrence.
- `productive_repeat` — a relevant recurrence exists, but it produces decision-relevant
  progress or advances the unresolved observable task state (example: re-running the same test
  after a code change — the operation/target recur, yet the evidence state legitimately
  changes and/or a real task-state transition is verified).
- `stalled_repeat` — a **non-cyclic** relevant recurrence exists, with no decision-relevant
  progress and no task-state advance under the frozen observable context.
- `cyclic` — a multi-step pattern returns to materially the same observable task / evidence
  state across repeated cycles, without net decision-relevant progress. (A normal
  `edit -> test -> inspect` loop that advances each round is NOT cyclic; the guard is
  "returns to materially the same state without net progress," not "a sequence ran twice.")

**Precedence (mutually exclusive):** when the `cyclic` definition applies, classify as
`cyclic`, not `stalled_repeat`. `stalled_repeat` covers only the non-cyclic single / local
no-progress recurrence; `cyclic` covers the repeating multi-step no-net-progress loop. This
keeps the two values disjoint under the single `repetition_state` label.
- `uncertain` — recurrence and/or progress cannot be established from the observables.

Traps avoided (explicit): the definition must NOT reduce to "same target = repetition,
different target = not" (too syntactic — the same test re-run before vs after a fix has an
identical target yet is productive verification); and it must NOT require operation and result
to be **jointly** equivalent (that would misclassify a FAIL -> PASS after a fix as `none`).

Relation to Amendment B: a recurrence with the **same** outcome can still be
`productive_repeat` when it supplies the discriminating information an unresolved proposition
needs (e.g. same test, same FAIL, resolving "is this reproducible?" -> a relevant recurrence
exists, evidence_progress may be positive, and repetition_state = `productive_repeat`).
Repetition is not equated with waste. `repetition_state` and `evidence_progress` remain
distinct judgments (recurrence structure vs marginal information) and are not merged.

Purpose: prevent a future governor from suppressing productive work — especially productive
verification — merely because operations or action categories recur.

## Amendment B — `evidence_progress` for repeated / confirmatory evidence

Supersedes/extends the v1.0 §7 decision-relevant-evidence definition for the repeated-
observation case (the governing question is unchanged; its application to repeats is
operationalized here).

Governing question (v1.0 §7, unchanged): does the new observation **change, strengthen,
weaken, or close** a task-relevant unresolved proposition / admissible decision / required
gate.

Operationalization for repeated observations (esp. repeated failures):

- The classification depends on whether the observation supplies the **discriminating
  information the currently-unresolved proposition needs** — NOT on outcome-sameness and NOT
  on observation-count.
- A repeated observation with the **same outcome CAN be new evidence** if the unresolved
  proposition is about reproducibility/confirmation (e.g., proposition = "is this failure
  reproducible?"; a second same-conditions failure resolves it -> `new_supporting` or
  `new_load_bearing`).
- A repeated observation is `none` when it merely re-observes an already-established fact that
  no currently-unresolved proposition depends on.
- Forbidden defaults: do NOT assume "same outcome = no new evidence"; do NOT assume "another
  observation = new evidence."

Required observable context: to classify a repeated observation, the window must make
explicit **what unresolved proposition / uncertainty this observation tests** — not merely a
comparison of command/environment hashes. This makes v1.0 §7's per-window observable context
(`task_ref` / `open_propositions` / `decision_state`) load-bearing for repeated-evidence
labeling.

If that required context is **absent** from the observable surface, `uncertain` remains
available and must not be forced to `none` or to a positive evidence label.

**Provenance rule (fail-closed) for the observable context.** `task_ref`,
`open_propositions`, and `decision_state` may be populated ONLY from prefix-visible authorized
observables. It is forbidden to populate them from: construction intent, `target_side`,
construction rationale, model-proxy labels, suffix outcome, private chain-of-thought, or any
author knowledge not present in the prefix observables. For a constructed fixture, if the
labeler is meant to know (for example) that the task tests whether a failure is reproducible,
that must itself appear in the constructed prefix's observable task / message (e.g. the user
task or a visible plan) — never injected from a private sidecar field. If the prefix
observables are insufficient to establish a proposition, do NOT manufacture one: leave the
context unresolved and `uncertain` remains valid. Faithful normalization / paraphrase is
allowed, but each populated `open_proposition` must be provenance-linked (grounded in prefix
observable span / event ids) so it can be mechanically audited as carrying no label leakage.

## Amendment C — `evidence_progress` window across COMPACTION

Supersedes the gap left by v1.0 §3/§5: v1.0 defines COMPACTION as a repetition discontinuity
but is silent on how the window `W(t) = (previous decision anchor, t]` interacts with a
`context_boundary = COMPACTION` inside it.

**Selected rule: ANNOTATE-and-classify (not reset, not silent-clip).**

- The window is **not reset** by COMPACTION: pre-compaction evidence remains established task
  evidence within W(t). *(invariant: pre-compaction evidence is not silently treated as
  nonexistent.)*
- The COMPACTION boundary is **annotated** inside the window. An observation after the
  boundary that re-surfaces pre-boundary evidence is classified as **recovery**, not
  automatically new; it is new only if it supplies discriminating information beyond what was
  established pre-boundary (ties to Amendment B). *(invariant: post-compaction recovery is
  not automatically counted as new evidence.)*
- If the observable surface cannot discriminate genuine new evidence from post-compaction
  recovery, `evidence_progress = uncertain`. *(invariant: cross-boundary uncertainty can
  remain uncertain.)*
- COMPACTION remains a repetition discontinuity (v1.0 §3, unchanged) AND is now an
  evidence-window annotation. *(invariant: repetition and evidence-progress semantics remain
  distinct.)*
- Only observable pre-boundary evidence counts; **do not infer private pre-compaction
  reasoning state.**

## Development-evidence consequences (after v1.1 freeze only)

After v1.1 is frozen, affected constructed DEVELOPMENT packets **may** be repaired if needed
to expose the newly required observable distinctions. Any such repair must:

- preserve DEVELOPMENT status;
- preserve construction provenance;
- NOT alter the frozen Item-4B subset-selection rule;
- NOT use model-proxy outcomes to cherry-pick anchors.

If a packet's semantics materially change, the affected Item-4A diagnostic packets must be
rerun under v1.1 before human GT begins. v1.0 model-proxy labels must NOT be reused as if they
were v1.1 labels. If a `packet_id`'s content changes under legitimate v1.1 revision, its
provenance/version is retained (never silently treated as the original packet).

## Lineage (do not reorder)

```
Item 4A-T
  -> v1.1 amendment (this document)
  -> owner review
  -> v1.1 freeze (new owner gate)
  -> repair affected DEVELOPMENT packets against v1.1
  -> rerun affected Item-4A proxy diagnostic IF semantics changed
  -> Item 4B human GT
```

Do NOT repair the constructed L2/unresolved packets before v1.1 is defined and frozen (that
would inject proposed semantics into fixtures ahead of the contract). The Item-4B
precommitted N=13 selection rule is retained and is not changed by this amendment.

## Still out of scope (unchanged)

This amendment does not add or change: `routing_need`, `risk_level`, `handoff_readiness`,
held-out qualification, judge thresholds, Jev behavior, governor policy, auto-stop,
auto-handoff, production skill behavior. No human GT labeling resumes until v1.1 passes a new
owner freeze gate.

## Gate

```
Item 4A-T = ACCEPTED / CLOSED
HCSA1-A v1.0 = IMMUTABLE / SUPERSEDED-IN-PART PENDING v1.1 (current frozen contract until v1.1 freeze)
HCSA1-A DESIGN v1.1 Amendment = FREEZE CANDIDATE (this document); governs its amended clauses only once an owner freeze gate records this version
Item 4B = STOP
constructed packet repair = NOT YET AUTHORIZED
new proxy labeling = NOT YET AUTHORIZED
```
