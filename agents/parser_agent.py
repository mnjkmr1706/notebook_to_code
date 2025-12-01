import os
from google.adk import Agent
from google.adk.models import Gemini
from src.tools.notebook_tools import read_notebook

from src.callbacks.pii_guardrail import pii_guardrail

def create_parser_agent(api_key: str = None):
    """
    Creates and configures the Parser Agent.
    """
    
    # Ensure GOOGLE_API_KEY is set
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    model = Gemini(model="gemini-2.0-flash")
    
    instruction = """
    You are a Notebook Parser Agent. Your goal is to take a raw Jupyter Notebook and extract two things:
    1. A clean string representation of the code.
    2. A markdown string containing the documentation and context found in the notebook.
    
    You have access to `read_notebook(path)`.
    
    When asked to parse a notebook:
    1. Read it using the tool.
    2. Analyze the content.
    3. Return a JSON-formatted string with keys "code" and "documentation".
    """
    
    agent = Agent(
        model=model,
        instruction=instruction,
        tools=[read_notebook],
        name="parser_agent",
        before_agent_callback=pii_guardrail
    )
    
    return agent
