import os
from google.adk import Agent
from google.adk.models import Gemini
from src.tools.notebook_tools import write_file

def create_refactorer_agent(api_key: str = None):
    """
    Creates and configures the Refactorer Agent.
    """
    
    # Ensure GOOGLE_API_KEY is set
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    model = Gemini(model="gemini-2.0-flash")
    
    instruction = """
    You are a Code Refactoring Agent. Your goal is to write production-ready Python code based on a provided folder structure plan and raw notebook code.
    
    Input:
    - Architecture Plan (JSON)
    - Raw Code (String)
    - Documentation/Context (String)
    
    Your Task:
    1. Analyze the input.
    2. For EACH file defined in the Architecture Plan, generate the appropriate code.
    3. Use the `write_file(path, content)` tool to write the code to disk.
    
    Guidelines:
    - Ensure code is modular, clean, and follows PEP 8.
    - Add docstrings to functions and classes.
    - Use the provided context to understand the logic.
    - Do NOT write placeholder code if possible; implement the logic from the notebook.
    """
    
    agent = Agent(
        model=model,
        instruction=instruction,
        tools=[write_file],
        name="refactorer_agent"
    )
    
    return agent
