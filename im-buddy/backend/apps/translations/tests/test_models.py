from django.test import TestCase, override_settings
from apps.translations.models import DocumentTranslation
from apps.visa_info.models import Language
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
import tempfile
import os

# Use Django's default file storage for tests
@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class DocumentTranslationModelTest(TestCase):
    """Test case for DocumentTranslation model"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        # Create a user
        test_user = User.objects.create_user(username='testuser', password='12345')
        
        # Create language objects
        english = Language.objects.create(code='en', name='English')
        spanish = Language.objects.create(code='es', name='Spanish')
        
        # Create a sample PDF file
        sample_pdf = SimpleUploadedFile(
            "test_document.pdf", 
            b"file_content", 
            content_type="application/pdf"
        )
        
        # Create a document translation
        DocumentTranslation.objects.create(
            user=test_user,
            original_document=sample_pdf,
            original_text="Hello world",
            translated_text="Hola mundo",
            source_language=english,
            target_language=spanish,
            file_name="test_document.pdf",
            status="completed"
        )
    
    def test_document_translation_creation(self):
        """Test that a document translation can be created"""
        translation = DocumentTranslation.objects.get(id=1)
        self.assertEqual(translation.original_text, "Hello world")
        self.assertEqual(translation.translated_text, "Hola mundo")
        self.assertEqual(translation.source_language.code, "en")
        self.assertEqual(translation.target_language.code, "es")
        self.assertEqual(translation.file_name, "test_document.pdf")
        self.assertEqual(translation.status, "completed")
        
    def test_user_relationship(self):
        """Test that a document translation is related to a user"""
        translation = DocumentTranslation.objects.get(id=1)
        self.assertEqual(translation.user.username, "testuser") 