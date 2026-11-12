---
name: home-assistant-services-and-events
skill_type: skill
description: >-
  Call services, fire and watch events, run intents, render templates and look up the
  triggers, conditions and services available for a target. Do NOT use for tasks outside
  the home-assistant-agent connector.
license: MIT
tags: [home-assistant, mcp]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---

# Home Assistant services, events and automation

Use the typed tools of the `home-assistant-agent` connector: one tool per upstream API operation, named `home_assistant_<operation>`. Each tool takes typed parameters; there is no `action` or `params_json` routing.

## Where the data lives

- **homeassistant-states** (`HOME_ASSISTANT_URL`): holds Device; read with `home_assistant_list_states`.
- **homeassistant-history** (`HOME_ASSISTANT_URL`): holds Observation; read with `home_assistant_get_history`.
- **homeassistant-calendars** (`HOME_ASSISTANT_URL`): holds Event; read with `home_assistant_get_calendars`.

## Workflows (tool-use contracts)

Each workflow is a tool-use contract in the connector ontology. Run the steps in order; read before you write.

### `home-assistant-manage-service`

1. `home_assistant_get_services` (no parameters) - Get services.
2. `home_assistant_get_services_for_target` (`expand_group`, `target`) - Get services for target.
3. `home_assistant_list_services` (no parameters) - List services.
4. `home_assistant_call_service` (`domain`, `return_response`, `service`, `service_data`) - Run call service. (destructive: ask the operator first)

### `home-assistant-manage-event`

1. `home_assistant_get_events` (no parameters) - Get events.
2. `home_assistant_list_events` (no parameters) - List events.
3. `home_assistant_subscribe_events` (`event_type`) - Run subscribe events.
4. `home_assistant_unsubscribe_events` (`subscription_id`) - Run unsubscribe events.
5. `home_assistant_fire_event` (`event_data`, `event_type`) - Run fire event. (destructive: ask the operator first)

### `home-assistant-manage-trigger`

1. `home_assistant_get_conditions_for_target` (`expand_group`, `target`) - Get conditions for target.
2. `home_assistant_get_triggers_for_target` (`expand_group`, `target`) - Get triggers for target.
3. `home_assistant_subscribe_trigger` (`trigger`) - Run subscribe trigger.

### `home-assistant-manage-intent`

1. `home_assistant_handle_intent` (`data`, `name`) - Handle intent. (destructive: ask the operator first)

### `home-assistant-inspect-template`

1. `home_assistant_render_template` (`template`) - Run render template.

## Guardrails

- Read before you write: every change starts from the read steps of its contract.
- Never print or log the long-lived access token.
- Identify devices by entity_id and confirm the entity exists before acting on it.
- Report a tool refusal or HTTP error as it is; never retry past a refusal or invent a result.
