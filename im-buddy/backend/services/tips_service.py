import requests
from .llama_common import make_api_request

# API endpoint URL
LLAMA_CHAT_URL = "https://api.llama.com/v1/chat/completions"

def generate_tips(visa_type, language):
    """
    Generate smart tips for completing visa applications using LLaMa API
    
    Args:
        visa_type (str): Visa type code
        language (str): Language code for the tips
        
    Returns:
        str: Generated tips content
    """
    # Craft a prompt to generate visa tips
    prompt = f"""
    Generate helpful tips for filling out a {visa_type} visa application.
    The tips should be clear, practical and address common mistakes.
    Please provide the tips in {language} language.
    Format the tips in a structured way with categories.
    """
    
    data = {
        "model": "llama-3",
        "messages": [
            {"role": "system", "content": "You are a helpful visa application assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        result = make_api_request(LLAMA_CHAT_URL, data)
        return result.get("choices", [{}])[0].get("message", {}).get("content", "No tips generated")
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLaMa API: {e}")
        return f"Tips generation error: {str(e)}" 