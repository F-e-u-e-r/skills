# Design Pack runtime reference — INTERACT (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 75 record(s).

## INTERACT-1002
- **strength:** default
- **scope:** gaps between adjacent touch targets
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: gaps between adjacent touch targets — must be satisfied. Override:

## INTERACT-1003
- **strength:** default
- **scope:** primary interactive affordances
- **override:** an interface verified to be mouse/trackpad-only with no touch or keyboard-primary usage
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: primary interactive affordances — must be satisfied. Override: an interface verified to be mouse/trackpad-only with no touch or keyboard-primary usage.

## INTERACT-1004
- **strength:** default
- **scope:** buttons triggering async operations
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: buttons triggering async operations — must be satisfied.

## INTERACT-1005
- **strength:** default
- **scope:** error conditions arising from a user action
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: error conditions arising from a user action — must be satisfied.

## INTERACT-1006
- **strength:** default
- **scope:** clickable elements on web
- **condition:** web/desktop pointer context
- **exceptions:** native form controls that already carry a platform pointer affordance
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: clickable elements on web — flagged when a clickable element lacks cursor:pointer. Applies when web/desktop pointer context.

## INTERACT-1007
- **strength:** avoid
- **scope:** main content area gesture handling
- **override:** the surface is itself a horizontally-paged/carousel component where horizontal swipe is the primary, clearly-affianced interaction
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Discouraged: main content area gesture handling — to be avoided by default. Override: the surface is itself a horizontally-paged/carousel component where horizontal swipe is the primary, clearly-affianced interaction.

## INTERACT-1008
- **strength:** default
- **scope:** web touch input
- **condition:** web/touch context
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: web touch input — flagged when tappable element has no touch-action declaration and suffers the legacy 300ms delay. Applies when web/touch context.

## INTERACT-1009
- **strength:** default
- **scope:** platform-standard gestures (swipe-back, pinch-zoom, etc.)
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: platform-standard gestures (swipe-back, pinch-zoom, etc.) — must be satisfied.

## INTERACT-1010
- **strength:** avoid
- **scope:** overriding OS-level system gestures (Control Center, back-swipe, and the like)
- **override:** an explicit, user-consented full-screen, kiosk, or game mode that requires suppressing system gestures
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Discouraged: overriding OS-level system gestures (Control Center, back-swipe, and the like). Override: an explicit, user-consented full-screen, kiosk, or game mode that requires suppressing system gestures.

## INTERACT-1011
- **strength:** default
- **scope:** pressable elements
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: pressable elements — must be satisfied.

## INTERACT-1012
- **strength:** heuristic
- **scope:** confirmations and important native-app actions
- **condition:** native/mobile platform with haptic capability
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: confirmations and important native-app actions — applied as contextual judgement, not a hard gate. Applies when native/mobile platform with haptic capability.

## INTERACT-1013
- **strength:** avoid
- **scope:** critical actions
- **override:** the gesture is supplemented by a documented visible-control fallback for the same action
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Discouraged: critical actions — to be avoided by default. Override: the gesture is supplemented by a documented visible-control fallback for the same action.

## INTERACT-1014
- **strength:** default
- **scope:** small icons and thin edge affordances
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: small icons and thin edge affordances — must be satisfied.

## INTERACT-1015
- **strength:** default
- **scope:** swipe-actionable list/card items
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: swipe-actionable list/card items — must be satisfied.

## INTERACT-1016
- **strength:** default
- **scope:** draggable elements
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: draggable elements — must be satisfied.

## INTERACT-1017
- **strength:** default
- **scope:** hover/pressed/disabled interactive states
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: hover/pressed/disabled interactive states — must be satisfied.

## INTERACT-1018
- **strength:** default
- **scope:** input field labelling
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: input field labelling — flagged when an input relies on placeholder text as its only label.

## INTERACT-1019
- **strength:** default
- **scope:** field-level validation error display
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: field-level validation error display — flagged when field error is not adjacent, or lacks the aria-describedby link.

## INTERACT-1020
- **strength:** default
- **scope:** form submission
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: form submission — must be satisfied.

## INTERACT-1021
- **strength:** default
- **scope:** required form fields
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: required form fields — must be satisfied.

