#!/usr/bin/env python3
"""Rules-only candidate (test T09): control-independence proof for the 16 candidate rules and the
deterministic rules-only reference (no DIAL-2002, no thresholds, no intensity policy, no
qualitative->numeric mapping). Also emits the normalized variant using the frozen adapter transform
motion-dp-normalize/1 (U+2014 -> ', ').

Inputs: the corpus and ../fixtures/motion-rules-only-candidate.json (candidate_ids).
Writes <workspace>/artifacts/{control-independence-proof.json, motion-reference.rules-only.md,
motion-reference.rules-only.normalized.md} (expected byte-identical to the fixtures)."""
import json, os, re
from _common import parser, load_corpus, sha, ensure_dir

args = parser(__doc__).parse_args()
ART = ensure_dir(os.path.join(args.workspace, "artifacts"))
corpus = load_corpus(args.corpus)
cand = json.load(open(os.path.join(args.fixtures, "motion-rules-only-candidate.json")))
IDS = cand["candidate_ids"]
EM = "—"
def normalize(s): return s.replace(" " + EM + " ", ", ").replace(EM + " ", ", ").replace(" " + EM, ",").replace(EM, ", ")

# --- control-independence proof (per candidate) ---
DIAL_TOKENS = re.compile(r"MOTION_INTENSITY|DIAL-|value\s*>|value\s*>=|threshold|dial\b", re.I)
proof = []
ok = True
for rid in IDS:
    es = corpus[rid]["effective_semantics"]
    blob = " ".join(str(es.get(k, "")) for k in ("scope", "condition", "override")) + " " + (corpus[rid].get("public_expression") or "")
    has_selector = bool(es.get("selector"))
    refs_dial = bool(DIAL_TOKENS.search(blob))
    indep = (not has_selector) and (not refs_dial)
    if not indep: ok = False
    proof.append({"id": rid, "has_selector": has_selector, "text_refs_dial_or_threshold": refs_dial,
                  "control_independent": indep})
print("=== control-independence ===")
for p in proof: print(f"  {p['id']:12s} selector={p['has_selector']} refs_dial={p['text_refs_dial_or_threshold']} -> independent={p['control_independent']}")
print(f"ALL {len(IDS)} CONTROL-INDEPENDENT:", ok)
json.dump({"schema": "control-independence-proof/1", "all_independent": ok, "proof": proof},
          open(os.path.join(ART, "control-independence-proof.json"), "w"), indent=2)

# --- deterministic rules-only reference ---
def entry(rid):
    r = corpus[rid]; es = r["effective_semantics"]; prov = r.get("provenance", {})
    L = [f"### {rid}  [{es.get('strength')}, {es.get('enforcement')}, verify={es.get('verification')}]"]
    L.append(f"- {r.get('public_expression','').strip()}")
    if es.get("scope"): L.append(f"- scope: {es['scope']}")
    if es.get("condition"): L.append(f"- condition: {es['condition']}")
    if es.get("override"): L.append(f"- override/exception: {es['override']}")
    L.append(f"- provenance: {prov.get('upstream_repo')} @ {str(prov.get('pinned_commit',''))[:12]} ({prov.get('design_phase')})")
    return "\n".join(L)
body = "\n".join(entry(r) for r in IDS)
art = f"""# MOTION reference — Design Pack rules-only projection (no control layer)
<!-- deterministic projection of {len(IDS)} sealed Design Pack MOTION rules; no DIAL-2002, no thresholds, no motion-intensity policy -->
<!-- input_corpus_sha256: 16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b  dp_seal: bd8cb1a -->
<!-- these are unconditional motion rules; they do NOT import A11Y-2001 or any dial-gated rule -->

## Design Pack motion rules ({len(IDS)})
{body}
"""
p = os.path.join(ART, "motion-reference.rules-only.md")
open(p, "w").write(art)
pn = os.path.join(ART, "motion-reference.rules-only.normalized.md")
open(pn, "w").write(normalize(art))
print("\n=== rules-only reference ===")
print(f"  motion-reference.rules-only.md             sha256={sha(p)[:16]}  bytes={os.path.getsize(p)}  rules={len(IDS)}")
print(f"  motion-reference.rules-only.normalized.md  sha256={sha(pn)[:16]}  bytes={os.path.getsize(pn)}  em_dashes={open(pn).read().count(EM)}")
