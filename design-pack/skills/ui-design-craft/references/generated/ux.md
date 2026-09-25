# Design Pack runtime reference — UX (GENERATED; do not hand-edit)

Deterministic projection of the canonical Phase-B corpus (SHA-256 `16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b`, merge `44f10443c16e926515af86ebdd1d52e003ed98cc`) via `design-pack/tools/project_corpus.py`. Authoritative semantic source; fields rendered verbatim. 76 record(s).

## UX-1001
- **strength:** default
- **scope:** non-critical images
- **exceptions:** formats requiring lossless/legacy compatibility
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: non-critical images — must be satisfied.

## UX-1002
- **strength:** default
- **scope:** images and embedded media
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: images and embedded media — flagged when media element has neither.

## UX-1003
- **strength:** default
- **scope:** web font loading
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: web font loading — flagged when web font has no font-display declaration.

## UX-1004
- **strength:** default
- **scope:** font preload directives
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: font preload directives — must be satisfied.

## UX-1005
- **strength:** default
- **scope:** above-the-fold styles
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: above-the-fold styles — must be satisfied.

## UX-1006
- **strength:** default
- **scope:** non-hero components
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: non-hero components — must be satisfied.

## UX-1007
- **strength:** default
- **scope:** route/feature-level code organization
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: route/feature-level code organization — must be satisfied.

## UX-1008
- **strength:** default
- **scope:** third-party script tags
- **exceptions:** a script whose synchronous execution order is a genuine functional requirement
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: third-party script tags — must be satisfied.

## UX-1009
- **strength:** default
- **scope:** DOM read/write sequencing
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: DOM read/write sequencing — must be satisfied.

## UX-1010
- **strength:** default
- **scope:** asynchronously-loaded content regions
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: asynchronously-loaded content regions — must be satisfied.

## UX-1011
- **strength:** default
- **scope:** below-the-fold images and heavy media are lazy-loaded
- **exceptions:** above-the-fold / LCP-candidate media, which should NOT be lazy-loaded
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: below-the-fold images and heavy media are lazy-loaded.

## UX-1012
- **strength:** default
- **scope:** lists with 50 or more items
- **condition:** list length >= 50 items
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: lists with 50 or more items — must be satisfied. Applies when list length >= 50 items.

## UX-1013
- **strength:** default
- **scope:** per-frame main-thread work
- **enforcement:** must_surface
- **verification:** L2
- **public_expression:** Required; surfaced on failure: per-frame main-thread work — flagged when per-frame work exceeds ~16ms causing dropped frames.

## UX-1014
- **strength:** default
- **scope:** operations exceeding ~1 second
- **condition:** operation expected duration > 1s
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: operations exceeding ~1 second — must be satisfied. Applies when operation expected duration > 1s.

## UX-1015
- **strength:** default
- **scope:** tap and scroll input response
- **enforcement:** contextual
- **verification:** L2
- **public_expression:** Required; surfaced on failure: tap and scroll input response — must be satisfied.

## UX-1017
- **strength:** default
- **scope:** high-frequency browser events (scroll, resize, input)
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: high-frequency browser events (scroll, resize, input) — must be satisfied.

## UX-1018
- **strength:** default
- **scope:** offline/PWA and mobile network loss
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: offline/PWA and mobile network loss — must be satisfied.

## UX-1019
- **strength:** default
- **scope:** slow-network conditions
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: slow-network conditions — must be satisfied.

## UX-1020
- **strength:** default
- **scope:** chart type selection
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: chart type selection — must be satisfied.

## UX-1021
- **strength:** default
- **scope:** chart legends
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: chart legends — must be satisfied.

## UX-1022
- **strength:** default
- **scope:** chart axis labelling
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: chart axis labelling — must be satisfied.

## UX-1023
- **strength:** default
- **scope:** very large datasets rendered in a chart
- **condition:** 1000+ data points
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: very large datasets rendered in a chart — must be satisfied. Applies when 1000+ data points.

## UX-1024
- **strength:** default
- **scope:** pie/donut charts with many categories
- **condition:** more than 5 categories
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: pie/donut charts with many categories — flagged when pie/donut chart has more than 5 categories. Applies when more than 5 categories.

