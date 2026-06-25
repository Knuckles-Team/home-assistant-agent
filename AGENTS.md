# AGENTS.md

> Claude Code loads this file via `CLAUDE.md` (`@AGENTS.md` import) — the two stay
> in sync. Edit **this** file, not `CLAUDE.md`.

## Tech Stack & Architecture
- Language/Version: Python 3.10+
- Core Libraries: `agent-utilities`, `fastmcp`, `pydantic-ai`
- Key principles: Functional patterns, Pydantic for data validation, asynchronous tool execution.
- Architecture:
    - `mcp_server.py`: Main MCP server entry point and tool registration.
    - `agent_server.py`: Pydantic AI agent server and run configuration.
    - `auth.py`: Authentication client singleton.
    - `api/`: Multi-protocol client backend (REST and WebSocket APIs).

### Architecture Diagram
```mermaid
graph TD
    User([User/A2A]) --> Server[A2A Server / FastAPI]
    Server --> Agent[Pydantic AI Agent]
    Agent --> MCP[MCP Server / FastMCP]
    MCP --> Client[API Client / Wrapper]
    Client --> ExternalAPI(["Home Assistant REST and WebSocket API"])
```

### Workflow Diagram
```mermaid
sequenceDiagram
    participant U as User
    participant S as Server
    participant A as Agent
    participant T as MCP Tool
    participant API as Home Assistant API

    U->>S: Request
    S->>A: Process Query
    A->>T: Invoke Tool
    T->>API: REST or WebSocket Call
    API-->>T: JSON / Event Response
    T-->>A: Tool Result
    A-->>S: Final Response
    S-->>U: Output
```

## Commands (run these exactly)
# Installation
```bash
pip install .[all]
```

# Quality & Linting (run from project root)
```bash
uv run ruff check .
uv run ruff format --check .
```

# Execution Commands
# Run MCP Server
```bash
home-assistant-mcp
```
# Run Agent
```bash
home-assistant-agent
```

## Project Structure Quick Reference
- MCP Entry Point → `home_assistant_agent/mcp_server.py`
- Agent Entry Point → `home_assistant_agent/agent_server.py`
- Source Code → `home_assistant_agent/`

### File Tree
```text
├── .bumpversion.cfg
├── .dockerignore
├── .env.example
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── AGENTS.md
├── CHANGELOG.md
├── Dockerfile
├── LICENSE
├── MANIFEST.in
├── README.md
├── compose.yml
├── debug.Dockerfile
├── home_assistant_agent/
│   ├── __init__.py
│   ├── __main__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api_client_base.py
│   │   ├── api_client_rest.py
│   │   └── api_client_websocket.py
│   ├── agent_server.py
│   ├── api_client.py
│   ├── auth.py
│   ├── home_assistant_models.py
│   ├── main_agent.json
│   ├── mcp_config.json
│   └── mcp_server.py
├── pyproject.toml
├── requirements.txt
└── tests/
    ├── conftest.py
    ├── pytest.ini
    ├── test_concept_parity.py
    ├── test_coverage.py
    ├── test_init.py
    └── test_startup.py
```

## Concept Registry & Traceability

This repository aligns perfectly with the standard `agent-utilities` architecture pillars:

### `CONCEPT:ECO-4.0` — Tool Interface & MCP Factory
Defines all 11 action-routed MCP tools: Config, States, Services, Events, History, Logbook, Calendar, Panels, Voice, Entities, and System.
- **Source Files:**
  - [mcp_server.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/home_assistant_agent/mcp_server.py)
  - [api_client_rest.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/home_assistant_agent/api/api_client_rest.py)
  - [api_client_websocket.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/home_assistant_agent/api/api_client_websocket.py)
