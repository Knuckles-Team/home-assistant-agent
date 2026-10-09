"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the ``home_assistant_agent.kg_ingest`` mapping seam — the Home Assistant
record → :Entity/:Device/:Area/:SensorReading typed-node/link mapping, and the
best-effort no-op guarantee when no engine is reachable — against a fake
``agent_connector_sdk.ingest`` transport boundary, so the suite runs identically
with zero KG infrastructure, never touches the real engine/session machinery, and
still exercises the SDK's own request-building/validation contract.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from home_assistant_agent.kg_ingest import (
    ingest_entities,
    ingest_history,
    ingest_registry,
    ingest_states,
)


class _FakeTransport:
    """Stand-in for the epistemic-graph ingest transport — records every request."""

    def __init__(self, error: Exception | None = None):
        self.requests: list[Any] = []
        self._error = error

    async def source_status(self, connector, stream):
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request):
        if self._error is not None:
            raise self._error
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data):
        raise AssertionError("this connector's ingestion carries no media")


def _ingest(error: Exception | None = None) -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport(error=error)
    return KnowledgeIngest(transport, loop=None), transport


@pytest.mark.asyncio
async def test_ingest_entities_submits_records_and_relationships():
    service, transport = _ingest()
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Entity", "entityId": "light.k"},
            {"id": "b", "node_type": "Device"},
        ],
        [{"source": "a", "target": "b", "relationship": "onDevice"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(transport.requests) == 1
    request = transport.requests[0]
    assert {r.record_id for r in request.records} == {"a", "b"}
    assert len(request.relationships) == 1
    rel = request.relationships[0]
    assert rel.source.record_id == "a"
    assert rel.target.record_id == "b"
    assert rel.relation_reference.endswith("/relations/onDevice")


@pytest.mark.asyncio
async def test_ingest_entities_drops_entries_without_id():
    service, transport = _ingest()
    await ingest_entities(
        [{"node_type": "Entity"}, {"id": "keep", "node_type": "Entity"}], ingest=service
    )
    assert [r.record_id for r in transport.requests[0].records] == ["keep"]


@pytest.mark.asyncio
async def test_ingest_states_maps_entity_and_reading():
    service, transport = _ingest()
    res = await ingest_states(
        [
            {
                "entity_id": "sensor.temp",
                "state": "21.5",
                "attributes": {
                    "friendly_name": "Temp",
                    "unit_of_measurement": "°C",
                    "device_class": "temperature",
                },
                "last_updated": "2026-07-04T10:00:00Z",
            }
        ],
        ingest=service,
    )
    # one :Entity + one :SensorReading node, linked :readingOf
    assert res == {"nodes": 2, "edges": 1}
    records = {r.record_id: r for r in transport.requests[0].records}
    ent = records["homeassistant:entity:sensor.temp"]
    assert ent.payload["entityId"] == "sensor.temp"
    assert ent.payload["unitOfMeasurement"] == "°C"
    assert ent.payload["deviceClass"] == "temperature"
    reading_id = "homeassistant:reading:sensor.temp@2026-07-04T10:00:00Z"
    assert records[reading_id].payload["state"] == "21.5"
    rel = transport.requests[0].relationships[0]
    assert rel.source.record_id == reading_id
    assert rel.target.record_id == "homeassistant:entity:sensor.temp"
    assert rel.relation_reference.endswith("/relations/readingOf")


@pytest.mark.asyncio
async def test_ingest_states_without_readings():
    service, transport = _ingest()
    res = await ingest_states(
        [{"entity_id": "light.k", "state": "on", "attributes": {}}],
        with_readings=False,
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    assert [r.record_id for r in transport.requests[0].records] == [
        "homeassistant:entity:light.k"
    ]


@pytest.mark.asyncio
async def test_ingest_registry_maps_entity_device_area():
    service, transport = _ingest()
    res = await ingest_registry(
        {
            "entities": [
                {
                    "ei": "light.kitchen",
                    "pl": "hue",
                    "di": "dev-1",
                    "ai": "kitchen",
                    "en": "Kitchen Light",
                }
            ]
        },
        ingest=service,
    )
    # :Entity + :Device + :Area nodes; :onDevice + :inArea edges
    assert res == {"nodes": 3, "edges": 2}
    records = {r.record_id: r for r in transport.requests[0].records}
    assert records["homeassistant:entity:light.kitchen"].payload["platform"] == "hue"
    assert "homeassistant:device:dev-1" in records
    assert "homeassistant:area:kitchen" in records
    rels = {
        (rel.source.record_id, rel.target.record_id, rel.relation_reference.rsplit("/", 1)[-1])
        for rel in transport.requests[0].relationships
    }
    assert ("homeassistant:entity:light.kitchen", "homeassistant:device:dev-1", "onDevice") in rels
    assert ("homeassistant:entity:light.kitchen", "homeassistant:area:kitchen", "inArea") in rels


@pytest.mark.asyncio
async def test_ingest_history_maps_timeseries_readings():
    service, transport = _ingest()
    res = await ingest_history(
        "sensor.power",
        [
            {"state": "100", "last_updated": "2026-07-04T10:00:00Z", "attributes": {}},
            {"state": "120", "last_updated": "2026-07-04T10:05:00Z", "attributes": {}},
        ],
        ingest=service,
    )
    # 1 :Entity + 2 :SensorReading nodes, 2 :readingOf edges
    assert res == {"nodes": 3, "edges": 2}
    ids = {r.record_id for r in transport.requests[0].records}
    assert "homeassistant:reading:sensor.power@2026-07-04T10:00:00Z" in ids
    assert "homeassistant:reading:sensor.power@2026-07-04T10:05:00Z" in ids
    assert all(
        rel.relation_reference.endswith("/relations/readingOf")
        for rel in transport.requests[0].relationships
    )


@pytest.mark.asyncio
async def test_ingest_history_empty_entity_id_is_noop():
    service, transport = _ingest()
    assert await ingest_history("", [{"state": "1"}], ingest=service) is None
    assert transport.requests == []


@pytest.mark.asyncio
async def test_ingest_empty_is_noop():
    service, transport = _ingest()
    assert await ingest_entities([], ingest=service) is None
    assert await ingest_states([], ingest=service) is None
    assert await ingest_registry({"entities": []}, ingest=service) is None
    assert transport.requests == []


@pytest.mark.asyncio
async def test_ingest_noops_when_submit_fails():
    # Any failure from the transport (engine unreachable, no ambient session, txn
    # conflict, ...) degrades to a clean no-op, never raises.
    service, _transport = _ingest(error=RuntimeError("engine unreachable"))
    assert await ingest_entities([{"id": "a", "node_type": "Entity"}], ingest=service) is None


@pytest.mark.asyncio
async def test_ingest_noops_without_engine():
    # No injected service: exercises the real current_ingest() lookup against
    # whatever KG stack (or lack thereof) is actually configured in the test
    # environment — must never raise, so the connector keeps working with zero
    # KG infrastructure.
    assert await ingest_entities([{"id": "a", "node_type": "Entity"}]) is None
