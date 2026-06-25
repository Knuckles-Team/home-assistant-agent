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

_Auto-generated from the live MCP server — do not edit by hand._

<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `home_assistant_calendar` | `CALENDARTOOL` | Manage home assistant calendar operations. |
| `home_assistant_config` | `CONFIGTOOL` | Manage home assistant config operations. |
| `home_assistant_entities` | `ENTITIESTOOL` | Manage home assistant entities operations. |
| `home_assistant_events` | `EVENTSTOOL` | Manage home assistant events operations. |
| `home_assistant_history` | `HISTORYTOOL` | Manage home assistant history operations. |
| `home_assistant_logbook` | `LOGBOOKTOOL` | Manage home assistant logbook operations. |
| `home_assistant_panels` | `PANELSTOOL` | Manage home assistant panels operations. |
| `home_assistant_services` | `SERVICESTOOL` | Manage home assistant services operations. |
| `home_assistant_states` | `STATESTOOL` | Manage home assistant states operations. |
| `home_assistant_system` | `SYSTEMTOOL` | Manage home assistant system operations. |
| `home_assistant_voice` | `VOICETOOL` | Manage home assistant voice operations. |

_11 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

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

> **Install the slim `[mcp]` extra.** All examples below install
> `home-assistant-agent[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "home-assistant-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "home-assistant-agent[mcp]",
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
        "home-assistant-agent[mcp]",
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
  knucklessg1/home-assistant-agent:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `home-assistant-agent[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `home-assistant-agent[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `home-assistant-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

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
    image: knucklessg1/home-assistant-agent:mcp
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

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOME_ASSISTANT_URL` | `http://localhost:8123` | 1. HOME_ASSISTANT_URL: The base URL of your Home Assistant instance. |
| `HOME_ASSISTANT_TOKEN` | `your_long_lived_access_token_here` | 2. HOME_ASSISTANT_TOKEN: Long-Lived Access Token generated from Home Assistant profile. |
| `HOME_ASSISTANT_AGENT_VERIFY` | `True` | 3. HOME_ASSISTANT_AGENT_VERIFY: Toggle SSL certificate verification (True/False). |
| `DEFAULT_AGENT_NAME` | `HomeAssistantAgent` | 4. DEFAULT_AGENT_NAME: The default name/display identifier for this agent. |
| `AGENT_DESCRIPTION` | `Expert assistant for interacting with and managing Home Assistant smart home devices.` | 5. AGENT_DESCRIPTION: Brief description of the agent's responsibilities. |
| `AGENT_SYSTEM_PROMPT` | `You are a helpful, secure home automation AI assistant. You can control home assistant lights, switches, media players, calendars, and query historical data.` | 6. AGENT_SYSTEM_PROMPT: Core system prompt directing the agent's behavior and traits. |
| `CONFIGTOOL` | `True` | 7. CONFIGTOOL: Enable config management tool. |
| `STATESTOOL` | `True` | 8. STATESTOOL: Enable state inspection and modification tool. |
| `SERVICESTOOL` | `True` | 9. SERVICESTOOL: Enable service call tool. |
| `EVENTSTOOL` | `True` | 10. EVENTSTOOL: Enable event monitoring and subscription tool. |
| `HISTORYTOOL` | `True` | 11. HISTORYTOOL: Enable historical state query tool. |
| `LOGBOOKTOOL` | `True` | 12. LOGBOOKTOOL: Enable logbook and error log query tool. |
| `CALENDARTOOL` | `True` | 13. CALENDARTOOL: Enable calendar schedule querying tool. |
| `PANELSTOOL` | `True` | 14. PANELSTOOL: Enable HA custom panels list tool. |
| `VOICETOOL` | `True` | 15. VOICETOOL: Enable voice entity exposition and settings tool. |
| `ENTITIESTOOL` | `True` | 16. ENTITIESTOOL: Enable entity registry lookup and display tool. |
| `SYSTEMTOOL` | `True` | 17. SYSTEMTOOL: Enable templates, intents, and system health tools. |
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | Options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `EUNOMIA_TYPE` | `none` | Options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `EUNOMIA_REMOTE_URL` | — | Remote Eunomia authorization server URL |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | — | OTLP collector endpoint |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `DEBUG` | `False` | Verbose logging |
| `PYTHONUNBUFFERED` | `1` | Unbuffered stdout (recommended in containers) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_23 package + 16 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


Every variable the server reads, grouped by purpose.

### Connection & Credentials (Home Assistant)
| Variable | Description | Default |
|----------|-------------|---------|
| `HOME_ASSISTANT_URL` | Base URL of the Home Assistant instance | `http://localhost:8123` |
| `HOME_ASSISTANT_TOKEN` | Long-Lived Access Token generated in Home Assistant | — |
| `HOME_ASSISTANT_AGENT_VERIFY` | Toggle SSL certificate verification (`True`/`False`) | `True` |

### MCP server / transport
| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |
| `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS` | Comma-separated tool allow/deny list | — |
| `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS` | Comma-separated tag allow/deny list | — |
| `PYTHONUNBUFFERED` | Unbuffered stdout (recommended in containers) | `1` |

### Agent runtime (full `[agent]` runtime only)
| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_AGENT_NAME` | Default name/display identifier for the agent | `HomeAssistantAgent` |
| `AGENT_DESCRIPTION` | Description of the agent's smart home duties | built-in |
| `AGENT_SYSTEM_PROMPT` | Core Pydantic AI system prompt | built-in |
| `MCP_URL` | URL of the MCP server the agent connects to | `http://localhost:8000/mcp` |
| `PROVIDER` | LLM provider (e.g. `openai`) | `openai` |
| `MODEL_ID` | Model id (e.g. `gpt-4o`) | `gpt-4o` |
| `ENABLE_WEB_UI` | Serve the AG-UI web interface | `True` |

### Telemetry & governance
| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry export | `True` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | — |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` / `OTEL_EXPORTER_OTLP_SECRET_KEY` | OTLP auth keys | — |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP protocol (e.g. `http/protobuf`) | — |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

### Tool toggles
Each action-routed tool can be disabled individually via its toggle env var (set to `false`):
`CONFIGTOOL`, `STATESTOOL`, `SERVICESTOOL`, `EVENTSTOOL`, `HISTORYTOOL`, `LOGBOOKTOOL`,
`CALENDARTOOL`, `PANELSTOOL`, `VOICETOOL`, `ENTITIESTOOL`, `SYSTEMTOOL`. The full list is in
the [Available MCP Tools](#available-mcp-tools) table above.

See [`.env.example`](.env.example) for a copy-paste starting point.

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

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `home-assistant-agent[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `home-assistant-agent[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `home-assistant-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "home-assistant-agent[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "home-assistant-agent[agent]"

# Everything (development)
uv pip install "home-assistant-agent[all]"      # or: python -m pip install "home-assistant-agent[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/home-assistant-agent:mcp` | `--target mcp` | `home-assistant-agent[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `home-assistant-mcp` |
| `knucklessg1/home-assistant-agent:latest` | `--target agent` (default) | `home-assistant-agent[agent]` — **full** agent runtime + epistemic-graph engine | `home-assistant-agent` |

```bash
docker build --target mcp   -t knucklessg1/home-assistant-agent:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/home-assistant-agent:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

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


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `home-assistant-agent` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx home-assistant-mcp` · or `uv tool install home-assistant-agent` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/home-assistant-agent:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
