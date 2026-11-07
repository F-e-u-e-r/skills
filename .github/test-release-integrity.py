#!/usr/bin/env python3
"""Integration tests for release_integrity_check.py (RELEASE-INTEGRITY V1).

Standard library only. Real disposable git repositories (no mocking of
load-bearing git behavior). Remotes are plain local repository paths, so the
suite needs no network. Helpers are local to this file.

Covers R1-R14 from the implementation authorization plus anti-vacuity controls
and the CLI contract. Each load-bearing control is exercised two-sided (a
correct arm that PASSES and a broken arm that FAILS), so a vacuous pass is
visible. WorktreeContainment pins that the verifier's teardown removes only
the worktree the verifier itself created.
"""
import ast
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "release_integrity_check.py")
sys.path.insert(0, HERE)
import release_integrity_check as ri  # noqa: E402

# Fixture integrity checker committed INTO each disposable repo. It mirrors the
# real .github/checks.py contract: root is the parent of .github/, and it fails
# (exit 1) iff the committed tree carries a 'tree-is-bad.txt' marker. The
# production tool runs whichever checks.py the expected commit's tree contains;
# in the real repo that is the real checker (see the historical proofs).
FIXTURE_CHECKS = (
    "#!/usr/bin/env python3\n"
    "import os, sys\n"
    "root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
    "sys.exit(1 if os.path.exists(os.path.join(root, 'tree-is-bad.txt')) else 0)\n"
)

INJECT_SENTINEL = "RELINT_INJECTED"
# A VALID git tag name (no space) that, if any code path interpolated it into a
# shell, would create a sentinel file via command substitution + redirection.
HOSTILE_TAG = "v1.0$(>%s)" % INJECT_SENTINEL

# Fixture checker for WorktreeContainment: exits 0, but when the committed
# tree carries drop-own-pointer.txt it first deletes the `.git` pointer FILE
# of the worktree it runs in - the verifier's own. A missing pointer makes
# os.remove raise (exit 1), and os.remove never deletes a directory.
CONTAINMENT_CHECKS = (
    "#!/usr/bin/env python3\n"
    "import os, sys\n"
    "root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
    "if os.path.exists(os.path.join(root, 'drop-own-pointer.txt')):\n"
    "    os.remove(os.path.join(root, '.git'))\n"
    "sys.exit(0)\n"
)


def _write(path, content):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def _git(cwd, *args, check=True):
    cp = subprocess.run(
        ["git", "-c", "user.email=t@example.com", "-c", "user.name=test", *args],
        cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True,
    )
    if check and cp.returncode != 0:
        raise AssertionError("git %s failed (rc=%d): %s" % (args, cp.returncode, cp.stderr))
    return cp.stdout.strip()


