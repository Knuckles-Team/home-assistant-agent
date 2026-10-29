"""Verify the connector's reusable Pages caller contract."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_CONFIG = ROOT / ".github/spec-dashboard.json"

pytestmark = pytest.mark.spec("PIPE-CONNSPEC-R128.3")


def _events(workflow: dict) -> dict:
    # YAML 1.1 parsers expose the unquoted `on` key as True.
    events = workflow.get("on", workflow.get(True))
    assert isinstance(events, dict)
    return events


def test_pages_dashboard_config_is_canonical() -> None:
    assert json.loads(DASHBOARD_CONFIG.read_text(encoding="utf-8")) == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }
