"""MCP tools for system operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from typing import Any

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from home_assistant_agent.auth import get_client


def register_system_tools(mcp: FastMCP):
    """Register system tools. CONCEPT:AU-ECO.messaging.native-backend-abstraction"""

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

        valid_actions = ["render_template", "ping", "handle_intent", "validate_config"]
        resolved = resolve_action(action, valid_actions, service="home-assistant-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "render_template":
            return await run_blocking(client.render_template, **kwargs)
        if action == "ping":
            return await run_blocking(client.ping, **kwargs)
        if action == "handle_intent":
            return await run_blocking(client.handle_intent, **kwargs)
        if action == "validate_config":
            return await run_blocking(client.validate_config, **kwargs)
        raise ValueError(f"Unknown action: {action}")
