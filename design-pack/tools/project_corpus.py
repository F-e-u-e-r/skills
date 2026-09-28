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
  THIRD_PARTY_NOTICES.md             scoped notice, composed byte-derived: Part A = the canonical corpus
                                      notice verbatim; Part B = the repository-root THIRD-PARTY-NOTICES.md
                                      entries applicable to this payload (skill-level sources), verbatim,
                                      + the root MIT text restricted to those works
  LICENSE                            verbatim copy of the repository LICENSE (MIT; design-pack's own material)
  LICENSE-APACHE-2.0                 verbatim copy of the repository-root Apache-2.0 full text (required by
                                      the Apache-2.0 work in Part B; SHA-256 pinned below)

The legal bundle exists because the plugin's distribution boundary is ./design-pack alone: every legal
source above lives outside it, so byte-derived copies are emitted inside and gated (projection_checks
check_distribution_attribution / check_clean_regeneration). The root notice stays the semantic authority
for attribution statements; nothing legal is hand-maintained inside design-pack/.

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
CANONICAL_CORPUS_PATH = "corpus/design-pack/public_records.json"
CANONICAL_CORPUS_SHA256 = "16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b"
CANONICAL_NOTICE_PATH = "corpus/design-pack/THIRD_PARTY_NOTICES.md"
CANONICAL_NOTICE_SHA256 = "b04f228ded8896dec1129aa81b13a126f0913086f8830116cbf61325863a4d4c"
CANONICAL_MERGE_SHA = "44f10443c16e926515af86ebdd1d52e003ed98cc"
GENERATOR_VERSION = "design-pack-projector/2"
RUNTIME_SCHEMA_VERSION = 2

GEN_DIR = "design-pack/generated"
REF_DIR = "design-pack/references/generated"
SCOPED_NOTICE = "design-pack/THIRD_PARTY_NOTICES.md"

# --- legal bundle: canonical repository sources projected byte-derived into the plugin boundary ----
ROOT_LICENSE_PATH = "LICENSE"                    # MIT; governs design-pack's own material
ROOT_NOTICE_PATH = "THIRD-PARTY-NOTICES.md"      # canonical legal notice = semantic authority for attribution
ROOT_APACHE_TEXT_PATH = "LICENSE-APACHE-2.0"     # canonical Apache-2.0 full text (repository root)
# Bytes of LICENSE-APACHE-2.0 = https://www.apache.org/licenses/LICENSE-2.0.txt (11358 bytes, fetched
# 2026-09-28). Pinned because the text is fixed: any drift is corruption, never a legitimate edit.
APACHE_TEXT_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
BUNDLE_LICENSE = "design-pack/LICENSE"
BUNDLE_APACHE_TEXT = "design-pack/LICENSE-APACHE-2.0"
# A root-notice entry (a '### ' block under the MIT / Apache sections) is applicable to this payload
# iff its text names the plugin or one of its skills. Idea-level sources (root section 4) carry no
# notice obligation by the root notice's own statement and are not projected.
NOTICE_APPLICABILITY_MARKERS = ("design-pack", "ui-design-craft", "motion-craft", "design-review-gate")
ROOT_MIT_SECTION = "Works under the MIT License"
ROOT_APACHE_SECTION = "Works under the Apache License 2.0"
ROOT_MIT_TEXT_SECTION = "MIT License text"
MIT_CONDITION_SENTENCE = "The above copyright notice and this permission notice shall be included in all"

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

# Apache-2.0 section 4(b): a file carrying ADAPTED EXPRESSION from an Apache-2.0 work must itself carry a
# prominent change notice. The sites are read mechanically from the applicable Apache entries of the root
# notice: a backticked design-pack skill name immediately followed by a section marker ("`motion-craft` §7"),
# optionally followed by "adapted from `<upstream path>`". The affected SKILL.md section must carry a
# notice that names the upstream repository, states the material was adapted and modified, and points at
# the shipped legal artifacts by their basenames (every backticked plain filename it names must ship).
_ADAPTED_SITE_RE = re.compile(r"`(" + "|".join(SKILLS) + r")` §(\d+)(?:[^`]*?adapted from\s+`([^`]+)`)?")
CHANGE_NOTICE_MARK = "Change notice (Apache-2.0 section 4(b))"
CHANGE_NOTICE_WORDS = ("adapted", "modified")

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
    """Per-skill reachable set under BIDIRECTIONAL runtime closure to a fixed point:
      (a) rule -> control it selector-binds;
      (b) control -> every rule it routes/gates (rows[].rule_ids, gated_branches[].rule_ids);
      (c) control that routes into an already-reached rule becomes reachable.
    Cross-domain target rules pulled in by (b) are included (minimally)."""
    byid = {r["id"]: r for r in recs}
    rule_ids = {r["id"] for r in recs if r["kind"] in RUNTIME_PAYLOAD_KINDS}
    controls = [r for r in recs if r["kind"] in RUNTIME_CONTROL_KINDS]
    ctrl_ids = {c["id"] for c in controls}

    def control_targets(c):
        es = c.get("effective_semantics") or {}
        out = set()
        for row in es.get("rows") or []:
            out |= set(row.get("rule_ids") or [])
        for br in es.get("gated_branches") or []:
            out |= set(br.get("rule_ids") or [])
        return out

    reach = {}
    for s in SKILLS:
        doms = SKILL_RULE_DOMAINS[s]
        r = {rid for rid in rule_ids if domain_of(rid) in doms}
        changed = True
        while changed:
            changed = False
            for rid in [x for x in r if x in rule_ids]:
                ref = selector_ref(byid[rid])
                if ref and ref in ctrl_ids and ref not in r:
                    r.add(ref); changed = True
            for c in controls:
                tgts = control_targets(c)
                if c["id"] in r:
                    for t in tgts:
                        if t not in r:
                            r.add(t); changed = True
                elif tgts & r and c["id"] not in r:
                    r.add(c["id"]); changed = True
        reach[s] = sorted(r)
    return reach


def skill_cross_domain(reach, recs):
    """Per skill: reachable PAYLOAD rules whose domain is outside the skill's own rule domains
    (pulled in only by control-target closure). These become the skill-local control-dependencies shard."""
    byid = {r["id"]: r for r in recs}
    out = {}
    for s, ids in reach.items():
        doms = SKILL_RULE_DOMAINS.get(s, set())
        out[s] = sorted(i for i in ids
                        if byid[i]["kind"] in RUNTIME_PAYLOAD_KINDS and domain_of(i) not in doms)
    return out

def render_control_dependencies(records):
    """Deterministic skill-local shard of CROSS-DOMAIN records required by control-target closure
    (so a skill never depends on searching another skill's references). Fields verbatim."""
    body = "\n\n".join(render_payload_block(r) for r in sorted(records, key=lambda x: x["id"]))
    return (_shard_header("CONTROL DEPENDENCIES (cross-domain rules required by this skill's controls)", len(records))
            + "\n" + body + "\n")


def skill_shard_files(reach, runtime):
    """Per skill: shard filenames it consumes = domains of its reachable payload records + controls.md
    (if it reaches a control) + control-dependencies.md (if control-closure pulled cross-domain rules)."""
    kind = {r["id"]: r["kind"] for r in _all_runtime(runtime)}
    recs = list(_all_runtime(runtime))
    cross = skill_cross_domain(reach, recs)
    out = {}
    for skill, ids in reach.items():
        doms = set(); needs_controls = False
        for rid in ids:
            k = kind.get(rid)
            if k in RUNTIME_PAYLOAD_KINDS:
                if domain_of(rid) in SKILL_RULE_DOMAINS.get(skill, set()):
                    doms.add(domain_of(rid))
            elif k in RUNTIME_CONTROL_KINDS:
                needs_controls = True
        files = sorted(f"{d.lower()}.md" for d in doms)
        if needs_controls:
            files.append("controls.md")
        if cross.get(skill):
            files.append("control-dependencies.md")
        out[skill] = files
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


# --- legal bundle (distribution closure): byte-derived from canonical repository sources ---------
_SECTION_RE = re.compile(r"^## (\d+)\. (.+?)\s*$")
_ENTRY_RE = re.compile(r"^### ")
_COPYRIGHT_RE = re.compile(r"^Copyright \(c\) ")

def _strip_separator(lines):
    """Drop trailing blank lines and a trailing '---' rule (section separators, not entry content)."""
    out = list(lines)
    while out and out[-1].strip() == "":
        out.pop()
    if out and out[-1].strip() == "---":
        out.pop()
        while out and out[-1].strip() == "":
            out.pop()
    return out

def parse_root_notice(text):
    """Split the canonical root notice into its numbered '## N. Title' sections; within a section, '### '
    lines open entries. Entry text runs from its heading to the line before the next entry or section,
    separators stripped. Returns [{num, title, body, entries: [{heading, text, copyright_lines}]}]."""
    sections = []
    cur = None
    for line in text.split("\n"):
        m = _SECTION_RE.match(line)
        if m:
            cur = {"num": int(m.group(1)), "title": m.group(2), "lines": [], "entries": []}
            sections.append(cur)
            continue
        if cur is None:
            continue
        if _ENTRY_RE.match(line):
            cur["entries"].append({"heading": line, "lines": [line]})
            continue
        (cur["entries"][-1]["lines"] if cur["entries"] else cur["lines"]).append(line)
    for s in sections:
        s["body"] = "\n".join(_strip_separator(s["lines"]))
        for e in s["entries"]:
            e["text"] = "\n".join(_strip_separator(e["lines"]))
            e["copyright_lines"] = [l for l in e["lines"] if _COPYRIGHT_RE.match(l)]
            del e["lines"]
        del s["lines"]
    return sections

def _section(sections, title):
    for s in sections:
        if s["title"] == title:
            return s
    raise ProjectionError(f"legal-bundle: root notice section {title!r} not found")

def _fenced_block(text):
    """Lines inside the first ``` fenced block of text."""
    out = []; inside = False
    for l in text.split("\n"):
        if l.startswith("```"):
            if inside:
                return out
            inside = True
            continue
        if inside:
            out.append(l)
    raise ProjectionError("legal-bundle: fenced block not found")

def entry_applicable(entry):
    return any(mk in entry["text"] for mk in NOTICE_APPLICABILITY_MARKERS)

def applicable_root_entries(sections):
    """[(kind, entry)] for every MIT / Apache root entry whose text names the plugin or one of its skills."""
    out = []
    for kind, title in (("mit", ROOT_MIT_SECTION), ("apache", ROOT_APACHE_SECTION)):
        for e in _section(sections, title)["entries"]:
            if entry_applicable(e):
                out.append((kind, e))
    return out

def render_scoped_mit_text(sections, selected_mit):
    """The root 'MIT License text' fenced block with its copyright list restricted to the selected works:
    header line, the selected copyright lines in root order, the permission text verbatim."""
    block = _fenced_block(_section(sections, ROOT_MIT_TEXT_SECTION)["body"])
    root_lines = [l for l in block if _COPYRIGHT_RE.match(l)]
    wanted = set()
    for _, e in selected_mit:
        if not e["copyright_lines"]:
            raise ProjectionError(f"legal-bundle: MIT entry without a copyright line: {e['heading']!r}")
        for l in e["copyright_lines"]:
            if l not in root_lines:
                raise ProjectionError(f"legal-bundle: root MIT text lacks the copyright line of {e['heading']!r}")
            wanted.add(l)
    last = max(i for i, l in enumerate(block) if _COPYRIGHT_RE.match(l))
    permission = block[last + 1:]
    while permission and permission[0].strip() == "":
        permission.pop(0)
    if not any(MIT_CONDITION_SENTENCE in l for l in permission):
        raise ProjectionError("legal-bundle: MIT permission text lacks the condition sentence")
    return "\n".join([block[0], ""] + [l for l in root_lines if l in wanted] + [""] + permission)

def render_scoped_notice(corpus_notice_bytes, root_text):
    """Compose the payload notice: Part A = corpus notice verbatim; Part B = applicable root entries verbatim
    + the restricted MIT text + the Apache full-text pointer. Deterministic: no timestamps, no environment."""
    sections = parse_root_notice(root_text)
    selected = applicable_root_entries(sections)
    if not selected:
        raise ProjectionError("legal-bundle: no root-notice entry is applicable to design-pack")
    mit = [(k, e) for k, e in selected if k == "mit"]
    apache = [(k, e) for k, e in selected if k == "apache"]
    parts = [
        "<!-- GENERATED by design-pack/tools/project_corpus.py; do not hand-edit. Every part below is byte-derived",
        "     from a canonical repository source; derivation and hashes: generated/manifest.json (\"attribution\"). -->",
        "# Third-Party Notices (design-pack distribution)",
        "",
        "The design-pack plugin is distributed as the `design-pack/` directory alone, so this file carries every",
        "third-party notice applicable to the files in this directory:",
        "",
        "- **Part A**: the canonical Phase-B design corpus that `generated/` and `skills/*/references/generated/`",
        "  derive from; a verbatim copy of `corpus/design-pack/THIRD_PARTY_NOTICES.md`.",
        "- **Part B**: the skill-level sources adapted into the three `skills/*/SKILL.md` files; the applicable",
        "  entries of the repository's `THIRD-PARTY-NOTICES.md`, reproduced verbatim, with the MIT copyright and",
        "  permission notice for the MIT works and, for the Apache-2.0 work, the full license text in",
        "  `LICENSE-APACHE-2.0` (this directory).",
        "",
        "The license governing design-pack's own material is `LICENSE` (MIT) in this directory.",
        "",
        "---",
        "",
        "## Part A: canonical corpus notice (verbatim copy of `corpus/design-pack/THIRD_PARTY_NOTICES.md`)",
        "",
        corpus_notice_bytes.decode("utf-8").rstrip("\n"),
        "",
        "---",
        "",
        "## Part B: skill-level sources (verbatim entries of the repository's `THIRD-PARTY-NOTICES.md`)",
        "",
    ]
    if mit:
        parts += ["## Part B.1: works under the MIT License", ""]
        for _, e in mit:
            parts += [e["text"], ""]
        parts += ["### MIT License text (applies to each Part B.1 work under its copyright notice above)", "",
                  "```", render_scoped_mit_text(sections, mit), "```", ""]
    if apache:
        parts += ["## Part B.2: works under the Apache License 2.0", ""]
        for _, e in apache:
            parts += [e["text"], ""]
        parts += [f"Full text of the Apache License, Version 2.0: `{os.path.basename(BUNDLE_APACHE_TEXT)}` in this directory",
                  f"(byte-identical to the repository-root `{ROOT_APACHE_TEXT_PATH}`).", ""]
    text = "\n".join(parts)
    consumed = "\n".join([e["text"] for _, e in selected] + [_section(sections, ROOT_MIT_TEXT_SECTION)["body"]])
    meta = {"applicable_entries": [e["heading"] for _, e in selected],
            "mit_entries": [e["heading"] for _, e in mit],
            "apache_entries": [e["heading"] for _, e in apache],
            "root_notice_consumed_sha256": sha256_bytes(consumed.encode("utf-8"))}
    return text, meta

def apache_adapted_sites(sections):
    """Files carrying adapted expression from an applicable Apache-2.0 work, read from the root notice
    (see _ADAPTED_SITE_RE): [{file, skill, section, upstream, adapted_from}] in root order."""
    out = []
    for kind, e in applicable_root_entries(sections):
        if kind != "apache":
            continue
        m = re.search(r"`([^`]+)`", e["heading"])
        upstream = m.group(1) if m else e["heading"]
        for s in _ADAPTED_SITE_RE.finditer(e["text"]):
            out.append({"file": f"design-pack/skills/{s.group(1)}/SKILL.md", "skill": s.group(1),
                        "section": int(s.group(2)), "upstream": upstream, "adapted_from": s.group(3)})
    return out

def render_legal_bundle(root):
    """Read the canonical legal sources under root and render every payload legal artifact.
    Returns ({output_rel: bytes}, accounting): a pure function of the sources; fails closed on a missing or
    drifted source. Shared by main() and by projection_checks (one derivation code path)."""
    def _read(rel):
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            raise ProjectionError(f"legal-bundle: canonical source missing: {rel}")
        with open(p, "rb") as fh:
            return fh.read()
    license_b = _read(ROOT_LICENSE_PATH)
    apache_b = _read(ROOT_APACHE_TEXT_PATH)
    if sha256_bytes(apache_b) != APACHE_TEXT_SHA256:
        raise ProjectionError(f"legal-bundle: {ROOT_APACHE_TEXT_PATH} SHA {sha256_bytes(apache_b)} != pinned {APACHE_TEXT_SHA256}")
    corpus_notice_b = _read(CANONICAL_NOTICE_PATH)
    if sha256_bytes(corpus_notice_b) != CANONICAL_NOTICE_SHA256:
        raise ProjectionError("attribution: canonical notice SHA mismatch")
    root_notice_b = _read(ROOT_NOTICE_PATH)
    notice_text, meta = render_scoped_notice(corpus_notice_b, root_notice_b.decode("utf-8"))
    notice_b = notice_text.encode("utf-8")
    sites = apache_adapted_sites(parse_root_notice(root_notice_b.decode("utf-8")))
    outputs = {BUNDLE_LICENSE: license_b, BUNDLE_APACHE_TEXT: apache_b, SCOPED_NOTICE: notice_b}
    accounting = {
        "reason": "design-pack ships as ./design-pack alone; every legal source (the repository LICENSE, the canonical "
                  "third-party notice, the Apache-2.0 full text, the corpus notice) lies outside that boundary, so "
                  "byte-derived copies of everything applicable to this payload are emitted inside it and gated.",
        "license_text_reconstructed": False,
        "applicability_markers": list(NOTICE_APPLICABILITY_MARKERS),
        "apache_4b": {
            "rule": "every file carrying adapted expression from an applicable Apache-2.0 work carries a prominent "
                    "change notice inside the adapted section (sites read from the root notice)",
            "notice_mark": CHANGE_NOTICE_MARK, "must_state": list(CHANGE_NOTICE_WORDS),
            "must_point_at": [os.path.basename(BUNDLE_APACHE_TEXT), os.path.basename(SCOPED_NOTICE)],
            "sites": sites,
        },
        "sources": {
            ROOT_LICENSE_PATH: {"sha256": sha256_bytes(license_b),
                                "role": "license governing design-pack's own material (MIT)"},
            ROOT_APACHE_TEXT_PATH: {"sha256": sha256_bytes(apache_b), "pinned_sha256": APACHE_TEXT_SHA256,
                                    "role": "Apache License 2.0 full text; bytes = https://www.apache.org/licenses/LICENSE-2.0.txt"},
            ROOT_NOTICE_PATH: {"consumed_sha256": meta["root_notice_consumed_sha256"],
                               "role": "canonical legal notice; semantic authority for attribution (the applicable entries and the MIT text are consumed)"},
            CANONICAL_NOTICE_PATH: {"sha256": CANONICAL_NOTICE_SHA256, "role": "canonical corpus notice (Part A)"},
        },
        "bundle": {
            BUNDLE_LICENSE: {"source": ROOT_LICENSE_PATH, "derivation": "verbatim-copy", "sha256": sha256_bytes(license_b),
                             "why": "recipients of the plugin must receive the license governing its own material"},
            BUNDLE_APACHE_TEXT: {"source": ROOT_APACHE_TEXT_PATH, "derivation": "verbatim-copy", "sha256": sha256_bytes(apache_b),
                                 "why": "Part B carries an Apache-2.0 work whose adapted expression ships in this payload; "
                                        "Apache-2.0 section 4(a) requires a copy of the License with any redistribution"},
            SCOPED_NOTICE: {"sources": [CANONICAL_NOTICE_PATH, ROOT_NOTICE_PATH],
                            "derivation": "composed: Part A = corpus notice verbatim; Part B = root-notice entries selected by "
                                          "the applicability markers, verbatim, + the root MIT text restricted to those works",
                            "sha256": sha256_bytes(notice_b),
                            "applicable_entries": meta["applicable_entries"],
                            "mit_entries": meta["mit_entries"], "apache_entries": meta["apache_entries"],
                            "why": "every third-party notice applicable to the files in this directory must travel with them"},
        },
    }
    return outputs, accounting


def build_manifest(corpus_sha, runtime_txt, support_txt, reach_txt, ext_txt, skill_shard_sha, recs, attribution):
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
        "attribution": attribution,
    }


