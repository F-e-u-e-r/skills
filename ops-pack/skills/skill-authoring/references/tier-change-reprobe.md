# Tier-change re-probe — the three-bucket triage

The always-loaded trigger and kernel live in `SKILL.md` §7, the bullet
"The tier the file is written for has changed — every fold verdict taken at
the old tier is a hypothesis again, not a verdict." That kernel points here.
Load this when a tier-change has fired the §7 bullet and you are about to
triage the file's rules. A file whose audience tier moved while its verdicts
did not can carry the quirks of every executor it has instructed, and this
triage exists to clear that. This reference holds the three-bucket
definitions, the incident-backing fence, and the re-probe mechanics the
kernel names but does not carry.

## The three buckets

Before any verdict is cited again, triage every rule in the file into exactly
one bucket:

- **(1) Context the executor cannot derive** — paths, live tool names,
  environment facts: keep, not probed.
- **(2) Workflow control** — "do it this way / in this order / check these N
  things", which a more capable executor may do unaided: the re-probe set.
- **(3) The load-bearing class §1's pruning guardrail already defines**
  (safety, verification, fail-closed, authorization-boundary, and the gates
  it lists): keep, and never probed by letting a live executor cross one to
  see whether it would — that run IS the incident. A sandboxed probe of a
  bucket-(3) rule is the user's call, asked before the run (the opener's
  ask-first rule, extended here to the whole bucket-(3) load-bearing class —
  not only its destructive / spending / publishing subset).

This partitions by necessity, not truth — §3's world-fact-first staleness
audit still applies to bucket (1) unchanged.

## The incident-backing fence

A rule is in bucket (3) by its CONTENT — because it is a safety,
verification, fail-closed, or authorization-boundary rule — and a rule in
that class by content **never leaves (3)**, incident or not. Only a rule
whose SOLE claim to bucket (3) is a dated incident backing it — one that does
NOT independently meet any of those four axes by content — may move to (2),
and only if that incident was the old executor's own quirk rather than a
standing hazard. Cannot tell whether the rule meets a §1 axis by content, or
cannot tell whether the incident was a quirk → it stays in (3); the triage
fails closed exactly as §1's guardrail requires ("when you cannot tell
whether a clause is load-bearing on one of these axes, treat it as
load-bearing").

This closes the demotion path a weaker executor would otherwise open: a rule
that is BOTH fail-closed / verification by content AND incident-backed — for
example "ack the webhook before durably recording it," backed by a
post-2xx-crash incident — stays in (3) on its content, and cannot be
reclassified to (2) by judging its incident "a quirk." Bucket (2) is the
re-probe set and a bare pass there makes a delete candidate; a
content-load-bearing rule must reach neither.
❌ "the crash was just the old model's quirk, so this ack-before-record rule
is workflow control now — re-probe it" — it is fail-closed by content; the
incident is not its only claim to (3), so it never leaves (3).

## Re-probe bucket (2)

Re-probe bucket (2) by the pair above (§7's bare-vs-ruled probe bullet), at
the new audience tier (for a multi-tier audience, the weakest tier it must
protect, as that bullet requires), rules already carrying a verdict first —
they survived one measurement; find out whether they survive this one — and
read each pair by the same table. A bare pass at the new tier makes a delete
candidate, never a deletion: deletion is its own edit, one rule per commit,
after the evidence is read, under the opener's ask-first rule.

## Bind the result, and Done

Bind the result to a surface the next pass reads (§3's binding rule): the
file's change record carries the line

> bucket triage at tier `<T>`, `<date>`; bucket-(3) rules probed live: `<each one named, or none>`

and a bucket-(2) rule with no verdict at the current tier is listed there as
queued.

Done when that line exists, every rule is bucketed, and every bucket-(2) rule
carries a current-tier verdict or a queue entry.
