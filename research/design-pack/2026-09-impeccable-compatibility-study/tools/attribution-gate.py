#!/usr/bin/env python3
"""Attribution/allowlist gate (test T16): deterministic; exit 1 on any violation. Run against a built
Impeccable `dist/` tree (see ../METHODOLOGY.md for the build recipe), the corpus and the 16-id
candidate allowlist. Checks: every allowlisted id has provenance and an expected-MIT origin; every
distribution reference directory that carries a motion-dp shard also carries the attribution file
(no orphan); shards carry only allowlisted ids; the attribution names every origin and the MIT text."""
import json, os, re, sys
from _common import parser, load_corpus

ap = parser(__doc__, need_workspace=False)
ap.add_argument("--dist", required=True, help="built Impeccable dist/ directory")
args = ap.parse_args()
DIST = args.dist
ALLOWLIST = set(json.load(open(os.path.join(args.fixtures, "motion-rules-only-candidate.json")))["candidate_ids"])
corpus = load_corpus(args.corpus)
EXPECTED_ORIGINS = {  # frozen: origin -> expected license (pinned re-verified)
    "nextlevelbuilder/ui-ux-pro-max-skill": "MIT", "Nutlope/hallmark": "MIT", "Leonxlnx/taste-skill": "MIT"}
NOTICE_MUST_NAME = ["Next Level Builder", "Hallmark contributors", "Leonxlnx"]

fail = []
# 1. allowlist size + every ID has provenance + origin license unchanged
if len(ALLOWLIST) != 16: fail.append(f"allowlist size {len(ALLOWLIST)} != 16")
for i in ALLOWLIST:
    prov = corpus.get(i, {}).get("provenance", {})
    if not prov.get("upstream_repo"): fail.append(f"{i}: no provenance")
    elif EXPECTED_ORIGINS.get(prov["upstream_repo"]) != "MIT": fail.append(f"{i}: origin {prov['upstream_repo']} not expected-MIT")

# 2. per-provider: any dist reference dir with a motion-dp shard must carry the attribution + only allowlisted IDs
provs = [d for d in os.listdir(DIST) if os.path.isdir(os.path.join(DIST, d))]
checked = 0
for p in provs:
    for root, _, files in os.walk(os.path.join(DIST, p)):
        shard_files = [f for f in files if re.match(r"motion-dp-(animate|audit|overdrive|polish)\.md$", f)]
        if not shard_files: continue
        checked += 1
        # orphan attribution check
        if "motion-dp-THIRD-PARTY.md" not in files:
            fail.append(f"{p}: shards present but attribution missing (ORPHAN) in {root}")
        # unapproved ID check
        for sf in shard_files:
            got = set(re.findall(r"MOTION-\d+", open(os.path.join(root, sf)).read()))
            bad = got - ALLOWLIST
            if bad: fail.append(f"{p}/{sf}: unapproved IDs {sorted(bad)}")
        # notice names all origins
        att = os.path.join(root, "motion-dp-THIRD-PARTY.md")
        if os.path.exists(att):
            txt = open(att).read()
            for nm in NOTICE_MUST_NAME:
                if nm not in txt: fail.append(f"{p}: attribution missing origin '{nm}'")
            if "Permission is hereby granted" not in txt: fail.append(f"{p}: attribution missing MIT permission text")

print(f"attribution gate: checked {checked} distribution reference dirs across {len(provs)} dist directories")
if fail:
    print("GATE FAIL:"); [print("  -", f) for f in fail[:20]]; sys.exit(1)
print("GATE PASS: allowlist=16, all provenance present, origins expected-MIT, no orphan attribution, no unapproved ID, notices complete")
