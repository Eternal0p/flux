"""
Script to list all available Gemini models with your API key.
This helps diagnose which models are available.
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file")
    exit(1)

genai.configure(api_key=api_key)

print("=" * 60)
print("AVAILABLE GEMINI MODELS")
print("=" * 60)
print()

try:
    # List all models
    models = genai.list_models()
    
    print(f"Found {len(list(genai.list_models()))} models:")
    print()
    
    for model in models:
        print(f"Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description}")
        print(f"  Supported Methods: {', '.join(model.supported_generation_methods)}")
        print()
        
except Exception as e:
    print(f"Error listing models: {str(e)}")
    print()
    print("This might mean:")
    print("1. Your API key is invalid")
    print("2. You don't have internet connection")
    print("3. The API endpoint is down")

print("=" * 60)
