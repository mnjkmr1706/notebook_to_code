import json
import nbformat
import sys
from pathlib import Path

# Add parent directory to path to import src module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm import get_llm


# Example usage of get_llm in different agents:
# ============================================

# Example 1: Initialize LLM with default settings
# llm = get_llm("gemini-2.0-flash")

# Example 2: Initialize LLM with custom system prompt
# prompt = "You are an expert Python code analyst. Analyze the provided code and provide detailed insights."
# llm = get_llm("gemini-1.5-pro", prompt=prompt)

# Example 3: Use the LLM to generate content
# response = llm.generate_content("Analyze this Python function: def hello(): pass")
# print(response.text)
