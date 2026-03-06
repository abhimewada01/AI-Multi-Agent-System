#!/usr/bin/env python3
"""
Test script to check if environment variables are loaded correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {bool(api_key)}")
print(f"API Key starts with 'sk-': {api_key.startswith('sk-') if api_key else False}")

if not api_key or api_key == "your_openai_api_key_here":
    print("❌ ERROR: Please set your OpenAI API key in the .env file")
    print("Edit .env file and replace 'your_openai_api_key_here' with your actual API key")
else:
    print("✅ API key is configured correctly")

# Test OpenAI import
try:
    import openai
    print("✅ OpenAI package imported successfully")
    
    # Test client creation
    client = openai.OpenAI(api_key=api_key)
    print("✅ OpenAI client created successfully")
    
except Exception as e:
    print(f"❌ Error with OpenAI: {e}")