## INTERACT-1022
- **strength:** default
- **scope:** views/lists with no content
- **condition:** no content present
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: views/lists with no content — must be satisfied. Applies when no content present.

## INTERACT-1023
- **strength:** default
- **scope:** toast notifications
- **override:** a toast carries an action the user may still need to invoke (e.g. Undo), which the undo-support rule implies should outlive a bare timed auto-dismiss
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: toast notifications — must be satisfied. Override: a toast carries an action the user may still need to invoke (e.g. Undo), which the undo-support rule implies should outlive a bare timed auto-dismiss.

## INTERACT-1024
- **strength:** default
- **scope:** destructive actions
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: destructive actions — flagged when a destructive action executes with no confirmation.

## INTERACT-1025
- **strength:** default
- **scope:** complex form inputs
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: complex form inputs — must be satisfied.

## INTERACT-1026
- **strength:** default
- **scope:** disabled UI elements
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: disabled UI elements — flagged when an element is styled disabled but lacks the semantic attribute.

## INTERACT-1027
- **strength:** default
- **scope:** complex option sets presented to the user
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: complex option sets presented to the user — must be satisfied.

## INTERACT-1028
- **strength:** default
- **scope:** field validation timing
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: field validation timing — flagged when an error is shown mid-keystroke before the field loses focus.

## INTERACT-1029
- **strength:** default
- **scope:** email/phone/numeric input fields
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: email/phone/numeric input fields — flagged when a semantic field (email/phone/number) uses a generic text type.

## INTERACT-1030
- **strength:** default
- **scope:** password input fields
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: password input fields — flagged when a password field has no visibility toggle.

## INTERACT-1031
- **strength:** default
- **scope:** form field autofill
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: form field autofill — flagged when a common field type (name/email/address/etc.) has no autocomplete attribute.

## INTERACT-1032
- **strength:** default
- **scope:** destructive or bulk actions
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: destructive or bulk actions — must be satisfied.

## INTERACT-1033
- **strength:** default
- **scope:** completed user actions
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: completed user actions — must be satisfied.

## INTERACT-1034
- **strength:** default
- **scope:** error message content
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: error message content — must be satisfied.

## INTERACT-1035
- **strength:** default
- **scope:** multi-step flows
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: multi-step flows — must be satisfied.

## INTERACT-1036
- **strength:** default
- **scope:** long forms
- **condition:** form is long / multi-field
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: long forms — must be satisfied. Applies when form is long / multi-field.

## INTERACT-1037
- **strength:** default
- **scope:** sheets/modals with unsaved changes
- **condition:** unsaved changes are present
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: sheets/modals with unsaved changes — must be satisfied. Applies when unsaved changes are present.

## INTERACT-1038
- **strength:** default
- **scope:** error message wording
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: error message wording — must be satisfied.

## INTERACT-1039
- **strength:** default
- **scope:** related form fields
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: related form fields — must be satisfied.

## INTERACT-1040
- **strength:** default
- **scope:** read-only form fields
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: read-only form fields — must be satisfied.

## INTERACT-1042
- **strength:** default
- **scope:** destructive action styling
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: destructive action styling — must be satisfied.

## INTERACT-1043
- **strength:** default
- **scope:** request timeouts
- **condition:** a request times out
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: request timeouts — must be satisfied. Applies when a request times out.

## INTERACT-1044
- **strength:** default
- **scope:** back navigation behavior
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: back navigation behavior — must be satisfied.

## INTERACT-1045
- **strength:** default
- **scope:** modals and sheets
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: modals and sheets — must be satisfied.

## INTERACT-1046
- **strength:** default
- **scope:** navigating back to a previous screen
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: navigating back to a previous screen — must be satisfied.

## INTERACT-1047
- **strength:** default
- **scope:** system gesture navigation (swipe-back, predictive back)
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: system gesture navigation (swipe-back, predictive back) — must be satisfied.

## INTERACT-1048
- **strength:** avoid
- **scope:** the navigation stack
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Discouraged: the navigation stack — to be avoided by default.

## INTERACT-1049
- **strength:** default
- **scope:** unavailable navigation destinations are handled explicitly
- **condition:** a nav destination is unavailable
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: unavailable navigation destinations are handled explicitly. Applies when a nav destination is unavailable.

