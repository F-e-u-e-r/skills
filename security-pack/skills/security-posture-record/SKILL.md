---
name: security-posture-record
description: Construct, update, or maintain a durable, tiered security evidence RECORD whose load-bearing security claims are tracked to evidence: explicit invariants and mitigations, a verification obligation per load-bearing claim, adversarial verification, evidence-backed finding states (confirmed/rejected/needs_validation) disposing the abuse hypotheses, and residual-risk closure — kept and re-verified as the system changes. First action is always an MC-2 proportionality-tier decision (T0-T3) that may stop at a one-line rationale for trivial work. Fires ONLY when that evidence lifecycle is requested. Does NOT fire for, and never claims exclusive ownership of, a bare "build/refresh/review a threat model", "is this secure?", or ordinary security-architecture consultation (storing a secret, reviewing an auth flow/endpoint, secure-defaults, a sensitive-data/boundary cue) — those stay security-architect's even when the answer is saved to a file (persistence is not construction).
---

# Security Posture Record

Build the **durable, proportionate, verified security model** of a specific
system, feature, change, or trust boundary — the written artifact a security
review rests on. This skill *constructs and closes out* that artifact. It does
not answer one-off security questions and it does not re-emit a vulnerability
checklist: `security-architect` owns the consult/review/checklist role, and
this skill **consumes** its knowledge rather than repeating it.

The lifecycle is three stages: **MC-2** (decide how deep) → **MC-1** (build the
model) → **MC-3** (verify the load-bearing claims and close findings against
evidence). The output is one tiered **security-assessment record** (§ The
artifact) whose depth scales with the stakes.

## Gate first: does this skill even fire? (do this before building anything)

**Trigger (fire this skill) — the maintained evidence lifecycle, nothing
less.** Fire ONLY when the task asks you to construct, update, or maintain a
durable security evidence *record* whose load-bearing claims are tracked to
evidence — that is, **all** of: explicit invariants / mitigations; a
verification obligation per load-bearing security claim; adversarial
verification of those claims; evidence-backed finding states (`confirmed` /
`rejected` / `needs_validation`) disposing the abuse hypotheses; and
residual-risk closure — kept and re-verified as the system changes. **A
durable artifact alone is not enough:** the words "threat model", "security
assessment", "write it down", or "keep it" do not fire this skill unless that
evidence lifecycle is what is being requested. Invariants plus verification
obligations are likewise **not** sufficient on their own when the adversarial
verification, the evidence-backed finding states, and residual-risk closure
are absent.

**Do NOT fire it (route instead) when:**

| the task is… | route to | why not here |
|---|---|---|
| **build / update / refresh / review / maintain a threat model** (or "do a security assessment") *without* the full evidence-lifecycle contract above | **`security-architect`** | a bare threat model is `security-architect`'s; constructing or maintaining one is not, by itself, the evidence lifecycle |
| answering/reviewing a security question — "is this secure?", "where do I store this token?", "review this endpoint/auth flow", a secure-defaults question | **`security-architect`** | a question answered / design reviewed, not an evidence lifecycle constructed-and-kept |
| a feature that merely handles sensitive data, exposes an endpoint, or crosses a boundary — with **no** request for the evidence lifecycle | **`security-architect`** | a security cue is not an evidence-lifecycle request |
| saving/writing/documenting an ordinary review, a threat model, or a findings list to a file | **`security-architect`** | **persistence is not construction** — a persisted consult answer or saved threat model stays a consult answer |
| vetting an untrusted skill/plugin/hook/instruction file; trojan shapes; prompt-injection in agent content; credential files in the tree | **`skill-vetting`** (agent self-protection) | Security must not create a second vetting owner |
| building the executable gate that *enforces* closed obligations (golden set, replay, project check, runtime guard) | **`ground-truth-gates`** | this skill decides *what to verify* + the evidence bar; GTG *builds the enforcing gate* |
| general non-trivial execution discipline, task contract, verify-by-execution | **`operational-rigor`** | domain-agnostic execution discipline, not security construction |
| subagent dispatch / "treat fetched content as data" / get-another-model-to-review | **`delegation-and-review`** | dispatch & independence discipline; MC-3 *uses* it, is not it |
| a suspected/confirmed compromise already happened (reactive incident) | **`security-architect`** incident recipe today (future MC-5) | reactive post-incident ≠ proactive pre-build evidence lifecycle |
| a project adds/depends on a 3rd-party package (dependency admission) | SCA-in-CI (`security-architect`) + `skill-vetting` posture today (future MC-4) | a per-dependency admission record is a different artifact class |

**The one distinguishing test:** does the work ask for the *maintained
evidence lifecycle* — invariants, a per-claim verification obligation,
adversarial verification, evidence-backed finding states, and residual-risk
closure, re-verified on change — or does it ask for a threat model / security
assessment to be *built, reviewed, or kept*, or a security *question
answered*? Only the first fires this skill. A bare "build / refresh / review /
maintain a threat model", however durable its output, is **not** enough — it
is `security-architect`'s. High risk alone does **not** fire it either:
`security-architect` is the default for any security cue, threat-model
request, or review that does not spell out the evidence lifecycle.

