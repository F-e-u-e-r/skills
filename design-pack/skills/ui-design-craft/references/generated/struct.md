# Design Pack runtime reference — STRUCT (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 110 record(s).

## STRUCT-1001
- **strength:** default
- **scope:** overall visual style selection for a product
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: overall visual style selection for a product — must be satisfied.

## STRUCT-1002
- **strength:** default
- **scope:** visual style across all pages of one product
- **override:** a documented, intentional style break for a distinct sub-product/section (e.g. a marketing microsite vs. the core app)
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: visual style across all pages of one product — must be satisfied. Override: a documented, intentional style break for a distinct sub-product/section (e.g. a marketing microsite vs. the core app).

## STRUCT-1003
- **strength:** avoid
- **scope:** icons used for navigation, settings, or system controls
- **enforcement:** warn
- **verification:** L1
- **public_expression:** Discouraged: icons used for navigation, settings, or system controls — flagged when an emoji character is used in place of a vector icon for a structural/navigational affordance.

## STRUCT-1004
- **strength:** default
- **scope:** shadow, blur, and radius stay consistent with the product's chosen style (glass, flat, clay, and similar)
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: shadow, blur, and radius stay consistent with the product's chosen style (glass, flat, clay, and similar).

## STRUCT-1005
- **strength:** default
- **scope:** navigation, controls, typography, and motion on iOS vs. Android
- **condition:** native iOS or Android target
- **override:** a deliberately platform-agnostic/branded design system that intentionally does not adapt per platform
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: navigation, controls, typography, and motion on iOS vs. Android — must be satisfied. Applies when native iOS or Android target. Override: a deliberately platform-agnostic/branded design system that intentionally does not adapt per platform.

## STRUCT-1006
- **strength:** default
- **scope:** a coherent elevation/shadow scale governs cards, sheets, and modals
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a coherent elevation/shadow scale governs cards, sheets, and modals.

## STRUCT-1007
- **strength:** default
- **scope:** icon set used across a product (stroke width, corner radius)
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: icon set used across a product (stroke width, corner radius) — must be satisfied.

## STRUCT-1008
- **strength:** default
- **scope:** choice between native/system controls and fully custom controls
- **override:** branding requirements explicitly justify a custom control
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: choice between native/system controls and fully custom controls — must be satisfied. Override: branding requirements explicitly justify a custom control.

## STRUCT-1009
- **strength:** avoid
- **scope:** use of background blur effects
- **override:** the blur is explicitly serving background dismissal semantics (modal/sheet), which is the stated correct use
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Discouraged: use of background blur effects — to be avoided by default. Override: the blur is explicitly serving background dismissal semantics (modal/sheet), which is the stated correct use.

## STRUCT-1010
- **strength:** default
- **scope:** primary call-to-action per screen
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: primary call-to-action per screen — flagged when more than one primary-styled CTA present on one screen.

## STRUCT-1011
- **strength:** default
- **scope:** the viewport meta tag on web pages
- **condition:** web context
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the viewport meta tag on web pages — flagged when viewport meta disables zoom, or is missing/misconfigured. Applies when web context.

## STRUCT-1012
- **strength:** default
- **scope:** responsive design process/methodology
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: responsive design process/methodology — must be satisfied.

## STRUCT-1013
- **strength:** default
- **scope:** responsive breakpoints
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: responsive breakpoints — must be satisfied.

## STRUCT-1014
- **strength:** default
- **scope:** mobile viewport content width
- **condition:** mobile viewport
- **enforcement:** must_surface
- **verification:** L2
- **public_expression:** Required; surfaced on failure: mobile viewport content width — flagged when horizontal scroll is present on mobile. Applies when mobile viewport.

## STRUCT-1015
- **strength:** default
- **scope:** desktop content container width
- **condition:** desktop viewport
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: desktop content container width — must be satisfied. Applies when desktop viewport.

## STRUCT-1016
- **strength:** default
- **scope:** layered/overlapping UI elements
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: layered/overlapping UI elements — must be satisfied.

