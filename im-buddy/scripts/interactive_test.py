import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_connection(api_base_url, api_key):
    """Test if we can connect to the API with the given base URL and key"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # First try a simple GET to check if the API is reachable
    try:
        print(f"Testing connection to {api_base_url}...")
        # Some APIs have health check or version endpoints we can use
        response = requests.get(f"{api_base_url}/versions", headers=headers)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print("Connection successful!")
            return True
        else:
            print(f"Connection failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection failed: {e}")
        return False

def update_api_config(base_url, api_key):
    """Update the API configuration in the codebase"""
    # Update llama_common.py with the new base URL
    common_path = os.path.join(os.path.dirname(__file__), 'backend/services/llama_common.py')
    with open(common_path, 'r') as f:
        content = f.read()
    
    # Replace the BASE_URL line
    updated = content.replace(
        'BASE_URL = "https://api.meta.ai/llama"',
        f'BASE_URL = "{base_url}"'
    )
    
    with open(common_path, 'w') as f:
        f.write(updated)
    
    # Update the API key in the .env file if needed
    env_path = os.path.join(os.path.dirname(__file__), 'backend/.env')
    with open(env_path, 'r') as f:
        env_content = f.read()
        
    if 'LLAMA_API_KEY=' in env_content:
        updated_env = env_content.replace(
            f"LLAMA_API_KEY={os.getenv('LLAMA_API_KEY')}",
            f"LLAMA_API_KEY={api_key}"
        )
        with open(env_path, 'w') as f:
            f.write(updated_env)
    
    print(f"Updated configuration files with base URL: {base_url}")
    print(f"API key: {'*' * 5}{api_key[-4:] if api_key else 'None'}")

def main():
    print("=" * 50)
    print("LLaMa API Interactive Test")
    print("=" * 50)
    print("\nThis script will help you test and configure the LLaMa API connection.")
    
    # Get current API key from environment
    current_api_key = os.getenv("LLAMA_API_KEY", "")
    masked_key = f"{'*' * 5}{current_api_key[-4:] if current_api_key else 'None'}"
    
    print(f"\nCurrent API Key: {masked_key}")
    
    # Ask for API base URL
    print("\nWhat is the correct base URL for the LLaMa API?")
    print("Examples:")
    print("  - https://api.meta.ai/llama")
    print("  - https://api.llama.ai")
    print("  - https://api.openai.com")
    base_url = input("> ").strip()
    
    # Ask if they want to update the API key
    update_key = input("\nDo you want to update the API key? (y/n): ").strip().lower() == 'y'
    
    if update_key:
        api_key = input("Enter your new API key: ").strip()
    else:
        api_key = current_api_key
    
    # Test the connection
    if base_url:
        if test_api_connection(base_url, api_key):
            # If connection is successful, update the configuration
            update_api_config(base_url, api_key)
            
            # Ask to run the regular test
            run_tests = input("\nDo you want to run the standard API tests? (y/n): ").strip().lower() == 'y'
            
            if run_tests:
                # Run the main test script
                print("\nRunning standard API tests...")
                os.system(f"{sys.executable} {os.path.join(os.path.dirname(__file__), 'test_llama_api.py')}")
        else:
            print("\nConnection test failed. Please check the API base URL and your API key.")
            print("You may need to check the API documentation for the correct endpoints.")
    else:
        print("\nNo base URL provided. Exiting.")

if __name__ == "__main__":
    main() 