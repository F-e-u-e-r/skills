# Provenance and acknowledgements

Full source history and acknowledgements for the skill packs in this repository — what was distilled or adapted, from whom, and under what license. Repository overview: [`../README.md`](../README.md); license: [`../LICENSE`](../LICENSE) and [`../THIRD-PARTY-NOTICES.md`](../THIRD-PARTY-NOTICES.md).

<details>
<summary><strong>Show all sources and acknowledgements</strong></summary>

This pack distills and adapts ideas from:

- **gyozalab** — Threads post; the one-shot "Fable 5 → durable institution"
  framing that seeded this pack:
  <https://www.threads.com/@gyozalab/post/DaS69OPFJxy>
- **林長揚** — Facebook post; AI-harness / system-improvement brief
  (institution-design ideas in `delegation-and-review` and `skill-authoring`):
  <https://www.facebook.com/story.php?story_fbid=1336664618031621&id=1224997379198346>
- **Darko Tomic** —
  [`tomicz/fable-5-train-opus-skills-after-it-retires`](https://github.com/tomicz/fable-5-train-opus-skills-after-it-retires),
  MIT License, Copyright (c) 2026 Darko Tomic; skill-library method in
  `skill-authoring`.
- **kannaiah** —
  [Reddit comment](https://www.reddit.com/r/ClaudeAI/comments/1ukynrw/comment/ovnh8zu/)
  on operational rigor, adapted into `operational-rigor`.
- **Boris Cherny** (Anthropic, Claude Code) — interview clips on
  per-release system-prompt ablation, as embedded with commentary in the
  YouTube video "Claude Code 之父建議，每六個月刪光你的 CLAUDE.md？"
  (<https://www.youtube.com/watch?v=Z-4AsgTYv2c>). The three-bucket
  triage adopted into the rule is the commentary channel's own proposal
  (channel named at the link), ideas only; tier-change re-probe rule in
  `skill-authoring` §7.
- **firaen22** (credited as "Friend A" before going public) — private
  Discord notes shared with the maintainer (a checks/-harness design note
  and a measured Claude Code harness export), adapted into
  `ground-truth-gates`, `operational-rigor`, `delegation-and-review`, and
  `skill-authoring`; source text is not distributed. Later contributed the
  cost-asymmetric golden runner and the first structural commit-hook
  parser work through GitHub PRs.
- **pro_ai.news** — Threads post; five-step goal-coaching protocol, adapted
  into `personal-goal-planning`:
  <https://www.threads.com/@pro_ai.news/post/DadQkGHjxq->
- **Curtis Chou** —
  [`curtischoutw/claude-institution`](https://github.com/curtischoutw/claude-institution)
  @ `8dea062`, MIT License, Copyright (c) 2026 Curtis Chou. The
  `verify-before-stop` hook is adapted from its `verify_gate.py` (itself
  adapted from Miguok/fable-harness), and ~10 judgment rules were absorbed
  into operational-rigor / delegation-and-review / skill-authoring. Reviewed
  in full; its always-loaded/nudge/template layer was deliberately not
  adopted — same reasoning as dropped-item 5. A 2026-07-24 delta pass over
  its post-`8dea062` commits adopted three further ideas: the explicit-model
  + labeled-dispatch rule and the ceiling-inversion ladder (`delegation-
  and-review` §1/§4, the latter from their 「Fable 起手」mechanism), and the
  forged-tool-output defense (`operational-rigor` §4, from their hard-rule
  #15 and its two logged incidents); the same pass ported their upstream's
  (Miguok) fail-open-telemetry fix idea into our `verify-before-stop` hook
  (landed separately as PR #74).
- **echo-of-machines** —
  [`echo-of-machines/fable-advisor`](https://github.com/echo-of-machines/fable-advisor);
  the advice-mode consult (a stronger tier recommends, the current tier keeps
  executing), adapted tier-relative into `delegation-and-review` §4. Same
  pattern as Anthropic's
  [advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool).
  Ideas only; no code taken.
- **TheColliny** —
  [`TheColliny/FableClaudeMDForOpus`](https://github.com/TheColliny/FableClaudeMDForOpus);
  event-phrased routing, adapted as the state-phrased trigger rule in
  `skill-authoring` §5. Ideas only; no code taken.
- **hamanpaul** —
  [`hamanpaul/testpilot-core`](https://github.com/hamanpaul/testpilot-core);
  its tier-2 environment-recovery design — the escalation counter driven by
  the orchestrator's own verify gate rather than a worker's self-report, and
  the intervention marker kept distinct from a passed gate — adapted into
  `delegation-and-review` §4. MIT, ideas only; no code taken.
- **sd0xdev** —
  [`sd0xdev/sd0x-dev-flow`](https://github.com/sd0xdev/sd0x-dev-flow)
  (MIT); a 2026-08-04 whole-repo mining sweep (98 skills) of this dev-flow
  command plugin. Three disciplines adopted after cross-family review: its
  `debug` skill's hypothesis-elimination probe protocol and its
  `necessity-audit` skill's per-element evidence thresholds (`operational-rigor`
  §6 and §2), and its `orchestrate` skill's deny-by-default admission gate keyed
  on monitoring coverage (`security-architect`, AI-agent/MCP section). Ideas
  only; no text taken.
- **openai/codex-security** —
  [`openai/codex-security`](https://github.com/openai/codex-security)
  (Apache-2.0); the `security-architect` half of a 2026-07-31 two-repo
  mining pass run jointly with
  [`Mapleeeeeeeeeee/cc-session-reader`](https://github.com/Mapleeeeeeeeeee/cc-session-reader)
  — that repo's material lands in the review/handoff batch's own
  entry. Method: a ten-agent verbatim scan across two model families
  plus a third-family cross-check, every load-bearing citation
  re-verified against the source, keeping only concepts the
  adjudication found no existing-skill equivalent for. Ideas only, no
  text. This batch, all from the security product's threat model,
  runtime security notes, bundled review doctrine, and tracker-intake
  rules: subprocess-environment minimization, the policy-shaped-data
  tier, the severity/confidence split, system-scoped threat models,
  and the audience-check-on-disclosure rule. (The review/handoff batch
  carries its own acknowledgements entry.)
- **2026-07 security-skill audit** — a 12-source sweep of community
  "security" skills preceding the 2026-07-12 doctrine batch. Idea-level
  adoptions only, no code: **eddygk/skill-vetting** (anti-override rule →
  `delegation-and-review` §7; original GitHub repository URL unavailable
  as of 2026-07-24 — attribution retained as eddygk/skill-vetting, GitHub), **UnitOneAI/SecuritySkills** (load-time
  execution audit → `operational-rigor` §2),
  **mukul975/Anthropic-Cybersecurity-Skills** (JWT `kid`/`jku`/`x5u` item,
  zero-width/bidi sweep), **gitgoodordietrying** (SCA-in-CI),
  **jgarrison929** (magic-byte upload validation). The same audit judged 3
  of the 12 to be live trojans — all self-described security tools; nothing
  from those was adopted, and the finding itself became doctrine
  (`operational-rigor` §2: self-described security tools earn stricter
  scrutiny, not less).
- **openai/codex-security · Mapleeeeeeeeeee/cc-session-reader —
  review/handoff batch (2026-07-31)** — from
  [`openai/codex-security`](https://github.com/openai/codex-security) and
  [`Mapleeeeeeeeeee/cc-session-reader`](https://github.com/Mapleeeeeeeeeee/cc-session-reader)
  (both Apache-2.0; ideas only, no text — the same pass's
  `security-architect` batch carries its own entry; same method there
  and here: ten-agent verbatim scan, third-family cross-check,
  load-bearing citations re-verified). From the compression tool's
  decision records: retention keyed on re-derivability,
  same-attempt/same-failure-only merging, labelled elisions with
  working retrieval steps, and the spot-check-what-was-dropped audit
  duty (`delegation-and-review` §5). From the security product's
  completion, comparison, and release-pipeline rules: the
  costumed-as-completion shapes a blocked run refuses
  (`delegation-and-review` §2), absence-is-not-resolution for recurring
  review campaigns (`delegation-and-review`
  `references/recurring-sweep-ledgers.md`),
  convergence-raises-priority-not-status (`cross-model-review` §3), and
  consumer-position verification (`operational-rigor` §4).
- **Sahir619** —
  [`Sahir619/fable-method`](https://github.com/Sahir619/fable-method),
  MIT License; a parallel Fable-sunset distillation with a published
  trap-scenario eval program (wins and nulls both). Ideas adopted on
  merit, no files copied: the behavioral trap-armed clause in
  `ground-truth-gates` (from their published negative — safe outcomes
  produced by runs that never met the trap), the
  ships-with-its-failing-test covenant in the Evals section, trap
  mechanisms from their published eval program, re-implemented as fresh
  fixtures in this pack's private suite, and — across `operational-rigor`,
  `delegation-and-review`, and `skill-authoring` — the authority-order,
  twin-sweep, ask-classification, prescribed-follow-up, and
  completion-claim-audit rules plus the enforcement ladder, pointer
  caution, and red-line authoring gate (that batch's behavioral rules
  probe-tested on those fixtures before shipping; its design/normative
  ones labeled `unprobed` in-body). From the v1.4.0 delta and its
  follow-ups — the AUTH-quote artifact, the owed-lines artifact gate,
  the installed-skill non-authorization vector, the gate-placement
  rule, the `domain-evidence-discipline` skill (their domain-adapter
  schema condensed to one four-nouns pattern), and the declared-scope,
  orient-first, and debris rules — all shipping explicitly `unprobed`
  in-body per the covenant, with the source's published results cited
  as shape (a restated number carries the source's own smoke-grade
  label).
- **Matt Pocock's Grill-me pattern; Superpowers (obra); OpenSpec** — the
  grill/decision-note layer of public spec-isolation and brainstorming
  workflows, adapted as `operational-rigor`'s §1 grill pass and §5
  decisions-note. Ideas only; no code taken. A 2026-07-24 delta pass over
  Superpowers v6.2.0 adopted three more ideas (MIT, ideas only): the
  compression-pressure-probe discipline and the verbatim-move map for
  probe-tuned prose (`skill-authoring` §7), and the change-detector /
  decision-vs-bug clause (`ground-truth-gates` rule 2).
- **Design-pack sources (2026-07-19 survey of 14 design repos)** — text
  adapted under MIT with notices (see `THIRD-PARTY-NOTICES.md`):
  **Emil Kowalski** ([`emilkowalski/skills`](https://github.com/emilkowalski/skills)),
  **Leonxlnx** ([`Leonxlnx/taste-skill`](https://github.com/leonxlnx/taste-skill)),
  **LottieFiles** ([`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill)),
  **Refero Design** ([`referodesign/refero_skill`](https://github.com/referodesign/refero_skill)).
  **nexu-io/open-design** (Apache-2.0): ideas - accent budget,
  linter-promotion architecture - plus two attributed Apache-2.0
  adaptations (the five-state table; the misquote-correction items),
  notice in `THIRD-PARTY-NOTICES.md`. Ideas only, no text:
  **garrytan/gstack** (MIT; measurement pairing, surface classifier,
  fix-loop shape, anti-convergence test, preference-poisoning defense — its
  self-described-unmeasured numeric heuristics deliberately not adopted),
  **benjitaylor/agentation** (PolyForm Shield — source-available, so ideas
  only by necessity as well as policy: pitfall-table form, critic/fixer
  loop), **tt-a1i/archify** (MIT; rule-paired-with-validator),
  **creativetimofficial/ui** (MIT; enumerated micro-text whitelist),
  **VoltAgent/awesome-design-md** (MIT; referenced as research corpus,
  nothing vendored). Surveyed and deliberately not mined:
  greensock/gsap-skills (library-usage doctrine plus embedded promotional
  steering), ui-ux-pro-max (breadth taxonomy), facebook/astryx (agent-infra
  patterns, noted for future eval work). Every embedded agent-directed
  marketing directive in mined sources was stripped per skill-authoring §6.
- **fable-agent-orchestration** @ `935e4a3` (git.wearein.space/elias, Apache-2.0)
- **agent-standard-oss** @ `3786c4c` (github.com/anmoln7, MIT); a
  2026-07-24 delta pass over its post-anchor commits adopted the capability
  triangle (`security-architect`) and co-sourced the quota/effort dispatch
  rule (`delegation-and-review` §1).
- `security-architect` and `product-roadmap` were built from reference drafts
  supplied directly by the pack's owner.
- **2026-07-24 starred-repo mining pass** — a sweep of the owner's starred
  agent-skill repositories; ideas only, no text adopted (each source's license
  noted; a no-license or field-of-use source is ideas-only by necessity as well
  as policy). One surveyed source was judged a **live trojan** (self-propagation
  into the reading agent's global config, an authorization-default flip, and an
  agent-obedience-engineering manual) and **nothing was taken from it** — the
  finding reinforced the "self-described security tools earn stricter scrutiny"
  rule (`operational-rigor` §2). Adopted, on merit, from the rest:
  - [`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail)
    (MIT) — external-ground-truth version anchoring (a mutual-consistency check
    passes while all artifacts are stale together) and deterministic-instrument
    gate framing (`ground-truth-gates`).
  - [`cloudflare/security-audit-skill`](https://github.com/cloudflare/security-audit-skill)
    (MIT) — mechanical-check-separate-from-model-judgment gate framing
    (`ground-truth-gates`) and the guardrail-prompts-are-not-controls /
    denial-of-wallet bar (`security-architect`).
  - [`s0912758806p/agentic-sop-to-work`](https://github.com/s0912758806p/agentic-sop-to-work)
    (MIT) — hermetic LLM-free hard gates with advisory-capped self-eval, and the
    globally-installed-hook silent-no-op opt-in (`ground-truth-gates`); a
    co-source of the labelled-degraded-fallback rule (`operational-rigor`).
  - [`openai/codex-plugin-cc`](https://github.com/openai/codex-plugin-cc)
    (Apache-2.0) — fix-the-contract-before-escalating-compute and
    no-silent-backfill-of-a-failed-delegate (`delegation-and-review`).
  - [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills)
    (MIT) — deterministic trigger-description collision checking
    (`skill-authoring`); co-source of fix-the-contract (`delegation-and-review`).
  - [`mindfold-ai/Trellis`](https://github.com/mindfold-ai/Trellis)
    (AGPL-3.0 — strictly ideas only, no text) — the subagent
    no-commit/push/merge boundary (`delegation-and-review`) and the three-tier
    memory-by-lifespan taxonomy (`skill-authoring`).
  - [`NYCU-Chung/my-claude-devteam`](https://github.com/NYCU-Chung/my-claude-devteam)
    (MIT) — reviewer role-purity via tool-grant denial
    (`delegation-and-review`), corroborating the hook opt-in rule.
  - [`matlab/matlab-agentic-toolkit`](https://github.com/matlab/matlab-agentic-toolkit)
    (MathWorks field-of-use license — ideas only, no text) — the
    self-severing-command one-way-door (`operational-rigor`) and the
    crowded-catalog trigger-degradation ladder (`skill-authoring`).
  - [`gsd-build/get-shit-done`](https://github.com/gsd-build/get-shit-done)
    (MIT; upstream archived — successor `open-gsd/gsd-core`) — the Unicode Tag
    Block gap it surfaced in the hidden-directive sweep, fixed in
    `operational-rigor` §2 and in this repo's own `.github/checks.py`; and the
    experiment-integrity set (arm-environment inventory, cross-arm attrition
    parity, finding placement, configuration binding) adapted into
    `ground-truth-gates`; and the checkpoint-batching cost discipline with
    its never-batch authorization carve-outs, plus the never-write-the-
    human's-reply boundary, adapted into `delegation-and-review`.
  - [`github/spec-kit`](https://github.com/github/spec-kit) (MIT) — the
    task-dependency shape of its tasks template (task ids, phase/story
    dependency ordering, the parallel marker for tasks sharing no
    dependency or files), adapted into `product-roadmap` §7's compact
    task edges.
  - [`vercel-labs/agent-skills`](https://github.com/vercel-labs/agent-skills)
    (MIT declared in its README, no LICENSE file — ideas only) — co-source of the
    mechanical-gate-separate-from-model-judgment framing (`ground-truth-gates`).
  - [`oso95/scroll-world`](https://github.com/oso95/scroll-world),
    [`vinhhien112/Three.js-Object-Sculptor-Codex-Plugin`](https://github.com/vinhhien112/Three.js-Object-Sculptor-Codex-Plugin),
    and [`GiMi-Xiaomi/gimi-illustration-skill`](https://github.com/GiMi-Xiaomi/gimi-illustration-skill)
    (all MIT) — co-sources of the never-silently-degrade / labelled-degraded-fallback
    rule (`operational-rigor`).
  - [`Nutlope/hallmark`](https://github.com/Nutlope/hallmark) (MIT) — its
    URL-fetch checklist surfaced the metadata-endpoint sharpening of the
    `security-architect` SSRF clause. Design-side ideas from all four of these
    land in the design-pack.

All adopted sources were read and checked; no embedded instructions were
executed, and nothing was taken from the sources the 2026-07 audit judged
malicious. Extraction took ideas only. Author + platform accompany every
link so the attribution survives link rot.

</details>
