# Post-merge validation of PRs #25–#29 — two-family review and fixes (2026-07-16)

The owner asked for a fresh validation of everything merged while the prior
session was absent — the net diff of PRs #25 (README per-skill sync check),
#26 (27 incident-mined rules across 5 files), #27 (version bump), #28
(external-systems split), #29 (mechanism-verification rule) — followed by a
cross-family gate on any fixes. Reviewers, per the owner's naming and a
session-time dry-run probe of each CLI: **grok-4.5 (`--reasoning-effort
max`)** and **gpt-5.6-sol (`model_reasoning_effort=max`)** — both a
different family from the author of the work under review (all five PRs were
authored by Claude-family agents) and from the dispatching session (also
Claude). Each PR had already passed a two-family gate at merge time; this
pass re-checked the merged state with fresh eyes, per the pack's own
prior-approval-is-not-evidence stance.

## Dispatcher pre-pass (verified by execution before the external round)

- The six rules PR #28 moved into `references/external-systems.md` are
  word-identical to the removed §4 text after the two documented `§4`
  spell-outs (normalized word-level diff of `5b47ea7`).
- No dangling references to the moved rules anywhere else in the pack;
  skill-authoring §7 really contains the ~150-line compaction trigger the
  reference file cites.
- The "4 of the 27 rules" claim in skill-authoring's new provenance matches
  PR #26's review thread exactly (four "incorrect mechanism" blockers, fixed
  in `0ab59a3` before merge).
- Version badge, zh-TW mirror, and a zero-width/bidi Unicode sweep: clean.
- **F1 (dispatcher's one finding):** `.claude/skills/skill-authoring/SKILL.md`
  (repo-local live install, gitignored) was missing PR #29's additions — a
  violation of the README maintainer rule PR #25 had just sharpened. The
  global `~/.claude` install and hooks were in sync.

## Round 1 — both families reviewed the net diff `87662b2..HEAD`

Verdicts: grok-4.5 `FIX: 1` (+2 nits); gpt-5.6-sol `FIX: A1–A11, F1`.
Both adjudicated F1 **AGREE** (executed afterward: `cp -R skills/.
.claude/skills/`, per-skill diff loop now empty). Every external finding was
reproduced or refuted against the actual text before any fix; dispositions:

| finding | disposition |
|---------|-------------|
| grok1 = A2 — `df` presented as a sufficient mount check | **Fixed** (both families independently). Reproduced: `df` exits 0 on an unmounted ordinary directory and reports the containing filesystem; on macOS `mountpoint`/`findmnt` don't exist, so `df` is the one command agents can always reach for. §2 now: `mountpoint -q`/`findmnt` — exit status is the answer; `df` — never gate on exit code, compare the reported device to the expected volume. |
| grok2 — two-dot check stated only empty⇒landed | **Fixed** (nit): non-empty is inconclusive, never grounds for re-applying the branch. |
| grok3 = A11 — fire-path "synthesize" vs golden "never synthesis" | **Fixed** (both families independently): synthesized firing inputs go to the test suite as a labeled synthetic set, never into the captured golden/replay corpus. |
| A1 — sync loop blind to removed/renamed published skills | **Fixed** in both READMEs: on remove/rename, delete the old dir from `.claude/skills/` in the same change. |
| A3 — timeout rule vs enclosing hard deadline | **Fixed**: below-tail deadline ⇒ no timeout value fixes it; restructure or accept-and-meter as a recorded decision. |
| A4 — error→retry amplifies provider outage | **Fixed**: short-TTL cooldown marker — typed non-answer, never served as a value. |
| A5 — advance-signal empty vs valid empty answer | **Fixed**: typed failure signal, mirrors the cache rule's validated-known-empty. |
| A6 — DST gap/fold policy stated but never executed | **Fixed**: ≥1 DST-observing TZ; execute the policy on ≥1 gap and ≥1 fold instant. |
| A7 — "await side effects" vs webhook ack deadline | **Fixed**: "await" = the durable handoff, not long-running processing; cross-ref to security-architect's webhook rule. |
| A8 — dedup marker and enqueue as two ops | **Fixed**: the created row IS the enqueued event (one op = handoff + dedup); pre-handoff markers forbidden with the crash scenario named. |
| A9 — expiring spend hold after an unknown-outcome charge | **Fixed**: reconcile-before-reclaim (query by idempotency key, or retry reuses the SAME key); expiry never converts "outcome unknown" into "never happened". |
| A10 — "calibrate difficulty per arm"; "every arm passes measures nothing" | **Partial**: wording fixed to calibrating the SHARED case set (per-arm tuning destroys comparability) and "measures nothing on the pass/fail axis". The scores/cost/latency half was rejected as out of context — the paragraph governs the golden runner as a case-based pass/fail grader. |
| F1 — stale repo-local live-install copy | **Executed** (not committable — gitignored path). |

Observed, not addressed (pre-existing, outside the reviewed range): README
line ~330 "the keep-in-sync contract above" — the Maintainer Notes section
sits below that line.

## Round 2 — fix verification on `cross-model-validation-fixes`

Verdicts: grok-4.5 `PROCEED` (all 13 dispositions CLOSED, the A10
partial-reject explicitly not contested, one nit); gpt-5.6-sol
`FIX: A4, A5, A8, A9, A10, B1, B2, B3` — four contests of round-1 fixes plus
three fresh findings, each a one-property-flipped variant of the fixed
scenario (the exact failure shape skill-authoring §2's new
mechanism-verification rule describes). Adjudications:

- **A9 contest — accepted (the important one).** Same-key retry only
  prevents the provider double-charging THIS request; releasing an
  unresolved hold still lets other requests consume budget a
  landed-but-unknown charge already spent — cap breach with no double
  charge anywhere. Now: reconcile resolves the hold to spent/failed; until
  resolved it stays held; expiry escalates to an alert, never a silent
  release.
- **B3 / A8 contest — accepted.** The enqueue-row-as-dedup-key fix left the
  row's lifecycle unstated: a worker deleting the consumed row deletes the
  dedup key, so a late redelivery (ack lost in transit) reprocesses. Now:
  the row (or a completed-state marker) outlives the platform's retry
  horizon.
- **B1 (grok's nit = codex's must-fix) + B2 — accepted.** The "three
  states" enumeration didn't name the cooldown and the bullet title
  ("never cache a failure") superficially forbade it; the fallback chain's
  terminal result was still a raw empty. Now: "never cache … *as an
  answer*", four entry kinds, and the terminal all-tiers-failed result
  keeps its failure type at the chain's outward interface.
- **A4 escalation — partial.** Failure-domain scoping of the cooldown
  accepted (a provider-wide outage cools the provider, not one key at a
  time). The in-flight lease / single-flight mandate declined as backlog:
  the residual is a bounded one-producer-latency stampede window, not
  standing reader-amplification, and the cited incident doesn't support
  mandating request-coalescing machinery in this reference.
- **A10 contest — accepted; it exposed a real ambiguity.** "Every arm
  passes" read two ways (each arm clears the gate vs. every case passes in
  every arm); 91% vs 100% both clearing a 90% gate is a meaningful score
  comparison. Now: halt only at the same ceiling/floor (identical outcome
  vectors); between the extremes, compare pre-registered per-arm scores.

