# Concept Registry — home-assistant-agent

> **Prefix**: `CONCEPT:HASS-*`
> **Version**: 0.15.0
> **Bridge**: [`CONCEPT:ECO-4.0`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:HASS-001` | Calendar Management | MCP tool domain `calendar` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-002` | Config Operations | MCP tool domain `config` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-003` | Entities Operations | MCP tool domain `entities` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-004` | Events Operations | MCP tool domain `events` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-005` | History Operations | MCP tool domain `history` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-006` | Logbook Operations | MCP tool domain `logbook` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-007` | Panels Operations | MCP tool domain `panels` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-008` | Services Operations | MCP tool domain `services` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-009` | States Operations | MCP tool domain `states` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-010` | System Information & Health | MCP tool domain `system` — Action-routed dynamic tool registration |
| `CONCEPT:HASS-011` | Voice Operations | MCP tool domain `voice` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:OS-5.2` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:OS-5.3` | Guardrail Engine | agent-utilities |
| `CONCEPT:OS-5.4` | Audit Logging | agent-utilities |
| `CONCEPT:KG-2.0` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:ECO-4.0` (Unified Toolkit Ingestion). The `home_assistant_agent` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all HASS-* concepts.
