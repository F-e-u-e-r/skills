# Design Pack runtime reference — TYPO (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 28 record(s).

## TYPO-1001
- **strength:** default
- **scope:** mobile body text
- **condition:** mobile viewport
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: mobile body text — flagged when body text < 16px on mobile. Applies when mobile viewport.

## TYPO-1003
- **strength:** default
- **scope:** badges, status tags, filter chips, removable values under space constraint
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: badges, status tags, filter chips, removable values under space constraint — must be satisfied.

## TYPO-1004
- **strength:** default
- **scope:** body text line-height
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: body text line-height — must be satisfied.

## TYPO-1006
- **strength:** heuristic
- **scope:** heading/body typeface pairing
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: heading/body typeface pairing — applied as contextual judgement, not a hard gate.

## TYPO-1007
- **strength:** default
- **scope:** the set of font sizes used across a product
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the set of font sizes used across a product — must be satisfied.

## TYPO-1008
- **strength:** default
- **scope:** type roles (display, headline, title, body, label) are applied to their intended purpose
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: type roles (display, headline, title, body, label) are applied to their intended purpose.

## TYPO-1009
- **strength:** default
- **scope:** font-weight usage for hierarchy
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: font-weight usage for hierarchy — must be satisfied.

## TYPO-1010
- **strength:** avoid
- **scope:** long text content that would otherwise be truncated
- **override:** space is genuinely insufficient for wrapping (e.g. a single-line table cell), where an ellipsis with a tooltip is acceptable
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Discouraged: truncating long text content by default. Override: space is genuinely insufficient for wrapping (for example, a single-line table cell), where an ellipsis with a tooltip is acceptable.

## TYPO-1011
- **strength:** avoid
- **scope:** letter-spacing/tracking on body text
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Discouraged: letter-spacing/tracking on body text — to be avoided by default.

## TYPO-1012
- **strength:** default
- **scope:** tabular figures are used for data columns, prices, and timers
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: tabular figures are used for data columns, prices, and timers.

## TYPO-1013
- **strength:** heuristic
- **scope:** short heading line-wrapping
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: short heading line-wrapping — applied as contextual judgement, not a hard gate.

## TYPO-1014
- **strength:** avoid
- **scope:** URLs, IDs, and user-generated content
- **override:** normal prose paragraphs, where word-break: break-all must not be applied
- **exceptions:** normal prose paragraphs (word-break:break-all is the misapplication case)
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Discouraged: applying word-break: break-all to URLs, IDs, and user-generated content by reflex. Override: normal prose paragraphs, where word-break: break-all must not be applied.

## TYPO-1015
- **strength:** default
- **scope:** numbers, dates, currencies on chart axes/labels
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: numbers, dates, currencies on chart axes/labels — must be satisfied.

## TYPO-1016
- **strength:** default
- **scope:** long-form text measure on large devices
- **condition:** large device (e.g. tablet)
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: long-form text measure on large devices — must be satisfied. Applies when large device (e.g. tablet).

## TYPO-2001
- **strength:** avoid
- **scope:** defaulting the body/UI sans typeface
- **condition:** the brief names no typeface and no design system exists
- **override:** the user asks for a neutral or standard feel, or the brief is a public-sector or accessibility-first site
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Discouraged: defaulting the body/UI sans typeface. Applies when the brief names no typeface and no design system exists. Override: the user asks for a neutral or standard feel, or the brief is a public-sector or accessibility-first site.

## TYPO-2002
- **strength:** avoid
- **scope:** a serif display/headline family chosen by default over a sans
- **override:** the brief names a serif outright, or the aesthetic is genuinely editorial, luxury, publication, manuscript, heritage, or vintage and the specific serif is justified for that brand
- **exceptions:** brand brief explicitly justifies the specific serif
- **enforcement:** warn
- **verification:** L1
- **public_expression:** Discouraged (warns): a serif display/headline family chosen by default over a sans. Override: the brief names a serif outright, or the aesthetic is genuinely editorial, luxury, publication, manuscript, heritage, or vintage and the specific serif is justified for that brand.

## TYPO-2003
- **strength:** default
- **scope:** italic display type containing descender letters
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: italic display type containing descender letters — flagged when leading value < 1.1, or no pb-1/mb-1-equivalent reserve present, on an italic word with a descender.

## TYPO-2004
- **strength:** default
- **scope:** emphasized words within a headline
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: emphasized words within a headline — flagged when the emphasized span's font-family differs from the enclosing headline's font-family.

## TYPO-2005
- **strength:** default
- **scope:** typography as a primary design/hierarchy material across the page
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: typography as a primary design/hierarchy material across the page — must be satisfied.

## TYPO-4001
- **strength:** default
- **scope:** a hero headline the model writes itself, with no user-supplied copy
- **override:** aggressive-display themes (Brutal, Riso, Manifesto) step down one type rung past 50 characters instead of using --text-display
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a hero headline the model writes itself, with no user-supplied copy. Override: aggressive-display themes (Brutal, Riso, Manifesto) step down one type rung past 50 characters instead of using --text-display.

## TYPO-4002
- **strength:** default
- **scope:** the display font token
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the display font token — flagged when the display font is one of the six named families.

## TYPO-4003
- **strength:** default
- **scope:** any decorative text effect (highlighter band, accent stroke, underline)
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: any decorative text effect (highlighter band, accent stroke, underline) — must be satisfied.

## TYPO-4004
- **strength:** default
- **scope:** font families used across the page
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: font families used across the page — flagged when count > 3.

## TYPO-4005
- **strength:** default
- **scope:** the outlier font (the third face, beyond display and body)
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the outlier font (the third face, beyond display and body) — flagged when count > 2.

## TYPO-4006
- **strength:** avoid
- **scope:** weak heading/display type
- **enforcement:** warn
- **verification:** L1
- **public_expression:** Discouraged (warns): weak heading/display type. Scope covers any heading or display element (h1–h6, a *__title class, a wordmark, a stat figure, a footer statement).

## TYPO-4007
- **strength:** default
- **scope:** a display-size element (.hero__display, .section__title, h1, h2, or anything at or above --text-2xl) that uses text-transform: uppercase
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a display-size element (.hero__display, .section__title, h1, h2, or anything at or above --text-2xl) that uses text-transform: uppercase.

## TYPO-4008
- **strength:** default
- **scope:** naming a typeface during hallmark study in image mode
- **override:** in URL mode, the page's own @font-face, Google Fonts <link>, or next/font declarations name the typeface authoritatively, so an exact name may be given
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: naming a typeface during hallmark study in image mode. Override: in URL mode, the page's own @font-face, Google Fonts <link>, or next/font declarations name the typeface authoritatively, so an exact name may be given.

## TYPO-6001
- **strength:** heuristic
- **scope:** body-text line length (measure)
- **enforcement:** contextual
- **verification:** L2
- **derived_from** (lineage — sources consumed into synthesis; not live records): TYPO-1002, TYPO-1005
- **public_expression:** Guidance: body-text line length (measure) — applied as contextual judgement, not a hard gate.
