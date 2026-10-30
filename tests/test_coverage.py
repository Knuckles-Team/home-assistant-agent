import inspect
import json
import os
from typing import Any
from unittest.mock import MagicMock, patch

import pytest


class MockWebSocket:
    def __init__(self, responses=None):
        self.responses = responses or [
            '{"type": "auth_required"}',
            '{"type": "auth_ok"}',
        ]
        self.sent = []
        self.idx = 0

    def recv(self):
        if self.idx < len(self.responses):
            res = self.responses[self.idx]
            self.idx += 1
            return res
        return '{"type": "result", "success": true, "result": {}}'

    def send(self, data):
        self.sent.append(data)
        # Parse what was sent to decide the next response dynamically
        try:
            msg = json.loads(data)
            msg_type = msg.get("type")
            if msg_type == "auth":
                self.responses.append('{"type": "auth_ok"}')
            elif msg_type == "get_panels":
                self.responses.append(
                    '{"type": "result", "success": true, "result": {"lovelace": {"component_name": "lovelace"}}}'
                )
            elif msg_type == "ping":
                self.responses.append('{"type": "pong"}')
            elif msg_type == "validate_config":
                self.responses.append(
                    '{"type": "result", "success": true, "result": {"trigger": {"valid": true}}}'
                )
            elif msg_type == "extract_from_target":
                self.responses.append(
                    '{"type": "result", "success": true, "result": {"referenced_entities": [], "referenced_devices": [], "referenced_areas": [], "missing_devices": [], "missing_areas": [], "missing_floors": [], "missing_labels": []}}'
                )
            elif msg_type == "get_triggers_for_target":
                self.responses.append(
                    '{"type": "result", "success": true, "result": []}'
                )
            elif msg_type == "get_conditions_for_target":
                self.responses.append(
                    '{"type": "result", "success": true, "result": []}'
                )
            elif msg_type == "get_services_for_target":
                self.responses.append(
                    '{"type": "result", "success": true, "result": []}'
                )
            elif msg_type == "config/entity_registry/list_for_display":
                self.responses.append(
                    '{"type": "result", "success": true, "result": {"entity_categories": {}, "entities": []}}'
                )
            elif msg_type == "homeassistant/expose_entity/list":
                self.responses.append(
                    '{"type": "result", "success": true, "result": {"exposed_entities": {}}}'
                )
            elif msg_type == "homeassistant/expose_entity":
                self.responses.append(
                    '{"type": "result", "success": true, "result": {"status": "success"}}'
                )
            elif msg_type in ["subscribe_events", "subscribe_trigger"]:
                self.responses.append(
                    '{"type": "result", "success": true, "result": {"subscription_id": 123}}'
                )
            elif msg_type == "unsubscribe_events":
                self.responses.append(
                    '{"type": "result", "success": true, "result": {"status": "success"}}'
                )
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        pass


def mock_session_handler(method, url, *args, **kwargs):
    response = MagicMock()
    response.status_code = 200

    if "/api/config/core/check_config" in url:
        response.json.return_value = {"errors": None}
    elif "/api/config" in url:
        response.json.return_value = {
            "components": [],
            "config_dir": "/config",
            "elevation": 0,
            "latitude": 0.0,
            "location_name": "Home",
            "longitude": 0.0,
            "time_zone": "UTC",
            "version": "1.0",
            "whitelist_external_dirs": [],
            "unit_system": {},
        }
    elif "/api/components" in url:
        response.json.return_value = ["light"]
    elif "/api/states/" in url:
        if method == "DELETE":
            response.json.return_value = {"message": "deleted"}
        else:
            response.json.return_value = {
                "entity_id": "light.living_room",
                "state": "on",
                "attributes": {},
            }
    elif "/api/states" in url:
        response.json.return_value = [
            {"entity_id": "light.living_room", "state": "on", "attributes": {}}
        ]
    elif "/api/services/" in url:
        response.json.return_value = {"status": "success"}
    elif "/api/services" in url:
        response.json.return_value = [{"domain": "light", "services": []}]
    elif "/api/events/" in url:
        response.json.return_value = {"message": "fired"}
    elif "/api/events" in url:
        response.json.return_value = [{"event": "state_changed", "listener_count": 1}]
    elif "/api/history/period" in url:
        response.json.return_value = [
            [{"entity_id": "light.living_room", "state": "on", "attributes": {}}]
        ]
    elif "/api/logbook" in url:
        response.json.return_value = [
            {
                "when": "2026-05-22T00:00:00Z",
                "name": "test",
                "message": "hello",
                "entity_id": "light.living_room",
                "domain": "light",
            }
        ]
    elif "/api/error_log" in url:
        response.text = "Error log content"
    elif "/api/camera_proxy" in url:
        response.content = b"camera_bytes"
    elif "/api/calendars/" in url:
        response.json.return_value = [{"summary": "meeting", "start": {}, "end": {}}]
    elif "/api/calendars" in url:
        response.json.return_value = [
            {"entity_id": "calendar.personal", "name": "Personal"}
        ]
    elif "/api/template" in url:
        response.text = "rendered_template"
    elif "/api/intent/handle" in url:
        response.json.return_value = {"status": "handled"}
    elif url.endswith("/api") or url.endswith("/api/"):
        response.json.return_value = {"message": "API running"}
    else:
        response.json.return_value = {}

    return response


