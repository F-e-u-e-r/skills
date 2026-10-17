#!/usr/bin/env python3
"""Require a pack's version to advance when its normative shipped surface changes.

Run in CI on pull_request only (the live history check), or locally:

    python3 .github/version_bump_check.py                 # origin/main -> HEAD
    python3 .github/version_bump_check.py --base <ref> --head <ref>

INVARIANT (owner Wave-1A policy)
--------------------------------
Evaluated over the PR's NET DELTA: merge-base(base, head) .. head.

  1. If an existing pack's canonical normative shipped surface changes between
     the merge-base and head, that pack's version at head must be strictly
     greater than its version at the merge-base.
  2. An existing pack's version must never DECREASE relative to the merge-base,
     even when no normative surface changed.

This check deliberately does NOT enforce bump magnitude (PATCH vs MINOR vs
MAJOR) - owner review owns that. A proactive bump with no normative change is
allowed. It does NOT validate tags/releases and does NOT run evidence probes.

ARCHITECTURE
------------
Pure deterministic CORE + thin git/CI ADAPTER (owner-mandated split):

  * The pure core (classify_path, plugin_normative_change,
    evaluate_version_policy, analyze) takes DATA, never git state: no
    subprocess, no filesystem reads, fully unit-testable with synthetic inputs
    in .github/test-version-bump.py. It returns ALL detected violations, not
    merely the first.
  * The adapter (git_* helpers, main) reads base/head from git, builds the
    data, calls the core, prints actionable diagnostics, and exits nonzero on
    any violation.

NORMATIVE SURFACE (atomic path treatment; no whitespace/comment exemptions -
any content change to a classified-normative path counts, owner decision C):

  * <pack>/skills/**/SKILL.md                      (frontmatter included)
  * <pack>/skills/**/references/**                 except the exclusions below
  * ops-pack/skills/ground-truth-gates/template/** (shipped executable template)
  * design-pack/normative-inventory.json
  * design-pack/normative-classification.json
  * design-pack/prose-mapping.json
  * corpus/design-pack/public_records.json         (canonical corpus source the
                                                    production bridge projects)
  * <pack>/.claude-plugin/plugin.json              non-version field change only
                                                    (field-aware; a version-only
                                                    edit is NOT the cause)

EXPLICIT NON-NORMATIVE (never triggers a bump), even under a pack tree:

  * <pack>/README.md, repo README.md, README.zh-Hant.md
  * **/references/provenance.md                    (narrow provenance exemption)
  * design-pack/generated/**                       (derived; clean-regeneration
  * design-pack/skills/**/references/generated/**   checks own its integrity)
  * .github/**, evidence/**, research/**
  * any other path under a pack not matched above  (LICENSE, tools/, notices)

RESIDUAL (named in the PR body, out of scope for v1): shared metadata/** rows
cannot be mapped to a single owning pack without new policy machinery, so this
checker does not classify metadata/** as any pack's normative surface.

Fail direction: a pack present at head whose version cannot be parsed fails
CLOSED (reported, nonzero exit).
"""
import argparse
import json
import subprocess
import sys

# The four canonical packs. Each pack's version source of truth:
#   <pack>/.claude-plugin/plugin.json  ->  top-level "version"
PACKS = ("ops-pack", "planning-pack", "design-pack", "security-pack")

PLUGIN_REL = ".claude-plugin/plugin.json"

# Design's canonical corpus source lives OUTSIDE the pack tree but is Design's
# normative semantic authority (design-pack/tools/project_corpus.py projects it).
DESIGN_CORPUS_SOURCE = "corpus/design-pack/public_records.json"

# Design normative JSON sidecars at the pack root (not generated).
DESIGN_ROOT_NORMATIVE = (
    "normative-inventory.json",
    "normative-classification.json",
    "prose-mapping.json",
)


# ---------------------------------------------------------------------------
# PURE CORE  (data in, verdict out; no git, no filesystem, no subprocess)
# ---------------------------------------------------------------------------

def parse_version(text):
    """Parse a simple MAJOR.MINOR.PATCH string into an int tuple, else None.

    Pure. Returns None for anything that is not exactly three dot-separated
    non-negative integers so the adapter can fail closed on a malformed version.
    """
    if not isinstance(text, str):
        return None
    parts = text.strip().split(".")
    if len(parts) != 3:
        return None
    out = []
    for p in parts:
        if not p.isdigit():
            return None
        out.append(int(p))
    return tuple(out)


def fmt_version(v):
    """Format a parsed version tuple back to 'X.Y.Z' (or '<none>')."""
    if v is None:
        return "<none>"
    return ".".join(str(n) for n in v)