class ReleaseIntegrityTests(unittest.TestCase):
    def _mkdtemp(self, prefix):
        d = tempfile.mkdtemp(prefix=prefix)
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        return d

    def _build_repo(self):
        """Disposable repo. main: c1(good) -> cbad(bad tree) -> c3(good);
        side branch cside(good) off c1 (NOT on main). Returns (repo, shas)."""
        repo = self._mkdtemp("relint-repo-")
        _git(repo, "init", "-q", "-b", "main")
        os.makedirs(os.path.join(repo, ".github"))
        _write(os.path.join(repo, ".github", "checks.py"), FIXTURE_CHECKS)
        _write(os.path.join(repo, "a.txt"), "a\n")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "c1")
        c1 = _git(repo, "rev-parse", "HEAD")

        _write(os.path.join(repo, "tree-is-bad.txt"), "boom\n")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "cbad")
        cbad = _git(repo, "rev-parse", "HEAD")

        os.remove(os.path.join(repo, "tree-is-bad.txt"))
        _write(os.path.join(repo, "c.txt"), "c\n")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "c3")
        c3 = _git(repo, "rev-parse", "HEAD")

        _git(repo, "checkout", "-q", "-b", "side", c1)
        _write(os.path.join(repo, "side.txt"), "s\n")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "cside")
        cside = _git(repo, "rev-parse", "HEAD")
        _git(repo, "checkout", "-q", "main")
        return repo, {"c1": c1, "cbad": cbad, "c3": c3, "cside": cside}

    def _clone(self, repo):
        """A local clone used purely as an ls-remote target (has every commit,
        no tags until a test creates them)."""
        remote = self._mkdtemp("relint-remote-")
        _git(None, "clone", "-q", repo, remote)
        return remote

    @staticmethod
    def _tag(where, name, sha, annotated=False):
        if annotated:
            _git(where, "tag", "-a", name, "-m", "msg", sha)
        else:
            _git(where, "tag", name, sha)

    # ---- R1-R4: resolution + ancestry (pre-tag) ---------------------------

    def test_r01_pre_tag_valid_expected_commit(self):
        repo, k = self._build_repo()
        sha, failures = ri.verify_pre_tag(k["c1"], "main", cwd=repo)
        self.assertEqual(sha, k["c1"])
        self.assertEqual(failures, [], "R1 expected PASS, got %s" % failures)

    def test_r02_historical_release_after_main_advances(self):
        repo, k = self._build_repo()
        # expected = release commit c1; main has advanced to c3 (M).
        self.assertNotEqual(k["c1"], k["c3"], "topology must have main ahead of expected")
        sha, failures = ri.verify_pre_tag(k["c1"], "main", cwd=repo)
        self.assertEqual(failures, [], "R2 ancestor-of-main must PASS despite inequality: %s" % failures)

    def test_r03_expected_commit_not_on_main(self):
        repo, k = self._build_repo()
        sha, failures = ri.verify_pre_tag(k["cside"], "main", cwd=repo)
        self.assertTrue(any(f.startswith("RI-2") for f in failures), failures)
        # cside tree is good, so the failure is specifically ancestry, not tree.
        self.assertFalse(any(f.startswith("RI-5") for f in failures), failures)

    def test_r04_unresolvable_expected_commit_no_fallback(self):
        repo, k = self._build_repo()
        bogus = "dead" * 10  # 40 hex, not an object in this repo
        sha, failures = ri.verify_pre_tag(bogus, "main", cwd=repo)
        self.assertIsNone(sha, "unresolvable expected must not silently fall back")
        self.assertTrue(any("expected-commit" in f for f in failures), failures)

    # ---- R5-R8: tag commit identity, lightweight and annotated ------------

    def test_r05_lightweight_tag_correct(self):
        repo, k = self._build_repo()
        remote = self._clone(repo)
        self._tag(repo, "rel", k["c1"])
        self._tag(remote, "rel", k["c1"])
        sha, failures = ri.verify_post_tag(k["c1"], "main", "rel", remote, cwd=repo)
        self.assertEqual(failures, [], "R5 expected PASS: %s" % failures)

    def test_r06_lightweight_tag_wrong_commit(self):
        repo, k = self._build_repo()
        remote = self._clone(repo)
        self._tag(repo, "rel", k["c3"])      # tag points elsewhere
        self._tag(remote, "rel", k["c3"])
        sha, failures = ri.verify_post_tag(k["c1"], "main", "rel", remote, cwd=repo)
        self.assertTrue(any(f.startswith("RI-8") for f in failures), failures)  # local
        self.assertTrue(any(f.startswith("RI-1") for f in failures), failures)  # remote

    def test_r07_annotated_tag_correct(self):
        repo, k = self._build_repo()
        remote = self._clone(repo)
        self._tag(repo, "arel", k["c1"], annotated=True)
        self._tag(remote, "arel", k["c1"], annotated=True)
        sha, failures = ri.verify_post_tag(k["c1"], "main", "arel", remote, cwd=repo)
        self.assertEqual(failures, [], "R7 annotated peel must PASS: %s" % failures)

    def test_r08_annotated_tag_wrong_commit(self):
        repo, k = self._build_repo()
        remote = self._clone(repo)
        self._tag(repo, "arel", k["c3"], annotated=True)
        self._tag(remote, "arel", k["c3"], annotated=True)
        sha, failures = ri.verify_post_tag(k["c1"], "main", "arel", remote, cwd=repo)
        self.assertTrue(any(f.startswith("RI-8") for f in failures), failures)
        self.assertTrue(any(f.startswith("RI-1") for f in failures), failures)

    # ---- R9-R11: tag presence / local vs remote --------------------------

    def test_r09_local_tag_absent(self):
        repo, k = self._build_repo()
        remote = self._clone(repo)
        self._tag(remote, "rel", k["c1"])   # remote correct; repo has NO local tag
        sha, failures = ri.verify_post_tag(k["c1"], "main", "rel", remote, cwd=repo)
        self.assertTrue(any(f.startswith("RI-8") for f in failures), failures)  # local absent
        self.assertFalse(any(f.startswith("RI-1") for f in failures), failures)  # remote fine

    def test_r10_remote_tag_absent(self):
        repo, k = self._build_repo()
        remote = self._clone(repo)
        self._tag(repo, "rel", k["c1"])     # local correct; remote has NO tag
        sha, failures = ri.verify_post_tag(k["c1"], "main", "rel", remote, cwd=repo)
        self.assertTrue(any(f.startswith("RI-1") for f in failures), failures)  # remote absent
        # anti-vacuity: remote identity is load-bearing and independent of local.
        self.assertFalse(any(f.startswith("RI-8") for f in failures), failures)

    def test_r11_remote_tag_differs(self):
        repo, k = self._build_repo()
        remote = self._clone(repo)
        self._tag(repo, "rel", k["c1"])     # local correct
        self._tag(remote, "rel", k["c3"])   # remote points elsewhere
        sha, failures = ri.verify_post_tag(k["c1"], "main", "rel", remote, cwd=repo)
        self.assertTrue(any(f.startswith("RI-1") for f in failures), failures)
        self.assertFalse(any(f.startswith("RI-8") for f in failures), failures)

    # ---- R12-R13: committed-tree validation + ambient independence --------

    def test_r12_committed_tree_check_failure(self):
        repo, k = self._build_repo()
        # cbad is an ANCESTOR of main (so ancestry passes) but its tree is bad.
        sha, failures = ri.verify_pre_tag(k["cbad"], "main", cwd=repo)
        self.assertTrue(any(f.startswith("RI-5") for f in failures), failures)
        self.assertFalse(any(f.startswith("RI-2") for f in failures), failures)

    def test_r13_dirty_ambient_tree_independence(self):
        repo, k = self._build_repo()
        # Dirty the AMBIENT working tree so a direct checks.py read would fail.
        _write(os.path.join(repo, "tree-is-bad.txt"), "ambient dirt\n")
        # Verifying the clean committed commit c1 must PASS regardless (RI-4).
        sha, failures = ri.verify_pre_tag(k["c1"], "main", cwd=repo)
        self.assertEqual(failures, [], "R13 must depend only on committed tree: %s" % failures)
        # anti-vacuity control: the delegated checker IS live - a bad committed
        # tree still fails in the very same dirtied repo.
        _, ctrl = ri.verify_pre_tag(k["cbad"], "main", cwd=repo)
        self.assertTrue(any(f.startswith("RI-5") for f in ctrl), ctrl)

    # ---- R14: argument / tag-name safety ---------------------------------

    def test_r14_hostile_tag_name_argv_safety(self):
        repo, k = self._build_repo()
        remote = self._clone(repo)
        self._tag(repo, HOSTILE_TAG, k["c1"])
        self._tag(remote, HOSTILE_TAG, k["c1"])
        cwd_before = os.getcwd()
        sha, failures = ri.verify_post_tag(k["c1"], "main", HOSTILE_TAG, remote, cwd=repo)
        self.assertEqual(failures, [], "R14 hostile-but-valid tag must resolve correctly: %s" % failures)
        # No shell interpolation anywhere: the injection sentinel never appears.
        for base in (repo, remote, cwd_before, os.getcwd()):
            self.assertFalse(
                os.path.exists(os.path.join(base, INJECT_SENTINEL)),
                "shell injection created sentinel in %s" % base,
            )

    # ---- anti-vacuity: ancestry is ancestor-of, not equality -------------

    def test_av_ancestry_not_equality(self):
        repo, k = self._build_repo()
        # Ancestor-of is directional and not equality: this is exactly what
        # makes R2 pass. An equality rule would reject c1 (c1 != c3).
        self.assertTrue(ri.is_ancestor(k["c1"], k["c3"], cwd=repo))
        self.assertFalse(ri.is_ancestor(k["c3"], k["c1"], cwd=repo))
        self.assertNotEqual(k["c1"], k["c3"])

    # ---- CLI contract: explicit phase/commit, deterministic exit codes ----

    def _cli(self, repo, *args):
        return subprocess.run(
            [sys.executable, SCRIPT, *args],
            cwd=repo, stdin=subprocess.DEVNULL, capture_output=True, text=True,
        )

    def test_cli_exit_codes_pass_and_fail(self):
        repo, k = self._build_repo()
        ok = self._cli(repo, "pre-tag", "--expected-commit", k["c1"], "--main-ref", "main")
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        self.assertIn("RELEASE-INTEGRITY: PASS (pre-tag)", ok.stdout)
        bad = self._cli(repo, "pre-tag", "--expected-commit", k["cside"], "--main-ref", "main")
        self.assertEqual(bad.returncode, 1, bad.stdout + bad.stderr)
        self.assertIn("RELEASE-INTEGRITY: FAIL (pre-tag)", bad.stdout)

    def test_cli_requires_explicit_phase_and_commit(self):
        repo, k = self._build_repo()
        no_phase = self._cli(repo)
        self.assertEqual(no_phase.returncode, 2, "phase must be explicit")
        no_commit = self._cli(repo, "pre-tag", "--main-ref", "main")
        self.assertEqual(no_commit.returncode, 2, "expected-commit must be explicit")


