#!/usr/bin/python


import os
import sys
import logging
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv, find_dotenv
from fastmcp import FastMCP
from agent_utilities.base_utilities import to_boolean, get_logger
from agent_utilities.mcp_utilities import create_mcp_server
from home_assistant_agent.auth import get_client

__version__ = "0.1.4"


logger = get_logger(name="MCP_Server")
logger.setLevel(logging.INFO)


def register_config_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-status", description="Check if Home Assistant API is up and running."
    )
    def ha_status() -> Dict[str, str]:
        return get_client().get_api_status()

    @mcp.tool(name="ha-config", description="Get Home Assistant configuration.")
    def ha_config() -> Dict[str, Any]:
        return get_client().get_config().model_dump()

    @mcp.tool(name="ha-components", description="List currently loaded components.")
    def ha_components() -> List[str]:
        return get_client().get_config().components


def register_states_tools(mcp: FastMCP):
    @mcp.tool(name="ha-list-states", description="Return a list of all entity states.")
    def ha_list_states() -> List[Dict[str, Any]]:
        return [s.model_dump() for s in get_client().get_states()]

    @mcp.tool(name="ha-get-state", description="Return the state of a specific entity.")
    def ha_get_state(entity_id: str) -> Dict[str, Any]:
        return get_client().get_state(entity_id).model_dump()


def register_services_tools(mcp: FastMCP):
    @mcp.tool(name="ha-list-services", description="List all available services.")
    def ha_list_services() -> List[Dict[str, Any]]:
        return [s.model_dump() for s in get_client().get_services()]

    @mcp.tool(
        name="ha-call-service", description="Call a service (e.g., turn a light on)."
    )
    def ha_call_service(
        domain: str, service: str, service_data: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return [
            s.model_dump()
            for s in get_client().call_service(domain, service, service_data)
        ]


def register_events_tools(mcp: FastMCP):
    @mcp.tool(name="ha-list-events", description="List all event types.")
    def ha_list_events() -> List[Dict[str, Any]]:
        return [e.model_dump() for e in get_client().get_events()]

    @mcp.tool(name="ha-fire-event", description="Fire an event.")
    def ha_fire_event(
        event_type: str, event_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        return get_client().fire_event(event_type, event_data)


def register_history_tools(mcp: FastMCP):
    @mcp.tool(name="ha-get-history", description="Get history of one or more entities.")
    def ha_get_history(
        entity_id: str, timestamp: Optional[str] = None, end_time: Optional[str] = None
    ) -> List[List[Dict[str, Any]]]:
        history = get_client().get_history(entity_id, timestamp, end_time)
        return [[s.model_dump() for s in h] for h in history]


def register_logbook_tools(mcp: FastMCP):
    @mcp.tool(name="ha-get-logbook", description="Get logbook entries.")
    def ha_get_logbook(
        timestamp: Optional[str] = None,
        entity_id: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        return [
            e.model_dump()
            for e in get_client().get_logbook(timestamp, entity_id, end_time)
        ]


def register_calendar_tools(mcp: FastMCP):
    @mcp.tool(name="ha-list-calendars", description="List calendar entities.")
    def ha_list_calendars() -> List[Dict[str, Any]]:
        return [c.model_dump() for c in get_client().get_calendars()]

    @mcp.tool(name="ha-get-calendar-events", description="Get events for a calendar.")
    def ha_get_calendar_events(
        entity_id: str, start: str, end: str
    ) -> List[Dict[str, Any]]:
        return [
            e.model_dump()
            for e in get_client().get_calendar_events(entity_id, start, end)
        ]


def register_prompts(mcp: FastMCP):
    @mcp.prompt(
        name="ha-status-check",
        description="Ask the agent to check the status and summary of Home Assistant.",
    )
    def ha_status_check() -> str:
        return "Check the status of Home Assistant, list loaded components, and summarize the current state of major entities (lights, switches, sensors)."


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Initialize and return the Home Assistant Agent MCP instance, args, and middlewares."""
    load_dotenv(find_dotenv())

    args, mcp, middlewares = create_mcp_server(
        name="home-assistant",
        version=__version__,
        instructions="Home Assistant Agent MCP Server",
    )

    registered_tags = []

    if to_boolean(os.getenv("CONFIGTOOL", "True")):
        register_config_tools(mcp)
        registered_tags.append("config")

    if to_boolean(os.getenv("STATESTOOL", "True")):
        register_states_tools(mcp)
        registered_tags.append("states")

    if to_boolean(os.getenv("SERVICESTOOL", "True")):
        register_services_tools(mcp)
        registered_tags.append("services")

    if to_boolean(os.getenv("EVENTSTOOL", "True")):
        register_events_tools(mcp)
        registered_tags.append("events")

    if to_boolean(os.getenv("HISTORYTOOL", "True")):
        register_history_tools(mcp)
        registered_tags.append("history")

    if to_boolean(os.getenv("LOGBOOKTOOL", "True")):
        register_logbook_tools(mcp)
        registered_tags.append("logbook")

    if to_boolean(os.getenv("CALENDARTOOL", "True")):
        register_calendar_tools(mcp)
        registered_tags.append("calendar")

    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server():
    mcp, args, middlewares, registered_tags = get_mcp_instance()

    print(f"Home Assistant Agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {registered_tags}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
