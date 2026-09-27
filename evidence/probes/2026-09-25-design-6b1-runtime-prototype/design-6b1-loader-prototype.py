#!/usr/bin/env python3
# ===================== PUBLIC PROJECTION (design/d6b1-public) =====================
# Sanitized projection of the DESIGN-6B1 prototype. The companion manifest here is
# STRUCTURAL: per-rule upstream-sourced `scope` prose and the `trigger` field are
# projected out (full `scope` kept only for the pack's own fence-clean D5-synthesized
# rules). The MANDATORY invariants proven below (population 448/448, hard_block 7,
# must_surface 125, gate population 132, keyword-tier gate leakage 0, gate miss 0,
# 16/16 regressions) are all scope-INDEPENDENT. Only the non-mandatory non-gate
# recall / generation-payload figures differ from the internal artifact.
# ================================================================================
# =============================================================================
# DESIGN-6B1 — Retrieval & Enforcement Prototype (loader + full-load oracle)
# DERIVED PROTOTYPE. Not production integration, not a canonical runtime artifact.
#   * mints no ID, mutates no registry, changes no sealed byte, promotes no check,
#     synthesizes no doctrine, seals nothing.
#   * Reads its rule data from the DERIVED companion `design-6b1-manifest.json`
#     (per-rule 4-level enforcement action + retrieval tier + positive triggers +
#     sealed-measured bytes). That manifest is derived from the sealed set + the
#     DESIGN-6A docs only; see its _meta for the derivation rules.
#
# WHAT THIS PROVES (the CORE acceptance test, Constraint D):
#   For each fixture it runs BOTH:
#     (1) ORACLE  = every rule whose sealed §8.3 applicability holds for the task
#                   (non-selector rules are maximally applicable — prose scope
#                    never DENIES, Constraint B; selector-gated rules are applicable
#                    iff their sealed §8.3 step-0 selector fires).
#     (2) LOADER  = kernel  +  sealed-selector-admitted  +  positively-retrieved.
#   and reports the applicable-vs-loaded hard_block / must_surface sets.
#   ANY loader miss of an oracle-applicable hard_block or must_surface is a FAIL.
#
# WHY ZERO-MISS IS STRUCTURAL (not fixture luck):
#   every non-selector hard_block/must_surface is UNCONDITIONALLY kernel-resident,
#   and every selector-gated hard_block/must_surface loads exactly when its sealed
#   dial/decision selector fires (= exactly when it is applicable, §8.3 step-0).
#   NO gate lives in the keyword-retrievable tier, so no prose rewording can drop
#   one — see the adversarial fixture F6-ADV.
#
# Run:  python3 design-6b1-loader-prototype.py
#       python3 design-6b1-loader-prototype.py --json   # machine-readable dump
# =============================================================================
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
MAN  = json.load(open(os.path.join(HERE, "design-6b1-manifest.json")))
R    = MAN["rules"]
CATKW    = MAN["_meta"]["category_keywords"]
VERB_SEL = {"DECISION-4001", "DECISION-4002"}          # verb/workflow selectors
STOP = set("the a an of in to for and or with any this that on at by from as is are be page "
           "element content when whenever not no never only its their all each other same every".split())

def bytes_of(ids): return sum(R[i]["bytes"] for i in ids)
def tok(b):        return b // 4
def pay(ids):
    ids = list(ids); b = bytes_of(ids); return {"rules": len(ids), "bytes": b, "tokens": tok(b)}

# ---- SEALED SELECTOR EVALUATION (§8.3 step-0; POSITIVE admission only) --------
# Config-driven (dial value / icon-role presence / verb flow), never prose-keyword.
def selector_fires(rid, fx):
    s = R[rid]["selector"]
    if s == "DIAL-2001":                                   # DESIGN_VARIANCE
        if rid == "STRUCT-2002": return fx["DV"] > 4
        if rid == "STRUCT-2003": return fx["DV"] >= 4
    elif s == "DIAL-2002":                                 # MOTION_INTENSITY
        if rid == "A11Y-2001":   return fx["MI"] > 3
        if rid == "MOTION-2003": return fx["MI"] > 4
        if rid == "MOTION-2005": return fx["MI"] > 5
    elif s == "DIAL-2003":                                 # VISUAL_DENSITY
        if rid == "STRUCT-2017": return fx["VD"] > 7
    elif s == "DECISION-1001":                             # icon-role present
        return fx["icons"]
    elif s == "DECISION-4001":                             # theme-route build step
        return "theme-route" in fx["verbs"]
    elif s == "DECISION-4002":                             # study emission
        return "study-emission" in fx["verbs"]
    return False

