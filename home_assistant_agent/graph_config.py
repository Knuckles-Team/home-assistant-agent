"""Home Assistant Agent graph configuration — tag prompts and env var mappings.

Standardized graph configuration to support hierarchical and specialized domain routing.
"""

                                                                       
TAG_PROMPTS: dict[str, str] = {
    "config": "You are a Home Assistant Configuration specialist. You can check API status, get system configuration, and list loaded components.",
    "states": "You are a Home Assistant State Management specialist. You can list all entity states and retrieve the state of specific entities.",
    "services": "You are a Home Assistant Service specialist. You can list available services and call services to control devices in the home.",
    "events": "You are a Home Assistant Event specialist. You can list event types and fire system events.",
    "history": "You are a Home Assistant History specialist. You can retrieve the historical state of entities over time.",
    "logbook": "You are a Home Assistant Logbook specialist. You can retrieve logs of system activities and state changes.",
    "calendar": "You are a Home Assistant Calendar specialist. You can list calendar entities and retrieve scheduled events.",
}


                                                                        
TAG_ENV_VARS: dict[str, str] = {
    "config": "CONFIGTOOL",
    "states": "STATESTOOL",
    "services": "SERVICESTOOL",
    "events": "EVENTSTOOL",
    "history": "HISTORYTOOL",
    "logbook": "LOGBOOKTOOL",
    "calendar": "CALENDARTOOL",
}
