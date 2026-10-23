# CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `home-assistant-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `home_assistant_agent` from it.
