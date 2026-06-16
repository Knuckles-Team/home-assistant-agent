"""Tests for standardized action discovery via the shared agent-utilities helper.

CONCEPT:ECO-4.0
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from mcp.shared.exceptions import McpError


@pytest.mark.asyncio
async def test_list_actions_and_did_you_mean():
    """list_actions returns the bounded action names; a bogus action raises guidance.

    CONCEPT:ECO-4.0
    """
    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware

    from home_assistant_agent.mcp_server import get_mcp_instance

    async def mock_on_request(self, context, call_next):
        return await call_next(context)

    async def mock_info(*args, **kwargs):
        pass

    with (
        patch.object(RateLimitingMiddleware, "on_request", mock_on_request),
        patch("fastmcp.Context.info", mock_info),
        patch("home_assistant_agent.auth.get_client", return_value=MagicMock()),
    ):
        mcp, _, _ = get_mcp_instance()

        # Discovery keyword returns the bounded action set for this tool.
        res = await mcp.call_tool("home_assistant_states", {"action": "list_actions"})
        payload = getattr(res, "structured_content", None) or res
        text = json.dumps(payload, default=str)
        assert "list_states" in text
        assert "get_state" in text

        # Unknown action raises a rich error pointing at list_actions.
        with pytest.raises(McpError, match="list_actions"):
            await mcp.call_tool(
                "home_assistant_states", {"action": "totally_bogus_action"}
            )
