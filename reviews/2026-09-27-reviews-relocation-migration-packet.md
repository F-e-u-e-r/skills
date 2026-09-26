# reviews/ relocation — migration discovery packet (design evidence only)

> **This is a discovery snapshot, not a complete consumer inventory and not an execution plan.**

**Status:** DESIGN EVIDENCE ONLY. No `git mv` performed; no migration
authorized. Baseline at authoring: `main` @ `b452914`, canonical battery green.
This packet exists so a future, separately-authorized coordinated migration can
start from evidence instead of re-deriving it. It does not decide a destination.

## The two axes (do not conflate)

- **Content authority:** `reviews/` content is *internal evidence*, not
  canonical doctrine (see `reviews/README.md`).
- **Path surface:** `reviews/` *paths* are a *cross-repo contract* — consumed by
  docs, gate code, hooks, and the design-pack corpus loader. Low content
  authority does NOT imply free relocation.

## Consumer inventory (v1: textual inbound-ref map + one seed-check)

### Tier 1 — runtime / gate-critical (a move BREAKS a gate or a loader)

| Consumer | Referenced path | Kind | Consequence if moved | Required rewrite + test |
|---|---|---|---|---|
| `design-pack/tools/project_corpus.py:25,27` | `reviews/2026-09-26-phase-b-semantic-publication/{public_records.json,THIRD_PARTY_NOTICES.md}` | fixed constant (`os.path.join(root, …)` at :153,:332) | design-pack corpus load fails; checks.py "design-pack production bridge contract (D6-B2.2)" fails | update both constants; regenerate `design-pack/generated/`; re-run checks.py + projection_checks |
| `design-pack/generated/manifest.json`, `generated/README.md` | same path | generated (embeds the path) | manifest points at a dead path | regenerate after the constant change |
| `design-pack/tools/projection_checks.py:262` | `reviews/2026-09-26-phase-b` | regex that FORBIDS SKILL.md referencing it | guard goes stale (forbids the old path) | update the forbidden pattern to the new path |
| `README.md`, `README.zh-Hant.md` | `[reviews/…](reviews/…)` links (README:535,585,591; zh:350,393,399) | rendered markdown links | checks.py "inline relative markdown links resolve" FAILS | update link targets; re-run checks.py |
| `hooks/skill-vetting-advisory.py` + `hooks/test-skill-vetting-advisory.py:1305` | `reviews/2026-07-25-skill-vetting-snapshot-threat-model.md` | hook EMITS the path; test `assertIn`s it | hook points users to a dead path; hook test fails | update the emitted path AND the assertion in lockstep |

### Tier 2 — doc / provenance pointers (break SILENTLY; not gate-caught; in shipped files)

| Consumer | Note |
|---|---|
| `ARCHITECTURE.md:188` | cites `reviews/2026-08-03-routing-contract-design.md` (§6 procedure). Canonical contract; doc pointer. |
| `ROADMAP.md:8,88` | markdown links to reviews/ — NOT gate-checked (unlike README). |
| `skills/*/SKILL.md` + `references/provenance.md` | evidence-provenance citations: cross-model-review (`…-issue115-scored-t4`, `…-campaign-synthesis`), operational-rigor §4 (`…-round5-results`), delegation-and-review, security-architect, skill-vetting, ground-truth-gates. Shipped doctrine. **CAUTION: distinguish REAL citations from ILLUSTRATIVE examples** — e.g. `delegation-and-review §2 "reviews/styling-ledger.md"` is a fictional example inside a rule; do NOT rewrite it. |
| `.github/derived_checks.py:9`, `test-derived-checks.py:5` | docstring citations of `…-pr3-derived-checks-design.md`. |
| `hooks/{gate-credential-destruction,skill_snapshot}.py`, `test-skill_snapshot.py` | docstring citations. |

### Tier 3 — staging (mostly gitignored; 3 whitelisted dirs)

`skills-staging/2026-07-30-{security-enhancement,campaign-ops,starledger-retro}/…` cite `reviews/2026-07-25-skill-vetting-*`. Lower priority.

## grep-does-not-equal-absence findings (path contracts the textual map misses)

- **`reviews/` contains self-executing probe harnesses** (`reviews/2026-08-*/*.py`: static_checks, prefix_checks, scored_checks, closure_checks, run_case, pycache_prefix_probe) that enumerate via `os.listdir` / `os.walk` / `glob` **relative to their own location**. Moving a probe dir as a UNIT preserves self-relative enumeration — BUT a script that computes a repo-root by relative traversal to reach outside its dir (e.g. `closure_checks.py:335` globs `skills/**/*.md` from a computed `REPO`) breaks if the dir's DEPTH changes. **Relative depth is a hidden path-contract.** These are mostly closed-campaign (issue115) harnesses, likely not re-run — low impact, but must not be broken silently.
- No glob-style `reviews/` enumeration found in CI (`*.yml`)/`*.sh`/`*.json`.

## Discovery gaps to close BEFORE executing any migration

1. Per-harness relative-path audit: which `reviews/*/` scripts reach outside their own dir or compute a repo-root; would a depth change break them?
2. Re-verify no other runtime reads `reviews/` paths beyond this set (this map is v1: textual grep + one enumeration seed-check).
3. Resolve the illustrative-vs-real citation split in skill files (never rewrite a fictional example path).

## Candidate destinations (OPTIONS ONLY — not decided; input to the target-architecture design)

- **(i) in-place partition** — `reviews/{decisions,probes,archive}`; keeps the root, sub-partitions. Still updates every consumer (`reviews/X` -> `reviews/probes/X`).
- **(ii) new `evidence/` root** — `evidence/{reviews,probes,historical}`; renames the root; every consumer updates `reviews/` -> `evidence/…`.
- **(iii) hybrid compatibility** — leave referenced paths in place while archiving only unreferenced bulk, or a forwarding layer; less consumer churn, adds a compatibility surface.
- Decision deferred to the target-architecture design (owner).

## Execution requirements (when a migration is authorized — NOT now)

- Path-only (no semantic edits), per `reviews/README.md`'s path-stability contract.
- All Tier-1 and Tier-2 consumers updated in lockstep with the moves; canonical battery green BEFORE and AFTER.
- Historical harnesses: preserve depth, or explicitly accept + document they will not re-run.
- Requires its own authorization; this packet is evidence, not authorization.
