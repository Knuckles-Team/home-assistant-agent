import json
import logging
from typing import Any

import requests
import urllib3
from agent_utilities.core.exceptions import ApiError, UnauthorizedError
from websockets.exceptions import ConnectionClosed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


class BaseApiClient:
    def __init__(self, base_url: str, token: str, verify: bool = True):
        self.raw_url = base_url.rstrip("/")
        self.base_url = self.raw_url
        if not self.base_url.endswith("/api"):
            self.base_url = f"{self.base_url}/api"

        self.token = token
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }
        )
        self.session.verify = self.verify
        self.headers = self.session.headers
        self._message_id = 1

        try:
            self.get_api_status()
        except Exception as e:
            if isinstance(e, UnauthorizedError):
                raise e

    def get_api_status(self) -> dict[str, str]:
        response = self.session.get(f"{self.base_url}/")
        if response.status_code == 401:
            raise UnauthorizedError("Invalid token")
        response.raise_for_status()
        return response.json()

    def _ws_call(self, message: dict[str, Any]) -> Any:
        from home_assistant_agent.api_client import connect

        ws_url = self.raw_url.replace("http", "ws", 1) + "/api/websocket"
        try:
            with connect(ws_url) as websocket:
                # 1. Wait for auth_required
                greeting = json.loads(websocket.recv())
                if greeting.get("type") != "auth_required":
                    raise ApiError(f"Unexpected WS greeting: {greeting}")

                # 2. Authenticate
                websocket.send(json.dumps({"type": "auth", "access_token": self.token}))
                auth_resp = json.loads(websocket.recv())
                if auth_resp.get("type") != "auth_ok":
                    raise UnauthorizedError(
                        f"WS Auth failed: {auth_resp.get('message')}"
                    )

                # 3. Send command
                message["id"] = self._message_id
                self._message_id += 1
                websocket.send(json.dumps(message))

                # 4. Wait for result
                while True:
                    resp = json.loads(websocket.recv())
                    if resp.get("type") == "result":
                        if not resp.get("success"):
                            raise ApiError(f"WS Command failed: {resp.get('error')}")
                        return resp.get("result")
                    elif resp.get("type") == "pong":
                        return "pong"
                    elif resp.get("type") in ["event", "auth_invalid"]:
                        return resp
        except ConnectionClosed as e:
            raise ApiError(f"WS Connection closed: {str(e)}") from e
        except Exception as e:
            raise ApiError(f"WS Error: {str(e)}") from e
