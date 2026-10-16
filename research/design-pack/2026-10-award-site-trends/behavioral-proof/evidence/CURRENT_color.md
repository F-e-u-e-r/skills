# Design Pack runtime reference — COLOR (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 30 record(s).

## COLOR-1001
- **strength:** heuristic
- **scope:** product color palette selection
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: product color palette selection — applied as contextual judgement, not a hard gate.

## COLOR-1002
- **strength:** default
- **scope:** light and dark theme variants of one product
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: light and dark theme variants of one product — must be satisfied.

## COLOR-1003
- **strength:** default
- **scope:** text-on-background color pairing
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: text-on-background color pairing — must be satisfied.

## COLOR-1004
- **strength:** default
- **scope:** color usage in component code
- **exceptions:** one-off illustrative/marketing surfaces explicitly exempted from the token system
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: color usage in component code — flagged when a component hardcodes a raw color literal instead of a semantic token.

## COLOR-1005
- **strength:** default
- **scope:** dark theme color derivation
- **condition:** dark theme
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: dark theme color derivation — must be satisfied. Applies when dark theme.

## COLOR-1006
- **strength:** default
- **scope:** foreground/background color pairs
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: foreground/background color pairs — flagged when ratio < 4.5 (AA target) — 7.0 (AAA) recorded as a stricter optional band, not the default fail_when.

## COLOR-1008
- **strength:** default
- **scope:** error/success state colors
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: error/success state colors — flagged when ratio < 4.5.

## COLOR-1009
- **strength:** default
- **scope:** chart color palettes
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: chart color palettes — must be satisfied.

## COLOR-1010
- **strength:** default
- **scope:** chart data lines/bars and their text labels
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: chart data lines/bars and their text labels — flagged when mark contrast < 3:1, or label contrast < 4.5:1.

## COLOR-1011
- **strength:** default
- **scope:** chart gridlines
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: chart gridlines — must be satisfied.

## COLOR-1012
- **strength:** default
- **scope:** meaningful icons and control-boundary contrast
- **override:** the icon is purely decorative and carries no information
- **exceptions:** purely decorative icons
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: meaningful icons and control boundaries meet contrast. Override: the icon is purely decorative and carries no information.

## COLOR-1013
- **strength:** default
- **scope:** card/surface separation from background in light mode
- **condition:** light theme
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: card/surface separation from background in light mode — must be satisfied. Applies when light theme.

## COLOR-1014
- **strength:** default
- **scope:** body text contrast in light mode
- **condition:** light theme
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: body text contrast in light mode — flagged when ratio < 4.5. Applies when light theme.

## COLOR-1015
- **strength:** default
- **scope:** normal (non-large) text meets the dark-mode contrast minimum
- **override:** large text or non-text UI, where the 3:1 threshold applies instead
- **exceptions:** large text or non-text UI (3:1 applies instead)
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: normal (non-large) text meets the dark-mode contrast minimum. Applies in dark theme. Override: large text or non-text UI, where the 3:1 threshold applies instead.

## COLOR-1016
- **strength:** default
- **scope:** dividers and borders across both themes
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: dividers and borders across both themes — must be satisfied.

## COLOR-1017
- **strength:** default
- **scope:** pressed/focused/disabled interaction states across both themes
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: pressed/focused/disabled interaction states across both themes — must be satisfied.

## COLOR-1018
- **strength:** default
- **scope:** one theming mechanism is used consistently across app surfaces, text, and icons
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: one theming mechanism is used consistently across app surfaces, text, and icons.

## COLOR-1019
- **strength:** default
- **scope:** modal/drawer scrim opacity
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: modal/drawer scrim opacity — must be satisfied.

## COLOR-2001
- **strength:** avoid
- **scope:** defaulting to a purple/violet accent aesthetic
- **override:** the brand or brief deliberately calls for purple, violet, or lila, executed with intent — a consistent palette, harmonised neutrals, and restrained gradients
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Discouraged: defaulting to a purple/violet accent aesthetic. Override: the brand or brief deliberately calls for purple, violet, or lila, executed with intent — a consistent palette, harmonised neutrals, and restrained gradients.

## COLOR-2002
- **strength:** default
- **scope:** the palette suits premium-consumer briefs (cookware, wellness, artisan, luxury, heritage-craft, DTC home goods)
- **condition:** those briefs
- **override:** the brief names those colors, or the identity is genuinely vintage, artisan, or warm-craft and the specific palette is justified for that brand
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: the palette suits premium-consumer briefs (cookware, wellness, artisan, luxury, heritage-craft, DTC home goods). Applies to those briefs. Override: the brief names those colors, or the identity is genuinely vintage, artisan, or warm-craft and the specific palette is justified for that brand.

