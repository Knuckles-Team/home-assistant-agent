---
name: home-assistant-entity-registry
skill_type: skill
description: >-
  Read and change entity states and the entity registry, and choose which entities voice
  assistants may control. Do NOT use for tasks outside the home-assistant-agent connector.
license: MIT
tags: [home-assistant, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Home Assistant entities and states

Use the typed tools of the `home-assistant-agent` connector: one tool per upstream API operation, named `home_assistant_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **homeassistant-states** (`HOME_ASSISTANT_URL`): holds Device; read with `home_assistant_list_states`.
- **homeassistant-history** (`HOME_ASSISTANT_URL`): holds Observation; read with `home_assistant_get_history`.
- **homeassistant-calendars** (`HOME_ASSISTANT_URL`): holds Event; read with `home_assistant_get_calendars`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `home-assistant-manage-state`

1. `home_assistant_get_state` (`entity_id`) - Get state.
2. `home_assistant_get_states` (no parameters) - Get states.
3. `home_assistant_list_states` (no parameters) - List states.
4. `home_assistant_update_state` (`attributes`, `entity_id`, `state`) - Update state.
5. `home_assistant_delete_state` (`confirm`, `entity_id`) - Delete state. (destructive: ask the operator first)

### `home-assistant-manage-registry`

1. `home_assistant_get_entity_registry_display` (no parameters) - Get entity registry display.
2. `home_assistant_get_entity_registry_list_for_display` (no parameters) - Get entity registry list for display.
3. `home_assistant_list_exposed_entities` (no parameters) - List exposed entities.
4. `home_assistant_expose_entities` (`assistants`, `entity_ids`, `should_expose`) - Run expose entities.
5. `home_assistant_expose_or_unexpose_entities` (`assistants`, `entity_ids`, `should_expose`) - Run expose or unexpose entities.

### `home-assistant-inspect-target`

1. `home_assistant_extract_from_target` (`expand_group`, `target`) - Run extract from target.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the long-lived access token.
- Identify devices by entity_id and confirm the entity exists before acting on it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
