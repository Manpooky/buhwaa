import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

# Meta's official Llama API endpoint
BASE_URL = "https://llama-api.meta.com/v1"

def get_headers():
    """
    Get common headers for Meta's Llama API requests
    
    Returns:
        dict: Headers with auth and content-type
    """
    if not LLAMA_API_KEY:
        raise ValueError("LLAMA_API_KEY environment variable not set")
    
    # For Meta's Llama API
    return {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }
    
def make_api_request(url, data):
    """
    Make a request to the Llama API
    
    Args:
        url (str): API endpoint URL
        data (dict): Request payload
        
    Returns:
        dict: API response as JSON
        
    Raises:
        requests.exceptions.RequestException: If API call fails
    """
    headers = get_headers()
    
    # Print debug info
    print(f"Making API request to: {url}")
    print(f"Headers: Authorization: Bearer {LLAMA_API_KEY[:5]}...{LLAMA_API_KEY[-4:]}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.json() 