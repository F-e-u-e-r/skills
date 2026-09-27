# 2026-07-09 — Fable-skills research sweep (20+ items): verdicts + enrichment TODO

Owner supplied a community research list (repos / Reddit threads / blogs / X).
Every load-bearing source was fetched and verified (WebFetch; Reddit via
Playwright headless with comments read, per owner instruction). External
content treated as data throughout. Fable subscription window closes
**2026-07-12 PT** — time-boxed actions marked below.

## Verdicts — behavior-skill packs

| Source | Verified | Verdict |
|---|---|---|
| benjaminard/fable-skills (9 habits, 23★ MIT) | ✅ substantive | 7/9 rules map to operational-rigor §2–§5 / delegation §1 §3 / skill-authoring §4. Residue: 2 communication rules (outcome-first-writing, plain-handoff) → candidate C; evidence-audited-analysis → TODO micro (spirit covered by rigor §1/§4) |
| Iwo Rigor Pack (6 skills, blind-tested 12-0-2) | ✅ | plan-gate/adversarial-verify/live-state-truth/scope-fence → rigor §2/§4/§5 §3. ruthless-editor → candidate C. memory-hygiene "never persist secrets, date entries" → TODO micro. **Main value = the blind-test methodology** → candidate A reference |
| DizzyMii/fable-skills (6 skills, 42★ MIT) | ✅ high quality | All 6 map (prove-it→claim tags; scope-discipline→rigor §3; native-code→slop list; context-thrift→delegation §1; outcome-first/finish-turn→C/§5). **Techniques worth mining: rationalization tables + baseline/post transcripts** → candidates A + TODO micro |
| goatstarter/goat-fable (53★ MIT) | ✅ | Always-loaded 200-line core = rejected architecture (README dropped-item 1 reasoning). **eval/ = 8 behavior-trap tasks + rubric** → candidate A primary reference (MIT) |
| UnpaidAttention/fable5-methodology (51★, **no license**) | ✅ | Heavy-constitution stack (rejected architecture); no license → ideas only, take nothing verbatim. evals/ behavioral regression → candidate A corroboration; AUDIT.md enforcement map ≈ placement test, skip |
| oliwoodman/fable-skills (5 task skills, 24★) | ✅ | security-sweep→security-architect; bug-hunter→rigor §2/§4; honest-advisor→product-roadmap + rigor honesty; project-setup/build-planner→generic. Skip |
| adamentwistle/fable-skills (35 skills, 41★ MIT, honest benchmarks) | ✅ | Bulk maps to the three core skills. Niche seams (numerical-care, concurrency-reasoning, cross-platform-care, error-message-quality) = per-domain depth the pack deliberately doesn't fragment into. TODO: distill a seam file only when the two-strike rule fires on that seam in real sessions |
| mrtooher/fable-mode + forks + 5-Gate (mindstudio) | ✅ (re-checked) | **Verdict unchanged from 2026-07-08 (skip).** Reinforced: author's evals are stage-presence assertions, not outcome quality; top r/claudeskills comment (33pts) criticizes prose-gates-without-enforcement; harness-native alternative noted (workflows/ultracode). mindstudio 5-Gate is an independent proprietary framing ≈ rigor §1/§2/§5. HalalifyMusic fork bundles a leaked system prompt — not adopted on principle |
| sgup/ai Fable5.md (thread 409 pts) | ✅ | Rules covered; always-loaded architecture rejected (skill-authoring §4). **Method is the value**: diff Fable-vs-Opus sessions from the same commits → TODO 3 (not time-boxed — transcripts persist locally). Top comment (41pts): "You don't [make it follow .md]. Make hooks instead" — community converging on this pack's core doctrine |
| baskduf/FableCodex | (2026-07-08) | Skip — covered + AGPL, never take code |
| Superpowers plugin | (2026-07-07) | Already evaluated: plugin install over vendoring; distill per-lesson only if proven |

## Verdicts — generators, prompts, meta

| Source | Verified | Verdict |
|---|---|---|
| Rodbourn retiring-architect gist (+ r/ClaudeAI 1ukynrw, 2563 pts / 160 comments) | ✅ | Its 3-reviewer process ≈ skill-authoring §6 three lenses (same community lineage). **Real gap it exposes: the pack lacks a project-skill taxonomy checklist** → candidate B. Generator itself not vendored — skill-authoring *is* our generator spec. Comment warnings: one full run burned **>30% of a weekly 20x-max Fable quota** |
| "Finding your unknowns" 8 skills (r/ClaudeCode 1up1bgd, 3 pts, 0 comments) | ✅ | Low signal; concepts map (blindspot→rigor §5 attack/omitted-case; interview-me→delegation §6). TODO micro: read Thariq Shihipar's source essay (Anthropic) directly |
| apoorvjain25/frontier (21 craft files, 71★ MIT) | ✅ substantive | 21-domain standards library — outside the pack's engineering focus and against its density principle. Optional per-domain borrow later |
| Model routing / effort skill (item 31) | — | delegation §1 already routes by task with volatile-lineup rule. Skip |
| Self-improving orchestrator STATE.md (item 32) | — | files-are-state (delegation §5) + fix log / two-strike (skill-authoring §4). Skip |
| Security/agent-debugging skills (item 33) | — | security-architect domain. Skip |
| Daniel Miessler 10 prompts (item 35) | ❌ blocked domain | One-shot meta-prompts, not skills; MIT adaptation exists (kazani-351/system-upgrade) |
| X items (Nate Herk, milesdeutscher, @aae_on_x), getmasset blog, substack departing-architect, r/ClaudeAI 1u4iktp, r/ClaudeCode 1u5zpn7 | ❌ skipped deliberately | Demo/derivative/duplicate coverage of items above; X is login-walled. No verdict impact expected; revisit only if a specific claim needs them |

