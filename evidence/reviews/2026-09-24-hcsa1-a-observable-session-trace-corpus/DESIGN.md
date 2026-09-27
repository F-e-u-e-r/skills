# HCSA1-A — Observable Session Trace Corpus (pre-freeze contract DRAFT)

**Status:** DESIGN DRAFT, pre-freeze repair round applied (2026-09-24). **DESIGN freeze =
HOLD.** Phase 0 = ACCEPTED / CLOSED; Phase 0.1 (compaction observability) = ACCEPTED /
CLOSED. This remains **DESIGN ONLY**.

**NOT AUTHORIZED:** corpus construction, semantic judge execution, Jev execution,
governor, auto-stop, auto-handoff, parser implementation, threshold calibration,
commit, push, PR.

**Initiative:** HCSA1 subtrack **A**. Downstream (each its own gate): **HCSA1-B** Judgment
Qualification, **HCSA1-C** Advisory Control Plane (advisory-only in v1), **HCSA1-D**
Session Lifecycle & Handoff. **Siblings:** PR #245 revision-required; PR #244 HOLD;
Security split PARKED design.

Evidence base: [PHASE0-RECON.md](PHASE0-RECON.md) (Phase 0 + 0.1, accepted/closed).

---

## 1. Why this, why now

AE1-v1 (closed 2026-09-24) established a routeable / autonomous-activation dissociation.
That result **motivates studying the execution / control layer next; it does not rule out
description-related mechanisms**, and does not establish the execution layer as the only or
the larger causal leverage. Methodology inherited from IH1 / AE1 / round-5: a judgment is a
hypothesis until a fixture that can fail says otherwise — prereg, golden set,
qualification-before-score, known-bad / two-sided proof, no silent backfill, owner gates,
PARK != NEXT.

## 2. What we are actually measuring

The study object is **observable execution redundancy / marginal evidence gain**, NOT
private reasoning. Private CoT is unavailable (Phase 0). The signals below are
**generation / reasoning-activity proxies** only — they never measure the length or content
of hidden reasoning: thinking-block count, `output_tokens`, `turn_duration`, `effort`. The
question is whether additional observable execution adds decision-relevant evidence
(see §7) or changes a decision — never "how long did it think."

| Pattern (all observable) | Reading |
|---|---|
| long generation + new evidence | healthy |
| long generation + decision refinement | potentially healthy |
| long generation + repeated evidence | suspect |
| long generation + no state change | stalled |
| post-completion continuation | candidate waste (only when prefix-ready AND the suffix audit finds no later load-bearing evidence — §5) |

## 3. Adapter and compaction contract

**Freeze the HCSA normalized OUTPUT schema, never native transcript schemas.** Observed
drift (record-type rename `ai-title` -> `custom-title`; CLI 2.1.221 -> 2.1.281;
context-dependent record types corpus-wide) forbids binding to the native schema.

```
native transcript version -> version-tolerant adapter(s) -> ONE frozen HCSA schema -> derived features -> labels/judges
```

**Compaction observability is represented SEPARATELY from compaction occurrence**, with an
explicit valid-state table so `UNKNOWN` can never be misread as "no compaction":

```
context_boundary_observability:  KNOWN | UNKNOWN
context_boundary:                NONE | COMPACTION | INDETERMINATE
```

| observability | context_boundary | meaning | legal? |
|---|---|---|---|
| KNOWN | NONE | observed; no compaction at this point (continuity provable here) | yes |
| KNOWN | COMPACTION | observed compaction boundary (semantic discontinuity) | yes |
| UNKNOWN | INDETERMINATE | marker capability not qualified; occurrence not determinable | yes |
| UNKNOWN | NONE / COMPACTION | — | **never emitted** |
| KNOWN | INDETERMINATE | — | **never emitted** |

- Phase 0.1 qualified the marker for the observed CLI streams: `system.subtype=compact_boundary`
  immediately followed by `user.isCompactSummary=true` -> `KNOWN` + `COMPACTION`. A
  stream/version whose marker capability is not qualified is `UNKNOWN` + `INDETERMINATE`,
  **never `KNOWN` + `NONE`**.
- `UNKNOWN` / `INDETERMINATE` must **never** be read downstream as "no compaction," and a
  deterministic feature must **never** treat it as continuity-proven.
- **Qualification traces that require reliable continuity MUST exclude `UNKNOWN` boundary
  observability.**
- A `COMPACTION` boundary is a **semantic discontinuity for repetition features**:
  *similar activity across a compaction boundary must not, by itself, be classified as
  stalled repetition.* The corpus includes a hard discriminating case for legitimate
  post-compaction recovery (§10).

## 4. Development vs qualification firewall

Before any corpus is constructed, two evidence classes are defined and kept apart:

```
DEVELOPMENT / CALIBRATION      HELD-OUT QUALIFICATION
```

- Development traces MAY: measure label difficulty; measure labeler disagreement; develop
  adapters / features; select qualification metrics; set later qualification thresholds.
- **Development traces MUST NEVER contribute to the final qualification denominator.**
- Held-out qualification **selection rules are frozen before any judge performance on that
  set is observed.**
- The final qualification PASS/FAIL uses **only** the held-out qualification set.
- Exact N, threshold values, and A/B/C counts may remain deferred until development /
  calibration evidence exists (§17).

## 5. Round-1 unit of analysis: the decision point t

Round-1 scope is exactly `evidence_progress`, `repetition_state`, `completion_readiness`.

The canonical evaluation anchor is a **decision point t**. The **prefix judgment view
contains only information available at or before t**; no suffix information is visible
during prefix labeling.

**Anchor-generation policy (frozen).** Which events BECOME a decision point t is fixed by a
preregistered, deterministic, auditable observable rule applied mechanically to the whole
event stream — t is NEVER selected after inspecting suffix outcome or judge behavior. The
round-1 frozen rule: emit a decision point t at every `assistant_turn` boundary that either
(a) issues one or more `tool_call`s or (b) carries a `stop_signal` — both are structural,
observable in the frozen schema (§9), and either may occur, so t is not tied to a single
event kind. If not every generated t is labeled, the labeled subset is drawn by a
preregistered sampling rule (frozen with N, §17), never hand-picked; on the held-out set no
manual cherry-pick of anchors is permitted. Because anchor generation and sampling are
mechanical and independent of suffix / outcome / judge, anchor selection cannot leak
difficulty or outcome.

- `repetition_state`: labeled prefix-bounded at t (events <= t).
- `evidence_progress`: labeled prefix-bounded at t, and **measured over an explicit window**
  `W(t) = (previous decision anchor, t]` — i.e., gain SINCE the previous decision point (or
  session start for the first t), never over the whole session. Freezing the window is what
  keeps ground truth stable across labelers (no free choice of history horizon).
- `completion_readiness` uses a three-step, leakage-sealed protocol:

```
A. PREFIX LABEL       judge completion_readiness using events <= t
B. SEAL LABEL         the prefix label is sealed (frozen) before any suffix is revealed
C. SUFFIX OUTCOME     reveal events > t; determine whether later load-bearing evidence
   AUDIT              makes stopping at t harmful
```

- The primary safety error is the **harmful premature-stop false positive** — "ready" at t
  when later real work proved t too early.
- **Future information must never be used to improve the prefix judgment retroactively.**
  The seal (B) is what makes this auditable.

## 6. Judgment domains

```
evidence_progress:   new_load_bearing | new_supporting | none | uncertain
repetition_state:    none | productive_repeat | stalled_repeat | cyclic | uncertain
completion_readiness: not_ready | plausibly_ready | ready | uncertain
```

`uncertain` is first-class: round-1's goal is to learn which states cannot be safely judged
on observables. **No automatic action semantics attach to these labels in HCSA1-A/B** — they
are observations, not commands. Round-2 adds `routing_need` / `risk_level` /
`handoff_readiness` (the last also waits on HCSA1-D).

## 7. Decision-relevant evidence (semantic gain) definition

Semantic evidence gain is defined **relative to the task's observable decision state**. A
new observation counts as decision-relevant only when it can legitimately:

```
change | strengthen | weaken | close
```

an unresolved task-relevant proposition or decision. **Novel text, a new tool call, a new
file, or a syntactically different command is NOT sufficient by itself.**

**Load-bearing vs supporting (operational, for `evidence_progress` labeling).** The two
values are distinguished by their effect on the *admissible decision*, not by importance, so
a second labeler can apply the boundary consistently:

- `new_load_bearing` = evidence capable, on its own or by resolving a required gate, of
  changing the admissible decision / disposition / authorization boundary.
- `new_supporting` = decision-relevant evidence that changes confidence or support but does
  not, by itself, alter the currently admissible decision or a required gate.

Boundary disagreements are recorded per §11, never silently reconciled.

Therefore each labeled prefix/window must carry enough **sanitized observable context**
(the semantic surface a judge is allowed to see, §9) to identify:

- the current task / question,
- the current unresolved proposition(s), where applicable,
- the current observable decision state.

Do not infer or reconstruct private chain of thought.

## 8. Structural vs semantic novelty (kept separate)

```
Structural Novelty       = deterministic observable differences (new tool / changed args / new file or range / changed command or result / new artifact)
Semantic Evidence Gain   = decision-relevant informational gain (§7)
```

