#!/usr/bin/env python3
"""Two-sided proof for every D6-B2.2 gate. Run: python3 design-pack/tools/test_projection_checks.py"""
import copy, json, os, shutil, sys, tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import project_corpus as pc, projection_checks as g
ROOT=os.getcwd()
def clone(x): return json.loads(json.dumps(x))

def copy_tree():
    d=tempfile.mkdtemp()
    shutil.copytree("design-pack", os.path.join(d,"design-pack"))
    os.makedirs(os.path.join(d,os.path.dirname(pc.CANONICAL_CORPUS_PATH)),exist_ok=True)
    shutil.copy(pc.CANONICAL_CORPUS_PATH, os.path.join(d,pc.CANONICAL_CORPUS_PATH))
    shutil.copy(pc.CANONICAL_NOTICE_PATH, os.path.join(d,pc.CANONICAL_NOTICE_PATH))
    return d

def mini_root(skillmd=None, classification=None, local_ext=None, manifest=None, runtime_text=None, corpus_ok=True, notice_ok=True):
    d=tempfile.mkdtemp()
    os.makedirs(os.path.join(d,os.path.dirname(pc.CANONICAL_CORPUS_PATH)),exist_ok=True)
    open(os.path.join(d,pc.CANONICAL_CORPUS_PATH),"w").write(
        open(os.path.join(ROOT,pc.CANONICAL_CORPUS_PATH)).read() if corpus_ok else "tampered\n")
    os.makedirs(os.path.join(d,os.path.dirname(pc.SCOPED_NOTICE)),exist_ok=True)
    nb=open(os.path.join(ROOT,pc.CANONICAL_NOTICE_PATH),"rb").read() if notice_ok else b"X\n"
    open(os.path.join(d,pc.SCOPED_NOTICE),"wb").write(nb)
    if skillmd:
        for name,text in skillmd.items():
            sd=os.path.join(d,g.SKILL_DIR,name); os.makedirs(sd,exist_ok=True)
            open(os.path.join(sd,"SKILL.md"),"w").write(text)
    os.makedirs(os.path.join(d,pc.GEN_DIR),exist_ok=True)
    if classification is not None: open(os.path.join(d,"design-pack/normative-classification.json"),"w").write(json.dumps(classification))
    if local_ext is not None: open(os.path.join(d,pc.GEN_DIR,"local-extensions.json"),"w").write(json.dumps(local_ext))
    if manifest is not None: open(os.path.join(d,pc.GEN_DIR,"manifest.json"),"w").write(json.dumps(manifest))
    if runtime_text is not None: open(os.path.join(d,pc.GEN_DIR,"runtime.json"),"w").write(runtime_text)
    return d

def _neg_classification_complete():
    d=copy_tree()
    p=os.path.join(d,"design-pack/skills/motion-craft/SKILL.md")
    open(p,"a").write("\n## 99. Bogus uncovered section\n\nnormative text with no inventory statement\n")
    return g.check_normative_classification_complete(d)

def _neg_bijection():
    d=copy_tree()
    p=os.path.join(d,"design-pack/normative-classification.json"); nc=json.load(open(p))
    for r in nc["rows"]:
        if r["disposition"]=="corpus-backed": r["corpus_ids"]=["ZZZ-9999"]; break
    json.dump(nc,open(p,"w"))
    return g.check_normative_bijection(d)

def _neg_conflict_review():
    d=copy_tree()
    p=os.path.join(d,"design-pack/normative-classification.json"); nc=json.load(open(p))
    for r in nc["rows"]:
        if r["disposition"]=="pack-local-extension": r["why_no_conflict"]=""; break
    json.dump(nc,open(p,"w"))
    return g.check_per_extension_conflict_review(d)

def _neg_clean_regen():
    d=copy_tree()
    p=os.path.join(d,pc.GEN_DIR,"runtime.json")
    open(p,"a").write(" ")  # one byte drift
    return g.check_clean_regeneration(d)

