# Home Assistant Agent - A2A | AG-UI | MCP

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

*Version: 0.12.1*

## Overview

**Home Assistant Agent MCP Server + A2A Agent**

Agent for interacting with Home Assistant REST API

This repository is actively maintained - Contributions are welcome!

## MCP

### Using as an MCP Server

The MCP Server can be run in two modes: `stdio` (for local testing) or `http` (for networked access).

#### Environment Variables

*   `HOME_ASSISTANT_URL`: The URL of the target service.
*   `HOME_ASSISTANT_TOKEN`: The API token or access token.

#### Run in stdio mode (default):
```bash
export HOME_ASSISTANT_URL="http://localhost:8080"
export HOME_ASSISTANT_TOKEN="your_token"
home-assistant-mcp --transport "stdio"
```

#### Run in HTTP mode:
```bash
export HOME_ASSISTANT_URL="http://localhost:8080"
export HOME_ASSISTANT_TOKEN="your_token"
home-assistant-mcp --transport "http" --host "0.0.0.0" --port "8000"
```

## A2A Agent

### Run A2A Server
```bash
export HOME_ASSISTANT_URL="http://localhost:8080"
export HOME_ASSISTANT_TOKEN="your_token"
home-assistant-agent --provider openai --model-id gpt-4o --api-key sk-...
```

## Security & Governance

This project is built on [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities), inheriting enterprise-grade security and governance features.

### Authentication & Authorization
| Feature | Description |
|---------|-------------|
| **OIDC Token Delegation** | RFC 8693 token exchange for user-context propagation from A2A → MCP |
| **Eunomia Policies** | Fine-grained, policy-driven tool authorization (`none`, `embedded`, `remote`) |
| **Scoped Credentials** | Tools execute with the caller's scoped identity where possible |
| **3LO / OAuth / API Token** | Multiple auth strategies with graceful fallback |

### Eunomia Policy Enforcement
Eunomia provides a policy enforcement point for all tool calls:
- **Embedded mode**: Load local `mcp_policies.json` for role-based access, sensitivity gating, and audit logging
- **Remote mode**: Forward authorization decisions to a central Eunomia policy server for multi-agent governance
- Enable via CLI: `--eunomia-type embedded --eunomia-policy-file mcp_policies.json`

### Runtime Protections
| Protection | Description |
|------------|-------------|
| **Tool Guard** | Sensitivity detection with human-in-the-loop approval gating |
| **Prompt Injection Defense** | Input scanning and repetition/loop guards |
| **Content Filtering** | Output schema enforcement and cost budget controls |
| **Stuck Loop Detection** | Automatic detection and recovery from agent loops |
| **Context Limit Warnings** | Proactive alerts before context window exhaustion |

### Graph Agent Architecture
The A2A agent uses `pydantic-graph` orchestration with:
- **RouterNode**: Lightweight classifier that routes queries to specialized domains
- **DomainNode**: Focused executor with only relevant tools loaded, preventing tool hallucination
- **Approval Gates**: Policy-driven approval workflows before sensitive operations
- **Usage Guards**: Budget and rate limiting enforcement

> **Production Recommendation**: Enable `--eunomia-type embedded` (or `remote`) + OIDC delegation + containerized deployment. See [`agent-utilities` documentation](https://github.com/Knuckles-Team/agent-utilities) for full policy configuration.

## Docker

### Build

```bash
docker build -t home-assistant-agent .
```

### Run MCP Server

```bash
docker run -d \
  --name home-assistant-agent \
  -p 8000:8000 \
  -e TRANSPORT=http \
  -e HOME_ASSISTANT_URL="http://your-service:8080" \
  -e HOME_ASSISTANT_TOKEN="your_token" \
  knucklessg1/home-assistant-agent:latest
```

### Deploy with Docker Compose

```yaml
services:
  home-assistant-agent:
    image: knucklessg1/home-assistant-agent:latest
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=http
      - HOME_ASSISTANT_URL=http://your-service:8080
      - HOME_ASSISTANT_TOKEN=your_token
    ports:
      - 8000:8000
```

#### Configure `mcp.json` for AI Integration (e.g. Claude Desktop)

```json
{
  "mcpServers": {
    "home-assistant": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "home-assistant-agent",
        "home-assistant-mcp"
      ],
      "env": {
        "HOME_ASSISTANT_URL": "http://your-service:8080",
        "HOME_ASSISTANT_TOKEN": "your_token"
      }
    }
  }
}
```

## Install Python Package

```bash
python -m pip install home-assistant-agent
```
```bash
uv pip install home-assistant-agent
```

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)


## MCP Configuration Examples

### stdio (recommended for local development)
```json
{
  "mcpServers": {
    "home-assistant": {
      "command": ".venv/bin/home-assistant-mcp",
      "args": [],
      "env": {
        "HOME_ASSISTANT_URL": "",
        "HOME_ASSISTANT_TOKEN": ""
}
    }
  }
}
```

### Streamable HTTP (recommended for production)
```json
{
  "mcpServers": {
    "home-assistant": {
      "url": "http://localhost:8080/home-assistant-mcp/mcp"
    }
  }
}
```
## Available MCP Tools

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

| Tool Name | Description |
|-----------|-------------|
| `ha_calendar` | Consolidated Action-Routed tool for calendar. Methods: list_calendars, get_calendar_events |
| `ha_config` | Consolidated Action-Routed tool for config. Methods: status, config, components, check_config |
| `ha_entities` | Consolidated Action-Routed tool for entities. Methods: get_entity_registry_display, extract_from_target, get_triggers_for_target, get_conditions_for_target, get_services_for_target |
| `ha_events` | Consolidated Action-Routed tool for events. Methods: list_events, fire_event, subscribe_events |
| `ha_history` | Consolidated Action-Routed tool for history. Methods: get_history |
| `ha_logbook` | Consolidated Action-Routed tool for logbook. Methods: get_logbook, get_error_log |
| `ha_panels` | Consolidated Action-Routed tool for panels. Methods: get_panels |
| `ha_services` | Consolidated Action-Routed tool for services. Methods: list_services, call_service |
| `ha_states` | Consolidated Action-Routed tool for states. Methods: list_states, get_state, update_state, delete_state |
| `ha_system` | Consolidated Action-Routed tool for system. Methods: render_template, ping, handle_intent, validate_config |
| `ha_voice` | Consolidated Action-Routed tool for voice. Methods: list_exposed_entities, expose_entities |
