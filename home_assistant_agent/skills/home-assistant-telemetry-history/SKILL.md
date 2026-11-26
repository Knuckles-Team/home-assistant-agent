---
name: home-assistant-telemetry-history
skill_type: skill
description: >-
  Analyze Home Assistant sensor telemetry and ingest it into the knowledge graph via the home-assistant-agent MCP server: sensor history, logbook, and typed entity and reading nodes. Use to chart a sensor, explain what changed and when, or make telemetry queryable. Do NOT use for live actuation (home-assistant-entity-control) or scenes and events (home-assistant-scene-automation).
license: MIT
tags: [home-assistant, iot, telemetry, timeseries, knowledge-graph, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Home Assistant Telemetry & History

Scope: Analyze Home Assistant sensor telemetry and push it into the knowledge graph via the home-assistant-agent MCP server — read a sensor's history/period timeseries, browse the logbook of state changes, and natively ingest entity states + history as typed :Entity/:SensorReading nodes for cross-session reasoning. Use when the agent must chart a sensor over time, explain what changed and when, or make home telemetry queryable in the KG. Do NOT use for live actuation/state reads (use home-assistant-entity-control) or scene/event orchestration (use home-assistant-scene-automation).

Timeseries + logbook analysis of Home Assistant entities, and the **native KG
ingestion** path that maps states and history into typed `:Entity` / `:SensorReading`
nodes (the `homeassistant` ontology leg) for durable, cross-session reasoning.

## When to use
- Pull a sensor's `history/period` series to chart or reason about a trend.
- Read the **logbook** to explain what changed, when, and why.
- Ingest live states and per-entity history into the knowledge graph as
  `:Entity` + `:SensorReading` timeseries nodes (`:readingOf` links).

## When NOT to use
- Reading a single current state or actuating a device → `home-assistant-entity-control`.
- Firing events, scenes, or registry/area introspection → `home-assistant-scene-automation`.
- Ad-hoc source-sync of entity documents (non-timeseries) — that is handled by the
  Tier-1 `homeassistant-states` connector preset, not this skill's ingest tools.

## Steps

1. Confirm the connector reaches Home Assistant with `home_assistant_ping` and verify the reply is a success.
2. Read the series with `home_assistant_get_history`(entity_id, timestamp, end_time) and verify the inner list holds readings inside the requested window.
3. Read what changed and when with `home_assistant_get_logbook`(entity_id, timestamp, end_time) and verify the entries cover the same window.
4. Write the series to the knowledge graph with `home_ingest_history`(entity_id, timestamp, end_time) and verify the returned `ingested` field is not null.
5. Write the current states with `home_ingest_states`(with_readings) and verify the returned `ingested` field is not null.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| Calls answer 401 or 403 | `HOME_ASSISTANT_TOKEN` is missing, expired or revoked | Create a new long-lived access token in the Home Assistant profile page, set `HOME_ASSISTANT_TOKEN`, and confirm with `home_assistant_status` |
| `home_assistant_get_history` returns an empty list | The window is older than the recorder retention or the entity_id is wrong | Shorten the window to the last few days and confirm the entity_id with `home_assistant_list_states` |
| An ingest tool returns `{"ingested": null}` | No medulla engine is reachable, so the ingest was a no-op | Restore the engine connection in the connector's environment settings and call the ingest tool again once `home_assistant_status` and the engine both answer |

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`home-assistant-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `HOME_ASSISTANT_URL` | ✅ | Base URL, e.g. `http://homeassistant.local:8123` |
| `HOME_ASSISTANT_TOKEN` | ✅ | Long-lived access token |
| `HOME_ASSISTANT_SSL_VERIFY` | optional | TLS verification toggle |

KG ingestion is **best-effort**: with no reachable medulla engine the
`home_ingest_*` tools return `{"ingested": null}` and the rest still works.

## Tools
| Typed tools |
|-------------|
| `home_assistant_get_history` |
| `home_assistant_get_logbook`, `home_assistant_get_error_log` |

Wire-First KG ingestion tools (native typed-node push, typed args):

| Tool | Purpose |
|------|---------|
| `home_ingest_states` | List all entity states → `:Entity` (+ `:SensorReading`) nodes |
| `home_ingest_history` | One entity's history series → `:SensorReading` timeseries |

### Key parameters
- `get_history` — `entity_id` (required), optional `timestamp` (ISO-8601 start) and
  `end_time`.
- `get_logbook` — optional `entity_id`, `timestamp`, `end_time`.
- `home_ingest_states` — `with_readings` (default `true`) also emits a `:SensorReading`
  per state.
- `home_ingest_history` — `entity_id` (required), optional `timestamp` / `end_time`.

## Recipes
Get a temperature sensor's history since a start time (`home_assistant_get_history`):
```json
{"entity_id":"sensor.living_room_temperature","timestamp":"2026-07-01T00:00:00Z"}
```
Read the logbook for one entity over a window (`home_assistant_get_logbook`):
```json
{"entity_id":"binary_sensor.front_door","timestamp":"2026-07-03T00:00:00Z","end_time":"2026-07-04T00:00:00Z"}
```
Ingest all current entity states (with readings) into the KG (`home_ingest_states`):
```json
{"with_readings": true}
```
Ingest one sensor's history window as timeseries readings (`home_ingest_history`):
```json
{"entity_id":"sensor.power_meter","timestamp":"2026-07-01T00:00:00Z"}
```

## Gotchas
- All tools take typed arguments; there is no JSON-string parameter.
- `get_history` returns a **list of lists** (one inner list per entity) — the
  `home_ingest_history` tool flattens it for you; if you parse raw output, index `[0]`.
- Reading history is bounded by HA's recorder retention (default ~10 days); older data
  needs a long-term-statistics query, not `history/period`.
- `:SensorReading` node ids are keyed by `entity_id@<last_updated>`, so re-ingesting the
  same window is idempotent (no duplicate readings).
- Ingest is a no-op when the engine is unreachable — check the returned `ingested`
  field, don't assume it landed.

## Related
- **Ontology:** the `homeassistant` leg (`:Entity`, `:Device`, `:Area`, `:SensorReading`,
  `:readingOf`) that these tools populate.
- **Control:** `home-assistant-entity-control` for live reads + actuation.
- **Orchestration:** `home-assistant-scene-automation` for events and registry.
