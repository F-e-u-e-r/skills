#!/usr/bin/env python3
"""Matched-content representation arms (test T07, final design): a FAITHFUL structured arm (A11Y-2001
dial-gated via its selector, no injected clause) and a MATCHED-CONTENT prose arm carrying identical
facts. The only variable between the arms is representation. Deterministic; verbatim canonical
semantics. Writes <workspace>/artifacts/matched/{structured3.md, flattened3.md}; both should be
byte-identical to ../fixtures/matched/."""
import os
from _common import parser, load_corpus, sha, ensure_dir

args = parser(__doc__, need_fixtures=False).parse_args()
OUT = ensure_dir(os.path.join(args.workspace, "artifacts", "matched"))
corpus = load_corpus(args.corpus)

RULES = ["MOTION-1009", "MOTION-1019", "MOTION-1020", "MOTION-1023", "MOTION-2002"]
TARGETS = ["A11Y-2001", "MOTION-2003", "MOTION-2005"]
d = corpus["DIAL-2002"]["effective_semantics"]
def es(i): return corpus[i]["effective_semantics"]
def pub(i): return corpus[i].get("public_expression", "").strip()

# Canonical activation note (both arms, identical) — states ONLY canonical facts:
# A11Y-2001.selector = DIAL-2002; activated at value>3; absolute (non-overridable) ONCE active.
ACT_NOTE = ("Activation is governed by the DIAL-2002 predicates: a target rule is active only when "
            "its predicate holds for the current MOTION_INTENSITY. A11Y-2001's selector is DIAL-2002, "
            "so it is activated at value > 3; its strength 'absolute'/'hard_block' means that once "
            "activated it cannot be weakened or overridden (it does not activate below its own threshold).")

# ---- STRUCTURED arm (faithful) ----
gate_yaml = "\n".join(f'  - when: "{b["condition"]}"\n    activates: {b["rule_ids"]}' for b in d["gated_branches"])
tgt_struct = "\n".join(
    f"- **{t}** [strength={es(t).get('strength')}, enforcement={es(t).get('enforcement')}"
    + (f", selector={es(t).get('selector')}" if es(t).get('selector') else "")
    + f"] — {pub(t)}"
    + (f"  override: {es(t)['override']}" if es(t).get('override') else "")
    + (f"  condition: {es(t)['condition']}" if es(t).get('condition') else "")
    for t in TARGETS)
rules_struct = "\n".join(f"- **{r}** [{es(r).get('strength')},{es(r).get('enforcement')}] — {pub(r)}" for r in RULES)
structured = f"""# MOTION reference — structured arm (matched-content ablation)
## Motion rules
{rules_struct}
## Runtime control: MOTION_INTENSITY
```yaml control
control_id: DIAL-2002
variable: MOTION_INTENSITY
range: {d.get('range')}
baseline: {d.get('baseline')}
gating:
{gate_yaml}
activation_note: "{ACT_NOTE}"
```
### Gated target rules
{tgt_struct}
"""
open(os.path.join(OUT, "structured3.md"), "w").write(structured)

# ---- FLATTENED arm (SAME facts, prose only; no YAML/table/control-block formatting) ----
def branch_prose():
    parts = []
    for b in d["gated_branches"]:
        parts.append(f"when MOTION_INTENSITY is {b['condition'].replace('value ', '')} it activates {', '.join(b['rule_ids'])}")
    return "; ".join(parts)
tgt_prose = " ".join(
    f"Rule {t} has strength {es(t).get('strength')} and enforcement {es(t).get('enforcement')}"
    + (f" with selector {es(t).get('selector')}" if es(t).get('selector') else "")
    + f": {pub(t)}"
    + (f" Its override is: {es(t)['override']}." if es(t).get('override') else "")
    + (f" It applies under the condition: {es(t)['condition']}." if es(t).get('condition') else "")
    for t in TARGETS)
rules_prose = " ".join(f"Rule {r} (strength {es(r).get('strength')}, enforcement {es(r).get('enforcement')}): {pub(r)}" for r in RULES)
flattened = f"""# MOTION reference — flattened arm (matched-content ablation)
Motion rules. {rules_prose}

Runtime control MOTION_INTENSITY. There is a control named DIAL-2002, variable MOTION_INTENSITY, range {d.get('range')}, baseline {d.get('baseline')}. Its gating: {branch_prose()}. {ACT_NOTE}

Gated target rules. {tgt_prose}
"""
open(os.path.join(OUT, "flattened3.md"), "w").write(flattened)

# ---- semantic-field parity check ----
S = open(os.path.join(OUT, "structured3.md")).read()
F = open(os.path.join(OUT, "flattened3.md")).read()
required = ["DIAL-2002", "MOTION_INTENSITY", "1-10", "baseline", "6",
            "> 3", "> 4", "> 5", "A11Y-2001", "MOTION-2003", "MOTION-2005",
            "absolute", "hard_block", "selector", "reduce", "premium",
            "MOTION-1009", "MOTION-1019", "MOTION-1020", "MOTION-1023", "MOTION-2002"]
print("=== semantic-field parity (must be present in BOTH arms) ===")
missing = []
for tok in required:
    inS, inF = tok in S, tok in F
    if not (inS and inF): missing.append((tok, inS, inF))
    print(f"  {tok:16s} structured={inS}  flattened={inF}")
print("PARITY:", "PASS (identical field coverage)" if not missing else f"FAIL {missing}")
for f in ("structured3.md", "flattened3.md"):
    p = os.path.join(OUT, f)
    print(f"  {f:16s} sha256={sha(p)[:16]}  bytes={os.path.getsize(p)}")
