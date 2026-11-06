#!/usr/bin/env python3
"""Bounded, portable wait on AUTHORITATIVE hosted CI state - a development tool,
not a hook (nothing registers it; run it by hand or from a background task).

Why it exists (2026-11-04): background CI waits were composed as

    timeout 1200 gh pr checks N --watch > out 2>&1; echo "WATCH_EXIT=$?" >> out; tail -8 out

which fails twice. `timeout` is GNU coreutils and absent on stock macOS, so the
watch died at once with 127; and a background task surfaces its LAST command's
status, so `tail` (or a trailing `echo`) reported "exit code 0" while the
side-channel file said 127. Dropping `timeout` to "fix" it removed the deadline.
Three occurrences are recorded (two on 2026-08-28, one on 2026-11-03).

This tool owns the whole lifecycle instead: its own monotonic deadline (no
timeout(1) dependency), one bounded `gh ... --json` query per poll (the query is
killed with its process group at min(query deadline, time left)), a verdict read
ONLY from the hosted JSON state - never from gh's exit code alone, never from
polling plumbing - and its own presentation (a per-poll line, the final check
table, a final status line) printed BEFORE it exits with the verdict.

Usage - make it the ONLY or LAST command of the background task:

    python3 hooks/bounded_wait.py pr-checks 294 --sha "$(git rev-parse HEAD)" --repo F-e-u-e-r/skills > out 2>&1
    python3 hooks/bounded_wait.py run 41723048498 --repo F-e-u-e-r/skills --deadline 1200

pr-checks REQUIRES --sha, the PR head commit whose checks you are waiting for:
right after a push the PR can still list the previous head's (green) checks,
so every poll first confirms the PR head IS that commit and treats any other
head as pending - a stale green is never read as this commit's green.

Appending `; tail out` or `; echo ...` after it re-creates the exact mask above:
the shell, not this tool, decides what a compound command reports. Read `out`
after the completion notification instead; its last line is the verdict.

Exit status (the authoritative result):
  0    SUCCESS  hosted terminal success: >= 1 check passed and none failed,
                was cancelled or is pending (run: completed + success)
  1    FAILURE  hosted terminal non-success: a check failed or was cancelled,
                every check was skipped, or the run concluded anything but success
  124  TIMEOUT  the deadline passed while the state was pending, or before any
                check was even reported - pending is never confirmed green
  125  ERROR    the watcher could not establish the state: gh missing, a query
                that failed, hung or printed unparseable/unknown state, or a gh
                exit status that contradicts its own JSON. Never success.
  2    usage error
Final stdout line: BOUNDED_WAIT status=<S> exit=<n> target=<T> elapsed=<s>s polls=<k> detail=<d>

Does NOT guarantee: anything about checks that register after a terminal verdict
(a late workflow); that the PR head did not move between its head query and its
checks query within one poll; that a cancelled watcher kills an in-flight gh
query (it is in its own session). A watcher crash prints an ERROR line and exits
125, never 1. Python 3.8+, stdlib only.
"""
import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time

EXIT_SUCCESS, EXIT_FAILURE, EXIT_TIMEOUT, EXIT_ERROR = 0, 1, 124, 125
CHECK_BUCKETS = {"pass", "fail", "pending", "skipping", "cancel"}
RUN_PENDING = {"queued", "in_progress", "waiting", "pending", "requested"}
RUN_NON_SUCCESS = {"failure", "cancelled", "timed_out", "action_required",
                   "startup_failure", "stale", "neutral", "skipped"}


class Query:
    """Outcome of one bounded subprocess call."""
    def __init__(self, rc=None, out="", err="", hung=False, deadline_cut=False, missing=False):
        self.rc, self.out, self.err = rc, out, err
        self.hung, self.deadline_cut, self.missing = hung, deadline_cut, missing


