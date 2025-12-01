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

from agents.architect_agent import create_architect_agent

# Suppress Pydantic warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

async def test_architect():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: API Key not found")
        return

    print("Initializing Architect Agent...")
    agent = create_architect_agent(api_key=api_key)
    
    session_service = InMemorySessionService()
    APP_NAME = "test_architect_app"
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
    
    # Mock output from Parser Agent
    parser_output = """
    {"code": "# Cell 1\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import accuracy_score\n\n# Cell 2\n# Load data\ndata = pd.DataFrame({\n    'feature1': [1, 2, 3, 4, 5],\n    'feature2': [5, 4, 3, 2, 1],\n    'target': [0, 0, 1, 1, 0]\n})\n\n\n# Cell 3\n# Preprocess\nX = data[['feature1', 'feature2']]\ny = data['target']\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\n\n# Cell 4\n# Train model\nmodel = LogisticRegression()\nmodel.fit(X_train, y_train)\n\n# Cell 5\n# Evaluate\npreds = model.predict(X_test)\nprint(f'Accuracy: {accuracy_score(y_test, preds)}')\n", "documentation": "# Load data\n\n# Preprocess\n\n# Train model\n\n# Evaluate\n"}
    """
    
    query = f"Design a folder structure for the following parsed notebook content:\n{parser_output}"
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    print("Testing Architect Agent...")
    
    final_response = ""
    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response = f"Escalated: {event.error_message}"
            break
            
    print("\nArchitect Output:")
    print(final_response)

if __name__ == "__main__":
    asyncio.run(test_architect())
