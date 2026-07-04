---
name: home-assistant-telemetry-history
description: >-
  Analyze Home Assistant sensor telemetry and push it into the knowledge graph
  via the home-assistant-agent MCP server — read a sensor's history/period
  timeseries, browse the logbook of state changes, and natively ingest entity
  states + history as typed :Entity/:SensorReading nodes for cross-session
  reasoning. Use when the agent must chart a sensor over time, explain what
  changed and when, or make home telemetry queryable in the KG. Do NOT use for
  live actuation/state reads (use home-assistant-entity-control) or scene/event
  orchestration (use home-assistant-scene-automation).
license: MIT
tags: [home-assistant, iot, telemetry, timeseries, knowledge-graph, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Home Assistant Telemetry & History

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

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`home-assistant-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `HOME_ASSISTANT_URL` | ✅ | Base URL, e.g. `http://homeassistant.local:8123` |
| `HOME_ASSISTANT_TOKEN` | ✅ | Long-lived access token |
| `HOME_ASSISTANT_SSL_VERIFY` | optional | TLS verification toggle |

KG ingestion is **best-effort**: with no reachable epistemic-graph engine the
`home_ingest_*` tools return `{"ingested": null}` and the rest still works.

## Tools & actions
| Condensed tool | Actions |
|----------------|---------|
| `home_assistant_history` | `get_history` |
| `home_assistant_logbook` | `get_logbook`, `get_error_log` |

Wire-First KG ingestion tools (native typed-node push, not action-routed):

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
Get a temperature sensor's history since a start time (`home_assistant_history`
`params_json`):
```json
{"entity_id":"sensor.living_room_temperature","timestamp":"2026-07-01T00:00:00Z"}
```
Read the logbook for one entity over a window (`home_assistant_logbook` `params_json`):
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
- `home_assistant_history` / `home_assistant_logbook` take a **JSON string**
  `params_json`; the `home_ingest_*` tools take **typed args** directly.
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
