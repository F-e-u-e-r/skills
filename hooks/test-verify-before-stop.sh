#!/usr/bin/env bash
# Regression tests for verify-before-stop.py — the hook always exits 0;
# a block is signaled by {"decision": "block"} on stdout. Tests cover both
# the allow path and the block path, per operational-rigor §2's install gate.
set -eu

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

command -v python3 >/dev/null 2>&1 || {
  echo "SKIP: python3 is required by verify-before-stop.py" >&2
  exit 0
}

tmp=$(mktemp -d "${TMPDIR:-/tmp}/ops-pack-vbs-test.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

# Build a transcript JSONL: a real user prompt, then tool_use blocks.
transcript_with() {
  # $1 = output path; remaining args = tool_use JSON blocks (already JSON)
  out="$1"; shift
  {
    printf '%s\n' '{"type":"user","message":{"content":"please do the task"}}'
    for block in "$@"; do
      printf '{"type":"assistant","message":{"content":[%s]}}\n' "$block"
    done
  } > "$out"
}

EDIT_PY='{"type":"tool_use","name":"Edit","input":{"file_path":"/work/app.py"}}'
EDIT_MD='{"type":"tool_use","name":"Edit","input":{"file_path":"/work/README.md"}}'
BASH_PYTEST='{"type":"tool_use","name":"Bash","input":{"command":"pytest -q"}}'
BASH_CAT_PYTEST_INI='{"type":"tool_use","name":"Bash","input":{"command":"cat pytest.ini"}}'
AGENT_VERIFY='{"type":"tool_use","name":"Task","input":{"prompt":"verify the fix: run the tests and report"}}'

run_hook() {
  # $1 = transcript path; $2 = stop_hook_active (true/false)
  TRANSCRIPT="$1" ACTIVE="$2" python3 - <<'PY' | HOME="$tmp" python3 "$root/hooks/verify-before-stop.py"
import json
import os

print(json.dumps({
    "transcript_path": os.environ["TRANSCRIPT"],
    "stop_hook_active": os.environ["ACTIVE"] == "true",
}))
PY
}

assert_block() {
  name="$1"; out="$2"
  # the whole stdout must be one valid JSON object with decision == "block"
  if printf '%s' "$out" | python3 -c '
import json, sys
d = json.load(sys.stdin)
sys.exit(0 if d.get("decision") == "block" and d.get("reason") else 1)
' 2>/dev/null; then
    echo "PASS $name"
  else
    echo "FAIL $name: expected a valid block JSON, got: $out" >&2
    exit 1
  fi
}

assert_pass() {
  name="$1"; out="$2"
  if [ -z "$out" ]; then
    echo "PASS $name"
  else
    echo "FAIL $name: expected pass-through (empty stdout), got: $out" >&2
    exit 1
  fi
}

# --- block path: code edited, no verification ---
transcript_with "$tmp/t1.jsonl" "$EDIT_PY"
assert_block "code edit without verification blocks" "$(run_hook "$tmp/t1.jsonl" false)"

# cat pytest.ini is not running tests (command-position match)
transcript_with "$tmp/t2.jsonl" "$EDIT_PY" "$BASH_CAT_PYTEST_INI"
assert_block "cat pytest.ini does not count as tests" "$(run_hook "$tmp/t2.jsonl" false)"

# --- allow path ---
transcript_with "$tmp/t3.jsonl" "$EDIT_PY" "$BASH_PYTEST"
assert_pass "code edit + pytest passes" "$(run_hook "$tmp/t3.jsonl" false)"

transcript_with "$tmp/t4.jsonl" "$EDIT_PY" "$AGENT_VERIFY"
assert_pass "code edit + verification-intent agent passes" "$(run_hook "$tmp/t4.jsonl" false)"

transcript_with "$tmp/t5.jsonl" "$EDIT_MD"
assert_pass "doc-only edit never blocks" "$(run_hook "$tmp/t5.jsonl" false)"

transcript_with "$tmp/t6.jsonl" "$EDIT_PY"
assert_pass "second Stop (relief valve) passes" "$(run_hook "$tmp/t6.jsonl" true)"

# Write counts as a code edit too (hook covers Edit/Write/NotebookEdit/MultiEdit)
WRITE_PY='{"type":"tool_use","name":"Write","input":{"file_path":"/work/new_module.py"}}'
transcript_with "$tmp/t7.jsonl" "$WRITE_PY"
assert_block "Write without verification blocks" "$(run_hook "$tmp/t7.jsonl" false)"

# Windowing: only tool calls after the LAST real user prompt count
{
  printf '%s\n' '{"type":"user","message":{"content":"first request"}}'
  printf '{"type":"assistant","message":{"content":[%s]}}\n' "$EDIT_PY"
  printf '%s\n' '{"type":"user","message":{"content":"second request, no edits after this"}}'
} > "$tmp/t8.jsonl"
assert_pass "edits before the last user prompt are out of window" "$(run_hook "$tmp/t8.jsonl" false)"

# --- quiet-degradation telemetry (2026-07-24, Miguok b6f794e lineage) ---
# Every silent no-op path must leave a log line; these fail on the pre-fix
# hook by the line's ABSENCE (runtime assertion on the log the hook wrote,
# never a grep of the hook's source).

hook_log="$tmp/.claude/hooks/hooks.log"

# Command substitution ($(...)) would strip trailing newlines and drop the
# exit status, so fail-open assertions here capture stdout to a FILE and
# assert rc==0 AND byte-empty output explicitly.
assert_failopen_raw() {
  # $1 = test name; $2 = raw stdin payload (may omit fields / be malformed)
  name="$1"; payload="$2"; outfile="$tmp/failopen.out"
  if printf '%s' "$payload" | HOME="$tmp" python3 "$root/hooks/verify-before-stop.py" > "$outfile" \
     && [ ! -s "$outfile" ]; then
    echo "PASS $name"
  else
    echo "FAIL $name: expected rc 0 + byte-empty stdout; rc=$? size=$(wc -c < "$outfile")" >&2
    exit 1
  fi
}

assert_failopen_transcript() {
  # $1 = test name; $2 = transcript path
  name="$1"; tpath="$2"; outfile="$tmp/failopen.out"
  if TRANSCRIPT="$tpath" ACTIVE=false python3 - <<'PY' | HOME="$tmp" python3 "$root/hooks/verify-before-stop.py" > "$outfile" \
     && [ ! -s "$outfile" ]; then
import json, os
print(json.dumps({"transcript_path": os.environ["TRANSCRIPT"], "stop_hook_active": False}))
PY
    echo "PASS $name"
  else
    echo "FAIL $name: expected rc 0 + byte-empty stdout; size=$(wc -c < "$outfile")" >&2
    exit 1
  fi
}

assert_log_line() {
  name="$1"; marker="$2"
  if [ -f "$hook_log" ] && grep -qF "$marker" "$hook_log"; then
    echo "PASS $name"
  else
    echo "FAIL $name: expected log line containing: $marker" >&2
    [ -f "$hook_log" ] && sed 's/^/  log: /' "$hook_log" >&2
    exit 1
  fi
}

# t9: payload without transcript_path → fail-open AND an ERROR postmortem
rm -f "$hook_log"
assert_failopen_raw "missing transcript_path still fails open (rc0, byte-empty)" '{"stop_hook_active": false}'
assert_log_line "missing transcript_path leaves schema-drift telemetry" "ERROR schema-drift: hook payload has no transcript_path"

# t10: user entries but no real prompt (local-command only) → pass + reason
rm -f "$hook_log"
{
  printf '%s\n' '{"type":"user","message":{"content":"<local-command-stdout></local-command-stdout>"}}'
  printf '{"type":"assistant","message":{"content":[%s]}}\n' "$EDIT_PY"
} > "$tmp/t10.jsonl"
assert_failopen_transcript "promptless transcript (user entries present) fails open" "$tmp/t10.jsonl"
assert_log_line "promptless-with-user-entries logs a PASS reason" "PASS degenerate transcript: user entries but no real user prompt"

# t11: no user-type entries at all → pass + WARN (unknown shape)
rm -f "$hook_log"
printf '{"type":"assistant","message":{"content":[%s]}}\n' "$EDIT_PY" > "$tmp/t11.jsonl"
assert_failopen_transcript "no-user-entries transcript fails open" "$tmp/t11.jsonl"
assert_log_line "no-user-entries logs a WARN" "WARN unknown transcript shape: no user-type entries"

# t11b: empty JSONL file → same unknown-shape WARN branch, named fixture
rm -f "$hook_log"
: > "$tmp/t11b.jsonl"
assert_failopen_transcript "empty transcript file fails open" "$tmp/t11b.jsonl"
assert_log_line "empty transcript logs the unknown-shape WARN" "WARN unknown transcript shape: no user-type entries"

# t12 (characterization, old-and-new): malformed stdin still fails open,
# and the except path leaves its (pre-existing) ERROR record
rm -f "$hook_log"
assert_failopen_raw "malformed stdin fails open" 'not json at all'
assert_log_line "malformed stdin leaves the except-path ERROR" "ERROR "

# t14-t17: TEST_CMD_RE coverage of this pack's own entrypoints (2026-07-24:
# the hook blocked its own repo's sessions twice while real verification ran
# — bash hooks/test-*.sh and python3 .github/checks.py were invisible to it)
BASH_HOOK_SUITE='{"type":"tool_use","name":"Bash","input":{"command":"bash hooks/test-verify-before-stop.sh"}}'
PY_CHECKS='{"type":"tool_use","name":"Bash","input":{"command":"python3 .github/checks.py"}}'
BASH_TEMPLATE_RUNALL='{"type":"tool_use","name":"Bash","input":{"command":"bash template/run-all.sh --min 0.9"}}'
BASH_CAT_SUITE='{"type":"tool_use","name":"Bash","input":{"command":"cat hooks/test-verify-before-stop.sh"}}'

transcript_with "$tmp/t14.jsonl" "$EDIT_PY" "$BASH_HOOK_SUITE"
assert_pass "bash hooks/test-*.sh counts as verification" "$(run_hook "$tmp/t14.jsonl" false)"

transcript_with "$tmp/t15.jsonl" "$EDIT_PY" "$PY_CHECKS"
assert_pass "python3 .github/checks.py counts as verification" "$(run_hook "$tmp/t15.jsonl" false)"

transcript_with "$tmp/t16.jsonl" "$EDIT_PY" "$BASH_TEMPLATE_RUNALL"
assert_pass "bash template/run-all.sh counts as verification" "$(run_hook "$tmp/t16.jsonl" false)"

transcript_with "$tmp/t17.jsonl" "$EDIT_PY" "$BASH_CAT_SUITE"
assert_block "cat of a test script is not verification" "$(run_hook "$tmp/t17.jsonl" false)"

# t13: block JSON survives a legacy-codepage stdout (the Miguok ebb9621
# incident class) — ensure_ascii output must not crash under cp950
transcript_with "$tmp/t13.jsonl" "$EDIT_PY"
out=$(TRANSCRIPT="$tmp/t13.jsonl" ACTIVE=false python3 - <<'PY' | HOME="$tmp" PYTHONIOENCODING=cp950 python3 "$root/hooks/verify-before-stop.py"
import json, os
print(json.dumps({"transcript_path": os.environ["TRANSCRIPT"], "stop_hook_active": False}))
PY
)
assert_block "block JSON survives cp950 stdout encoding" "$out"

echo "OK: all verify-before-stop tests passed"
