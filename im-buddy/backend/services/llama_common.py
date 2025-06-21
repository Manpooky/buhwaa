import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

def get_headers():
    """
    Get common headers for LLaMa API requests
    
    Returns:
        dict: Headers with auth and content-type
    """
    if not LLAMA_API_KEY:
        raise ValueError("LLAMA_API_KEY environment variable not set")
        
    return {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }
    
def make_api_request(url, data):
    """
    Make a request to the LLaMa API
    
    Args:
        url (str): API endpoint URL
        data (dict): Request payload
        
    Returns:
        dict: API response as JSON
        
    Raises:
        requests.exceptions.RequestException: If API call fails
    """
    headers = get_headers()
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.json() 