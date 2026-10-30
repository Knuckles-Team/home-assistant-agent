from fastmcp import FastMCP

from scion_sdk.connector import build_server


def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully.

    CONCEPT:AU-ECO.messaging.native-backend-abstraction
    """
    _, mcp = build_server("home_assistant_agent", command_args=[])
    assert isinstance(mcp, FastMCP)
    assert "home-assistant" in mcp.name
