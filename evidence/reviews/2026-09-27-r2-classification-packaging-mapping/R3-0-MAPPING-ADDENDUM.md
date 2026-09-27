# R3-0 — post-freeze consumer delta sweep (addendum to the R2 mapping freeze)

> **Addendum to `MAPPING-FREEZE.md`. Pre-move closure gate of the R3 path-only
> relocation; recorded BEFORE any `git mv`.** Baseline: `main` @ `831db8b`.
> Sweep window: manifest baseline `25cefe4` → `831db8b` (`86c88a9` manifest,
> `d6f374b`/`e56e619` R1a, `016221d` R1a erratum, `4e75c26` R2).

## Question

`MAPPING-FREEZE.md` §5 carries the manifest's 68 external consumer sites
unchanged. R1a landed AFTER the manifest and added an executable consumer of
`reviews/…` paths. Which real consumers were added after the manifest / the R2
freeze, and how does each relocate?

## Method (all read-only, re-runnable)

- `git diff --name-status 25cefe4..831db8b` — 8 files changed, **all under
  `reviews/`**; zero files changed outside `reviews/`.
- Literal external sweep `git grep -n "reviews/" -- ':(exclude)reviews/'` at
  `25cefe4` and at `831db8b`: **67 = 67**, content-identical (line numbers
  aside). The segment-form site (`hooks/test-skill-vetting-advisory.py:1309`,
  `os.path.join(REPO, "reviews", …)`) is likewise unchanged → the external
  consumer set is exactly the manifest's 68.
- Segment-form sweep `git grep -nE "[\"']reviews[\"']"` over `reviews/**/*.py`
  at `831db8b`: hits only in the 8 R1a disposition-set harnesses plus one
  throwaway-fixture line in the R1a gate (`relocation_safety_checks.py:58`).
- Hardened-harness literal check: `git grep -n reviews --` over the 4 R1a-hardened
  harnesses = **0 hits**; their sibling references (`ROOT/../<unit>`) name
  `2026-08-13-issue115-t2-probe-prereg`, `2026-08-13-issue115-t2probe-prefix`,
  `2026-08-14-issue115-t5-placement-probe-prereg`, `2026-08-15-issue115-t5p-prefix`,
  `2026-08-08-issue115-stage2` — every one lands flat under `evidence/probes/`
  (sibling-adjacency invariant holds); `design_checks.py` reaches only the
  non-moving `skills/`.
- Gitignored local trees (not tracked, not shipped, not in the move-set):
  `evals/` 157 files, `internal/` 4, `pack-eval-artifacts/` 1, non-whitelisted
  `skills-staging/` 8, `design-mining/` 0 reference `reviews/` →
  **excluded/untracked**, no action (their consumers of old paths are local
  working material governed by their own lines).

## Findings — the post-freeze delta

| Post-freeze item | Class | Relocation behavior |
|---|---|---|
| `reviews/2026-09-27-r1a-e1-harness-path-hardening/relocation_safety_checks.py` — `HARDENED` list (4 quoted paths, `:81`–`:84`) + `DISPO_CONTROL` (`:97`) | **REWRITE-AT-MOVE** (a real executable regression gate; it opens these files) | The 5 quoted path literals are rewritten mechanically to their frozen targets: `t2probe-prefix`, `t2probe-scored`, `t5p-scored`, `t2-probe-prereg` → `evidence/probes/…`; `t2-amendment-design` → `evidence/reviews/…` (E-2). The gate must PASS after the move. |
| same file, docstring `:6`–`:7`, comment `:51`–`:53`, throwaway temp-repo fixture `:58`–`:59` (`os.path.join(tmp, "reviews", "unit")`) | fictional/example (illustrative text + an isolated fixture outside the repository) | untouched |
| `R1A-DISPOSITION.md`, `MAPPING-FREEZE.md`, `2026-09-27-reviews-relocation-manifest.md`, and this addendum | intentional historical old-path text (baseline-pinned snapshot records that describe the pre-move tree by design) | relocate by the mechanical rule; the `reviews/…` mentions inside them are NOT rewritten |
| the 4 R1a-hardened harnesses | no consumer of a `reviews/` literal remains | relocate; no rewrite |

**No new runtime or gate consumer exists whose relocation behavior cannot be
preserved by a mechanical path rewrite.** The single executable delta is the
R1a gate itself, and its rewrite is a literal-for-literal path substitution.

## Post-manifest units — home under the freeze's mechanical rule

These three units did not exist at the manifest baseline and so have no master-table
row; the freeze's rule (`reviews/<unit>` → `evidence/{reviews|probes}/<unit>` by
artifact role, basename preserved) places them:

| Unit | Home | Primary role |
|---|---|---|
| `2026-09-27-reviews-relocation-manifest.md` | `evidence/reviews/` | design/audit record |
| `2026-09-27-r1a-e1-harness-path-hardening/` | `evidence/reviews/` | disposition record + its verifier — same shape as `2026-08-16-issue115-closure-state` (E-2 rule: primary role, not the mere presence of a `.py`) |
| `2026-09-27-r2-classification-packaging-mapping/` | `evidence/reviews/` | adjudication record (+ this addendum) |

