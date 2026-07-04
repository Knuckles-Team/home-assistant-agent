"""MCP tools for events operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from home_assistant_agent.auth import get_client


def register_events_tools(mcp: FastMCP):
    """Register events tools. CONCEPT:AU-ECO.messaging.native-backend-abstraction"""

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

        CONCEPT:AU-ECO.messaging.native-backend-abstraction
        """
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["list_events", "fire_event", "subscribe_events"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_events":
            return await run_blocking(client.list_events, **kwargs)
        if action == "fire_event":
            return await run_blocking(client.fire_event, **kwargs)
        if action == "subscribe_events":
            return await run_blocking(client.subscribe_events, **kwargs)
        raise ValueError(f"Unknown action: {action}")
