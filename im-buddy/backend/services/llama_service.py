import requests
from .llama_common import make_api_request

# API endpoint URL
LLAMA_TRANSLATE_URL = "https://api.llama.com/v1/translate"

def translate_text(text, source_language, target_language):
    """
    Translate text using the LLaMa API
    
    Args:
        text (str): Text to translate
        source_language (str): Source language code
        target_language (str): Target language code
        
    Returns:
        str: Translated text
    """
    data = {
        "text": text,
        "source_language": source_language,
        "target_language": target_language
    }
    
    try:
        result = make_api_request(LLAMA_TRANSLATE_URL, data)
        return result.get("translated_text", "")
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLaMa API: {e}")
        return f"Translation error: {str(e)}" 