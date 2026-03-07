"""
Agent Manager Service (Fixed)
Orchestrates the execution of all agents in the multi-agent system.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

from agents.research_agent_new import ResearchAgent
from agents.planning_agent_new import PlanningAgent
from agents.coding_agent_minimal import CodingAgent
from agents.execution_agent_new import ExecutionAgent

logger = logging.getLogger(__name__)

class AgentManager:
    """Manages and orchestrates all agents in the multi-agent system"""
    
    def __init__(self):
        self.agents = {
            "research": ResearchAgent(),
            "planning": PlanningAgent(),
            "coding": CodingAgent(),
            "execution": ExecutionAgent()
        }
        self.execution_history = []
        self.current_execution = None
        
    async def process_task(self, task: str) -> Dict[str, Any]:
        """
        Process a task through the complete multi-agent pipeline
        
        Args:
            task: The task to process
            
        Returns:
            Dictionary containing all agent results and execution metadata
        """
        start_time = time.time()
        execution_id = f"exec_{int(start_time)}"
        
        logger.info(f"Starting task processing: {task}")
        logger.info(f"Execution ID: {execution_id}")
        
        # Initialize execution context
        context = {
            "task": task,
            "execution_id": execution_id,
            "start_time": start_time
        }
        
        try:
            # Execute agents sequentially
            results = {}
            
            # Step 1: Research Agent
            logger.info("Executing Research Agent")
            research_result = await self._execute_agent("research", task, context)
            results["research"] = research_result["result"]
            context["research"] = research_result["result"]
            
            # Step 2: Planning Agent
            logger.info("Executing Planning Agent")
            planning_result = await self._execute_agent("planning", task, context)
            results["planning"] = planning_result["result"]
            context["planning"] = planning_result["result"]
            
            # Step 3: Coding Agent
            logger.info("Executing Coding Agent")
            coding_result = await self._execute_agent("coding", task, context)
            results["code"] = coding_result["result"]["code"]  # Fixed: access the code directly
            context["coding"] = coding_result["result"]
            
            # Step 4: Execution Agent
            logger.info("Executing Execution Agent")
            execution_result = await self._execute_agent("execution", task, context)
            results["execution"] = execution_result["result"]
            context["execution"] = execution_result["result"]
            
            # Calculate total execution time
            total_time = time.time() - start_time
            
            # Create final result
            final_result = {
                "task": task,
                "execution_id": execution_id,
                "research": results["research"].get("summary", "Research completed"),
                "plan": results["planning"].get("summary", "Planning completed"),
                "code": results["code"],
                "execution": results["execution"].get("summary", "Execution completed"),
                "total_time": total_time,
                "agent_times": {
                    "research": research_result["execution_time"],
                    "planning": planning_result["execution_time"],
                    "coding": coding_result["execution_time"],
                    "execution": execution_result["execution_time"]
                },
                "quality_assessment": results["execution"].get("quality_assessment", {}),
                "timestamp": datetime.now().isoformat()
            }
            
            # Store execution history
            self._store_execution(execution_id, task, final_result)
            
            logger.info(f"Task processing completed in {total_time:.2f}s")
            return final_result
            
        except Exception as e:
            logger.error(f"Error processing task: {str(e)}")
            raise
    
    async def _execute_agent(self, agent_name: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single agent
        
        Args:
            agent_name: Name of the agent to execute
            task: The task to process
            context: Current execution context
            
        Returns:
            Dictionary containing agent execution results
        """
        agent = self.agents[agent_name]
        
        # Reset agent state
        agent.reset()
        
        # Execute agent
        result = await agent.execute(task, context)
        
        # Log execution details
        logger.info(f"{agent_name} agent completed in {result['execution_time']:.2f}s with status: {result['status']}")
        
        if result["status"] == "failed":
            logger.error(f"{agent_name} agent failed: {result['error']}")
        
        return result
    
    def _store_execution(self, execution_id: str, task: str, result: Dict[str, Any]):
        """Store execution details in history"""
        
        execution_record = {
            "execution_id": execution_id,
            "task": task,
            "timestamp": datetime.now().isoformat(),
            "total_time": result["total_time"],
            "agent_times": result["agent_times"],
            "quality_score": result.get("quality_assessment", {}).get("overall_score", 0),
            "status": "completed"
        }
        
        self.execution_history.append(execution_record)
        
        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of all agents"""
        
        status = {}
        for name, agent in self.agents.items():
            status[name] = agent.get_info()
        
        return status
    
    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent execution history"""
        
        return self.execution_history[-limit:] if limit > 0 else self.execution_history
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        
        if not self.execution_history:
            return {
                "total_executions": 0,
                "average_execution_time": 0,
                "average_quality_score": 0,
                "agent_performance": {}
            }
        
        # Calculate metrics
        total_executions = len(self.execution_history)
        
        # Average execution time
        total_time = sum(exec["total_time"] for exec in self.execution_history)
        avg_execution_time = total_time / total_executions
        
        # Average quality score
        quality_scores = [exec["quality_score"] for exec in self.execution_history if exec["quality_score"] > 0]
        avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Agent performance
        agent_performance = {}
        for agent_name in self.agents.keys():
            agent_times = [exec["agent_times"].get(agent_name, 0) for exec in self.execution_history]
            if agent_times:
                agent_performance[agent_name] = {
                    "average_time": sum(agent_times) / len(agent_times),
                    "total_executions": len(agent_times)
                }
        
        return {
            "total_executions": total_executions,
            "average_execution_time": avg_execution_time,
            "average_quality_score": avg_quality_score,
            "agent_performance": agent_performance,
            "last_execution": self.execution_history[-1] if self.execution_history else None
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform system health check"""
        
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "system": {}
        }
        
        # Check each agent
        for name, agent in self.agents.items():
            agent_health = {
                "status": "healthy",
                "last_execution": None,
                "error_count": 0
            }
            
            # Check recent executions for this agent
            recent_executions = self.execution_history[-10:]  # Last 10 executions
            agent_errors = 0
            
            for exec in recent_executions:
                if exec["agent_times"].get(name) is not None:
                    agent_health["last_execution"] = exec["timestamp"]
            
            # Update health status based on agent state
            if agent.status == "failed":
                agent_health["status"] = "unhealthy"
                health_status["status"] = "degraded"
            
            health_status["agents"][name] = agent_health
        
        # System health checks
        system_health = {
            "memory_usage": "normal",  # Could be implemented with psutil
            "cpu_usage": "normal",     # Could be implemented with psutil
            "disk_space": "normal",    # Could be implemented with psutil
            "error_rate": self._calculate_error_rate()
        }
        
        health_status["system"] = system_health
        
        return health_status
    
    def _calculate_error_rate(self) -> str:
        """Calculate recent error rate"""
        
        if not self.execution_history:
            return "low"
        
        recent_executions = self.execution_history[-20:]  # Last 20 executions
        failed_executions = sum(1 for exec in recent_executions if exec.get("status") == "failed")
        
        error_rate = failed_executions / len(recent_executions)
        
        if error_rate == 0:
            return "low"
        elif error_rate < 0.1:
            return "low"
        elif error_rate < 0.3:
            return "medium"
        else:
            return "high"
    
    def reset_all_agents(self):
        """Reset all agents to initial state"""
        
        for agent in self.agents.values():
            agent.reset()
        
        logger.info("All agents reset to initial state")
    
    def get_agent_info(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific agent"""
        
        if agent_name not in self.agents:
            return None
        
        return self.agents[agent_name].get_info()
    
    async def execute_single_agent(self, agent_name: str, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a single agent (for testing or debugging)"""
        
        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        context = context or {}
        context["task"] = task
        
        return await self._execute_agent(agent_name, task, context)
    
    def export_execution_data(self, format: str = "json") -> str:
        """Export execution data in specified format"""
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "system_metrics": self.get_system_metrics(),
            "execution_history": self.execution_history,
            "agent_status": self.get_agent_status()
        }
        
        if format.lower() == "json":
            import json
            return json.dumps(export_data, indent=2)
        elif format.lower() == "csv":
            # Convert to CSV format (simplified)
            import csv
            import io
            
            output = io.StringIO()
            if self.execution_history:
                fieldnames = self.execution_history[0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.execution_history)
            
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old execution data"""
        
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_timestamp = cutoff_date.isoformat()
        
        original_count = len(self.execution_history)
        self.execution_history = [
            exec for exec in self.execution_history 
            if exec["timestamp"] > cutoff_timestamp
        ]
        
        removed_count = original_count - len(self.execution_history)
        logger.info(f"Cleaned up {removed_count} old execution records")
        
        return removed_count

# Global agent manager instance
agent_manager = AgentManager()

async def process_task_with_manager(task: str) -> Dict[str, Any]:
    """
    Convenience function to process a task using the global agent manager
    
    Args:
        task: The task to process
        
    Returns:
        Dictionary containing all agent results
    """
    return await agent_manager.process_task(task)
