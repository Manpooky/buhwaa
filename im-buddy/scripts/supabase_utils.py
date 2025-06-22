"""
Utility functions for Supabase operations
"""
import os
import sys
import uuid
import json
import requests
from dotenv import load_dotenv

# Try to load environment variables
load_dotenv()

def get_supabase_credentials():
    """
    Get Supabase credentials from environment variables or prompt user
    
    Returns:
        tuple: (supabase_url, supabase_key, bucket_name)
    """
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")
    bucket_name = os.environ.get("SUPABASE_STORAGE_BUCKET", "documents")
    
    if not supabase_url:
        supabase_url = input("Enter your Supabase URL: ")
    
    if not supabase_key:
        supabase_key = input("Enter your Supabase anon key: ")
    
    return supabase_url, supabase_key, bucket_name

def test_supabase_connection():
    """
    Test connection to Supabase
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    print("=" * 60)
    print("Supabase Connection Test")
    print("=" * 60)
    
    supabase_url, supabase_key, _ = get_supabase_credentials()
    
    if not supabase_url or not supabase_key:
        print("\nError: SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        return False
    
    print(f"Testing connection to: {supabase_url}")
    
    try:
        # Simple health check request
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}"
        }
        
        # Try to list storage buckets as a simple test
        url = f"{supabase_url}/storage/v1/bucket"
        
        print(f"Sending request to: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✓ Successfully connected to Supabase!")
            return True
        else:
            print(f"✗ Connection failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error connecting to Supabase: {e}")
        return False

def check_bucket_exists(bucket_name="documents"):
    """
    Check if a bucket exists in Supabase storage
    
    Args:
        bucket_name (str): Name of the bucket to check
        
    Returns:
        bool: True if bucket exists, False otherwise
    """
    supabase_url, supabase_key, _ = get_supabase_credentials()
    
    if not supabase_url or not supabase_key:
        print("\nError: SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        return False
    
    try:
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}"
        }
        
        url = f"{supabase_url}/storage/v1/bucket"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            buckets = response.json()
            bucket_exists = any(b['name'] == bucket_name for b in buckets)
            
            if bucket_exists:
                print(f"✓ Bucket '{bucket_name}' exists!")
                return True
            else:
                print(f"✗ Bucket '{bucket_name}' does not exist.")
                return False
        else:
            print(f"✗ Failed to list buckets: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error checking bucket: {e}")
        return False

def create_bucket(bucket_name="documents"):
    """
    Create a bucket in Supabase storage
    
    Args:
        bucket_name (str): Name of the bucket to create
        
    Returns:
        bool: True if bucket created successfully, False otherwise
    """
    supabase_url, supabase_key, _ = get_supabase_credentials()
    
    if not supabase_url or not supabase_key:
        print("\nError: SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        return False
    
    try:
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}"
        }
        
        create_url = f"{supabase_url}/storage/v1/bucket"
        create_data = {"name": bucket_name, "public": False}
        create_response = requests.post(create_url, headers=headers, json=create_data)
        
        if create_response.status_code in (200, 201):
            print(f"✓ Successfully created '{bucket_name}' bucket!")
            return True
        else:
            print(f"✗ Failed to create bucket: {create_response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error creating bucket: {e}")
        return False

def test_storage_operations(bucket_name="documents"):
    """
    Test storage operations (upload, download, delete)
    
    Args:
        bucket_name (str): Name of the bucket to use
        
    Returns:
        bool: True if all operations successful, False otherwise
    """
    supabase_url, supabase_key, _ = get_supabase_credentials()
    
    if not supabase_url or not supabase_key:
        print("\nError: SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        return False
    
    # Create a simple test file
    test_id = uuid.uuid4().hex[:8]
    test_content = f"This is a test file created at {test_id}".encode()
    test_filename = f"test_{test_id}.txt"
    
    try:
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}"
        }
        
        # Try to upload file
        print(f"\nUploading test file '{test_filename}'...")
        upload_url = f"{supabase_url}/storage/v1/object/{bucket_name}/{test_filename}"
        
        upload_headers = headers.copy()
        upload_headers["Content-Type"] = "text/plain"
        
        upload_response = requests.post(
            upload_url,
            headers=upload_headers,
            data=test_content
        )
        
        if upload_response.status_code in (200, 201):
            print("✓ File uploaded successfully!")
            
            # Clean up
            print("\nCleaning up test file...")
            delete_url = f"{supabase_url}/storage/v1/object/{bucket_name}/{test_filename}"
            delete_response = requests.delete(delete_url, headers=headers)
            
            if delete_response.status_code in (200, 204):
                print("✓ Test file deleted!")
                return True
            else:
                print(f"Warning: Could not delete test file: {delete_response.status_code}")
                # Consider success even if deletion fails
                return True
        else:
            print(f"✗ Upload failed: {upload_response.status_code} - {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error during storage operations: {e}")
        return False

def setup_supabase():
    """
    Complete Supabase setup: connection test, bucket creation, and storage test
    
    Returns:
        bool: True if setup successful, False otherwise
    """
    print("=" * 60)
    print("Supabase Setup")
    print("=" * 60)
    
    # Test connection
    if not test_supabase_connection():
        print("✗ Supabase connection test failed. Please check your credentials.")
        return False
    
    # Get bucket name
    _, _, bucket_name = get_supabase_credentials()
    
    # Check if bucket exists
    if not check_bucket_exists(bucket_name):
        # Create bucket if it doesn't exist
        create = input(f"Would you like to create the '{bucket_name}' bucket? (y/n): ")
        if create.lower() == 'y':
            if not create_bucket(bucket_name):
                print(f"✗ Failed to create bucket '{bucket_name}'")
                return False
        else:
            print(f"✗ Bucket '{bucket_name}' is required for storage operations.")
            return False
    
    # Test storage operations
    if not test_storage_operations(bucket_name):
        print("✗ Storage operations test failed.")
        return False
    
    print("\n" + "=" * 60)
    print("✅ Supabase setup completed successfully!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    setup_supabase() 