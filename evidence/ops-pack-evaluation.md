# Ops Pack — evaluation

How the **Ops Pack** is tested against its own doctrine, and the current results. Per-surface counts, experiment identities and owner adjudications live in the individual records under [`reviews/`](reviews/); the evidence index is [`README.md`](README.md).

## Evals: testing the pack itself

The pack is tested against its own doctrine ("a rule you cannot test is a
claim") with a private suite of trap tasks — planted out-of-scope bug,
self-contradicting spec, vacuous test, plan-only pressure, embedded
injection, wrong headline numbers — blind-graded with rubrics mapped to
specific pack rules. The fixtures are deliberately **not published**: a trap
task stops measuring anything once models may have seen it, and the first
round showed even a trap-describing *directory name* can tip a model off.

Honest baseline (2026-07-10, 8 arms × 6 tasks, 48 sessions, blind-graded):
**no outcome-level increment from the skills was measurable on 2026 frontier
models at max effort** — the tasks saturated (44/48 perfect scores; the
predicted no-skill failures occurred zero times in any arm). With-skills
runs did differ in process (rules cited by name, pre-declared expected
observations, explicit scope contracts, observed-not-handled ledgers) — at
roughly 1.6× the session time. A second, covert round (14 sessions, one
realistic ticket, mechanically verified and independently re-checked)
reproduced the ceiling and moved all remaining discrimination to the
noticing-and-reporting layer; full numbers and corrections in
[evidence/reviews/2026-07-11-pack-eval-rounds-1-2.md](reviews/2026-07-11-pack-eval-rounds-1-2.md).
The hooks now carry allow+block unit suites but remain unmeasured at the
behavioral-arm level. Treat the pack accordingly: a consistency layer and
an enforcement substrate, not a proven score boost. (This round measured
`ops-pack`'s discipline skills; `design-pack` postdates it and carries its own
smoke-grade probe record in [its section](../README.md#design-pack-the-design-skills).)

Round-4 update (2026-07-24): the successor suite ran a pre-registered
scored campaign at the weak tier (haiku; 12 fixture cells, bare-vs-ruled
arms differing only by an inlined rule excerpt, mechanical
transcript-verified arming, verbatim reply capture, frozen
fixtures/oracles, n=3 per arm). The frontier-tier null above stands
untouched. At the weak tier, exactly ONE cell discriminated (bare 0/3
vs ruled 3/3) — its rule's marker is now labeled probed-in-part
(skill-authoring §6) — and one smoke-round finding (n=1 smoke grade, distinct from the
scored cells) produced the pack's first probe-backed doctrine repair
(the decision-binding fallback in delegation-and-review §1); every other cell floored, saturated, hit the
saturation-veto, resolved NOT-DISCRIMINATED on its extension slots, or
was unscoreable under the pre-registered verdict table. Read it as
measurement working, not as a score boost: results live in the private
ledger and are cited as shape.

House covenant (2026-07-16, adopted from fable-method's "prime directive"
— see acknowledgements): a new behavioral rule ships with the probe or
trap that would have failed without it, or it ships explicitly labeled
`unprobed`. The covenant's instrument is the private suite's successor
round — trap mechanisms adapted from fable-method's published eval
program, re-implemented as fresh private fixtures — owner-run and
unpublished like the rest of the suite.

## Evaluation results

We evaluate Ops Pack with controlled routing and behavioral probes rather than relying only on anecdotal examples.

Current results suggest that **skill availability and routing quality are not the same thing as autonomous skill activation**.

| Finding | Result |
|---|---|
| Autonomous activation | weak |
| Explicit routing | strong overall, surface-specific |
| Task-side T2 intervention | `0/6 → 4/6` |
| Description-side T2 intervention | `0/6 → 0/6` |
| Routeability vs autonomous activation (AE1) | ref gate `11/12`, ordinary activation `0/12` |

* **Explicit routing is substantially stronger than ordinary activation.** In the canonical routing evaluation, the pack correctly handled most expected routing decisions, while ordinary behavioral runs rarely invoked an available skill automatically.
* **Generic activation prompts were not enough.** Two Activation Bridge experiments increased observable skill invocation only modestly, leaving most eligible tasks without an autonomous skill activation.
* **The failure is surface-specific, not pack-wide.** Localization experiments found some task surfaces route reliably while others miss, select neighboring skills, or remain unactivated.
* **Task wording can causally affect routing.** For weak `ground-truth-gates` surfaces, adding explicit trust / verification framing increased correct routing from **0/6 to 4/6** in a small controlled experiment; one surface moved from **0/3 to 3/3**.
* **Changing the skill description did not reproduce that effect.** A reciprocal experiment kept the natural task wording fixed and narrowly expanded the `ground-truth-gates` description. Correct routing on the target surfaces remained **0/6 → 0/6**, while existing strong surfaces were retained. The candidate description was therefore **not shipped**.

**Activation Execution Probe v1 (AE1).** AE1 tested whether tasks that are explicitly routeable to a pack skill also invoke that skill autonomously during ordinary execution. On the preregistered `T4a`/`T4b` surfaces, the contemporaneous explicit-routing reference gate passed (**11/12**), while ordinary execution produced **0/12** expected-skill activations and **0/12** any-Skill activations — an explicit-routeability / autonomous-activation dissociation under the tested AE1 configuration. AE1 does **not** establish a causal effect of the routing instruction or the tool allowlist, that skill descriptions are uninvolved, a population-wide activation rate, or any behavioral skill usefulness or uplift. Design, counts, and interpretation boundary: [evidence/reviews/2026-09-24-ae1-v1-scored-reconciliation.md](reviews/2026-09-24-ae1-v1-scored-reconciliation.md).

These experiments are directional and currently use small per-condition samples, so we treat them as evidence for engineering decisions rather than population-level performance estimates.

The current working conclusion is that the main remaining challenge is **activation and task-surface discrimination**, not a broad need to rewrite skill descriptions. Production skill content remains unchanged unless a controlled experiment supports the change.

Per-surface counts, experiment identities, and owner adjudications for this round: [evidence/reviews/2026-09-18-activation-eval-reconciliation.md](reviews/2026-09-18-activation-eval-reconciliation.md).
