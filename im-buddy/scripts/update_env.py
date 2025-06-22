"""
Script to update the .env file with Supabase credentials
"""
import os
import re

def update_env_file():
    """Update the .env file with user-provided Supabase credentials"""
    print("=" * 60)
    print("Supabase .env Configuration Setup")
    print("=" * 60)
    
    # Get Supabase credentials from user
    supabase_url = input("Enter your Supabase URL (e.g. https://xxxxxxxxxxxx.supabase.co): ")
    supabase_key = input("Enter your Supabase Anon Key: ")
    bucket_name = input("Enter the storage bucket name [documents]: ") or "documents"
    
    # Path to .env file
    env_path = ".env"
    
    # Check if .env file exists
    env_exists = os.path.exists(env_path)
    
    if env_exists:
        # Read existing .env file
        with open(env_path, "r") as f:
            env_content = f.read()
            
        # Update or add Supabase credentials
        env_content = update_env_var(env_content, "SUPABASE_URL", supabase_url)
        env_content = update_env_var(env_content, "SUPABASE_ANON_KEY", supabase_key)
        env_content = update_env_var(env_content, "SUPABASE_STORAGE_BUCKET", bucket_name)
        
        # Write updated content back to .env file
        with open(env_path, "w") as f:
            f.write(env_content)
            
        print(f"\n✅ Updated .env file with Supabase credentials!")
    else:
        # Create new .env file
        env_content = f"""# Supabase Configuration
SUPABASE_URL={supabase_url}
SUPABASE_ANON_KEY={supabase_key}
SUPABASE_STORAGE_BUCKET={bucket_name}

# Django Configuration
DEBUG=True
SECRET_KEY=django-insecure-key-for-development
"""
        # Write to .env file
        with open(env_path, "w") as f:
            f.write(env_content)
            
        print(f"\n✅ Created new .env file with Supabase credentials!")
    
    print("\nYou can now run the test script to verify Supabase connectivity:")
    print("python test_supabase_upload.py")

def update_env_var(content, key, value):
    """Update an environment variable in the .env content"""
    # Check if the key already exists
    if re.search(rf"^{key}=", content, re.MULTILINE):
        # Update existing key
        return re.sub(rf"^{key}=.*$", f"{key}={value}", content, flags=re.MULTILINE)
    else:
        # Add new key
        return content + f"\n{key}={value}\n"

if __name__ == "__main__":
    update_env_file() 