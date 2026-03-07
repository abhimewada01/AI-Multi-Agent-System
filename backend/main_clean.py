"""
AI Multi-Agent System - Main FastAPI Application
Main entry point for the AI Multi-Agent System backend.
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

# Load environment variables from .env file
load_dotenv()

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
    
    Workflow: Research → Planning → Coding → Execution
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
    print("Main endpoint: POST /process-task")
    uvicorn.run(app, host="0.0.0.0", port=8000)
