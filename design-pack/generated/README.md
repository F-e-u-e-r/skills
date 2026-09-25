# design-pack/generated/ — GENERATED, do not hand-edit

Deterministic projection of the canonical Phase-B semantic corpus
(`reviews/2026-09-26-phase-b-semantic-publication/public_records.json`,
SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`,
merged `44f10443c16e926515af86ebdd1d52e003ed98cc`). These files are
machine-generated and CI-verifiable — never hand-edit; edit the canonical corpus
and regenerate.

- `runtime.json` — 454 runtime records (443 rule, 5 synthesized_rule, 3 decision_table, 3 dial). **Zero evidence/conflict.**
- `projection-support.json` — 88 projection-support-only records (85 evidence, 3 conflict). Not required for ordinary skill execution.
- `manifest.json` — schema/version, canonical corpus SHA + merge SHA, kind policy, populations, per-artifact SHA-256, attribution linkage.
- `skill-reachability.json` — which production skill(s) reach each of the 454 runtime records.
- agent-consumption shards are mirrored SKILL-LOCALLY at `design-pack/skills/<skill>/references/generated/*.md` (per-domain + `controls.md`; deterministic copies, byte duplication is not context duplication).
- `local-extensions.json` — pack-local production requirements NOT in the corpus (authority=pack-local-extension, no Phase-B provenance).

Regenerate: `python3 design-pack/tools/project_corpus.py`
Verify (two-sided gates): `python3 design-pack/tools/test_projection_checks.py`

`effective_semantics` is copied verbatim (no reinterpretation); record-level
provenance and d5_disposition are dropped (retained in the canonical corpus +
`design-pack/THIRD_PARTY_NOTICES.md`). `synthesized_rule.derived_from` and
`conflict.participants` are lineage to sources consumed into synthesis (not live
records).
