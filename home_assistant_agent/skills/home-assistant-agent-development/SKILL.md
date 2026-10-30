---
name: home-assistant-agent-development
domain: development
skill_type: skill
description: >-
  Develop, test, gate, and release the home-assistant-agent connector. Use this
  skill when changing Home Assistant REST or WebSocket mappings, governed MCP
  tools, knowledge-graph ingestion, packaged connector content, documentation,
  or repository gates.
license: MIT
tags: [home-assistant, development, connector, mcp, test, gates]
tier: repository
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# home-assistant-agent development

This repository owns the Home Assistant REST and WebSocket API clients, their
Pydantic models, action-routed MCP tools, source declarations and knowledge-graph
ingestion mappings, and packaged connector content. Shared connector contracts,
transports, TLS profiles, and credential helpers belong to
`scion-sdk`; admission, serving, and durable graph state belong to
their owning repositories. Read `AGENTS.md` before changing code and keep
credentials, private endpoints, entity data, and customer records out of source,
logs, fixtures, and skill content.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the
owning spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend the
  existing spec before adding requirement text. `PIPE-CONNSPEC-R128.4` is a
  central pipelines criterion; do not invent a local status row for it.
- Reuse the one `Connector` in `home_assistant_agent/__init__.py`, the unified
  `HomeAssistantApi` facade in `home_assistant_agent/api/__init__.py`, and the
  shared `BaseApiClient` in `home_assistant_agent/api/api_client_base.py`. Do
  not create a second API, MCP, authentication, or transport plane.
- Preserve the `HOME_ASSISTANT_URL` and `HOME_ASSISTANT_TOKEN` settings in
  `home_assistant_agent/auth.py`, the SDK TLS resolver used by
  `BaseApiClient`, and the REST/WebSocket split in
  `home_assistant_agent/api/api_client_rest.py` and
  `home_assistant_agent/api/api_client_websocket.py`. Never hardcode a secret,
  endpoint, or TLS-verification bypass.
- Keep the action-routed registrations in `home_assistant_agent/mcp_server.py`
  aligned with the SDK dynamic surface. Preserve the source declarations in
  `home_assistant_agent/connector_sources.py` and the typed mappings in
  `home_assistant_agent/kg_ingest.py`; keep tenant and installation data
  neutral.
- Every delivered requirement needs a bound focused test. Generated
  `specs/*/status.json` files come from the shared hooks; never hand-edit them.
- Keep `home_assistant_agent/skills/`, `home_assistant_agent/ontology/`,
  prompts, `mcp_config.json`, and source declarations coherent with the existing
  package-data and `home-assistant-mcp` entry point. One logical change per
  commit, with the central criterion recorded using the repository's documented
  `Spec: none (<reason>)` form when no local requirements row exists, plus the
  assisting-agent trailer.

## Setup and gates

Use the pinned environment from `uv sync --locked`, then run the shared gates:

```bash
uv sync --locked
uvx pre-commit run --all-files
uvx pre-commit run --all-files --hook-stage pre-push
```

For focused feedback, run the smallest affected test with the locked
environment:

```bash
uv run --locked --extra test pytest -q tests/test_home_assistant_development_skill.py
```

The canonical `.pre-commit-config.yaml` delegates connector-standard, secrets,
spec, tests-fast, and dependency-readiness checks to
`Knuckles-Team/pipelines` at `rev: main`. Do not copy those hooks locally or
bypass a failing check.

## Connector-specific checks

- Keep the REST client methods and WebSocket command methods behind the single
  `HomeAssistantApi` facade. Validate response models and translate provider
  failures through the existing SDK and client boundaries.
- Preserve SDK TLS resolution and bearer-token handling. Mock Home Assistant
  HTTP/WebSocket responses in local tests; never call a live instance or use
  live credentials in a gate.
- Keep the `home_assistant_agent/skills/`, `home_assistant_agent/ontology/`,
  `home_assistant_agent/connectors/` (when present), prompts, and
  `mcp_config.json` files in package data. Keep the source declarations and
  ontology mappings explicit and installation-neutral.
- Documentation is published by `.github/workflows/pages.yml`, which calls
  `pages_pipeline.yml@main`. The Python release and rendered connector image
  are called by `.github/workflows/pipeline.yml`; do not add a second publisher
  or commit generated Docker artifacts.

## Packaging and publication

`pyproject.toml` declares
`home-assistant-mcp = "home_assistant_agent:connector"` and packages
`skills/**`, prompts, ontology, connector content, and `mcp_config.json`. For a
genuine packaged-content release, keep the project version, `CHANGELOG.md`, and
the editable `home-assistant-agent` entry in `uv.lock` coherent, then inspect
`uv build` output for
`home_assistant_agent/skills/home-assistant-agent-development/SKILL.md`.

The canonical release caller is `.github/workflows/pipeline.yml`: it publishes
the Python connector with `python_pipeline.yml@main`, then builds the rendered
connector container with `container_pipeline.yml@main` and
`render_connector: true`. Do not claim package, container, or Pages publication
from a local build; require exact-source hosted evidence and the public artifact.

## Delivery discipline

Work in a real Git worktree based on `origin/main`. Inspect the complete diff,
stage only reviewed paths, and verify `git status --short` after every gate.
Do not use `git stash`, `git add -A`, or `git add .`; preserve unrelated working
tree changes. Keep runtime, ontology, source status, and generated artifacts
outside a bounded skill slice unless the owning requirement explicitly requires
them.
