# R1a — E-1 harness path-hardening + disposition record

> **Semantic-preparation record. NO `git mv`, NO relocation performed here.**
> Baseline: `main` @ `d7b9966` (branch `relocation/r1a-e1-harness-path-hardening`).
> This record accompanies the R1a code change (four hardened harnesses) and
> records the disposition of the harnesses that were *not* hardened, plus the
> E-3 round5 unit-boundary resolution.

## Purpose

The migration manifest (`reviews/2026-09-27-reviews-relocation-manifest.md`)
identified 12 depth-sensitive issue-115 harnesses (each computing the repo
root as two levels up from the script — 11 spelled
`REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))`, and
`2026-09-02-recursive-delegation-c12/c12_checks.py` spelled
`ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))`;
the same depth coupling either way). Under the target `evidence/probes/<unit>/` home the same
`../..` reaches `evidence/`, not the repo root, so the harness would silently
resolve the wrong root after a path-only move.

R1a is the **semantic-preparation** commit the manifest's E-1 disposition
requires: it removes that depth coupling *while the harnesses are still at
their old path*, so a subsequent relocation commit can remain path-only. R1a
does not move anything.

## Governance model applied

Reading the harness source (not the manifest summary) established that only a
subset can be made depth-independent *without changing probe semantics or
altering frozen campaign evidence*. The adjudicated model is:

- **R1a — harden the cleanly-hardenable harnesses** (below): repo-root
  discovery made depth-independent; current-location behaviour byte-identical
  to the pre-change baseline; relocation-safe.
- **Disposition — mark the rest `non-rerunnable historical artifact`** (C):
  no semantic rewrite, no seal regeneration. Their bytes and history are
  preserved and relocate under the eventual path mapping, but they are **not
  required to be executable after relocation**, and a post-relocation failure
  in them is **not** a regression. A rewrite to restore re-runnability
  (option B) is explicitly out of scope; if a specific harness ever needs it,
  that is a separate, per-unit rehabilitation authorization — not part of the
  relocation phase.

## 1. Hardened harnesses (4) — depth-independent, zero drift

> **Scope of "hardened":** each harness's OWN repo-root / sibling / git-pathspec
> location logic is made depth-independent and relocation-safe — the single
> property `relocation_safety_checks.py` proves. This is NOT a claim of
> end-to-end post-relocation re-runnability; see the erratum at the end of §2 for
> `t2probe-prefix` / `t2probe-scored`, which invoke the disposition-set prereg
> checker at runtime.

| Harness | Change |
|---|---|
| `reviews/2026-08-13-issue115-t2probe-prefix/prefix_checks.py` | `REPO` → `git -C ROOT rev-parse --show-toplevel`; `PREREG` → `ROOT/../<unit>`; `git status` pathspec → `os.path.relpath(PREREG, REPO)` |
| `reviews/2026-08-13-issue115-t2probe-scored/scored_checks.py` | `REPO` → git-toplevel; `PREREG` → sibling-relative; two `git status` reviews/ pathspecs → `os.path.relpath(...)` (`skills` kept literal) |
| `reviews/2026-08-14-issue115-t2-amendment-design/design_checks.py` | `REPO` → git-toplevel (no reviews/ literal; only reaches non-moving `skills/`) |
| `reviews/2026-08-15-issue115-t5p-scored/scored_checks.py` | `REPO` → git-toplevel; `PKG` → sibling-relative; three `git diff HEAD` reviews/ pathspecs → `os.path.relpath(...)` (`skills`, `metadata` kept literal) |

