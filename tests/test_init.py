from fastmcp import FastMCP
from home_assistant_agent.mcp_server import get_mcp_instance

def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully."""
    mcp, args, middlewares, registered_tags = get_mcp_instance()
    assert isinstance(mcp, FastMCP)
    assert "home-assistant" in mcp.name

def test_import_home_assistant_agent():
    """Test that the package can be imported."""
    import home_assistant_agent
    assert home_assistant_agent.__version__ is not None
