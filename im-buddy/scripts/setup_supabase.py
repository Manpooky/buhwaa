"""
Interactive Supabase setup and testing script
"""
import os
import sys
import uuid
import json

try:
    from supabase import create_client
    import requests
except ImportError:
    print("Required packages not installed. Installing now...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "supabase", "requests"])
        from supabase import create_client
        import requests
    except Exception as e:
        print(f"Failed to install required packages: {e}")
        print("Please try to install them manually: pip install supabase requests")
        sys.exit(1)

def create_env_file(url, key, bucket):
    """Create or update .env file with Supabase credentials"""
    env_path = ".env"
    
    # Check if file exists and read current content
    existing_content = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    try:
                        k, v = line.strip().split("=", 1)
                        existing_content[k] = v
                    except ValueError:
                        # Skip lines that don't have a key=value format
                        pass
    
    # Update content with new values
    existing_content["SUPABASE_URL"] = url
    existing_content["SUPABASE_ANON_KEY"] = key
    existing_content["SUPABASE_STORAGE_BUCKET"] = bucket
    
    # Write back to file
    with open(env_path, "w") as f:
        for k, v in existing_content.items():
            f.write(f"{k}={v}\n")
    
    print(f"✓ Updated {env_path} with Supabase credentials")

def test_supabase_connection(url, key, bucket):
    """Test connection to Supabase and verify storage works"""
    print("\nTesting Supabase connection...")
    
    try:
        # Initialize client
        supabase = create_client(url, key)
        
        # Check if bucket exists
        print(f"Checking if bucket '{bucket}' exists...")
        buckets = supabase.storage.list_buckets()
        bucket_names = [b['name'] for b in buckets]
        
        if bucket not in bucket_names:
            print(f"Creating bucket '{bucket}'...")
            supabase.storage.create_bucket(bucket, {'public': False})
            print(f"✓ Created bucket '{bucket}'!")
        else:
            print(f"✓ Bucket '{bucket}' already exists!")
        
        # Create and upload test file
        test_id = uuid.uuid4().hex[:8]
        test_content = f"This is a test file for Supabase storage - {test_id}".encode()
        test_filename = f"test_{test_id}.txt"
        test_path = f"test/{test_filename}"
        
        print(f"\nUploading test file '{test_filename}'...")
        supabase.storage.from_(bucket).upload(
            test_path,
            test_content,
            {"content-type": "text/plain"}
        )
        print("✓ File uploaded successfully!")
        
        # Verify upload
        print("\nVerifying file exists...")
        try:
            files = supabase.storage.from_(bucket).list("test")
            file_exists = any(f['name'] == test_filename for f in files)
            if file_exists:
                print(f"✓ Test file '{test_filename}' found in storage!")
            else:
                print(f"✗ Test file '{test_filename}' not found in storage!")
        except Exception as e:
            print(f"Error listing files: {e}")
        
        # Clean up
        print("\nCleaning up test file...")
        try:
            supabase.storage.from_(bucket).remove([test_path])
            print("✓ Test file deleted!")
        except Exception as e:
            print(f"Error deleting file: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Supabase Setup and Test")
    print("=" * 60)
    
    # Check for existing values in .env
    env_path = ".env"
    supabase_url = None
    supabase_key = None
    supabase_bucket = "documents"
    
    if os.path.exists(env_path):
        print(f"Found existing .env file at {env_path}")
        try:
            with open(env_path, "r") as f:
                for line in f:
                    if line.strip().startswith("SUPABASE_URL="):
                        supabase_url = line.strip().split("=", 1)[1]
                    elif line.strip().startswith("SUPABASE_ANON_KEY="):
                        supabase_key = line.strip().split("=", 1)[1]
                    elif line.strip().startswith("SUPABASE_STORAGE_BUCKET="):
                        supabase_bucket = line.strip().split("=", 1)[1]
        except Exception as e:
            print(f"Error reading .env file: {e}")
    
    # Get Supabase URL
    if supabase_url and supabase_url != "your_supabase_url_here":
        print(f"Current Supabase URL: {supabase_url}")
        change = input("Do you want to change it? (y/n): ")
        if change.lower() == 'y':
            supabase_url = input("Enter your Supabase URL (e.g., https://xyz.supabase.co): ")
    else:
        supabase_url = input("Enter your Supabase URL (e.g., https://xyz.supabase.co): ")
    
    # Get Supabase key
    if supabase_key and supabase_key != "your_supabase_anon_key":
        print(f"Current Supabase anon key: {supabase_key[:5]}...{supabase_key[-4:] if len(supabase_key) > 8 else ''}")
        change = input("Do you want to change it? (y/n): ")
        if change.lower() == 'y':
            supabase_key = input("Enter your Supabase anon key: ")
    else:
        supabase_key = input("Enter your Supabase anon key: ")
    
    # Get bucket name
    print(f"Current storage bucket name: {supabase_bucket}")
    change = input("Do you want to change it? (y/n): ")
    if change.lower() == 'y':
        supabase_bucket = input("Enter bucket name (default is 'documents'): ") or "documents"
    
    # Save to .env file
    create_env_file(supabase_url, supabase_key, supabase_bucket)
    
    # Test connection
    success = test_supabase_connection(supabase_url, supabase_key, supabase_bucket)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Supabase is configured and working correctly!")
        print("Your PDF translation feature should work properly with Supabase storage.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Supabase configuration test failed.")
        print("Please check your credentials and try again.")
        print("=" * 60)
    
    return success

if __name__ == "__main__":
    main() 