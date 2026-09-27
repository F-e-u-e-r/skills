# Report — Impeccable compatibility study (2026-09)

**Independent study; not affiliated with or endorsed by the Impeccable maintainers.** Subject:
`pbakaus/impeccable` at commit `9d715cc4f5564a990ca8345abfdd5df6dc9b41c8` (Apache-2.0; plugin 4.4.0,
npm 4.1.0, engine 0.1.6). Comparison corpus: the Design Pack canonical corpus of this repository
(seal `bd8cb1a`, sha256 `16ad01fb…`, 542 records). Every finding below is written as what the study
observed at that revision; the machine-readable form, with the sha256 of each internal source artifact,
is `RESULTS.json`. Units are defined before they are used (§12 defines every provider count). Five
interim claims were superseded during the study; they are preserved in `CORRECTIONS.md` and referenced
where relevant.

## 1. Inventory (T01)

At the tested revision the study inventoried 1 skill and 24 commands: 23 active and 1 deprecated alias
(`craft`), which is excluded from every semantic denominator below. Each command reads one reference
file (`skill/reference/<command>.md`) on demand, some with a native-platform variant, and 12 further
reference files are not tied to a command. 61 deterministic detectors (32 "slop", 29 "quality") are
implemented in compiled Rust/WASM. Command descriptions are not reproduced here; `RESULTS.json` T01
lists name, status, alias target and reference path only.

## 2. Semantic overlap accounting (T02)

The corpus's 448 rule and synthesized-rule records were related to the host's reference statements in
274 relation records, one classification each. Three numbers are reported and never collapsed into one:

- **274 relation records**;
- **182 distinct Impeccable reference statements** (a reference file plus heading, further distinguished
  by the specific statement cited; these fall under 97 distinct file-and-heading anchors in 19 reference
  files);
- **448 distinct corpus ids** — every rule and synthesized-rule record, a complete partition with no gap
  or overlap.

Classes: DESIGN_PACK_MORE_SPECIFIC 100 · EQUIVALENT 63 · IMPECCABLE_MORE_SPECIFIC 30 ·
DESIGN_PACK_ONLY 27 · COMPLEMENTARY 26 · IMPECCABLE_ONLY 12 · POTENTIAL_CONFLICT 10 ·
NOT_COMPARABLE 6 (definitions in `METHODOLOGY.md` §3). Confidence was recorded per record: 137 high,
137 pattern-inferred. The dominant pattern is the corpus adding a concrete threshold, override or
verification level to a principle the host states qualitatively; a solid convergent core (63 equivalent)
sits under it, and in 30 records the host is the more operational side (concrete numeric fills where a
corpus record is a bare heuristic). The relation records are not published (they quote host statements);
the counts are.

## 3. Conflicts (T03)

Ten relation records were classified POTENTIAL_CONFLICT: 7 real, 2 real-but-narrow, 1
apparent-and-resolved-by-scope. All ten are rule-level threshold, default or exception mismatches;
none is structural; no winner was picked. `RESULTS.json` T03 carries each as a pointer row (commit,
path, locator, our paraphrase of both sides, the corpus record's effective semantics). In brief, the
pairs are: a single 44 px interactive-target minimum versus a 24 px web-pointer minimum with a separate
touch minimum; an unconditional ban on eyebrow labels (twice: section and hero) versus bounded use under a
count ceiling; a categorical rejection of nested cards versus purposeful container nesting; a prescribed
slight tracking increase for light-on-dark body text versus avoiding body tracking; gray-neutrals-by-
default versus tinted-neutrals-by-default; hue-from-meaning versus a genre-to-palette default; two
fixed-percentage accent bands versus a rejection of fixed-percentage dosage; and a 4.5:1 floor for
error/success colors whose text-versus-non-text scope decides whether it meets the host's 3:1 non-text
allowance.

## 4. Detector alignment (T04)

All 61 detector ids were classified exactly once against the corpus: 9 direct executable matches, 38
partial, 9 adjacent signals, 5 host-only. Read in reverse, 216 corpus rules qualify as hard or
surfaced-with-L1-verification requirements; 40 of them correspond to a direct or partial detector and
176 do not — concentrated in INTERACT (34), A11Y (33) and STRUCT (48), i.e. runtime and interaction
behavior a static snapshot analyzer does not see. Detector names and descriptions are not reproduced;
ids, categories and our classification are.

## 5. Control layer and runtime accounting (T05)

The corpus's 6 runtime controls (3 dials, 3 decision tables) were evaluated separately from the rule
records: closure of every control to its target rules holds; classes DESIGN_PACK_MORE_SPECIFIC 3,
COMPLEMENTARY 2, DESIGN_PACK_ONLY 1; 0 hard control-layer conflicts. Two soft observations were recorded:
the two systems' controls are of different kinds (semantic rule-gating dials versus user-facing tuning
parameters), and the MOTION dial's baseline is more motion-committing than the host's restraint-leaning
default — the seed of §9.

