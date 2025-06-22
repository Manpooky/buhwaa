"""
Test Supabase storage by uploading a file, verifying it exists, and then deleting it
"""
import os
import io
import sys
import uuid
import time
import json

# Add the project directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

# First try to load using django's settings
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.im_buddy.settings')
    import django
    django.setup()
    from backend.services.supabase_client import get_client
    from backend.services.supabase_storage import SupabaseStorage
    print("✓ Using Django configuration")
    USING_DJANGO = True
except Exception as e:
    print(f"Could not load Django settings: {e}")
    print("✓ Falling back to direct .env loading")
    USING_DJANGO = False
    
    # Try to load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("python-dotenv not found, trying to load directly from .env file")
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.strip() and not line.strip().startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value
        except Exception as e:
            print(f"Error loading .env file: {e}")
    
    # Import required libraries for direct Supabase access
    try:
        from supabase import create_client
        import requests
    except ImportError as e:
        print(f"Error: Required libraries not found: {e}")
        print("Please install with: pip install supabase requests")
        sys.exit(1)

def get_supabase_client():
    """Get Supabase client either from Django or direct config"""
    if USING_DJANGO:
        return get_client()
    else:
        # Get credentials from environment
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_key:
            print("Error: Supabase credentials not found in environment")
            print("Make sure SUPABASE_URL and SUPABASE_ANON_KEY are set in .env file")
            sys.exit(1)
            
        return create_client(supabase_url, supabase_key)

def main():
    """Test Supabase storage connection by uploading and verifying a file"""
    print("=" * 60)
    print("Supabase Storage Test")
    print("=" * 60)
    
    # Get credentials
    supabase_url = os.environ.get("SUPABASE_URL")
    bucket_name = os.environ.get("SUPABASE_STORAGE_BUCKET", "documents")
    
    print(f"Supabase URL: {supabase_url}")
    print(f"Bucket name: {bucket_name}")
    
    try:
        # Get client
        supabase = get_supabase_client()
        print("✓ Successfully connected to Supabase!")
        
        # List available buckets
        print("\nListing available storage buckets...")
        try:
            buckets = supabase.storage.list_buckets()
            bucket_names = [b['name'] for b in buckets]
            print(f"Available buckets: {bucket_names}")
            
            # Check if our target bucket exists
            if bucket_name in bucket_names:
                print(f"✓ Bucket '{bucket_name}' exists and is accessible!")
            else:
                # Prompt for alternative bucket
                print(f"✗ Bucket '{bucket_name}' doesn't exist or isn't accessible.")
                
                if bucket_names:
                    print(f"Please select from available buckets: {bucket_names}")
                    bucket_index = input(f"Enter bucket number (0-{len(bucket_names)-1}) or press Enter to try '{bucket_name}' anyway: ")
                    
                    if bucket_index.strip() and bucket_index.isdigit() and 0 <= int(bucket_index) < len(bucket_names):
                        bucket_name = bucket_names[int(bucket_index)]
                        print(f"Using bucket '{bucket_name}'")
                    else:
                        print(f"Continuing with '{bucket_name}' (may fail if bucket doesn't exist)")
                else:
                    print("No buckets available with your current permissions.")
                    print("You might need admin access to create buckets or contact your Supabase admin.")
                    return False
                    
        except Exception as bucket_error:
            print(f"✗ Error listing buckets: {bucket_error}")
            print("Continuing with default bucket configuration...")
        
        # Create test file
        test_id = uuid.uuid4().hex[:8]
        test_content = f"This is a test file for Supabase storage - {test_id}".encode()
        test_filename = f"test_{test_id}.txt"
        test_path = test_filename  # Start with just the filename
        
        print(f"\nUploading test file '{test_filename}'...")
        
        # Upload test file
        try:
            supabase.storage.from_(bucket_name).upload(
                test_path,
                test_content,
                {"content-type": "text/plain"}
            )
            print("✓ File uploaded successfully!")
        except Exception as upload_error:
            print(f"✗ Upload failed: {upload_error}")
            print("\nThis may be due to:")
            print("1. The bucket doesn't exist")
            print("2. You don't have permission to upload to this bucket")
            print("3. The RLS policies are restricting uploads")
            return False
        
        # List files to verify upload
        print("\nListing files to verify upload...")
        try:
            files = supabase.storage.from_(bucket_name).list()
            print(f"Files in bucket: {json.dumps(files[:5], indent=2)}")  # Limiting to 5 files to avoid large outputs
            
            # Check if our file exists
            file_exists = any(f['name'] == test_path for f in files)
            if file_exists:
                print(f"✓ Test file '{test_filename}' found in storage!")
            else:
                print(f"✗ Test file '{test_filename}' not found in storage!")
                print("Files might take a moment to appear or file might have been stored in a subfolder.")
        except Exception as list_error:
            print(f"✗ Error listing files: {list_error}")
            
        # Get public URL
        try:
            file_url = supabase.storage.from_(bucket_name).get_public_url(test_path)
            print(f"\nPublic URL (may not be accessible if bucket is private): {file_url}")
        except Exception as url_error:
            print(f"✗ Error getting public URL: {url_error}")
        
        # Clean up
        print("\nCleaning up test file...")
        try:
            supabase.storage.from_(bucket_name).remove([test_path])
            print("✓ Test file deleted!")
        except Exception as delete_error:
            print(f"✗ Error deleting file: {delete_error}")
            print("You might not have permission to delete files or the file was already removed.")
        
        print("\n" + "=" * 60)
        print("✅ Supabase storage connection test completed!")
        print("Your PDF translation feature should work properly with Supabase storage if you saw")
        print("successful file upload and listing operations above.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\n" + "=" * 60)
        print("❌ Supabase storage test failed.")
        print("Please check your credentials and Supabase configuration.")
        print("=" * 60)
        return False

if __name__ == "__main__":
    main() 