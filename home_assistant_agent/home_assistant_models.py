from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class HAConfig(BaseModel):
    components: List[str]
    config_dir: str
    elevation: int
    latitude: float
    location_name: str
    longitude: float
    time_zone: str
    version: str
    whitelist_external_dirs: List[str]
    unit_system: Dict[str, str]


class HAState(BaseModel):
    entity_id: str
    state: str
    attributes: Dict[str, Any]
    last_changed: Optional[str] = None
    last_updated: Optional[str] = None


class HAService(BaseModel):
    domain: str
    services: List[str]


class HAEvent(BaseModel):
    event: str
    listener_count: int


class HALogbookEntry(BaseModel):
    when: str
    name: str
    message: str
    entity_id: str
    domain: str
    context_user_id: Optional[str] = None


class HACalendar(BaseModel):
    entity_id: str
    name: str


class HACalendarEvent(BaseModel):
    summary: str
    start: Dict[str, str]
    end: Dict[str, str]
    location: Optional[str] = None
    description: Optional[str] = None


class HAResponse(BaseModel):
    message: Optional[str] = None
    changed_states: Optional[List[HAState]] = None
    service_response: Optional[Dict[str, Any]] = None
