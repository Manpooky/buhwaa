import os
import sys

# Add the backend directory to the path so we can import the services
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from backend.services.llama_service import translate_text
    from backend.services.tips_service import generate_tips
    
    # Test the translation service
    print("-" * 50)
    print("Testing LLaMa Translation API")
    print("-" * 50)
    
    translation_result = translate_text(
        text="Hello, how are you? I need help with my visa application.",
        source_language="en",
        target_language="es"
    )
    
    print(f"Original: Hello, how are you? I need help with my visa application.")
    print(f"Translated to Spanish: {translation_result}")
    print("\n")
    
    # Test the tips generation service
    print("-" * 50)
    print("Testing LLaMa Tips Generation API")
    print("-" * 50)
    
    tips_result = generate_tips(
        visa_type="B2",
        language="en"
    )
    
    print("Generated Tips for B2 visa:")
    print(tips_result)
    
except ImportError as e:
    print(f"Error importing LLaMa services: {e}")
    print("Make sure you're running this script from the project root directory.")
    
except Exception as e:
    print(f"Error during API test: {e}")
    print("Check that your API key is properly set in the .env file.") 