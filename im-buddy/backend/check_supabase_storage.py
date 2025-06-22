"""
Script to check if Supabase storage is properly configured
"""

import os
import io
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'im_buddy.settings')
django.setup()

from services.supabase_client import get_client
from services.supabase_storage import SupabaseStorage
from django.conf import settings

def main():
    """
    Check Supabase storage configuration
    """
    print("=" * 60)
    print("Supabase Storage Configuration Check")
    print("=" * 60)
    
    # Check Supabase URL and key
    supabase_url = getattr(settings, 'SUPABASE_URL', None)
    supabase_key = getattr(settings, 'SUPABASE_ANON_KEY', None)
    bucket_name = getattr(settings, 'SUPABASE_STORAGE_BUCKET', 'documents')
    
    print(f"Supabase URL: {'Set' if supabase_url else 'Not Set'}")
    print(f"Supabase Key: {'Set' if supabase_key else 'Not Set'}")
    print(f"Storage Bucket: {bucket_name}")
    
    if not supabase_url or not supabase_key:
        print("\nError: Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file")
        return
    
    # Test Supabase client
    print("\nTesting Supabase client connection...")
    try:
        supabase = get_client()
        print("✓ Supabase client initialized successfully!")
    except Exception as e:
        print(f"✗ Error initializing Supabase client: {e}")
        return
    
    # Check if bucket exists, create if not
    print(f"\nChecking if bucket '{bucket_name}' exists...")
    try:
        buckets = supabase.storage.list_buckets()
        bucket_names = [b['name'] for b in buckets]
        
        if bucket_name not in bucket_names:
            print(f"Bucket '{bucket_name}' not found. Creating...")
            supabase.storage.create_bucket(bucket_name)
            print(f"✓ Created bucket '{bucket_name}'!")
        else:
            print(f"✓ Bucket '{bucket_name}' already exists!")
    except Exception as e:
        print(f"✗ Error checking/creating bucket: {e}")
        return
    
    # Test storing a file
    print("\nTesting file upload...")
    try:
        storage = SupabaseStorage(bucket_name)
        test_file = io.BytesIO(b"This is a test file for Supabase storage.")
        test_file.name = "test.txt"
        
        # Upload the file
        path = storage._save("test.txt", test_file)
        print(f"✓ File uploaded successfully to {path}")
        
        # Get the URL
        url = storage.url(path)
        print(f"✓ File URL: {url}")
        
        # Clean up
        print("Cleaning up test file...")
        storage.delete(path)
        print("✓ Test file deleted!")
        
    except Exception as e:
        print(f"✗ Error testing file storage: {e}")
        return
    
    print("\n✅ Supabase storage is properly configured!")
    print("You can now use Supabase to store document files.")

if __name__ == "__main__":
    main() 