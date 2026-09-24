# Activation Execution Probe v1 (AE1) — scored-result reconciliation (2026-09-24)

Purpose: publish the canonical AE1-v1 result from preserved, owner-reconciled
experiment evidence. Figures below were read from the on-disk scored return
packet (raw run artifacts are gitignored / local-only; this note is the tracked
summary). Where a summary index disagreed with a detailed packet, the packet wins.

Status: **AE1-v1 SCORED = ACCEPTED / CANONICAL; AE1-v1 = COMPLETE / CLOSED**
(owner raw-evidence reconciliation PASS, 2026-09-24).

## Research question

Given task surfaces already demonstrated to route correctly under *explicit*
routing, does a *hardened* *ordinary-execution* instrument convert that routing
competence into *autonomous* skill activation? AE1 is deliberately not a fresh
attempt to rediscover whether a generic cue helps (Activation Bridge v1/v2 already
scored that); it isolates activation execution on surfaces where routing is not in
doubt.

## Provenance and baseline

- **R5 governing freeze:** `c6ef853af391`. The scored run is governed solely by the
  R5 freeze (recorded qualification milestones: R1 not qualified, R2 accepted, R3
  mechanically qualified on a preregistration contradiction, R5 qualified /
  canonical).
- **IH1-R2 measurement baseline:** `98a0fee7e91a` — the hardened
  routing/activation observation instrument (Instrument Hardening v1, round 2:
  qualified / canonical). AE1 is the activation-execution experiment run on top of
  that accepted instrument, not a change to it.
- Model throughout: `claude-haiku-4-5-20251001` (weak tier). Real sessions only.

## Design

- **Surfaces — `T4a` / `T4b` (rationale).** In the scored Localization Probe, the
  `ground-truth-gates` `T4` surface routed **6/6** under explicit routing — it is a
  *proven-routeable* surface. Restricting AE1 to `T4a`/`T4b` means a failure to
  activate cannot be blamed on routing ambiguity: routing competence on these
  surfaces is already established, so the two failure modes (routing ambiguity vs
  activation-execution failure) are not conflated.
- **Two-arm design.**
  - **Arm-R (reference gate):** contemporaneous *explicit-routing* control on the
    same surfaces — confirms the surfaces are still routeable in this run.
  - **Arm-O (ordinary execution):** the primary arm — ordinary task execution with
    no explicit routing instruction; measures whether an available skill is invoked
    autonomously.
- **N = 24 / cap = 24.** 12 runs per arm (`T4a` x6, `T4b` x6). All 24 are real
  haiku sessions.

## Reference gate (Arm-R)

Contemporaneous explicit-routing reference gate **PASS**:

- `T4a` = **6/6**
- `T4b` = **5/6**
- pooled = **11/12**

The surfaces reproduced their routeability contemporaneously with the
ordinary-execution measurement — routing competence is present in this run, not
imported from an earlier campaign.

## Primary endpoint (Arm-O)

Ordinary-execution autonomous activation:

- expected-skill activation: `T4a` **0/6**, `T4b` **0/6**, pooled **0/12**
- any-Skill activation (any pack skill, not only the expected one): **0/12**

## Final counts and the INVALID distinction

- **Final AE1 INVALID = 0.**
- The raw frozen reducer may label a clean, no-Skill *terminal* run as
  `INVALID:no-decision`. AE1's **preregistered post-hoc rule** maps eligible clean,
  exact-model-verified no-decision terminals to **NO_ACTIVATION** (a negative
  activation observation), not to INVALID: a no-Skill terminal on a required-skill
  surface is exactly the primary-endpoint negative, not a broken run. The
  underlying raw evidence is preserved and not erased; the mapping is a labeling
  rule over retained terminals, applied uniformly and fixed before scoring.

## Interpretation boundary

AE1 establishes an **explicit-routeability / autonomous-activation dissociation**
under the tested configuration: on `T4a`/`T4b`, explicit routeability reproduced
contemporaneously (11/12) while autonomous skill activation was not observed in
ordinary execution (0/12).

AE1 does **not** establish:

- a causal effect of the routing instruction;
- a causal effect of the tool allowlist;
- that skill descriptions are uninvolved;
- a population-wide activation rate (this is an engineering sample, not a
  population estimate; no statistical significance is claimed);
- behavioral skill usefulness or uplift (AE1 stopped at the activation /
  routing-observation layer and did not measure task-quality uplift).

The earlier natural-activation **0/48** autonomous-invocation result (the
round5-deployed R2 baseline) is **consistent supporting prior evidence**; AE1 is
**not** an identical replication of that endpoint (different instrument, arms, and
surfaces).

## Progression and closure

- **Progression rule = NOT MET.** Ordinary autonomous activation did not reach the
  preregistered threshold that would qualify a behavioral follow-up.
- **Behavioral follow-up = NOT ELIGIBLE.**
- **Closure:** AE1-v1 is COMPLETE / CLOSED. No new activation treatment is promoted
  and no next experiment is inferred from this result. Any new activation
  hypothesis requires independent motivation, new preregistration, and a fresh
  owner gate. Production skill content is unchanged.