**Runtime accounting, stated once:** 448 rule and synthesized-rule records were mapped and accounted
(§2) and 6 runtime controls were evaluated separately (this section); together these correspond to the
corpus's 454 runtime records. The study does not claim an existing single combined 454-row public
ledger. The 88 support records (85 evidence, 3 conflict) are a separate slice, described in
`PROVENANCE.md`, and were not mapped.

## 6. Deterministic projection and fidelity gate (T06)

A projector selected 9 corpus ids (5 MOTION rules, the MOTION dial and its 3 target rules) and emitted a
machine-readable projection plus two reference arms. Regeneration was byte-identical. A fidelity gate
checking control id, variable, range, baseline, the three predicates and the three targets passed on the
real projection and failed on all three deliberately corrupted variants (a missing target, an altered
threshold, a flattened control) — the gate was shown able to fail. Reproduced in this packaging session
(`tools/project_motion.py`, `tools/fidelity_test.py`: identical bytes, gate PASS, 3/3 negatives fail).

## 7. Representation ablation (T07; first run superseded)

With two arms carrying **identical** semantic fields (21 checked: control id, variable, range, baseline,
three predicates, three target ids, strengths, enforcement, selector, override, condition and the five
baseline rule ids), differing only in representation (fenced YAML block versus prose sentences), the
consuming agent gated correctly in 3/3 cells for the structured arm and 3/3 for the prose arm — at
intensity 2 (nothing active), 7 (all three active) and 7 with reduced motion (all three, the a11y rule
absolute). The study therefore observed that the reference layer preserved control behavior in either
representation when the predicates, targets and conditions were complete. The first run's 3/3 versus
0/3 (`T07-first-run`) is superseded: its prose arm had ids and thresholds removed, so it measured
information loss, not representation (`CORRECTIONS.md` C2); its intensity-2 structured cell also
over-applied the a11y rule because the first projector injected a non-canonical clause (C3).

## 8. Control input and default behavior (T08)

The host exposes no structured source for the dial's variable at the tested revision (no intensity
argument, no bounded scale in its context files or command modes). In three cells with the host's own
motion reference plus the faithful structured arm: with **no** explicit intensity the agent resolved the
dial to its baseline 6 and activated the three gated rules, explicitly noting the disagreement with the
host reference's restraint posture; "restrained" resolved to 5 (two rules); "bold" resolved to 8
(three rules). No rule step exists above 5, so the 1–10 dial has about three effective bands. The
study classifies the no-input path as a real default conflict (`CORRECTIONS.md` C4): a canonical control
default became the host's implicit default because nothing in the host supplied the value.

## 9. Rules-only candidate (T09)

Of the 42 MOTION rule records, 16 were selected as additive and control-independent: 18 were excluded
as equivalent to host guidance, 3 as host-stronger, 3 as having no host consumer, 2 as depending on the
dial (42 = 16 + 18 + 3 + 3 + 2). The 16 carry classes DESIGN_PACK_MORE_SPECIFIC 13 and COMPLEMENTARY 3;
none has a selector or references the dial, a threshold or the intensity variable (16/16
control-independent; reproduced identically by `tools/build_rules_only.py`). The selection used the
internal relation records and is not publicly re-derivable; the derived ledger ships as a fixture.

## 10. Build prose gate (T10)

The host's build runs a prose validator over its skill sources. Projecting the 16 rules' corpus text
unchanged failed that validator on the U+2014 em dash (16 occurrences, one per rule's public
expression). A deterministic adapter-side transform — em dash to comma-space, applied only to the
projection, never to the corpus — passed two guards (only the em dash changed; no wording changed) and
the build then completed. The fresh reproduction build in this packaging session behaved the same way
(exit 0; both prose validators clean with the normalized shards).

## 11. Codex build path (T12)

The build regenerated `.codex/skills/impeccable/reference/` including the shards and links. This
supersedes the intake-stage reading that the Codex output had no per-command reference directory,
which came from the committed clone's partial `.codex` tree (`CORRECTIONS.md` C1). Confirmed on the
fresh build (codex output PRESERVED).

## 12. Provider fan-out (T11) — counting units first

| Unit | Count | Definition at `9d715cc4` |
|---|---|---|
| transformer definitions | **19** | entries of `PROVIDERS` in `scripts/lib/transformers/providers.js`, one `configDir` each (the `antigravity` entry uses `.agent`) |
| build-log "providers" | **19** | the build's own count when assembling `dist/universal` — the same set |
| `dist/` directories | **23** | the 19 transformer-named directories + `cursor-plugin` + `openai` + `vscode` + `universal` |
| `universal` | **1** | an aggregate directory holding all 19 `configDir` trees; inside the 23, outside the evaluation |
| evaluated fan-out outputs | **22** | the 23 minus `universal`; each checked for the 4 shards, the attribution file, the 4 command links, all 16 ids and no unrelated-command link |
| zip packaging outputs | **2** | `openai-plugin.zip`, `universal.zip`; archives of the above, not separately evaluated |
| attribution-gate reference dirs | **41** | `skills/impeccable/reference/` directories found across the 23 `dist/` directories |

