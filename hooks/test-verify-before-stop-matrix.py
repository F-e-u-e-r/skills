#!/usr/bin/env python3
"""Verification-evidence regression matrix for verify-before-stop.py.

Every case drives the hook through its REAL entry surface - a Stop payload on
stdin naming a JSONL transcript - and reads only what the hook emits (stdout +
exit status + its own log). Nothing here re-implements the hook's logic.

Contract under test (the hook's header has the long form): after the LAST code
edit of the turn, ONE of these must appear, or the Stop is blocked -
  V1  executed code that exercises the change (a script, a module, a test or
      check runner, a compile/syntax check; inline code only if it names an
      edited file);
  V2  a verification-intent subagent dispatch (Agent/Task, or SendMessage to
      one), including the pack's own critic/adversarial/audit idiom;
  V3  an explicit final-report line
      "No executable test applies: <reason>; verified by <method>".
V4/V5 are the fail-closed side: no evidence, or prose/markers/inspection only,
still blocks. V6: evidence that precedes the last edit does not count.

Usage:
  python3 hooks/test-verify-before-stop-matrix.py              # gate (exit 1 on any miss)
  python3 hooks/test-verify-before-stop-matrix.py --hook P --report
      # run the same cases against another hook build and print every verdict
      # without failing - how the pre-fix RED evidence is produced.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
DEFAULT_HOOK = os.path.join(HERE, "verify-before-stop.py")


def edit(path, tool="Edit"):
    return {"type": "tool_use", "name": tool, "input": {"file_path": path}}


def bash(cmd, desc=None, result=None):
    inp = {"command": cmd}
    if desc:
        inp["description"] = desc
    b = {"type": "tool_use", "name": "Bash", "input": inp}
    if result is not None:
        b["__result__"] = result  # the tool_result text the transcript records
    return b


def agent(desc, prompt, tool="Agent"):
    return {"type": "tool_use", "name": tool, "input": {"description": desc, "prompt": prompt}}


def send(message, summary=""):
    return {"type": "tool_use", "name": "SendMessage",
            "input": {"to": "a7ac2899ee56efdbf", "summary": summary, "message": message}}


def text(t):
    return {"type": "text", "text": t}


JUST = ("No executable test applies: these files are eval fixtures read by probe "
        "arms, not shipped code; verified by diffing each fixture against the "
        "D-EVAL-SPEC checklist")

# Real command shapes observed in blocked sessions (2026-10-28..11-02).
RUN_EVAL = ('python3 -I regression/run_eval.py > /tmp/postfix_out.txt 2>&1; '
            'echo "REAL_EXIT=$?"; echo "=== FAILURES ==="; grep -n "x" regression/RESULTS.md')
PY_COMPILE = ('cd /Users/u/fable/internal/xh && python3 -I -m py_compile harness/review_worker.py '
              'harness/review_orchestrator.py && echo "COMPILE OK"')
SELFTEST = 'cd prototypes && \\\necho "=== REG-A ===" && bash ./launcher-selftest.sh; echo "rc=$?"'
CRITIC_PROMPT = ("You are a FRESH-CONTEXT adversarial critic. Your job is to BREAK a security "
                 "patch, not to bless it. Assume the author is overconfident. Be concrete: a "
                 "finding must come with a reproduction (inputs -> observed wrong output).")

W = "/Users/u/fable/internal/xh/harness/review_worker.py"
APP = "/work/app.py"

# (id, blocks, last_assistant_message or None, expected verdict)
CASES = [
    # V1 - project-specific executable verification is recognized
    ("V1a-run-eval-script", [edit(W), bash(RUN_EVAL)], None, "PASS"),
    ("V1b-py-compile-module", [edit(W), bash(PY_COMPILE)], None, "PASS"),
    ("V1c-relative-selftest", [edit("/w/prototypes/reviewer-launcher.sh"), bash(SELFTEST)], None, "PASS"),
    ("V1d-env-prefix-option-interp", [edit(APP), bash("PYTHONPATH=. python3 -u tools/check_projection.py")], None, "PASS"),
    ("V1e-inline-names-edited", [edit(W), bash("python3 - <<'PY'\nimport review_worker\nassert review_worker.parse('x')\nPY")], None, "PASS"),
    ("V1f-pytest-preserved", [edit(APP), bash("pytest -q")], None, "PASS"),
    ("V1g-bash-n-syntax", [edit("/w/hooks/x.sh"), bash("bash -n /w/hooks/x.sh && echo syntax-ok")], None, "PASS"),
    ("V1h-shell-c-recursion", [edit(APP), bash('bash -c "python3 -m pytest -q"')], None, "PASS"),
    ("V1i-wrapped-by-timeout", [edit(APP), bash("timeout 600 python3 -I regression/run_eval.py")], None, "PASS"),
    ("V1j-abs-script-path", [edit(APP), bash("/Users/u/fable/hooks/test-verify-before-stop.sh")], None, "PASS"),
    ("V1k-unbalanced-quote-fallback", [edit(APP), bash("python3 -I regression/run_eval.py; echo don't")], None, "PASS"),
    ("V1l-parallel-same-message", [[edit(APP), bash("pytest -q")]], None, "PASS"),
    # V2 - verification-intent subagent dispatch
    ("V2a-critic-dispatch", [edit(W), agent("Fresh adversarial critic on Part-A patch", CRITIC_PROMPT)], None, "PASS"),
    ("V2b-verify-agent-preserved", [edit(APP), agent("", "verify the fix: run the tests and report", "Task")], None, "PASS"),
    ("V2c-sendmessage-rereview", [edit(W), send("Re-review round as the adversarial critic: try to break the M1 fix.", "Re-review the M1 fix")], None, "PASS"),
    ("V2e-doctrine-critic-only", [edit(W), agent("Fresh critic on canonical doctrine delta", "You are a FRESH-CONTEXT doctrine critic. Judge a small edit to two canonical skill files.")], None, "PASS"),
    ("V2f-auditor-only", [edit(W), agent("Fresh-context eval critique", "You are an adversarial, fresh-context auditor of an internal evaluation. Find what is overclaimed.")], None, "PASS"),
    ("V2d-impl-agent-not-verification", [edit(APP), agent("Implement the parser", "Write the parser module and wire it in")], None, "BLOCK"),
    # V3 - explicit no-executable-test justification (final report)
    ("V3a-justification-lam", [edit("/w/fixture/services/tiers.py", "Write")], JUST, "PASS"),
    ("V3b-justification-transcript-fallback", [edit("/w/fixture/services/tiers.py", "Write"), text(JUST)], None, "PASS"),
    ("V3c-justification-without-method", [edit(APP)], "No executable test applies: fixture data only.", "BLOCK"),
    ("V3e-quoted-template-is-not-a-justification", [edit(APP)], 'The hook accepts a final line "No executable test applies: <reason>; verified by <method>".', "BLOCK"),
    ("V3d-justification-before-last-edit", [edit(APP), text(JUST), edit("/work/other.py")], None, "BLOCK"),
    # V4 - true missing verification still fails closed
    ("V4a-inspect-only", [edit(APP), bash("git diff --stat; cat /work/app.py")], None, "BLOCK"),
    ("V4b-search-only", [edit(APP), bash("grep -n 'def ' /work/app.py | head -20")], None, "BLOCK"),
    ("V4c-vcs-with-verify-words", [edit(APP), bash('gh pr view 12; git commit -m "verify tests pass"')], None, "BLOCK"),
    ("V4d-no-tool-calls", [edit(APP)], None, "BLOCK"),
    ("V4e-pip-install-not-verification", [edit(APP), bash("python3 -m pip install -r requirements.txt")], None, "BLOCK"),
    # V5 - prose / marker / decorative action alone never satisfies
    ("V5a-echo-marker", [edit(APP), bash('echo "VERIFICATION_EXECUTED: all tests passed"')], None, "BLOCK"),
    ("V5b-inline-print-marker", [edit(APP), bash("python3 -c \"print('VERIFICATION_EXECUTED')\"")], None, "BLOCK"),
    ("V5c-final-prose-claim", [edit(APP)], "I verified the change and all tests pass.", "BLOCK"),
    ("V5d-description-claim-only", [edit(APP), bash("true", desc="Run the full test suite to verify")], None, "BLOCK"),
    ("V5e-heredoc-data-not-executed", [edit(APP), bash("cat > /work/run_tests.sh <<'EOF'\npython3 -m pytest -q\nEOF")], None, "BLOCK"),
    ("V5f-abs-system-tool", [edit(APP), bash("/bin/echo ok")], None, "BLOCK"),
    ("V5g-marker-in-final-text", [edit(APP)], "VERIFICATION_EXECUTED", "BLOCK"),
    # V6 - verification that precedes the last code edit does not count
    ("V6a-test-then-edit", [bash("pytest -q"), edit(APP)], None, "BLOCK"),
    ("V6b-test-edit-test", [bash("pytest -q"), edit(APP), bash("pytest -q")], None, "PASS"),
    ("V6c-agent-then-edit", [agent("", "verify the fix: run the tests and report", "Task"), edit(APP)], None, "BLOCK"),
    ("V6d-edit-test-edit", [edit(APP), bash("pytest -q"), edit("/work/b.py")], None, "BLOCK"),
    # A - attacks on the classifier itself (forged command position, data that
    # looks like code, info-only flags, inline markers) and parser edges
    ("A01-forged-position-in-quotes", [edit(APP), bash('echo "a; pytest -q"')], None, "BLOCK"),
    ("A02-cat-heredoc-data", [edit(APP), bash("cat <<EOF\npytest -q\nEOF")], None, "BLOCK"),
    ("A03-shell-reads-heredoc-script", [edit(APP), bash("bash <<'EOF'\npytest -q\nEOF")], None, "PASS"),
    ("A04-interp-heredoc-marker", [edit(APP), bash("python3 <<'EOF'\nprint('VERIFIED')\nEOF")], None, "BLOCK"),
    ("A05-echo-quoted-interp", [edit(APP), bash("echo 'python3 x.py'")], None, "BLOCK"),
    ("A06-version-flag", [edit(APP), bash("python3 --version && node -v")], None, "BLOCK"),
    ("A07-module-server-and-pretty", [edit(APP), bash("python3 -m json.tool x.json; python3 -m http.server 8000")], None, "BLOCK"),
    ("A08-project-module", [edit(APP), bash("python3 -m mypkg.selftest")], None, "PASS"),
    ("A09-shell-c-inspection", [edit(APP), bash("sh -c 'echo ok' && /bin/sh -c \"true\"")], None, "BLOCK"),
    ("A10-command-v-lookup", [edit(APP), bash("command -v python3")], None, "BLOCK"),
    ("A11-here-string-no-credit", [edit(APP), bash('python3 <<< "import app"')], None, "BLOCK"),
    ("A12-comment-only", [edit(APP), bash("# pytest -q")], None, "BLOCK"),
    ("A13-comment-does-not-eat-next-line", [edit(APP), bash("echo hi # note\npytest -q")], None, "PASS"),
    ("A14-combined-flags-marker", [edit(APP), bash("python3 -Ic 'print(1)'")], None, "BLOCK"),
    ("A15-combined-flags-names-edit", [edit(APP), bash("python3 -Ic 'import app; app.main()'")], None, "PASS"),
    ("A16-shell-o-then-c-inspection", [edit(APP), bash("bash -euo pipefail -c 'echo x'")], None, "BLOCK"),
    ("A17-shell-o-then-script", [edit(APP), bash("bash -euo pipefail ./check.sh")], None, "PASS"),
    ("A18-pipe-into-sh-no-credit", [edit(APP), bash("printf 'pytest\\n' | sh")], None, "BLOCK"),
    ("A19-node-test-runner", [edit("/work/app.js"), bash("node --test")], None, "PASS"),
    ("A20-shell-keywords", [edit(APP), bash("if pytest -q; then echo ok; fi")], None, "PASS"),
    ("A21-vcs-only", [edit(APP), bash("git status && git diff")], None, "BLOCK"),
    ("A22-quoted-forgery-in-unbalanced-cmd", [edit(APP), bash('echo "a; pytest -q"; echo don\'t')], None, "BLOCK"),
    ("A23-absolute-path-runner", [edit(APP), bash("/opt/homebrew/bin/pytest -q")], None, "PASS"),
    ("A24-ruby-syntax-check", [edit("/w/a.rb"), bash("ruby -c lib/a.rb")], None, "PASS"),
    ("A25-php-lint", [edit("/w/a.php"), bash("php -l src/a.php")], None, "PASS"),
    ("A26-deno-test-runner", [edit("/w/a.ts"), bash("deno test --allow-read")], None, "PASS"),
    ("A27-deno-install-not-verification", [edit("/w/a.ts"), bash("deno install npm:left-pad && bun install")], None, "BLOCK"),
    # P - JS package managers and Monitor (real false positives found by the
    # replay of 4254 logged Stops, 2026-11-04)
    ("P1-npm-run-script", [edit("/w/astro.config.mjs"), bash("npm run --silent check 2>&1 | tail -3 && npm run --silent build")], None, "PASS"),
    ("P2-pnpm-filter-exec-vitest", [edit("/w/a.test.tsx"), bash("pnpm --filter @starred/dashboard exec vitest run src/x.test.tsx")], None, "PASS"),
    ("P3-pnpm-recursive-script", [edit("/w/a.ts"), bash("pnpm -r typecheck 2>&1 | tail -8")], None, "PASS"),
    ("P4-npx-package-bin", [edit("/w/probe-worker.mjs"), bash("npx wrangler dev --port 8799 --ip 127.0.0.1 2>&1")], None, "PASS"),
    ("P5-monitor-runs-script", [edit("/w/monitor-poll.py"), {"type": "tool_use", "name": "Monitor", "input": {"command": "python3 /w/monitor-poll.py 82310", "description": "poll"}}], None, "PASS"),
    ("P6-pm-install-not-verification", [edit("/w/a.ts"), bash("npm install && pnpm add lodash && npm ci && yarn")], None, "BLOCK"),
    ("P7-pm-version-not-verification", [edit("/w/a.ts"), bash("npm --version; pnpm -v")], None, "BLOCK"),
    # B - request-copy entries (`api-request-blob`) are not conversation events
    ("B1-blob-copy-of-old-test-does-not-verify", [bash("pytest -q"), edit(APP),
        {"__raw__": {"type": "api-request-blob", "hash": "h1", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "toolu_0001", "name": "Bash", "input": {"command": "pytest -q"}}]}}}], None, "BLOCK"),
    ("B2-blob-copy-of-old-edit-does-not-block", [edit(APP), bash("pytest -q"),
        {"__raw__": {"type": "api-request-blob", "hash": "h2", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "toolu_0001", "name": "Edit", "input": {"file_path": APP}}]}}}], None, "PASS"),
    ("B3-blob-copy-of-pre-window-test-does-not-verify", [
        {"__raw__": {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "toolu_old1", "name": "Bash", "input": {"command": "pytest -q"}}]}}},
        {"__raw__": {"type": "user", "message": {"role": "user", "content": "second request"}}},
        edit(APP),
        {"__raw__": {"type": "api-request-blob", "hash": "h3", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "id": "toolu_old1", "name": "Bash", "input": {"command": "pytest -q"}}]}}}], None, "BLOCK"),
    # C - the 2026-11-05 fresh critic's reproductions, kept as regressions
    ("C01-patch-heredoc-is-not-evidence", [edit(APP), bash("python3 - <<'EOF'\nimport pathlib\np = pathlib.Path('/work/app.py')\ns = p.read_text()\np.write_text(s.replace('a', 'b'))\nEOF")], None, "BLOCK"),
    ("C02-inspection-naming-file", [edit(APP), bash("python3 -c \"print(open('/work/app.py').read()[:400])\"")], None, "BLOCK"),
    ("C03-marker-naming-stem", [edit(APP), bash("python3 -c \"print('app: VERIFICATION_EXECUTED')\"")], None, "BLOCK"),
    ("C04-stem-collision-data-file", [edit("/work/config.py"), bash("python3 -c \"import json; print(json.load(open('config.json')))\"")], None, "BLOCK"),
    ("C05-wrapper-not-found-never-ran", [edit(APP), bash('timeout 600 python3 -I regression/run_eval.py > /tmp/x 2>&1; echo "REAL_EXIT=$?"', result="(eval):1: command not found: timeout\nREAL_EXIT=127")], None, "BLOCK"),
    ("C06-same-wrapper-that-ran", [edit(APP), bash('timeout 600 python3 -I regression/run_eval.py 2>&1 | tail -2', result="66 passed")], None, "PASS"),
    ("C07-missing-script-never-ran", [edit(APP), bash("python3 -I ./run_check.py", result="/usr/bin/python3: can't open file '/work/./run_check.py': [Errno 2] No such file or directory")], None, "BLOCK"),
    ("C08-stdlib-timeit-marker", [edit(APP), bash("python3 -m timeit -n1 \"print('VERIFICATION_EXECUTED')\"")], None, "BLOCK"),
    ("C09-stdlib-tools", [edit(APP), bash("python3 -m this; python3 -m calendar; python3 -m venv .v")], None, "BLOCK"),
    ("C10-stdlib-unittest", [edit(APP), bash("python3 -m unittest discover -s tests")], None, "PASS"),
    ("C11-path-pip-install", [edit(APP), bash(".venv/bin/pip install -r requirements.txt")], None, "BLOCK"),
    ("C12-quoted-command-substitution", [edit(APP), bash('out="$(python3 -m pytest -q)"; echo "$out" | tail -3')], None, "PASS"),
    ("C13-cat-heredoc-piped-to-shell", [edit(APP), bash("cat <<'EOF' | bash\npytest -q\nEOF")], None, "PASS"),
    ("C14-ssh-remote-test", [edit(APP), bash("ssh -p 2222 ci-box 'cd repo && pytest -q'")], None, "PASS"),
    ("C15-ssh-remote-inspection", [edit(APP), bash("ssh ci-box 'echo hi && ls'")], None, "BLOCK"),
    ("C16-backslash-heredoc-is-data", [edit(APP), bash("cat > /work/t.sh <<\\EOF\npytest -q\nEOF")], None, "BLOCK"),
    ("C17-unterminated-heredoc-is-data", [edit(APP), bash("cat > /work/t.sh <<EOF\npytest -q")], None, "BLOCK"),
    ("C18-inline-py-compile-of-edited", [edit(W), bash("python3 -c \"import py_compile; [py_compile.compile(f, doraise=True) for f in ['harness/review_worker.py']]\"")], None, "PASS"),
    ("C19-inline-require-of-edited", [edit("/work/app.js"), bash("node -e \"require('./app.js').main()\"")], None, "PASS"),
    ("C20-inline-node-marker", [edit("/work/app.js"), bash("node -e \"console.log('app ok')\"")], None, "BLOCK"),
    ("C21-inline-loads-edited-by-path", [edit("/work/reexpress.py"), bash("python3 - <<'PY'\nimport importlib.util\nspec = importlib.util.spec_from_file_location('reexpress', 'reexpress.py')\nmod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)\nprint(len(mod.REX))\nPY")], None, "PASS"),
    # unchanged surface
    ("U1-doc-only-edit", [edit("/work/README.md")], None, "PASS"),
    ("U2-cat-pytest-ini", [edit(APP), bash("cat pytest.ini")], None, "BLOCK"),
]


def write_transcript(path, blocks):
    """A real user prompt, then one assistant entry per block (a nested list = one
    assistant message carrying several blocks), each tool_use answered by a
    tool_result entry as in real transcripts."""
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps({"type": "user", "message": {"role": "user", "content": "please do the task"}}) + "\n")
        for item in blocks:
            if isinstance(item, dict) and "__raw__" in item:
                f.write(json.dumps(item["__raw__"]) + "\n")
                continue
            group = item if isinstance(item, list) else [item]
            content, results = [], {}
            for b in group:
                b = dict(b)
                if b["type"] == "tool_use":
                    n += 1
                    b["id"] = "toolu_%04d" % n
                    results[b["id"]] = b.pop("__result__", "ok")
                content.append(b)
            f.write(json.dumps({"type": "assistant", "message": {"role": "assistant", "content": content}}) + "\n")
            for b in content:
                if b["type"] == "tool_use":
                    f.write(json.dumps({"type": "user", "message": {"role": "user", "content": [
                        {"type": "tool_result", "tool_use_id": b["id"], "content": results[b["id"]]}]}}) + "\n")


def run_case(hook, tmp, cid, blocks, lam):
    tpath = os.path.join(tmp, cid + ".jsonl")
    write_transcript(tpath, blocks)
    payload = {"transcript_path": tpath, "stop_hook_active": False, "hook_event_name": "Stop"}
    if lam is not None:
        payload["last_assistant_message"] = lam
    home = os.path.join(tmp, "home-" + cid)
    os.makedirs(home)
    env = dict(os.environ, HOME=home)
    p = subprocess.run([sys.executable, hook], input=json.dumps(payload), capture_output=True,
                       text=True, env=env, timeout=60)
    out = p.stdout
    if out == "":
        verdict, reason = "PASS", ""
    else:
        try:
            d = json.loads(out)
            verdict = "BLOCK" if d.get("decision") == "block" and d.get("reason") else "OTHER"
            reason = d.get("reason") or ""
        except ValueError:
            verdict, reason = "OTHER", ""
    logp = os.path.join(home, ".claude", "hooks", "hooks.log")
    log = open(logp, encoding="utf-8").read() if os.path.exists(logp) else ""
    return verdict, p.returncode, reason, log, p.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook", default=DEFAULT_HOOK)
    ap.add_argument("--report", action="store_true", help="print every verdict; never fail")
    a = ap.parse_args()
    hook = os.path.realpath(a.hook)
    print("subject hook: %s" % hook)
    failures = []
    with tempfile.TemporaryDirectory(prefix="vbs-matrix-") as tmp:
        for cid, blocks, lam, expect in CASES:
            verdict, rc, reason, log, err = run_case(hook, tmp, cid, blocks, lam)
            problems = []
            if rc != 0:
                problems.append("hook exit %d (contract: always 0)" % rc)
            if verdict != expect:
                problems.append("verdict %s, expected %s" % (verdict, expect))
            if not a.report and verdict == expect == "BLOCK" and "No executable test applies" not in reason:
                problems.append("block reason does not name the V3 justification form")
            if not a.report and cid.startswith("V3") and expect == "PASS" and "PASS no-exec justification" not in log:
                problems.append("V3 pass left no audit log line")
            if "ERROR" in log:
                problems.append("hook logged an internal ERROR: %s" % log.strip()[-200:])
            status = "ok  " if not problems else "MISS"
            print("%s %-38s expect=%-5s got=%-5s rc=%d%s" % (status, cid, expect, verdict, rc,
                  "" if not problems else "  <- " + "; ".join(problems)))
            if problems:
                failures.append(cid)
    print("cases=%d misses=%d" % (len(CASES), len(failures)))
    if a.report:
        return 0
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
