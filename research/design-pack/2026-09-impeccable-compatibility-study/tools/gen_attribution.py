#!/usr/bin/env python3
"""Attribution fixture (test T16): one deterministic third-party notice for the 16 Design Pack-derived
MOTION rules, preserving each origin's MIT copyright line and the full MIT permission notice. In the
fan-out experiment this file travelled next to the shards so that attribution could not be orphaned.

Inputs: the corpus and ../fixtures/motion-rules-only-candidate.json (candidate_ids).
Writes <workspace>/artifacts/motion-dp-THIRD-PARTY.md (expected byte-identical to the fixture)."""
import hashlib, json, os, collections
from _common import parser, load_corpus, ensure_dir

args = parser(__doc__).parse_args()
ART = ensure_dir(os.path.join(args.workspace, "artifacts"))
corpus = load_corpus(args.corpus)
ids = json.load(open(os.path.join(args.fixtures, "motion-rules-only-candidate.json")))["candidate_ids"]

MIT_PERMISSION = ("Permission is hereby granted, free of charge, to any person obtaining a copy "
"of this software and associated documentation files (the \"Software\"), to deal "
"in the Software without restriction, including without limitation the rights "
"to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
"copies of the Software, and to permit persons to whom the Software is "
"furnished to do so, subject to the following conditions:\n\n"
"The above copyright notice and this permission notice shall be included in all "
"copies or substantial portions of the Software.\n\n"
"THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR "
"IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
"FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE "
"AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
"LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, "
"OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE "
"SOFTWARE.")
ORIGINS = {
 "nextlevelbuilder/ui-ux-pro-max-skill": {"copyright": "Copyright (c) 2024 Next Level Builder",
    "url": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill", "pin": "dcc40ff5133ef78276117db0cc34e7b83cc8aeba"},
 "Nutlope/hallmark": {"copyright": "Copyright (c) 2026 Hallmark contributors",
    "url": "https://github.com/Nutlope/hallmark", "pin": "13ac0ec7e148655948100b6396439e481361d690"},
 "Leonxlnx/taste-skill": {"copyright": "Copyright (c) 2026 Leonxlnx",
    "url": "https://github.com/Leonxlnx/taste-skill", "pin": "c184364c58658b2f131b4ae8bd3d206cabb3deee"},
}
by_origin = collections.defaultdict(list)
for i in ids: by_origin[corpus[i]["provenance"]["upstream_repo"]].append(i)

parts = ["# Third-Party Notices - Design Pack MOTION rules",
"",
"The `motion-dp-*.md` reference files in this skill are **derived runtime-governance metadata**",
"projected from the design skills below (the upstream source works are **not** redistributed).",
"Each upstream is MIT-licensed; its copyright and the full MIT permission notice are preserved below,",
"as required by the MIT license, and ship with these reference files in every distribution.",
""]
for repo in sorted(by_origin):
    o = ORIGINS[repo]; ids_here = sorted(by_origin[repo])
    parts += [f"## {repo}", f"- Source: {o['url']}", f"- Pinned commit: `{o['pin']}`",
              f"- Derived Design Pack rule IDs: {', '.join(ids_here)}", "",
              "```", o["copyright"], "", MIT_PERMISSION, "```", ""]
art = "\n".join(parts)
p = os.path.join(ART, "motion-dp-THIRD-PARTY.md")
open(p, "w").write(art)
sha = hashlib.sha256(art.encode()).hexdigest()
# em-dash check (must be build-safe)
print("em dashes in attribution (must be 0):", art.count("—"))
print("origins covered:", len(by_origin), "| ids covered:", sum(len(v) for v in by_origin.values()))
print("motion-dp-THIRD-PARTY.md sha256=", sha[:16], "bytes=", len(art.encode()))
