# Impeccable compatibility study (2026-09)

**Independent study; not affiliated with or endorsed by the Impeccable maintainers.**

An independent compatibility and integration-feasibility study of
[**Impeccable**](https://github.com/pbakaus/impeccable) at commit
`9d715cc4f5564a990ca8345abfdd5df6dc9b41c8` (Apache-2.0), evaluated against the Design Pack canonical
corpus of this repository (`corpus/design-pack/public_records.json`, sealed at `bd8cb1a`, sha256
`16ad01fb…`, 542 records). The study asked how the two rule sets overlap and conflict, and whether a
deterministic projection of corpus semantics could be carried, routed and attributed through the host's
existing reference layer, build and provider fan-out — measured on disposable copies, at one pinned
revision.

This directory is a **research record**, not a capability of the pack: nothing in it is adopted into
the skills, the corpus or the generated references, it is read by no loader, and it ships in no plugin.
The study makes no proposal to the Impeccable project and describes no contribution to it.

## Contents

| File | What it is |
|---|---|
| `REPORT.md` | findings by test family, in observation form, plus what they do and do not establish |
| `METHODOLOGY.md` | environment, models, cell construction, definitions, per-test procedure, reproduction recipe |
| `RESULTS.json` | machine-readable matrices for all tests; every number carries the sha256 of the internal artifact it came from |
| `LIMITATIONS.md` | the bounds of these observations |
| `CORRECTIONS.md` | five interim claims that were superseded during the study, preserved with their evidence |
| `PROVENANCE.md` | subject and corpus identities, license position, origin of every corpus id used in a fixture, AI tooling, internal-evidence anchors |
| `fixtures/` | 19 files: our projections, matched-content arms, control fixtures and attribution notice (all Design Pack-derived; no Impeccable text) |
| `tools/` | 8 reproduction tools (+ one shared helper module) that regenerate the fixtures from the public corpus and run the gates |
| `MANIFEST.sha256` | sha256 of every file in this directory |

## Headline observations (details and units in `REPORT.md`)

- 274 relation records connect 182 distinct Impeccable reference statements to all 448 rule and
  synthesized-rule records of the corpus; the largest class is the corpus adding a concrete threshold,
  override or verification to a principle the host states qualitatively (100), followed by equivalence (63).
- 10 rule-level conflicts (7 real, 2 narrow, 1 apparent) were recorded in pointer form; none is
  structural and none was adjudicated.
- A deterministic 16-rule MOTION projection survived the host's build and reached all 22 evaluated
  provider-specific outputs intact, routed only to its four consuming commands, once one adapter-side
  punctuation normalization (em dash) satisfied the host's prose validator.
- With identical facts, a prose control block gated as reliably as a YAML one (3/3 vs 3/3); the first
  run's 3/3 vs 0/3 was an information ablation and is preserved as a correction.
- With no explicit intensity, the consuming agent inherited the corpus dial's baseline (6) rather than
  the host's restraint posture — a default-path conflict, not a representation failure.
- Third-party attribution travelled with the derived shards into every evaluated output (0 orphans),
  because the host build ships no root notice into its provider skill packages.

## AI assistance

This study used AI-assisted repository analysis, semantic classification, test execution and synthesis
(Claude Code; models and sessions in `METHODOLOGY.md`). Every behavioral experiment cell used
**n = 1**; the results are **bounded observations, not statistical benchmarks**; all tested agent
behavior comes from a **single Claude model family**. The owner set the scope and acceptance criteria,
reviewed the corrections and took the publication decisions.

## License

Our report, matrices, fixtures and tools are released under this repository's MIT license
(`LICENSE` at the repository root). Impeccable is cited by commit, path, heading and line; no Impeccable
reference text, command or detector description, generated output, source snapshot or patch is included
(see `PROVENANCE.md`).

## Reproduce

`tools/README.md` gives the run order; `METHODOLOGY.md` §8 gives the full recipe, including how to
rebuild the host at the pinned commit with the fixtures applied. Inputs are public: Impeccable at
`9d715cc4`, this repository's corpus, and the fixtures here.

## Citation

> Impeccable compatibility study (2026-09): independent compatibility and integration-feasibility study of
> pbakaus/impeccable at commit 9d715cc4 against the Design Pack canonical corpus (seal bd8cb1a).
> F-e-u-e-r/skills, `research/design-pack/2026-09-impeccable-compatibility-study/`. MIT.
