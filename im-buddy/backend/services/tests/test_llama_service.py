import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from services.llama_service import translate_text


class LlamaServiceTest(TestCase):
    """Test case for Llama service"""
    
    @patch('services.llama_service.make_api_request')
    def test_translate_text(self, mock_api_request):
        """Test translating text"""
        # Mock the API response
        mock_api_request.return_value = {
            "response": "Hola mundo"
        }
        
        # Call the function
        result = translate_text(
            text="Hello world",
            source_language="en",
            target_language="es"
        )
        
        # Assert the result
        self.assertEqual(result, "Hola mundo")
        
        # Verify the API was called with the correct parameters
        mock_api_request.assert_called_once()
        args, kwargs = mock_api_request.call_args
        self.assertIn("messages", args[1])
        self.assertIn("stream", args[1])
        self.assertIn("model", args[1])
    
    @patch('services.llama_service.make_api_request')
    def test_translate_text_with_choices(self, mock_api_request):
        """Test translating text with choices format"""
        # Mock the API response in OpenAI format
        mock_api_request.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Hola mundo"
                    }
                }
            ]
        }
        
        # Call the function
        result = translate_text(
            text="Hello world",
            source_language="en",
            target_language="es"
        )
        
        # Assert the result
        self.assertEqual(result, "Hola mundo") 