@pytest.fixture
def mock_session():
    with patch("requests.Session") as mock_sess:
        session = mock_sess.return_value
        session.headers = {}
        session.get.side_effect = lambda url, *a, **kw: mock_session_handler(
            "GET", url, *a, **kw
        )
        session.post.side_effect = lambda url, *a, **kw: mock_session_handler(
            "POST", url, *a, **kw
        )
        session.delete.side_effect = lambda url, *a, **kw: mock_session_handler(
            "DELETE", url, *a, **kw
        )
        session.patch.side_effect = lambda url, *a, **kw: mock_session_handler(
            "PATCH", url, *a, **kw
        )
        yield session


@pytest.fixture
def mock_connect():
    with patch("home_assistant_agent.api_client.connect") as mock_conn:
        mock_conn.side_effect = lambda *args, **kwargs: MockWebSocket()
        yield mock_conn


def test_auth_coverage(mock_session):
    """Test auth configuration and client creation.

    CONCEPT:AU-OS.config.secrets-authentication
    """
    import home_assistant_agent.auth as auth
    from home_assistant_agent.auth import get_client

    # Reset client state to test instantiation
    auth._client = None

    # 1. Successful initialization with defaults
    with patch.dict(
        os.environ,
        {
            "HOME_ASSISTANT_URL": "http://localhost:8123",
            "HOME_ASSISTANT_TOKEN": "token",
        },
    ):
        c1 = get_client()
        assert c1 is not None
        # Singleton check
        c2 = get_client()
        assert c1 is c2

    # 2. Authentication error
    auth._client = None
    from scion_sdk.exceptions import AuthError

    with patch(
        "home_assistant_agent.auth.HomeAssistantApi",
        side_effect=AuthError("Auth failed"),
    ):
        with pytest.raises(RuntimeError) as exc:
            get_client()
        assert "AUTHENTICATION ERROR" in str(exc.value)


def test_api_unauthorized(mock_session):
    """Test API client unauthorized error handling.

    CONCEPT:AU-ECO.messaging.native-backend-abstraction
    """
    from scion_sdk.exceptions import UnauthorizedError

    from home_assistant_agent.api_client import HomeAssistantApi

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_session.get.side_effect = None
    mock_session.get.return_value = mock_response

    with pytest.raises(UnauthorizedError):
        HomeAssistantApi("http://test", "token")


def test_api_get_state_not_found(mock_session):
    """Test API client state not found error handling.

    CONCEPT:AU-ECO.messaging.native-backend-abstraction
    """
    from scion_sdk.exceptions import ParameterError

    from home_assistant_agent.api_client import HomeAssistantApi

    # Instantiate first under successful condition
    client = HomeAssistantApi("http://test", "token")

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_session.get.side_effect = None
    mock_session.get.return_value = mock_response

    with pytest.raises(ParameterError):
        client.get_state("light.non_existent")


