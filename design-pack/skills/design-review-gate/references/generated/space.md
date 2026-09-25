# Design Pack runtime reference — SPACE (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 19 record(s).

## SPACE-1001
- **strength:** default
- **scope:** primary touch targets clear the device notch, Dynamic Island, gesture bar, and screen edges
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: primary touch targets clear the device notch, Dynamic Island, gesture bar, and screen edges.

## SPACE-1002
- **strength:** default
- **scope:** padding/gap/section-spacing values across a product
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: padding/gap/section-spacing values across a product — must be satisfied.

## SPACE-1003
- **strength:** heuristic
- **scope:** component spacing under touch
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: component spacing under touch — applied as contextual judgement, not a hard gate.

## SPACE-1004
- **strength:** default
- **scope:** content beneath a fixed navbar or bottom bar is not occluded
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: content beneath a fixed navbar or bottom bar is not occluded.

## SPACE-1005
- **strength:** default
- **scope:** grouping and separation of content via whitespace
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: grouping and separation of content via whitespace — must be satisfied.

## SPACE-1006
- **strength:** default
- **scope:** fixed headers, tab bars, and CTA bars respect device safe areas
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: fixed headers, tab bars, and CTA bars respect device safe areas.

## SPACE-1007
- **strength:** default
- **scope:** tappable content near OS status/navigation bars
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: tappable content near OS status/navigation bars — must be satisfied.

## SPACE-1008
- **strength:** default
- **scope:** padding/gap/section-spacing system in native/mobile app UI
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: padding/gap/section-spacing system in native/mobile app UI — must be satisfied.

## SPACE-1009
- **strength:** default
- **scope:** vertical rhythm tiers by hierarchy level
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: vertical rhythm tiers by hierarchy level — must be satisfied.

## SPACE-1010
- **strength:** default
- **scope:** horizontal insets/gutters by breakpoint and orientation
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: horizontal insets/gutters by breakpoint and orientation — must be satisfied.

## SPACE-1011
- **strength:** default
- **scope:** scrollable content relative to fixed headers/footers
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: scrollable content relative to fixed headers/footers — must be satisfied.

## SPACE-2001
- **strength:** default
- **scope:** per-section content shape and copy register (landing/portfolio pages)
- **override:** the section's job justifies more content than the default shape
- **exceptions:** section's job justifies more
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: per-section content shape and copy register (landing/portfolio pages) — flagged when word count > 8. Override: the section's job justifies more content than the default shape.

## SPACE-2002
- **strength:** default
- **scope:** long lists (>5 items) and data-dump content (spec sheets, publication tables, award lists, pricing matrices)
- **condition:** item count > 5, or content is a large tabular/list data dump
- **override:** the data itself is the product and deserves a different, dedicated page
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: long lists (>5 items) and data-dump content (spec sheets, publication tables, award lists, pricing matrices) — flagged when item count > 5 using the default list component. Applies when item count > 5, or content is a large tabular/list data dump. Override: the data itself is the product and deserves a different, dedicated page.

## SPACE-2003
- **strength:** default
- **scope:** spacing and structure for long specification tables
- **condition:** spec-heavy product domains (cookware, hardware, apparel, artisan goods)
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: spacing and structure for long specification tables. Applies to spec-heavy product domains (cookware, hardware, apparel, artisan goods).

## SPACE-2004
- **strength:** default
- **scope:** proof-read every visible string before shipping
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: proof-read every visible string before shipping.

## SPACE-2005
- **strength:** default
- **scope:** avoid fake-precise numeric copy (specs, stats, metrics)
- **override:** the figure comes from real data (brief, brand guidelines, public metrics) or is clearly labeled as mock/sample
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: avoid fake-precise numeric copy (specs, stats, metrics). Override: the figure comes from real data (brief, brand guidelines, public metrics) or is clearly labeled as mock/sample.

## SPACE-2006
- **strength:** default
- **scope:** overall page density and inter-section spacing
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: overall page density and inter-section spacing — must be satisfied.

## SPACE-4001
- **strength:** default
- **scope:** every padding, gap, and margin declaration
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: every padding, gap, and margin declaration — flagged when a value is off-scale.

## SPACE-4002
- **strength:** default
- **scope:** a prose container sets a readable max-width
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a prose container sets a readable max-width.
