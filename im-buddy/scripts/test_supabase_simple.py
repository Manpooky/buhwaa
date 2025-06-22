import os
import sys
import json
import requests

def main():
    """
    Simple Supabase connection test
    """
    print("=" * 60)
    print("Supabase Connection Test")
    print("=" * 60)
    
    # Get Supabase credentials from environment or prompt user
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")
    
    if not supabase_url:
        supabase_url = input("Enter your Supabase URL: ")
    
    if not supabase_key:
        supabase_key = input("Enter your Supabase anon key: ")
    
    print(f"Testing connection to: {supabase_url}")
    
    # Test connection using REST API
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
            buckets = response.json()
            print(f"\nStorage buckets: {json.dumps(buckets, indent=2)}")
            
            # Check if 'documents' bucket exists
            docs_bucket = next((b for b in buckets if b['name'] == 'documents'), None)
            if docs_bucket:
                print("\n✓ 'documents' bucket exists!")
            else:
                print("\n✗ 'documents' bucket does not exist.")
                create = input("Would you like to create the 'documents' bucket? (y/n): ")
                if create.lower() == 'y':
                    # Create the documents bucket
                    create_url = f"{supabase_url}/storage/v1/bucket"
                    create_data = {"name": "documents", "public": False}
                    create_response = requests.post(create_url, headers=headers, json=create_data)
                    if create_response.status_code in (200, 201):
                        print("✓ Successfully created 'documents' bucket!")
                    else:
                        print(f"✗ Failed to create bucket: {create_response.text}")
                
            return True
        else:
            print(f"✗ Connection failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error connecting to Supabase: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n" + "=" * 60)
        print("Supabase connection is working correctly!")
        print("Your PDF translation feature should work properly with Supabase storage.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Supabase connection test failed.")
        print("Please check your credentials and make sure Supabase is properly set up.")
        print("=" * 60) 