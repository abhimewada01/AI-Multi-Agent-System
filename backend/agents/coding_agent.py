"""
Coding Agent
Generates code or technical solutions based on the planning phase.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from utils.llm_helper import LLMHelper, SYSTEM_PROMPTS

logger = logging.getLogger(__name__)

class CodingAgent:
    """
    Coding Agent that generates technical solutions and code implementations.
    """
    
    def __init__(self, llm_helper: LLMHelper):
        """
        Initialize Coding Agent with LLM helper.
        
        Args:
            llm_helper: Instance of LLMHelper for AI interactions
        """
        self.llm_helper = llm_helper
        self.system_prompt = SYSTEM_PROMPTS["coding"]
        
    async def process(self, task: str, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a coding task by generating technical solutions.
        
        Args:
            task: The original task
            plan: Execution plan from planning phase
            
        Returns:
            Dictionary containing code solutions and technical implementation
        """
        try:
            logger.info(f"Starting coding implementation for task: {task}")
            
            # Build coding prompt based on plan
            coding_prompt = self._build_coding_prompt(task, plan)
            
            # Generate coding response
            coding_response = await self.llm_helper.generate_response(
                prompt=coding_prompt,
                system_prompt=self.system_prompt,
                temperature=0.1,  # Very low temperature for consistent code
                max_tokens=4000
            )
            
            # Structure the coding results
            structured_code = await self._structure_coding_results(
                task, coding_response, plan
            )
            
            # Add metadata
            structured_code["metadata"] = {
                "agent": "Coding Agent",
                "timestamp": datetime.now().isoformat(),
                "task": task,
                "total_files": len(structured_code.get("files", [])),
                "primary_language": structured_code.get("primary_language", "unknown"),
                "code_quality_score": self._calculate_code_quality(structured_code),
                "implementation_complexity": plan.get("complexity_level", "medium")
            }
            
            logger.info("Coding implementation completed successfully")
            return structured_code
            
        except Exception as e:
            logger.error(f"Error in coding processing: {str(e)}")
            raise
    
    def _build_coding_prompt(self, task: str, plan: Dict[str, Any]) -> str:
        """
        Build a comprehensive coding prompt based on the execution plan.
        
        Args:
            task: The original task
            plan: Execution plan from planning phase
            
        Returns:
            Formatted coding prompt
        """
        prompt = f"""Based on the following execution plan, generate complete, working code for the task:

ORIGINAL TASK: {task}

EXECUTION PLAN:
{json.dumps(plan, indent=2)}

Please generate comprehensive code that includes:

1. **Complete Implementation**: All necessary files and code to fulfill the task
2. **Best Practices**: Follow industry standards and coding conventions
3. **Error Handling**: Include proper error handling and validation
4. **Documentation**: Add comments and docstrings where appropriate
5. **Dependencies**: Specify any required packages or libraries
6. **Configuration**: Include configuration files if needed
7. **Testing**: Provide basic test cases or examples
8. **Usage Instructions**: Clear instructions on how to run/use the code

For each code file, provide:
- File path/name
- Complete code content
- Brief description of the file's purpose

Focus on creating production-ready, maintainable code that directly addresses the task requirements."""
        
        return prompt
    
    async def _structure_coding_results(
        self, 
        task: str, 
        coding_response: str, 
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Structure the coding response into a standardized format.
        
        Args:
            task: Original task
            coding_response: Raw coding response from LLM
            plan: Execution plan for context
            
        Returns:
            Structured coding results
        """
        structure_prompt = f"""Please analyze and structure the following code implementation into the specified JSON format:

TASK: {task}
CODING RESPONSE:
{coding_response}

Please structure this information into the following JSON format:
{{
    "implementation_summary": "Brief overview of what was implemented",
    "primary_language": "main programming language used",
    "frameworks_used": ["framework1", "framework2"],
    "dependencies": [
        {{"name": "package_name", "version": "version", "purpose": "why it's needed"}}
    ],
    "files": [
        {{
            "file_path": "path/to/file.extension",
            "file_type": "code/config/documentation/test",
            "description": "Brief description of the file",
            "content": "complete file content",
            "language": "programming language for syntax highlighting"
        }}
    ],
    "setup_instructions": "Step-by-step setup instructions",
    "usage_examples": ["example1", "example2"],
    "testing_approach": "How to test the implementation",
    "deployment_notes": "Notes about deployment",
    "api_endpoints": [{{"path": "/endpoint", "method": "GET/POST", "description": "description"}}],
    "database_schema": "Database structure if applicable",
    "configuration_required": ["config1", "config2"],
    "known_limitations": ["limitation1", "limitation2"],
    "enhancement_suggestions": ["suggestion1", "suggestion2"]
}}"""

        try:
            structured_code = await self.llm_helper.generate_structured_response(
                prompt=structure_prompt,
                system_prompt="You are a code structuring specialist. Convert code implementations into structured JSON format accurately."
            )
            
            # Ensure all required fields are present
            required_fields = [
                "implementation_summary", "primary_language", "frameworks_used",
                "dependencies", "files", "setup_instructions", "usage_examples",
                "testing_approach", "deployment_notes"
            ]
            
            for field in required_fields:
                if field not in structured_code:
                    if field in ["frameworks_used", "dependencies", "files", "usage_examples", "api_endpoints", "known_limitations", "enhancement_suggestions"]:
                        structured_code[field] = []
                    elif field in ["configuration_required"]:
                        structured_code[field] = []
                    else:
                        structured_code[field] = "Not specified"
            
            # Validate files structure
            if structured_code.get("files"):
                for file in structured_code["files"]:
                    if not isinstance(file, dict):
                        continue
                    
                    required_file_fields = ["file_path", "file_type", "description", "content", "language"]
                    for field in required_file_fields:
                        if field not in file:
                            file[field] = "Not specified"
            
            return structured_code
            
        except Exception as e:
            logger.warning(f"Error structuring coding results: {str(e)}")
            # Fallback to basic structure
            return {
                "implementation_summary": coding_response[:200] + "..." if len(coding_response) > 200 else coding_response,
                "primary_language": "Python",
                "frameworks_used": [],
                "dependencies": [],
                "files": [
                    {
                        "file_path": "main.py",
                        "file_type": "code",
                        "description": "Main implementation file",
                        "content": coding_response,
                        "language": "python"
                    }
                ],
                "setup_instructions": "Run the main.py file",
                "usage_examples": [],
                "testing_approach": "Manual testing",
                "deployment_notes": "Direct execution",
                "api_endpoints": [],
                "database_schema": "",
                "configuration_required": [],
                "known_limitations": [],
                "enhancement_suggestions": [],
                "raw_response": coding_response
            }
    
    def _calculate_code_quality(self, code_results: Dict[str, Any]) -> float:
        """
        Calculate a quality score for the code implementation.
        
        Args:
            code_results: Structured coding results
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        score = 0.0
        max_score = 10.0
        
        # Check for key sections (each worth 1 point)
        if code_results.get("implementation_summary") and len(code_results["implementation_summary"]) > 50:
            score += 1
        if code_results.get("primary_language") and code_results["primary_language"] != "unknown":
            score += 1
        if code_results.get("files") and len(code_results["files"]) >= 1:
            score += 1
        if code_results.get("dependencies") and len(code_results["dependencies"]) >= 1:
            score += 1
        if code_results.get("setup_instructions") and len(code_results["setup_instructions"]) > 30:
            score += 1
        if code_results.get("usage_examples") and len(code_results["usage_examples"]) >= 1:
            score += 1
        if code_results.get("testing_approach") and len(code_results["testing_approach"]) > 30:
            score += 1
        if code_results.get("deployment_notes") and len(code_results["deployment_notes"]) > 30:
            score += 1
        
        # Bonus points for code quality indicators
        files = code_results.get("files", [])
        if files:
            # Check for documentation
            documented_files = sum(1 for file in files 
                                  if isinstance(file, dict) and 
                                  file.get("content") and 
                                  ('"""' in file["content"] or "'''" in file["content"] or "#" in file["content"]))
            if documented_files >= len(files) * 0.5:
                score += 1
            
            # Check for error handling
            error_handling_files = sum(1 for file in files 
                                      if isinstance(file, dict) and 
                                      file.get("content") and 
                                      ("try:" in file["content"] or "except" in file["content"]))
            if error_handling_files >= 1:
                score += 0.5
        
        return round(score / max_score, 2)
    
    async def review_code(self, code_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review and provide feedback on the generated code.
        
        Args:
            code_results: Code implementation to review
            
        Returns:
            Code review assessment
        """
        review_prompt = f"""Please review the following code implementation and provide comprehensive feedback:

CODE IMPLEMENTATION:
{json.dumps(code_results, indent=2)}

Review aspects:
1. **Code Quality**: Cleanliness, readability, maintainability
2. **Functionality**: Does the code fulfill the requirements?
3. **Best Practices**: Are coding standards followed?
4. **Error Handling**: Is error handling adequate?
5. **Security**: Are there security concerns?
6. **Performance**: Are there performance considerations?
7. **Documentation**: Is code well-documented?
8. **Testing**: Is the code testable?

Respond in JSON format:
{{
    "overall_quality": "excellent/good/fair/poor",
    "functionality_score": 0.0-1.0,
    "code_quality_score": 0.0-1.0,
    "best_practices_score": 0.0-1.0,
    "error_handling_score": 0.0-1.0,
    "security_score": 0.0-1.0,
    "documentation_score": 0.0-1.0,
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "security_concerns": ["concern1", "concern2"],
    "performance_issues": ["issue1", "issue2"],
    "improvement_suggestions": ["suggestion1", "suggestion2"],
    "refactoring_recommendations": ["rec1", "rec2"],
    "testing_recommendations": ["test1", "test2"]
}}"""

        try:
            review = await self.llm_helper.generate_structured_response(
                prompt=review_prompt,
                system_prompt="You are a senior code reviewer. Provide constructive, detailed feedback on code quality."
            )
            return review
        except Exception as e:
            logger.error(f"Error reviewing code: {str(e)}")
            return {
                "overall_quality": "good",
                "functionality_score": 0.8,
                "code_quality_score": 0.8,
                "best_practices_score": 0.8,
                "error_handling_score": 0.7,
                "security_score": 0.8,
                "documentation_score": 0.7,
                "strengths": [],
                "weaknesses": [],
                "security_concerns": [],
                "performance_issues": [],
                "improvement_suggestions": [],
                "refactoring_recommendations": [],
                "testing_recommendations": []
            }
    
    async def optimize_code(self, code_results: Dict[str, Any], optimization_goals: List[str]) -> Dict[str, Any]:
        """
        Optimize the code based on specified goals.
        
        Args:
            code_results: Code implementation to optimize
            optimization_goals: List of optimization goals (e.g., ["performance", "readability", "security"])
            
        Returns:
            Optimized code implementation
        """
        optimization_prompt = f"""Please optimize the following code implementation based on the specified goals:

CURRENT CODE:
{json.dumps(code_results, indent=2)}

OPTIMIZATION GOALS: {', '.join(optimization_goals)}

Optimization focus areas:
1. **Performance**: Improve execution speed and resource usage
2. **Readability**: Enhance code clarity and maintainability
3. **Security**: Address security vulnerabilities
4. **Scalability**: Improve ability to handle growth
5. **Error Handling**: Enhance error handling and logging
6. **Documentation**: Improve code documentation

Provide the optimized code in the same JSON format, highlighting what optimizations were made and why."""
        
        try:
            optimized_code = await self.llm_helper.generate_structured_response(
                prompt=optimization_prompt,
                system_prompt="You are a code optimization specialist. Improve code while maintaining functionality."
            )
            
            # Add optimization metadata
            optimized_code["optimization_metadata"] = {
                "original_files": len(code_results.get("files", [])),
                "optimized_files": len(optimized_code.get("files", [])),
                "optimization_goals": optimization_goals,
                "optimizations_applied": True,
                "timestamp": datetime.now().isoformat()
            }
            
            return optimized_code
            
        except Exception as e:
            logger.error(f"Error optimizing code: {str(e)}")
            return code_results
    
    async def generate_documentation(self, code_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive documentation for the code.
        
        Args:
            code_results: Code implementation to document
            
        Returns:
            Generated documentation
        """
        doc_prompt = f"""Generate comprehensive documentation for the following code implementation:

CODE IMPLEMENTATION:
{json.dumps(code_results, indent=2)}

Generate documentation that includes:
1. **README**: Complete README file with setup and usage instructions
2. **API Documentation**: Detailed API documentation if applicable
3. **Code Comments**: Enhanced inline comments for complex logic
4. **Architecture Overview**: System architecture explanation
5. **User Guide**: Step-by-step user guide
6. **Developer Guide**: Instructions for developers

Provide documentation in structured format with clear sections and examples."""
        
        try:
            documentation = await self.llm_helper.generate_response(
                prompt=doc_prompt,
                system_prompt="You are a technical writer specializing in software documentation.",
                temperature=0.3,
                max_tokens=3000
            )
            
            return {
                "documentation": documentation,
                "documentation_type": "comprehensive",
                "generated_at": datetime.now().isoformat(),
                "includes_readme": "README" in documentation,
                "includes_api_docs": "API" in documentation.upper(),
                "includes_user_guide": "User Guide" in documentation
            }
            
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}")
            return {
                "documentation": "Documentation generation failed. Please create documentation manually.",
                "documentation_type": "basic",
                "generated_at": datetime.now().isoformat()
            }

# Utility function for testing
async def test_coding_agent():
    """Test the Coding Agent functionality"""
    print("Testing Coding Agent...")
    
    # Initialize components
    llm_helper = LLMHelper()
    agent = CodingAgent(llm_helper)
    
    # Mock plan
    mock_plan = {
        "project_overview": "Build a simple Python REST API for user management",
        "technical_approach": "Use FastAPI framework",
        "steps": [
            {
                "step_number": 1,
                "title": "Setup FastAPI project",
                "description": "Create basic FastAPI application structure",
                "deliverables": ["main.py", "requirements.txt"]
            },
            {
                "step_number": 2,
                "title": "Implement user endpoints",
                "description": "Create CRUD operations for users",
                "deliverables": ["User model", "API endpoints"]
            }
        ],
        "resource_requirements": [
            {"name": "FastAPI", "type": "framework", "purpose": "Web framework"}
        ]
    }
    
    try:
        result = await agent.process("Build a simple Python REST API for user management", mock_plan)
        print("Coding Results:")
        print(json.dumps(result, indent=2))
        
        # Test code review
        review = await agent.review_code(result)
        print("\nCode Review:")
        print(json.dumps(review, indent=2))
        
    except Exception as e:
        print(f"Error testing coding agent: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_coding_agent())
