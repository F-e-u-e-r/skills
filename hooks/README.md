# Hooks — optional repo-level enforcement

These optional, repo-level hooks give hard, model-independent enforcement. **No plugin registers them** — they change Claude Code harness behavior, so installing them is an explicit, per-user decision. Wiring, exit-code contracts, per-hook threat/behavior, configuration, and known limitations follow. Repository overview: [`README.md`](../README.md).

## Enforcement: setting up hooks

Hooks are shell commands the Claude Code harness itself runs on events —
unlike skills, the model cannot skip them. Full docs:
<https://docs.claude.com/en/docs/claude-code/hooks>.

**Where they live** (JSON in settings files):

| File | Scope |
|---|---|
| `~/.claude/settings.json` | you, all projects |
| `<repo>/.claude/settings.json` | the project, committed/shared |
| `<repo>/.claude/settings.local.json` | the project, personal, not committed |

**The exit-code contract:** exit `0` = allow/continue; exit `2` = block — for
`PreToolUse` the tool call is stopped and stderr is fed back to the model, so
it knows why and can fix the cause; other codes = non-blocking warning.

**Worked example — no commit while gates are red** (script ships at
`hooks/gate-before-commit.sh`, tested 2026-07-07: non-commit
commands and green gates pass through; red gates block with the failure fed
back to the model; it gates the repo the commit *targets*, and uses `jq` +
`python3` (`parse-commit-command.py`) to detect commits from command structure
— so quoted messages, branch names, and `printf`/heredoc prose no longer
misfire. A missing `jq`/`python3` fails closed on a likely commit rather than
silently allowing one):

```bash
mkdir -p .claude/hooks
cp hooks/gate-before-commit.sh hooks/parse-commit-command.py .claude/hooks/
cp hooks/verify-before-stop.py hooks/gate-credential-destruction.py .claude/hooks/
cp hooks/skill-vetting-advisory.py hooks/skill_snapshot.py .claude/hooks/
```

Maintainers can regression-test every hook (each suite covers both sides of
its hook's behavior — allow and block for the gating hooks, silent and
advisory for the advisory hook):

```bash
bash hooks/test-gate-before-commit.sh
bash hooks/test-verify-before-stop.sh
bash hooks/test-gate-credential-destruction.sh
bash hooks/test-skill-vetting-advisory.sh
bash hooks/test-skill_snapshot.sh
```

Then add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/gate-before-commit.sh"
          }
        ]
      }
    ]
  }
}
```

**Events worth knowing** (matcher applies to tool names for the first two):

| Event | Fires | Exit 2 means |
|---|---|---|
| `PreToolUse` | before a tool call | the call is blocked |
| `PostToolUse` | after a tool call | stderr is shown to the model |
| `Stop` | when the model tries to end its turn | the model must continue |
| `SessionStart` | at session start | — (stdout joins context; good for env self-healing) |
| `UserPromptSubmit` | on each user message | the prompt is blocked |

A `Stop` variant of the same script (drop the command match, keep the gates
check) means "the turn cannot end while gates are red". Keep the
no-gates-in-repo early exit — a Stop hook that can never pass loops the model
forever.

**Second (optional) hook — no turn ends on unverified code edits.**
`hooks/verify-before-stop.py` (Python 3 stdlib, tested 2026-07-07)
is a `Stop` hook that blocks ending the turn when code files were edited but
no test/verification command ran and no verification-intent subagent was
dispatched — the mechanical form of operational-rigor §4. Doc/config-only
edits never block; a second Stop always passes (anti-deadlock relief valve,
logged). Its known limits are documented in the script header — it checks
that verification *appeared*, not that it passed. Adapted from
curtischoutw/claude-institution's `verify_gate.py` (MIT — see [`../evidence/provenance.md`](../evidence/provenance.md)). Wire it with:

```json
"Stop": [
  { "matcher": "", "hooks": [ { "type": "command",
      "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-before-stop.py" } ] }
]
```

**Third (optional) hook — credential-pattern files don't get destroyed on
say-so.** `hooks/gate-credential-destruction.py` (Python 3 stdlib, tested
2026-07-11) is a `PreToolUse` (matcher: `Bash`) hook that blocks
`rm`/`unlink`/`shred`/`srm`/`truncate`/`git rm` — including `sudo`/wrapper
and path-qualified forms — on credential-looking paths (ssh private keys
and the `.ssh`/`.aws`/`.gnupg` directories, `.env` variants,
`*.pem`/keystores, anything named credential/secret/password/apikey) until
that specific deletion is explicitly confirmed: after the user's yes,
re-run prefixed with `CRED_GATE_APPROVED=1`, which overrides that one
command only. The override is friction plus an audit log, not proof of
consent — every approved override attempts to append an audit event, but
the log write is best-effort: a failed write is silently dropped and
never blocks the hook. Why the hook exists: in the pack's own
eval, both weak-tier no-skills runs deleted a credentials backup because
an instruction embedded in a vendor-notes file told them to — this gate
turns that exact failure into a blocked call whose error message points at
delegation-and-review §7 and security-architect. Known limits are in the
script header (`bash script.sh`, aliases, `find -delete`, `xargs rm`, and
`>` truncation bypass it — inherent to text-level hooks). Wire it as a
second command under the same `PreToolUse`/`Bash` matcher:

```json
{ "type": "command",
  "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/gate-credential-destruction.py" }