## New leads from comments (owner-directed comment sweep)

- **attunehq/nudge** (Apache-2.0, 77★, Rust): hook-surface rules engine — PreToolUse/UserPromptSubmit matching → interrupt/substitute/inject; "learned notes" (problem→fix→verification) retrieved at the moment of action. Mechanized compile-don't-retrieve. TODO 6.
- **Matt Pocock / Kun Chen / Nate Jones skill packs** — repeatedly recommended in the 2563-pt thread (55/31/30-pt comments). Unverified. TODO 5.
- Community convergence note: two independent top comments land on "enforcement needs hooks/CI, not prose" — external validation of the pack's gates-over-prose architecture; no change needed.

## Candidates for owner approval

- **A. Behavioral eval harness for the pack itself** (highest value; four independent sources converged: Iwo blind-test, goat-fable eval/, fable5-methodology evals/, DizzyMii transcripts). Small `evals/` of trap tasks — planted bug, contradictory spec, tempting unrelated fix, fake-passing test — plus a blind grading rubric, so skill edits get A/B checked instead of trusted. This is delegation §5 verifier-decay + "gates over prose" applied to the pack. Not Fable-dependent (Opus can grade; optionally have Fable draft traps before 7/12).
- **B. skill-authoring §5 addition (~8 lines): project-skill taxonomy** — the knowledge categories worth a file when building a repo's skill library (debugging-playbook, failure-archaeology, architecture-contract, config-and-flags, build-and-env, run-and-operate, diagnostics-and-tooling, validation-and-qa), gated by "only categories with real incidents/history behind them earn a file."
- **C (low priority). Two communication lines** (outcome-first summary; plain-handoff without invented shorthand) into delegation §5 handoff pack. Multiple sources converge, but Claude Code's harness already instructs this natively — the case for adding is portability (Codex CLI / Gemini CLI / API harnesses).

## Enrichment TODO backlog

1–3. **[owner-side]** Fable-window and transcript-distillation actions — packaged into an owner-internal playbook; not distributed with the repo.
4. **[not time-boxed]** Build candidate A (evals/ trap tasks + rubric).
5. Verify the Matt Pocock / Kun Chen / Nate Jones skill packs.
6. Evaluate attunehq/nudge vs the pack's zero-dependency hooks.
7. Micro-items: "never persist secrets in memory/notes" line (skill-authoring §4 or security-architect); rationalization-table technique as a §1 example form; read Thariq's unknowns essay; data-analysis discipline (only if owner's real work hits it); adamentwistle seam files on two-strike trigger.

## 2026-07-09 (later) — implementation round (owner approved A+B+C + backlog)

**Landed in the pack:**
- **A DONE** — `evals/` shipped: 6 trap tasks (planted-adjacent-bug, contradictory-spec, fake-passing-test, false-stop-pressure, injection-in-content, headline-number), each mapped to a specific pack rule; `run.sh` sandbox materializer; blind grader prompt; README×2 section. Fixtures/extraction/gates **verified by execution 2026-07-09** (leak check clean; 04's check.sh FAILs pre-rename, PASSes post; 06 sums as designed). Open: `claude -p` flags + skills-aside isolation unverified until first real run; **baseline A/B round not yet run**.
- **B DONE** — skill-authoring §5: project-skill taxonomy bullet + "real incidents behind it" gate.
- **C DONE** — delegation-and-review §5: final-summary communication line (outcome first, expand shorthand, shorten by dropping items).
- **⑦a DONE** — skill-authoring §4: no secrets in memory/notes/fix-log files.
- **⑦b DONE** — skill-authoring §1: strongest negative example quotes an observed rationalization.
- **⑦c DONE (no edit)** — Thariq's essay (official claude.com blog) read: references-as-specs / implementation-notes / interview / quiz patterns judged covered by delegation §2/§6 + rigor §1; evidence-audited-analysis became **eval task 06** instead of a rule (gates over prose).

**Research verdicts (backlog items 5, 6, 2):**
- **mattpocock/skills** (161k★, MIT, 34 skills): single-purpose *user-invoked workflow primitives* (grill-me, tdd, to-spec, handoff…) — a different genre from this pack's auto-trigger discipline; the discipline-shaped ones (code-review, diagnosing-bugs, handoff) are already covered. Compatible to install selectively alongside the pack; nothing to vendor.
- **Kun Chen**: `no-mistakes` (kunchenguid/no-mistakes) = mechanized gate pipeline (binary + /skill: run pipeline → safe autofixes → escalate rest) — same layer as hooks/CI; doctrine already in ground-truth-gates; optional per-project trial. OPINIONS.md pattern ≈ memory-architecture doctrine (covered). **Nate Jones**: commentary/educational content; no packaged skill artifact located to evaluate.
- **attunehq/nudge** (Apache-2.0, Rust, 77★): hook-surface rules engine (PreToolUse/UserPromptSubmit match → interrupt/substitute/inject; learned notes delivered at action time). Complementary, adds a binary dep. Verdict: **watch** — trial only when a rule is repeatedly read-but-violated and needs mechanization beyond the pack's zero-dep bash/python hooks (skill-authoring §7 layering rule).
- **Miessler prompts**: direct fetch domain-blocked; content confirmed via search + MIT adaptation **kazani-351/system-upgrade** (17 prompts, 6 categories). Overlap warning stands: harness-audit prompts may try to rebuild architectures this pack deliberately dropped.

**Backlog statuses**: 1–3 → packaged owner-side (internal playbook, not distributed); 4 → harness DONE, first A/B round open; 5/6/7 → DONE per verdicts above.
