# Design Pack runtime reference — MOTION (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 42 record(s).

## MOTION-1001
- **strength:** heuristic
- **scope:** animation duration/timing selection
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: animation duration/timing selection — applied as contextual judgement, not a hard gate.

## MOTION-1002
- **strength:** default
- **scope:** CSS properties animated
- **override:** a property genuinely cannot be expressed via transform/opacity for the intended effect (rare)
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: CSS properties animated — flagged when an animation targets width/height/top/left instead of transform. Override: a property genuinely cannot be expressed via transform/opacity for the intended effect (rare).

## MOTION-1003
- **strength:** heuristic
- **scope:** loading-state feedback matched to expected wait time
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: loading-state feedback matched to expected wait time — applied as contextual judgement, not a hard gate.

## MOTION-1004
- **strength:** heuristic
- **scope:** number of simultaneously animated elements per view
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Guidance: number of simultaneously animated elements per view — applied as contextual judgement, not a hard gate.

## MOTION-1005
- **strength:** default
- **scope:** easing curve selection by motion type
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: easing curve selection by motion type — must be satisfied.

## MOTION-1006
- **strength:** default
- **scope:** purpose of any animation
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: purpose of any animation — must be satisfied.

## MOTION-1007
- **strength:** default
- **scope:** state changes (hover, active, expanded, collapsed, modal) carry appropriate transitions
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: state changes (hover, active, expanded, collapsed, modal) carry appropriate transitions.

## MOTION-1008
- **strength:** default
- **scope:** page/screen transitions
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: page/screen transitions — must be satisfied.

## MOTION-1009
- **strength:** avoid
- **scope:** parallax effects
- **override:** prefers-reduced-motion is honored and the effect does not cause disorientation
- **enforcement:** warn
- **verification:** L1
- **public_expression:** Discouraged: parallax effects — flagged when parallax runs without a reduced-motion guard. Override: prefers-reduced-motion is honored and the effect does not cause disorientation.

## MOTION-1010
- **strength:** heuristic
- **scope:** easing curve family
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: easing curve family — applied as contextual judgement, not a hard gate.

## MOTION-1011
- **strength:** default
- **scope:** paired enter/exit animation durations
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: paired enter/exit animation durations — must be satisfied.

## MOTION-1012
- **strength:** default
- **scope:** list/grid item entrance stagger
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: list/grid item entrance stagger — must be satisfied.

## MOTION-1013
- **strength:** default
- **scope:** transitions between screens/major views
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: transitions between screens/major views — must be satisfied.

## MOTION-1014
- **strength:** default
- **scope:** in-progress animations relative to new user input
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: in-progress animations relative to new user input — must be satisfied.

## MOTION-1015
- **strength:** avoid
- **scope:** user input during an in-progress animation
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Discouraged: user input during an in-progress animation — to be avoided by default.

## MOTION-1016
- **strength:** default
- **scope:** content replacement within one container
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: content replacement within one container — must be satisfied.

## MOTION-1017
- **strength:** default
- **scope:** press feedback on tappable cards/buttons
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: press feedback on tappable cards/buttons — must be satisfied.

## MOTION-1018
- **strength:** default
- **scope:** drag/swipe/pinch gestures
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: drag/swipe/pinch gestures — must be satisfied.

## MOTION-1019
- **strength:** default
- **scope:** direction of translate/scale used to express hierarchy
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: direction of translate/scale used to express hierarchy — must be satisfied.

## MOTION-1020
- **strength:** default
- **scope:** duration/easing tokens across a product
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: duration/easing tokens across a product — must be satisfied.

## MOTION-1021
- **strength:** default
- **scope:** fading elements' minimum opacity while transitioning
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: fading elements' minimum opacity while transitioning — must be satisfied.

## MOTION-1022
- **strength:** default
- **scope:** modal/sheet entrance animation
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: modal/sheet entrance animation — must be satisfied.

## MOTION-1023
- **strength:** default
- **scope:** directionality of forward/backward navigation animation
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: directionality of forward/backward navigation animation — must be satisfied.

## MOTION-1024
- **strength:** default
- **scope:** layout-affecting properties in animation
- **enforcement:** must_surface
- **verification:** L2
- **public_expression:** Required; surfaced on failure: layout-affecting properties in animation — flagged when an animation measurably contributes to layout shift.

## MOTION-1025
- **strength:** default
- **scope:** rapid/repeated state changes mid-animation
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: rapid/repeated state changes mid-animation — must be satisfied.