# ---- POSITIVE CATEGORY RETRIEVAL (Constraint B: additive; a miss denies nothing)
def _scope_tokens(rid):
    sc = (R[rid].get("scope") or "").lower()   # PUBLIC: tolerate projected-out scope
    return {w for w in re.findall(r"[a-z][a-z\-]{3,}", sc) if w not in STOP}

def category_retrieve(fx):
    txt = fx["brief"].lower(); hit = set()
    for rid, r in R.items():
        if r["tier"] != "retrievable-category":
            continue
        kws = CATKW.get(r["category"], [])
        if any(k in txt for k in kws) or any(t in txt for t in _scope_tokens(rid)):
            hit.add(rid)                                   # POSITIVE match only
    return hit

# ---- FULL-LOAD ORACLE (sealed §8.3 applicability) -----------------------------
def oracle(fx):
    out = set()
    for rid, r in R.items():
        if r["selector"]:
            if selector_fires(rid, fx):                    # step-0 gate == applicability
                out.add(rid)
        else:
            out.add(rid)                                   # non-selector: applicable (scope never DENIES)
    return out

# ---- PROTOTYPE LOADER (kernel + positively-retrieved) -------------------------
KERNEL = {i for i, r in R.items() if r["tier"] == "kernel"}
CRITIQUE = {i for i, r in R.items() if r["tier"] == "critique"}

def loader_generation(fx):
    out = set(KERNEL)                                      # always-resident floor
    for rid, r in R.items():
        if r["tier"] in ("retrievable-selector", "behavior") and selector_fires(rid, fx):
            out.add(rid)                                   # sealed-selector admission
    out |= category_retrieve(fx)                           # positive category retrieval
    return out

def loader_render(fx):                                     # render pass adds deferred L3
    return loader_generation(fx) | CRITIQUE

# ---- ENFORCEMENT-SET HELPERS --------------------------------------------------
def gates(ids):   return {i for i in ids if R[i]["enf_action"] in ("hard_block", "must_surface")}
def actives(ids): return {i for i in ids if R[i]["n_active"] > 0}
def in_tier(ids, t): return {i for i in ids if R[i]["tier"] == t}

# ---- FIXTURES (F1-F5 = DESIGN-6A set; F6-ADV = adversarial semantic-mismatch) --
FIX = [
 {"id": "F1", "name": "generic marketing landing page", "DV": 8, "MI": 6, "VD": 4, "icons": True, "verbs": [],
  "brief": "Marketing landing page: hero section with headline copy and a primary CTA button, feature cards "
           "with icons, testimonial section, animated scroll reveals, responsive nav and footer. Bold color "
           "palette and clear typography."},
 {"id": "F2", "name": "minimal / restrained brand site", "DV": 3, "MI": 2, "VD": 4, "icons": True, "verbs": [],
  "brief": "Minimal restrained brand site: quiet layout, generous whitespace, restrained neutral color, refined "
           "typography, a small set of icon links in the header, static presentation with almost no motion."},
 {"id": "F3", "name": "high-density data dashboard", "DV": 8, "MI": 6, "VD": 9, "icons": True, "verbs": [],
  "brief": "High-density analytics dashboard: many metric tiles and data tables, dense grid layout, interactive "
           "chart elements and filter controls, icon buttons, color-coded status, animated transitions between views."},
 {"id": "F4", "name": "hallmark study / build-from-DNA", "DV": 8, "MI": 6, "VD": 4, "icons": True,
  "verbs": ["theme-route", "study-emission"],
  "brief": "Build a page from a studied design DNA: run the hallmark study theme-route to lock the palette and "
           "type roles from the diagnosis, then emit a study design.md. Hero, feature grid with icons, CTA, "
           "animated reveals, color theme, typography."},
 {"id": "F5", "name": "icon-free long-form article", "DV": 6, "MI": 5, "VD": 4, "icons": False, "verbs": [],
  "brief": "Icon-free long-form editorial article: long body text, headings and pull quotes, comfortable reading "
           "measure and line length, typographic hierarchy, restrained color, subtle section spacing. No icons, "
           "minimal interaction."},
 # -- ADVERSARIAL (Constraint E): fetch-and-rebuild whose wording deliberately AVOIDS the sealed rules' terms
 #    ("fetch/url/untrusted/prompt-injection", "interactive", "motion/animation", "icon", "accessibility") while
 #    remaining semantically applicable to UX-4031, INTERACT-6001, A11Y-2001, the DECISION-1001 icon rules, etc.
 {"id": "F6-ADV", "name": "adversarial semantic-mismatch (fetch-rebuild)", "DV": 8, "MI": 6, "VD": 4,
  "icons": True, "verbs": [],
  "brief": "Point the builder at a competitor's web address, pull down whatever markup and styling live there, "
           "and reproduce the same overall vibe. Give it lively movement on entry, things people can poke at with "
           "a thumb, and little picture-glyphs next to the menu words. Make it feel premium."},
]

