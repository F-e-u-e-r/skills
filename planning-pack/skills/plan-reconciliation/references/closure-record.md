# Closure record — template (owned by `plan-reconciliation`)

Loaded on demand by `plan-reconciliation` §3 (Close). The closure record reconciles every intended item against
the approved (possibly amended) baseline, with evidence, so **nothing vanishes**. (Architecture §3/§6, A11.)

## Before building it (AR-A11-C1)

If shipped reality legitimately supersedes the plan, record an **explicit, approved baseline change FIRST**, then
reconcile against the amended baseline — never treat drift as intended by reconciling against a stale plan.

## Template

```
closure of plan <id> @ baseline vN
reconciled against:   <baseline version — amended first if AR-A11-C1 applied>

intended items (the closure baseline — every planned item):
  <item ID> — <delivery state> — <evidence reference> — <disposition if not delivered>
  …

unrequested work surfaced (both directions — A11-06):
  <what was done that was not planned> — <kept / reverted / recorded as follow-up>

dispositions for undelivered items (A11-02; none may be silently dropped):
  <item ID> — <recorded disposition> — <authority, if dropped/waived (A11-05)>
```

## The three delivery states (the distinction is load-bearing)

- **delivered** — established *with evidence* as delivered.
- **undelivered** — established *with evidence* as not delivered (missing/partial). A **recorded disposition is
  required** (A11-02). A *contradicting* item is undelivered unless shipped reality legitimately supersedes the
  plan (then AR-A11-C1 first).
- **NOT VERIFIED** — delivery **cannot be established**. An **Ops evidence state**: reported, **never counted as
  delivered**, **no Planning disposition required** (A11-04 deferred).

**Load-bearing:** "undelivered" is **never** inferred from "not counted as delivered"; NOT VERIFIED ≠ undelivered.
Any NOT-VERIFIED item is excluded from the undelivered-disposition accounting.

## Ownership boundary

You (Planning) reconcile and classify; **Ops owns**: whether an item's evidence actually establishes delivery
(evidence quality — operational-rigor §4–§5, delegation-and-review §3), the honesty of the final completion claim,
and the human authority required to drop/waive an item.

Source: architecture §3 (A11 folding) + §6 (three delivery states). On disagreement about the artifact model, the model
canonical in `planning` wins.