Phase 0 showed exact syntactic duplicates are rare (6/329 tool inputs; 1/308 Bash), so
structural novelty is at most a cheap candidate floor — high precision only on exact
repeats, low recall on semantic redundancy. **Do NOT freeze an aggregate `Evidence Gain
Ratio` in HCSA1-A.** Whether the two ever combine into one scalar is an HCSA1-B empirical
question (§17).

## 9. Frozen HCSA observable event schema (round-1 PROPOSAL — freezes at owner review)

The adapter OUTPUT (not the native record). A trace = ordered `events`; each event:

- `idx`, `session_local_id`, `ts`, `parent_ref` (branch reconstruction)
- `kind`: `user_turn` / `assistant_turn` / `tool_call` / `tool_result` / `context_boundary` / `stop_signal` / `auth_event`
- assistant_turn (activity proxies): `thinking_block_count`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `effort`, `turn_duration_ms`
- tool_call: `tool_name`, `arg_shape`, `arg_hash`, and where present `command_hash`, `file_path_pseudonym`, `file_range`
- tool_result: `status`, `is_error`, `exit_code`, `stdout_present`, `stderr_present`, `bytes`
- context_boundary: `context_boundary_observability` (KNOWN|UNKNOWN) + `context_boundary` (NONE|COMPACTION|INDETERMINATE) — §3
- auth_event: `permission_mode`, `denial_kind`, `hook_fired`
- stop_signal: `stop_reason`, `stop_hook`, `interrupted`

**Semantic observation surface (part of the frozen contract, not hidden outside it).**
Structural fields above cannot support the semantic evidence-gain judgment of §7, so the
schema explicitly freezes what a judge is permitted to read as semantic content:

- `user_turn` / `assistant_turn`: `sanitized_text` — equivalence-preserving sanitized
  message content (§12).
- `tool_result`: `sanitized_result_excerpt` OR a provenance-linked sanitized content ref —
  bounded, equivalence-preserving (§12).
- per labeled window (§7): `task_ref`, `open_propositions`, `decision_state` — sanitized,
  observable-only.

The judge sees **sanitized** semantic content, never raw. What the judge may see is fixed by
this contract; it is not left to implementation. Semantic *labels* are NOT part of the frozen
schema — they come from the labeling protocol (§11).

## 10. Hard discriminating pairs the corpus MUST contain (round-1)

The corpus is judged on the cases a naive length/repeat heuristic confuses:

- productive-long-generation vs redundant-long-generation
- true loop (stalled/cyclic) vs false-looking-loop-that-later-resolves — the "later
  resolves" fact is a **SUFFIX OUTCOME AUDIT** fact (§5), never written into the prefix GT;
  the prefix label at t stays prefix-bounded.
- looks-complete -> nothing material later vs looks-complete -> blocker / new load-bearing
  evidence later (this pair IS the completion suffix-audit, §5)
- legitimate post-compaction recovery (`KNOWN` + `COMPACTION`, §3) vs genuine stall

A corpus missing these **round-1** pairs cannot qualify any round-1 judge (coverage check,
§13).

**Future (HCSA1-D, NOT part of the round-1 gate):** handoff-worthy context saturation vs
bad-handoff / redo-known-work — deferred with `handoff_readiness` (§6). It is not a round-1
corpus MUST.

## 11. Labeling protocol (leakage-safe, blinded, disagreement-preserving)

- Anchored at decision point t (§5); prefix-bounded; `evidence_progress` over `W(t)`;
  completion sealed then suffix-audited.
- Ground truth is human / owner (semantic); no deterministic proxy is presented as a label.
- **Label-then-measure**: labels frozen before any judge runs.
- **Blinding:** labelers must NOT see candidate judge outputs before producing ground-truth
  labels.
- **Independent second labeler on the hard discriminating subset.**
- **Record, per labeled item:** labeler A; labeler B; agreement/disagreement; adjudicated
  label (if required); reason for adjudication. Disagreement is never silently overwritten.
- Development-set disagreement is evidence used to refine the protocol.
- **Anti-gaming:** disagreement is NEVER resolved by changing labels to improve judge
  performance.

## 12. Privacy / provenance preservation

Four layers, distinct trust levels:

```
raw local evidence      = private, immutable, never tracked by default (source of truth stays local)
normalized local trace  = adapter-derived, provenance-linked, local/untracked
curated sanitized fixture = sanitized + bounded; sanitization must preserve tested-behavior equivalence
public tracked artifact = schema + labels + approved sanitized fixtures only
```

**Sanitization must preserve every equivalence relation relevant to the judgment under
test** — it must neither create nor destroy repetition/novelty signal:

- same source path -> same stable pseudonym; different source paths -> distinct pseudonyms
- event order -> preserved
- tool identity -> preserved
- same-vs-different command relation -> preserved
- same-vs-different result relation -> preserved where required

