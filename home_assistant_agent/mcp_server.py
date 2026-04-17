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

# General urllib3/chardet mismatch warnings
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import os
import sys
import logging
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv, find_dotenv
from fastmcp import FastMCP
from agent_utilities.base_utilities import to_boolean, get_logger
from agent_utilities.mcp_utilities import create_mcp_server
from home_assistant_agent.auth import get_client

__version__ = "0.2.1"

logger = get_logger(name="MCP_Server")
logger.setLevel(logging.INFO)


def register_config_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-status",
        description="Check if Home Assistant API is up and running.",
        tags={"config"},
    )
    def ha_status() -> Dict[str, str]:
        return get_client().get_api_status()

    @mcp.tool(
        name="ha-config",
        description="Get Home Assistant configuration.",
        tags={"config"},
    )
    def ha_config() -> Dict[str, Any]:
        return get_client().get_config().model_dump()

    @mcp.tool(
        name="ha-components",
        description="List currently loaded components.",
        tags={"config"},
    )
    def ha_components() -> List[str]:
        return get_client().get_components()

    @mcp.tool(
        name="ha-check-config",
        description="Trigger a check of configuration.yaml.",
        tags={"config"},
    )
    def ha_check_config() -> Dict[str, Any]:
        return get_client().check_config()


def register_states_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-list-states",
        description="Return a list of all entity states.",
        tags={"states"},
    )
    def ha_list_states() -> List[Dict[str, Any]]:
        return [s.model_dump() for s in get_client().get_states()]

    @mcp.tool(
        name="ha-get-state",
        description="Return the state of a specific entity.",
        tags={"states"},
    )
    def ha_get_state(entity_id: str) -> Dict[str, Any]:
        return get_client().get_state(entity_id).model_dump()

    @mcp.tool(
        name="ha-update-state",
        description="Updates or creates a state for an entity (internal representation).",
        tags={"states"},
    )
    def ha_update_state(
        entity_id: str, state: str, attributes: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return get_client().update_state(entity_id, state, attributes).model_dump()

    @mcp.tool(
        name="ha-delete-state",
        description="Deletes an entity state.",
        tags={"states"},
    )
    def ha_delete_state(entity_id: str) -> Dict[str, str]:
        return get_client().delete_state(entity_id)


def register_services_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-list-services",
        description="List all available services.",
        tags={"services"},
    )
    def ha_list_services() -> List[Dict[str, Any]]:
        return [s.model_dump() for s in get_client().get_services()]

    @mcp.tool(
        name="ha-call-service",
        description="Call a service (e.g., turn a light on).",
        tags={"services"},
    )
    def ha_call_service(
        domain: str,
        service: str,
        service_data: Optional[Dict[str, Any]] = None,
        return_response: bool = False,
    ) -> Any:
        return get_client().call_service(domain, service, service_data, return_response)


def register_events_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-list-events",
        description="List all event types and listener counts.",
        tags={"events"},
    )
    def ha_list_events() -> List[Dict[str, Any]]:
        return [e.model_dump() for e in get_client().get_events()]

    @mcp.tool(
        name="ha-fire-event",
        description="Fire an event on the Home Assistant event bus.",
        tags={"events"},
    )
    def ha_fire_event(
        event_type: str, event_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        return get_client().fire_event(event_type, event_data)

    @mcp.tool(
        name="ha-subscribe-events",
        description="Subscribe to events (one-shot check).",
        tags={"events"},
    )
    def ha_subscribe_events(event_type: Optional[str] = None) -> Any:
        return get_client().subscribe_events(event_type)


def register_history_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-get-history",
        description="Get history of one or more entities.",
        tags={"history"},
    )
    def ha_get_history(
        entity_id: str, timestamp: Optional[str] = None, end_time: Optional[str] = None
    ) -> List[List[Dict[str, Any]]]:
        history = get_client().get_history(entity_id, timestamp, end_time)
        return [[s.model_dump() for s in h] for h in history]


def register_logbook_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-get-logbook", description="Get logbook entries.", tags={"logbook"}
    )
    def ha_get_logbook(
        timestamp: Optional[str] = None,
        entity_id: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        return [
            e.model_dump()
            for e in get_client().get_logbook(timestamp, entity_id, end_time)
        ]

    @mcp.tool(
        name="ha-get-error-log",
        description="Retrieve all errors logged during the current session.",
        tags={"logbook"},
    )
    def ha_get_error_log() -> str:
        return get_client().get_error_log()


def register_calendar_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-list-calendars",
        description="List calendar entities.",
        tags={"calendar"},
    )
    def ha_list_calendars() -> List[Dict[str, Any]]:
        return [c.model_dump() for c in get_client().get_calendars()]

    @mcp.tool(
        name="ha-get-calendar-events",
        description="Get events for a calendar.",
        tags={"calendar"},
    )
    def ha_get_calendar_events(
        entity_id: str, start: str, end: str
    ) -> List[Dict[str, Any]]:
        return [
            e.model_dump()
            for e in get_client().get_calendar_events(entity_id, start, end)
        ]


