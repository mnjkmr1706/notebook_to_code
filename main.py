import os
import sys
import argparse
import logging
import datetime
import json
import warnings
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

# Configure Logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f"exec_log_{timestamp}.log")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    filename=log_file,
    filemode='w'
)

print(f"Logging to: {log_file}")

# Suppress Pydantic serializer warnings arising from library interactions
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

def main():
    parser = argparse.ArgumentParser(description="Convert a Jupyter Notebook to a production-ready code pipeline.")
    parser.add_argument("--notebook", type=str, required=True, help="Path to the input Jupyter Notebook")
    args = parser.parse_args()
    notebook_path = args.notebook

    if not os.path.exists(notebook_path):
        print(f"Error: Notebook file not found at {notebook_path}")
        logging.error(f"Notebook not found: {notebook_path}")
        return

    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file")
        logging.error("GOOGLE_API_KEY not found")
        return

    # Check if OUTPUT folder exists and has files
    output_dir = "OUTPUT"
    if os.path.exists(output_dir) and os.listdir(output_dir):
        print(f"\nWarning: {output_dir}/ directory contains existing files.")
        user_response = input("Delete all files in OUTPUT/? (yes/no): ").strip().lower()
        if user_response == "yes":
            import shutil
            shutil.rmtree(output_dir)
            print(f"Deleted {output_dir}/ directory.")
            logging.info(f"User approved deletion of {output_dir}/")
        else:
            print("Workflow cancelled. Please backup or remove OUTPUT/ manually.")
            logging.info("User declined OUTPUT/ cleanup. Workflow cancelled.")
            return

    # PII Pre-check
    print("Running PII Pre-check...")
    try:
        with open(notebook_path, 'r') as f:
            notebook_content = f.read()
            warnings_list = check_pii(notebook_content)
            if warnings_list:
                print("\nSECURITY ALERT: PII Detected in notebook file!")
                for w in warnings_list:
                    print(f"- {w}")
                logging.critical(f"PII detected in notebook: {warnings_list}")
                return
    except Exception as e:
        print(f"Error reading notebook for PII check: {e}")
        logging.error(f"Error reading notebook: {e}")
        return

    print(f"Starting Multi-Agent Pipeline for: {notebook_path}")
    logging.info(f"Starting pipeline for {notebook_path}")

    # Initialize Agents
    try:
        parser_agent = create_parser_agent(api_key=api_key)
        architect_agent = create_architect_agent(api_key=api_key)
        refactorer_agent = create_refactorer_agent(api_key=api_key)
        devops_agent = create_devops_agent(api_key=api_key)
        reviewer_agent = create_reviewer_agent(api_key=api_key)
    except ValueError as e:
        print(f"Error initializing agents: {e}")
        logging.error(f"Agent initialization error: {e}")
        return

    # Initialize Session Service
    session_service = InMemorySessionService()
    APP_NAME = "notebook_to_code_pipeline"
    USER_ID = "user_1"
    SESSION_ID = "session_1"
    
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    def get_response_text(response):
        if hasattr(response, 'text'):
            return response.text
        # Assume it's a generator or iterable of event chunks
        text = ""
        for event in response:
            # ADK events have a 'content' attribute with the response
            if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        text += part.text
            elif hasattr(event, 'text') and event.text:
                text += event.text
            elif isinstance(event, str):
                text += event
        return text

    # --- Pipeline Orchestration ---
    
    # 1. Parser Agent
    print("\n--- Running parser_agent ---")
    logging.info("Running parser_agent")
    parser_runner = Runner(agent=parser_agent, app_name=APP_NAME, session_service=session_service)
    parser_response = parser_runner.run(
        user_id=USER_ID, 
        session_id=SESSION_ID, 
        new_message=types.Content(role="user", parts=[types.Part(text=f"Parse the notebook at '{notebook_path}'")])
    )
    parser_text = get_response_text(parser_response)
    print("Parser finished.")
    logging.info(f"Parser response: {parser_text[:100]}...")

    # 2. Architect Agent
    print("\n--- Running architect_agent ---")
    logging.info("Running architect_agent")
    architect_runner = Runner(agent=architect_agent, app_name=APP_NAME, session_service=session_service)
    architect_response = architect_runner.run(
        user_id=USER_ID, 
        session_id=SESSION_ID, 
        new_message=types.Content(role="user", parts=[types.Part(text="Based on the parsed code and documentation, design the project structure.")])
    )
    architect_text = get_response_text(architect_response)
    print("Architect finished.")
    logging.info(f"Architect response: {architect_text[:100]}...")

    # Feedback Loop
    max_rounds = 3
    for round_num in range(1, max_rounds + 1):
        print(f"\n=== Round {round_num} ===")
        logging.info(f"Starting Round {round_num}")
        
        # 3. Refactorer Agent
        print("\n--- Running refactorer_agent ---")
        logging.info("Running refactorer_agent")
        refactorer_runner = Runner(agent=refactorer_agent, app_name=APP_NAME, session_service=session_service)
        refactorer_response = refactorer_runner.run(
            user_id=USER_ID, 
            session_id=SESSION_ID, 
            new_message=types.Content(role="user", parts=[types.Part(text="Generate the production-ready code based on the plan.")])
        )
        refactorer_text = get_response_text(refactorer_response)
        print("Refactorer finished.")
        logging.info(f"Refactorer response: {refactorer_text[:100]}...")

        # 4. DevOps Agent
        print("\n--- Running devops_agent ---")
        logging.info("Running devops_agent")
        devops_runner = Runner(agent=devops_agent, app_name=APP_NAME, session_service=session_service)
        devops_response = devops_runner.run(
            user_id=USER_ID, 
            session_id=SESSION_ID, 
            new_message=types.Content(role="user", parts=[types.Part(text="Create the deployment configuration files.")])
        )
        devops_text = get_response_text(devops_response)
        print("DevOps finished.")
        logging.info(f"DevOps response: {devops_text[:100]}...")

        # 5. Reviewer Agent
        print("\n--- Running reviewer_agent ---")
        logging.info("Running reviewer_agent")
        reviewer_runner = Runner(agent=reviewer_agent, app_name=APP_NAME, session_service=session_service)
        review_response = reviewer_runner.run(
            user_id=USER_ID, 
            session_id=SESSION_ID, 
            new_message=types.Content(role="user", parts=[types.Part(text="Review the generated code and configuration. If everything is production-ready with no issues, respond with ONLY 'APPROVED'. If there are any issues, provide ONLY specific feedback without saying APPROVED.")])
        )
        # Consume generator immediately to avoid it being exhausted
        final_response = ""
        for event in review_response:
            if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_response += part.text
        
        print(f"Reviewer finished. Verdict: {final_response[:50]}...")
        logging.info(f"Reviewer verdict: {final_response}")
        
        if "APPROVED" in final_response:
            print("\nPipeline successfully completed! Code is approved.")
            break
        else:
            print("\nCode review feedback received.")
            feedback = final_response
            if round_num == max_rounds:
                print("\nMax rounds reached. Requesting human review.")
                logging.warning("Max rounds reached without approval.")
            else:
                print("\nSending feedback to Refactorer for next round...")
                # Pass feedback to next round (implicitly via session history)

if __name__ == "__main__":
    main()