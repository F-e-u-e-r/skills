#!/usr/bin/env python3
"""D6-B2.1 deterministic production projection of the Phase-B canonical corpus.

Emits, under design-pack/, a physically-separated production bridge:
  generated/runtime.json            454 runtime records (rule/synthesized_rule/decision_table/dial)
  generated/projection-support.json  88 support records (evidence/conflict)
  generated/manifest.json            build manifest (per-artifact SHA-256, populations, kind policy,
                                      canonical corpus SHA/merge SHA, attribution linkage; NO timestamps)
  generated/skill-reachability.json  which production skill(s) reach each of the 454 runtime records
  references/generated/<domain>.md   agent-consumption shards (verbatim semantic fields)
  references/generated/controls.md   decision tables + dials (control closure)
  THIRD_PARTY_NOTICES.md             byte-identical scoped copy of the canonical notice (attribution)

Semantic authority = the canonical corpus. This projector performs
projection/implementation transforms only; effective_semantics is copied VERBATIM.
NOT authorized: semantic rewriting, mining/reconciliation, corpus modification, commit.
Same input -> byte-identical output.
"""
import hashlib
import json
import os
import re

# --- pinned canonical input identity (PR #254 merge checkpoint) --------------
CANONICAL_CORPUS_PATH = "reviews/2026-09-26-phase-b-semantic-publication/public_records.json"
CANONICAL_CORPUS_SHA256 = "16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b"
CANONICAL_NOTICE_PATH = "reviews/2026-09-26-phase-b-semantic-publication/THIRD_PARTY_NOTICES.md"
CANONICAL_NOTICE_SHA256 = "b04f228ded8896dec1129aa81b13a126f0913086f8830116cbf61325863a4d4c"
CANONICAL_MERGE_SHA = "44f10443c16e926515af86ebdd1d52e003ed98cc"
GENERATOR_VERSION = "design-pack-projector/2"
RUNTIME_SCHEMA_VERSION = 2

GEN_DIR = "design-pack/generated"
REF_DIR = "design-pack/references/generated"
SCOPED_NOTICE = "design-pack/THIRD_PARTY_NOTICES.md"

RUNTIME_PAYLOAD_KINDS = ("rule", "synthesized_rule")
RUNTIME_CONTROL_KINDS = ("decision_table", "dial")
RUNTIME_KINDS = RUNTIME_PAYLOAD_KINDS + RUNTIME_CONTROL_KINDS
SUPPORT_KINDS = ("evidence", "conflict")
KIND_POLICY = {
    "rule": "runtime-payload", "synthesized_rule": "runtime-payload",
    "decision_table": "runtime-control", "dial": "runtime-control",
    "evidence": "projection-support-only", "conflict": "projection-support-only",
}
KNOWN_KINDS = set(KIND_POLICY)
KEEP_RECORD_FIELDS = ("id", "kind", "effective_semantics", "public_expression", "notes")

# skill rule-domain reachability (control reach is DERIVED by closure, below)
ALL_RULE_DOMAINS = {"A11Y", "ANTISLOP", "COLOR", "INTERACT", "MOTION", "SPACE", "STRUCT", "TYPO", "UX"}
SKILL_RULE_DOMAINS = {
    "ui-design-craft": ALL_RULE_DOMAINS - {"MOTION"},   # static-visual producer: every non-motion domain
    "motion-craft": {"MOTION"},                          # motion producer
    "design-review-gate": set(ALL_RULE_DOMAINS),         # compliance reviewer: the full rule set
}
SKILLS = ("ui-design-craft", "motion-craft", "design-review-gate")

SELECTOR_LEAD = re.compile(r"\s*([A-Z][A-Z0-9]+-\d{3,4})")
DOMAIN_OF = re.compile(r"^([A-Z][A-Z0-9]*)-")


class ProjectionError(Exception):
    pass


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def sha256_file(path):
    with open(path, "rb") as f:
        return sha256_bytes(f.read())

def domain_of(rid):
    return DOMAIN_OF.match(rid).group(1)

def selector_ref(rec):
    sel = (rec.get("effective_semantics") or {}).get("selector")
    if not sel:
        return None
    m = SELECTOR_LEAD.match(sel)
    return m.group(1) if m else None

def curate(rec):
    return {k: rec[k] for k in KEEP_RECORD_FIELDS if k in rec}

def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


# --- agent-consumption shard rendering (deterministic; verbatim fields) ------
RULE_FIELD_ORDER = ["strength", "scope", "condition", "override", "exceptions",
                    "enforcement", "verification", "selector"]

