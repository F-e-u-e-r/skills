# Limitations

These are bounded observations about one revision of one system, produced by an AI-assisted
procedure. They are not statistical benchmarks and not a quality ranking of either system.

1. **n = 1 per behavioral cell.** All 21 behavioral cells (6 first-run consumption, 6 matched-content
   consumption, 3 control-binding, 2 additivity, 4 routed-command) were run once each with a fresh
   subagent. No cell was repeated; no variance is estimated; a single run can be wrong in either
   direction.
2. **Single model family.** Every behavioral cell was consumed by `claude-sonnet-5`; the orchestrator
   and scorer was `claude-opus-4-8`. Nothing here is replicated on another model family, and the
   behavioral findings (gating, default inheritance, routing discipline) should be read as "observed with
   these models".
3. **Not blind.** The agents were told they were in a controlled test and instructed to follow only the
   supplied reference file(s); they were not told the hypothesis, but the design was neither
   hypothesis-blind nor double-blind, and the cells were scored by the orchestrating model against the
   canonical dial predicates, not by an independent human rater.
4. **Tested revision only.** All statements are about `pbakaus/impeccable` at
   `9d715cc4f5564a990ca8345abfdd5df6dc9b41c8`. The default branch head was still that commit at the end of
   the study and at packaging; anything after it is out of scope. The prose-validator interaction (T10) is
   a property of that revision's `docs/STYLE.md`.
5. **Semantic classification is judgment.** The 274 relation records and the 61 detector classifications
   are AI-assisted readings with recorded confidence (137 high, 137 pattern-inferred); they were
   completeness-checked (every corpus rule id accounted, every detector id exactly once) but not
   independently double-coded. The relation records themselves are not published because they quote
   Impeccable statements; only counts are.
6. **Conflicts are paraphrased.** The 10 conflict rows carry our paraphrase of both sides and a pointer
   (commit, path, line); readers should consult the cited lines at the pinned commit rather than rely on
   the paraphrase.
7. **Detector alignment is a reading, not an execution.** The detectors are compiled Rust/WASM; the study
   read their catalog and mapped it semantically. No detector was executed against fixtures.
8. **The candidate derivation is not publicly re-derivable.** Selecting the 16 candidate rules from the
   42 MOTION records used the relation-level maps, which stay internal. The derived ledger (ids,
   accounting buckets, exclusions) ships as a fixture instead, and every downstream test runs from it.
9. **Fan-out is a structural check.** "PRESERVED" for the 22 evaluated outputs means the shards,
   attribution file, links and ids are present and intact in the built output trees; the shards were not
   executed inside each provider's harness. Behavioral routing (T13) was tested in one harness (Claude
   Code) only, and `overdrive` only statically.
10. **Reproduction environment.** The fresh reproduction build ran the host's `scripts/build.js` under
    Node v23.10.0 with `--skip-root-sync`, reusing the study's installed devDependencies rather than a
    clean install; the host's own scripts invoke the same file through `bun`. Build output counts
    matched the study's.
11. **Provider counts depend on the counting unit.** 19 transformer definitions, 23 `dist/` directories
    (including `universal` and three packaging-oriented directories), 22 evaluated outputs, 2 zip
    archives — see `METHODOLOGY.md` §4 before comparing any of these numbers with other sources.
12. **The first-run arms are superseded.** `T07-first-run` and the first projector are preserved for
    history (`CORRECTIONS.md` C2, C3); they must not be read as findings.