## STRUCT-1017
- **strength:** avoid
- **scope:** nested scroll regions
- **override:** an intentionally independent scroll region (e.g. a data table or code block) where nested scroll is the correct, expected behavior
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Discouraged: nested scroll regions — to be avoided by default. Override: an intentionally independent scroll region (e.g. a data table or code block) where nested scroll is the correct, expected behavior.

## STRUCT-1018
- **strength:** default
- **scope:** full-viewport-height mobile layouts
- **condition:** mobile web context
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: full-viewport-height mobile layouts — flagged when layout uses 100vh on mobile where dvh is available. Applies when mobile web context.

## STRUCT-1019
- **strength:** default
- **scope:** landscape orientation
- **condition:** device rotated to landscape
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: landscape orientation — must be satisfied. Applies when device rotated to landscape.

## STRUCT-1020
- **strength:** default
- **scope:** mobile content ordering
- **condition:** mobile viewport
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: mobile content ordering — must be satisfied. Applies when mobile viewport.

## STRUCT-1021
- **strength:** default
- **scope:** how visual hierarchy is established
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: how visual hierarchy is established — must be satisfied.

## STRUCT-1022
- **strength:** default
- **scope:** collections of chips/tags that no longer fit their container
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: collections of chips/tags that no longer fit their container — must be satisfied.

## STRUCT-1023
- **strength:** default
- **scope:** bottom navigation bars
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: bottom navigation bars — flagged when bottom nav has more than 5 items.

## STRUCT-1024
- **strength:** default
- **scope:** drawer/sidebar navigation
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: drawer/sidebar navigation — must be satisfied.

## STRUCT-1025
- **strength:** default
- **scope:** key screens' reachability via URL/deep link
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: key screens' reachability via URL/deep link — must be satisfied.

## STRUCT-1026
- **strength:** default
- **scope:** top-level navigation on iOS
- **condition:** iOS native
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: top-level navigation on iOS — must be satisfied. Applies when iOS native.

## STRUCT-1027
- **strength:** default
- **scope:** primary structure on Android
- **condition:** Android native
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: primary structure on Android — must be satisfied. Applies when Android native.

## STRUCT-1028
- **strength:** default
- **scope:** navigation item presentation
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: navigation item presentation — flagged when a primary nav item has an icon with no text label.

## STRUCT-1029
- **strength:** default
- **scope:** current-location indication in navigation
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: current-location indication in navigation — must be satisfied.

## STRUCT-1030
- **strength:** default
- **scope:** primary vs. secondary navigation separation
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: primary vs. secondary navigation separation — must be satisfied.

## STRUCT-1031
- **strength:** default
- **scope:** search feature placement
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: search feature placement — must be satisfied.

## STRUCT-1032
- **strength:** default
- **scope:** deep page hierarchies on web
- **condition:** web context, hierarchy depth >= 3 levels
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: deep page hierarchies on web — must be satisfied. Applies when web context, hierarchy depth >= 3 levels.

## STRUCT-1033
- **strength:** heuristic
- **scope:** unread/pending indicators on nav items
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: unread/pending indicators on nav items — applied as contextual judgement, not a hard gate.

## STRUCT-1034
- **strength:** default
- **scope:** actions exceeding available UI space
- **condition:** available action-bar space is exceeded
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: actions exceeding available UI space — must be satisfied. Applies when available action-bar space is exceeded.

## STRUCT-1035
- **strength:** default
- **scope:** bottom navigation nesting
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: bottom navigation nesting — must be satisfied.

## STRUCT-1036
- **strength:** default
- **scope:** navigation pattern selection by screen size
- **condition:** viewport width >= 1024px selects sidebar; smaller selects bottom/top nav
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: navigation pattern selection by screen size — must be satisfied. Applies when viewport width >= 1024px selects sidebar; smaller selects bottom/top nav.

## STRUCT-1037
- **strength:** default
- **scope:** navigation placement across all pages of a product
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: navigation placement across all pages of a product — must be satisfied.

## STRUCT-1038
- **strength:** default
- **scope:** combining navigation patterns at one hierarchy level
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: combining navigation patterns at one hierarchy level — must be satisfied.

