#!/usr/bin/python
"""Main entry point for running the Home Assistant agent server.

CONCEPT:AU-OS.safety.doom-loop-detection
"""

from home_assistant_agent.agent_server import agent_server

if __name__ == "__main__":
    agent_server()
