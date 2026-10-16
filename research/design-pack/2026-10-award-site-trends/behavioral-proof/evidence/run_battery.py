#!/usr/bin/env python3
"""Run the pre-registered behavioral battery on claude-haiku-4-5-20251001.
Each cell -> its own run-keyed output file; never overwrite. No grading here."""
import json, os, re, subprocess, sys, time

BP = "/private/tmp/claude-501/-Users-ccso-Developer-fable/33a7ad6c-e91a-419f-b004-85989a00f5e8/scratchpad/bp"
RUNS = os.path.join(BP, "runs"); os.makedirs(RUNS, exist_ok=True)
MODEL = "claude-haiku-4-5-20251001"

def dfile(name): return open(os.path.join(BP, name), encoding="utf-8").read()

PREAMBLE = ("You must follow this design doctrine when answering, and do not invent "
            "rules beyond it.\n\n===DESIGN DOCTRINE START===\n{doc}\n===DESIGN DOCTRINE END===\n\n{task}")

TASKS = {
 "C1": ("Here is a proposed visual design for an internal B2B SaaS settings page "
        "(team billing + notification preferences): a full-viewport animated WebGL hero "
        "behind the form; the setting groups are laid out as a horizontal/spatial "
        "room-to-room scroll; a forced dark-only theme; every toggle and tab animates "
        "over ~700ms ease-in-out; frosted-glass blur panels float over the hero. "
        "Review it. List concrete problems, one per line (write 'none' if there are none). "
        "Then end with exactly one line: `CONTEXT-FIT: OK` or `CONTEXT-FIT: NOT-OK` - "
        "whether this visual approach suits an internal B2B SaaS settings page."),
 "C2": ("Critique this design: a restrained, conventional SaaS analytics dashboard - "
        "system font, at most two accents, flat cards, 180ms transitions, both light and "
        "dark supported. Does the doctrine require adding any immersive or experimental "
        "devices here? List any you would ADD (write 'none' if none). End with exactly one "
        "line: `ADDS-SPECTACLE: YES` or `ADDS-SPECTACLE: NO`."),
 "C3": ("Propose a color palette for a developer-tools product landing page. Give specific "
        "guidance: the field/base, the accent(s), and how visual hierarchy is carried. "
        "End with exactly one line: `ACCENT-COUNT: <n>` giving the number of distinct accent "
        "colors you recommend."),
 "C4": ("Propose typography for an editorial design-studio portfolio site. Give specific "
        "guidance: the display/heading role, the body/interface role, and how contrast is "
        "achieved. End with exactly one line: `NAMED-FONTS: <comma-separated list, or none>` "
        "listing any specific font families you named."),
 "C5": ("A client commissions an experimental, Awwwards-style campaign microsite for an art "
        "exhibition; the explicit goal is an immersive scroll experience. Using the doctrine, "
        "what design approach fits? Name concrete devices. End with exactly one line: "
        "`SPECTACLE-ALLOWED: YES` or `SPECTACLE-ALLOWED: NO`."),
 "C6": ("For that experimental campaign microsite, the client wants heavy scroll-driven "
        "motion. Using the doctrine, list the non-negotiable constraints that still apply. "
        "End with exactly one line: `REDUCED-MOTION-REQUIRED: YES` or `REDUCED-MOTION-REQUIRED: NO`."),
}
VERDICT = {
 "C1": r"CONTEXT-FIT:\s*(OK|NOT-OK)", "C2": r"ADDS-SPECTACLE:\s*(YES|NO)",
 "C3": r"ACCENT-COUNT:\s*(\d+)", "C4": r"NAMED-FONTS:\s*(.+)",
 "C5": r"SPECTACLE-ALLOWED:\s*(YES|NO)", "C6": r"REDUCED-MOTION-REQUIRED:\s*(YES|NO)",
}
# (case, arm, reps, [doctrine files])
CELLS = [
 ("C1","CURRENT",2,["CURRENT_antislop.md"]),
 ("C1","PROPOSED",3,["PROPOSED_antislop.md"]),
 ("C1","BAD",3,["BAD_doctrine.md"]),
 ("C2","PROPOSED",2,["PROPOSED_antislop.md"]),
 ("C3","CURRENT",1,["CURRENT_color.md"]),
 ("C3","PROPOSED",2,["PROPOSED_color.md"]),
 ("C4","CURRENT",1,["CURRENT_typo.md"]),
 ("C4","PROPOSED",2,["PROPOSED_typo.md"]),
 ("C5","CURRENT",1,["CURRENT_antislop.md"]),
 ("C5","PROPOSED",2,["PROPOSED_antislop.md"]),
 ("C6","PROPOSED",2,["PROPOSED_antislop.md","PROPOSED_motion.md"]),
]

index = []
for case, arm, reps, docs in CELLS:
    doc = "\n\n".join(dfile(d) for d in docs)
    prompt = PREAMBLE.format(doc=doc, task=TASKS[case])
    for rep in range(1, reps+1):
        key = f"{case}_{arm}_r{rep}"
        t0 = time.time()
        try:
            p = subprocess.run(["claude","-p",prompt,"--model",MODEL,"--output-format","json"],
                               capture_output=True, text=True, timeout=240)
            raw = p.stdout
            d = json.loads(raw)
            result = d.get("result") or ""
            is_err = bool(d.get("is_error"))
            mu = list((d.get("modelUsage") or {}).keys())
        except Exception as e:
            result = ""; is_err = True; mu = []; raw = f"EXC:{e}"
        dt = round(time.time()-t0,1)
        m = re.search(VERDICT[case], result)
        verdict = m.group(1).strip() if m else None
        completed = bool(result) and not is_err and verdict is not None
        open(os.path.join(RUNS, key+".txt"), "w", encoding="utf-8").write(result or raw)
        row = {"key":key,"case":case,"arm":arm,"rep":rep,"secs":dt,"model_receipt":mu,
               "is_error":is_err,"verdict":verdict,"completed":completed,"chars":len(result or "")}
        index.append(row)
        print(key, "->", "OK" if completed else "NOT-COMPLETED", "| verdict=", verdict, "| mu=", mu, "| err=", is_err, flush=True)

open(os.path.join(RUNS, "index.jsonl"), "w").write("\n".join(json.dumps(r) for r in index))
done = sum(1 for r in index if r["completed"])
print(f"\nBATTERY DONE: {done}/{len(index)} cells completed")
