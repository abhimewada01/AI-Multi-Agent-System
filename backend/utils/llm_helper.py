"""
LLM Helper Utility
Centralized interface for interacting with Language Models.
Supports OpenAI API and can be extended for other LLM providers.
"""

import os
import json
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LLMConfig:
    """Configuration for LLM provider"""
    provider: str = "openai"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 2000
    api_key: Optional[str] = None

class LLMHelper:
    """
    Helper class for interacting with Language Models.
    Provides a unified interface for different LLM providers.
    """
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """
        Initialize LLM Helper with configuration.
        
        Args:
            config: LLM configuration object
        """
        self.config = config or LLMConfig()
        self._setup_provider()
        
    def _setup_provider(self):
        """Setup the LLM provider based on configuration"""
        if self.config.provider == "openai":
            self._setup_openai()
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
    
    def _setup_openai(self):
        """Setup OpenAI client"""
        try:
            import openai
            self.client = openai.OpenAI(
                api_key=self.config.api_key or os.getenv("OPENAI_API_KEY")
            )
            logger.info("OpenAI client initialized successfully")
        except ImportError:
            logger.error("OpenAI package not installed. Install with: pip install openai")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            raise
    
    async def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            Generated response as string
        """
        try:
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add user prompt
            messages.append({"role": "user", "content": prompt})
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=temperature or self.config.temperature,
                max_tokens=max_tokens or self.config.max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    async def generate_structured_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        output_format: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate a structured response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            output_format: Expected output format specification
            
        Returns:
            Structured response as dictionary
        """
        try:
            # Add format instructions to prompt
            if output_format:
                format_instruction = f"\n\nPlease respond in the following JSON format:\n{json.dumps(output_format, indent=2)}"
                prompt += format_instruction
            
            response_text = await self.generate_response(prompt, system_prompt)
            
            # Try to parse as JSON
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # If not valid JSON, return as text
                return {"response": response_text}
                
        except Exception as e:
            logger.error(f"Error generating structured response: {str(e)}")
            raise
    
    def get_token_count(self, text: str) -> int:
        """
        Estimate token count for given text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Estimated token count
        """
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model(self.config.model)
            return len(encoding.encode(text))
        except ImportError:
            # Fallback estimation (rough approximation: 1 token ≈ 4 characters)
            return len(text) // 4
    
    def validate_api_key(self) -> bool:
        """
        Validate that the API key is properly configured.
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            if self.config.provider == "openai":
                # Simple validation by checking if key exists and has reasonable format
                api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
                return api_key is not None and api_key.startswith("sk-")
            return False
        except Exception:
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration.
        
        Returns:
            Dictionary with model information
        """
        return {
            "provider": self.config.provider,
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "api_key_configured": self.validate_api_key()
        }

# Predefined system prompts for different agents
SYSTEM_PROMPTS = {
    "research": """You are a Research Agent specializing in gathering and organizing information. 
Your task is to research the given topic and provide comprehensive, well-structured information.
Focus on accuracy, relevance, and clarity. Organize your findings logically.""",
    
    "planning": """You are a Planning Agent that breaks down complex tasks into manageable steps.
Your task is to analyze the research information and create a detailed, step-by-step plan.
Be specific, logical, and consider dependencies between steps.""",
    
    "coding": """You are a Coding Agent that generates technical solutions and code.
Your task is to implement the plan by generating clean, well-documented code.
Focus on best practices, error handling, and maintainability.""",
    
    "execution": """You are an Execution Agent that coordinates and produces final results.
Your task is to synthesize all previous outputs and create a comprehensive final response.
Ensure the solution addresses the original task completely and professionally."""
}

# Example usage and testing functions
async def test_llm_helper():
    """Test the LLM Helper functionality"""
    print("Testing LLM Helper...")
    
    # Initialize helper
    helper = LLMHelper()
    
    # Check configuration
    print("Model Info:", helper.get_model_info())
    
    # Test basic response
    try:
        response = await helper.generate_response(
            "What is artificial intelligence?",
            system_prompt="You are a helpful AI assistant."
        )
        print("Basic Response:", response[:100] + "...")
    except Exception as e:
        print("Error in basic response:", str(e))
    
    # Test structured response
    try:
        structured = await helper.generate_structured_response(
            "List 3 key benefits of Python programming",
            output_format={"benefits": ["string"], "summary": "string"}
        )
        print("Structured Response:", structured)
    except Exception as e:
        print("Error in structured response:", str(e))

if __name__ == "__main__":
    asyncio.run(test_llm_helper())
