"""
Services Module
Contains service classes for the multi-agent system.
"""

from .agent_manager import AgentManager, agent_manager, process_task_with_manager

__all__ = [
    "AgentManager",
    "agent_manager", 
    "process_task_with_manager"
]
