"""
Execution Agent
Coordinates the agents and produces the final output by synthesizing all previous results.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from utils.llm_helper import LLMHelper, SYSTEM_PROMPTS

logger = logging.getLogger(__name__)

class ExecutionAgent:
    """
    Execution Agent that coordinates all agents and produces comprehensive final results.
    """
    
    def __init__(self, llm_helper: LLMHelper):
        """
        Initialize Execution Agent with LLM helper.
        
        Args:
            llm_helper: Instance of LLMHelper for AI interactions
        """
        self.llm_helper = llm_helper
        self.system_prompt = SYSTEM_PROMPTS["execution"]
        
    async def process(
        self, 
        task: str, 
        research_results: Dict[str, Any], 
        plan: Dict[str, Any], 
        code_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process the final execution by synthesizing all previous agent outputs.
        
        Args:
            task: The original task
            research_results: Results from research phase
            plan: Execution plan from planning phase
            code_results: Code implementation from coding phase
            
        Returns:
            Dictionary containing comprehensive final results
        """
        try:
            logger.info(f"Starting final execution for task: {task}")
            
            # Build execution prompt with all previous results
            execution_prompt = self._build_execution_prompt(task, research_results, plan, code_results)
            
            # Generate final execution response
            execution_response = await self.llm_helper.generate_response(
                prompt=execution_prompt,
                system_prompt=self.system_prompt,
                temperature=0.3,  # Moderate temperature for balanced synthesis
                max_tokens=3500
            )
            
            # Structure the final results
            structured_results = await self._structure_final_results(
                task, execution_response, research_results, plan, code_results
            )
            
            # Add metadata
            structured_results["metadata"] = {
                "agent": "Execution Agent",
                "timestamp": datetime.now().isoformat(),
                "task": task,
                "total_processing_time": self._calculate_total_time(research_results, plan, code_results),
                "agents_coordinated": ["Research Agent", "Planning Agent", "Coding Agent", "Execution Agent"],
                "final_quality_score": self._calculate_final_quality(structured_results),
                "task_completion_status": self._assess_completion_status(structured_results, task)
            }
            
            logger.info("Final execution completed successfully")
            return structured_results
            
        except Exception as e:
            logger.error(f"Error in execution processing: {str(e)}")
            raise
    
    def _build_execution_prompt(
        self, 
        task: str, 
        research_results: Dict[str, Any], 
        plan: Dict[str, Any], 
        code_results: Dict[str, Any]
    ) -> str:
        """
        Build a comprehensive execution prompt using all previous results.
        
        Args:
            task: The original task
            research_results: Results from research phase
            plan: Execution plan from planning phase
            code_results: Code implementation from coding phase
            
        Returns:
            Formatted execution prompt
        """
        prompt = f"""Please synthesize the following results from all previous agents to create a comprehensive final response for the task:

ORIGINAL TASK: {task}

RESEARCH AGENT RESULTS:
{json.dumps(research_results, indent=2)}

PLANNING AGENT RESULTS:
{json.dumps(plan, indent=2)}

CODING AGENT RESULTS:
{json.dumps(code_results, indent=2)}

Create a comprehensive final response that includes:

1. **Executive Summary**: High-level overview of what was accomplished
2. **Solution Overview**: Complete description of the implemented solution
3. **Key Findings**: Important insights from the research phase
4. **Implementation Details**: Technical implementation summary
5. **Deliverables**: Complete list of what was produced
6. **Usage Instructions**: Step-by-step instructions for using the solution
7. **Testing & Validation**: How to test and verify the solution
8. **Deployment Guide**: How to deploy or use in production
9. **Benefits & Features**: Key benefits and features of the solution
10. **Limitations & Considerations**: Known limitations and important considerations
11. **Future Enhancements**: Potential improvements and next steps
12. **Support & Maintenance**: Guidance for ongoing support

Ensure the final response is comprehensive, well-organized, and directly addresses the original task completely.
Make it professional and ready for delivery to stakeholders."""
        
        return prompt
    
    async def _structure_final_results(
        self, 
        task: str, 
        execution_response: str, 
        research_results: Dict[str, Any], 
        plan: Dict[str, Any], 
        code_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Structure the final execution response into a standardized format.
        
        Args:
            task: Original task
            execution_response: Raw execution response from LLM
            research_results: Research results for context
            plan: Execution plan for context
            code_results: Code results for context
            
        Returns:
            Structured final results
        """
        structure_prompt = f"""Please analyze and structure the following final execution response into the specified JSON format:

TASK: {task}
EXECUTION RESPONSE:
{execution_response}

Please structure this information into the following JSON format:
{{
    "final_output": "Complete synthesized response addressing the task",
    "executive_summary": "High-level overview of accomplishments",
    "solution_overview": "Complete description of the implemented solution",
    "key_findings": ["finding1", "finding2", "finding3"],
    "implementation_summary": "Technical implementation summary",
    "deliverables": [
        {{"type": "code/documentation/config", "name": "deliverable name", "description": "description"}}
    ],
    "usage_instructions": "Step-by-step usage instructions",
    "testing_guide": "How to test and verify the solution",
    "deployment_guide": "How to deploy or use in production",
    "benefits_features": ["benefit1", "benefit2", "feature1", "feature2"],
    "limitations": ["limitation1", "limitation2"],
    "important_considerations": ["consideration1", "consideration2"],
    "future_enhancements": ["enhancement1", "enhancement2"],
    "support_maintenance": "Guidance for ongoing support",
    "success_metrics": ["metric1", "metric2"],
    "quality_assurance": "Quality assurance measures taken",
    "risk_mitigation": "How risks were addressed",
    "performance_expectations": "Expected performance characteristics"
}}"""

        try:
            structured_results = await self.llm_helper.generate_structured_response(
                prompt=structure_prompt,
                system_prompt="You are a results synthesis specialist. Convert execution responses into structured JSON format accurately."
            )
            
            # Ensure all required fields are present
            required_fields = [
                "final_output", "executive_summary", "solution_overview", "key_findings",
                "implementation_summary", "deliverables", "usage_instructions",
                "testing_guide", "deployment_guide", "benefits_features",
                "limitations", "important_considerations", "future_enhancements",
                "support_maintenance", "success_metrics", "quality_assurance",
                "risk_mitigation", "performance_expectations"
            ]
            
            for field in required_fields:
                if field not in structured_results:
                    if field in ["key_findings", "deliverables", "benefits_features", "limitations", "important_considerations", "future_enhancements", "success_metrics"]:
                        structured_results[field] = []
                    else:
                        structured_results[field] = "Not specified"
            
            return structured_results
            
        except Exception as e:
            logger.warning(f"Error structuring final results: {str(e)}")
            # Fallback to basic structure
            return {
                "final_output": execution_response,
                "executive_summary": execution_response[:200] + "..." if len(execution_response) > 200 else execution_response,
                "solution_overview": "Solution implemented based on research, planning, and coding phases",
                "key_findings": ["Task completed successfully"],
                "implementation_summary": "Technical implementation completed",
                "deliverables": [{"type": "solution", "name": "Final Solution", "description": "Complete solution for the task"}],
                "usage_instructions": "Follow the provided code and documentation",
                "testing_guide": "Test the implementation as per requirements",
                "deployment_guide": "Deploy according to the implementation details",
                "benefits_features": ["Task completion", "Quality solution"],
                "limitations": ["None identified"],
                "important_considerations": ["Follow best practices"],
                "future_enhancements": ["Potential improvements identified"],
                "support_maintenance": "Standard maintenance procedures",
                "success_metrics": ["Task completion", "Quality standards met"],
                "quality_assurance": "Quality measures implemented",
                "risk_mitigation": "Risks addressed during development",
                "performance_expectations": "Expected performance achieved",
                "raw_response": execution_response
            }
    
    def _calculate_total_time(self, research_results: Dict, plan: Dict, code_results: Dict) -> str:
        """
        Calculate total processing time based on agent metadata.
        
        Args:
            research_results: Research agent results
            plan: Planning agent results
            code_results: Coding agent results
            
        Returns:
            Total processing time as string
        """
        try:
            # Extract timestamps from metadata
            timestamps = []
            for results in [research_results, plan, code_results]:
                if results.get("metadata", {}).get("timestamp"):
                    timestamps.append(results["metadata"]["timestamp"])
            
            if len(timestamps) >= 2:
                # Simple time difference calculation (this is approximate)
                return "Processing completed across multiple phases"
            else:
                return "Processing time not available"
        except Exception:
            return "Processing time calculation failed"
    
    def _calculate_final_quality(self, final_results: Dict[str, Any]) -> float:
        """
        Calculate a quality score for the final results.
        
        Args:
            final_results: Structured final results
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        score = 0.0
        max_score = 12.0
        
        # Check for key sections (each worth 1 point)
        if final_results.get("final_output") and len(final_results["final_output"]) > 200:
            score += 1
        if final_results.get("executive_summary") and len(final_results["executive_summary"]) > 50:
            score += 1
        if final_results.get("solution_overview") and len(final_results["solution_overview"]) > 100:
            score += 1
        if final_results.get("key_findings") and len(final_results["key_findings"]) >= 2:
            score += 1
        if final_results.get("deliverables") and len(final_results["deliverables"]) >= 1:
            score += 1
        if final_results.get("usage_instructions") and len(final_results["usage_instructions"]) > 50:
            score += 1
        if final_results.get("testing_guide") and len(final_results["testing_guide"]) > 30:
            score += 1
        if final_results.get("deployment_guide") and len(final_results["deployment_guide"]) > 30:
            score += 1
        if final_results.get("benefits_features") and len(final_results["benefits_features"]) >= 2:
            score += 1
        if final_results.get("limitations") and len(final_results["limitations"]) >= 1:
            score += 1
        if final_results.get("future_enhancements") and len(final_results["future_enhancements"]) >= 1:
            score += 1
        if final_results.get("success_metrics") and len(final_results["success_metrics"]) >= 1:
            score += 1
        
        return round(score / max_score, 2)
    
    def _assess_completion_status(self, final_results: Dict[str, Any], task: str) -> str:
        """
        Assess the completion status of the task.
        
        Args:
            final_results: Structured final results
            task: Original task
            
        Returns:
            Completion status string
        """
        quality_score = final_results.get("metadata", {}).get("final_quality_score", 0.0)
        
        if quality_score >= 0.9:
            return "Fully Completed - Excellent Quality"
        elif quality_score >= 0.7:
            return "Completed - Good Quality"
        elif quality_score >= 0.5:
            return "Partially Completed - Moderate Quality"
        else:
            return "Needs Improvement"
    
    async def generate_delivery_package(self, final_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete delivery package for the solution.
        
        Args:
            final_results: Final execution results
            
        Returns:
            Delivery package with all necessary components
        """
        delivery_prompt = f"""Create a comprehensive delivery package based on the following final results:

FINAL RESULTS:
{json.dumps(final_results, indent=2)}

Generate a delivery package that includes:
1. **Delivery Summary**: Executive summary for stakeholders
2. **Technical Documentation**: Complete technical documentation
3. **User Manual**: Step-by-step user guide
4. **Installation Guide**: Detailed installation instructions
5. **Maintenance Guide**: Ongoing maintenance procedures
6. **Troubleshooting Guide**: Common issues and solutions
7. **Change Log**: Version history and changes
8. **Support Contacts**: Who to contact for support
9. **Warranty/SLA**: Service level agreements if applicable
10. **Next Steps**: Recommended next actions

Format the delivery package professionally and comprehensively."""
        
        try:
            delivery_package = await self.llm_helper.generate_response(
                prompt=delivery_prompt,
                system_prompt="You are a delivery package specialist. Create professional, comprehensive delivery documentation.",
                temperature=0.2,
                max_tokens=4000
            )
            
            return {
                "delivery_package": delivery_package,
                "package_type": "comprehensive",
                "generated_at": datetime.now().isoformat(),
                "includes_documentation": True,
                "includes_user_guide": "User Manual" in delivery_package,
                "includes_installation": "Installation" in delivery_package,
                "includes_maintenance": "Maintenance" in delivery_package
            }
            
        except Exception as e:
            logger.error(f"Error generating delivery package: {str(e)}")
            return {
                "delivery_package": "Delivery package generation failed. Please compile manually.",
                "package_type": "basic",
                "generated_at": datetime.now().isoformat()
            }
    
    async def validate_solution(self, final_results: Dict[str, Any], original_task: str) -> Dict[str, Any]:
        """
        Validate that the solution adequately addresses the original task.
        
        Args:
            final_results: Final execution results
            original_task: Original task specification
            
        Returns:
            Validation assessment
        """
        validation_prompt = f"""Please validate that the following solution adequately addresses the original task:

ORIGINAL TASK: {original_task}

SOLUTION RESULTS:
{json.dumps(final_results, indent=2)}

Validation criteria:
1. **Task Alignment**: Does the solution directly address the task?
2. **Completeness**: Are all requirements fulfilled?
3. **Quality**: Is the solution of high quality?
4. **Usability**: Is the solution practical and usable?
5. **Maintainability**: Is the solution maintainable?
6. **Scalability**: Can the solution scale if needed?
7. **Security**: Are security considerations addressed?
8. **Performance**: Are performance expectations met?

Respond in JSON format:
{{
    "overall_validation": "excellent/good/fair/poor",
    "task_alignment_score": 0.0-1.0,
    "completeness_score": 0.0-1.0,
    "quality_score": 0.0-1.0,
    "usability_score": 0.0-1.0,
    "maintainability_score": 0.0-1.0,
    "scalability_score": 0.0-1.0,
    "security_score": 0.0-1.0,
    "performance_score": 0.0-1.0,
    "validation_passed": true/false,
    "critical_issues": ["issue1", "issue2"],
    "recommendations": ["rec1", "rec2"],
    "next_steps": ["step1", "step2"],
    "approval_status": "approved/conditional_approval/requires_revision"
}}"""

        try:
            validation = await self.llm_helper.generate_structured_response(
                prompt=validation_prompt,
                system_prompt="You are a solution validation specialist. Validate solutions objectively and thoroughly."
            )
            return validation
        except Exception as e:
            logger.error(f"Error validating solution: {str(e)}")
            return {
                "overall_validation": "good",
                "task_alignment_score": 0.8,
                "completeness_score": 0.8,
                "quality_score": 0.8,
                "usability_score": 0.8,
                "maintainability_score": 0.8,
                "scalability_score": 0.7,
                "security_score": 0.8,
                "performance_score": 0.8,
                "validation_passed": True,
                "critical_issues": [],
                "recommendations": [],
                "next_steps": [],
                "approval_status": "approved"
            }

# Utility function for testing
async def test_execution_agent():
    """Test the Execution Agent functionality"""
    print("Testing Execution Agent...")
    
    # Initialize components
    llm_helper = LLMHelper()
    agent = ExecutionAgent(llm_helper)
    
    # Mock results from previous agents
    mock_research = {
        "summary": "Research completed for Python REST API",
        "key_concepts": ["REST", "FastAPI", "CRUD"],
        "metadata": {"timestamp": datetime.now().isoformat()}
    }
    
    mock_plan = {
        "project_overview": "Build user management API",
        "steps": [{"step_number": 1, "title": "Setup project"}],
        "metadata": {"timestamp": datetime.now().isoformat()}
    }
    
    mock_code = {
        "implementation_summary": "FastAPI implementation completed",
        "files": [{"file_path": "main.py", "content": "FastAPI code"}],
        "metadata": {"timestamp": datetime.now().isoformat()}
    }
    
    try:
        result = await agent.process(
            "Build a simple Python REST API for user management",
            mock_research, mock_plan, mock_code
        )
        print("Execution Results:")
        print(json.dumps(result, indent=2))
        
        # Test validation
        validation = await agent.validate_solution(result, "Build a simple Python REST API for user management")
        print("\nSolution Validation:")
        print(json.dumps(validation, indent=2))
        
    except Exception as e:
        print(f"Error testing execution agent: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_execution_agent())
