#!/usr/bin/env python3
"""Per-command generated shards (test T13): a clean partition of the 16 candidate rules into one shard
per consuming command (each rule in exactly ONE shard, no duplication), from the single corpus source.
Emits raw + normalized (motion-dp-normalize/1) variants and the shard manifest.

Inputs: the corpus and ../fixtures/consumer-reachability.json.
Writes <workspace>/artifacts/shards/motion-dp-<cmd>.{raw,normalized}.md and <workspace>/artifacts/shard-manifest.json
(expected byte-identical to the fixtures)."""
import json, os
from _common import parser, load_corpus, sha, ensure_dir

args = parser(__doc__).parse_args()
ART = ensure_dir(os.path.join(args.workspace, "artifacts"))
corpus = load_corpus(args.corpus)
matrix = json.load(open(os.path.join(args.fixtures, "consumer-reachability.json")))["matrix"]
EM = "—"
def normalize(s): return s.replace(" " + EM + " ", ", ").replace(EM + " ", ", ").replace(" " + EM, ",").replace(EM, ", ")
OUT = ensure_dir(os.path.join(ART, "shards"))

by_cmd = {}
for m in matrix:
    for c in m["consumer_commands"]:
        by_cmd.setdefault(c, []).append(m["id"])

def entry(rid, norm):
    r = corpus[rid]; es = r["effective_semantics"]; prov = r.get("provenance", {})
    pe = r.get("public_expression", "").strip()
    sc, co, ov = es.get("scope"), es.get("condition"), es.get("override")
    if norm:
        pe = normalize(pe); sc = normalize(sc) if sc else sc; co = normalize(co) if co else co; ov = normalize(ov) if ov else ov
    L = [f"### {rid}  [{es.get('strength')}, {es.get('enforcement')}, verify={es.get('verification')}]", f"- {pe}"]
    if sc: L.append(f"- scope: {sc}")
    if co: L.append(f"- condition: {co}")
    if ov: L.append(f"- override/exception: {ov}")
    L.append(f"- provenance: {prov.get('upstream_repo')} ({prov.get('design_phase')})")
    return "\n".join(L)

manifest = {}
for cmd, ids in sorted(by_cmd.items()):
    ids = sorted(ids)
    for tag, norm in (("raw", False), ("normalized", True)):
        body = "\n".join(entry(r, norm) for r in ids)
        art = f"""# MOTION reference: Design Pack rules for `{cmd}` ({tag})
<!-- generated projection of {len(ids)} sealed Design Pack MOTION rules routed to the {cmd} command; no dial/control -->
## Design Pack motion rules ({len(ids)})
{body}
"""
        p = os.path.join(OUT, f"motion-dp-{cmd}.{tag}.md")
        open(p, "w").write(art)
    manifest[cmd] = {"ids": ids, "count": len(ids),
                     "raw_sha": sha(os.path.join(OUT, f"motion-dp-{cmd}.raw.md"))[:16],
                     "normalized_sha": sha(os.path.join(OUT, f"motion-dp-{cmd}.normalized.md"))[:16]}
# duplication check: union of shard IDs == 16, no ID in >1 shard
allids = [i for c in by_cmd for i in by_cmd[c]]
dup = [i for i in set(allids) if allids.count(i) > 1]
json.dump({"schema": "shard-manifest/1", "shards": manifest, "total_ids": len(allids),
           "duplicated_ids": dup}, open(os.path.join(ART, "shard-manifest.json"), "w"), indent=2)
for c, v in sorted(manifest.items()): print(f"  motion-dp-{c}: {v['count']} rules  norm_sha={v['normalized_sha']}  ids={v['ids']}")
print("total IDs across shards:", len(allids), "| duplicated across shards:", dup or "NONE (single home per rule)")
