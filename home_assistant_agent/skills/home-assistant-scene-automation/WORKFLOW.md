# Home Assistant Scene Automation

Orchestrate Home Assistant scenes, events, and automations via the home-assistant-agent MCP server — fire events, activate scenes/scripts through services, introspect the entity registry and areas, and discover which services/triggers/conditions a target supports. Use when the agent must set up or trigger multi-entity flows, drive event-based automations, or map devices to areas/registry metadata. Do NOT use for single-entity reads/actuation (use home-assistant-entity-control) or history/telemetry analysis (use home-assistant-telemetry-history).

# Home Assistant Scenes, Events & Automation

Multi-entity orchestration on Home Assistant: fire **events**, activate **scenes /
scripts** via services, and introspect the **entity registry** + **areas** and the
triggers/conditions/services a target supports — the discovery layer that makes
automation building reliable.

## When to use
- Fire a custom event or trigger an event-driven automation.
- Activate a scene or run a script (`scene.turn_on`, `script.<name>`).
- Introspect the entity registry / areas / devices, and resolve which entities,
  devices, and areas a target (a service call target) references.
- Discover the services, triggers, and conditions valid for a target before building
  an automation.

## When NOT to use
- Reading/actuating a single entity → `home-assistant-entity-control`.
- History, logbook, or KG telemetry ingestion → `home-assistant-telemetry-history`.
- Rendering templates / validating config / handling intents — those are on the
  `home_assistant_system` tool (adjacent, not covered here).

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`home-assistant-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `HOME_ASSISTANT_URL` | ✅ | Base URL, e.g. `[configured-endpoint]` |
| `HOME_ASSISTANT_TOKEN` | ✅ | Long-lived access token |
| `HOME_ASSISTANT_TLS_PROFILE` | optional | Named AgentConfig TLS profile; peer and hostname verification are mandatory. |
| `HOME_ASSISTANT_TLS_PROFILE_REF` | optional | Reference-backed AgentConfig TLS profile selector. |

## Tools & actions
| Condensed tool | Actions |
|----------------|---------|
| `home_assistant_events` | `list_events`, `fire_event`, `subscribe_events` |
| `home_assistant_services` | `list_services`, `call_service` |
| `home_assistant_entities` | `get_entity_registry_display`, `extract_from_target`, `get_triggers_for_target`, `get_conditions_for_target`, `get_services_for_target` |

### Key parameters
- `fire_event` — `event_type` (required) + optional `event_data`.
- `call_service` — `domain`, `service`, `service_data` (used here for `scene`/`script`).
- `extract_from_target` — a `target` object (`entity_id`/`device_id`/`area_id`) to
  resolve referenced + missing entities/devices/areas.
- `get_*_for_target` — a `target` to enumerate valid services/triggers/conditions.

## Recipes (`params_json`)
Activate a scene:
```json
{"domain":"scene","service":"turn_on","service_data":{"entity_id":"scene.movie_night"}}
```
Run a script:
```json
{"domain":"script","service":"turn_on","service_data":{"entity_id":"script.arrive_home"}}
```
Fire a custom event:
```json
{"event_type":"my_custom_event","event_data":{"reason":"agent_trigger"}}
```
Resolve everything a target references (entities/devices/areas):
```json
{"target":{"area_id":"living_room"}}
```
List the entity registry (entity_id → platform / device / area):
```json
{}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object.
- The entity registry uses **compact keys** — `ei`=entity_id, `pl`=platform,
  `di`=device_id, `ai`=area_id, `en`=name; map them when reading `get_entity_registry_display`.
- Scenes/scripts are activated **through `call_service`** (domain `scene`/`script`),
  not a dedicated tool.
- Before building an automation, call `get_services_for_target` /
  `get_triggers_for_target` so you use only valid service/trigger names for that target.
- `subscribe_events` opens a stream; it is for listening, not a one-shot request —
  prefer `fire_event` / `get_logbook` for point-in-time work.

## Related
- **Control:** `home-assistant-entity-control` for the individual actuations a scene
  composes.
- **Telemetry:** `home-assistant-telemetry-history` to verify an automation's effect
  in the logbook/history and in the KG.
- **Registry → KG:** `home_ingest_states` maps registry entities into `:Entity`/`:Device`/
  `:Area` nodes for graph-side reasoning.