## STRUCT-1039
- **strength:** default
- **scope:** use of modals for primary navigation flows
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: use of modals for primary navigation flows — must be satisfied.

## STRUCT-1040
- **strength:** default
- **scope:** core navigation reachability from deep pages
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: core navigation reachability from deep pages — must be satisfied.

## STRUCT-1041
- **strength:** default
- **scope:** destructive controls (account deletion, sign-out) relative to ordinary navigation
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: destructive controls — account deletion, sign-out — are separated from ordinary navigation.

## STRUCT-1042
- **strength:** default
- **scope:** chart layout on small screens
- **condition:** small/mobile screen
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: chart layout on small screens — must be satisfied. Applies when small/mobile screen.

## STRUCT-1043
- **strength:** default
- **scope:** drill-down chart interactions
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: drill-down chart interactions — must be satisfied.

## STRUCT-1044
- **strength:** default
- **scope:** structural icons (navigation, settings, system controls) in native/mobile app UI
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: structural icons (navigation, settings, system controls) in native/mobile app UI — flagged when an emoji is used for a navigation/settings/system-control icon.

## STRUCT-1045
- **strength:** default
- **scope:** icon asset format
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: icon asset format — must be satisfied.

## STRUCT-1046
- **strength:** default
- **scope:** brand logo usage
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: brand logo usage — must be satisfied.

## STRUCT-1047
- **strength:** default
- **scope:** icon sizing
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: icon sizing — must be satisfied.

## STRUCT-1048
- **strength:** default
- **scope:** icon stroke width within one visual layer
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: icon stroke width within one visual layer — must be satisfied.

## STRUCT-1049
- **strength:** default
- **scope:** filled vs. outline icon style at one hierarchy level
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: filled vs. outline icon style at one hierarchy level — must be satisfied.

## STRUCT-1050
- **strength:** default
- **scope:** icon alignment to text baseline
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: icon alignment to text baseline — must be satisfied.

## STRUCT-1051
- **strength:** default
- **scope:** content width is tuned per device class
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: content width is tuned per device class.

## STRUCT-2002
- **strength:** avoid
- **scope:** the centered hero / H1 layout as a default
- **override:** editorial, manifesto, or launch-announcement briefs in which the message is itself the design
- **enforcement:** contextual
- **verification:** L2
- **selector:** DIAL-2001 (DESIGN_VARIANCE > 4)
- **public_expression:** Discouraged: the centered hero / H1 layout as a default. Override: editorial, manifesto, or launch-announcement briefs in which the message is itself the design.

## STRUCT-2003
- **strength:** default
- **scope:** responsive collapse behavior of asymmetric/variance-driven layouts
- **enforcement:** must_surface
- **verification:** L2
- **selector:** DIAL-2001
- **public_expression:** Required; surfaced on failure: responsive collapse behavior of asymmetric/variance-driven layouts — flagged when an asymmetric multi-column layout does not collapse to a strict single column (full width) below 768px.

## STRUCT-2004
- **strength:** default
- **scope:** hero section content sizing and CTA visibility
- **condition:** brief is a landing page / portfolio hero (greenfield or redesign)
- **enforcement:** must_surface
- **verification:** L1+L2
- **public_expression:** Required; surfaced on failure: hero section content sizing and CTA visibility — flagged when word count > 20. Applies when brief is a landing page / portfolio hero (greenfield or redesign).

## STRUCT-2005
- **strength:** default
- **scope:** hero top padding
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: hero top padding — flagged when declared/computed desktop hero top padding > pt-24 (~6rem / 96px).

## STRUCT-2006
- **strength:** default
- **scope:** hero text-element composition and trust/logo-wall placement relative to the hero
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: hero text-element composition and trust/logo-wall placement relative to the hero — flagged when count > 4, or both an eyebrow/brand-strip AND a secondary tagline element are present.

## STRUCT-2007
- **strength:** default
- **scope:** primary navigation bar layout and height
- **enforcement:** must_surface
- **verification:** L2
- **public_expression:** Required; surfaced on failure: primary navigation bar layout and height — flagged when nav items wrap to a second line at desktop.