## UX-1025
- **strength:** heuristic
- **scope:** small chart datasets
- **condition:** dataset is small
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: small chart datasets — applied as contextual judgement, not a hard gate. Applies when dataset is small.

## UX-1026
- **strength:** default
- **scope:** chart axis tick density
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: chart axis tick density — must be satisfied.

## UX-1027
- **strength:** default
- **scope:** information density within one chart
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: information density within one chart — must be satisfied.

## UX-1028
- **strength:** default
- **scope:** chart visual decoration vs. data trends
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Required; surfaced on failure: chart visual decoration vs. data trends — must be satisfied.

## UX-1029
- **strength:** heuristic
- **scope:** data-heavy products
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: data-heavy products — applied as contextual judgement, not a hard gate.

## UX-1030
- **strength:** default
- **scope:** time-series charts
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: time-series charts — must be satisfied.

## UX-1031
- **strength:** heuristic
- **scope:** triage order when reviewing/prioritizing UI/UX work across categories
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: triage order when reviewing/prioritizing UI/UX work across categories — applied as contextual judgement, not a hard gate.

## UX-2001
- **strength:** default
- **scope:** pre-generation brief interpretation
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: pre-generation brief interpretation — must be satisfied.

## UX-2002
- **strength:** default
- **scope:** pre-generation design-read declaration
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: pre-generation design-read declaration — must be satisfied.

## UX-2003
- **strength:** default
- **scope:** ask a clarifying question only when a brief is genuinely ambiguous
- **condition:** the design read truly diverges on the unresolved point
- **override:** if context allows a confident inference, do not ask
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: ask a clarifying question only when a brief is genuinely ambiguous. Applies when the design read truly diverges on the unresolved point. Override: if context allows a confident inference, do not ask.

## UX-2004
- **strength:** default
- **scope:** choose and combine a foundational design system deliberately
- **override:** for an aesthetic direction with no single official package, build on native CSS plus Tailwind plus a maintained component library
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: choose and combine a foundational design system deliberately. Override: for an aesthetic direction with no single official package, build on native CSS plus Tailwind plus a maintained component library.

## UX-2005
- **strength:** default
- **scope:** sourcing priority for visual assets and social-proof logos
- **override:** neither image generation nor real photography available — mark placeholder slots clearly and name the images still needed
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: prioritise where visual assets and social-proof logos are sourced. Override: when neither image generation nor real photography is available, mark each placeholder slot clearly and tell the user which images are still needed.

## UX-2006
- **strength:** default
- **scope:** detect redesign mode, audit before changing, and preserve the existing product surface
- **condition:** the task is a redesign, not a greenfield build
- **override:** explicit user approval to change URL structure, primary nav labels, form field names or order, brand logo/wordmark, or existing legal/consent/cookie copy
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: detect redesign mode, audit before changing, and preserve the existing product surface. Applies when the task is a redesign, not a greenfield build. Override: explicit user approval to change URL structure, primary nav labels, form field names or order, brand logo/wordmark, or existing legal/consent/cookie copy.

## UX-2007
- **strength:** default
- **scope:** pre-ship gate over every other rule's compliance
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: pre-ship gate over every other rule's compliance — must be satisfied.

## UX-2008
- **strength:** default
- **scope:** workflow order when image generation is available for a visually-important task
- **condition:** image generation available and the work centers on frontend visual quality
- **override:** a mostly-technical job (a bug fix), a precise design system already supplied, or structural rather than visual work
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: sequence the workflow so image generation runs first when it matters. Applies when image generation is available and the work centers on frontend visual quality. Override: a mostly-technical job (a bug fix), a precise design system already supplied, or work that is structural rather than visual.

## UX-4001
- **strength:** default
- **scope:** any output about to be handed back to the user
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: any output about to be handed back to the user — flagged when stamp absent.

## UX-4002
- **strength:** default
- **scope:** route an incoming brief to the Component-scope flow rather than the full-page Design flow before Step 0
- **condition:** at least two signals fire: the brief names a single UI element; the brief is 30 words or fewer and refers to one element; the target is a single component file; or the user says "just the X" / "only the Y" / "this one element"
- **override:** only one signal fires and the brief is otherwise multi-section, so stay in the page-level flow
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: route an incoming brief to the Component-scope flow rather than the full-page Design flow before Step 0. Applies when at least two signals fire: the brief names a single UI element; the brief is 30 words or fewer and refers to one element; the target is a single component file; or the user says "just the X" / "only the Y" / "this one element". Override: only one signal fires and the brief is otherwise multi-section, so stay in the page-level flow.

