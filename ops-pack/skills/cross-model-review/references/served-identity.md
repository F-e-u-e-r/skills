# cross-model-review · references: served identity (provider provenance + maturity)

Lower-level reference for `SKILL.md` §1 (family-diversity) and §5 (identity evidence). The skill text
owns the **provider-neutral contract**; this file holds the concrete, VOLATILE provider mechanics and
the current maturity record. Everything about which CLI, which flag, and which provider is attested is
session-time-re-verifiable — re-discover it, never trust a flag or a maturity row recalled from here
(same covenant as `SKILL.md` §1 and the Provenance re-verify line).

## Requested vs served identity

```
requested_model = routing intent — what you asked for (-m / client config / dispatcher label)
served_model    = what TRUSTED provider/runtime evidence proves actually served the request
no trusted provider/runtime evidence  ->  served_model = unknown
```

`requested_model != served_model` unless trusted evidence establishes the relation. **`unknown` is
honest, not a failure.** It does NOT mean the reviewer is disabled and does NOT block ordinary review
execution — you may still route on the requested model and use the reviewer; it simply earns no
provider-attested identity credit. A gate that specifically requires attested served identity treats
`unknown` as unconfirmed (fails closed), and must never silently convert a requested family into an
attested family.

## Identity provenance — trust order (highest → lowest)

Trusted (may populate a trusted `served_model` and earn attested-family credit):
- **provider structured metadata** in the reviewer's structured-output stdout, carrying real
  provenance — keyed by the served model AND corroborated by an unforgeable anchor (cost/usage
  accounting or a server request-id the client cannot fabricate) — the served-model key alone, or
  the anchor alone, is not enough (e.g. a `modelUsage` block with `costUSD`/token counts);
- an equivalent **server-confirmed** identity header/field.

Untrusted (recorded for the audit trail; NEVER earns attested credit):
- the **requested** model / dispatcher label (routing intent, not a receipt);
- a **client banner** — a startup echo of the requested slug (e.g. a CLI's `model:` line);
- a **model self-report** — the model naming itself inside the review text (a family label at best);
- **catalog membership** — "the model exists in the provider's list" is not evidence it served THIS call;
- **plain / model-controlled JSON-looking output** — JSON serialization alone does not make a field
  trustworthy; a model can print `{"modelUsage":{…}}` in a plain response. Provider metadata is
  trusted for its PROVENANCE, not its shape (see structured mode below).

## Structured provider mode (execution provenance)

Provider-attested served identity may be derived ONLY through a parent/adapter-owned channel the
reviewed model cannot forge. The primary channel is the provider's STRUCTURED-OUTPUT mode: the
provider CLI owns the top-level output structure and the reviewed model controls only its nested text,
so the model cannot fabricate the envelope. An equivalent server-confirmed transport surface (e.g. an
unforgeable response header) is the other acceptable channel. **Channel provenance and served-model
evidence are SEPARATE requirements** — being in the channel does not by itself prove any served model;
the provider metadata carried in it must still establish that. The channel fact must come from the parent-owned invocation (the adapter that
built the command), never from the model's own output or from untrusted content spliced into the
command.

Current provider mechanics (VOLATILE — verify at session time; do not hard-code):

```
grok CLI   : structured mode = `--output-format json`  -> emits `modelUsage` keyed by the served
             model with cost/usage accounting = provider-attested served identity.
codex CLI  : structured mode = `exec --json`           -> JSONL events; as of 0.166.0 carries NO
             server-origin served-model field on any readable surface -> served_model = unknown.
```

## Per-provider maturity (as of 2026-11-02; re-verify on any CLI/model move)

| provider | execution | requested identity | served identity | attestation |
|---|---|---|---|---|
| **Grok** (`grok`, `--output-format json`) | mature | known | **provider-confirmed** (`modelUsage` keyed by served slug + cost/usage) | **mature** |
| **Codex** (`codex`, `exec --json`, 0.166.0) | mature | known | **unknown** (no server-origin field on any readable CLI surface) | **unavailable from current CLI surface** |

Codex note: the served value exists server-side (Codex core reads the `openai-model` response header)
but is not persisted to any tool-readable surface (`exec --json`, rollouts, hooks). This is an
upstream *observability* limitation, not a review incapability — Codex is fully usable as a reviewer;
it simply earns no attested served identity.

## Tracking

- **Issue #295** (this repo) — Codex served-model attestation gap; upgrade trigger: if a future Codex
  version persists a server-origin served model, add the minimal attested-identity adapter branch +
  deterministic regressions (keyed-by-served / server-origin provenance required, not a bare field),
  then one bounded live confirmation — mirroring the grok path. Upstream dependency: **openai/codex#47779**
  (served-model persistence; also #47354). Do NOT file a duplicate upstream issue.
- **Issue #296** (this repo) — reviewer reliability: explicit stdin ownership + hard reviewer deadline
  (the invariant lives in delegation-and-review §4; the issue holds the incident/history).

## Upgrade rule (never weaken the standard to make a gate green)

Future providers follow the same model: use trusted served evidence if present; otherwise route on
the requested model, record `served_model = unknown`, and upgrade the adapter + skills when upstream
support appears. Never weaken the evidence standard to manufacture a green gate, and never add a
reviewer family merely to make a gate pass.
