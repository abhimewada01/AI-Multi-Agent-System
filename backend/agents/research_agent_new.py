"""
Research Agent
Responsible for gathering information from user queries and organizing research results.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ResearchAgent(BaseAgent):
    """Research Agent that analyzes requirements and gathers information"""
    
    def __init__(self):
        super().__init__(
            name="Research Agent",
            description="Analyzes requirements and gathers relevant information"
        )
    
    async def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process the research task
        
        Args:
            task: The task to research
            context: Additional context information
            
        Returns:
            Dictionary containing research results
        """
        # Simulate research processing time
        await asyncio.sleep(0.5)
        
        # Analyze task type and requirements
        task_lower = task.lower()
        analysis = self._analyze_task(task_lower)
        
        # Generate research findings
        findings = self._generate_findings(task, analysis)
        
        # Identify key requirements
        requirements = self._identify_requirements(task_lower)
        
        # Determine technology stack
        tech_stack = self._determine_tech_stack(task_lower)
        
        return {
            "analysis": analysis,
            "findings": findings,
            "requirements": requirements,
            "tech_stack": tech_stack,
            "summary": f"Research completed for task: {task}. {findings}",
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_task(self, task: str) -> Dict[str, Any]:
        """Analyze the task type and complexity"""
        
        # Determine task category
        categories = {
            "web_development": ["website", "web", "frontend", "html", "css", "react", "vue", "angular"],
            "backend_development": ["api", "backend", "server", "python", "fastapi", "django", "flask"],
            "mobile_development": ["mobile", "app", "ios", "android", "react native", "flutter"],
            "data_science": ["data", "analysis", "ml", "machine learning", "pandas", "numpy"],
            "devops": ["deploy", "docker", "ci/cd", "infrastructure", "aws", "azure"],
            "general": []
        }
        
        task_category = "general"
        for category, keywords in categories.items():
            if any(keyword in task for keyword in keywords):
                task_category = category
                break
        
        # Estimate complexity
        complexity_indicators = {
            "simple": ["basic", "simple", "small", "quick"],
            "medium": ["medium", "moderate", "standard"],
            "complex": ["complex", "advanced", "enterprise", "large", "scalable"]
        }
        
        complexity = "medium"
        for level, indicators in complexity_indicators.items():
            if any(indicator in task for indicator in indicators):
                complexity = level
                break
        
        return {
            "category": task_category,
            "complexity": complexity,
            "estimated_time": self._estimate_time(complexity),
            "key_features": self._extract_features(task)
        }
    
    def _generate_findings(self, task: str, analysis: Dict[str, Any]) -> str:
        """Generate research findings based on analysis"""
        
        category = analysis["category"]
        complexity = analysis["complexity"]
        
        findings_map = {
            "web_development": {
                "simple": "This is a straightforward web development task that can be implemented with modern HTML/CSS/JavaScript. The project will require basic frontend structure and styling.",
                "medium": "This web development task requires a well-structured frontend with responsive design and interactive components. Consider using a modern framework for better maintainability.",
                "complex": "This is a complex web application that requires advanced frontend architecture, state management, and possibly backend integration. A component-based approach with proper testing is recommended."
            },
            "backend_development": {
                "simple": "This is a basic backend task that can be implemented with a simple API structure. Focus on core functionality and basic error handling.",
                "medium": "This backend development task requires a well-designed API with proper authentication, database integration, and error handling. Consider using a framework like FastAPI or Django.",
                "complex": "This is a complex backend system requiring microservices architecture, advanced security, scalability considerations, and comprehensive testing. Enterprise-grade patterns and practices are recommended."
            },
            "data_science": {
                "simple": "This is a basic data analysis task that can be handled with pandas and basic visualization. Focus on data cleaning and exploratory analysis.",
                "medium": "This data science task requires statistical analysis, machine learning models, and comprehensive visualization. Consider the full data science pipeline.",
                "complex": "This is an advanced data science project requiring sophisticated ML algorithms, big data processing, and deployment considerations. Enterprise ML practices are recommended."
            },
            "general": {
                "simple": "This is a straightforward development task that can be implemented with standard programming practices.",
                "medium": "This task requires careful planning and implementation with proper architecture and design patterns.",
                "complex": "This is a complex development task requiring enterprise-level architecture, scalability considerations, and comprehensive testing."
            }
        }
        
        return findings_map.get(category, findings_map["general"]).get(complexity, findings_map["general"]["medium"])
    
    def _identify_requirements(self, task: str) -> List[str]:
        """Identify key requirements from the task"""
        
        requirements = []
        
        # Common requirement patterns
        requirement_patterns = {
            "authentication": ["auth", "login", "user", "security", "register"],
            "database": ["database", "db", "storage", "persist", "save"],
            "api": ["api", "endpoint", "rest", "service"],
            "ui": ["ui", "interface", "frontend", "design", "user"],
            "testing": ["test", "testing", "unit", "integration"],
            "deployment": ["deploy", "production", "host", "server"],
            "performance": ["performance", "optimize", "fast", "efficient"],
            "security": ["security", "secure", "protect", "encrypt"]
        }
        
        for requirement, keywords in requirement_patterns.items():
            if any(keyword in task for keyword in keywords):
                requirements.append(requirement)
        
        return requirements
    
    def _determine_tech_stack(self, task: str) -> List[str]:
        """Determine appropriate technology stack"""
        
        tech_stack = []
        
        # Technology mapping
        tech_mapping = {
            "python": ["python", "fastapi", "django", "flask", "pandas", "numpy"],
            "javascript": ["javascript", "js", "node", "react", "vue", "angular"],
            "web": ["html", "css", "frontend", "website", "web"],
            "database": ["database", "sql", "nosql", "mongodb", "postgresql"],
            "cloud": ["aws", "azure", "cloud", "deploy", "serverless"],
            "mobile": ["mobile", "ios", "android", "react native", "flutter"]
        }
        
        for tech, keywords in tech_mapping:
            if any(keyword in task for keyword in keywords):
                tech_stack.extend(keywords[:3])  # Limit to top 3 technologies
        
        return list(set(tech_stack))  # Remove duplicates
    
    def _extract_features(self, task: str) -> List[str]:
        """Extract key features from the task"""
        
        features = []
        
        # Common feature patterns
        feature_patterns = {
            "crud": ["create", "read", "update", "delete", "crud"],
            "real_time": ["real-time", "live", "websocket", "socket"],
            "responsive": ["responsive", "mobile", "tablet"],
            "search": ["search", "filter", "query"],
            "upload": ["upload", "file", "image", "document"],
            "notification": ["notification", "alert", "email", "sms"],
            "dashboard": ["dashboard", "analytics", "reports", "charts"],
            "payment": ["payment", "stripe", "paypal", "billing"]
        }
        
        for feature, keywords in feature_patterns.items():
            if any(keyword in task for keyword in keywords):
                features.append(feature)
        
        return features
    
    def _estimate_time(self, complexity: str) -> str:
        """Estimate development time based on complexity"""
        
        time_estimates = {
            "simple": "1-2 hours",
            "medium": "4-8 hours",
            "complex": "1-3 days"
        }
        
        return time_estimates.get(complexity, "4-8 hours")
