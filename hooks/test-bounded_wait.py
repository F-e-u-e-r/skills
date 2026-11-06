#!/usr/bin/env python3
"""Regression suite for bounded_wait.py (W1-W8 of the 2026-11-04 hardening).

Every case runs the REAL tool as a subprocess against a fake `gh` that replays a
scripted sequence of hosted states and checks the argv it was given. Assertions
read only the tool's own exit status and stdout. No network, no real gh.
"""
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.realpath(__file__))
TOOL = os.path.join(HERE, "bounded_wait.py")
PY = sys.executable

SHA = "c548c3dd21da8169a90da8ad882bda9dc9d8e7a5"
OLD_SHA = "53b817b0000000000000000000000000000000aa"

FAKE_GH = r'''#!%(py)s
import json, os, sys, time
d = os.environ["FAKE_GH_DIR"]
with open(os.path.join(d, "argv.log"), "a") as f:
    f.write(json.dumps(sys.argv[1:]) + "\n")
with open(os.path.join(d, "pid.log"), "a") as f:
    f.write(str(os.getpid()) + "\n")
script = json.load(open(os.path.join(d, "script.json")))
key = " ".join(sys.argv[1:3])  # "pr view" / "pr checks" / "run view"
if isinstance(script, list):  # a bare list scripts the main query; the PR head matches
    script = {"pr view": [{"out": json.dumps({"headRefOid": "%(sha)s"})}], "pr checks": script, "run view": script}
seq = script[key]
n_path = os.path.join(d, "n-" + key.replace(" ", "-"))
n = int(open(n_path).read()) if os.path.exists(n_path) else 0
open(n_path, "w").write(str(n + 1))
step = seq[min(n, len(seq) - 1)]  # the last step repeats forever
if step.get("descendant"):
    if os.fork() == 0:
        os.setsid()  # escapes the watcher's process-group kill, keeps the pipes
        time.sleep(step["descendant"])
        os._exit(0)
time.sleep(step.get("sleep", 0))
sys.stdout.write(step.get("out", ""))
sys.stderr.write(step.get("err", ""))
sys.exit(step.get("rc", 0))
'''

PASS_ = {"bucket": "pass", "name": "consistency", "state": "SUCCESS"}
PEND = {"bucket": "pending", "name": "hook-suites", "state": "IN_PROGRESS"}
FAIL = {"bucket": "fail", "name": "hook-suites", "state": "FAILURE"}
CANC = {"bucket": "cancel", "name": "hook-suites", "state": "CANCELLED"}
SKIP = {"bucket": "skipping", "name": "docs", "state": "SKIPPED"}


def checks(*cs, rc=0):
    return {"out": json.dumps(list(cs)), "rc": rc}


def run(status, conclusion=""):
    return {"out": json.dumps({"status": status, "conclusion": conclusion, "url": "https://example.invalid/r"}), "rc": 0}


class Env:
    def __init__(self, root, script):
        self.dir = tempfile.mkdtemp(dir=root)
        json.dump(script, open(os.path.join(self.dir, "script.json"), "w"))
        self.gh = os.path.join(self.dir, "gh")
        with open(self.gh, "w") as f:
            f.write(FAKE_GH % {"py": PY, "sha": SHA})
        os.chmod(self.gh, os.stat(self.gh).st_mode | stat.S_IXUSR)
        # a PATH holding no timeout/gtimeout at all (W3): the tool and the fake gh
        # are reached by absolute path; only `tail` is linked, for the W4 control
        self.path = os.path.join(self.dir, "bin")
        os.makedirs(self.path)
        os.symlink(shutil.which("tail"), os.path.join(self.path, "tail"))

    def tool(self, mode, target, *extra, shell=None, suffix="", sha=SHA):
        args = [PY, TOOL, mode, target, "--repo", "o/r", "--gh", self.gh,
                "--interval", "0.05", "--query-timeout", "5"] + list(extra)
        if mode == "pr-checks" and sha:
            args += ["--sha", sha]
        env = {"PATH": self.path, "FAKE_GH_DIR": self.dir, "HOME": self.dir}
        t0 = time.monotonic()
        try:
            if shell:
                out = os.path.join(self.dir, "out.txt")
                line = " ".join("'%s'" % a for a in args) + " > '%s' 2>&1" % out + suffix
                p = subprocess.run([shell, "-c", line], capture_output=True, text=True, env=env, timeout=20)
                text = open(out).read()
            else:
                p = subprocess.run(args, capture_output=True, text=True, env=env, timeout=20)
                text = p.stdout
        except subprocess.TimeoutExpired:
            return "HANG", "(tool did not finish within 20s)", time.monotonic() - t0
        return p.returncode, text, time.monotonic() - t0

    def argv_log(self):
        return [json.loads(l) for l in open(os.path.join(self.dir, "argv.log"))]

    def pids(self):
        return [int(l) for l in open(os.path.join(self.dir, "pid.log"))]


