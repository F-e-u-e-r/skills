#!/usr/bin/env bash
# Regression suite for bounded_wait.py (portable bounded CI wait); the cases
# live in test-bounded_wait.py. Exit status is the suite's, unmasked.
set -eu
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
command -v python3 >/dev/null 2>&1 || { echo "SKIP: python3 is required by bounded_wait.py" >&2; exit 0; }
python3 "$root/hooks/test-bounded_wait.py" || { echo "FAIL bounded-wait suite" >&2; exit 1; }
echo "OK: all bounded-wait tests passed"
