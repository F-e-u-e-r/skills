#!/usr/bin/env python3
"""Control-fidelity gate (test T06): proves the projected DIAL-2002 retains full control semantics,
and is SHOWN ABLE TO FAIL via deliberately corrupted negative cases (known-bad-arm proof).

Input: <workspace>/artifacts/motion-projection.json produced by project_motion.py."""
import json, copy, os
from _common import parser

args = parser(__doc__, need_fixtures=False).parse_args()
ART = os.path.join(args.workspace, "artifacts")
proj = json.load(open(os.path.join(ART, "motion-projection.json")))

def validate(p):
    e = []
    c = p.get("control", {})
    if c.get("control_id") != "DIAL-2002": e.append("control_id")
    if c.get("variable") != "MOTION_INTENSITY": e.append("variable")
    if c.get("range") not in ("1-10", [1, 10]): e.append(f"range={c.get('range')}")
    if c.get("baseline") != 6: e.append("baseline")
    gates = {g["when"]: tuple(g["activates"]) for g in c.get("gating", [])}
    expect = {"value > 3": ("A11Y-2001",), "value > 4": ("MOTION-2003",), "value > 5": ("MOTION-2005",)}
    if gates != expect: e.append(f"gating={gates}")
    tgts = set(c.get("targets", {}).keys())
    if tgts != {"A11Y-2001", "MOTION-2003", "MOTION-2005"}: e.append(f"targets={tgts}")
    a = c.get("targets", {}).get("A11Y-2001", {})
    if a.get("strength") != "absolute" or a.get("enforcement") != "hard_block":
        e.append("A11Y-2001 not absolute/hard_block")
    return (len(e) == 0, e)

ok, e = validate(proj)
print("REAL projection:", "PASS" if ok else "FAIL " + str(e))
assert ok, f"real projection must pass: {e}"

neg = {}
n1 = copy.deepcopy(proj)
n1["control"]["targets"].pop("A11Y-2001", None)
n1["control"]["gating"] = [g for g in n1["control"]["gating"] if "A11Y-2001" not in g["activates"]]
neg["missing_A11Y-2001"] = n1
n2 = copy.deepcopy(proj)
for g in n2["control"]["gating"]:
    if g["activates"] == ["MOTION-2003"]: g["when"] = "value > 9"
neg["altered_threshold"] = n2
n3 = copy.deepcopy(proj)
n3["control"] = {"control_id": None}  # flattened / unstructured
neg["flattened_unstructured"] = n3

all_fail = True
for name, p in neg.items():
    ok, e = validate(p)
    print(f"NEG[{name}]:", "correctly FAILED" if not ok else "!!! WRONGLY PASSED")
    if ok: all_fail = False
print("FIDELITY GATE:", "PASS (real passes, all 3 negatives fail)" if all_fail else "BROKEN")
