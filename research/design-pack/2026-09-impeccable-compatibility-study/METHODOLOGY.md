# Methodology

## 1. Subject, corpus, environment

- **Subject:** `pbakaus/impeccable`, commit `9d715cc4f5564a990ca8345abfdd5df6dc9b41c8`, cloned clean;
  Apache-2.0; plugin 4.4.0, npm 4.1.0, engine 0.1.6. Read-only throughout: every build ran on a
  disposable copy, never on the clone; no issue, pull request or contact with the project.
- **Corpus:** `corpus/design-pack/public_records.json` of this repository, sha256
  `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, sealed at commit
  `bd8cb1a97474b7a180b93f50bb114404da2d2b99`; 542 records = 454 runtime (443 rule, 5 synthesized_rule,
  3 decision_table, 3 dial) + 88 support (85 evidence, 3 conflict). The corpus was immutable for the
  study; "Impeccable exposes a better rule" was recorded as a finding, never as a corpus change.
- **Study sessions:** 2026-09-27/28, Claude Code, one orchestrating session (`claude-opus-4-8`) that
  spawned subagents; the exact Claude Code CLI version of the study session is not recorded.
- **Packaging/validation session:** 2026-09-28, Claude Code 2.1.283, `claude-fable-5-1`; Node
  v23.10.0 for the host build; Python 3.9 for the tools.

## 2. Models, cells, blindness

| Role | Model | Count |
|---|---|---|
| orchestrator, classifier, scorer | `claude-opus-4-8` | 1 session |
| behavioral cells (consumption, control-binding, additivity, routed commands) | `claude-sonnet-5` subagents | 21 cells, **n = 1 each** |
| read-only fact verification of repository claims | `claude-opus-4-8` subagent | 1 |
| packaging, reproduction, validation | `claude-fable-5-1` | 1 session |

Cells: 6 first-run consumption (2 arms × 3 conditions), 6 matched-content consumption (2 × 3),
3 control-binding (no signal / "restrained" / "bold"), 2 additivity (baseline / candidate), 4 routed
commands (`animate`, `audit`, `polish`, `colorize`). Each cell was one fresh subagent given the file
path(s) of the reference(s) to follow, told to read them with the shell (`cat`; the subagent file-read
tool was sandboxed to the project directory), told to follow only those files and to answer from them,
and asked to declare the active gated-rule set (consumption cells), the resolved intensity and posture
(control-binding), or the rules loaded and applied (routed and additivity cells). The prompts stated
that the run was a controlled test of whether the reference is followed. **The design was not
hypothesis-blind or double-blind**: agents were not told the hypothesis, but they knew they were being
tested, and the orchestrating model scored their declarations against the canonical dial predicates.
Per-cell model identity was verified during packaging from the subagent transcripts (internal); every
behavioral cell resolved to `claude-sonnet-5`.

## 3. Definitions

- **Relation record** — one classified link between an Impeccable reference statement (file + heading,
  distinguished by the specific statement cited) and one or more corpus ids; one-sided records carry a
  null side rather than a fabricated link.
- **Classes (exactly one per record):** EQUIVALENT (same condition/scope and materially the same
  behavior); IMPECCABLE_MORE_SPECIFIC (compatible, the host narrower or more operational);
  DESIGN_PACK_MORE_SPECIFIC (compatible, the corpus carrying stronger structured semantics — condition,
  strength, exception, override, verification or control); COMPLEMENTARY (coexist, different
  dimensions); POTENTIAL_CONFLICT (overlapping trigger, materially incompatible guidance, threshold or
  precedence — never merely "one side is stricter"); IMPECCABLE_ONLY; DESIGN_PACK_ONLY; NOT_COMPARABLE
  (routing, tooling, workflow, machinery).
- **Three accounting numbers, never collapsed:** relation records; distinct Impeccable reference
  statements; distinct corpus ids. Commands: inventory 24 = 23 active + 1 deprecated alias (`craft`),
  the alias excluded from every semantic denominator. Detectors: all 61 ids appear exactly once.
- **Runtime accounting:** 448 rule/synthesized-rule records mapped (T02) + 6 runtime controls evaluated
  separately (T05) correspond to the 454 runtime records; no single combined 454-row ledger is claimed;
  the 88 support records are described separately and were not mapped.
- **Conflict verdicts:** real / real-narrow / apparent-resolved-by-scope; no winner picked.
- **Behavioral ground truth:** the canonical dial `DIAL-2002` (range 1–10, baseline 6, predicates
  `value > 3 → A11Y-2001`, `value > 4 → MOTION-2003`, `value > 5 → MOTION-2005`; A11Y-2001 has
  `selector: DIAL-2002`, strength absolute and enforcement hard_block, meaning non-overridable once
  active). A cell is CORRECT when the declared active set equals the predicate-derived set for the
  stated intensity, and the a11y rule's status matches.

## 4. Provider counting units (defined before use)

| Unit | Count | Definition at `9d715cc4` |
|---|---|---|
| transformer definitions | 19 | entries of `PROVIDERS` in `scripts/lib/transformers/providers.js`, one `configDir` each (`antigravity` ↔ `.agent`) |
| build-log "providers" | 19 | the build's own count when assembling `dist/universal`; same set |
| `dist/` directories | 23 | 19 transformer-named + `cursor-plugin` + `openai` + `vscode` + `universal` |
| `universal` | 1 | aggregate of all 19 `configDir` trees; counted in the 23, excluded from evaluation |
| evaluated fan-out outputs | 22 | the 23 minus `universal` |
| zip packaging outputs | 2 | `openai-plugin.zip`, `universal.zip`; not separately evaluated |
| attribution-gate reference dirs | 41 | `skills/impeccable/reference/` directories walked across the 23 |

An output is **PRESERVED** when its reference directory holds the 4 shards and the attribution file,
each of the 4 consuming command references links only its own shard, the shards together carry exactly
the 16 candidate ids, and none of `colorize`, `layout`, `typeset`, `critique`, `harden`, `clarify`
links a shard.

## 5. Procedures — analysis tests

- **T01 inventory:** read `skill/scripts/command-metadata.json`, `skill/SKILL.src.md` and
  `skill/reference/` at the pinned commit; record name, status, alias, reference path, native variant;
  list non-command references; count detectors from `crates/live/assets/antipatterns.json`.
- **T02 semantic map:** five subagent passes, one per cluster (A11Y+INTERACT, MOTION, STRUCTURE,
  UX+ANTISLOP, VISUAL), each producing relation records against the pinned reference files and the
  corpus fields (`effective_semantics`, not prose); completeness invariant: the union of corpus ids equals
  the cluster's id set; grounding: zero unknown ids, every cited file on disk; re-verified on every
  hand-back. Counts recomputed at packaging from the records.
- **T03 conflicts:** every POTENTIAL_CONFLICT re-read against raw bytes (host line, corpus effective
  semantics); verdict recorded; no winner. Published in pointer form.
- **T04 detectors:** all 61 ids classified once; reverse gap = corpus rules with enforcement in
  {hard_block, must_surface} or verification in {L1, L1+L2} that are not a candidate of any direct or
  partial detector record.
- **T05 controls:** 6 controls related with the same class model; closure to target rules checked.

## 6. Procedures — projection and behavioral tests

- **T06:** `project_motion.py` (first design) → projection JSON + two arms; `fidelity_test.py`
  validates the control fields and three corrupted variants.
- **T07:** first run — 2 arms × 3 conditions (intensity 2; 7; 7 with `prefers-reduced-motion`), one
  subagent per cell; matched-content run — arms from `build_matched_arms.py` (21 semantic fields
  verified identical by script), same 2 × 3 design, fresh subagents.
- **T08:** three subagents executing the host's `animate` reference plus the faithful structured arm on a
  landing-page hero task; signal absent / "restrained, subtle" / "bold, expressive"; recorded resolved
  intensity, posture and active set.
- **T09:** candidate selection from the 42 MOTION records using the relation records (internal), then
  `build_rules_only.py`: control-independence proof (no selector; no textual reference to the
  intensity variable, dial or thresholds) and the rules-only reference.
- **T10–T12:** on a disposable copy of the clone: add the single-file candidate (T10/T11) or the four
  shards and links (T13); run `node scripts/build.js --skip-root-sync`; raw text → validator failure
  recorded; normalized text (`normalization-contract.json`: U+2014 → `, `, guards: only the em dash
  changed, no wording changed) → build success; inspect each `dist/` directory (T11) and the codex
  directory (T12).
- **T13:** `derive_routing.py` (internal) produced the consumer map from the relation records;
  `gen_shards.py` produced 4 shards + manifest; each consuming command reference received one link;
  static PRESERVED check on 22 outputs; behavioral cells for `animate`, `audit` (with an `ease` keyword
  as overreach bait for a rule that lives in the `animate` shard), `polish`, and `colorize` as negative
  control; `overdrive` static only.
- **T14:** two subagents on the same task, one with the host's motion reference alone, one with the
  reference plus the 16-rule candidate; applied / not-applicable / dial-leakage recorded.
- **T15:** `second_source_test.py`: mutate the corpus input in memory, regenerate, compare.
- **T16:** `gen_attribution.py` produced the attribution file; `attribution-gate.py` walked every
  `dist/` directory (orphan check, unapproved-id check, origin and permission-text check); negatives
  were run by removing the attribution from one output and by injecting `MOTION-9999`.
- **T17:** each origin's `LICENSE` re-fetched at its pinned commit; source-path directories checked for
  component-specific license files.
- **T18:** `git ls-remote https://github.com/pbakaus/impeccable.git refs/heads/main`.

