<h1 align="center">Skills</h1>

<p align="center">
  <em>Role-oriented skill packs distilled from real-world experience —<br><strong>reusable skills, not preserved transcripts.</strong></em>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <img alt="3 packs" src="https://img.shields.io/badge/packs-3-7aa2ff.svg">
  <img alt="15 skills" src="https://img.shields.io/badge/skills-15-7aa2ff.svg">
  <img alt="Status: alpha" src="https://img.shields.io/badge/status-alpha-orange.svg">
  <a href="https://github.com/F-e-u-e-r/skills/issues"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
  <a href="https://github.com/F-e-u-e-r/skills/actions/workflows/checks.yml"><img alt="checks" src="https://github.com/F-e-u-e-r/skills/actions/workflows/checks.yml/badge.svg"></a>
</p>

<p align="center"><strong>English</strong> · <a href="README.zh-Hant.md">繁體中文</a></p>

---

This repository collects several focused, role-oriented **skill packs** distilled
from real-world experience. They capture patterns that repeatedly proved useful
across planning, execution, design, review, and verification — consolidated into
reusable skills rather than preserving the full conversations, workflows, or
source material they came from.

Three packs ship today — **15 skills in total**:

| Pack | Focus | Skills | Version |
|---|---|---:|---:|
| **Ops Pack** | Execution governance — rigor, delegation, verification, evidence, review | 10 | 0.3.0 |
| **Planning Pack** | Executable planning contracts and reconciliation (Planning ↔ Ops) | 2 | 0.1.0 |
| **Design Pack** | UI/UX, motion, and design review | 3 | 0.1.0 |

Each pack versions independently. The packs are currently distributed as **Claude
Code plugins** through this repository's marketplace ([Install](#install) below),
alongside **four optional hooks** — repo-level, installed by hand; no plugin
registers them (see [hooks/README.md](hooks/README.md)). Install
any pack alone or in combination.

The packs also evolve from observed failures, contributor experience, open-source
ideas, research, and targeted evaluation. Evidence strength stays explicit: tested
behavior, observed experience, research findings, and unprobed guidance are not
presented as if they were the same thing.

> [!NOTE]
> **Status: early alpha.** Ops Pack is at **Early alpha (`v0.3.0`)**; Planning Pack
> and Design Pack are at `0.1.0`. Rules change as real sessions expose misses, and the
> packs are [measured against their own doctrine](evidence/ops-pack-evaluation.md)
> — honest null results included. Issues and PRs with concrete failure cases are welcome.

**At a glance**

|  |  |
|---|---|
| **3** role-oriented packs | **15** skills in total |
| **4** optional hooks | **CI** consistency checks on every push |
| **Status** early alpha | **Evidence** experience + research + controlled evaluation, nulls included |

## Contents

