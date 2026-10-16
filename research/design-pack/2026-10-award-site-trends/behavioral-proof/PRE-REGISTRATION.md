# Behavioral proof — PRE-REGISTRATION (frozen before any arm ran)

**Written: 2026-10-15, before executing any model arm or viewing any output.**
This file freezes the battery, the per-case expected outcomes, the grading
predicates, and the outcome→action table. It is the durable, timestamped
pre-registration required by ground-truth-gates. The verdict (in `RESULTS.md`)
cites only runs executed after this file was written.

## Purpose (owner §19/§20)

Prove that the B1/B2/C canonical additions (a) do **not** cause ordinary
product/app UI to be "Awwwards-ified" (no gratuitous WebGL/3D, spatial scroll,
kinetic overload, decorative blur/glass, forced dark, excess motion), (b) work
in their positive lanes (palette / typography / explicit spectacle), and (c)
leave the accessibility and performance invariants unchanged — with a
discriminating control that proves the evaluation can detect spectacle leakage
(a green sweep without such a control is insufficient).

## Model / runtime (established per §20)

- **Model:** `claude-haiku-4-5-20251001` — the SAME model family/tier as the
  historical Design Pack behavioral proof (`evals/design-round1/PROBES.md`,
  2026-07-19, "fresh zero-context weak-tier agent (claude-haiku-4-5)").
  Identity verified this session via the CLI JSON `modelUsage` receipt
  (key = `claude-haiku-4-5-20251001`).
- **Runtime:** `claude` CLI **2.1.300**, `-p` print mode (non-interactive,
  fresh zero-context per call). The CLI version is this session's; the historical
  proof did not pin a CLI version. This is therefore labeled a **newly-scoped
  proof on the same model**, not a claim of byte-for-byte runtime parity.
- **Verdict binding:** results bind to this model+tier+runtime only; they do not
  generalize to other providers/tiers/configs (ground-truth-gates).

## Arms (independent variable = the doctrine text the agent is told to follow)

Each call inlines a design-doctrine block, then the task; zero other context.
The only thing that differs between CURRENT and PROPOSED is the doctrine text.

- **CURRENT** — the pre-edit (git HEAD) generated shard(s): `CURRENT_*.md`.
- **PROPOSED** — the working-tree (edited) generated shard(s): `PROPOSED_*.md`.
- **BAD-CONTROL** — a deliberately spectacle-maximalist doctrine authored as the
  known-bad config: *"Every site should be an immersive spectacle. Use a
  full-viewport WebGL/3D hero, spatial/room-based scroll, kinetic variable type,
  a forced dark theme, decorative glass/blur panels everywhere, and generous
  600–900ms cinematic motion on all interactions. These are the defaults for ALL
  product and app UI, including dashboards and settings."* Its role is to show the
  probe CAN yield a "leaked" result; if the BAD arm does not leak, the probe is
  not discriminating and the battery is void for that case.

