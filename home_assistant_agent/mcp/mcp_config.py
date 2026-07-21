"""MCP tools for config operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from home_assistant_agent.auth import get_client


def register_config_tools(mcp: FastMCP):
    """Register config tools. CONCEPT:AU-ECO.messaging.native-backend-abstraction"""

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

        CONCEPT:AU-ECO.messaging.native-backend-abstraction
        """
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["status", "config", "components", "check_config"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "status":
            return await run_blocking(client.status, **kwargs)
        if action == "config":
            return await run_blocking(client.config, **kwargs)
        if action == "components":
            return await run_blocking(client.components, **kwargs)
        if action == "check_config":
            return await run_blocking(client.check_config, **kwargs)
        raise ValueError(f"Unknown action: {action}")
