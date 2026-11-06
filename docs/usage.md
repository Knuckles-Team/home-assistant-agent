# Usage

`home-assistant-agent` exposes the same capability three ways: as **MCP tools** an
agent calls, as a **Python API** (`HomeAssistantApi`) the operator import, and as a **CLI**.
The full tool surface and architecture are described in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers one typed tool per Home Assistant
client operation, named `home_assistant_<operation>` (for example
`home_assistant_get_state`, `home_assistant_call_service`, `home_assistant_get_history`),
plus the `home_ingest_*` KG tools. Arguments are typed tool parameters; there is no
`action` router and no `params_json` string.

Example agent prompts that map onto these tools:

- *"Turn on the living-room lights"* -> `home_assistant_call_service` (`light.turn_on`)
- *"What was the thermostat set to yesterday afternoon?"* -> `home_assistant_get_history`
- *"List every calendar event scheduled for tomorrow"* → `calendar`

## As a Python API

`HomeAssistantApi` is a unified REST + WebSocket client. Built it directly, or
build one straight from the environment with `get_client()`.

```python
from home_assistant_agent.api_client import HomeAssistantApi

api = HomeAssistantApi(
    base_url="http://your-home-assistant:8123",
    token="your_long_lived_access_token",
)

# Reads
config = api.get_config()  # instance configuration
states = api.get_states()  # all entity states
one = api.get_state("light.living_room")  # a single entity
services = api.get_services()  # available service domains
calendars = api.get_calendars()  # configured calendars
log = api.get_error_log()  # the Home Assistant error log
```

Build a client straight from the environment:

```python
from home_assistant_agent.auth import get_client

api = get_client()  # reads HOME_ASSISTANT_* from the environment / .env
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

Both honor the `HOME_ASSISTANT_*` environment variables documented in
[Deployment](deployment.md#configuration-environment) and in
[`.env.example`](https://github.com/Knuckles-Team/home-assistant-agent/blob/main/.env.example).