class WorktreeContainment(unittest.TestCase):
    """The verifier may clean up only the worktree it created.

    Its teardown ended with a bare `git worktree prune`. The worktree registry
    is shared by every linked worktree of a repository, so each run also
    deleted the admin entry - HEAD, index, reflog - of any OTHER worktree whose
    directory or `.git` pointer was missing. Real disposable repositories and
    real git: unrelated worktrees are put in exactly the states a prune
    deletes, git confirms it WOULD delete them, then the real verifier runs."""

    def setUp(self):
        base = os.path.realpath(tempfile.mkdtemp(prefix="relint-containment-"))
        self.addCleanup(shutil.rmtree, base, ignore_errors=True)
        # The verifier's own mkdtemp goes through a symlinked temp root, so the
        # path it holds is not the string git registers (the macOS
        # /var -> /private/var shape, reproduced on every OS).
        self.tmp_real = os.path.join(base, "tmp-real")
        os.mkdir(self.tmp_real)
        link = os.path.join(base, "tmp-link")
        os.symlink(self.tmp_real, link)
        self.addCleanup(setattr, tempfile, "tempdir", tempfile.tempdir)
        tempfile.tempdir = link
        self.base = base
        self.repo = os.path.join(base, "repo")
        os.mkdir(self.repo)
        _git(self.repo, "init", "-q", "-b", "main")
        os.makedirs(os.path.join(self.repo, ".github"))
        _write(os.path.join(self.repo, ".github", "checks.py"), CONTAINMENT_CHECKS)
        _write(os.path.join(self.repo, "a.txt"), "a\n")
        self.c_ok = self._commit("ok")
        _write(os.path.join(self.repo, "drop-own-pointer.txt"), "x\n")
        self.c_drop = self._commit("checker damages its own worktree")
        # NOT the verifier's: two in the states a bare prune deletes, one healthy.
        self.unrelated = {n: self._register(os.path.join(base, n))
                          for n in ("dir-gone", "pointer-gone", "healthy")}
        shutil.rmtree(os.path.join(base, "dir-gone"))
        os.remove(os.path.join(base, "pointer-gone", ".git"))
        # PREMISE, or "it survived" proves nothing: git itself rates both
        # damaged entries prunable and the healthy one not. Dry run, and only
        # inside this disposable repository.
        dry = subprocess.run(["git", "worktree", "prune", "--dry-run", "--verbose"],
                             cwd=self.repo, stdin=subprocess.DEVNULL,
                             capture_output=True, text=True)
        said = dry.stdout + dry.stderr
        for name, admin in self.unrelated.items():
            self.assertEqual(name != "healthy",
                             "worktrees/%s:" % os.path.basename(admin) in said,
                             "fixture premise (%s): %s" % (name, said))
        self.before = self._registry()

    def _commit(self, msg):
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-q", "-m", msg)
        return _git(self.repo, "rev-parse", "HEAD")

    def _register(self, path):
        """`git worktree add` -> the admin entry that backs `path`."""
        _git(self.repo, "worktree", "add", "-q", "--detach", path, self.c_ok)
        with open(os.path.join(path, ".git"), encoding="utf-8") as fh:
            gitdir = fh.read().split(":", 1)[1].strip()
        return os.path.normpath(os.path.join(path, gitdir))

    def _registry(self):
        """Every admin entry -> {file: sha256 of its bytes}."""
        top = os.path.join(self.repo, ".git", "worktrees")
        out = {}
        for entry in sorted(os.listdir(top)) if os.path.isdir(top) else ():
            files = {}
            for root, _dirs, names in os.walk(os.path.join(top, entry)):
                for name in names:
                    with open(os.path.join(root, name), "rb") as fh:
                        rel = os.path.relpath(os.path.join(root, name), os.path.join(top, entry))
                        files[rel] = hashlib.sha256(fh.read()).hexdigest()
            out[entry] = files
        return out

    def test_a_unrelated_prunable_worktrees_survive_the_verifier(self):
        _sha, failures = ri.verify_pre_tag(self.c_ok, "main", cwd=self.repo)
        self.assertEqual([], failures, "the verdict must still be PASS")
        self.assertEqual(self.before, self._registry(),
                         "every pre-existing admin entry (index, HEAD, reflog) "
                         "must survive byte-identical, and none of the "
                         "verifier's may remain")
        self.assertEqual([], os.listdir(self.tmp_real),
                         "the verifier's temp directory must be gone")

    def test_b_damaged_owned_worktree_is_still_removed(self):
        """What the prune did for the verifier itself: a worktree whose own
        `.git` pointer is gone cannot be removed by one scoped remove, and
        would leak its entry. At c_drop the checker deletes that pointer."""
        probe = os.path.join(self.base, "probe")
        probe_admin = self._register(probe)
        os.remove(os.path.join(probe, ".git"))
        plain = subprocess.run(["git", "worktree", "remove", "--force", probe],
                               cwd=self.repo, stdin=subprocess.DEVNULL,
                               capture_output=True, text=True)
        self.assertNotEqual(0, plain.returncode, "premise: one scoped remove must fail")
        self.assertTrue(os.path.isdir(probe_admin), "premise: and leave its entry behind")
        shutil.rmtree(probe)
        _git(self.repo, "worktree", "remove", "--force", probe)
        self.assertEqual(self.before, self._registry(), "premise probe must leave no trace")

        _sha, failures = ri.verify_pre_tag(self.c_drop, "main", cwd=self.repo)
        self.assertEqual([], failures,
                         "the checker removed its own pointer and passed")
        self.assertEqual(self.before, self._registry(),
                         "the verifier's damaged entry must not leak, and every "
                         "unrelated entry must survive byte-identical")
        self.assertEqual([], os.listdir(self.tmp_real),
                         "the verifier's temp directory must be gone")

    def test_c_no_registry_wide_git_command_in_module(self):
        """Structural tripwire for the current shape (A and B are the
        behavioural protection): every git-worktree argv in the module, read
        from its syntax tree, is `worktree add --quiet --detach` in
        check_committed_tree or `worktree remove --force` (one force) in
        _cleanup_worktree; no prune, gc or maintenance literal anywhere."""
        with open(SCRIPT, encoding="utf-8") as fh:
            tree = ast.parse(fh.read())
        parent = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parent[child] = node

        def owner(node):
            while node in parent:
                node = parent[node]
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return node.name
            return "<module>"

        found = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and node.value in ("prune", "gc", "maintenance"):
                found.add((node.value, owner(node)))
            if isinstance(node, (ast.List, ast.Tuple)):
                words = tuple(e.value for e in node.elts if isinstance(e, ast.Constant))
                if "worktree" in words:
                    found.add((words[words.index("worktree"):], owner(node)))
        self.assertEqual({(("worktree", "add", "--quiet", "--detach"), "check_committed_tree"),
                          (("worktree", "remove", "--force"), "_cleanup_worktree")}, found)


if __name__ == "__main__":
    unittest.main(verbosity=2)
