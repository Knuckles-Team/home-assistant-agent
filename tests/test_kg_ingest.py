"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_states`` / ``ingest_registry`` /
``ingest_history`` seam with a fake engine client (no engine required), asserting the
txn add_node/commit + edge calls and the Home Assistant record → :Entity/:Device/:Area/
:SensorReading mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from home_assistant_agent.kg_ingest import (
    ingest_entities,
    ingest_history,
    ingest_registry,
    ingest_states,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "Entity", "entityId": "light.k"},
            {"id": "b", "type": "Device"},
        ],
        [{"source": "a", "target": "b", "type": "onDevice"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "home-assistant-agent"
    assert c.txn.nodes["a"]["domain"] == "homeassistant"
    assert c.edges.edges == [("a", "b", {"type": "onDevice"})]


def test_ingest_states_maps_entity_and_reading():
    c = _FakeClient()
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
        ],
        client=c,
        graph="__commons__",
    )
    # one :Entity + one :SensorReading node, linked :readingOf
    assert res == {"nodes": 2, "edges": 1}
    ent = c.txn.nodes["homeassistant:entity:sensor.temp"]
    assert ent["type"] == "Entity"
    assert ent["entityId"] == "sensor.temp"
    assert ent["unitOfMeasurement"] == "°C"
    assert ent["deviceClass"] == "temperature"
    reading_id = "homeassistant:reading:sensor.temp@2026-07-04T10:00:00Z"
    assert c.txn.nodes[reading_id]["type"] == "SensorReading"
    assert c.txn.nodes[reading_id]["state"] == "21.5"
    assert c.edges.edges == [
        (reading_id, "homeassistant:entity:sensor.temp", {"type": "readingOf"})
    ]


def test_ingest_states_without_readings():
    c = _FakeClient()
    res = ingest_states(
        [{"entity_id": "light.k", "state": "on", "attributes": {}}],
        with_readings=False,
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    assert "homeassistant:entity:light.k" in c.txn.nodes


def test_ingest_registry_maps_entity_device_area():
    c = _FakeClient()
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
        },
        client=c,
        graph="__commons__",
    )
    # :Entity + :Device + :Area nodes; :onDevice + :inArea edges
    assert res == {"nodes": 3, "edges": 2}
    assert c.txn.nodes["homeassistant:entity:light.kitchen"]["platform"] == "hue"
    assert c.txn.nodes["homeassistant:device:dev-1"]["type"] == "Device"
    assert c.txn.nodes["homeassistant:area:kitchen"]["type"] == "Area"
    assert (
        "homeassistant:entity:light.kitchen",
        "homeassistant:device:dev-1",
        {"type": "onDevice"},
    ) in c.edges.edges
    assert (
        "homeassistant:entity:light.kitchen",
        "homeassistant:area:kitchen",
        {"type": "inArea"},
    ) in c.edges.edges


def test_ingest_history_maps_timeseries_readings():
    c = _FakeClient()
    res = ingest_history(
        "sensor.power",
        [
            {"state": "100", "last_updated": "2026-07-04T10:00:00Z", "attributes": {}},
            {"state": "120", "last_updated": "2026-07-04T10:05:00Z", "attributes": {}},
        ],
        client=c,
        graph="__commons__",
    )
    # 1 :Entity + 2 :SensorReading nodes, 2 :readingOf edges
    assert res == {"nodes": 3, "edges": 2}
    assert "homeassistant:reading:sensor.power@2026-07-04T10:00:00Z" in c.txn.nodes
    assert "homeassistant:reading:sensor.power@2026-07-04T10:05:00Z" in c.txn.nodes
    assert all(e[2] == {"type": "readingOf"} for e in c.edges.edges)


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Entity"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_states([], client=_FakeClient()) is None
    assert ingest_registry({"entities": []}, client=_FakeClient()) is None
    assert ingest_history("sensor.x", [], client=_FakeClient()) == {
        "nodes": 1,
        "edges": 0,
    }