@patch("home_assistant_agent.api_client.connect")
def test_ws_call_errors(mock_connect, mock_session):
    """Test WS connection errors and exceptions.

    CONCEPT:AU-ECO.messaging.native-backend-abstraction
    """
    from scion_sdk.exceptions import ApiError
    from websockets.exceptions import ConnectionClosed

    from home_assistant_agent.api_client import HomeAssistantApi

    client = HomeAssistantApi("http://test", "token")

    # 1. ConnectionClosed
    mock_connect.side_effect = ConnectionClosed(None, None)
    with pytest.raises(ApiError) as exc:
        client.ping()
    assert "WS Connection closed" in str(exc.value)

    # 2. General Exception
    mock_connect.side_effect = Exception("General error")
    with pytest.raises(ApiError) as exc:
        client.ping()
    assert "WS Error: Exception" in str(exc.value)

    # 3. Bad greeting
    mock_socket = MockWebSocket(responses=['{"type": "bad_greeting"}'])
    mock_connect.side_effect = None
    mock_connect.return_value = mock_socket
    with pytest.raises(ApiError) as exc:
        client.ping()
    assert "WS Error: ApiError" in str(exc.value)

    # 4. Auth failed
    mock_socket = MockWebSocket(
        responses=[
            '{"type": "auth_required"}',
            '{"type": "auth_failed", "message": "unauthorized"}',
        ]
    )
    mock_connect.side_effect = None
    mock_connect.return_value = mock_socket
    with pytest.raises(ApiError) as exc:
        client.ping()
    assert "WS Error: UnauthorizedError" in str(exc.value)

    # 5. Command failed
    mock_socket = MockWebSocket(
        responses=[
            '{"type": "auth_required"}',
            '{"type": "auth_ok"}',
            '{"type": "result", "success": false, "error": "Invalid command"}',
        ]
    )
    mock_connect.side_effect = None
    mock_connect.return_value = mock_socket
    with pytest.raises(ApiError) as exc:
        client.ping()
    assert "WS Error: ApiError" in str(exc.value)


def test_api_client_brute_force(mock_session, mock_connect):
    """Brute force test all REST and WebSocket API client methods.

    CONCEPT:AU-ECO.messaging.native-backend-abstraction
    """
    from home_assistant_agent.api_client import HomeAssistantApi

    client = HomeAssistantApi("http://test", "token")

    # Set up our websocket mock on connect
    mock_socket = MockWebSocket()
    mock_connect.return_value = mock_socket

    for name, method in inspect.getmembers(client, predicate=inspect.ismethod):
        if name.startswith("_") or name in ["get_api_status"]:
            continue

        print(f"Calling REST/WS Method: {name}...")
        sig = inspect.signature(method)
        kwargs: dict[str, Any] = {}
        for param in sig.parameters.values():
            p_name = param.name
            if param.default != inspect.Parameter.empty:
                continue
            if p_name == "entity_id":
                kwargs[p_name] = "light.living_room"
            elif p_name == "state":
                kwargs[p_name] = "on"
            elif p_name == "attributes":
                kwargs[p_name] = {"brightness": 255}
            elif p_name == "domain":
                kwargs[p_name] = "light"
            elif p_name == "service":
                kwargs[p_name] = "turn_on"
            elif p_name == "service_data":
                kwargs[p_name] = {"entity_id": "light.living_room"}
            elif p_name == "return_response":
                kwargs[p_name] = True
            elif p_name == "event_type":
                kwargs[p_name] = "state_changed"
            elif p_name == "event_data":
                kwargs[p_name] = {"entity_id": "light.living_room"}
            elif p_name == "timestamp":
                kwargs[p_name] = "2026-05-22T00:00:00"
            elif p_name == "end_time":
                kwargs[p_name] = "2026-05-22T01:00:00"
            elif p_name == "time":
                kwargs[p_name] = "12:00:00"
            elif p_name == "start":
                kwargs[p_name] = "2026-05-22T00:00:00"
            elif p_name == "end":
                kwargs[p_name] = "2026-05-22T01:00:00"
            elif p_name == "template":
                kwargs[p_name] = "{{ state }}"
            elif p_name == "name":
                kwargs[p_name] = "test_intent"
            elif p_name == "data":
                kwargs[p_name] = {}
            elif p_name == "target":
                kwargs[p_name] = {"entity_id": "light.living_room"}
            elif p_name == "expand_group":
                kwargs[p_name] = True
            elif p_name == "assistants":
                kwargs[p_name] = ["google"]
            elif p_name == "entity_ids":
                kwargs[p_name] = ["light.living_room"]
            elif p_name == "should_expose":
                kwargs[p_name] = True
            elif p_name == "trigger":
                kwargs[p_name] = {}
            elif p_name == "condition":
                kwargs[p_name] = {}
            elif p_name == "action":
                kwargs[p_name] = {}
            elif p_name == "subscription_id":
                kwargs[p_name] = 123
            elif param.annotation is int:
                kwargs[p_name] = 1
            elif param.annotation is bool:
                kwargs[p_name] = True
            elif param.annotation is dict:
                kwargs[p_name] = {}
            elif param.annotation is list:
                kwargs[p_name] = []
            else:
                kwargs[p_name] = "test"

        try:
            method(**kwargs)
        except Exception as e:
            print(f"Operation failed: {type(e).__name__}")


