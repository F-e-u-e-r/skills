# Decision record — template, significance, timing

Loaded on demand by `planning` Step 3 (Decide). A decision record captures a load-bearing choice so a later
session — or `plan-reconciliation` — can see what was decided, what was rejected, and why, and whether it may be
reopened. (Architecture §3 / A3-01…A3-07, A9-07.)

## When a choice earns a record (significance — A3-02)

Record a choice when a later agent could silently reverse it without the recorded *why*, or when it binds other
work: an interface/contract shape, an architecture or storage choice, a dependency, a sequencing rule, a
requirement precedence call, a deferred-decision boundary. A micro-choice a later reader would never mistake for
design does **not** earn a record (that is the plan-level over-building INV-3/O8 warns against).

## Template

```
DR-<id>  (stable ID; referenced by work items and requirements it binds)
decision:        <what was chosen, in one line>
rejected:        <the alternative(s) not taken>
why:             <the reason the chosen option wins — the load-bearing rationale>
derives from:    <requirement ID(s) this decision serves (A3-07 trace check)>
interface oblig: <any contract this imposes on other work (A3-06)>
reopen if:       <the condition under which this must be revisited (A9-07), or "stable">
status:          open | decided | superseded-by DR-<id>   (append-only; never erase — AR-A9-C1)
```

## Timing & triage (A3-03)

- Decide **now** only what blocks progress or binds imminent work; explicitly **defer** the rest, recording the
  deferral as an open question (see `policy-parameters.md` P2) with its own reopen/decide-by condition.
- A decision **traces to a requirement** (A3-07) — this is a trace check, not a ban on design; design derived from
  requirements is expected.
- **No silent reversal:** changing a decided record is an append-only supersession (`status: superseded-by …`),
  never an in-place edit. Ops enforces non-reversal during execution; `plan-reconciliation` consumes `reopen if`.

## Element admission is NOT decided here

Whether an *executor* may invent an abstraction, optimization, or flexibility at build time is **Ops's** call
(operational-rigor §2/§5), not a plan decision record. Keep plan decisions at the plan level.

Source: architecture §3 (A3 folding) + §4. On disagreement about the artifact model, `plan-artifact.md` wins.
