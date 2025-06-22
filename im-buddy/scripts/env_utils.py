"""
Utilities for managing environment variables and .env files
"""
import os
import re
import sys

def load_env_file(env_path=".env"):
    """
    Load environment variables from .env file
    
    Args:
        env_path (str): Path to .env file
        
    Returns:
        dict: Dictionary of environment variables
    """
    env_vars = {}
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
                    # Also set in environment
                    os.environ[key] = value
    
    return env_vars

def save_env_file(env_vars, env_path=".env"):
    """
    Save environment variables to .env file
    
    Args:
        env_vars (dict): Dictionary of environment variables
        env_path (str): Path to .env file
    """
    with open(env_path, 'w') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

def update_env_var(env_vars, key, value):
    """
    Update an environment variable in the env_vars dictionary
    
    Args:
        env_vars (dict): Dictionary of environment variables
        key (str): Environment variable name
        value (str): Environment variable value
        
    Returns:
        dict: Updated dictionary of environment variables
    """
    env_vars[key] = value
    return env_vars

def setup_llama_api_key(env_path=".env"):
    """
    Set up the Llama API key in the .env file
    
    Args:
        env_path (str): Path to .env file
        
    Returns:
        bool: True if successful, False otherwise
    """
    print("=" * 60)
    print("Meta Llama API Key Setup")
    print("=" * 60)
    
    # Load existing environment variables
    env_vars = load_env_file(env_path)
    
    # Check if any of the Llama API key variables already exist
    key_names = ["LLAMA_API_KEY", "META_API_KEY", "LLAMA_KEY", "META_LLAMA_API_KEY", "LLAMA_TOKEN"]
    existing_key = None
    
    for key in key_names:
        if key in env_vars:
            existing_key = key
            print(f"Found existing API key variable: {key}")
            break
    
    if existing_key:
        update = input(f"Do you want to update the existing {existing_key}? (y/n): ").lower() == 'y'
        if not update:
            print("Keeping existing API key.")
            return True
    
    # Prompt for API key
    api_key = input("Enter your Meta Llama API key: ").strip()
    if not api_key:
        print("Error: API key cannot be empty.")
        return False
    
    # Use LLAMA_API_KEY as the default variable name
    key_name = existing_key or "LLAMA_API_KEY"
    env_vars = update_env_var(env_vars, key_name, api_key)
    
    # Save to .env file
    save_env_file(env_vars, env_path)
    print(f"API key saved to {env_path} file as {key_name}")
    return True

def setup_supabase_credentials(env_path=".env"):
    """
    Set up Supabase credentials in the .env file
    
    Args:
        env_path (str): Path to .env file
        
    Returns:
        bool: True if successful, False otherwise
    """
    print("=" * 60)
    print("Supabase Credentials Setup")
    print("=" * 60)
    
    # Get Supabase credentials from user
    supabase_url = input("Enter your Supabase URL (e.g. https://xxxxxxxxxxxx.supabase.co): ")
    supabase_key = input("Enter your Supabase Anon Key: ")
    bucket_name = input("Enter the storage bucket name [documents]: ") or "documents"
    
    if not supabase_url or not supabase_key:
        print("Error: Supabase URL and Anon Key are required.")
        return False
    
    # Load existing environment variables
    env_vars = load_env_file(env_path)
    
    # Update or add Supabase credentials
    env_vars = update_env_var(env_vars, "SUPABASE_URL", supabase_url)
    env_vars = update_env_var(env_vars, "SUPABASE_ANON_KEY", supabase_key)
    env_vars = update_env_var(env_vars, "SUPABASE_STORAGE_BUCKET", bucket_name)
    
    # Add Django configuration if not present
    if "DEBUG" not in env_vars:
        env_vars = update_env_var(env_vars, "DEBUG", "True")
    
    if "SECRET_KEY" not in env_vars:
        env_vars = update_env_var(env_vars, "SECRET_KEY", "django-insecure-key-for-development")
    
    # Save to .env file
    save_env_file(env_vars, env_path)
    print(f"Supabase credentials saved to {env_path}")
    return True

def setup_all_credentials(env_path=".env"):
    """
    Set up all required credentials in the .env file
    
    Args:
        env_path (str): Path to .env file
        
    Returns:
        bool: True if successful, False otherwise
    """
    print("=" * 60)
    print("Environment Setup")
    print("=" * 60)
    
    # Set up Supabase credentials
    if not setup_supabase_credentials(env_path):
        return False
    
    # Set up Llama API key
    if not setup_llama_api_key(env_path):
        return False
    
    print("\n" + "=" * 60)
    print("✅ Environment setup completed successfully!")
    print("=" * 60)
    return True

def check_environment():
    """
    Check if all required environment variables are set
    
    Returns:
        bool: True if all required variables are set, False otherwise
    """
    print("=" * 60)
    print("Environment Check")
    print("=" * 60)
    
    # Required environment variables
    required_vars = {
        "SUPABASE_URL": "Supabase URL",
        "SUPABASE_ANON_KEY": "Supabase Anon Key",
        "LLAMA_API_KEY": "Meta Llama API Key (or equivalent)",
    }
    
    # Check for Llama API key variants
    llama_key_vars = ["LLAMA_API_KEY", "META_API_KEY", "LLAMA_KEY", "META_LLAMA_API_KEY", "LLAMA_TOKEN"]
    has_llama_key = any(os.environ.get(key) for key in llama_key_vars)
    
    all_set = True
    
    for var, description in required_vars.items():
        # Special handling for Llama API key
        if var == "LLAMA_API_KEY":
            if has_llama_key:
                print(f"✓ {description}: Set")
            else:
                print(f"✗ {description}: Not Set")
                all_set = False
        else:
            if os.environ.get(var):
                print(f"✓ {description}: Set")
            else:
                print(f"✗ {description}: Not Set")
                all_set = False
    
    # Optional variables
    optional_vars = {
        "SUPABASE_STORAGE_BUCKET": "Supabase Storage Bucket (default: documents)",
        "DEBUG": "Django Debug Mode (default: True)",
        "SECRET_KEY": "Django Secret Key",
    }
    
    print("\nOptional Variables:")
    for var, description in optional_vars.items():
        if os.environ.get(var):
            print(f"✓ {description}: Set")
        else:
            print(f"- {description}: Not Set")
    
    if all_set:
        print("\n✅ All required environment variables are set!")
    else:
        print("\n❌ Some required environment variables are missing.")
        print("Run 'python scripts/env_utils.py' to set up your environment.")
    
    return all_set

if __name__ == "__main__":
    # If run directly, set up all credentials
    setup_all_credentials() 