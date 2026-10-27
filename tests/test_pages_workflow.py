"""Verify the connector's reusable Pages caller contract."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/pages.yml"
DASHBOARD_CONFIG = ROOT / ".github/spec-dashboard.json"

pytestmark = pytest.mark.spec("PIPE-CONNSPEC-R128.3")


def _workflow() -> dict:
    parsed = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    return parsed


def _events(workflow: dict) -> dict:
    # YAML 1.1 parsers expose the unquoted `on` key as True.
    events = workflow.get("on", workflow.get(True))
    assert isinstance(events, dict)
    return events


def test_pages_caller_enables_dashboard_and_pages_permissions() -> None:
    workflow = _workflow()
    events = _events(workflow)
    push = events["push"]
    assert "main" in push["branches"]
    assert set(push["paths"]) >= {
        "docs/**",
        "mkdocs.yml",
        "README.md",
        "specs/**",
        ".github/spec-dashboard.json",
        ".github/workflows/pages.yml",
    }
    assert "workflow_dispatch" in events

    job = workflow["jobs"]["publish-pages"]
    assert (
        job["uses"]
        == "Knuckles-Team/pipelines/.github/workflows/pages_pipeline.yml@main"
    )
    assert job["with"] == {
        "content_source": "docs",
        "spec_dashboard_enabled": True,
        "spec_dashboard_config": ".github/spec-dashboard.json",
    }
    assert job["permissions"] == {
        "contents": "read",
        "pages": "write",
        "id-token": "write",
    }


def test_pages_dashboard_config_is_canonical() -> None:
    assert json.loads(DASHBOARD_CONFIG.read_text(encoding="utf-8")) == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }
