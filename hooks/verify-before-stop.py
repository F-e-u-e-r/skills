#!/usr/bin/env python3
"""Claude Code Stop hook: block ending the turn when code files were edited
but no test/verification command ran and no verification-intent subagent was
dispatched. Mechanically enforces operational-rigor §4 (verify by execution)
and §5 (independent verification for load-bearing work).

Adapted from `verify_gate.py` in curtischoutw/claude-institution @ 8dea062
(MIT License, Copyright (c) 2026 Curtis Chou), itself adapted from
Miguok/fable-harness. The window/anchor design is upstream's; the evidence
classifier was rebuilt in-repo (2026-11-04, see below); messages rewritten to
point at this pack's rules. Python 3.8+, stdlib only.

Behavior:
- Only triggers when code-extension files were edited this turn AND no
  verification evidence appeared AFTER THE LAST code edit (operational-rigor
  §5: a fix invalidates earlier green results). Doc/config edits never block.
- Evidence is one of three classes (2026-11-04 rebuild; the name-list detector
  it replaces blocked 430 of 430 sampled real turns that had in fact executed
  project checks such as `python3 -I regression/run_eval.py`):
  V1 executed code: each Bash/Monitor command is split into simple commands
     and classified by WHAT RUNS (which launcher executes which kind of
     target), not by the name of a project's test script - an interpreter
     running a script file or a non-stdlib module (env prefixes, wrappers such
     as timeout/env/time, and interpreter options are stripped), a stdlib
     check (`-m unittest|doctest|py_compile|compileall|runpy|...`), a shell
     `-c` string, `ssh host '<cmd>'` or `$(...)` (recursed), the syntax-check
     flags in OPTS (`bash -n`, `node --check|--test`, `ruby -c`, `perl -c`,
     `php -l`), a package script/binary (npm/pnpm/yarn/npx), a relative-path
     executable, an absolute path to a code file, or a runner from
     TEST_CMD_RE. Inline code (`-c`, `-e`, a heredoc on stdin) counts only
     when it LOADS, compiles or runs an edited unit (import/require/source,
     py_compile, runpy, subprocess of the file): a patch script that rewrites
     the file, `print(open('app.py').read())`, or `print('app: VERIFIED')`
     exercise nothing. Heredoc DATA bodies (`cat > f <<EOF`, an unterminated
     heredoc) never count; a heredoc fed to a shell - directly or through
     `cat <<EOF |` - is classified as the script it is. A command whose own
     tool_result says it never launched (command not found, can't open file,
     no such file, permission denied) gets no credit.
  V2 a verification-intent dispatch (Agent/Task prompt or description, or a
     SendMessage whose text shows it; the recipient is not checked) - the hook
     must not punish the pack's own delegate-the-check rule; the vocabulary
     includes the critic/adversarial/audit idiom. Intent is LEXICAL: an
     implementation dispatch that mentions a critic also counts.
  V3 an explicit final-report line "No executable test applies: <reason>;
     verified by <method>" (read from the documented `last_assistant_message`
     Stop field, falling back to assistant text after the last edit). Honor
     system, like the relief valve - but explicit, and audit-logged with text.
- Prose, Bash `description` text, `echo` markers, and inspection commands
  (cat/grep/git/gh/...) never count.
- stop_hook_active (the second Stop) always passes — relief valve so a
  blocked turn cannot deadlock; the pass is logged for audit.
- Fail-open: any internal error passes, with the traceback logged.
- Quiet-degradation telemetry (2026-07-24, after Miguok/fable-harness
  b6f794e fixed the same defect class upstream): every silent no-op path
  now attempts to leave a log line (best-effort — _log swallows its own
  failures to preserve fail-open), so a harness schema drift cannot
  disable the gate invisibly for weeks. Levels (checked after the relief
  valve — a second Stop logs its own PASS first): missing transcript_path
  = ERROR (schema drift); a transcript with user entries but no real prompt = PASS with
  reason (known degenerate shape — sampled 2026-07-24: real sessions carry
  61-209 user entries, mostly list-content tool results); a transcript
  with NO user-type entries at all (or empty) = WARN (unknown shape,
  possible drift).

Known limits (mechanically unfixable; do not treat this hook as omniscient):
- It checks that evidence APPEARED, not that tests passed, that the executed
  script exercises the edit (`python3 unrelated.py` counts), or that a V3
  justification is honest. A determined agent can satisfy it; it exists to
  catch the forgetful one.
- Double-Stop escape: after a block, replying anything and stopping again
  passes (the relief valve). The audit log is the only compensation.
- The window covers only tool calls after the last real user prompt; harness
  string entries (task notifications, subagent hand-backs, a post-compaction
  system reminder) also anchor it, so an edit made before one of them leaves
  the window (fail-open, pre-existing).
- Edits made through Bash (sed -i, heredoc writes, scripts) are invisible:
  only Edit/Write/NotebookEdit/MultiEdit tool calls count as edits.
- A command denied by a permission prompt or a hook still counts unless its
  result text shows a not-found/permission failure; a result the transcript
  has not caught up with, or a background launch's, is treated as absent.
- Any package script (`npm run deploy`) or package binary (`npx prettier
  --write`) counts; info flags on runners (`pytest --version`) count; a dead
  branch (`if false; then pytest; fi`) counts - presence, not reachability.
- Not recognized: implicit-target runners outside TEST_CMD_RE (make test,
  tox), toolchain checkers/compilers (tsc, mypy, shellcheck, swift build,
  go build/vet, cargo check, javac, cc, xcodebuild, tsx/ts-node, pre-commit),
  container exec (docker/kubectl), sudo, xargs and find -exec launches;
  stdin piped into an interpreter from anything but a `cat` heredoc.
- A real prompt whose content is a list (an image, a pasted block) does not
  anchor the window (pre-existing); subagent edits, extensionless scripts and
  upper-case extensions are not seen as code edits.
"""

