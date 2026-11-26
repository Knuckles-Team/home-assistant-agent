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

## Steps

1. Check the instance answers with `home_assistant_get_error_log` and verify the log text is returned.
2. Read an entity's history with `home_assistant_get_history`(entity_id, timestamp, end_time) and verify the window holds readings.
3. Read state changes with `home_assistant_get_logbook`(entity_id, timestamp, end_time) and verify the entries match the history window.
4. List the calendars with `home_assistant_get_calendars` and verify the calendar entity_id you need appears.
5. Read its events with `home_assistant_get_calendar_events`(entity_id, start, end) and verify the events fall inside the requested range.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| Calls answer 401 or 403 | `HOME_ASSISTANT_TOKEN` is missing, expired or revoked | Create a new long-lived access token in the Home Assistant profile page, set `HOME_ASSISTANT_TOKEN`, and confirm with `home_assistant_status` |
| History or logbook is empty | The window is older than the recorder retention or the entity_id is wrong | Use a recent window and confirm the entity_id with `home_assistant_list_states` |
| Calendar events are missing | The calendar entity_id or the start and end range is wrong | Take the entity_id from `home_assistant_get_calendars` and pass both start and end in ISO-8601 form |

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
