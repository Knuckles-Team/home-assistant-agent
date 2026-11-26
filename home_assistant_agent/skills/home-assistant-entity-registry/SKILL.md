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

## Steps

1. Read the current states with `home_assistant_list_states` and verify the target entity_id is present.
2. Inspect the registry with `home_assistant_get_entity_registry_display` and verify the entity's area and name.
3. List what assistants may control with `home_assistant_list_exposed_entities` and verify whether the entity is exposed.
4. Change exposure with `home_assistant_expose_entities`(assistants, entity_ids, should_expose) after approval, and verify the call returns without an error.
5. Read the exposure list with `home_assistant_list_exposed_entities` and verify the entity now appears or disappears as intended.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| Calls answer 401 or 403 | `HOME_ASSISTANT_TOKEN` is missing, expired or revoked | Create a new long-lived access token in the Home Assistant profile page, set `HOME_ASSISTANT_TOKEN`, and confirm with `home_assistant_status` |
| An entity_id is not found | The entity_id is misspelled or the entity was renamed | List candidates with `home_assistant_list_states` and use the exact entity_id |
| `home_assistant_delete_state` is refused | The destructive call was sent without confirm=true | Obtain the requester's approval of the entity_id and call `home_assistant_delete_state`(entity_id, confirm=true) |

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
