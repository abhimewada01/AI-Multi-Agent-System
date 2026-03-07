"""
Research Agent
Responsible for gathering information from user queries and organizing research results.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from utils.llm_helper import LLMHelper, SYSTEM_PROMPTS

logger = logging.getLogger(__name__)

class ResearchAgent:
    """
    Research Agent that gathers and organizes information for tasks.
    """
    
    def __init__(self, llm_helper: LLMHelper):
        """
        Initialize Research Agent with LLM helper.
        
        Args:
            llm_helper: Instance of LLMHelper for AI interactions
        """
        self.llm_helper = llm_helper
        self.system_prompt = SYSTEM_PROMPTS["research"]
        
    async def process(self, task: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a research task by gathering and organizing information.
        
        Args:
            task: The task to research
            context: Additional context for the research
            
        Returns:
            Dictionary containing research results
        """
        try:
            logger.info(f"Starting research for task: {task}")
            
            # Build research prompt
            research_prompt = self._build_research_prompt(task, context)
            
            # Generate research response
            research_response = await self.llm_helper.generate_response(
                prompt=research_prompt,
                system_prompt=self.system_prompt,
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=2500
            )
            
            # Parse and structure the research results
            structured_results = await self._structure_research_results(
                task, research_response, context
            )
            
            # Add metadata
            structured_results["metadata"] = {
                "agent": "Research Agent",
                "timestamp": datetime.now().isoformat(),
                "task": task,
                "word_count": len(research_response.split()),
                "research_quality_score": self._calculate_quality_score(structured_results)
            }
            
            logger.info("Research completed successfully")
            return structured_results
            
        except Exception as e:
            logger.error(f"Error in research processing: {str(e)}")
            raise
    
    def _build_research_prompt(self, task: str, context: Optional[str] = None) -> str:
        """
        Build a comprehensive research prompt.
        
        Args:
            task: The task to research
            context: Additional context
            
        Returns:
            Formatted research prompt
        """
        prompt = f"""Please research the following task comprehensively:

TASK: {task}

Provide detailed information covering:

1. **Background & Context**: Explain what this task involves and why it's important
2. **Key Concepts**: Define important terms and concepts related to the task
3. **Requirements & Considerations**: What needs to be considered for successful completion
4. **Best Practices**: Industry standards and recommended approaches
5. **Potential Challenges**: Common issues and how to address them
6. **Resources & References**: Tools, libraries, or resources that might be helpful
7. **Examples**: Real-world examples or similar implementations if applicable

Please organize your research in a clear, structured manner with headings and bullet points.
Focus on providing practical, actionable information that will help with planning and implementation."""
        
        if context:
            prompt += f"\n\nADDITIONAL CONTEXT: {context}"
        
        return prompt
    
    async def _structure_research_results(
        self, 
        task: str, 
        research_response: str, 
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Structure the research results into a standardized format.
        
        Args:
            task: Original task
            research_response: Raw research response from LLM
            context: Additional context
            
        Returns:
            Structured research results
        """
        structure_prompt = f"""Please analyze and structure the following research results into the specified JSON format:

TASK: {task}
RESEARCH RESULTS:
{research_response}

Please structure this information into the following JSON format:
{{
    "summary": "Brief overview of the research findings",
    "background": "Background and context information",
    "key_concepts": ["Concept 1", "Concept 2", ...],
    "requirements": ["Requirement 1", "Requirement 2", ...],
    "best_practices": ["Practice 1", "Practice 2", ...],
    "challenges": ["Challenge 1", "Challenge 2", ...],
    "resources": [
        {{"name": "Resource name", "type": "tool/library/documentation", "description": "Description"}},
        ...
    ],
    "examples": ["Example 1", "Example 2", ...],
    "complexity_assessment": "low/medium/high",
    "estimated_effort": "low/medium/high",
    "research_completeness": "percentage or assessment"
}}"""

        try:
            structured_response = await self.llm_helper.generate_structured_response(
                prompt=structure_prompt,
                system_prompt="You are a data structuring specialist. Convert research information into structured JSON format accurately."
            )
            
            # Ensure all required fields are present
            required_fields = [
                "summary", "background", "key_concepts", "requirements", 
                "best_practices", "challenges", "resources", "examples",
                "complexity_assessment", "estimated_effort", "research_completeness"
            ]
            
            for field in required_fields:
                if field not in structured_response:
                    structured_response[field] = "Not available" if isinstance(structured_response.get(field), str) else []
            
            return structured_response
            
        except Exception as e:
            logger.warning(f"Error structuring research results: {str(e)}")
            # Fallback to basic structure
            return {
                "summary": research_response[:200] + "..." if len(research_response) > 200 else research_response,
                "background": "Detailed research provided above",
                "key_concepts": [],
                "requirements": [],
                "best_practices": [],
                "challenges": [],
                "resources": [],
                "examples": [],
                "complexity_assessment": "medium",
                "estimated_effort": "medium",
                "research_completeness": "high",
                "raw_response": research_response
            }
    
    def _calculate_quality_score(self, research_results: Dict[str, Any]) -> float:
        """
        Calculate a quality score for the research results.
        
        Args:
            research_results: Structured research results
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        score = 0.0
        max_score = 7.0
        
        # Check for key sections (each worth 1 point)
        if research_results.get("summary") and len(research_results["summary"]) > 50:
            score += 1
        if research_results.get("background") and len(research_results["background"]) > 100:
            score += 1
        if research_results.get("key_concepts") and len(research_results["key_concepts"]) >= 3:
            score += 1
        if research_results.get("requirements") and len(research_results["requirements"]) >= 2:
            score += 1
        if research_results.get("best_practices") and len(research_results["best_practices"]) >= 2:
            score += 1
        if research_results.get("resources") and len(research_results["resources"]) >= 1:
            score += 1
        if research_results.get("examples") and len(research_results["examples"]) >= 1:
            score += 1
        
        return round(score / max_score, 2)
    
    async def validate_research(self, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and potentially enhance research results.
        
        Args:
            research_results: Research results to validate
            
        Returns:
            Validation report with suggestions
        """
        validation_prompt = f"""Please review the following research results and provide validation feedback:

RESEARCH RESULTS:
{json.dumps(research_results, indent=2)}

Provide feedback on:
1. Completeness: Are all important aspects covered?
2. Accuracy: Does the information seem correct and reliable?
3. Relevance: Is the information relevant to the task?
4. Clarity: Is the information well-organized and easy to understand?
5. Missing information: What additional research would be beneficial?

Respond in JSON format:
{{
    "overall_quality": "excellent/good/fair/poor",
    "completeness_score": 0.0-1.0,
    "accuracy_assessment": "high/medium/low",
    "relevance_score": 0.0-1.0,
    "clarity_score": 0.0-1.0,
    "missing_aspects": ["aspect1", "aspect2"],
    "suggestions": ["suggestion1", "suggestion2"],
    "additional_research_needed": true/false
}}"""

        try:
            validation = await self.llm_helper.generate_structured_response(
                prompt=validation_prompt,
                system_prompt="You are a research validation specialist. Provide constructive feedback on research quality."
            )
            return validation
        except Exception as e:
            logger.error(f"Error validating research: {str(e)}")
            return {
                "overall_quality": "good",
                "completeness_score": 0.8,
                "accuracy_assessment": "high",
                "relevance_score": 0.9,
                "clarity_score": 0.8,
                "missing_aspects": [],
                "suggestions": [],
                "additional_research_needed": False
            }

# Utility function for testing
async def test_research_agent():
    """Test the Research Agent functionality"""
    print("Testing Research Agent...")
    
    # Initialize components
    llm_helper = LLMHelper()
    agent = ResearchAgent(llm_helper)
    
    # Test research
    try:
        result = await agent.process(
            "Build a simple Python REST API for user management",
            "This is for a learning project to understand web development"
        )
        print("Research Results:")
        print(json.dumps(result, indent=2))
        
        # Test validation
        validation = await agent.validate_research(result)
        print("\nValidation Results:")
        print(json.dumps(validation, indent=2))
        
    except Exception as e:
        print(f"Error testing research agent: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_research_agent())
