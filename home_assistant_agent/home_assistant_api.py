import requests
import urllib3
from typing import Any, Dict, List, Optional
from agent_utilities.api_utilities import require_auth
from agent_utilities.exceptions import AuthError, UnauthorizedError, ParameterError
from .home_assistant_models import HAState, HAConfig, HAService, HAEvent, HALogbookEntry, HACalendar, HACalendarEvent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HomeAssistantApi:
    def __init__(self, base_url: str, token: str, verify: bool = True):
        self.base_url = base_url.rstrip("/")
        if not self.base_url.endswith("/api"):
            self.base_url = f"{self.base_url}/api"
        
        self.token = token
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        })
        self.session.verify = self.verify
        self.headers = self.session.headers
        
                         
        try:
            self.get_api_status()
        except Exception as e:
                                                            
                                                  
            if isinstance(e, UnauthorizedError):
                raise e

    def get_api_status(self) -> Dict[str, str]:
        response = self.session.get(f"{self.base_url}/")
        if response.status_code == 401:
            raise UnauthorizedError("Invalid token")
        response.raise_for_status()
        return response.json()

    @require_auth
    def get_config(self) -> HAConfig:
        response = self.session.get(f"{self.base_url}/config")
        response.raise_for_status()
        return HAConfig(**response.json())

    @require_auth
    def get_states(self) -> List[HAState]:
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
    def get_services(self) -> List[HAService]:
        response = self.session.get(f"{self.base_url}/services")
        response.raise_for_status()
        return [HAService(**s) for s in response.json()]

    @require_auth
    def get_events(self) -> List[HAEvent]:
        response = self.session.get(f"{self.base_url}/events")
        response.raise_for_status()
        return [HAEvent(**s) for s in response.json()]

    @require_auth
    def call_service(self, domain: str, service: str, service_data: Optional[Dict[str, Any]] = None) -> List[HAState]:
        url = f"{self.base_url}/services/{domain}/{service}"
        response = self.session.post(url, json=service_data or {})
        response.raise_for_status()
                                        
        return [HAState(**s) for s in response.json()]

    @require_auth
    def fire_event(self, event_type: str, event_data: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        url = f"{self.base_url}/events/{event_type}"
        response = self.session.post(url, json=event_data or {})
        response.raise_for_status()
        return response.json()

    @require_auth
    def get_history(self, entity_id: str, timestamp: Optional[str] = None, end_time: Optional[str] = None) -> List[List[HAState]]:
        url = f"{self.base_url}/history/period"
        if timestamp:
            url = f"{url}/{timestamp}"
        
        params = {"filter_entity_id": entity_id}
        if end_time:
            params["end_time"] = end_time
            
        response = self.session.get(url, params=params)
        response.raise_for_status()
                                                               
        return [[HAState(**s) for s in entity_history] for entity_history in response.json()]

    @require_auth
    def get_logbook(self, timestamp: Optional[str] = None, entity_id: Optional[str] = None, end_time: Optional[str] = None) -> List[HALogbookEntry]:
        url = f"{self.base_url}/logbook"
        if timestamp:
            url = f"{url}/{timestamp}"
            
        params = {}
        if entity_id:
            params["entity"] = entity_id
        if end_time:
            params["end_time"] = end_time
            
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return [HALogbookEntry(**entry) for entry in response.json()]

    @require_auth
    def get_calendars(self) -> List[HACalendar]:
        response = self.session.get(f"{self.base_url}/calendars")
        response.raise_for_status()
        return [HACalendar(**c) for c in response.json()]

    @require_auth
    def get_calendar_events(self, entity_id: str, start: str, end: str) -> List[HACalendarEvent]:
        url = f"{self.base_url}/calendars/{entity_id}"
        params = {"start": start, "end": end}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return [HACalendarEvent(**e) for e in response.json()]
