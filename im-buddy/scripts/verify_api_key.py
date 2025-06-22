import os
import sys
import json
from dotenv import load_dotenv

# Add the backend directory to the path so we can import the services
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Load environment variables
load_dotenv()

# Import from common module
try:
    from backend.services.llama_common import LLAMA_API_KEY, get_headers, BASE_URL
except ImportError:
    print("Error: Could not import LLaMa common services.")
    print("Make sure you're running this script from the project root directory.")
    sys.exit(1)

def verify_api_key():
    """Verify that the API key is correctly configured"""
    
    print("=" * 50)
    print("API Key Verification")
    print("=" * 50)
    
    # Check if API key is set
    if not LLAMA_API_KEY:
        print("ERROR: API key is not set in the environment!")
        print("Please check your .env file in the backend directory.")
        return
    
    # Check for expected format
    expected_key = "LLM|576663171867913|srTp5_yE10lm-iOY5O8sP7U8HWQ"
    if LLAMA_API_KEY != expected_key:
        print(f"WARNING: API key does not match expected value!")
        print(f"Expected: {expected_key[:10]}...{expected_key[-4:]}")
        print(f"Found:    {LLAMA_API_KEY[:10]}...{LLAMA_API_KEY[-4:] if len(LLAMA_API_KEY) > 14 else LLAMA_API_KEY}")
        
        confirm = input("\nWould you like to update the API key to the expected value? (y/n): ")
        if confirm.lower() == 'y':
            # Update the backend/.env file
            env_path = os.path.join(os.path.dirname(__file__), 'backend/.env')
            with open(env_path, 'r') as f:
                env_content = f.read()
                
            if 'LLAMA_API_KEY=' in env_content:
                updated = env_content.replace(
                    f"LLAMA_API_KEY={LLAMA_API_KEY}",
                    f"LLAMA_API_KEY={expected_key}"
                )
                with open(env_path, 'w') as f:
                    f.write(updated)
                print("API key has been updated in backend/.env file.")
                print("Please restart any running scripts to apply the changes.")
                return
    
    # Check if we're using the correct auth format
    print("\nAPI key is set correctly.")
    headers = get_headers()
    
    print("\nChecking authorization headers...")
    if headers.get("Authorization") == LLAMA_API_KEY:
        print("✅ Authorization header is using the LLM-format key directly (correct)")
    elif headers.get("Authorization", "").startswith("Bearer "):
        print("⚠️  Authorization header is using the Bearer prefix (wrong for LLM-format keys)")
    
    print(f"\nAPI Base URL: {BASE_URL}")
    
    print("\nConfiguration details:")
    print("-" * 50)
    print(f"API Key format: {'LLM-format' if LLAMA_API_KEY.startswith('LLM|') else 'Bearer-token format'}")
    print(f"Key starts with: {LLAMA_API_KEY.split('|')[0] if '|' in LLAMA_API_KEY else LLAMA_API_KEY[:10]+'...'}")
    print(f"Authorization header: {headers.get('Authorization', '').split('|')[0]}|{'*'*10}|{'*'*10}" if '|' in headers.get('Authorization', '') else headers.get('Authorization', '')[:10]+'...')
    
    print("\nReady to test API connectivity!")
    print("Next steps: Run 'python chat_test.py' to test the API connection")
    

if __name__ == "__main__":
    verify_api_key() 