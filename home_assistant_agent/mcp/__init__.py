"""MCP tool registration modules for home-assistant-agent.

Auto-generated during ecosystem standardization.
Each domain has its own module with a register_*_tools function.
"""

from home_assistant_agent.mcp.mcp_calendar import register_calendar_tools
from home_assistant_agent.mcp.mcp_config import register_config_tools
from home_assistant_agent.mcp.mcp_entities import register_entities_tools
from home_assistant_agent.mcp.mcp_events import register_events_tools
from home_assistant_agent.mcp.mcp_history import register_history_tools
from home_assistant_agent.mcp.mcp_logbook import register_logbook_tools
from home_assistant_agent.mcp.mcp_panels import register_panels_tools
from home_assistant_agent.mcp.mcp_services import register_services_tools
from home_assistant_agent.mcp.mcp_states import register_states_tools
from home_assistant_agent.mcp.mcp_system import register_system_tools
from home_assistant_agent.mcp.mcp_voice import register_voice_tools

__all__ = [
    "register_calendar_tools",
    "register_config_tools",
    "register_entities_tools",
    "register_events_tools",
    "register_history_tools",
    "register_logbook_tools",
    "register_panels_tools",
    "register_services_tools",
    "register_states_tools",
    "register_system_tools",
    "register_voice_tools",
]
