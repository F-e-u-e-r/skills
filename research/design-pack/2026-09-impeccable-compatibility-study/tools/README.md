# tools/ — 8 reproduction tools

All tools read the public corpus (`corpus/design-pack/public_records.json`, sha256-pinned to the sealed
corpus) and the fixtures in `../fixtures/`, and write only to `--workspace` (default `./workspace`).
`_common.py` is a shared argument/path helper, not a tool. Run order and expected results are in
`../METHODOLOGY.md` §8.

| Tool | Produces | Test |
|---|---|---|
| `project_motion.py` | first-design projection + two arms (superseded design, kept for history) | T06, T07-first-run |
| `fidelity_test.py` | control-fidelity gate over the projection, with 3 negatives | T06 |
| `build_matched_arms.py` | matched-content structured/prose arms (`fixtures/matched/`) | T07 |
| `second_source_test.py` | input-mutation proof (`fixtures/second_source_test/`) | T15 |
| `build_rules_only.py` | control-independence proof; rules-only reference, raw + normalized | T09, T10 |
| `gen_shards.py` | 4 per-command shards (raw + normalized) + shard manifest | T13 |
| `gen_attribution.py` | third-party attribution fixture | T16 |
| `attribution-gate.py` | attribution/allowlist gate over a built `dist/` tree (`--dist`) | T16 |

Two derivation scripts used during the study (candidate selection and consumer-map derivation) are not
published because they read the internal relation-level maps; their outputs ship as fixtures
(`motion-rules-only-candidate.json`, `consumer-reachability.json`).
