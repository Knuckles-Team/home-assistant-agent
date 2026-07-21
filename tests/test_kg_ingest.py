"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the ``home_assistant_agent.kg_ingest`` mapping seam — the Home Assistant
record → :Entity/:Device/:Area/:SensorReading typed-node/link mapping, and the
best-effort no-op guarantee when no engine is reachable — against a stubbed
``agent_utilities.knowledge_graph.memory.native_ingest.ingest_entities`` so the
suite runs identically with zero KG infrastructure and never touches the real
engine/session machinery. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

from home_assistant_agent import kg_ingest
from home_assistant_agent.kg_ingest import (
    ingest_entities,
    ingest_history,
    ingest_registry,
    ingest_states,
)


class _Recorder:
    """Stand-in for ``native_ingest.ingest_entities`` — records the call and answers it."""

    def __init__(self, error: Exception | None = None):
        self.calls: list[dict[str, Any]] = []
        self._error = error

    def __call__(self, entities, relationships=None, *, source, domain, client=None, graph=None):
        self.calls.append(
            {
                "entities": entities,
                "relationships": relationships or [],
                "source": source,
                "domain": domain,
                "client": client,
                "graph": graph,
            }
        )
        if self._error is not None:
            raise self._error
        return {"nodes": len(entities), "edges": len(relationships or [])}


def test_ingest_entities_delegates_to_native_ingest(monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(kg_ingest, "_native_ingest_entities", rec)
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Entity", "entityId": "light.k"},
            {"id": "b", "node_type": "Device"},
        ],
        [{"source": "a", "target": "b", "relationship": "onDevice"}],
        client="injected-client",
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(rec.calls) == 1
    call = rec.calls[0]
    assert call["source"] == "home-assistant-agent"
    assert call["domain"] == "homeassistant"
    assert call["client"] == "injected-client"
    assert call["graph"] == "__commons__"
    assert {e["id"] for e in call["entities"]} == {"a", "b"}
    assert call["relationships"] == [
        {"source": "a", "target": "b", "relationship": "onDevice"}
    ]


def test_ingest_entities_drops_entries_without_id(monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(kg_ingest, "_native_ingest_entities", rec)
    ingest_entities([{"node_type": "Entity"}, {"id": "keep", "node_type": "Entity"}])
    assert [e["id"] for e in rec.calls[0]["entities"]] == ["keep"]


def test_ingest_states_maps_entity_and_reading(monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(kg_ingest, "_native_ingest_entities", rec)
    res = ingest_states(
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
        ]
    )
    # one :Entity + one :SensorReading node, linked :readingOf
    assert res == {"nodes": 2, "edges": 1}
    entities = {e["id"]: e for e in rec.calls[0]["entities"]}
    ent = entities["homeassistant:entity:sensor.temp"]
    assert ent["node_type"] == "Entity"
    assert ent["entityId"] == "sensor.temp"
    assert ent["unitOfMeasurement"] == "°C"
    assert ent["deviceClass"] == "temperature"
    reading_id = "homeassistant:reading:sensor.temp@2026-07-04T10:00:00Z"
    assert entities[reading_id]["node_type"] == "SensorReading"
    assert entities[reading_id]["state"] == "21.5"
    assert rec.calls[0]["relationships"] == [
        {
            "source": reading_id,
            "target": "homeassistant:entity:sensor.temp",
            "relationship": "readingOf",
        }
    ]


def test_ingest_states_without_readings(monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(kg_ingest, "_native_ingest_entities", rec)
    res = ingest_states(
        [{"entity_id": "light.k", "state": "on", "attributes": {}}],
        with_readings=False,
    )
    assert res == {"nodes": 1, "edges": 0}
    assert [e["id"] for e in rec.calls[0]["entities"]] == ["homeassistant:entity:light.k"]


def test_ingest_registry_maps_entity_device_area(monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(kg_ingest, "_native_ingest_entities", rec)
    res = ingest_registry(
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
        }
    )
    # :Entity + :Device + :Area nodes; :onDevice + :inArea edges
    assert res == {"nodes": 3, "edges": 2}
    entities = {e["id"]: e for e in rec.calls[0]["entities"]}
    assert entities["homeassistant:entity:light.kitchen"]["platform"] == "hue"
    assert entities["homeassistant:device:dev-1"]["node_type"] == "Device"
    assert entities["homeassistant:area:kitchen"]["node_type"] == "Area"
    rels = rec.calls[0]["relationships"]
    assert {
        "source": "homeassistant:entity:light.kitchen",
        "target": "homeassistant:device:dev-1",
        "relationship": "onDevice",
    } in rels
    assert {
        "source": "homeassistant:entity:light.kitchen",
        "target": "homeassistant:area:kitchen",
        "relationship": "inArea",
    } in rels


def test_ingest_history_maps_timeseries_readings(monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(kg_ingest, "_native_ingest_entities", rec)
    res = ingest_history(
        "sensor.power",
        [
            {"state": "100", "last_updated": "2026-07-04T10:00:00Z", "attributes": {}},
            {"state": "120", "last_updated": "2026-07-04T10:05:00Z", "attributes": {}},
        ],
    )
    # 1 :Entity + 2 :SensorReading nodes, 2 :readingOf edges
    assert res == {"nodes": 3, "edges": 2}
    ids = {e["id"] for e in rec.calls[0]["entities"]}
    assert "homeassistant:reading:sensor.power@2026-07-04T10:00:00Z" in ids
    assert "homeassistant:reading:sensor.power@2026-07-04T10:05:00Z" in ids
    assert all(rel["relationship"] == "readingOf" for rel in rec.calls[0]["relationships"])


def test_ingest_history_empty_entity_id_is_noop(monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(kg_ingest, "_native_ingest_entities", rec)
    assert ingest_history("", [{"state": "1"}]) is None
    assert rec.calls == []


def test_ingest_empty_is_noop(monkeypatch):
    rec = _Recorder()
    monkeypatch.setattr(kg_ingest, "_native_ingest_entities", rec)
    assert ingest_entities([]) is None
    assert ingest_states([]) is None
    assert ingest_registry({"entities": []}) is None
    assert rec.calls == []


def test_ingest_noops_when_native_ingest_fails(monkeypatch):
    # Any failure from the native primitive (engine unreachable, no ambient
    # session, txn conflict, ...) degrades to a clean no-op, never raises.
    monkeypatch.setattr(
        kg_ingest,
        "_native_ingest_entities",
        _Recorder(error=RuntimeError("engine unreachable")),
    )
    assert ingest_entities([{"id": "a", "node_type": "Entity"}]) is None


def test_ingest_noops_without_engine():
    # No monkeypatch: exercises the real import against whatever KG stack (or
    # lack thereof) is actually present in the test environment — must never
    # raise, so the connector keeps working with zero KG infrastructure.
    assert ingest_entities([{"id": "a", "node_type": "Entity"}]) is None