def pack_of(path):
    """Return the owning pack for a path, or None.

    Pure, string-only. A path's owner is its first segment when that is a pack;
    the Design corpus source is owned by design-pack despite living elsewhere.
    """
    if path == DESIGN_CORPUS_SOURCE:
        return "design-pack"
    seg = path.split("/", 1)[0]
    return seg if seg in PACKS else None


def classify_path(path):
    """Classify one changed path.

    Returns (owning_pack_or_None, is_normative_bool). Pure, string-only.

    plugin.json is reported as (pack, False) here: whether it is a normative
    change is decided field-aware by plugin_normative_change, not by its path.
    """
    pack = pack_of(path)
    if pack is None:
        return (None, False)

    # The Design corpus source (outside the pack tree) is normative.
    if path == DESIGN_CORPUS_SOURCE:
        return (pack, True)

    rel = path[len(pack) + 1:]  # path relative to the pack root

    # plugin.json: path channel never marks it normative (field-aware elsewhere).
    if rel == PLUGIN_REL:
        return (pack, False)

    # Pack README is non-normative.
    if rel == "README.md":
        return (pack, False)

    if rel.startswith("skills/"):
        # Exclusions first so they win over the references/** inclusion.
        if rel.endswith("/references/provenance.md"):
            return (pack, False)
        if "/references/generated/" in rel:
            return (pack, False)
        if rel.endswith("/SKILL.md"):
            return (pack, True)
        if "/references/" in rel:
            return (pack, True)
        # Ops ships an executable starter template; any change counts.
        if pack == "ops-pack" and rel.startswith("skills/ground-truth-gates/template/"):
            return (pack, True)
        # Any other file under skills/ is not a v1-classified normative surface
        # (none exist in the current tree).
        return (pack, False)

    # Design normative JSON sidecars at the pack root.
    if pack == "design-pack" and rel in DESIGN_ROOT_NORMATIVE:
        return (pack, True)

    # Design generated projection output is derived, not normative.
    if pack == "design-pack" and rel.startswith("generated/"):
        return (pack, False)

    # Everything else under a pack (LICENSE, tools/, notices, ...) is not a
    # v1-classified normative surface.
    return (pack, False)


def plugin_normative_change(base_obj, head_obj):
    """True iff a plugin.json changed in a NON-version field.

    Pure. Compares parsed manifests with the top-level 'version' removed, so a
    version-only bump never classifies itself as the normative cause that
    requires the bump. Add/remove of the manifest (one side None) is handled by
    the new/removed-pack path in evaluate_version_policy, not here.
    """
    if base_obj is None or head_obj is None:
        return False
    b = dict(base_obj)
    h = dict(head_obj)
    b.pop("version", None)
    h.pop("version", None)
    return b != h


def evaluate_version_policy(normative_changed, base_versions, head_versions):
    """Owner Wave-1A policy over grouped data. Pure; returns list[str].

    normative_changed: {pack: bool}
    base_versions / head_versions: {pack: version_tuple_or_None}
                                   (None means the pack is absent at that rev)

    Returns every violation, not just the first.
    """
    violations = []
    for pack in PACKS:
        base_v = base_versions.get(pack)
        head_v = head_versions.get(pack)
        changed = bool(normative_changed.get(pack, False))

        if head_v is None:
            # Pack absent at head (removed, or never existed): no version to
            # enforce. Pack removal is a larger structural change owner review
            # and other checks cover.
            continue
        if base_v is None:
            # New pack at head: no prior version to compare. The adapter has
            # already confirmed head_v parses as a valid simple semver.
            continue

        if head_v < base_v:
            # Monotonicity: fires regardless of normative change, and subsumes
            # the no-advance message for this pack.
            violations.append(
                "{pack}: version regressed (base {b}, head {h})".format(
                    pack=pack, b=fmt_version(base_v), h=fmt_version(head_v)))
            continue
        if changed and not (head_v > base_v):
            violations.append(
                "{pack}: normative shipped surface changed but version did not "
                "advance (base {b}, head {h})".format(
                    pack=pack, b=fmt_version(base_v), h=fmt_version(head_v)))
    return violations


def analyze(changes, base_versions, head_versions, base_plugins, head_plugins):
    """Pure orchestrator: classify changes, then apply the policy.

    changes:        iterable of (path, status) tuples (status unused for
                    classification; add/modify/delete all count for a
                    normative path).
    base_versions / head_versions: {pack: version_tuple_or_None}
    base_plugins / head_plugins:    {pack: parsed_plugin_json_or_None}

    Returns (violations, changed_normative_paths) where the second is
    {pack: [path, ...]} for diagnostics.
    """
    normative_changed = {p: False for p in PACKS}
    changed_norm_paths = {p: [] for p in PACKS}
    plugin_changed_packs = set()

    for path, _status in changes:
        if path.endswith("/" + PLUGIN_REL) or path == PLUGIN_REL:
            p = pack_of(path)
            if p in PACKS:
                plugin_changed_packs.add(p)
            continue
        pack, is_norm = classify_path(path)
        if pack and is_norm:
            normative_changed[pack] = True
            changed_norm_paths[pack].append(path)

    for pack in plugin_changed_packs:
        if plugin_normative_change(base_plugins.get(pack), head_plugins.get(pack)):
            normative_changed[pack] = True
            changed_norm_paths[pack].append(
                pack + "/" + PLUGIN_REL + " (non-version fields)")

    violations = evaluate_version_policy(
        normative_changed, base_versions, head_versions)
    return violations, changed_norm_paths


