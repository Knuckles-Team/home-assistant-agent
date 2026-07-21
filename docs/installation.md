# Installation

`home-assistant-agent` is a standard Python package and a prebuilt container image.
Pick the path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Home Assistant instance** with a long-lived access token — see
  [Backing Platform](platform.md) to deploy one locally.

## From PyPI (recommended)

```bash
pip install home-assistant-agent
```

### Optional extras

The base install ships the MCP server runtime. Install the extra for what you need:

| Extra | Install | Pulls in |
|---|---|---|
| _(base)_ | `pip install home-assistant-agent` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "home-assistant-agent[agent]"` | Pydantic-AI agent server + Logfire tracing |
| `all` | `pip install "home-assistant-agent[all]"` | MCP server, agent server, and tracing |
| `test` | `pip install "home-assistant-agent[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

```bash
# Typical: run the MCP server and the A2A agent server
pip install "home-assistant-agent[all]"
```

## From source

```bash
git clone https://github.com/Knuckles-Team/home-assistant-agent.git
cd home-assistant-agent
pip install -e ".[all]"          # editable install with every extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[all]"
uv run home-assistant-mcp
```

## Prebuilt Docker image

A multi-stage runtime image is published on every release (installs
`home-assistant-agent[all]`, entrypoint `home-assistant-mcp`):

```bash
docker pull example/home-assistant-agent@sha256:<digest>

docker run --rm -i \
  -e HOME_ASSISTANT_URL=http://your-home-assistant:8123 \
  -e HOME_ASSISTANT_TOKEN=your_long_lived_access_token \
  example/home-assistant-agent@sha256:<digest>        # stdio transport (default)
```

For an HTTP server with a published port and the agent server, see
[Deployment](deployment.md).

## Verify the install

```bash
home-assistant-mcp --help
home-assistant-agent --help
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server (and agent server) behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the API, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
