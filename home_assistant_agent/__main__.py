#!/usr/bin/python
"""Main entry point for running the Home Assistant MCP server.

CONCEPT:AU-OS.safety.doom-loop-detection
"""

from home_assistant_agent.mcp_server import mcp_server

if __name__ == "__main__":
    mcp_server()
