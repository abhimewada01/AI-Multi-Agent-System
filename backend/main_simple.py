"""
AI Multi-Agent System - Simple FastAPI Application
Minimal working implementation for testing frontend integration
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
import time

# Initialize FastAPI app
app = FastAPI(
    title="AI Multi-Agent System",
    description="A system where multiple AI agents collaborate to solve complex tasks",
    version="1.0.0"
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
    context: Optional[str] = None

class SystemResponse(BaseModel):
    task: str
    research: Optional[str] = None
    plan: Optional[str] = None
    code: Optional[str] = None
    execution: Optional[str] = None
    total_time: Optional[float] = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "AI Multi-Agent System API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agents": "ready"}

@app.post("/process-task")
async def process_task(request: TaskRequest):
    """
    Process a task through the multi-agent system.
    Minimal implementation that always returns results.
    """
    start_time = time.time()
    
    try:
        task = request.task
        print(f"Processing task: {task}")
        
        # Simulate agent processing with delays
        await asyncio.sleep(0.5)  # Research agent delay
        research = f"Research completed for task: {task}. Key findings identified and requirements gathered."
        
        await asyncio.sleep(0.5)  # Planning agent delay
        plan = f"Planning completed for task: {task}. Step-by-step execution plan created with 4 main phases."
        
        await asyncio.sleep(0.5)  # Coding agent delay
        code = f"Code generation completed for task: {task}. Technical solution implemented with best practices."
        
        await asyncio.sleep(0.5)  # Execution agent delay
        execution = f"Execution completed for task: {task}. All agents coordinated successfully and final result delivered."
        
        total_time = time.time() - start_time
        
        return {
            "research": research,
            "plan": plan,
            "code": code,
            "execution": execution,
            "total_time": total_time
        }
        
    except Exception as e:
        print(f"Error processing task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing task: {str(e)}")

@app.post("/process-advanced")
async def process_task_advanced(request: TaskRequest):
    """
    Advanced processing with real AI agents (if available).
    Falls back to simple implementation if AI agents fail.
    """
    try:
        # Try to use real AI agents first
        from agents.research_agent import ResearchAgent
        from agents.planning_agent import PlanningAgent
        from agents.coding_agent import CodingAgent
        from agents.execution_agent import ExecutionAgent
        from utils.llm_helper import LLMHelper
        
        # Initialize agents
        llm_helper = LLMHelper()
        research_agent = ResearchAgent(llm_helper)
        planning_agent = PlanningAgent(llm_helper)
        coding_agent = CodingAgent(llm_helper)
        execution_agent = ExecutionAgent(llm_helper)
        
        start_time = time.time()
        
        # Step 1: Research Agent
        print(f"Starting research for task: {request.task}")
        research_result = await research_agent.process(request.task, request.context)
        
        # Step 2: Planning Agent
        print("Starting planning phase")
        planning_result = await planning_agent.process(request.task, research_result)
        
        # Step 3: Coding Agent
        print("Starting coding phase")
        coding_result = await coding_agent.process(request.task, planning_result)
        
        # Step 4: Execution Agent
        print("Starting execution phase")
        execution_result = await execution_agent.process(
            request.task, 
            research_result, 
            planning_result, 
            coding_result
        )
        
        total_time = time.time() - start_time
        
        return {
            "research": research_result.get("summary", "Research completed"),
            "plan": planning_result.get("project_overview", "Planning completed"),
            "code": coding_result.get("implementation_summary", "Coding completed"),
            "execution": execution_result.get("final_output", "Execution completed"),
            "total_time": total_time
        }
        
    except Exception as e:
        print(f"AI agents failed, falling back to simple implementation: {str(e)}")
        # Fallback to simple implementation
        return await process_task(request)

@app.get("/agents/status")
async def get_agents_status():
    """Get status of all agents"""
    return {
        "research_agent": "ready",
        "planning_agent": "ready", 
        "coding_agent": "ready",
        "execution_agent": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting AI Multi-Agent System...")
    print("API will be available at: http://localhost:8000")
    print("Frontend will be available at: http://localhost:8000/static/index.html")
    print("Simple endpoint: POST /process-task")
    print("Advanced endpoint: POST /process-advanced")
    uvicorn.run(app, host="0.0.0.0", port=8000)
