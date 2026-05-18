#!/usr/bin/python
import warnings

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
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from home_assistant_agent.auth import get_client

__version__ = "0.12.0"

logger = get_logger(name="home-assistant-agent")
logger.setLevel(logging.INFO)


def register_config_tools(mcp: FastMCP):
    @mcp.tool(tags={"config"})
    async def home_assistant_config(
        action: str = Field(
            description="Action to perform. Must be one of: 'status', 'config', 'components', 'check_config'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage config operations.

        Actions:
          - 'status': Call status
          - 'config': Call config
          - 'components': Call components
          - 'check_config': Call check_config
        """
        kwargs: dict[str, Any]
        if action == "status":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.status(**kwargs)
        if action == "config":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.config(**kwargs)
        if action == "components":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.components(**kwargs)
        if action == "check_config":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.check_config(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: status', 'config', 'components', 'check_config"
        )


def register_states_tools(mcp: FastMCP):
    @mcp.tool(tags={"states"})
    async def home_assistant_states(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_states', 'get_state', 'update_state', 'delete_state'"
        ),
        entity_id: str | None = Field(default=None, description="entity id"),
        state: str | None = Field(default=None, description="state"),
        attributes: dict[str, Any] | None = Field(
            default=None, description="attributes"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage states operations.

        Actions:
          - 'list_states': Call list_states
          - 'get_state': Call get_state
          - 'update_state': Call update_state
          - 'delete_state': Call delete_state
        """
        kwargs: dict[str, Any]
        if action == "list_states":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_states(**kwargs)
        if action == "get_state":
            kwargs = {"entity_id": entity_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_state(**kwargs)
        if action == "update_state":
            kwargs = {
                "entity_id": entity_id,
                "state": state,
                "attributes": attributes,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_state(**kwargs)
        if action == "delete_state":
            kwargs = {"entity_id": entity_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_state(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_states', 'get_state', 'update_state', 'delete_state"
        )


def register_services_tools(mcp: FastMCP):
    @mcp.tool(tags={"services"})
    async def home_assistant_services(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_services', 'call_service'"
        ),
        domain: str | None = Field(default=None, description="domain"),
        service: str | None = Field(default=None, description="service"),
        service_data: dict[str, Any] | None = Field(
            default=None, description="service data"
        ),
        return_response: bool | None = Field(
            default=None, description="return response"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage services operations.

        Actions:
          - 'list_services': Call list_services
          - 'call_service': Call call_service
        """
        kwargs: dict[str, Any]
        if action == "list_services":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_services(**kwargs)
        if action == "call_service":
            kwargs = {
                "domain": domain,
                "service": service,
                "service_data": service_data,
                "return_response": return_response,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.call_service(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_services', 'call_service"
        )


def register_events_tools(mcp: FastMCP):
    @mcp.tool(tags={"events"})
    async def home_assistant_events(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_events', 'fire_event', 'subscribe_events'"
        ),
        event_type: Any | None = Field(default=None, description="event type"),
        event_data: dict[str, Any] | None = Field(
            default=None, description="event data"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage events operations.

        Actions:
          - 'list_events': Call list_events
          - 'fire_event': Call fire_event
          - 'subscribe_events': Call subscribe_events
        """
        kwargs: dict[str, Any]
        if action == "list_events":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_events(**kwargs)
        if action == "fire_event":
            kwargs = {
                "event_type": event_type,
                "event_data": event_data,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.fire_event(**kwargs)
        if action == "subscribe_events":
            kwargs = {"event_type": event_type}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.subscribe_events(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_events', 'fire_event', 'subscribe_events"
        )


def register_history_tools(mcp: FastMCP):
    @mcp.tool(tags={"history"})
    async def home_assistant_history(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_history'"
        ),
        entity_id: str | None = Field(default=None, description="entity id"),
        timestamp: str | None = Field(default=None, description="timestamp"),
        end_time: str | None = Field(default=None, description="end time"),
        client=Depends(get_client),
    ) -> dict:
        """Manage history operations.

        Actions:
          - 'get_history': Call get_history
        """
        kwargs: dict[str, Any]
        if action == "get_history":
            kwargs = {
                "entity_id": entity_id,
                "timestamp": timestamp,
                "end_time": end_time,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_history(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: get_history")


def register_logbook_tools(mcp: FastMCP):
    @mcp.tool(tags={"logbook"})
    async def home_assistant_logbook(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_logbook', 'get_error_log'"
        ),
        timestamp: str | None = Field(default=None, description="timestamp"),
        entity_id: str | None = Field(default=None, description="entity id"),
        end_time: str | None = Field(default=None, description="end time"),
        client=Depends(get_client),
    ) -> dict:
        """Manage logbook operations.

        Actions:
          - 'get_logbook': Call get_logbook
          - 'get_error_log': Call get_error_log
        """
        kwargs: dict[str, Any]
        if action == "get_logbook":
            kwargs = {
                "timestamp": timestamp,
                "entity_id": entity_id,
                "end_time": end_time,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_logbook(**kwargs)
        if action == "get_error_log":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_error_log(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_logbook', 'get_error_log"
        )


def register_calendar_tools(mcp: FastMCP):
    @mcp.tool(tags={"calendar"})
    async def home_assistant_calendar(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_calendars', 'get_calendar_events'"
        ),
        entity_id: str | None = Field(default=None, description="entity id"),
        start: str | None = Field(default=None, description="start"),
        end: str | None = Field(default=None, description="end"),
        client=Depends(get_client),
    ) -> dict:
        """Manage calendar operations.

        Actions:
          - 'list_calendars': Call list_calendars
          - 'get_calendar_events': Call get_calendar_events
        """
        kwargs: dict[str, Any]
        if action == "list_calendars":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_calendars(**kwargs)
        if action == "get_calendar_events":
            kwargs = {
                "entity_id": entity_id,
                "start": start,
                "end": end,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_calendar_events(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_calendars', 'get_calendar_events"
        )


def register_panels_tools(mcp: FastMCP):
    @mcp.tool(tags={"panels"})
    async def home_assistant_panels(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_panels'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage panels operations.

        Actions:
          - 'get_panels': Call get_panels
        """
        kwargs: dict[str, Any]
        if action == "get_panels":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_panels(**kwargs)
        raise ValueError(f"Unknown action: {action}. Must be one of: get_panels")


def register_voice_tools(mcp: FastMCP):
    @mcp.tool(tags={"voice"})
    async def home_assistant_voice(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_exposed_entities', 'expose_entities'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage voice operations.

        Actions:
          - 'list_exposed_entities': Call list_exposed_entities
          - 'expose_entities': Call expose_entities
        """
        kwargs: dict[str, Any]
        if action == "list_exposed_entities":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_exposed_entities(**kwargs)
        if action == "expose_entities":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.expose_entities(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_exposed_entities', 'expose_entities"
        )


def register_entities_tools(mcp: FastMCP):
    @mcp.tool(tags={"entities"})
    async def home_assistant_entities(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_entity_registry_display', 'extract_from_target', 'get_triggers_for_target', 'get_conditions_for_target', 'get_services_for_target'"
        ),
        target: dict[str, Any] | None = Field(default=None, description="target"),
        expand_group: bool | None = Field(default=None, description="expand group"),
        client=Depends(get_client),
    ) -> dict:
        """Manage entities operations.

        Actions:
          - 'get_entity_registry_display': Call get_entity_registry_display
          - 'extract_from_target': Call extract_from_target
          - 'get_triggers_for_target': Call get_triggers_for_target
          - 'get_conditions_for_target': Call get_conditions_for_target
          - 'get_services_for_target': Call get_services_for_target
        """
        kwargs: dict[str, Any]
        if action == "get_entity_registry_display":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_entity_registry_display(**kwargs)
        if action == "extract_from_target":
            kwargs = {"target": target, "expand_group": expand_group}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.extract_from_target(**kwargs)
        if action == "get_triggers_for_target":
            kwargs = {"target": target, "expand_group": expand_group}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_triggers_for_target(**kwargs)
        if action == "get_conditions_for_target":
            kwargs = {"target": target, "expand_group": expand_group}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_conditions_for_target(**kwargs)
        if action == "get_services_for_target":
            kwargs = {"target": target, "expand_group": expand_group}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_services_for_target(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_entity_registry_display', 'extract_from_target', 'get_triggers_for_target', 'get_conditions_for_target', 'get_services_for_target"
        )


def register_system_tools(mcp: FastMCP):
    @mcp.tool(tags={"system"})
    async def home_assistant_system(
        action: str = Field(
            description="Action to perform. Must be one of: 'render_template', 'ping', 'handle_intent', 'validate_config'"
        ),
        template: str | None = Field(default=None, description="template"),
        name: str | None = Field(default=None, description="name"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        trigger: Any | None = Field(default=None, description="trigger"),
        condition: Any | None = Field(default=None, description="condition"),
        action_data: Any | None = Field(default=None, description="action"),
        client=Depends(get_client),
    ) -> dict:
        """Manage system operations.

        Actions:
          - 'render_template': Call render_template
          - 'ping': Call ping
          - 'handle_intent': Call handle_intent
          - 'validate_config': Call validate_config
        """
        kwargs: dict[str, Any]
        if action == "render_template":
            kwargs = {"template": template}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.render_template(**kwargs)
        if action == "ping":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.ping(**kwargs)
        if action == "handle_intent":
            kwargs = {"name": name, "data": data}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.handle_intent(**kwargs)
        if action == "validate_config":
            kwargs = {
                "trigger": trigger,
                "condition": condition,
                "action": action_data,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.validate_config(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: render_template', 'ping', 'handle_intent', 'validate_config"
        )


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
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
    mcp_server()
