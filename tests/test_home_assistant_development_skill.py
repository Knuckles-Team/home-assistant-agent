"""PIPE-CONNSPEC-R128.4: the Home Assistant development skill is packaged."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = (
    ROOT
    / "home_assistant_agent"
    / "skills"
    / "home-assistant-agent-development"
    / "SKILL.md"
)

pytestmark = pytest.mark.spec("PIPE-CONNSPEC-R128.4")


def test_development_skill_has_rapid_contract_and_package_binding() -> None:
    text = SKILL.read_text(encoding="utf-8")
    frontmatter = text.split("---", 2)[1]
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert SKILL.is_file()
    assert re.search(
        r"^name:\s*home-assistant-agent-development\s*$", frontmatter, re.M
    )
    assert re.search(r"^skill_type:\s*skill\s*$", frontmatter, re.M)
    assert "## Rapid delivery: the 5-minute contract" in text
    for term in (
        "home_assistant_agent/__init__.py",
        "home_assistant_agent/api/__init__.py",
        "home_assistant_agent/api/api_client_base.py",
        "home_assistant_agent/api/api_client_rest.py",
        "home_assistant_agent/api/api_client_websocket.py",
        "home_assistant_agent/auth.py",
        "home_assistant_agent/mcp_server.py",
        "home_assistant_agent/connector_sources.py",
        "home_assistant_agent/kg_ingest.py",
        "HOME_ASSISTANT_URL",
        "HOME_ASSISTANT_TOKEN",
        "home-assistant-mcp",
        "mcp_config.json",
        "skills/**",
        "python_pipeline.yml@main",
        "container_pipeline.yml@main",
        "render_connector: true",
        "pages_pipeline.yml@main",
        "uv run --locked --extra test pytest",
    ):
        assert term in text

    assert "verify=False" not in text
    assert "--no-verify" not in text
    package_data = project["tool"]["setuptools"]["package-data"][
        "home_assistant_agent"
    ]
    assert "skills/**" in package_data
    assert project["project"]["entry-points"]["agent_connector_sdk.connector"] == {
        "home-assistant-mcp": "home_assistant_agent:connector"
    }
