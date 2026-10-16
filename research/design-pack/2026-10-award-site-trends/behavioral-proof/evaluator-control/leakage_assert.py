#!/usr/bin/env python3
"""
Deterministic evaluator control for the pre-registered Case-1 spectacle-leakage
criterion (research/design-pack/2026-10-award-site-trends/behavioral-proof).

Why this exists: the behavioral proof has NO separable scorer -- run_battery*.py
only CAPTURE model output (their own comment: "No grading here"); grading was by
human reading of the captured files. Per owner adjudication §4, this is the
NARROWEST deterministic assertion that implements the pre-registered Case-1 leak
criterion, so the criterion can be exercised two-sided (a GOOD output must not
leak; a known-bad output must leak) -- a green sweep without a known-bad that can
fail is not an armed gate (ground-truth-gates item 2).

Pre-registered criterion (PRE-REGISTRATION.md, CASE 1 -> the FAIL clause):
  For an ORDINARY product/app page that carries a gratuitous spectacle device
  bundle, the review LEAKS iff it waves the spectacle through. Operationalized on
  the structural verdict line the subject is required to emit (the graded prose
  cannot produce it incidentally -- ground-truth-gates "key on a structural
  marker the subject must create"):

      CONTEXT-FIT: OK      -> LEAK    (spectacle approved for ordinary UI) -> FAIL (exit 1)
      CONTEXT-FIT: NOT-OK  -> NO-LEAK (ordinary UI not waved through)       -> PASS (exit 0)
      (verdict line absent)-> NOT-COMPLETED (never scored as a pass)        -> exit 2

The verdict line is the sole authority. The device-vocabulary scan below is a
NON-AUTHORITATIVE diagnostic printed for context only: those device terms occur
in BOTH a leaking review and a rejecting one (the rejecting review names the same
devices as problems), so they cannot discriminate leak from no-leak and are never
used to decide the verdict. Scope: ordinary-page leak only; the override lane
(experimental/agency brief) legitimately yields OK and is NOT this control's
subject.

Usage: leakage_assert.py <output-file>
"""
import re, sys

# identical to run_battery.py VERDICT["C1"] -- reuse the proof's own parser
VERDICT_RE = re.compile(r"CONTEXT-FIT:\s*(OK|NOT-OK)")
DEVICE_RE = re.compile(
    r"webgl|3d|spatial|room-to-room|scrollytelling|horizontal narrative|kinetic|"
    r"variable type|reactive cursor|frosted|glassmorphism|glass|blur|700ms|cinematic",
    re.I,
)


def classify(text):
    matches = VERDICT_RE.findall(text)
    if not matches:
        return "NOT-COMPLETED", None
    verdict = matches[-1]  # the required final line
    return ("LEAK" if verdict == "OK" else "NO-LEAK"), verdict


def main():
    if len(sys.argv) != 2:
        print("usage: leakage_assert.py <output-file>")
        return 2
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()
    status, verdict = classify(text)
    has_dev = bool(DEVICE_RE.search(text))
    print(f"{path}: verdict={verdict} -> {status}  "
          f"(device-vocab present: {has_dev} [diagnostic, non-authoritative])")
    if status == "LEAK":
        print("  REASON: CONTEXT-FIT: OK on an ordinary product page = the spectacle "
              "device bundle was waved through (leak into ordinary UI).")
    return {"NO-LEAK": 0, "LEAK": 1, "NOT-COMPLETED": 2}[status]


if __name__ == "__main__":
    sys.exit(main())
