"""
LLM utility functions for initializing Google Generative AI models with customized prompts.
"""

from typing import Optional
import os

try:
    import google.generativeai as genai
    GOOGLE_SDK_AVAILABLE = True
except ImportError:
    GOOGLE_SDK_AVAILABLE = False


def get_llm(model_name: str, prompt: Optional[str] = None):
    """
    Initialize and return a Google Generative AI model instance with optional customized prompt.
    
    This utility function creates LLM instances that can be used across different agents
    with consistent configuration and optional prompt customization.
    
    Args:
        model_name (str): The name of the model to use. Supported models:
            - "gemini-2.0-flash": Google's Gemini 2.0 Flash (fastest)
            - "gemini-1.5-pro": Google's Gemini 1.5 Pro (most capable)
            - "gemini-1.5-flash": Google's Gemini 1.5 Flash
        
        prompt (str, optional): Customized system prompt to configure the model's behavior.
            This will be used as the system instruction for the model.
            Defaults to None (use model's default behavior).
    
    Returns:
        genai.GenerativeModel: Configured Google Generative AI model instance ready for use.
    
    Raises:
        ValueError: If the model_name is not supported or if Google SDK is not installed.
        
    Example:
        # Using with default prompt
        llm = get_llm("gemini-2.0-flash")
        
        # Using with custom prompt
        llm = get_llm(
            "gemini-1.5-pro",
            prompt="You are a helpful code assistant specialized in Python development."
        )
        
        # Generate content
        response = llm.generate_content("Write a function to calculate factorial")
    """
    
    if not GOOGLE_SDK_AVAILABLE:
        raise ImportError(
            "Google Generative AI SDK not installed. "
            "Install it with: pip install google-generativeai"
        )
    
    # Configure API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    
    model_name = model_name.lower().strip()
    
    # Validate model name
    supported_models = {
        "gemini-2.0-flash": "gemini-2.0-flash",
        "gemini-1.5-pro": "gemini-1.5-pro",
        "gemini-1.5-flash": "gemini-1.5-flash",
    }
    
    if model_name not in supported_models:
        raise ValueError(
            f"Unsupported model: {model_name}. "
            f"Supported models: {', '.join(supported_models.keys())}"
        )
    
    # Get the full model identifier
    full_model_name = supported_models[model_name]
    
    # Create the model instance with optional system prompt
    if prompt:
        llm = genai.GenerativeModel(
            model_name=full_model_name,
            system_instruction=prompt,
        )
    else:
        llm = genai.GenerativeModel(model_name=full_model_name)
    
    return llm
