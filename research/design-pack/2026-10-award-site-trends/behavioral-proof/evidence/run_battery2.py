#!/usr/bin/env python3
"""Amended re-runs (AMENDMENT-1): amended Case 1 (context-discrimination) +
amended Case 6 (CURRENT vs PROPOSED differential). Outputs under runs2/."""
import json, os, re, subprocess, time

BP = "/private/tmp/claude-501/-Users-ccso-Developer-fable/33a7ad6c-e91a-419f-b004-85989a00f5e8/scratchpad/bp"
RUNS = os.path.join(BP, "runs2"); os.makedirs(RUNS, exist_ok=True)
MODEL = "claude-haiku-4-5-20251001"
def dfile(n): return open(os.path.join(BP, n), encoding="utf-8").read()
PRE = ("You must follow this design doctrine when answering, and do not invent "
       "rules beyond it.\n\n===DESIGN DOCTRINE START===\n{doc}\n===DESIGN DOCTRINE END===\n\n{task}")

DEVICES = ("a full-viewport animated WebGL hero; the sections are laid out as a "
           "horizontal/spatial room-to-room scroll; kinetic/variable display type at large "
           "scale; a reactive cursor; every transition animates over ~700ms cinematic easing; "
           "frosted-glass blur panels float over the hero")
def c1_task(page):
    return (f"Here is a proposed visual design for {page}: {DEVICES}. Review it. List concrete "
            f"problems, one per line (write 'none' if there are none). Then end with exactly one "
            f"line: `CONTEXT-FIT: OK` or `CONTEXT-FIT: NOT-OK` - whether this visual approach "
            f"suits {page}.")
PAGE_ORD = "an internal B2B SaaS settings page (team billing + notification preferences)"
PAGE_EXP = ("an experimental art-exhibition campaign microsite whose explicit goal is an "
            "immersive scroll experience")
C6_TASK = ("For an experimental, Awwwards-style art-exhibition campaign microsite, the client "
           "wants heavy scroll-driven motion. Using the doctrine, list the non-negotiable "
           "constraints that still apply. End with exactly one line: "
           "`REDUCED-MOTION-REQUIRED: YES` or `REDUCED-MOTION-REQUIRED: NO`.")

# (case, arm, reps, doctrine-files, task)
CELLS = [
 ("C1a","PROPOSED",3,["PROPOSED_antislop.md"], c1_task(PAGE_ORD)),
 ("C1a","CURRENT", 2,["CURRENT_antislop.md"],  c1_task(PAGE_ORD)),
 ("C1b","PROPOSED",3,["PROPOSED_antislop.md"], c1_task(PAGE_EXP)),
 ("C1b","CURRENT", 2,["CURRENT_antislop.md"],  c1_task(PAGE_EXP)),
 ("C6","CURRENT", 3,["CURRENT_antislop.md","CURRENT_motion.md"], C6_TASK),
 ("C6","PROPOSED",3,["PROPOSED_antislop.md","PROPOSED_motion.md"], C6_TASK),
]
VERD = {"C1a": r"CONTEXT-FIT:\s*(OK|NOT-OK)", "C1b": r"CONTEXT-FIT:\s*(OK|NOT-OK)",
        "C6": r"REDUCED-MOTION-REQUIRED:\s*(YES|NO)"}

index=[]
for case, arm, reps, docs, task in CELLS:
    doc="\n\n".join(dfile(d) for d in docs)
    prompt=PRE.format(doc=doc, task=task)
    for rep in range(1,reps+1):
        key=f"{case}_{arm}_r{rep}"; t0=time.time()
        try:
            p=subprocess.run(["claude","-p",prompt,"--model",MODEL,"--output-format","json"],
                             capture_output=True,text=True,timeout=240)
            d=json.loads(p.stdout); result=d.get("result") or ""; is_err=bool(d.get("is_error"))
            mu=list((d.get("modelUsage") or {}).keys())
        except Exception as e:
            result="";is_err=True;mu=[];p=None
        dt=round(time.time()-t0,1); m=re.search(VERD[case],result)
        verdict=m.group(1).strip() if m else None
        completed=bool(result) and not is_err and verdict is not None
        open(os.path.join(RUNS,key+".txt"),"w",encoding="utf-8").write(result or "EMPTY")
        row={"key":key,"case":case,"arm":arm,"rep":rep,"secs":dt,"model_receipt":mu,
             "is_error":is_err,"verdict":verdict,"completed":completed,"chars":len(result or "")}
        index.append(row)
        print(key,"->","OK" if completed else "NOT-COMPLETED","| verdict=",verdict,"| mu=",mu,flush=True)
open(os.path.join(RUNS,"index.jsonl"),"w").write("\n".join(json.dumps(r) for r in index))
print(f"\nAMENDED BATTERY DONE: {sum(1 for r in index if r['completed'])}/{len(index)} completed")
