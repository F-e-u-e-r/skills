#!/usr/bin/env python3
"""Reproduces the study's FIRST projection design (test T06/T07 first run): sealed Design Pack MOTION
scope -> a structured-control reference and an information-ablated prose arm.

Preserved for reproducibility of the first run only. Two properties of this generator were later
corrected (see ../CORRECTIONS.md): the structured arm's `interpretation` clause over-states A11Y-2001's
activation (C3), and the prose arm strips ids/thresholds, so the first 3/3-vs-0/3 comparison was an
information ablation (C2). The matched-content arms in build_matched_arms.py supersede it.

Deterministic (no timestamps); same input -> byte-identical output. Reads the corpus only; writes to
<workspace>/artifacts/{motion-projection.json, motion-reference.structured.md, motion-reference.flattened.md}."""
import json, os
from _common import parser, load_corpus, sha, ensure_dir, CORPUS_SHA256

args = parser(__doc__, need_fixtures=False).parse_args()
ART = ensure_dir(os.path.join(args.workspace, "artifacts"))
CORPUS_SHA = CORPUS_SHA256
GEN = "motion-poc-projector/1"

SCOPE_RULES = ["MOTION-1009","MOTION-1019","MOTION-1020","MOTION-1023","MOTION-2002",  # DP-more-specific demo
               "A11Y-2001","MOTION-2003","MOTION-2005"]                                # dial targets
CONTROL = "DIAL-2002"

corpus = load_corpus(args.corpus)

def rule_entry(rid):
    r = corpus[rid]; es = r["effective_semantics"]
    prov = r.get("provenance", {})
    lines = [f"### {rid}  [{es.get('strength')}, {es.get('enforcement')}, verify={es.get('verification')}]"]
    lines.append(f"- semantics: {r.get('public_expression','').strip()}")
    if es.get("scope"): lines.append(f"- scope: {es['scope']}")
    if es.get("condition"): lines.append(f"- condition: {es['condition']}")
    if es.get("override"): lines.append(f"- override/exception: {es['override']}")
    lines.append(f"- provenance: {prov.get('upstream_repo')} @ {prov.get('pinned_commit','')[:12]} ({prov.get('design_phase')})")
    return "\n".join(lines)

# ---- machine-readable projection (source of truth for fidelity tests) ----
c = corpus[CONTROL]; ces = c["effective_semantics"]
proj = {
  "generator": GEN, "input_corpus_sha256": CORPUS_SHA, "dp_seal": "bd8cb1a",
  "domain": "MOTION",
  "control": {
    "control_id": CONTROL, "variable": "MOTION_INTENSITY",
    "range": ces.get("range"), "baseline": ces.get("baseline"),
    "gating": [{"when": b["condition"], "activates": b["rule_ids"]} for b in ces.get("gated_branches", [])],
    "targets": {t: {"strength": corpus[t]["effective_semantics"].get("strength"),
                    "enforcement": corpus[t]["effective_semantics"].get("enforcement"),
                    "override": corpus[t]["effective_semantics"].get("override"),
                    "semantics": corpus[t].get("public_expression","").strip()}
                for b in ces.get("gated_branches", []) for t in b["rule_ids"]},
  },
  "rules": {rid: {"strength": corpus[rid]["effective_semantics"].get("strength"),
                  "enforcement": corpus[rid]["effective_semantics"].get("enforcement"),
                  "semantics": corpus[rid].get("public_expression","").strip(),
                  "provenance": corpus[rid].get("provenance", {}).get("upstream_repo")}
            for rid in SCOPE_RULES},
}
json.dump(proj, open(os.path.join(ART, "motion-projection.json"), "w"), ensure_ascii=False, indent=2, sort_keys=True)

# ---- STRUCTURED reference (existing-reference-slot hypothesis) ----
gate_yaml = "\n".join(f'  - when: "{b["condition"]}"\n    activates: {b["rule_ids"]}' for b in ces.get("gated_branches", []))
tgt_lines = "\n".join(
  f"- **{t}** [{corpus[t]['effective_semantics'].get('strength')}, {corpus[t]['effective_semantics'].get('enforcement')}] — "
  f"{corpus[t].get('public_expression','').strip()[:200]}"
  + (f"  _(override: {corpus[t]['effective_semantics']['override'][:120]})_" if corpus[t]['effective_semantics'].get('override') else "")
  for b in ces.get("gated_branches", []) for t in b["rule_ids"])
structured = f"""# MOTION reference (Design Pack projection — {GEN})
<!-- deterministic projection of sealed Design Pack MOTION scope; do not hand-edit; regenerate from source -->
<!-- input_corpus_sha256: {CORPUS_SHA}  dp_seal: bd8cb1a -->

## Motion rules
{chr(10).join(rule_entry(r) for r in SCOPE_RULES if not r.startswith(('A11Y-2001','MOTION-2003','MOTION-2005')))}

## Runtime control: MOTION_INTENSITY  (first-class control — NOT advice)
<!-- design-pack-control: structured gating; a target rule is ACTIVE only when its predicate holds -->
```yaml control
control_id: {CONTROL}
variable: MOTION_INTENSITY
range: {ces.get('range')}
baseline: {ces.get('baseline')}
gating:
{gate_yaml}
interpretation: "A target rule is ACTIVE only when its predicate holds for the current MOTION_INTENSITY. A target rule is NOT active merely by appearing below. A11Y-2001 is absolute/non-overridable wherever motion is present and never weakens as intensity rises."
```
### Gated target rules (active per predicate above)
{tgt_lines}
"""
open(os.path.join(ART, "motion-reference.structured.md"), "w").write(structured)

# ---- FLATTENED negative control (gating stripped to generic prose) ----
flattened = f"""# MOTION reference (flattened arm — negative control)
<!-- SAME rules, control DELIBERATELY flattened to prose: thresholds/targets/dial removed -->

## Motion rules
{chr(10).join(rule_entry(r) for r in SCOPE_RULES if not r.startswith(('A11Y-2001','MOTION-2003','MOTION-2005')))}

## Motion intensity (guidance)
Aim for a lively, polished motion feel appropriate to the brief. Provide reduced-motion
handling, make sure the page actually moves where motion is promised, and add tasteful
micro-interactions where they fit. Use more motion when it suits the product and less when
restraint serves better.
"""
open(os.path.join(ART, "motion-reference.flattened.md"), "w").write(flattened)

for f in ("motion-projection.json", "motion-reference.structured.md", "motion-reference.flattened.md"):
    p = os.path.join(ART, f)
    print(f"  {f:38s} sha256={sha(p)[:16]}  bytes={os.path.getsize(p)}")
print("PROJECTION DONE  scope_ids=", SCOPE_RULES + [CONTROL])
