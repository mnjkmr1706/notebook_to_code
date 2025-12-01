import os
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from src.tools.notebook_tools import read_notebook, write_file

def create_pipeline_agent(api_key: str = None):
    """
    Creates and configures the Pipeline Agent.
    """
    
    # Ensure OPENROUTER_API_KEY is set
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY")
        
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")

    # Initialize LiteLlm with OpenRouter model
    # Using x-ai/grok-code-fast-1 via OpenRouter
    model = LiteLlm(model="openrouter/x-ai/grok-code-fast-1", max_tokens=10000, api_key=api_key)
    
    system_prompt = """
    You are an expert Machine Learning Engineer specializing in refactoring Jupyter Notebooks into production-ready code pipelines.
    
    Your goal is to take a raw notebook containing ML code (data loading, preprocessing, model definition, training, evaluation) and convert it into a structured Python project.
    
    You have access to the following tools:
    - `read_notebook(path)`: Read the content of the notebook.
    - `write_file(path, content)`: Write code to files.
    
    Process:
    1.  Read the notebook using `read_notebook`.
    2.  Analyze the code to understand the data flow, model architecture, and training loop.
    3.  Refactor the code into modular files. Suggested structure:
        - `data_loader.py`: Data loading and preprocessing.
        - `model.py`: Model definition.
        - `train.py`: Training loop and evaluation.
        - `utils.py`: Helper functions.
        - `requirements.txt`: Dependencies.
    4.  Write these files using `write_file`.
    5.  Ensure the code is clean, documented, and follows best practices.
    
    When writing files, provide the full content.
    """
    
    agent = Agent(
        model=model,
        instruction=system_prompt,
        tools=[read_notebook, write_file],
        name="pipeline_agent"
    )
    
    return agent
