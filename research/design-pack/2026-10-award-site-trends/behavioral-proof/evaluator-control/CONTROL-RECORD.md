# Deterministic evaluator control — Case-1 spectacle-leakage (owner §4)

**Written 2026-10-16.** Closes the owner's §4 requirement: add one small
deterministic evaluator control so the pre-registered Case-1 leakage criterion is
two-sided-armed (a GOOD output must not leak; a known-bad output must leak),
without re-running the model battery. No LLM generation was used.

## Why a new control was needed

- The behavioral proof has **no separable scorer**: `evidence/run_battery.py` and
  `evidence/run_battery2.py` only *capture* model output (their own comment: "No
  grading here"); the per-case grades in `RESULTS.md` were assigned by human
  reading. Per owner §4, the narrowest deterministic assertion implementing the
  pre-registered Case-1 leak criterion is created here instead.
- The original pre-registered BAD-doctrine control **VOIDed** (battery 1): the
  weak-tier model's "a settings page must be efficient" prior overrode the
  injected spectacle-everywhere doctrine, so every arm (incl. BAD) sat at the
  `NOT-OK` ceiling and the probe could not discriminate. The amended Case-1
  context-variation run established discrimination behaviorally, but — as the
  owner notes — that does not by itself satisfy a two-sided *evaluator* control.
  This record supplies it deterministically.

## The assertion (authority = the structural verdict line)

`leakage_assert.py` implements the pre-registered CASE-1 FAIL clause for an
**ordinary** product/app page carrying the gratuitous spectacle device bundle:

| final line | meaning | status | exit |
|---|---|---|---|
| `CONTEXT-FIT: OK` | spectacle waved through onto ordinary UI | **LEAK** | 1 (FAIL) |
| `CONTEXT-FIT: NOT-OK` | ordinary UI not waved through | **NO-LEAK** | 0 (PASS) |
| (verdict line absent) | — | **NOT-COMPLETED** | 2 (never a pass) |

The verdict regex is identical to `run_battery.py`'s `VERDICT["C1"]`
(`CONTEXT-FIT:\s*(OK|NOT-OK)`) — the proof's own parser, reused. The verdict
line is a structural marker the graded prose cannot produce incidentally
(ground-truth-gates). A device-vocabulary scan is printed only as a
**non-authoritative diagnostic**: those device terms occur in *both* a leaking
and a rejecting review (the rejecting one names them as problems), so they cannot
discriminate and are never used to decide — a real captured OK cell
(`C1b_PROPOSED_r2`) even has device-vocab=False, confirming the verdict line, not
the vocabulary, is the correct key.

**Scope:** the control's subject is the **ordinary page**. On a genuinely
experimental/agency brief, `OK` is the override lane working as intended and is
**not** a leak; the assertion is applied to ordinary-page outputs for the leak
verdict.

## Frozen fixtures (hashed before scoring)

Authored by hand (no model call), then hashed, then scored — not modified after.

| fixture | sha256 | role |
|---|---|---|
| `GOOD_ordinary.md` | `2ab3a5457cf087a0c9c089b243419a447ceff8458fc03a6baaa9b9c8178d609e` | settings-page review that rejects the device bundle; ends `CONTEXT-FIT: NOT-OK` |
| `BAD_ordinary.md`  | `d6e009f237eb992861ba33d442d123372d75f32e2b3b028aaca23f5f58eb7af7` | same settings-page task, recommends/keeps the device bundle with no experimental justification; ends `CONTEXT-FIT: OK` |

## Two-sided result (the §4 requirement)

```
GOOD_ordinary.md : verdict=NOT-OK -> NO-LEAK  -> exit 0   (no spectacle-leak failure)
BAD_ordinary.md  : verdict=OK     -> LEAK     -> exit 1   (spectacle-leak failure)
  REASON: CONTEXT-FIT: OK on an ordinary product page = the spectacle device bundle was waved through.
```

**The assertion discriminates GOOD from BAD, and BAD fails specifically for the
intended reason.** The §4 BLOCKED condition ("evaluator cannot discriminate these
two fixtures") does **not** apply.

## Cross-check against the real captured corpus (strengthens "armed")

Applying the same assertion to the proof's real ordinary-page outputs:

| captured cell(s) | verdict | status | exit | agrees with |
|---|---|---|---|---|
| `runs-battery2-amended/C1a_PROPOSED_r1..r3` | NOT-OK ×3 | NO-LEAK | 0 | human grade (no leak) |
| `runs-battery2-amended/C1a_CURRENT_r1..r2` | NOT-OK ×2 | NO-LEAK | 0 | human grade (no leak) |
| `runs-battery1/C1_BAD_r1..r3` (VOID control) | NOT-OK ×3 | NO-LEAK | 0 | **reproduces the VOID**: the real BAD-doctrine arm did not leak |
| `runs-battery2-amended/C1b_PROPOSED_r1..r3` (experimental) | OK ×3 | (LEAK verdict at ordinary scope) | 1 | the override lane — `OK` here is correct, not a leak |

The last two rows matter: the real BAD-doctrine arm could NOT arm the gate
(exactly why §4 is needed — a frozen synthetic BAD does it), and the experimental
rows show the assertion is not a trivial always-pass (it fires exit 1 on `OK`) and
that the verdict line tracks context.

## Conclusion

The Case-1 spectacle-leakage criterion is **deterministically armed, two-sided**:
`GOOD_ordinary` → no-leak, `BAD_ordinary` → leak-for-the-intended-reason, and the
assertion reproduces every real captured grade. This is a research/evidence
artifact only; it is not loaded by any runtime and ships with no plugin.
