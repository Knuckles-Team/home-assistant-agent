# Backing Platform — Home Assistant

`home-assistant-agent` is a **client** of a Home Assistant instance. This page
provides a Docker recipe for deploying one locally to serve as the target of
`HOME_ASSISTANT_URL`. For production topologies, follow the upstream
[Home Assistant documentation](https://www.home-assistant.io/installation/).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe.

## Single-node deployment (Compose)

Home Assistant publishes the `homeassistant/home-assistant` image. The following
stack runs one instance on `:8123` with a persistent configuration volume:

```yaml
# docker/home-assistant.compose.yml
services:
  homeassistant:
    image: docker.io/homeassistant/home-assistant@sha256:<digest>
    container_name: homeassistant
    hostname: homeassistant
    restart: always
    privileged: true
    environment:
      - TZ=America/Chicago
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - homeassistant:/config
    ports:
      - "8123:8123"

volumes:
  homeassistant:
```

```bash
docker compose -f docker/home-assistant.compose.yml up -d

# Complete onboarding at the web UI, then create a long-lived access token
# under Profile → Security → Long-lived access tokens.
curl -s http://localhost:8123/  # the onboarding UI
```

## Connect home-assistant-agent

After onboarding, generate a long-lived access token in the Home Assistant profile
and point the connector at the instance:

```bash
export HOME_ASSISTANT_URL=http://localhost:8123
export HOME_ASSISTANT_TOKEN=your_long_lived_access_token
# Configure a named AgentConfig TLS profile for private PKI; verification is mandatory.

home-assistant-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places Home Assistant and the MCP server on one Docker network, so
the server reaches Home Assistant by container name:

```yaml
# docker/stack.compose.yml
services:
  homeassistant:
    image: docker.io/homeassistant/home-assistant@sha256:<digest>
    hostname: homeassistant
    privileged: true
    volumes:
      - homeassistant:/config
    ports: ["8123:8123"]

  home-assistant-agent-mcp:
    image: example/home-assistant-agent@sha256:<digest>
    depends_on: [homeassistant]
    environment:
      - HOME_ASSISTANT_URL=http://homeassistant:8123
      - HOME_ASSISTANT_TOKEN=your_long_lived_access_token
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

volumes:
  homeassistant:
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

With the instance running and a valid token configured, the MCP tools and the
[Python API](usage.md#as-a-python-api) can read configuration, states, history, and
calendars, and call services across your smart home.