## MOTION-1026
- **strength:** default
- **scope:** chart entrance animation
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: chart entrance animation — flagged when chart animation has no reduced-motion gating.

## MOTION-1027
- **strength:** heuristic
- **scope:** animation timing token selection in native/mobile app UI
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: animation timing token selection in native/mobile app UI — applied as contextual judgement, not a hard gate.

## MOTION-2001
- **strength:** default
- **scope:** any animation added to the page
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: any animation added to the page — must be satisfied.

## MOTION-2002
- **strength:** default
- **scope:** horizontal scrolling text marquees on one page
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: horizontal scrolling text marquees on one page — flagged when count > 1.

## MOTION-2003
- **strength:** default
- **scope:** the shipped page actually moves where motion is claimed (hero entry, scroll-reveal, CTA hover physics)
- **override:** if working motion cannot be delivered in scope, reduce MOTION_INTENSITY to 3 and deliver a clean static page
- **enforcement:** must_surface
- **verification:** L1
- **selector:** DIAL-2002 (MOTION_INTENSITY > 4)
- **public_expression:** Required; surfaced on failure: the shipped page actually moves where motion is claimed (hero entry, scroll-reveal, CTA hover physics). Override: if working motion cannot be delivered in scope, reduce MOTION_INTENSITY to 3 and deliver a clean static page.

## MOTION-2004
- **strength:** default
- **scope:** GSAP ScrollTrigger pin configuration for sticky-stack and horizontal-pan scroll patterns
- **condition:** a sticky-stack or horizontal-pan scroll pattern is used
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: GSAP ScrollTrigger pin configuration for sticky-stack and horizontal-pan scroll patterns — flagged when the pin trigger's declared start value is left at the ScrollTrigger default rather than tuned to the pattern.

## MOTION-2005
- **strength:** default
- **scope:** magnetic pointer-tracking micro-physics and perpetual/looping micro-interactions where they earn their place
- **condition:** premium, playful, or agency briefs, and sections that benefit (status indicators, live feeds)
- **override:** informational sections stay still — not every card needs an infinite loop
- **enforcement:** contextual
- **verification:** L1
- **selector:** DIAL-2002 (MOTION_INTENSITY > 5)
- **public_expression:** Guidance: magnetic pointer-tracking micro-physics and perpetual/looping micro-interactions where they earn their place. Applies for premium, playful, or agency briefs, and sections that benefit (status indicators, live feeds). Override: informational sections stay still — not every card needs an infinite loop.

## MOTION-2006
- **strength:** default
- **scope:** scroll-position and animation-frame handling in source code
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: scroll-position and animation-frame handling in source code — flagged when any of the three patterns is present.

## MOTION-2007
- **strength:** default
- **scope:** CSS properties targeted by animations/transitions
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: CSS properties targeted by animations/transitions — flagged when an animated/transitioned property is one of top, left, width, or height.

## MOTION-4001
- **strength:** default
- **scope:** any CSS transition or animation timing function used on UI state changes
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: any CSS transition or animation timing function used on UI state changes — flagged when a timing-function value is the literal `ease` keyword, or a bounce/overshoot `cubic-bezier(...)` (a component > 1 in the 2nd or 4th argument), applied to a UI state change.

## MOTION-4002
- **strength:** default
- **scope:** every animation decision in a build
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: every animation decision in a build — must be satisfied.

## MOTION-4003
- **strength:** default
- **scope:** any CSS transition declaration
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: any CSS transition declaration — flagged when found.

## MOTION-4004
- **strength:** default
- **scope:** hover effects applied across the page
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: hover effects applied across the page — flagged when ≥ 2 unrelated elements share the exact same hover-scale value.

## MOTION-4005
- **strength:** default
- **scope:** transitions on UI state changes (buttons, modals, tooltips)
- **override:** reserve overshoot easings for physical interactions such as drag-release
- **exceptions:** physical/drag-release interactions
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: transitions on UI state changes (buttons, modals, tooltips). Override: reserve overshoot easings for physical interactions such as drag-release.

## MOTION-4006
- **strength:** default
- **scope:** an element's :hover rule
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: an element's :hover rule — flagged when count > 1.

## MOTION-4007
- **strength:** default
- **scope:** every transition/animation declaration is intentional and well-formed
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: every transition/animation declaration is intentional and well-formed.

## MOTION-4008
- **strength:** default
- **scope:** the N12 archetype's banner-retract animation
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the N12 archetype's banner-retract animation — flagged when height is directly animated/transitioned on retract.
