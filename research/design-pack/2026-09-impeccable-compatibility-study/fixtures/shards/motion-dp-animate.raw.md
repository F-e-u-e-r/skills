# MOTION reference: Design Pack rules for `animate` (raw)
<!-- generated projection of 9 sealed Design Pack MOTION rules routed to the animate command; no dial/control -->
## Design Pack motion rules (9)
### MOTION-1004  [heuristic, contextual, verify=L2]
- Guidance: number of simultaneously animated elements per view — applied as contextual judgement, not a hard gate.
- scope: number of simultaneously animated elements per view
- provenance: nextlevelbuilder/ui-ux-pro-max-skill (D1)
### MOTION-1005  [default, contextual, verify=none]
- Required; surfaced on failure: easing curve selection by motion type — must be satisfied.
- scope: easing curve selection by motion type
- provenance: nextlevelbuilder/ui-ux-pro-max-skill (D1)
### MOTION-1009  [avoid, warn, verify=L1]
- Discouraged: parallax effects — flagged when parallax runs without a reduced-motion guard. Override: prefers-reduced-motion is honored and the effect does not cause disorientation.
- scope: parallax effects
- override/exception: prefers-reduced-motion is honored and the effect does not cause disorientation
- provenance: nextlevelbuilder/ui-ux-pro-max-skill (D1)
### MOTION-1016  [default, contextual, verify=none]
- Required; surfaced on failure: content replacement within one container — must be satisfied.
- scope: content replacement within one container
- provenance: nextlevelbuilder/ui-ux-pro-max-skill (D1)
### MOTION-1019  [default, contextual, verify=none]
- Required; surfaced on failure: direction of translate/scale used to express hierarchy — must be satisfied.
- scope: direction of translate/scale used to express hierarchy
- provenance: nextlevelbuilder/ui-ux-pro-max-skill (D1)
### MOTION-1023  [default, contextual, verify=L3]
- Required; surfaced on failure: directionality of forward/backward navigation animation — must be satisfied.
- scope: directionality of forward/backward navigation animation
- provenance: nextlevelbuilder/ui-ux-pro-max-skill (D1)
### MOTION-2002  [default, must_surface, verify=L1]
- Required; surfaced on failure: horizontal scrolling text marquees on one page — flagged when count > 1.
- scope: horizontal scrolling text marquees on one page
- provenance: Leonxlnx/taste-skill (D2)
### MOTION-4001  [default, must_surface, verify=L1]
- Required; surfaced on failure: any CSS transition or animation timing function used on UI state changes — flagged when a timing-function value is the literal `ease` keyword, or a bounce/overshoot `cubic-bezier(...)` (a component > 1 in the 2nd or 4th argument), applied to a UI state change.
- scope: any CSS transition or animation timing function used on UI state changes
- provenance: Nutlope/hallmark (D3)
### MOTION-4008  [default, must_surface, verify=L1]
- Required; surfaced on failure: the N12 archetype's banner-retract animation — flagged when height is directly animated/transitioned on retract.
- scope: the N12 archetype's banner-retract animation
- provenance: Nutlope/hallmark (D3)
