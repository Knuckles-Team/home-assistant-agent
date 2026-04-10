# MCP_AGENTS.md - Dynamic Agent Registry

This file tracks the generated agents from MCP servers. You can manually modify the 'Tools' list to customize agent expertise.

## Agent Mapping Table

| Name | Description | System Prompt | Tools | Tag | Source MCP |
|------|-------------|---------------|-------|-----|------------|
| Home Config Specialist | Expert specialist for config domain tasks. | You are a Home Config specialist. Help users manage and interact with Config functionality using the available tools. | ha-status, ha-config, ha-components, ha-check-config | config | home |
| Home States Specialist | Expert specialist for states domain tasks. | You are a Home States specialist. Help users manage and interact with States functionality using the available tools. | ha-list-states, ha-get-state, ha-update-state, ha-delete-state | states | home |
| Home Services Specialist | Expert specialist for services domain tasks. | You are a Home Services specialist. Help users manage and interact with Services functionality using the available tools. | ha-list-services, ha-call-service | services | home |
| Home Events Specialist | Expert specialist for events domain tasks. | You are a Home Events specialist. Help users manage and interact with Events functionality using the available tools. | ha-list-events, ha-fire-event, ha-subscribe-events | events | home |
| Home History Specialist | Expert specialist for history domain tasks. | You are a Home History specialist. Help users manage and interact with History functionality using the available tools. | ha-get-history | history | home |
| Home Logbook Specialist | Expert specialist for logbook domain tasks. | You are a Home Logbook specialist. Help users manage and interact with Logbook functionality using the available tools. | ha-get-logbook, ha-get-error-log | logbook | home |
| Home Calendar Specialist | Expert specialist for calendar domain tasks. | You are a Home Calendar specialist. Help users manage and interact with Calendar functionality using the available tools. | ha-list-calendars, ha-get-calendar-events | calendar | home |
| Home Panels Specialist | Expert specialist for panels domain tasks. | You are a Home Panels specialist. Help users manage and interact with Panels functionality using the available tools. | ha-get-panels | panels | home |
| Home Voice Specialist | Expert specialist for voice domain tasks. | You are a Home Voice specialist. Help users manage and interact with Voice functionality using the available tools. | ha-list-exposed-entities, ha-expose-entities | voice | home |
| Home Entities Specialist | Expert specialist for entities domain tasks. | You are a Home Entities specialist. Help users manage and interact with Entities functionality using the available tools. | ha-get-entity-registry-display, ha-extract-from-target, ha-get-triggers-for-target, ha-get-conditions-for-target, ha-get-services-for-target | entities | home |
| Home System Specialist | Expert specialist for system domain tasks. | You are a Home System specialist. Help users manage and interact with System functionality using the available tools. | ha-render-template, ha-ping, ha-handle-intent, ha-validate-config | system | home |

## Tool Inventory Table

| Tool Name | Description | Tag | Source |
|-----------|-------------|-----|--------|
| ha-status | Check if Home Assistant API is up and running. | config | home |
| ha-config | Get Home Assistant configuration. | config | home |
| ha-components | List currently loaded components. | config | home |
| ha-check-config | Trigger a check of configuration.yaml. | config | home |
| ha-list-states | Return a list of all entity states. | states | home |
| ha-get-state | Return the state of a specific entity. | states | home |
| ha-update-state | Updates or creates a state for an entity (internal representation). | states | home |
| ha-delete-state | Deletes an entity state. | states | home |
| ha-list-services | List all available services. | services | home |
| ha-call-service | Call a service (e.g., turn a light on). | services | home |
| ha-list-events | List all event types and listener counts. | events | home |
| ha-fire-event | Fire an event on the Home Assistant event bus. | events | home |
| ha-subscribe-events | Subscribe to events (one-shot check). | events | home |
| ha-get-history | Get history of one or more entities. | history | home |
| ha-get-logbook | Get logbook entries. | logbook | home |
| ha-get-error-log | Retrieve all errors logged during the current session. | logbook | home |
| ha-list-calendars | List calendar entities. | calendar | home |
| ha-get-calendar-events | Get events for a calendar. | calendar | home |
| ha-get-panels | Get registered panels in Home Assistant. | panels | home |
| ha-list-exposed-entities | List exposure status of entities across all assistants. | voice | home |
| ha-expose-entities | Expose or unexpose entities to voice assistants. | voice | home |
| ha-get-entity-registry-display | Get lightweight, optimized list of entity registry entries for UI display. | entities | home |
| ha-extract-from-target | Extract entities, devices, and areas from one or multiple targets. | entities | home |
| ha-get-triggers-for-target | Get applicable triggers for entities of a given target. | entities | home |
| ha-get-conditions-for-target | Get applicable conditions for entities of a given target. | entities | home |
| ha-get-services-for-target | Get applicable services for entities of a given target. | entities | home |
| ha-render-template | Render a Home Assistant template. | system | home |
| ha-ping | Ping the Home Assistant WebSocket API. | system | home |
| ha-handle-intent | Handle an intent in Home Assistant. | system | home |
| ha-validate-config | Validate triggers, conditions, and action configurations. | system | home |
