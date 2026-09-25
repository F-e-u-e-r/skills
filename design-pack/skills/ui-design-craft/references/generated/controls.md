# Design Pack runtime reference — CONTROLS (decision tables + dials) (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 6 record(s).

## DECISION-1001 (decision_table)
- **input_dimension:** the icon's contextual role (semantics follow use, not glyph)
- **selection_mode:** all_matches
- **rows** (ordered):
  - `decorative-beside-text` — when: decorative icon placed beside visible text that already conveys the same meaning → A11Y-1005
  - `meaningful-standalone` — when: meaningful icon with no adjacent visible text duplicating its meaning → A11Y-1006
  - `interactive-control` — when: icon is itself an interactive control (e.g. icon-only button) → A11Y-1007
- **public_expression:** Selector (icon accessibility semantics by role): routes by the icon's contextual role (semantics follow use, not glyph); every matching role applies. Routing: decorative-beside-text → A11Y-1005; meaningful-standalone → A11Y-1006; interactive-control → A11Y-1007.

## DECISION-4001 (decision_table)
- **input_dimension:** which of the four theme-route conditions holds when the theme-route step is reached
- **selection_mode:** first_match
- **rows** (ordered):
  - `studied-dna` — when: the conversation already carries a study diagnosis and the user wants the build derived from that DNA → UX-4009
  - `custom-named` — when: the user selected the custom route — stated directly, or confirmed after Step-1 signal detection fired → COLOR-4001
  - `catalog-named` — when: the user selected the catalog route, or accepted it by not choosing custom → UX-4011
  - `catalog-default` — when: neither route was raised; Step-1 signals did not fire (a plain brief) → UX-4011
- **public_expression:** Selector (theme route): routes by which of the four theme-route conditions holds; the first matching condition applies, in order. Routing: studied-dna → UX-4009; custom-named → COLOR-4001; catalog-named → UX-4011; catalog-default → UX-4011.

## DECISION-4002 (decision_table)
- **input_dimension:** the user's answer to the URL-mode emission attestation question — (a), (b), or (c)
- **selection_mode:** exactly_one
- **rows** (ordered):
  - `own-site` — when: answer (a) -- "my own site" → UX-4035
  - `public-reference-own-brand` — when: answer (b) -- "public reference for own brand" → UX-4035
  - `something-else` — when: answer (c) -- "something else" → UX-4036
- **public_expression:** Selector (study design.md emission attestation dispatch (URL mode)): routes by the user's answer to the URL-mode emission attestation question — (a), (b), or (c); exactly one alternative applies. Routing: own-site → UX-4035; public-reference-own-brand → UX-4035; something-else → UX-4036.

## DIAL-2001 (dial)
- **baseline:** 8
- **range:** 1-10
- **gated_branches** (ordered):
  - when value > 4 → STRUCT-2002
  - when value >= 4 → STRUCT-2003
- **public_expression:** Configuration dial DESIGN_VARIANCE (baseline 8, range 1-10). Threshold branches gate rules: value > 4 → STRUCT-2002; value >= 4 → STRUCT-2003.

## DIAL-2002 (dial)
- **baseline:** 6
- **range:** 1-10
- **gated_branches** (ordered):
  - when value > 3 → A11Y-2001
  - when value > 4 → MOTION-2003
  - when value > 5 → MOTION-2005
- **public_expression:** Configuration dial MOTION_INTENSITY (baseline 6, range 1-10). Threshold branches gate rules: value > 3 → A11Y-2001; value > 4 → MOTION-2003; value > 5 → MOTION-2005.

## DIAL-2003 (dial)
- **baseline:** 4
- **range:** 1-10
- **gated_branches** (ordered):
  - when value > 7 → STRUCT-2017
- **public_expression:** Configuration dial VISUAL_DENSITY (baseline 4, range 1-10). Threshold branches gate rules: value > 7 → STRUCT-2017.
