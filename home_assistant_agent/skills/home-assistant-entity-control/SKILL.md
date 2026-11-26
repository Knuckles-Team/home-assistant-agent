---
name: home-assistant-entity-control
skill_type: skill
description: >-
  Read and control Home Assistant entities via the home-assistant-agent MCP server: inspect state, call services to actuate devices, set or clear state. Use to answer what an entity is doing, turn things on or off, or adjust a thermostat, brightness or cover. Do NOT use for history analysis (home-assistant-telemetry-history) or scenes and events (home-assistant-scene-automation).
license: MIT
tags: [home-assistant, iot, smart-home, entities, services, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Home Assistant Entity Control

Scope: Read and control Home Assistant entities via the home-assistant-agent MCP server — inspect entity state, call services to actuate devices (lights, switches, climate, covers, media players), and set/clear state. Use when the agent must answer "what is an entity doing?", turn something on/off, adjust a thermostat/brightness/cover position, or trigger a service on a device. Do NOT use for long-term telemetry/history analysis (use home-assistant-telemetry-history) or scene/automation orchestration and event-driven flows (use home-assistant-scene-automation).

Domain-typed read + actuation of Home Assistant **entities**. Prefer these tools
over raw REST — they return entity-shaped state and route service calls through
the integration domain (`light`, `switch`, `climate`, `cover`, `media_player`, …).

## When to use
- Read the current state + attributes of one entity, or list all entity states.
- Actuate a device by calling a service (`light.turn_on`, `climate.set_temperature`,
  `cover.set_cover_position`, `media_player.play_media`, …).
- Set or delete an entity's state directly (for template/input entities).

## When NOT to use
- Historical trends / logbook / KG telemetry ingestion → `home-assistant-telemetry-history`.
- Firing arbitrary events, entity-registry/area introspection, or multi-step
  scene/automation flows → `home-assistant-scene-automation`.
- Discovering which services/params a target supports → the `entities` tool's
  `get_services_for_target` (covered in `home-assistant-scene-automation`).

## Steps

1. Confirm the connector reaches Home Assistant with `home_assistant_ping` and verify the reply is a success, not an HTTP error.
2. Read the entity with `home_assistant_get_state`(entity_id) and verify the state and attributes belong to the intended device.
3. Check the service is offered with `home_assistant_list_services` and verify the domain and service name appear in the list.
4. Actuate the device with `home_assistant_call_service`(domain, service, service_data) after the requester approved the action, and verify the call returns without an error.
5. Read the entity again with `home_assistant_get_state`(entity_id) and verify the state changed as requested.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| Calls answer 401 or 403 | `HOME_ASSISTANT_TOKEN` is missing, expired or revoked | Create a new long-lived access token in the Home Assistant profile page, set `HOME_ASSISTANT_TOKEN`, and confirm with `home_assistant_status` |
| `home_assistant_get_state` returns not found | The entity_id is misspelled or the entity was renamed | List candidates with `home_assistant_list_states` and use the exact entity_id it returns |
| `home_assistant_delete_state` is refused | The destructive call was sent without confirm=true | Obtain the requester's approval of the entity_id and call `home_assistant_delete_state`(entity_id, confirm=true) |

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`home-assistant-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `HOME_ASSISTANT_URL` | ✅ | Base URL, e.g. `http://homeassistant.local:8123` |
| `HOME_ASSISTANT_TOKEN` | ✅ | Long-lived access token |
| `HOME_ASSISTANT_SSL_VERIFY` | optional | TLS verification toggle (alias `HOME_ASSISTANT_AGENT_VERIFY`) |

## Tools
Each operation is its own tool named `home_assistant_<operation>`; arguments are typed tool parameters.
whose keys are passed straight to the client method.

| Typed tools |
|-------------|
| `home_assistant_list_states`, `home_assistant_get_state`, `home_assistant_update_state`, `home_assistant_delete_state` |
| `home_assistant_list_services`, `home_assistant_call_service` |

### Key parameters
- `entity_id` — required for `get_state` / `update_state` / `delete_state`
  (e.g. `light.kitchen`, `climate.living_room`).
- `call_service` takes `domain`, `service`, and `service_data` (the target +
  parameters), plus optional `return_response`.
- `update_state` takes `entity_id`, `state`, and optional `attributes`.

## Recipes (tool arguments)
Read one entity's state:
```json
{"entity_id":"sensor.living_room_temperature"}
```
Turn on a light at 60% warm-white:
```json
{"domain":"light","service":"turn_on","service_data":{"entity_id":"light.kitchen","brightness_pct":60,"color_temp_kelvin":2700}}
```
Set a thermostat target temperature:
```json
{"domain":"climate","service":"set_temperature","service_data":{"entity_id":"climate.living_room","temperature":21.5}}
```
Open a cover to 50%:
```json
{"domain":"cover","service":"set_cover_position","service_data":{"entity_id":"cover.garage","position":50}}
```

## Gotchas
- The service `domain` is the integration (`light`), not the entity's — derive it
  from the `entity_id` prefix (`light.kitchen` → domain `light`).
- `call_service` returns the list of states it changed (or a `service_response` when
  `return_response` is set) — read it back to confirm the actuation took effect.
- `update_state` sets the state **in HA's state machine only**; it does not command
  the physical device — use `call_service` to actuate hardware.
- Always confirm the entity exists first (`get_state`); a bad `entity_id` 404s.

## Related
- **Telemetry:** `home-assistant-telemetry-history` for history/logbook trends and
  pushing state into the knowledge graph.
- **Orchestration:** `home-assistant-scene-automation` for events, scenes, and
  registry/area introspection.