## Round 3 — final closure round

Mid-round CLI drift, recorded per the skill's volatility rule: the grok CLI
(now 0.2.101) stopped accepting `--reasoning-effort max` between round 2 and
round 3 — rounds 1–2 ran at max; round 3 ran at `high`, the highest tier the
CLI now exposes. Identity evidence throughout is the requested `-m` +
tool status, not self-report.

Verdicts: grok-4.5 (high) `PROCEED` — every round-2 item CLOSED, no new
defects, and the A4 single-flight decline judged justified ("residual is
bounded, not standing amplification"; filed as BACKLOG). gpt-5.6-sol (max)
`FIX: A4` — everything else CLOSED, no new defects, one remaining contest
with a quantified scenario: before the FIRST failure completes, concurrent
misses reach the producer at traffic × producer-timeout volume (e.g.
10k req/s × 30s ⇒ up to 300k calls) with no admission bound.

**Final A4 adjudication (dispatcher):** the scenario's arithmetic is real,
and the two lenses disagree only on where the bound must live. In this
pack's system the money bound on a paid surface is already mandatory and
lives in security-architect's spend/abuse section (atomic check-and-decrement
cap chain on every unauthenticated paid path) — the cache cooldown is a
retry-suppression layer, not the admission or spend-control layer. Fixed by
naming exactly that in the rule: the cooldown bounds retries, not first
admission; the pre-marker window is traffic × producer-timeout; the money
bound is always the atomic spend-cap chain (cross-ref), and an admission
bound (single-flight / concurrency cap) is added when the producer cannot
tolerate that window. This closes codex's valid kernel (the rule no longer
implies the cooldown alone bounds the window) without mandating
request-coalescing machinery doctrine-wide (grok's justified-decline
judgment). Mandatory single-flight remains BACKLOG for the owner.

## Gate summary

- grok-4.5: round 1 `FIX: 1` → round 2 `PROCEED` → round 3 `PROCEED`.
- gpt-5.6-sol: round 1 `FIX: A1–A11, F1` → round 2 `FIX: A4, A5, A8, A9,
  A10, B1, B2, B3` → round 3 `FIX: A4` with all else CLOSED; A4's valid
  kernel fixed by cross-reference + window naming, residual
  machinery-mandate adjudicated BACKLOG with both models' reasoning
  recorded above.
- Round cap (2–3) reached; no thrash — codex's contests converged
  monotonically (11 → 3 fresh + 4 contests → 1 contest), each round-2/3
  contest a one-property-flipped variant of a round-1 fix, which is the
  failure shape skill-authoring §2's new mechanism-verification rule
  predicts for exactly this kind of work.
- Every fix was re-synced into the repo-local live install
  (`.claude/skills/`, gitignored) after each round; the per-skill diff loop
  returns empty.
- Zero-width/bidi Unicode sweep on all changed files after the final edit:
  clean.

BACKLOG (owner's call, non-blocking): optional single-flight / in-flight
lease guidance for the cold-miss stampede window; README line ~330's
"the keep-in-sync contract above" direction word (pre-existing, outside
the reviewed range).
