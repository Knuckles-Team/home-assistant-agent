from typing import Any

from agent_utilities.api_utilities import require_auth
from agent_utilities.core.exceptions import ParameterError

from home_assistant_agent.api.api_client_base import BaseApiClient
from home_assistant_agent.home_assistant_models import (
    HACalendar,
    HACalendarEvent,
    HAConfig,
    HAEvent,
    HALogbookEntry,
    HAService,
    HAState,
)


class Api(BaseApiClient):
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

    # --- Compatibility Alias Methods ---
    @require_auth
    def status(self) -> dict[str, str]:
        return self.get_api_status()

    @require_auth
    def config(self) -> HAConfig:
        return self.get_config()

    @require_auth
    def components(self) -> list[str]:
        return self.get_components()

    @require_auth
    def list_states(self) -> list[HAState]:
        return self.get_states()

    @require_auth
    def list_services(self) -> list[HAService]:
        return self.get_services()

    @require_auth
    def list_events(self) -> list[HAEvent]:
        return self.get_events()

    @require_auth
    def list_calendars(self) -> list[HACalendar]:
        return self.get_calendars()
