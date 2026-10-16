# AMENDMENT 1 to the behavioral pre-registration

**Written 2026-10-16, after the first battery completed and was inspected,
before any amended arm ran.** Per ground-truth-gates: when a run trips its own
pre-registered validity clause, void the affected cells, write the amendment in
the durable record, disclose that partial results were seen, argue the peek
could not manufacture the amended outcome, and re-run from zero. The verdict
cites only the amended re-runs for the voided cells; cases not voided keep their
first-battery results.

## What tripped (from the first battery, run 1)

- **CASE 1 — VOIDED.** The pre-registered BAD-doctrine control did NOT leak:
  `C1_BAD` returned `NOT-OK` on all 3 replicates, identical to CURRENT (2/2) and
  PROPOSED (3/3). Reading `C1_BAD_r1` shows why — the weak-tier model's prior
  that a settings page must be efficient overrode the injected
  spectacle-everywhere doctrine (it wrote, in substance, "the award-experience
  doctrine conflicts with a tool's purpose"). Every arm sat at the same ceiling
  (`NOT-OK`), so the probe carried no discriminating evidence and cannot
  distinguish "PROPOSED does not leak" from "the model never leaks here
  regardless of doctrine." Pre-registered kill clause: VOID Case 1, redesign the
  control, re-run from zero, do not score.
- **CASE 6 — predicate mis-measured; re-scoped.** The pre-registered predicate
  "any `NO` = FAIL" conflates a weak-tier recall omission with a doctrine waiver.
  `C6_PROPOSED` split r1=`YES`, r2=`NO`. Reading the bodies: r1 lists MOTION-1009
  (prefers-reduced-motion) and MOTION-2026 and answers `YES`; r2 enumerates a
  partial/garbled set of MOTION rule ids, simply omits MOTION-1009 from its list,
  and answers `NO`. This is a lossy weak-tier enumeration, not a removal of the
  floor. Load-bearing ground truth independent of any model run: `motion.md`
  body is byte-identical CURRENT↔PROPOSED (only the header SHA line differs), and
  it contains the reduced-motion floor (MOTION-1009 + §6 "Reduced motion is a
  floor"). The C change touches ANTISLOP-2008 only; it does not touch motion
  doctrine. So the behavioral question is not "absolute YES-rate" (that is
  weak-tier recall noise) but "did the C change DEGRADE the floor relative to
  CURRENT" — a differential test.

## Partial results seen before amending (full disclosure)

Before writing this amendment I had seen: Case 1 all arms `NOT-OK` (incl. BAD);
Case 2 both `NO` (pass); Case 3 all `ACCENT-COUNT: 1`, no banned hex (pass);
Case 4 PROPOSED `Crimson Text, Inter`, role-framed, no Fraunces/Instrument Serif
(pass); Case 5 all `YES` with device vocabulary (pass); Case 6 split `YES`/`NO`.

## Why the peek cannot manufacture the amended outcomes

- **Case 1 amended** changes the controlled variable from DOCTRINE to CONTEXT:
  same PROPOSED doctrine, same `CONTEXT-FIT` line, the only change is the page
  (ordinary B2B settings vs. an experimental art-exhibition microsite carrying
  the SAME device bundle). The amended pass requires PROPOSED to FLIP to `OK` on
  the experimental page. The voided run's direction was "everything `NOT-OK`" —
  it gives no path to an `OK` and makes a flip HARDER, not easier; so a flip, if
  observed, is genuine and could not have been manufactured by the peek. The
  boundary-stability arm (CURRENT on both pages) is independent new data.
- **Case 6 amended** adds CURRENT at the same n for a differential parity test,
  and leans on the byte-identical `motion.md` ground truth (a fact about the
  files, not a model run, established before the peek). Whether CURRENT also
  splits YES/NO is independent of having seen PROPOSED split.

## Amended method (run from zero; score only these)

### Amended CASE 1 — context-discrimination control (single variable = page)
Doctrine inlined: antislop shard. Verdict line: `CONTEXT-FIT: OK|NOT-OK`.
Device bundle held identical across both pages: full-viewport WebGL hero,
spatial/room-to-room scroll, kinetic/variable display type, reactive cursor,
~700ms cinematic motion, frosted-glass panels.
- **1a-ORDINARY** page = internal B2B SaaS settings page. PROPOSED ×3, CURRENT ×2.
- **1b-EXPERIMENTAL** page = experimental art-exhibition campaign microsite whose
  explicit goal is an immersive scroll experience. PROPOSED ×3, CURRENT ×2.
- **Discrimination predicate:** the probe discriminates iff PROPOSED's verdict
  differs by context — `NOT-OK` on 1a, `OK` on 1b. Then: no-leak iff every
  PROPOSED 1a = `NOT-OK` (ordinary UI not waved through) AND PROPOSED 1b = `OK`
  (the override lane correctly applies when context justifies). Boundary
  stability iff CURRENT matches PROPOSED on both pages (the C change did not move
  the gate). FAIL (leak) iff any PROPOSED 1a = `OK`. UNTESTABLE iff PROPOSED does
  not differ across 1a/1b (still a ceiling → report, do not score as pass).

### Amended CASE 6 — differential reduced-motion parity
Same prompt + `REDUCED-MOTION-REQUIRED: YES|NO`. CURRENT ×3, PROPOSED ×3.
- **Ground-truth (load-bearing):** PROPOSED `motion.md` still contains the
  reduced-motion floor (verified by file diff + grep; independent of the model).
- **Differential predicate (behavioral, supporting):** PROPOSED's `YES`-rate is
  NOT lower than CURRENT's. PASS iff ground-truth holds AND PROPOSED yes-rate ≥
  CURRENT yes-rate. A shared weak-tier split (both omit sometimes) is recall
  noise, not a C-induced regression. FAIL only iff PROPOSED yes-rate < CURRENT
  yes-rate (my change degraded it) or the floor is absent from PROPOSED doctrine.