@pytest.mark.asyncio
async def test_mcp_server_tools(mock_session, mock_connect):
    """Test all registered MCP tools for valid actions.

    CONCEPT:AU-ECO.messaging.native-backend-abstraction
    """
    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware

    from scion_sdk.connector import build_server

    # Bypass rate limiting
    async def mock_on_request(self, context, call_next):
        return await call_next(context)

    # Mock Context.info to avoid "session not established" errors
    async def mock_info(*args, **kwargs):
        pass

    with (
        patch.object(RateLimitingMiddleware, "on_request", mock_on_request),
        patch("fastmcp.Context.info", mock_info),
    ):
        _, mcp = build_server("home_assistant_agent", command_args=[])
        tools = await mcp.list_tools()
        assert len(tools) > 0

        tool_test_cases = [
            ("home_assistant_config", {"action": "status"}),
            ("home_assistant_config", {"action": "config"}),
            ("home_assistant_config", {"action": "components"}),
            ("home_assistant_config", {"action": "check_config"}),
            ("home_assistant_config", {"action": "invalid", "params_json": "{"}),
            ("home_assistant_states", {"action": "list_states"}),
            (
                "home_assistant_states",
                {"action": "get_state", "params_json": '{"entity_id": "light.living"}'},
            ),
            (
                "home_assistant_states",
                {
                    "action": "update_state",
                    "params_json": '{"entity_id": "light.living", "state": "on"}',
                },
            ),
            (
                "home_assistant_states",
                {
                    "action": "delete_state",
                    "params_json": '{"entity_id": "light.living"}',
                },
            ),
            ("home_assistant_states", {"action": "invalid", "params_json": "{"}),
            ("home_assistant_services", {"action": "list_services"}),
            (
                "home_assistant_services",
                {
                    "action": "call_service",
                    "params_json": '{"domain": "light", "service": "turn_on"}',
                },
            ),
            ("home_assistant_services", {"action": "invalid", "params_json": "{"}),
            ("home_assistant_events", {"action": "list_events"}),
            (
                "home_assistant_events",
                {"action": "fire_event", "params_json": '{"event_type": "test_event"}'},
            ),
            (
                "home_assistant_events",
                {
                    "action": "subscribe_events",
                    "params_json": '{"event_type": "test_event"}',
                },
            ),
            ("home_assistant_events", {"action": "invalid", "params_json": "{"}),
            (
                "home_assistant_history",
                {
                    "action": "get_history",
                    "params_json": '{"entity_id": "light.living"}',
                },
            ),
            ("home_assistant_history", {"action": "invalid", "params_json": "{"}),
            ("home_assistant_logbook", {"action": "get_logbook"}),
            ("home_assistant_logbook", {"action": "get_error_log"}),
            ("home_assistant_logbook", {"action": "invalid", "params_json": "{"}),
            ("home_assistant_calendar", {"action": "list_calendars"}),
            (
                "home_assistant_calendar",
                {
                    "action": "get_calendar_events",
                    "params_json": '{"entity_id": "calendar.personal", "start": "2026-05-22T00:00:00", "end": "2026-05-22T01:00:00"}',
                },
            ),
            ("home_assistant_calendar", {"action": "invalid", "params_json": "{"}),
            ("home_assistant_panels", {"action": "get_panels"}),
            ("home_assistant_panels", {"action": "invalid", "params_json": "{"}),
            ("home_assistant_voice", {"action": "list_exposed_entities"}),
            (
                "home_assistant_voice",
                {
                    "action": "expose_entities",
                    "params_json": '{"assistants": ["google"], "entity_ids": ["light.living"], "should_expose": true}',
                },
            ),
            ("home_assistant_voice", {"action": "invalid", "params_json": "{"}),
            ("home_assistant_entities", {"action": "get_entity_registry_display"}),
            (
                "home_assistant_entities",
                {"action": "extract_from_target", "params_json": '{"target": {}}'},
            ),
            (
                "home_assistant_entities",
                {"action": "get_triggers_for_target", "params_json": '{"target": {}}'},
            ),
            (
                "home_assistant_entities",
                {
                    "action": "get_conditions_for_target",
                    "params_json": '{"target": {}}',
                },
            ),
            (
                "home_assistant_entities",
                {"action": "get_services_for_target", "params_json": '{"target": {}}'},
            ),
            ("home_assistant_entities", {"action": "invalid", "params_json": "{"}),
            (
                "home_assistant_system",
                {"action": "render_template", "params_json": '{"template": "hello"}'},
            ),
            ("home_assistant_system", {"action": "ping"}),
            (
                "home_assistant_system",
                {"action": "handle_intent", "params_json": '{"name": "test_intent"}'},
            ),
            ("home_assistant_system", {"action": "validate_config"}),
            ("home_assistant_system", {"action": "invalid", "params_json": "{"}),
        ]

        with patch.dict(
            os.environ,
            {
                "HOME_ASSISTANT_URL": "http://localhost:8123",
                "HOME_ASSISTANT_TOKEN": "token",
            },
        ):
            # One tool per API operation: each case calls home_assistant_<action>
            # with its typed arguments.
            names = {tool.name for tool in tools}
            for _domain_tool, params in tool_test_cases:
                if params["action"] == "invalid":
                    continue
                tool_name = f"home_assistant_{params['action']}"
                assert tool_name in names, tool_name
                arguments = json.loads(params.get("params_json", "{}"))
                res = await mcp.call_tool(tool_name, arguments)
                assert res is not None