## UX-4003
- **strength:** default
- **scope:** a brief genuinely ambiguous between component scope and page scope (for example, "design a pricing section")
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: a brief genuinely ambiguous between component scope and page scope (for example, "design a pricing section").

## UX-4004
- **strength:** default
- **scope:** a project that already has code (package.json, tailwind.config, index.html, any CSS) before any Hallmark output is written
- **override:** the user says to ignore the existing project — skip pre-flight and state that it was skipped
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: a project that already has code (package.json, tailwind.config, index.html, any CSS) before any Hallmark output is written. Override: the user says to ignore the existing project — skip pre-flight and state that it was skipped.

## UX-4005
- **strength:** heuristic
- **scope:** repeat Hallmark runs in the same project after the first pre-flight scan may reuse the cache.json and tailwind.config mtimes are no newer than the cached .hallmark/preflight.json and the user did not ask to re-scan
- **condition:** package
- **override:** the user asks to refresh pre-flight, or the tracked config mtimes are newer than the cache — re-scan
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance (heuristic): repeat Hallmark runs in the same project after the first pre-flight scan may reuse the cache. Applies when package.json and tailwind.config mtimes are no newer than the cached .hallmark/preflight.json and the user did not ask to re-scan. Override: the user asks to refresh pre-flight, or the tracked config mtimes are newer than the cache — re-scan.

## UX-4006
- **strength:** default
- **scope:** entering the default Design flow, before any macrostructure or theme is picked
- **override:** the audit, study, or redesign --mood verbs read context from the target rather than the user, so the gate is silent for them
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: entering the default Design flow, before any macrostructure or theme is picked. Override: the audit, study, or redesign --mood verbs read context from the target rather than the user, so the gate is silent for them.

## UX-4007
- **strength:** default
- **scope:** picking a genre before the theme route, once per Design-flow run
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: picking a genre before the theme route, once per Design-flow run — must be satisfied.

## UX-4008
- **strength:** default
- **scope:** choosing between the catalog and custom theme routes once a macrostructure is picked
- **override:** the brief asks for a custom or tailored theme, names a specific brand anchor color, describes a multi-attribute aesthetic no single catalog theme carries (three or more vibe words), or attaches a brand-mood reference — then ask one short custom-vs-catalog follow-up and route on the answer
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: choosing between the catalog and custom theme routes once a macrostructure is picked. Override: the brief asks for a custom or tailored theme, names a specific brand anchor color, describes a multi-attribute aesthetic no single catalog theme carries (three or more vibe words), or attaches a brand-mood reference — then ask one short custom-vs-catalog follow-up and route on the answer.

## UX-4009
- **strength:** default
- **scope:** the theme system of a page-scope Design-flow build
- **override:** the user later redirects (for example, asks for a different theme or to ignore the extracted DNA) — route back to the normal catalog/custom dispatch and resume diversification
- **enforcement:** contextual
- **verification:** L1
- **selector:** DECISION-4001 (theme-route)
- **public_expression:** Guidance: the theme system of a page-scope Design-flow build. Override: the user later redirects (for example, asks for a different theme or to ignore the extracted DNA) — route back to the normal catalog/custom dispatch and resume diversification.

## UX-4010
- **strength:** default
- **scope:** the macrostructure pick, the diversification rotation summary, and the nav/footer archetype pick, each before any code is written
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: the macrostructure pick, the diversification rotation summary, and the nav/footer archetype pick, each before any code is written — must be satisfied.

## UX-4011
- **strength:** default
- **scope:** a build's theme system, once the theme route resolves to catalog, picking among the 21 named themes
- **exceptions:** the theme route is studied-DNA or custom (cluster membership only governs the catalog route)
- **enforcement:** contextual
- **verification:** L1
- **selector:** DECISION-4001
- **public_expression:** Required; surfaced on failure: a build's theme system, once the theme route resolves to catalog, picking among the 21 named themes — flagged when the picked theme is outside the active genre's cluster.

