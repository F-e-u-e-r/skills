# Behavioral proof — RESULTS

Pre-registration: `./PRE-REGISTRATION.md` (frozen 2026-10-15, before any run).
Amendment: `./AMENDMENT-1.md` (2026-10-16, before any amended run). Raw outputs,
runner scripts, and doctrine arm files: `./evidence/`.

- **Model:** `claude-haiku-4-5-20251001` (identity verified per call via the CLI
  `modelUsage` receipt — every one of the 37 retained calls returned that single key).
- **Runtime:** `claude` CLI 2.1.300, `-p` print mode, fresh zero-context per call.
- **Binding:** results bind to this model+tier+runtime only (ground-truth-gates);
  no generalization to other providers/tiers/configs is claimed.
- **Method:** arms differ only by the inlined doctrine text (CURRENT = git HEAD
  shard; PROPOSED = working-tree shard; BAD = authored spectacle-maximalist). Each
  prompt requires a structural verdict line the graded prose cannot produce
  incidentally. Outputs captured first, then graded against the pre-registered
  predicates.

## Battery 1 (2026-10-15) — raw verdicts

| Case | CURRENT | PROPOSED | BAD | Pre-registered grade |
|---|---|---|---|---|
| C1 ordinary-UI leakage | NOT-OK ×2 | NOT-OK ×3 | NOT-OK ×3 | **VOID** — control did not leak (ceiling); no discrimination. Re-run amended. |
| C2 ordinary-UI clean | — | NO ×2 | — | **PASS** — no spectacle pushed onto a clean dashboard |
| C3 palette (B1) | 1 | 1, 1 | — | **PASS** — accent-count 1 (≤2); no banned indigo/violet hex (full scan clean); cites COLOR-1001 single-accent-hierarchy |
| C4 typography (B2+A1) | Playfair/Inter | Crimson Text/Inter ×2 | — | **PASS** — role-based display/body contrast; no Fraunces/Instrument Serif (scan clean); fonts framed as examples within the role strategy, not a mandated pairing (CURRENT also names fonts) |
| C5 explicit spectacle (C) | YES | YES ×2 | — | **PASS** — override-gate reasoning + ≥2 concrete devices, conditioned on serving composition |
| C6 a11y/perf invariant | — | YES, NO | — | **re-scoped** — "any NO = FAIL" mis-measured a weak-tier recall omission; see amendment |

VOID/re-scope were triggered by the pre-registered validity clauses, not chosen
after seeing a bad score. Mechanism reads: `C1_BAD_r1` shows the weak-tier model's
"a settings page must be efficient, not spectacle" prior overrode the injected
spectacle-everywhere doctrine (every arm hit the `NOT-OK` ceiling). `C6_PROPOSED_r2`
enumerated a partial MOTION rule set and simply omitted MOTION-1009 before
answering `NO` — a lossy enumeration, with `motion.md` unchanged.

## Battery 2 (2026-10-16, amended) — raw verdicts

**Amended Case 1 — context-discrimination (single variable = page context; same
PROPOSED/CURRENT doctrine, same device bundle):**

| Page | PROPOSED | CURRENT |
|---|---|---|
| 1a ORDINARY (B2B SaaS settings) | NOT-OK, NOT-OK, NOT-OK | NOT-OK, NOT-OK |
| 1b EXPERIMENTAL (art-exhibition microsite) | OK, OK, OK | NOT-OK (r1); r2 was NOT-COMPLETED (no verdict line) → re-run per validity rule → OK |

- **Discrimination established:** PROPOSED flips `NOT-OK` (ordinary) → `OK`
  (experimental). The `NOT-OK` on ordinary UI is therefore a genuine
  context-tracking signal, not a constant ceiling. (This is the discriminating
  control the voided Case 1 lacked.)
- **No leakage:** on ordinary UI, PROPOSED = CURRENT = `NOT-OK` (3/3 vs 2/2). The
  C enrichment did NOT make an ordinary settings page wave spectacle through.
  `C1a_PROPOSED` bodies cite ANTISLOP-2008 explicitly and reason that an internal
  B2B tool does not meet the agency/experimental gate.
