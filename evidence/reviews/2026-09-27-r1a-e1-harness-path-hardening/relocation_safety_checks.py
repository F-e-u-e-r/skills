#!/usr/bin/env python3
"""Relocation-safety regression gate for the R1a harness path-hardening.

Proves the single property R1a establishes: repo-root discovery in the
hardened issue-115 harnesses is INDEPENDENT of the script's directory
depth, so a later path-only `git mv` to a deeper home (e.g.
evidence/probes/<unit>/ instead of reviews/<unit>/) cannot silently
resolve the wrong repo root.

Two mechanical checks, each paired with a control that proves the check
can fail (a check that cannot fail proves nothing):

  1. `git rev-parse --show-toplevel` is depth-invariant, while the
     superseded `os.path.abspath(os.path.join(dir, "..", ".."))`
     arithmetic is NOT (control).
  2. every HARDENED harness uses git-toplevel and no longer computes
     REPO via `os.path.join(ROOT, "..", "..")`; a disposition-set
     harness still carries the old pattern by design (control), so the
     check distinguishes hardened from untouched rather than always
     passing.

Read-only against the repository. A throwaway git repo is created in the
OS temp dir (outside this repository) and removed. Run from anywhere;
exits non-zero on any failure.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile


def toplevel(cwd):
    return subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True, check=True).stdout.strip()


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(toplevel(HERE))
FAILS = []


def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + ((" — " + str(detail)) if not ok and detail else ""))
    if not ok:
        FAILS.append(name)


# ---- 1. Depth-invariance of the hardened discovery mechanism ----------------
# In an isolated throwaway repo, mirror the current (reviews/<unit>/) and a
# future deeper (evidence/probes/<unit>/) home and confirm git-toplevel
# returns the SAME root from both depths, while the superseded ../.. does not.
tmp = tempfile.mkdtemp(prefix="r1a-reloc-probe-")
try:
    subprocess.run(["git", "init", "-q", tmp], check=True)
    root = os.path.realpath(toplevel(tmp))
    shallow = os.path.join(tmp, "reviews", "unit")               # 2 below root
    deeper = os.path.join(tmp, "evidence", "probes", "unit")     # 3 below root
    os.makedirs(shallow)
    os.makedirs(deeper)
    tl_shallow = os.path.realpath(toplevel(shallow))
    tl_deeper = os.path.realpath(toplevel(deeper))
    check("git-toplevel returns the repo root from a reviews-depth dir",
          tl_shallow == root, tl_shallow)
    check("git-toplevel returns the repo root from an evidence/probes-depth dir",
          tl_deeper == root, tl_deeper)
    check("git-toplevel is depth-invariant (identical root at both depths)",
          tl_shallow == tl_deeper, (tl_shallow, tl_deeper))
    old_shallow = os.path.realpath(os.path.join(shallow, "..", ".."))
    old_deeper = os.path.realpath(os.path.join(deeper, "..", ".."))
    check("[control] superseded ../.. arithmetic is depth-sensitive (differs by depth)",
          old_shallow != old_deeper, (old_shallow, old_deeper))
    check("[control] superseded ../.. does NOT reach the repo root from the deeper dir",
          old_deeper != root, old_deeper)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---- 2. Hardened harnesses use git-toplevel; none uses REPO=../.. -----------
HARDENED = [
    "evidence/probes/2026-08-13-issue115-t2probe-prefix/prefix_checks.py",
    "evidence/probes/2026-08-13-issue115-t2probe-scored/scored_checks.py",
    "evidence/reviews/2026-08-14-issue115-t2-amendment-design/design_checks.py",
    "evidence/probes/2026-08-15-issue115-t5p-scored/scored_checks.py",
]
OLD_REPO_PAT = re.compile(r'REPO\s*=\s*os\.path\.abspath\(os\.path\.join\(ROOT,\s*"\.\.",\s*"\.\."\)\)')
TOPLEVEL_PAT = re.compile(r'rev-parse",\s*"--show-toplevel"')

for rel in HARDENED:
    src = open(os.path.join(REPO, rel), encoding="utf-8").read()
    check(f"hardened uses git-toplevel: {rel}", TOPLEVEL_PAT.search(src) is not None)
    check(f"hardened dropped REPO=../..: {rel}", OLD_REPO_PAT.search(src) is None)

# Control: a disposition-set harness is left untouched and still carries the
# old depth-sensitive pattern. This proves OLD_REPO_PAT actually matches the
# superseded construct, so the "dropped REPO=../.." checks above are real.
DISPO_CONTROL = "evidence/probes/2026-08-13-issue115-t2-probe-prereg/static_checks.py"
ctrl = open(os.path.join(REPO, DISPO_CONTROL), encoding="utf-8").read()
check("[control] disposition-set harness still carries REPO=../.. (untouched by design)",
      OLD_REPO_PAT.search(ctrl) is not None, DISPO_CONTROL)

print()
if FAILS:
    print("RELOCATION-SAFETY: FAIL —", len(FAILS), "failure(s):", FAILS)
    sys.exit(1)
print("RELOCATION-SAFETY: ALL PASS")
