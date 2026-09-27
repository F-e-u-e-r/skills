# fixtures/ — 19 files, all Design Pack-derived

None of these files contains Impeccable text; host reference files are cited only as `file#heading`
pointers. All are regenerable from the public corpus with `../tools/` except the two derived ledgers
marked *derived*, whose derivation used internal relation-level maps.

| File | Role | Test |
|---|---|---|
| `matched/structured3.md`, `matched/flattened3.md` | matched-content arms (identical 21 semantic fields; YAML vs prose) | T07 |
| `shards/motion-dp-{animate,audit,overdrive,polish}.{raw,normalized}.md` | per-command shards; `.normalized` = adapter transform applied | T10, T11, T13 |
| `motion-reference.rules-only.md`, `.normalized.md` | single-file 16-rule reference used in the first fan-out run | T10, T11 |
| `motion-rules-only-candidate.json` | *derived*: candidate ids, exclusion accounting (42 = 16+18+3+3+2), classes; public copy omits the internal file's license/proposed-use bookkeeping rows | T09 |
| `consumer-reachability.json` | *derived*: rule → consuming command (+ `file#heading` pointer) | T13 |
| `normalization-contract.json` | em-dash inventory and the frozen transform `motion-dp-normalize/1` | T10 |
| `shard-manifest.json` | shard identity ledger (ids, counts, hashes) | T13 |
| `second_source_test/control.from-{original,mutated}-input.json` | input-mutation controls | T15 |
| `motion-dp-THIRD-PARTY.md` | MIT attribution for the three origins of the 16 rules (copyright + full permission text); in the fan-out experiment it travelled next to the shards | T16, T17 |

The shard and reference fixtures are test payloads that were placed into disposable copies of the host
for measurement; they are not distributed anywhere else.
