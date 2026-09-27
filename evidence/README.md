# `evidence/` — evidence and record ledger

This directory holds the project's **evidence and record trail**: review
records, measurement/probe artifacts, and historical campaign material. It is
**not** canonical doctrine.

## What this is / is not

- **Is:** the durable record of how decisions were reached and what was
  measured -- human-written review records, machine-produced probe/eval
  artifacts, and the historical evidence behind claims made elsewhere in the
  repo.
- **Is not:** normative doctrine. The canonical, normative sources are the
  skills' own `SKILL.md` files and `ARCHITECTURE.md` (the stability/architecture
  contract). Where a review record and a canonical source disagree, the
  canonical source wins. A record here is evidence for a claim, never the
  claim's authority.

## Content classes

Entries fall into three semantic classes. Artifact role is the tree's **one
physical axis** (the two subdirectories below); lifecycle is recorded on the
entry, never as a directory (see "Path stability" below):

- **Human review records** (`evidence/reviews/`) -- a person's or a review
  pass's written assessment, disposition, or design note (e.g. a design review,
  a routing-contract design, a threat model).
- **Machine probe / eval artifacts** (`evidence/probes/`) -- the outputs of a
  measurement run: scored probes, eval batches, corpora, and their manifests
  (e.g. the `issue115` activation-probe campaign, the round-5 results). Typically
  large, numerous, and produced mechanically; a campaign's harness, fixtures,
  output, and manifest stay together as one unit.
- **Historical evidence** -- superseded or completed-campaign material retained
  as the record behind a finding: no longer the current state, kept so the claim
  it backs stays checkable. This is a lifecycle status (`current` / `closed` /
  `superseded` / `historical`) marked on the entry; a closed campaign stays
  under its artifact-role home.

A single entry may carry more than one class; an entry that mixes a human
record with a runnable checker gets one home by its primary role, never a
split.

## Authority

A record here is **evidence, not authority**. It supports a claim that lives in
a canonical source (a `SKILL.md`, `ARCHITECTURE.md`, a provenance file); it does
not override one. A citation from a canonical source into `evidence/` is a
provenance pointer -- the canonical text is the rule, the review record is the
why. In-file text in a record claiming "approved" / "final" never confers
authority it does not have.

## Retention

- **Long-term:** any record that backs a still-live claim or a design contract --
  anything cited from a `SKILL.md`, `ARCHITECTURE.md`, a provenance file,
  `README*.md`/`ROADMAP.md`, or gate / design-pack code -- is retained until a
  coordinated migration re-homes it.
- **Campaign artifact:** bulk mechanical probe output from a completed campaign
  may in future be archived, but is retained in place for now.
- Nothing here is deleted casually: evidence behind a shipped claim stays
  checkable.

## Path stability

**Every existing `evidence/` path is a stable contract until a coordinated
migration changes it.** These paths are consumed well beyond this directory --
`ARCHITECTURE.md`, `README*.md`, `ROADMAP.md`, several `SKILL.md` / provenance
files, `.github/` gate code, and `hooks/` (including a hook test) all cite
specific `evidence/` paths. Moving or renaming an existing path is therefore
**not** a local edit: it is a repo-wide, path-only migration that must update
every consumer and keep the canonical checks green. Do not relocate an existing
evidence path outside such a migration.

The design-pack corpus (`reviews/2026-09-26-phase-b-semantic-publication/`,
read by the `design-pack/` corpus loader) is canonical machine-consumed data,
not evidence. It is the only tracked content still under the former `reviews/`
root, pinned at that path until its own dedicated relocation to a canonical-data
surface; do not move it with, or into, this tree.

## Placing new evidence

When you add a new record:

- **Name its class** -- make it clear (in the entry's own heading/README or its
  containing note) whether it is a human review record, a machine probe
  artifact, or historical evidence, and mark its lifecycle status.
- Put human review records under `evidence/reviews/` and machine probe / eval
  artifacts under `evidence/probes/`, grouped under a dated campaign directory,
  as the existing `2026-08-*` entries are, so bulk output stays separable from
  human records.
- Do not add new material under the former `reviews/` root; it is retained only
  for the pinned corpus above.
