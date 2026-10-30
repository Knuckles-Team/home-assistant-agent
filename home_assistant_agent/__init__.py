#!/usr/bin/env python

from scion_sdk.connector import Connector

from home_assistant_agent.api_client import HomeAssistantApi
from home_assistant_agent.auth import get_client

connector = Connector(
    api=HomeAssistantApi,
    get_client=get_client,
    tools="home_assistant_agent.mcp_server",
    instructions="home-assistant-agent MCP Server — one tool per API operation.",
)
