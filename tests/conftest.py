"""Shared test fixtures for Home Assistant Agent."""

import pytest


@pytest.fixture
def mock_env(monkeypatch):
    """Set standard test environment variables."""
    monkeypatch.setenv("HOME_URL", "https://test.example.com")
    monkeypatch.setenv("HOME_TOKEN", "test-token-12345")
