"""
Planning Agent
Responsible for creating step-by-step execution plans and project architecture.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class PlanningAgent(BaseAgent):
    """Planning Agent that creates detailed execution plans"""
    
    def __init__(self):
        super().__init__(
            name="Planning Agent",
            description="Creates step-by-step execution plans and project architecture"
        )
    
    async def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process the planning task
        
        Args:
            task: The task to plan
            context: Additional context information (including research results)
            
        Returns:
            Dictionary containing planning results
        """
        # Simulate planning processing time
        await asyncio.sleep(0.5)
        
        # Extract research context if available
        research_context = context.get("research", {}) if context else {}
        
        # Create execution phases
        phases = self._create_execution_phases(task, research_context)
        
        # Define project structure
        project_structure = self._define_project_structure(task, research_context)
        
        # Create implementation roadmap
        roadmap = self._create_implementation_roadmap(phases)
        
        # Identify dependencies
        dependencies = self._identify_dependencies(task, research_context)
        
        # Estimate timeline
        timeline = self._estimate_timeline(phases)
        
        return {
            "phases": phases,
            "project_structure": project_structure,
            "roadmap": roadmap,
            "dependencies": dependencies,
            "timeline": timeline,
            "summary": f"Planning completed for task: {task}. Step-by-step execution plan created with {len(phases)} main phases.",
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_execution_phases(self, task: str, research_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create detailed execution phases"""
        
        task_category = research_context.get("analysis", {}).get("category", "general")
        complexity = research_context.get("analysis", {}).get("complexity", "medium")
        
        phase_templates = {
            "web_development": [
                {
                    "name": "Requirements Analysis",
                    "description": "Define project requirements, user stories, and acceptance criteria",
                    "duration": "1-2 hours",
                    "deliverables": ["Requirements document", "User stories", "Wireframes"],
                    "tasks": ["Stakeholder interviews", "Requirement gathering", "User story creation"]
                },
                {
                    "name": "Design & Architecture",
                    "description": "Create system architecture, database design, and UI/UX design",
                    "duration": "2-4 hours",
                    "deliverables": ["System architecture diagram", "Database schema", "UI mockups"],
                    "tasks": ["Architecture design", "Database design", "UI/UX design", "Technology selection"]
                },
                {
                    "name": "Frontend Development",
                    "description": "Implement the user interface and client-side functionality",
                    "duration": "4-8 hours",
                    "deliverables": ["HTML/CSS/JS files", "Responsive design", "Interactive components"],
                    "tasks": ["HTML structure", "CSS styling", "JavaScript functionality", "Responsive design"]
                },
                {
                    "name": "Testing & Deployment",
                    "description": "Test the application and deploy to production",
                    "duration": "2-3 hours",
                    "deliverables": ["Test reports", "Deployed application", "Documentation"],
                    "tasks": ["Unit testing", "Integration testing", "Deployment setup", "Documentation"]
                }
            ],
            "backend_development": [
                {
                    "name": "API Design",
                    "description": "Design RESTful API endpoints and data models",
                    "duration": "1-2 hours",
                    "deliverables": ["API specification", "Data models", "Database schema"],
                    "tasks": ["Endpoint design", "Data modeling", "Database schema design"]
                },
                {
                    "name": "Core Implementation",
                    "description": "Implement core business logic and API endpoints",
                    "duration": "3-6 hours",
                    "deliverables": ["API endpoints", "Business logic", "Database integration"],
                    "tasks": ["API implementation", "Business logic", "Database integration", "Error handling"]
                },
                {
                    "name": "Authentication & Security",
                    "description": "Implement user authentication and security measures",
                    "duration": "2-3 hours",
                    "deliverables": ["Authentication system", "Security middleware", "Access control"],
                    "tasks": ["User authentication", "Security implementation", "Access control"]
                },
                {
                    "name": "Testing & Documentation",
                    "description": "Test API endpoints and create documentation",
                    "duration": "2-3 hours",
                    "deliverables": ["Test suite", "API documentation", "Deployment guide"],
                    "tasks": ["API testing", "Documentation", "Performance testing"]
                }
            ],
            "data_science": [
                {
                    "name": "Data Collection & Preparation",
                    "description": "Collect, clean, and prepare data for analysis",
                    "duration": "2-4 hours",
                    "deliverables": ["Clean dataset", "Data documentation", "Exploratory analysis"],
                    "tasks": ["Data collection", "Data cleaning", "Exploratory analysis"]
                },
                {
                    "name": "Feature Engineering",
                    "description": "Create and select relevant features for modeling",
                    "duration": "2-3 hours",
                    "deliverables": ["Feature set", "Feature documentation", "Feature importance"],
                    "tasks": ["Feature creation", "Feature selection", "Feature scaling"]
                },
                {
                    "name": "Model Development",
                    "description": "Develop and train machine learning models",
                    "duration": "3-5 hours",
                    "deliverables": ["Trained models", "Model evaluation", "Model documentation"],
                    "tasks": ["Model selection", "Model training", "Model evaluation", "Hyperparameter tuning"]
                },
                {
                    "name": "Deployment & Monitoring",
                    "description": "Deploy models and set up monitoring",
                    "duration": "2-3 hours",
                    "deliverables": ["Deployed model", "Monitoring system", "Performance reports"],
                    "tasks": ["Model deployment", "Monitoring setup", "Performance tracking"]
                }
            ],
            "general": [
                {
                    "name": "Requirements Analysis",
                    "description": "Analyze requirements and define project scope",
                    "duration": "1-2 hours",
                    "deliverables": ["Requirements document", "Project scope", "Success criteria"],
                    "tasks": ["Requirement analysis", "Scope definition", "Success criteria"]
                },
                {
                    "name": "Design & Planning",
                    "description": "Create project design and detailed implementation plan",
                    "duration": "2-3 hours",
                    "deliverables": ["Project design", "Implementation plan", "Resource allocation"],
                    "tasks": ["System design", "Implementation planning", "Resource planning"]
                },
                {
                    "name": "Implementation",
                    "description": "Implement the core functionality",
                    "duration": "3-6 hours",
                    "deliverables": ["Working solution", "Code documentation", "Test results"],
                    "tasks": ["Core implementation", "Testing", "Documentation"]
                },
                {
                    "name": "Testing & Deployment",
                    "description": "Test the solution and deploy for use",
                    "duration": "1-2 hours",
                    "deliverables": ["Test reports", "Deployed solution", "User documentation"],
                    "tasks": ["Final testing", "Deployment", "User documentation"]
                }
            ]
        }
        
        # Adjust phases based on complexity
        phases = phase_templates.get(task_category, phase_templates["general"])
        
        if complexity == "simple":
            # Reduce phases for simple projects
            phases = phases[:3]
            for phase in phases:
                # Reduce duration estimates
                if "1-2" in phase["duration"]:
                    phase["duration"] = "0.5-1 hour"
                elif "2-4" in phase["duration"]:
                    phase["duration"] = "1-2 hours"
                elif "3-6" in phase["duration"]:
                    phase["duration"] = "2-3 hours"
                elif "4-8" in phase["duration"]:
                    phase["duration"] = "2-4 hours"
        
        elif complexity == "complex":
            # Add additional phases for complex projects
            additional_phase = {
                "name": "Optimization & Scaling",
                "description": "Optimize performance and prepare for scaling",
                "duration": "3-5 hours",
                "deliverables": ["Performance optimizations", "Scaling strategy", "Monitoring setup"],
                "tasks": ["Performance optimization", "Scaling preparation", "Monitoring implementation"]
            }
            phases.append(additional_phase)
        
        return phases
    
    def _define_project_structure(self, task: str, research_context: Dict[str, Any]) -> Dict[str, Any]:
        """Define the project structure and organization"""
        
        task_category = research_context.get("analysis", {}).get("category", "general")
        
        structures = {
            "web_development": {
                "frontend": {
                    "components": ["src/components", "src/pages", "src/styles", "src/utils"],
                    "assets": ["public/images", "public/fonts", "public/icons"],
                    "config": ["src/config", "src/constants"]
                },
                "backend": {
                    "api": ["api/endpoints", "api/models", "api/middleware"],
                    "services": ["services/auth", "services/data", "services/utils"],
                    "database": ["database/migrations", "database/seeds"]
                },
                "shared": ["docs", "tests", "scripts", "config"]
            },
            "backend_development": {
                "api": ["api/v1/endpoints", "api/v1/models", "api/v1/schemas"],
                "core": ["core/auth", "core/database", "core/config"],
                "services": ["services/user", "services/business", "services/external"],
                "utils": ["utils/helpers", "utils/validators", "utils/decorators"],
                "tests": ["tests/unit", "tests/integration", "tests/e2e"],
                "docs": ["docs/api", "docs/deployment", "docs/development"]
            },
            "data_science": {
                "data": ["data/raw", "data/processed", "data/external"],
                "notebooks": ["notebooks/exploratory", "notebooks/experiments"],
                "src": ["src/data_processing", "src/features", "src/models", "src/visualization"],
                "tests": ["tests/unit", "tests/integration"],
                "docs": ["docs/data_dictionary", "docs/model_documentation", "docs/reports"]
            },
            "general": {
                "src": ["src/main", "src/utils", "src/config"],
                "tests": ["tests"],
                "docs": ["docs"],
                "scripts": ["scripts"],
                "config": ["config"]
            }
        }
        
        return structures.get(task_category, structures["general"])
    
    def _create_implementation_roadmap(self, phases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create a detailed implementation roadmap"""
        
        roadmap = []
        cumulative_time = 0
        
        for i, phase in enumerate(phases):
            # Extract time estimate (convert to hours for calculation)
            duration_str = phase["duration"]
            if "hour" in duration_str:
                if "-" in duration_str:
                    # Take average of range
                    times = [int(x) for x in duration_str.replace("hours", "").replace("hour", "").split("-")]
                    avg_time = sum(times) / 2
                else:
                    avg_time = float(duration_str.replace("hours", "").replace("hour", ""))
            else:
                avg_time = 2  # Default to 2 hours
            
            cumulative_time += avg_time
            
            roadmap.append({
                "phase": i + 1,
                "name": phase["name"],
                "description": phase["description"],
                "duration": phase["duration"],
                "cumulative_time": f"{cumulative_time:.1f} hours",
                "deliverables": phase["deliverables"],
                "key_tasks": phase["tasks"][:3],  # Top 3 key tasks
                "dependencies": self._get_phase_dependencies(i)
            })
        
        return roadmap
    
    def _identify_dependencies(self, task: str, research_context: Dict[str, Any]) -> List[str]:
        """Identify project dependencies"""
        
        dependencies = []
        tech_stack = research_context.get("tech_stack", [])
        
        # Map technologies to dependencies
        tech_dependencies = {
            "python": ["python >= 3.8", "pip", "virtualenv"],
            "fastapi": ["fastapi", "uvicorn", "pydantic"],
            "django": ["django", "django-rest-framework"],
            "react": ["react", "react-dom", "webpack"],
            "vue": ["vue", "vue-router", "vuex"],
            "node": ["node.js", "npm", "express"],
            "pandas": ["pandas", "numpy", "matplotlib"],
            "database": ["sqlalchemy", "psycopg2", "mysql-connector"],
            "aws": ["boto3", "aws-cli"],
            "docker": ["docker", "docker-compose"]
        }
        
        for tech in tech_stack:
            for tech_name, deps in tech_dependencies.items():
                if tech_name in tech:
                    dependencies.extend(deps)
        
        # Remove duplicates and sort
        return sorted(list(set(dependencies)))
    
    def _estimate_timeline(self, phases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate project timeline and milestones"""
        
        total_duration = 0
        milestones = []
        
        for i, phase in enumerate(phases):
            # Parse duration (simplified)
            duration_str = phase["duration"]
            if "hour" in duration_str:
                if "-" in duration_str:
                    times = [int(x) for x in duration_str.replace("hours", "").replace("hour", "").split("-")]
                    avg_time = sum(times) / 2
                else:
                    avg_time = float(duration_str.replace("hours", "").replace("hour", ""))
            else:
                avg_time = 2
            
            total_duration += avg_time
            
            # Create milestone for phase completion
            milestones.append({
                "name": f"Complete {phase['name']}",
                "estimated_completion": f"{total_duration:.1f} hours",
                "deliverables": phase["deliverables"]
            })
        
        return {
            "total_estimated_hours": f"{total_duration:.1f} hours",
            "estimated_days": f"{total_duration / 8:.1f} days",
            "milestones": milestones,
            "critical_path": self._identify_critical_path(phases)
        }
    
    def _get_phase_dependencies(self, phase_index: int) -> List[str]:
        """Get dependencies for a specific phase"""
        
        if phase_index == 0:
            return []
        
        # Generally, each phase depends on the completion of the previous phase
        return [f"Phase {phase_index} completion"]
    
    def _identify_critical_path(self, phases: List[Dict[str, Any]]) -> List[str]:
        """Identify the critical path for project completion"""
        
        # For simplicity, assume all phases are on the critical path
        # In a real implementation, this would be more sophisticated
        critical_path = []
        
        for phase in phases:
            critical_path.append(phase["name"])
        
        return critical_path