## STRUCT-2008
- **strength:** default
- **scope:** bento/feature-grid cell composition
- **enforcement:** must_surface
- **verification:** L1+L2
- **public_expression:** Required; surfaced on failure: bento/feature-grid cell composition — flagged when cell count != content-item count (an empty cell exists, or content is missing a cell).

## STRUCT-2009
- **strength:** default
- **scope:** vary the layout family across page sections
- **condition:** the page has many sections (roughly eight or more)
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: vary the layout family across page sections. Applies when the page has many sections (roughly eight or more).

## STRUCT-2010
- **strength:** default
- **scope:** consecutive image-plus-text split sections are broken up
- **override:** interrupt the pattern with a full-width, vertical-stack, bento-grid, marquee, or other layout family
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: consecutive image-plus-text split sections are broken up. Override: interrupt the pattern with a full-width, vertical-stack, bento-grid, marquee, or other layout family.

## STRUCT-2011
- **strength:** default
- **scope:** eyebrow (small uppercase wide-tracking) labels above section headlines
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: eyebrow (small uppercase wide-tracking) labels above section headlines — flagged when count > ceil(sectionCount / 3).

## STRUCT-2012
- **strength:** default
- **scope:** section headers pair a headline with an explainer paragraph judiciously
- **override:** the smaller column carries a real visual or interactive element rather than filler
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: section headers pair a headline with an explainer paragraph judiciously. Override: the smaller column carries a real visual or interactive element rather than filler.

## STRUCT-2013
- **strength:** default
- **scope:** a consistent corner-radius system across components
- **override:** a documented mixed-radius rule that is stated and applied everywhere (for example, full-pill buttons, 16px cards, 8px inputs)
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Guidance: a consistent corner-radius system across components. Override: a documented mixed-radius rule that is stated and applied everywhere (for example, full-pill buttons, 16px cards, 8px inputs).

## STRUCT-2014
- **strength:** default
- **scope:** responsive fallback declaration for multi-column sections
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: responsive fallback declaration for multi-column sections — flagged when a multi-column section declares md:/lg: grid classes with no corresponding unprefixed single-column base declaration.

## STRUCT-2015
- **strength:** default
- **scope:** container/box nesting depth around a single content region
- **override:** a box has a clear, documented purpose
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: container/box nesting depth around a single content region — must be satisfied. Override: a box has a clear, documented purpose.

## STRUCT-2016
- **strength:** default
- **scope:** overall visual-direction commitment for a generated design (theme, background, typography character, hero architecture, section system, signature components, motion-implied cues)
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: overall visual-direction commitment for a generated design (theme, background, typography character, hero architecture, section system, signature components, motion-implied cues) — flagged when count != 4.

## STRUCT-2017
- **strength:** default
- **scope:** data/metric presentation containers and numeral typography
- **enforcement:** must_surface
- **verification:** L1
- **selector:** DIAL-2003
- **public_expression:** Required; surfaced on failure: data/metric presentation containers and numeral typography — flagged when a generic bordered/shadowed card wraps a single data metric.

## STRUCT-4001
- **strength:** default
- **scope:** the stamp comment at the top of a Component-scope artifact's CSS
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the stamp comment at the top of a Component-scope artifact's CSS — flagged when stamp absent, or the 'states:' line does not enumerate all eight states.

## STRUCT-4002
- **strength:** default
- **scope:** the order of operations in the default Design flow, from genre pick through theme selection
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: the order of operations in the default Design flow, from genre pick through theme selection — must be satisfied.

## STRUCT-4003
- **strength:** default
- **scope:** choosing a macrostructure when a Hallmark macrostructure CSS stamp already exists in the codebase, or a prior Hallmark output exists for this user this session, but no .hallmark/log.json history is available to check
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: choosing a macrostructure when a Hallmark macrostructure CSS stamp already exists in the codebase, or a prior Hallmark output exists for this user this session, but no .hallmark/log.json history is available to check.

## STRUCT-4004
- **strength:** default
- **scope:** picking a macrostructure when the project has a persisted `.hallmark/log.json` (created by a previous Hallmark run)
- **exceptions:** the project's first Hallmark run, with no prior output to diversify against
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: picking a macrostructure when the project has a persisted `.hallmark/log.json` (created by a previous Hallmark run) — flagged when the current pick equals any of those three values.

