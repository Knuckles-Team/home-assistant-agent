# Concept Registry — home-assistant-agent

> **Prefix**: `CONCEPT:HASS-*`
> **Version**: 0.15.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/scion-sdk/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:HA-OS.governance.hass` | Calendar Management | MCP tool domain `calendar` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-2` | Config Operations | MCP tool domain `config` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-3` | Entities Operations | MCP tool domain `entities` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-4` | Events Operations | MCP tool domain `events` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-5` | History Operations | MCP tool domain `history` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-6` | Logbook Operations | MCP tool domain `logbook` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-7` | Panels Operations | MCP tool domain `panels` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-8` | Services Operations | MCP tool domain `services` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-9` | States Operations | MCP tool domain `states` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-10` | System Information & Health | MCP tool domain `system` — Action-routed dynamic tool registration |
| `CONCEPT:HA-OS.governance.hass-11` | Voice Operations | MCP tool domain `voice` — Action-routed dynamic tool registration |

## Cross-Project References (from scion-sdk)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | scion-sdk |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | scion-sdk |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | scion-sdk |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | scion-sdk |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | scion-sdk |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | scion-sdk |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | scion-sdk |

## Synergy with scion-sdk

This project integrates with `scion-sdk` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `home_assistant_agent` MCP server registers its tools with the scion-sdk FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all HASS-* concepts.
