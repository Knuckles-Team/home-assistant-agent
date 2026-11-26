---
name: home-assistant-system-config
skill_type: skill
description: >-
  Check that Home Assistant is up and read or validate its configuration, components and
  panels. Do NOT use for tasks outside the home-assistant-agent connector.
license: MIT
tags: [home-assistant, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Home Assistant system and configuration

Use the typed tools of the `home-assistant-agent` connector: one tool per upstream API operation, named `home_assistant_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Steps

1. Check the instance with `home_assistant_ping` and verify the reply is a success.
2. Read the status with `home_assistant_status` and verify it reports the instance as running.
3. Read the configuration with `home_assistant_get_config` and verify the location and version fields are present.
4. Validate the configuration with `home_assistant_check_config` and verify the result reports no errors.
5. List the loaded components with `home_assistant_get_components` and verify the integration you expect is loaded.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| Calls answer 401 or 403 | `HOME_ASSISTANT_TOKEN` is missing, expired or revoked | Create a new long-lived access token in the Home Assistant profile page, set `HOME_ASSISTANT_TOKEN`, and confirm with `home_assistant_status` |
| Calls time out or the connection is refused | `HOME_ASSISTANT_URL` is wrong or the instance is down | Correct `HOME_ASSISTANT_URL` including the port and scheme, then confirm with `home_assistant_ping` |
| `home_assistant_check_config` reports errors | A configuration file holds an invalid entry | Read the reported error, correct the named entry in the Home Assistant configuration, and call `home_assistant_check_config` again to confirm it is clean |

## Where the data lives

- **homeassistant-states** (`HOME_ASSISTANT_URL`): holds Device; read with `home_assistant_list_states`.
- **homeassistant-history** (`HOME_ASSISTANT_URL`): holds Observation; read with `home_assistant_get_history`.
- **homeassistant-calendars** (`HOME_ASSISTANT_URL`): holds Event; read with `home_assistant_get_calendars`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `home-assistant-inspect-config`

1. `home_assistant_check_config` (no parameters) - Check config.
2. `home_assistant_components` (no parameters) - Run components.
3. `home_assistant_config` (no parameters) - Run config.
4. `home_assistant_get_components` (no parameters) - Get components.
5. `home_assistant_get_config` (no parameters) - Get config.
6. `home_assistant_get_panels` (no parameters) - Get panels.
7. `home_assistant_validate_config` (`action`, `condition`, `trigger`) - Run validate config.

### `home-assistant-inspect-health`

1. `home_assistant_ping` (no parameters) - Ping.
2. `home_assistant_status` (no parameters) - Status.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the long-lived access token.
- Identify devices by entity_id and confirm the entity exists before acting on it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
