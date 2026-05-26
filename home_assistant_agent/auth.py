#!/usr/bin/python
import os

import urllib3

from home_assistant_agent.api_client import HomeAssistantApi

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from agent_utilities.core.exceptions import AuthError, UnauthorizedError

_client = None


def get_client():
    """Get or create a singleton API client instance.

    CONCEPT:OS-5.1
    """
    global _client
    if _client is None:
        base_url = os.getenv("HOME_ASSISTANT_URL", "http://localhost:8123")
        token = os.getenv("HOME_ASSISTANT_TOKEN", "")
        verify_env = (
            os.getenv("HOME_ASSISTANT_SSL_VERIFY")
            or os.getenv("HOME_ASSISTANT_AGENT_VERIFY")
            or "True"
        )
        verify = verify_env.lower() in (
            "true",
            "1",
            "yes",
        )

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
