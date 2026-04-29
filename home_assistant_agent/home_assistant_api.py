import json
import logging
from typing import Any

import requests
import urllib3
from agent_utilities.api_utilities import require_auth
from agent_utilities.exceptions import ApiError, ParameterError, UnauthorizedError
from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect

from .home_assistant_models import (
    HACalendar,
    HACalendarEvent,
    HAConfig,
    HAEntityRegistryDisplay,
    HAEvent,
    HAExposedEntities,
    HAExtractFromTargetResult,
    HALogbookEntry,
    HAPanel,
    HAService,
    HAState,
    HAValidateConfigResult,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)


class HomeAssistantApi:
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

    # --- REST API Methods ---

    @require_auth
    def get_config(self) -> HAConfig:
        response = self.session.get(f"{self.base_url}/config")
        response.raise_for_status()
        return HAConfig(**response.json())

    @require_auth
    def get_components(self) -> list[str]:
        response = self.session.get(f"{self.base_url}/components")
        response.raise_for_status()
        return response.json()

    @require_auth
    def get_states(self) -> list[HAState]:
        response = self.session.get(f"{self.base_url}/states")
        response.raise_for_status()
        return [HAState(**s) for s in response.json()]

    @require_auth
    def get_state(self, entity_id: str) -> HAState:
        response = self.session.get(f"{self.base_url}/states/{entity_id}")
        if response.status_code == 404:
            raise ParameterError(f"Entity {entity_id} not found")
        response.raise_for_status()
        return HAState(**response.json())

    @require_auth
    def update_state(
        self, entity_id: str, state: str, attributes: dict[str, Any] | None = None
    ) -> HAState:
        url = f"{self.base_url}/states/{entity_id}"
        data: dict[str, Any] = {"state": state}
        if attributes:
            data["attributes"] = attributes
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return HAState(**response.json())

    @require_auth
    def delete_state(self, entity_id: str) -> dict[str, str]:
        url = f"{self.base_url}/states/{entity_id}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()

    @require_auth
    def get_services(self) -> list[HAService]:
        response = self.session.get(f"{self.base_url}/services")
        response.raise_for_status()
        return [HAService(**s) for s in response.json()]

    @require_auth
    def get_events(self) -> list[HAEvent]:
        response = self.session.get(f"{self.base_url}/events")
        response.raise_for_status()
        return [HAEvent(**s) for s in response.json()]

    @require_auth
    def call_service(
        self,
        domain: str,
        service: str,
        service_data: dict[str, Any] | None = None,
        return_response: bool = False,
    ) -> list[HAState] | dict[str, Any]:
        url = f"{self.base_url}/services/{domain}/{service}"
        params: dict[str, Any] = {}
        if return_response:
            params["return_response"] = ""
        response = self.session.post(url, json=service_data or {}, params=params)
        response.raise_for_status()
        return response.json()

    @require_auth
    def fire_event(
        self, event_type: str, event_data: dict[str, Any] | None = None
    ) -> dict[str, str]:
        url = f"{self.base_url}/events/{event_type}"
        response = self.session.post(url, json=event_data or {})
        response.raise_for_status()
        return response.json()

    @require_auth
    def get_history(
        self,
        entity_id: str,
        timestamp: str | None = None,
        end_time: str | None = None,
    ) -> list[list[HAState]]:
        url = f"{self.base_url}/history/period"
        if timestamp:
            url = f"{url}/{timestamp}"

        params = {"filter_entity_id": entity_id}
        if end_time:
            params["end_time"] = end_time

        response = self.session.get(url, params=params)
        response.raise_for_status()

        return [
            [HAState(**s) for s in entity_history] for entity_history in response.json()
        ]

    @require_auth
    def get_logbook(
        self,
        timestamp: str | None = None,
        entity_id: str | None = None,
        end_time: str | None = None,
    ) -> list[HALogbookEntry]:
        url = f"{self.base_url}/logbook"
        if timestamp:
            url = f"{url}/{timestamp}"

        params: dict[str, Any] = {}
        if entity_id:
            params["entity"] = entity_id
        if end_time:
            params["end_time"] = end_time

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return [HALogbookEntry(**entry) for entry in response.json()]

    @require_auth
    def get_error_log(self) -> str:
        response = self.session.get(f"{self.base_url}/error_log")
        response.raise_for_status()
        return response.text

    @require_auth
    def get_camera_proxy(self, entity_id: str, time: str | None = None) -> bytes:
        url = f"{self.base_url}/camera_proxy/{entity_id}"
        params: dict[str, Any] = {}
        if time:
            params["time"] = time
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.content

    @require_auth
    def get_calendars(self) -> list[HACalendar]:
        response = self.session.get(f"{self.base_url}/calendars")
        response.raise_for_status()
        return [HACalendar(**c) for c in response.json()]

    @require_auth
    def get_calendar_events(
        self, entity_id: str, start: str, end: str
    ) -> list[HACalendarEvent]:
        url = f"{self.base_url}/calendars/{entity_id}"
        params = {"start": start, "end": end}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return [HACalendarEvent(**e) for e in response.json()]

    @require_auth
    def render_template(self, template: str) -> str:
        url = f"{self.base_url}/template"
        response = self.session.post(url, json={"template": template})
        response.raise_for_status()
        return response.text

    @require_auth
    def check_config(self) -> dict[str, Any]:
        url = f"{self.base_url}/config/core/check_config"
        response = self.session.post(url)
        response.raise_for_status()
        return response.json()

    @require_auth
    def handle_intent(
        self, name: str, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        url = f"{self.base_url}/intent/handle"
        response = self.session.post(url, json={"name": name, "data": data or {}})
        response.raise_for_status()
        return response.json()

    # --- WebSocket API Methods ---

    def _ws_call(self, message: dict[str, Any]) -> Any:
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

    @require_auth
    def get_panels(self) -> list[HAPanel]:
        res = self._ws_call({"type": "get_panels"})
        return [HAPanel(url_path=k, **v) for k, v in res.items()]

    @require_auth
    def ping(self) -> str:
        return self._ws_call({"type": "ping"})

    @require_auth
    def validate_config(
        self,
        trigger: Any | None = None,
        condition: Any | None = None,
        action: Any | None = None,
    ) -> HAValidateConfigResult:
        msg = {"type": "validate_config"}
        if trigger:
            msg["trigger"] = trigger
        if condition:
            msg["condition"] = condition
        if action:
            msg["action"] = action
        res = self._ws_call(msg)
        return HAValidateConfigResult(**res)

    @require_auth
    def extract_from_target(
        self, target: dict[str, Any], expand_group: bool = False
    ) -> HAExtractFromTargetResult:
        res = self._ws_call(
            {
                "type": "extract_from_target",
                "target": target,
                "expand_group": expand_group,
            }
        )
        return HAExtractFromTargetResult(**res)

    @require_auth
    def get_triggers_for_target(
        self, target: dict[str, Any], expand_group: bool = True
    ) -> list[str]:
        return self._ws_call(
            {
                "type": "get_triggers_for_target",
                "target": target,
                "expand_group": expand_group,
            }
        )

    @require_auth
    def get_conditions_for_target(
        self, target: dict[str, Any], expand_group: bool = True
    ) -> list[str]:
        return self._ws_call(
            {
                "type": "get_conditions_for_target",
                "target": target,
                "expand_group": expand_group,
            }
        )

    @require_auth
    def get_services_for_target(
        self, target: dict[str, Any], expand_group: bool = True
    ) -> list[str]:
        return self._ws_call(
            {
                "type": "get_services_for_target",
                "target": target,
                "expand_group": expand_group,
            }
        )

    @require_auth
    def get_entity_registry_list_for_display(self) -> HAEntityRegistryDisplay:
        res = self._ws_call({"type": "config/entity_registry/list_for_display"})
        return HAEntityRegistryDisplay(**res)

    @require_auth
    def list_exposed_entities(self) -> HAExposedEntities:
        res = self._ws_call({"type": "homeassistant/expose_entity/list"})
        return HAExposedEntities(**res)

    @require_auth
    def expose_or_unexpose_entities(
        self, assistants: list[str], entity_ids: list[str], should_expose: bool
    ) -> Any:
        return self._ws_call(
            {
                "type": "homeassistant/expose_entity",
                "assistants": assistants,
                "entity_ids": entity_ids,
                "should_expose": should_expose,
            }
        )

    @require_auth
    def subscribe_events(self, event_type: str | None = None) -> Any:
        msg = {"type": "subscribe_events"}
        if event_type:
            msg["event_type"] = event_type
        return self._ws_call(msg)

    @require_auth
    def subscribe_trigger(self, trigger: Any) -> Any:
        return self._ws_call({"type": "subscribe_trigger", "trigger": trigger})

    @require_auth
    def unsubscribe_events(self, subscription_id: int) -> Any:
        return self._ws_call(
            {"type": "unsubscribe_events", "subscription": subscription_id}
        )