def render_payload_block(rec):
    es = rec.get("effective_semantics") or {}
    out = [f"## {rec['id']}"]
    for k in RULE_FIELD_ORDER:
        if es.get(k) not in (None, ""):
            out.append(f"- **{k}:** {es[k]}")
    df = es.get("derived_from")
    if df:
        out.append(f"- **derived_from** (lineage — sources consumed into synthesis; not live records): {', '.join(df)}")
    if rec.get("notes") not in (None, ""):
        out.append(f"- **notes:** {rec['notes']}")
    if rec.get("public_expression") not in (None, ""):
        out.append(f"- **public_expression:** {rec['public_expression']}")
    return "\n".join(out)

def render_control_block(rec):
    es = rec.get("effective_semantics") or {}
    out = [f"## {rec['id']} ({rec['kind']})"]
    if rec["kind"] == "decision_table":
        out.append(f"- **input_dimension:** {es.get('input_dimension','')}")
        out.append(f"- **selection_mode:** {es.get('selection_mode','')}")
        out.append("- **rows** (ordered):")
        for row in es.get("rows") or []:
            out.append(f"  - `{row.get('id')}` — when: {row.get('condition','')} → {', '.join(row.get('rule_ids') or [])}")
    else:  # dial
        out.append(f"- **baseline:** {es.get('baseline')}")
        out.append(f"- **range:** {es.get('range')}")
        out.append("- **gated_branches** (ordered):")
        for br in es.get("gated_branches") or []:
            out.append(f"  - when {br.get('condition','')} → {', '.join(br.get('rule_ids') or [])}")
    if rec.get("public_expression") not in (None, ""):
        out.append(f"- **public_expression:** {rec['public_expression']}")
    return "\n".join(out)

def _shard_header(title, n):
    return (f"# Design Pack runtime reference — {title} (GENERATED; do not hand-edit)\n\n"
            f"Deterministic projection of the canonical Phase-B corpus "
            f"(SHA-256 `{CANONICAL_CORPUS_SHA256}`, merge `{CANONICAL_MERGE_SHA}`) via "
            f"`design-pack/tools/project_corpus.py`. Authoritative semantic source; "
            f"fields rendered verbatim. {n} record(s).\n")

def render_shards(runtime):
    """Return {relpath_under_REF_DIR: text}. One shard per payload domain + one controls shard."""
    shards = {}
    payload = runtime["rules"] + runtime["synthesized_rules"]
    by_domain = {}
    for r in payload:
        by_domain.setdefault(domain_of(r["id"]), []).append(r)
    for dom in sorted(by_domain):
        recs = sorted(by_domain[dom], key=lambda x: x["id"])
        body = "\n\n".join(render_payload_block(r) for r in recs)
        shards[f"{dom.lower()}.md"] = _shard_header(dom, len(recs)) + "\n" + body + "\n"
    controls = sorted(runtime["decision_tables"] + runtime["dials"], key=lambda x: x["id"])
    body = "\n\n".join(render_control_block(r) for r in controls)
    shards["controls.md"] = _shard_header("CONTROLS (decision tables + dials)", len(controls)) + "\n" + body + "\n"
    return shards


def load_canonical(root):
    p = os.path.join(root, CANONICAL_CORPUS_PATH)
    got = sha256_file(p)
    if got != CANONICAL_CORPUS_SHA256:
        raise ProjectionError(f"canonical-source: SHA {got} != {CANONICAL_CORPUS_SHA256}")
    with open(p, encoding="utf-8") as f:
        return json.load(f), got


def classify(recs):
    ids = [r["id"] for r in recs]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise ProjectionError(f"duplicate-id: {dupes}")
    unknown = sorted({r["kind"] for r in recs if r["kind"] not in KNOWN_KINDS})
    if unknown:
        raise ProjectionError(f"unknown-kind (fail closed): {unknown}")
    runtime = {"rules": [], "synthesized_rules": [], "decision_tables": [], "dials": []}
    support = {"evidence": [], "conflict": []}
    to_bucket = {"rule": ("rt", "rules"), "synthesized_rule": ("rt", "synthesized_rules"),
                 "decision_table": ("rt", "decision_tables"), "dial": ("rt", "dials"),
                 "evidence": ("sp", "evidence"), "conflict": ("sp", "conflict")}
    for r in recs:
        w, key = to_bucket[r["kind"]]
        (runtime if w == "rt" else support)[key].append(curate(r))
    for d in (runtime, support):
        for k in d:
            d[k].sort(key=lambda x: x["id"])
    return runtime, support


