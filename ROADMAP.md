# Opus Pack — research roadmap

> All items below are **PARKED** until explicitly promoted by the owner. "Now"
> means the highest-priority item to consider authorizing next; it is **not**
> execution authorization. PARK is not NEXT, and PARK is not latent authorization.

This roadmap is built on the reconciled evaluation state in
[reviews/2026-09-18-activation-eval-reconciliation.md](reviews/2026-09-18-activation-eval-reconciliation.md)
(raw run artifacts are local-only / gitignored). Current production skill content
is unchanged, and nothing here proposes changing it without a controlled experiment
that supports the change.

Frontier: the canonical routing benchmark is strong, but explicit task-surface
routing is **mixed** and autonomous activation remains **weak**. Localization is
**L3 / MIXED**: some surfaces route cleanly while others miss or select neighboring
skills. On the weak-`ground-truth-gates` T2 surface, task-side framing recovers
routing (Surface-Cue **G2/G5**) while the tested description-side expansion does not
(Description-Boundary **D2**) — so the open question is activation execution and
task-surface discrimination, and **no pack-wide description rewrite** follows.

## Closed — Instrument Hardening v1

**Instrument Hardening v1 (IH1) = COMPLETE / CLOSED.** IH1-R2 =
**QUALIFIED / CANONICAL** (freeze `98a0fee7e91a`), owner-accepted.

IH1 produced the hardened routing / activation observation instrument and then
supplied the hardened measurement baseline that **AE1-v1 (below) reused**
(`98a0fee7e91a`). Earlier probing had exposed **stop-compliance** weakness and
**T1b-style runaway** task execution (localization: stop-after-routing 9/21;
T1b ×3 timed out at the wall); the qualified IH1-R2 instrument resolved these
without changing skill content.

Qualification criteria met:

- reliable decision → observation → stop lifecycle
- no T1b-style runaway task execution
- known-bad cases demonstrably fail
- routing / activation observability preserved
- INVALID remains INVALID
- no silent rerun / replacement / backfill
- raw provenance retained
- no skill-content change

## Parallel Now — Stable Evaluation / Governance Playbook

Document only the methodology that is **already stable**:

- manifest / SHA binding
- qualification-before-score
- known-bad / two-sided proof
- INVALID preservation
- no silent backfill
- full inventory audit where load-bearing
- failed-revision provenance
- contemporaneous controls
- owner STOP / authorization gates
- PARK ≠ NEXT
- PARK ≠ latent authorization

Do **not** canonicalize any pre-IH1 routing / activation probe implementation.
The hardened, qualified instrument is **IH1-R2** (`98a0fee7e91a`, closed above);
the earlier unqualified probe setup it replaced is not canonical.

## Closed — Activation Execution Probe v1 (AE1)

**Activation Execution Probe v1 (AE1) = COMPLETE / CLOSED.** Scored, owner-accepted
as canonical (2026-09-24).

Research question: given surfaces already shown to route correctly under explicit
routing, does a *hardened* ordinary-execution instrument convert that routing
competence into autonomous skill activation? AE1 ran the hardened instrument
(IH1-R2 measurement baseline `98a0fee7e91a`) on the preregistered `T4a`/`T4b`
surfaces in a two-arm design (N = 24), governed by the R5 freeze `c6ef853af391`.

Canonical result:

- explicit-routing reference gate **PASS (11/12)**
- ordinary expected-skill activation **0/12**
- any-Skill activation **0/12**
- progression rule **NOT MET**
- behavioral follow-up **NOT ELIGIBLE**

This is an explicit-routeability / autonomous-activation dissociation under the
tested AE1 configuration. It does **not** establish a causal effect of the routing
instruction or the tool allowlist, that skill descriptions are uninvolved, a
population-wide activation rate, or any behavioral skill usefulness or uplift. Full
design, counts, and interpretation boundary:
[reviews/2026-09-24-ae1-v1-scored-reconciliation.md](reviews/2026-09-24-ae1-v1-scored-reconciliation.md).

Prior supporting evidence (already scored, not reopened): Activation Bridge v1/v2
each scored appropriate activation 6/41 (generic cues insufficient at this tier;
the v1-v2 comparison is not a clean contemporaneous causal contrast); Localization
**L3 / MIXED** (skill-and-surface-specific). The earlier natural-activation 0/48
autonomous-invocation endpoint is consistent supporting prior evidence, not an
identical replication.

**No new activation treatment is promoted and no next experiment is inferred from
this result.** Any new activation hypothesis requires independent motivation, new
preregistration, and a fresh owner gate. `AGENTS.md` remains **HOLD** unless
separately authorized.

## Later / Conditional — Broader Holdout Effectiveness

Promote **only** if the activation-execution work indicates that skill-content /
routing-generalization remains a load-bearing bottleneck.

Potential future goal: new **preregistered** holdout surfaces, unseen during the
current tuning, to measure generalization rather than fixture optimization. Do not
execute now.

## Optional Science — Higher-n Surface-Cue Replication

Recorded as **optional only**. The existing directional result is already sufficient
for the current production decision (**do not change production skill content**).
Higher-n or stronger-tier replication should be promoted only if a concrete future
product or engineering decision requires stronger stability evidence. Do not execute
now.

## Explicitly closed / not-next

- **GTG Description-Boundary Probe v1 = COMPLETE.**
- Tested candidate description = **rejected for shipment** (description `389884bc` /
  SKILL `ec660a81`; canonical `ground-truth-gates` SKILL.md `29f2d5f9` unchanged).
- **T2 description-repair search = closed.** No post-hoc wording search — do not add
  another clause, broaden the clause, copy more T2 wording into the description, or
  run alternative descriptions until one goes green.

A future description hypothesis is not ordinary roadmap continuation. It would
require **independent motivation, new preregistration, and new owner authorization**.
