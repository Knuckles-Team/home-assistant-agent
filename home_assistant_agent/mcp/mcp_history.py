"""MCP tools for history operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from home_assistant_agent.auth import get_client


def register_history_tools(mcp: FastMCP):
    """Register history tools. CONCEPT:ECO-4.0"""

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

        if action == "get_history":
            return client.get_history(**kwargs)
        raise ValueError(f"Unknown action: {action}")