def reachability(recs):
    """Return {skill: sorted([record ids])} plus fan-out. Rule reach by domain policy;
    control reach DERIVED by closure: a control is reachable by a skill if any rule the
    skill reaches selector-binds it, or it routes/gates a rule the skill reaches."""
    byid = {r["id"]: r for r in recs}
    rules = [r for r in recs if r["kind"] in RUNTIME_PAYLOAD_KINDS]
    controls = [r for r in recs if r["kind"] in RUNTIME_CONTROL_KINDS]

    def control_targets(c):
        es = c.get("effective_semantics") or {}
        out = set()
        for row in es.get("rows") or []:
            out |= set(row.get("rule_ids") or [])
        for br in es.get("gated_branches") or []:
            out |= set(br.get("rule_ids") or [])
        return out

    reach = {s: set() for s in SKILLS}
    for s in SKILLS:
        doms = SKILL_RULE_DOMAINS[s]
        skill_rules = {r["id"] for r in rules if domain_of(r["id"]) in doms}
        reach[s] |= skill_rules
        # control closure
        for c in controls:
            bound_by = any(selector_ref(byid[rid]) == c["id"] for rid in skill_rules)
            routes_into = bool(control_targets(c) & skill_rules)
            if bound_by or routes_into:
                reach[s].add(c["id"])
    return {s: sorted(reach[s]) for s in SKILLS}


def skill_shard_files(reach, runtime):
    """Per skill: the shard filenames it consumes = domains of its reachable payload records + controls.md if it reaches any control."""
    kind={r["id"]:r["kind"] for r in _all_runtime(runtime)}
    out={}
    for skill, ids in reach.items():
        doms=set(); needs_controls=False
        for rid in ids:
            k=kind.get(rid)
            if k in RUNTIME_PAYLOAD_KINDS: doms.add(domain_of(rid))
            elif k in RUNTIME_CONTROL_KINDS: needs_controls=True
        files=sorted(f"{d.lower()}.md" for d in doms)
        if needs_controls: files.append("controls.md")
        out[skill]=files
    return out


def _all_runtime(runtime):
    for k in ("rules","synthesized_rules","decision_tables","dials"):
        for r in runtime[k]: yield r


def build_local_extensions(root):
    """Emit the pack-local-extension registry from the bijective statement-level classification.
    Authority = pack-local-extension; explicitly NOT Phase-B corpus provenance; never enters runtime.json."""
    with open(os.path.join(root, "design-pack/normative-classification.json"), encoding="utf-8") as f:
        nc = json.load(f)
    exts = []
    for r in nc["rows"]:
        if r.get("disposition") == "pack-local-extension":
            exts.append({"ext_id": r["ext_id"], "stmt_id": r["stmt_id"], "skill": r["skill"],
                         "section": r.get("section"), "statement": r["statement"],
                         "relation": r.get("relation"), "nearest_corpus_ids": r.get("nearest_corpus_ids", []),
                         "why_no_conflict": r.get("why_no_conflict"), "authority": "pack-local-extension"})
    exts.sort(key=lambda x: x["ext_id"])
    from collections import Counter
    by_skill = dict(Counter(e["skill"] for e in exts))
    return {"_note": "Pack-local Design Pack production requirements NOT represented in the canonical Phase-B corpus. Authority is STRICTLY BELOW canonical corpus semantics; each entry is stricter/orthogonal/implementation-specific and may only add or tighten, never weaken/reverse/broaden/contradict a corpus rule. Carries NO Phase-B provenance; never merged into runtime.json.",
            "authority": "pack-local-extension", "phase_b_provenance": False,
            "source": "design-pack/normative-classification.json (bijective with normative-inventory.json)",
            "count": len(exts), "count_by_skill": by_skill, "extensions": exts}


