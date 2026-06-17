# Home Assistant Agent
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/home-assistant-agent)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/home-assistant-agent)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/home-assistant-agent)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/home-assistant-agent)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/home-assistant-agent)
![PyPI - License](https://img.shields.io/pypi/l/home-assistant-agent)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/home-assistant-agent)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/home-assistant-agent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/home-assistant-agent)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/home-assistant-agent)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/home-assistant-agent)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/home-assistant-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/home-assistant-agent)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/home-assistant-agent)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/home-assistant-agent)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/home-assistant-agent)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/home-assistant-agent)

*Version: 0.34.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, the optional A2A agent server, and guidance for provisioning the Home
> Assistant platform are maintained in the
> [official documentation](https://knuckles-team.github.io/home-assistant-agent/).

---

## Overview

**Home Assistant Agent** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Agent for interacting with Home Assistant REST API.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Agent for interacting with Home Assistant REST API API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Config** | `CONFIG_TOOL` | `True` | Register config tools. CONCEPT:ECO-4.0 Action-routed methods: `check_config`, `components`, `config`, `status`. |
| **States** | `STATES_TOOL` | `True` | Register states tools. CONCEPT:ECO-4.0 Action-routed methods: `delete_state`, `get_state`, `list_states`, `update_state`. |
| **Services** | `SERVICES_TOOL` | `True` | Register services tools. CONCEPT:ECO-4.0 Action-routed methods: `call_service`, `list_services`. |
| **Events** | `EVENTS_TOOL` | `True` | Register events tools. CONCEPT:ECO-4.0 Action-routed methods: `fire_event`, `list_events`, `subscribe_events`. |
| **History** | `HISTORY_TOOL` | `True` | Register history tools. CONCEPT:ECO-4.0 Action-routed methods: `get_history`. |
| **Logbook** | `LOGBOOK_TOOL` | `True` | Register logbook tools. CONCEPT:ECO-4.0 Action-routed methods: `get_error_log`, `get_logbook`. |
| **Calendar** | `CALENDAR_TOOL` | `True` | Register calendar tools. CONCEPT:ECO-4.0 Action-routed methods: `get_calendar_events`, `list_calendars`. |
| **Panels** | `PANELS_TOOL` | `True` | Register panels tools. CONCEPT:ECO-4.0 Action-routed methods: `get_panels`. |
| **Voice** | `VOICE_TOOL` | `True` | Register voice tools. CONCEPT:ECO-4.0 Action-routed methods: `expose_entities`, `list_exposed_entities`. |
| **Entities** | `ENTITIES_TOOL` | `True` | Register entities tools. CONCEPT:ECO-4.0 Action-routed methods: `extract_from_target`, `get_conditions_for_target`, `get_entity_registry_display`, `get_services_for_target`, `get_triggers_for_target`. |
| **System** | `SYSTEM_TOOL` | `True` | Register system tools. CONCEPT:ECO-4.0 Action-routed methods: `handle_intent`, `ping`, `render_template`, `validate_config`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](docs/mcp.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "home-assistant-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "home-assistant-agent",
        "home-assistant-mcp"
      ],
      "env": {
        "HOME_ASSISTANT_URL": "http://localhost:8123",
        "HOME_ASSISTANT_TOKEN": "your_long_lived_token_here",
        "HOME_ASSISTANT_AGENT_VERIFY": "True"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "home-assistant-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "home-assistant-agent",
        "home-assistant-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "HOME_ASSISTANT_URL": "http://localhost:8123",
        "HOME_ASSISTANT_TOKEN": "your_long_lived_token_here",
        "HOME_ASSISTANT_AGENT_VERIFY": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "home-assistant-agent": {
      "url": "http://localhost:8000/home-assistant-agent/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name home-assistant-agent-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e HOME_ASSISTANT_URL="http://localhost:8123" \
  -e HOME_ASSISTANT_TOKEN="your_token_here" \
  -e HOME_ASSISTANT_AGENT_VERIFY="True" \
  knucklessg1/home-assistant-agent:latest
```

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`home-assistant-agent` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/home-assistant-agent/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://home-assistant-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export HOME_ASSISTANT_URL="http://localhost:8123"
export HOME_ASSISTANT_TOKEN="your_token_here"
export HOME_ASSISTANT_AGENT_VERIFY="True"

# Run the agent server
home-assistant-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  home-assistant-agent-mcp:
    image: knucklessg1/home-assistant-agent:latest
    container_name: home-assistant-agent-mcp
    hostname: home-assistant-agent-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  home-assistant-agent-agent:
    image: knucklessg1/home-assistant-agent:latest
    container_name: home-assistant-agent-agent
    hostname: home-assistant-agent-agent
    restart: always
    depends_on:
      - home-assistant-agent-mcp
    env_file:
      - ../.env
    command: [ "home-assistant-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://home-assistant-agent-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9004:9004"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9004/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](docs/agent.md).

---

## Configuration & Environment Variables

The Home Assistant Agent supports **17 environment variables** to fine-tune the client wrapper, agent configuration, and modular tools toggles.

| # | Environment Variable | Default | Description |
|---|----------------------|---------|-------------|
| 1 | `HOME_ASSISTANT_URL` | `http://localhost:8123` | Base URL of the Home Assistant instance |
| 2 | `HOME_ASSISTANT_TOKEN` | *None* | Long-Lived Access Token generated in Home Assistant |
| 3 | `HOME_ASSISTANT_AGENT_VERIFY` | `True` | Toggle SSL certificate verification (True/False) |
| 4 | `DEFAULT_AGENT_NAME` | `HomeAssistantAgent` | Default name/display identifier for the agent |
| 5 | `AGENT_DESCRIPTION` | *Multi-line* | Description of the agent's smart home duties |
| 6 | `AGENT_SYSTEM_PROMPT` | *Multi-line* | Core Pydantic AI system prompt for agent instructions |
| 7 | `CONFIGTOOL` | `True` | Toggle Config management tool (`True`/`False`) |
| 8 | `STATESTOOL` | `True` | Toggle State inspection tool (`True`/`False`) |
| 9 | `SERVICESTOOL` | `True` | Toggle Service execution tool (`True`/`False`) |
| 10 | `EVENTSTOOL` | `True` | Toggle Event monitoring tool (`True`/`False`) |
| 11 | `HISTORYTOOL` | `True` | Toggle State history tool (`True`/`False`) |
| 12 | `LOGBOOKTOOL` | `True` | Toggle Logbook & error log tool (`True`/`False`) |
| 13 | `CALENDARTOOL` | `True` | Toggle Calendar scheduling tool (`True`/`False`) |
| 14 | `PANELSTOOL` | `True` | Toggle HA custom panels tool (`True`/`False`) |
| 15 | `VOICETOOL` | `True` | Toggle Voice & entity exposition tool (`True`/`False`) |
| 16 | `ENTITIESTOOL` | `True` | Toggle Entity registry lookup tool (`True`/`False`) |
| 17 | `SYSTEMTOOL` | `True` | Toggle Template & health systems tool (`True`/`False`) |

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install home-assistant-agent[all]

# Using standard pip
python -m pip install home-assistant-agent[all]
```

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/home-assistant-agent/)
and is the recommended reference for installation, deployment, and day-to-day
operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/home-assistant-agent/installation/) | pip, source, extras, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/home-assistant-agent/deployment/) | run the MCP server, the agent server, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/home-assistant-agent/usage/) | the MCP tools, the `HomeAssistantApi` client, the CLI |
| [Backing Platform](https://knuckles-team.github.io/home-assistant-agent/platform/) | deploy Home Assistant with Docker |
| [Overview](https://knuckles-team.github.io/home-assistant-agent/overview/) | architecture, tool surface, ecosystem role |
| [Concepts](https://knuckles-team.github.io/home-assistant-agent/concepts/) | concept registry (`CONCEPT:HASS-*`) |

`AGENTS.md` is the canonical contributor/agent guidance.

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`
