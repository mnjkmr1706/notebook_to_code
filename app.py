import streamlit as st
import os
import sys
import shutil
import time
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

from agents.parser_agent import create_parser_agent
from agents.architect_agent import create_architect_agent
from agents.refactorer_agent import create_refactorer_agent
from agents.devops_agent import create_devops_agent
from agents.reviewer_agent import create_reviewer_agent
from src.utils.security import check_pii

# Page config
st.set_page_config(
    page_title="Notebook to Code Agent",
    page_icon="🤖",
    layout="centered"
)

# Load environment
load_dotenv()

def get_response_text(response):
    """Extract text from ADK response generator"""
    if hasattr(response, 'text'):
        return response.text
    text = ""
    for event in response:
        if hasattr(event, 'content') and hasattr(event.content, 'parts'):
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    text += part.text
        elif hasattr(event, 'text') and event.text:
            text += event.text
        elif isinstance(event, str):
            text += event
    return text

def run_pipeline_generator(notebook_path, api_key):
    """Run the multi-agent pipeline and yield status updates"""
    
    yield "🚀 Initializing agents..."
    
    try:
        parser_agent = create_parser_agent(api_key=api_key)
        architect_agent = create_architect_agent(api_key=api_key)
        refactorer_agent = create_refactorer_agent(api_key=api_key)
        devops_agent = create_devops_agent(api_key=api_key)
        reviewer_agent = create_reviewer_agent(api_key=api_key)
    except Exception as e:
        yield f"❌ Error initializing agents: {str(e)}"
        return

    # Initialize session
    session_service = InMemorySessionService()
    APP_NAME = "notebook_to_code_pipeline"
    USER_ID = "web_user"
    SESSION_ID = "web_session"
    
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    # Parser Agent
    yield "🔍 Parser Agent: Reading and analyzing notebook..."
    parser_runner = Runner(agent=parser_agent, app_name=APP_NAME, session_service=session_service)
    parser_response = parser_runner.run(
        user_id=USER_ID, 
        session_id=SESSION_ID, 
        new_message=types.Content(role="user", parts=[types.Part(text=f"Parse the notebook at '{notebook_path}'")])
    )
    get_response_text(parser_response) # Consume
    yield "✅ Parser Agent: Notebook parsed successfully."
    
    # Architect Agent
    yield "🏗️ Architect Agent: Designing project structure..."
    architect_runner = Runner(agent=architect_agent, app_name=APP_NAME, session_service=session_service)
    architect_response = architect_runner.run(
        user_id=USER_ID, 
        session_id=SESSION_ID, 
        new_message=types.Content(role="user", parts=[types.Part(text="Based on the parsed code and documentation, design the project structure.")])
    )
    get_response_text(architect_response) # Consume
    yield "✅ Architect Agent: Project structure designed."
    
    # Feedback Loop
    max_rounds = 3
    for round_num in range(1, max_rounds + 1):
        yield f"🔄 Round {round_num}: Refactoring code..."
        
        # Refactorer Agent
        refactorer_runner = Runner(agent=refactorer_agent, app_name=APP_NAME, session_service=session_service)
        refactorer_response = refactorer_runner.run(
            user_id=USER_ID, 
            session_id=SESSION_ID, 
            new_message=types.Content(role="user", parts=[types.Part(text="Generate the production-ready code based on the plan.")])
        )
        get_response_text(refactorer_response) # Consume
        
        # DevOps Agent
        yield f"⚙️ Round {round_num}: Creating deployment files..."
        devops_runner = Runner(agent=devops_agent, app_name=APP_NAME, session_service=session_service)
        devops_response = devops_runner.run(
            user_id=USER_ID, 
            session_id=SESSION_ID, 
            new_message=types.Content(role="user", parts=[types.Part(text="Create the deployment configuration files.")])
        )
        get_response_text(devops_response) # Consume
        
        # Reviewer Agent
        yield f"👀 Round {round_num}: Reviewing code..."
        reviewer_runner = Runner(agent=reviewer_agent, app_name=APP_NAME, session_service=session_service)
        review_response = reviewer_runner.run(
            user_id=USER_ID, 
            session_id=SESSION_ID, 
            new_message=types.Content(role="user", parts=[types.Part(text="Review the generated code and configuration. If everything is production-ready with no issues, respond with ONLY 'APPROVED'. If there are any issues, provide ONLY specific feedback without saying APPROVED.")])
        )
        
        final_response = get_response_text(review_response)
        
        if "APPROVED" in final_response:
            yield "🎉 Pipeline completed! Code approved."
            return
        else:
            if round_num == max_rounds:
                yield f"⚠️ Max rounds reached. Last feedback: {final_response[:100]}..."
                return
            else:
                yield f"🔧 Reviewer Feedback: {final_response[:100]}... Retrying."

# --- Chat UI ---

st.title("🤖 Notebook to Code Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI coding assistant. Upload a Jupyter Notebook, and I'll convert it into a production-ready Python project for you."}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File Uploader (placed outside chat input for simplicity in Streamlit)
uploaded_file = st.sidebar.file_uploader("Upload .ipynb", type=['ipynb'])
api_key = st.sidebar.text_input("Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))

if uploaded_file and api_key:
    if "processed_file" not in st.session_state or st.session_state.processed_file != uploaded_file.name:
        
        # User message
        st.session_state.messages.append({"role": "user", "content": f"I've uploaded `{uploaded_file.name}`. Please convert it."})
        with st.chat_message("user"):
            st.markdown(f"I've uploaded `{uploaded_file.name}`. Please convert it.")
            
        # Save file
        notebook_path = f"uploaded_{uploaded_file.name}"
        with open(notebook_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # PII Check
        with st.chat_message("assistant"):
            st.markdown("🔒 Checking for PII...")
            with open(notebook_path, 'r') as f:
                warnings = check_pii(f.read())
                if warnings:
                    st.error("⚠️ PII Detected! Please sanitize your notebook.")
                    st.stop()
                else:
                    st.success("✅ No PII detected.")

            # Run Pipeline
            message_placeholder = st.empty()
            full_response = ""
            
            for status_update in run_pipeline_generator(notebook_path, api_key):
                full_response += status_update + "\n\n"
                message_placeholder.markdown(full_response)
                time.sleep(0.5) # UI smoothing
            
            # Finalize
            if os.path.exists("OUTPUT") and os.listdir("OUTPUT"):
                shutil.make_archive("generated_code", 'zip', "OUTPUT")
                with open("generated_code.zip", "rb") as f:
                    st.download_button(
                        label="⬇️ Download Generated Code",
                        data=f,
                        file_name="generated_code.zip",
                        mime="application/zip"
                    )
                st.session_state.messages.append({"role": "assistant", "content": full_response + "\n\n✅ **Done! Download your code above.**"})
                st.session_state.processed_file = uploaded_file.name
            else:
                st.session_state.messages.append({"role": "assistant", "content": full_response + "\n\n❌ **Failed to generate code.**"})

        # Cleanup
        if os.path.exists(notebook_path):
            os.remove(notebook_path)

elif not api_key:
    st.sidebar.warning("Please enter your Google API Key.")
