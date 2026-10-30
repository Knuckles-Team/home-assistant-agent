# Installation

`home-assistant-agent` is a standard Python package and a prebuilt container image.
Pick the path that matches how the operator want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Home Assistant instance** with a long-lived access token — see
  [Backing Platform](platform.md) to deploy one locally.

## From PyPI (recommended)

```bash
pip install home-assistant-agent
```

### Optional extras

The base install ships the MCP server runtime. Install the extra for what the operator need:

| Extra | Install | Pulls in |
|---|---|---|
| _(base)_ | `pip install home-assistant-agent` | FastMCP MCP-server runtime (`scion-sdk`) |
| `test` | `pip install "home-assistant-agent[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` |

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

[Deployment](deployment.md).

## Verify the install

## Next steps

- **[Usage](usage.md)** — call the tools, the API, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
