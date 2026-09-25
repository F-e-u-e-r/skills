# Design Pack runtime reference — ANTISLOP (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 16 record(s).

## ANTISLOP-2001
- **strength:** absolute
- **scope:** the em-dash is banned from all generated copy, markup, and visible text
- **enforcement:** hard_block
- **verification:** L1
- **notes:** Effective strength is absolute (non-overridable).
- **public_expression:** Hard requirement (non-overridable): the em-dash is banned from all generated copy, markup, and visible text — across headlines, eyebrows, pills, body, quotes, attribution, captions, buttons, and alt text.

## ANTISLOP-2002
- **strength:** default
- **scope:** generated names, avatars, numeric data, brand names, and marketing verbs in copy/content
- **override:** brief supplies real data, or explicitly labels a value as mock/example/sample
- **exceptions:** brief explicitly requests one of these as a real brand/product name
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: generated names, avatars, numeric data, brand names, and marketing verbs in copy/content — flagged when any exact blocklist match present. Override: brief supplies real data, or explicitly labels a value as mock/example/sample.

## ANTISLOP-2003
- **strength:** default
- **scope:** hero and section product-preview imagery, and any hand-rolled decorative SVG, are not faked
- **override:** a single simple geometric mark (square, circle, wordmark) the agent is confident in, or a brief that explicitly requests a hand-drawn SVG
- **enforcement:** must_surface
- **verification:** L2
- **public_expression:** Required; surfaced on failure: hero and section product-preview imagery, and any hand-rolled decorative SVG, are not faked. Override: a single simple geometric mark (square, circle, wordmark) the agent is confident in, or a brief that explicitly requests a hand-drawn SVG.

## ANTISLOP-2004
- **strength:** default
- **scope:** avoid boilerplate hero eyebrows, section-numbering micro-labels, and range-label eyebrows
- **override:** a brief explicitly about product-launch or preview status, for version/status labels only
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: avoid boilerplate hero eyebrows, section-numbering micro-labels, and range-label eyebrows. Override: a brief explicitly about product-launch or preview status, for version/status labels only.

## ANTISLOP-2005
- **strength:** default
- **scope:** separator punctuation and decorative status indicators are not scattered across the page
- **override:** a dot or indicator that conveys real semantic state (a live server-status or availability flag), used sparingly
- **exceptions:** the dot conveys real semantic state per override
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: separator punctuation and decorative status indicators are not scattered across the page. Override: a dot or indicator that conveys real semantic state (a live server-status or availability flag), used sparingly.

## ANTISLOP-2006
- **strength:** default
- **scope:** marketing-copy register (headers, labels, step/stage indicators, locale/time strips) avoids slop patterns
- **override:** a genuinely global studio whose work is timezone-relevant, a travel brand, or a real physical venue (locale/weather strips only); a single footer contact address is always fine
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: marketing-copy register (headers, labels, step/stage indicators, locale/time strips) avoids slop patterns. Override: a genuinely global studio whose work is timezone-relevant, a travel brand, or a real physical venue (locale/weather strips only); a single footer contact address is always fine.

## ANTISLOP-2007
- **strength:** default
- **scope:** decorative image overlays, footer version strings, and long-list row dividers are not added as filler
- **override:** a real, credited, permissioned photo; a genuinely limited-run waitlist backed by real stock data
- **enforcement:** must_surface
- **verification:** L2
- **public_expression:** Required; surfaced on failure: decorative image overlays, footer version strings, and long-list row dividers are not added as filler. Override: a real, credited, permissioned photo; a genuinely limited-run waitlist backed by real stock data.

## ANTISLOP-2008
- **strength:** default
- **scope:** avoid decorative typographic and graphic flourishes (forced headline line-breaks, rotated text, hairline grids, hero-bottom text strips)
- **override:** an explicitly agency, Awwwards, or experimental brief where the device serves a real composition; a strip carrying real links or status; a genuine compositional reason for a split header
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: avoid decorative typographic and graphic flourishes (forced headline line-breaks, rotated text, hairline grids, hero-bottom text strips). Override: an explicitly agency, Awwwards, or experimental brief where the device serves a real composition; a strip carrying real links or status; a genuine compositional reason for a split header.

## ANTISLOP-2009
- **strength:** default
- **scope:** micro-UI chrome (pills, pseudo-system labels, decorative tags) in generated design references
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: micro-UI chrome (pills, pseudo-system labels, decorative tags) in generated design references — must be satisfied.

## ANTISLOP-4001
- **strength:** avoid
- **scope:** falling through to the Specimen macrostructure on a vague brief (no explicit editorial, foundry, journal, or specimen-sheet signal)
- **override:** an explicitly editorial, type-foundry, journal, or specimen-sheet brief, where Specimen is a legitimate choice
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Discouraged: falling through to the Specimen macrostructure on a vague brief (no explicit editorial, foundry, journal, or specimen-sheet signal). Override: an explicitly editorial, type-foundry, journal, or specimen-sheet brief, where Specimen is a legitimate choice.

## ANTISLOP-4002
- **strength:** default
- **scope:** a hero or enrichment slot that needs photographic content when the user supplied no real assets
- **condition:** the brief signals a photographic need (e-commerce, team, food, travel) and no real assets are given
- **override:** a brief that allows non-photographic imagery (SaaS landing, manifesto, agency splash, editorial-led) — prefer the imagery kit over photo placeholders
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: a hero or enrichment slot that needs photographic content when the user supplied no real assets. Applies when the brief signals a photographic need (e-commerce, team, food, travel) and no real assets are given. Override: a brief that allows non-photographic imagery (SaaS landing, manifesto, agency splash, editorial-led) — prefer the imagery kit over photo placeholders.

## ANTISLOP-4003
- **strength:** default
- **scope:** any generated copy
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: any generated copy — flagged when any listed string is found.

## ANTISLOP-4004
- **strength:** default
- **scope:** icon usage across the page
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: icon usage across the page — flagged when ≥ 2 distinct icon libraries are mixed, OR a listed emoji glyph is used as a functional icon in one of the named contexts.

## ANTISLOP-4005
- **strength:** default
- **scope:** a decorative hero element
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: a decorative hero element — cursor, scanline, gradient blob, abstract shape, ornament, badge, or sticker — earns its place rather than being added by reflex.

## ANTISLOP-4006
- **strength:** default
- **scope:** a quantitative claim, testimonial, logo, or case-study count in generated copy is not invented
- **override:** the user supplied the metric, testimonial, logo, or count
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Guidance: a quantitative claim, testimonial, logo, or case-study count in generated copy is not invented. Override: the user supplied the metric, testimonial, logo, or count.

## ANTISLOP-4007
- **strength:** default
- **scope:** any browser, phone, code-block, terminal, or IDE chrome depicted in the artifact
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: any browser, phone, code-block, terminal, or IDE chrome depicted in the artifact — must be satisfied.