def register_panels_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-get-panels",
        description="Get registered panels in Home Assistant.",
        tags={"panels"},
    )
    def ha_get_panels() -> List[Dict[str, Any]]:
        return [p.model_dump() for p in get_client().get_panels()]


def register_voice_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-list-exposed-entities",
        description="List exposure status of entities across all assistants.",
        tags={"voice"},
    )
    def ha_list_exposed_entities() -> Dict[str, Any]:
        return get_client().list_exposed_entities().model_dump()

    @mcp.tool(
        name="ha-expose-entities",
        description="Expose or unexpose entities to voice assistants.",
        tags={"voice"},
    )
    def ha_expose_entities(
        assistants: List[str], entity_ids: List[str], should_expose: bool
    ) -> Any:
        return get_client().expose_or_unexpose_entities(
            assistants, entity_ids, should_expose
        )


def register_entities_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-get-entity-registry-display",
        description="Get lightweight, optimized list of entity registry entries for UI display.",
        tags={"entities"},
    )
    def ha_get_entity_registry_display() -> Dict[str, Any]:
        return get_client().get_entity_registry_list_for_display().model_dump()

    @mcp.tool(
        name="ha-extract-from-target",
        description="Extract entities, devices, and areas from one or multiple targets.",
        tags={"entities"},
    )
    def ha_extract_from_target(
        target: Dict[str, Any], expand_group: bool = False
    ) -> Dict[str, Any]:
        return get_client().extract_from_target(target, expand_group).model_dump()

    @mcp.tool(
        name="ha-get-triggers-for-target",
        description="Get applicable triggers for entities of a given target.",
        tags={"entities"},
    )
    def ha_get_triggers_for_target(
        target: Dict[str, Any], expand_group: bool = True
    ) -> List[str]:
        return get_client().get_triggers_for_target(target, expand_group)

    @mcp.tool(
        name="ha-get-conditions-for-target",
        description="Get applicable conditions for entities of a given target.",
        tags={"entities"},
    )
    def ha_get_conditions_for_target(
        target: Dict[str, Any], expand_group: bool = True
    ) -> List[str]:
        return get_client().get_conditions_for_target(target, expand_group)

    @mcp.tool(
        name="ha-get-services-for-target",
        description="Get applicable services for entities of a given target.",
        tags={"entities"},
    )
    def ha_get_services_for_target(
        target: Dict[str, Any], expand_group: bool = True
    ) -> List[str]:
        return get_client().get_services_for_target(target, expand_group)


def register_system_tools(mcp: FastMCP):
    @mcp.tool(
        name="ha-render-template",
        description="Render a Home Assistant template.",
        tags={"system"},
    )
    def ha_render_template(template: str) -> str:
        return get_client().render_template(template)

    @mcp.tool(
        name="ha-ping",
        description="Ping the Home Assistant WebSocket API.",
        tags={"system"},
    )
    def ha_ping() -> str:
        return get_client().ping()

    @mcp.tool(
        name="ha-handle-intent",
        description="Handle an intent in Home Assistant.",
        tags={"system"},
    )
    def ha_handle_intent(
        name: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return get_client().handle_intent(name, data)

    @mcp.tool(
        name="ha-validate-config",
        description="Validate triggers, conditions, and action configurations.",
        tags={"system"},
    )
    def ha_validate_config(
        trigger: Optional[Any] = None,
        condition: Optional[Any] = None,
        action: Optional[Any] = None,
    ) -> Dict[str, Any]:
        return get_client().validate_config(trigger, condition, action).model_dump()


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

    tool_groups = [
        ("CONFIG", register_config_tools, "config"),
        ("STATES", register_states_tools, "states"),
        ("SERVICES", register_services_tools, "services"),
        ("EVENTS", register_events_tools, "events"),
        ("HISTORY", register_history_tools, "history"),
        ("LOGBOOK", register_logbook_tools, "logbook"),
        ("CALENDAR", register_calendar_tools, "calendar"),
        ("PANELS", register_panels_tools, "panels"),
        ("VOICE", register_voice_tools, "voice"),
        ("ENTITIES", register_entities_tools, "entities"),
        ("SYSTEM", register_system_tools, "system"),
    ]

    for env_suffix, register_func, tag in tool_groups:
        if to_boolean(os.getenv(f"{env_suffix}TOOL", "True")):
            register_func(mcp)
            registered_tags.append(tag)

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
