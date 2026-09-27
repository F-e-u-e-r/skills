# Q4 — Exhaustive `reviews/` migration manifest (DESIGN EVIDENCE ONLY)

> **Read-only audit. No `git mv`, no repo edit performed. This maps a FUTURE,
> separately-authorized migration; it does not perform one.** Baseline: `main` @
> `25cefe4` (verified `git rev-parse HEAD`), working tree clean except one
> untracked file (`reviews/2026-09-25-hcsa1-b0-.../DESIGN.md`).

Supersedes the v1 discovery snapshot (`reviews/2026-09-27-reviews-relocation-migration-packet.md`)
with an exhaustive inventory. Applies the adjudicated target IA
(`reviews/2026-09-27-target-ia-architecture-design.md`) EXACTLY, classifying in
order: (1) **authority/ownership** — canonical machine-consumed data → `corpus/`;
canonical instruction (`skills/`, `ARCHITECTURE.md`) stays; (2) **artifact role**
— human review/adjudication/design → `evidence/reviews/`; measurement campaign /
runnable evidence unit → `evidence/probes/`; (3) **lifecycle** — recorded as
METADATA on the entry, never a directory.

## Classification rule actually applied (and the one refinement)

The IA's review-vs-probe split is clean for pure-doc and pure-campaign dirs, but
several `reviews/` dirs bundle a human review/design/disposition doc AND a
runnable checker in one directory. Refinement used here, aligned with the IA's
own "closed scored campaign … 'probe' is its identity … preserve the unit and
its depth": **a directory that contains a runnable `.py` evidence/verification
unit is classified `probe`** (the runnable unit + its depth dependency is the
migration-load-bearing property), with the human-doc content noted. Genuinely
dual-identity dirs are marked **MIXED** and surfaced in ESCALATE §E-2.

---

## COVERAGE STATEMENT (read this first)

- **`reviews/` paths enumerated: 63 top-level units** = 62 tracked (44 dated
  subdirs + 18 loose top-level files) + 1 untracked dir (`hcsa1-b0`). These
  comprise **1650 tracked files + 1 untracked file** (`git ls-files reviews/ | wc -l` = 1650).
  Every top-level unit appears as a row below. Sub-entries (issue115 slot dirs,
  fixtures, rubrics, raw/*, verdicts/) are classified at the UNIT level per the
  task; verified they carry data only, no path logic (only `.py` files carry
  logic — see next bullet).
- **Harness scripts audited: 31 of 31** (`git ls-files 'reviews/**/*.py'` = 31;
  **zero `.sh`**). Every one was swept for depth/outside-dir signals
  (`parents[`, `__file__`, `os.path.dirname`, `os.walk`, `os.listdir`, `glob`,
  `REPO`, `ROOT`, `HERE`, `../`, `abspath`, `realpath`, `join(`, `toplevel`,
  `subprocess`, `cwd`, `open(`, `skills/`, `reviews/`). The 10 needing
  disambiguation had **every path-handling line read**. [verified: ran
  `git ls-files` + per-file grep on all 31]
- **External consumer sites found: 68 distinct file:line citations** = 67 from
  the literal seed grep (`git grep -n "reviews/" -- ':(exclude)reviews/'`) + **1
  found ONLY by the segment-form sweep** (`hooks/test-skill-vetting-advisory.py:1309`,
  `os.path.join(REPO, "reviews", "…")` — invisible to a literal `reviews/` grep).
- **Internal cross-references within `reviews/`: 78 hits** (`git grep -nE
  "reviews/20…" -- 'reviews/**'`), mapped in §Internal-Xref.
- **What I READ IN FULL:** both authority docs; `reviews/README.md`;
  `.github/checks.py` link-validation logic (§383-402); the illustrative-example
  context (`delegation-and-review/SKILL.md:460-478`); the Tier-1 hook assertion
  context (`test-skill-vetting-advisory.py:1300-1312`); the full path-handling of
  the 10 disambiguated harnesses; the shape of every ambiguous no-`.py` finding
  dir.
- **What I only GREPPED (bounded):** the ~50 `provenance.md`/`SKILL.md` citation
  lines (one line + existence-test each, not full-file reads — real/illustrative
  decided by on-disk existence, a verifiable discriminator); the 1650 leaf
  evidence files were enumerated + unit-classified, NOT individually opened
  (verified they are data: no `.py`/logic among them beyond the 31 harnesses).
- **Finder exhaustion:** literal-seed, segment-form-all-tracked, untracked-tree,
  absolute-path, and bare-dir finders were run; the last **4 consecutive rounds
  surfaced zero NEW external consumers** beyond the single `:1309` catch → no-new-
  consumer concluded per the two-empty-rounds rule.
- **Bounded-out:** `design-mining/` is **gitignored** (`.gitignore:16`) and
  contains **zero `reviews/` references** [verified: `git check-ignore -v` +
  `grep -rlE`]; excluded from migration scope.

---

## MASTER TABLE — one row per `reviews/` top-level unit

Legend: **Class** = corpus | review | probe | MIXED. **Depth?** = does a script
in the unit compute repo-root by relative traversal / reach outside its own dir?
Consumers list is `file:line`. "→ rewrite" names the required edit + the gate/test
that re-runs.

### Group A — CORPUS (canonical machine-consumed data)

| Current path | Class | Lifecycle | Target path | Depth? | Inbound consumers (file:line) | Required rewrite + gate/test | Illustrative-not-rewrite |
|---|---|---|---|---|---|---|---|
| `reviews/2026-09-26-phase-b-semantic-publication/` (2 files: `public_records.json`, `THIRD_PARTY_NOTICES.md`) | corpus | current / production input | **TARGET ownership `corpus/design-pack/` — but THIS ROUND: leave-in-place-pinned** (deferred to a separately-authorized corpus relocation, pending the packaging-surface gate) | no | **TIER-1.** `design-pack/tools/project_corpus.py:25,27` (fixed constants, joined at `:153,:332`); `design-pack/generated/manifest.json:5,13`; `design-pack/generated/README.md:4`; `design-pack/tools/projection_checks.py:262` (regex FORBIDS SKILL.md citing it) | **This round: NO rewrite (pinned).** On the deferred corpus move: update both constants; **regenerate** `design-pack/generated/` (never hand-edit); update the `projection_checks.py:262` forbidden pattern to the new path; re-run `checks.py` (D6-B2.2 "design-pack production bridge contract") + `projection_checks.py` + `design_pack_checks.py` | — |