## 7. Publication method

Every internal artifact (85 files) received a disposition in an owner-reviewed ledger: shipped verbatim,
aggregated into `RESULTS.json`, published in redacted pointer form, kept internal, or excluded as
containing the subject's expression. Impeccable text is never reproduced: conflicts and inventory are
pointer-form (commit, path, heading or line, our paraphrase). Two gates ran on the finished package: an
8-word-shingle overlap scan of every package file against the whole Impeccable source tree at the pinned
commit, and a bounded manual review for shorter copied expressions. The ledger, gate outputs and the
plugin-install proof are kept in this repository under
`evidence/reviews/2026-09-28-impeccable-study-release-spec/release-validation/`.

## 8. Reproduction recipe (public inputs only)

Inputs: this repository (the corpus and this directory), Impeccable at `9d715cc4`, Node ≥ 20, Python ≥ 3.9.

```bash
# 1. regenerate the fixtures from the public corpus (order matters for the first two)
cd research/design-pack/2026-09-impeccable-compatibility-study/tools
python3 project_motion.py      --workspace /tmp/ws     # first-design arms (superseded; see CORRECTIONS C2/C3)
python3 fidelity_test.py       --workspace /tmp/ws     # expect: FIDELITY GATE: PASS (3 negatives fail)
python3 second_source_test.py  --workspace /tmp/ws     # expect: VERDICT: SINGLE SOURCE OF TRUTH
python3 build_matched_arms.py  --workspace /tmp/ws     # expect: PARITY: PASS; identical to fixtures/matched/
python3 build_rules_only.py    --workspace /tmp/ws     # expect: ALL 16 CONTROL-INDEPENDENT: True
python3 gen_shards.py          --workspace /tmp/ws     # expect: 16 ids, duplicated: NONE
python3 gen_attribution.py     --workspace /tmp/ws     # expect: em dashes 0; 3 origins; 16 ids
diff -r /tmp/ws/artifacts/shards ../fixtures/shards && diff -r /tmp/ws/artifacts/matched ../fixtures/matched
```

