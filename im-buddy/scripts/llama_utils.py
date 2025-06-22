"""
Utility functions for testing and interacting with the Meta Llama API
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the path so we can import the services
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.append(backend_path)

# Check for API key under different possible environment variable names
def get_llama_api_key():
    """
    Get the Llama API key from environment variables
    
    Returns:
        str: API key or None if not found
    """
    possible_key_names = ["LLAMA_API_KEY", "META_API_KEY", "LLAMA_KEY", "META_LLAMA_API_KEY", "LLAMA_TOKEN"]
    api_key = None
    
    for key_name in possible_key_names:
        api_key = os.getenv(key_name)
        if api_key:
            print(f"Found API key using environment variable: {key_name}")
            break
    
    return api_key

# Default model to use
DEFAULT_MODEL = "Llama-4-Maverick-17B-128E-Instruct-FP8"

def chat_with_llama(prompt, model=DEFAULT_MODEL):
    """
    Simple function to chat with Meta's Llama API using the official client
    
    Args:
        prompt (str): User prompt
        model (str): Model name to use
        
    Returns:
        str: Model response
    """
    try:
        # Import here to avoid errors if the package is not installed
        from llama_api_client import LlamaAPIClient
        
        api_key = get_llama_api_key()
        if not api_key:
            return "Error: API key not found in environment variables."
        
        print("\nSending request to Meta's Llama API...")
        print(f"Model: {model}")
        
        # Initialize the Llama API client with explicit API key
        client = LlamaAPIClient(api_key=api_key)
        
        # Create a chat completion
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        
        # Extract the content from the response
        return completion.completion_message.content.text
            
    except Exception as e:
        error_msg = str(e)
        print(f"Error calling Llama API: {error_msg}")
        
        # Try to extract any useful information from the error
        if "400 Bad Request" in error_msg:
            print("\nAPI reported Bad Request. This could be due to:")
            print("- Incorrect model name")
            print("- Malformed request format")
            print("- Invalid parameters")
        elif "401 Unauthorized" in error_msg:
            print("\nAPI reported Unauthorized. This could be due to:")
            print("- Invalid API key")
            print("- Expired API key")
            print("- Insufficient permissions")
        elif "404 Not Found" in error_msg:
            print("\nAPI endpoint not found. This could be due to:")
            print("- Incorrect API endpoint URL")
            print("- Endpoint not available for your account")
        
        return f"Error: {error_msg}"

def test_translation():
    """
    Test the translation service
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from services.llama_service import translate_text
        
        print("-" * 50)
        print("Testing LLaMa Translation API")
        print("-" * 50)
        
        translation_result = translate_text(
            text="Hello, how are you? I need help with my visa application.",
            source_language="en",
            target_language="es"
        )
        
        print(f"Original: Hello, how are you? I need help with my visa application.")
        print(f"Translated to Spanish: {translation_result}")
        
        return True
    except Exception as e:
        print(f"Error testing translation service: {e}")
        return False

def test_tips_generation():
    """
    Test the tips generation service
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from services.llama_service import generate_tips
        
        print("-" * 50)
        print("Testing LLaMa Tips Generation API")
        print("-" * 50)
        
        tips_result = generate_tips(
            visa_type="B2",
            language="en"
        )
        
        print("Generated Tips for B2 visa:")
        print(tips_result)
        
        return True
    except Exception as e:
        print(f"Error testing tips generation service: {e}")
        return False

def interactive_chat():
    """
    Run an interactive chat session with the Llama API
    """
    print("=" * 50)
    print("Meta Llama API Chat Test")
    print("=" * 50)
    print("\nThis script allows you to chat with Meta's Llama model.")
    print(f"Using model: {DEFAULT_MODEL}")
    
    while True:
        # Get user prompt
        print("\nEnter your prompt (or 'exit' to quit):")
        prompt = input("> ").strip()
        
        if not prompt or prompt.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        # Get response from API
        response = chat_with_llama(prompt)
        
        print("\nResponse:")
        print("-" * 50)
        print(response)
        print("-" * 50)

def test_all_services():
    """
    Test all Llama API services
    
    Returns:
        bool: True if all tests pass, False otherwise
    """
    api_key = get_llama_api_key()
    if not api_key:
        print("Error: API key not found in environment variables.")
        print("Please set one of these in your .env file: LLAMA_API_KEY, META_API_KEY, LLAMA_KEY, META_LLAMA_API_KEY, LLAMA_TOKEN")
        return False
    
    # Test translation service
    translation_success = test_translation()
    
    # Test tips generation service
    tips_success = test_tips_generation()
    
    # Report results
    print("\n" + "=" * 50)
    print("Llama API Test Results")
    print("=" * 50)
    print(f"Translation Service: {'✓ Passed' if translation_success else '✗ Failed'}")
    print(f"Tips Generation Service: {'✓ Passed' if tips_success else '✗ Failed'}")
    
    return translation_success and tips_success

if __name__ == "__main__":
    # If run directly, test all services
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_chat()
    else:
        test_all_services() 