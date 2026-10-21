#!/usr/bin/env python3
"""Deterministic release-integrity verifier (Wave 1B-2, RELEASE-INTEGRITY V1).

Binds four facts at release time, in two explicit phases:

    pre-tag   expected commit  <->  canonical-main ancestry  <->  committed-tree integrity
    post-tag  all of pre-tag    +   local tag identity       <->  remote tag identity

Usage:
    python3 .github/release_integrity_check.py pre-tag \
        --expected-commit <sha> [--main-ref origin/main]
    python3 .github/release_integrity_check.py post-tag \
        --expected-commit <sha> --tag <tag> [--main-ref origin/main] [--remote origin]

This is a release-time VERIFIER, not a release orchestrator. It creates no
tags, no GitHub Releases, no pack releases, no release notes, and no version
bumps, and it makes no GitHub API calls. Every git operation is read-only
except for one isolated, self-cleaning temporary detached worktree used to
validate the exact committed tree.

Threat core bound here:
    RI-1  wrong tag commit (remote tag identity)
    RI-2  expected release commit not on canonical-main ancestry
    RI-3  moving-main / TOCTOU (the main ref is resolved once to a pinned SHA)
    RI-4  dirty / ambient working-tree contamination (isolated committed tree)
    RI-5  pack / repository projections inconsistent at the release commit
    RI-8  expected tag resolves to the wrong commit (local tag identity)

The exact committed tree is validated by delegating to the repository's own
.github/checks.py (pack projection / README parity / marketplace consistency
already live there), executed INSIDE the isolated worktree at the expected
commit. This tool never reimplements those rules and never runs them against
the ambient checkout.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

_HEX = set("0123456789abcdef")


class IntegrityError(Exception):
    """A load-bearing release-integrity resolution failed (fail-closed)."""


def _noop(_msg):
    pass


def _git(args, cwd=None):
    """Run a git command via argv (never a shell). Returns CompletedProcess."""
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
    )


def _is_sha(value):
    return len(value) == 40 and all(c in _HEX for c in value)


def resolve_commit(ref, cwd=None):
    """Resolve ref to a full 40-hex commit SHA, peeling tags; fail closed.

    `rev-parse --verify <ref>^{commit}` resolves an explicit commit, peels a
    tag to its commit, and exits nonzero on a missing ref, a non-commit object,
    or an ambiguous short name. There is deliberately NO fallback to HEAD,
    origin/main, the latest tag, or the latest release.
    """
    cp = _git(["rev-parse", "--verify", "--end-of-options", "%s^{commit}" % ref], cwd=cwd)
    sha = cp.stdout.strip()
    if cp.returncode != 0 or not _is_sha(sha):
        raise IntegrityError("could not resolve %r to a commit object" % ref)
    return sha


def is_ancestor(ancestor_sha, descendant_sha, cwd=None):
    """True iff ancestor_sha is an ancestor of descendant_sha; errors fail closed.

    Equivalent to `git merge-base --is-ancestor`: exit 0 ancestor, exit 1 not,
    any other exit is an error (never read as a pass).
    """
    cp = _git(["merge-base", "--is-ancestor", ancestor_sha, descendant_sha], cwd=cwd)
    if cp.returncode == 0:
        return True
    if cp.returncode == 1:
        return False
    raise IntegrityError(
        "ancestry check errored (rc=%d): %s" % (cp.returncode, cp.stderr.strip())
    )


def local_tag_commit(tag, cwd=None):
    """Commit a LOCAL tag resolves to, peeling annotated tags; fail closed.

    `refs/tags/<tag>^{commit}` peels an annotated tag object to its commit and
    resolves a lightweight tag directly, so the raw annotated-tag-object SHA is
    never compared to a commit. Fully qualifying under refs/tags/ keeps a
    like-named branch from being resolved instead.
    """
    cp = _git(
        ["rev-parse", "--verify", "--end-of-options", "refs/tags/%s^{commit}" % tag],
        cwd=cwd,
    )
    sha = cp.stdout.strip()
    if cp.returncode != 0 or not _is_sha(sha):
        raise IntegrityError("local tag %r not found or not a commit" % tag)
    return sha


def remote_tag_commit(remote, tag, cwd=None):
    """Commit a REMOTE tag resolves to, via git-only `ls-remote` (no GitHub API).

    Handles both tag forms by preferring the peeled `refs/tags/<tag>^{}` line
    (annotated tag -> commit) over the bare `refs/tags/<tag>` line (lightweight
    tag -> commit, or an annotated tag OBJECT which must never be compared).
    Only exact ref names are accepted, so a fuzzy ls-remote match cannot leak
    in. Absent, ambiguous, or a command failure all fail closed.
    """
    cp = _git(["ls-remote", "--tags", "--", remote, tag, "%s^{}" % tag], cwd=cwd)
    if cp.returncode != 0:
        raise IntegrityError(
            "ls-remote failed for tag %r on %r (rc=%d)" % (tag, remote, cp.returncode)
        )
    exact_bare = "refs/tags/%s" % tag
    exact_peeled = "refs/tags/%s^{}" % tag
    bare, peeled = set(), set()
    for line in cp.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        sha, ref = parts[0].strip(), parts[1].strip()
        if not _is_sha(sha):
            continue
        if ref == exact_peeled:
            peeled.add(sha)
        elif ref == exact_bare:
            bare.add(sha)
    if peeled:
        if len(peeled) != 1:
            raise IntegrityError("ambiguous remote peeled tag %r on %r" % (tag, remote))
        return next(iter(peeled))
    if bare:
        if len(bare) != 1:
            raise IntegrityError("ambiguous remote tag %r on %r" % (tag, remote))
        return next(iter(bare))
    raise IntegrityError("remote tag %r not found on %r" % (tag, remote))


def _cleanup_worktree(path, cwd):
    """Best-effort teardown of a temporary worktree (on success OR failure)."""
    try:
        _git(["worktree", "remove", "--force", path], cwd=cwd)
    except Exception:
        pass
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    try:
        _git(["worktree", "prune"], cwd=cwd)
    except Exception:
        pass


def check_committed_tree(expected_sha, cwd=None):
    """Validate the EXACT committed tree at expected_sha, isolated from ambient.

    A fresh detached worktree is created at the expected commit OUTSIDE the
    ambient checkout, the repository's own .github/checks.py is executed inside
    it, exit 0 is required, and the worktree is removed. Ambient (possibly
    dirty) working-tree files cannot influence the result (pins RI-4).

    Returns (ok: bool, output: str). Setup failures fail closed via
    IntegrityError.
    """
    worktree = tempfile.mkdtemp(prefix="relint-tree-")
    try:
        add = _git(["worktree", "add", "--quiet", "--detach", worktree, expected_sha], cwd=cwd)
        if add.returncode != 0:
            raise IntegrityError(
                "could not create isolated worktree at %s: %s"
                % (expected_sha, add.stderr.strip())
            )
        checks = os.path.join(worktree, ".github", "checks.py")
        if not os.path.isfile(checks):
            raise IntegrityError(
                "committed tree %s has no .github/checks.py to delegate to" % expected_sha
            )
        proc = subprocess.run(
            [sys.executable, checks],
            cwd=worktree,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
        )
        return proc.returncode == 0, proc.stdout + proc.stderr
    finally:
        _cleanup_worktree(worktree, cwd)


def _pre_tag_invariants(expected, main_ref, cwd, log, failures):
    """Shared pre-tag core. Returns expected_sha, or None if it is unresolvable
    (a hard prerequisite for every later check)."""
    try:
        expected_sha = resolve_commit(expected, cwd=cwd)
    except IntegrityError as exc:
        failures.append("expected-commit: %s" % exc)
        return None
    log("expected-commit verified: %s" % expected_sha)

    # RI-2: expected must be an ancestor of canonical main (NOT equality).
    try:
        main_sha = resolve_commit(main_ref, cwd=cwd)
        log("main-ref %s resolved: %s" % (main_ref, main_sha))
        if is_ancestor(expected_sha, main_sha, cwd=cwd):
            log("ok    RI-2  expected is an ancestor of %s" % main_ref)
        else:
            failures.append(
                "RI-2  expected %s is NOT an ancestor of %s (%s)"
                % (expected_sha, main_ref, main_sha)
            )
    except IntegrityError as exc:
        failures.append("RI-2  ancestry: %s" % exc)

    # RI-5: the exact committed tree passes the repo's own integrity checks.
    try:
        ok_tree, output = check_committed_tree(expected_sha, cwd=cwd)
        if ok_tree:
            log("ok    RI-5  committed-tree integrity (.github/checks.py) at %s" % expected_sha[:12])
        else:
            failures.append(
                "RI-5  committed-tree integrity: .github/checks.py failed at %s" % expected_sha
            )
            log("---- delegated .github/checks.py output ----")
            log(output.rstrip())
            log("--------------------------------------------")
    except IntegrityError as exc:
        failures.append("RI-5  committed-tree integrity: %s" % exc)

    return expected_sha


def verify_pre_tag(expected, main_ref="origin/main", cwd=None, log=_noop):
    """pre-tag phase: expected commit, canonical-main ancestry, committed tree.

    No tag existence is required or inspected and no GitHub Release metadata is
    read. Returns (expected_sha_or_None, failures)."""
    log("mode: pre-tag")
    failures = []
    expected_sha = _pre_tag_invariants(expected, main_ref, cwd, log, failures)
    return expected_sha, failures


def verify_post_tag(expected, main_ref="origin/main", tag=None, remote="origin",
                    cwd=None, log=_noop):
    """post-tag phase: every pre-tag invariant plus local and remote tag identity.

    The tool does NOT create or push the tag; it only verifies that an
    already-created tag resolves (by commit peeling) to the expected commit
    both locally and on the remote. Returns (expected_sha_or_None, failures)."""
    log("mode: post-tag")
    failures = []
    expected_sha = _pre_tag_invariants(expected, main_ref, cwd, log, failures)
    if expected_sha is None:
        return None, failures  # unresolvable expected: tag identity is meaningless

    # RI-8: local tag commit identity (peeled) equals expected.
    try:
        local_sha = local_tag_commit(tag, cwd=cwd)
        if local_sha == expected_sha:
            log("ok    RI-8  local tag %r == expected (%s)" % (tag, local_sha[:12]))
        else:
            failures.append(
                "RI-8  local tag %r resolves to %s, expected %s" % (tag, local_sha, expected_sha)
            )
    except IntegrityError as exc:
        failures.append("RI-8  local tag: %s" % exc)

    # RI-1: remote tag commit identity (peeled) equals expected.
    try:
        remote_sha = remote_tag_commit(remote, tag, cwd=cwd)
        if remote_sha == expected_sha:
            log("ok    RI-1  remote tag %r on %r == expected (%s)" % (tag, remote, remote_sha[:12]))
        else:
            failures.append(
                "RI-1  remote tag %r on %r resolves to %s, expected %s"
                % (tag, remote, remote_sha, expected_sha)
            )
    except IntegrityError as exc:
        failures.append("RI-1  remote tag: %s" % exc)

    return expected_sha, failures


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="release_integrity_check.py",
        description="Deterministic release-time integrity verifier (pre-tag / post-tag).",
    )
    sub = ap.add_subparsers(dest="phase", required=True)

    pre = sub.add_parser("pre-tag", help="expected commit + canonical-main ancestry + committed tree")
    pre.add_argument("--expected-commit", required=True,
                     help="explicit release commit (load-bearing; no implicit default)")
    pre.add_argument("--main-ref", default="origin/main",
                     help="canonical main ref expected must be an ancestor of (default origin/main)")

    post = sub.add_parser("post-tag", help="pre-tag invariants + local/remote tag identity")
    post.add_argument("--expected-commit", required=True,
                      help="explicit release commit (load-bearing; no implicit default)")
    post.add_argument("--tag", required=True, help="release tag to verify (no inference)")
    post.add_argument("--main-ref", default="origin/main")
    post.add_argument("--remote", default="origin")

    args = ap.parse_args(argv)

    if args.phase == "pre-tag":
        _, failures = verify_pre_tag(args.expected_commit, args.main_ref, log=print)
    else:
        _, failures = verify_post_tag(
            args.expected_commit, args.main_ref, args.tag, args.remote, log=print
        )

    print()
    if failures:
        for item in failures:
            print("FAIL  [%s] %s" % (args.phase, item))
        print("RELEASE-INTEGRITY: FAIL (%s) - %d invariant(s) failed" % (args.phase, len(failures)))
        return 1
    print("RELEASE-INTEGRITY: PASS (%s)" % args.phase)
    return 0


if __name__ == "__main__":
    sys.exit(main())