## INTERACT-1050
- **strength:** default
- **scope:** chart data-point interaction
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: chart data-point interaction — must be satisfied.

## INTERACT-1051
- **strength:** default
- **scope:** charts with no underlying data
- **condition:** no data exists
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: charts with no underlying data — must be satisfied. Applies when no data exists.

## INTERACT-1052
- **strength:** default
- **scope:** charts while data is loading
- **condition:** chart data is loading
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: charts while data is loading — must be satisfied. Applies when chart data is loading.

## INTERACT-1054
- **strength:** default
- **scope:** chart legend interactivity
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: chart legend interactivity — must be satisfied.

## INTERACT-1055
- **strength:** default
- **scope:** chart data-load failure has a defined UI state
- **condition:** chart data fails to load
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: chart data-load failure has a defined UI state. Applies when chart data fails to load.

## INTERACT-1056
- **strength:** default
- **scope:** press-state visual treatment for icons/controls
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: press-state visual treatment for icons/controls — must be satisfied.

## INTERACT-1059
- **strength:** default
- **scope:** disabled-control semantics in native/mobile app UI
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: disabled-control semantics in native/mobile app UI — flagged when a control appears tappable but has no semantic disabled state and silently no-ops.

## INTERACT-1061
- **strength:** default
- **scope:** concurrent gesture regions in native/mobile app UI
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: concurrent gesture regions in native/mobile app UI — must be satisfied.

## INTERACT-2001
- **strength:** default
- **scope:** interactive and clickable elements define an :active state
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: interactive and clickable elements define an :active state.

## INTERACT-2002
- **strength:** default
- **scope:** loading, empty, and error states for any async/data-driven UI
- **override:** toasts are acceptable specifically for transient errors
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: loading, empty, and error states for any async/data-driven UI — flagged when a data-driven section has no declared loading, empty, or error branch. Override: toasts are acceptable specifically for transient errors.

## INTERACT-2003
- **strength:** default
- **scope:** CTA label semantics across one page
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: CTA label semantics across one page — flagged when two or more CTAs on the page fall in the same named synonym cluster.

## INTERACT-2004
- **strength:** default
- **scope:** CTA button label rendering at desktop
- **enforcement:** must_surface
- **verification:** L2
- **public_expression:** Required; surfaced on failure: CTA button label rendering at desktop — flagged when line count > 1.

## INTERACT-2005
- **strength:** default
- **scope:** form field composition (label/input/helper/error)
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: form field composition (label/input/helper/error) — flagged when the label does not precede the input in source order, the error text is not positioned after the input, or the only label mechanism is a placeholder attribute with no associated <label>.

## INTERACT-2006
- **strength:** default
- **scope:** third-party library imports in generated code
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: third-party library imports in generated code — flagged when an imported package has no corresponding package.json dependency entry and no install command was output.

## INTERACT-2007
- **strength:** avoid
- **scope:** ad-hoc icon libraries and hand-rolled glyphs
- **override:** an established icon library is fine when the user requests it or the project already depends on it; a hand-drawn SVG only when the glyph is missing from every allowed library
- **exceptions:** glyph genuinely missing from every allowed library
- **enforcement:** warn
- **verification:** L1
- **public_expression:** Discouraged (warns): ad-hoc icon libraries and hand-rolled glyphs. Override: an established icon library is fine when the user requests it or the project already depends on it; a hand-drawn SVG only when the glyph is missing from every allowed library.

## INTERACT-2008
- **strength:** avoid
- **scope:** arbitrary z-index stacking and emoji in generated copy or markup
- **override:** emoji are allowed, used sparingly and deliberately, when the user asks for a playful, chat-style, or social-native register
- **enforcement:** warn
- **verification:** L1
- **public_expression:** Discouraged (warns): arbitrary z-index stacking and emoji in generated copy or markup. Override: emoji are allowed, used sparingly and deliberately, when the user asks for a playful, chat-style, or social-native register.

## INTERACT-4001
- **strength:** default
- **scope:** an interactive component built under the Component-scope flow (a button, input, card, modal, dropdown, tooltip, select, checkbox, switch, tab strip, chip, badge, banner, snackbar, popover, slider, date picker, avatar)
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: an interactive component built under the Component-scope flow (a button, input, card, modal, dropdown, tooltip, select, checkbox, switch, tab strip, chip, badge, banner, snackbar, popover, slider, date picker, avatar) — flagged when any of the eight states has no corresponding styling in the artifact.

