#!/usr/bin/env python3
"""D6-B2.1 contract gates for the split production bridge. Pure predicates
([] == pass). test_projection_checks.py drives each PASS-on-real + FAIL-on-bad."""
import json
import os
import re
import subprocess

import project_corpus as pc

GEN = pc.GEN_DIR
REF = pc.REF_DIR
SKILL_DIR = "design-pack/skills"
SELECTOR_LEAD = pc.SELECTOR_LEAD
BANNED = re.compile(
    r"SEALED|scratchpad|worktree|/private/|claude-501|e13fc78a|cac5bae5|session_[0-9A-Za-z]|"
    r"design/d6a|design/d6b1|d0-d4-mining|d5-reconciliation|seal-d0-d3|"
    r"authority_ledger|coverage_ledger|audit_ledger|review_ledger|audit_final|audit_rows|"
    r"repair\d?\.py|reexpress\.py|build_public\.py|audit_complete\.py|dispositions\.json|flagged\.json|\.md-E",
    re.I)


def _load(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as f:
        return json.load(f)

def load_all(root):
    runtime = _load(root, os.path.join(GEN, "runtime.json"))
    support = _load(root, os.path.join(GEN, "projection-support.json"))
    manifest = _load(root, os.path.join(GEN, "manifest.json"))
    reach = _load(root, os.path.join(GEN, "skill-reachability.json"))
    corpus = _load(root, pc.CANONICAL_CORPUS_PATH)
    return runtime, support, manifest, reach, corpus

def runtime_records(runtime):
    for k in ("rules", "synthesized_rules", "decision_tables", "dials"):
        for r in runtime[k]:
            yield r

def rule_ids(runtime):
    return {r["id"] for r in runtime["rules"]} | {r["id"] for r in runtime["synthesized_rules"]}
def control_ids(runtime):
    return {r["id"] for r in runtime["decision_tables"]} | {r["id"] for r in runtime["dials"]}


# ---- accepted D6-B2 gates (adapted to split layout) ------------------------
def check_canonical_source(root):
    p = os.path.join(root, pc.CANONICAL_CORPUS_PATH)
    got = pc.sha256_file(p)
    return [] if got == pc.CANONICAL_CORPUS_SHA256 else [f"canonical-source: {got} != {pc.CANONICAL_CORPUS_SHA256}"]

def check_coverage(runtime, support, corpus):
    f = []
    placed = [r["id"] for r in runtime_records(runtime)] + [r["id"] for k in support for r in support[k]]
    corpus_ids = [r["id"] for r in corpus]
    if sorted(placed) != sorted(corpus_ids):
        f.append(f"coverage: placed {len(placed)} != corpus {len(corpus_ids)}")
    if len(placed) != len(set(placed)):
        f.append("coverage: a record placed more than once")
    return f

def check_semantic_preservation(runtime, support, corpus):
    f = []
    bycorpus = {r["id"]: r for r in corpus}
    for r in list(runtime_records(runtime)) + [x for k in support for x in support[k]]:
        src = bycorpus[r["id"]]
        for fld in ("effective_semantics", "public_expression", "notes"):
            if r.get(fld) != src.get(fld):
                f.append(f"semantic: {r['id']} {fld} mutated")
    return f

def check_runtime_reference_closure(runtime):
    f = []; rids = rule_ids(runtime); cids = control_ids(runtime)
    for dt in runtime["decision_tables"]:
        for row in dt["effective_semantics"]["rows"]:
            for t in row.get("rule_ids", []):
                if t not in rids: f.append(f"closure: {dt['id']} -> {t} not runtime rule")
    for dl in runtime["dials"]:
        for br in dl["effective_semantics"].get("gated_branches", []):
            for t in br.get("rule_ids", []):
                if t not in rids: f.append(f"closure: {dl['id']} -> {t} not runtime rule")
    for r in runtime["rules"] + runtime["synthesized_rules"]:
        ref = pc.selector_ref(r)
        if ref and ref not in cids: f.append(f"closure: {r['id']} selector -> {ref} not runtime control")
    return f

def check_decision_tables(runtime, corpus):
    f = []; bycorpus = {r["id"]: r for r in corpus}
    for dt in runtime["decision_tables"]:
        es = dt["effective_semantics"]; src = bycorpus[dt["id"]]["effective_semantics"]
        if es.get("selection_mode") not in {"all_matches","first_match","exactly_one"}:
            f.append(f"decision: {dt['id']} bad selection_mode")
        rows = es.get("rows") or []
        if not rows: f.append(f"decision: {dt['id']} no rows")
        for row in rows:
            if not (row.get("condition") or "").strip(): f.append(f"decision: {dt['id']} empty predicate")
        if [r.get("id") for r in rows] != [r.get("id") for r in src.get("rows", [])]:
            f.append(f"decision: {dt['id']} row order differs from canonical")
        if es.get("selection_mode") != src.get("selection_mode"):
            f.append(f"decision: {dt['id']} mode differs")
    return f

def check_isolation(*artifacts):
    f = []
    for a in artifacts:
        blob = json.dumps(a, ensure_ascii=False)
        hits = sorted(set(m.group(0) for m in BANNED.finditer(blob)))
        if hits: f.append(f"isolation: banned tokens {hits[:6]}")
    return f

def check_determinism(root):
    a = pc.dumps(pc.classify(_load(root, pc.CANONICAL_CORPUS_PATH))[0])
    b = pc.dumps(pc.classify(_load(root, pc.CANONICAL_CORPUS_PATH))[0])
    on_disk = open(os.path.join(root, GEN, "runtime.json"), encoding="utf-8").read()
    out = []
    if a != b: out.append("determinism: two builds differ")
    if a != on_disk: out.append("determinism: emitted runtime.json != rebuild")
    return out


# ---- new D6-B2.1 gates -----------------------------------------------------
def check_physical_isolation(runtime, support):
    """runtime.json: only the 4 runtime kinds, zero evidence/conflict; support: exactly 88 evidence/conflict."""
    f = []
    for r in runtime_records(runtime):
        if r["kind"] in ("evidence", "conflict"):
            f.append(f"physical-isolation: {r['id']} ({r['kind']}) is in runtime.json")
    n_rt = sum(len(runtime[k]) for k in runtime)
    if n_rt != 454: f.append(f"physical-isolation: runtime has {n_rt}, want 454")
    n_sp = sum(len(support[k]) for k in support)
    if n_sp != 88: f.append(f"physical-isolation: support has {n_sp}, want 88")
    for r in [x for k in support for x in support[k]]:
        if r["kind"] not in ("evidence", "conflict"):
            f.append(f"physical-isolation: {r['id']} ({r['kind']}) is in support")
    return f

def check_skill_reachability(runtime, reach):
    """union of all skill reaches == all 454 runtime records."""
    f = []
    all_rt = {r["id"] for r in runtime_records(runtime)}
    union = set().union(*[set(v) for v in reach.values()]) if reach else set()
    missing = sorted(all_rt - union)
    extra = sorted(union - all_rt)
    if missing: f.append(f"reachability: {len(missing)} runtime records reachable by no skill e.g. {missing[:3]}")
    if extra: f.append(f"reachability: reach names {len(extra)} non-runtime ids e.g. {extra[:3]}")
    return f

def check_per_skill_control_closure(runtime, reach):
    """within each skill's reachable set, every selector-bound rule's control is reachable."""
    f = []; byid = {r["id"]: r for r in runtime_records(runtime)}
    for skill, ids in reach.items():
        s = set(ids)
        for rid in ids:
            r = byid.get(rid)
            if not r: continue
            ref = pc.selector_ref(r)
            if ref and ref not in s:
                f.append(f"control-closure: {skill}: {rid} selector -> {ref} not in skill reach")
    return f

def check_generated_reference_fidelity(root, runtime):
    """Every on-disk skill-local shard is byte-identical to its deterministic re-render.
    Domain shards + controls.md come from render_shards; per-skill control-dependencies.md
    from render_control_dependencies over that skill's cross-domain records."""
    f = []
    expected = pc.render_shards(runtime)
    all_rt = list(pc._all_runtime(runtime)); rt_byid = {r["id"]: r for r in all_rt}
    try:
        reach = _load(root, os.path.join(GEN, "skill-reachability.json"))
    except Exception as e:
        return [f"fidelity: skill-reachability unreadable ({e})"]
    cross = pc.skill_cross_domain(reach, all_rt)
    base = os.path.join(root, SKILL_DIR)
    for skill in sorted(os.listdir(base)):
        gd = os.path.join(base, skill, "references", "generated")
        if not os.path.isdir(gd):
            continue
        for fn in sorted(os.listdir(gd)):
            if not fn.endswith(".md"):
                continue
            if fn == "control-dependencies.md":
                want = pc.render_control_dependencies([rt_byid[i] for i in cross.get(skill, [])])
            elif fn in expected:
                want = expected[fn]
            else:
                f.append(f"fidelity: {skill}/{fn} is not a known generated shard"); continue
            if open(os.path.join(gd, fn), encoding="utf-8").read() != want:
                f.append(f"fidelity: {skill}/{fn} differs from deterministic re-render")
    for r in runtime["rules"] + runtime["synthesized_rules"]:
        dom = pc.domain_of(r["id"]).lower(); shard = expected.get(f"{dom}.md", "")
        for k, v in (r.get("effective_semantics") or {}).items():
            if isinstance(v, str) and v and v not in shard:
                f.append(f"fidelity: {r['id']} field {k} not verbatim in {dom}.md")
    return f


def check_full_control_target_closure(runtime, reach):
    """BIDIRECTIONAL closure: for every skill, every control it reaches has ALL its target rules
    (rows[].rule_ids, gated_branches[].rule_ids) reachable in the same skill set."""
    f = []
    byid = {r["id"]: r for r in runtime_records(runtime)}
    def targets(c):
        es = c.get("effective_semantics") or {}; out = set()
        for row in es.get("rows") or []: out |= set(row.get("rule_ids") or [])
        for br in es.get("gated_branches") or []: out |= set(br.get("rule_ids") or [])
        return out
    for skill, ids in reach.items():
        s = set(ids)
        for cid in ids:
            r = byid.get(cid)
            if r and r["kind"] in ("decision_table", "dial"):
                for t in targets(r):
                    if t not in s:
                        f.append(f"control-target-closure: {skill}: control {cid} target {t} not reachable")
    return f


def check_skill_local_dependency_resolution(root, runtime, reach):
    """Every runtime record a skill reaches must be resolvable from that skill's OWN local shard files
    (## <id> present), so correctness never depends on searching another skill's references."""
    f = []
    base = os.path.join(root, SKILL_DIR)
    import re as _re
    for skill, ids in reach.items():
        gd = os.path.join(base, skill, "references", "generated")
        blob = ""
        if os.path.isdir(gd):
            for fn in sorted(os.listdir(gd)):
                if fn.endswith(".md"):
                    blob += open(os.path.join(gd, fn), encoding="utf-8").read() + "\n"
        present = set(_re.findall(r"^## ([A-Z][A-Z0-9]+-\d{3,4})", blob, flags=_re.M))
        for rid in ids:
            if rid not in present:
                f.append(f"local-resolution: {skill}: reachable {rid} not present in any skill-local shard")
    return f


REF_LINK = re.compile(r"\]\((references/generated/[A-Za-z0-9._-]+\.md)\)")

def _skillmd_refs(root, skill):
    sp = os.path.join(root, SKILL_DIR, skill, "SKILL.md")
    if not os.path.exists(sp):
        return "", []
    text = open(sp, encoding="utf-8").read()
    return text, REF_LINK.findall(text)


def check_reference_path_existence(root):
    """Every skill-local references/generated/*.md link in a SKILL.md resolves to an existing file."""
    f = []
    for skill in os.listdir(os.path.join(root, SKILL_DIR)):
        text, refs = _skillmd_refs(root, skill)
        for rel in sorted(set(refs)):
            target = os.path.normpath(os.path.join(root, SKILL_DIR, skill, rel))
            if not os.path.exists(target):
                f.append(f"ref-path: {skill}/SKILL.md -> {rel} missing")
    return f

def check_no_cross_skill_reference(root):
    """No SKILL.md may reach generated references via ../ traversal, repo-root, scratchpad, or the dated reviews path."""
    f = []
    bad = re.compile(r"\.\./.*references/generated|/private/|scratchpad|reviews/2026-09-26-phase-b")
    for skill in os.listdir(os.path.join(root, SKILL_DIR)):
        text, _ = _skillmd_refs(root, skill)
        for m in sorted(set(x.group(0) for x in bad.finditer(text))):
            f.append(f"cross-skill: {skill}/SKILL.md uses forbidden reference path '{m}'")
    return f

def check_selective_load_policy(root):
    """References are on-demand Markdown links, not eager @-injection of every shard."""
    f = []
    for skill in os.listdir(os.path.join(root, SKILL_DIR)):
        text, refs = _skillmd_refs(root, skill)
        if not text:
            continue
        if re.search(r"@references/generated/", text):
            f.append(f"selective-load-policy: {skill}/SKILL.md uses eager @-injection")
        if refs and "]" not in text:  # links must be Markdown link form
            f.append(f"selective-load-policy: {skill}/SKILL.md references not in Markdown-link form")
    return f

def check_per_skill_supporting_file_reachability(root, runtime, reach):
    """Every domain a skill reaches has a shard file present under that skill; controls present if it reaches a control."""
    f = []
    want = pc.skill_shard_files(reach, runtime)
    for skill, files in want.items():
        gd = os.path.join(root, SKILL_DIR, skill, "references", "generated")
        for fn in files:
            if not os.path.exists(os.path.join(gd, fn)):
                f.append(f"supporting-reachability: {skill} missing shard {fn} for a reached domain")
    return f

def check_normative_classification_complete(root):
    """Every content ## section of each SKILL.md has >=1 normative-inventory statement (section coverage)."""
    f = []
    try:
        inv = _load(root, "design-pack/normative-inventory.json")
    except Exception as e:
        return [f"classification: inventory unreadable ({e})"]
    secs_by_skill = {}
    for st in inv["statements"]:
        secs_by_skill.setdefault(st["skill"], set()).add(st["section"])
    for skill in ("ui-design-craft", "motion-craft", "design-review-gate"):
        text, _ = _skillmd_refs(root, skill)
        blob = " ".join(secs_by_skill.get(skill, set()))
        for sec in re.findall(r"^## (.+)$", text, flags=re.M):
            low = sec.lower()
            if low.startswith(("corpus-derived", "when not", "provenance")):
                continue
            num = re.match(r"(\d+)\.", sec)
            token = ("\u00a7" + num.group(1)) if num else sec.split(" ")[0]
            if token not in blob and sec[:12] not in blob:
                f.append(f"classification: {skill} section '{sec}' has no inventory statement")
    return f

def check_normative_bijection(root):
    """inventory <-> classification is 1:1; corpus_ids valid; pack-local ext_id present; orchestration rows carry no semantic ids."""
    f = []
    inv = _load(root, "design-pack/normative-inventory.json")
    nc = _load(root, "design-pack/normative-classification.json")
    ext = _load(root, os.path.join(GEN, "local-extensions.json"))
    corpus_ids = {r["id"] for r in _load(root, pc.CANONICAL_CORPUS_PATH)}
    inv_ids = [s["stmt_id"] for s in inv["statements"]]
    cls_ids = [r["stmt_id"] for r in nc["rows"]]
    if sorted(inv_ids) != sorted(cls_ids):
        f.append("bijection: inventory stmt_id set != classification stmt_id set")
    if len(cls_ids) != len(set(cls_ids)):
        f.append("bijection: duplicate stmt_id in classification")
    ext_ids_registry = {e["ext_id"] for e in ext["extensions"]}
    for r in nc["rows"]:
        d = r["disposition"]
        if d == "corpus-backed":
            ids = r.get("corpus_ids") or []
            if not ids:
                f.append(f"bijection: {r['stmt_id']} corpus-backed with no corpus_ids")
            for cid in ids:
                if cid not in corpus_ids:
                    f.append(f"bijection: {r['stmt_id']} cites non-corpus id {cid}")
        elif d == "pack-local-extension":
            if r.get("ext_id") not in ext_ids_registry:
                f.append(f"bijection: {r['stmt_id']} ext_id not in local-extensions.json")
        elif d == "orchestration-only":
            if r.get("corpus_ids") or r.get("ext_id"):
                f.append(f"bijection: orchestration-only {r['stmt_id']} carries a semantic id")
        else:
            f.append(f"bijection: {r['stmt_id']} unknown disposition {d!r}")
    # local-extensions all trace back to a pack-local row
    ple_rows = {r["ext_id"] for r in nc["rows"] if r.get("disposition") == "pack-local-extension"}
    for e in ext["extensions"]:
        if e["ext_id"] not in ple_rows:
            f.append(f"bijection: local-extension {e['ext_id']} has no classification row")
    return f

def check_per_extension_conflict_review(root):
    """Every pack-local extension carries relation in {stricter,orthogonal,implementation-specific} + a non-empty why_no_conflict; 0 global conflicts."""
    f = []
    nc = _load(root, "design-pack/normative-classification.json")
    if nc.get("conflicts_found"):
        f.append(f"conflict-review: {len(nc['conflicts_found'])} conflict(s) recorded")
    ok_rel = {"stricter", "orthogonal", "implementation-specific"}
    for r in nc["rows"]:
        if r.get("disposition") == "pack-local-extension":
            if r.get("relation") not in ok_rel:
                f.append(f"conflict-review: {r.get('ext_id')} relation {r.get('relation')!r} invalid")
            if not (r.get("why_no_conflict") or "").strip():
                f.append(f"conflict-review: {r.get('ext_id')} missing why_no_conflict")
    return f

def check_clean_regeneration(root):
    """Rebuild every generated artifact in memory from the canonical corpus; fail on any byte diff vs the on-disk tree. No timestamps."""
    f = []
    recs, corpus_sha = pc.load_canonical(root)
    runtime, support = pc.classify(recs); reach = pc.reachability(recs)
    runtime_txt = pc.dumps(runtime); support_txt = pc.dumps(support); reach_txt = pc.dumps(reach)
    ext = pc.build_local_extensions(root); ext_txt = pc.dumps(ext)
    shards = pc.render_shards(runtime); per_skill = pc.skill_shard_files(reach, runtime)
    all_rt = list(pc._all_runtime(runtime)); rt_byid = {r["id"]: r for r in all_rt}
    cross = pc.skill_cross_domain(reach, all_rt)
    def _stext(skill, fn):
        if fn == "control-dependencies.md":
            return pc.render_control_dependencies([rt_byid[i] for i in cross.get(skill, [])])
        return shards[fn]
    skill_shard_sha = {}
    for skill, files in per_skill.items():
        for fn in files:
            skill_shard_sha[f"skills/{skill}/references/generated/{fn}"] = pc.sha256_bytes(_stext(skill, fn).encode())
    scoped = os.path.join(root, pc.SCOPED_NOTICE)
    notice_rel = {
        "reason": "design-pack ships as ./design-pack; the canonical repo-level notice is outside that boundary, so a byte-identical scoped copy is emitted inside it.",
        "canonical_notice": pc.CANONICAL_NOTICE_PATH, "scoped_copy": pc.SCOPED_NOTICE,
        "sha256": pc.CANONICAL_NOTICE_SHA256,
        "byte_identical": os.path.exists(scoped) and pc.sha256_file(scoped) == pc.CANONICAL_NOTICE_SHA256,
        "license_text_reconstructed": False}
    manifest_txt = pc.dumps(pc.build_manifest(corpus_sha, runtime_txt, support_txt, reach_txt, ext_txt, skill_shard_sha, recs, notice_rel))
    want = {os.path.join(GEN, "runtime.json"): runtime_txt, os.path.join(GEN, "projection-support.json"): support_txt,
            os.path.join(GEN, "skill-reachability.json"): reach_txt, os.path.join(GEN, "local-extensions.json"): ext_txt,
            os.path.join(GEN, "manifest.json"): manifest_txt}
    for skill, files in per_skill.items():
        for fn in files:
            want[os.path.join(SKILL_DIR, skill, "references", "generated", fn)] = _stext(skill, fn)
    for rel, text in want.items():
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            f.append(f"clean-regen: missing {rel}")
        elif open(p, encoding="utf-8").read() != text:
            f.append(f"clean-regen: {rel} differs from clean regeneration")
    if not notice_rel["byte_identical"]:
        f.append("clean-regen: scoped notice not byte-identical")
    return f

def check_pack_local_extension_non_conflict(root):
    """local-extensions is authority-labelled + non-Phase-B; delegates per-extension conflict to conflict-review."""
    f = []
    ext = _load(root, os.path.join(GEN, "local-extensions.json"))
    if ext.get("phase_b_provenance") is not False:
        f.append("extension-conflict: local-extensions claims Phase-B provenance")
    for e in ext.get("extensions", []):
        if e.get("authority") != "pack-local-extension":
            f.append(f"extension-conflict: {e.get('ext_id')} not authority=pack-local-extension")
    return f

def check_provenance_separation(root, runtime):
    """runtime.json carries only canonical corpus records; local-extensions.json is separate + labelled."""
    f = []
    corpus_ids = {r["id"] for r in _load(root, pc.CANONICAL_CORPUS_PATH)}
    for r in runtime_records(runtime):
        if r["id"] not in corpus_ids:
            f.append(f"provenance: runtime.json has non-corpus id {r['id']}")
    man = _load(root, os.path.join(GEN, "manifest.json"))
    ga = man.get("generated_artifacts", {})
    if ga.get("generated/runtime.json", {}).get("authority") != "phase-b-corpus":
        f.append("provenance: manifest runtime.json not authority=phase-b-corpus")
    le = ga.get("generated/local-extensions.json", {})
    if le.get("authority") != "pack-local-extension" or le.get("phase_b_provenance") is not False:
        f.append("provenance: manifest local-extensions.json not labelled pack-local-extension / non-Phase-B")
    return f

def _unmapped_removed(head_secs, cur_secs, recorded_deletions, skill):
    return [sec for sec in sorted(set(head_secs) - set(cur_secs))
            if (skill, sec) not in recorded_deletions]


def check_unmapped_prose(root):
    """No SKILL.md section present at git HEAD may be absent now unless recorded as a mapped deletion.
    Reports (does not fail on) the unmapped-prose list."""
    f = []
    try:
        mapping = _load(root, "design-pack/prose-mapping.json")
    except Exception as e:
        return [f"unmapped-prose: prose-mapping.json unreadable: {e}"]
    recorded_deletions = set()
    for d in mapping.get("deletions_this_pass", []):
        recorded_deletions.add((d.get("skill"), d.get("section")))
    for skill in ("ui-design-craft", "motion-craft", "design-review-gate"):
        rel = f"{SKILL_DIR}/{skill}/SKILL.md"
        try:
            head = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=root,
                                   capture_output=True, text=True, check=True).stdout
        except Exception as e:
            f.append(f"unmapped-prose: cannot read HEAD:{rel}: {e}"); continue
        head_secs = set(re.findall(r"^## (.+)$", head, flags=re.M))
        cur = open(os.path.join(root, rel), encoding="utf-8").read()
        cur_secs = set(re.findall(r"^## (.+)$", cur, flags=re.M))
        for sec in _unmapped_removed(head_secs, cur_secs, recorded_deletions, skill):
            f.append(f"unmapped-prose: {skill} section '{sec}' removed without a recorded mapping")
    return f

def check_distribution_attribution(root):
    """design-pack ships as ./design-pack; the canonical notice is outside that boundary,
    so a byte-identical scoped copy must exist inside design-pack/."""
    f = []
    scoped = os.path.join(root, pc.SCOPED_NOTICE)
    if not os.path.exists(scoped):
        return ["attribution: scoped notice missing inside design-pack/"]
    if pc.sha256_file(scoped) != pc.CANONICAL_NOTICE_SHA256:
        f.append("attribution: scoped notice not byte-identical to canonical")
    return f
