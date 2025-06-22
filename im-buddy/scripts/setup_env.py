import os
import sys

def setup_env():
    """
    Set up the .env file with the Llama API key
    """
    # Check if .env file exists
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    # Read existing content if file exists
    env_content = {}
    if os.path.exists(env_path):
        print(f"Found existing .env file at {env_path}")
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_content[key] = value
    
    # Check if any of the Llama API key variables already exist
    key_names = ["LLAMA_API_KEY", "META_API_KEY", "LLAMA_KEY", "META_LLAMA_API_KEY", "LLAMA_TOKEN"]
    existing_key = None
    
    for key in key_names:
        if key in env_content:
            existing_key = key
            print(f"Found existing API key variable: {key}")
            break
    
    if existing_key:
        update = input(f"Do you want to update the existing {existing_key}? (y/n): ").lower() == 'y'
        if not update:
            print("Keeping existing API key.")
            return
    
    # Prompt for API key
    api_key = input("Enter your Meta Llama API key: ").strip()
    if not api_key:
        print("Error: API key cannot be empty.")
        sys.exit(1)
    
    # Use LLAMA_API_KEY as the default variable name
    key_name = existing_key or "LLAMA_API_KEY"
    env_content[key_name] = api_key
    
    # Write back to .env file
    with open(env_path, 'w') as f:
        for key, value in env_content.items():
            f.write(f"{key}={value}\n")
    
    print(f"API key saved to .env file as {key_name}")

if __name__ == "__main__":
    setup_env() 