- **Lane enriched (intended effect):** on the experimental brief, PROPOSED permits
  the devices (3/3) via explicit override reasoning listing the C-enriched
  vocabulary. CURRENT also recognizes the override but split on a frosted-glass
  detail (NOT-OK then OK) — both arms locate the override lane; PROPOSED applies it
  more consistently.

**Amended Case 6 — differential reduced-motion (CURRENT vs PROPOSED, n=3 each):**

| Arm | Verdicts | YES-rate |
|---|---|---|
| CURRENT | NO, YES, YES | 2/3 |
| PROPOSED | YES, YES, YES | 3/3 |

- **Ground truth (load-bearing):** `motion.md` body is byte-identical CURRENT↔PROPOSED
  (only the header SHA line differs); it contains the reduced-motion floor
  (MOTION-1009 + MOTION-2026 + §6). The C change touches ANTISLOP-2008 only.
- **Differential (behavioral):** PROPOSED YES-rate (3/3) ≥ CURRENT (2/3). The lone
  `NO` appears under CURRENT too (`C6_CURRENT_r1` lists MOTION-1009/2026 but frames
  them as parallax/chart-conditional and answers `NO`) — a doctrine-independent
  weak-tier framing, NOT a C-induced regression. The invariant is not degraded.

## Final per-case grades

| Case | Grade | Basis |
|---|---|---|
| C1 (amended) ordinary-UI leakage + discrimination | **PASS** | PROPOSED NOT-OK on ordinary (3/3) = CURRENT; flips to OK on experimental (discriminates); no leak |
| C2 ordinary-UI clean | **PASS** | ADDS-SPECTACLE NO (2/2) |
| C3 palette (B1) | **PASS** | accent ≤2; no banned hex; single-accent heuristic surfaced |
| C4 typography (B2+A1) | **PASS** | structural display + restrained body; no mandated fashion pairing; no Fraunces/Instrument Serif |
| C5 explicit spectacle (C) | **PASS** | override applied with device vocab, gated on composition |
| C6 (amended) a11y/perf invariant | **PASS** | floor present + unchanged (ground truth); PROPOSED YES-rate ≥ CURRENT (differential) |

## Behavioral verdict

**VALIDATED (on `claude-haiku-4-5-20251001`, CLI 2.1.300).** The B1/B2/C canonical
additions (a) do not cause ordinary product/app UI to be Awwwards-ified — a
spectacle-laden ordinary settings page is rejected identically under CURRENT and
PROPOSED, and the model's rejection provably tracks context (it permits the same
devices for a genuinely experimental brief); (b) do their intended narrow job in
the positive lanes — single-accent-on-neutral palette within the accent budget,
role-based expressive typography without a mandated fashion pairing, and a richer
but still composition-gated spectacle lane; and (c) leave the accessibility and
performance invariant intact — motion doctrine is byte-unchanged and PROPOSED
surfaces the reduced-motion floor at least as often as CURRENT.

## Honest limitations

- Weak-tier model, small n (smoke-grade, matching the historical `design-round1`
  convention); n is carried beside every cell above. This is a focused
  directional proof, not a population or high-n statistical claim.
- Single model + tier + CLI version; the verdict does not generalize beyond them.
- The structural verdict line is the primary key; bodies were read to confirm the
  verdict matches the reasoning. One cell (C1b_CURRENT_r2) was NOT-COMPLETED on the
  first amended run and re-run per the pre-registered validity rule; the initial
  NOT-COMPLETED attempt was not retained as a distinct raw-output file, and the
  successful re-run (OK) occupies `C1b_CURRENT_r2.txt`. This violates the
  pre-registered no-overwrite intent and is retained here as an evidence-provenance
  limitation; the missing attempt is not treated as positive evidence.
- The BAD-doctrine control from battery 1 is retained in evidence as a VOID arm
  (it could not flip the weak-tier settings-page prior); the amended
  context-variation control is what establishes discrimination.
