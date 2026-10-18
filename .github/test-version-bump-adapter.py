#!/usr/bin/env python3
"""Real-git integration tests for the version_bump_check.py ADAPTER.

Run locally or in CI (push AND pull_request):

    python3 .github/test-version-bump-adapter.py

Unlike .github/test-version-bump.py (which exercises ONLY the pure policy
core with synthetic data), these tests drive the full adapter end to end
against REAL disposable git repositories: tempfile.TemporaryDirectory +
`git init` + real commits/branches, invoking the actual checker as a
subprocess. The load-bearing git behavior (merge-base selection, `git diff
--name-status -z` path parsing, manifest object/path existence) is NEVER
mocked - that is exactly the surface under test.

Primary purpose: pin the standalone fail-closed contract restored by this
change - a plugin manifest that EXISTS but cannot be read as a JSON object
(malformed JSON, top-level non-object, unexpected blob-read failure) is
INVALID and must fail the checker directly, no longer collapsing into the
genuinely-MISSING state. The checker must make that true on its own, without
relying on .github/checks.py.

Controls (owner Wave-1B-1 section 12):
  A1  multi-commit branch: net delta (merge-base..head), not HEAD^..head
  A2  real `git diff --name-status -z` parsing: add + delete + spaced name
  A3  malformed HEAD manifest -> nonzero  (PRIMARY regression control)
  A4  base MISSING / head VALID           -> accepted new-pack behavior
  A5  base VALID  / head MISSING           -> no version-bump failure
  A6  unresolvable base ref                -> nonzero, no silent fallback
  A7  malformed BASE manifest              -> nonzero
  A8  top-level JSON not an object         -> nonzero (head, and base)
  A9  base VALID object, missing version   -> nonzero (base-side version parse fail)
  A10 base VALID object, malformed version -> nonzero (base-side version parse fail)

All helpers are local to this file (owner section 5: no shared helper module).
Standard library only. No network, no remote, no secrets (owner section 19).
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

CHECKER = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "version_bump_check.py")

# Hermetic git: ignore the developer's global/system config (identity,
# signing, hooks, default branch) so the tests are deterministic everywhere
# and never try to GPG-sign. Identity is supplied explicitly below.
ENV = dict(
    os.environ,
    GIT_CONFIG_GLOBAL=os.devnull,
    GIT_CONFIG_SYSTEM=os.devnull,
    GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",
    GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid",
)

PLUGIN_REL = ".claude-plugin/plugin.json"


# --- local helpers ---------------------------------------------------------

def git(repo, *args):
    """Run a git command in `repo`, raising on nonzero (setup must not fail)."""
    return subprocess.run(
        ["git", "-C", repo] + list(args),
        env=ENV, capture_output=True, text=True, check=True)


def write(repo, rel, content):
    """Write `content` to repo/rel, creating parent directories."""
    full = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def remove(repo, rel):
    """Delete repo/rel from the working tree (git add -A stages the removal)."""
    os.remove(os.path.join(repo, rel))


def plugin_manifest(pack, version, description="d"):
    """A valid plugin.json string for `pack` at `version`."""
    return json.dumps(
        {"name": pack, "version": version, "description": description}) + "\n"


def commit(repo, msg):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg)


def new_repo(stack):
    """Create a disposable repo on branch `main`; register it for cleanup."""
    tmp = tempfile.TemporaryDirectory(prefix="vbc-adapter-")
    stack.append(tmp)
    repo = tmp.name
    git(repo, "init", "-q", "-b", "main")
    return repo


def run_checker(repo, base, head):
    """Invoke the ACTUAL checker as a subprocess over base..head in `repo`."""
    return subprocess.run(
        ["python3", CHECKER, "--base", base, "--head", head],
        cwd=repo, env=ENV, capture_output=True, text=True)


# ===========================================================================

class AdapterIntegrationTests(unittest.TestCase):
    def setUp(self):
        # Each test owns its disposable repositories; cleaned up in tearDown.
        self._tmpdirs = []

    def tearDown(self):
        for t in self._tmpdirs:
            t.cleanup()

    def repo(self):
        return new_repo(self._tmpdirs)

    # -- A1: net delta over the true merge-base, not HEAD^ ------------------
    def test_A1_multi_commit_merge_base_net_delta(self):
        repo = self.repo()
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        write(repo, "ops-pack/skills/x/SKILL.md", "---\nname: x\ndescription: long enough description\n---\nA\n")
        commit(repo, "base")

        git(repo, "checkout", "-q", "-b", "feature")
        # commit 1: normative change WITH the bump (this commit alone is fine)
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.3"))
        write(repo, "ops-pack/skills/x/SKILL.md", "---\nname: x\ndescription: long enough description\n---\nB\n")
        commit(repo, "c1: normative + bump")
        # commit 2 (HEAD): another normative change, NO further bump
        write(repo, "ops-pack/skills/x/SKILL.md", "---\nname: x\ndescription: long enough description\n---\nC\n")
        commit(repo, "c2: normative, no bump")

        # Net delta merge-base(main,feature)..feature: 0.4.2 -> 0.4.3 advanced
        # across a normative change => PASS. A naive HEAD^..HEAD window (0.4.3
        # -> 0.4.3, normative) would FAIL; proving the checker uses the base's
        # merge-base, not HEAD^.
        net = run_checker(repo, "main", "feature")
        self.assertEqual(net.returncode, 0,
                         "net-delta over merge-base must PASS\n" + net.stdout + net.stderr)

        head_parent_window = run_checker(repo, "feature^", "feature")
        self.assertNotEqual(head_parent_window.returncode, 0,
                            "the HEAD^..HEAD window must FAIL, confirming the "
                            "scenario truly differs by base selection\n"
                            + head_parent_window.stdout)

    # -- A2: real -z name-status parsing (add + delete + spaced path) -------
    def test_A2_changed_path_parsing_add_delete_space(self):
        repo = self.repo()
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        write(repo, "ops-pack/skills/x/references/to-delete.md", "old\n")
        commit(repo, "base")

        git(repo, "checkout", "-q", "-b", "feature")
        remove(repo, "ops-pack/skills/x/references/to-delete.md")
        # A normative reference file whose name contains a space.
        write(repo, "ops-pack/skills/x/references/a b.md", "new\n")
        # version deliberately NOT advanced -> normative change must FAIL,
        # and the diagnostic must echo the exact paths the -z parse produced.
        commit(repo, "feature: delete + add (spaced)")

        r = run_checker(repo, "main", "feature")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("ops-pack/skills/x/references/a b.md", r.stdout,
                      "spaced path must survive -z parsing verbatim\n" + r.stdout)
        self.assertIn("ops-pack/skills/x/references/to-delete.md", r.stdout,
                      "deleted path must be parsed and classified\n" + r.stdout)

    # -- A3: malformed HEAD manifest (PRIMARY regression control) -----------
    def test_A3_malformed_head_manifest_fails_closed(self):
        repo = self.repo()
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        write(repo, "ops-pack/skills/x/SKILL.md", "---\nname: x\ndescription: long enough description\n---\nA\n")
        commit(repo, "base")

        git(repo, "checkout", "-q", "-b", "feature")
        write(repo, "ops-pack/" + PLUGIN_REL, "{ this is not valid json\n")
        write(repo, "ops-pack/skills/x/SKILL.md", "---\nname: x\ndescription: long enough description\n---\nB\n")
        commit(repo, "feature: malformed head manifest")

        r = run_checker(repo, "main", "feature")
        self.assertNotEqual(r.returncode, 0,
                            "malformed HEAD manifest must fail closed\n" + r.stdout)
        self.assertIn("head:", r.stdout, r.stdout)
        self.assertIn("ops-pack", r.stdout, r.stdout)
        self.assertIn("ops-pack/" + PLUGIN_REL, r.stdout, r.stdout)

    # -- A4: base MISSING / head VALID -> accepted new-pack behavior --------
    def test_A4_base_missing_head_valid_new_pack(self):
        repo = self.repo()
        # ops-pack present and unchanged both sides keeps the repo realistic.
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        commit(repo, "base: only ops-pack")

        git(repo, "checkout", "-q", "-b", "feature")
        # security-pack introduced new at head with a valid initial version
        # AND its own normative content.
        write(repo, "security-pack/" + PLUGIN_REL, plugin_manifest("security-pack", "0.1.0"))
        write(repo, "security-pack/skills/foo/SKILL.md", "---\nname: foo\ndescription: long enough description\n---\nnew\n")
        commit(repo, "feature: introduce security-pack")

        r = run_checker(repo, "main", "feature")
        self.assertEqual(r.returncode, 0,
                         "a newly-introduced pack with a valid version must "
                         "pass (no prior version to compare)\n" + r.stdout + r.stderr)

    # -- A5: base VALID / head MISSING -> no version-bump failure -----------
    def test_A5_base_valid_head_missing_no_bump_failure(self):
        repo = self.repo()
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        write(repo, "security-pack/" + PLUGIN_REL, plugin_manifest("security-pack", "0.1.0"))
        write(repo, "security-pack/skills/foo/SKILL.md", "---\nname: foo\ndescription: long enough description\n---\nx\n")
        commit(repo, "base: ops + security")

        git(repo, "checkout", "-q", "-b", "feature")
        remove(repo, "security-pack/" + PLUGIN_REL)
        remove(repo, "security-pack/skills/foo/SKILL.md")
        commit(repo, "feature: remove security-pack")

        r = run_checker(repo, "main", "feature")
        # This checker must NOT raise a version-bump failure for the removed
        # pack. (It does NOT assert repo-wide pack deletion is valid - that is
        # governed by consistency/metadata checks and owner migration policy.)
        self.assertEqual(r.returncode, 0,
                         "removing a pack must not be a version-bump failure\n"
                         + r.stdout + r.stderr)

    # -- A6: unresolvable base ref -> nonzero, no silent fallback -----------
    def test_A6_unresolvable_base_ref_fails_closed(self):
        repo = self.repo()
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        commit(repo, "base")
        git(repo, "checkout", "-q", "-b", "feature")
        write(repo, "ops-pack/README.md", "readme\n")
        commit(repo, "feature")

        r = run_checker(repo, "no-such-base-ref-xyz", "feature")
        self.assertNotEqual(r.returncode, 0,
                            "an unresolvable base ref must fail closed\n" + r.stdout)
        # No fallback to HEAD^/main/tag/empty-diff: it must not report success.
        self.assertNotIn("version-bump: OK", r.stdout,
                         "must not silently fall back to a success\n" + r.stdout)

    # -- A7: malformed BASE manifest -> nonzero -----------------------------
    def test_A7_malformed_base_manifest_fails_closed(self):
        repo = self.repo()
        write(repo, "ops-pack/" + PLUGIN_REL, "{ not valid json at base\n")
        write(repo, "ops-pack/skills/x/SKILL.md", "---\nname: x\ndescription: long enough description\n---\nA\n")
        commit(repo, "base: malformed manifest")

        git(repo, "checkout", "-q", "-b", "feature")
        # head is a perfectly valid manifest + version
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        commit(repo, "feature: valid manifest")

        r = run_checker(repo, "main", "feature")
        self.assertNotEqual(r.returncode, 0,
                            "malformed BASE manifest must fail closed\n" + r.stdout)
        self.assertIn("base:", r.stdout, r.stdout)
        self.assertIn("ops-pack/" + PLUGIN_REL, r.stdout, r.stdout)

    # -- A8: top-level JSON not an object (head, and base) ------------------
    def test_A8_top_level_not_object_fails_closed_head(self):
        repo = self.repo()
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        commit(repo, "base")
        git(repo, "checkout", "-q", "-b", "feature")
        # Syntactically valid JSON, but the top level is an array.
        write(repo, "ops-pack/" + PLUGIN_REL, "[1, 2, 3]\n")
        commit(repo, "feature: head manifest is a JSON array")

        r = run_checker(repo, "main", "feature")
        self.assertNotEqual(r.returncode, 0,
                            "top-level non-object HEAD manifest must fail closed\n" + r.stdout)
        self.assertIn("head:", r.stdout, r.stdout)

    def test_A8_top_level_not_object_fails_closed_base(self):
        repo = self.repo()
        # Syntactically valid JSON string at base; head is a valid object.
        write(repo, "ops-pack/" + PLUGIN_REL, '"just a string"\n')
        commit(repo, "base: manifest is a JSON string")
        git(repo, "checkout", "-q", "-b", "feature")
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        commit(repo, "feature: valid object")

        r = run_checker(repo, "main", "feature")
        self.assertNotEqual(r.returncode, 0,
                            "top-level non-object BASE manifest must fail closed\n" + r.stdout)
        self.assertIn("base:", r.stdout, r.stdout)

    # -- A9: base VALID object, missing version -> base-side parse fail -----
    def test_A9_base_valid_object_missing_version_fails_closed(self):
        repo = self.repo()
        # Base manifest is a VALID JSON object but has no "version" key. It must
        # NOT be collapsed into base-missing (new-pack) and pass: it is a base
        # pack whose version contract is unmet -> fail closed.
        write(repo, "ops-pack/" + PLUGIN_REL,
              json.dumps({"name": "ops-pack", "description": "d"}) + "\n")
        commit(repo, "base: valid object, no version field")

        git(repo, "checkout", "-q", "-b", "feature")
        # Head is otherwise valid.
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        commit(repo, "feature: valid manifest + version")

        r = run_checker(repo, "main", "feature")
        self.assertNotEqual(r.returncode, 0,
                            "a valid base object with no version must fail "
                            "closed, not read as a new pack\n" + r.stdout + r.stderr)
        self.assertIn("base:", r.stdout, r.stdout)
        self.assertIn("ops-pack", r.stdout, r.stdout)
        self.assertIn("cannot parse a simple MAJOR.MINOR.PATCH version", r.stdout,
                      "diagnostic must identify the base version parse failure\n"
                      + r.stdout)

    # -- A10: base VALID object, malformed version -> base-side parse fail --
    def test_A10_base_valid_object_malformed_version_fails_closed(self):
        repo = self.repo()
        # Base manifest is a VALID JSON object with a malformed version string.
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.x"))
        commit(repo, "base: valid object, malformed version")

        git(repo, "checkout", "-q", "-b", "feature")
        # Head is otherwise valid.
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        commit(repo, "feature: valid manifest + version")

        r = run_checker(repo, "main", "feature")
        self.assertNotEqual(r.returncode, 0,
                            "a valid base object with a malformed version must "
                            "fail closed\n" + r.stdout + r.stderr)
        self.assertIn("base:", r.stdout, r.stdout)
        self.assertIn("cannot parse a simple MAJOR.MINOR.PATCH version", r.stdout,
                      "diagnostic must identify the base version parse failure\n"
                      + r.stdout)


class AdapterEndToEndSanity(unittest.TestCase):
    """Two-sided anchor: the real adapter path yields PASS and FAIL verdicts
    on an ordinary valid-manifest normative change, mirroring the pure-core
    policy through real git (so a PASS here is not a vacuous always-green)."""

    def setUp(self):
        self._tmpdirs = []

    def tearDown(self):
        for t in self._tmpdirs:
            t.cleanup()

    def _repo_with_normative_change(self, head_version):
        repo = new_repo(self._tmpdirs)
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", "0.4.2"))
        write(repo, "ops-pack/skills/x/SKILL.md", "---\nname: x\ndescription: long enough description\n---\nA\n")
        commit(repo, "base")
        git(repo, "checkout", "-q", "-b", "feature")
        write(repo, "ops-pack/skills/x/SKILL.md", "---\nname: x\ndescription: long enough description\n---\nB\n")
        write(repo, "ops-pack/" + PLUGIN_REL, plugin_manifest("ops-pack", head_version))
        commit(repo, "feature: normative change")
        return repo

    def test_normative_change_with_bump_passes(self):
        repo = self._repo_with_normative_change("0.4.3")
        r = run_checker(repo, "main", "feature")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_normative_change_without_bump_fails(self):
        repo = self._repo_with_normative_change("0.4.2")
        r = run_checker(repo, "main", "feature")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("did not", r.stdout, r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
