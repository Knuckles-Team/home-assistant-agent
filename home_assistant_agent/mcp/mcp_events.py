"""MCP tools for events operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from home_assistant_agent.auth import get_client


def register_events_tools(mcp: FastMCP):
    """Register events tools. CONCEPT:ECO-4.0"""

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

        if action == "list_events":
            return client.list_events(**kwargs)
        if action == "fire_event":
            return client.fire_event(**kwargs)
        if action == "subscribe_events":
            return client.subscribe_events(**kwargs)
        raise ValueError(f"Unknown action: {action}")
