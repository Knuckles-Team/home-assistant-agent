"""CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R003: models accept the shapes a live server returns."""

import pytest

from home_assistant_agent.home_assistant_models import (
    HALogbookEntry,
    HAPanel,
    HAService,
)

pytestmark = pytest.mark.spec("CONN-HOME-ASSISTANT-AGENT-CONNECTOR-CONTENT-R003")


def test_service_domain_lists_services_as_a_mapping():
    """`GET /api/services` returns each domain's services as a mapping, not a list."""
    svc = HAService(domain="light", services={"turn_on": {"fields": {}}})
    assert "turn_on" in svc.services


def test_logbook_entry_accepts_state_only_records():
    """A logbook record can carry only `when`, `state` and `entity_id`."""
    entry = HALogbookEntry(when="2026-11-06T00:00:00+00:00", state="on")
    assert entry.name is None and entry.message is None


def test_get_panels_accepts_a_panel_that_repeats_url_path():
    """A panel record that carries its own `url_path` must not raise on a duplicate keyword."""
    from home_assistant_agent.api.api_client_websocket import Api

    api = object.__new__(Api)
    api._ws_call = lambda msg: {
        "lovelace": {"component_name": "lovelace", "url_path": "lovelace"}
    }
    panels = (
        Api.get_panels.__wrapped__(api)
        if hasattr(Api.get_panels, "__wrapped__")
        else Api.get_panels(api)
    )
    assert [p.url_path for p in panels] == ["lovelace"]
