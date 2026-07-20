# Usage

`home-assistant-agent` exposes the same capability three ways: as **MCP tools** an
agent calls, as a **Python API** (`HomeAssistantApi`) you import, and as a **CLI**.
The full tool surface and architecture are described in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers eleven action-routed tool
domains. Each domain is enabled independently by its environment flag (all default
to enabled):

| Tool domain | Flag | Covers |
|---|---|---|
| `config` | `CONFIGTOOL` | Instance configuration, components, config validation |
| `states` | `STATESTOOL` | Read, set, and delete entity states |
| `services` | `SERVICESTOOL` | List and call Home Assistant services |
| `events` | `EVENTSTOOL` | List event types and fire events |
| `history` | `HISTORYTOOL` | Historical state queries over a time window |
| `logbook` | `LOGBOOKTOOL` | Logbook entries and the error log |
| `calendar` | `CALENDARTOOL` | List calendars and calendar events |
| `panels` | `PANELSTOOL` | Custom Lovelace panels |
| `voice` | `VOICETOOL` | Voice-exposed entities and settings |
| `entities` | `ENTITIESTOOL` | Entity registry lookup |
| `system` | `SYSTEMTOOL` | Templates, intents, and system health |

Example agent prompts that map onto these tools:

- *"Turn on the living-room lights"* → `services` (call `light.turn_on`)
- *"What was the thermostat set to yesterday afternoon?"* → `history`
- *"List every calendar event scheduled for tomorrow"* → `calendar`

## As a Python API

`HomeAssistantApi` is a unified REST + WebSocket client. Construct it directly, or
build one straight from the environment with `get_client()`.

```python
from home_assistant_agent.api_client import HomeAssistantApi

api = HomeAssistantApi(
    base_url="http://your-home-assistant:8123",
    token="your_long_lived_access_token",
)

# Reads
config = api.get_config()                 # instance configuration
states = api.get_states()                 # all entity states
one = api.get_state("light.living_room")  # a single entity
services = api.get_services()             # available service domains
calendars = api.get_calendars()           # configured calendars
log = api.get_error_log()                 # the Home Assistant error log
```

Build a client straight from the environment:

```python
from home_assistant_agent.auth import get_client
api = get_client()        # reads HOME_ASSISTANT_* from the environment / .env
```

### Actions

State changes and service calls go through the same client:

```python
# Set an entity state
api.update_state("input_boolean.guest_mode", "on")

# Call a service
api.call_service("light", "turn_on", {"entity_id": "light.living_room"})

# Fire an event
api.fire_event("custom_event", {"source": "home-assistant-agent"})
```

## As a CLI

Both entry points are command-line programs.

```bash
# MCP server (stdio by default; --transport for HTTP / SSE)
home-assistant-mcp --transport streamable-http --host 0.0.0.0 --port 8000

# A2A agent server (connects to the MCP server, exposes an A2A endpoint + web UI)
home-assistant-agent --provider openai --model-id gpt-4o --api-key sk-...
```

Both honor the `HOME_ASSISTANT_*` environment variables documented in
[Deployment](deployment.md#configuration-environment) and in
[`.env.example`](https://github.com/Knuckles-Team/home-assistant-agent/blob/main/.env.example).
