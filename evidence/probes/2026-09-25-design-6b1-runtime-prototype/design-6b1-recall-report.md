# DESIGN-6B1 Recall Report — PUBLIC PROJECTION

**Status:** DERIVED PROTOTYPE — public projection. Reproducible via `python3 design-6b1-loader-prototype.py` (reads the structural `design-6b1-manifest.json` in this directory). Mints no ID, mutates no registry, changes no sealed byte. `[verified: ran design-6b1-loader-prototype.py; exit 0]`

> This package is a sanitized **projection**: per-rule upstream-sourced `scope` prose and the `trigger` field are projected out of the manifest (full `scope` retained only for the pack's own fence-clean D5-synthesized rules). The MANDATORY invariants below are **scope-independent**; only the non-mandatory non-gate-recall / generation-payload figures differ from the internal artifact, because positive category retrieval here falls back to category-keyword matching where per-rule scope is absent.

## EXIT GATE — the mandatory invariants

| metric | value |
|---|---|
| population accounting | **448 / 448** |
| kernel payload (always-resident floor) | **133 rules · 137075 B · ~34268 tok** |
| full-load 448 (oracle ceiling) | 448 rules · 399528 B · ~99882 tok |
| hard_block / must_surface (gate population) | **7 / 125 (= 132 gates)** |
| keyword-tier gate leakage | **0** |
| full-load-oracle hard_block/must_surface miss | **0** on all 6 fixtures |
| mandatory regressions | **16/16 PASS** |

The always-resident floor drops **80354 → 34268 tok (−57%)** vs the DESIGN-6A always-on baseline (347 rules · 321417 B). L3 critique (~15365 tok) is deferred to the render pass.

## 1. Per-fixture dual-run (public loader)

| fixture | GEN rules · ~tok | oracle gates | loader covers | **MISS** | active-check recall | non-gate recall |
|---|---|--:|--:|:--:|:--:|:--:|
| **F1** generic marketing landing page | 323 · ~74919 | 131 | 131 | **0** | 138/138 | 182/214 |
| **F2** minimal / restrained brand site | 279 · ~66305 | 128 | 128 | **0** | 135/135 | 143/214 |
| **F3** high-density data dashboard | 256 · ~61163 | 132 | 132 | **0** | 139/139 | 114/214 |
| **F4** hallmark study / build-from-DNA | 309 · ~73197 | 131 | 131 | **0** | 138/138 | 163/214 |
| **F5** icon-free long-form article | 312 · ~72255 | 128 | 128 | **0** | 135/135 | 175/214 |
| **F6-ADV** adversarial semantic-mismatch (fetch-rebuild) | 177 · ~43836 | 131 | 131 | **0** | 138/138 | 36/214 |

**Total hard_block/must_surface miss across all fixtures: 0.** Every fixture recalls 100% of applicable active checks. Non-gate recall is <100% by design (that tier holds only checkless generation-constraints + candidate-only advisory, where a positive-retrieval miss provably drops NO enforcement); the public projection's non-gate figures are lower than the internal artifact's because scope-token retrieval is projected out — this changes no gate.

## 2. Why zero-miss is structural (not fixture luck)

Every non-selector `hard_block`/`must_surface` (125) is UNCONDITIONALLY kernel-resident; the 7 selector-gated gates load iff their sealed dial/icon-role selector fires (= exactly when applicable, §8.3 step-0). **No gate lives in the keyword-retrievable tier** (leakage = 0), so no prose rewording — and no scope projection — can drop one. Oracle-gates ⊆ (kernel ∪ selector-fired) = loader-gates, for every possible task.

## 3. Mandatory regressions (Constraint F)

| # | assertion | expected | actual | |
|--:|---|---|---|:--:|
| 1 | TC1 INTERACT-6001 enf=must_surface & tier=kernel | `['must_surface', 'kernel']` | `['must_surface', 'kernel']` | PASS |
| 2 | TC1.P1/P2 scope names form-inputs AND interactive chart elements | `[True, True]` | `[True, True]` | PASS |
| 3 | TC1.P3/N1 exactly ONE active L2 check, ZERO candidate (no promotion) | `[1, 'L2', 0]` | `[1, 'L2', 0]` | PASS |
| 4 | TC1.N3 A11Y-1022 kept SEPARATE (own rule, not folded) | `True` | `True` | PASS |
| 5 | TC2 UX-4031 enf=contextual & checks:[] (N1 no synthesized proxy) | `['contextual', 0]` | `['contextual', 0]` | PASS |
| 6 | TC2 tier=kernel (safety boundary resists adversarial keyword-avoidance) | `kernel` | `kernel` | PASS |
| 7 | TC2 UX-4031 present in ADVERSARIAL F6 generation set | `True` | `True` | PASS |
| 8 | TC2.N2 UX-4030 (SSRF) NOT revived | `False` | `False` | PASS |
| 9 | TC3 MOTION-1001 heuristic, checks:[], enf=contextual (no duration-band gate) | `['heuristic', 0, 'contextual']` | `['heuristic', 0, 'contextual']` | PASS |
| 10 | TC3 tier=retrievable-category (heuristic guidance; a miss drops NO gate) | `retrievable-category` | `retrievable-category` | PASS |
| 11 | TC3.N1/N2 no Emil rule & no synthesized duration rule minted | `[False, False]` | `[False, False]` | PASS |
| 12 | A2001 selector_fires MI=6 True / MI=2 False | `[True, False]` | `[True, False]` | PASS |
| 13 | A2001 in oracle(F1 MI6)=applicable / NOT in oracle(F2 MI2)=correctly-absent | `[True, False]` | `[True, False]` | PASS |
| 14 | A2001 hard_block & loader COVERS it when applicable (F1) | `['hard_block', True]` | `['hard_block', True]` | PASS |
| 15 | C4003 avoid + HAS active check + enf=warn (NOT hard_block/must_surface) | `['avoid', True, 'warn']` | `['avoid', True, 'warn']` | PASS |
| 16 | C4003 tier=kernel (warn kept resident; strength/check separation survives) | `kernel` | `kernel` | PASS |

**16/16 PASS.**