## STRUCT-4005
- **strength:** default
- **scope:** picking a catalog theme, once a macrostructure has already been picked
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: picking a catalog theme, once a macrostructure has already been picked — flagged when all three axis values match the previous theme's three axis values (i.e. fewer than one axis differs).

## STRUCT-4006
- **strength:** default
- **scope:** at Step 2, a nav archetype (N1–N13, N1b) and a footer archetype (Ft1–Ft8) are picked alongside the macrostructure
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: at Step 2, a nav archetype (N1–N13, N1b) and a footer archetype (Ft1–Ft8) are picked alongside the macrostructure.

## STRUCT-4007
- **strength:** default
- **scope:** pick a nav or footer archetype suited to a real product page
- **override:** N1a when the page genuinely has only two destinations; Ft3 when the page is a genuine docs root or hub
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: pick a nav or footer archetype suited to a real product page. Override: N1a when the page genuinely has only two destinations; Ft3 when the page is a genuine docs root or hub.

## STRUCT-4008
- **strength:** default
- **scope:** a project that already ships an entry stylesheet (app/globals.css, src/index.css, src/styles/global.css)
- **condition:** such a stylesheet exists
- **override:** the user explicitly asks to overwrite it
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a project that already ships an entry stylesheet (app/globals.css, src/index.css, src/styles/global.css). Applies when such a stylesheet exists. Override: the user explicitly asks to overwrite it.

## STRUCT-4010
- **strength:** default
- **scope:** card components
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: card components — flagged when found.

## STRUCT-4011
- **strength:** default
- **scope:** card components
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: card components — flagged when the coloured side border is visually thick relative to the hairline standard.

## STRUCT-4012
- **strength:** avoid
- **scope:** a centered hero
- **override:** atmospheric and playful genres permit a centered hero where the full-bleed canvas itself functions as the composition; editorial and atelier permit a narrow centered hero, though the eyebrow or CTA still breaks the axis
- **enforcement:** contextual
- **verification:** L1+L2
- **public_expression:** Discouraged: a centered hero. Override: atmospheric and playful genres permit a centered hero where the full-bleed canvas itself functions as the composition; editorial and atelier permit a narrow centered hero, though the eyebrow or CTA still breaks the axis.

## STRUCT-4013
- **strength:** default
- **scope:** section-to-section transitions down the page
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: section-to-section transitions down the page — flagged when every boundary uses identical whitespace-only separation with no rule/ornament/colour-shift variation.

## STRUCT-4014
- **strength:** default
- **scope:** the top of the emitted CSS
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the top of the emitted CSS — flagged when stamp absent.

## STRUCT-4015
- **strength:** default
- **scope:** a build that reuses an archetype (macrostructure, nav, footer, hero, etc.) from a previous Hallmark output
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a build that reuses an archetype (macrostructure, nav, footer, hero, etc.) from a previous Hallmark output — flagged when every knob value matches the previous output's.

## STRUCT-4016
- **strength:** absolute
- **scope:** every emitted page, at every viewport width between 320px and 1920px
- **enforcement:** hard_block
- **verification:** L1+L2
- **public_expression:** Hard requirement (non-overridable): every emitted page, at every viewport width between 320px and 1920px — flagged when either selector is missing the clip declaration, or hidden is used instead of clip.

## STRUCT-4017
- **strength:** default
- **scope:** an interactive bar (nav, toolbar, command bar, hero CTA row, footer link strip) aligns elements of differing heights
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: an interactive bar (nav, toolbar, command bar, hero CTA row, footer link strip) aligns elements of differing heights.

## STRUCT-4018
- **strength:** default
- **scope:** the page's top-level nav archetype
- **override:** the page genuinely has only two destinations and the genre's routing table allows N1a
- **exceptions:** page has exactly 2 destinations and the genre routing table allows N1a
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Guidance: the page's top-level nav archetype. Override: the page genuinely has only two destinations and the genre's routing table allows N1a.