import datetime
import json
import os
import re
import shlex
import sys
import sysconfig
import traceback

EDIT_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}
AGENT_TOOLS = {"Task", "Agent", "SendMessage"}
AGENT_TEXT_FIELDS = ("prompt", "description", "message", "summary")

CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".go", ".rs", ".java", ".rb", ".php", ".c", ".cpp", ".cc", ".h", ".hpp",
    ".cs", ".swift", ".kt", ".kts", ".scala", ".sh", ".bash", ".zsh",
    ".sql", ".lua", ".ex", ".exs", ".clj", ".cljs", ".hs", ".ml", ".mli",
    ".r", ".m", ".mm", ".vue", ".svelte", ".dart", ".jl",
    ".ipynb", ".tf", ".pl", ".pm", ".groovy",
}

# Test/check runners whose target is implicit (the runner discovers it), so no
# script path appears on the command line. Defined once; both regexes below use it.
_RUNNER_WRAP = r"(?:(?:time|npx|uv\s+run|poetry\s+run|pdm\s+run)\s+)?"
_RUNNERS = (
    r"pytest|py\.test|python3?\s+-m\s+pytest|"
    r"npm\s+(?:run\s+)?test|yarn\s+test|pnpm\s+test|"
    r"jest|vitest|"
    r"go\s+test|cargo\s+test|"
    r"mvn\s+test|gradle\s+test|\.\/gradlew\s+test|"
    r"rspec|bundle\s+exec\s+rspec|"
    r"dotnet\s+test|swift\s+test|phpunit|ctest|mix\s+test|"
    r"bash\s+\S*run-all\.sh|"      # gtg convention: checks/ or template/ run-all.sh
    r"bash\s+\S*test-[\w.-]+\.sh|"  # test-*.sh suites; \S* tolerates false-allows (mytest-/contest- prefixes) — presence heuristic, cheap direction
    r"python3?\s+\S*checks\.py"     # repo check scripts (.github/checks.py)
)
# Raw-text form (command position = line start or after ;|&|( ) - the
# pre-2026-11-04 detector, kept only as the fallback if the classifier raises.
TEST_CMD_RE = re.compile(
    r"(?:^|[\n;&|(]\s*)" + _RUNNER_WRAP + "(" + _RUNNERS + r")\b", re.IGNORECASE)

# The same alternation anchored to ONE simple command's own words: the
# structural classifier applies it per command, so quoted text such as
# `echo "a; pytest"` can no longer forge a command position.
RUNNER_RE = re.compile(_RUNNER_WRAP + "(" + _RUNNERS + r")\b", re.IGNORECASE)

VERIFY_INTENT_RE = re.compile(
    r"(驗證|實跑|跑.{0,6}測試|read-?back|第二意見|審查|複核|"
    r"verif(?:y|ication)|run\s+(?:the\s+)?tests?|"
    # the pack's own fresh-context check idiom (delegation-and-review §3)
    r"\bcritics?\b|\baudit(?:or|ors|ing)?\b|\bred[- ]?team(?:ing|er)?\b|"
    r"\badversarial(?:ly)?\s+(?:review|critic|audit))",
    re.IGNORECASE,
)

# V3: an explicit statement that no executable verification applies, naming the
# bounded method used instead. The method clause is mandatory, and a method that
# is still the `<method>` placeholder is a report QUOTING the form (as one about
# this hook would), not using it.
NO_EXEC_JUSTIFICATION_RE = re.compile(
    r"\bno executable test applies\b[^\n;]*;\s*verified by\s+(?P<method>(?![`'\"*_]*<)[^\n]{8,})",
    re.IGNORECASE,
)

