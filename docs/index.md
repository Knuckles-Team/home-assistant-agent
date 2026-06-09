# home-assistant-agent

Home Assistant **REST + WebSocket API, MCP Server, and A2A Agent** for the
agent-utilities ecosystem — control lights, switches, media players, calendars,
and query historical state across your smart home.

!!! info "Official documentation"
    This site is the canonical reference for `home-assistant-agent`, maintained
    alongside every release.

[![PyPI](https://img.shields.io/pypi/v/home-assistant-agent)](https://pypi.org/project/home-assistant-agent/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/home-assistant-agent)](https://github.com/Knuckles-Team/home-assistant-agent/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/home-assistant-agent)

## Overview

`home-assistant-agent` wraps the Home Assistant REST and WebSocket API surface with
typed, deterministic MCP tools and an optional Pydantic-AI agent server. It provides:

- **`HomeAssistantApi`** — a unified REST + WebSocket client over the Home Assistant
  API (configuration, states, services, events, history, logbook, calendars, and
  system health).
- **Action-routed MCP tools** across eleven domains — Config, States, Services,
  Events, History, Logbook, Calendar, Panels, Voice, Entities, and System — each
  toggled independently by environment flag.
- **An optional A2A agent server** (`home-assistant-agent`) that wires the same tool
  surface into a Pydantic-AI graph agent with an embedded web UI.

Every tool registration is governed by an environment flag, so the server exposes
only the capabilities you enable and remains inactive when credentials are absent.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP server, the agent server, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `HomeAssistantApi` client, and the CLI.
- :material-home-assistant: **[Backing Platform](platform.md)** — deploy Home Assistant with Docker.
- :material-sitemap: **[Overview](overview.md)** — architecture, tool surface, and ecosystem role.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:HASS-*` registry.

</div>

## Quick start

```bash
pip install "home-assistant-agent"
home-assistant-mcp                 # stdio MCP server (default transport)
```

Connect it to a Home Assistant instance:

```bash
export HOME_ASSISTANT_URL=http://your-home-assistant:8123
export HOME_ASSISTANT_TOKEN=your_long_lived_access_token
home-assistant-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI extras, Docker image, all transports, the agent server, reverse
proxy, DNS).
