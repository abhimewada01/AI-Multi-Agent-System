"""
AI Multi-Agent System - Enhanced Main Application
Professional developer-grade AI tool with modular architecture.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import time
import logging
from datetime import datetime

# Import the agent manager
from services.agent_manager_fixed import agent_manager, process_task_with_manager

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Multi-Agent System",
    description="Professional AI developer dashboard with multi-agent architecture",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Pydantic models
class TaskRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = None

class SystemResponse(BaseModel):
    task: str
    research: Optional[str] = None
    plan: Optional[str] = None
    code: Optional[Dict[str, Any]] = None
    execution: Optional[str] = None
    total_time: Optional[float] = None
    agent_times: Optional[Dict[str, float]] = None
    quality_assessment: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    agents: Dict[str, Any]
    system: Dict[str, Any]

class MetricsResponse(BaseModel):
    total_executions: int
    average_execution_time: float
    average_quality_score: float
    agent_performance: Dict[str, Any]
    last_execution: Optional[Dict[str, Any]]

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "AI Multi-Agent System - Professional Dashboard",
        "version": "2.0.0",
        "description": "Multi-agent AI system for code generation and development",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "process_task": "/process-task",
            "agents": "/agents",
            "history": "/history"
        },
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check() -> HealthResponse:
    """Comprehensive health check endpoint"""
    try:
        health_status = await agent_manager.health_check()
        return HealthResponse(**health_status)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.get("/metrics")
async def get_metrics() -> MetricsResponse:
    """Get system performance metrics"""
    try:
        metrics = agent_manager.get_system_metrics()
        return MetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Metrics retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Metrics retrieval failed")

@app.get("/agents")
async def get_agents_status():
    """Get status of all agents"""
    try:
        agents_status = agent_manager.get_agent_status()
        return {
            "agents": agents_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Agent status retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Agent status retrieval failed")

@app.get("/agents/{agent_name}")
async def get_agent_info(agent_name: str):
    """Get information about a specific agent"""
    try:
        agent_info = agent_manager.get_agent_info(agent_name)
        if not agent_info:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        return agent_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Agent info retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Agent info retrieval failed")

@app.get("/history")
async def get_execution_history(limit: int = 10):
    """Get execution history"""
    try:
        if limit < 1 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
        
        history = agent_manager.get_execution_history(limit)
        return {
            "history": history,
            "total_count": len(history),
            "limit": limit,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"History retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail="History retrieval failed")

@app.post("/process-task")
async def process_task(request: TaskRequest) -> SystemResponse:
    """
    Process a task through the multi-agent system.
    
    This is the main endpoint that orchestrates all agents:
    Research → Planning → Coding → Execution
    
    Args:
        request: Task request with task description and optional context
        
    Returns:
        System response with all agent results and metadata
    """
    start_time = time.time()
    
    try:
        task = request.task
        logger.info(f"Processing task: {task}")
        
        # Validate task
        if not task or not task.strip():
            raise HTTPException(status_code=400, detail="Task cannot be empty")
        
        if len(task) > 10000:
            raise HTTPException(status_code=400, detail="Task too long (max 10000 characters)")
        
        # Process task through agent manager
        result = await process_task_with_manager(task)
        
        # Log successful execution
        logger.info(f"Task processed successfully in {result['total_time']:.2f}s")
        logger.info(f"Quality score: {result.get('quality_assessment', {}).get('overall_score', 'N/A')}")
        
        return SystemResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Task processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task processing failed: {str(e)}")

@app.post("/process-task/{agent_name}")
async def process_single_agent(agent_name: str, request: TaskRequest):
    """
    Process a task through a single agent (for testing/debugging)
    
    Args:
        agent_name: Name of the agent to execute
        request: Task request
        
    Returns:
        Agent execution result
    """
    try:
        if agent_name not in ["research", "planning", "coding", "execution"]:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
        
        # Execute single agent
        result = await agent_manager.execute_single_agent(
            agent_name, 
            request.task, 
            request.context
        )
        
        logger.info(f"Single agent {agent_name} executed in {result['execution_time']:.2f}s")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Single agent execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Single agent execution failed: {str(e)}")

@app.post("/reset")
async def reset_system():
    """Reset all agents to initial state"""
    try:
        agent_manager.reset_all_agents()
        logger.info("System reset completed")
        return {
            "message": "System reset completed",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"System reset failed: {str(e)}")
        raise HTTPException(status_code=500, detail="System reset failed")

@app.get("/export/{format}")
async def export_data(format: str = "json"):
    """Export system data in specified format"""
    try:
        if format not in ["json", "csv"]:
            raise HTTPException(status_code=400, detail="Format must be 'json' or 'csv'")
        
        data = agent_manager.export_execution_data(format)
        
        from fastapi.responses import Response
        
        if format == "json":
            return Response(
                content=data,
                media_type="application/json",
                headers={"Content-Disposition": "attachment; filename=ai_agent_system_export.json"}
            )
        else:
            return Response(
                content=data,
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=ai_agent_system_export.csv"}
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Data export failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Data export failed")

@app.post("/cleanup")
async def cleanup_old_data(days: int = 30):
    """Clean up old execution data"""
    try:
        if days < 1 or days > 365:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
        
        removed_count = agent_manager.cleanup_old_data(days)
        logger.info(f"Cleaned up {removed_count} old execution records")
        
        return {
            "message": f"Cleaned up {removed_count} old execution records",
            "days": days,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Data cleanup failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Data cleanup failed")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return {
        "error": "Resource not found",
        "status_code": 404,
        "message": str(exc.detail),
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(422)
async def validation_error_handler(request, exc):
    """Handle validation errors"""
    return {
        "error": "Validation error",
        "status_code": 422,
        "message": "Invalid request data",
        "details": exc.errors(),
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(exc)}")
    return {
        "error": "Internal server error",
        "status_code": 500,
        "message": "An unexpected error occurred",
        "timestamp": datetime.now().isoformat()
    }

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("AI Multi-Agent System starting up...")
    logger.info(f"FastAPI version: {app.version}")
    logger.info("All agents initialized and ready")
    
    # Perform initial health check
    try:
        health = await agent_manager.health_check()
        logger.info(f"System health: {health['status']}")
    except Exception as e:
        logger.error(f"Initial health check failed: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("AI Multi-Agent System shutting down...")

# Development server configuration
if __name__ == "__main__":
    import uvicorn
    
    # Check if running in development mode
    dev_mode = os.getenv("DEVELOPMENT", "true").lower() == "true"
    
    if dev_mode:
        logger.info("Starting in development mode")
        uvicorn.run(
            "main_new:app",
            host="0.0.0.0",
            port=8002,
            reload=True,
            log_level="info"
        )
    else:
        logger.info("Starting in production mode")
        uvicorn.run(
            "main_new:app",
            host="0.0.0.0",
            port=8002,
            workers=4,
            log_level="warning"
        )