PY_RE = re.compile(r"^(?:python|pypy)(?:\d+(?:\.\d+)*)?$")
FAMILIES = {
    "node": {"node", "nodejs"}, "deno": {"deno"}, "bun": {"bun"},
    "ruby": {"ruby"}, "perl": {"perl"}, "php": {"php"},
    "shell": {"bash", "sh", "zsh", "dash", "ksh"},
    "misc": {"lua", "luajit", "Rscript", "julia"},
}
# per family: inline-code options, options consuming the next word, and flags
# that make the run a check of its own (syntax check / built-in test runner).
# Info flags need no entry: `python3 --version` has no operand, so no credit.
OPTS = {
    "python": ({"-c"}, {"-W", "-X", "-Q"}, set()),
    "node": ({"-e", "--eval", "-p", "--print"},
             {"-r", "--require", "--import", "--loader", "--experimental-loader",
              "--env-file", "-C", "--conditions", "--input-type"},
             {"--test", "-c", "--check"}),
    "ruby": ({"-e"}, {"-I", "-r", "-C", "-E"}, {"-c"}),
    "perl": ({"-e", "-E"}, {"-I"}, {"-c"}),
    "php": ({"-r"}, {"-d", "-c"}, {"-l"}),
    "shell": ({"-c"}, {"-o", "+o", "-O", "+O", "--rcfile", "--init-file"}, {"-n"}),
    "misc": ({"-e"}, set(), set()),
}
DENO_BUN_EXEC_SUBCMDS = {"test", "check", "run", "x"}
DENO_BUN_TOOL_SUBCMDS = {"install", "i", "add", "remove", "rm", "init", "create", "upgrade",
                         "pm", "link", "unlink", "outdated", "update", "publish", "fmt",
                         "info", "doc", "repl", "completions", "cache"}
# `python3 -m <module>`: a project or third-party module runs code; a STDLIB
# module runs a stdlib tool (timeit, json.tool, http.server, venv, calendar...)
# unless it is one of the stdlib checks/runners below. pip-family modules are
# third-party tooling, not checks.
PY_NON_VERIFY_MODULES = {"pip", "pipx", "virtualenv"}
STDLIB_VERIFY_MODULES = {"unittest", "doctest", "py_compile", "compileall", "test",
                         "runpy", "trace", "cProfile", "profile", "pdb"}
# Inline code (`-c`, `-e`, a heredoc on stdin) counts only when it LOADS, compiles
# or runs an edited unit - mentioning its name is not enough: a patch script that
# reads and rewrites app.py, `print(open('app.py').read())`, or
# `print('app: VERIFIED')` all name the file and exercise nothing. {s} = module
# stem, {b} = basename (both regex-escaped).
LOAD_PATTERNS = {
    "python": (r"(?:^|;)[ \t]*import[ \t]+[^\n#;]*(?<![\w])(?:[\w.]*\.)?{s}(?![\w])",
               r"(?:^|;)[ \t]*from[ \t]+(?:[\w.]*\.)?{s}(?:\.[\w.]+)?[ \t]+import\b",
               r"(?:^|;)[ \t]*from[ \t]+[\w.]+[ \t]+import[ \t]+[^\n#;]*(?<![\w]){s}(?![\w])",
               r"(?:import_module|__import__)\s*\(\s*['\"][\w.]*(?<![\w]){s}(?![\w])",
               r"\b(?:spec_from_file_location|SourceFileLoader|run_path|load_source)\s*\([^\n]*['\"][^'\"\n]*(?<![\w]){b}['\"]",
               r"(?s)\b(?:py_compile|compileall|runpy)\b.*['\"][^'\"\n]*(?<![\w]){b}['\"]",
               r"(?s)['\"][^'\"\n]*(?<![\w]){b}['\"].*\b(?:py_compile|compileall|runpy)\b",
               r"\bexec\s*\(\s*(?:compile\s*\(\s*)?open\s*\(\s*['\"][^'\"\n]*(?<![\w]){b}['\"]",
               r"(?:subprocess\.\w+|os\.system)\s*\([^\n]*['\"][^'\"\n]*(?<![\w]){b}\b"),
    "node": (r"\b(?:require|import)\s*\(\s*['\"][^'\"]*(?<![\w]){s}(?:\.\w+)?['\"]",
             r"\b(?:from|import)\s+['\"][^'\"]*(?<![\w]){s}(?:\.\w+)?['\"]"),
    "ruby": (r"\b(?:require|require_relative|load)\s*\(?\s*['\"][^'\"]*(?<![\w]){s}(?:\.rb)?['\"]",),
    "perl": (r"\b(?:require|use|do)\s+['\"]?[\w:/.]*(?<![\w]){s}(?![\w])",),
    "php": (r"\b(?:require|include)(?:_once)?\s*\(?\s*['\"][^'\"]*(?<![\w]){b}['\"]",),
    "misc": (r"\b(?:require|dofile|source|include)\s*\(?\s*['\"][^'\"]*(?<![\w])(?:{s}|{b})['\"]",
             r"\busing\s+[\w, ]*(?<![\w]){s}(?![\w])"),
}
# A tool_result proving a launch never happened (zsh, bash, python, node).
NOT_FOUND_RES = (
    re.compile(r"command not found: (\S+)"),
    re.compile(r"(\S+): command not found"),
    re.compile(r"no such file or directory: (\S+)"),
    re.compile(r"(\S+): No such file or directory"),
    re.compile(r"permission denied: (\S+)"),
    re.compile(r"(\S+): Permission denied"),
    re.compile(r"can't open file '([^']+)'"),
    re.compile(r"Cannot find module '([^']+)'"),
)
SSH_ARG_OPTS = set("bcDEeFIiJLlmOopQRSWw")
WRAPPERS = {"time", "command", "exec", "nice", "nohup", "env", "timeout", "gtimeout",
            "caffeinate"}
