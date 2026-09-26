# Target IA architecture — adjudicated design (no relocation authorized)

> **Design / adjudication record. Target shape decided; NO `git mv`, NO migration authorized.** Builds on the migration discovery packet (`reviews/2026-09-27-reviews-relocation-migration-packet.md`, merged `cb0b4cb`). The exhaustive migration manifest (old->new map) is the NEXT step, built against this shape.

## The core model: separate three concepts the class-count model conflated

A 4-way `{reviews, probes, historical, corpora}` split mixed three unrelated
axes and would force unanswerable questions ("a *closed probe* -> `probes/` or
`historical/`?"). The target IA separates them:

- **Authority** — what is canonical vs derived/evidence. `skills/` + architecture
  doctrine are canonical instruction; the **corpus** is canonical
  machine-consumed semantic data. Evidence is not authority.
- **Artifact role** — the ONE physical classification axis under the evidence
  trail: **review** (human reasoning / adjudication / design) vs **probe**
  (measurement campaigns + runnable evidence units).
- **Lifecycle** — `current` / `closed` / `superseded` / `historical` is
  **metadata/status, not a sibling directory**. A superseded item stays under
  its artifact-role home, marked historical; it does not migrate to a
  `historical/` folder.

```
Canonical authority
├── skills/ + ARCHITECTURE.md doctrine        (canonical instruction)
└── corpus/                                   (canonical machine-consumed data)

Evidence trail
└── evidence/
    ├── reviews/   human reasoning / adjudication / design records
    └── probes/    measurement campaigns + runnable evidence units

Lifecycle (current/closed/superseded/historical) = metadata on an entry,
NOT a directory axis.
```

## Target tree (north star — ownership, not this-round authorization)

```
corpus/
└── design-pack/
    ├── public_records.json          # canonical Phase-B corpus (design-pack semantic authority)
    └── THIRD_PARTY_NOTICES.md
evidence/
├── README.md                        # (successor to today's reviews/README.md contract)
├── reviews/                         # human review / adjudication / design records
└── probes/                          # campaigns: harness + fixtures + scored output + manifest, each as a UNIT
```

`historical`/`closed` are recorded per entry, never as a peer directory.

## Dispositions

- **Corpus (`public_records.json`) — rightful home is a canonical-data surface
  SEPARATE from `evidence/`** (it is production input / semantic authority, not
  a decision record). This is a final architecture judgment. The **literal path
  `corpus/design-pack/` is a candidate, pending a packaging-surface gate**
  (below). **This-round migration strategy: LEAVE IN PLACE, pinned** — the
  corpus is the packet's highest Tier-1 coupling (fixed constants in
  `project_corpus.py`, generated manifests, the `projection_checks` negative
  guard, a SHA pin). Target shape != migration strategy: its rightful home is
  named, its move is deferred to a dedicated, separately-authorized corpus
  relocation.
- **Threat model -> `evidence/reviews/`** — its primary role is a human
  design/review artifact.
- **Closed scored campaign -> `evidence/probes/`, harness + fixtures + output +
  manifest moved as ONE unit.** "Closed" is lifecycle; "probe" is its identity.
  It does NOT go to a `historical/` bucket. The self-relative traversal /
  depth dependency the packet found means splitting the unit or changing its
  depth can break historical re-runnability — preserve the unit and its depth.

## Added gate — corpus literal-path packaging surface (before fixing `corpus/design-pack/`)

`opus-pack`'s plugin `source` is `"./"` (repo root) and `design-pack`'s is
`"./design-pack"`. Before the corpus literal path is fixed, confirm what a
top-level `corpus/` (and, more broadly, an `evidence/` root) does to BOTH
plugins' packaging/install surface — i.e. what a plugin install actually pulls
in from the repo root. This does not change the "corpus is not evidence"
judgment; it decides the safest physical location. **This gate also applies to
the `evidence/` root** — verify the reorganization does not change the
published package surface before any relocation.

## Compatibility policy

- **Tier-1 (runtime/gate-critical):** corpus constants + generated + negative
  guard, README markdown links, the skill-vetting hook emit + test assertion.
  Either one coordinated lockstep update, or leave-in-place (the corpus takes
  leave-in-place this round). No half-moved Tier-1 path.
- **Tier-2/3 (doc/provenance pointers):** update directly at move time; most
  warrant no alias. A transitional alias is justified only for a path with a
  known external deep-link, with a stated sunset condition (a forwarding layer
  is a second path surface — never let a transitional state become permanent).

## Execution gates (carried from the packet; apply to any authorized migration)

- Path-only; no semantic edits in the migration commit.
- Canonical battery green BEFORE and AFTER (checks.py + test-derived-checks +
  all hook suites + gate-template).
- Generated artifacts are REGENERATED from their source, never hand-edited.
- A historical harness that will not stay runnable at its new location gets an
  explicit disposition (documented), never a silent break.
- Migration requires its own authorization; this record authorizes none.

## Manifest classification rule (for Q4)

Classify each path in order: **authority/ownership first** (is it canonical
data -> `corpus/`, or canonical instruction -> stays), **artifact role second**
(review vs probe -> `evidence/…`), **lifecycle last** (recorded as metadata).
Never let "historical" compete with "probe" for a directory.

## Next

Q4 — build the exhaustive old->new migration manifest against this shape,
closing the packet's three discovery gaps (per-harness relative-path audit;
re-verify no other runtime reads the paths; illustrative-vs-real citation
split). Recommended as a bounded fresh-context sweep. No `git mv` until a
migration is separately authorized on that manifest.