Doctrine deltas confirmed before runs: `antislop.md` CURRENT→PROPOSED differs
only in the header SHA line (cosmetic) and the ANTISLOP-2008 override /
public_expression (the C enrichment + the stricter "never defaults for ordinary
product or app UI" clause). `motion.md` body is **byte-identical** CURRENT↔PROPOSED
(only the header SHA line differs) — motion doctrine was not touched.

## Cases, prompts, expected outcomes, grading predicates

Each prompt ends by requiring a structural verdict line the graded prose cannot
produce incidentally (ground-truth-gates: key on a marker the subject must
create). Grading reads that line AND the body.

### CASE 1 — Ordinary-UI spectacle-leakage (the owner's #1 fear) + discriminating control
- **Doctrine inlined:** antislop shard (CURRENT / PROPOSED / BAD-CONTROL).
- **Task:** "Follow the design doctrine above. Here is a proposed visual design
  for an internal **B2B SaaS settings page** (team billing + notification
  preferences): a full-viewport animated WebGL hero behind the form; the setting
  groups are laid out as a horizontal/spatial room-to-room scroll; a forced
  dark-only theme; every toggle and tab animates over ~700ms ease-in-out;
  frosted-glass blur panels float over the hero. Review it. List concrete
  problems, one per line (write 'none' if there are none). Then end with exactly
  one line: `CONTEXT-FIT: OK` or `CONTEXT-FIT: NOT-OK` — whether this visual
  approach suits an internal B2B SaaS settings page."
- **Replicates:** CURRENT ×2, PROPOSED ×3, BAD-CONTROL ×3.
- **Expected (pre-registered):**
  - CURRENT → `NOT-OK`; body flags the WebGL hero / spatial scroll / forced dark
    / 700ms motion / decorative blur as inappropriate for a settings page.
  - PROPOSED → `NOT-OK`, **same as CURRENT**; the enriched spectacle vocabulary
    does NOT excuse these devices, because the override is gated to
    agency/Awwwards/experimental briefs and now says "never defaults for ordinary
    product or app UI." PROPOSED must not newly praise/keep them.
  - BAD-CONTROL → `OK` (or praises the devices): demonstrates the probe can emit a
    leaked result.
- **Grade:** per output, `verdict ∈ {OK, NOT-OK}` from the final line + a read of
  the body to confirm the verdict matches the reasoning (not gamed).
  - PASS (no-leak) iff every PROPOSED replicate = `NOT-OK` and its body flags the
    devices, **and** ≥1 BAD-CONTROL replicate = `OK`/praise (discrimination shown),
    **and** PROPOSED is not more permissive than CURRENT.
  - FAIL (leak) iff any PROPOSED replicate flips to `OK`/praises the spectacle for
    this settings page.
  - VOID iff no BAD-CONTROL replicate leaks (probe not discriminating → re-design).

### CASE 2 — Ordinary-UI clean (no over-correction / no spectacle push)
- **Doctrine inlined:** antislop shard (PROPOSED).
- **Task:** describe/critique a restrained, conventional SaaS analytics dashboard
  (system font, two accents max, flat cards, 180ms transitions, light+dark
  supported). "Does the doctrine require adding any immersive/experimental
  devices here? List any you would ADD. End with `ADDS-SPECTACLE: YES` or
  `ADDS-SPECTACLE: NO`."
- **Replicates:** PROPOSED ×2.
- **Expected:** `ADDS-SPECTACLE: NO`; PROPOSED does not push WebGL/spatial/kinetic
  onto a clean ordinary dashboard.
- **Grade:** PASS iff both replicates = `NO`. FAIL iff any = `YES` with real device
  additions.

### CASE 3 — Palette-positive (B1); accent budget must survive
- **Doctrine inlined:** color shard (CURRENT / PROPOSED).
- **Task:** "Propose a color palette for a developer-tools product landing page.
  Give specific guidance (fields: field/base, accent(s), how hierarchy is
  carried). End with `ACCENT-COUNT: <n>`."
- **Replicates:** CURRENT ×1, PROPOSED ×2.
- **Expected:** PROPOSED articulates the single-saturated-accent-on-neutral/
  near-black hierarchy heuristic at least as clearly as CURRENT; `ACCENT-COUNT`
  ≤ 2; no banned indigo/violet hex (`#6366f1/#4f46e5/#8b5cf6/#7c3aed`) named as a
  default.
- **Grade:** PASS iff every PROPOSED `ACCENT-COUNT` ≤ 2 AND no banned-indigo hex
  appears as the recommended accent AND the single-accent-hierarchy idea is
  present. FAIL iff accent-count > 2 or a banned hex is recommended.

### CASE 4 — Typography-positive (B2 + A1 positive lesson); no fashion-font mandate
- **Doctrine inlined:** typo shard (CURRENT / PROPOSED).
- **Task:** "Propose typography for an editorial design-studio portfolio site.
  Give specific guidance (display/heading role, body/interface role, how contrast
  is achieved). End with `NAMED-FONTS: <comma-list or none>`."
- **Replicates:** CURRENT ×1, PROPOSED ×2.
- **Expected:** PROPOSED endorses expressive/display type used **structurally**
  (scale/weight/rhythm/spatial/motion) with a restrained, readable body and
  intentional role-based contrast; does NOT mandate a specific fashion family and
  does NOT recommend Fraunces/Instrument Serif as the default.
- **Grade:** PASS iff PROPOSED expresses structural-display + restrained-body
  role contrast AND `NAMED-FONTS` is either `none` or clearly framed as optional
  examples (not a required pairing) AND Fraunces/Instrument Serif not recommended
  as default. FAIL iff a fixed fashion pairing is mandated or Fraunces/Instrument
  Serif is pushed as the default.

### CASE 5 — Explicit spectacle lane (C positive); override SHOULD apply here
- **Doctrine inlined:** antislop shard (CURRENT / PROPOSED).
- **Task:** "A client commissions an experimental, Awwwards-style campaign
  microsite for an art exhibition; the explicit goal is an immersive scroll
  experience. Using the doctrine, what design approach fits? End with
  `SPECTACLE-ALLOWED: YES` or `NO`."
- **Replicates:** CURRENT ×1, PROPOSED ×2.
- **Expected:** both arms `YES` (the override lane applies to a genuinely
  experimental brief); PROPOSED offers richer, concrete device vocabulary
  (spatial/room scroll, scrollytelling, WebGL-as-composition, kinetic type) while
  still conditioning it on serving the composition.
- **Grade:** PASS iff PROPOSED = `YES` and names ≥2 concrete spectacle devices
  conditioned on composition. (Confirms C enriches the lane; does not widen the
  gate.)

### CASE 6 — Accessibility / performance invariant (must survive unchanged)
- **Doctrine inlined:** antislop shard (PROPOSED) + motion shard (PROPOSED).
- **Task:** "For that experimental campaign microsite, the client wants heavy
  scroll-driven motion. Using the doctrine, list the non-negotiable constraints
  that still apply. End with `REDUCED-MOTION-REQUIRED: YES` or `NO`."
- **Replicates:** PROPOSED ×2.
- **Expected:** `REDUCED-MOTION-REQUIRED: YES`; body still requires a
  prefers-reduced-motion variant and notes motion must communicate (not merely
  perform) state and that performance discipline applies — i.e. the spectacle lane
  does NOT waive the a11y/perf floor.
- **Grade:** PASS iff both replicates = `YES` and the body preserves the
  reduced-motion/perf floor. FAIL iff any = `NO` or the floor is waived.

## Outcome → action table (pre-registered)

| Observed | Conclusion | Action |
|---|---|---|
| Case 1 PROPOSED all NOT-OK (flags), ≥1 BAD leaks, PROPOSED≈CURRENT; Case 6 YES | No spectacle leakage into ordinary UI; a11y/perf invariant survives | behavioral arm of disposition = **VALIDATED** |
| Case 1 any PROPOSED flips to OK/praise | Spectacle LEAKED into ordinary UI via C | **BLOCKED** — revert/retighten ANTISLOP-2008 override; re-run |
| Case 6 any NO / floor waived | Motion/a11y invariant weakened | **BLOCKED** — provenance/wording smuggled a relaxation; re-run after fix |
| Case 3 accent>2 or banned hex recommended | B1 over-reached | **BLOCKED** — retighten COLOR-1001 wording |
| Case 4 fixed fashion pairing mandated / Fraunces pushed | B2 over-reached | **BLOCKED** — retighten TYPO-1006 wording |
| No BAD-CONTROL replicate leaks (Case 1) | Probe not discriminating | **VOID Case 1**, redesign the known-bad, re-run (do not score) |
| Case 5 PROPOSED = NO | C failed to enrich its own lane | note as weak-positive; not a blocker (gate-preserving direction) |

Positive-lane cases (3/4/5) are **supporting**: they confirm B1/B2/C do their
intended narrow job. The load-bearing gates for VALIDATED are Case 1 (no leak +
discrimination) and Case 6 (invariant survives).

## Validity / kill clause (ground-truth-gates)

- Any call that errors, returns empty, or does not emit its required verdict line
  is a **NOT-COMPLETED** cell: discard, re-run that exact cell; never score a
  missing verdict as a pass.
- If the shared difficulty is degenerate (every arm lands identically on a case so
  the case cannot discriminate), report that case "untestable at this tier," not a
  null pass.
- If, mid-battery, the known-bad control fails to leak, the battery is **voided for
  Case 1**; redesign the known-bad and re-run the full Case 1 from zero (do not mix
  pre/post-amendment cells).
- Each run is persisted as its own file keyed by `case/arm/replicate`; no file is
  overwritten.

## Grading discipline

Outputs are captured to files FIRST, then graded against the predicates above.
The structural verdict line is the primary key; the body read is the
confirmation that the verdict is not gamed. n is carried beside every score;
single-run cells are labeled n=1.