### Group B — LOOSE REVIEW records (human reasoning / design / adjudication → `evidence/reviews/`)

| Current path | Class | Lifecycle | Target path | Depth? | Inbound consumers (file:line) | Required rewrite + gate/test | Illustrative |
|---|---|---|---|---|---|---|---|
| `reviews/2026-07-07-fresh-context-review.md` | review | historical | `evidence/reviews/2026-07-07-fresh-context-review.md` | no | none found | none | — |
| `reviews/2026-07-07-guideline-6-mining.md` | review | historical | `evidence/reviews/…` | no | none found | none | — |
| `reviews/2026-07-08-community-sources-and-advisor-rung.md` | review | historical | `evidence/reviews/…` | no | none found | none | — |
| `reviews/2026-07-09-fable-skills-research-review.md` | review | historical | `evidence/reviews/…` | no | none found | none | — |
| `reviews/2026-07-11-pack-eval-rounds-1-2.md` | review (eval writeup) | historical, still-cited | `evidence/reviews/2026-07-11-pack-eval-rounds-1-2.md` | no | **TIER-1 (gate link).** `README.md:535` (link), `README.zh-Hant.md:350` (link); `README.md:322` (prose), `README.zh-Hant.md:322` (prose); `skills/delegation-and-review/references/provenance.md:19`; `skills/security-architect/references/provenance.md:14` | rewrite README **links** :535/:350 → re-run `checks.py` "inline relative markdown links resolve"; rewrite prose :322/:322 (silent); update 2 provenance.md pointers | — |
| `reviews/2026-07-12-cross-model-review-skill-review.md` | review | historical | `evidence/reviews/…` | no | `skills/cross-model-review/references/provenance.md:14` | update provenance pointer (silent) | — |
| `reviews/2026-07-16-post-merge-validation-pr25-29.md` | review (validation) | historical | `evidence/reviews/…` | no | `skills/ground-truth-gates/references/provenance.md:31`; `skills/operational-rigor/references/external-systems.md:302`; `skills/operational-rigor/references/provenance.md:44`; `skills/security-architect/references/provenance.md:36` | update 4 provenance/reference pointers (silent) | — |
| `reviews/2026-07-25-skill-vetting-round8-design.md` | review (design) | historical (design, unimplemented) | `evidence/reviews/…` | no | `skills/skill-vetting/SKILL.md:238,263`; `skills-staging/2026-07-30-security-enhancement/MANIFEST.md:100`, `skill-vetting-hardening-archaeology/SKILL.md:41,169`, `:220` (glob `reviews/2026-07-25-skill-vetting-*.md`), `skill-vetting-security-invariants/SKILL.md:241`, `START-HERE.md:40` | update `skill-vetting/SKILL.md` (shipped doctrine) + Tier-3 staging cites incl. the **glob** at `:220` | — |
| `reviews/2026-07-25-skill-vetting-snapshot-threat-model.md` | review (threat model) | historical, live-cited | `evidence/reviews/2026-07-25-skill-vetting-snapshot-threat-model.md` | no | **TIER-1 (hook + hook test).** `hooks/skill-vetting-advisory.py:9` (EMITS path); `hooks/test-skill-vetting-advisory.py:1305` (`assertIn` on emitted src) **and `:1309`** (`os.path.isfile(os.path.join(REPO,"reviews","…"))` — SEGMENT-FORM, literal-grep-invisible); `hooks/skill_snapshot.py:18`, `hooks/test-skill_snapshot.py:4` (docstrings); `README.md:460` (prose); `skills/skill-vetting/references/provenance.md:45`; skills-staging: `mutation-matrix-…/SKILL.md:67`, `skill-vetting-security-invariants/SKILL.md:15`, `security-hardening-review-ops/SKILL.md:18` (glob), `START-HERE.md:39`, `UNCERTAINTY.md:11` | **LOCKSTEP:** update the hook EMIT (`advisory.py:9`) AND both test assertions (`:1305` literal + **`:1309` os.path.join segment**) in the same change; re-run the full hook suite (`test-skill-vetting-advisory.py`, `test-skill_snapshot.py`). Update prose + provenance + staging. | — |
| `reviews/2026-08-03-pr3-derived-checks-design.md` | review (design) | historical | `evidence/reviews/…` | no | `.github/derived_checks.py:9` (docstring); `.github/test-derived-checks.py:5` (docstring) | update 2 docstrings (no assertion binds the path; not gate-fatal) | — |
| `reviews/2026-08-03-routing-contract-design.md` | review (design) | historical, canonical pointer | `evidence/reviews/…` | no | `ARCHITECTURE.md:188` (§6 routing-contract procedure pointer) | update ARCHITECTURE pointer — **NOT gate-checked (silent break)**; `checks.py` link-validation covers README* only | — |
| `reviews/2026-08-04-round5-results/` (RESULT-SUMMARY, PREREG, RECEIPTS, MANIFEST.sha256, `raw/*` bare+ruled+scored transcripts) | **probe** (eval campaign output) | closed | `evidence/probes/2026-08-04-round5/results/` (see §E-3) | no (`.py`-free) | `skills/delegation-and-review/references/recurring-sweep-ledgers.md:72`; `skills/operational-rigor/SKILL.md:960`; `skills/security-architect/SKILL.md:460`; internal `2026-08-16-closure-state/closure_checks.py:166` (`RESULT-SUMMARY.md`), `RECEIPTS.json:148` | update 3 shipped cites (SKILL.md ×2 = shipped doctrine; recurring-sweep-ledgers ref); closure_checks literal string → §Depth #10; see §E-3 | — |
| `reviews/2026-08-04-round5-targets.json` | **probe** (frozen campaign manifest) | closed | `evidence/probes/2026-08-04-round5/targets.json` (see §E-3) | no | internal only: `2026-08-16-closure-state/closure_checks.py:112` (reads via `REPO/reviews/…`); `round5-results/{PREREG.md:3,RECEIPTS.md:5,11}`; `round5-scope-plan.md:4,53`; `closure-state/RECEIPTS.json:149` | closure_checks literal string → §Depth #10; keep co-located with results/ so intra-triad refs resolve; see §E-3 | — |
| `reviews/2026-08-04-round5-scope-plan.md` | review (scope plan, campaign-bound) | closed | `evidence/reviews/…` **or** co-locate with round5 (see §E-3) | no | internal: `round5-results/PREREG.md:3`, `RECEIPTS.md:5,11`, `round5-scope-plan.md:4,53` reference the sibling `round5-targets.json` | see §E-3 (round5 unit-boundary) | — |
| *(note: the `2026-08-09-…` and `2026-08-13-…` issue115 dirs are rows in Group C below, not here)* | — | — | — | — | — | — | — |
| `reviews/2026-09-18-activation-eval-reconciliation.md` | review (reconciliation) | current, live-cited | `evidence/reviews/…` | no | **TIER-1 (gate link).** `README.md:591` (link); `README.zh-Hant.md:399` (link); `ROADMAP.md:8` (link, NOT gate-checked) | rewrite README links → re-run `checks.py` link check; rewrite ROADMAP link (silent) | — |
| `reviews/2026-09-24-ae1-v1-scored-reconciliation.md` | review (reconciliation) | current, live-cited | `evidence/reviews/…` | no | **TIER-1 (gate link).** `README.md:585` (link); `README.zh-Hant.md:393` (link); `ROADMAP.md:88` (link, NOT gate-checked) | rewrite README links → re-run `checks.py` link check; rewrite ROADMAP link (silent) | — |
| `reviews/2026-09-27-reviews-relocation-migration-packet.md` | review (this migration's v1 evidence) | current | `evidence/reviews/…` | no | referenced by `2026-09-27-target-ia-architecture-design.md:3` (internal) | update the IA doc's internal pointer if both move | — |
| `reviews/2026-09-27-target-ia-architecture-design.md` | review (the IA design) | current | `evidence/reviews/…` | no | none external | none | — |
| `reviews/README.md` | review (the tree's own contract) | current | **`evidence/README.md`** (IA: "successor to today's `reviews/README.md` contract") | no | none path-specific; describes consumer classes generically | rewrite its prose to describe the `evidence/` tree (semantic content update as the new root README) | — |

### Group C — issue115 CAMPAIGN (the largest cluster; probe vs review per unit)

| Current path | Class | Lifecycle | Target path | Depth? | Inbound consumers (file:line) | Required rewrite + gate/test | Illustrative |
|---|---|---|---|---|---|---|---|
| `reviews/2026-08-08-issue115-stage2/` (`make_manifest.py`, `static_checks.py`, fixtures/, rubrics/, wrappers/) | probe | closed campaign | `evidence/probes/2026-08-08-issue115-stage2/` | **self-contained** (`ROOT`=own dir; `os.walk(ROOT)`; no `REPO`) — SAFE to move whole | internal: read as SEALED sibling by `2026-08-14-t5-placement-probe-prereg/make_manifest.py:127` (`../2026-08-08-…`), and by t5p-prefix/t5p-scored harness lists | move whole unit; **must remain a sibling of the t5 dirs** (see §Depth, sibling-adjacency) | — |
| `reviews/2026-08-09-issue115-row1/` | probe | closed | `evidence/probes/…` | no (`.py`-free raw output) | none external | move whole unit | — |
| `reviews/2026-08-09-issue115-s1/` | probe | closed | `evidence/probes/…` | no | none external | move whole unit | — |
| `reviews/2026-08-09-issue115-scored-t1f1/` | probe | closed | `evidence/probes/…` | no | internal: `section-a-disposition/DISPOSITION-RECORD.md:60` | move whole unit | — |
| `reviews/2026-08-09-issue115-scored-t2/` | probe | closed | `evidence/probes/…` | no | internal: `row1/LEDGER.md:56`, `section-a-disposition:61` | move whole unit | — |
| `reviews/2026-08-09-issue115-scored-t3/` | probe | closed | `evidence/probes/…` | no | internal: `section-a-disposition:62` | move whole unit | — |
| `reviews/2026-08-09-issue115-scored-t4/` | probe | closed | `evidence/probes/…` | no | `skills/cross-model-review/SKILL.md:183` (shipped evidence cite); internal `section-a-disposition:60` | update SKILL cite (shipped doctrine); move whole unit | — |
| `reviews/2026-08-09-issue115-scored-t5/` | probe | closed | `evidence/probes/…` | no | internal: `section-a-disposition:63`; harness lists in t5-placement-disposition `closure/disposition_checks.py` | move whole unit | — |
| `reviews/2026-08-09-issue115-scored-t5-narrative/` | probe | closed | `evidence/probes/…` | no | internal: `section-a-disposition:64` | move whole unit | — |
| `reviews/2026-08-09-issue115-scored-t6/` | probe | closed | `evidence/probes/…` | no | internal: `section-a-disposition:65` | move whole unit | — |
| `reviews/2026-08-09-issue115-scored-t7/` | probe | closed | `evidence/probes/…` | no | internal: `section-a-disposition:66` | move whole unit | — |
| `reviews/2026-08-09-issue115-smoke-batch/` | probe | closed | `evidence/probes/…` | no | none external | move whole unit | — |
| `reviews/2026-08-13-issue115-campaign-synthesis/` | review (synthesis/adjudication) | closed | `evidence/reviews/…` | no | `skills/cross-model-review/SKILL.md:184` (shipped cite); internal: `2026-08-16-closure-state/closure_checks.py:104,105` reads `CLOSURE-ASSESSMENT.md` via `git rev-parse HEAD:reviews/…`, `RECEIPTS.json:150`, `CLOSURE-STATE.md:32` | update SKILL cite; **its git-blob path string inside closure_checks.py breaks — see §Depth/#12** | — |
| `reviews/2026-08-13-issue115-doctrine-concern-adjudication/` | review (adjudication) | closed | `evidence/reviews/…` | no | internal: `t5-placement-disposition/{closure,disposition}_checks.py` harness lists | move whole unit | — |
| `reviews/2026-08-13-issue115-section-a-disposition/` | review (disposition) | closed | `evidence/reviews/…` | no | internal: `2026-08-16-closure-state/RECEIPTS.json:151` (+ its own DISPOSITION-RECORD cross-cites many scored-t* dirs) | move whole unit | — |
| `reviews/2026-08-13-issue115-t2-probe-prereg/` (`make_manifest.py`, `static_checks.py`) | probe | closed | `evidence/probes/…` | **DEPTH-SENSITIVE** (`static_checks.py:9 REPO=../..`; reads `REPO/skills/delegation-and-review/SKILL.md`, `git -C REPO`, `REPO/reviews/2026-08-08-…`). `make_manifest.py`: `ROOT`=own, `SEALED_STAGE2_DIR` defined `:16` **but unused** | internal: read by t2probe-prefix/scored (`PREREG=REPO/reviews/2026-08-13-issue115-t2-probe-prereg`) | see §Depth #1 (disposition required) | — |
| `reviews/2026-08-13-issue115-t2-semantic-determination/` | review (determination) | closed | `evidence/reviews/…` | no | internal: `2026-08-16-closure-state/RECEIPTS.json:152` | move whole unit | — |
| `reviews/2026-08-13-issue115-t2probe-prefix/` (`prefix_checks.py`) | probe | closed | `evidence/probes/…` | **DEPTH-SENSITIVE** (`:10 REPO=../..`; `PREREG=REPO/reviews/2026-08-13-…:11,145`; `git -C REPO`) | internal: read by t5p-prefix landing_checks (`T2_DRYRUN=REPO/reviews/2026-08-13-issue115-t2probe-prefix`) | see §Depth #2 | — |
| `reviews/2026-08-13-issue115-t2probe-scored/` (`scored_checks.py`) | probe | closed | `evidence/probes/…` | **DEPTH-SENSITIVE** (`:10 REPO=../..`; `PREREG=REPO/reviews/2026-08-13-…:11`; hardcodes `reviews/2026-08-13-issue115-t2-probe-prereg` `:173`, `reviews/2026-08-13-issue115-t2probe-prefix` `:174`; `git -C REPO`) | internal | see §Depth #3 | — |
| `reviews/2026-08-14-issue115-t2-amendment-design/` (`design_checks.py`) | **MIXED** (design doc + checker) | closed | `evidence/reviews/…` OR probes (see §E-2) | **DEPTH-SENSITIVE** (`:8 REPO=../..`; `TARGET=REPO/skills/operational-rigor/references/external-systems.md`; `git -C REPO`). Also a `_gate/` verdict `.md` embeds ABSOLUTE `/Users/ccso/…/reviews/2026-08-14-…/T2-AMENDMENT-DESIGN.md` (frozen model output, non-executing) | none external | see §Depth #4 + §E-2 | — |
| `reviews/2026-08-14-issue115-t2-doctrine-mutation/` | review (doctrine mutation record) | closed | `evidence/reviews/…` | no (`.py`-free) | none external | move whole unit | — |
| `reviews/2026-08-14-issue115-t5-placement-probe-prereg/` (`make_manifest.py`, `static_checks.py`) | probe | closed | `evidence/probes/…` | **DEPTH-SENSITIVE + SIBLING-ADJACENCY.** `static_checks.py:11 REPO=../..` (reads `REPO/skills`, `git`, `REPO/reviews/2026-08-08-…`). `make_manifest.py:17,127` reads `ROOT/../2026-08-08-issue115-stage2/…` (SEALED sibling, **used**) | internal: read by t5p-prefix/scored (`PKG=REPO/reviews/2026-08-14-…`) | see §Depth #5 + #9 (must stay sibling of `2026-08-08-issue115-stage2`) | — |
| `reviews/2026-08-15-issue115-t5-placement-disposition/` (`closure_checks.py`, `disposition_checks.py`) | **MIXED** (disposition doc + closure checks) | closed | `evidence/reviews/…` OR probes (§E-2) | **DEPTH-SENSITIVE + NAME-SENSITIVE.** `closure_checks.py:12 REPO=../..`, reads `REPO/reviews/2026-08-15-issue115-t5p-scored:81`, hardcodes 6 `reviews/2026-08-…` strings `:102-107`, runs `disposition_checks.py`. `disposition_checks.py:10 REPO=../..`, `SCORED/PREREG/SEALED_T5=REPO/reviews/…:11-13`, **asserts `os.path.basename(ROOT)=="2026-08-15-issue115-t5-placement-disposition":225`** | internal | see §Depth #6/#7 (basename assert survives a name-preserving move; REPO + literal strings break) | — |
| `reviews/2026-08-15-issue115-t5p-prefix/` (`landing_checks.py`, `prefix_checks.py`) | probe | closed | `evidence/probes/…` | **DEPTH-SENSITIVE.** both `:11/:8 REPO=../..`; `PKG=REPO/reviews/2026-08-14-…`; `landing_checks.py:18 T2_DRYRUN=REPO/reviews/2026-08-13-…`; hardcodes `reviews/2026-08-14-…`,`reviews/2026-08-08-…`,`reviews/2026-08-13-…` `:129-131,:33`; `git -C REPO`; runs `prefix_checks.py` | internal: read by t5p-scored | see §Depth #8 | — |
| `reviews/2026-08-15-issue115-t5p-scored/` (`scored_checks.py`) | probe | closed | `evidence/probes/…` | **DEPTH-SENSITIVE.** `:12 REPO=../..`; `PKG=REPO/reviews/2026-08-14-…`; walk list hardcodes `reviews/2026-08-14-…`,`reviews/2026-08-15-issue115-t5p-prefix`,`reviews/2026-08-08-…`,`skills`,`metadata` `:136-138`; `git diff HEAD` | internal: read by t5-placement-disposition (`REPO/reviews/2026-08-15-issue115-t5p-scored`) | see §Depth #10 | — |
| `reviews/2026-08-16-issue115-closure-state/` (`closure_checks.py`) | **MIXED** (closure-state record + strong checker) | closed | `evidence/reviews/…` OR probes (§E-2) | **DEPTH-SENSITIVE (HIGHEST).** `:16 REPO=../..`; reads `REPO/reviews/2026-08-04-round5-targets.json:112`; `git rev-parse HEAD:reviews/2026-08-13-issue115-campaign-synthesis/…:104`; `rf("reviews/2026-08-04-round5-results/RESULT-SUMMARY.md"):166`; `harness=REPO/evals/round4/…:261`, `subject=REPO/evals/round4/run4.sh:262`; **globs `REPO/skills/**/*.md`:335** | internal (round5, campaign-synthesis, section-a, t2-semantic-determination, t5-placement-disposition) | see §Depth #11 (reaches `evals/round4` + `skills` + 5 sibling reviews paths) | — |

### Group D — SECURITY / DOCTRINE finding & probe dirs (2026-08-21 → 2026-09-25)

| Current path | Class | Lifecycle | Target path | Depth? | Inbound consumers (file:line) | Required rewrite + gate/test | Illustrative |
|---|---|---|---|---|---|---|---|
| `reviews/2026-08-21-issue2-activation-gated-payload/` (README, STATIC-DISCRIMINATION, fixtures/) | probe (fixture-based discrimination evidence) | closed | `evidence/probes/…` | no (`.py`-free) | `skills/operational-rigor/references/provenance.md:389` | update provenance pointer (silent); move whole unit | — |
| `reviews/2026-08-21-u00ad-sweep-hotfix/` (`proof.py`) | **MIXED** (hotfix record + proof) | closed | `evidence/probes/…` OR reviews (§E-2) | **NOT depth-sensitive** (`proof.py:19 ROOT=git rev-parse --show-toplevel`; reads `skills/operational-rigor/SKILL.md`,`skills/skill-vetting/SKILL.md`) — move-resilient via git-root | none external (HOTFIX.md self-hashes its own files) | move whole unit; `proof.py` re-runnable at any depth (git-root) | — |
| `reviews/2026-08-22-issue1-exfiltration-channel/` (README, STATIC-DISCRIMINATION, fixtures/) | probe (fixture-based) | closed | `evidence/probes/…` | no | `skills/skill-vetting/references/provenance.md:33` | update provenance pointer (silent); move whole unit | — |
| `reviews/2026-08-29-coverage-before-clearance/` (design-review-packet, verdicts/) | review (design review + gate) | closed | `evidence/reviews/…` | no | none external | move whole unit | — |
| `reviews/2026-08-29-git-mechanics-correction/` | review | closed | `evidence/reviews/…` | no | none external | move whole unit | — |
| `reviews/2026-08-29-rerun-is-new-evidence/` | review | closed | `evidence/reviews/…` | no | none external | move whole unit | — |
| `reviews/2026-08-30-meaningful-approval-review/` (packets/, verdicts/, gate-trail) | review (design review + gate) | closed | `evidence/reviews/…` | no | `skills/operational-rigor/references/provenance.md:667` | update provenance pointer (silent); move whole unit | — |
| `reviews/2026-08-30-runtime-artifact-correspondence/` (`harness/{drive,run_case,d11_probe}.py`) | probe | closed | `evidence/probes/…` | **NOT depth-sensitive** (harness `HERE`=own dir; `PYCACHE/WORK` under `HERE`; `run_case`/`d11_probe` operate on passed work/temp dirs) — self-contained | `skills/operational-rigor/references/provenance.md:553` | update provenance pointer (silent); move whole unit | — |
| `reviews/2026-08-30-trust-grant-breadth/` (design-review-packet-r1/r2, verdicts/) | review (design review + gate) | closed | `evidence/reviews/…` | no | `skills/operational-rigor/references/provenance.md:500` | update provenance pointer (silent); move whole unit | — |
| `reviews/2026-08-30-visible-identity-confusability/` (`harness/h_probe.py`) | probe | closed | `evidence/probes/…` | **NOT depth-sensitive** (`h_probe.py` fully self-contained — zero outside-dir signals) | `skills/operational-rigor/references/provenance.md:602` | update provenance pointer (silent); move whole unit | — |
| `reviews/2026-08-31-out-of-tree-cache-removal/` (`harness/pycache_prefix_probe.py`) | probe | closed | `evidence/probes/…` | **NOT depth-sensitive** (`pycache_prefix_probe.py` uses `tempfile.mkdtemp` + `os.walk(temp)` — operates in temp) | none external (internal: `packets/packet-r2.md:53` self-cites) | move whole unit | — |
| `reviews/2026-09-01-reviewer-execution-principal-c8/` (`closure/*.py`, `gate-record/{v3,v4}edit.py`) | **MIXED** (design/gate record + one-shot landing scripts) | closed (already executed) | `evidence/reviews/…` OR probes (§E-2) | **NOT depth-to-root sensitive, BUT HARDCODED ABSOLUTE paths.** `compose_landing.py:68,72,86` + `reconstruction_check.py:12-14` write/read `/Users/ccso/Developer/fable/skills/…` (abs, already-stale-if-cloned). CWD-relative reads (`DESIGN-v4-owner-repair.md`, `landed-*.txt`). `reconstruction_check.py:11 V4="../gate-record/DESIGN-v4.md"` = intra-unit sibling (preserved by moving unit whole) | `skills/cross-model-review/references/provenance.md:79`; `skills/delegation-and-review/references/provenance.md:479` | update 2 provenance pointers (silent); move whole unit. Scripts are **historical one-shot** (they already landed doctrine into `skills/`); hardcoded-abs breakage is pre-existing, not introduced by this migration | — |
| `reviews/2026-09-02-recursive-delegation-c12/` (`c12_checks.py`) | probe | closed | `evidence/probes/…` | **DEPTH-SENSITIVE + NAME/PATH-SENSITIVE.** `:40 ROOT=os.path.join(dirname,"..","..")`; `DR/CMR/RECEIPT=ROOT/skills/…:42-44`; **asserts files `startswith("reviews/2026-09-02-recursive-delegation-c12/"):188`**; `git`/`cwd=ROOT` | `skills/cross-model-review/references/provenance.md:91`; `skills/delegation-and-review/references/provenance.md:517` | update 2 provenance pointers; see §Depth #12 (self-path literal `:188` breaks on move) | — |
| `reviews/2026-09-09-s1-provenance-relocation/` (`relocate.py`, `verify.py`, README) | probe (one-shot migration + verifier) | closed (already executed) | `evidence/probes/…` | **NOT depth-sensitive** (`relocate.py:17`/`verify.py:18 ROOT=git rev-parse --show-toplevel`) — move-resilient. `relocate.py` MUTATES `skills/*/SKILL.md` (historical, already run); `verify.py` reads `skills/` + `git show 076f9d0` | none external | move whole unit; git-root scripts re-runnable at any depth | — |
| `reviews/2026-09-24-hcsa1-a-observable-session-trace-corpus/` (3 DESIGN `.md` only) | review (design records) — **NOT corpus** | current line | `evidence/reviews/…` | no | **none external** (`git grep hcsa1-a` outside reviews/ = NONE) | none. **Despite "corpus" in the name**, the tracked content is design docs, the actual corpus infra is gitignored (`evals/hcsa1-a-build/`), and NO runtime loader consumes it → it is evidence, not canonical `corpus/` authority. See §E-4 | — |
| `reviews/2026-09-25-design-6b1-runtime-prototype/` (`design-6b1-loader-prototype.py`, manifest.json, recall-report.md, README) | **MIXED** (design prototype + runnable loader) | current line | `evidence/probes/…` OR reviews (§E-2) | **NOT depth-sensitive** (`loader-prototype.py:43 HERE`=own dir; `:44` reads `HERE/design-6b1-manifest.json` only — self-contained) | none external | move whole unit; loader reads only its own sibling manifest | — |
| `reviews/2026-09-25-hcsa1-b0-consumer-model-operational-validity/DESIGN.md` **(UNTRACKED)** | review (design draft) | current, uncommitted | `evidence/reviews/…` | no | none (no `reviews/` citations in it) | **§E-5: untracked — a `git mv` migration cannot move it until it is committed or explicitly excluded**; otherwise orphaned | — |

---

## TIER-1 SUBSET (gate/runtime-critical — a move BREAKS a gate, loader, or hook test)

1. **`reviews/2026-09-26-phase-b-semantic-publication/`** (corpus) — `project_corpus.py:25,27` constants + `generated/{manifest.json:5,13,README.md:4}` + `projection_checks.py:262` regex. Gate: `checks.py` D6-B2.2 bridge contract + `projection_checks`. **This round: LEAVE-IN-PLACE-PINNED** (no move). Highest coupling.
2. **`reviews/2026-07-25-skill-vetting-snapshot-threat-model.md`** — hook `skill-vetting-advisory.py:9` EMITS it; test `test-skill-vetting-advisory.py:1305` (literal `assertIn`) **AND `:1309`** (`os.path.join(REPO,"reviews",…)` existence check). Gate: full hook test suite. **Requires 3-way lockstep** (emit + 2 assertions) and is the one consumer a literal `reviews/` grep-and-replace MISSES (`:1309`).
3. **README gate-checked links** — `README.md:535` (`2026-07-11-pack-eval-rounds-1-2.md`), `:585` (`2026-09-24-ae1-v1-scored-reconciliation.md`), `:591` (`2026-09-18-activation-eval-reconciliation.md`) + `README.zh-Hant.md:350,393,399`. Gate: `checks.py` "inline relative markdown links resolve" (README* only). Break these → red gate.

**NOT Tier-1 (break SILENTLY, not gate-caught):** `ARCHITECTURE.md:188`; `ROADMAP.md:8,88`; README prose `:322,:460` + zh `:237,:322`; all `skills/*/provenance.md` + `SKILL.md` cites; `.github/*_checks.py` docstrings; Tier-3 `skills-staging/*`. `checks.py` validates links in README* ONLY — ROADMAP/ARCHITECTURE link rot is not caught.

---

## DEPTH-SENSITIVITY DETAIL (Gap 1 — the hidden path-contract)

**The core mechanic:** a script at `reviews/X/foo.py` computing `REPO =
os.path.abspath(os.path.join(ROOT, "..", ".."))` reaches the **repo root** (X →
reviews → root = 2 levels). Under the target `evidence/probes/X/foo.py`, the same
`../..` reaches **`evidence/`, not the repo root** (X → probes → evidence). So
EVERY depth-sensitive harness is **doubly broken** by the move: (a) `REPO`
mis-computes, and (b) the hardcoded `"reviews/…"` literal cross-ref/blob strings
inside it are now wrong (should be `"evidence/probes/…"`). **Both fixes are
SEMANTIC code edits, which the execution gate "path-only; no semantic edits in
the migration commit" FORBIDS.** → this is the central escalation (§E-1).

Depth-sensitive harnesses (12 scripts / 10 dirs), each `REPO=../..`:

| # | Script | Outside-dir reach | Breaks on move to `evidence/probes/` |
|---|---|---|---|
| 1 | `2026-08-13-issue115-t2-probe-prereg/static_checks.py:9` | `REPO/skills/delegation-and-review/SKILL.md:66`; `git -C REPO`; `REPO/reviews/2026-08-08-…:10` | REPO + literal string |
| 2 | `2026-08-13-issue115-t2probe-prefix/prefix_checks.py:10` | `PREREG=REPO/reviews/2026-08-13-…:11`; `git -C REPO`; hardcodes `reviews/2026-08-13-…:145` | REPO + literal |
| 3 | `2026-08-13-issue115-t2probe-scored/scored_checks.py:10` | `PREREG=REPO/reviews/…:11`; hardcodes `reviews/2026-08-13-…:173,174`; `git -C REPO` | REPO + literals |
| 4 | `2026-08-14-issue115-t2-amendment-design/design_checks.py:8` | `TARGET=REPO/skills/operational-rigor/references/external-systems.md:9`; `git -C REPO` | REPO |
| 5 | `2026-08-14-issue115-t5-placement-probe-prereg/static_checks.py:11` | `REPO/skills`; `REPO/reviews/2026-08-08-…:12`; `git -C REPO` | REPO + literal |
| 6 | `2026-08-15-issue115-t5-placement-disposition/closure_checks.py:12` | `REPO/reviews/2026-08-15-issue115-t5p-scored:81`; hardcodes 6 `reviews/2026-08-…:102-107`; `git -C REPO` | REPO + literals |
| 7 | `2026-08-15-issue115-t5-placement-disposition/disposition_checks.py:10` | `SCORED/PREREG/SEALED_T5=REPO/reviews/…:11-13`; **basename==own-dir-name assert:225**; `git -C REPO` | REPO + literals (basename assert SURVIVES a name-preserving move) |
| 8 | `2026-08-15-issue115-t5p-prefix/{landing_checks.py:11, prefix_checks.py:8}` | `PKG=REPO/reviews/2026-08-14-…`; `T2_DRYRUN=REPO/reviews/2026-08-13-…:18`; hardcodes `reviews/2026-08-14/08/13-…:129-131,33`; `git -C REPO` | REPO + literals |
| 9 | `2026-08-15-issue115-t5p-scored/scored_checks.py:12` | `PKG=REPO/reviews/2026-08-14-…`; walk list `reviews/2026-08-14/…,t5p-prefix,2026-08-08-…,skills,metadata:136-138`; `git diff HEAD` | REPO + literals |
| 10 | `2026-08-16-issue115-closure-state/closure_checks.py:16` | `REPO/reviews/2026-08-04-round5-targets.json:112`; `git HEAD:reviews/2026-08-13-campaign-synthesis/…:104`; `reviews/2026-08-04-round5-results/…:166`; `REPO/evals/round4/{run4.sh,harness}:261,262`; **globs `REPO/skills/**/*.md`:335** | REPO + literals (highest reach: evals/round4 + skills + 5 sibling reviews) |
| 11 | `2026-09-02-recursive-delegation-c12/c12_checks.py:40` | `ROOT/skills/{delegation-and-review,cross-model-review}/…:42-44`; **asserts files `startswith("reviews/2026-09-02-recursive-delegation-c12/"):188**`; `cwd=ROOT` | REPO + self-path literal |

**Sibling-adjacency (not repo-depth, but relative-sibling) — #9 in table above:**
`2026-08-14-issue115-t5-placement-probe-prereg/make_manifest.py:127` reads
`ROOT/../2026-08-08-issue115-stage2/…` — requires `2026-08-08-issue115-stage2`
to remain its **directory sibling** after the move. Preserved if all issue115
probes land flat under `evidence/probes/`.

**NOT depth-sensitive (safe to move at any depth):** the git-toplevel scripts
(`2026-08-21-u00ad-sweep-hotfix/proof.py`, `2026-09-09-s1-provenance-relocation/{relocate,verify}.py`);
the self-contained harnesses (`2026-08-30-runtime-artifact-correspondence/harness/*`,
`2026-08-30-visible-identity-confusability/harness/h_probe.py`,
`2026-08-31-out-of-tree-cache-removal/harness/pycache_prefix_probe.py`,
`2026-09-25-design-6b1-runtime-prototype/design-6b1-loader-prototype.py`,
`2026-08-08-issue115-stage2/{make_manifest,static_checks}.py`); the CWD-relative +
hardcoded-absolute c8 scripts (not depth-to-root, but abs-path fragile).

---

## GAP 3 — ILLUSTRATIVE-vs-REAL citation split (verified by on-disk existence test)

Method: extracted every distinct `reviews/…` token cited in shipped files
(`skills/**`, `README*`, `ROADMAP.md`, `ARCHITECTURE.md`, `hooks/**`, `.github/**`,
`skills-staging/**`) and tested each for on-disk existence. A cited path that does
NOT exist is illustrative/fictional. [verified: ran existence test on all]

- **EXACTLY ONE fictional/illustrative citation repo-wide → DO NOT REWRITE:**
  `reviews/styling-ledger.md` in **`skills/delegation-and-review/SKILL.md:472`**
  — inside a `✅` example: *"packet names styling-sweep-2026Q3 and
  reviews/styling-ledger.md, reconciled item-by-item…"*. Both `styling-ledger.md`
  AND the campaign id `styling-sweep-2026Q3` are made-up illustrations of what a
  recurring-sweep packet should name. **A grep-and-replace of `reviews/` would
  corrupt this example.** [verified: `styling-ledger.md` NOT on disk;
  read SKILL.md:460-478 context]
- **All other cited paths EXIST → REAL citations → rewrite on move.** Two apparent
  "not-on-disk" hits were grep wrap/glob artifacts of real files, NOT fictional:
  `reviews/2026-07-11-pack-eval-` (line-wrap in `hooks/gate-credential-destruction.py:7`
  → real `…-rounds-1-2.md`) and `reviews/2026-07-25-skill-vetting-*.md` (a **glob**
  in skills-staging → real `round8-design.md` + `snapshot-threat-model.md`). The
  glob form (`reviews/2026-07-25-skill-vetting-*.md`) is itself a rewrite target
  in `skill-vetting-hardening-archaeology/SKILL.md:220`.
- One **bare-directory** prose reference (not a specific path):
  `skills-staging/2026-07-30-campaign-ops/repo-boundaries-and-sync/SKILL.md:15`
  *"`reviews/` — public review and threat-model records"* — on a root rename
  `reviews/`→`evidence/` this prose updates; not a dated-path rewrite. Tier-3.

---

## INTERNAL CROSS-REFERENCE MAP (why split-across-targets matters)

When `reviews/` splits into `corpus/` + `evidence/reviews/` + `evidence/probes/`,
a reference from one unit to another whose endpoints land in DIFFERENT subtrees
needs its literal path rewritten too. Key internal dependency clusters:

- **round5 triad:** `round5-results/` (probe) ↔ `round5-targets.json` (probe
  manifest) ↔ `round5-scope-plan.md` (review). Cross-cited in `PREREG.md:3`,
  `RECEIPTS.md:5,11`, `scope-plan.md:4,53`, and read by
  `2026-08-16-closure-state/closure_checks.py:112,166`. If results+targets →
  probes/ but scope-plan → reviews/, the closure_checks literal strings AND the
  intra-triad references cross a subtree boundary. → §E-3.
- **t2/t5 probe chain:** t2-probe-prereg → t2probe-prefix → t2probe-scored;
  t5-placement-probe-prereg → t5p-prefix → t5p-scored; all read `2026-08-08-issue115-stage2`
  as SEALED. All are probes → land together under `evidence/probes/`, so the
  git-`REPO`-relative strings still resolve **after the REPO-depth fix** (which
  itself is the §E-1 semantic-edit problem).
- **closure/disposition → doc dirs:** `t5-placement-disposition` (MIXED) and
  `closure-state` (MIXED) harnesses read doc-dirs `campaign-synthesis` (review),
  `section-a-disposition` (review), `t2-semantic-determination` (review) via
  `git HEAD:reviews/…` blob strings — these CROSS the probe/review boundary and
  break if the checker (probe subtree) and the doc (review subtree) diverge.

---

## DISPOSITIONS (owner-adjudicated 2026-09-27)

- **E-1 RESOLVED — KEEP PATH-ONLY RELOCATION.** Depth-sensitive runnable harnesses
  require a separate pre-migration semantic-hardening change, or an explicit
  per-unit retirement disposition. A relocation commit itself must NOT repair
  relative-path logic. No harness may become non-runnable silently. Contract:
  *runnable historical harnesses may not be silently broken by relocation; if a
  target path changes a harness's relative-depth assumptions, first land an
  independent semantic-hardening change while it is still at the OLD path —
  reviewed, tested, green — and only then may the subsequent relocation commit
  remain path-only.* Two commits per affected unit: **(A) semantic-preparation**
  (old location) — replace `REPO=../..` with depth-independent discovery
  (`git rev-parse --show-toplevel`, as `u00ad-sweep-hotfix/proof.py` and
  `s1-provenance-relocation/*.py` already do) and neutralize the embedded
  `"reviews/…"` literals; add the harness test; independent review; green.
  **(B) relocation** — `git mv` only, no semantic edits, old → `evidence/probes/…`;
  same battery + harness verification. Rejected: blanket documented-non-rerun (a
  closed campaign is still part of the evidence chain; "probably won't re-run" is
  not license to break a runnable artifact) and depth-1 (distorts the
  architecture for migration convenience). Retiring a specific harness is an
  EXPLICIT per-unit `non-rerunnable historical artifact` disposition, never the
  migration's default escape hatch.
- **E-2 OPEN** — per-unit classification of the 6 MIXED dirs at manifest
  finalization, by each unit's primary role (splitting a unit stays discouraged).
- **E-3 OPEN** — round5 physical-unit decision at finalization (co-locate as one
  probe unit vs split by role); does not affect the architecture model.
- **E-4 RESOLVED — `corpus/` is reserved for canonical machine-consumed production
  semantic inputs; a name containing "corpus" does NOT qualify by name alone.**
  `2026-09-24-hcsa1-a-observable-session-trace-corpus/` is design/review docs with
  no production authority and no runtime consumer → `evidence/reviews/`, NOT
  `corpus/`. `corpus/` is reserved exclusively for design-pack's canonical
  semantic authority (`public_records.json`).
- **E-5 EXECUTION FLAG** — the untracked `hcsa1-b0/DESIGN.md` is not in the tracked
  move-set; before relocation it gets a separate disposition/commit or an explicit
  exclusion, never handled implicitly by `git mv`.
- **E-6 EXECUTION FLAG** — `2026-09-01-c8` hardcoded absolute paths are a
  pre-existing defect, out of this design phase's scope; if a future migration
  needs that harness runnable it falls into E-1's semantic-prep lane, else its own
  disposition. Not fixed now.

## ESCALATE — original discovery detail (pre-adjudication; the DISPOSITIONS above are the owner-adjudicated outcome)

**E-1 — Depth-sensitive #115 harnesses vs the path-only execution gate (BLOCKING).**
The 12 depth-sensitive scripts (§Depth) cannot survive a move to
`evidence/probes/` without (a) patching `REPO=../..`→`../../..` and (b) rewriting
their embedded `"reviews/…"` literal/blob strings → both are **semantic code
edits**, forbidden by "path-only; no semantic edits in the migration commit."
The IA sanctions ONE resolution ("a historical harness that will not stay
runnable at its new location gets an explicit disposition, documented, never a
silent break") but does not pick among: **(a)** accept documented non-rerun for
these CLOSED issue-#115 harnesses; **(b)** authorize a SEPARATE semantic-patch
commit (traversal +1 + literal rewrite) outside the path-only commit; **(c)**
keep probes at depth-1 (`evidence/X`), contradicting the `probes/` bucket. I
cannot choose for the owner. Note also `git HEAD:reviews/…` blob-SHA reads
(`closure_checks.py:104`) assume the OLD path existed at the pinned commit — they
read history, so they may keep working against the pre-move blob regardless of
the new location, but the literal string still needs the owner's disposition.

**E-2 — MIXED review+probe units (6) need an identity ruling.**
`2026-08-14-t2-amendment-design`, `2026-08-15-t5-placement-disposition`,
`2026-08-16-closure-state`, `2026-08-21-u00ad-sweep-hotfix`, `2026-09-01-c8`,
`2026-09-25-design-6b1-runtime-prototype` each bundle a human review/design doc
AND a runnable script in one dir. I classified each toward the runnable-unit home
(probes) to preserve depth/unit, but the human-doc identity could anchor them to
`evidence/reviews/`. The IA says "unless it genuinely mixes" — these genuinely
mix. Owner must rule per-dir (splitting a unit is explicitly discouraged by the
IA, so the ruling is which single home).

**E-3 — round5 campaign unit boundary.** Spread across 3 top-level entries
(`round5-results/` dir + loose `round5-targets.json` + loose `round5-scope-plan.md`),
two probe + one review, mutually cross-referenced and read by closure_checks. Do
they co-locate as one `evidence/probes/2026-08-04-round5/` unit (preserving refs)
or split by role (scope-plan→reviews)? Unit boundary needs an owner call.

**E-4 — `hcsa1-a` "corpus" naming vs the `corpus/` bucket.** `2026-09-24-hcsa1-a-observable-session-trace-corpus/`
is named "corpus" but its tracked content is DESIGN docs only, the real corpus
infra is gitignored, and it has ZERO runtime consumer → I classified it
`review`, NOT `corpus/`. Confirm the `corpus/` bucket is reserved exclusively for
design-pack semantic authority (`public_records.json`).

**E-5 — Untracked entries.** `reviews/2026-09-25-hcsa1-b0-.../DESIGN.md` is
UNTRACKED; a `git mv` migration cannot move it until it is committed or explicitly
excluded — otherwise it is orphaned at the old root. (`design-mining/` is
gitignored + reviews-ref-free → correctly out of scope.) Owner must decide
commit-then-migrate vs leave-untracked.

**E-6 — c8 hardcoded absolute paths (pre-existing, flag-only).** The
`2026-09-01-c8` closure/reconstruction scripts hardcode `/Users/ccso/Developer/fable/skills/…`.
Not introduced by this migration and already clone-fragile, but if the owner ever
re-runs them post-move they fail regardless of the reviews/ move. Flagged, not
mine to fix.

---

## EXECUTION GATES (carried from the IA + packet — apply to ANY authorized migration)

- Path-only; no semantic edits in the migration commit. Per E-1 (RESOLVED), path
  coupling in depth-sensitive harnesses is removed in a SEPARATE pre-migration
  semantic-hardening commit — the relocation commit itself stays path-only; no
  conflict.
- Canonical battery GREEN before AND after: `.github/checks.py` +
  `.github/test-derived-checks.py` + `.github/design_pack_checks.py` +
  `design-pack/tools/projection_checks.py` + all hook suites
  (`test-skill-vetting-advisory.py`, `test-skill_snapshot.py`) + gate-template.
- Generated artifacts (`design-pack/generated/*`) REGENERATED from source, never
  hand-edited.
- Migration requires its OWN authorization; this manifest authorizes none.
