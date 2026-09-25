#!/usr/bin/env python3
"""CI enforcement of the design-pack production bridge contract (D6-B2.2-CLOSE).

Runs the production-contract gates (design-pack/tools/projection_checks.py) against
the real tree. Guarded on presence: if the generated bridge is not in this tree
(pre-integration main), it enforces nothing. Once the production-integration PR
commits design-pack/generated/, this gate is always live.

Reuses the existing checks.py convention: run(root) -> list of failure strings.
"""
import os
import sys


def run(root):
    if not os.path.exists(os.path.join(root, "design-pack/generated/manifest.json")):
        return []  # bridge not present in this tree; nothing to enforce yet
    tools = os.path.join(root, "design-pack/tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    import projection_checks as g  # noqa: E402
    runtime, support, manifest, reach, corpus = g.load_all(root)
    failures = []

    def add(label, res):
        for r in res:
            failures.append(f"{label}: {r}")

    # required CI failure conditions (owner D6-B2.2-CLOSE §6) -> gates
    add("canonical-source", g.check_canonical_source(root))                 # stale corpus SHA
    add("coverage", g.check_coverage(runtime, support, corpus))
    add("physical-isolation", g.check_physical_isolation(runtime, support)) # runtime/support drift
    add("skill-reachability", g.check_skill_reachability(runtime, reach))   # missing reachability
    add("runtime-reference-closure", g.check_runtime_reference_closure(runtime))  # dangling refs
    add("per-skill-control-closure", g.check_per_skill_control_closure(runtime, reach))
    add("semantic-preservation", g.check_semantic_preservation(runtime, support, corpus))
    add("generated-reference-fidelity", g.check_generated_reference_fidelity(root, runtime))  # fidelity mismatch
    add("decision-tables", g.check_decision_tables(runtime, corpus))
    add("isolation", g.check_isolation(runtime, support, manifest, reach))
    add("no-cross-skill-reference", g.check_no_cross_skill_reference(root))  # cross-skill traversal
    add("reference-path-existence", g.check_reference_path_existence(root))  # missing skill-local ref
    add("per-skill-supporting-reachability", g.check_per_skill_supporting_file_reachability(root, runtime, reach))
    add("selective-load-policy", g.check_selective_load_policy(root))
    add("normative-classification-complete", g.check_normative_classification_complete(root))  # classification incompleteness
    add("normative-bijection", g.check_normative_bijection(root))            # accounting/bijection
    add("per-extension-conflict-review", g.check_per_extension_conflict_review(root))
    add("pack-local-extension-non-conflict", g.check_pack_local_extension_non_conflict(root))
    add("provenance-separation", g.check_provenance_separation(root, runtime))  # provenance-boundary
    add("distribution-attribution", g.check_distribution_attribution(root))  # attribution SHA
    add("clean-regeneration", g.check_clean_regeneration(root))              # stale generated artifacts / no-diff
    return failures


if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    res = run(ROOT)
    for r in res:
        print("FAIL " + r)
    print(f"{len(res)} design-pack contract failure(s)" if res else "design-pack production bridge contract: all checks passed")
    sys.exit(1 if res else 0)