## COLOR-2003
- **strength:** default
- **scope:** accent-color usage across all sections of one page
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: accent-color usage across all sections of one page — flagged when more than one distinct non-neutral hue appears in an accent role across the page.

## COLOR-2004
- **strength:** default
- **scope:** accent-color count and saturation for the page's default palette
- **enforcement:** must_surface
- **verification:** L1+L2
- **public_expression:** Required; surfaced on failure: accent-color count and saturation for the page's default palette — flagged when saturation >= 80%.

## COLOR-4001
- **strength:** default
- **scope:** a build's theme system, once the theme route resolves to custom
- **enforcement:** contextual
- **verification:** L3
- **selector:** DECISION-4001
- **public_expression:** Required; surfaced on failure: a build's theme system, once the theme route resolves to custom — must be satisfied.

## COLOR-4002
- **strength:** default
- **scope:** every build, including single-page builds
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: every build, including single-page builds — flagged when no tokens.css is emitted, or a token referenced in the page CSS via var(--*) has no matching declaration in tokens.css.

## COLOR-4003
- **strength:** avoid
- **scope:** any gradient in the artifact
- **override:** executed-with-intent brand-signature system (coherent, deliberate, evidenced), scoped to a background/non-text element only; the background-clip:text gradient invariant is never exempted
- **enforcement:** warn
- **verification:** L1
- **notes:** The executed-with-intent brand-signature override is scoped to background/non-text; the text-gradient invariant is never exempted.
- **public_expression:** Discouraged: gradients in the artifact. A headline that paints its text via a `background-clip: text` fill over a gradient is an exceptionless failure in every genre (active check). Purple/blue or cyan/magenta gradients on non-text elements are flagged unless they belong to a deliberate, coherent, evidenced brand-signature system applied to a background element. Effective strength avoid.

## COLOR-4004
- **strength:** default
- **scope:** base colors (paper, ink) used anywhere in the artifact
- **override:** the modern-minimal genre permits pure #fff paper — the monochrome style of brands such as Stripe or ElevenLabs
- **exceptions:** modern-minimal genre, paper token only, #fff specifically -- pure #000 remains banned even for modern-minimal
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: base colors (paper, ink) used anywhere in the artifact. Override: the modern-minimal genre permits pure #fff paper — the monochrome style of brands such as Stripe or ElevenLabs.

## COLOR-4005
- **strength:** default
- **scope:** neutral and surface color tokens carry appropriate warmth
- **override:** the modern-minimal genre permits chroma-free neutral tokens — the monochrome style of brands such as Stripe or ElevenLabs
- **exceptions:** modern-minimal genre
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: neutral and surface color tokens carry appropriate warmth. Override: the modern-minimal genre permits chroma-free neutral tokens — the monochrome style of brands such as Stripe or ElevenLabs.

## COLOR-4006
- **strength:** default
- **scope:** the accent color's viewport coverage stays restrained
- **override:** the atmospheric genre permits accent-tinted radial blooms over roughly 20% of the canvas, where the bloom is the design
- **exceptions:** atmospheric genre, radial-bloom background only
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Guidance: the accent color's viewport coverage stays restrained. Override: the atmospheric genre permits accent-tinted radial blooms over roughly 20% of the canvas, where the bloom is the design.

## COLOR-4007
- **strength:** avoid
- **scope:** an abstract background used as hero enrichment
- **condition:** the page has an abstract background
- **override:** the atmospheric genre permits up to two warm-toned radial blooms over roughly 20–30% of the canvas, fixed-attached and not animating
- **exceptions:** atmospheric genre, within the stated bounds
- **enforcement:** contextual
- **verification:** L2
- **notes:** The executed-with-intent brand-signature override is scoped to background/non-text.
- **public_expression:** Discouraged: an abstract background used as hero enrichment. Applies when the page has an abstract background. Override: the atmospheric genre permits up to two warm-toned radial blooms over roughly 20–30% of the canvas, fixed-attached and not animating.

## COLOR-4008
- **strength:** default
- **scope:** every colour value and font-family declaration in the artifact
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: every colour value and font-family declaration in the artifact — flagged when found used directly on a rule rather than via var(--token).