def run_fixture(fx):
    orc = oracle(fx); lg = loader_generation(fx); lr = loader_render(fx)
    o_gate = gates(orc); l_gate = gates(lr); miss = sorted(o_gate - l_gate)
    o_act = actives(orc); l_act = actives(lr)
    o_rc = in_tier(orc, "retrievable-category"); l_rc = in_tier(lg, "retrievable-category")
    return {
        "id": fx["id"], "name": fx["name"],
        "config": {"DV": fx["DV"], "MI": fx["MI"], "VD": fx["VD"], "icons": fx["icons"], "verbs": fx["verbs"]},
        "kernel_payload": pay(KERNEL),
        "generation_payload": pay(lg),
        "render_payload": pay(lr),
        "critique_addon": pay(CRITIQUE & lr),
        "oracle_gates": len(o_gate), "loader_covers_gates": len(o_gate & l_gate),
        "gate_miss_count": len(miss), "gate_miss": miss,
        "active_check_recall": [len(o_act & l_act), len(o_act)],
        "nongate_guidance_recall": [len(o_rc & l_rc), len(o_rc)],
    }

# ---- MANDATORY REGRESSIONS (Constraint F) -------------------------------------
def _act(rid): return [c for c in _checks(rid) if c["status"] == "active"]
def _checks(rid):  # reconstruct check list from counts is lossy; use manifest fields directly
    return [{"status": "active"}] * R[rid]["n_active"] + [{"status": "candidate"}] * R[rid]["n_candidate"]

def regressions():
    F = {fx["id"]: fx for fx in FIX}
    out = []
    def chk(name, expected, actual):
        out.append({"name": name, "pass": expected == actual, "expected": expected, "actual": actual})
    # TC-1 INTERACT-6001 {must_surface, L2, kernel}
    r = R["INTERACT-6001"]
    chk("TC1 INTERACT-6001 enf=must_surface & tier=kernel", ("must_surface", "kernel"), (r["enf_action"], r["tier"]))
    chk("TC1.P1/P2 scope names form-inputs AND interactive chart elements", (True, True),
        ("form input" in r["scope"].lower(), "chart" in r["scope"].lower()))
    chk("TC1.P3/N1 exactly ONE active L2 check, ZERO candidate (no promotion)", (1, "L2", 0),
        (r["n_active"], r["verification"], r["n_candidate"]))
    chk("TC1.N3 A11Y-1022 kept SEPARATE (own rule, not folded)", True, "A11Y-1022" in R)
    # TC-2 UX-4031 {contextual, none, kernel(safety)}
    r = R["UX-4031"]
    chk("TC2 UX-4031 enf=contextual & checks:[] (N1 no synthesized proxy)", ("contextual", 0), (r["enf_action"], r["n_checks"]))
    chk("TC2 tier=kernel (safety boundary resists adversarial keyword-avoidance)", "kernel", r["tier"])
    chk("TC2 UX-4031 present in ADVERSARIAL F6 generation set", True, "UX-4031" in loader_generation(F["F6-ADV"]))
    chk("TC2.N2 UX-4030 (SSRF) NOT revived", False, "UX-4030" in R)
    # TC-3 MOTION-1001 {contextual, none} + Emil boundary
    r = R["MOTION-1001"]
    chk("TC3 MOTION-1001 heuristic, checks:[], enf=contextual (no duration-band gate)", ("heuristic", 0, "contextual"),
        (r["final_strength"], r["n_checks"], r["enf_action"]))
    chk("TC3 tier=retrievable-category (heuristic guidance; a miss drops NO gate)", "retrievable-category", r["tier"])
    chk("TC3.N1/N2 no Emil rule & no synthesized duration rule minted", (False, False),
        (any(k.startswith("EMIL") for k in R), "MOTION-6001" in R))
    # A11Y-2001 selector case (applicable at MI>3, not <=3)
    hi = {"DV": 0, "MI": 6, "VD": 0, "icons": False, "verbs": []}
    lo = {"DV": 0, "MI": 2, "VD": 0, "icons": False, "verbs": []}
    chk("A2001 selector_fires MI=6 True / MI=2 False", (True, False),
        (selector_fires("A11Y-2001", hi), selector_fires("A11Y-2001", lo)))
    chk("A2001 in oracle(F1 MI6)=applicable / NOT in oracle(F2 MI2)=correctly-absent", (True, False),
        ("A11Y-2001" in oracle(F["F1"]), "A11Y-2001" in oracle(F["F2"])))
    chk("A2001 hard_block & loader COVERS it when applicable (F1)", ("hard_block", True),
        (R["A11Y-2001"]["enf_action"], "A11Y-2001" in loader_render(F["F1"])))
    # COLOR-4003 case (active exceptionless L1 check but WARN, not hard_block, because avoid)
    r = R["COLOR-4003"]
    chk("C4003 avoid + HAS active check + enf=warn (NOT hard_block/must_surface)", ("avoid", True, "warn"),
        (r["final_strength"], r["n_active"] >= 1, r["enf_action"]))
    chk("C4003 tier=kernel (warn kept resident; strength/check separation survives)", "kernel", r["tier"])
    return out

