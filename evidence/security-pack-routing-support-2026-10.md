# Security Pack v1 — routing-support record (2026-10)

**What this records.** The model/configuration support floor for *autonomous routing*
of the Security Pack v1 skill (`security-posture-record`), and the Phase-1f evidence
behind it. It is a documentation record, not a machine-readable compatibility schema;
no `supported_model` / compat field is introduced anywhere in `metadata/` or any
`plugin.json`.

## Test date and configuration

- **Routing battery run:** 2026-10-10 (UTC) — Security Implementation Phase 1f
  current-runtime model refresh. Pre-registration + harness replica + drivers were
  hash-frozen at 2026-10-10T16:19:01Z, before the first scored run (16:19:14Z).
- **Owner acceptance of Phase 1f + tier-scope resolution:** 2026-10-11 (local).
- **Claude Code CLI:** 2.1.286.
- **Harness:** the frozen Phase-1d/N2 Gate-S judge + the Gate-R forced-choice
  routing-preference assay, byte-identical to Phase 1e (no name, description, case,
  expected label, scorer, or decision rule changed). Gate R is a forced-choice
  routing-*preference* assay, **not** an autonomous-activation measurement.

## Exact model IDs (resolved, never aliases)

Resolved exact IDs were recorded from the runtime's own receipts; the CLI 2.1.286
`haiku` alias resolves to the **older** `claude-haiku-4-5-20251001`, so aliases are
never used as the support claim.

| role | resolved exact ID |
|---|---|
| current strong tier (verified floor) | `claude-sonnet-5-5` |
| historical strong-tier comparator (Phase 1c/1d/1e) | `claude-sonnet-5` |
| current weak tier (tested, not supported for autonomous routing) | `claude-haiku-5-5` |
| CLI `haiku` alias at 2.1.286 (stale; distinct older model) | `claude-haiku-4-5-20251001` |

## The claims

**Supported (exact):** autonomous Security-v1 skill routing was verified on
`claude-sonnet-5-5` under the tested Claude Code configuration.

**Not supported (exact):** `claude-haiku-5-5` is not supported for autonomous
Security-v1 routing in this release.

**Scope / non-claim (exact):** other model/configuration support is unverified unless
separately recorded. This does not restrict explicit invocation, which was not tested —
the unsupported finding is about *autonomous routing preference*, not about whether the
skill can be invoked by name.

## Phase-1f result summary

**`claude-sonnet-5-5` — CLEAN (the verified floor).** With the production seam
(`security-architect` = SHADOW-v2, `security-posture-record` = `candidate_demagnetized`):
R0 routed the five lifecycle cues → `security-posture-record` 5/5, the eight
GTG-exclusive cues → `ground-truth-gates` 8/8, the three architect-only cues →
`security-architect` 3/3 with zero Security leak, and the route-out cue → `skill-vetting`.
Gate R clean on all four seam predicates; **exact parity** with the historical strong
tier `claude-sonnet-5` (same clean profile). N2 word-free lifecycle diagnostics →
candidate 4/4.

**`claude-haiku-5-5` — NOT adoptable for autonomous Security-v1 routing.**
- Gate S (semantic trigger-disjointness, symmetric SEC↔GTG): **HARD FAIL** — all five
  SEC-exclusive lifecycle cues collide (the real `ground-truth-gates` description is
  judged APPLICABLE on every one of them), with the `candidate_bad` control used as the
  discriminator.
- Gate R (routing preference): R0 was not clean — GTG-exclusive routed to GTG only 5/8
  (2 to other, 1 none) and one lifecycle cue mis-routed to `security-architect`
  (lifecycle → candidate 4/5). A frozen alternate weak-tier encoding (RCG) recovered the
  lifecycle (5/5) but collapsed GTG-exclusive to 3/8 — so no weak-tier encoding is
  simultaneously clean.
- Weak-tier tuning is CLOSED (owner): no further weak-tier encoding work, no assist/RCG
  adoption. `claude-haiku-5-5` is routing-support-unverified; this says nothing about
  explicit invocation.

(The CLI `haiku` alias — the older `claude-haiku-4-5-20251001` — routed lifecycle cues
→ `ground-truth-gates` 0/4 candidate under R0, a separate confirmation that aliases lag
and resolved exact IDs must be used.)

## Future model/runtime refresh rule

`claude-sonnet-5-5` is the *current verified* configuration, not a timeless invariant. A
material model or runtime change (a new Sonnet/Haiku version, a CLI change that alters
skill routing, or a harness change) reruns the Phase-1f routing battery — recording the
**resolved exact model IDs** of that run — before any parity or support claim is
extended. The `claude-haiku-5-5` unsupported finding is specific to that exact ID and is
not generalized to future Haiku versions. Historical frozen artifacts are not rewritten;
a refresh adds a new dated record of this kind.
