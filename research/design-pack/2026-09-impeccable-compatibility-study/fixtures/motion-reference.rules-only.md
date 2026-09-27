# MOTION reference — Design Pack rules-only projection (no control layer)
<!-- deterministic projection of 16 sealed Design Pack MOTION rules; no DIAL-2002, no thresholds, no motion-intensity policy -->
<!-- input_corpus_sha256: 16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b  dp_seal: bd8cb1a -->
<!-- these are unconditional motion rules; they do NOT import A11Y-2001 or any dial-gated rule -->

## Design Pack motion rules (16)
### MOTION-1003  [heuristic, contextual, verify=L3]
- Guidance: loading-state feedback matched to expected wait time — applied as contextual judgement, not a hard gate.
- scope: loading-state feedback matched to expected wait time
- provenance: nextlevelbuilder/ui-ux-pro-max-skill @ dcc40ff5133e (D1)
### MOTION-1004  [heuristic, contextual, verify=L2]
- Guidance: number of simultaneously animated elements per view — applied as contextual judgement, not a hard gate.
- scope: number of simultaneously animated elements per view
- provenance: nextlevelbuilder/ui-ux-pro-max-skill @ dcc40ff5133e (D1)
### MOTION-1005  [default, contextual, verify=none]
- Required; surfaced on failure: easing curve selection by motion type — must be satisfied.
- scope: easing curve selection by motion type
- provenance: nextlevelbuilder/ui-ux-pro-max-skill @ dcc40ff5133e (D1)
### MOTION-1009  [avoid, warn, verify=L1]
- Discouraged: parallax effects — flagged when parallax runs without a reduced-motion guard. Override: prefers-reduced-motion is honored and the effect does not cause disorientation.
- scope: parallax effects
- override/exception: prefers-reduced-motion is honored and the effect does not cause disorientation
- provenance: nextlevelbuilder/ui-ux-pro-max-skill @ dcc40ff5133e (D1)
### MOTION-1016  [default, contextual, verify=none]
- Required; surfaced on failure: content replacement within one container — must be satisfied.
- scope: content replacement within one container
- provenance: nextlevelbuilder/ui-ux-pro-max-skill @ dcc40ff5133e (D1)
### MOTION-1018  [default, contextual, verify=L3]
- Required; surfaced on failure: drag/swipe/pinch gestures — must be satisfied.
- scope: drag/swipe/pinch gestures
- provenance: nextlevelbuilder/ui-ux-pro-max-skill @ dcc40ff5133e (D1)
### MOTION-1019  [default, contextual, verify=none]
- Required; surfaced on failure: direction of translate/scale used to express hierarchy — must be satisfied.
- scope: direction of translate/scale used to express hierarchy
- provenance: nextlevelbuilder/ui-ux-pro-max-skill @ dcc40ff5133e (D1)
### MOTION-1020  [default, contextual, verify=L1]
- Required; surfaced on failure: duration/easing tokens across a product — must be satisfied.
- scope: duration/easing tokens across a product
- provenance: nextlevelbuilder/ui-ux-pro-max-skill @ dcc40ff5133e (D1)
### MOTION-1023  [default, contextual, verify=L3]
- Required; surfaced on failure: directionality of forward/backward navigation animation — must be satisfied.
- scope: directionality of forward/backward navigation animation
- provenance: nextlevelbuilder/ui-ux-pro-max-skill @ dcc40ff5133e (D1)
### MOTION-2002  [default, must_surface, verify=L1]
- Required; surfaced on failure: horizontal scrolling text marquees on one page — flagged when count > 1.
- scope: horizontal scrolling text marquees on one page
- provenance: Leonxlnx/taste-skill @ c184364c5865 (D2)
### MOTION-2006  [default, must_surface, verify=L1]
- Required; surfaced on failure: scroll-position and animation-frame handling in source code — flagged when any of the three patterns is present.
- scope: scroll-position and animation-frame handling in source code
- provenance: Leonxlnx/taste-skill @ c184364c5865 (D2)
### MOTION-4001  [default, must_surface, verify=L1]
- Required; surfaced on failure: any CSS transition or animation timing function used on UI state changes — flagged when a timing-function value is the literal `ease` keyword, or a bounce/overshoot `cubic-bezier(...)` (a component > 1 in the 2nd or 4th argument), applied to a UI state change.
- scope: any CSS transition or animation timing function used on UI state changes
- provenance: Nutlope/hallmark @ 13ac0ec7e148 (D3)
### MOTION-4003  [default, must_surface, verify=L1]
- Required; surfaced on failure: any CSS transition declaration — flagged when found.
- scope: any CSS transition declaration
- provenance: Nutlope/hallmark @ 13ac0ec7e148 (D3)
### MOTION-4004  [default, contextual, verify=L1]
- Required; surfaced on failure: hover effects applied across the page — flagged when ≥ 2 unrelated elements share the exact same hover-scale value.
- scope: hover effects applied across the page
- provenance: Nutlope/hallmark @ 13ac0ec7e148 (D3)
### MOTION-4006  [default, contextual, verify=L1]
- Required; surfaced on failure: an element's :hover rule — flagged when count > 1.
- scope: an element's :hover rule
- provenance: Nutlope/hallmark @ 13ac0ec7e148 (D3)
### MOTION-4008  [default, must_surface, verify=L1]
- Required; surfaced on failure: the N12 archetype's banner-retract animation — flagged when height is directly animated/transitioned on retract.
- scope: the N12 archetype's banner-retract animation
- provenance: Nutlope/hallmark @ 13ac0ec7e148 (D3)
