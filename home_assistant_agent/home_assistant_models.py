from typing import Any, Dict, List, Optional, Union
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


class HAPanel(BaseModel):
    component_name: str
    icon: Optional[str] = None
    title: Optional[str] = None
    url_path: str
    config: Optional[Dict[str, Any]] = None


class HAEntityRegistryEntry(BaseModel):
    ei: str  # Entity ID
    pl: str  # Platform
    ai: Optional[str] = None  # Area ID
    lb: Optional[List[str]] = None  # Labels
    di: Optional[str] = None  # Device ID
    ic: Optional[str] = None  # Icon
    tk: Optional[str] = None  # Translation Key
    ec: Optional[int] = None  # Entity Category
    hb: Optional[bool] = None  # Hidden By
    hn: Optional[bool] = None  # Has Entity Name
    en: Optional[str] = None  # Entity Name
    dp: Optional[int] = None  # Display Precision


class HAEntityRegistryDisplay(BaseModel):
    entity_categories: Dict[int, str]
    entities: List[HAEntityRegistryEntry]


class HAExposedEntities(BaseModel):
    exposed_entities: Dict[str, Dict[str, bool]]


class HAValidateConfigItem(BaseModel):
    valid: bool
    error: Optional[str] = None


class HAValidateConfigResult(BaseModel):
    trigger: Optional[HAValidateConfigItem] = None
    condition: Optional[HAValidateConfigItem] = None
    action: Optional[HAValidateConfigItem] = None


class HAExtractFromTargetResult(BaseModel):
    referenced_entities: List[str]
    referenced_devices: List[str]
    referenced_areas: List[str]
    missing_devices: List[str]
    missing_areas: List[str]
    missing_floors: List[str]
    missing_labels: List[str]


class HAResponse(BaseModel):
    message: Optional[str] = None
    changed_states: Optional[List[HAState]] = None
    service_response: Optional[Dict[str, Any]] = None
    result: Optional[Union[Dict[str, Any], List[Any], str, bool, int]] = None
