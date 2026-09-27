# DESIGN-6B1 — Derived Runtime Retrieval/Enforcement Prototype

**Status: DERIVED PROTOTYPE — not production-ready, not a sealed artifact.**

DESIGN-6B1 is a derived runtime prototype: a structural, per-rule classification of the
design pack's reconciled rule set into a 4-level enforcement action and a retrieval tier,
plus the inert validation machinery that proves the resulting selective-loading scheme
never drops an enforcement gate.

This publication contains **derived runtime classifications and validation machinery, not
mirrors of upstream source repositories.** The canonical mining and reconciliation source
artifacts (the DESIGN-0 synthesis contract and the sealed DESIGN-1..5 extraction/reconciliation
documents) are maintained separately and are **not redistributed here.**

**DESIGN-6 production integration is not complete.** This is the B1 retrieval/enforcement
prototype checkpoint only — no production loader, no pack integration, no sealed runtime mapping.

## Contents

| file | what it is |
|---|---|
| `design-6b1-manifest.json` | Structural per-rule manifest (448 rules): enforcement action, retrieval tier, verification layer, check counts, selector dependency, measured byte span, lineage labels. **Projection** — see below. |
| `design-6b1-loader-prototype.py` | Inert loader + full-load-oracle dual-run harness. No network, no writes; reads the manifest, prints the proof, exits 0/1. |
| `design-6b1-recall-report.md` | Acceptance results produced by running the loader against this exact manifest. |

Reproduce: `python3 design-6b1-loader-prototype.py`

## Validated invariants (this exact public package)

- Population accounting: **448 / 448** reconciled rules.
- Always-resident kernel floor: **133 rules · ~34268 tok** (−57% vs the 347-rule / ~80354-tok always-on baseline).
- Enforcement distribution: **7 hard_block · 125 must_surface · 7 warn · 309 contextual**.
- Gate population (hard_block + must_surface): **132**.
- **Keyword-tier gate leakage: 0** — no enforcement gate lives in the keyword-retrievable tier.
- **Full-load-oracle hard_block/must_surface miss: 0** on all fixtures.
- Mandatory regression suite: **16 / 16 PASS**.

The zero-miss property is **structural**: every non-selector gate is unconditionally
kernel-resident, and every selector-gated gate loads exactly when its sealed dial/icon-role
selector fires. Governance correctness therefore does not depend on lexical-retrieval recall.

## Projection (what is and is not published here)

The public manifest is a **projection** of a richer internal artifact:

- The `trigger` field is projected out of every rule.
- Per-rule `scope` prose is projected out, **except** for the pack's own D5-synthesized rules
  whose scope text contains no upstream evidence material.

This avoids redistributing upstream-sourced scope expression. The mandatory invariants above
are **scope-independent** (gate coverage derives from tier + sealed selectors, never from
keyword/scope retrieval). Only the non-mandatory non-gate-recall and generation-payload figures
differ from the internal artifact, because the loader's positive category retrieval falls back
to category-keyword matching where per-rule scope is absent.

## Provenance

Derived — by read-only classification, minting no ID and changing no sealed byte — from the
design pack's sealed governance set. Lineage (SHA-256 of each sealed source, recorded for
traceability; the sealed documents themselves are not included here):

| sealed source | sha-256 (prefix) |
|---|---|
| DESIGN-0 synthesis contract | `2244f317` |
| DESIGN-1 (ui-ux-pro-max) | `dcdb38f3` |
| DESIGN-2 (taste-skill) | `4bb58435` |
| DESIGN-3 (hallmark) | `42ff6484` |
| DESIGN-4 (awesome-design-md) | `d2ca056d` |
| DESIGN-5 (reconciliation) | `4c6a34e7` |
| design-id-registry.yaml | `69c377f6` |
| design-0-errata.yaml | `9dd6dddf` |

### Upstream sources and licenses

The sealed design corpus was mined from the following third-party skills, each at a pinned
commit. Licenses were verified against each repository's `LICENSE` file at the pinned commit
(not inferred from repository visibility):

| upstream repo | pinned commit | license (verified at pin) |
|---|---|---|
| `nextlevelbuilder/ui-ux-pro-max-skill` | `dcc40ff5` | MIT |
| `Leonxlnx/taste-skill` | `c184364c` | MIT |
| `Nutlope/hallmark` | `13ac0ec7` | MIT |
| `VoltAgent/awesome-design-md` | `f6961238` | MIT |

This package redistributes derived runtime metadata, not the upstream source material. Upstream
copyright remains with the respective authors under the MIT License.