def main():
    results = [run_fixture(fx) for fx in FIX]
    regs = regressions()
    if "--json" in sys.argv:
        print(json.dumps({"kernel": pay(KERNEL), "full_load_448": pay(list(R)),
                          "fixtures": results, "regressions": regs}, indent=1)); return
    print("=" * 78)
    print("DESIGN-6B1 loader/oracle dual-run   (population = %d rules)" % len(R))
    print("=" * 78)
    k = pay(KERNEL); fl = pay(list(R))
    print("KERNEL (always-resident floor): %d rules  %d B  ~%d tok" % (k["rules"], k["bytes"], k["tokens"]))
    print("FULL-LOAD 448 (oracle ceiling): %d rules  %d B  ~%d tok" % (fl["rules"], fl["bytes"], fl["tokens"]))
    print("DESIGN-6A baseline (347, always-on): 321417 B  ~80354 tok   <- the floor this phase cuts")
    print("-" * 78)
    total_miss = 0
    for r in results:
        g = r["generation_payload"]; rp = r["render_payload"]
        print("[%s] %s   DV%d MI%d VD%d icons=%s verbs=%s" % (
            r["id"], r["name"], r["config"]["DV"], r["config"]["MI"], r["config"]["VD"],
            r["config"]["icons"], r["config"]["verbs"]))
        print("     kernel %d tok | GEN %d rules ~%d tok | RENDER %d rules ~%d tok (+critique %d tok)" % (
            k["tokens"], g["rules"], g["tokens"], rp["rules"], rp["tokens"], r["critique_addon"]["tokens"]))
        print("     oracle-applicable hard_block/must_surface=%d ; loader covers=%d ; MISS=%d %s" % (
            r["oracle_gates"], r["loader_covers_gates"], r["gate_miss_count"], r["gate_miss"] or ""))
        print("     applicable active-check recall %d/%d | non-gate guidance recall %d/%d" % (
            r["active_check_recall"][0], r["active_check_recall"][1],
            r["nongate_guidance_recall"][0], r["nongate_guidance_recall"][1]))
        total_miss += r["gate_miss_count"]
    print("-" * 78)
    print("TOTAL hard_block/must_surface MISS across all fixtures: %d   (MANDATORY: 0)" % total_miss)
    print("=" * 78)
    npass = sum(1 for x in regs if x["pass"])
    print("REGRESSIONS: %d/%d PASS" % (npass, len(regs)))
    for x in regs:
        print("  [%s] %s" % ("PASS" if x["pass"] else "FAIL", x["name"]))
        if not x["pass"]:
            print("        expected=%r actual=%r" % (x["expected"], x["actual"]))
    ok = (total_miss == 0 and npass == len(regs))
    print("=" * 78)
    print("EXIT GATE: %s" % ("PASS — 0 gate miss, all regressions green" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