Retain private provenance sufficient to trace a sanitized fixture back to its raw source
**without publishing local paths, personal identifiers, secrets, or source content.** This
is the first concrete use case for the future **Agent & Context Security** domain.

## 13. Qualification (crux — HCSA1-B, restated, not run here)

- **Safety priority (frozen; not a single FP/FN direction):** No single FP/FN direction
  governs all three judgments — e.g. `evidence_progress`'s unsafe error is a MISS
  (`new_load_bearing` -> `none`), not a false positive, and these labels carry no action
  semantics. The frozen safety priority is to avoid judgments that would later justify
  **suppressing productive or load-bearing work**. The per-judgment unsafe-error families
  below are authoritative.
- **Per-judgment unsafe-error families (frozen; thresholds deferred):**
  - `repetition_state`: productive work labeled `stalled_repeat` / `cyclic` (false-stall).
  - `completion_readiness`: harmful premature-stop FP — `ready` at t when the suffix audit
    (§5) shows stopping at t was harmful.
  - `evidence_progress`: a true `new_load_bearing` labeled `none` (an unsafe miss of
    load-bearing evidence).
- **Coverage / abstention metric (anti-`uncertain`-gaming):** abstention rate (fraction of
  `uncertain`) is reported per judgment as a first-class quantity. A judge cannot earn a good
  unsafe-error score by abstaining: qualification requires bounded abstention, so returning
  `uncertain` everywhere fails coverage rather than scoring FP = 0.
- **Coverage check:** a judge that scores well only because the corpus lacks hard healthy
  cases is NOT qualified.
- **Held-out only; offline; advisory-only downstream; hard limits (step/spend caps,
  authorization boundary, destructive-action block) stay deterministic, never gated by a
  semantic judge.** Numeric thresholds deferred (§17).

## 14. Invariants / guardrails

- Freeze the adapter OUTPUT schema, never native-parser assumptions (§3).
- Compaction: observability (KNOWN/UNKNOWN) separate from occurrence (NONE/COMPACTION/
  INDETERMINATE), valid-state table enforced; UNKNOWN never read as "no compaction" and
  never continuity-proven; UNKNOWN excluded from continuity-requiring qualification (§3).
- Development / held-out firewall; final PASS/FAIL on held-out only; dev never in the
  qualification denominator (§4).
- Leakage-safe, sealed, blinded labeling; disagreement preserved; no label-gaming (§5, §11).
- Decision-relevant evidence defined against the decision state, not surface novelty (§7);
  the judge's permitted semantic surface is part of the frozen schema (§9).
- Two-layer novelty; no frozen scalar (§8).
- Per-judgment unsafe-error families + abstention/coverage metric (§13).
- Four-tier privacy; equivalence-preserving sanitization; raw never tracked by default (§12).
- `uncertain` first-class; no action semantics on labels (§6).
- Observable-only; never depend on private CoT.
- No silent backfill; no post-freeze corpus/label edits without a recorded revision.
- Owner gate between subtracks; DESIGN != build authorization; no shipped pack content change.

## 15. Explicitly NOT in HCSA1-A / NOT YET AUTHORIZED

Corpus construction, semantic judge execution, Jev execution, governor, auto-stop,
auto-handoff, parser implementation, threshold calibration, commit/push/PR. Also: no
cross-session lifecycle expansion (PARK to HCSA1-D), no production skill/pack content change,
no control of any real side effect.

## 16. Gate sequence and evidence handoff

```
Phase 0    = ACCEPTED / CLOSED
Phase 0.1  = ACCEPTED / CLOSED
this draft = pre-freeze contract DRAFT (repair round applied)
   -> EVIDENCE HANDOFF: the actual final bytes of DESIGN.md + PHASE0-RECON.md are
      provided to the owner (the review checks the files themselves, not a summary)
   -> OWNER FREEZE / NO-FREEZE ADJUDICATION
   -> prereg FREEZE (manifest/SHA)                 [NOT YET]
   -> (gated) build: adapter, normalized traces, development/held-out split, curated
      fixtures, labels
   -> HCSA1-B judge qualification (held-out only)
```

Until owner adjudication: **HCSA1-A prereg = NOT FROZEN; corpus construction = NOT
AUTHORIZED; judge execution = NOT AUTHORIZED.**

## 17. Deferred values (explicitly UNFROZEN)

- final corpus N
- held-out qualification FP threshold (and the per-judgment unsafe-error thresholds of §13)
- exact A/B/C corpus composition (real historical / curated bounded excerpts / adversarial
  constructed; mixed, primary must be real sessions)
- whether Structural Novelty and Semantic Evidence Gain ever combine into one scalar

These may be decided **only after development / calibration evidence exists, and before
held-out qualification scoring** (§4).
