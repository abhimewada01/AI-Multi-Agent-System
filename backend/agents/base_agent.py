"""
Base Agent Class
Abstract base class for all AI agents in the multi-agent system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.execution_time = 0.0
        self.status = "waiting"  # waiting, running, completed, failed
        self.result = None
        self.error = None
        
    @abstractmethod
    async def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process the task and return results
        
        Args:
            task: The task to process
            context: Additional context information
            
        Returns:
            Dictionary containing the agent's results
        """
        pass
    
    async def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the agent with timing and error handling
        
        Args:
            task: The task to process
            context: Additional context information
            
        Returns:
            Dictionary containing the agent's results and metadata
        """
        start_time = time.time()
        
        try:
            self.status = "running"
            logger.info(f"Starting {self.name} agent")
            
            # Process the task
            result = await self.process(task, context)
            
            # Calculate execution time
            self.execution_time = time.time() - start_time
            self.status = "completed"
            self.result = result
            
            logger.info(f"{self.name} agent completed in {self.execution_time:.2f}s")
            
            return {
                "agent": self.name,
                "status": "completed",
                "result": result,
                "execution_time": self.execution_time,
                "error": None
            }
            
        except Exception as e:
            self.execution_time = time.time() - start_time
            self.status = "failed"
            self.error = str(e)
            
            logger.error(f"{self.name} agent failed: {e}")
            
            return {
                "agent": self.name,
                "status": "failed",
                "result": None,
                "execution_time": self.execution_time,
                "error": str(e)
            }
    
    def reset(self):
        """Reset agent state"""
        self.status = "waiting"
        self.execution_time = 0.0
        self.result = None
        self.error = None
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "execution_time": self.execution_time,
            "error": self.error
        }
