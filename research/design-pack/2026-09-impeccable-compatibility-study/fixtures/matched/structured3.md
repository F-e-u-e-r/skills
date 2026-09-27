# MOTION reference — structured arm (matched-content ablation)
## Motion rules
- **MOTION-1009** [avoid,warn] — Discouraged: parallax effects — flagged when parallax runs without a reduced-motion guard. Override: prefers-reduced-motion is honored and the effect does not cause disorientation.
- **MOTION-1019** [default,contextual] — Required; surfaced on failure: direction of translate/scale used to express hierarchy — must be satisfied.
- **MOTION-1020** [default,contextual] — Required; surfaced on failure: duration/easing tokens across a product — must be satisfied.
- **MOTION-1023** [default,contextual] — Required; surfaced on failure: directionality of forward/backward navigation animation — must be satisfied.
- **MOTION-2002** [default,must_surface] — Required; surfaced on failure: horizontal scrolling text marquees on one page — flagged when count > 1.
## Runtime control: MOTION_INTENSITY
```yaml control
control_id: DIAL-2002
variable: MOTION_INTENSITY
range: 1-10
baseline: 6
gating:
  - when: "value > 3"
    activates: ['A11Y-2001']
  - when: "value > 4"
    activates: ['MOTION-2003']
  - when: "value > 5"
    activates: ['MOTION-2005']
activation_note: "Activation is governed by the DIAL-2002 predicates: a target rule is active only when its predicate holds for the current MOTION_INTENSITY. A11Y-2001's selector is DIAL-2002, so it is activated at value > 3; its strength 'absolute'/'hard_block' means that once activated it cannot be weakened or overridden (it does not activate below its own threshold)."
```
### Gated target rules
- **A11Y-2001** [strength=absolute, enforcement=hard_block, selector=DIAL-2002] — Hard requirement (non-overridable): any motion/animation effect on the page — flagged when no prefers-reduced-motion handling present.
- **MOTION-2003** [strength=default, enforcement=must_surface, selector=DIAL-2002 (MOTION_INTENSITY > 4)] — Required; surfaced on failure: the shipped page actually moves where motion is claimed (hero entry, scroll-reveal, CTA hover physics). Override: if working motion cannot be delivered in scope, reduce MOTION_INTENSITY to 3 and deliver a clean static page.  override: if working motion cannot be delivered in scope, reduce MOTION_INTENSITY to 3 and deliver a clean static page
- **MOTION-2005** [strength=default, enforcement=contextual, selector=DIAL-2002 (MOTION_INTENSITY > 5)] — Guidance: magnetic pointer-tracking micro-physics and perpetual/looping micro-interactions where they earn their place. Applies for premium, playful, or agency briefs, and sections that benefit (status indicators, live feeds). Override: informational sections stay still — not every card needs an infinite loop.  override: informational sections stay still — not every card needs an infinite loop  condition: premium, playful, or agency briefs, and sections that benefit (status indicators, live feeds)
