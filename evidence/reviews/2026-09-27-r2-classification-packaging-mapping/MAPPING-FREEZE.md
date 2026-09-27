# R2 — classification + packaging gate + final old→new mapping freeze

> **Design / adjudication record. NO `git mv`, NO relocation performed here.**
> Baseline: `main` @ `32939a3` (branch `relocation/r2-classification-packaging-mapping`).
> Closes the OPEN items the exhaustive manifest
> (`reviews/2026-09-27-reviews-relocation-manifest.md`) left for finalization
> (E-2, E-5) and confirms the packaging-surface gate, then FREEZES the old→new
> mapping. The manifest's master table remains the exhaustive per-file map; this
> record amends its open items and declares the result frozen.

## Sequence context

- **R1a (E-1 semantic-prep) — DONE / MERGED** (`ff4e2b5`, PR #267; erratum `32939a3`, PR #268). 4 harnesses depth-hardened (relocation-safe location logic, zero drift); 8 harnesses dispositioned `non-rerunnable historical artifact`. See `reviews/2026-09-27-r1a-e1-harness-path-hardening/R1A-DISPOSITION.md`.
- **R2 (this record) — classification + packaging + mapping freeze.** No `git mv`.
- **Next (separate authorization):** the actual path-only relocation PR.

## 1. Packaging-surface gate — RESULT (empirically settled)

**Question:** under `opus-pack`'s plugin `source: "./"` (repo root), does renaming
`reviews/` → `evidence/` (and, later, adding a top-level `corpus/`) change the
plugin's install/publish payload or its active/loaded surface?

**Method:** (a) authoritative Claude Code plugin docs for the LOADED surface;
(b) direct inspection of a real on-disk plugin install for the PAYLOAD.

**Findings:**
- **Active/loaded surface — NO change.** Component discovery is convention-based
  (`skills/`, `commands/`, `agents/`, `hooks/hooks.json`, `.mcp.json`, …) plus
  explicit manifest paths; non-component top-level directories (`reviews/`,
  `evidence/`, `corpus/`) are never scanned or loaded. Neither plugin.json
  declares `files`/`include`/`exclude`. [doc: code.claude.com plugins
  manifest-reference — Standard layout / Fields] Empirically corroborated by the
  payload evidence below: the `codex` install carries non-component `scripts/`,
  `schemas/`, `prompts/` on disk yet those are NOT loaded as components (present
  ≠ active), so a non-component `reviews/`/`evidence/` directory would not be part
  of the active surface either.
- **Install/publish payload — WHOLE source tree (not component-filtered).**
  Empirically, a real plugin install copies non-component content, not just the
  recognized component dirs: the installed `codex` plugin at
  `~/.claude/plugins/cache/openai-codex/codex/1.0.5/` contains `scripts/`,
  `schemas/`, `prompts/`, `CHANGELOG.md`, `LICENSE`, `NOTICE` alongside
  `skills/`/`commands/`/`agents/`/`hooks/`; the marketplace clones under
  `~/.claude/plugins/marketplaces/*` are full git clones (they carry `tests/`,
  `scripts/`, `.github/`, `.git/`). [verified: ran `ls`/`find` on the on-disk
  install 2026-09-27] Method note: `opus-pack` is NOT installed on this host
  (only the `openai-codex` and `claude-plugins-official` marketplaces are), so
  this is the SHARED Claude Code plugin-install mechanism observed via the `codex`
  install as PROXY, combined with the absence of any `files`/`include`/`exclude`
  in `opus-pack`'s own manifests — the whole-tree conclusion for `opus-pack`
  follows from that shared mechanism, not from a direct opus-pack install
  observation.
- **Therefore for `opus-pack` (`source: "./"`):** the evidence trail already
  ships in the install payload today (whole-tree). Renaming `reviews/` →
  `evidence/` is **RENAME-ONLY**: the same bytes ship under a new top-level
  directory name — **no NEW shipped surface, no removed surface, no active-surface
  change.** `design-pack` (`source: "./design-pack"`) is unaffected by top-level
  dir changes outside its subtree.

**Conclusion: the reviews/→evidence/ relocation is packaging-safe (rename-only).**

**Observed, not addressed (out of R2 scope):** the whole evidence trail ships to
every `opus-pack` installer today (a pre-existing property, NOT introduced by the
relocation). If the owner ever wants the evidence trail excluded from the shipped
payload, the plugin manifest offers no `files`/`exclude` mechanism for arbitrary
directories (docs are silent / ambiguous on payload-scoping); that would need a
separate approach (e.g. marketplace `source` pointing at a component subdir, or a
split repo) and its own authorization. Not required for a rename-only relocation.
The future top-level `corpus/` is also not new shipped content — its bytes
(`public_records.json`) already ship inside
`reviews/2026-09-26-phase-b-semantic-publication/` — but the corpus move stays
LEAVE-IN-PLACE-PINNED this cycle regardless.

## 2. E-2 — the 6 MIXED units, adjudicated by PRIMARY artifact role

Rule applied (owner): classify by primary artifact role (human review/adjudication/design
→ `evidence/reviews/`; measurement campaign / runnable evidence unit →
`evidence/probes/`), NOT by lifecycle and NOT by the mere presence of a `.py`.
Splitting a unit stays disallowed — each gets ONE home.

| MIXED unit | Home | Primary role (evidence) |
|---|---|---|
| `2026-08-14-issue115-t2-amendment-design` | `evidence/reviews/` | A doctrine-amendment DESIGN (`T2-AMENDMENT-DESIGN.md`) + a 7-file human review gate (`_gate/` luna/sol HOLD/PROCEED rounds); `design_checks.py` only mechanically verifies the design. Human design/adjudication dominant. |
| `2026-08-15-issue115-t5-placement-disposition` | `evidence/reviews/` | A DISPOSITION/adjudication record (`DISPOSITION.md`) + review gate; the two `.py` verify it. Human adjudication dominant. |
| `2026-08-16-issue115-closure-state` | `evidence/reviews/` | The issue-115 tracker CLOSURE-STATE adjudication (`CLOSURE-STATE.md` + gate + `RECEIPTS.json`); `closure_checks.py` verifies it. Human adjudication dominant. |
| `2026-09-01-reviewer-execution-principal-c8` | `evidence/reviews/` | Overwhelmingly a DESIGN + multi-round GATE record (42 `.md`: `DESIGN-v1..v4`, r1/r2/r3/nc1 gate rounds, adjudications, packets, probe transcripts). The 6 `.py` are one-shot landing/closure scripts (already executed, historical). Human design/adjudication dominant. |
| `2026-08-21-u00ad-sweep-hotfix` | `evidence/probes/` | An "evidence record" whose core is a two-sided runnable PROOF engine (`proof.py`, baseline vs post modes) + its baseline/post evidence logs + `hotfix.diff`. Runnable-evidence unit dominant. `proof.py` already uses git-toplevel (move-resilient). |
| `2026-09-25-design-6b1-runtime-prototype` | `evidence/probes/` | A runnable loader PROTOTYPE (`design-6b1-loader-prototype.py`) + `manifest.json` + a recall/invariant MEASUREMENT report (`recall-report.md`, "EXIT GATE — mandatory invariants", metrics, reproducible via the loader). Runnable-evidence/measurement dominant. `loader-prototype.py` is self-contained (own-dir). |

Result: **4 → `evidence/reviews/`, 2 → `evidence/probes/`.** (E-2 CLOSED.)

## 3. E-3 / E-4 / E-5 / corpus — status

- **E-3 RESOLVED** (owner, 2026-09-27): round5's three top-level entries co-locate
  as ONE probe unit `evidence/probes/2026-08-04-round5/` (`targets.json` +
  `scope-plan.md` + `results/`). See R1A-DISPOSITION.md §3.
- **E-4 RESOLVED** (manifest): `2026-09-24-hcsa1-a-observable-session-trace-corpus/`
  is design/review docs with no runtime consumer → `evidence/reviews/`, NOT
  `corpus/`. `corpus/` is reserved for design-pack's canonical semantic authority.
- **E-5 RESOLVED — EXCLUDE** (owner, 2026-09-27): the untracked
  `reviews/2026-09-25-hcsa1-b0-consumer-model-operational-validity/DESIGN.md` is
  unfrozen working material and is **not committed for the sake of IA
  relocation**. It stays untracked, OUTSIDE the relocation manifest/move-set; its
  own HCSA governance decides any future publication. The path-only `git mv`
  migration must not touch it (nothing to move — it is untracked).
- **Corpus — LEAVE-IN-PLACE-PINNED** (manifest/IA): `2026-09-26-phase-b-semantic-publication/`
  (`public_records.json` etc.) stays at its current path this cycle; its move to a
  canonical `corpus/` surface is a separate, later, dedicated relocation
  (highest Tier-1 coupling). NOT part of this mapping's move-set.

## 4. Frozen old→new mapping

The exhaustive per-file map is the manifest's MASTER TABLE
(`reviews/2026-09-27-reviews-relocation-manifest.md`), now amended by §2–§3 above
and frozen as follows. Mechanical rule for every unit not called out explicitly:
`reviews/<unit>` → `evidence/{reviews|probes}/<unit>` by its manifest artifact-role
class, basename preserved (a name-preserving path-only move).

**Explicit / non-mechanical entries (the frozen closures):**

| Current path | Frozen target | Notes |
|---|---|---|
| `reviews/2026-09-26-phase-b-semantic-publication/` | **LEAVE-IN-PLACE-PINNED** | corpus; deferred to a separate corpus relocation |
| `reviews/2026-08-04-round5-results/` + `reviews/2026-08-04-round5-targets.json` + `reviews/2026-08-04-round5-scope-plan.md` | `evidence/probes/2026-08-04-round5/{results/, targets.json, scope-plan.md}` | E-3: one co-located probe unit |
| `reviews/2026-09-24-hcsa1-a-observable-session-trace-corpus/` | `evidence/reviews/2026-09-24-hcsa1-a-observable-session-trace-corpus/` | E-4: review, not corpus (name notwithstanding) |
| `reviews/2026-09-25-hcsa1-b0-consumer-model-operational-validity/` (untracked) | **EXCLUDED** | E-5: not in the move-set |
| `reviews/2026-08-14-issue115-t2-amendment-design/` | `evidence/reviews/…` | E-2 (MIXED→review) |
| `reviews/2026-08-15-issue115-t5-placement-disposition/` | `evidence/reviews/…` | E-2 (MIXED→review); contains non-rerunnable-historical harnesses |
| `reviews/2026-08-16-issue115-closure-state/` | `evidence/reviews/…` | E-2 (MIXED→review); contains non-rerunnable-historical harness |
| `reviews/2026-09-01-reviewer-execution-principal-c8/` | `evidence/reviews/…` | E-2 (MIXED→review) |
| `reviews/2026-08-21-u00ad-sweep-hotfix/` | `evidence/probes/…` | E-2 (MIXED→probe) |
| `reviews/2026-09-25-design-6b1-runtime-prototype/` | `evidence/probes/…` | E-2 (MIXED→probe) |
| `reviews/README.md` | `evidence/README.md` | successor root contract (semantic content update, per manifest) |
| `reviews/styling-ledger.md` | **DOES NOT EXIST** (fictional example citation in `delegation-and-review/SKILL.md:472`) | never created, never rewritten |

**Sibling-adjacency invariant (from R1a / manifest):** all `issue115` probe units
(stage2, t2*, t5*) land FLAT under `evidence/probes/` so the sibling-relative
references R1a introduced (`ROOT/../<unit>`) continue to resolve. The round5 unit
is the one intentional nesting (E-3).

**Disposition status carried into the mapping:** the 8 R1a-dispositioned harnesses
still relocate by path-only `git mv` (they are part of their units), but remain
`non-rerunnable historical artifact` — not required to run green after the move, and
a post-move failure in them is not a regression (R1A-DISPOSITION.md §2). The 4
R1a-hardened harnesses relocate with depth-independent location logic; note the
erratum (R1A-DISPOSITION.md §2) that `t2probe-prefix`/`t2probe-scored` invoke a
disposition-set prereg checker at runtime and so are depth-hardened but not
end-to-end re-runnable post-relocation.

## 5. Consumer rewrites (carried from the manifest; unchanged by R2)

R2 changes no consumer. The manifest enumerates all 68 external consumer sites and
the Tier-1 lockstep set that a path-only move must update IN THE RELOCATION COMMIT:
- README* gate-checked markdown links (`checks.py` "inline relative markdown links resolve");
- the skill-vetting hook's threat-model pointer (`hooks/skill-vetting-advisory.py:9` — a module-docstring "Design record:" reference, NOT a runtime emission; the manifest's "emits" wording is imprecise, though the citation and the required file-move update are exact) + BOTH test assertions (`test-skill-vetting-advisory.py:1305` literal `assertIn` AND `:1309` `os.path.join(REPO,"reviews",…)` segment-form);
- (corpus Tier-1 is not in this move-set — leave-in-place-pinned).
Tier-2/3 (provenance/SKILL.md pointers, ROADMAP/ARCHITECTURE links, docstrings,
skills-staging cites incl. the `2026-07-25-skill-vetting-*.md` glob) update at
move time. The fictional `reviews/styling-ledger.md` is never rewritten.

## 6. Freeze declaration + next step

**This mapping is FROZEN.** The open items the manifest deferred (E-2, E-5) are
closed; E-3/E-4/corpus are settled; the packaging-surface gate passes (rename-only,
no active-surface or new-shipped-surface change). Every remaining `reviews/<unit>`
maps mechanically to `evidence/{reviews|probes}/<unit>` by artifact role, basename
preserved.

**The actual path-only relocation (`git mv` + the Tier-1 lockstep consumer
rewrites + the E-4/E-3 placements) is a SEPARATE change requiring its OWN
authorization.** It is NOT performed here. Canonical battery must be green before
AND after it. `corpus/` and E-5 `hcsa1-b0` are explicitly out of that move-set.
