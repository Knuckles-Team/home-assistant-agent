#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import sys
from typing import Any

from agent_utilities.core.config import load_config
from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface
from starlette.requests import Request
from starlette.responses import JSONResponse

from home_assistant_agent.api_client import HomeAssistantApi
from home_assistant_agent.auth import get_client

__version__ = "2.1.0"

logger = get_logger(name="home-assistant-agent")
logger.setLevel(logging.INFO)


def register_config_tools(mcp: FastMCP):
    """Register config tools."""

    @mcp.tool(tags={"config"})
    async def home_assistant_config(
        action: str = Field(
            description="Action to perform. Must be one of: 'status', 'config', 'components', 'check_config'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant config operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["status", "config", "components", "check_config"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_states_tools(mcp: FastMCP):
    """Register states tools."""

    @mcp.tool(tags={"states"})
    async def home_assistant_states(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_states', 'get_state', 'update_state', 'delete_state'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant states operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["list_states", "get_state", "update_state", "delete_state"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_services_tools(mcp: FastMCP):
    """Register services tools."""

    @mcp.tool(tags={"services"})
    async def home_assistant_services(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_services', 'call_service'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant services operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["list_services", "call_service"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_events_tools(mcp: FastMCP):
    """Register events tools."""

    @mcp.tool(tags={"events"})
    async def home_assistant_events(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_events', 'fire_event', 'subscribe_events'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant events operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["list_events", "fire_event", "subscribe_events"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_history_tools(mcp: FastMCP):
    """Register history tools."""

    @mcp.tool(tags={"history"})
    async def home_assistant_history(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_history'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant history operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["get_history"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_logbook_tools(mcp: FastMCP):
    """Register logbook tools."""

    @mcp.tool(tags={"logbook"})
    async def home_assistant_logbook(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_logbook', 'get_error_log'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant logbook operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["get_logbook", "get_error_log"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_calendar_tools(mcp: FastMCP):
    """Register calendar tools."""

    @mcp.tool(tags={"calendar"})
    async def home_assistant_calendar(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_calendars', 'get_calendar_events'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant calendar operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["list_calendars", "get_calendar_events"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_panels_tools(mcp: FastMCP):
    """Register panels tools."""

    @mcp.tool(tags={"panels"})
    async def home_assistant_panels(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_panels'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant panels operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["get_panels"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_voice_tools(mcp: FastMCP):
    """Register voice tools."""

    @mcp.tool(tags={"voice"})
    async def home_assistant_voice(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_exposed_entities', 'expose_entities'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant voice operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["list_exposed_entities", "expose_entities"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_entities_tools(mcp: FastMCP):
    """Register entities tools."""

    @mcp.tool(tags={"entities"})
    async def home_assistant_entities(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_entity_registry_display', 'extract_from_target', 'get_triggers_for_target', 'get_conditions_for_target', 'get_services_for_target'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant entities operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = [
            "get_entity_registry_display",
            "extract_from_target",
            "get_triggers_for_target",
            "get_conditions_for_target",
            "get_services_for_target",
        ]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_system_tools(mcp: FastMCP):
    """Register system tools."""

    @mcp.tool(tags={"system"})
    async def home_assistant_system(
        action: str = Field(
            description="Action to perform. Must be one of: 'render_template', 'ping', 'handle_intent', 'validate_config'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> Any:
        """Manage home assistant system operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["render_template", "ping", "handle_intent", "validate_config"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        return await run_blocking(getattr(client, action), **kwargs)
def register_kg_tools(mcp: FastMCP):
    """Register native epistemic-graph ingestion tools (Wire-First).

    CONCEPT:AU-KG.ingest.enterprise-source-extractor. Lists Home Assistant records via
    the real client and pushes them into the knowledge graph as typed :Entity/:Device/
    :Area/:SensorReading nodes + links. Best-effort: no-ops (``"ingested": None``) when
    no engine is reachable.
    """

    @mcp.tool(tags={"kg"})
    async def home_ingest_states(
        with_readings: bool = Field(
            default=True,
            description="Also emit a :SensorReading timeseries node per entity state.",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest all Home Assistant entity states into epistemic-graph.

        Lists live states via the HA API and pushes them as typed :Entity nodes (plus a
        :SensorReading ``:readingOf`` each entity when ``with_readings``) into the KG via
        the fast engine client. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if ctx:
            await ctx.info("Ingesting Home Assistant states into the KG...")
        from home_assistant_agent.kg_ingest import ingest_states

        states = await run_blocking(client.list_states)
        records = states if isinstance(states, list) else [states]
        result = ingest_states(records, with_readings=with_readings)
        return {"listed": len(records), "ingested": result}

    @mcp.tool(tags={"kg"})
    async def home_ingest_history(
        entity_id: str = Field(
            description="entity_id whose history/period series to ingest as :SensorReading timeseries."
        ),
        timestamp: str | None = Field(
            default=None, description="ISO-8601 start time for the history window."
        ),
        end_time: str | None = Field(
            default=None, description="ISO-8601 end time for the history window."
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest a Home Assistant history series for one entity as timeseries readings.

        Pulls ``get_history`` for the entity and pushes each point as a :SensorReading
        node ``:readingOf`` its :Entity. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if ctx:
            await ctx.info(f"Ingesting history for {entity_id} into the KG...")
        from home_assistant_agent.kg_ingest import ingest_history

        series = await run_blocking(
            client.get_history,
            entity_id=entity_id,
            timestamp=timestamp,
            end_time=end_time,
        )
        # get_history returns list[list[HAState]] (one inner list per entity); flatten.
        points: list[Any] = []
        for group in series or []:
            if isinstance(group, list):
                points.extend(group)
            else:
                points.append(group)
        result = ingest_history(entity_id, points)
        return {"points": len(points), "ingested": result}


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="home-assistant-agent MCP",
        version=__version__,
        instructions="home-assistant-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    register_tool_surface(
        mcp,
        client_cls=HomeAssistantApi,
        get_client=get_client,
        service="home-assistant-agent",
        tools_module=sys.modules[__name__],
    )

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    """Run the MCP server."""
    mcp, args, middlewares = get_mcp_instance()
    print(f"home-assistant-agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    if "pytest" not in sys.modules:
        mcp_server()
