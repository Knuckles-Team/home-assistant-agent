from typing import Any

from pydantic import BaseModel


class HAConfig(BaseModel):
    components: list[str]
    config_dir: str
    elevation: int
    latitude: float
    location_name: str
    longitude: float
    time_zone: str
    version: str
    whitelist_external_dirs: list[str]
    unit_system: dict[str, str]


class HAState(BaseModel):
    entity_id: str
    state: str
    attributes: dict[str, Any]
    last_changed: str | None = None
    last_updated: str | None = None


class HAService(BaseModel):
    domain: str
    services: list[str]


class HAEvent(BaseModel):
    event: str
    listener_count: int


class HALogbookEntry(BaseModel):
    when: str
    name: str
    message: str
    entity_id: str
    domain: str
    context_user_id: str | None = None


class HACalendar(BaseModel):
    entity_id: str
    name: str


class HACalendarEvent(BaseModel):
    summary: str
    start: dict[str, str]
    end: dict[str, str]
    location: str | None = None
    description: str | None = None


class HAPanel(BaseModel):
    component_name: str
    icon: str | None = None
    title: str | None = None
    url_path: str
    config: dict[str, Any] | None = None


class HAEntityRegistryEntry(BaseModel):
    ei: str  # Entity ID
    pl: str  # Platform
    ai: str | None = None  # Area ID
    lb: list[str] | None = None  # Labels
    di: str | None = None  # Device ID
    ic: str | None = None  # Icon
    tk: str | None = None  # Translation Key
    ec: int | None = None  # Entity Category
    hb: bool | None = None  # Hidden By
    hn: bool | None = None  # Has Entity Name
    en: str | None = None  # Entity Name
    dp: int | None = None  # Display Precision


class HAEntityRegistryDisplay(BaseModel):
    entity_categories: dict[int, str]
    entities: list[HAEntityRegistryEntry]


class HAExposedEntities(BaseModel):
    exposed_entities: dict[str, dict[str, bool]]


class HAValidateConfigItem(BaseModel):
    valid: bool
    error: str | None = None


class HAValidateConfigResult(BaseModel):
    trigger: HAValidateConfigItem | None = None
    condition: HAValidateConfigItem | None = None
    action: HAValidateConfigItem | None = None


class HAExtractFromTargetResult(BaseModel):
    referenced_entities: list[str]
    referenced_devices: list[str]
    referenced_areas: list[str]
    missing_devices: list[str]
    missing_areas: list[str]
    missing_floors: list[str]
    missing_labels: list[str]


class HAResponse(BaseModel):
    message: str | None = None
    changed_states: list[HAState] | None = None
    service_response: dict[str, Any] | None = None
    result: dict[str, Any] | list[Any] | str | bool | int | None = None
