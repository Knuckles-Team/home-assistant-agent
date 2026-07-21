#!/usr/bin/python

from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

from home_assistant_agent.api_client import HomeAssistantApi

_client = None


def get_client():
    """Get or create a singleton API client instance.

    CONCEPT:AU-OS.config.secrets-authentication
    """
    global _client
    if _client is None:
        base_url = setting("HOME_ASSISTANT_URL", "http://localhost:8123")
        token = setting("HOME_ASSISTANT_TOKEN", "")
        try:
            _client = HomeAssistantApi(
                base_url=base_url,
                token=token,
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                "AUTHENTICATION ERROR: The configured credentials were rejected. "
                f"Please check your HOME_ASSISTANT_TOKEN and HOME_ASSISTANT_URL environment variables. "
                f"Error details: {type(e).__name__}"
            ) from e

    return _client
