"""MCP tools for config operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from home_assistant_agent.auth import get_client


def register_config_tools(mcp: FastMCP):
    """Register config tools. CONCEPT:ECO-4.0"""

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

        if action == "status":
            return client.status(**kwargs)
        if action == "config":
            return client.config(**kwargs)
        if action == "components":
            return client.components(**kwargs)
        if action == "check_config":
            return client.check_config(**kwargs)
        raise ValueError(f"Unknown action: {action}")