TWO_WORD_WRAPPERS = {("uv", "run"), ("poetry", "run"), ("pdm", "run"), ("pipenv", "run"),
                     ("hatch", "run"), ("rye", "run"), ("bundle", "exec")}
# JS package managers are that ecosystem's launcher: running a package script
# (`npm run check`, `pnpm -r test`, `yarn build`) or a package binary
# (`pnpm exec vitest`, `npx tsc`) executes code; installing/inspecting does not.
PM_EXEC_SUBCMDS = {
    "npm": {"run", "run-script", "rum", "urn", "test", "t", "tst", "start", "exec", "x"},
    "pnpm": {"run", "test", "t", "tst", "exec", "dlx", "start"},
    "yarn": {"run", "test", "exec", "dlx", "start", "node"},
}
PM_SHORTHAND = {"pnpm", "yarn"}  # an unknown subcommand is a script/bin name
PM_TOOL_SUBCMDS = {"add", "install", "i", "ci", "remove", "rm", "uninstall", "un", "update", "up",
                   "upgrade", "publish", "pack", "info", "view", "list", "ls", "la", "ll",
                   "outdated", "audit", "why", "init", "create", "config", "set", "get", "cache",
                   "store", "link", "unlink", "login", "logout", "whoami", "version", "prune",
                   "dedupe", "import", "fetch", "rebuild", "help", "global", "env", "setup",
                   "patch", "licenses", "bin", "root", "doctor", "self-update", "plugin",
                   "workspace", "workspaces", "approve-builds"}
PM_ARG_OPTS = {"--filter", "-F", "-C", "--dir", "--prefix", "--workspace", "--cwd",
               "--reporter", "--loglevel"}
EXEC_TOOLS = {"Bash", "Monitor"}  # both run a shell command line
SHELL_KEYWORDS = {"if", "then", "else", "elif", "while", "until", "do", "!", "{", "time"}
HEREDOC_RE = re.compile(r"(?<!<)<<(-?)[ \t]*\\?(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2")
PLACEHOLDER_RE = re.compile(r"^__VBS_HEREDOC_(\d+)__$")

LOG_PATH = os.path.expanduser("~/.claude/hooks/hooks.log")
LOCAL_COMMAND_MARKERS = ("<local-command-stdout>", "<command-name>", "<local-command-caveat>")

BLOCK_REASON = (
    "Code files were edited this turn (Edit/Write/NotebookEdit), but no "
    "verification evidence appeared after the last code edit. This hook only "
    "checks that verification APPEARED — not that it passed.\n"
    "Per operational-rigor §4: \"Verify by execution wherever possible. If "
    "impossible, say so and state what the user must run.\"\n"
    "Any ONE of these, after the last code edit, satisfies it: run code that "
    "exercises the change (the project's tests, check or regression scripts, "
    "a compile/syntax check - e.g. bash checks/run-all.sh, pytest, "
    "python3 -m py_compile <file>) and show the output; dispatch a "
    "fresh-context verification subagent such as a critic "
    "(delegation-and-review §3); or, if no executable verification applies "
    "(e.g. config-only, fixture data), put this line in the final report: "
    "\"No executable test applies: <reason>; verified by <method>\"."
)


def _log(line):
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{ts} verify-before-stop: {line}\n")
    except Exception:
        pass


def load_transcript(path):
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def is_real_user_prompt(entry):
    if entry.get("type") != "user":
        return False
    content = (entry.get("message") or {}).get("content")
    if not isinstance(content, str):
        return False
    return not any(marker in content for marker in LOCAL_COMMAND_MARKERS)


def _edited_names(paths):
    """(stem, basename) pairs of edited code files."""
    names = set()
    for p in paths:
        base = os.path.basename(p)
        stem = os.path.splitext(base)[0]
        if base and stem:
            names.add((stem, base))
    return names