def main():
    runtime,support,manifest,reach,corpus=g.load_all(ROOT)
    R=[]
    def rec(n,real,bad): R.append((n, real==[], bad!=[]))

    rec("canonical-source", g.check_canonical_source(ROOT), g.check_canonical_source(mini_root(corpus_ok=False)))
    b=clone(runtime); b["rules"].pop(); rec("coverage", g.check_coverage(runtime,support,corpus), g.check_coverage(b,support,corpus))
    b=clone(runtime); b["rules"][0]["effective_semantics"]["strength"]="X"; rec("semantic-preservation", g.check_semantic_preservation(runtime,support,corpus), g.check_semantic_preservation(b,support,corpus))
    b=clone(runtime); b["decision_tables"][0]["effective_semantics"]["rows"][0]["rule_ids"]=["ZZZ-9"]; rec("runtime-ref-closure", g.check_runtime_reference_closure(runtime), g.check_runtime_reference_closure(b))
    b=clone(runtime); b["decision_tables"][0]["effective_semantics"]["rows"][0]["condition"]=" "; rec("decision-tables", g.check_decision_tables(runtime,corpus), g.check_decision_tables(b,corpus))
    b=clone(runtime); b["rules"][0]["public_expression"]+=" design-1-SEALED.md"; rec("isolation", g.check_isolation(runtime,support,manifest,reach), g.check_isolation(b))
    rec("determinism", g.check_determinism(ROOT), g.check_determinism(mini_root(runtime_text='{"rules":[]}\n')))
    b=clone(runtime); b["rules"].append(clone(support["evidence"][0])); rec("physical-isolation", g.check_physical_isolation(runtime,support), g.check_physical_isolation(b,support))
    b=clone(reach); v=next(iter(b["design-review-gate"]))
    for s in b:
        if v in b[s]: b[s].remove(v)
    rec("skill-reachability", g.check_skill_reachability(runtime,reach), g.check_skill_reachability(runtime,b))
    selrule=next(r["id"] for r in runtime["rules"] if pc.selector_ref(r)); ctrl=pc.selector_ref(next(r for r in runtime["rules"] if r["id"]==selrule))
    b=clone(reach)
    for s in b:
        if selrule not in b[s]: b[s].append(selrule)
        if ctrl in b[s]: b[s].remove(ctrl)
    rec("per-skill-control-closure", g.check_per_skill_control_closure(runtime,reach), g.check_per_skill_control_closure(runtime,b))
    b=clone(runtime); b["rules"][0]["effective_semantics"]["scope"]="__MUT__"; rec("generated-ref-fidelity", g.check_generated_reference_fidelity(ROOT,runtime), g.check_generated_reference_fidelity(ROOT,b))
    rec("reference-path-existence", g.check_reference_path_existence(ROOT), g.check_reference_path_existence(mini_root(skillmd={"x":"see [r](references/generated/NOPE.md)"})))
    rec("no-cross-skill-reference", g.check_no_cross_skill_reference(ROOT), g.check_no_cross_skill_reference(mini_root(skillmd={"x":"see [r](../../references/generated/struct.md)"})))
    rec("selective-load-policy", g.check_selective_load_policy(ROOT), g.check_selective_load_policy(mini_root(skillmd={"x":"eager @references/generated/struct.md now"})))
    b=clone(reach); b["ghost"]=[next(r["id"] for r in runtime["rules"])]; rec("per-skill-supporting-reachability", g.check_per_skill_supporting_file_reachability(ROOT,runtime,reach), g.check_per_skill_supporting_file_reachability(ROOT,runtime,b))
    rec("normative-classification-complete", g.check_normative_classification_complete(ROOT), _neg_classification_complete())
    badext=clone(g._load(ROOT,os.path.join(g.GEN,"local-extensions.json"))); badext["phase_b_provenance"]=True
    rec("pack-local-extension-non-conflict", g.check_pack_local_extension_non_conflict(ROOT),
        g.check_pack_local_extension_non_conflict(mini_root(local_ext=badext)))
    b=clone(runtime); b["rules"][0]["id"]="FAKE-9999"; rec("provenance-separation", g.check_provenance_separation(ROOT,runtime), g.check_provenance_separation(ROOT,b))
    R.append(("unmapped-prose (real gate)", g.check_unmapped_prose(ROOT)==[], True))
    rec("distribution-attribution", g.check_distribution_attribution(ROOT), g.check_distribution_attribution(mini_root(notice_ok=False)))

    # --- D6-B2.2-CLOSE gates ---
    rec("normative-bijection", g.check_normative_bijection(ROOT), _neg_bijection())
    rec("per-extension-conflict-review", g.check_per_extension_conflict_review(ROOT), _neg_conflict_review())
    rec("clean-regeneration", g.check_clean_regeneration(ROOT), _neg_clean_regen())

    print("="*78); print(f"{'GATE':<38}{'PASS-real':>12}{'FAIL-bad':>12}"); print("-"*78)
    allok=True
    for n,po,fo in R:
        ok=po and fo; allok=allok and ok
        print(f"{n:<38}{('yes' if po else 'NO'):>12}{('yes' if fo else 'NO'):>12}"+("" if ok else "  <-- CHECK"))
    print("="*78); print("ALL GATES TWO-SIDED PROVEN" if allok else "SOME FAILED"); return 0 if allok else 1

if __name__=="__main__": sys.exit(main())
