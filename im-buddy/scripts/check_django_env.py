"""
Check if Django environment is properly configured
"""
import os
import sys

def check_env_variables():
    """Check if required environment variables are set"""
    required_vars = [
        "DJANGO_SECRET_KEY",
        "DEBUG",
        "ALLOWED_HOSTS"
    ]
    
    print("Checking Django environment variables...")
    
    # Try to load from .env file
    try:
        from dotenv import load_dotenv
        print("Loading .env file from backend directory...")
        load_dotenv("backend/.env")
    except ImportError:
        print("Warning: python-dotenv is not installed. Will check environment variables directly.")
    
    # Check if variables are set
    missing = []
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            status = "✓"
        else:
            status = "✗"
            missing.append(var)
        
        print(f"{status} {var}: {'Set' if value else 'Not set'}")
    
    if missing:
        print("\nMissing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        
        print("\nPlease create or update your backend/.env file with these variables.")
        print("Example values:")
        print('DJANGO_SECRET_KEY="django-insecure-your-secret-key-for-development"')
        print('DEBUG=True')
        print('ALLOWED_HOSTS=localhost,127.0.0.1')
        
        return False
    
    return True

if __name__ == "__main__":
    if check_env_variables():
        print("\nAll required Django environment variables are set!")
        print("You should be able to run the Django server.")
    else:
        print("\nFailed: Missing required environment variables.")
        print("Please fix the issues above and try again.") 