# ---------------------------------------------------------------------------
# GIT / CI ADAPTER  (the only place that touches git state)
# ---------------------------------------------------------------------------

def _git(args):
    """Run a git command, returning stdout (text). Raises on nonzero exit."""
    return subprocess.run(
        ["git"] + args,
        check=True, capture_output=True, text=True).stdout


def git_merge_base(base_ref, head_ref):
    """The actual merge-base (fork point) of base and head."""
    return _git(["merge-base", base_ref, head_ref]).strip()


def git_name_status(merge_base, head_ref):
    """Changed (path, status) pairs for merge_base..head.

    Rename detection is disabled (owner decision): a move reads as delete + add,
    which is the deterministic treatment a skill rename must trigger on.
    """
    out = _git([
        "diff", "--no-renames", "--name-status", "-z", merge_base, head_ref])
    toks = out.split("\0")
    changes = []
    i = 0
    while i < len(toks):
        status = toks[i]
        if status == "":
            i += 1
            continue
        if i + 1 >= len(toks):
            break
        path = toks[i + 1]
        changes.append((path, status[0]))
        i += 2
    return changes


def git_read_file(rev, path):
    """Return file contents at a revision, or None if it does not exist there."""
    r = subprocess.run(
        ["git", "show", "{rev}:{path}".format(rev=rev, path=path)],
        capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return r.stdout


def read_plugin(rev, pack):
    """Parse <pack>/.claude-plugin/plugin.json at rev. None if absent/unparseable."""
    raw = git_read_file(rev, pack + "/" + PLUGIN_REL)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Require pack version advance for normative changes "
                    "(evaluated over PR net delta: merge-base(base, head)..head).")
    ap.add_argument("--base", default="origin/main",
                    help="base ref (default: origin/main)")
    ap.add_argument("--head", default="HEAD",
                    help="head ref (default: HEAD)")
    args = ap.parse_args(argv)

    merge_base = git_merge_base(args.base, args.head)
    head_rev = _git(["rev-parse", args.head]).strip()

    changes = git_name_status(merge_base, args.head)

    base_plugins = {p: read_plugin(merge_base, p) for p in PACKS}
    head_plugins = {p: read_plugin(args.head, p) for p in PACKS}

    base_versions = {}
    head_versions = {}
    adapter_errors = []
    for p in PACKS:
        bp, hp = base_plugins[p], head_plugins[p]
        base_versions[p] = parse_version(bp.get("version")) if isinstance(bp, dict) else None
        head_versions[p] = parse_version(hp.get("version")) if isinstance(hp, dict) else None
        # A pack present at head whose version is missing/unparseable fails closed.
        if hp is not None and head_versions[p] is None:
            adapter_errors.append(
                "{pack}: cannot parse a simple MAJOR.MINOR.PATCH version at head "
                "({pack}/{rel})".format(pack=p, rel=PLUGIN_REL))

    violations, detail = analyze(
        changes, base_versions, head_versions, base_plugins, head_plugins)

    print("version-bump: base={base} head={head} merge-base={mb}".format(
        base=args.base, head=head_rev[:12], mb=merge_base[:12]))

    all_problems = list(violations) + list(adapter_errors)
    if not all_problems:
        touched = sorted(p for p in PACKS
                         if base_versions[p] != head_versions[p]
                         or detail[p])
        note = (" (pack surfaces/versions touched: " + ", ".join(touched) + ")"
                if touched else " (no pack normative surface changed)")
        print("version-bump: OK - every pack with a normative change advanced "
              "its version, and no version regressed" + note)
        return 0

    print("")
    print("Version-bump policy violations (base .. head net delta):")
    for v in violations:
        print("  - " + v)
        pack = v.split(":", 1)[0]
        for path in detail.get(pack, []):
            print("      changed normative path: " + path)
    for e in adapter_errors:
        print("  - " + e)
    print("")
    print("Fix: advance the offending pack's version in "
          "<pack>/.claude-plugin/plugin.json (bump magnitude is owner review's "
          "call), or revert the normative change. Provenance/derived/generated "
          "and development-only paths do not require a bump.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