After normalization, **22 of 22** evaluated outputs carried the candidate intact — all 16 ids, byte-
consistent content, no output rewrote semantics, none blocked. The fresh reproduction build reproduced
22/22 PRESERVED with the links in place.

## 13. Selective loading and routing (T13)

The reachability map assigns every candidate rule exactly one consuming command: `animate` 9, `audit`
3, `polish` 3, `overdrive` 1 (not `critique` — `CORRECTIONS.md` C5). Four per-command shards were
generated from the single corpus source with no id duplicated; each consuming command's reference
gained one link to its own shard; the shards are not linked from the skill's always-on routing, so an
ordinary invocation does not load them. In the built outputs, 22/22 kept the per-command links, no
unrelated command linked a shard, and no shard carried another command's ids. Behaviorally (n = 1 per
route): `animate` loaded only its shard and applied 4 of 9 rules, holding 5 as loaded-not-applicable;
`audit` applied 2 of 3 and did **not** reach the `animate`-shard rule an `ease` keyword would have
triggered (the overreach bait); `polish` applied 2 of 3; `colorize` (negative control) opened none of
the shard files although they were present; `critique` carries no link and is structurally identical to
`colorize`; `overdrive` was verified statically only.

## 14. Behavioral additivity (T14)

With the host's own motion reference alone as baseline, adding the 16-rule reference led the agent to
apply 8 rules as non-redundant concrete triggers and to hold the other 8 as not applicable to the task
(no stretching); it referenced neither the dial nor baseline 6 and did not over-apply the excluded
control-dependent rules.

## 15. Single source of truth (T15)

Mutating only the corpus input (baseline 6 → 4; one threshold `> 4` → `> 6`) changed exactly those two
values in the regenerated control block, left the other gates unchanged, and the live reference carried
the original-input values — no hand-maintained duplicate of rule text or thresholds exists.
Reproduced identically by `tools/second_source_test.py`.

## 16. Attribution propagation (T16)

The host build places no root notice file into the provider skill packages (only the `cursor` and
`vscode` outputs receive the Apache-2.0 license file), so a repository-root-only third-party notice
would be orphaned from the packaged distributions. A single attribution file preserving each origin's
MIT copyright line and full permission text was therefore placed next to the shards. In the built
outputs it travelled with them into 22/22 evaluated outputs (0 orphans); a deterministic gate over 41
reference directories in 23 `dist/` directories passed, and failed on both negatives (attribution
removed; an unapproved id injected). Fresh build: gate PASS, 41/23. A production-shaped disposable patch
was used for the study's routed build; it is internal evidence (sha256 prefix `526fc4db`, 15 files,
+1577 lines) and is not shipped.

## 17. License provenance (T17)

All 16 candidate rules trace to MIT-licensed upstreams verified at pinned commits: 9 to
`nextlevelbuilder/ui-ux-pro-max-skill` (`dcc40ff5`), 5 to `Nutlope/hallmark` (`13ac0ec7`), 2 to
`Leonxlnx/taste-skill` (`c184364c`); no path-level license exception exists at those commits. What the
fixtures carry is Design Pack-derived governance metadata, not upstream source.

## 18. Upstream freshness (T18)

`refs/heads/main` of `pbakaus/impeccable` was `9d715cc4` at the end of the study and again at packaging
(2026-09-27T20:14:53Z UTC).

## 19. What these results do and do not establish

They establish, for the tested revision and the bounded behavioral runs described in this study:
that the host's reference layer, build and fan-out can carry a deterministic, attributed projection
of corpus semantics to every evaluated output without a second source of truth; that faithful gating
depends on information completeness rather than serialization format; that the tested consumer-
scoped routing confined the projected semantics to the declared consumers; and that, on the tested
no-input path, the canonical control default became the effective host default when the host
supplied no value.

They do not establish: statistical reliability (n = 1), cross-model generality (one family), runtime
behavior inside any provider other than the one harness used, the correctness of either rule set, or
anything about revisions after `9d715cc4`. See `LIMITATIONS.md`.

## 20. Future synthesis candidates (listed only; nothing adopted)

Six candidate learnings were noted for a separate, owner-gated synthesis pass. They are **not** adopted
into Design Pack by this study, and any future adoption would go through comparison against the corpus
and the skills' own text first:

1. control fidelity depends on preserving explicit predicates, targets and conditions, not on
   serialization format (§7);
2. consumer-scoped selective loading limits unrelated semantic overreach (§13);
3. consumer-specific normalization belongs in a projection adapter, never in the canonical corpus (§10);
4. a canonical control default must not cross a system boundary without an explicit input contract (§8);
5. attribution must co-propagate with every distributed artifact, because downstream packaging can drop
   root notices (§16);
6. byte-identical regeneration plus input-mutation propagation is a workable proof of a single source of
   truth (§15).
