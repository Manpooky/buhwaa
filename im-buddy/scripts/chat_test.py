import os
import sys
from dotenv import load_dotenv
from llama_api_client import LlamaAPIClient

# Load environment variables from .env file
load_dotenv()

# Check for API key under different possible environment variable names
possible_key_names = ["LLAMA_API_KEY", "META_API_KEY", "LLAMA_KEY", "META_LLAMA_API_KEY", "LLAMA_TOKEN"]
api_key = None

for key_name in possible_key_names:
    api_key = os.getenv(key_name)
    if api_key:
        print(f"Found API key using environment variable: {key_name}")
        break

if not api_key:
    print("Error: API key not found in environment variables.")
    print(f"Please set one of these in your .env file: {', '.join(possible_key_names)}")
    sys.exit(1)

# Define the model to use
MODEL = "Llama-4-Maverick-17B-128E-Instruct-FP8"

def chat_with_llama(prompt):
    """
    Simple function to chat with Meta's Llama API using the official client
    
    Args:
        prompt (str): User prompt
        
    Returns:
        str: Model response
    """
    try:
        print("\nSending request to Meta's Llama API...")
        print(f"Model: {MODEL}")
        
        # Initialize the Llama API client with explicit API key
        client = LlamaAPIClient(api_key=api_key)
        
        # Create a chat completion following the example
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        
        # Extract the content from the response based on the example
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

def main():
    print("=" * 50)
    print("Meta Llama API Chat Test")
    print("=" * 50)
    print("\nThis script allows you to chat with Meta's Llama model.")
    print(f"Using model: {MODEL}")
    
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

if __name__ == "__main__":
    main() 