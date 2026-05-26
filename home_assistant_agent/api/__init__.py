from home_assistant_agent.api.api_client_rest import Api as RestApi
from home_assistant_agent.api.api_client_websocket import Api as WebsocketApi


class Api(RestApi, WebsocketApi):
    """Unified Home Assistant API Client combining decomposed sub-clients."""