- [Install](#install) · [How these packs are built](#how-these-packs-are-built) · [`ops-pack`](#ops-pack-the-discipline-skills) · [`planning-pack`](#planning-pack-the-planning-skills) · [`design-pack`](#design-pack-the-design-skills)
- [Architecture & stability](#architecture--stability) · [Maintainer notes](#maintainer-notes) · [License](#license)

## How these packs are built

The packs are **distilled from experience**, not transcribed from it. The pipeline:

1. **Start from real work** — operating sessions, observed successes and failures,
   maintainer and contributor experience, plus useful open-source ideas, targeted
   repository study, and focused research.
2. **Consolidate into role-oriented skills** — recurring patterns become small,
   reusable skills rather than preserved conversations or whole source projects.
3. **Check provenance and licensing** — ideas are filtered on merit, not copied
   wholesale; sources and permissive-license notices are tracked.
4. **Review load-bearing changes independently** — the author is not the judge.
5. **Gate what can be gated** — deterministic consistency checks and, where
   practical, controlled routing / behavioral / execution probes.
6. **Keep evidence strength explicit** — tested behavior, observed experience,
   research, and still-unprobed guidance stay labeled as what they are, and
   limitations and null results are kept rather than hidden.

The throughline is distillation from experience — not a claim that every rule has
experimental proof.

## Install

The packs are currently distributed as **Claude Code plugins**. This repository
is the **marketplace**; add it once, then install whichever plugins you want. Install targets use `plugin@marketplace`, and the marketplace ID is
`opus-pack`:

```
/plugin marketplace add F-e-u-e-r/skills
/plugin install ops-pack@opus-pack
/plugin install planning-pack@opus-pack
/plugin install design-pack@opus-pack
```

`ops-pack@opus-pack` installs the discipline plugin (10 skills);
`planning-pack@opus-pack` installs the planning plugin (2 skills);
`design-pack@opus-pack` installs the design plugin (3 skills). Install any,
or all three. Skills arrive namespaced (`ops-pack:operational-rigor`,
`design-pack:ui-design-craft`, …) and update via `/plugin marketplace update`.
No plugin registers the hooks — they change harness behavior, so
installing them stays a manual, per-user decision (see
[hooks/README.md](hooks/README.md)).

**Or copy skills into place** — globally, or per project. Each block is
self-contained:

```bash
# ops-pack (discipline) skills, global:
mkdir -p ~/.claude/skills && cp -R ops-pack/skills/* ~/.claude/skills/
# planning-pack (planning) skills, global:
mkdir -p ~/.claude/skills && cp -R planning-pack/skills/* ~/.claude/skills/
# design-pack (design) skills, global:
mkdir -p ~/.claude/skills && cp -R design-pack/skills/* ~/.claude/skills/
# per project instead: swap ~/.claude for <repo>/.claude
```

Pick ONE method per plugin: installing a plugin AND copying its skills makes
every skill available twice (`ops-pack:<skill>` and `<skill>`), and automatic
selection may pick either copy. Skills load on demand: only the description
occupies context until triggered.

> **Upgrading from the `opus-pack` plugin id.** The discipline plugin was renamed `opus-pack` -> `ops-pack`; the marketplace id intentionally stays `opus-pack`, so the install id is now `ops-pack@opus-pack`. If you enabled `opus-pack@opus-pack` before the rename, run `/plugin marketplace update opus-pack` and then, once, `/plugin install ops-pack@opus-pack` -- your enablement carries over (the old id shows as "Renamed to ops-pack" until you do) and no skills are lost. Enablement enforced through managed (admin) settings does not auto-migrate; an administrator must update it there.

## `ops-pack`: the discipline skills

| Skill | What it does |
|---|---|
| `operational-rigor` | Execution discipline: task contract, action gating, verify-by-execution, honest completion |
| `delegation-and-review` | Delegation, two-critic review, escalation ladder, long-task handoff, injection defense |
| `ground-truth-gates` | Executable verification gates (golden / replay / project); ships a runnable `template/` |
| `skill-authoring` | Executable-rule format for weaker models; provenance, decay, memory architecture |
| `security-architect` | Practical security for a non-expert owner: auth, secrets, web/backend/DB, untrusted ingestion |
| `product-roadmap` | Product-owner lens: evidence before opinion, Now/Next/Later, milestones, task split |
| `personal-goal-planning` | Coach-style tiered personal / career goals with a weekly review loop |
| `domain-evidence-discipline` | Evidence discipline for non-code deliverables (marketing / research / data / ops) |
| `skill-vetting` | Vet a third-party skill / plugin / hook for trojan patterns before it runs |
| `cross-model-review` | Adversarial review from a *different model family* before a load-bearing merge |

<p><img alt="Ops Pack version v0.3.0" src="https://img.shields.io/badge/version-v0.3.0-orange.svg"></p>

**The discipline lineage** — the ten highest-leverage principles, what was
deliberately dropped, how skills and agents actually get invoked, and how the
pack degrades — lives in [`ops-pack/README.md`](ops-pack/README.md). Optional
repo-level hooks for hard enforcement are documented in
[`hooks/README.md`](hooks/README.md); evaluation evidence in
[`evidence/ops-pack-evaluation.md`](evidence/ops-pack-evaluation.md).

## `planning-pack`: the planning skills

| Skill | What it does |
|---|---|
| `planning` | An executable work contract before building: framed intent, testable requirements, scoped non-goals, dependency-ordered tasks; depth D0–D3 (D0 stays with `operational-rigor`) |
| `plan-reconciliation` | Reconcile an approved plan with reality once execution starts — revise when it no longer fits, or close when done — with evidence |

`planning` and `plan-reconciliation` form the **Planning Pack** (Planning ↔ Ops):
they own *what to build and how the plan changes*, while `ops-pack`'s
execution-discipline skills own *carrying it out*. A Planning artifact is never
execution authorization, and Planning depth never discounts execution rigor.

**Known weak-tier limitation (QUALIFIED-ADOPTABLE).** The Planning Pack ships as **QUALIFIED-ADOPTABLE: 13/14
clean behavioural claims, 1 documented weak-tier limitation, 0 harmful behaviours, D0 preserved**. The one open claim is a documented weak-tier limitation, stated here rather than omitted. The limitation: `plan-reconciliation` reliably preserves the revalidation /
re-approval / Ops-authorization gate, but on weaker executor tiers it does not reliably perform absence-sensitive
whole-plan orphan detection itself (it tends to describe or request the revalidation rather than carry it out).
The failure mode is fail-safe — under-detection defaults to "cannot resume / escalate", never a false "safe to
resume".

> **Migration — Planning moved to its own plugin (ops-pack 0.3.0).** `planning` and `plan-reconciliation` shipped inside the `ops-pack` plugin through v0.2.0; from `ops-pack` 0.3.0 they ship as the separate **`planning-pack`** plugin (version 0.1.0). This is a **documented namespace migration, not transparent compatibility**: there is no cross-plugin skill-rename bridge, so a user who had `ops-pack@opus-pack` enabled and updates **without** installing `planning-pack` will find those two skills **simply absent**. That absence is **expected and announced here — it is not a silent loss**. To restore the full set, install **both** `ops-pack@opus-pack` **and** `planning-pack@opus-pack`; after installing `planning-pack`, `planning` and `plan-reconciliation` return, exactly once, under the `planning-pack:` namespace. The full planning + execution setup needs both installs. See `ARCHITECTURE.md` §3.


## `design-pack`: the design skills

Three design-craft skills applying the same doctrine style — numeric budgets,
prohibited patterns, observable gates — to visual design work. Install it like
any plugin ([Install](#install) above); it versions independently
(currently 0.1.0). The skills stand on their own — `design-review-gate` carries
two load-bearing ops-pack clauses verbatim — and are sharper with `ops-pack`
alongside, but don't require it.

| Skill | What it does |
|---|---|
| `ui-design-craft` | UI composition and visual craft: layout, hierarchy, typography, color, state quality, anti-generic design |
| `motion-craft` | Motion behavior: timing, easing, gesture/spring, choreography, reduced-motion, performance |
| `design-review-gate` | Structured design review turned into measurable, ranked findings |

**How it stays grounded.** The guidance is not hand-copied across three skills:
it projects from a single canonical corpus of design semantics, through a
deterministic build, into skill-local reference files each `SKILL.md` loads
selectively. The corpus is the primary authority; pack-local extensions add
production guidance beneath it. Full corpus / projection architecture:
[`ARCHITECTURE.md`](ARCHITECTURE.md).

**Evidence.** `ui-design-craft` / `motion-craft` gates and `design-review-gate`
§4 were probe-tested at smoke grade (fresh weak-tier agent, bare-vs-ruled arms,
expected-before-actual) on private fixtures; §§1–3 of the review loop are not
yet probed, and the record keeps one voided round and one NULL (both in the
skills' own provenance notes). The hex and font-fashion bans decay fastest —
re-verify each model generation. An independent
[Impeccable](https://github.com/pbakaus/impeccable) compatibility study
(observations only, vendored into nothing) lives under
[`research/design-pack/2026-09-impeccable-compatibility-study/`](research/design-pack/2026-09-impeccable-compatibility-study/).

## Architecture & stability

Full normative contract: **[`ARCHITECTURE.md`](ARCHITECTURE.md)** — the
canonical source for tiers, stability, pre-1.0 migration, plugin dependency
classes, adjacent-skill rules, routing-contract changes, and the reference
grammar. This section is a summary projection; **on any inconsistency,
`ARCHITECTURE.md` (English) is authoritative.**

**Skill tiers** (the agent-discipline skills in `ops-pack` and `planning-pack`; canonical map in
[`metadata/skill-tiers.json`](metadata/skill-tiers.json)):

<!-- BEGIN GENERATED SKILL TIERS -->
| Tier | Skills |
|------|--------|
| Core (7) | `operational-rigor`, `delegation-and-review`, `ground-truth-gates`, `cross-model-review`, `skill-authoring`, `skill-vetting`, `security-architect` |
| Domain adapter (5) | `product-roadmap`, `personal-goal-planning`, `domain-evidence-discipline`, `planning`, `plan-reconciliation` |
<!-- END GENERATED SKILL TIERS -->

Core skills are the shared agent-execution doctrine; a domain adapter applies
that discipline to a narrower domain. Skill tier and plugin dependency class are
separate axes.

<!-- BEGIN GENERATED PLUGIN DEPENDENCIES -->
**Plugin dependency class.** `design-pack` is **`recommended-with ops-pack`**:
its skills complete their primary workflows on their own (`motion-craft` has no
cross-pack dependency; the two load-bearing cross-pack clauses are carried
verbatim and bind on their own), while `ops-pack` adds the extra rigor its
pointers name. `planning-pack` is **`recommended-with ops-pack`**: it produces a usable plan on its own but names the Ops execution safeguards (authorization, evidence, non-reversal) it hands off to. See `ARCHITECTURE.md` §4.
<!-- END GENERATED PLUGIN DEPENDENCIES -->

**Stability, in one line:** published skills are stable interfaces and evolve
**additively by default** — new capability arrives as new skills or plugins, not
by removing, renaming, relocating, or narrowing the trigger scope of an existing
one; the only breaking-migration window (deprecation notice + transition window +
compatibility coverage, completed not merely announced) is strictly before the
source plugin's 1.0 (plugins version independently), and after that 1.0 published
skills stay indefinitely with no pre-authorized break path. Details in
`ARCHITECTURE.md` §§2–3.

Detailed evaluation records, provenance, and research history live under
[`evidence/`](evidence/README.md) (including
[`evidence/ops-pack-evaluation.md`](evidence/ops-pack-evaluation.md) and
[`evidence/provenance.md`](evidence/provenance.md)) and [`research/`](research/).

## Maintainer Notes

Before pushing, run `python3 .github/checks.py` — the same consistency gate
CI runs (skill frontmatter, version agreement across all four sites plus the
plugin manifests, README relative links, zero-width/bidi sweep; the hook
test suites run as separate CI steps). Standing invariant: the plugin
package must never declare or register hooks (no `hooks/hooks.json`, no
hooks field in `plugin.json`) — the consent posture stated in the install
section depends on it.

This working tree may hold two identical skill sets: `ops-pack/skills/` is the publish
source; `.claude/skills/` is the local live install and is ignored by git. Edit
any SKILL.md → sync the other copy (`cp -R ops-pack/skills/. .claude/skills/`) and, before
pushing, diff per published skill so local project skills don't read as drift:
`for d in ops-pack/skills/*/; do diff -rq "$d" ".claude/skills/$(basename $d)"; done`. The
loop only checks dirs still present in `ops-pack/skills/` (and `cp -R` never deletes), so
when you remove or rename a published skill, delete its old dir from
`.claude/skills/` by hand in the same change. Edit
either README → mirror the change in the other language.

Release naming: every `plugin.json` version bump gets a matching `vX.Y.Z` git tag
and a GitHub Release (marked pre-release while the pack is alpha), and the README
version badge reads `vX.Y.Z`. Tags before `v0.1.16` used the legacy `alpha-X.Y.Z`
form; intermediate versions were never individually tagged, and `v0.1.16`
is the first canonical release of record.

## License

The skill packs in this repository are released under the [MIT License](LICENSE)
— Copyright (c) 2026 F-e-u-e-r.

It incorporates and adapts third-party work under permissive licenses (MIT and
Apache-2.0); the copyright and permission notices those licenses require to
travel with the code are collected in
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md). The most concrete case is
the `verify-before-stop` hook — a derivative of MIT-licensed code by Curtis Chou
(and, upstream, Miguok). No copyleft (GPL/AGPL/LGPL) exists anywhere in the
chain. The `guideline *.txt` source drafts are private source material (the
owner's, plus firaen22's private note) and are not distributed
(excluded via `.gitignore`).

Full source history and acknowledgements: [`evidence/provenance.md`](evidence/provenance.md).