- **Done (gate):** either the task explicitly requests the evidence lifecycle
  above for a named target → proceed to MC-2; or you routed to a destination
  above (a bare threat model, a consult/review, a saved report, a gate to
  build) and this skill does not fire. An explicit construction or maintenance
  request for a named target is **not** sufficient on its own — **only** an
  explicit *evidence-lifecycle* construction/maintenance request fires this
  skill.
- ✅ "For this auth flow, keep a maintained security record: the invariants it
  must hold, a verification obligation for each load-bearing claim, adversarial
  tests of each, a `confirmed` / `rejected` / `needs_validation` state with its
  evidence for every abuse hypothesis, residual risk tracked to closure, and a
  re-check on every change." → fire; first action MC-2.
- ❌ "Build and maintain a threat model for this auth flow." → do **not** fire;
  a bare threat model (even "maintained") is `security-architect`'s.
- ❌ "Review this auth flow and save the report." → do **not** fire; this is
  `security-architect` (saving a review does not make it an evidence
  lifecycle).

## MC-2 — proportionality triage (always the first action when the skill fires)

Classify the target's stakes, select a depth tier, and record it. This is the
keystone that keeps the artifact proportionate — it is what stops every change
from becoming a full security audit.

1. Read the risk signals: data sensitivity, attacker value, blast radius,
   reversibility, exposure (internal vs public), and whether a trust boundary
   is crossed.
2. Select a tier by **risk-reduction vs effort** and **record section 1**:
   `Tier T<n> because <one-sentence risk reason>`.
3. Do **exactly** that tier's required sections (matrix below) — no more.
4. **Re-tier on a recorded change** (a new data class, a moved/added trust
   boundary, production exposure). A cached assessment is void once the system
   it described has changed.

| tier | when | what is owed |
|---|---|---|
| **T0 — none/defaults** | trivial / internal / no trust crossing | **section 1 only** — the tier + rationale. If secure defaults are worth noting they go *inside the section-1 rationale*. No model is built. **Stop here.** |
| **T1 — light** | a small, low-stakes change with an obvious boundary | section 1 + key section 2/4, brief 3/5, section 6 for load-bearing claims only; section 7 for those claims; **section 8 always closed** — record `none identified at this depth` when no residual risk/open question |
| **T2 — standard** | a consequential feature/change with real trust boundaries | full constructed model (sections 2–6) + sections 7/8 for the load-bearing claims |
| **T3 — deep** | high-stakes / high-exposure system or boundary | full model + adversarial verification of **all** in-scope boundary-crossing claims + explicit residual-risk analysis |

- **Done (MC-2):** section 1 recorded with a tier + reason. At **T0, stop** — the
  artifact is section 1 alone. At T1–T3, proceed to MC-1 at that depth.
