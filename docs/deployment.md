# Deployment

This page covers running `home-assistant-agent` as a long-lived server: the
transports, a Docker Compose stack, the optional A2A agent server, putting it behind
a Caddy reverse proxy, and giving it a DNS name with Technitium. To provision the
**Home Assistant instance** it connects to, see [Backing Platform](platform.md).

> `home-assistant-agent` ships **two** entry points: an **MCP server** (console
> script `home-assistant-mcp`) — a typed, deterministic tool surface a policy router
> or agent calls — and an optional **A2A agent server** (console script
> `home-assistant-agent`) that wraps that tool surface in a Pydantic-AI graph agent.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    home-assistant-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    home-assistant-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    home-assistant-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`home-assistant-agent` is configured entirely from the environment. The **required**
set:

| Var | Default | Meaning |
|---|---|---|
| `HOME_ASSISTANT_URL` | `http://localhost:8123` | Home Assistant base URL |
| `HOME_ASSISTANT_TOKEN` | _(unset)_ | Long-lived access token |
| `HOME_ASSISTANT_AGENT_VERIFY` | `True` | Verify TLS certificates |
| `HOST` | `0.0.0.0` | Bind address (HTTP transports) |
| `PORT` | `8000` | Bind port (HTTP transports) |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |

Each MCP tool domain is registered only when its flag is enabled (all default to
`True`): `CONFIGTOOL`, `STATESTOOL`, `SERVICESTOOL`, `EVENTSTOOL`, `HISTORYTOOL`,
`LOGBOOKTOOL`, `CALENDARTOOL`, `PANELSTOOL`, `VOICETOOL`, `ENTITIESTOOL`,
`SYSTEMTOOL`. The full set, with the agent and observability settings, is documented
in [`.env.example`](https://github.com/Knuckles-Team/home-assistant-agent/blob/main/.env.example).
Copy it to `.env` and fill in only what you use.

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/home-assistant-agent/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  home-assistant-agent-mcp:
    image: knucklessg1/home-assistant-agent:latest
    container_name: home-assistant-agent-mcp
    hostname: home-assistant-agent-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
cp .env.example .env          # then edit HOME_ASSISTANT_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Run the A2A agent server

For an autonomous agent over the same tool surface, run the agent server (console
script `home-assistant-agent`). It connects to the MCP server over HTTP and exposes
an A2A endpoint plus an embedded web UI.

```bash
export HOME_ASSISTANT_URL=http://your-home-assistant:8123
export HOME_ASSISTANT_TOKEN=your_long_lived_access_token
home-assistant-agent --provider openai --model-id gpt-4o --api-key sk-...
```

The repo ships [`docker/agent.compose.yml`](https://github.com/Knuckles-Team/home-assistant-agent/blob/main/docker/agent.compose.yml),
which runs the MCP server **and** the agent server on one network. The agent reaches
the MCP server by container name via `MCP_URL` and publishes the A2A server on
`:9004`:

```yaml
services:
  home-assistant-agent-mcp:
    image: knucklessg1/home-assistant-agent:latest
    hostname: home-assistant-agent-mcp
    env_file: ["../.env"]
    environment:
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

  home-assistant-agent-agent:
    image: knucklessg1/home-assistant-agent:latest
    depends_on: [home-assistant-agent-mcp]
    command: ["home-assistant-agent"]
    env_file: ["../.env"]
    environment:
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://home-assistant-agent-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
    ports: ["9004:9004"]
```

```bash
docker compose -f docker/agent.compose.yml up -d
```

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .arpa zone
home-assistant-agent.arpa {
    tls internal
    reverse_proxy home-assistant-agent-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
home-assistant-agent.example.com {
    reverse_proxy home-assistant-agent-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.arpa:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=home-assistant-agent.arpa" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=10.0.0.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `home-assistant-agent.arpa → <caddy-host-ip>` in the
Technitium web console (`http://technitium.arpa:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "home-assistant-agent": {
      "command": "uv",
      "args": ["run", "home-assistant-mcp"],
      "env": {
        "HOME_ASSISTANT_URL": "http://your-home-assistant:8123",
        "HOME_ASSISTANT_TOKEN": "your_long_lived_access_token",
        "HOME_ASSISTANT_AGENT_VERIFY": "True"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://home-assistant-agent.arpa/mcp`
instead.
