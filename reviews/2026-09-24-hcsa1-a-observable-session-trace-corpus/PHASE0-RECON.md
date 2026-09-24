# HCSA1-A Phase 0 — Session-Log Observability Reconnaissance

**Status:** READ-ONLY reconnaissance complete (2026-09-24). Honored: no parser
implementation, no corpus build, no semantic judgments, no Jev, no frontier judge,
no auto-stop/handoff, no transcript mutation, no commit/PR. Method: disposable
read-only Python enumeration over sampled transcripts, aggregates only — no CoT text,
message text, or tool payloads were read into analysis (only types, keys, counts,
low-cardinality value sets, tool names, and content-hash equality).

Purpose: establish the real observable evidence surface before freezing the corpus
schema or qualification protocol.

**Phase 0.1 addendum (compaction, read-only):** compaction has a reliable native marker
where its capability is qualified — `system.subtype=compact_boundary` immediately followed
by `user.isCompactSummary=true` (34 occurrences across 6 sessions in other local projects;
none in this project). Where qualified, the adapter emits `observability=KNOWN` +
`context_boundary=COMPACTION`; a stream/version whose marker capability is not qualified is
`observability=UNKNOWN` (never `NONE`) and is excluded from continuity-requiring
qualification (see DESIGN §3). Private-project content was never read or named — only
marker type and location were detected.

---

## Return packet

### 1. Transcript locations + formats

- **Primary — interactive sessions:** `~/.claude/projects/<encoded-cwd>/*.jsonl`, one
  JSONL file per session, one JSON record per line. This project
  (`<encoded-cwd>`): 31 files, ~62 MB, 2026-08-28 to 2026-09-24.
- **Controlled / eval sessions:** `~/.claude/projects/-private-tmp-av2-sb-*` (96 dirs =
  AE1 activation fixtures), `-private-tmp-loc-sb-*`, `-private-tmp-r5-actprim-*`. Same
  record schema; `entrypoint=sdk-cli`.
- **Subagent transcripts:** `<session-tmp>/tasks/*.output`. Same record schema;
  `entrypoint=sdk-cli`.
- **Other stores (not transcript schema; noted for cross-reference):**
  `~/.claude/history.jsonl`, `~/.claude/sessions/`, `~/.claude/state/`,
  `~/.claude/file-history/`, `~/.claude/shell-snapshots/`, `~/.claude/tasks/`.
- Format is normalizable across the three transcript classes behind **one HCSA adapter
  interface** — this is NOT a claim that one adapter implementation covers all present or
  future native schemas (see §5, §6). They differ only in `entrypoint` and which
  event-driven records appear.

### 2. Sampled session classes / versions

- **Classes:** interactive CLI working sessions (`entrypoint=cli`); SDK/eval-sandbox
  sessions (`sdk-cli`); subagent `.output` (`sdk-cli`); near-empty stub sessions
  (7 lines: mode / file-history-snapshot / user / system / queue-operation, no
  assistant — opened-then-abandoned or post-`/clear`).
- **CLI versions (drift is real):** main project = 2.1.221 (27 files), 2.1.272 (3),
  2.1.280 (1); across all project dirs = 2.1.221, 2.1.263, 2.1.269, 2.1.272 (184),
  2.1.281 (12). Span 2.1.221 -> 2.1.281.
- **Models in-transcript:** `claude-opus-4-8`, `claude-fable-5`; model can change
  WITHIN a session (`message.model`), with fallback recorded in `system`
  (`originalModel` / `fallbackModel` / `direction` / `trigger`).

### 3. Observable-field matrix (tag = RAW / DERIVABLE / NOT AVAILABLE / UNSTABLE)

**1 — Session identity**
- `sessionId` (per record) — **RAW**
- `uuid` / `parentUuid` (message DAG; within-session branching) — **RAW**
- `timestamp` (per record, most) — **RAW**
- model identity (`message.model`; intra-session switch; system fallback fields) — **RAW**
- CLI `version` — **RAW**, but **UNSTABLE** across the corpus (drifts)
- parent SESSION / fork-of-session id — **NOT AVAILABLE** in the primary transcript streams inspected (other local stores not reconciled)

**2 — User / assistant turns**
- turn boundaries (user/assistant records + uuid/parentUuid) — **RAW**
- message text (`message.content` text items) — **RAW**
- reasoning summaries — **NOT AVAILABLE** (thinking text field empty)
- private CoT — **NOT AVAILABLE** (`thinking` present but empty in 100% of sampled
  items; keys `{type, thinking, signature}`; no `redacted_thinking`)