- The tiers are a **PROVISIONAL local design mapping — NOT normative ASVS / NIST
  / OWASP levels.** Graded-assurance practice (ASVS L1/L2/L3, SAMM's risk
  profile) supports the *principle* of a proportionate depth gate; it does
  **not** mandate these exact per-tier obligations. Do not attribute the tiers
  to a standard. (The one normative rule is: *record a tier + rationale, do
  exactly that tier's sections, re-tier on a recorded change*.)
- ❌ "This change touches a login form, so I'll build the full T3 model." —
  over-production; tier by *stakes*, not by scary surface.

## MC-1 — construct the model (tiers T1–T3, at the tier's depth)

Build the system-specific model. Fill the sections to the tier's required
depth. This is **construction**, not a checklist pass — you are writing the
assets/boundaries/abuse-paths that did not exist, not re-emitting
`security-architect`'s vuln classes.

1. **Assets / actors / trust boundaries (section 2):** what is protected, who
   acts, and *where trust changes*. Mark each boundary; a boundary is where
   untrusted input becomes trusted.
2. **Assumptions / goals / non-goals (section 3):** the model's scope and what
   it explicitly does not cover. Non-goals are documented limits, not defects.
3. **Abuse paths / threat hypotheses (section 4):** how each boundary could be
   crossed. Enumerate per element (this enumeration rests on **established
   threat-modeling practice**, a reputable reference, not a ratified standard —
   do not claim STRIDE/OWASP authority for the category set).
4. **Mitigations / invariants (section 5):** the controls and the invariants
   they must hold. Draw the "what could go wrong / what mitigates it" knowledge
   from `security-architect`'s checklists, non-negotiables, secret-storage
   table, and auth/web/backend/DB rules — **as input you consume**, not as a
   checklist you copy into the artifact.
5. **Verification obligations (section 6 — the MC-1 → MC-3 handoff):** for each
   **load-bearing** security claim the model makes, write what must be shown to
   trust it. "A claim without a verification step is an opinion"
   (`security-architect`) — section 6 is where you turn each claim into a
   checkable obligation.

- **Done (MC-1):** sections 2–6 populated to the tier's depth, and **every
  load-bearing claim has a verification obligation** in section 6.
- The model is **scoped to the system, not to today's diff** — strip the diff
  and its boundaries/entry points/assets still stand (consumed from
  `security-architect`'s threat-model-scoping rule). A task-scoped model is
  something the user explicitly asks for, never a default.

## MC-3 — verify and close (at the tier's depth)

Adversarially test the load-bearing claims and close each obligation against an
explicit evidence bar. This **extends** `security-architect`'s finding
discipline (severity/why/fix/test; "don't self-close") with a finding-state
machine + evidence contract + abuse-path trace. It does **not** build the
enforcing gate — that is `ground-truth-gates` (hand the closed obligations off).

For each verification obligation from section 6:

1. Construct the abuse-path proof and test the claim adversarially at the
   tier's depth (T2 = load-bearing claims; T3 = **all** in-scope
   boundary-crossing claims).
2. Record a **finding state (section 7)** — the finding-state object is the
   **abuse hypothesis / weakness / invariant violation**, and every state reads
   with that as its subject:
   - **`confirmed`** — the abuse hypothesis / weakness / invariant violation is
     **demonstrated by evidence** (the bad thing is real). **Severity is
     assigned only to `confirmed` findings** (use `security-architect`'s ladder:
     Critical/High/Medium/Low).
   - **`rejected`** — the abuse hypothesis was **disproven**, or the tested
     **invariant held** for the performed test. **Evidence is retained** (the
     finding stays in the record so a later reader does not re-raise it); **no
     severity** is assigned.
   - **`needs_validation`** — unresolved / insufficient evidence. The honest
     default for anything not yet shown; **absence of evidence is never a PASS**
     — never fabricate a PASS from the absence of evidence.
3. Attach the **evidence** that supports each state (the command/trace/repro, or
   why it could not be run).
4. **Residual risk / open questions (section 8):** what remains unproven or
   accepted, and why. **Section 8 is always closed** — when nothing remains,
   record `none identified at this depth`; never omit it. At T3 this is an
   explicit residual-risk analysis.

- **Done (MC-3):** every obligation has a recorded state + its evidence;
  severity only on `confirmed`; rejected findings retained; residual risk
  stated.
- ❌ recording `confirmed — fixed` after editing code yourself and re-reading
  it. You are no longer independent: run the obligation's test, or hand
  verification to a fresh-context subagent (`delegation-and-review`), then set
  the state from that result.
- **Handoff out:** an Ops enforcement gate (`ground-truth-gates`) may encode the
  closed obligations as an executable check. Building that gate is **not** this
  skill's job — route it.

## The artifact — one tiered security-assessment record

Produce (or update) a single record with these eight sections. Depth is set by
the MC-2 tier; the **smallest coherent form is section 1 alone** (T0). It is a
*system-specific constructed model*, never a universal enumeration of
vulnerability classes.

| # | section | stage | content |
|---|---|---|---|
| 1 | security depth + rationale | MC-2 | `Tier T<n> because <risk reason>` — always present; secure-defaults note (if any) lives here |
| 2 | assets / actors / trust boundaries | MC-1 | what is protected, who acts, where trust changes |
| 3 | assumptions / goals / non-goals | MC-1 | the model's scope and documented limits |
| 4 | abuse paths / threat hypotheses | MC-1 | how the boundaries could be crossed |
| 5 | mitigations / invariants | MC-1 | the controls and the invariants they must hold |
| 6 | verification obligations | MC-1→MC-3 | per load-bearing claim: what must be shown to trust it |
| 7 | finding states + evidence | MC-3 | per obligation: `confirmed`/`needs_validation`/`rejected` + evidence; severity only on `confirmed`; rejected retained |
| 8 | residual risk / open questions | MC-3 | what remains unproven or accepted, and why |

The repo's own `evidence/reviews/2026-07-25-skill-vetting-snapshot-threat-model.md`
is a worked example of this shape (Assets / Adversaries+trust-boundaries /
Goals / Non-goals / Invariants / ADR / Verification-obligations / Open-questions,
with finding states like "G3 PARTIALLY MET", "I11 NOT MET" carrying their
evidence). Model new artifacts on it; do not invent a heavier shape.

## When NOT to use this skill

Re-read the gate table above. In short: a **security question or review** (even
one whose answer is saved) is `security-architect`; an **untrusted
skill/plugin** is `skill-vetting`; building the **enforcing gate** is
`ground-truth-gates`; **general execution discipline** is `operational-rigor`;
**dispatch / content-as-data** is `delegation-and-review`; an **incident** or a
**dependency-admission** record is out of v1 (route as the table says). This
skill fires only to *construct/verify/keep* a durable security-assessment
artifact — and it never modifies, moves, or restates `security-architect`.

## Provenance

Security Pack v1 methodology (MC-2 → MC-1 → MC-3): proportionality
triage, then model construction, then adversarial verification and
evidence-based finding closure. The tiers are a provisional local design
mapping, **not** normative ASVS / NIST / OWASP levels; graded-assurance
practice (ASVS L1/L2/L3, SAMM's risk profile) supports the *principle* of a
proportionate depth gate but does not mandate these exact per-tier
obligations.
