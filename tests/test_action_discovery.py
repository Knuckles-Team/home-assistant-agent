"""Tests for standardized action discovery via the shared agent-connector-sdk helper.

CONCEPT:AU-ECO.messaging.native-backend-abstraction
"""

from unittest.mock import MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_one_typed_tool_per_client_operation():
    """Every public client operation is its own typed, annotated MCP tool.

    CONCEPT:AU-ECO.messaging.native-backend-abstraction
    """
    from agent_connector_sdk.mcp.action_dispatch import public_actions

    from home_assistant_agent.api import Api
    from home_assistant_agent.mcp_server import get_mcp_instance

    with patch("home_assistant_agent.auth.get_client", return_value=MagicMock()):
        mcp, _, _ = get_mcp_instance()
    tools = {tool.name: tool for tool in await mcp.local_provider.list_tools()}
    operations = {
        f"home_assistant_{name}"
        for name in public_actions(Api)
        if name not in {"close", "get_api_status"}
    }
    assert operations <= set(tools)
    assert len(operations) == 41
    assert not [
        name
        for name, tool in tools.items()
        if "action" in tool.parameters.get("properties", {}) and name not in operations
    ]
    state = tools["home_assistant_get_state"]
    assert state.parameters["required"] == ["entity_id"]
    assert state.annotations.read_only_hint is True
    assert tools["home_assistant_delete_state"].annotations.destructive_hint is True