def _loads_edited(code, fam, names):
    """Does inline code load, compile, or run one of the edited units?"""
    for stem, base in names:
        for pat in LOAD_PATTERNS.get(fam, ()):
            rx = pat.replace("{s}", re.escape(stem)).replace("{b}", re.escape(base))
            if re.search(rx, code or "", re.MULTILINE):
                return True
    return False


def _is_stdlib(module):
    root = module.split(".")[0]
    if root in sys.builtin_module_names:
        return True
    std = sysconfig.get_paths().get("stdlib") or ""
    return bool(std) and (os.path.isfile(os.path.join(std, root + ".py"))
                          or os.path.isdir(os.path.join(std, root)))


def _module_runs_code(module):
    root = (module or "").split(".")[0]
    if not root or root in PY_NON_VERIFY_MODULES:
        return False
    if root in STDLIB_VERIFY_MODULES:
        return True
    return not _is_stdlib(root)


def _not_found(result_text):
    """Programs/scripts the command's own output says never launched."""
    gone = set()
    for rx in NOT_FOUND_RES:
        for m in rx.finditer(result_text or ""):
            tok = m.group(1).strip("'\":")
            if tok:
                gone.update({tok, os.path.basename(tok)})
    return gone


def _extract_heredocs(text):
    """Pull heredoc bodies out of the command text. Each `<<DELIM` operator is
    replaced by a placeholder word; its body lines are removed so they can never
    be parsed as commands (a heredoc is DATA unless a shell or interpreter reads
    it - decided later, per simple command). An operator with no closing
    delimiter line is left alone (it was not a heredoc)."""
    lines = text.split("\n")
    out, bodies, i = [], [], 0
    while i < len(lines):
        line = lines[i]
        pending = []

        def _swap(m):
            pending.append((m.group(1) == "-", m.group(3)))
            return " __VBS_HEREDOC_%d__ " % (len(bodies) + len(pending) - 1)

        swapped = HEREDOC_RE.sub(_swap, line)
        j = i + 1
        closed, collected = True, []
        for strip_tabs, delim in pending:
            body = []
            while j < len(lines):
                cand = lines[j].lstrip("\t") if strip_tabs else lines[j]
                j += 1
                if cand == delim:
                    break
                body.append(lines[j - 1])
            else:
                closed = False
            collected.append("\n".join(body))
        if pending:
            # an unterminated heredoc runs to end of input, as in bash: still data
            out.append(swapped)
            bodies.extend(collected)
            i = j if closed else len(lines)
        else:
            out.append(line)
            i += 1
    return "\n".join(out), bodies


def _tokenize(text):
    lex = shlex.shlex(text, posix=True, punctuation_chars=";&|()<>\n")
    lex.whitespace = " \t\r"
    lex.whitespace_split = True
    lex.commenters = ""  # shlex comments swallow the newline that ends them
    return list(lex)


def _segments(tokens):
    """Split tokens into simple commands, each paired with the separator that
    ended the previous one ("|" marks a pipe feeding it). Punctuation runs that
    contain < or > are redirections (kept, skipped later)."""
    segs, cur, sep, prev = [], [], "", ""
    for t in tokens:
        if t and all(c in ";&|()<>\n" for c in t) and not ("<" in t or ">" in t):
            if cur:
                segs.append((cur, prev))
                prev = t
            cur = []
        else:
            cur.append(t)
    if cur:
        segs.append((cur, prev))
    return segs


def _args(words):
    """Drop redirections (operator + target, and a leading fd number) and heredoc
    placeholders; return (plain words, heredoc indexes fed to this command)."""
    plain, docs, i = [], [], 0
    while i < len(words):
        w = words[i]
        m = PLACEHOLDER_RE.match(w)
        if m:
            docs.append(int(m.group(1)))
        elif w and all(c in "<>&" for c in w) and ("<" in w or ">" in w):
            i += 1  # skip the redirection target too
        elif w.isdigit() and i + 1 < len(words) and words[i + 1][:1] in ("<", ">"):
            pass
        else:
            plain.append(w)
        i += 1
    return plain, docs


def _strip_prefixes(words, launched=None):
    """Strip env assignments, shell keywords, and transparent wrappers; every
    wrapper removed is appended to `launched` (it must exist for anything to run)."""
    changed = True
    while words and changed:
        changed = False
        w = words[0]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", w) or w in SHELL_KEYWORDS:
            words, changed = words[1:], True
        elif len(words) > 1 and (w, words[1]) in TWO_WORD_WRAPPERS:
            if launched is not None:
                launched.append(w)
            words, changed = words[2:], True
        elif w in WRAPPERS:
            if launched is not None:
                launched.append(w)
            if w == "command" and len(words) > 1 and words[1] in ("-v", "-V"):
                return []  # `command -v x` is a lookup, not a run
            words = words[1:]
            while words and (words[0].startswith("-") or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0])):
                opt = words[0]
                takes = (w in ("timeout", "gtimeout") and opt in ("-s", "-k", "--signal", "--kill-after")) \
                    or (w == "nice" and opt == "-n") or (w == "env" and opt in ("-u", "-C", "-S")) \
                    or (w == "caffeinate" and opt in ("-t", "-w"))
                words = words[2:] if takes else words[1:]
            if w in ("timeout", "gtimeout") and words:
                words = words[1:]  # the DURATION operand
            changed = True
    return words


