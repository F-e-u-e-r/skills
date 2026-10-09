# Pre-commit gate — ship-gate split doctrine PR (2026-10-09)

You are the **pre-commit** reviewer for load-bearing edits in F-e-u-e-r/skills (ops-pack /
planning-pack). Read the files in --cwd. Do not edit files or use the network.

## Scope

- Adds evidence record: `evidence/reviews/2026-10-09-external-harness-ship-gate-split.md`
- `plan-reconciliation`: §2b layered packets when full-plan formal review diverges (`unprobed`)

**Out of scope:** routing promotion, machine-specific Splash install, new skills, weakening
cross-model-review §6 dual-family requirement for ship gate (a).

## Rubric

1. Pack style: verdict-first, `unprobed` where evidence is external-only.
2. Additive doctrine; no contradiction with INV-1 or cross-model-review §5b.
3. Evidence record states canonical skills win.
4. §2b does not authorize execution without grant (INV-1 called).

Author ran `python3 .github/checks.py` → all checks passed (2026-10-09).

LAST LINE exactly `PROCEED` or `FIX F1, F2`. Nothing after.

---

## git diff

```diff
diff --git a/planning-pack/skills/plan-reconciliation/SKILL.md b/planning-pack/skills/plan-reconciliation/SKILL.md
index d6520a2..0af9e1d 100644
--- a/planning-pack/skills/plan-reconciliation/SKILL.md
+++ b/planning-pack/skills/plan-reconciliation/SKILL.md
@@ -50,6 +50,30 @@ Trigger: OR has stopped (it owns detection and the stop — OR §2; you do not p
 
 Supporting seam rules (A9-03, A9-06) are supporting, not core — apply them, do not elevate them to gates.
 
+## §2b — Layered review packets when full-plan review diverges (`unprobed`)
+
+When execution depends on a **harness** (deterministic selftest, freeze manifest, staged
+code packet) but the **full plan document** is also sent through a **dual-family formal**
+review loop, those loops can disagree: bounded **fix-check** briefs may reach dual
+`PROCEED` while the **full packet** never does (open-ended adversarial scope on the
+document, not a host failure).
+
+**Steps (operator choice — record it):**
+
+1. **Name two packets** — (a) *ship gate*: host selftest + manifest + staged harness tree
+   with dual-family precommit; (b) *formal plan*: full methodology doc, may stay
+   **advisory** if you document residual risk and disposition of open FIX items.
+2. **Do not** treat formal FIX on (b) as blocking (a) when (a) was pre-authorized under
+   a recorded amendment and (b)'s open items are **dispositioned** (reject / defer /
+   scope-freeze), not silently ignored.
+3. **INV-1 still binds** — revising or extending scope under (a) needs its own grant;
+   advisory (b) does not authorize new execution.
+4. **cross-model-review** still applies to (a): same-model bench self-review is a weak
+   lens (§5b); deterministic selftest validates harness state, not reviewer judgment.
+
+(`unprobed` — external harness incident shape, 2026-10-09;
+`evidence/reviews/2026-10-09-external-harness-ship-gate-split.md`.)
+
 ## §3 — Close (all work items done)
 
 Run before OR's completion claim; OR still owns the honesty of that claim (OR §5).
```
