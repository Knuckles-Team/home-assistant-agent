# CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT — The connector serves its packaged content

Owner: home-assistant-agent. Cross-repo IDs: `SCION-CONNECTOR-CONTROL-R071`, `SCION-CONNECTOR-CONTROL-R073`.

## Purpose and user stories

The `home-assistant-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

## Why a new spec

The specs of this repository were read; none owns this capability. This spec states it for this connector only.

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: the SDK modules and the engine, which own the shared capabilities.

## User Scenarios & Testing

### User Story 1 - The connector serves its packaged content (Priority: P1)

The `home-assistant-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R001` (default content) is exercised, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.

### User Story 2 - The pack extends only the core ontology (Priority: P1)

The fleet operator and the engine rely on this behaviour of ``: its pack adds terms under the core ontology and declares no second copy of a core term. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `` connector built from the default branch, **When** `tests/test_ontology_extends_core.py::test_pack_declares_no_core_term` runs, **Then** the served Turtle declares none of the listed core terms.

### Edge Cases

- If `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R001` is not met, its proving test fails: default content.

## Requirements

- **FR-001**: Default content. Rows: `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R001`.
- **FR-002**: The pack extends only the core ontology. Rows: `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R004`.

## Success Criteria

- **SC-001**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R001`.
- **SC-002**: The served Turtle declares none of the listed core terms. Rows: `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R004`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R004` | plan.md Production caller chain | T-004 | tests/test_ontology_extends_core.py::test_pack_declares_no_core_term |
