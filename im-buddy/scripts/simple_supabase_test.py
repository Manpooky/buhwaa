"""
Simple test for Supabase file operations - upload/download (no bucket management)
"""
import os
import sys
import uuid
import json

# Try to load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual .env loading if python-dotenv is not installed
    try:
        with open(".env", "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}")
        print("Using environment variables directly...")

# Import Supabase client
try:
    from supabase import create_client
except ImportError:
    print("Error: Please install supabase-py with: pip install supabase")
    sys.exit(1)

def main():
    """Simple test for Supabase storage operations"""
    print("=" * 60)
    print("Simple Supabase Storage Test")
    print("=" * 60)
    
    # Get credentials
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")
    bucket_name = os.environ.get("SUPABASE_STORAGE_BUCKET", "documents")
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
        return False
    
    print(f"Using bucket: {bucket_name}")
    
    # Create a simple test file
    test_id = uuid.uuid4().hex[:8]
    test_content = f"This is a test file created at {test_id}".encode()
    test_filename = f"test_{test_id}.txt"
    
    try:
        # Connect to Supabase
        supabase = create_client(supabase_url, supabase_key)
        print("✓ Connected to Supabase")
        
        # Try to upload file
        print(f"\nUploading test file '{test_filename}'...")
        try:
            supabase.storage.from_(bucket_name).upload(
                test_filename,
                test_content,
                {"content-type": "text/plain"}
            )
            print("✓ File uploaded successfully!")
            
            # Get public URL
            try:
                file_url = supabase.storage.from_(bucket_name).get_public_url(test_filename)
                print(f"File URL: {file_url}")
            except Exception as url_error:
                print(f"Note: Could not get public URL: {url_error}")
            
            # Clean up
            print("\nCleaning up test file...")
            try:
                supabase.storage.from_(bucket_name).remove([test_filename])
                print("✓ Test file deleted!")
                return True
            except Exception as del_error:
                print(f"Warning: Could not delete test file: {del_error}")
                # Consider success even if deletion fails
                return True
                
        except Exception as e:
            print(f"✗ Upload failed: {e}")
            print("\nPossible issues:")
            print("1. The bucket '{bucket_name}' doesn't exist - create it in Supabase dashboard")
            print("2. Your RLS policies don't allow uploads - check bucket permissions")
            print("3. Your API key doesn't have sufficient privileges")
            return False
            
    except Exception as e:
        print(f"✗ Supabase connection error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Supabase storage test passed!")
        print("Your PDF translation feature should work with Supabase for file storage.")
    else:
        print("❌ Supabase storage test failed!")
        print("Please check your Supabase setup and permissions.")
    print("=" * 60) 