def run_query(argv, limit, deadline_cut):
    """Run argv with stdin closed, at most `limit` seconds. `deadline_cut` records
    whether the limit is the overall deadline (-> TIMEOUT) or the per-query cap
    (-> ERROR), so the two are never conflated."""
    try:
        proc = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, start_new_session=True)
    except OSError as exc:  # not found, not executable, exec format error, ...
        return Query(missing=True, err="%s: %s" % (type(exc).__name__, exc))
    try:
        out, err = proc.communicate(timeout=max(limit, 0.0))
        return Query(rc=proc.returncode, out=out.decode("utf-8", "replace"),
                     err=err.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (AttributeError, OSError):
            proc.kill()
        try:
            proc.communicate(timeout=1.0)
        except subprocess.TimeoutExpired:
            # a descendant that left the process group still holds the pipes:
            # stop reading, or the deadline is only as good as its lifetime
            for stream in (proc.stdout, proc.stderr):
                try:
                    stream.close()
                except OSError:
                    pass
            try:
                proc.wait(timeout=1.0)
            except subprocess.TimeoutExpired:
                pass
        return Query(hung=True, deadline_cut=deadline_cut)


def _tail(text, n=3):
    lines = [l for l in (text or "").strip().splitlines() if l.strip()]
    return " / ".join(lines[-n:])[:300]


def classify_checks(q):
    """-> (state, detail, table) for `gh pr checks --json bucket,name,state,...`."""
    if q.rc == 1 and not q.out.strip() and "no checks reported" in q.err:
        return "PENDING", "no checks reported yet", []
    if q.rc not in (0, 1, 8):
        return "ERROR", "gh exited %s: %s" % (q.rc, _tail(q.err) or "(no stderr)"), []
    try:
        data = json.loads(q.out)
    except ValueError:
        return "ERROR", "unparseable gh output (rc=%s): %s" % (q.rc, _tail(q.out or q.err)), []
    if not isinstance(data, list) or not all(isinstance(c, dict) for c in data):
        return "ERROR", "unexpected JSON shape (want a list of checks)", []
    table = ["%-8s %s" % (c.get("bucket"), c.get("name")) for c in data]
    if not data:
        state, detail = "PENDING", "no checks reported yet"
    else:
        buckets = [c.get("bucket") for c in data]
        unknown = sorted({str(b) for b in buckets if b not in CHECK_BUCKETS})
        if unknown:
            return "ERROR", "unknown check bucket(s): %s" % ", ".join(unknown), table
        bad = [c.get("name") for c in data if c.get("bucket") in ("fail", "cancel")]
        pending = sum(1 for b in buckets if b == "pending")
        passed = sum(1 for b in buckets if b == "pass")
        if bad:
            state, detail = "FAILURE", "failed/cancelled: %s" % ", ".join(map(str, bad))
        elif pending:
            state, detail = "PENDING", "%d of %d checks pending" % (pending, len(buckets))
        elif passed:
            state, detail = "SUCCESS", "%d passed, %d skipped" % (passed, len(buckets) - passed)
        else:
            state, detail = "FAILURE", "no check passed (all %d skipped)" % len(buckets)
    # gh's own exit status may only AGREE with the JSON; a contradiction means
    # we are not reading what we think we are reading
    if (q.rc == 8 and state != "PENDING") or (q.rc == 1 and state == "SUCCESS"):
        return "ERROR", "gh exit %s contradicts JSON state %s" % (q.rc, state), table
    return state, detail, table


def classify_head(q, sha):
    """-> (state, detail) for `gh pr view --json headRefOid`: is the PR head the
    commit we are waiting for? Any other head is pending, never an answer."""
    if q.rc != 0:
        return "ERROR", "gh pr view exited %s: %s" % (q.rc, _tail(q.err) or "(no stderr)")
    try:
        head = json.loads(q.out).get("headRefOid")
    except (ValueError, AttributeError):
        return "ERROR", "unparseable gh pr view output: %s" % _tail(q.out)
    if not isinstance(head, str) or not head:
        return "ERROR", "gh pr view returned no headRefOid"
    if head.lower().startswith(sha.lower()):
        return "MATCH", head
    return "PENDING", "PR head is %s, waiting for %s" % (head[:12], sha[:12])


def classify_run(q, sha=None):
    """-> (state, detail, table) for `gh run view --json status,conclusion,...`."""
    if q.rc != 0:
        return "ERROR", "gh exited %s: %s" % (q.rc, _tail(q.err) or "(no stderr)"), []
    try:
        data = json.loads(q.out)
    except ValueError:
        return "ERROR", "unparseable gh output: %s" % _tail(q.out), []
    if not isinstance(data, dict):
        return "ERROR", "unexpected JSON shape (want an object)", []
    status, conclusion = data.get("status"), data.get("conclusion")
    table = ["status=%s conclusion=%s %s" % (status, conclusion, data.get("url") or "")]
    if sha and not str(data.get("headSha") or "").lower().startswith(sha.lower()):
        return "ERROR", "run is for %s, not %s" % (str(data.get("headSha"))[:12], sha[:12]), table
    if status == "completed":
        if conclusion == "success":
            return "SUCCESS", "run concluded success", table
        if conclusion in RUN_NON_SUCCESS:
            return "FAILURE", "run concluded %s" % conclusion, table
        return "ERROR", "completed run with unknown conclusion %r" % (conclusion,), table
    if status in RUN_PENDING:
        return "PENDING", "run %s" % status, table
    return "ERROR", "unknown run status %r" % (status,), table


def build(args):
    repo = ["-R", args.repo] if args.repo else []
    if args.mode == "pr-checks":
        argv = [args.gh, "pr", "checks"] + repo + [args.target, "--json", "bucket,name,state,link,workflow"]
        head = [args.gh, "pr", "view"] + repo + [args.target, "--json", "headRefOid"]
        return argv, classify_checks, head
    argv = [args.gh, "run", "view"] + repo + [args.target, "--json", "status,conclusion,name,url,headSha"]
    return argv, (lambda q: classify_run(q, args.sha)), None


def watch(args, out=sys.stdout):
    argv, classify, head_argv = build(args)
    target = "%s %s%s" % (args.mode, args.target, (" -R " + args.repo) if args.repo else "")
    start = time.monotonic()
    deadline_at = start + args.deadline
    polls, last, table = 0, "no poll completed", []

    def finish(status, code, detail):
        for row in table:
            print("  " + row, file=out)
        print("BOUNDED_WAIT status=%s exit=%d target=%s elapsed=%.1fs polls=%d detail=%s"
              % (status, code, target, time.monotonic() - start, polls, detail), file=out)
        out.flush()
        return code

    while True:
        left = deadline_at - time.monotonic()
        if left <= 0:
            return finish("TIMEOUT", EXIT_TIMEOUT, "deadline %.0fs passed; last state: %s" % (args.deadline, last))
        polls += 1
        state = None
        if head_argv is not None:
            q = run_query(head_argv, min(args.query_timeout, left), left <= args.query_timeout)
            bad = _query_failure(q, args, last)
            if bad:
                return finish(*bad)
            state, detail = classify_head(q, args.sha)
            if state == "MATCH":
                state = None
            left = deadline_at - time.monotonic()
            if left <= 0 and state is None:
                return finish("TIMEOUT", EXIT_TIMEOUT, "deadline passed before the checks query; last state: %s" % last)
        if state is None:
            q = run_query(argv, min(args.query_timeout, left), left <= args.query_timeout)
            bad = _query_failure(q, args, last)
            if bad:
                return finish(*bad)
            state, detail, rows = classify(q)
            table = rows or table
        print("poll %d: %s - %s" % (polls, state, detail), file=out)
        out.flush()
        if state == "SUCCESS":
            return finish("SUCCESS", EXIT_SUCCESS, detail)
        if state == "FAILURE":
            return finish("FAILURE", EXIT_FAILURE, detail)
        if state == "ERROR":
            return finish("ERROR", EXIT_ERROR, detail)
        last = detail
        # the loop-top check is the deadline gate; a query started past it would
        # get a zero limit and be killed before it could report
        time.sleep(max(0.0, min(args.interval, deadline_at - time.monotonic())))


def _query_failure(q, args, last):
    if q.missing:
        return "ERROR", EXIT_ERROR, "cannot execute %r (%s)" % (args.gh, q.err)
    if q.hung:
        if q.deadline_cut:
            return "TIMEOUT", EXIT_TIMEOUT, "deadline passed during a query; last state: %s" % last
        return "ERROR", EXIT_ERROR, "query exceeded %.0fs query timeout" % args.query_timeout
    return None


def _sha(text):
    if not re.match(r"^[0-9a-fA-F]{7,40}$", text or ""):
        raise argparse.ArgumentTypeError("must be a 7-40 character hex commit id")
    return text


def _positive(text):
    v = float(text)
    if not v > 0 or v != v or v == float("inf"):
        raise argparse.ArgumentTypeError("must be a finite number > 0")
    return v


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("mode", choices=("pr-checks", "run"))
    ap.add_argument("target", help="PR number/URL/branch (pr-checks) or run id (run)")
    ap.add_argument("--repo", "-R", help="OWNER/REPO (default: gh's current repo)")
    ap.add_argument("--deadline", type=_positive, default=1200.0, help="seconds (default 1200; no unbounded mode)")
    ap.add_argument("--interval", type=_positive, default=20.0, help="seconds between polls (default 20)")
    ap.add_argument("--query-timeout", type=_positive, default=60.0, help="seconds per gh query (default 60)")
    ap.add_argument("--gh", default="gh", help="gh executable (default: gh on PATH)")
    ap.add_argument("--sha", type=_sha, help="commit the checks must belong to (required for pr-checks)")
    args = ap.parse_args(argv)
    if args.mode == "pr-checks" and not args.sha:
        ap.error("pr-checks needs --sha <PR head commit>: right after a push the PR can still "
                 "list the previous head's checks")
    try:
        return watch(args)
    except Exception as exc:  # a watcher crash must never read as hosted FAILURE (1)
        print("BOUNDED_WAIT status=ERROR exit=%d target=%s %s elapsed=? polls=? detail=watcher crashed: %s: %s"
              % (EXIT_ERROR, args.mode, args.target, type(exc).__name__, exc))
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
