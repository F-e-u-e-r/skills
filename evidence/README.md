# `evidence/` — evidence and record ledger

This directory holds the project's **evidence and record trail**: review
records, measurement/probe artifacts, and historical campaign material. It is
**not** canonical doctrine.

Two top-level summary pages index this trail: [`ops-pack-evaluation.md`](ops-pack-evaluation.md) (how the Ops Pack is tested, with links into the records) and [`provenance.md`](provenance.md) (full source history and acknowledgements). The dated records themselves live under the three subdirectories described below.

## What this is / is not

- **Is:** the durable record of how decisions were reached and what was
  measured -- human-written review records, machine-produced probe/eval
  artifacts, and preserved reference and operating libraries behind claims made elsewhere in the
  repo.
- **Is not:** normative doctrine. The canonical, normative sources are the
  skills' own `SKILL.md` files and `ARCHITECTURE.md` (the stability/architecture
  contract). Where a review record and a canonical source disagree, the
  canonical source wins. A record here is evidence for a claim, never the
  claim's authority.

## Content classes

Entries fall into three semantic classes. Artifact role is the tree's **one
physical axis** (the three subdirectories below); lifecycle is recorded on the
entry, never as a directory (see "Path stability" below):

- **Human review records** (`evidence/reviews/`) -- a person's or a review
  pass's written assessment, disposition, or design note (e.g. a design review,
  a routing-contract design, a threat model).
- **Machine probe / eval artifacts** (`evidence/probes/`) -- the outputs of a
  measurement run: scored probes, eval batches, corpora, and their manifests
  (e.g. the `issue115` activation-probe campaign, the round-5 results). Typically
  large, numerous, and produced mechanically; a campaign's harness, fixtures,
  output, and manifest stay together as one unit.
- **Preserved reference / operating libraries** (`evidence/libraries/`) -- a
  retained reference or operating library kept for the record: distilled skill
  libraries, campaign playbooks, and similar operating material that is neither a
  human review record nor a machine probe artifact (e.g. the `2026-07-30-*`
  retiring-architect / campaign libraries). Staged, not installed -- preserved as
  evidence, never loaded as a production skill.

A single entry may carry more than one class; an entry that mixes a human
record with a runnable checker gets one home by its primary role, never a
split. **Lifecycle status** -- `staged`, `current`, `closed`, `superseded`,
`historical`, `declined` -- is recorded on the entry, never as a directory: a
closed, superseded, historical, or declined entry stays under its artifact-role
home (`reviews/`, `probes/`, or `libraries/`).

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

The design-pack corpus (`corpus/design-pack/`, read by the `design-pack/`
corpus loader) is canonical machine-consumed data, not evidence; it lives on its
own canonical-data surface, never in this tree. The former `reviews/` root holds
no tracked content.

## Placing new evidence

When you add a new record:

- **Name its class** -- make it clear (in the entry's own heading/README or its
  containing note) whether it is a human review record, a machine probe
  artifact, or a preserved reference / operating library, and mark its lifecycle status.
- Put human review records under `evidence/reviews/`, machine probe / eval
  artifacts under `evidence/probes/`, and preserved reference / operating
  libraries under `evidence/libraries/`, grouped under a dated campaign
  directory, as the existing `2026-08-*` entries are, so bulk output stays
  separable from human records.
- Do not add new material under the former `reviews/` root.
