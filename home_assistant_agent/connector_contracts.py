"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        "home-assistant-manage-state",
        (
            ToolStep(
                "home_assistant_get_state",
                params=("entity_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_get_states",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_list_states",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_update_state",
                params=(
                    "attributes",
                    "entity_id",
                    "state",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "home_assistant_delete_state",
                params=(
                    "confirm",
                    "entity_id",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-manage-registry",
        (
            ToolStep(
                "home_assistant_get_entity_registry_display",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_get_entity_registry_list_for_display",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_list_exposed_entities",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_expose_entities",
                params=(
                    "assistants",
                    "entity_ids",
                    "should_expose",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "home_assistant_expose_or_unexpose_entities",
                params=(
                    "assistants",
                    "entity_ids",
                    "should_expose",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-inspect-target",
        (
            ToolStep(
                "home_assistant_extract_from_target",
                params=(
                    "expand_group",
                    "target",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-manage-service",
        (
            ToolStep(
                "home_assistant_get_services",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_get_services_for_target",
                params=(
                    "expand_group",
                    "target",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_list_services",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_call_service",
                params=(
                    "domain",
                    "return_response",
                    "service",
                    "service_data",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-manage-event",
        (
            ToolStep(
                "home_assistant_get_events",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_list_events",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_subscribe_events",
                params=("event_type",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "home_assistant_unsubscribe_events",
                params=("subscription_id",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                "home_assistant_fire_event",
                params=(
                    "event_data",
                    "event_type",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-manage-trigger",
        (
            ToolStep(
                "home_assistant_get_conditions_for_target",
                params=(
                    "expand_group",
                    "target",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_get_triggers_for_target",
                params=(
                    "expand_group",
                    "target",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_subscribe_trigger",
                params=("trigger",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-manage-intent",
        (
            ToolStep(
                "home_assistant_handle_intent",
                params=(
                    "data",
                    "name",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-inspect-template",
        (
            ToolStep(
                "home_assistant_render_template",
                params=("template",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-inspect-calendar",
        (
            ToolStep(
                "home_assistant_get_calendar_events",
                params=(
                    "end",
                    "entity_id",
                    "start",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_get_calendars",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_list_calendars",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-inspect-camera",
        (
            ToolStep(
                "home_assistant_get_camera_proxy",
                params=(
                    "entity_id",
                    "time",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-inspect-error-log",
        (
            ToolStep(
                "home_assistant_get_error_log",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-manage-history",
        (
            ToolStep(
                "home_assistant_get_history",
                params=(
                    "end_time",
                    "entity_id",
                    "timestamp",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_get_logbook",
                params=(
                    "end_time",
                    "entity_id",
                    "timestamp",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_ingest_history",
                params=(
                    "end_time",
                    "entity_id",
                    "timestamp",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-manage-ingest",
        (
            ToolStep(
                "home_ingest_states",
                params=("with_readings",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-inspect-config",
        (
            ToolStep(
                "home_assistant_check_config",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_components",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_config",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_get_components",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_get_config",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_get_panels",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_validate_config",
                params=(
                    "actions",
                    "condition",
                    "trigger",
                ),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        "home-assistant-inspect-health",
        (
            ToolStep(
                "home_assistant_ping",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
            ToolStep(
                "home_assistant_status",
                params=(),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal("NOT_FOUND", "the requested record does not exist"),
                ),
            ),
        ),
    ),
)

LINKS = (
    SurfaceLink(
        "home-assistant-manage-state",
        tools=(
            "home_assistant_delete_state",
            "home_assistant_get_state",
            "home_assistant_get_states",
            "home_assistant_list_states",
            "home_assistant_update_state",
        ),
        prompts=(
            "home-assistant-home-automation-operator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-entity-registry",),
    ),
    SurfaceLink(
        "home-assistant-manage-registry",
        tools=(
            "home_assistant_expose_entities",
            "home_assistant_expose_or_unexpose_entities",
            "home_assistant_get_entity_registry_display",
            "home_assistant_get_entity_registry_list_for_display",
            "home_assistant_list_exposed_entities",
        ),
        prompts=(
            "home-assistant-home-automation-operator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-entity-registry",),
    ),
    SurfaceLink(
        "home-assistant-inspect-target",
        tools=("home_assistant_extract_from_target",),
        prompts=(
            "home-assistant-home-automation-operator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-entity-registry",),
    ),
    SurfaceLink(
        "home-assistant-manage-service",
        tools=(
            "home_assistant_call_service",
            "home_assistant_get_services",
            "home_assistant_get_services_for_target",
            "home_assistant_list_services",
        ),
        prompts=(
            "home-assistant-home-automation-operator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-services-and-events",),
    ),
    SurfaceLink(
        "home-assistant-manage-event",
        tools=(
            "home_assistant_fire_event",
            "home_assistant_get_events",
            "home_assistant_list_events",
            "home_assistant_subscribe_events",
            "home_assistant_unsubscribe_events",
        ),
        prompts=(
            "home-assistant-home-automation-operator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-services-and-events",),
    ),
    SurfaceLink(
        "home-assistant-manage-trigger",
        tools=(
            "home_assistant_get_conditions_for_target",
            "home_assistant_get_triggers_for_target",
            "home_assistant_subscribe_trigger",
        ),
        prompts=(
            "home-assistant-home-automation-operator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-services-and-events",),
    ),
    SurfaceLink(
        "home-assistant-manage-intent",
        tools=("home_assistant_handle_intent",),
        prompts=(
            "home-assistant-home-automation-operator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-services-and-events",),
    ),
    SurfaceLink(
        "home-assistant-inspect-template",
        tools=("home_assistant_render_template",),
        prompts=(
            "home-assistant-home-automation-operator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-services-and-events",),
    ),
    SurfaceLink(
        "home-assistant-inspect-calendar",
        tools=(
            "home_assistant_get_calendar_events",
            "home_assistant_get_calendars",
            "home_assistant_list_calendars",
        ),
        prompts=(
            "home-assistant-home-insights-analyst",
            "home_automation_specialist",
        ),
        skills=("home-assistant-observability",),
    ),
    SurfaceLink(
        "home-assistant-inspect-camera",
        tools=("home_assistant_get_camera_proxy",),
        prompts=(
            "home-assistant-home-insights-analyst",
            "home_automation_specialist",
        ),
        skills=("home-assistant-observability",),
    ),
    SurfaceLink(
        "home-assistant-inspect-error-log",
        tools=("home_assistant_get_error_log",),
        prompts=(
            "home-assistant-home-insights-analyst",
            "home_automation_specialist",
        ),
        skills=("home-assistant-observability",),
    ),
    SurfaceLink(
        "home-assistant-manage-history",
        tools=(
            "home_assistant_get_history",
            "home_assistant_get_logbook",
            "home_ingest_history",
        ),
        prompts=(
            "home-assistant-home-insights-analyst",
            "home_automation_specialist",
        ),
        skills=("home-assistant-observability",),
    ),
    SurfaceLink(
        "home-assistant-manage-ingest",
        tools=("home_ingest_states",),
        prompts=(
            "home-assistant-home-insights-analyst",
            "home_automation_specialist",
        ),
        skills=("home-assistant-observability",),
    ),
    SurfaceLink(
        "home-assistant-inspect-config",
        tools=(
            "home_assistant_check_config",
            "home_assistant_components",
            "home_assistant_config",
            "home_assistant_get_components",
            "home_assistant_get_config",
            "home_assistant_get_panels",
            "home_assistant_validate_config",
        ),
        prompts=(
            "home-assistant-home-platform-administrator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-system-config",),
    ),
    SurfaceLink(
        "home-assistant-inspect-health",
        tools=(
            "home_assistant_ping",
            "home_assistant_status",
        ),
        prompts=(
            "home-assistant-home-platform-administrator",
            "home_automation_specialist",
        ),
        skills=("home-assistant-system-config",),
    ),
    SurfaceLink(
        "home-assistant-agent-operations",
        tools=(
            "home_assistant_get_states",
            "home_assistant_ping",
        ),
        prompts=("home_automation_specialist",),
        skills=("home-assistant-agent-operations",),
    ),
    SurfaceLink(
        "home-assistant-entity-control",
        tools=(
            "home_assistant_call_service",
            "home_assistant_delete_state",
            "home_assistant_get_state",
            "home_assistant_list_services",
            "home_assistant_list_states",
            "home_assistant_update_state",
        ),
        prompts=("home_automation_specialist",),
        skills=("home-assistant-entity-control",),
    ),
    SurfaceLink(
        "home-assistant-scene-automation",
        tools=(
            "home_assistant_call_service",
            "home_assistant_extract_from_target",
            "home_assistant_fire_event",
            "home_assistant_get_conditions_for_target",
            "home_assistant_get_entity_registry_display",
            "home_assistant_get_services_for_target",
            "home_assistant_get_triggers_for_target",
            "home_assistant_handle_intent",
            "home_assistant_list_events",
            "home_assistant_list_services",
            "home_assistant_ping",
            "home_assistant_render_template",
            "home_assistant_subscribe_events",
            "home_assistant_validate_config",
            "home_ingest_states",
        ),
        prompts=("home_automation_specialist",),
        skills=("home-assistant-scene-automation",),
    ),
    SurfaceLink(
        "home-assistant-telemetry-history",
        tools=(
            "home_assistant_get_error_log",
            "home_assistant_get_history",
            "home_assistant_get_logbook",
            "home_ingest_history",
            "home_ingest_states",
        ),
        prompts=("home_automation_specialist",),
        skills=("home-assistant-telemetry-history",),
    ),
)

LOCATIONS = (
    DataLocation(
        "homeassistant-states",
        ("Device",),
        "HOME_ASSISTANT_URL",
        "home_assistant_list_states",
    ),
    DataLocation(
        "homeassistant-history",
        ("Observation",),
        "HOME_ASSISTANT_URL",
        "home_assistant_get_history",
    ),
    DataLocation(
        "homeassistant-calendars",
        ("Event",),
        "HOME_ASSISTANT_URL",
        "home_assistant_get_calendars",
    ),
)

ROLES = (
    BusinessRole(
        "home automation operator",
        tasks=(
            "home-assistant-inspect-target",
            "home-assistant-inspect-template",
            "home-assistant-manage-event",
            "home-assistant-manage-intent",
            "home-assistant-manage-registry",
            "home-assistant-manage-service",
            "home-assistant-manage-state",
            "home-assistant-manage-trigger",
        ),
    ),
    BusinessRole(
        "home insights analyst",
        tasks=(
            "home-assistant-inspect-calendar",
            "home-assistant-inspect-camera",
            "home-assistant-inspect-error-log",
            "home-assistant-manage-history",
            "home-assistant-manage-ingest",
        ),
    ),
    BusinessRole(
        "home platform administrator",
        tasks=(
            "home-assistant-inspect-config",
            "home-assistant-inspect-health",
        ),
    ),
)