## STRUCT-4019
- **strength:** default
- **scope:** the page's footer archetype
- **override:** the page functions as a genuine documentation root or hub
- **exceptions:** the page functions as a documentation root or hub
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Guidance: the page's footer archetype. Override: the page functions as a genuine documentation root or hub.

## STRUCT-4020
- **strength:** default
- **scope:** the hero section, verified at a 1280x800 viewport
- **override:** a long-form, art-directed statement — for instance a poem broadside or a scroll-poster — may exceed one screen, provided the first screen reads as a complete, deliberate composition
- **enforcement:** must_surface
- **verification:** L1+L2
- **public_expression:** Required; surfaced on failure: the hero section, verified at a 1280x800 viewport. Override: a long-form, art-directed statement — for instance a poem broadside or a scroll-poster — may exceed one screen, provided the first screen reads as a complete, deliberate composition.

## STRUCT-4021
- **strength:** absolute
- **scope:** a button label, primary nav link, footer link, tab label, breadcrumb, or CTA text does not wrap or truncate at any viewport from 320px to 1920px
- **enforcement:** hard_block
- **verification:** L2
- **public_expression:** Hard requirement (non-overridable): a button label, primary nav link, footer link, tab label, breadcrumb, or CTA text does not wrap or truncate at any viewport from 320px to 1920px.

## STRUCT-4022
- **strength:** absolute
- **scope:** a grid-template-columns/rows track containing a 1fr track that renders an image-bearing element
- **enforcement:** hard_block
- **verification:** L1
- **public_expression:** Hard requirement (non-overridable): a grid-template-columns/rows track containing a 1fr track that renders an image-bearing element — flagged when bare 1fr is used on such a track.

## STRUCT-4023
- **strength:** absolute
- **scope:** display-size text elements (h1, .hero__display, .section__title, and hero-equivalent classes) render within their intended bounds
- **enforcement:** hard_block
- **verification:** L1
- **public_expression:** Hard requirement (non-overridable): display-size text elements (h1, .hero__display, .section__title, and hero-equivalent classes) render within their intended bounds.

## STRUCT-4024
- **strength:** default
- **scope:** a theme or variant that overrides .section__head to a non-1fr grid-template-columns.section__head grid columns to anything other than 1fr
- **condition:** a theme sets
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: a theme or variant that overrides .section__head to a non-1fr grid-template-columns. Applies when a theme sets .section__head grid columns to anything other than 1fr.

## STRUCT-4025
- **strength:** default
- **scope:** any wrapper (whatever its class) that contains both an eyebrow/label/number/kicker and a heading
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: any wrapper (whatever its class) that contains both an eyebrow/label/number/kicker and a heading.

## STRUCT-4026
- **strength:** default
- **scope:** a page with sticky elements beneath a sticky top-level nav
- **condition:** a sticky page-level nav coexists with another element set to position: sticky; top: 0
- **exceptions:** pages with no sticky elements at all pass trivially
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a page with sticky elements beneath a sticky top-level nav. Applies when a sticky page-level nav coexists with another element set to position: sticky; top: 0.

## STRUCT-4027
- **strength:** default
- **scope:** reusing an earlier study diagnosis's CSS stamp when one is available in the conversation
- **override:** the user has redirected — a different theme, or setting the extracted DNA aside
- **exceptions:** trivially passes when the conversation holds no such study
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: reuse an earlier study diagnosis's CSS stamp when one is available in the current conversation. Override: the user has redirected — for example, asked for a different theme or to set the extracted DNA aside.

## STRUCT-4028
- **strength:** default
- **scope:** the centre link cluster of the canonical SaaS three-section nav archetype (N1b)
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Guidance: the centre link cluster of the canonical SaaS three-section nav archetype (N1b).

## STRUCT-4029
- **strength:** default
- **scope:** the N5 (floating pill) nav archetype
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the N5 (floating pill) nav archetype — flagged when pill width approaches full viewport width (~95%+) or exceeds ~720px.

## STRUCT-4030
- **strength:** default
- **scope:** choosing the N6 (newspaper masthead) nav archetype
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: choosing the N6 (newspaper masthead) nav archetype — must be satisfied.

