#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

from typing import Any

from scion_sdk.mcp.concurrency import run_blocking

from home_assistant_agent.auth import get_client


def register_kg_tools(mcp: FastMCP):
    """Register native epistemic-graph ingestion tools (Wire-First).

    CONCEPT:AU-KG.ingest.enterprise-source-extractor. Lists Home Assistant records via
    the real client and pushes them into the knowledge graph as typed :Entity/:Device/
    :Area/:SensorReading nodes + links. Best-effort: no-ops (``"ingested": None``) when
    no engine is reachable.
    """

    @mcp.tool(tags={"kg"})
    async def home_ingest_states(
        with_readings: bool = Field(
            default=True,
            description="Also emit a :SensorReading timeseries node per entity state.",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest all Home Assistant entity states into epistemic-graph.

        Lists live states via the HA API and pushes them as typed :Entity nodes (plus a
        :SensorReading ``:readingOf`` each entity when ``with_readings``) into the KG via
        the fast engine client. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if ctx:
            await ctx.info("Ingesting Home Assistant states into the KG...")
        from home_assistant_agent.kg_ingest import ingest_states

        states = await run_blocking(client.list_states)
        records = states if isinstance(states, list) else [states]
        result = await ingest_states(records, with_readings=with_readings)
        return {"listed": len(records), "ingested": result}

    @mcp.tool(tags={"kg"})
    async def home_ingest_history(
        entity_id: str = Field(
            description="entity_id whose history/period series to ingest as :SensorReading timeseries."
        ),
        timestamp: str | None = Field(
            default=None, description="ISO-8601 start time for the history window."
        ),
        end_time: str | None = Field(
            default=None, description="ISO-8601 end time for the history window."
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> Any:
        """Ingest a Home Assistant history series for one entity as timeseries readings.

        Pulls ``get_history`` for the entity and pushes each point as a :SensorReading
        node ``:readingOf`` its :Entity. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if ctx:
            await ctx.info(f"Ingesting history for {entity_id} into the KG...")
        from home_assistant_agent.kg_ingest import ingest_history

        series = await run_blocking(
            client.get_history,
            entity_id=entity_id,
            timestamp=timestamp,
            end_time=end_time,
        )
        # get_history returns list[list[HAState]] (one inner list per entity); flatten.
        points: list[Any] = []
        for group in series or []:
            if isinstance(group, list):
                points.extend(group)
            else:
                points.append(group)
        result = await ingest_history(entity_id, points)
        return {"points": len(points), "ingested": result}
