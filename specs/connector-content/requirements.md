# CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `home-assistant-mcp` as the single `scion_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Proving test: `tests/test_default_content_surfaces.py`. Caller chain: the home-assistant-mcp console script (scion_sdk.cli:serve) loads the scion_sdk.connector entry point home_assistant_agent:connector (home_assistant_agent/__init__.py:8), and the SDK build_server serves the packaged skills, ontology and prompts as resources and prompts. Shape: Connector in home_assistant_agent/__init__.py passes no content= argument; default content comes from home_assistant_agent/skills, ontology and prompts, and the test follows the documentdb-mcp tests/test_default_content_surfaces.py pattern. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Planned test: `tests/test_default_content_surfaces.py::test_default_content_surfaces`. |