def main():
    root = os.getcwd()
    recs, corpus_sha = load_canonical(root)
    runtime, support = classify(recs)
    reach = reachability(recs)
    runtime_txt = dumps(runtime); support_txt = dumps(support); reach_txt = dumps(reach)
    ext = build_local_extensions(root); ext_txt = dumps(ext)

    # legal bundle: byte-derived copies of every applicable legal source inside the plugin boundary
    legal_outputs, attribution = render_legal_bundle(root)
    for rel, data in legal_outputs.items():
        with open(os.path.join(root, rel), "wb") as fh: fh.write(data)

    # SKILL-LOCAL shards (documented supporting-file model): mirror each skill's shards under its own references/generated/
    all_shards = render_shards(runtime)
    per_skill = skill_shard_files(reach, runtime)
    all_rt = list(_all_runtime(runtime))
    rt_byid = {r["id"]: r for r in all_rt}
    cross = skill_cross_domain(reach, all_rt)  # per-skill cross-domain payload records (ids)
    def shard_text(skill, fn):
        if fn == "control-dependencies.md":
            return render_control_dependencies([rt_byid[i] for i in cross.get(skill, [])])
        return all_shards[fn]
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
            text = shard_text(skill, fn)
            with open(os.path.join(d, fn), "w", encoding="utf-8") as fh: fh.write(text)
            skill_shard_sha[f"skills/{skill}/references/generated/{fn}"] = sha256_bytes(text.encode())

    manifest = build_manifest(corpus_sha, runtime_txt, support_txt, reach_txt, ext_txt, skill_shard_sha, recs, attribution)
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
    for rel, data in legal_outputs.items(): print(f"  legal-bundle[{rel}] sha256={sha256_bytes(data)[:16]} bytes={len(data)}")
    print("attribution applicable root entries:", attribution["bundle"][SCOPED_NOTICE]["applicable_entries"])


if __name__ == "__main__":
    main()