def _pm_runs_code(pm, args):
    arg_opts = PM_ARG_OPTS | ({"-w"} if pm == "npm" else set())
    i = 0
    while i < len(args):
        if args[i] in arg_opts:
            i += 2
        elif args[i].startswith("-"):
            i += 1
        else:
            break
    if i >= len(args):
        return False  # bare `yarn` installs; bare `npm` prints help
    sub = args[i]
    if sub in PM_EXEC_SUBCMDS[pm]:
        return True
    return pm in PM_SHORTHAND and sub not in PM_TOOL_SUBCMDS


def _family(prog):
    if PY_RE.match(prog):
        return "python"
    for fam, names in FAMILIES.items():
        if prog in names:
            return fam
    return None


PATTERN_FAMILY = {"python": "python", "node": "node", "deno": "node", "bun": "node",
                  "ruby": "ruby", "perl": "perl", "php": "php", "misc": "misc"}


def _interp_runs_code(fam, args, docs, bodies, names, depth, gone):
    inline_opts, arg_opts, check_flags = OPTS["node" if fam in ("deno", "bun") else fam]
    pfam = PATTERN_FAMILY.get(fam)
    if fam in ("deno", "bun"):
        rest = [a for a in args if not a.startswith("-")]
        if rest and rest[0] in DENO_BUN_TOOL_SUBCMDS:
            return False
        if rest and rest[0] in DENO_BUN_EXEC_SUBCMDS:
            return True
    i, check = 0, False
    while i < len(args):
        a = args[i]
        if a == "--":
            i += 1
            break
        if a in check_flags:
            check = True
            i += 1
            continue
        if fam == "python" and a.startswith("-") and not a.startswith("--") and len(a) > 1:
            # python short options combine (`-Ic code`, `-IBm mod`, `-Wignore`)
            for k, ch in enumerate(a[1:], 1):
                if ch in "cmWXQ":
                    val = a[k + 1:] or (args[i + 1] if i + 1 < len(args) else "")
                    if ch == "c":
                        return _loads_edited(val, pfam, names)
                    if ch == "m":
                        return _module_runs_code(val)
                    i += 0 if a[k + 1:] else 1
                    break
            i += 1
            continue
        if fam == "shell" and a.startswith(("-", "+")) and not a.startswith("--") and len(a) > 1:
            consumed = 0
            for ch in a[1:]:
                if ch == "c":
                    code = args[i + 1 + consumed] if i + 1 + consumed < len(args) else ""
                    return depth < 4 and _command_runs_code(code, names, depth + 1, gone)
                if ch == "n":
                    check = True
                if ch in "oO":
                    consumed += 1
            i += 1 + consumed
            continue
        if a in inline_opts or any(a.startswith(o + "=") for o in inline_opts if o.startswith("--")):
            code = a.split("=", 1)[1] if "=" in a else (args[i + 1] if i + 1 < len(args) else "")
            if fam == "shell":
                return depth < 4 and _command_runs_code(code, names, depth + 1, gone)
            return _loads_edited(code, pfam, names)
        if a in arg_opts:
            i += 2
            continue
        if a.startswith("-") and a != "-":
            i += 1
            continue
        break
    operand = args[i] if i < len(args) else None
    if operand is not None and operand != "-":
        # a script file (or deno/bun path) runs - unless its own output says it was never found
        return operand not in gone and os.path.basename(operand) not in gone
    if check:
        return True  # `node --test`, a syntax check with its target elsewhere
    body = "\n".join(bodies[d] for d in docs if d < len(bodies))
    if not body:
        return False  # stdin from a pipe or terminal: content unknown, so no credit
    if fam == "shell":
        return depth < 4 and _command_runs_code(body, names, depth + 1, gone)
    return _loads_edited(body, pfam, names)


def _substitutions(word):
    """Bodies of $(...) and `...` inside one (possibly quoted) word."""
    out, i = [], 0
    while i < len(word):
        if word.startswith("$(", i):
            level, j = 1, i + 2
            while j < len(word) and level:
                level += {"(": 1, ")": -1}.get(word[j], 0)
                j += 1
            out.append(word[i + 2:j - 1] if not level else word[i + 2:])
            i = j
        elif word[i] == "`":
            j = word.find("`", i + 1)
            out.append(word[i + 1:j if j != -1 else len(word)])
            i = len(word) if j == -1 else j + 1
        else:
            i += 1
    return out


