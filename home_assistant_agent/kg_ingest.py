"""Native epistemic-graph ingestion for Home Assistant records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the package natively pushes its home-automation data
into the epistemic-graph knowledge graph as **typed OWL nodes** (`:Device`, `:Entity`,
`:Area`, `:SensorReading`, `:HomeAssistantService`, `:LogbookEntry`) + links through the
required ``agent_utilities.knowledge_graph.memory.native_ingest`` authority.

Two modalities, per the ``homeassistant`` ontology leg:

* **typed nodes** — entity registry + live states → :Entity/:Device/:Area nodes + links.
* **timeseries** — each state / history point → a :SensorReading node linked :readingOf
  its :Entity, carrying :state + :measuredAt (the sensor-reading timeseries).

Nodes carry shared provenance (``domain``/``source``) and match the classes federated by
``home_assistant_agent.ontology``. Node ids follow
``homeassistant:<class>:<externalId>``.
"""

from __future__ import annotations

from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

_SOURCE = "home-assistant-agent"
_DOMAIN = "homeassistant"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships through native ingestion."""
    return _native_ingest_entities(
        entities,
        relationships,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def _as_dict(record: Any) -> dict[str, Any]:
    """Coerce a pydantic model / mapping into a plain dict."""
    if hasattr(record, "model_dump"):
        return record.model_dump()
    if isinstance(record, dict):
        return record
    return dict(record)


def _reading_id(entity_id: str, ts: str | None) -> str:
    """Stable id for a timeseries reading of an entity at a timestamp."""
    stamp = ts or "latest"
    return f"{_DOMAIN}:reading:{entity_id}@{stamp}"


def ingest_states(
    states: list[Any],
    *,
    with_readings: bool = True,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map Home Assistant states (``HAState``) → :Entity (+ :SensorReading) nodes.

    Each state contributes an :Entity node keyed ``homeassistant:entity:<entity_id>``
    carrying its friendly_name / unit_of_measurement / device_class (from attributes),
    and — when ``with_readings`` — a :SensorReading timeseries node ``:readingOf`` it,
    carrying the state value + last_updated timestamp.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for raw in states or []:
        rec = _as_dict(raw)
        entity_id = rec.get("entity_id")
        if not entity_id:
            continue
        attrs = rec.get("attributes") or {}
        node_id = f"{_DOMAIN}:entity:{entity_id}"
        entities.append(
            {
                "id": node_id,
                "node_type": "Entity",
                "entityId": entity_id,
                "state": rec.get("state"),
                "friendlyName": attrs.get("friendly_name"),
                "unitOfMeasurement": attrs.get("unit_of_measurement"),
                "deviceClass": attrs.get("device_class"),
                "measuredAt": rec.get("last_updated") or rec.get("last_changed"),
                "externalToolId": entity_id,
            }
        )
        if with_readings:
            ts = rec.get("last_updated") or rec.get("last_changed")
            rid = _reading_id(entity_id, ts)
            entities.append(
                {
                    "id": rid,
                    "node_type": "SensorReading",
                    "entityId": entity_id,
                    "state": rec.get("state"),
                    "unitOfMeasurement": attrs.get("unit_of_measurement"),
                    "measuredAt": ts,
                }
            )
            relationships.append(
                {"source": rid, "target": node_id, "relationship": "readingOf"}
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_registry(
    display: Any,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map the entity registry (``HAEntityRegistryDisplay``) → :Entity/:Device/:Area.

    Each registry entry yields an :Entity node with its platform, plus :Device and
    :Area nodes and :onDevice / :inArea links resolved from the compact registry
    fields (``ei``/``pl``/``di``/``ai``).
    """
    rec = _as_dict(display)
    raw_entries = rec.get("entities") or []
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    seen_devices: set[str] = set()
    seen_areas: set[str] = set()
    for raw in raw_entries:
        entry = _as_dict(raw)
        entity_id = entry.get("ei")
        if not entity_id:
            continue
        ent_node = f"{_DOMAIN}:entity:{entity_id}"
        entities.append(
            {
                "id": ent_node,
                "node_type": "Entity",
                "entityId": entity_id,
                "platform": entry.get("pl"),
                "friendlyName": entry.get("en"),
                "externalToolId": entity_id,
            }
        )
        device_id = entry.get("di")
        if device_id:
            dev_node = f"{_DOMAIN}:device:{device_id}"
            if device_id not in seen_devices:
                entities.append(
                    {"id": dev_node, "node_type": "Device", "deviceId": device_id}
                )
                seen_devices.add(device_id)
            relationships.append(
                {"source": ent_node, "target": dev_node, "relationship": "onDevice"}
            )
        area_id = entry.get("ai")
        if area_id:
            area_node = f"{_DOMAIN}:area:{area_id}"
            if area_id not in seen_areas:
                entities.append(
                    {"id": area_node, "node_type": "Area", "areaId": area_id}
                )
                seen_areas.add(area_id)
            relationships.append(
                {"source": ent_node, "target": area_node, "relationship": "inArea"}
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_history(
    entity_id: str,
    history: list[Any],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map a Home Assistant history series → :SensorReading timeseries nodes.

    ``history`` is the flat list of ``HAState`` points for a single ``entity_id`` (the
    inner list from ``get_history``). Each point becomes a :SensorReading ``:readingOf``
    the entity, keyed by its timestamp so re-ingesting the same window is idempotent.
    """
    if not entity_id:
        return ingest_entities([], client=client, graph=graph)
    ent_node = f"{_DOMAIN}:entity:{entity_id}"
    entities: list[dict[str, Any]] = [
        {"id": ent_node, "node_type": "Entity", "entityId": entity_id}
    ]
    relationships: list[dict[str, Any]] = []
    for raw in history or []:
        rec = _as_dict(raw)
        ts = rec.get("last_updated") or rec.get("last_changed")
        attrs = rec.get("attributes") or {}
        rid = _reading_id(entity_id, ts)
        entities.append(
            {
                "id": rid,
                "node_type": "SensorReading",
                "entityId": entity_id,
                "state": rec.get("state"),
                "unitOfMeasurement": attrs.get("unit_of_measurement"),
                "measuredAt": ts,
            }
        )
        relationships.append(
            {"source": rid, "target": ent_node, "relationship": "readingOf"}
        )
    return ingest_entities(entities, relationships, client=client, graph=graph)
