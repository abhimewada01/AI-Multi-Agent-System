"""
Planning Agent
Breaks down problems into smaller tasks and creates step-by-step execution plans.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from utils.llm_helper import LLMHelper, SYSTEM_PROMPTS

logger = logging.getLogger(__name__)

class PlanningAgent:
    """
    Planning Agent that breaks down complex tasks into manageable steps.
    """
    
    def __init__(self, llm_helper: LLMHelper):
        """
        Initialize Planning Agent with LLM helper.
        
        Args:
            llm_helper: Instance of LLMHelper for AI interactions
        """
        self.llm_helper = llm_helper
        self.system_prompt = SYSTEM_PROMPTS["planning"]
        
    async def process(self, task: str, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a planning task by breaking down the problem into steps.
        
        Args:
            task: The original task to plan
            research_results: Results from the research phase
            
        Returns:
            Dictionary containing the execution plan
        """
        try:
            logger.info(f"Starting planning for task: {task}")
            
            # Analyze research and build planning prompt
            planning_prompt = self._build_planning_prompt(task, research_results)
            
            # Generate planning response
            planning_response = await self.llm_helper.generate_response(
                prompt=planning_prompt,
                system_prompt=self.system_prompt,
                temperature=0.2,  # Lower temperature for more structured planning
                max_tokens=3000
            )
            
            # Structure the plan
            structured_plan = await self._structure_execution_plan(
                task, planning_response, research_results
            )
            
            # Add metadata
            structured_plan["metadata"] = {
                "agent": "Planning Agent",
                "timestamp": datetime.now().isoformat(),
                "task": task,
                "total_steps": len(structured_plan.get("steps", [])),
                "estimated_duration": structured_plan.get("estimated_duration", "unknown"),
                "complexity_level": structured_plan.get("complexity_level", "medium"),
                "plan_quality_score": self._calculate_plan_quality(structured_plan)
            }
            
            logger.info("Planning completed successfully")
            return structured_plan
            
        except Exception as e:
            logger.error(f"Error in planning processing: {str(e)}")
            raise
    
    def _build_planning_prompt(self, task: str, research_results: Dict[str, Any]) -> str:
        """
        Build a comprehensive planning prompt based on research results.
        
        Args:
            task: The original task
            research_results: Results from research phase
            
        Returns:
            Formatted planning prompt
        """
        prompt = f"""Based on the following research results, create a detailed execution plan for the task:

ORIGINAL TASK: {task}

RESEARCH RESULTS:
{json.dumps(research_results, indent=2)}

Please create a comprehensive execution plan that includes:

1. **Project Overview**: Brief summary of what needs to be accomplished
2. **Technical Approach**: Recommended methodology and technologies
3. **Execution Steps**: Detailed step-by-step breakdown with:
   - Step number and title
   - Description of what needs to be done
   - Estimated time/effort
   - Dependencies on other steps
   - Expected outputs/deliverables
   - Potential risks and mitigation strategies

4. **Resource Requirements**: Tools, libraries, or resources needed
5. **Testing Strategy**: How to validate and test each step
6. **Deployment/Delivery**: How the final result will be delivered
7. **Timeline**: Rough timeline for completion
8. **Success Criteria**: How to determine if the task is successfully completed

Organize the plan logically, considering dependencies and workflow. Be specific and actionable in each step."""
        
        return prompt
    
    async def _structure_execution_plan(
        self, 
        task: str, 
        planning_response: str, 
        research_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Structure the planning response into a standardized format.
        
        Args:
            task: Original task
            planning_response: Raw planning response from LLM
            research_results: Research results for context
            
        Returns:
            Structured execution plan
        """
        structure_prompt = f"""Please analyze and structure the following execution plan into the specified JSON format:

TASK: {task}
PLANNING RESPONSE:
{planning_response}

Please structure this information into the following JSON format:
{{
    "project_overview": "Brief summary of the project",
    "technical_approach": "Recommended methodology and technologies",
    "complexity_level": "low/medium/high",
    "estimated_duration": "time estimate (e.g., '2-3 hours', '1-2 days')",
    "steps": [
        {{
            "step_number": 1,
            "title": "Step title",
            "description": "Detailed description of what needs to be done",
            "estimated_effort": "time estimate (e.g., '30 minutes', '1 hour')",
            "dependencies": [],
            "deliverables": ["deliverable1", "deliverable2"],
            "risks": ["risk1", "risk2"],
            "mitigation_strategies": ["strategy1", "strategy2"]
        }}
    ],
    "resource_requirements": [
        {{"name": "Resource name", "type": "tool/library/service", "purpose": "Why it's needed"}}
    ],
    "testing_strategy": "How to validate and test the solution",
    "deployment_approach": "How the final result will be delivered",
    "timeline": "Rough timeline for completion",
    "success_criteria": ["criteria1", "criteria2", "criteria3"],
    "alternative_approaches": ["alternative1", "alternative2"],
    "contingency_plans": ["plan1", "plan2"]
}}"""

        try:
            structured_plan = await self.llm_helper.generate_structured_response(
                prompt=structure_prompt,
                system_prompt="You are a project planning specialist. Convert planning information into structured JSON format accurately."
            )
            
            # Ensure all required fields are present
            required_fields = [
                "project_overview", "technical_approach", "complexity_level", 
                "estimated_duration", "steps", "resource_requirements",
                "testing_strategy", "deployment_approach", "timeline", "success_criteria"
            ]
            
            for field in required_fields:
                if field not in structured_plan:
                    if field == "steps":
                        structured_plan[field] = []
                    elif field in ["resource_requirements", "success_criteria", "alternative_approaches", "contingency_plans"]:
                        structured_plan[field] = []
                    else:
                        structured_plan[field] = "Not specified"
            
            # Validate steps structure
            if structured_plan.get("steps"):
                for i, step in enumerate(structured_plan["steps"]):
                    if not isinstance(step, dict):
                        continue
                    
                    required_step_fields = [
                        "step_number", "title", "description", "estimated_effort",
                        "dependencies", "deliverables", "risks", "mitigation_strategies"
                    ]
                    
                    for field in required_step_fields:
                        if field not in step:
                            if field in ["dependencies", "deliverables", "risks", "mitigation_strategies"]:
                                step[field] = []
                            else:
                                step[field] = "Not specified"
            
            return structured_plan
            
        except Exception as e:
            logger.warning(f"Error structuring execution plan: {str(e)}")
            # Fallback to basic structure
            return {
                "project_overview": planning_response[:200] + "..." if len(planning_response) > 200 else planning_response,
                "technical_approach": "Based on research findings",
                "complexity_level": research_results.get("complexity_assessment", "medium"),
                "estimated_duration": "To be determined",
                "steps": [
                    {
                        "step_number": 1,
                        "title": "Implementation",
                        "description": "Execute the task based on research",
                        "estimated_effort": "TBD",
                        "dependencies": [],
                        "deliverables": ["Final solution"],
                        "risks": ["Technical challenges"],
                        "mitigation_strategies": ["Research and testing"]
                    }
                ],
                "resource_requirements": [],
                "testing_strategy": "Manual testing and validation",
                "deployment_approach": "Direct delivery",
                "timeline": "Flexible",
                "success_criteria": ["Task completion"],
                "alternative_approaches": [],
                "contingency_plans": [],
                "raw_response": planning_response
            }
    
    def _calculate_plan_quality(self, plan: Dict[str, Any]) -> float:
        """
        Calculate a quality score for the execution plan.
        
        Args:
            plan: Structured execution plan
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        score = 0.0
        max_score = 10.0
        
        # Check for key sections (each worth 1 point)
        if plan.get("project_overview") and len(plan["project_overview"]) > 50:
            score += 1
        if plan.get("technical_approach") and len(plan["technical_approach"]) > 50:
            score += 1
        if plan.get("steps") and len(plan["steps"]) >= 2:
            score += 1
        if plan.get("resource_requirements") and len(plan["resource_requirements"]) >= 1:
            score += 1
        if plan.get("testing_strategy") and len(plan["testing_strategy"]) > 30:
            score += 1
        if plan.get("deployment_approach") and len(plan["deployment_approach"]) > 30:
            score += 1
        if plan.get("success_criteria") and len(plan["success_criteria"]) >= 2:
            score += 1
        if plan.get("timeline") and plan["timeline"] != "Flexible":
            score += 1
        
        # Bonus points for detailed steps
        if plan.get("steps"):
            detailed_steps = sum(1 for step in plan["steps"] 
                              if isinstance(step, dict) and 
                              step.get("description") and len(step["description"]) > 100)
            if detailed_steps >= len(plan["steps"]) * 0.8:
                score += 1
            if detailed_steps >= len(plan["steps"]) * 0.5:
                score += 0.5
        
        return round(score / max_score, 2)
    
    async def optimize_plan(self, plan: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize the execution plan based on given constraints.
        
        Args:
            plan: Current execution plan
            constraints: Constraints like time limit, resource limits, etc.
            
        Returns:
            Optimized execution plan
        """
        optimization_prompt = f"""Please optimize the following execution plan based on the given constraints:

CURRENT PLAN:
{json.dumps(plan, indent=2)}

CONSTRAINTS:
{json.dumps(constraints, indent=2)}

Optimization goals:
1. Reduce complexity while maintaining quality
2. Minimize resource usage
3. Shorten timeline if possible
4. Combine or eliminate redundant steps
5. Prioritize critical path items

Provide the optimized plan in the same JSON format, highlighting what changes were made and why."""
        
        try:
            optimized_plan = await self.llm_helper.generate_structured_response(
                prompt=optimization_prompt,
                system_prompt="You are a project optimization specialist. Improve plans while maintaining quality and feasibility."
            )
            
            # Add optimization metadata
            optimized_plan["optimization_metadata"] = {
                "original_steps": len(plan.get("steps", [])),
                "optimized_steps": len(optimized_plan.get("steps", [])),
                "original_duration": plan.get("estimated_duration"),
                "optimized_duration": optimized_plan.get("estimated_duration"),
                "optimization_applied": True,
                "timestamp": datetime.now().isoformat()
            }
            
            return optimized_plan
            
        except Exception as e:
            logger.error(f"Error optimizing plan: {str(e)}")
            return plan
    
    async def validate_plan_feasibility(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the feasibility of the execution plan.
        
        Args:
            plan: Execution plan to validate
            
        Returns:
            Feasibility assessment
        """
        validation_prompt = f"""Please validate the feasibility of the following execution plan:

EXECUTION PLAN:
{json.dumps(plan, indent=2)}

Assess:
1. **Technical Feasibility**: Are the technical approaches realistic?
2. **Resource Availability**: Are the required resources commonly available?
3. **Timeline Realism**: Is the estimated timeline reasonable?
4. **Risk Assessment**: Are risks properly identified and mitigated?
5. **Completeness**: Does the plan cover all necessary aspects?
6. **Dependency Logic**: Are step dependencies logical and achievable?

Respond in JSON format:
{{
    "overall_feasibility": "high/medium/low",
    "technical_feasibility": "high/medium/low",
    "resource_feasibility": "high/medium/low",
    "timeline_feasibility": "high/medium/low",
    "risk_assessment": "adequate/some_concerns/inadequate",
    "completeness_score": 0.0-1.0,
    "dependency_logic_score": 0.0-1.0,
    "concerns": ["concern1", "concern2"],
    "recommendations": ["recommendation1", "recommendation2"],
    "modifications_suggested": ["modification1", "modification2"]
}}"""

        try:
            validation = await self.llm_helper.generate_structured_response(
                prompt=validation_prompt,
                system_prompt="You are a project validation specialist. Assess plan feasibility objectively."
            )
            return validation
        except Exception as e:
            logger.error(f"Error validating plan feasibility: {str(e)}")
            return {
                "overall_feasibility": "medium",
                "technical_feasibility": "medium",
                "resource_feasibility": "high",
                "timeline_feasibility": "medium",
                "risk_assessment": "adequate",
                "completeness_score": 0.8,
                "dependency_logic_score": 0.8,
                "concerns": [],
                "recommendations": [],
                "modifications_suggested": []
            }

# Utility function for testing
async def test_planning_agent():
    """Test the Planning Agent functionality"""
    print("Testing Planning Agent...")
    
    # Initialize components
    llm_helper = LLMHelper()
    agent = PlanningAgent(llm_helper)
    
    # Mock research results
    mock_research = {
        "summary": "Building a Python REST API for user management",
        "key_concepts": ["REST API", "FastAPI", "CRUD operations"],
        "requirements": ["User authentication", "Data validation"],
        "complexity_assessment": "medium",
        "resources": [{"name": "FastAPI", "type": "framework"}]
    }
    
    try:
        result = await agent.process("Build a simple Python REST API for user management", mock_research)
        print("Planning Results:")
        print(json.dumps(result, indent=2))
        
        # Test feasibility validation
        validation = await agent.validate_plan_feasibility(result)
        print("\nFeasibility Validation:")
        print(json.dumps(validation, indent=2))
        
    except Exception as e:
        print(f"Error testing planning agent: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_planning_agent())