```bash
# 2. rebuild the host at the pinned commit on a disposable copy with the fixtures applied
git clone https://github.com/pbakaus/impeccable.git /tmp/impeccable && git -C /tmp/impeccable checkout 9d715cc4f5564a990ca8345abfdd5df6dc9b41c8
cd /tmp/impeccable && npm install            # devDependencies (archiver) are needed by scripts/build.js
F=<path-to>/research/design-pack/2026-09-impeccable-compatibility-study/fixtures
for c in animate audit overdrive polish; do
  cp "$F/shards/motion-dp-$c.normalized.md" "skill/reference/motion-dp-$c.md"
  printf '\n<!-- Design Pack motion rules (generated projection) -->\nFor additional structured motion rules, load [reference/motion-dp-%s.md](motion-dp-%s.md).\n' "$c" "$c" >> "skill/reference/$c.md"
done
cp "$F/motion-dp-THIRD-PARTY.md" skill/reference/
node scripts/build.js --skip-root-sync        # expect exit 0; the build reports the universal directory assembled from 19 providers and both prose validators clean
```

```bash
# 3. gates on the built output
python3 <tools>/attribution-gate.py --dist /tmp/impeccable/dist   # expect: GATE PASS (41 reference dirs, 23 dist directories)
ls /tmp/impeccable/dist | wc -l                                    # expect 25 entries: 23 directories + 2 zips
```

The three appended lines are ours (a blank line, an HTML comment, one sentence with a relative link);
they are the only edits made to host files in the study's routed build, apart from a root `NOTICE.md`
pointer that is not needed to reproduce any measured property. Raw (un-normalized) shards can be
substituted in step 2 to reproduce the T10 validator failure.
