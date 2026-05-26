from websockets.sync.client import connect

from home_assistant_agent.api import Api as HomeAssistantApi

__all__ = ["HomeAssistantApi", "connect"]
