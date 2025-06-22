import httpx
import json
from typing import List, Dict, Any
import os
import logging
from llama_api_client import LlamaAPIClient
from dotenv import load_dotenv
from prompt import ImmigrationFormPrompts

# Set up logging
logger = logging.getLogger(__name__)

load_dotenv()

class LlamaClient:
    def __init__(self):
        self.api_key = os.getenv("LLAMA_API_KEY")
        if not self.api_key:
            logger.error("LLAMA_API_KEY not found in environment variables")
            raise ValueError("LLAMA_API_KEY environment variable is required")
        
        logger.info("Initializing LlamaClient with API key")
        self.client = LlamaAPIClient(api_key=self.api_key)
    
    def translate_pdf_content(
        self, 
        pdf_content: str, 
        form_fields: List[Dict[str, Any]], 
        form_metadata: Dict[str, Any],
        target_language: str,
        source_language: str
    ) -> Dict[str, Any]:
        logger.info(f"Starting translation from {source_language} to {target_language}")
        logger.info(f"Content length: {len(pdf_content)} characters")
        logger.info(f"Number of form fields: {len(form_fields)}")
        
        prompt = self._build_translation_prompt(pdf_content, form_fields, form_metadata, target_language, source_language)
        logger.info(f"Generated prompt length: {len(prompt)} characters")
        
        try:
            logger.info("Making API request to Llama model...")
            response = self.client.chat.completions.create(
                    model="Llama-4-Maverick-17B-128E-Instruct-FP8", 
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert immigration form translator. Translate the following form content to the user's language."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    temperature=0.1,
                )
            
            translated_text = response.completion_message.content.text
            logger.info(f"Successfully received translation. Length: {len(translated_text)} characters")
            
            return {
                "translated_text": translated_text
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            raise Exception(f"Llama API error: {str(e)}")
    
    def _build_translation_prompt(self, pdf_content: str, form_fields: List[Dict[str, Any]], form_metadata: Dict[str, Any], target_language: str, source_language: str) -> str:
        logger.debug("Building translation prompt")
        try:
            prompt = ImmigrationFormPrompts.phase1_translation_prompt(pdf_content, form_fields, form_metadata, target_language, source_language)
            logger.debug(f"Successfully built prompt of length {len(prompt)}")
            return prompt
        except Exception as e:
            logger.error(f"Error building prompt: {str(e)}")
            raise
