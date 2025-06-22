"""
Simple script to test Supabase connection
"""

import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'im_buddy.settings')
django.setup()

from services.supabase_client import get_client

def main():
    """Test Supabase connection"""
    print("=" * 60)
    print("Supabase Connection Test")
    print("=" * 60)
    
    # Check if environment variables are set
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    print(f"SUPABASE_URL: {'Set' if supabase_url else 'Not Set'}")
    print(f"SUPABASE_ANON_KEY: {'Set' if supabase_key else 'Not Set'}")
    
    if not supabase_url or not supabase_key:
        print("\nError: Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file")
        return
    
    # Test connection to Supabase
    print("\nTesting connection to Supabase...")
    try:
        client = get_client()
        # A simple query to check the connection
        response = client.table('health_check').select('*').limit(1).execute()
        print(f"✓ Successfully connected to Supabase!")
        print(f"\nResponse: {response}")
    except Exception as e:
        print(f"✗ Error connecting to Supabase: {e}")

if __name__ == "__main__":
    main() 