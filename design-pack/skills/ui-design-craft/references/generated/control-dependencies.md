# Design Pack runtime reference — CONTROL DEPENDENCIES (cross-domain rules required by this skill's controls) (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 2 record(s).

## MOTION-2003
- **strength:** default
- **scope:** the shipped page actually moves where motion is claimed (hero entry, scroll-reveal, CTA hover physics)
- **override:** if working motion cannot be delivered in scope, reduce MOTION_INTENSITY to 3 and deliver a clean static page
- **enforcement:** must_surface
- **verification:** L1
- **selector:** DIAL-2002 (MOTION_INTENSITY > 4)
- **public_expression:** Required; surfaced on failure: the shipped page actually moves where motion is claimed (hero entry, scroll-reveal, CTA hover physics). Override: if working motion cannot be delivered in scope, reduce MOTION_INTENSITY to 3 and deliver a clean static page.

## MOTION-2005
- **strength:** default
- **scope:** magnetic pointer-tracking micro-physics and perpetual/looping micro-interactions where they earn their place
- **condition:** premium, playful, or agency briefs, and sections that benefit (status indicators, live feeds)
- **override:** informational sections stay still — not every card needs an infinite loop
- **enforcement:** contextual
- **verification:** L1
- **selector:** DIAL-2002 (MOTION_INTENSITY > 5)
- **public_expression:** Guidance: magnetic pointer-tracking micro-physics and perpetual/looping micro-interactions where they earn their place. Applies for premium, playful, or agency briefs, and sections that benefit (status indicators, live feeds). Override: informational sections stay still — not every card needs an infinite loop.