## INTERACT-4002
- **strength:** default
- **scope:** every interactive element in a page-scope (default-flow) build
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: every interactive element in a page-scope (default-flow) build — flagged when any of the eight states has no corresponding styling.

## INTERACT-4003
- **strength:** default
- **scope:** apply the microinteraction recipe appropriate to each interaction (button, input, modal, toast, drag, copy, and the like)
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: apply the microinteraction recipe appropriate to each interaction (button, input, modal, toast, drag, copy, and the like).

## INTERACT-4004
- **strength:** default
- **scope:** skip a success toast when the action's effect is already visible to the user
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: skip a success toast when the action's effect is already visible to the user.

## INTERACT-4005
- **strength:** default
- **scope:** a tooltip
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a tooltip — flagged when the hover delay is outside 800-1000ms, or the focus delay is not 0ms, or the two are equal.

## INTERACT-4006
- **strength:** default
- **scope:** input, textarea, and select fields are styled across default, hover, focus, error, and disabled states
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: input, textarea, and select fields are styled across default, hover, focus, error, and disabled states.

## INTERACT-4007
- **strength:** absolute
- **scope:** a CSS-only radio-tab pattern (<input type="radio"> siblings with :checked selectors) is not shipped
- **condition:** the artifact implements tab toggles that way
- **enforcement:** hard_block
- **verification:** L1
- **public_expression:** Hard requirement (non-overridable): a CSS-only radio-tab pattern (<input type="radio"> siblings with :checked selectors) is not shipped. Applies when the artifact implements tab toggles that way.

## INTERACT-4008
- **strength:** default
- **scope:** an N1b nav dropdown
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: an N1b nav dropdown — flagged when the dropdown opens only via a click handler with no hover/focus CSS state.

## INTERACT-4009
- **strength:** default
- **scope:** the implementation of the floating-on-scroll-morph nav archetype
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: the implementation of the floating-on-scroll-morph nav archetype.

## INTERACT-4010
- **strength:** default
- **scope:** an N11 mega-menu panel's hover-open behaviour
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: an N11 mega-menu panel's hover-open behaviour — flagged when the panel closes immediately on pointerleave with no grace delay.

## INTERACT-6001
- **strength:** default
- **scope:** any interactive tap/click target (buttons, icon controls, mobile form inputs, interactive chart elements) web+native
- **override:** a pointer-only/desktop context governed instead by the web-pointer minimum A11Y-1022 (24x24 CSS px); a control whose hit area is legitimately extended beyond the visual glyph to meet the minimum satisfies the rule (check exception, not a rule defeat)
- **enforcement:** must_surface
- **verification:** L2
- **derived_from** (lineage — sources consumed into synthesis; not live records): INTERACT-1001, INTERACT-1041, INTERACT-1053, INTERACT-1057, INTERACT-1060
- **notes:** Chart expand-on-touch behavior is a runtime-integration caveat.
- **public_expression:** Required; surfaced on failure: any interactive tap/click target (buttons, icon controls, mobile form inputs, interactive chart elements) web+native — flagged when width or height below 44pt (iOS) / 48dp (Android). Override: a pointer-only/desktop context governed instead by the web-pointer minimum A11Y-1022 (24x24 CSS px); a control whose hit area is legitimately extended beyond the visual glyph to meet the minimum satisfies the rule (check exception, not a rule defeat).

## INTERACT-6002
- **strength:** default
- **scope:** visible feedback on a tap/press interaction, web+native/mobile
- **override:** an interaction whose intended affordance is an explicit, communicated delay (e.g. a long-press that is itself the signal)
- **enforcement:** contextual
- **verification:** L2
- **derived_from** (lineage — sources consumed into synthesis; not live records): UX-1016, INTERACT-1058
- **public_expression:** Required; surfaced on failure: visible feedback on a tap/press interaction, web+native/mobile — must be satisfied. Override: an interaction whose intended affordance is an explicit, communicated delay (e.g. a long-press that is itself the signal).