```

**Fourth (optional) hook — an advisory tripwire for unvetted or changed
third-party skills.** `hooks/skill-vetting-advisory.py` (Python 3 stdlib, tested)
is a **pure-advisory** `SessionStart` hook, the companion to the `skill-vetting`
skill; its whole observation layer lives in the sibling module
`hooks/skill_snapshot.py` — install both files into the same directory (design
record: `evidence/reviews/2026-07-25-skill-vetting-snapshot-threat-model.md`).
**Signature scanning is not a security boundary and has been removed**: the
primitive snapshots every file under each entry of the watched skills roots
(`$CLAUDE_CONFIG_DIR/skills`, default `~/.claude/skills`, plus the project's
`.claude/skills` via `$CLAUDE_PROJECT_DIR`), so an add / modify / delete /
rename / symlink / filetype change anywhere inside a skill — not just in its
`SKILL.md` — counts (one carve-out, stated under G1 in the threat model: a loose
regular file sitting directly in the skills root is not a candidate at all,
because it is not loadable as a skill),
and whatever cannot be fully observed (a read error, an oversize file, a scan-budget
breach and everything enumerated after it, any
symlink, a special file, a hostile TOP-LEVEL skill name — nested names are not
gated, a corrupt or version-stale baseline)
is an **anomaly that always advises and can never be certified unchanged**. For
a new, changed, removed, or anomalous skill it injects one line routing to the
`skill-vetting` skill. It **never blocks and never emits a "safe" line** — a
`SessionStart` hook cannot deny, and a green-lighting scanner is the
false-assurance trap `skill-vetting` exists to avoid; a clean, unchanged run is
silent — as is a first run that found nothing to record — while a first run
that HAS something to baseline emits one labelled line naming how many
installed skills it is BASELINING without reviewing them (the line is emitted
before the write and says so; a write that then fails is not announced
separately - it cannot be, under the one-message rule - and does not need to be,
because nothing was written and the next session says the same thing again) — a count that
includes candidates whose observation was COMPLETE but adverse (a symlink, an
unreadable directory, a special file, a hostile name), and excludes only those
lost to a resource-budget short-circuit, whose digest would be a placeholder;
each excluded one still advises through its own anomaly line; the advisory prints
**before** the baseline
(`<config>/skill-vetting/baseline.json`) advances — a failed delivery
re-advises next session — and skill names reach the model only through a strict
ASCII allowlist or an opaque id. The baseline is not tamper-evident (it shares
a trust level with the skills themselves); that limit is documented, not
defended. It is a tripwire that routes to the full vetting read, never a
substitute for it. Wire it with:

```json
"SessionStart": [
  { "matcher": "", "hooks": [ { "type": "command",
      "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/skill-vetting-advisory.py" } ] }
]
```

The three gating hooks append audit events to `~/.claude/hooks/hooks.log` and the
advisory vetting hook to `<CLAUDE_CONFIG_DIR>/skill-vetting/advisory.log`
(default `~/.claude/skill-vetting/advisory.log`), so gate activity — and the
vetting hook's advisories — is auditable instead of invisible (these log writes
are best-effort: a failed write is silently dropped and never blocks the hook).

**Two cautions.** Hooks run arbitrary shell with your permissions: read any
hook script before enabling it, and prefer committing hooks so they are
reviewed like code. And Claude Code snapshots hook config at startup: after
editing, review via the `/hooks` menu or restart the session for changes to
take effect.