FAILS = []


def check(name, cond, info=""):
    print(("ok   " if cond else "FAIL ") + name + ("" if cond else "  <- " + info))
    if not cond:
        FAILS.append(name)


def final(text):
    lines = [l for l in text.strip().splitlines() if l.startswith("BOUNDED_WAIT ")]
    return lines[-1] if lines else ""


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    # a zombie still answers kill(0); ask ps for a live state
    st = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True).stdout.strip()
    return bool(st) and not st.startswith("Z")


def main():
    root = tempfile.mkdtemp(prefix="bounded-wait-test-")
    try:
        # W1 normal success: pending, pending, then all pass
        e = Env(root, [checks(PEND, rc=8), checks(PASS_, PEND, rc=8), checks(PASS_, SKIP)])
        rc, out, _ = e.tool("pr-checks", "294")
        check("W1 pr-checks reaches SUCCESS -> exit 0", rc == 0 and "status=SUCCESS exit=0" in final(out) and "polls=3" in final(out), out)
        check("W1 head query precedes the checks query, real gh shapes",
              e.argv_log()[0] == ["pr", "view", "-R", "o/r", "294", "--json", "headRefOid"]
              and e.argv_log()[1] == ["pr", "checks", "-R", "o/r", "294", "--json", "bucket,name,state,link,workflow"], str(e.argv_log()[:2]))
        e = Env(root, [run("in_progress"), run("completed", "success")])
        rc, out, _ = e.tool("run", "41723048498")
        check("W1 run reaches success -> exit 0", rc == 0 and "status=SUCCESS" in final(out), out)
        check("W1 run argv shape", e.argv_log()[0][:5] == ["run", "view", "-R", "o/r", "41723048498"], str(e.argv_log()[0]))

        # W2 bounded deadline: never terminal
        e = Env(root, [checks(PEND, rc=8)])
        rc, out, dt = e.tool("pr-checks", "294", "--deadline", "1")
        check("W2 pending forever -> TIMEOUT 124", rc == 124 and "status=TIMEOUT exit=124" in final(out), out)
        check("W2 completes within the deadline + slack", dt < 6, "elapsed %.1fs" % dt)
        # W2b a hung query is cut at the overall deadline -> TIMEOUT, process group killed
        e = Env(root, [{"sleep": 60, "out": "[]"}])
        rc, out, dt = e.tool("pr-checks", "294", "--deadline", "1")
        check("W2b hung query at deadline -> TIMEOUT 124", rc == 124 and "deadline passed during a query" in final(out), out)
        check("W2b bounded despite a 60s hang", dt < 6, "elapsed %.1fs" % dt)
        time.sleep(0.2)
        check("W2b hung gh was killed (no orphan)", not any(alive(p) for p in e.pids()), str(e.pids()))
        # W2c a hung query under the per-query cap (deadline not reached) -> ERROR
        e = Env(root, [{"sleep": 60, "out": "[]"}])
        rc, out, dt = e.tool("pr-checks", "294", "--deadline", "30", "--query-timeout", "0.5")
        check("W2c query hang under per-query cap -> ERROR 125", rc == 125 and "query timeout" in final(out), out)
        check("W2c bounded by the query cap", dt < 6, "elapsed %.1fs" % dt)

        # W3 no timeout(1) anywhere on PATH: same behavior
        e = Env(root, [checks(PEND, rc=8)])
        ctl = os.path.join(e.dir, "ctl")
        os.makedirs(ctl)
        with open(os.path.join(ctl, "timeout"), "w") as f:
            f.write("#!/bin/sh\nexit 0\n")
        os.chmod(os.path.join(ctl, "timeout"), 0o755)
        check("W3 probe: no timeout/gtimeout on the test PATH",
              shutil.which("timeout", path=e.path) is None and shutil.which("gtimeout", path=e.path) is None)
        check("W3 positive control: the same probe finds a planted timeout", shutil.which("timeout", path=ctl) is not None)
        rc, out, dt = e.tool("pr-checks", "294", "--deadline", "1")
        check("W3 deadline still enforced without timeout(1)", rc == 124 and dt < 6, "rc=%s %.1fs" % (rc, dt))

        # W4 the watcher presents its own failure and still exits with it; as the
        # last command of a shell line the shell surfaces the watcher's status
        e = Env(root, [checks(PASS_, FAIL, rc=1)])
        rc, out, _ = e.tool("pr-checks", "294")
        check("W4 failure printed (table + verdict) and exit 1",
              rc == 1 and "fail     hook-suites" in out and "status=FAILURE exit=1" in final(out), out)
        for sh in ("/bin/zsh", "/bin/bash"):
            if not os.path.exists(sh):
                print("skip W4 composition under %s (absent)" % sh)
                continue
            e = Env(root, [checks(PASS_, FAIL, rc=1)])
            rc, out, _ = e.tool("pr-checks", "294", shell=sh)
            check("W4 %s: watcher-last background line surfaces exit 1" % os.path.basename(sh),
                  rc == 1 and "status=FAILURE" in final(out), "rc=%s" % rc)
            e = Env(root, [checks(PASS_, FAIL, rc=1)])
            rc, out, _ = e.tool("pr-checks", "294", shell=sh, suffix="; tail -n 3 '%s'" % os.path.join(e.dir, "out.txt"))
            check("W4 %s control: appending tail masks it (why the usage rule exists)" % os.path.basename(sh),
                  rc == 0 and "status=FAILURE" in out, "rc=%s" % rc)

        # W5 pending hosted state beyond the deadline is never green
        for label, step in (("rc8 pending", checks(PEND, rc=8)),
                            ("no checks reported yet", {"rc": 1, "err": "no checks reported on the 'x' branch\n"}),
                            ("empty list rc0", checks())):
            e = Env(root, [step])
            rc, out, _ = e.tool("pr-checks", "294", "--deadline", "0.6")
            check("W5 %s -> TIMEOUT, not success" % label, rc == 124 and "status=TIMEOUT" in final(out), out)
        e = Env(root, [run("queued")])
        rc, out, _ = e.tool("run", "1", "--deadline", "0.6")
        check("W5 run queued forever -> TIMEOUT", rc == 124, out)

        # W6 success only because the hosted state is SUCCESS: gh exiting 0 with a
        # pending table must not end the wait
        e = Env(root, [checks(PEND, rc=0)])
        rc, out, _ = e.tool("pr-checks", "294", "--deadline", "0.6")
        check("W6 gh rc0 + pending JSON -> keeps waiting (TIMEOUT)", rc == 124, out)
        e = Env(root, [checks(PEND, rc=8), checks(PASS_)])
        rc, out, _ = e.tool("pr-checks", "294")
        check("W6 eventual hosted success -> exit 0 citing the hosted state", rc == 0 and "1 passed" in final(out), out)

        # W7 hosted failure -> failure
        for label, script, mode in (("fail bucket", [checks(FAIL, rc=1)], "pr-checks"),
                                    ("fail bucket, gh rc0", [checks(PASS_, FAIL, rc=0)], "pr-checks"),
                                    ("cancel bucket", [checks(CANC, rc=1)], "pr-checks"),
                                    ("all skipped", [checks(SKIP)], "pr-checks"),
                                    ("run failure", [run("completed", "failure")], "run"),
                                    ("run cancelled", [run("completed", "cancelled")], "run"),
                                    ("run timed_out", [run("completed", "timed_out")], "run"),
                                    ("run neutral", [run("completed", "neutral")], "run")):
            e = Env(root, script)
            rc, out, _ = e.tool(mode, "294")
            check("W7 %s -> FAILURE 1" % label, rc == 1 and "status=FAILURE" in final(out), out)

        # W8 watcher-internal failure -> explicit ERROR, never success
        for label, script, mode in (("auth error rc4", [{"rc": 4, "err": "gh auth login required"}], "pr-checks"),
                                    ("garbage output", [{"rc": 0, "out": "<html>oops"}], "pr-checks"),
                                    ("unknown bucket", [checks({"bucket": "weird", "name": "x"})], "pr-checks"),
                                    ("non-list JSON", [{"rc": 0, "out": "{}"}], "pr-checks"),
                                    ("rc1 contradicts all-pass", [checks(PASS_, rc=1)], "pr-checks"),
                                    ("rc8 contradicts all-pass", [checks(PASS_, rc=8)], "pr-checks"),
                                    ("run 404", [{"rc": 1, "err": "failed to get run: HTTP 404: Not Found"}], "run"),
                                    ("run unknown status", [run("exploded")], "run"),
                                    ("run unknown conclusion", [run("completed", "mystery")], "run")):
            e = Env(root, script)
            rc, out, _ = e.tool(mode, "294")
            check("W8 %s -> ERROR 125" % label, rc == 125 and "status=ERROR exit=125" in final(out), out)
        e = Env(root, [checks(PASS_)])
        e.gh = os.path.join(e.dir, "no-such-gh")
        rc, out, _ = e.tool("pr-checks", "1", "--deadline", "2")
        check("W8 gh missing -> ERROR 125 (not pending)", rc == 125 and "cannot execute" in final(out), "rc=%s %s" % (rc, out))

        # W9 the checks must belong to the commit waited for (stale head after a push)
        e = Env(root, {"pr view": [{"out": json.dumps({"headRefOid": OLD_SHA})}] * 2 + [{"out": json.dumps({"headRefOid": SHA})}],
                       "pr checks": [checks(PASS_)]})
        rc, out, _ = e.tool("pr-checks", "294")
        n_checks = sum(1 for a in e.argv_log() if a[:2] == ["pr", "checks"])
        check("W9a stale head's green is not trusted; success after the head moves", rc == 0 and "polls=3" in final(out) and n_checks == 1, "rc=%s checks-queries=%d %s" % (rc, n_checks, final(out)))
        e = Env(root, {"pr view": [{"out": json.dumps({"headRefOid": OLD_SHA})}], "pr checks": [checks(PASS_)]})
        rc, out, _ = e.tool("pr-checks", "294", "--deadline", "0.6")
        check("W9b head never reaches the commit -> TIMEOUT, never green", rc == 124 and "waiting for" in final(out), out)
        e = Env(root, [checks(PASS_)])
        rc, out, _ = e.tool("pr-checks", "294", sha=None)
        check("W9c pr-checks without --sha is a usage error", rc == 2, "rc=%s" % rc)
        e = Env(root, {"pr view": [{"rc": 1, "err": "GraphQL: Could not resolve to a PullRequest"}], "pr checks": [checks(PASS_)]})
        rc, out, _ = e.tool("pr-checks", "294")
        check("W9d head query failure -> ERROR 125", rc == 125 and "gh pr view exited 1" in final(out), out)
        e = Env(root, [{"out": json.dumps({"status": "completed", "conclusion": "success", "headSha": OLD_SHA}), "rc": 0}])
        rc, out, _ = e.tool("run", "1", "--sha", SHA)
        check("W9e run for another commit -> ERROR 125", rc == 125 and "run is for" in final(out), out)
        e = Env(root, [{"out": json.dumps({"status": "completed", "conclusion": "success", "headSha": SHA}), "rc": 0}])
        rc, out, _ = e.tool("run", "1", "--sha", SHA[:9])
        check("W9f run for the commit (short sha) -> SUCCESS", rc == 0, out)

        # W10 a descendant that escaped the process group and holds the pipes
        # cannot stretch the deadline
        e = Env(root, [{"sleep": 60, "descendant": 15}])
        rc, out, dt = e.tool("pr-checks", "294", "--deadline", "1")
        check("W10 deadline holds despite a pipe-holding descendant", rc == 124 and dt < 5, "rc=%s elapsed %.1fs" % (rc, dt))

        # W11 an un-executable gh (exec format error) is a watcher ERROR, not exit 1
        e = Env(root, [checks(PASS_)])
        with open(e.gh, "wb") as f:
            f.write(b"\x7fELF-not-really")
        rc, out, _ = e.tool("pr-checks", "294", "--deadline", "2")
        check("W11 exec format error -> ERROR 125 'cannot execute' (not a crash)", rc == 125 and "status=ERROR" in final(out) and "cannot execute" in final(out), "rc=%s %s" % (rc, out))

        # W12 any watcher crash -> ERROR 125 (never the hosted-FAILURE code 1)
        probe = ("import sys; sys.path.insert(0, %r); import bounded_wait as b\n"
                 "def boom(args, out=None): raise RuntimeError('injected')\n"
                 "b.watch = boom\n"
                 "sys.exit(b.main(['run', '1', '--gh', 'gh']))" % HERE)
        p = subprocess.run([PY, "-c", probe], capture_output=True, text=True, timeout=30,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        check("W12 crash -> exit 125 + ERROR line", p.returncode == 125 and "status=ERROR" in final(p.stdout) and "injected" in p.stdout,
              "rc=%s %s" % (p.returncode, p.stdout + p.stderr))

        # usage: no unbounded or invalid deadline
        for bad in ("0", "-5", "nan", "inf"):
            p = subprocess.run([PY, TOOL, "run", "1", "--deadline", bad], capture_output=True, text=True, timeout=30)
            check("usage: --deadline %s rejected (exit 2)" % bad, p.returncode == 2, p.stderr[-200:])
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("checks failed: %d" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