def _simple_runs_code(words, docs, bodies, names, depth, gone):
    if depth < 4:
        # a command substitution inside any word runs (`out="$(pytest -q)"`)
        for w in words:
            for inner in _substitutions(w):
                if _command_runs_code(inner, names, depth + 1, gone):
                    return True
    launched = []
    words = _strip_prefixes(words, launched)
    if not words or words[0].startswith("#"):
        return False
    prog_tok = words[0]
    prog = os.path.basename(prog_tok)
    if any(x in gone for x in launched + [prog_tok, prog]):
        return False  # the command's own output says this never launched
    if RUNNER_RE.match(" ".join([prog] + words[1:])):
        return True  # pytest, npm test, ... (also as /path/to/pytest)
    if re.match(r"^pip[\d.]*$|^pipx$", prog):
        return False  # package installs, however the pip is reached
    if prog in PM_EXEC_SUBCMDS:
        return _pm_runs_code(prog, words[1:])
    if prog in ("npx", "bunx", "pnpx"):
        rest = words[1:]
        while rest and rest[0].startswith("-"):
            rest = rest[2:] if rest[0] in ("-p", "--package") else rest[1:]
        return bool(rest)  # a package binary runs (like `python3 -m <tool>`)
    if prog == "ssh":
        # `ssh [opts] host <remote command>`: the remote command is a shell line
        rest, k = words[1:], 0
        while k < len(rest) and rest[k].startswith("-"):
            k += 2 if rest[k][-1:] in SSH_ARG_OPTS and len(rest[k]) == 2 else 1
        remote = rest[k + 1:]
        return depth < 4 and bool(remote) and _command_runs_code(" ".join(remote), names, depth + 1, gone)
    fam = _family(prog)
    if fam:
        return _interp_runs_code(fam, words[1:], docs, bodies, names, depth, gone)
    if "/" in prog_tok:
        if not prog_tok.startswith(("/", "~")):
            return True  # ./run_tests, bin/check: a project-local executable
        return os.path.splitext(prog)[1].lower() in CODE_EXTENSIONS
    return False


def _classify_segments(segs, bodies, names, depth, gone):
    carry = []
    for seg, sep in segs:
        words, docs = _args(seg)
        if sep == "|" and carry:
            docs = docs + carry  # `cat <<EOF | bash`: the heredoc is the next stage's stdin
        if _simple_runs_code(words, docs, bodies, names, depth, gone):
            return True
        stripped = _strip_prefixes(list(words))
        carry = docs if (stripped and os.path.basename(stripped[0]) == "cat" and docs
                         and len(stripped) == 1) else []
    return False


def _command_runs_code(command, names, depth=0, gone=frozenset()):
    """V1: does this Bash command text execute code (see the header)?"""
    text = (command or "").replace("\\\n", " ")
    stripped, bodies = _extract_heredocs(text)
    try:
        tokens = _tokenize(stripped)
    except ValueError:
        # unbalanced quoting (`echo don't`): classify line by line; a line that
        # still fails has its quoted spans replaced by a placeholder word and is
        # cut at the stray quote, so quoted text can never become a command
        for line in stripped.split("\n"):
            try:
                toks = _tokenize(line)
            except ValueError:
                safe = re.sub(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"", " Q ", line)
                safe = re.split(r"['\"]", safe)[0]
                toks = [t for t in re.split(r"\s+", re.sub(r"([;&|()<>])", r" \1 ", safe)) if t]
            if _classify_segments(_segments(toks), bodies, names, depth, gone):
                return True
        return False
    return _classify_segments(_segments(tokens), bodies, names, depth, gone)


def _bash_verifies(command, names, gone=frozenset()):
    try:
        return _command_runs_code(command, names, 0, gone)
    except Exception:
        # never let the classifier fail the gate open or closed on its own bug:
        # degrade to the pre-2026-11-04 detector for this command
        _log("WARN classifier error, raw-regex fallback: " + traceback.format_exc().replace("\n", " | ")[-300:])
        return bool(TEST_CMD_RE.search(command or ""))


def _justification(texts):
    for t in texts:
        m = NO_EXEC_JUSTIFICATION_RE.search(t or "")
        if m:
            return m.group(0)
    return None


