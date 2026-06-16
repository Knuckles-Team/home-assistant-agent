"""MCP tools for entities operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from home_assistant_agent.auth import get_client


def register_entities_tools(mcp: FastMCP):
    """Register entities tools. CONCEPT:ECO-4.0"""

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

        CONCEPT:ECO-4.0
        """
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

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
