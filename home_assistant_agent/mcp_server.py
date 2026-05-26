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
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

from home_assistant_agent.auth import get_client

__version__ = "0.15.0"

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
        """Manage home assistant config operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "status":
            return client.status(**kwargs)
        if action == "config":
            return client.config(**kwargs)
        if action == "components":
            return client.components(**kwargs)
        if action == "check_config":
            return client.check_config(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant states operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_states":
            return client.list_states(**kwargs)
        if action == "get_state":
            return client.get_state(**kwargs)
        if action == "update_state":
            return client.update_state(**kwargs)
        if action == "delete_state":
            return client.delete_state(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant services operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_services":
            return client.list_services(**kwargs)
        if action == "call_service":
            return client.call_service(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant events operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_events":
            return client.list_events(**kwargs)
        if action == "fire_event":
            return client.fire_event(**kwargs)
        if action == "subscribe_events":
            return client.subscribe_events(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant history operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_history":
            return client.get_history(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant logbook operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_logbook":
            return client.get_logbook(**kwargs)
        if action == "get_error_log":
            return client.get_error_log(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant calendar operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_calendars":
            return client.list_calendars(**kwargs)
        if action == "get_calendar_events":
            return client.get_calendar_events(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant panels operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_panels":
            return client.get_panels(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant voice operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_exposed_entities":
            return client.list_exposed_entities(**kwargs)
        if action == "expose_entities":
            return client.expose_entities(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant entities operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_entity_registry_display":
            return client.get_entity_registry_display(**kwargs)
        if action == "extract_from_target":
            return client.extract_from_target(**kwargs)
        if action == "get_triggers_for_target":
            return client.get_triggers_for_target(**kwargs)
        if action == "get_conditions_for_target":
            return client.get_conditions_for_target(**kwargs)
        if action == "get_services_for_target":
            return client.get_services_for_target(**kwargs)
        raise ValueError(f"Unknown action: {action}")

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
        """Manage home assistant system operations.
"""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "render_template":
            return client.render_template(**kwargs)
        if action == "ping":
            return client.ping(**kwargs)
        if action == "handle_intent":
            return client.handle_intent(**kwargs)
        if action == "validate_config":
            return client.validate_config(**kwargs)
        raise ValueError(f"Unknown action: {action}")

def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance.
"""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="home-assistant-agent MCP",
        version=__version__,
        instructions="home-assistant-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_CONFIGTOOL = to_boolean(os.getenv("CONFIGTOOL", "True"))
    if DEFAULT_CONFIGTOOL:
        register_config_tools(mcp)
    DEFAULT_STATESTOOL = to_boolean(os.getenv("STATESTOOL", "True"))
    if DEFAULT_STATESTOOL:
        register_states_tools(mcp)
    DEFAULT_SERVICESTOOL = to_boolean(os.getenv("SERVICESTOOL", "True"))
    if DEFAULT_SERVICESTOOL:
        register_services_tools(mcp)
    DEFAULT_EVENTSTOOL = to_boolean(os.getenv("EVENTSTOOL", "True"))
    if DEFAULT_EVENTSTOOL:
        register_events_tools(mcp)
    DEFAULT_HISTORYTOOL = to_boolean(os.getenv("HISTORYTOOL", "True"))
    if DEFAULT_HISTORYTOOL:
        register_history_tools(mcp)
    DEFAULT_LOGBOOKTOOL = to_boolean(os.getenv("LOGBOOKTOOL", "True"))
    if DEFAULT_LOGBOOKTOOL:
        register_logbook_tools(mcp)
    DEFAULT_CALENDARTOOL = to_boolean(os.getenv("CALENDARTOOL", "True"))
    if DEFAULT_CALENDARTOOL:
        register_calendar_tools(mcp)
    DEFAULT_PANELSTOOL = to_boolean(os.getenv("PANELSTOOL", "True"))
    if DEFAULT_PANELSTOOL:
        register_panels_tools(mcp)
    DEFAULT_VOICETOOL = to_boolean(os.getenv("VOICETOOL", "True"))
    if DEFAULT_VOICETOOL:
        register_voice_tools(mcp)
    DEFAULT_ENTITIESTOOL = to_boolean(os.getenv("ENTITIESTOOL", "True"))
    if DEFAULT_ENTITIESTOOL:
        register_entities_tools(mcp)
    DEFAULT_SYSTEMTOOL = to_boolean(os.getenv("SYSTEMTOOL", "True"))
    if DEFAULT_SYSTEMTOOL:
        register_system_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares

def mcp_server() -> None:
    """Run the MCP server.
"""
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