## Manifest-prescribed internal pointer rewrite (1 site, carried as-is)

The master-table row for `2026-09-27-reviews-relocation-migration-packet.md`
prescribes "update the IA doc's internal pointer if both move". Both move, so
`2026-09-27-target-ia-architecture-design.md:3` (`Builds on the migration
discovery packet (…)`) is rewritten to the packet's new path. It is the only
internal (`reviews/`-to-`reviews/`) cross-reference the frozen record
prescribes; every other internal cross-reference stays byte-identical (frozen
evidence records, several sealed by a `MANIFEST.sha256`; the relocation-record
family above; the 8 disposition-set harnesses).

## Two literal hits that are NOT consumers (a blind grep-and-replace would corrupt them)

- `skills/delegation-and-review/SKILL.md:472` `reviews/styling-ledger.md` —
  fictional example (already adjudicated in the manifest Gap 3). Never rewritten.
- `skills-staging/2026-07-30-starledger-retro/doc-status-sweep-method/SKILL.md:25`
  `review/reviews/reviewed/reviewer` — a word-stem example in prose, not a path.
  It is one of the 67 literal `reviews/` hits and the manifest's existence test
  did not call it out as its own class; recorded here so it is never rewritten.

## Pinned-corpus consumers — stay exactly as they are (6 sites)

`design-pack/tools/project_corpus.py:25,27`, `design-pack/generated/manifest.json:5,13`,
`design-pack/generated/README.md:4`, `design-pack/tools/projection_checks.py:262`
cite `reviews/2026-09-26-phase-b-semantic-publication/…`, which is
LEAVE-IN-PLACE-PINNED (freeze §3/§4). Not rewritten; `design-pack/generated/`
is not regenerated (its source is unchanged).

## Residual old-path allowlist (the post-move sweep must land entirely inside it)

1. the pinned corpus: its own path and the 6 consumer sites above;
2. intentional old→new migration/history prose: the relocation-record family
   (`2026-09-27-reviews-relocation-migration-packet.md`,
   `2026-09-27-target-ia-architecture-design.md`,
   `2026-09-27-reviews-relocation-manifest.md`, `R1A-DISPOSITION.md`,
   `MAPPING-FREEZE.md`, this addendum) and the successor `evidence/README.md`'s
   mention of the pinned corpus / former root;
3. the fictional `reviews/styling-ledger.md`;
4. the non-path word-stem text (`doc-status-sweep-method/SKILL.md:25`);
5. adjudicated historical literals, bytes unchanged: the 8 R1a disposition-set
   harnesses (`non-rerunnable historical artifact`, R1A-DISPOSITION §2) and the
   frozen evidence records' internal cross-references (manifest Internal-Xref);
6. the R1a gate's illustrative docstring/comment and its throwaway temp fixture.

Anything else still pointing at a moved path after the move is a FAIL.

## Verdict

**R3-0 PASS — bounded, mechanical.** The consumer set is the manifest's 68 plus
one post-manifest executable (the R1a gate, REWRITE-AT-MOVE). No integrity
contract was found that the frozen mapping plus mechanical rewrite cannot
preserve. The path-only relocation proceeds under the R3 execution contract.

## Two executable literals adjudicated by rehearsing the post-move sweep (not consumers)

The post-move residual sweep was rehearsed on a staged, uncommitted `git mv` of
the frozen mapping that was then reset before this record was committed (so this
record still precedes any committed move). Its strict rule — any `.py`/`.sh`
under `evidence/` still spelling an old path must be one of the 8 disposition-set
harnesses — surfaced two more executables. Both are adjudicated historical
literals, bytes unchanged:

- `2026-08-08-issue115-stage2/make_manifest.py:52`–`:53` — two
  `reviews/2026-08-08-issue115-stage2/…` strings inside
  `T1_SECURITY["allowed_occurrence_locations"]`: DATA that the one-shot generator
  embedded into the sealed `MANIFEST.json` (`:131`), which is pinned by
  `MANIFEST.sha256` (`25700fd5…`, the package identity cited from
  `skills/cross-model-review/SKILL.md`) and which self-hashes `make_manifest.py`.
  `static_checks.py` locates the sentinel through its own dir-relative set
  (`:198`), never through these strings. Rewriting them would alter a sealed,
  owner-approved package version ("immutable once owner-approved") — forbidden;
  they are not runtime path consumers.
- `2026-09-09-s1-provenance-relocation/verify.py:94` — the regex fragment
  `reviews/2026-` inside Gate 6 (dated-chronology density), a report-only metric
  (not part of the verifier's `status`/`fails`) of an already-executed one-shot
  verifier; the fragment still matches as a substring of the new spelling
  `evidence/reviews/2026-`, so even its report is unchanged. Not a path consumer.

These two join allowlist item 5 explicitly; the sweep script names them line by
line rather than widening the executable rule.