## STRUCT-4031
- **strength:** default
- **scope:** the N7 (brutal slab) nav archetype
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the N7 (brutal slab) nav archetype — flagged when any of the three is present.

## STRUCT-4032
- **strength:** default
- **scope:** choosing the N8 (terminal command) nav archetype
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: choosing the N8 (terminal command) nav archetype — must be satisfied.

## STRUCT-4033
- **strength:** default
- **scope:** the N9 (edge-aligned minimal) nav archetype
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the N9 (edge-aligned minimal) nav archetype — flagged when additional inline links are present between wordmark and CTA.

## STRUCT-4034
- **strength:** default
- **scope:** the N11 (mega-menu panel) nav archetype
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the N11 (mega-menu panel) nav archetype — flagged when columns > 4, OR panel height exceeds ~60vh, OR an item link has no accompanying description text.

## STRUCT-4035
- **strength:** default
- **scope:** the banner tier of the announcement-banner-plus-retracting-nav archetype (N12)
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the banner tier of the announcement-banner-plus-retracting-nav archetype (N12).

## STRUCT-4036
- **strength:** default
- **scope:** choosing the Ft5 (Statement) footer archetype
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: choosing the Ft5 (Statement) footer archetype — must be satisfied.

## STRUCT-4037
- **strength:** default
- **scope:** choosing the Ft6 (Letter close) footer archetype
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: choosing the Ft6 (Letter close) footer archetype — must be satisfied.

## STRUCT-4038
- **strength:** default
- **scope:** choosing the Ft7 (Newsletter-first) footer archetype
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: choosing the Ft7 (Newsletter-first) footer archetype — flagged when the footer is Ft7 AND no above-the-fold subscribe CTA exists on the page.

## STRUCT-4039
- **strength:** default
- **scope:** choosing the Ft8 (Marquee scroll) footer archetype
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: choosing the Ft8 (Marquee scroll) footer archetype — must be satisfied.

## STRUCT-4040
- **strength:** default
- **scope:** `hallmark audit` grading a page that uses the generic AI template shape
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: `hallmark audit` grading a page that uses the generic AI template shape — must be satisfied.

## STRUCT-4041
- **strength:** default
- **scope:** an audited file that carries a Hallmark macrostructure stamp
- **condition:** the audited file has such a stamp
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Guidance: an audited file that carries a Hallmark macrostructure stamp. Applies when the audited file has such a stamp.

## STRUCT-4042
- **strength:** default
- **scope:** auditing a page inside a project whose root has a design.md (or DESIGN.md)
- **condition:** the project root has one
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: auditing a page inside a project whose root has a design.md (or DESIGN.md). Applies when the project root has one.

## STRUCT-4043
- **strength:** default
- **scope:** a multi-page redesign (a `design.md`-managed, "designed-as-app" project)
- **condition:** the redesign is multi-page (routed via UX-4022) OR the project already has design.md
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a multi-page redesign (a `design.md`-managed, "designed-as-app" project) — flagged when two pages in the same designed-as-app project use different theme/accent/type-pairing token values. Applies when the redesign is multi-page (routed via UX-4022) OR the project already has design.md.

## STRUCT-6001
- **strength:** avoid
- **scope:** a multi-item feature/benefit row
- **override:** a 3-/4-tier pricing comparison table (an established comparison structure), or a card row differentiated by genuine content/visual hierarchy rather than a template default; where cards are interchangeable prefer 2-column zig-zag, asymmetric grid, scroll-pinned, or horizontal-scroll
- **enforcement:** contextual
- **verification:** L2
- **derived_from** (lineage — sources consumed into synthesis; not live records): STRUCT-2001, STRUCT-4009
- **notes:** Verification is a rendered L2 check.
- **public_expression:** Discouraged: a multi-item feature/benefit row — flagged when 3 or more such near-identical cards form one equal-width horizontal row. Override: a 3-/4-tier pricing comparison table (an established comparison structure), or a card row differentiated by genuine content/visual hierarchy rather than a template default; where cards are interchangeable prefer 2-column zig-zag, asymmetric grid, scroll-pinned, or horizontal-scroll.