- thinking-block COUNT per turn (generation/reasoning-activity proxy) — **RAW**
- `effort` (assistant) — **RAW**

**3 — Tool activity**
- tool name (`tool_use.name`) — **RAW**
- arguments (`tool_use.input`) — **RAW**
- result (`tool_result` + `toolUseResult.{stdout,stderr,content,structuredPatch,...}`) — **RAW**
- error (`tool_result.is_error`; `toolUseResult.success` / `interrupted`) — **RAW**
- start/end time (`durationMs` / `durationSeconds` where present) — **RAW**; else **DERIVABLE** (timestamp deltas)
- retries — **DERIVABLE** (repeated tool_use)
- parallelism (multiple tool_use/message; `backgroundTaskId` / `isAsync` / `pendingBackgroundAgentCount`) — **RAW / DERIVABLE**
- subagent dispatch (`agentId` / `outputFile` / `resolvedModel` / `canReadOutputFile`) — **RAW**

**4 — Files / commands**
- file path (`toolUseResult.filePath`) — **RAW**
- read/write distinction (tool name + `oldString`/`newString`/`structuredPatch`/`originalFile`/`userModified`) — **RAW / DERIVABLE**
- command string (`toolUseResult.command` / `commandName`; Bash input) — **RAW**
- exit code (`toolUseResult.code` / `returnCodeInterpretation`; `success`) — **RAW**
- stdout / stderr (`toolUseResult.stdout` / `stderr`) — **RAW**
- repeated equivalent operation — exact input = **DERIVABLE**, high-precision; same
  filePath / same command = **DERIVABLE** but candidate structural signal only (not
  high-precision alone); semantic equivalence **NOT deterministic** (needs a judge)

**5 — Decision artifacts**
- plan / update / final messages (assistant text) — **RAW**
- explicit stop signals (`system.stopReason`, `stop_hook_summary`, `preventedContinuation`) — **RAW**
- tool denial (`user.toolDenialKind`) — **RAW** (event-driven)
- AskUserQuestion (`toolUseResult.questions` / `answers`) — **RAW**
- `attributionSkill` (which skill was active) — **RAW** (useful for routing GT, round 2)
- semantic decision states in prose ("ACCEPTED"/"HOLD") — **DERIVABLE only via semantic judge** (out of Phase-0 scope)

**6 — Context / token telemetry**
- input / output tokens (`message.usage.input_tokens` / `output_tokens`) — **RAW**
- cache tokens = context-size proxy (`cache_read_input_tokens` / `cache_creation_input_tokens`) — **RAW**
- cumulative context usage — **DERIVABLE** (running sum)
- turn duration (`system.turn_duration`) — **RAW**; also **DERIVABLE** (timestamp deltas)
- model switch (`message.model` change; system fallback fields) — **RAW**
- compaction event — **RAW** where the marker capability is qualified (Phase 0.1):
  `system.subtype=compact_boundary` immediately followed by `user.isCompactSummary=true`;
  found in other local projects, none in this project's sessions. Where qualified, adapter
  emits `observability=KNOWN` + `context_boundary=COMPACTION`. A stream/version whose marker
  capability is **not qualified** -> `observability=UNKNOWN` (never `NONE`); excluded from
  continuity-requiring qualification (DESIGN §3)
- extras (`iterations`, `speed`, `service_tier`, `inference_geo`) — **RAW**

