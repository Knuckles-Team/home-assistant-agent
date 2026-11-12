---
name: home-assistant-observability
skill_type: skill
description: >-
  Read state history, the logbook, the error log, calendars and camera snapshots, and
  ingest states and history into the knowledge graph. Do NOT use for tasks outside the
  home-assistant-agent connector.
license: MIT
tags: [home-assistant, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Home Assistant history and observability

Use the typed tools of the `home-assistant-agent` connector: one tool per upstream API operation, named `home_assistant_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **homeassistant-states** (`HOME_ASSISTANT_URL`): holds Device; read with `home_assistant_list_states`.
- **homeassistant-history** (`HOME_ASSISTANT_URL`): holds Observation; read with `home_assistant_get_history`.
- **homeassistant-calendars** (`HOME_ASSISTANT_URL`): holds Event; read with `home_assistant_get_calendars`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `home-assistant-inspect-calendar`

1. `home_assistant_get_calendar_events` (`end`, `entity_id`, `start`) - Get calendar events.
2. `home_assistant_get_calendars` (no parameters) - Get calendars.
3. `home_assistant_list_calendars` (no parameters) - List calendars.

### `home-assistant-inspect-camera`

1. `home_assistant_get_camera_proxy` (`entity_id`, `time`) - Get camera proxy.

### `home-assistant-inspect-error-log`

1. `home_assistant_get_error_log` (no parameters) - Get error log.

### `home-assistant-manage-history`

1. `home_assistant_get_history` (`end_time`, `entity_id`, `timestamp`) - Get history.
2. `home_assistant_get_logbook` (`end_time`, `entity_id`, `timestamp`) - Get logbook.
3. `home_ingest_history` (`end_time`, `entity_id`, `timestamp`) - Run home ingest history.

### `home-assistant-manage-ingest`

1. `home_ingest_states` (`with_readings`) - Run home ingest states.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the long-lived access token.
- Identify devices by entity_id and confirm the entity exists before acting on it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
