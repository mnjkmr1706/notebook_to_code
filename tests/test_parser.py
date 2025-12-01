import os
import sys
import asyncio
import warnings
from dotenv import load_dotenv
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.parser_agent import create_parser_agent

# Suppress Pydantic warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

async def test_parser():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: API Key not found")
        return

    print("Initializing Parser Agent...")
    agent = create_parser_agent(api_key=api_key)
    
    session_service = InMemorySessionService()
    APP_NAME = "test_parser_app"
    USER_ID = "test_user"
    SESSION_ID = "test_session"
    
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    notebook_path = "sample_notebook.ipynb"
    query = f"Parse the notebook at '{notebook_path}'."
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    print(f"Testing Parser Agent with {notebook_path}...")
    
    final_response = ""
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response = f"Escalated: {event.error_message}"
            break
            
    print("\nParser Output:")
    print(final_response)

if __name__ == "__main__":
    asyncio.run(test_parser())
