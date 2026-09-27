# Corrections

Five interim claims made during the study were superseded before publication. They are preserved here
with the evidence that replaced them; the internal artifacts that still carry the interim wording are
named so that a reviewer can check the history rather than take the final wording on trust. Nothing in
`REPORT.md` or `RESULTS.json` relies on an interim claim.

| # | Interim claim | Where it was made | Superseding evidence | Consequence |
|---|---|---|---|---|
| **C1 — Codex blocker** | The Codex output has no per-command reference directory, so a reference-shard projection is blocked for Codex (intake local blocker "LB2"; option B "blocked for Codex"). | intake exit report §9/§11; `integration-blockers.json` (sha256 `b2f4fc7b…`); `architecture-options.json` (`8dbc440d…`) | Running the host's actual build regenerated `.codex/skills/impeccable/reference/` with the candidate shards and links; the committed clone's `.codex` tree was a partial, stale snapshot. Confirmed again on the fresh reproduction build (T11/T12: codex output PRESERVED). | The blocker is withdrawn. The intake-stage artifacts are published only as restated counts; the interim wording is not copied. |
| **C2 — flattened 0/3** | A structured (YAML) control block is load-bearing: the structured arm gated 3/3, the prose arm 0/3. | first-run consumption cells; `consumption-results.json` (`e01fc267…`) | The first prose arm had the rule ids and thresholds stripped, so the comparison ablated information, not representation. Matched-content arms with 21 identical semantic fields gated 3/3 and 3/3 (`matched-consumption-results.json`, `12450366…`). | The finding is inverted: representation is not load-bearing, information completeness is (T07). The first run is kept as `T07-first-run`, status superseded. |
| **C3 — low-intensity A11Y** | At intensity 2 the structured arm correctly enforced A11Y-2001 as an absolute floor because motion was present. | first-run cell S-A; the first projector's `interpretation` clause | Re-reading the sealed records: A11Y-2001 carries `selector: DIAL-2002` and activates at `value > 3`; "absolute" means non-overridable once active, not active below its threshold. The first projector had injected a non-canonical clause; the cell was model over-application of an injected clause, not a canonical behavior. Corrected arms return not-active at intensity 2 in both representations. | The first projector (`tools/project_motion.py`) is published unchanged for reproducibility with this caveat in its docstring; the faithful arms are `tools/build_matched_arms.py`. |
| **C4 — baseline 6 scope** | The dial's baseline of 6 is `SCOPE_RESOLVED` because the dial's own mechanism (per-brief intensity, an override to 3) resolves the energetic default. | first PoC exit report §11 | No structured intensity source exists in the host at the tested commit, so the production default path is the no-input path; in that path the consuming agent anchored on 6 (T08). Reclassified as a real no-input default conflict; explicit user signals bind correctly (restrained → 5, bold → 8). | T08 reports the default-path conflict; the resolution is a control-input contract question, not a representation fix. |
| **C5 — critique consumer** | The `critique` command is a consumer of the MOTION-4008 candidate (fourth consumer alongside animate, audit, polish). | rules-only candidate exit report §4 | The reachability map routes every candidate rule to exactly one command: animate 9, audit 3, polish 3, **overdrive 1** (`consumer-reachability.json`, `b1c3e070…`). `critique` carries no motion link and loaded nothing in the routed run, structurally identical to the `colorize` negative control. | `critique` is removed as a candidate consumer; overdrive is the fourth consumer (T13). |

## What was not corrected

The 10 conflicts, the 8-class relation model, the detector classification, the fan-out and attribution
results and the license provenance stand as recorded; their internal artifacts were re-read during
packaging and the numbers in `RESULTS.json` were recomputed from them where the artifact is
machine-readable (T02, T04, T05, T09, T13).
