"""
Execution Agent
Responsible for final output generation, review, and quality assurance.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ExecutionAgent(BaseAgent):
    """Execution Agent that provides final output and quality assurance"""
    
    def __init__(self):
        super().__init__(
            name="Execution Agent",
            description="Provides final output, review, and quality assurance"
        )
    
    async def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process the execution task
        
        Args:
            task: The original task
            context: Additional context information (including all previous agent results)
            
        Returns:
            Dictionary containing execution results and final output
        """
        # Simulate execution processing time
        await asyncio.sleep(0.5)
        
        # Extract context information
        research_context = context.get("research", {}) if context else {}
        planning_context = context.get("planning", {}) if context else {}
        coding_context = context.get("coding", {}) if context else {}
        
        # Perform quality assessment
        quality_assessment = self._assess_quality(research_context, planning_context, coding_context)
        
        # Generate final summary
        final_summary = self._generate_final_summary(task, research_context, planning_context, coding_context)
        
        # Create execution report
        execution_report = self._create_execution_report(task, context, quality_assessment)
        
        # Provide recommendations
        recommendations = self._generate_recommendations(task, research_context, planning_context, coding_context)
        
        # Generate deployment instructions
        deployment_instructions = self._generate_deployment_instructions(coding_context)
        
        return {
            "quality_assessment": quality_assessment,
            "final_summary": final_summary,
            "execution_report": execution_report,
            "recommendations": recommendations,
            "deployment_instructions": deployment_instructions,
            "summary": f"Execution completed for task: {task}. All agents coordinated successfully and final result delivered with quality score: {quality_assessment.get('overall_score', 0)}/100.",
            "timestamp": datetime.now().isoformat()
        }
    
    def _assess_quality(self, research_context: Dict[str, Any], planning_context: Dict[str, Any], coding_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the quality of all agent outputs"""
        
        quality_scores = {
            "research": self._assess_research_quality(research_context),
            "planning": self._assess_planning_quality(planning_context),
            "coding": self._assess_coding_quality(coding_context)
        }
        
        # Calculate overall quality score
        overall_score = sum(quality_scores.values()) / len(quality_scores)
        
        # Determine quality grade
        if overall_score >= 90:
            grade = "A+ (Excellent)"
        elif overall_score >= 80:
            grade = "A (Very Good)"
        elif overall_score >= 70:
            grade = "B (Good)"
        elif overall_score >= 60:
            grade = "C (Acceptable)"
        else:
            grade = "D (Needs Improvement)"
        
        return {
            "research": quality_scores["research"],
            "planning": quality_scores["planning"],
            "coding": quality_scores["coding"],
            "overall_score": round(overall_score, 1),
            "grade": grade,
            "assessment_details": self._get_quality_details(quality_scores)
        }
    
    def _assess_research_quality(self, research_context: Dict[str, Any]) -> float:
        """Assess the quality of research output"""
        
        score = 0.0
        max_score = 100.0
        
        # Check for analysis (20 points)
        if research_context.get("analysis"):
            score += 20
        
        # Check for findings (20 points)
        if research_context.get("findings"):
            score += 20
        
        # Check for requirements (20 points)
        requirements = research_context.get("requirements", [])
        if len(requirements) > 0:
            score += 20
        
        # Check for tech stack (20 points)
        tech_stack = research_context.get("tech_stack", [])
        if len(tech_stack) > 0:
            score += 20
        
        # Check for timestamp (10 points)
        if research_context.get("timestamp"):
            score += 10
        
        # Check for comprehensive analysis (10 points)
        analysis = research_context.get("analysis", {})
        if analysis.get("category") and analysis.get("complexity"):
            score += 10
        
        return min(score, max_score)
    
    def _assess_planning_quality(self, planning_context: Dict[str, Any]) -> float:
        """Assess the quality of planning output"""
        
        score = 0.0
        max_score = 100.0
        
        # Check for phases (25 points)
        phases = planning_context.get("phases", [])
        if len(phases) >= 3:
            score += 25
        elif len(phases) >= 2:
            score += 15
        elif len(phases) >= 1:
            score += 10
        
        # Check for project structure (20 points)
        if planning_context.get("project_structure"):
            score += 20
        
        # Check for roadmap (20 points)
        if planning_context.get("roadmap"):
            score += 20
        
        # Check for timeline (20 points)
        if planning_context.get("timeline"):
            score += 20
        
        # Check for dependencies (15 points)
        dependencies = planning_context.get("dependencies", [])
        if len(dependencies) > 0:
            score += 15
        
        return min(score, max_score)
    
    def _assess_coding_quality(self, coding_context: Dict[str, Any]) -> float:
        """Assess the quality of coding output"""
        
        score = 0.0
        max_score = 100.0
        
        # Check for code generation (30 points)
        if coding_context.get("code"):
            score += 30
        
        # Check for documentation (20 points)
        if coding_context.get("documentation"):
            score += 20
        
        # Check for examples (15 points)
        examples = coding_context.get("examples", [])
        if len(examples) > 0:
            score += 15
        
        # Check for test cases (15 points)
        test_cases = coding_context.get("test_cases", [])
        if len(test_cases) > 0:
            score += 15
        
        # Check for dependencies (10 points)
        dependencies = coding_context.get("code", {}).get("dependencies", [])
        if len(dependencies) > 0:
            score += 10
        
        # Check for setup instructions (10 points)
        if coding_context.get("code", {}).get("setup_instructions"):
            score += 10
        
        return min(score, max_score)
    
    def _get_quality_details(self, quality_scores: Dict[str, float]) -> Dict[str, str]:
        """Get detailed quality assessment"""
        
        details = {}
        
        for agent, score in quality_scores.items():
            if score >= 90:
                details[agent] = "Excellent - Comprehensive and well-structured output"
            elif score >= 80:
                details[agent] = "Very Good - High quality with minor improvements possible"
            elif score >= 70:
                details[agent] = "Good - Solid output with some areas for improvement"
            elif score >= 60:
                details[agent] = "Acceptable - Basic output that meets requirements"
            else:
                details[agent] = "Needs Improvement - Output lacks completeness or quality"
        
        return details
    
    def _generate_final_summary(self, task: str, research_context: Dict[str, Any], planning_context: Dict[str, Any], coding_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive final summary"""
        
        # Extract key information
        task_category = research_context.get("analysis", {}).get("category", "general")
        complexity = research_context.get("analysis", {}).get("complexity", "medium")
        tech_stack = research_context.get("tech_stack", [])
        requirements = research_context.get("requirements", [])
        
        # Get code information
        code_info = coding_context.get("code", {})
        code_language = code_info.get("language", "Unknown")
        code_features = code_info.get("features", [])
        
        # Get planning information
        phases = planning_context.get("phases", [])
        timeline = planning_context.get("timeline", {})
        
        return {
            "task_overview": {
                "original_task": task,
                "category": task_category,
                "complexity": complexity,
                "estimated_difficulty": self._get_difficulty_description(complexity)
            },
            "technical_solution": {
                "language": code_language,
                "tech_stack": tech_stack,
                "features": code_features,
                "architecture": self._determine_architecture(task_category, complexity)
            },
            "project_scope": {
                "requirements_met": requirements,
                "phases_planned": len(phases),
                "estimated_timeline": timeline.get("estimated_days", "Unknown"),
                "deliverables": self._extract_deliverables(phases)
            },
            "success_metrics": {
                "requirements_coverage": len(requirements),
                "feature_completeness": len(code_features),
                "code_quality": self._assess_coding_quality(coding_context),
                "planning_thoroughness": self._assess_planning_quality(planning_context)
            },
            "next_steps": self._generate_next_steps(task_category, complexity)
        }
    
    def _get_difficulty_description(self, complexity: str) -> str:
        """Get difficulty description"""
        descriptions = {
            "simple": "Beginner-friendly with straightforward implementation",
            "medium": "Intermediate complexity requiring some experience",
            "complex": "Advanced project requiring expertise and careful planning"
        }
        return descriptions.get(complexity, "Unknown difficulty")
    
    def _determine_architecture(self, category: str, complexity: str) -> str:
        """Determine the architecture pattern used"""
        
        architectures = {
            "web_development": {
                "simple": "Single-page application with vanilla JavaScript",
                "medium": "Component-based architecture with modern frameworks",
                "complex": "Microservices architecture with separated frontend/backend"
            },
            "backend_development": {
                "simple": "Monolithic API with basic structure",
                "medium": "Layered architecture with service separation",
                "complex": "Microservices with event-driven architecture"
            },
            "data_science": {
                "simple": "Notebook-based analysis with basic pipelines",
                "medium": "Modular pipeline with reusable components",
                "complex": "Enterprise data platform with ML operations"
            },
            "general": {
                "simple": "Script-based solution",
                "medium": "Object-oriented design with patterns",
                "complex": "Enterprise architecture with design patterns"
            }
        }
        
        return architectures.get(category, architectures["general"]).get(complexity, "Standard architecture")
    
    def _extract_deliverables(self, phases: List[Dict[str, Any]]) -> List[str]:
        """Extract deliverables from planning phases"""
        
        deliverables = []
        for phase in phases:
            phase_deliverables = phase.get("deliverables", [])
            deliverables.extend(phase_deliverables)
        
        return list(set(deliverables))  # Remove duplicates
    
    def _generate_next_steps(self, category: str, complexity: str) -> List[str]:
        """Generate next steps for the project"""
        
        base_steps = [
            "Review and test the generated code",
            "Set up development environment",
            "Customize the solution to specific needs",
            "Deploy to staging environment for testing"
        ]
        
        category_specific = {
            "web_development": [
                "Test responsive design on multiple devices",
                "Optimize performance and loading times",
                "Set up analytics and monitoring",
                "Configure domain and SSL certificates"
            ],
            "backend_development": [
                "Set up database and migrations",
                "Configure authentication and authorization",
                "Implement logging and error handling",
                "Set up CI/CD pipeline"
            ],
            "data_science": [
                "Validate model performance with test data",
                "Set up data pipeline automation",
                "Create monitoring and alerting",
                "Document model training process"
            ],
            "mobile_development": [
                "Test on multiple devices and screen sizes",
                "Submit to app stores",
                "Set up crash reporting and analytics",
                "Plan for future updates and maintenance"
            ]
        }
        
        steps = base_steps + category_specific.get(category, [])
        
        if complexity == "complex":
            steps.extend([
                "Conduct security audit",
                "Set up monitoring and alerting",
                "Create comprehensive documentation",
                "Plan for scalability and maintenance"
            ])
        
        return steps
    
    def _create_execution_report(self, task: str, context: Dict[str, Any], quality_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive execution report"""
        
        # Calculate execution metrics
        research_time = context.get("research", {}).get("execution_time", 0)
        planning_time = context.get("planning", {}).get("execution_time", 0)
        coding_time = context.get("coding", {}).get("execution_time", 0)
        execution_time = quality_assessment.get("execution_time", 0)
        
        total_time = research_time + planning_time + coding_time + execution_time
        
        return {
            "execution_summary": {
                "task": task,
                "total_execution_time": total_time,
                "agent_times": {
                    "research": research_time,
                    "planning": planning_time,
                    "coding": coding_time,
                    "execution": execution_time
                },
                "quality_score": quality_assessment.get("overall_score", 0),
                "quality_grade": quality_assessment.get("grade", "Unknown")
            },
            "agent_performance": {
                "research": {
                    "status": context.get("research", {}).get("status", "unknown"),
                    "time": research_time,
                    "quality_score": quality_assessment.get("research", 0)
                },
                "planning": {
                    "status": context.get("planning", {}).get("status", "unknown"),
                    "time": planning_time,
                    "quality_score": quality_assessment.get("planning", 0)
                },
                "coding": {
                    "status": context.get("coding", {}).get("status", "unknown"),
                    "time": coding_time,
                    "quality_score": quality_assessment.get("coding", 0)
                },
                "execution": {
                    "status": "completed",
                    "time": execution_time,
                    "quality_score": quality_assessment.get("overall_score", 0)
                }
            },
            "project_metrics": {
                "requirements_identified": len(context.get("research", {}).get("requirements", [])),
                "phases_planned": len(context.get("planning", {}).get("phases", [])),
                "code_files_generated": len(context.get("coding", {}).get("code", {}).get("files", {})),
                "dependencies_required": len(context.get("coding", {}).get("code", {}).get("dependencies", [])),
                "test_cases_created": len(context.get("coding", {}).get("test_cases", []))
            },
            "quality_analysis": {
                "overall_assessment": quality_assessment.get("grade", "Unknown"),
                "strengths": self._identify_strengths(context),
                "areas_for_improvement": self._identify_improvements(context),
                "recommendations": self._generate_quality_recommendations(quality_assessment)
            }
        }
    
    def _identify_strengths(self, context: Dict[str, Any]) -> List[str]:
        """Identify strengths in the project"""
        
        strengths = []
        
        # Research strengths
        research = context.get("research", {})
        if len(research.get("requirements", [])) >= 3:
            strengths.append("Comprehensive requirements analysis")
        if len(research.get("tech_stack", [])) >= 2:
            strengths.append("Well-researched technology stack")
        
        # Planning strengths
        planning = context.get("planning", {})
        if len(planning.get("phases", [])) >= 3:
            strengths.append("Detailed project planning with multiple phases")
        if planning.get("timeline"):
            strengths.append("Realistic timeline estimation")
        
        # Coding strengths
        coding = context.get("coding", {})
        code = coding.get("code", {})
        if len(code.get("features", [])) >= 3:
            strengths.append("Comprehensive feature implementation")
        if code.get("documentation"):
            strengths.append("Complete documentation provided")
        if len(coding.get("test_cases", [])) >= 2:
            strengths.append("Test cases included for quality assurance")
        
        return strengths
    
    def _identify_improvements(self, context: Dict[str, Any]) -> List[str]:
        """Identify areas for improvement"""
        
        improvements = []
        
        # Research improvements
        research = context.get("research", {})
        if len(research.get("requirements", [])) < 2:
            improvements.append("Could include more detailed requirements analysis")
        if len(research.get("tech_stack", [])) < 2:
            improvements.append("Technology stack could be more comprehensive")
        
        # Planning improvements
        planning = context.get("planning", {})
        if len(planning.get("phases", [])) < 3:
            improvements.append("Planning could include more detailed phases")
        if not planning.get("dependencies"):
            improvements.append("Dependencies should be clearly identified")
        
        # Coding improvements
        coding = context.get("coding", {})
        if len(coding.get("test_cases", [])) < 2:
            improvements.append("More comprehensive test cases recommended")
        if not coding.get("code", {}).get("documentation"):
            improvements.append("Code documentation should be included")
        
        return improvements
    
    def _generate_quality_recommendations(self, quality_assessment: Dict[str, Any]) -> List[str]:
        """Generate quality improvement recommendations"""
        
        recommendations = []
        overall_score = quality_assessment.get("overall_score", 0)
        
        if overall_score < 70:
            recommendations.extend([
                "Review and enhance all agent outputs for completeness",
                "Add more detailed documentation and examples",
                "Ensure all requirements are properly addressed"
            ])
        elif overall_score < 85:
            recommendations.extend([
                "Fine-tune specific areas identified for improvement",
                "Add more comprehensive test coverage",
                "Enhance documentation with more examples"
            ])
        else:
            recommendations.extend([
                "Maintain high quality standards",
                "Consider advanced features and optimizations",
                "Prepare for production deployment"
            ])
        
        # Specific agent recommendations
        research_score = quality_assessment.get("research", 0)
        if research_score < 80:
            recommendations.append("Enhance research with more comprehensive analysis")
        
        planning_score = quality_assessment.get("planning", 0)
        if planning_score < 80:
            recommendations.append("Add more detail to project planning phases")
        
        coding_score = quality_assessment.get("coding", 0)
        if coding_score < 80:
            recommendations.append("Improve code quality with better documentation and tests")
        
        return recommendations
    
    def _generate_recommendations(self, task: str, research_context: Dict[str, Any], planning_context: Dict[str, Any], coding_context: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate comprehensive recommendations"""
        
        return {
            "immediate_actions": [
                "Review the generated code for any customization needs",
                "Set up the development environment as specified",
                "Test all features and functionality",
                "Create a backup of the generated code"
            ],
            "short_term_goals": [
                "Complete initial testing and debugging",
                "Customize the solution to specific requirements",
                "Set up version control (Git)",
                "Create initial documentation"
            ],
            "long_term_objectives": [
                "Deploy to production environment",
                "Set up monitoring and analytics",
                "Plan for future enhancements",
                "Create comprehensive user documentation"
            ],
            "best_practices": [
                "Follow coding standards and conventions",
                "Implement proper error handling",
                "Add comprehensive logging",
                "Use automated testing where possible"
            ],
            "security_considerations": [
                "Review code for security vulnerabilities",
                "Implement proper authentication if needed",
                "Validate all user inputs",
                "Use secure communication protocols"
            ]
        }
    
    def _generate_deployment_instructions(self, coding_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate deployment instructions for the generated code"""
        
        code_info = coding_context.get("code", {})
        language = code_info.get("language", "").lower()
        setup_instructions = code_info.get("setup_instructions", "")
        dependencies = code_info.get("dependencies", [])
        
        deployment_guides = {
            "python": {
                "local_development": [
                    "Create a virtual environment: python -m venv venv",
                    "Activate virtual environment: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)",
                    "Install dependencies: pip install -r requirements.txt",
                    "Run the application: python main.py"
                ],
                "production_deployment": [
                    "Set up production server (AWS, Azure, GCP)",
                    "Configure environment variables",
                    "Set up database if required",
                    "Deploy using Docker or direct server deployment",
                    "Set up SSL certificate",
                    "Configure monitoring and logging"
                ],
                "docker_deployment": [
                    "Create Dockerfile with Python base image",
                    "Copy application files and install dependencies",
                    "Expose appropriate ports",
                    "Build and run Docker container"
                ]
            },
            "javascript": {
                "local_development": [
                    "Install Node.js and npm",
                    "Install dependencies: npm install",
                    "Run development server: npm start or npm run dev",
                    "Open browser to localhost:3000"
                ],
                "production_deployment": [
                    "Build production version: npm run build",
                    "Deploy to hosting service (Vercel, Netlify, AWS)",
                    "Configure environment variables",
                    "Set up CDN for static assets"
                ]
            },
            "html/css/javascript": {
                "local_development": [
                    "Open index.html in web browser",
                    "Use live server extension for development",
                    "Test in multiple browsers"
                ],
                "production_deployment": [
                    "Upload files to web server",
                    "Configure domain and DNS",
                    "Set up SSL certificate",
                    "Optimize assets for performance"
                ]
            }
        }
        
        return {
            "language": language,
            "setup_instructions": setup_instructions,
            "dependencies": dependencies,
            "deployment_guide": deployment_guides.get(language, deployment_guides["html/css/javascript"]),
            "environment_setup": self._generate_environment_setup(language),
            "testing_instructions": self._generate_testing_instructions(language),
            "monitoring_setup": self._generate_monitoring_setup(language)
        }
    
    def _generate_environment_setup(self, language: str) -> List[str]:
        """Generate environment setup instructions"""
        
        setups = {
            "python": [
                "Install Python 3.8 or higher",
                "Install pip package manager",
                "Set up virtual environment",
                "Configure IDE or code editor"
            ],
            "javascript": [
                "Install Node.js (version 14 or higher)",
                "Install npm or yarn package manager",
                "Set up code editor with JavaScript support",
                "Install browser developer tools"
            ],
            "html/css/javascript": [
                "Install modern web browser",
                "Set up code editor with HTML/CSS/JS support",
                "Install browser developer tools",
                "Set up local web server (optional)"
            ]
        }
        
        return setups.get(language, ["Set up appropriate development environment"])
    
    def _generate_testing_instructions(self, language: str) -> List[str]:
        """Generate testing instructions"""
        
        instructions = {
            "python": [
                "Run unit tests: python -m pytest",
                "Test coverage: python -m pytest --cov",
                "Integration testing: test all components together",
                "Performance testing: check response times"
            ],
            "javascript": [
                "Run unit tests: npm test",
                "End-to-end testing: npm run test:e2e",
                "Linting: npm run lint",
                "Type checking: npm run type-check"
            ],
            "html/css/javascript": [
                "Manual testing in browser",
                "Cross-browser compatibility testing",
                "Responsive design testing",
                "Performance testing with browser tools"
            ]
        }
        
        return instructions.get(language, ["Test all functionality manually"])
    
    def _generate_monitoring_setup(self, language: str) -> List[str]:
        """Generate monitoring setup instructions"""
        
        monitoring = {
            "python": [
                "Set up application logging",
                "Monitor performance metrics",
                "Set up error tracking (Sentry)",
                "Monitor resource usage"
            ],
            "javascript": [
                "Set up error tracking (Sentry)",
                "Monitor performance metrics",
                "Set up analytics (Google Analytics)",
                "Monitor user behavior"
            ],
            "html/css/javascript": [
                "Set up basic error logging",
                "Monitor page load times",
                "Set up user analytics",
                "Monitor server response times"
            ]
        }
        
        return monitoring.get(language, ["Set up basic monitoring and logging"])
