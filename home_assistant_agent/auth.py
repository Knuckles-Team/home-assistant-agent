#!/usr/bin/python
import urllib3

from home_assistant_agent.api_client import HomeAssistantApi

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError

_client = None


def get_client():
    """Get or create a singleton API client instance.

    CONCEPT:AU-OS.config.secrets-authentication
    """
    global _client
    if _client is None:
        base_url = setting("HOME_ASSISTANT_URL", "http://localhost:8123")
        token = setting("HOME_ASSISTANT_TOKEN", "")
        if setting("HOME_ASSISTANT_SSL_VERIFY", None) is not None:
            verify = setting("HOME_ASSISTANT_SSL_VERIFY", True)
        else:
            verify = setting("HOME_ASSISTANT_AGENT_VERIFY", True)

        try:
            _client = HomeAssistantApi(
                base_url=base_url,
                token=token,
                verify=verify,
            )
        except (AuthError, UnauthorizedError) as e:
            raise RuntimeError(
                f"AUTHENTICATION ERROR: The credentials provided are not valid for '{base_url}'. "
                f"Please check your HOME_ASSISTANT_TOKEN and HOME_ASSISTANT_URL environment variables. "
                f"Error details: {str(e)}"
            ) from e

    return _client