## UX-4012
- **strength:** default
- **scope:** choosing a hero-enrichment technique once the image-need check confirms a need
- **exceptions:** complex character motion genuinely beyond what hand-building can achieve
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: choosing a hero-enrichment technique once the image-need check confirms the brief needs one — flagged when Lottie is used while a lower tier (CSS art, hand-built SVG, or generated imagery) would suffice.

## UX-4013
- **strength:** default
- **scope:** every page-scope Design-flow build, after Step 4 and before code is emitted
- **override:** component-scope builds replace the preview with the eight-state demo wrapper; when a design.md already exists at the root, skip only the lock-the-system CTA line
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: every page-scope Design-flow build, after Step 4 and before code is emitted. Override: component-scope builds replace the preview with the eight-state demo wrapper; when a design.md already exists at the root, skip only the lock-the-system CTA line.

## UX-4014
- **strength:** default
- **scope:** writing `.hallmark/log.json` after every page-scope Design-flow build (default verb) or a multi-page redesign
- **override:** component-scope builds append no log entry at all (STRUCT-4001's stamp is the component-scope durable record instead); a multi-page redesign writes one combined entry with "scope": "app" rather than one entry per page
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Required; surfaced on failure: writing `.hallmark/log.json` after every page-scope Design-flow build (default verb) or a multi-page redesign — flagged when entry count exceeds 20, or the newest entry is not at array index 0. Override: component-scope builds append no log entry at all (STRUCT-4001's stamp is the component-scope durable record instead); a multi-page redesign writes one combined entry with "scope": "app" rather than one entry per page.

## UX-4015
- **strength:** default
- **scope:** a project that has a design.md at its root (a system-managed project).md exists
- **condition:** such a design
- **override:** a single-page project with no design.md — skip this step and emit only tokens.css
- **enforcement:** contextual
- **verification:** L1
- **public_expression:** Guidance: a project that has a design.md at its root (a system-managed project). Applies when such a design.md exists. Override: a single-page project with no design.md — skip this step and emit only tokens.css.

## UX-4016
- **strength:** default
- **scope:** whether to emit a design.md capturing the build's design system as a portable file
- **condition:** the user explicitly asks (for example, to lock the system or make it portable)
- **override:** a design.md already exists — refresh its Exports section rather than overwriting the file
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: whether to emit a design.md capturing the build's design system as a portable file. Applies when the user explicitly asks (for example, to lock the system or make it portable). Override: a design.md already exists — refresh its Exports section rather than overwriting the file.

## UX-4017
- **strength:** default
- **scope:** every build, as the final step before handoff
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: every build, as the final step before handoff — must be satisfied.

## UX-4018
- **strength:** default
- **scope:** a demo video used as hero enrichment
- **condition:** the page has a demo video
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a demo video used as hero enrichment. Applies when the page has a demo video.

## UX-4019
- **strength:** default
- **scope:** any edit Hallmark makes to an existing project (default verb or redesign) is non-destructive by default
- **override:** the user explicitly requests deletion, or signs off on a per-file plan that enumerates what will be removed
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: any edit Hallmark makes to an existing project (default verb or redesign) is non-destructive by default. Override: the user explicitly requests deletion, or signs off on a per-file plan that enumerates what will be removed.

## UX-4020
- **strength:** default
- **scope:** `hallmark audit` output
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: `hallmark audit` output — must be satisfied.

## UX-4021
- **strength:** default
- **scope:** an audited file whose stamp names a genre
- **condition:** the stamp names one
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: an audited file whose stamp names a genre. Applies when the stamp names one.

## UX-4022
- **strength:** default
- **scope:** entering `hallmark redesign`, before any other step
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: entering `hallmark redesign`, before any other step — must be satisfied.

## UX-4023
- **strength:** default
- **scope:** a multi-page redesign, before touching any individual page
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: a multi-page redesign, before touching any individual page — must be satisfied.

## UX-4024
- **strength:** default
- **scope:** a page inside a designed-as-app project that genuinely needs something design.md does not allow.md does not currently permit
- **condition:** a page needs a deviation the design
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: a page inside a designed-as-app project that genuinely needs something design.md does not allow. Applies when a page needs a deviation the design.md does not currently permit.

## UX-4025
- **strength:** default
- **scope:** a single-page redesign
- **override:** a design.md exists at the root — treat it as a designed-as-app project, read the design.md, and follow it instead of the single-page rules
- **enforcement:** contextual
- **verification:** L3
- **public_expression:** Guidance: a single-page redesign. Override: a design.md exists at the root — treat it as a designed-as-app project, read the design.md, and follow it instead of the single-page rules.

## UX-4026
- **strength:** default
- **scope:** a single-page redesign with a `--mood <name>` argument, or an explicit request for a different kind of design than the current genre
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: a single-page redesign with a `--mood <name>` argument, or an explicit request for a different kind of design than the current genre — must be satisfied.

## UX-4027
- **strength:** default
- **scope:** routing `hallmark study` input to image mode or URL mode
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: routing `hallmark study` input to image mode or URL mode — must be satisfied.

## UX-4028
- **strength:** default
- **scope:** hallmark study before extracting anything, in either mode
- **override:** the user's own prior work, or a public reference site the user cites for their own inspiration — proceed
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: hallmark study before extracting anything, in either mode. Override: the user's own prior work, or a public reference site the user cites for their own inspiration — proceed.

## UX-4029
- **strength:** default
- **scope:** `hallmark study` in URL mode, before WebFetch fires
- **override:** an ambiguous URL (unfamiliar agency page, personal portfolio, unknown SaaS) -> ask once rather than auto-refuse
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: `hallmark study` in URL mode, before WebFetch fires — flagged when a hard-refuse pattern matches. Override: an ambiguous URL (unfamiliar agency page, personal portfolio, unknown SaaS) -> ask once rather than auto-refuse.

## UX-4031
- **strength:** default
- **scope:** HTML/CSS/scripts fetched from a URL in `hallmark study`'s URL mode
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: HTML/CSS/scripts fetched from a URL in `hallmark study`'s URL mode — must be satisfied.

## UX-4032
- **strength:** default
- **scope:** a WebFetch response in `hallmark study` URL mode
- **enforcement:** must_surface
- **verification:** L1
- **public_expression:** Required; surfaced on failure: a WebFetch response in `hallmark study` URL mode — flagged when both conditions hold.

## UX-4033
- **strength:** default
- **scope:** `hallmark study` when the user supplies more than one screenshot or URL
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: `hallmark study` when the user supplies more than one screenshot or URL — must be satisfied.

## UX-4034
- **strength:** default
- **scope:** emitting a design.md from a study diagnosis
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: emitting a design.md from a study diagnosis. Applies when, after a diagnosis, the user asks to lock the DNA, write/export a design.md, or make the DNA portable.

## UX-4035
- **strength:** default
- **scope:** the Provenance block of a design.md emitted from a URL-mode study diagnosis
- **override:** the attestation status is already known from earlier in the conversation — carry it forward rather than re-asking
- **enforcement:** contextual
- **verification:** none
- **selector:** DECISION-4002 (study-emission)
- **public_expression:** Guidance: the Provenance block of a design.md emitted from a URL-mode study diagnosis. Override: the attestation status is already known from earlier in the conversation — carry it forward rather than re-asking.

## UX-4036
- **strength:** default
- **scope:** a design.md emission request from a URL-mode study diagnosis
- **enforcement:** contextual
- **verification:** none
- **selector:** DECISION-4002
- **public_expression:** Required; surfaced on failure: a design.md emission request from a URL-mode study diagnosis — must be satisfied.

## UX-4037
- **strength:** default
- **scope:** the content of a `design.md` emitted from `study`
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: the content of a `design.md` emitted from `study` — must be satisfied.

## UX-4038
- **strength:** default
- **scope:** after a `hallmark study` diagnosis is returned
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Required; surfaced on failure: after a `hallmark study` diagnosis is returned — must be satisfied.

## UX-4039
- **strength:** default
- **scope:** suggesting a catalog theme from an extracted DNA schema, once the schema is filled
- **enforcement:** contextual
- **verification:** none
- **public_expression:** Guidance: suggesting a catalog theme from an extracted DNA schema, once the schema is filled.