**Hardening mechanism (all four):**
- `REPO = subprocess.run(["git", "-C", ROOT, "rev-parse", "--show-toplevel"], ..., check=True).stdout.strip()`, then a non-empty guard (`sys.exit` on empty) and `os.path.abspath(...)` normalization. Fail-loud; no silent fallback to `../..`; no hard-coded machine path; cwd-independent (uses the script's own dir via `-C ROOT`).
- Sibling package references (`os.path.join(REPO, "reviews", "<unit>")`) become `os.path.abspath(os.path.join(ROOT, "..", "<unit>"))` — identical current resolution, and they follow the packages if all issue-115 units relocate together.
- Git operations that *survive* relocation — `git status --porcelain` and `git diff HEAD` (both compare against the working tree / current HEAD, which is clean after any commit) — take `os.path.relpath(<target>, REPO)` instead of a `"reviews/…"` literal, so the pathspec follows the file to its new home. `skills`/`metadata` pathspecs (non-moving) stay literal.

**Semantic invariants preserved (unchanged):** fixtures, scoring, expected
verdicts, sample/target identity, thresholds, probe logic, output contract,
campaign historical evidence. The only semantic change is *how the harness
finds the repo root and its sibling artifacts*.

**Zero-drift evidence:** each hardened harness was run before and after the
change; on a clean committed tree its output is byte-identical to the
pre-change baseline (same PASS/FAIL lines, counts, and final verdict).
Repo-root discovery depth-independence is guarded by
`relocation_safety_checks.py` in this directory.

> Note on baseline state: 10 of the 12 issue-115 harnesses are already RED at
> `d7b9966` — they pin doctrine blobs and baseline commits that the repository
> has evolved past since the campaigns closed (Aug 2026). Those failures are
> historical-pin drift, independent of location. "Zero drift" here means the
> hardening does not change each harness's observable pass/fail pattern at the
> current location — not that the harnesses are green.

## 2. Disposition set (8) — `non-rerunnable historical artifact`

Not hardened. Left byte-for-byte as-is. Two reasons, both amounting to
"integrity defined against frozen state, which editing or relocating breaks":

### 2a. Sealed prereg packages — editing the checker breaks its own seal

| Harness | Reason |
|---|---|
| `reviews/2026-08-13-issue115-t2-probe-prereg/static_checks.py` | Its package `MANIFEST.json` records `sha256(static_checks.py)` (and `make_manifest.py`) under `documents`, and the harness self-verifies those hashes ("MANIFEST recorded hashes match recomputation"). Any byte change to the checker — including the depth-hardening — breaks that self-hash. Restoring it requires regenerating the sealed `MANIFEST.json`/`MANIFEST.sha256`, i.e. altering frozen campaign evidence (option B), which is out of scope. |
| `reviews/2026-08-14-issue115-t5-placement-probe-prereg/static_checks.py` | Same: `MANIFEST.json` self-hashes `static_checks.py` + `make_manifest.py`. |

### 2b. Frozen-baseline harnesses — the move is a diff against a pinned commit

These assert "byte-unchanged since a specific historical commit" via
`git diff <FROZEN-COMMIT> -- <path>` (or read blobs by a repo-root-relative
path fixed in frozen data). A path-only relocation is *itself* a change
relative to that pinned commit, so the check cannot pass after any move —
verified: `git diff <frozen> -- <old path>` and `git diff <frozen> -- <new
path>` are both non-empty after a `git mv`; only the frozen literal or a
semantic rewrite could change that, and neither is in R1's scope.

| Harness | Frozen-baseline mechanism |
|---|---|
| `reviews/2026-08-15-issue115-t5p-prefix/prefix_checks.py` | `git diff MERGE -- reviews/2026-08-14-…` (`:31`–`:35`). Currently GREEN (37/37); would flip to FAIL on relocation. |
| `reviews/2026-08-15-issue115-t5p-prefix/landing_checks.py` | `git diff MERGE -- reviews/×3, skills, metadata` (`:127`–`:134`); also executes `prefix_checks.py` above. |
| `reviews/2026-08-15-issue115-t5-placement-disposition/closure_checks.py` | `git diff PRE_DISPOSITION_MAIN -- skills, metadata, reviews/×6` (`:101`–`:109`); also executes `disposition_checks.py`. |
| `reviews/2026-08-15-issue115-t5-placement-disposition/disposition_checks.py` | `git diff PRE_DISPOSITION_MAIN -- skills, metadata, reviews/×6` (`:214`–`:223`). (Its `os.path.basename(ROOT) == "…-disposition"` assertion at `:225` would survive a name-preserving move; the frozen diff would not.) |
| `reviews/2026-08-16-issue115-closure-state/closure_checks.py` | `git diff --name-only BASELINE_MAIN -- reviews` with a "new files only inside this dir" assertion (`:95`–`:98`); blob reads `git rev-parse HEAD:<reviews path>` where the paths are keys of the frozen `RECEIPTS.json` `blobs` map (`:101`–`:105`); reads round5 units (`:112`, `:166`). |
| `reviews/2026-09-02-recursive-delegation-c12/c12_checks.py` | `git diff --name-only BASE` (whole-repo file-confinement) plus a `startswith("reviews/2026-09-02-recursive-delegation-c12/")` self-path assertion (`:185`–`:188`). |

All eight are already RED or (for `t5p-prefix/prefix_checks.py`) will flip on
relocation; none is depended upon as a green gate.

**Erratum (correcting an earlier overclaim in this record).** Two of the hardened
harnesses invoke a disposition-set harness at runtime and REQUIRE it to pass:
`t2probe-prefix/prefix_checks.py:147` and `t2probe-scored/scored_checks.py:175`
each run `t2-probe-prereg/static_checks.py` and assert
`"ALL PASS" in stdout and returncode == 0`, recording their OWN failure otherwise
— they do NOT tolerate a non-ALL-PASS prereg. So R1a hardens their *own location
logic* (repo-root discovery + sibling refs + git pathspecs are depth-independent
and relocation-safe — which is all `relocation_safety_checks.py` claims), but it
does NOT make `t2probe-prefix` / `t2probe-scored` *end-to-end re-runnable /
output-stable* after relocation: at runtime they call the sealed disposition-set
prereg checker, itself a `non-rerunnable historical artifact`. Neither is
therefore treated as a relocation gate. This is a documentation correction only —
no code change, no prereg rehabilitation, and option B stays closed.
(`t2-probe-prereg/static_checks.py` is already RED at baseline on doctrine-pin
drift, independent of relocation, so this dependency is not a new failure R1a
introduced.)

## 3. E-3 resolved — round5 is a single co-located probe unit

The round5 campaign's three current top-level entries co-locate as ONE probe
unit at its eventual home:

```
evidence/probes/2026-08-04-round5/
├── targets.json          (from reviews/2026-08-04-round5-targets.json)
├── scope-plan.md         (from reviews/2026-08-04-round5-scope-plan.md)
└── results/              (from reviews/2026-08-04-round5-results/)
```

Rationale: the three are one measurement campaign's manifest/input/planning +
outputs, not three different authorities; the physical axis is artifact role
(probe), and a campaign's harness/inputs/outputs are preserved as one unit.
This removes the classification block on `closure-state/closure_checks.py`
(#11): its round5 references have a defined target home. #11 nonetheless stays
in the disposition set (2b) — its integrity is frozen-commit-bound and is not
being semantically rewritten.

## 4. What R1a does and does not do

- **Does:** make repo-root discovery depth-independent in 4 harnesses; add
  `relocation_safety_checks.py`; record the disposition of 8 harnesses and the
  E-3 resolution.
- **Does NOT:** `git mv` / relocate anything; edit or regenerate any
  `MANIFEST.json` / `MANIFEST.sha256` or other frozen campaign evidence; change
  any fixture, score, threshold, verdict, or probe logic; touch the manifest,
  README/ROADMAP/ARCHITECTURE, hooks, generated files, or the untracked
  `hcsa1-b0` material; rewrite `reviews/styling-ledger.md` (a fictional example
  citation, deliberately untouched).

Relocation remains a later, separately-authorized, path-only change.
