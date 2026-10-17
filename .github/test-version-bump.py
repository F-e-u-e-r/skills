#!/usr/bin/env python3
"""Two-sided unit tests for the pure version-bump policy core.

Run locally or in CI (push AND pull_request):

    python3 .github/test-version-bump.py

These exercise ONLY the pure core of version_bump_check.py with synthetic
inputs - no git, no filesystem. They prove each owner-required control can both
PASS and FAIL, and pin the policy-boundary decisions (whitespace, comments,
frontmatter description, plugin.json version-only, provenance) so a later edit
cannot silently relax them.

The live history-dependent checker (git adapter) is not exercised here; it runs
against real PR net deltas in the dedicated pull_request CI job.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import version_bump_check as v


# --- synthetic-input helpers (keep tests declarative) ----------------------

def bh(base_over=None, head_over=None):
    """Build (base_versions, head_versions) dicts over the four packs.

    Packs not named default to present and EQUAL ('2.0.0' both sides) so they
    never trigger. A value of None marks the pack ABSENT at that revision.
    """
    base_over = base_over or {}
    head_over = head_over or {}
    base, head = {}, {}
    for p in v.PACKS:
        b = base_over.get(p, "2.0.0")
        h = head_over.get(p, "2.0.0")
        base[p] = v.parse_version(b) if b is not None else None
        head[p] = v.parse_version(h) if h is not None else None
    return base, head


def run(changes, base_over=None, head_over=None,
        base_plugins=None, head_plugins=None):
    """Classify + evaluate synthetic changes; return the violation list."""
    base, head = bh(base_over, head_over)
    violations, _detail = v.analyze(
        changes, base, head, base_plugins or {}, head_plugins or {})
    return violations


# ===========================================================================
# Pure helpers
# ===========================================================================

class TestParseVersion(unittest.TestCase):
    def test_simple_semver(self):
        self.assertEqual(v.parse_version("0.4.2"), (0, 4, 2))
        self.assertEqual(v.parse_version(" 1.0.0 "), (1, 0, 0))

    def test_rejects_non_semver(self):
        for bad in ("1.0", "1.0.0.0", "1.0.x", "v1.0.0", "", "1..0", None, 3):
            self.assertIsNone(v.parse_version(bad), bad)

    def test_tuple_ordering(self):
        self.assertTrue(v.parse_version("0.4.3") > v.parse_version("0.4.2"))
        self.assertTrue(v.parse_version("0.1.0") < v.parse_version("0.2.0"))


class TestClassifyPath(unittest.TestCase):
    def test_normative_paths(self):
        norm = [
            "ops-pack/skills/operational-rigor/SKILL.md",
            "ops-pack/skills/operational-rigor/references/anything.md",
            "ops-pack/skills/ground-truth-gates/template/run-all.sh",
            "ops-pack/skills/ground-truth-gates/template/golden/cases.jsonl",
            "planning-pack/skills/planning/SKILL.md",
            "planning-pack/skills/planning/references/x.md",
            "security-pack/skills/foo/SKILL.md",
            "design-pack/skills/ui-design-craft/SKILL.md",
            "design-pack/skills/ui-design-craft/references/color.md",
            "design-pack/normative-inventory.json",
            "design-pack/normative-classification.json",
            "design-pack/prose-mapping.json",
            "corpus/design-pack/public_records.json",
        ]
        for p in norm:
            pack, is_norm = v.classify_path(p)
            self.assertIsNotNone(pack, p)
            self.assertTrue(is_norm, "expected normative: " + p)

    def test_non_normative_paths(self):
        non = [
            "ops-pack/README.md",
            "ops-pack/skills/operational-rigor/references/provenance.md",
            "planning-pack/skills/planning/references/provenance.md",
            "ops-pack/.claude-plugin/plugin.json",            # field-aware elsewhere
            "design-pack/generated/manifest.json",
            "design-pack/generated/README.md",
            "design-pack/skills/ui-design-craft/references/generated/color.md",
            "design-pack/LICENSE",
            "design-pack/tools/project_corpus.py",
            "corpus/design-pack/THIRD_PARTY_NOTICES.md",
            "README.md",
            "README.zh-Hant.md",
            ".github/version_bump_check.py",
            ".github/workflows/checks.yml",
            "evidence/reviews/x.md",
            "research/design-pack/x.md",
            "metadata/routing-corpus.jsonl",
            "metadata/pack-topology.json",
            "hooks/some-hook.sh",
        ]
        for p in non:
            _pack, is_norm = v.classify_path(p)
            self.assertFalse(is_norm, "expected NON-normative: " + p)

    def test_corpus_source_owned_by_design(self):
        self.assertEqual(v.classify_path(v.DESIGN_CORPUS_SOURCE),
                         ("design-pack", True))


class TestPluginNormativeChange(unittest.TestCase):
    def test_version_only_is_not_normative(self):
        base = {"name": "ops-pack", "version": "0.4.2", "description": "d"}
        head = {"name": "ops-pack", "version": "0.4.3", "description": "d"}
        self.assertFalse(v.plugin_normative_change(base, head))

    def test_non_version_field_is_normative(self):
        base = {"name": "ops-pack", "version": "0.4.2", "description": "old"}
        head = {"name": "ops-pack", "version": "0.4.2", "description": "new"}
        self.assertTrue(v.plugin_normative_change(base, head))

    def test_added_or_removed_manifest_is_not_counted_here(self):
        obj = {"name": "x", "version": "0.1.0"}
        self.assertFalse(v.plugin_normative_change(None, obj))
        self.assertFalse(v.plugin_normative_change(obj, None))


class TestEvaluateReturnsAllViolations(unittest.TestCase):
    def test_collects_every_pack(self):
        base, head = bh(
            {"ops-pack": "1.0.0", "planning-pack": "1.0.0"},
            {"ops-pack": "1.0.0", "planning-pack": "0.9.0"})  # planning regressed
        res = v.evaluate_version_policy(
            {"ops-pack": True, "planning-pack": False}, base, head)
        # ops: normative no-advance; planning: regression -> two findings.
        self.assertEqual(len(res), 2)
        self.assertTrue(any("ops-pack" in r and "did not" in r for r in res))
        self.assertTrue(any("planning-pack" in r and "regressed" in r for r in res))


# ===========================================================================
# Required PASS controls (owner section 23)
# ===========================================================================

class TestPassControls(unittest.TestCase):
    def test_23_1_ops_normative_skill_change_with_advance(self):
        self.assertEqual([], run(
            [("ops-pack/skills/skill-vetting/SKILL.md", "M")],
            {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.3"}))

    def test_23_2_planning_normative_change_with_advance(self):
        self.assertEqual([], run(
            [("planning-pack/skills/planning/references/x.md", "M")],
            {"planning-pack": "0.1.1"}, {"planning-pack": "0.1.2"}))

    def test_23_3_two_packs_change_both_advance(self):
        self.assertEqual([], run(
            [("ops-pack/skills/a/SKILL.md", "M"),
             ("design-pack/skills/b/SKILL.md", "M")],
            {"ops-pack": "0.4.2", "design-pack": "0.2.0"},
            {"ops-pack": "0.5.0", "design-pack": "0.2.1"}))

    def test_23_4_provenance_only_no_bump(self):
        self.assertEqual([], run(
            [("ops-pack/skills/a/references/provenance.md", "M")],
            {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.2"}))

    def test_23_5_readme_only_no_bump(self):
        self.assertEqual([], run(
            [("ops-pack/README.md", "M"),
             ("README.md", "M"),
             ("README.zh-Hant.md", "M")],
            {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.2"}))

    def test_23_6_generated_design_projection_only_no_bump(self):
        self.assertEqual([], run(
            [("design-pack/generated/manifest.json", "M"),
             ("design-pack/generated/runtime.json", "M"),
             ("design-pack/skills/ui-design-craft/references/generated/color.md", "M")],
            {"design-pack": "0.2.0"}, {"design-pack": "0.2.0"}))

    def test_23_7_no_normative_change_versions_unchanged(self):
        self.assertEqual([], run([], None, None))

    def test_23_8_proactive_bump_no_normative_change(self):
        self.assertEqual([], run(
            [("ops-pack/README.md", "M")],
            {"ops-pack": "0.4.2"}, {"ops-pack": "0.5.0"}))

    def test_23_9_new_pack_with_valid_initial_version(self):
        # security-pack absent at base, present at head with a valid version,
        # even with its own normative content added.
        self.assertEqual([], run(
            [("security-pack/skills/foo/SKILL.md", "A")],
            {"security-pack": None}, {"security-pack": "0.1.0"}))


# ===========================================================================
# Required FAIL controls (owner section 24)
# ===========================================================================

class TestFailControls(unittest.TestCase):
    def test_24_1_ops_normative_skill_change_no_bump(self):
        res = run([("ops-pack/skills/skill-vetting/SKILL.md", "M")],
                  {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.2"})
        self.assertTrue(any("ops-pack" in r and "did not" in r for r in res), res)

    def test_24_2_frontmatter_description_change_no_bump(self):
        # A description-only edit still changes SKILL.md; atomic path treatment
        # catches it. (Owner decision B: description is normative.)
        res = run([("ops-pack/skills/security-architect/SKILL.md", "M")],
                  {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.2"})
        self.assertTrue(res)

    def test_24_3_normative_reference_change_no_bump(self):
        res = run([("ops-pack/skills/a/references/thing.md", "M")],
                  {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.2"})
        self.assertTrue(res)

    def test_24_4_skill_addition_no_bump(self):
        res = run([("planning-pack/skills/new-skill/SKILL.md", "A")],
                  {"planning-pack": "0.1.1"}, {"planning-pack": "0.1.1"})
        self.assertTrue(res)

    def test_24_5_skill_removal_no_bump(self):
        res = run([("planning-pack/skills/old-skill/SKILL.md", "D")],
                  {"planning-pack": "0.1.1"}, {"planning-pack": "0.1.1"})
        self.assertTrue(res)

    def test_24_6_two_packs_change_only_one_advances(self):
        res = run(
            [("ops-pack/skills/a/SKILL.md", "M"),
             ("design-pack/skills/b/SKILL.md", "M")],
            {"ops-pack": "0.4.2", "design-pack": "0.2.0"},
            {"ops-pack": "0.5.0", "design-pack": "0.2.0"})  # design did NOT advance
        self.assertEqual(len(res), 1, res)
        self.assertTrue("design-pack" in res[0] and "did not" in res[0])

    def test_24_7_version_decrease_without_normative_change(self):
        res = run([], {"planning-pack": "0.1.1"}, {"planning-pack": "0.1.0"})
        self.assertTrue(any("planning-pack" in r and "regressed" in r for r in res))

    def test_24_8_plugin_json_non_version_field_change_no_bump(self):
        base_pl = {"ops-pack": {"name": "ops-pack", "version": "0.4.2", "description": "old"}}
        head_pl = {"ops-pack": {"name": "ops-pack", "version": "0.4.2", "description": "new"}}
        res = run([("ops-pack/.claude-plugin/plugin.json", "M")],
                  {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.2"},
                  base_pl, head_pl)
        self.assertTrue(any("ops-pack" in r and "did not" in r for r in res), res)

    def test_24_9_ops_template_change_no_bump(self):
        res = run([("ops-pack/skills/ground-truth-gates/template/run-all.sh", "M")],
                  {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.2"})
        self.assertTrue(res)


# ===========================================================================
# Policy-boundary tests (owner section 25) - pin the owner's decisions
# ===========================================================================

class TestPolicyBoundaries(unittest.TestCase):
    def test_whitespace_only_normative_skill_fails_without_bump(self):
        # The classifier never inspects content, so a whitespace-only SKILL.md
        # edit is treated exactly like any other content change: FAIL.
        res = run([("ops-pack/skills/a/SKILL.md", "M")],
                  {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.2"})
        self.assertTrue(res, "whitespace-only normative change must not be exempt")

    def test_comment_only_ops_template_change_fails_without_bump(self):
        res = run([("ops-pack/skills/ground-truth-gates/template/sentinel/run.mjs", "M")],
                  {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.2"})
        self.assertTrue(res, "comment-only template change must not be exempt")

    def test_description_only_change_fails_without_bump(self):
        res = run([("design-pack/skills/motion-craft/SKILL.md", "M")],
                  {"design-pack": "0.2.0"}, {"design-pack": "0.2.0"})
        self.assertTrue(res, "frontmatter description change must not be exempt")

    def test_plugin_json_version_only_increase_passes(self):
        base_pl = {"ops-pack": {"name": "ops-pack", "version": "0.4.2", "description": "d"}}
        head_pl = {"ops-pack": {"name": "ops-pack", "version": "0.4.3", "description": "d"}}
        res = run([("ops-pack/.claude-plugin/plugin.json", "M")],
                  {"ops-pack": "0.4.2"}, {"ops-pack": "0.4.3"},
                  base_pl, head_pl)
        self.assertEqual([], res, "version-only plugin bump must be allowed")

    def test_provenance_only_change_passes(self):
        res = run([("planning-pack/skills/planning/references/provenance.md", "M")],
                  {"planning-pack": "0.1.1"}, {"planning-pack": "0.1.1"})
        self.assertEqual([], res, "provenance-only change must not require a bump")


if __name__ == "__main__":
    unittest.main(verbosity=2)