- **Tests:**
  - [test_coverage.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/tests/test_coverage.py#L285-L670)

### `CONCEPT:OS-5.0` — Operating System and Agents
Directs the lazy loader, entry points, and CLI runtime interface.
- **Source Files:**
  - [__init__.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/home_assistant_agent/__init__.py)
  - [__main__.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/home_assistant_agent/__main__.py)
  - [agent_server.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/home_assistant_agent/agent_server.py)
- **Tests:**
  - [test_init.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/tests/test_init.py)
  - [test_startup.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/tests/test_startup.py)
  - [test_coverage.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/tests/test_coverage.py#L209-L229)

### `CONCEPT:OS-5.1` — Security & Auth
Credentials and authentication client setup.
- **Source Files:**
  - [auth.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/home_assistant_agent/auth.py)
  - [api_client_base.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/home_assistant_agent/api/api_client_base.py)
- **Tests:**
  - [test_coverage.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/tests/test_coverage.py#L230-L263)

### `CONCEPT:ORCH-1.5` — Orchestration Workflows/Agents
Pydantic AI Graph Agent configuration.
- **Source Files:**
  - [agent_server.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/home_assistant_agent/agent_server.py)
- **Tests:**
  - [test_coverage.py](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/tests/test_coverage.py#L264-L284)

## Code Style & Conventions
**Always:**
- Use `agent-utilities` for common patterns (e.g., `create_mcp_server`, `create_agent_server`).
- Define input/output models using Pydantic.
- Include descriptive docstrings for all tools (they are used as tool descriptions for LLMs).
- Check for optional dependencies using `try/except ImportError`.

## Dos and Don'ts
**Do:**
- Run lint/test via `uv run ruff check .` and `pytest`.
- Use existing patterns from `agent-utilities`.
- Keep tools focused and idempotent where possible.

**Don't:**
- Use `cd` commands in scripts; use absolute paths or relative to project root.
- Add new dependencies to `dependencies` in `pyproject.toml` without checking `optional-dependencies` first.
- Hardcode secrets; use environment variables or `.env` files.

## Safety & Boundaries
**Always do:**
- Run lint/test via `pre-commit`.
- Use `agent-utilities` base classes.

**Ask first:**
- Major refactors of `mcp_server.py` or `agent_server.py`.
- Deleting or renaming public tool functions.

**Never do:**
- Commit `.env` files or secrets.
- Modify `agent-utilities` or `universal-skills` files from within this package.

## When Stuck
- Propose a plan first before making large changes.
- Check `agent-utilities` documentation for existing helpers.

## ⛔ No Scratch or Temporary Files in Repository

**NEVER write any of the following to this repository:**
- Temporary test scripts (`test_*.py`, `debug_*.py` outside of `tests/`)
- Scratch scripts or experimental one-off files
- Log files (`.log`, `.txt` command output)
- Random text files with command output or debug dumps
- Any file that is NOT production source code, tests in `tests/`, or documentation

**Why:** These files expose private filesystem paths, credentials, and internal infrastructure details when pushed to GitHub publicly.

**Where to put scratch work instead:**
- Use `~/workspace/scratch/` for temporary scripts and experiments
- Use `~/workspace/reports/` for command output and reports
- Keep test scripts in the `tests/` directory following proper pytest conventions

## ⛔ Keep the Repository Root Pristine — No Scratch / Temp / Debug Files

**The repository ROOT must contain only canonical project files** (packaging,
config, docs, lockfiles). The only hidden directories allowed at root are
`.git/`, `.github/`, and `.specify/` (plus a local, git-ignored `.venv/`).

**NEVER write any of the following — anywhere in the repo, and ESPECIALLY at the root:**
- One-off / debug / migration scripts: `fix_*.py`, `migrate_*.py`, `refactor_*.py`,
  `replace_*.py`, `update_*.py`, `debug_*.py`, or `test_*.py` **at the root**
  (real tests live in `tests/` only).
- Databases / data dumps: `*.db`, `*.db-wal`, `*.sqlite*`, `*.corrupted`.
- Logs / command output: `*.log`, scratch `*.txt`, `*.orig`, `*.rej`, `*.bak`.
- Build artifacts: `*.tsbuildinfo`, compiled binaries, coverage files.
- AI agent scratch directories: `.agent/`, `.agents/`, `.agent_data/`, `.tmp/`,
  `.hypothesis/`, or any per-tool cache committed to git.
- Any file that is NOT production source, a test in `tests/`, documentation, or
  a recognized config/lockfile.

**Why:** scratch at the root leaks private paths/credentials, bloats the tree,
and erodes a pristine codebase.

**Where scratch goes instead:** `~/workspace/scratch/` (experiments),
`~/workspace/reports/` (command output); tests go in `tests/` (pytest).
Before finishing a task, run `git status` and confirm no stray root files were added.

## Working Discipline — think, simplify, stay surgical, verify

These four habits cut the most common LLM coding mistakes. For trivial tasks, use
judgment; the bias here is correctness over speed.

- **Think before coding.** State your assumptions explicitly. If a request has more than
  one reasonable reading, surface the options instead of silently picking one. If a
  simpler approach exists, say so and push back when warranted. When something is
  genuinely unclear, stop and name what's confusing — ask, don't guess.
- **Simplicity first.** Write the minimum code that solves the stated problem — no
  speculative features, no abstraction for single-use code, no configurability that
  wasn't requested, no error handling for impossible states. If you wrote 200 lines and
  it could be 50, rewrite it. (Name code from its purpose, never `wave0`/`phase2`/`v2`.)
- **Stay surgical.** Every changed line should trace directly to the task. Don't refactor,
  reformat, or "improve" working code adjacent to your change; match the existing style
  even where you'd do it differently. Remove only the imports/symbols your own change
  orphaned; if you spot unrelated dead code, mention it rather than deleting it inline.
  *Exception — the Quality Bar below:* lint/format/type errors the pre-commit gate flags
  get fixed regardless of who introduced them. In short: **surgical on behavior, clean on
  lint.**
- **Verify against a goal.** Turn the task into a checkable outcome before you start:
  "fix the bug" → "write a failing test that reproduces it, then make it pass"; "add
  validation" → "tests for the invalid inputs pass". For multi-step work, state the short
  plan and the check for each step, then loop until the checks pass.

## Quality Bar — Leave the Codebase Clean (REQUIRED)

After completing any code change, run the project's pre-commit suite and drive it
**fully green** before committing:

```bash
pre-commit run --all-files
```

Resolve **every** issue it reports — failures, lint errors, type errors, and
warnings — **including problems that pre-date your change and were not caused by
your edits**. The standing goal is a clean, working codebase with **no errors and
no warnings**. Do not silence checks (`# noqa`, `# type: ignore`, `SKIP=`,
`--no-verify`) to force green unless the exception is already documented in this
file as a known, unavoidable limitation. Only commit once `pre-commit run
--all-files` passes cleanly; if a check legitimately cannot pass, stop and explain
why rather than bypassing it.

## Working with Git Worktrees (multi-session)

Multiple agents/sessions work the `agent-packages/*` repos concurrently. **Do not
edit the canonical checkout** (`/home/apps/workspace/agent-packages/<repo>`) — a
background `repository-manager` sync can reset its working tree and discard
uncommitted edits. Take your own git worktree on your own branch instead:

```bash
# preferred — repository-manager MCP:
rm_worktree add <repo> <your-branch>      # -> /home/apps/worktrees/<repo>/<your-branch>

# raw-git fallback:
git -C agent-packages/<repo> checkout main
git -C agent-packages/<repo> worktree add /home/apps/worktrees/<repo>/<branch> -b <branch>
```

Work in the worktree and **commit often** (commits survive a working-tree reset).
Each session must use a **distinct branch** — git allows a branch in only one
worktree, which is what keeps concurrent sessions from colliding. Worktrees live
under `/home/apps/worktrees/` (outside the workspace scan, so the sync leaves them
alone).

**Finishing work in a worktree** — run this sequence before calling it done:
1. **Pre-commit green** — `pre-commit run --all-files`; resolve every issue per the
   Quality Bar above (including pre-existing), no `--no-verify`.
2. **Commit** in the worktree.
3. **Merge to main locally** — `rm_worktree merge <repo> <branch> --into main`
   (or `git merge --no-ff`). Push only when the user asks.
4. **Clean up** — remove the worktree and delete the merged branch:
   `rm_worktree remove <repo> <branch> --delete-branch`; `rm_worktree prune` clears
   stale entries. (Raw-git: `git worktree remove <path> && git branch -d <branch>`.)

<!-- BEGIN concept-coordination (generated) -->
## Concept-ID Coordination (multi-session)

Working in parallel with other sessions/worktrees? **Reserve a concept id before you write its `CONCEPT:` marker** so two sessions never collide:

```bash
agent-utilities --json concept reserve --ns KG-2   # or a package prefix, e.g. KEY
```

Full protocol (ledger, merge=union, reconcile, MCP/REST): <https://knuckles-team.github.io/agent-utilities/concept_coordination/>
<!-- END concept-coordination (generated) -->
