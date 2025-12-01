from typing import Optional
from google.genai import types
from src.utils.security import check_pii

def pii_guardrail(callback_context, **kwargs) -> Optional[types.Content]:
    """
    ADK Callback: Checks user input for PII before agent execution.
    """
    context = callback_context
    # Extract the last user message from the context
    # Context structure depends on ADK version, but typically has 'new_message' or similar
    # For 'before_agent', context usually has the input message.
    
    # Inspecting context to find the message text
    # Assuming context.new_message is available and is of type types.Content
    
    try:
        # Check for user_content (ADK specific)
        content_obj = getattr(context, 'user_content', None) or getattr(context, 'new_message', None)
        
        if content_obj:
            message_text = ""
            if hasattr(content_obj, 'parts'):
                for part in content_obj.parts:
                    if hasattr(part, 'text'):
                        message_text += part.text + "\n"
            
            if message_text:
                warnings = check_pii(message_text)
                if warnings:
                    warning_msg = "SECURITY ALERT: PII Detected in input. Execution blocked.\n"
                    warning_msg += "Found: " + ", ".join(warnings)
                    
                    # Return a Content object to short-circuit the agent
                    return types.Content(
                        role="model",
                        parts=[types.Part(text=warning_msg)]
                    )
    except Exception as e:
        # Fallback logging or error handling
        print(f"Error in PII guardrail: {e}")
        
    return None # Allow execution to proceed
