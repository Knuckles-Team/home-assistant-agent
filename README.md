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

*Version: 0.13.0*

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

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Config** | `CONFIGTOOL` | `True` | Manage home assistant config operations. Action-routed methods: `status`, `config`, `components`, `check_config`. |
| **States** | `STATESTOOL` | `True` | Manage home assistant states operations. Action-routed methods: `list_states`, `get_state`, `update_state`, `delete_state`. |
| **Services** | `SERVICESTOOL` | `True` | Manage home assistant services operations. Action-routed methods: `list_services`, `call_service`. |
| **Events** | `EVENTSTOOL` | `True` | Manage home assistant events operations. Action-routed methods: `list_events`, `fire_event`, `subscribe_events`. |
| **History** | `HISTORYTOOL` | `True` | Manage home assistant history operations. Action-routed methods: `get_history`. |
| **Logbook** | `LOGBOOKTOOL` | `True` | Manage home assistant logbook operations. Action-routed methods: `get_logbook`, `get_error_log`. |
| **Calendar** | `CALENDARTOOL` | `True` | Manage home assistant calendar operations. Action-routed methods: `list_calendars`, `get_calendar_events`. |
| **Panels** | `PANELSTOOL` | `True` | Manage home assistant panels operations. Action-routed methods: `get_panels`. |
| **Voice** | `VOICETOOL` | `True` | Manage home assistant voice operations. Action-routed methods: `list_exposed_entities`, `expose_entities`. |
| **Entities** | `ENTITIESTOOL` | `True` | Manage home assistant entities operations. Action-routed methods: `get_entity_registry_display`, `extract_from_target`, `get_triggers_for_target`, `get_conditions_for_target`, `get_services_for_target`. |
| **System** | `SYSTEMTOOL` | `True` | Manage home assistant system operations. Action-routed methods: `render_template`, `ping`, `handle_intent`, `validate_config`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/docs/mcp.md).

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
        "HASS_HOST": "your_hass_host_here",
        "HASS_USERNAME": "your_hass_username_here",
        "HASS_PASSWORD": "your_hass_password_here",
        "HASS_TOKEN": "your_hass_token_here"
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
        "HASS_HOST": "your_hass_host_here",
        "HASS_USERNAME": "your_hass_username_here",
        "HASS_PASSWORD": "your_hass_password_here",
        "HASS_TOKEN": "your_hass_token_here"
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
  -e HASS_HOST="your_value" \
  -e HASS_USERNAME="your_value" \
  -e HASS_PASSWORD="your_value" \
  -e HASS_TOKEN="your_value" \
  knucklessg1/home-assistant-agent:latest
```

---

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export HASS_HOST="your_value"
export HASS_USERNAME="your_value"
export HASS_PASSWORD="your_value"
export HASS_TOKEN="your_value"

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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](file:///home/apps/workspace/agent-packages/agents/home-assistant-agent/docs/agent.md).

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
