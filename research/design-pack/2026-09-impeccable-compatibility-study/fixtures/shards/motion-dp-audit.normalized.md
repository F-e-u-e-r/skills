# MOTION reference: Design Pack rules for `audit` (normalized)
<!-- generated projection of 3 sealed Design Pack MOTION rules routed to the audit command; no dial/control -->
## Design Pack motion rules (3)
### MOTION-2006  [default, must_surface, verify=L1]
- Required; surfaced on failure: scroll-position and animation-frame handling in source code, flagged when any of the three patterns is present.
- scope: scroll-position and animation-frame handling in source code
- provenance: Leonxlnx/taste-skill (D2)
### MOTION-4003  [default, must_surface, verify=L1]
- Required; surfaced on failure: any CSS transition declaration, flagged when found.
- scope: any CSS transition declaration
- provenance: Nutlope/hallmark (D3)
### MOTION-4004  [default, contextual, verify=L1]
- Required; surfaced on failure: hover effects applied across the page, flagged when ≥ 2 unrelated elements share the exact same hover-scale value.
- scope: hover effects applied across the page
- provenance: Nutlope/hallmark (D3)
