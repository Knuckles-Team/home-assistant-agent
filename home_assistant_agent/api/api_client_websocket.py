from typing import Any

from agent_utilities.core.decorators import require_auth

from home_assistant_agent.api.api_client_base import BaseApiClient
from home_assistant_agent.home_assistant_models import (
    HAEntityRegistryDisplay,
    HAExposedEntities,
    HAExtractFromTargetResult,
    HAPanel,
    HAValidateConfigResult,
)


class Api(BaseApiClient):
    @require_auth
    def get_panels(self) -> list[HAPanel]:
        res = self._ws_call({"type": "get_panels"})
        return [HAPanel(url_path=k, **v) for k, v in res.items()]

    @require_auth
    def ping(self) -> str:
        return self._ws_call({"type": "ping"})

    @require_auth
    def validate_config(
        self,
        trigger: Any | None = None,
        condition: Any | None = None,
        action: Any | None = None,
    ) -> HAValidateConfigResult:
        msg = {"type": "validate_config"}
        if trigger:
            msg["trigger"] = trigger
        if condition:
            msg["condition"] = condition
        if action:
            msg["action"] = action
        res = self._ws_call(msg)
        return HAValidateConfigResult(**res)

    @require_auth
    def extract_from_target(
        self, target: dict[str, Any], expand_group: bool = False
    ) -> HAExtractFromTargetResult:
        res = self._ws_call(
            {
                "type": "extract_from_target",
                "target": target,
                "expand_group": expand_group,
            }
        )
        return HAExtractFromTargetResult(**res)

    @require_auth
    def get_triggers_for_target(
        self, target: dict[str, Any], expand_group: bool = True
    ) -> list[str]:
        return self._ws_call(
            {
                "type": "get_triggers_for_target",
                "target": target,
                "expand_group": expand_group,
            }
        )

    @require_auth
    def get_conditions_for_target(
        self, target: dict[str, Any], expand_group: bool = True
    ) -> list[str]:
        return self._ws_call(
            {
                "type": "get_conditions_for_target",
                "target": target,
                "expand_group": expand_group,
            }
        )

    @require_auth
    def get_services_for_target(
        self, target: dict[str, Any], expand_group: bool = True
    ) -> list[str]:
        return self._ws_call(
            {
                "type": "get_services_for_target",
                "target": target,
                "expand_group": expand_group,
            }
        )

    @require_auth
    def get_entity_registry_list_for_display(self) -> HAEntityRegistryDisplay:
        res = self._ws_call({"type": "config/entity_registry/list_for_display"})
        return HAEntityRegistryDisplay(**res)

    @require_auth
    def list_exposed_entities(self) -> HAExposedEntities:
        res = self._ws_call({"type": "homeassistant/expose_entity/list"})
        return HAExposedEntities(**res)

    @require_auth
    def expose_or_unexpose_entities(
        self, assistants: list[str], entity_ids: list[str], should_expose: bool
    ) -> Any:
        return self._ws_call(
            {
                "type": "homeassistant/expose_entity",
                "assistants": assistants,
                "entity_ids": entity_ids,
                "should_expose": should_expose,
            }
        )

    @require_auth
    def subscribe_events(self, event_type: str | None = None) -> Any:
        msg = {"type": "subscribe_events"}
        if event_type:
            msg["event_type"] = event_type
        return self._ws_call(msg)

    @require_auth
    def subscribe_trigger(self, trigger: Any) -> Any:
        return self._ws_call({"type": "subscribe_trigger", "trigger": trigger})

    @require_auth
    def unsubscribe_events(self, subscription_id: int) -> Any:
        return self._ws_call(
            {"type": "unsubscribe_events", "subscription": subscription_id}
        )

    # --- Compatibility Alias Methods ---
    @require_auth
    def expose_entities(
        self, assistants: list[str], entity_ids: list[str], should_expose: bool
    ) -> Any:
        return self.expose_or_unexpose_entities(assistants, entity_ids, should_expose)

    @require_auth
    def get_entity_registry_display(self) -> HAEntityRegistryDisplay:
        return self.get_entity_registry_list_for_display()
