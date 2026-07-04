"""MCP tools for voice operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from home_assistant_agent.auth import get_client


def register_voice_tools(mcp: FastMCP):
    """Register voice tools. CONCEPT:AU-ECO.messaging.native-backend-abstraction"""

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

        valid_actions = ["list_exposed_entities", "expose_entities"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_exposed_entities":
            return await run_blocking(client.list_exposed_entities, **kwargs)
        if action == "expose_entities":
            return await run_blocking(client.expose_entities, **kwargs)
        raise ValueError(f"Unknown action: {action}")
