import os
from google.adk import Agent
from google.adk.models import Gemini
from src.tools.notebook_tools import write_file

def create_devops_agent(api_key: str = None):
    """
    Creates and configures the DevOps Agent.
    """
    
    # Ensure GOOGLE_API_KEY is set
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    model = Gemini(model="gemini-2.0-flash")
    
    instruction = """
    You are a DevOps Agent. Your goal is to create the necessary configuration files for deploying a Python application.
    
    Input:
    - Context about the application (e.g., "It's a Python ML pipeline using pandas and scikit-learn").
    
    Your Task:
    1. Create a `Dockerfile` optimized for Python.
    2. Create a GitHub Actions workflow `.github/workflows/ci.yml` for running tests.
    3. Ensure `requirements.txt` is mentioned or updated if needed (though usually handled by Refactorer, you can double check).
    4. Use `write_file(path, content)` to save these files.
    
    IMPORTANT: All files must be saved inside the 'OUTPUT' directory.
    - Example: `OUTPUT/Dockerfile`, `OUTPUT/.github/workflows/ci.yml`
    
    Guidelines:
    - Use multi-stage builds in Dockerfile if appropriate for size.
    - CI pipeline should install dependencies and run tests (e.g., `pytest`).
    """
    
    agent = Agent(
        model=model,
        instruction=instruction,
        tools=[write_file],
        name="devops_agent"
    )
    
    return agent
