# Home Assistant Agent
## CLI or API | MCP

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

*Version: 2.3.3*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> Assistant platform are maintained in the
> [official documentation](https://knuckles-team.github.io/home-assistant-agent/).

---

## Overview

**Home Assistant Agent** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Agent for interacting with Home Assistant REST API.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Complete support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Agent for interacting with Home Assistant REST API API. The operator can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server use dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

_Auto-generated from the live MCP server — do not edit by hand._

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (`MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `home_assistant_calendar` | `CALENDARTOOL` | Manage home assistant calendar operations. |
| `home_assistant_entities` | `ENTITIESTOOL` | Manage home assistant entities operations. |
| `home_assistant_events` | `EVENTSTOOL` | Manage home assistant events operations. |
| `home_assistant_history` | `HISTORYTOOL` | Manage home assistant history operations. |
| `home_assistant_logbook` | `LOGBOOKTOOL` | Manage home assistant logbook operations. |
| `home_assistant_panels` | `PANELSTOOL` | Manage home assistant panels operations. |
| `home_assistant_services` | `SERVICESTOOL` | Manage home assistant services operations. |
| `home_assistant_states` | `STATESTOOL` | Manage home assistant states operations. |
| `home_assistant_system` | `SYSTEMTOOL` | Manage home assistant system operations. |
| `home_assistant_voice` | `VOICETOOL` | Manage home assistant voice operations. |
| `home_ingest_history` | `KGTOOL` | Ingest a Home Assistant history series for one entity as timeseries readings. |
| `home_ingest_states` | `KGTOOL` | Ingest all Home Assistant entity states into epistemic-graph. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>41 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `home_assistant_call_service` | `APITOOL` | Invoke the call_service operation. |
| `home_assistant_check_config` | `APITOOL` | Invoke the check_config operation. |
| `home_assistant_components` | `APITOOL` | Invoke the components operation. |
| `home_assistant_config` | `CONFIGTOOL` | Invoke the config operation. |
| `home_assistant_delete_state` | `APITOOL` | Invoke the delete_state operation. |
| `home_assistant_expose_entities` | `APITOOL` | Invoke the expose_entities operation. |
| `home_assistant_expose_or_unexpose_entities` | `APITOOL` | Invoke the expose_or_unexpose_entities operation. |
| `home_assistant_extract_from_target` | `APITOOL` | Invoke the extract_from_target operation. |
| `home_assistant_fire_event` | `APITOOL` | Invoke the fire_event operation. |
| `home_assistant_get_calendar_events` | `APITOOL` | Invoke the get_calendar_events operation. |
| `home_assistant_get_calendars` | `APITOOL` | Invoke the get_calendars operation. |
| `home_assistant_get_camera_proxy` | `APITOOL` | Invoke the get_camera_proxy operation. |
| `home_assistant_get_components` | `APITOOL` | Invoke the get_components operation. |
| `home_assistant_get_conditions_for_target` | `APITOOL` | Invoke the get_conditions_for_target operation. |
| `home_assistant_get_config` | `APITOOL` | Invoke the get_config operation. |
| `home_assistant_get_entity_registry_display` | `APITOOL` | Invoke the get_entity_registry_display operation. |
| `home_assistant_get_entity_registry_list_for_display` | `APITOOL` | Invoke the get_entity_registry_list_for_display operation. |
| `home_assistant_get_error_log` | `APITOOL` | Invoke the get_error_log operation. |
| `home_assistant_get_events` | `APITOOL` | Invoke the get_events operation. |
| `home_assistant_get_history` | `APITOOL` | Invoke the get_history operation. |
| `home_assistant_get_logbook` | `APITOOL` | Invoke the get_logbook operation. |
| `home_assistant_get_panels` | `APITOOL` | Invoke the get_panels operation. |
| `home_assistant_get_services` | `APITOOL` | Invoke the get_services operation. |
| `home_assistant_get_services_for_target` | `APITOOL` | Invoke the get_services_for_target operation. |
| `home_assistant_get_state` | `APITOOL` | Invoke the get_state operation. |
| `home_assistant_get_states` | `APITOOL` | Invoke the get_states operation. |
| `home_assistant_get_triggers_for_target` | `APITOOL` | Invoke the get_triggers_for_target operation. |
| `home_assistant_handle_intent` | `APITOOL` | Invoke the handle_intent operation. |
| `home_assistant_list_calendars` | `APITOOL` | Invoke the list_calendars operation. |
| `home_assistant_list_events` | `APITOOL` | Invoke the list_events operation. |
| `home_assistant_list_exposed_entities` | `APITOOL` | Invoke the list_exposed_entities operation. |
| `home_assistant_list_services` | `APITOOL` | Invoke the list_services operation. |
| `home_assistant_list_states` | `APITOOL` | Invoke the list_states operation. |
| `home_assistant_ping` | `APITOOL` | Invoke the ping operation. |
| `home_assistant_render_template` | `APITOOL` | Invoke the render_template operation. |
| `home_assistant_status` | `APITOOL` | Invoke the status operation. |
| `home_assistant_subscribe_events` | `APITOOL` | Invoke the subscribe_events operation. |
| `home_assistant_subscribe_trigger` | `APITOOL` | Invoke the subscribe_trigger operation. |
| `home_assistant_unsubscribe_events` | `APITOOL` | Invoke the unsubscribe_events operation. |
| `home_assistant_update_state` | `APITOOL` | Invoke the update_state operation. |
| `home_assistant_validate_config` | `APITOOL` | Invoke the validate_config operation. |

</details>

_12 action-routed tool(s) · 41 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (**`intent` default** — the six verb-tools, granular set loaded on demand · `condensed` action-routed · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/usage.md](docs/usage.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows the operator to restrict the set of exposed tools to prevent blowing up the LLM's context window.

The operator can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to the operator's transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the connector-focused `[mcp]` extra.** Examples use `home-assistant-agent[mcp]` to add
> FastMCP / FastAPI through `agent-connector-sdk`; the required Agent Connector SDK core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "home-assistant-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "home-assistant-agent[mcp]",
        "home-assistant-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "intent",
        "CALENDARTOOL": "True",
        "CONFIGTOOL": "True",
        "ENTITIESTOOL": "True",
        "EVENTSTOOL": "True",
        "HISTORYTOOL": "True",
        "HOME_ASSISTANT_TOKEN": "your_long_lived_access_token_here",
        "HOME_ASSISTANT_URL": "http://localhost:8123",
        "KGTOOL": "True",
        "LOGBOOKTOOL": "True",
        "PANELSTOOL": "True",
        "SERVICESTOOL": "True",
        "STATESTOOL": "True",
        "SYSTEMTOOL": "True",
        "VOICETOOL": "True"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as Arbora. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "home-assistant-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "home-assistant-agent[mcp]",
        "home-assistant-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
        "CALENDARTOOL": "True",
        "CONFIGTOOL": "True",
        "ENTITIESTOOL": "True",
        "EVENTSTOOL": "True",
        "HISTORYTOOL": "True",
        "HOME_ASSISTANT_TOKEN": "your_long_lived_access_token_here",
        "HOME_ASSISTANT_URL": "http://localhost:8123",
        "KGTOOL": "True",
        "LOGBOOKTOOL": "True",
        "PANELSTOOL": "True",
        "SERVICESTOOL": "True",
        "STATESTOOL": "True",
        "SYSTEMTOOL": "True",
        "VOICETOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "home-assistant-mcp": {
      "url": "http://localhost:8000/home-assistant-mcp/mcp"
    }
  }
}
```

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
  -e CALENDARTOOL=True \
  -e CONFIGTOOL=True \
  -e ENTITIESTOOL=True \
  -e EVENTSTOOL=True \
  -e HISTORYTOOL=True \
  -e HOME_ASSISTANT_TOKEN=your_long_lived_access_token_here \
  -e HOME_ASSISTANT_URL=http://localhost:8123 \
  -e KGTOOL=True \
  -e LOGBOOKTOOL=True \
  -e PANELSTOOL=True \
  -e SERVICESTOOL=True \
  -e STATESTOOL=True \
  -e SYSTEMTOOL=True \
  -e VOICETOOL=True \
  registry.example.invalid/home-assistant-agent@sha256:<digest> home-assistant-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`home-assistant-agent` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/home-assistant-agent/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
<!-- END GENERATED: additional-deployment-options -->

## Agent

# Set credentials
export HOME_ASSISTANT_URL="http://localhost:8123"
export HOME_ASSISTANT_TOKEN="your_token_here"
# Configure TLS_PROFILE or TLS_PROFILE_REF through AgentConfig for private PKI.

# Connector-focused MCP server (includes the shared graph engine)
uv pip install "home-assistant-agent[mcp]"

# Everything (development)
uv pip install "home-assistant-agent[all]"      # or: python -m pip install "home-assistant-agent[all]"
```

### Container images (`:mcp`)

One multi-stage `docker/Dockerfile` builds the MCP-only image (`--target mcp`):

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|

```bash
