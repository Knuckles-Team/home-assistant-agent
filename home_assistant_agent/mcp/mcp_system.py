"""MCP tools for system operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from home_assistant_agent.auth import get_client


def register_system_tools(mcp: FastMCP):
    """Register system tools. CONCEPT:ECO-4.0"""

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

        if action == "render_template":
            return client.render_template(**kwargs)
        if action == "ping":
            return client.ping(**kwargs)
        if action == "handle_intent":
            return client.handle_intent(**kwargs)
        if action == "validate_config":
            return client.validate_config(**kwargs)
        raise ValueError(f"Unknown action: {action}")