**7 — Authorization state**
- permission mode (`user.permissionMode`: auto / acceptEdits / ...) — **RAW**
- tool denial (`user.toolDenialKind`) — **RAW** (event-driven)
- approval grant — **DERIVABLE** (a tool that ran was allowed; no separate explicit grant record)
- outward-action gate / hooks (`system.hookInfos` / `hookErrors` / `hookCount`; `stop_hook_summary`) — **RAW** (the pack's own gate hooks are observable)

**8 — Session lifecycle**
- entrypoint = session class (`cli` / `sdk-cli`) — **RAW**
- turn duration / stop-hook / scheduled fire / away (`system.subtype`) — **RAW**
- interruption / crash (`toolUseResult.interrupted`, `user.interruptedMessageId`, `system.stopReason`) — **RAW**
- fork WITHIN a session (parentUuid branching) — **RAW / DERIVABLE**
- resume — **DERIVABLE** (no explicit event; entrypoint / mode / continuation)
- fork / handoff / close ACROSS sessions — **NOT AVAILABLE** in the primary transcript streams inspected (other local stores not reconciled; PARK to HCSA1-D)

### 4. Lifecycle / fork / handoff availability

Within-session lifecycle is well covered (RAW): turn duration, stop-hook events,
scheduled fires, interruptions, and the parentUuid message DAG (which gives
within-session branching). **Cross-session** fork/handoff/close is the gap, scoped to
what was inspected: no record in the PRIMARY TRANSCRIPT STREAMS links a session to one
it forked from, handed off to, or closed into. Other local stores (`history.jsonl`,
`sessions/`, `state/`) were NOT reconciled in Phase 0 and are claimed neither way. Any
inference (timestamps, cwd, `leafUuid`) would be unreliable. Round-1's three judgments
are all within-session and do not need it;
`handoff_readiness` (round 2) and HCSA1-D do — flag for a capture hook or an
explicit-inference decision there.

### 5. Schema-instability findings

- Record-type names drift within one behavior window: `ai-title` -> `custom-title` (2026-09-24).
- Many record types / fields are event-driven (present only when the event occurred):
  `file-history-delta`, `pr-link`, `queue-operation`, refusal machinery
  (`apiRefusalCategory`, `retractedMessageUuids`), `pendingBackgroundAgentCount`,
  `interruptedMessageId`, `resolvedModel`.
- `toolUseResult` shape varies by tool (expected).
- CLI-version drift 2.1.221 -> 2.1.281 across the corpus.
- Conclusion: binding to the raw internal JSON schema is a maintenance trap.

### 6. Recommendation

**Usable, via an adapter — not direct schema binding.** Most needed observables are
RAW or cleanly DERIVABLE, across all three transcript classes. Build:

```
native transcript (cli / sdk-cli / subagent .output)
      -> adapter (absorbs record-type renames, event-driven fields, version drift; normalizes the 3 classes)
      -> HCSA observable event schema
      -> derived features
      -> golden labels / judges
```

- **One observable is missing from the primary transcript streams inspected:** explicit
  cross-session lifecycle (fork/handoff/close). Other local stores not reconciled. Not
  needed for round 1; PARK to HCSA1-D.
- **Private CoT is NOT AVAILABLE** and must not be a dependency — consistent with the
  observable-only design; nothing to change.

---

## Two design-critical conclusions (feed the DESIGN.md upgrade)

### A. Private CoT unavailable; generation-activity has RAW proxies (not a reasoning-length measure)
The corpus cannot depend on CoT content (thinking text is stripped; only a signed
placeholder + count remain). But observable **generation / reasoning-activity proxies**
survive — thinking-block count per turn, `output_tokens`, assistant `effort`, and
`system.turn_duration` (all RAW). These do NOT measure the length or content of hidden
reasoning. The study object is **observable execution redundancy / marginal evidence
gain**: whether the observable activity co-occurs with new decision-relevant evidence —
which is what the `redundant != long` distinction actually needs.

### B. The novelty fork: deterministic catches syntactic repeats only
Exact-duplicate tool inputs are trivially detectable, but their rate is LOW in real
sessions (6/329 tool inputs, 1/308 Bash in a long session) — real redundancy is rarely
byte-identical. Therefore:
- `repetition_state`: exact-repeat is high-precision; same-filePath revisit and
  same-command are candidate structural signals only (not high-precision alone) -> partly
  **DERIVABLE**.
- `evidence_progress` (decision-relevant novelty): a new command with semantically
  duplicate output, or a re-read yielding no new decision-relevant fact, is invisible to
  hashing -> **needs semantic judgment**.
- No aggregate `Evidence Gain Ratio` is frozen here: structural novelty is at most a
  candidate cheap floor, semantic evidence gain needs a judge, and whether the two ever
  combine into one scalar is deferred to HCSA1-B (see DESIGN §8). A semantic judge is
  load-bearing for round-1 `evidence_progress`; the deterministic layer alone is insufficient.

## Consequences for the round-1 corpus/schema contract
1. Adapter-first: freeze the HCSA observable event schema (the adapter's OUTPUT), not
   the native transcript schema.
2. Round-1 observables are all present: turn duration, tokens, thinking-block count,
   tool name/input/result, filePath/command/exit/stdout, permissionMode, denials,
   stop-hook, parentUuid DAG.
3. `evidence_progress` labeling must be human/owner ground truth (semantic); do not
   pretend a deterministic proxy is the label.
4. Corpus can draw from three real classes already on disk (interactive, eval-sandbox,
   subagent) — external validity + controlled cases both available without new capture.
5. Defer anything cross-session (handoff) to round 2 / HCSA1-D.
