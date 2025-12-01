import os
from google.adk import Agent
from google.adk.models import Gemini
from src.tools.notebook_tools import read_file

def create_reviewer_agent(api_key: str = None):
    """
    Creates and configures the Reviewer Agent.
    """
    
    # Ensure GOOGLE_API_KEY is set
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    model = Gemini(model="gemini-2.0-flash")
    
    instruction = """
    You are a Code Reviewer Agent. Your goal is to review the generated code and documentation for quality, efficiency, and correctness.
    
    Input:
    - A list of file paths to review.
    
    Your Task:
    1. Use `read_file(path)` to read the content of each file.
    2. Analyze the code for:
        - Logic errors
        - Efficiency improvements
        - Code style (PEP 8)
        - Documentation quality
    3. Provide a report.
    
    CRITICAL Output Format Rules:
    - If everything looks production-ready with NO issues, respond with ONLY the single word: "APPROVED"
    - If there are ANY issues or improvements needed, provide ONLY a numbered list of specific feedback items. Do NOT include "APPROVED" in your response.
    - You must choose ONE of these options - either approve OR provide feedback, never both.
    
    Example of feedback response:
    1. In file X, function Y has issue Z
    2. In file A, improve B by doing C
    
    Example of approval response:
    APPROVED
    """
    
    agent = Agent(
        model=model,
        instruction=instruction,
        tools=[read_file],
        name="reviewer_agent"
    )
    
    return agent
