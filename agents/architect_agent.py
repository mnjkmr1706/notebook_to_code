import os
from google.adk import Agent
from google.adk.models import Gemini

def create_architect_agent(api_key: str = None):
    """
    Creates and configures the Architect Agent.
    """
    
    # Ensure GOOGLE_API_KEY is set
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    model = Gemini(model="gemini-2.0-flash")
    
    instruction = """
    You are a Software Architect Agent. Your goal is to design a robust, production-ready folder structure for a Python project based on provided code and documentation.
    
    Input:
    - Code string (from a notebook)
    - Documentation string
    
    Output:
    - A JSON structure representing the file system.
    - Keys are filenames/directories.
    - Values are descriptions of what should go in them.
    
    Example Output:
    {
        "OUTPUT/src": {
            "data_loader.py": "Functions for loading and preprocessing data",
            "model.py": "Model definition class",
            "train.py": "Training loop"
        },
        "OUTPUT/requirements.txt": "List of dependencies",
        "OUTPUT/README.md": "Project documentation"
    }
    
    IMPORTANT: ALL files and directories MUST be inside the 'OUTPUT' directory.
    Do not write any code. Just design the structure.
    """
    
    agent = Agent(
        model=model,
        instruction=instruction,
        name="architect_agent"
    )
    
    return agent