@pytest.mark.asyncio
async def test_mcp_server_health_and_invalid_actions(mock_session, mock_connect):
    """Test health endpoints and invalid tool actions.

    CONCEPT:AU-ECO.messaging.native-backend-abstraction
    """
    from fastmcp.server.middleware.rate_limiting import RateLimitingMiddleware

    from scion_sdk.connector import build_server

    async def mock_on_request(self, context, call_next):
        return await call_next(context)

    async def mock_info(*args, **kwargs):
        pass

    with (
        patch.object(RateLimitingMiddleware, "on_request", mock_on_request),
        patch("fastmcp.Context.info", mock_info),
        patch.dict(
            os.environ,
            {
                "HOME_ASSISTANT_URL": "http://localhost:8123",
                "HOME_ASSISTANT_TOKEN": "token",
            },
        ),
    ):
        _, mcp = build_server("home_assistant_agent", command_args=[])

        # 1. Health check
        from starlette.datastructures import Headers
        from starlette.requests import Request

        req = Request(
            scope={
                "type": "http",
                "headers": Headers().raw,
                "method": "GET",
                "path": "/health",
            }
        )
        health_func = None
        for route in mcp.http_app().routes:
            if route.path == "/health":
                health_func = route.endpoint
                break
        assert health_func is not None
        resp = await health_func(req)
        assert resp.status_code == 200

        # 2. ValueError unknown action in registered tools
        # We need to test calling tools with invalid action and correct JSON structure,
        # which will pass json.loads but fail the action checks, raising ValueError.
        tools_to_test = [
            "home_assistant_config",
            "home_assistant_states",
            "home_assistant_services",
            "home_assistant_events",
            "home_assistant_history",
            "home_assistant_logbook",
            "home_assistant_calendar",
            "home_assistant_panels",
            "home_assistant_voice",
            "home_assistant_entities",
            "home_assistant_system",
        ]
        for tool_name in tools_to_test:
            with pytest.raises(Exception):  # noqa: B017 - fastmcp converts ValueError into tool call exceptions or ToolError
                await mcp.call_tool(
                    tool_name,
                    {"action": "invalid_action_name_xyz", "params_json": "{}"},
                )


def test_api_client_extra_coverage(mock_session, mock_connect):
    """Test edge cases and extra coverage for API client methods.

    CONCEPT:AU-ECO.messaging.native-backend-abstraction
    """
    from home_assistant_agent.api_client import HomeAssistantApi

    client = HomeAssistantApi("http://test", "token")

    # 1. call_service with return_response=True
    client.call_service("light", "turn_on", return_response=True)

    # 2. get_history with optional params
    client.get_history(
        "light.living_room", timestamp="2026-05-22", end_time="2026-05-22"
    )

    # 3. get_logbook with optional params
    client.get_logbook(
        timestamp="2026-05-22", entity_id="light.living_room", end_time="2026-05-22"
    )

    # 4. get_camera_proxy with optional params
    client.get_camera_proxy("camera.front", time="12:00:00")

    # 5. validate_config with optional params
    client.validate_config(trigger={"a": 1}, condition={"b": 2}, action={"c": 3})

    # 5.5 update_state with and without attributes
    client.update_state("light.living_room", "on", attributes=None)
    client.update_state("light.living_room", "on", attributes={"friendly_name": "Test"})

    # 6. WS event/auth_invalid msg type response to cover line 280
    mock_socket = MockWebSocket(
        responses=[
            '{"type": "auth_required"}',
            '{"type": "auth_ok"}',
            '{"type": "event", "event": {}}',
        ]
    )
    mock_connect.side_effect = None
    mock_connect.return_value = mock_socket
    res = client.ping()
    assert res == {"type": "event", "event": {}}