def build_manifest(corpus_sha, runtime_txt, support_txt, reach_txt, ext_txt, skill_shard_sha, recs, notice_relationship):
    from collections import Counter
    canon = dict(Counter(r["kind"] for r in recs))
    runtime_total = sum(canon.get(k, 0) for k in RUNTIME_KINDS)
    return {
        "artifact": "design-pack production bridge manifest (generated; do not hand-edit)",
        "generated": True, "generator": GENERATOR_VERSION, "runtime_schema_version": RUNTIME_SCHEMA_VERSION,
        "canonical_corpus": {"path": CANONICAL_CORPUS_PATH, "sha256": corpus_sha, "merge_sha": CANONICAL_MERGE_SHA},
        "kind_policy": KIND_POLICY,
        "population": {
            "canonical_total": len(recs), "canonical_by_kind": canon,
            "runtime_total": runtime_total, "support_total": len(recs) - runtime_total,
            "runtime_payload_by_kind": {k: canon[k] for k in RUNTIME_PAYLOAD_KINDS if k in canon},
            "runtime_control_by_kind": {k: canon[k] for k in RUNTIME_CONTROL_KINDS if k in canon},
            "projection_support_by_kind": {k: canon[k] for k in SUPPORT_KINDS if k in canon},
        },
        "generated_artifacts": {
            "generated/runtime.json": {"sha256": sha256_bytes(runtime_txt.encode()), "authority": "phase-b-corpus"},
            "generated/projection-support.json": {"sha256": sha256_bytes(support_txt.encode()), "authority": "phase-b-corpus"},
            "generated/skill-reachability.json": {"sha256": sha256_bytes(reach_txt.encode())},
            "generated/local-extensions.json": {"sha256": sha256_bytes(ext_txt.encode()), "authority": "pack-local-extension", "phase_b_provenance": False},
        },
        "skill_local_reference_sha256": skill_shard_sha,
        "attribution": notice_relationship,
    }


def main():
    root = os.getcwd()
    recs, corpus_sha = load_canonical(root)
    runtime, support = classify(recs)
    reach = reachability(recs)
    runtime_txt = dumps(runtime); support_txt = dumps(support); reach_txt = dumps(reach)
    ext = build_local_extensions(root); ext_txt = dumps(ext)

    # attribution: byte-identical scoped notice inside the plugin boundary
    with open(os.path.join(root, CANONICAL_NOTICE_PATH), "rb") as fh: notice_bytes = fh.read()
    if sha256_bytes(notice_bytes) != CANONICAL_NOTICE_SHA256:
        raise ProjectionError("attribution: canonical notice SHA mismatch")
    with open(os.path.join(root, SCOPED_NOTICE), "wb") as fh: fh.write(notice_bytes)
    notice_relationship = {
        "reason": "design-pack ships as ./design-pack; the canonical repo-level notice is outside that boundary, so a byte-identical scoped copy is emitted inside it.",
        "canonical_notice": CANONICAL_NOTICE_PATH, "scoped_copy": SCOPED_NOTICE,
        "sha256": CANONICAL_NOTICE_SHA256,
        "byte_identical": sha256_file(os.path.join(root, SCOPED_NOTICE)) == CANONICAL_NOTICE_SHA256,
        "license_text_reconstructed": False}

    # SKILL-LOCAL shards (documented supporting-file model): mirror each skill's shards under its own references/generated/
    all_shards = render_shards(runtime)
    per_skill = skill_shard_files(reach, runtime)
    shared = os.path.join(root, REF_DIR)  # remove the superseded shared consumption dir
    if os.path.isdir(shared):
        for fn in os.listdir(shared): os.remove(os.path.join(shared, fn))
        os.rmdir(shared)
    skill_shard_sha = {}
    for skill, files in per_skill.items():
        d = os.path.join(root, "design-pack/skills", skill, "references/generated")
        os.makedirs(d, exist_ok=True)
        # clean stale generated shards, then write current
        for fn in list(os.listdir(d)):
            if fn.endswith(".md"): os.remove(os.path.join(d, fn))
        for fn in files:
            text = all_shards[fn]
            with open(os.path.join(d, fn), "w", encoding="utf-8") as fh: fh.write(text)
            skill_shard_sha[f"skills/{skill}/references/generated/{fn}"] = sha256_bytes(text.encode())

    manifest = build_manifest(corpus_sha, runtime_txt, support_txt, reach_txt, ext_txt, skill_shard_sha, recs, notice_relationship)
    manifest_txt = dumps(manifest)

    os.makedirs(os.path.join(root, GEN_DIR), exist_ok=True)
    for name, text in (("runtime.json", runtime_txt), ("projection-support.json", support_txt),
                       ("skill-reachability.json", reach_txt), ("local-extensions.json", ext_txt),
                       ("manifest.json", manifest_txt)):
        with open(os.path.join(root, GEN_DIR, name), "w", encoding="utf-8") as fh: fh.write(text)
    old = os.path.join(root, GEN_DIR, "design-runtime.json")
    if os.path.exists(old): os.remove(old)

    print("runtime/support:", sum(len(v) for v in runtime.values()), "/", sum(len(v) for v in support.values()))
    print("reachability union:", len(set().union(*[set(v) for v in reach.values()])))
    print("local-extensions:", ext["count"])
    for skill, files in per_skill.items(): print(f"  skill-local[{skill}] shards:", files)
    print("attribution byte_identical:", notice_relationship["byte_identical"])


if __name__ == "__main__":
    main()
