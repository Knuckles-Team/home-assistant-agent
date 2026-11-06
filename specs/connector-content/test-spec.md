# CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py` | The listings include the packaged skills, ontology and prompts. |
| T-002 | `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R002` | `tests/test_action_discovery.py::test_no_action_router_registrars_remain` | The server module defines only `register_kg_tools`. |
| T-003 | `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R003` | `tests/test_live_shapes.py::test_service_domain_lists_services_as_a_mapping` | A mapping of services, a state-only logbook record and a panel with its own `url_path` all parse. |