def analyze(entries, last_assistant_message=None):
    """Return (edited_code, verification_seen, status, evidence) for the turn.

    status: "ok" — a real user prompt anchored the window;
    "promptless-with-user-entries" — user entries exist but none is a real
    prompt (known degenerate shape: local-command/compaction edges);
    "no-user-entries" — no user-type entry at all, or an empty transcript
    (unknown shape — likely schema drift).
    evidence: which class satisfied the gate ("V1"/"V2"/"V3: <line>"), or None.
    Only evidence positioned AFTER the last code edit counts (V6).
    """
    last_idx = None
    for i, entry in enumerate(entries):
        if is_real_user_prompt(entry):
            last_idx = i
    if last_idx is None:
        has_user = any(
            isinstance(e, dict) and e.get("type") == "user" for e in entries
        )
        status = "promptless-with-user-entries" if has_user else "no-user-entries"
        return False, False, status, None  # fail-open by design; caller logs why

    seq = 0
    last_edit = None
    edited_paths = []
    events = []  # (seq, kind, payload, tool_use_id)
    results = {}  # tool_use_id -> tool_result text (absent while the transcript lags)
    for entry in entries[last_idx + 1:]:
        if entry.get("type") != "user":
            continue
        message = entry.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        for block in content if isinstance(content, list) else ():
            if isinstance(block, dict) and block.get("type") == "tool_result":
                body = block.get("content")
                if isinstance(body, list):
                    body = "\n".join(str(b.get("text") or "") for b in body if isinstance(b, dict))
                results[block.get("tool_use_id")] = body if isinstance(body, str) else ""
    for entry in entries[last_idx + 1:]:
        # Only the conversation record counts. Newer transcripts also store
        # content-addressed copies of request messages (`api-request-blob`),
        # written both before and after the real entry - counting them would
        # let an OLD test run appear after the last edit (or an old edit after
        # the test, or a test from before the window inside it). Sampled
        # 2026-11-04: 3905 such copies in 173 transcripts, none carrying a tool
        # call absent from the real entries, and no real entry repeating an id.
        if entry.get("type") != "assistant":
            continue
        message = entry.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            seq += 1
            btype = block.get("type")
            if btype == "text":
                events.append((seq, "text", block.get("text") or "", None))
                continue
            if btype != "tool_use":
                continue
            name = block.get("name")
            tool_input = block.get("input") or {}
            if not isinstance(tool_input, dict):
                tool_input = {}
            if name in EDIT_TOOLS:
                path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
                if isinstance(path, str) and any(path.endswith(ext) for ext in CODE_EXTENSIONS):
                    last_edit = seq
                    edited_paths.append(path)
            elif name in EXEC_TOOLS:
                cmd = tool_input.get("command")
                events.append((seq, "bash", cmd if isinstance(cmd, str) else "", block.get("id")))
            elif name in AGENT_TOOLS:
                events.append((seq, "agent", " ".join(
                    str(tool_input.get(k) or "") for k in AGENT_TEXT_FIELDS), None))
    if last_edit is None:
        return False, False, "ok", None

    names = _edited_names(edited_paths)
    after = [(k, v, t) for s, k, v, t in events if s > last_edit]
    for kind, payload, tid in after:
        if kind == "bash" and _bash_verifies(payload, names, _not_found(results.get(tid))):
            return True, True, "ok", "V1"
        if kind == "agent" and VERIFY_INTENT_RE.search(payload):
            return True, True, "ok", "V2"
    texts = [v for k, v, _ in after if k == "text"]
    if isinstance(last_assistant_message, str):
        texts.insert(0, last_assistant_message)
    line = _justification(texts)
    if line:
        return True, True, "ok", "V3: " + line
    return True, False, "ok", None


def main():
    """Always exits 0 (fail-open); a block is signaled via stdout JSON."""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}

        if data.get("stop_hook_active"):
            _log("PASS stop_hook_active (second Stop — relief valve, logged for audit)")
            return 0

        transcript_path = data.get("transcript_path")
        if not transcript_path:
            # Schema drift: without this field the gate can never run again.
            # Silent return here is how the upstream gate died unnoticed for
            # days (Miguok/fable-harness b6f794e) — leave a postmortem line.
            _log("ERROR schema-drift: hook payload has no transcript_path — gate cannot run (fail-open)")
            return 0

        lam = data.get("last_assistant_message")
        edited_code, verification_seen, status, evidence = analyze(
            load_transcript(transcript_path),
            last_assistant_message=lam if isinstance(lam, str) else None)
        if evidence and evidence.startswith("V3"):
            # the honor-system class: keep what was claimed, for audit
            _log("PASS no-exec justification: " + evidence[4:].replace("\n", " ")[:300])
        if status == "promptless-with-user-entries":
            _log("PASS degenerate transcript: user entries but no real user prompt (known shape) — fail-open by design")
        elif status == "no-user-entries":
            _log("WARN unknown transcript shape: no user-type entries at all — possible schema drift; gate cannot window (fail-open)")
        if edited_code and not verification_seen:
            _log("BLOCK code edited with no verification evidence after the last edit")
            # json.dumps keeps ensure_ascii=True (default): stdout stays pure
            # ASCII, so a legacy-codepage console (e.g. Windows cp950) cannot
            # crash the print and silently kill the gate — the exact upstream
            # incident (Miguok ebb9621). Do not "fix" this to ensure_ascii=False.
            print(json.dumps({"decision": "block", "reason": BLOCK_REASON},
                             ensure_ascii=True))
        return 0
    except Exception:
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        return 0


if __name__ == "__main__":
    sys.exit(main())
